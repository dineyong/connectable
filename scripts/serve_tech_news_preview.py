"""Local RSS preview with a 15-minute background refresh and ignored runtime cache.

No deployment/scheduler is configured. Closing this process stops refreshing.
The committed cache is read-only; publisher failures keep each prior source.
"""
import argparse
import json
import sys
import threading
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.serve_mockup import Handler, ROOT as WEB
from scripts.tech_news import CACHE, ROOT, asset, refresh, validate

RUNTIME=ROOT/'data/news/.runtime-tech-news.json'


class NewsState:
    def __init__(self):
        self.lock=threading.Lock()
        self.data=validate(json.loads(CACHE.read_text()))
        if RUNTIME.exists():
            try:self.data=validate(json.loads(RUNTIME.read_text()))
            except (ValueError,OSError):pass

    def update(self,fetcher=None):
        with self.lock:old=self.data
        result=refresh(old,**({'fetcher':fetcher} if fetcher else {}))
        temp=RUNTIME.with_suffix('.tmp');temp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');temp.replace(RUNTIME)
        with self.lock:self.data=result

    def encoded(self):
        with self.lock:return asset(self.data).encode()


class NewsHandler(Handler):
    def do_GET(self):
        if urlsplit(self.path).path=='/tech-news-data.js':
            result=self.server.news_state.encoded()
            self.send_response(200);self.send_header('Content-Type','application/javascript; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(result)));self.end_headers();self.wfile.write(result)
        else:super().do_GET()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port',type=int,default=8875)
    args=p.parse_args()
    state=NewsState();stop=threading.Event()
    def updater():
        # Preserve the checked initial cache; next scheduled check is in 15 min.
        while not stop.wait(900):
            try:state.update()
            except (ValueError,OSError) as e:print('news update failed:',type(e).__name__,flush=True)
    server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(NewsHandler,directory=str(WEB)))
    server.news_state=state
    threading.Thread(target=updater,daemon=True).start()
    print(f'local auto-refresh news: http://127.0.0.1:{args.port}/tech-news.html',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:stop.set();server.server_close()


if __name__=='__main__':main()

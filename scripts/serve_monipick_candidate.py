"""Loopback-only smoke server for public-format artifacts, not a Cloudflare emulator.

Checks the project's static paths, headers and redirects. CDN, TLS, Access and
Cloudflare caching/host behavior still require real deployment verification.
"""
import argparse
from fnmatch import fnmatchcase
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import tempfile
from urllib.parse import unquote, urlsplit

from scripts.build_monipick_public_candidate import build_candidate, validate_candidate


def read_headers(site, path):
    result={}
    matching=False
    for line in (site/'_headers').read_text().splitlines():
        if not line.strip() or line.lstrip().startswith('#'): continue
        if not line[0].isspace():
            matching=not line.startswith('https://') and fnmatchcase(path,line)
        elif matching:
            key, value=line.strip().split(':',1)
            result[key]=result[key]+', '+value.strip() if key in result else value.strip()
    return result


def handler_for(output):
    errors=validate_candidate(output)
    if errors: raise ValueError('; '.join(errors))
    site=(Path(output)/'site').resolve()
    redirects={}
    for line in (site/'_redirects').read_text().splitlines():
        source,target,status=line.split()
        redirects[source]=(target,int(status))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self): self.respond(False)
        def do_HEAD(self): self.respond(True)
        def respond(self, head):
            request=urlsplit(self.path)
            path=unquote(request.path)
            parts=path.split('/')
            unsafe=(not path.startswith('/') or path.startswith('//') or '\\' in path or
                    any(c in path for c in ('\x00','\r','\n')) or any(p in ('.','..') for p in parts))
            if unsafe:
                self.send_error(400);return
            suffix=('?'+request.query) if request.query else ''
            target=site/path.lstrip('/')
            redirect=redirects.get(path)
            if not redirect and path.endswith('/index.html') and target.is_file():
                redirect=(path[:-10],308)
            elif not redirect and path.endswith('.html') and target.is_file():
                redirect=(path[:-5],308)
            elif not redirect and target.is_dir() and not path.endswith('/'):
                redirect=(path+'/',308)
            if redirect:
                self.send_response(redirect[1])
                self.send_header('Location',redirect[0]+suffix)
                self.send_header('Content-Length','0')
                self.end_headers();return
            if path.endswith('/'): target=target/'index.html'
            elif not target.is_file() and target.with_suffix('.html').is_file() and not Path(path).suffix:
                target=target.with_suffix('.html')
            hidden=any(p.startswith('.') or p.startswith('_') for p in parts)
            status=200
            if hidden or not target.is_file() or not target.resolve().is_relative_to(site):
                status,target=404,site/'404.html'
            content=target.read_bytes()
            self.send_response(status)
            types={'.html':'text/html; charset=utf-8','.js':'application/javascript',
                   '.css':'text/css; charset=utf-8','.xml':'application/xml','.txt':'text/plain; charset=utf-8'}
            self.send_header('Content-Type',types.get(target.suffix,'application/octet-stream'))
            self.send_header('Content-Length',str(len(content)))
            for key,value in read_headers(site,path).items(): self.send_header(key,value)
            self.end_headers()
            if not head:self.wfile.write(content)

    return Handler


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=8876)
    parser.add_argument('--output',help='existing validated candidate; otherwise build in a temporary directory')
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='monipick-candidate-') as temporary:
        output=Path(args.output) if args.output else Path(temporary)/'candidate'
        if not args.output:build_candidate(output)
        handler=handler_for(output)
        print(f'LOCAL ONLY: http://127.0.0.1:{args.port}/ — publication unauthorized',flush=True)
        ThreadingHTTPServer(('127.0.0.1',args.port),handler).serve_forever()


if __name__=='__main__': main()

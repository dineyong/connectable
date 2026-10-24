"""Loopback-only proposed content review. Never deploys or changes production."""
import argparse
from http.server import ThreadingHTTPServer
from pathlib import Path
import tempfile
from scripts.prepare_monipick_content_candidate import build_content_candidate, validate_content_candidate
from scripts.serve_monipick_candidate import handler_for


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=8877)
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='monipick-content-review-') as temporary:
        output=Path(temporary)/'candidate'
        build_content_candidate(output)
        server=ThreadingHTTPServer(('127.0.0.1',args.port),handler_for(output,validate_content_candidate))
        print(f'REVIEW ONLY: http://127.0.0.1:{server.server_port}/',flush=True)
        server.serve_forever()


if __name__=='__main__': main()

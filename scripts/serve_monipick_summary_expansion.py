"""Loopback-only proposed content review. Never deploys or changes production."""
import argparse
from http.server import ThreadingHTTPServer
from pathlib import Path
import tempfile
from scripts.prepare_monipick_summary_expansion import build_summary_expansion, validate_summary_expansion
from scripts.serve_monipick_candidate import handler_for


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=8899)
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='monipick-content-review-') as temporary:
        output=Path(temporary)/'candidate'
        build_summary_expansion(output)
        server=ThreadingHTTPServer(('127.0.0.1',args.port),handler_for(output,validate_summary_expansion))
        print(f'REVIEW ONLY: http://127.0.0.1:{server.server_port}/',flush=True)
        server.serve_forever()


if __name__=='__main__': main()

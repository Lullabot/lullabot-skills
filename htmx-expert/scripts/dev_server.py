#!/usr/bin/env python3
"""Serve a dedicated htmx prototype directory on loopback, never production."""
import argparse
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse


class HtmxHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path.startswith('/api/'):
            fragment = b'<div>Response HTML</div>'
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(fragment)))
            self.end_headers()
            self.wfile.write(fragment)
        else:
            super().do_GET()


def create_server(directory: Path, port: int) -> HTTPServer:
    directory = directory.resolve()
    if not directory.is_dir():
        raise ValueError(f'Prototype directory does not exist: {directory}')
    # No public bind option: sharing requires a separately reviewed workflow.
    return HTTPServer(('127.0.0.1', port), partial(HtmxHandler, directory=str(directory)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', required=True, type=Path, help='Dedicated public/synthetic prototype files only; no private files or symlinks')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error('port must be between 1 and 65535')
    try:
        with create_server(args.directory, args.port) as server:
            print(f'Serving {args.directory.resolve()} at http://127.0.0.1:{args.port}; Ctrl+C to stop', flush=True)
            server.serve_forever()
    except (OSError, ValueError) as error:
        parser.exit(1, f'Error: {error}\n')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()

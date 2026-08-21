from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOST = '127.0.0.1'
PORT = 8000


class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)


if __name__ == '__main__':
    server = ThreadingHTTPServer((HOST, PORT), QuietHandler)
    print(f'Serving {ROOT} at http://{HOST}:{PORT}/')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server...')
    finally:
        server.server_close()

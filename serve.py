#!/usr/bin/env python3
"""
slide-studio local save server.
Serves the project directory and accepts POST /save to write edits back to disk.

Usage:
    python serve.py
    Open: http://localhost:8500/presentation.html
"""
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8500
PAPER_DIR = os.path.dirname(os.path.abspath(__file__))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PAPER_DIR, **kwargs)

    def do_POST(self):
        if self.path == '/save':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            filename = self.headers.get('X-Filename', 'presentation.html')
            # Prevent path traversal
            filename = os.path.basename(filename)
            filepath = os.path.join(PAPER_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(body)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'saved')
            print(f'  saved {filename}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Length, X-Filename')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.end_headers()

    def log_message(self, format, *args):
        if args and str(args[1]) not in ('200', '304'):
            super().log_message(format, *args)


print(f'slide-studio -> http://localhost:{PORT}/presentation.html')
print('Ctrl+C to stop\n')
HTTPServer(('localhost', PORT), Handler).serve_forever()

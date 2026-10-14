"""Dev server for the hero prototype.

Serves a directory, wraps page.html in the same doctype skeleton the artifact
host adds, and accepts POST /__save?name=x (a data: URL body) to write frame
captures into <dir>/../captures/x.jpg|png.
"""
import base64
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ROOT = os.path.abspath(sys.argv[1])
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8790
CAPTURES = os.path.join(os.path.dirname(ROOT), "captures")
SKELETON = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
    "</head><body>{}</body></html>"
)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            with open(os.path.join(ROOT, "page.html"), encoding="utf-8") as f:
                body = SKELETON.format(f.read()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        url = urlparse(self.path)
        if url.path != "/__save":
            self.send_error(404)
            return
        name = os.path.basename(parse_qs(url.query).get("name", ["frame"])[0])
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode()
        header, data = raw.split(",", 1)
        ext = "png" if "png" in header else "jpg"
        os.makedirs(CAPTURES, exist_ok=True)
        out = os.path.join(CAPTURES, f"{name}.{ext}")
        with open(out, "wb") as f:
            f.write(base64.b64decode(data))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(out.encode())


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()

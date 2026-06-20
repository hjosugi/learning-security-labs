from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


SECURITY_HEADERS = {
    "content-security-policy": "default-src 'self'",
    "x-content-type-options": "nosniff",
    "referrer-policy": "no-referrer",
}


def security_headers() -> dict[str, str]:
    return dict(SECURITY_HEADERS)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = b"local security header lab\n"
        self.send_response(200)
        self.send_header("content-type", "text/plain")
        for name, value in security_headers().items():
            self.send_header(name, value)
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


def run(port: int = 8091) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.serve_forever()
    return server


if __name__ == "__main__":
    run()

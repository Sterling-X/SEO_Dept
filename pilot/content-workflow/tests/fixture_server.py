#!/usr/bin/env python3
"""Local HTTP server for the research fixtures (tests only).

Serves tests/fixtures/valid-run/research-pages/ on 127.0.0.1 with text/html content types so the
research layer can fetch, bind, and re-verify synthetic authorities without any network access.
Fixture runs point their reserved `.example` URLs at this server through CW_FIXTURE_URL_REWRITE;
cw_research.rewrite_url honours that variable only when run.json says fixture: true.

Usage inside a test:

    with FixtureServer() as server:
        os.environ[FIXTURE_REWRITE_ENV] = server.rewrite_map()
        ...

`rewrite_map(legislature="leg")` lets a test point the legislature prefix at the `leg-changed` tree
to simulate an amended statute, or at a closed port to simulate an unavailable authority.
"""

from __future__ import annotations

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PAGES_ROOT = Path(__file__).resolve().parent / "fixtures" / "valid-run" / "research-pages"
LEGISLATURE_PREFIX = "https://legislature.exampleland.example"
COURTS_PREFIX = "https://courts.exampleland.example"
CLIENT_PREFIX = "https://gomez-nunez-law.example"


class _Handler(BaseHTTPRequestHandler):
    root: Path = PAGES_ROOT

    def log_message(self, *_args) -> None:  # noqa: D401 - silence the default access log
        return

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        rel = path.lstrip("/")
        candidates = [self.root / (rel + "index.html")] if path.endswith("/") else [self.root / (rel + ".html"), self.root / rel / "index.html"]
        for candidate in candidates:
            try:
                resolved = candidate.resolve()
                resolved.relative_to(self.root.resolve())
            except (OSError, ValueError):
                continue
            if resolved.is_file():
                body = resolved.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
        self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"fixture page not found\n")


class FixtureServer:
    def __init__(self, root: Path = PAGES_ROOT) -> None:
        handler = type("FixtureHandler", (_Handler,), {"root": root})
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    @property
    def base_url(self) -> str:
        host, port = self.server.server_address[:2]
        return f"http://{host}:{port}"

    def rewrite_map(self, *, legislature: str | None = "leg", courts: str | None = "courts", client: str | None = "client") -> str:
        """Prefix map for CW_FIXTURE_URL_REWRITE. A None tree points the prefix at a closed port so the
        fetch fails (unavailable-source simulation)."""
        closed = "http://127.0.0.1:9/unavailable"
        pairs = [
            (LEGISLATURE_PREFIX, f"{self.base_url}/{legislature}" if legislature else closed),
            (COURTS_PREFIX, f"{self.base_url}/{courts}" if courts else closed),
            (CLIENT_PREFIX, f"{self.base_url}/{client}" if client else closed),
        ]
        return ";".join(f"{prefix}={target}" for prefix, target in pairs)

    def __enter__(self) -> "FixtureServer":
        self.thread.start()
        return self

    def __exit__(self, *_exc) -> None:
        self.server.shutdown()
        self.server.server_close()

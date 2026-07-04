#!/usr/bin/env python3
"""Local review server: serves the built _site/ + POST /feedback -> .feedback/feedback.jsonl.

Adapted from etchy's demo server (deploy/demo/etchy-server.py). Use together with
the dev-only feedback widget (_includes/feedback_widget.html), which renders when
the site is built with JEKYLL_ENV=development:

    bundle exec jekyll build          # JEKYLL_ENV defaults to development
    python3 scripts/dev-server.py     # http://localhost:4000

Usage:  python3 scripts/dev-server.py [PORT] [ROOT]
Serves ROOT (default: <repo>/_site) on 0.0.0.0:PORT (default 4000).
Feedback lands in .feedback/feedback.jsonl (gitignored — may contain PII).
"""
import base64
import datetime
import json
import os
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
ROOT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(REPO, "_site")
FEEDBACK = os.environ.get("SITE_FEEDBACK") or os.path.join(REPO, ".feedback", "feedback.jsonl")
os.makedirs(os.path.dirname(os.path.abspath(FEEDBACK)), exist_ok=True)
_lock = threading.Lock()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def end_headers(self):
        # Dev server: freshness beats caching after every rebuild.
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def send_head(self):
        # GitHub Pages serves /kitium as kitium.html (permalink /:slug).
        # SimpleHTTPRequestHandler doesn't, so mirror that behaviour here.
        path = self.path.split("?", 1)[0]
        if "." not in os.path.basename(path):
            candidate = os.path.join(ROOT, path.lstrip("/").rstrip("/") + ".html")
            if path not in ("", "/") and os.path.isfile(candidate):
                self.path = path.rstrip("/") + ".html"
        return super().send_head()

    def do_POST(self):
        if self.path.split("?", 1)[0] != "/feedback":
            self.send_error(404)
            return
        try:
            n = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(n) if n > 0 else b"{}"
            data = json.loads(raw.decode("utf-8") or "{}")
            if not isinstance(data, dict):
                data = {"value": data}
        except Exception:
            self.send_error(400, "bad json")
            return

        # Pasted screenshots arrive as data: URLs -> decode to .feedback/screenshots/
        # and log the relative path so the jsonl stays readable.
        def _save_shot(durl, idx):
            header, b64 = durl.split(",", 1)
            ext = "jpg" if "image/jpeg" in header else "webp" if "image/webp" in header else "png"
            sdir = os.path.join(os.path.dirname(os.path.abspath(FEEDBACK)), "screenshots")
            os.makedirs(sdir, exist_ok=True)
            stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S_%f")
            fname = f"{stamp}-{idx}-{self.client_address[0].replace(':', '_')}.{ext}"
            with open(os.path.join(sdir, fname), "wb") as imgf:
                imgf.write(base64.b64decode(b64))
            return os.path.join("screenshots", fname)

        shots = data.get("screenshots")
        if isinstance(shots, list):
            paths = []
            for i, s in enumerate(shots):
                durl = s.get("data") if isinstance(s, dict) else s
                if isinstance(durl, str) and durl.startswith("data:image/"):
                    try:
                        paths.append(_save_shot(durl, i))
                    except Exception:
                        paths.append("(screenshot decode failed)")
            data["screenshots"] = paths
        elif isinstance(data.get("screenshot"), str) and data["screenshot"].startswith("data:image/"):
            try:
                data["screenshot"] = _save_shot(data["screenshot"], 0)
            except Exception:
                data["screenshot"] = "(screenshot decode failed)"

        rec = {
            "ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            "ip": self.client_address[0],
            "ua": self.headers.get("User-Agent", ""),
        }
        rec.update(data)
        try:
            with _lock, open(FEEDBACK, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except Exception as e:
            self.send_error(500, f"write failed: {e}")
            return
        body = b'{"ok":true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass  # quiet


if __name__ == "__main__":
    httpd = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"site dev: serving {ROOT} on 0.0.0.0:{PORT}  (POST /feedback -> {FEEDBACK})")
    httpd.serve_forever()

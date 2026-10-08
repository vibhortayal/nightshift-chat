"""Visitor feedback endpoint — stores thumbs up/down per answer."""
import json
import os
import urllib.request
from http.server import BaseHTTPRequestHandler

KV_URL = os.environ.get("KV_REST_API_URL", "")
KV_TOKEN = os.environ.get("KV_REST_API_TOKEN", "")


def kv_call(*args):
    if not KV_URL or not KV_TOKEN:
        return None
    try:
        body = json.dumps(list(args)).encode()
        req = urllib.request.Request(
            KV_URL,
            data=body,
            headers={"Authorization": f"Bearer {KV_TOKEN}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read()).get("result")
    except Exception:
        return None


class handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "https://vibhortayal.github.io")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "https://vibhortayal.github.io")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length > 2048 or length <= 0:
                self._send(400, {"error": "Invalid request."})
                return
            body = json.loads(self.rfile.read(length))
            vote = body.get("vote", "").strip().lower()
            qhash = body.get("qhash", "").strip()[:64]

            if vote not in ("up", "down") or not qhash:
                self._send(400, {"error": "Need vote (up/down) and qhash."})
                return

            # Store: increment counter, log the vote
            kv_call("HINCRBY", "chat:feedback:counts", f"{qhash}:{vote}", 1)
            kv_call("LPUSH", "chat:feedback:log",
                    json.dumps({"qhash": qhash, "vote": vote}))
            kv_call("LTRIM", "chat:feedback:log", 0, 999)  # keep last 1000

            self._send(200, {"ok": True})
        except Exception as e:
            self._send(500, {"error": "Failed to record feedback."})

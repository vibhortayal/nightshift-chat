"""Admin endpoint: dump recent chatbot question logs.
Password-protected via ADMIN_PASSWORD env var, passed as X-Admin-Password header.
"""
import json
import os
import urllib.request
from http.server import BaseHTTPRequestHandler

KV_URL = os.environ.get("KV_REST_API_URL", "")
KV_TOKEN = os.environ.get("KV_REST_API_TOKEN", "")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")


def kv_call(*args):
    if not KV_URL or not KV_TOKEN:
        return None
    try:
        data = json.dumps(list(args)).encode()
        req = urllib.request.Request(
            KV_URL,
            data=data,
            headers={"Authorization": f"Bearer {KV_TOKEN}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode()).get("result")
    except Exception:
        return None


class handler(BaseHTTPRequestHandler):
    def _send(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        self._handle()

    def do_POST(self):
        self._handle()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Admin-Password, Content-Type")
        self.end_headers()

    def _handle(self):
        password = self.headers.get("X-Admin-Password", "")
        if not ADMIN_PASSWORD or password != ADMIN_PASSWORD:
            self._send(401, {"error": "unauthorized"})
            return

        keys = []
        cursor = 0
        try:
            while True:
                result = kv_call("SCAN", cursor, "MATCH", "chat:log:*", "COUNT", 100)
                if not result:
                    break
                cursor = int(result[0])
                keys.extend(result[1])
                if cursor == 0 or len(keys) >= 500:
                    break
        except Exception as e:
            self._send(500, {"error": f"scan failed: {e}"})
            return

        keys.sort(reverse=True)
        keys = keys[:200]
        logs = []
        for k in keys:
            val = kv_call("GET", k)
            if val:
                try:
                    logs.append(json.loads(val))
                except Exception:
                    pass

        self._send(200, {"count": len(logs), "logs": logs})

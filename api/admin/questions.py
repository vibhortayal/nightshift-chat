"""Admin endpoint: dump recent chatbot question logs.
Password-protected via ADMIN_PASSWORD env var, passed as X-Admin-Password header.
"""
import hashlib
import hmac
import json
import os
import time
import urllib.request
from http.server import BaseHTTPRequestHandler

KV_URL = os.environ.get("KV_REST_API_URL", "")
KV_TOKEN = os.environ.get("KV_REST_API_TOKEN", "")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")

# Admin origin for CORS — same Vercel deployment serves the admin UI
ADMIN_ORIGIN = "https://nightshift-chat-vibhor-t.vercel.app"


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
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        # Restrict CORS to the admin origin (same deployment serves the UI)
        origin = self.headers.get("Origin", "")
        if origin == ADMIN_ORIGIN:
            self.send_header("Access-Control-Allow-Origin", origin)
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _check_auth(self):
        """Constant-time password check with brute-force rate limiting."""
        password = self.headers.get("X-Admin-Password", "")
        if not ADMIN_PASSWORD:
            return False
        # Rate limit failed attempts: 10 per minute per IP
        ip = self.headers.get("X-Forwarded-For", "unknown").split(",")[0].strip()
        iphash = hashlib.md5(ip.encode()).hexdigest()[:12]
        fail_key = f"chat:adminfail:{iphash}"
        fails = kv_call("GET", fail_key)
        if fails and int(fails) >= 10:
            return False
        ok = hmac.compare_digest(password, ADMIN_PASSWORD)
        if not ok:
            kv_call("INCR", fail_key)
            kv_call("EXPIRE", fail_key, 60)
        return ok

    def do_GET(self):
        self._handle()

    def do_POST(self):
        self._handle()

    def do_DELETE(self):
        """Clear all question logs. Password-protected."""
        if not self._check_auth():
            self._send(401, {"error": "unauthorized"})
            return

        deleted = 0
        cursor = 0
        try:
            while True:
                result = kv_call("SCAN", cursor, "MATCH", "chat:log:*", "COUNT", 100)
                if not result:
                    break
                cursor = int(result[0])
                batch = result[1]
                if batch:
                    kv_call("DEL", *batch)
                    deleted += len(batch)
                if cursor == 0:
                    break
        except Exception as e:
            self._send(500, {"error": f"delete failed: {e}", "deleted": deleted})
            return

        self._send(200, {"deleted": deleted})

    def do_POST(self):
        """Reset daily caps. Password-protected."""
        if not self._check_auth():
            self._send(401, {"error": "unauthorized"})
            return

        from datetime import datetime
        from zoneinfo import ZoneInfo
        day = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")

        deleted = 0
        cursor = 0
        try:
            while True:
                result = kv_call("SCAN", cursor, "MATCH", "chat:daily:*", "COUNT", 100)
                if not result:
                    break
                cursor = int(result[0])
                if result[1]:
                    kv_call("DEL", *result[1])
                    deleted += len(result[1])
                if cursor == 0:
                    break
            cursor = 0
            while True:
                result = kv_call("SCAN", cursor, "MATCH", "chat:ipdaily:*", "COUNT", 100)
                if not result:
                    break
                cursor = int(result[0])
                if result[1]:
                    kv_call("DEL", *result[1])
                    deleted += len(result[1])
                if cursor == 0:
                    break
        except Exception as e:
            self._send(500, {"error": f"reset failed: {e}", "deleted": deleted})
            return

        self._send(200, {"deleted": deleted, "day": day})

    def do_PUT(self):
        """Clear all strike counters. Password-protected. One-time use."""
        if not self._check_auth():
            self._send(401, {"error": "unauthorized"})
            return

        deleted = 0
        cursor = 0
        try:
            while True:
                result = kv_call("SCAN", cursor, "MATCH", "chat:strikes:*", "COUNT", 100)
                if not result:
                    break
                cursor = int(result[0])
                if result[1]:
                    kv_call("DEL", *result[1])
                    deleted += len(result[1])
                if cursor == 0:
                    break
        except Exception as e:
            self._send(500, {"error": f"clear failed: {e}", "deleted": deleted})
            return

        self._send(200, {"deleted": deleted})

    def do_OPTIONS(self):
        self.send_response(200)
        origin = self.headers.get("Origin", "")
        if origin == ADMIN_ORIGIN:
            self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Admin-Password, Content-Type")
        self.end_headers()

    def _handle(self):
        if not self._check_auth():
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
                if cursor == 0:
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

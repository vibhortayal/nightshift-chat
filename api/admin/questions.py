"""Admin endpoint: dump recent chatbot question logs.
Password-protected via ADMIN_PASSWORD env var, passed as X-Admin-Password header.
"""
import json
import os
import time
import urllib.request

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


class handler:
    def GET(self, request):
        return self._handle(request)

    def POST(self, request):
        return self._handle(request)

    def _handle(self, request):
        # Auth check
        password = request.headers.get("x-admin-password", "")
        if not ADMIN_PASSWORD or password != ADMIN_PASSWORD:
            return {
                "statusCode": 401,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "unauthorized"}),
            }

        # Scan for log keys (KV SCAN)
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
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": f"scan failed: {e}"}),
            }

        # Fetch values (most recent first by key timestamp)
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

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"count": len(logs), "logs": logs}),
        }

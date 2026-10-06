"""Nightshift chatbot backend — answers questions about the factory using repo docs."""
import json
import os
import urllib.request
from http.server import BaseHTTPRequestHandler

# Docs to pull from the public submission repo
DOCS = [
    "https://raw.githubusercontent.com/vibhortayal/nightshift-pocketful/main/FACTORY.md",
    "https://raw.githubusercontent.com/vibhortayal/nightshift-pocketful/main/README.md",
    "https://raw.githubusercontent.com/vibhortayal/nightshift-pocketful/main/mandates/nightshift-architect.md",
    "https://raw.githubusercontent.com/vibhortayal/nightshift-pocketful/main/mandates/nightshift-implementer.md",
    "https://raw.githubusercontent.com/vibhortayal/nightshift-pocketful/main/mandates/nightshift-verifier.md",
]

# Simple in-memory cache
_doc_cache = None

def get_docs():
    global _doc_cache
    if _doc_cache:
        return _doc_cache
    parts = []
    for url in DOCS:
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                parts.append(f"--- {url.split('/')[-1]} ---\n{r.read().decode('utf-8', errors='ignore')}")
        except Exception:
            pass
    _doc_cache = "\n\n".join(parts)
    return _doc_cache

SYSTEM = """You are a helpful assistant for Team Nightshift's hackathon project page.
Answer questions about the Nightshift factory, the hackathon, how the team built it, and the Pocketful app.
Use ONLY the context provided below. If the answer isn't in the context, say so briefly.
Keep answers concise (2-4 sentences usually). Be friendly and direct."""

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            question = body.get('question', '').strip()
            if not question:
                self._send(400, {"error": "No question provided"})
                return

            docs = get_docs()
            api_key = os.environ.get('GEMINI_API_KEY', '')
            if not api_key:
                self._send(500, {"error": "API key not configured"})
                return

            prompt = f"{SYSTEM}\n\nContext:\n{docs}\n\nQuestion: {question}\nAnswer:"
            
            req_data = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.3, "maxOutputTokens": 500}
            }).encode()
            
            req = urllib.request.Request(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
                data=req_data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                resp = json.loads(r.read())
            
            answer = resp["candidates"][0]["content"]["parts"][0]["text"]
            self._send(200, {"answer": answer.strip()})
        except Exception as e:
            self._send(500, {"error": str(e)[:200]})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _send(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

"""Nightshift chatbot backend — answers questions about the factory using a compressed knowledge file."""
import json
import os
import re
import time
import urllib.request
from http.server import BaseHTTPRequestHandler

# Single compressed knowledge file (~800 tokens) instead of full docs (~16k)
CONTEXT_URL = "https://raw.githubusercontent.com/vibhortayal/nightshift-chat/main/CONTEXT.md"

# Simple in-memory caches (per warm instance)
_context_cache = None
_answer_cache = {}       # normalized question -> answer
_rate_buckets = {}       # ip -> [timestamps]

SYSTEM = """You are Spark, answering questions on Team Nightshift's hackathon project page.
Use ONLY the context below. Keep every answer to 2-3 short lines.
End with one relevant link from the context (repo, submission, or project page) where they can read more.
If the answer isn't in the context, say so in one line and link the repo."""

# Topic gate: only project questions reach the LLM. Saves quota.
TOPIC_KEYWORDS = {
    "nightshift", "factory", "factories", "hackathon", "band", "pocketful",
    "architect", "implementer", "verifier", "seat", "seats", "agent", "agents",
    "claude", "spark", "instinct", "vibhor", "dark", "wearedevelopers", "lablab",
    "mandate", "mandates", "harness", "stage", "stages", "build", "built",
    "code", "coding", "team", "run", "runs", "test", "tests", "spec", "room",
    "tablekeeper", "toy", "docker", "review", "reviewer", "dispatch", "opus",
    "sonnet", "commandment", "block",
}

OFFTOPIC_REPLY = ("I only answer questions about Team Nightshift, the Dark Factory, and the hackathon. "
                  "Try asking about how the factory works, the seats, or the build.")

# Pre-answered FAQs — zero tokens for the most common questions
FAQS = [
    ({"what is the nightshift factory", "what is nightshift", "what is dark factory"},
     "Dark Factory is a three-seat AI software factory on the Band platform: Architect (plans), Implementer (builds), Verifier (checks). One human message starts a run; the seats handle everything after.\nMore: https://github.com/vibhortayal/nightshift-pocketful"),
    ({"who built", "who made", "who created", "team"},
     "Team Nightshift: Vibhor Tayal (human) plus AI agents Spark, Instinct, and Claude — built for the WeAreDevelopers x BAND hackathon.\nMore: https://vibhortayal.github.io/nightshift/"),
    ({"pocketful", "what did it build", "what was built"},
     "Pocketful — a kids' pocket-money/savings app, built through 4 of 4 stages in 2h 27min (Run 7, Oct 2 2026).\nMore: https://github.com/vibhortayal/nightshift-pocketful"),
    ({"how does it work", "how it works", "how do the seats work"},
     "Architect turns the spec into a checklist; Implementer builds one exact version; Verifier tests it independently and gives one PASS/BLOCK verdict. Five BLOCKs stops the run.\nMore: https://github.com/vibhortayal/nightshift-pocketful/blob/main/FACTORY.md"),
    ({"cost", "how much", "tokens"},
     "The submitted run used ~141M tokens (~$59 at list price), covered by a Claude Max subscription — no per-run bill.\nMore: https://github.com/vibhortayal/nightshift-pocketful/blob/main/FACTORY.md"),
]

def get_context():
    global _context_cache
    if _context_cache:
        return _context_cache
    try:
        with urllib.request.urlopen(CONTEXT_URL, timeout=10) as r:
            _context_cache = r.read().decode("utf-8", errors="ignore")
    except Exception:
        _context_cache = ""
    return _context_cache

def normalize(q):
    q = q.lower()
    q = re.sub(r"[^a-z0-9 ]", "", q)
    return re.sub(r"\s+", " ", q).strip()

def check_faq(norm_q):
    for keywords, answer in FAQS:
        if any(k in norm_q for k in keywords):
            return answer
    return None

def rate_limited(ip):
    now = time.time()
    bucket = _rate_buckets.get(ip, [])
    bucket = [t for t in bucket if now - t < 60]
    if len(bucket) >= 15:
        return True
    bucket.append(now)
    _rate_buckets[ip] = bucket
    return False

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            question = body.get("question", "").strip()
            if not question:
                self._send(400, {"error": "No question provided"})
                return

            ip = self.headers.get("X-Forwarded-For", "?").split(",")[0].strip()
            if rate_limited(ip):
                self._send(429, {"error": "Too many questions — wait a minute and try again."})
                return

            norm_q = normalize(question)

            # 1. Answer cache (warm instances)
            if norm_q in _answer_cache:
                self._send(200, {"answer": _answer_cache[norm_q], "cached": True})
                return

            # 2. FAQ pre-answers — zero tokens
            faq = check_faq(norm_q)
            if faq:
                _answer_cache[norm_q] = faq
                self._send(200, {"answer": faq, "cached": True})
                return

            # 3. Topic gate — off-topic never reaches the LLM
            words = set(norm_q.split())
            if not words & TOPIC_KEYWORDS:
                self._send(200, {"answer": OFFTOPIC_REPLY})
                return

            # 4. LLM with compressed context
            api_key = os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                self._send(500, {"error": "API key not configured"})
                return

            prompt = f"{SYSTEM}\n\nContext:\n{get_context()}\n\nQuestion: {question}\nAnswer:"
            req_data = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.3, "maxOutputTokens": 300},
            }).encode()

            req = urllib.request.Request(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}",
                data=req_data,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                resp = json.loads(r.read())

            answer = resp["candidates"][0]["content"]["parts"][0]["text"].strip()
            _answer_cache[norm_q] = answer
            self._send(200, {"answer": answer})
        except Exception as e:
            self._send(500, {"error": str(e)[:200]})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _send(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

"""Smoke-test every API endpoint against the running server."""
import json, sys, os, time, urllib.request, urllib.error

# Fix Windows console encoding
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = "http://127.0.0.1:8000"

def post(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode()
        print(f"  HTTP {e.code}: {detail}")
        return None

def get(path):
    req = urllib.request.Request(BASE + path)
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())

TEXTS = {
    "en": "India is a large and diverse country with many languages.",
    "hi": "भारत कई भाषाओं और संस्कृतियों वाला एक विविध देश है।",
    "mr": "भारत हा अनेक भाषा आणि संस्कृती असलेला विविधतापूर्ण देश आहे."
}

print("=== GET /api/tokenizers ===")
d = get("/api/tokenizers")
print(f"  {len(d)} tokenizers: {[t['name'] for t in d]}")

print("\n=== POST /api/tokenize (all tokenizers, Hindi) ===")
d = post("/api/tokenize", {"text": TEXTS["hi"]})
if d:
    for name, info in d.items():
        print(f"  {name}: {info['count']} tokens")

print("\n=== POST /api/tokenize (BERT vs GPT-4o, Hindi) ===")
d = post("/api/tokenize", {"text": TEXTS["hi"], "tokenizers": ["BERT multilingual (WordPiece)", "GPT-4o / o200k (BPE)"]})
if d:
    for name, info in d.items():
        tokens_repr = [repr(t) for t in info['tokens'][:5]]
        print(f"  {name}: {info['count']} tokens, first 5: {tokens_repr}")

print("\n=== POST /api/probs (English) ===")
d = post("/api/probs", {"text": TEXTS["en"]})
if d:
    print(f"  {len(d['tokens'])} tokens, perplexity={d['perplexity']:.1f}")
    for t in d["tokens"][:5]:
        print(f"    '{t['token']}' p={t['prob']:.4f} top_guess='{t['top_guess']}'")

print("\n=== POST /api/probs (Hindi) ===")
d = post("/api/probs", {"text": TEXTS["hi"]})
if d:
    print(f"  {len(d['tokens'])} tokens, perplexity={d['perplexity']:.1f}")
    for t in d["tokens"][:3]:
        print(f"    '{t['token']}' p={t['prob']:.6f}")

print("\n=== POST /api/stats ===")
d = post("/api/stats", {"texts": TEXTS})
if d:
    for r in d:
        print(f"  {r['tokenizer']:35s} {r['language']:8s} {r['tokens']:4d} tokens  fertility={r['fertility']:.2f}  x_en={r['cost_multiplier']}")

print("\n=== POST /api/stats (GPT only) ===")
d = post("/api/stats", {"texts": TEXTS, "tokenizers": ["GPT-2 (BPE)", "GPT-4 / cl100k (BPE)", "GPT-4o / o200k (BPE)"]})
if d:
    for r in d:
        print(f"  {r['tokenizer']:25s} {r['language']:8s} {r['tokens']:4d} tokens  x_en={r['cost_multiplier']}  context%={r['effective_context_pct']}")

print("\n=== POST /api/explain (u2 - expects 503 without GROQ_API_KEY) ===")
d = post("/api/explain", {"kind": "u2", "texts": TEXTS, "lang": "hi"})
if d:
    print(f"  LLM response length: {len(d['text'])} chars")

print("\n=== Validation: empty text ===")
d = post("/api/probs", {"text": ""})

print("\n=== Validation: unknown tokenizer ===")
d = post("/api/tokenize", {"text": "hello", "tokenizers": ["nonexistent"]})

print("\n=== GET / (index.html) ===")
try:
    req = urllib.request.Request(BASE + "/")
    resp = urllib.request.urlopen(req, timeout=10)
    html = resp.read().decode()
    print(f"  Status: {resp.status}, length: {len(html)} bytes")
    assert "Tokenizer Explorer" in html, "Title not found in HTML!"
    print("  HTML contains expected title.")
except Exception as e:
    print(f"  ERROR: {e}")

print("\nAll smoke tests done!")

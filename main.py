import math
import os
from typing import Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

import tiktoken
import torch
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel, field_validator
from transformers import AutoModelForCausalLM, AutoTokenizer

app = FastAPI(title="Tokenizer Explorer for Indian Languages")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

MAX_TEXT_LEN = 5000  # guard against very long inputs

TOKENIZERS = {
    "GPT-2 (BPE)": ("hf", "gpt2", "BPE"),
    "GPT-4 / cl100k (BPE)": ("tt", "cl100k_base", "BPE"),
    "GPT-4o / o200k (BPE)": ("tt", "o200k_base", "BPE"),
    "BERT-base English (WordPiece)": ("hf", "bert-base-uncased", "WordPiece"),
    "BERT multilingual (WordPiece)": ("hf", "bert-base-multilingual-cased", "WordPiece"),
    "XLM-R (SentencePiece)": ("hf", "xlm-roberta-base", "SentencePiece"),
    "MuRIL Indic (WordPiece)": ("hf", "google/muril-base-cased", "WordPiece"),
}
GPT_ONLY = ["GPT-2 (BPE)", "GPT-4 / cl100k (BPE)", "GPT-4o / o200k (BPE)"]
LANG_NAMES = {"en": "English", "hi": "Hindi", "mr": "Marathi"}

_tok_cache, _lm = {}, {}


def get_tok(name):
    if name not in TOKENIZERS:
        raise HTTPException(400, f"Unknown tokenizer {name}")
    if name not in _tok_cache:
        kind, ident, _ = TOKENIZERS[name]
        _tok_cache[name] = tiktoken.get_encoding(ident) if kind == "tt" else AutoTokenizer.from_pretrained(ident)
    return _tok_cache[name]


def tokenize(name, text):
    tok = get_tok(name)
    kind = TOKENIZERS[name][0]
    if kind == "tt":
        out = []
        for i in tok.encode(text):
            b = tok.decode_single_token_bytes(i)
            try:
                out.append(b.decode("utf-8"))
            except UnicodeDecodeError:
                out.append("<0x" + b.hex().upper() + ">")  # partial UTF-8 byte fragment
        return out
    return tok.tokenize(text)


def stats_rows(texts: Dict[str, str], names: List[str], price: float):
    rows = []
    for name in names:
        per_lang = {}
        for code, text in texts.items():
            if not text.strip():
                continue
            toks = tokenize(name, text)
            words = max(len(text.split()), 1)
            per_lang[code] = {
                "tokenizer": name,
                "family": TOKENIZERS[name][2],
                "language": LANG_NAMES.get(code, code),
                "code": code,
                "tokens": len(toks),
                "words": words,
                "fertility": round(len(toks) / words, 2),
                "chars_per_token": round(len(text) / len(toks), 2),
                "bytes_per_token": round(len(text.encode("utf-8")) / len(toks), 2),
                "cost_per_1k_texts": round(len(toks) * 1000 / 1e6 * price, 4),
            }
        base = per_lang.get("en", {}).get("tokens")
        for r in per_lang.values():
            r["cost_multiplier"] = round(r["tokens"] / base, 2) if base else None
            r["effective_context_pct"] = round(100 * base / r["tokens"]) if base else None
            rows.append(r)
    return rows


def load_lm():
    if not _lm:
        _lm["tok"] = AutoTokenizer.from_pretrained("gpt2")
        _lm["model"] = AutoModelForCausalLM.from_pretrained("gpt2").eval()
    return _lm["tok"], _lm["model"]


def llm(prompt: str) -> str:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise HTTPException(503, "GROQ_API_KEY is not set on the server")
    c = OpenAI(api_key=key, base_url=os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1"))
    model_name = os.getenv("CHAT_MODEL", "openai/gpt-oss-120b")
    try:
        r = c.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an NLP teaching assistant. Be precise and concise."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        return r.choices[0].message.content
    except Exception as e:
        raise HTTPException(502, f"Groq LLM call failed: {str(e)}")


# ------------------------------- API ----------------------------------------
def _check_text(v: str) -> str:
    v = v.strip()
    if not v:
        raise ValueError("Text must not be empty")
    if len(v) > MAX_TEXT_LEN:
        raise ValueError(f"Text too long ({len(v)} chars, max {MAX_TEXT_LEN})")
    return v


class TokReq(BaseModel):
    text: str
    tokenizers: Optional[List[str]] = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, v):
        return _check_text(v)


class TextReq(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, v):
        return _check_text(v)


class StatsReq(BaseModel):
    texts: Dict[str, str]
    tokenizers: Optional[List[str]] = None
    price: float = 2.5


class ExplainReq(BaseModel):
    kind: str  # "u2" or "u5"
    texts: Dict[str, str]
    lang: str = "hi"
    price: float = 2.5


@app.get("/api/tokenizers")
def list_tokenizers():
    return [{"name": n, "family": v[2]} for n, v in TOKENIZERS.items()]


@app.post("/api/tokenize")  # U2, U3
def api_tokenize(req: TokReq):
    out = {}
    for n in req.tokenizers or list(TOKENIZERS):
        toks = tokenize(n, req.text)
        out[n] = {"family": TOKENIZERS[n][2], "tokens": toks, "count": len(toks)}
    return out


@app.post("/api/probs")  # U1
def api_probs(req: TextReq):
    tok, model = load_lm()
    ids = tok(req.text, return_tensors="pt").input_ids
    inp = torch.cat([torch.tensor([[tok.eos_token_id]]), ids], dim=1)  # <|endoftext|> as BOS
    with torch.no_grad():
        logits = model(inp).logits[0, :-1]
    probs = logits.softmax(-1)
    p = probs[torch.arange(ids.shape[1]), ids[0]]
    top = probs.argmax(-1)
    rows = [
        {
            "token": tok.convert_ids_to_tokens(int(ids[0, i])),
            "prob": float(p[i]),
            "top_guess": tok.decode([int(top[i])]),
        }
        for i in range(ids.shape[1])
    ]
    ppl = math.exp(-sum(math.log(max(r["prob"], 1e-12)) for r in rows) / len(rows))
    return {"tokens": rows, "perplexity": ppl}


@app.post("/api/stats")  # U4, U5
def api_stats(req: StatsReq):
    return stats_rows(req.texts, req.tokenizers or list(TOKENIZERS), req.price)


@app.post("/api/explain")  # U2 + U5 LLM
def api_explain(req: ExplainReq):
    if req.kind == "u2":
        text = req.texts.get(req.lang, "")
        picks = ["GPT-4 / cl100k (BPE)", "BERT multilingual (WordPiece)", "XLM-R (SentencePiece)"]
        lines = [f"{TOKENIZERS[n][2]} ({n}): {tokenize(n, text)}" for n in picks]
        prompt = (
            f"Three tokenisers split this {LANG_NAMES[req.lang]} text: '{text}'\n\n" + "\n".join(lines) +
            "\n\nExplain (1) how BPE, WordPiece and SentencePiece differ in training objective and splitting "
            "(merge rule, likelihood scoring, ## prefix, ▁ marker, byte-level fallback) and (2) why the splits "
            "above look the way they do for this language."
        )
    elif req.kind == "u5":
        rows = stats_rows(req.texts, GPT_ONLY, req.price)
        table = "\n".join(f"{r['tokenizer']} | {r['language']} | {r['tokens']} tokens | x{r['cost_multiplier']}" for r in rows)
        prompt = (
            "Token counts for the same sentence in English, Hindi and Marathi:\n" + table +
            "\n\nDiscuss the cost unfairness for Indian-language users: API price, shrinking context window, "
            "latency, quality. Explain causes (training-corpus imbalance, byte-level BPE on 3-byte Devanagari "
            "characters, vocabulary size) and realistic mitigations (larger multilingual vocabularies, "
            "Indic tokenisers, vocabulary extension and fine-tuning, per-character pricing)."
        )
    else:
        raise HTTPException(400, "kind must be u2 or u5")
    return {"text": llm(prompt)}


@app.post("/api/transcribe")  # U3 Whisper
async def api_transcribe(audio: UploadFile = File(...), lang: str = Form("hi")):
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise HTTPException(503, "GROQ_API_KEY is not set on the server")
    data = await audio.read()
    if not data:
        raise HTTPException(400, "Audio data is empty")
    fname = audio.filename or "speech.webm"
    ext = os.path.splitext(fname)[1].lower()
    valid_exts = {".flac", ".mp3", ".mp4", ".mpeg", ".mpga", ".m4a", ".ogg", ".wav", ".webm"}
    if ext not in valid_exts:
        fname = "speech.webm"
    c = OpenAI(api_key=key, base_url=os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1"))
    try:
        r = c.audio.transcriptions.create(
            file=(fname, data),
            model=os.getenv("WHISPER_MODEL", "whisper-large-v3"),
            language=lang,
        )
        return {"text": r.text}
    except Exception as e:
        raise HTTPException(502, f"Groq Whisper transcription failed: {str(e)}")


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")

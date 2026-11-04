# Tokenizer Explorer for Indian Languages

A web application that demonstrates how different tokenizers split **English, Hindi and Marathi** text, and what that costs users in tokens, money, and context window. Built for a Generative AI course assignment covering Units 1–5.

## Features

| Tab | Feature |
|-----|---------|
| **U1** | Per-token probability under GPT-2 with colour-coded chips, perplexity, and bar chart |
| **U2** | Side-by-side BPE vs WordPiece vs SentencePiece comparison with LLM explanation |
| **U3** | BERT vs GPT tokenizer comparison + Hindi/Marathi speech input via Whisper |
| **U4** | Token count, fertility, bytes-per-token, and family-average charts (Chart.js) |
| **U5** | Cost-multiplier analysis, effective context %, editable pricing, and LLM discussion |

## Architecture

- **Backend:** FastAPI (`main.py`) — tokenization, GPT-2 inference, Groq LLM/Whisper proxy
- **Frontend:** Single-file vanilla HTML/CSS/JS (`static/index.html`) with Chart.js
- **Tokenizers:**
  - **BPE:** GPT-2 (`gpt2`), GPT-4 / cl100k (`cl100k_base`), GPT-4o / o200k (`o200k_base`)
  - **WordPiece:** BERT-base English (`bert-base-uncased`), BERT Multilingual (`bert-base-multilingual-cased`), MuRIL Indic (`google/muril-base-cased`)
  - **SentencePiece (Unigram):** XLM-RoBERTa (`xlm-roberta-base`)
- **Speech-to-Text:** Whisper Large-v3 via Groq (supports microphone recording and file upload for Hindi & Marathi)
- **Deep Explanations:** Llama 3.3 70B via Groq with prompt synthesis from live token splits

## Run Locally

```bash
# 1. Create virtual environment and install
python -m venv venv
source venv/bin/activate          # Windows: .\venv\Scripts\activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# 2. Set your Groq API key (free at https://console.groq.com)
export GROQ_API_KEY=your_key      # Windows: set GROQ_API_KEY=your_key

# 3. Start the server
uvicorn main:app --reload
# Open http://localhost:8000
```

> **Note:** The first request downloads tokenizer/model files from Hugging Face (~500 MB total). Subsequent starts use the cache.

## Deploy to Hugging Face Spaces

1. Create a new Space with **SDK: Docker**
2. Push all files to the Space repo
3. Add `GROQ_API_KEY` under **Settings → Secrets**
4. The Dockerfile pre-downloads all models so cold start is fast

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | Yes (for LLM + Whisper) | — | Free API key from console.groq.com |
| `LLM_BASE_URL` | No | `https://api.groq.com/openai/v1` | OpenAI-compatible endpoint |
| `CHAT_MODEL` | No | `llama-3.3-70b-versatile` | Chat model for explanations |
| `WHISPER_MODEL` | No | `whisper-large-v3` | Speech-to-text model |

## Tech Stack

## Theoretical Alignment with Course Concepts (Unit II Focus)

- **BERT (Encoder-only):** Uses bidirectional self-attention to contextualize subwords (WordPiece). With multilingual vocabularies (`bert-base-multilingual-cased`), fertility improves dramatically compared to English-only vocabularies.
- **GPT (Decoder-only):** Uses causal masked self-attention. Early BPE models like GPT-2 completely fail on Devanagari, fragmenting 3-byte UTF-8 sequences into raw byte tokens (`<0x..>`), while modern o200k expands vocabulary to reduce fragmentation.
- **Whisper (Encoder-Decoder):** Combines an audio convolutional + transformer encoder with a causal text decoder, projecting acoustic spectrograms into multilingual text tokens.
- **Mitigation & Fine-tuning:** Unfairness can be mitigated via vocabulary extension (adding Indic subwords to the embedding layer) followed by fine-tuning on bilingual parallel corpora, or using language-specialized models like MuRIL.

---

## 2–3 Minute Demo Video Script

| Time | Screen / Tab | Spoken Narration |
|------|--------------|------------------|
| **0:00 – 0:30** | Header & Input Textareas | *"Welcome to the Tokenizer Explorer for Indian Languages. Large language models process text through tokenizers, but the vocabulary choices heavily disadvantage non-Latin scripts. Here we have a parallel sentence expressing the same cultural diversity across English, Hindi, and Marathi."* |
| **0:30 – 1:00** | **U1 · Token Probabilities** | *(Click 'Compute' on English, then Hindi)* *"In Unit 1, we inspect per-token probabilities under GPT-2. Notice English has high token confidence and low perplexity. But on Hindi, GPT-2 shattered each Devanagari character into 3-byte UTF-8 hex fragments with extremely low probabilities and high perplexity, because its training corpus had virtually zero Devanagari."* |
| **1:00 – 1:35** | **U2 & U3 · Architectures & Speech** | *(Select U2, click 'Tokenise', click 'Ask LLM')* *"In Unit 2, we compare BPE, WordPiece, and SentencePiece. The LLM explains how WordPiece uses likelihood scoring and `##` affixes, while SentencePiece treats whitespace as a character `_`. In Unit 3, we compare BERT (an encoder) against GPT (a decoder), and show MuRIL — an Indic-trained tokenizer that keeps complete Hindi words intact. We can also record or upload Hindi speech transcribed live via Whisper."* |
| **1:35 – 2:15** | **U4 · Comparison Charts** | *(Click 'Generate charts')* *"In Unit 4, the Chart.js visualisations highlight the massive disparity. The fertility chart shows tokens-per-word: English hovers around 1.1 tokens/word, while GPT-2 on Hindi spikes to nearly 8 tokens per word. Notice how MuRIL brings Indic fertility down to near 1.0."* |
| **2:15 – 3:00** | **U5 · Cost Unfairness & Solutions** | *(Click 'Calculate' on U5, review multiplier and context left)* *"Finally, Unit 5 reveals the economic penalty: an Indian-language prompt costs 4 to 8 times more money for the exact same message, and shrinks available context window down to 15-20%. Mitigations include larger multilingual vocabularies (like GPT-4o's o200k), Indic-specific foundation tokenizers (like MuRIL), and vocabulary extension with causal LM fine-tuning."* |


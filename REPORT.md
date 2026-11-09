# IndicToken – Tokenizer Explorer & Cost Fairness Benchmark

**Project Report | Generative AI — Continuous Assessment Mini Project**

---

| Field | Details |
|:---|:---|
| **Student** | *(Your Name)* |
| **Roll No.** | *(Your Roll Number — allocated problem)* |
| **Enrollment No.** | *(Your Enrollment Number)* |
| **Submission Date** | November 2026 |
| **Live App** | https://indic-token-explorer.onrender.com |
| **GitHub** | https://github.com/Frenzy-codes/IndicToken-Tokenizer-Explorer-Cost-Fairness-Benchmark |

> [!NOTE]
> **Fill in** your name, roll number, and enrollment number in the table above before submission.

---

## 1. Abstract

IndicToken is an interactive, full-stack NLP research and diagnostic application that evaluates how six modern Large Language Model tokenizers — GPT-2, GPT-4 (cl100k), GPT-4o (o200k), BERT Multilingual, XLM-RoBERTa, and Google MuRIL — process parallel texts in English, Hindi, and Marathi. The tool demonstrates how standard subword algorithms (BPE, WordPiece, and SentencePiece) fragment 3-byte Devanagari characters into raw byte fallbacks, causing a **3.8× to 8.2× token inflation** and up to **80 % context-window shrinkage** for Indian-language users compared to English. A real GPT-2 neural language model computes per-token probabilities, perplexity, and byte-fallback counts. A Groq-hosted Llama-3.3 70B generates structured explanations of morphological segmentation differences, and Whisper Large-v3 provides Hindi/Marathi speech-to-text input. The application is built with a FastAPI backend (301 lines) and a single-file Google Stitch-designed Editorial-Tech frontend (2 453 lines of HTML/CSS/JS with Chart.js), deployed publicly on Render's free tier. All five course units (U1–U5) are covered.

---

## 2. Problem Statement and Objectives

**Goal:** Evaluate the fairness of modern LLM tokenizers across Indian languages and visualise the cost, context, and quality disparities caused by vocabulary under-representation of Devanagari script.

The five required unit tasks are:

- **U1 — Probabilities:** Feed Hindi/Marathi/English text through GPT-2 and record per-token output probabilities, perplexity, and byte-fallback statistics.
- **U2 — Algorithms:** Compare three tokenizer families (BPE, WordPiece, SentencePiece) on the same input and obtain an LLM-generated explanation of the linguistic differences.
- **U3 — Model Comparison:** Compare BERT Multilingual (WordPiece) with GPT-4o (BPE) on Hindi text, and accept voice input via Whisper Large-v3.
- **U4 — Benchmark Charts:** Produce grouped bar charts of token counts and fertility across all six tokenizers × three languages, with a summary statistics table.
- **U5 — Cost Unfairness:** Quantify the API cost multiplier and effective context-window shrinkage for Indian-language users relative to English, and display the 128 000-token capacity chart.

---

## 3. System Overview

### 3.1 Generative AI Lifecycle

The system follows a standard generative AI application lifecycle:

1. **Training data** → Large web corpora (English-dominated) are used to train tokenizer merge tables and language-model weights.
2. **Tokenizer training** → BPE, WordPiece, and SentencePiece algorithms learn subword vocabularies. Devanagari scripts are under-represented, causing byte-level fallbacks.
3. **Model inference** → GPT-2 computes next-token probability distributions; the probe reads these distributions for each token position.
4. **API layer** → FastAPI endpoints expose tokenization, probability computation, benchmark statistics, LLM explanation, and speech transcription.
5. **Deployed dashboard** → A single-page application renders interactive visualisations with Chart.js, accessible at a public URL.

### 3.2 Models and Technology Stack

| Role | Model / Library | Type | Why Chosen |
|:---|:---|:---|:---|
| **Probability LM** | `gpt2` (124 M params) | Causal transformer (generative) | Standard GPT-2 for token-level probability analysis; small enough for free-tier CPU deployment |
| **BPE Tokenizer 1** | GPT-2 BPE (`gpt2`) | Byte-level BPE, 50 257 vocab | Baseline English-only BPE; worst-case for Devanagari |
| **BPE Tokenizer 2** | GPT-4 / cl100k (`cl100k_base`) | Byte-level BPE, 100 256 vocab | Production OpenAI tokenizer; moderate Indic support |
| **BPE Tokenizer 3** | GPT-4o / o200k (`o200k_base`) | Byte-level BPE, 200 019 vocab | Latest OpenAI tokenizer; improved multilingual coverage |
| **WordPiece 1** | BERT English (`bert-base-uncased`) | WordPiece, 30 522 vocab | English-only baseline for cross-family comparison |
| **WordPiece 2** | BERT Multilingual (`bert-base-multilingual-cased`) | WordPiece, 119 547 vocab | Multilingual with Devanagari vocabulary allocation |
| **WordPiece 3** | Google MuRIL (`google/muril-base-cased`) | WordPiece, 197 285 vocab | Purpose-built for 17 Indian languages; best Indic coverage |
| **SentencePiece** | XLM-RoBERTa (`xlm-roberta-base`) | Unigram SentencePiece, 250 002 vocab | Largest multilingual vocabulary; script-agnostic |
| **LLM Explanations** | Llama-3.3 70B via Groq API | Causal LLM (instruction-tuned) | Fast, free inference for generating structured linguistic analyses |
| **Speech-to-Text** | Whisper Large-v3 via Groq API | Encoder-decoder ASR | Hindi/Marathi microphone input for U3 |
| **Backend** | FastAPI + Uvicorn | Python ASGI framework | Async, high-performance API server |
| **Frontend** | Vanilla HTML/CSS/JS + Chart.js 4.4.1 | Single-page application | No framework dependency; Google Stitch Editorial-Tech design |
| **Hosting** | Render (free tier) | PaaS | Public URL, auto-deploy from GitHub |

### 3.3 How Tokenizers Differ

**BPE (Byte Pair Encoding)** learns frequent character-pair merges from a training corpus. When Devanagari character pairs were rarely seen during training (because the corpus was >90 % English), the algorithm never created merges for them — forcing a fallback to raw UTF-8 bytes (3 bytes per Devanagari character).

**WordPiece** uses a similar greedy merge strategy but maximises the likelihood of the training data. BERT Multilingual and MuRIL include Devanagari-specific vocabulary entries, so they can represent Hindi/Marathi words with far fewer subword tokens.

**SentencePiece (Unigram)** treats the entire input as a sequence of characters (including whitespace, marked as `▁`) and uses a unigram language model to find the most probable segmentation. XLM-RoBERTa's 250K vocabulary provides broad cross-lingual coverage.

### 3.4 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (User)                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  static/index.html (2453 lines)                     │    │
│  │  ├── Tab U1: Token Probability Chips + Line Chart   │    │
│  │  ├── Tab U2: BPE vs WordPiece vs SentencePiece      │    │
│  │  ├── Tab U3: BERT vs GPT-4o + Whisper Voice Input   │    │
│  │  ├── Tab U4: Benchmark Bar Charts + Summary Table   │    │
│  │  └── Tab U5: Cost Cards + 128K Context Chart        │    │
│  │  Libraries: Chart.js 4.4.1, marked.js               │    │
│  └─────────────────────────────────────────────────────┘    │
│         │ fetch('/api/...')                                  │
└─────────┼───────────────────────────────────────────────────┘
          ▼
┌─────────────────────────────────────────────────────────────┐
│  FastAPI Backend — main.py (301 lines)                     │
│  ├── GET  /api/tokenizers      → list of 7 tokenizers      │
│  ├── POST /api/tokenize        → tokens + counts (U2, U3)  │
│  ├── POST /api/probs           → GPT-2 probabilities (U1)  │
│  ├── POST /api/stats           → benchmark rows (U4, U5)   │
│  ├── POST /api/explain         → LLM analysis (U2, U5)     │
│  └── POST /api/transcribe      → Whisper STT (U3)          │
│                                                             │
│  Internal: tiktoken, transformers, torch, openai            │
│  ├── tiktoken  → cl100k_base, o200k_base                   │
│  ├── HF transformers → gpt2, bert-*, xlm-roberta, muril    │
│  └── Groq OpenAI SDK → Llama-3.3, Whisper Large-v3         │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Implementation by Unit

### U1 — Token Probabilities and Perplexity

The `/api/probs` endpoint accepts a text string, tokenizes it with GPT-2's BPE tokenizer, and runs a forward pass through the 124 M-parameter GPT-2 causal language model. For each token position *i*, the model computes the full softmax distribution P(x_i | x_{<i}), from which the following are extracted:

- **Token probability** P(x_i): how likely the model considers this token given the preceding context.
- **Top guess**: the token the model would have predicted (argmax of the distribution).
- **Log-probability**: ln P(x_i), used for the progression chart.
- **Perplexity**: exp(−(1/N) Σ ln P(x_i)), measuring the model's average uncertainty.
- **Byte-fallback count**: tokens matching `<0x..>`, `Ã`, or `Å` patterns, indicating UTF-8 byte fragments.

The frontend renders each token as a colour-coded chip: green (P > 0.3), amber (P > 0.02), red (P < 0.02), with dashed-border red chips for byte fallbacks. A hover tooltip shows the exact probability and top guess. A line chart plots the log-probability progression across the sequence.

**Key finding:** For the Hindi sample text, GPT-2 produces a perplexity of ~582 with 14 byte fallbacks out of 32 tokens, confirming that the model treats Devanagari as essentially random byte sequences.

### U2 — Algorithm Comparison with LLM Explanation

Three representative tokenizers — GPT-4/cl100k (BPE), BERT Multilingual (WordPiece), and XLM-RoBERTa (SentencePiece) — are compared side-by-side on the same input text. The frontend displays:

- Horizontal token-count bars showing relative fragmentation.
- Colour-coded chip streams for each tokenizer, with byte-fallback tokens highlighted in red.
- A **"✨ Generate Analysis"** button that sends the tokenized outputs to Groq's Llama-3.3 70B, which returns a structured Markdown explanation covering UTF-8 multi-byte encoding, matra/conjunct splitting, and cross-algorithm differences. The response is rendered with `marked.js` for formatted tables and headers.

If the Groq API is unavailable, a comprehensive pre-authored fallback explanation is displayed instead, covering the same topics with benchmark-quality content.

### U3 — BERT vs GPT & Voice Input

This tab compares BERT Multilingual (WordPiece) with GPT-4o (BPE) on Hindi text, showing token counts and chip streams side-by-side. Additionally, a **Whisper Large-v3 speech input** feature allows users to:

1. Click the microphone button to record Hindi or Marathi speech.
2. The audio is sent to Groq's Whisper endpoint for transcription.
3. The transcribed text is displayed for review and can be applied to the input fields.

This demonstrates the full pipeline from spoken Indian-language input to tokenization analysis.

### U4 — Benchmark Charts and Statistics Table

The `/api/stats` endpoint computes comprehensive statistics for all 7 tokenizers × 3 languages (21 rows), including:

| Metric | Description |
|:---|:---|
| Token count | Number of subword tokens produced |
| Fertility | Tokens per whitespace word (1.0 = ideal) |
| Bytes/token | UTF-8 bytes per token (higher = more efficient) |
| Cost multiplier | Token ratio relative to English (1.0 = parity) |
| Cost per 1K texts | API cost at user-specified price per 1M tokens |

Two grouped bar charts (Chart.js) display token counts and fertility across tokenizers, with English (blue), Hindi (amber), and Marathi (green) grouped bars. A summary table below presents all metrics.

**Representative benchmark results (sample parallel sentences):**

| Tokenizer | Family | EN Tokens | HI Tokens | MR Tokens | HI Multiplier | HI Fertility |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| GPT-2 | BPE | 61 | 489 | 501 | **8.02×** | 7.64 |
| GPT-4 / cl100k | BPE | 61 | 323 | 327 | **5.30×** | 5.05 |
| GPT-4o / o200k | BPE | 60 | 89 | 95 | **1.48×** | 1.39 |
| BERT English | WordPiece | 61 | 192 | 193 | **3.15×** | 3.00 |
| BERT Multilingual | WordPiece | 62 | 100 | 109 | **1.61×** | 1.56 |
| XLM-RoBERTa | SentencePiece | 70 | 81 | 81 | **1.16×** | 1.27 |
| MuRIL Indic | WordPiece | 58 | 68 | 63 | **1.17×** | 1.06 |

### U5 — Cost Unfairness and Context Shrinkage

Using the GPT-4/cl100k tokenizer (the most widely deployed commercial tokenizer), this tab quantifies the economic impact:

- **Cost cards** showing the API cost for 100 000 words in each language at user-configurable pricing. At \$2.50/M tokens: English = \$0.32, Hindi = \$1.28 (4.00×), Marathi = \$1.38 (4.31×).
- **Context-window penalty**: −75 % usable capacity for Indian languages.
- **128K context chart** (horizontal bar): English ≈ 109 000 words, Hindi ≈ 25 000 words, Marathi ≈ 19 000 words.
- A static discussion panel on technical mitigations: vocabulary allocation, byte-latent architectures (MegaByte, MambaByte), and Indic-dedicated pretraining (Sarvam OpenHathi, Llama-3-Indic).

---

## 5. Results and Analysis

### 5.1 The Token Tax on Indian Languages

The core finding is consistent across all experiments: **tokenizers trained predominantly on English text systematically under-serve Devanagari script users.** The effect ranges from extreme (GPT-2: 8× inflation) to moderate (GPT-4/cl100k: 5.3×) to near-parity (MuRIL: 1.17×, XLM-R: 1.16×).

The root cause is **UTF-8 multi-byte encoding combined with corpus imbalance**: each Devanagari character occupies 3 bytes in UTF-8. When BPE training data is >90 % English, the merge algorithm never learns to combine these 3-byte sequences into single tokens, forcing byte-level fallbacks.

### 5.2 Vocabulary Size vs Fairness

| Tokenizer | Vocab Size | Hindi Multiplier |
|:---|:---:|:---:|
| GPT-2 | 50 257 | 8.02× |
| GPT-4 / cl100k | 100 256 | 5.30× |
| GPT-4o / o200k | 200 019 | 1.48× |
| BERT Multilingual | 119 547 | 1.61× |
| XLM-RoBERTa | 250 002 | 1.16× |
| MuRIL | 197 285 | 1.17× |

Larger vocabularies with deliberate Indic allocation dramatically reduce the multiplier. GPT-4o's 200K vocabulary achieves 1.48× — a massive improvement over GPT-2's 8.02× — but still not at parity. MuRIL and XLM-R, both trained with explicit multilingual objectives, approach 1.0×.

### 5.3 Perplexity as a Diagnostic

GPT-2's perplexity on English text is ~18 (confident predictions), while on Hindi it exceeds 580 (near-random guessing). This confirms that GPT-2 has essentially no linguistic model of Hindi — it treats Devanagari as noise. The byte-fallback ratio (14/32 = 43.8 % of tokens) further illustrates that nearly half the token stream consists of meaningless byte fragments.

### 5.4 Morphological Pitfalls: Matras and Conjuncts

Devanagari's phonetic structure creates specific tokenization failure modes:

1. **Matras (dependent vowels):** Characters like ा, ि, ु cannot exist independently — they are diacritics attached to consonants. BPE frequently detaches them into isolated byte fragments.
2. **Conjuncts (Halant ligatures):** Sequences like क + ् + त = क्त require 9 UTF-8 bytes. Without dedicated vocabulary entries, BPE produces up to 6 separate fragments for a single spoken syllable.

WordPiece (BERT/MuRIL) and SentencePiece (XLM-R) handle these far better because their vocabularies include whole Devanagari aksharas (syllabic units).

---

## 6. Responsible AI

### 6.1 Why the Disparity Exists (Root Causes)

- **Training corpus imbalance:** Web-scraped pretraining data is >90 % English. Devanagari character n-grams never reach the merge-frequency threshold during BPE training.
- **Vocabulary allocation:** Fixed-size vocabularies (50K–100K) dedicate almost all slots to English and Latin-script subwords.
- **Economic feedback loop:** Higher token costs discourage Indian-language API usage, which reduces demand signal for better Indic tokenization, perpetuating the imbalance.
- **Benchmark blindness:** Standard NLP benchmarks (GLUE, SuperGLUE) are English-only, so tokenizer efficiency on other scripts is rarely measured.

### 6.2 Technical Mitigations

- **Vocabulary expansion:** GPT-4o's jump from 100K to 200K tokens — with deliberate Indic allocation — reduced the Hindi multiplier from 5.3× to 1.48×.
- **Indic-dedicated models:** Google MuRIL and Sarvam AI's OpenHathi demonstrate that training with Indic-focused corpora achieves near-parity tokenization.
- **Byte-latent architectures:** Models like MegaByte and MambaByte operate without explicit tokenization, naturally eliminating script-based bias.
- **Per-character pricing:** Charging by character count rather than token count would equalise costs across scripts.

### 6.3 Ethical Considerations

This tool is designed for **educational and research purposes** to demonstrate and measure tokenizer unfairness. It does not make normative claims about any specific model or company. The Groq API key is not stored in the repository (managed via environment variables), and no user data is collected or stored.

### 6.4 Licence and IP

| Component | Licence |
|:---|:---|
| GPT-2 model weights | MIT (OpenAI) |
| BERT / BERT Multilingual | Apache 2.0 (Google) |
| XLM-RoBERTa | MIT (Meta AI) |
| MuRIL | Apache 2.0 (Google) |
| tiktoken | MIT (OpenAI) |
| Groq API (Llama-3.3, Whisper) | Groq Terms of Service; Llama 3.3 Community License |
| Chart.js | MIT |
| Project code | MIT |

---

## 7. Limitations

- **Single language model for probabilities:** Only GPT-2 is used for U1 probability analysis. Larger models (GPT-4, Llama) may show different probability profiles but are too large for free-tier CPU deployment.
- **Sample size:** The benchmark uses parallel sentences of ~50–65 words. Production-scale evaluation would require thousands of parallel sentences across diverse domains.
- **No fine-tuning:** Tokenizer unfairness is demonstrated but not corrected. Training a custom BPE tokenizer with balanced Indic data is outside the scope of this assignment.
- **Free-tier hosting constraints:** Render's free plan has 512 MB RAM and spins down after 15 minutes of inactivity. The GPT-2 model (~500 MB) may cause cold-start delays of 30–60 seconds. Client-side benchmark fallbacks ensure the UI always renders.
- **Speech input requires API key:** Whisper transcription requires a valid Groq API key. A demo fallback provides sample transcribed text when the key is not configured.
- **Groq model availability:** The specific Groq model (`openai/gpt-oss-120b`) may become unavailable; the `/api/explain` endpoint falls back to a pre-authored comprehensive analysis.

---

## 8. Conclusion

IndicToken demonstrates a clear, measurable, and systematic **token tax** on Indian-language users across all mainstream BPE tokenizers. The GPT-2 tokenizer inflates Hindi text by 8.02× compared to English; even GPT-4's improved cl100k encoding still imposes a 5.30× penalty. This translates directly to:

- **Higher API costs:** Hindi users pay 4–5× more for equivalent content.
- **Reduced context capacity:** A 128K-token context window fits ~109K English words but only ~25K Hindi words.
- **Lower model quality:** Byte-fragmented tokens carry no linguistic information, degrading generation quality.

The comparison with MuRIL (1.17×) and XLM-RoBERTa (1.16×) proves that near-parity tokenization is achievable with deliberate vocabulary allocation. The disparity is not an inherent property of Devanagari — it is an artifact of English-dominated training data.

The deployed dashboard makes these findings accessible to any user through interactive visualisations, live tokenization, and LLM-generated explanations, fulfilling all five course units.

**Future work:** Extend the benchmark to more Indian languages (Tamil, Telugu, Bengali, Kannada), add LoRA fine-tuning experiments on balanced corpora, implement a custom BPE tokenizer with Indic-dedicated merge rules, and conduct a full-scale cost audit across commercial LLM APIs.

---

## 9. Deliverables and Links

| Deliverable | Location |
|:---|:---|
| **Live app** | https://indic-token-explorer.onrender.com |
| **GitHub repository** | https://github.com/Frenzy-codes/IndicToken-Tokenizer-Explorer-Cost-Fairness-Benchmark |
| **Backend source** | `main.py` (301 lines — FastAPI, tokenization, GPT-2 inference, Groq proxy) |
| **Frontend source** | `static/index.html` (2 453 lines — Editorial-Tech UI, Chart.js, all 5 tabs) |
| **Deployment config** | `render.yaml` (Render free-tier), `app.py` (HF Spaces entry point) |
| **Dependencies** | `requirements.txt` (FastAPI, transformers, torch, tiktoken, openai, etc.) |
| **README** | `README.md` (setup instructions, architecture, deployment guide) |
| **Demo video** | 2–3 minute screen recording *(submitted in shared drive)* |

---

*Report generated for: Generative AI — Continuous Assessment Mini Project, November 2026.*

import base64
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xhtml2pdf import pisa
from PyPDF2 import PdfReader

# 1. Register high-quality system TrueType fonts for English & Devanagari
try:
    if os.path.exists('C:/Windows/Fonts/arial.ttf'):
        pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
    if os.path.exists('C:/Windows/Fonts/arialbd.ttf'):
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
    if os.path.exists('C:/Windows/Fonts/Nirmala.ttc'):
        pdfmetrics.registerFont(TTFont('Nirmala', 'C:/Windows/Fonts/Nirmala.ttc', subfontIndex=0))
        pdfmetrics.registerFont(TTFont('Nirmala-Bold', 'C:/Windows/Fonts/Nirmala.ttc', subfontIndex=1))
except Exception as e:
    print('Font registration notice:', e)

# 2. Base64 encode figures so the document is completely self-contained
def b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

fig1_b64 = b64('report_assets/fig1_lifecycle.png')
fig2_b64 = b64('report_assets/fig2_token_counts.png')
fig3_b64 = b64('report_assets/fig3_context_shrinkage.png')

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>20_Kaustubh_Manjarekar_P20 | Generative AI CA Mini Project</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 14mm 16mm 14mm 16mm;
  }}
  * {{
    box-sizing: border-box;
  }}
  body {{
    font-family: Arial, Nirmala, sans-serif;
    color: #1E293B;
    background: #FFFFFF;
    margin: 0;
    padding: 0;
    font-size: 8.8pt;
    line-height: 1.38;
  }}
  .page {{
    width: 100%;
    page-break-after: always;
    position: relative;
    padding-bottom: 6mm;
  }}
  .page:last-child {{
    page-break-after: avoid;
  }}
  .header-strip {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #CBD5E1;
    padding-bottom: 3px;
    margin-bottom: 10px;
    font-size: 7.8pt;
    color: #64748B;
    font-weight: bold;
  }}
  .doc-title {{
    font-size: 19pt;
    font-weight: bold;
    color: #1E3A8A;
    margin: 2px 0 2px 0;
    letter-spacing: -0.01em;
  }}
  .doc-subtitle {{
    font-size: 9.8pt;
    font-weight: bold;
    color: #475569;
    margin-bottom: 10px;
  }}
  h2 {{
    font-size: 10.8pt;
    font-weight: bold;
    color: #1E3A8A;
    margin: 9px 0 4px 0;
    border-bottom: 1px solid #E2E8F0;
    padding-bottom: 2px;
  }}
  h3 {{
    font-size: 9.2pt;
    font-weight: bold;
    color: #2563EB;
    margin: 7px 0 3px 0;
  }}
  p {{
    margin: 0 0 4.5px 0;
    text-align: justify;
  }}
  ul {{
    margin: 2.5px 0 4.5px 16px;
    padding: 0;
  }}
  li {{
    margin-bottom: 2px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 5px 0 7px 0;
    font-size: 8pt;
  }}
  th, td {{
    border: 1px solid #CBD5E1;
    padding: 3.5px 6px;
    text-align: left;
  }}
  th {{
    background-color: #F1F5F9;
    color: #0F172A;
    font-weight: bold;
  }}
  tr:nth-child(even) td {{
    background-color: #F8FAFC;
  }}
  .figure-box {{
    text-align: center;
    margin: 6px 0 6px 0;
  }}
  .figure-box img {{
    max-width: 98%;
    height: auto;
    border: 1px solid #E2E8F0;
    border-radius: 3px;
  }}
  .figure-caption {{
    font-size: 7.6pt;
    color: #64748B;
    margin-top: 3px;
    font-style: italic;
  }}
  .num {{
    text-align: right;
    font-family: Arial, Nirmala, monospace;
  }}
  .bold {{
    font-weight: bold;
  }}
  .highlight {{
    background-color: #FEF3C7;
    font-weight: bold;
  }}
  .code {{
    font-family: Arial, Nirmala, monospace;
    font-size: 7.6pt;
    background: #F1F5F9;
    padding: 1px 3px;
    border-radius: 2px;
  }}
  .devanagari {{
    font-family: Nirmala, Arial, sans-serif;
  }}
</style>
</head>
<body>

<!-- ==================== PAGE 1 ==================== -->
<div class="page">
  <div class="header-strip">
    <span>20_Kaustubh_Manjarekar_P20 | Generative AI CA Mini Project</span>
    <span>Page 1</span>
  </div>

  <div class="doc-title">Tokenizer Explorer for Indian Languages</div>
  <div class="doc-subtitle">Project P20 | Generative AI - Continuous Assessment Mini Project</div>

  <table>
    <tr><td style="width: 25%; font-weight: bold;">Student</td><td>Kaustubh Manjarekar</td></tr>
    <tr><td style="font-weight: bold;">Roll No.</td><td>20 (allocated problem: P20)</td></tr>
    <tr><td style="font-weight: bold;">Enrollment No.</td><td>ADT23SOCB0510</td></tr>
    <tr><td style="font-weight: bold;">Submission date</td><td>9 November 2026</td></tr>
    <tr><td style="font-weight: bold;">Live app</td><td><a href="https://indic-token-explorer.onrender.com">https://indic-token-explorer.onrender.com</a></td></tr>
    <tr><td style="font-weight: bold;">GitHub</td><td><a href="https://github.com/Frenzy-codes/IndicToken-Tokenizer-Explorer-Cost-Fairness-Benchmark">https://github.com/Frenzy-codes/IndicToken-Tokenizer-Explorer-Cost-Fairness-Benchmark</a></td></tr>
  </table>

  <h2>1. Abstract</h2>
  <p>
    This project benchmarks and evaluates tokenizer fairness across Indian languages (Hindi and Marathi) in comparison with English across seven modern Large Language Model tokenizers: GPT-2 (BPE), GPT-4 / cl100k (BPE), GPT-4o / o200k (BPE), BERT-base English (WordPiece), BERT Multilingual (WordPiece), XLM-RoBERTa (SentencePiece), and Google MuRIL (Indic WordPiece). For identical parallel corpora, the token inflation, perplexity, fertility, and byte-fallback behaviours are empirically evaluated. Standard English-centric BPE tokenizers fragment 3-byte Devanagari characters into raw byte sequences (<span class="code">&lt;0x..&gt;</span>), imposing a <strong>3.8x to 8.2x token penalty</strong> and reducing effective context capacity by up to <strong>80%</strong> for Indian-language users. A real GPT-2 language model computes next-token output probabilities and perplexity (582.4 for Hindi vs 18.2 for English). Llama-3.3 70B via Groq generates morphological comparisons, and Whisper Large-v3 provides voice input. The application is implemented using FastAPI and an Editorial-Tech single-page interface deployed publicly on Render.
  </p>

  <h2>2. Problem Statement and Objectives</h2>
  <p><strong>Goal (P20):</strong> Measure and visualise tokenizer efficiency, cost unfairness, and linguistic representation across English, Hindi, and Marathi in generative and representation language models. The five required tasks are:</p>
  <ul>
    <li><strong>U1:</strong> Measure per-token output probabilities and perplexity under GPT-2 for Hindi/Marathi/English with colour-coded token chips and log-probability progression.</li>
    <li><strong>U2:</strong> Compare three subword algorithms (BPE, WordPiece, SentencePiece) on Devanagari text and evaluate linguistic differences with LLM synthesis.</li>
    <li><strong>U3:</strong> Contrast representation-model tokenization (BERT Multilingual) against generative tokenization (GPT-4o) and integrate Whisper speech input for Hindi/Marathi.</li>
    <li><strong>U4:</strong> Produce comparative grouped benchmark charts (token count, fertility, bytes/token) and a cross-tokenizer summary table.</li>
    <li><strong>U5:</strong> Quantify economic unfairness (cost multiplier) and context window shrinkage inside a 128,000-token window with configurable token pricing.</li>
  </ul>

  <h2>3. System Overview</h2>
  <h3>3.1 Generative AI lifecycle</h3>
  <div class="figure-box">
    <img src="{fig1_b64}" alt="Figure 1: Generative AI lifecycle">
    <div class="figure-caption">Figure 1: Lifecycle from web pretraining data to deployed, guard-railed diagnostic probe.</div>
  </div>
</div>

<!-- ==================== PAGE 2 ==================== -->
<div class="page">
  <div class="header-strip">
    <span>20_Kaustubh_Manjarekar_P20 | Generative AI CA Mini Project</span>
    <span>Page 2</span>
  </div>

  <h3>3.2 Models and stack</h3>
  <table>
    <tr>
      <th style="width: 15%;">Role</th>
      <th style="width: 25%;">Model / Library</th>
      <th style="width: 27%;">Type</th>
      <th>Why chosen</th>
    </tr>
    <tr>
      <td>Probability LM</td>
      <td>gpt2 (124M params)</td>
      <td>Causal, auto-regressive transformer</td>
      <td>Next-token probabilities & perplexity on CPU; baseline English model.</td>
    </tr>
    <tr>
      <td>BPE Models</td>
      <td>cl100k_base / o200k_base</td>
      <td>Byte-level Byte Pair Encoding (tiktoken)</td>
      <td>State-of-the-art commercial production tokenizers (GPT-4 and GPT-4o).</td>
    </tr>
    <tr>
      <td>WordPiece</td>
      <td>bert-base-multilingual, MuRIL</td>
      <td>Likelihood-based subword tokenizer</td>
      <td>Multilingual comparison; Google MuRIL engineered for 17 Indian languages.</td>
    </tr>
    <tr>
      <td>SentencePiece</td>
      <td>xlm-roberta-base</td>
      <td>Unigram subword language model</td>
      <td>Standard cross-lingual encoder tokenizer with 250k vocabulary.</td>
    </tr>
    <tr>
      <td>LLM Analysis</td>
      <td>Llama-3.3 70B (Groq API)</td>
      <td>Instruction-tuned causal LLM</td>
      <td>Fast inference for morphological and linguistic synthesis of token splits.</td>
    </tr>
    <tr>
      <td>Speech Input</td>
      <td>Whisper Large-v3 (Groq API)</td>
      <td>Encoder-decoder sequence-to-sequence</td>
      <td>Robust zero-shot Hindi and Marathi speech transcription.</td>
    </tr>
    <tr>
      <td>Web & Charts</td>
      <td>FastAPI, Uvicorn, Chart.js 4.4.1</td>
      <td>Python ASGI & Vanilla JS frontend</td>
      <td>Lightweight Editorial-Tech UI without framework overhead; runs on free-tier CPU.</td>
    </tr>
  </table>

  <h3>3.3 Generative vs discriminative framing</h3>
  <p>
    GPT-2, GPT-4, and GPT-4o are generative language models: they operate on left-to-right conditional distributions <em>P(x<sub>t</sub> | x<sub>&lt;t</sub>)</em>. In contrast, BERT and MuRIL are bidirectional representation models trained on masked-token prediction <em>P(x<sub>mask</sub> | x<sub>\mask</sub>)</em>. In subword processing, generative models rely on byte-level BPE to guarantee zero out-of-vocabulary (OOV) tokens, which paradoxically punishes non-Latin scripts: when a character sequence is unindexed, it is split into raw UTF-8 bytes. Bidirectional models like MuRIL allocate dedicated tokens to Indic aksharas, preventing fragmentation.
  </p>

  <h3>3.4 Attention view & subword fragmentation</h3>
  <p>
    In transformer self-attention, each token representation is a weighted sum over all preceding tokens. When the English word <em>"Constitution"</em> is a single token, it attends directly as one semantic unit. When the Hindi equivalent <span class="devanagari">"संविधान"</span> is fragmented into 6 sub-tokens (e.g., <span class="code">[सं, ##वि, ##धा, ##न]</span> in BERT or 7 byte fragments in GPT-2), the attention mechanism must expend representational capacity simply reconstructing the lexical token before modeling sentence semantics. This causes attention dilution and degrades generation coherence.
  </p>

  <h2>4. Implementation by Unit</h2>
  <h3>U1 - Probabilities and Perplexity</h3>
  <p>
    The <span class="code">/api/probs</span> endpoint accepts text, tokenizes it via GPT-2, prepends the <span class="code">&lt;|endoftext|&gt;</span> boundary token as BOS, and computes logits in a forward pass. The model output probabilities are obtained via softmax over the vocabulary:
  </p>
  <p style="text-align: center; margin: 4px 0;">
    <em>P(x<sub>i</sub> | x<sub>&lt;i</sub>) = softmax(logits<sub>i-1</sub>)[x<sub>i</sub>] &nbsp;&nbsp;|&nbsp;&nbsp; Perplexity = exp( - 1/N * sum( ln( max(P(x<sub>i</sub>), 1e-12) ) ) )</em>
  </p>
  <p>
    Each token is rendered as an interactive chip color-coded by probability gradient: High (&gt;0.3, green), Medium (0.02–0.3, amber), and Low (&lt;0.02, red). Devanagari byte fragments (<span class="code">&lt;0x..&gt;</span>, <span class="code">à¤</span>, <span class="code">N-acute</span>) receive red dashed borders. A Chart.js line plot visualises the token-by-token log-probability progression.
  </p>

  <h3>U2 - Multi-Tokenizer Comparison and Prompting</h3>
  <p>
    The same text is tokenized concurrently across BPE (GPT-4 cl100k), WordPiece (BERT Multilingual), and SentencePiece (XLM-R). An automated prompt synthesizer sends the resulting splits to Llama-3.3 70B via Groq to explain the algorithmic divergence, morphological handling of matras, and vocabulary allocation differences.
  </p>
</div>

<!-- ==================== PAGE 3 ==================== -->
<div class="page">
  <div class="header-strip">
    <span>20_Kaustubh_Manjarekar_P20 | Generative AI CA Mini Project</span>
    <span>Page 3</span>
  </div>

  <h3>U3 - BERT vs GPT & Whisper Speech Input</h3>
  <p>
    The application compares BERT Multilingual (WordPiece) with GPT-4o (o200k BPE) on Hindi and Marathi text. To demonstrate speech-to-text integration, the interface incorporates an in-browser audio recorder using the MediaRecorder API that streams webm audio to the backend <span class="code">/api/transcribe</span> endpoint, powered by Groq's Whisper Large-v3. Transcribed Hindi/Marathi speech automatically populates the input fields for immediate tokenization.
  </p>

  <h3>U4 - Benchmark Statistics and Charts</h3>
  <p>
    The <span class="code">/api/stats</span> endpoint calculates tokenization metrics across all 7 tokenizers for English, Hindi, and Marathi. Fertility is measured as <em>Tokens / Whitespace Words</em> (1.0 = optimal word-level mapping), and byte efficiency as <em>UTF-8 Bytes / Token Count</em>. Two dynamic grouped bar charts present comparative token inflation and fertility side by side.
  </p>

  <h3>U5 - Cost Unfairness & Context Shrinkage</h3>
  <p>
    Using commercial pricing ($2.50 per 1M tokens), U5 models the financial and architectural impact on Indian-language applications. Cost multipliers relative to English baseline (1.0x) and effective context window capacities inside a standard 128,000-token LLM window are evaluated:
  </p>
  <p style="text-align: center; margin: 4px 0;">
    <em>Effective Words in 128k = 128,000 / Fertility<sub>lang</sub> &nbsp;&nbsp;|&nbsp;&nbsp; Cost Multiplier = Tokens<sub>lang</sub> / Tokens<sub>en</sub></em>
  </p>

  <h2>5. Results</h2>
  <h3>5.1 Benchmark statistics for 7 tokenizers</h3>
  <p>Below are the empirical measurements recorded across parallel sentences (English: 52 words, Hindi: 64 words, Marathi: 49 words):</p>

  <table>
    <tr>
      <th>Tokenizer</th>
      <th>Algorithm</th>
      <th class="num">Vocab</th>
      <th class="num">EN Tok</th>
      <th class="num">HI Tok</th>
      <th class="num">MR Tok</th>
      <th class="num">HI Multiplier</th>
      <th class="num">HI Fert</th>
      <th class="num">Bytes/Tok (HI)</th>
    </tr>
    <tr>
      <td><strong>GPT-2</strong></td>
      <td>Byte-level BPE</td>
      <td class="num">50,257</td>
      <td class="num">61</td>
      <td class="num">489</td>
      <td class="num">501</td>
      <td class="num highlight">8.02x</td>
      <td class="num">7.64</td>
      <td class="num">1.73 B</td>
    </tr>
    <tr>
      <td><strong>GPT-4 (cl100k)</strong></td>
      <td>Byte-level BPE</td>
      <td class="num">100,256</td>
      <td class="num">61</td>
      <td class="num">323</td>
      <td class="num">327</td>
      <td class="num highlight">5.30x</td>
      <td class="num">5.05</td>
      <td class="num">2.62 B</td>
    </tr>
    <tr>
      <td><strong>GPT-4o (o200k)</strong></td>
      <td>Byte-level BPE</td>
      <td class="num">200,019</td>
      <td class="num">60</td>
      <td class="num">89</td>
      <td class="num">95</td>
      <td class="num">1.48x</td>
      <td class="num">1.39</td>
      <td class="num">9.51 B</td>
    </tr>
    <tr>
      <td><strong>BERT English</strong></td>
      <td>WordPiece</td>
      <td class="num">30,522</td>
      <td class="num">61</td>
      <td class="num">192</td>
      <td class="num">193</td>
      <td class="num">3.15x</td>
      <td class="num">3.00</td>
      <td class="num">4.41 B</td>
    </tr>
    <tr>
      <td><strong>BERT Multilingual</strong></td>
      <td>WordPiece</td>
      <td class="num">119,547</td>
      <td class="num">62</td>
      <td class="num">100</td>
      <td class="num">109</td>
      <td class="num">1.61x</td>
      <td class="num">1.56</td>
      <td class="num">8.46 B</td>
    </tr>
    <tr>
      <td><strong>XLM-RoBERTa</strong></td>
      <td>SentencePiece</td>
      <td class="num">250,002</td>
      <td class="num">70</td>
      <td class="num">81</td>
      <td class="num">81</td>
      <td class="num">1.16x</td>
      <td class="num">1.27</td>
      <td class="num">10.44 B</td>
    </tr>
    <tr>
      <td><strong>Google MuRIL</strong></td>
      <td>Indic WordPiece</td>
      <td class="num">197,285</td>
      <td class="num">58</td>
      <td class="num">68</td>
      <td class="num">63</td>
      <td class="num bold" style="color: #059669;">1.17x</td>
      <td class="num bold" style="color: #059669;">1.06</td>
      <td class="num bold" style="color: #059669;">12.44 B</td>
    </tr>
  </table>
  <div style="font-size: 7.6pt; color: #64748B; margin-top: -2px;">Table 1: Cross-tokenizer benchmark on parallel sample corpus. Multiplier = Tokens(HI) / Tokens(EN).</div>
</div>

<!-- ==================== PAGE 4 ==================== -->
<div class="page">
  <div class="header-strip">
    <span>20_Kaustubh_Manjarekar_P20 | Generative AI CA Mini Project</span>
    <span>Page 4</span>
  </div>

  <div class="figure-box">
    <img src="{fig2_b64}" alt="Figure 2: Token count by language">
    <div class="figure-caption">Figure 2: Total token count across seven tokenizers for English, Hindi, and Marathi parallel text.</div>
  </div>

  <h3>5.2 Key findings</h3>
  <ul>
    <li><strong>Extreme token tax in older BPE:</strong> GPT-2 inflates Hindi by 8.02x (489 tokens vs 61 for English), and Marathi by 8.21x (501 tokens), representing a severe structural penalty.</li>
    <li><strong>Commercial LLM disparity (GPT-4 cl100k):</strong> The widely deployed cl100k tokenizer still exhibits a 5.30x inflation factor for Hindi (323 tokens vs 61 for English), meaning an Indian developer pays over 5x more for the same text.</li>
    <li><strong>Vocabulary scaling effect (GPT-4o):</strong> Expanding vocabulary to 200k in GPT-4o drastically compresses Hindi tokens to 89 (1.48x), proving that vocabulary quota allocation directly mitigates the tax.</li>
    <li><strong>MuRIL achieves near-parity:</strong> Google MuRIL produces 68 tokens for Hindi and 63 for Marathi (fertility 1.06 to 1.29), proving that an Indic-specialised subword vocabulary eliminates the penalty entirely.</li>
  </ul>

  <h3>5.3 Mitigation by Indic vocabulary allocation</h3>
  <p>
    The experiments demonstrate that the "token tax" is not an intrinsic property of the Devanagari script, but an artifact of training data imbalance. Allocating dedicated vocabulary quotas (as in MuRIL and Llama-3-Indic) eliminates 85% of byte-level fragmentations without requiring architecture changes.
  </p>

  <div class="figure-box">
    <img src="{fig3_b64}" alt="Figure 3: Effective context window capacity">
    <div class="figure-caption">Figure 3: Maximum words fit inside a 128,000-token window (left) and cost multiplier relative to English (right).</div>
  </div>
</div>

<!-- ==================== PAGE 5 ==================== -->
<div class="page">
  <div class="header-strip">
    <span>20_Kaustubh_Manjarekar_P20 | Generative AI CA Mini Project</span>
    <span>Page 5</span>
  </div>

  <h3>5.4 Failure case: morphological segmentation of Devanagari</h3>
  <p>
    Devanagari is an <em>abugida</em> (alphasyllabary), where each base consonant carries an inherent vowel [a], modified by vowel diacritics (<em>matras</em>) or joined via virama (halant) into conjuncts (<em>sanyuktakshar</em>). Standard BPE tokenizers fail catastrophically on these morphological constructs:
  </p>
  <ul>
    <li><strong>Matra Detachment:</strong> The word <span class="devanagari">"भारत"</span> (Bharat / bha-ra-ta) requires 7 tokens in GPT-2 (<span class="code">['à¤', 'N-acute', 'à¤¾', 'à¤', '°', 'à¤', '¤']</span>). The aa-matra (<span class="devanagari">"ा"</span>) is detached from the consonant <span class="devanagari">"भ"</span> into an isolated byte fragment, destroying the phonetic syllable boundary.</li>
    <li><strong>Conjunct Splitting:</strong> The ligature in <span class="devanagari">"त्योहार"</span> (Tyohar / t-ya conjunct: <span class="devanagari">त् + य</span>) consumes 9 UTF-8 bytes. GPT-4 cl100k splits this single spoken syllable into 4 distinct tokens (<span class="code">['&lt;0xE0&gt;', '&lt;0xA4&gt;', '&lt;0xA4&gt;', '्यो']</span>).</li>
    <li><strong>Nasalisation (Anusvara):</strong> In <span class="devanagari">"संविधान"</span> (Samvidhan / Constitution), the dot diacritic (<span class="devanagari">"ं"</span>) is isolated into a trailing byte fragment in GPT-2 instead of binding to <span class="devanagari">"स"</span>.</li>
  </ul>

  <h2>6. Responsible AI</h2>
  <h3>6.1 Why the disparity appears (likely sources)</h3>
  <ul>
    <li><strong>Pretraining corpus imbalance:</strong> Web scrapes (Common Crawl) consist of &gt;85% English text. Devanagari n-grams rarely cross the frequency threshold required for subword merge creation during BPE training.</li>
    <li><strong>Greedy merge heuristics:</strong> Frequency-driven merge algorithms penalise non-Latin scripts because their global unigram frequency is orders of magnitude lower than English common words.</li>
    <li><strong>Fixed-size vocabulary allocation:</strong> Tokenizer budgets (e.g., 32k or 50k) are dominated by Latin subwords, punctuation, and code tokens, leaving minimal slots for South Asian scripts.</li>
  </ul>

  <h3>6.2 Guardrails & diagnostic thresholds</h3>
  <p>
    The probe incorporates automated diagnostic guardrails to flag biased tokenization:
  </p>
  <ul>
    <li><strong>Byte-fallback alert:</strong> When byte fragments (<span class="code">&lt;0x..&gt;</span>) exceed 15% of total tokens, a warning banner alerts the user that subword embeddings will suffer from information loss.</li>
    <li><strong>Perplexity threshold:</strong> When GPT-2 perplexity exceeds 200.0, the UI flags high model uncertainty and linguistic misalignment.</li>
    <li><strong>Fertility guardrail:</strong> Fertility &gt; 3.0 tokens/word is flagged as a high-cost generation hazard, recommending migration to an Indic-optimized model like MuRIL or GPT-4o.</li>
  </ul>

  <h3>6.3 Licence and IP note</h3>
  <p>
    All underlying models and libraries are utilized in full compliance with their respective open-source licenses: GPT-2 (MIT License), BERT & MuRIL (Apache 2.0), XLM-RoBERTa (MIT), tiktoken (MIT), and Llama-3.3 / Whisper via Groq API under Groq terms of service. All sample corpora and evaluations are published strictly for educational and academic research. No proprietary keys are committed to source control.
  </p>

  <h2>7. Limitations</h2>
  <ul>
    <li><strong>Single language model for probability scoring:</strong> GPT-2 is the sole causal LM used for token probabilities (U1) due to free-tier CPU memory constraints (512MB RAM ceiling on Render). Larger causal models like Llama-3 or Mistral could not be hosted locally on free CPU tiers.</li>
    <li><strong>Corpus scale:</strong> Benchmark statistics are computed on representative multi-sentence parallel paragraphs rather than gigabyte-scale corpora.</li>
    <li><strong>Whisper voice input dependency:</strong> Real-time microphone transcription depends on external Groq API availability; an automated synthetic fallback is provided when the API key is not configured.</li>
  </ul>
</div>

<!-- ==================== PAGE 6 ==================== -->
<div class="page">
  <div class="header-strip">
    <span>20_Kaustubh_Manjarekar_P20 | Generative AI CA Mini Project</span>
    <span>Page 6</span>
  </div>

  <p>
    <strong>Hosting constraints:</strong> On Render's free tier, the web service spins down after 15 minutes of inactivity and requires 30–50 seconds on cold start. The application incorporates resilient client-side precomputed benchmark caches so the dashboard remains interactive immediately upon page load.
  </p>

  <h2>8. Conclusion</h2>
  <p>
    The IndicToken benchmark demonstrates that tokenizer unfairness is a significant, measurable tax on Indian-language LLM users. Commercial BPE tokenizers like GPT-4 cl100k inflate token consumption by <strong>5.30x for Hindi and 5.36x for Marathi</strong>, resulting in:
  </p>
  <ul>
    <li><strong>Direct economic inflation:</strong> Indian users pay more than 5x higher API inference fees for equivalent information content.</li>
    <li><strong>Severe context shrinkage:</strong> Inside a 128k context window, English users can submit ~109,000 words, whereas Hindi users hit context overflow at only ~25,000 words.</li>
    <li><strong>Attention and latency degradation:</strong> Over-segmentation increases transformer decoding steps by 5x, increasing latency and diluting self-attention weights across meaningless byte fragments.</li>
  </ul>
  <p>
    Crucially, the success of <strong>Google MuRIL (1.17x multiplier, 1.06 fertility)</strong> and <strong>GPT-4o (1.48x multiplier)</strong> proves that tokenizer unfairness is completely solvable. By expanding vocabulary size and deliberately reserving token quotas for South Asian scripts, foundational model developers can eliminate the token tax without architectural changes.
  </p>
  <p>
    <strong>Future Work:</strong> Expanding the benchmark to Dravidian language scripts (Tamil, Telugu, Kannada, Malayalam), evaluating byte-latent models (MegaByte, MambaByte) that bypass subwords entirely, and integrating LoRA fine-tuning on bilingual parallel text.
  </p>

  <h2>9. Deliverables and Links</h2>
  <table>
    <tr>
      <th style="width: 25%;">Deliverable</th>
      <th>Location</th>
    </tr>
    <tr>
      <td><strong>Live Web Application</strong></td>
      <td><a href="https://indic-token-explorer.onrender.com">https://indic-token-explorer.onrender.com</a></td>
    </tr>
    <tr>
      <td><strong>GitHub Repository</strong></td>
      <td><a href="https://github.com/Frenzy-codes/IndicToken-Tokenizer-Explorer-Cost-Fairness-Benchmark">https://github.com/Frenzy-codes/IndicToken-Tokenizer-Explorer-Cost-Fairness-Benchmark</a></td>
    </tr>
    <tr>
      <td><strong>Backend Source Code</strong></td>
      <td><span class="code">main.py</span> (FastAPI backend, lazy tokenizer caching, GPT-2 LM, Groq proxy)</td>
    </tr>
    <tr>
      <td><strong>Frontend Dashboard</strong></td>
      <td><span class="code">static/index.html</span> (Google Stitch Editorial-Tech UI, Chart.js, 5 tab modules)</td>
    </tr>
    <tr>
      <td><strong>Cloud Deployment</strong></td>
      <td><span class="code">render.yaml</span> (Render free-tier configuration), <span class="code">app.py</span> (Hugging Face Spaces)</td>
    </tr>
    <tr>
      <td><strong>Project Report (PDF & MD)</strong></td>
      <td><span class="code">20_Kaustubh_Manjarekar_P20.pdf</span>, <span class="code">REPORT.md</span></td>
    </tr>
    <tr>
      <td><strong>Demo Video (2–3 mins)</strong></td>
      <td>Screen recording walking through U1–U5 submitted in shared drive folder <span class="code">20_Kaustubh_Manjarekar</span></td>
    </tr>
  </table>

  <div style="margin-top: 25px; border-top: 1px solid #CBD5E1; padding-top: 8px; font-size: 7.8pt; color: #64748B; text-align: center;">
    20_Kaustubh_Manjarekar_P20 | Generative AI CA Mini Project — Page 6 of 6 · November 2026
  </div>
</div>

</body>
</html>
"""

# 3. Write HTML file
with open('20_Kaustubh_Manjarekar_P20.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print('Wrote 20_Kaustubh_Manjarekar_P20.html')

# 4. Generate PDF file via xhtml2pdf
output_pdf = '20_Kaustubh_Manjarekar_P20.pdf'
with open(output_pdf, 'wb') as f:
    status = pisa.CreatePDF(html_content, dest=f)

print('pisa error status:', status.err)
print('PDF file size:', round(os.path.getsize(output_pdf) / 1024, 1), 'KB')

reader = PdfReader(output_pdf)
print('Total pages in generated PDF:', len(reader.pages))

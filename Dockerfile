FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-download tokeniser and LM weights so cold start is instant
ENV HF_HOME=/tmp/hf
RUN python -c "\
from transformers import AutoTokenizer, AutoModelForCausalLM; \
AutoTokenizer.from_pretrained('gpt2'); \
AutoModelForCausalLM.from_pretrained('gpt2'); \
AutoTokenizer.from_pretrained('bert-base-uncased'); \
AutoTokenizer.from_pretrained('bert-base-multilingual-cased'); \
AutoTokenizer.from_pretrained('xlm-roberta-base'); \
AutoTokenizer.from_pretrained('google/muril-base-cased'); \
"

EXPOSE 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

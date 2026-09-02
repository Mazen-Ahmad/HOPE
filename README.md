# HOPE — Financial Query Router

> **Hopefully, it works.**

HOPE is a multi-stage NLP pipeline that takes a natural language finance query, decomposes it into atomic sub-queries, and routes each one to the appropriate specialist agent.

---

## How It Works

```
User Query
    │
    ▼
Stage 1 — Query Decomposition        (Ling LLM via OpenRouter)
    │  Splits compound queries into atomic sub-queries
    │
    ▼
Stage 2 — Structured Extraction      (Ling LLM via OpenRouter)
    │  Extracts financial_terms and query_type — logging/debug only
    │
    ▼
Stage 3 — SetFit Classification      (BAAI/bge-small-en-v1.5 + sklearn head)
    │  Routes each sub-query to one of 4 agents with a confidence score
    │
    ▼
Response: [{query, agent, confidence, extraction}]
```

### The 4 Agents

| Agent | Handles |
|---|---|
| `profitability_agent` | ROI, ROE, EBITDA, net income, margins, NIM, interest income |
| `liquidity_agent` | Current ratio, cash flow, working capital, LCR, NSFR, loan-to-deposit |
| `product_agent` | Product CRUD, pricing, SKUs, policies, catalog management |
| `knowledge_agent` | Definitions, greetings, general finance concepts, regulatory explanations |

---

## Model Choices & Rationale

### Stage 1 & 2 — `inclusionai/ling-3.0-flash-fin:free` (OpenRouter)
- Finance-domain LLM, free tier on OpenRouter
- Used for decomposition because it understands financial context well enough to avoid over-splitting trend/time-range queries (e.g. "monthly NIM trend over 2 months" stays as one query)
- Temperature = 0 for deterministic output

### Stage 3 — SetFit with `BAAI/bge-small-en-v1.5`
- **Why SetFit**: Designed for few-shot text classification. Achieves high accuracy with small datasets (400 rows here) by using contrastive fine-tuning on sentence pairs before training a lightweight sklearn head.
- **Why `bge-small-en-v1.5`**: Small (33M params), fast, strong semantic embeddings, well-suited for short finance queries.
- **Two components saved after training**:
  - `model.safetensors` — fine-tuned sentence transformer weights (127MB)
  - `model_head.pkl` — trained sklearn LogisticRegression head (13KB)
- **Training**: 200 rows, 80/20 stratified split, seed=42, 3 epochs, batch size 16. Achieved 100% validation accuracy.
- **Confidence threshold**: 0.75 — predictions below this log a warning but still return a result.

---

## Backend File Reference

### `app.py`
Flask entry point. Two routes:
- `POST /api/finance/route-query` — accepts `{query: string}`, returns `{sub_queries: [...]}`
- `GET /api/health` — health check

### `finance_router.py`
Orchestrates all three stages. `route_query(raw_query)` calls decompose → extract → classify for each sub-query and returns the final response dict.

Key detail: if the LLM returns an empty `sub_queries` list (e.g. for very short inputs like "hi"), it falls back to treating the raw query as a single sub-query so the classifier always gets a chance to run.

### `classifier.py`
SetFit inference wrapper.
- `_load_model()` — loads `SetFitModel` from `models/setfit_finance/` with LFS pointer detection (checks file sizes to catch git LFS pointer files being loaded instead of real binaries)
- `classify(sub_query)` — returns `ClassificationResult(agent, confidence)`
- Uses `model.predict()` for the label and `model_head.classes_` (alphabetical order) for mapping proba columns — **not** `model.labels` which follows a different order

### `extractor.py`
Stage 2 extraction using the Ling LLM. Returns `{financial_terms: [...], query_type: string}`. Output is logged for debugging only — it does not feed into the classifier.

### `taxonomy.json`
Config file defining:
- `query_types`: `["calculation", "lookup", "definition", "crud_action", "general"]`
- `signal_groups`: keyword lists for profitability, liquidity, product, and knowledge signals — used to guide the extractor prompt

### `finance_query_classification_dataset.csv`
Training data. 200 rows (after deduplication by sub-query), 4 classes balanced at 50 rows each:
- Columns: `id`, `raw_query`, `sub_query`, `financial_terms`, `query_type`, `correct_agent`
- Multi-query rows are split into separate sub-query rows (e.g. a compound query produces 2–3 rows with the same `raw_query` but different `sub_query` and `correct_agent`)

### `requirements.txt`
Key pinned versions:
- `transformers==4.44.2` — pinned to avoid incompatibility with `setfit==1.1.3`
- `sentence-transformers==3.3.1` — pinned for same reason
- `Pillow` — required by sentence-transformers image utilities

### `models/setfit_finance/`
Trained model directory tracked via Git LFS. Contains:
- `model.safetensors` — fine-tuned transformer weights (127MB, LFS)
- `model_head.pkl` — sklearn LogisticRegression head (13KB, LFS)
- Supporting config/tokenizer files

### `.env`
Not committed. Must contain:
```
OPENROUTER_API_KEY=your_key_here
```

### `eval_only.py`
Standalone evaluation script (gitignored). Loads the trained model and runs it against the validation split to print accuracy, classification report, and confusion matrix.

---

## Setup — Fork & Run Locally

### Prerequisites
- Python 3.11
- Node.js 18+
- Git with Git LFS installed (`git lfs install`)

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_USERNAME/HOPE.git
cd HOPE
git lfs pull
```

`git lfs pull` is required to download the actual model files. Without it you get 134-byte pointer files instead of the real binaries.

### 2. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

Create `.env` in the `backend/` folder:
```
OPENROUTER_API_KEY=your_openrouter_key_here
```

Get a free key at [openrouter.ai](https://openrouter.ai). The model used (`inclusionai/ling-3.0-flash-fin:free`) is on the free tier — limit is 50 requests/day.

Start the backend:
```bash
python app.py
```

### 3. Frontend
```bash
cd frontend
npm install
```

Create `.env.local` in the `frontend/` folder:
```
VITE_BACKEND_URL=http://localhost:5000
```

Start the frontend:
```bash
npm run dev
```

Open `http://localhost:5173`.

---

## Retraining the Model

Retrain when you've collected enough anomalies to batch-add to the dataset.

### When to Retrain
- A query is routed to the wrong agent with high confidence
- A new financial concept appears that isn't covered (e.g. NIM was missing initially)
- A new query type needs to be added

### Steps

**1. Add anomalies to the CSV**

Open `backend/finance_query_classification_dataset.csv` and append new rows following the existing format:
```
id,raw_query,sub_query,financial_terms,query_type,correct_agent
PROF_0101,Your query here,Your sub-query here,relevant term,calculation,profitability_agent
```

Rules:
- Keep classes balanced — add roughly equal rows per agent
- If a compound query produces multiple sub-queries, add one row per sub-query with the same `raw_query`
- `correct_agent` must be one of: `profitability_agent`, `liquidity_agent`, `product_agent`, `knowledge_agent`

**2. Retrain**
```bash
cd backend
python classifier.py
```

This will:
- Do an 80/20 stratified split (seed=42)
- Fine-tune `BAAI/bge-small-en-v1.5` using SetFit contrastive training
- Train the sklearn LogisticRegression head
- Save the model to `models/setfit_finance/`
- Print validation accuracy, classification report, and confusion matrix

Training takes 4–5 hours on CPU.

**3. Verify**

Check the printed validation accuracy and confusion matrix. Pay attention to profitability ↔ liquidity confusion — those two are the most similar semantically.

**4. Commit the new model**

```bash
git add backend/models/setfit_finance/ backend/finance_query_classification_dataset.csv
git commit -m "Retrain: add NIM and regulatory query examples"
git push origin main
```

Git LFS handles `model.safetensors` and `model_head.pkl` automatically via `.gitattributes`.

---

## Known Anomalies (Pending Next Retrain)

| Query | Expected | Got | Reason |
|---|---|---|---|
| "monthly trend of net interest margin" | `profitability_agent` | misclassified | NIM not in original training data — fixed in v2 dataset |
| "What policies are banks required to have for customer service?" | `knowledge_agent` | `product_agent` | Regulatory/policy queries were missing — fixed in v2 dataset |

---

## Environment Variables Summary

| Variable | Where | Required | Description |
|---|---|---|---|
| `OPENROUTER_API_KEY` | `backend/.env` | Yes | OpenRouter API key for Ling LLM |
| `VITE_BACKEND_URL` | `frontend/.env.local` | Yes (prod) | Backend URL for frontend to call |

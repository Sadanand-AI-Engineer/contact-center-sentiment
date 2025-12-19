# Contact Center Sentiment Analysis (Async LLM Pipeline)

A production-style, async sentiment analysis pipeline for contact-center conversations using **Python**, **Ollama (local LLMs)**, and **batched concurrency**.  
Designed to demonstrate real-world data engineering and applied AI patterns such as async execution, throughput optimization, and operational metrics.

---

## 🔍 Project Overview

This project analyzes customer sentiment from contact-center conversations by:
- Extracting **customer-only messages**
- Running **local LLM inference** via Ollama
- Processing data using **async + batch + parallel execution**
- Capturing **latency, throughput, and system metrics**
- Producing **analytics-ready outputs (CSV + JSON)**

The architecture mirrors how large-scale NLP pipelines are built in production systems.

---

##  Key Features

- **Async + Parallel Processing**
  - Uses `asyncio` + `aiohttp`
  - Configurable concurrency limits to protect system resources

- **Batch-Oriented Execution**
  - Conversations processed in batches for predictable throughput
  - Per-batch timing and performance tracking

- **Local LLM Inference (Ollama)**
  - No external API dependency
  - Supports models like `llama3.2`, `phi3`, `mistral`

- **Resilient JSON Parsing**
  - Handles imperfect LLM outputs
  - Gracefully falls back to raw model output when parsing fails

- **Operational Metrics**
  - Per-conversation latency
  - Batch throughput
  - CPU & memory snapshots

- **Production-Style Code Structure**
  - Engine-driven execution
  - Clear separation of responsibilities across modules

---


## 📂 Project Structure

contact-center-sentiment
- engine.py — Main entry point (run this file)
- config.py — Central configuration
- data_processing.py — CSV loading & conversation structuring
- ollama_client.py — Async Ollama inference client
- batch_runner.py — Batch + concurrency orchestration
- metrics.py — Output writing & run statistics
- requirements.txt — Python dependencies
- synthetic_conversations_1M_input.csv
- README.md


---

## ⚙️ Setup Instructions (Windows / VS Code)

### 1️⃣ Prerequisites
- Python **3.10+**
- Ollama installed and running  
  ```bash
  ollama run llama3.2

2️⃣ Clone the Repository
git clone https://github.com/Sadanand-AI-Engineer/contact-center-sentiment.git
cd contact-center-sentiment

3️⃣ Create & Activate Virtual Environment
python -m venv .venv
.venv\Scripts\Activate.ps1

4️⃣ Run the Pipeline
python engine.py


---The engine automatically installs missing dependencies from requirements.txt on first run.

📤 Output Files Explained

After execution, the following files are generated:

1️⃣ sentiment_results_ollama_optimized.csv

Clean, analytics-ready output

conversation_id

sentiment (positive / neutral / negative)

score (0–1 confidence)

summary (short explanation)

👉 Use this for dashboards, BI tools, or downstream analytics.

2️⃣ sentiment_results_ollama_optimized_full.csv

Full diagnostic output
Includes:

Raw LLM responses

Retry attempts

Per-conversation latency

Error flags (json_parse_failed, network errors)

👉 Useful for debugging and model behavior analysis.

3️⃣ batch_stats_ollama_optimized.csv

Batch-level performance metrics

Batch duration

Throughput (conversations/sec)

👉 Shows how performance scales with concurrency.

4️⃣ run_stats_ollama_optimized.json

Run-level metadata

Total runtime

Overall throughput

CPU & memory usage

System information

Useful for capacity planning and benchmarking.

**Design Decisions (Why This Matters)**

Customer-only text → focuses sentiment on customer experience

Character & message limits → reduces tokens, improves speed

Async + batching → mimics real production inference pipelines

Local LLMs → cost-free, privacy-friendly experimentation

👤 Author

Sadanand
AI / Data Engineering | Async pipelines | LLM systems | Python

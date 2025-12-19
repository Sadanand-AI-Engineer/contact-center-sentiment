# config.py

CSV_PATH = "synthetic_conversations_1M_input.csv"

MAX_CONVERSATIONS: int | None = 100

BATCH_SIZE = 8
CONCURRENCY_LIMIT = 4

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

MAX_CUSTOMER_MESSAGES = 6
MAX_CHARS = 600

OLLAMA_NUM_PREDICT = 64

SENTIMENT_PROMPT_TEMPLATE = """
You are a contact center quality analyst.

You will be given ONLY the customer's messages from a conversation with an agent.

Classify the OVERALL sentiment of the CUSTOMER as one of:
- positive
- neutral
- negative

Return ONLY valid JSON in this exact format, nothing else:

{{
  "sentiment": "positive" or "neutral" or "negative",
  "score": 0.0 to 1.0,
  "summary": "one short sentence explaining why"
}}

Customer messages:
{conversation_text}
"""


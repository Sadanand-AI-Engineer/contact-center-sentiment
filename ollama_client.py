# ollama_client.py
import asyncio
import json
import re
import time
from typing import Optional

import aiohttp

import config
from models import Conversation, SentimentResult
from data_processing import ConversationFormatter


class OllamaResponseParser:
    def try_parse_sentiment_json(self, raw_output: str) -> Optional[dict]:
        if not raw_output:
            return None

        text = raw_output.strip()

        if text.startswith("```"):
            text = re.sub(r"^```[a-zA-Z0-9]*", "", text).strip()
            text = re.sub(r"```$", "", text).strip()

        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start : end + 1]

        text = re.sub(r",\s*([}\]])", r"\1", text)

        try:
            return json.loads(text)
        except Exception:
            return None


class OllamaSentimentClient:
    def __init__(self) -> None:
        self.formatter = ConversationFormatter()
        self.parser = OllamaResponseParser()

    async def analyze_one(
        self,
        session: aiohttp.ClientSession,
        conversation: Conversation,
        max_retries: int = 2,
        timeout_sec: int = 60,
    ) -> SentimentResult:
        conv_text = self.formatter.format_customer_only(conversation)
        prompt = config.SENTIMENT_PROMPT_TEMPLATE.format(conversation_text=conv_text)

        payload = {
            "model": config.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": config.OLLAMA_NUM_PREDICT, "temperature": 0.2},
        }

        start_time = time.perf_counter()

        for attempt in range(1, max_retries + 1):
            try:
                async with session.post(config.OLLAMA_URL, json=payload, timeout=timeout_sec) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    raw_output = (data.get("response") or "").strip()

                    sentiment_obj = self.parser.try_parse_sentiment_json(raw_output)
                    latency = time.perf_counter() - start_time

                    if sentiment_obj is None:
                        print(f"[WARN] Could not strictly parse JSON for {conversation.conversation_id}.")
                        return SentimentResult(
                            conversation_id=conversation.conversation_id,
                            sentiment=None,
                            score=None,
                            summary=None,
                            raw_model_output=raw_output,
                            attempts=attempt,
                            latency_sec=latency,
                            error="json_parse_failed",
                        )

                    return SentimentResult(
                        conversation_id=conversation.conversation_id,
                        sentiment=sentiment_obj.get("sentiment"),
                        score=sentiment_obj.get("score"),
                        summary=sentiment_obj.get("summary"),
                        raw_model_output=raw_output,
                        attempts=attempt,
                        latency_sec=latency,
                        error=None,
                    )

            except Exception as e:
                print(f"[ERROR] Conversation {conversation.conversation_id}, attempt {attempt}: {e}")
                if attempt == max_retries:
                    latency = time.perf_counter() - start_time
                    return SentimentResult(
                        conversation_id=conversation.conversation_id,
                        sentiment=None,
                        score=None,
                        summary=None,
                        raw_model_output=None,
                        attempts=attempt,
                        latency_sec=latency,
                        error=str(e),
                    )
                await asyncio.sleep(1.0 * attempt)

        # Should never reach here
        latency = time.perf_counter() - start_time
        return SentimentResult(
            conversation_id=conversation.conversation_id,
            sentiment=None,
            score=None,
            summary=None,
            raw_model_output=None,
            attempts=max_retries,
            latency_sec=latency,
            error="unexpected_fallthrough",
        )

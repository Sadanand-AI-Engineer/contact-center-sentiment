# models.py
from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class Message:
    role: str
    text: str


@dataclass
class Conversation:
    conversation_id: str
    messages: List[Message]


@dataclass
class SentimentResult:
    conversation_id: str
    sentiment: Optional[str]
    score: Optional[float]
    summary: Optional[str]
    raw_model_output: Optional[str]
    attempts: int
    latency_sec: float
    error: Optional[str]


@dataclass
class BatchStat:
    batch_index: int
    records: int
    duration_sec: float
    throughput_conv_per_sec: float

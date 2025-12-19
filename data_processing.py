# data_processing.py
from typing import List
import pandas as pd

from models import Conversation, Message
import config


class ConversationLoader:
    def load_from_csv(self, csv_path: str) -> List[Conversation]:
        df = pd.read_csv(csv_path)

        if "turn_index" in df.columns:
            df = df.sort_values(by=["conversation_id", "turn_index"])

        conversations: List[Conversation] = []
        for conv_id, group in df.groupby("conversation_id"):
            messages: List[Message] = []
            for _, row in group.iterrows():
                messages.append(
                    Message(
                        role=str(row.get("role", "unknown")),
                        text=str(row.get("text", "")),
                    )
                )
            conversations.append(Conversation(conversation_id=str(conv_id), messages=messages))

        return conversations


class ConversationFormatter:
    def format_customer_only(self, conversation: Conversation) -> str:
        msgs = conversation.messages

        customer_msgs = [m for m in msgs if m.role.lower() == "customer"]
        if not customer_msgs:
            customer_msgs = msgs

        customer_msgs = customer_msgs[-config.MAX_CUSTOMER_MESSAGES:]

        text_joined = "\n".join(m.text.replace("\n", " ") for m in customer_msgs)

        if len(text_joined) > config.MAX_CHARS:
            text_joined = text_joined[-config.MAX_CHARS:]

        return text_joined

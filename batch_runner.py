# batch_runner.py
import time
from typing import List, Tuple, Dict, Any
import asyncio

import aiohttp

import config
from models import Conversation, SentimentResult, BatchStat
from ollama_client import OllamaSentimentClient


class BatchRunner:
    def __init__(self) -> None:
        self.client = OllamaSentimentClient()

    def _chunk(self, items: List[Conversation], size: int):
        for i in range(0, len(items), size):
            yield items[i : i + size]

    async def run(self, conversations: List[Conversation]) -> Tuple[List[SentimentResult], Dict[str, Any]]:
        results: List[SentimentResult] = []
        batch_stats: List[BatchStat] = []

        run_stats: Dict[str, Any] = {
            "total_conversations": len(conversations),
            "batch_size": config.BATCH_SIZE,
            "concurrency_limit": config.CONCURRENCY_LIMIT,
            "batches": [],
        }

        connector = aiohttp.TCPConnector(limit=config.CONCURRENCY_LIMIT)

        overall_start = time.perf_counter()
        async with aiohttp.ClientSession(connector=connector) as session:
            total = len(conversations)

            for batch_index, batch in enumerate(self._chunk(conversations, config.BATCH_SIZE), start=1):
                batch_start = time.perf_counter()
                print(f"Processing batch {batch_index} ({len(batch)} conversations)...")

                tasks = [self.client.analyze_one(session, conv) for conv in batch]
                batch_results = await asyncio.gather(*tasks, return_exceptions=False) # same as asyncio.gather but aiohttp-safe

                results.extend(batch_results)

                batch_end = time.perf_counter()
                duration = batch_end - batch_start
                throughput = len(batch) / duration if duration > 0 else 0.0

                print(
                    f"Finished batch {batch_index}. "
                    f"Time: {duration:.2f}s, Throughput: {throughput:.2f} conv/s, "
                    f"Total processed: {len(results)}/{total}"
                )

                bs = BatchStat(
                    batch_index=batch_index,
                    records=len(batch),
                    duration_sec=duration,
                    throughput_conv_per_sec=throughput,
                )
                batch_stats.append(bs)

                run_stats["batches"].append(
                    {
                        "batch_index": bs.batch_index,
                        "records": bs.records,
                        "duration_sec": bs.duration_sec,
                        "throughput_conv_per_sec": bs.throughput_conv_per_sec,
                    }
                )

        overall_end = time.perf_counter()
        total_duration = overall_end - overall_start
        run_stats["total_duration_sec"] = total_duration
        run_stats["overall_throughput_conv_per_sec"] = (
            len(conversations) / total_duration if total_duration > 0 else 0.0
        )

        return results, run_stats

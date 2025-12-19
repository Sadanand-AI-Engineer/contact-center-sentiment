# metrics.py
import json
from typing import Any, Dict, List

import pandas as pd
import psutil
import platform

from models import SentimentResult


class OutputWriter:
    def save_results(self, results: List[SentimentResult]) -> None:
        df = pd.DataFrame([r.__dict__ for r in results])

        df_simple = df[["conversation_id", "sentiment", "score", "summary"]]
        df_simple.to_csv("sentiment_results_ollama_optimized.csv", index=False)

        df.to_csv("sentiment_results_ollama_optimized_full.csv", index=False)

        print("Saved: sentiment_results_ollama_optimized.csv")
        print("Saved: sentiment_results_ollama_optimized_full.csv")

    def enrich_run_stats(self, run_stats: Dict[str, Any]) -> Dict[str, Any]:
        run_stats["system_info"] = {
            "platform": platform.platform(),
            "cpu_count_logical": psutil.cpu_count(logical=True),
            "cpu_count_physical": psutil.cpu_count(logical=False),
        }

        run_stats["cpu_percent_after_run"] = psutil.cpu_percent(interval=1.0)

        mem = psutil.virtual_memory()
        run_stats["memory_info"] = {
            "total_gb": mem.total / (1024 ** 3),
            "available_gb": mem.available / (1024 ** 3),
            "used_gb": mem.used / (1024 ** 3),
            "percent_used": mem.percent,
        }

        return run_stats

    def save_stats(self, run_stats: Dict[str, Any]) -> None:
        with open("run_stats_ollama_optimized.json", "w", encoding="utf-8") as f:
            json.dump(run_stats, f, indent=2)

        batch_stats_df = pd.DataFrame(run_stats["batches"])
        batch_stats_df.to_csv("batch_stats_ollama_optimized.csv", index=False)

        print("Saved: run_stats_ollama_optimized.json")
        print("Saved: batch_stats_ollama_optimized.csv")

# engine.py
import os
import sys
import subprocess



def ensure_dependencies():
    required = ["pandas", "aiohttp", "psutil"]

    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if not missing:
        return

    print(f"[SETUP] Missing packages detected: {missing}")
    print("[SETUP] Installing dependencies from requirements.txt...")

    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    print("[SETUP] Install complete. Restarting engine...")

    # Safer restart on Windows (handles spaces in paths)
    subprocess.check_call([sys.executable] + sys.argv)
    sys.exit(0)

ensure_dependencies()



ensure_dependencies()

import asyncio

import config
from data_processing import ConversationLoader
from batch_runner import BatchRunner
from metrics import OutputWriter


async def main() -> None:
    print(f"Loading conversations from {config.CSV_PATH}...")

    loader = ConversationLoader()
    conversations = loader.load_from_csv(config.CSV_PATH)

    print(f"Loaded {len(conversations)} conversations from file.")

    if config.MAX_CONVERSATIONS is not None and config.MAX_CONVERSATIONS < len(conversations):
        conversations = conversations[: config.MAX_CONVERSATIONS]
        print(f"Processing only first {config.MAX_CONVERSATIONS} conversations (speed/demo limit).")
    else:
        print("Processing all loaded conversations.")

    runner = BatchRunner()
    results, run_stats = await runner.run(conversations)

    writer = OutputWriter()
    writer.save_results(results)

    run_stats = writer.enrich_run_stats(run_stats)
    writer.save_stats(run_stats)

    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())

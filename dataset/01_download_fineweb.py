"""
Step 01: Download and prepare FineWeb dataset for language quality pre-training.
FineWeb provides high-quality general language data (5-10B tokens target).
We extract a subset suitable for reasoning model adaptation.
"""

import os
import json
import time
import logging
from pathlib import Path
from datasets import load_dataset

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def download_fineweb(output_file: str = "fineweb_raw.jsonl", max_samples: int = 100000) -> str:
    """
    Download FineWeb dataset and convert to our reasoning format.
    
    FineWeb is used for general language quality adaptation.
    We don't train reasoning here - just language foundation.
    """
    logger.info(f"Loading FineWeb from HuggingFace (subset: sample-10BT)...")
    
    # Load a manageable subset of FineWeb
    dataset = load_dataset("HuggingFaceFW/fineweb", "sample-10BT", split="train", streaming=True)
    
    count = 0
    written = 0
    with open(OUTPUT_DIR / output_file, "w", encoding="utf-8") as f:
        for item in dataset:
            count += 1
            
            # Extract text content
            text = item.get("text", "")
            if not text or len(text) < 200:  # Skip very short samples
                continue
            
            # Create a reasoning-style sample from general text
            # For FineWeb, we use the text as-is for language adaptation
            sample = {
                "source": "fineweb",
                "domain": "general_language",
                "text": text[:4096],  # Truncate to sequence length
                "tokens_est": len(text.split()),
                "reasoning_type": "none",  # No reasoning, pure language
            }
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            written += 1
            
            if written % 10000 == 0:
                logger.info(f"  Written {written} samples ({count} seen).")
            
            if written >= max_samples:
                break
    
    logger.info(f"FineWeb download complete: {written} samples written to {output_file}")
    return str(OUTPUT_DIR / output_file)


def estimate_tokens(jsonl_file: str) -> int:
    """Estimate total tokens in a JSONL file."""
    total = 0
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            sample = json.loads(line)
            total += sample.get("tokens_est", len(sample.get("text", "").split()))
    return total


def main():
    logger.info("=" * 60)
    logger.info("Step 01: FineWeb Language Quality Dataset")
    logger.info("=" * 60)
    
    output_file = download_fineweb()
    tokens = estimate_tokens(output_file)
    
    logger.info(f"Estimated tokens: {tokens:,}")
    logger.info(f"Target: 5-10B tokens (this is a sample for development)")
    logger.info(f"Output: {output_file}")
    
    return output_file


if __name__ == "__main__":
    main()

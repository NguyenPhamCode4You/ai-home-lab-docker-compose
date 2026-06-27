"""
Step 08: Merge all dataset sources into a single unified dataset.
Applies the target ratios: 30% code, 25% debugging, 20% engineering, 15% synthetic, 10% natural language.
"""

import os
import json
import random
import logging
from pathlib import Path
from collections import Counter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── Dataset composition ratios ───────────────────────────────────────────
TARGET_RATIOS = {
    "code_reasoning": 0.30,
    "debugging": 0.25,
    "engineering": 0.20,
    "synthetic_reasoning": 0.15,
    "natural_language": 0.10,
}

# ─── Source to domain mapping ───────────────────────────────────────────
SOURCE_TO_DOMAIN = {
    # Code reasoning sources
    "the_stack": "code_reasoning",
    "code_search_net": "code_reasoning",
    "apps": "code_reasoning",
    # Debugging sources
    "swe_bench": "debugging",
    "swe_bench_synthetic": "debugging",
    # Engineering sources
    "github_pr": "engineering",
    "github_pr_synthetic": "engineering",
    "stackoverflow": "engineering",
    "stackoverflow_synthetic": "engineering",
    # Synthetic reasoning
    "synthetic": "synthetic_reasoning",
    # Natural language
    "natural_language_synthetic": "natural_language",
    # FineWeb (general language)
    "fineweb": "natural_language",
}


def count_samples_in_file(filepath: Path) -> int:
    """Count the number of samples in a JSONL file."""
    if not filepath.exists():
        return 0
    count = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for _ in f:
            count += 1
    return count


def load_samples(filepath: Path, max_samples: int = None) -> list:
    """Load samples from a JSONL file."""
    samples = []
    if not filepath.exists():
        return samples
    
    count = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if max_samples and count >= max_samples:
                break
            try:
                sample = json.loads(line.strip())
                samples.append(sample)
                count += 1
            except json.JSONDecodeError:
                continue
    return samples


def merge_datasets(total_samples: int = 100000) -> str:
    """
    Merge all dataset sources into a single unified dataset.
    
    Applies target ratios to balance the dataset composition.
    """
    logger.info("=" * 60)
    logger.info("Merging all dataset sources")
    logger.info("=" * 60)
    
    # Calculate target counts per domain
    domain_targets = {domain: int(total_samples * ratio) for domain, ratio in TARGET_RATIOS.items()}
    # Adjust to hit exact total
    diff = total_samples - sum(domain_targets.values())
    domain_targets[list(domain_targets.keys())[0]] += diff
    
    logger.info("Target distribution:")
    for domain, count in domain_targets.items():
        logger.info(f"  {domain}: {count} samples ({domain/count/total_samples*100:.1f}%)")
    
    # Collect all source files by domain
    domain_files = {domain: [] for domain in TARGET_RATIOS}
    
    for source_file in OUTPUT_DIR.glob("*.jsonl"):
        source_name = source_file.stem.lower()
        
        # Determine domain from filename
        domain = None
        for key in SOURCE_TO_DOMAIN:
            if key in source_name:
                domain = SOURCE_TO_DOMAIN[key]
                break
        
        if domain and source_file.exists():
            sample_count = count_samples_in_file(source_file)
            if sample_count > 0:
                domain_files[domain].append((source_file, sample_count))
                logger.info(f"  Found: {source_file.name} ({sample_count} samples) -> {domain}")
    
    # Load samples from each domain
    all_samples = {}
    for domain in TARGET_RATIOS:
        all_samples[domain] = []
        for filepath, count in domain_files[domain]:
            samples = load_samples(filepath)
            all_samples[domain].extend(samples)
            logger.info(f"  Loaded {len(samples)} samples from {filepath.name}")
    
    # Sample each domain to match target ratios
    merged_samples = []
    for domain, target_count in domain_targets.items():
        available = all_samples.get(domain, [])
        if not available:
            logger.warning(f"  No samples available for domain: {domain}")
            continue
        
        if len(available) > target_count:
            # Randomly sample to target count
            sampled = random.sample(available, target_count)
            logger.info(f"  Sampled {len(sampled)} from {len(available)} available ({domain})")
        else:
            sampled = available
            logger.info(f"  Using all {len(sampled)} samples ({domain})")
        
        merged_samples.extend(sampled)
    
    # Shuffle the final dataset
    random.shuffle(merged_samples)
    
    # Write merged dataset
    output_file = OUTPUT_DIR / "merged_dataset.jsonl"
    with open(output_file, "w", encoding="utf-8") as f:
        for sample in merged_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
    
    # Print distribution statistics
    domain_counts = Counter(s.get("source", "unknown") for s in merged_samples)
    logger.info(f"\nMerged dataset written to: {output_file}")
    logger.info(f"Total samples: {len(merged_samples)}")
    logger.info("\nSource distribution:")
    for source, count in domain_counts.most_common():
        logger.info(f"  {source}: {count}")
    
    return str(output_file)


def main():
    total_samples = 100000  # Adjust as needed
    output_file = merge_datasets(total_samples)
    logger.info(f"\nDone! Merged dataset: {output_file}")
    return output_file


if __name__ == "__main__":
    main()

# Reasoning Model Dataset Generator

This folder contains scripts to generate a complete dataset for training a small reasoning model (<1B parameters) based on the design document for training a model to produce high-quality reasoning plans.

## Design Overview

The goal is to train a model to produce structured reasoning plans, NOT to solve problems directly. The model learns:

- **Observation** → **Hypothesis** → **Verification** → **Result** → **Revision**
- Decomposition, planning, debugging workflow
- Backtracking, hypothesis generation, elimination
- Alternative approaches, decision trees

## Dataset Composition

| Domain              | Ratio | Source                                       |
| ------------------- | ----- | -------------------------------------------- |
| Code Reasoning      | 30%   | The Stack v2, CodeSearchNet, APPS            |
| Debugging           | 25%   | SWE-bench (real GitHub bugs)                 |
| Engineering         | 20%   | GitHub PR discussions, Stack Overflow        |
| Synthetic Reasoning | 15%   | Generated from engineering workflows         |
| Natural Language    | 10%   | Technical docs, incident reports, blog posts |

## Pipeline Steps

```
Step 01: FineWeb (language quality)          → 5-10B tokens target
Step 02: Code Reasoning (Stack, CodeSearchNet, APPS)
Step 03: SWE-bench (real GitHub bugs)
Step 04: GitHub PR Discussions
Step 05: Stack Overflow Discussions
Step 06: Synthetic Reasoning (largest source)
Step 07: Natural Language Reasoning
Step 08: Merge all sources into unified dataset
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the full pipeline

```bash
python run_pipeline.py
```

### 3. Run with custom options

```bash
# Target specific sample count
python run_pipeline.py --total-samples 200000

# Skip certain steps
python run_pipeline.py --skip-steps 01,02

# Resume from last failed step
python run_pipeline.py --resume
```

## Output

All outputs go to `dataset/output/`:

```
output/
├── fineweb_raw.jsonl                    # Step 01
├── the_stack_reasoning.jsonl            # Step 02
├── code_searchnet_reasoning.jsonl       # Step 02
├── apps_reasoning.jsonl                 # Step 02
├── swe_bench_reasoning.jsonl            # Step 03
├── github_pr_reasoning.jsonl            # Step 04
├── stackoverflow_reasoning.jsonl        # Step 05
├── synthetic_reasoning.jsonl            # Step 06
├── natural_language_reasoning.jsonl     # Step 07
└── merged_dataset.jsonl                 # Step 08 (final)
```

## Training Configuration (from design doc)

```python
target_model = "Qwen3-0.6B"
lora_rank = 64
lora_alpha = 128
dropout = 0.0
sequence_length = 4096
learning_rate = 2e-4
epochs = 2
micro_batch_size = 2
gradient_accumulation = 16
effective_batch_size = 32
optimizer = "AdamW8bit"
scheduler = "cosine"
warmup_ratio = 0.03
```

## Reasoning Format

Training samples follow this structure:

```json
{
  "source": "swe_bench",
  "domain": "debugging",
  "problem": "Docker container exits immediately after startup.",
  "reasoning_type": "engineering_debugging",
  "reasoning": "Observation:\nContainer exits instantly.\n\nPossible causes:\n- ENTRYPOINT finished\n- crash\n- missing dependency\n\nCheck:\n1. docker logs <container_id>\n2. docker inspect for exit code\n\nHypothesis:\nENTRYPOINT script completes without running the app.\n\nVerification:\ndocker logs shows empty output, exit code 0.\n\nResult:\nContainer exited cleanly, not a crash.\n\nHypothesis rejected:\nApplication crash is not the cause.\n\nNew hypothesis:\nThe ENTRYPOINT script has a bug.\n\nAlternative plan:\nFix ENTRYPOINT to use exec form.\n\nNext investigation:\nReview Dockerfile ENTRYPOINT."
}
```

## Key Design Decisions

1. **No direct CoT datasets** - Most CoT datasets contain fake reasoning ("Hmm... Let's think..."). We train on real engineering workflows instead.

2. **Reasoning only, no answers** - Train on `Problem → Reasoning`, NOT `Problem → Answer`. The model learns to reason, not to solve.

3. **Self-correction patterns** - Include hypothesis → verification → revision cycles to teach backtracking.

4. **Real engineering data** - SWE-bench, GitHub PRs, and Stack Overflow discussions contain authentic reasoning patterns.

5. **Synthetic data for scale** - Generate millions of samples following real engineering patterns for the bulk of training data.

## Files

| File                                 | Description                                        |
| ------------------------------------ | -------------------------------------------------- |
| `config.py`                          | Configuration for all datasets and training params |
| `01_download_fineweb.py`             | FineWeb language quality dataset                   |
| `02_download_code_reasoning.py`      | Code reasoning from Stack, CodeSearchNet, APPS     |
| `03_download_swe_bench.py`           | SWE-bench engineering debugging                    |
| `04_download_github_pr.py`           | GitHub PR discussions                              |
| `05_download_stackoverflow.py`       | Stack Overflow discussions                         |
| `06_generate_synthetic_reasoning.py` | Synthetic reasoning (largest source)               |
| `07_generate_natural_language.py`    | Natural language reasoning                         |
| `08_merge_datasets.py`               | Merge all sources with target ratios               |
| `run_pipeline.py`                    | Master pipeline entry point                        |
| `requirements.txt`                   | Python dependencies                                |
| `README.md`                          | This file                                          |

## Next Steps After Dataset Generation

1. Review `merged_dataset.jsonl` for quality
2. Split into train/val/test sets
3. Format for Unsloth training
4. Train with LoRA (r=64, alpha=128)
5. Evaluate on reasoning benchmarks

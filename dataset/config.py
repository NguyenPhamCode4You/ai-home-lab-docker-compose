"""
Configuration for dataset generation pipeline.
Defines sources, ratios, output paths, and processing parameters.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

# ─── Base paths ───────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = BASE_DIR / "output"
RAW_DIR = BASE_DIR / "raw"
TEMP_DIR = BASE_DIR / "temp"

# ─── Dataset composition ratios ───────────────────────────────────────────────
# Target: 30% code, 25% debugging, 20% engineering, 15% synthetic reasoning, 10% natural language
DATASET_RATIOS = {
    "code_reasoning": 0.30,
    "debugging": 0.25,
    "engineering": 0.20,
    "synthetic_reasoning": 0.15,
    "natural_language": 0.10,
}

# ─── Training target ─────────────────────────────────────────────────────────
TRAINING_CONFIG = {
    "target_model": "Qwen3-0.6B",
    "lora_rank": 64,
    "lora_alpha": 128,
    "dropout": 0.0,
    "sequence_length": 4096,
    "learning_rate": 2e-4,
    "epochs": 2,
    "micro_batch_size": 2,
    "gradient_accumulation": 16,
    "effective_batch_size": 32,
    "optimizer": "AdamW8bit",
    "scheduler": "cosine",
    "warmup_ratio": 0.03,
}

# ─── Reasoning format templates ───────────────────────────────────────────────
REASONING_FORMATS = {
    "observation_hypothesis": {
        "name": "Observation → Hypothesis → Verification",
        "template": """Observation:
{observation}

Possible causes:
- {cause_1}
- {cause_2}
- {cause_3}

Check:
{check}

Result:
{result}

Hypothesis rejected:
{rejected}

New hypothesis:
{new_hypothesis}

Next investigation:
{next_investigation}""",
    },
    "goal_plan": {
        "name": "Goal → Plan → Checkpoint",
        "template": """GOAL:
{goal}

KNOWN FACTS:
{known_facts}

UNKNOWNS:
{unknowns}

ASSUMPTIONS:
{assumptions}

PLAN:
{plan}

CHECKPOINT:
{checkpoint}

IF FAIL:
ALTERNATIVE PLAN:
{alternative_plan}

NEXT STEP:
{next_step}""",
    },
    "self_correction": {
        "name": "Reasoning v1 → Correction → Reasoning v2",
        "template": """REASONING V1:
Hypothesis:
{hypothesis_v1}

Verification:
{verification_v1}

Result:
{result_v1}

PROBLEM FOUND:
{problem_found}

CORRECTION:
{correction}

REASONING V2:
New hypothesis:
{hypothesis_v2}

Verification:
{verification_v2}

Result:
{result_v2}""",
    },
}

# ─── Data source configurations ───────────────────────────────────────────────
DATA_SOURCES = {
    "fineweb": {
        "name": "FineWeb",
        "description": "General language quality pre-training",
        "url": "https://huggingface.co/datasets/HuggingFaceFW/fineweb",
        "target_tokens": 5_000_000_000,  # 5B tokens
        "subsets": ["sample-10bt", "sample-100bt"],
        "output_file": "fineweb_tokens.jsonl",
    },
    "the_stack": {
        "name": "The Stack v2",
        "description": "Code reasoning - problem → reasoning extraction",
        "url": "https://huggingface.co/datasets/bigcode/the-stack",
        "languages": ["python", "javascript", "typescript", "go", "rust", "java", "csharp"],
        "output_file": "code_reasoning.jsonl",
        "max_examples": 20000,
    },
    "codesearchnet": {
        "name": "CodeSearchNet",
        "description": "Code search pairs for reasoning extraction",
        "url": "https://huggingface.co/datasets/code_search_net",
        "output_file": "code_searchnet_reasoning.jsonl",
        "max_examples": 10000,
    },
    "apps": {
        "name": "APPS",
        "description": "Programming problems with reasoning paths",
        "url": "https://huggingface.co/datasets/hendrycks/apps",
        "output_file": "apps_reasoning.jsonl",
        "max_examples": 10000,
    },
    "swe_bench": {
        "name": "SWE-bench",
        "description": "Real GitHub bugs - issue → reasoning (ignore patch)",
        "url": "https://huggingface.co/datasets/princeton-nlp/SWE-bench",
        "output_file": "swe_bench_reasoning.jsonl",
        "split": "full",
        "max_examples": 5000,
    },
    "github_pr": {
        "name": "GitHub PR Discussions",
        "description": "PR review discussions with reasoning patterns",
        "url": "https://huggingface.co/datasets/CodeFeedback/PR-Dataset",
        "output_file": "github_pr_reasoning.jsonl",
        "max_examples": 10000,
    },
    "stackoverflow": {
        "name": "Stack Overflow",
        "description": "Comments, discussions, alternative solutions, failures",
        "url": "https://huggingface.co/datasets/fka/awesome-stackoverflow",
        "output_file": "stackoverflow_reasoning.jsonl",
        "max_examples": 10000,
    },
}

# ─── Synthetic reasoning generation config ────────────────────────────────────
SYNTHETIC_CONFIG = {
    "num_samples": 50000,
    "domains": [
        "software_debugging",
        "devops_infrastructure",
        "api_integration",
        "database_troubleshooting",
        "performance_optimization",
        "security_vulnerability",
        "deployment_failure",
        "code_review",
        "architecture_decision",
        "incident_response",
    ],
    "llm_prompt": """Do NOT solve the problem. Only reason through it.

Generate structured reasoning with:
- Observation
- Hypothesis
- Alternative
- Failure mode
- Next investigation

Keep it in engineering workflow format.
Do not provide a final answer or solution.""",
}

# ─── Output format ────────────────────────────────────────────────────────────
OUTPUT_FORMAT = {
    "instruction": "reasoning",
    "input_prefix": "PROBLEM:\n{problem}",
    "output_prefix": "REASONING:\n{reasoning}",
    "separator": "\n\n",
}

# ─── Create directories ───────────────────────────────────────────────────────
def ensure_dirs():
    """Create all necessary directories."""
    for d in [OUTPUT_DIR, RAW_DIR, TEMP_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    for d in OUTPUT_DIR.iterdir():
        pass  # output dir is populated by scripts
    return BASE_DIR, OUTPUT_DIR, RAW_DIR, TEMP_DIR


if __name__ == "__main__":
    ensure_dirs()
    print("Dataset configuration loaded successfully.")
    print(f"Base dir:      {BASE_DIR}")
    print(f"Output dir:    {OUTPUT_DIR}")
    print(f"Raw dir:       {RAW_DIR}")
    print(f"Temp dir:      {TEMP_DIR}")
    print(f"Target ratios: {DATASET_RATIOS}")
    print(f"Target model:  {TRAINING_CONFIG['target_model']}")

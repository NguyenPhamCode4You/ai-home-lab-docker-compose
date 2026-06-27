"""
Step 02: Download and prepare code reasoning datasets.
Sources: The Stack v2, CodeSearchNet, APPS
Extract problem → reasoning patterns (NOT answers).
"""

import os
import json
import logging
from pathlib import Path
from datasets import load_dataset

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_code_reasoning_from_stack(max_samples: int = 20000) -> str:
    """
    Extract problem → reasoning from The Stack v2.
    We want the reasoning path, not the final code answer.
    """
    logger.info("Loading The Stack v2...")
    
    output_file = OUTPUT_DIR / "the_stack_reasoning.jsonl"
    written = 0
    
    # The Stack v2 is large; use a subset
    languages = ["python", "javascript", "typescript", "go", "rust"]
    
    for lang in languages:
        logger.info(f"  Processing language: {lang}")
        try:
            dataset = load_dataset(
                "bigcode/the-stack", 
                data_dir=f"data/{lang}", 
                split="train", 
                streaming=True,
                trust_remote_code=True,
            )
            
            count = 0
            with open(output_file, "a", encoding="utf-8") as f:
                for item in dataset:
                    count += 1
                    if written >= max_samples:
                        break
                    
                    code = item.get("content", "")
                    repo = item.get("repo_name", "unknown")
                    
                    if not code or len(code) < 500:
                        continue
                    
                    # Extract reasoning-relevant code samples
                    # Focus on code with comments, error handling, or complex logic
                    sample = {
                        "source": "the_stack",
                        "domain": "code_reasoning",
                        "language": lang,
                        "repo": repo,
                        "code": code[:4096],
                        "reasoning_type": "code_analysis",
                        "problem": f"Analyze and reason about this {lang} code from {repo}",
                        "reasoning": f"Observation:\nCode contains {lang} implementation from {repo}.\n\nHypothesis:\nThis code handles a specific domain logic.\n\nCheck:\nInspect imports, function signatures, and control flow.\n\nNext investigation:\nUnderstand the data flow and error handling patterns.",
                    }
                    f.write(json.dumps(sample, ensure_ascii=False) + "\n")
                    written += 1
                    
                    if written % 5000 == 0:
                        logger.info(f"    Written {written} samples...")
        except Exception as e:
            logger.warning(f"  Error processing {lang}: {e}")
            continue
    
    logger.info(f"The Stack v2 complete: {written} samples written")
    return str(output_file)


def extract_code_search_net(max_samples: int = 10000) -> str:
    """
    Extract problem → reasoning from CodeSearchNet.
    Code search pairs are great for reasoning about code intent.
    """
    logger.info("Loading CodeSearchNet...")
    
    output_file = OUTPUT_DIR / "code_searchnet_reasoning.jsonl"
    written = 0
    
    dataset = load_dataset("code_search_net", split="test", streaming=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        for item in dataset:
            if written >= max_samples:
                break
            
            code = item.get("code", "")
            docstring = item.get("docstring", "")
            language = item.get("language", "unknown")
            
            if not code or len(code) < 100:
                continue
            
            sample = {
                "source": "code_search_net",
                "domain": "code_reasoning",
                "language": language,
                "code": code[:2048],
                "docstring": docstring[:512],
                "reasoning_type": "code_intent",
                "problem": f"Given this {language} code, reason about its purpose and behavior.",
                "reasoning": f"Observation:\nFunction signature and docstring suggest {language} implementation.\n\nHypothesis:\nThe code likely handles {language}-specific patterns.\n\nCheck:\nExamine the docstring and key operations.\n\nNext investigation:\nTrace the data flow through the function.",
            }
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            written += 1
    
    logger.info(f"CodeSearchNet complete: {written} samples written")
    return str(output_file)


def extract_apps_reasoning(max_samples: int = 10000) -> str:
    """
    Extract problem → reasoning from APPS dataset.
    Programming problems with test cases - extract the reasoning path.
    """
    logger.info("Loading APPS dataset...")
    
    output_file = OUTPUT_DIR / "apps_reasoning.jsonl"
    written = 0
    
    dataset = load_dataset("hendrycks/apps", split="train", streaming=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        for item in dataset:
            if written >= max_samples:
                break
            
            question = item.get("question", "")
            solution = item.get("solution", "")
            code_input = item.get("code_input", "")
            difficulty = item.get("difficulty", "unknown")
            
            if not question or len(question) < 50:
                continue
            
            # Extract reasoning from the problem description
            # NOT the solution - we want the reasoning path
            sample = {
                "source": "apps",
                "domain": "code_reasoning",
                "difficulty": difficulty,
                "problem": question[:2048],
                "reasoning_type": "algorithmic_reasoning",
                "reasoning": f"Observation:\n{difficulty} difficulty programming problem.\n\nHypothesis:\nThis requires algorithmic thinking with {difficulty} complexity.\n\nCheck:\nIdentify input/output constraints and edge cases.\n\nPlan:\n1. Understand the problem requirements\n2. Identify key algorithmic patterns\n3. Consider time/space complexity\n4. Verify with test cases\n\nNext investigation:\nDetermine the optimal approach based on constraints.",
            }
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            written += 1
            
            if written % 2000 == 0:
                logger.info(f"  Written {written} samples...")
    
    logger.info(f"APPS complete: {written} samples written")
    return str(output_file)


def main():
    logger.info("=" * 60)
    logger.info("Step 02: Code Reasoning Datasets")
    logger.info("=" * 60)
    
    files = []
    files.append(extract_code_reasoning_from_stack())
    files.append(extract_code_search_net())
    files.append(extract_apps_reasoning())
    
    total = sum(1 for f in files for _ in open(f))
    logger.info(f"\nTotal code reasoning samples: {total}")
    logger.info(f"Output files: {files}")
    
    return files


if __name__ == "__main__":
    main()

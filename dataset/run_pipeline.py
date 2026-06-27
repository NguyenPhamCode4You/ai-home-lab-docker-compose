"""
Master pipeline: Run all dataset generation steps in order.
This is the main entry point for generating the complete dataset.

Usage:
    python run_pipeline.py [--total-samples 100000] [--skip-steps 01,02]

Steps:
    01 - Download FineWeb (language quality)
    02 - Download code reasoning datasets (The Stack, CodeSearchNet, APPS)
    03 - Download SWE-bench (engineering debugging)
    04 - Download GitHub PR discussions
    05 - Download Stack Overflow discussions
    06 - Generate synthetic reasoning (largest source)
    07 - Generate natural language reasoning
    08 - Merge all sources into unified dataset
"""

import os
import sys
import json
import time
import logging
import argparse
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = BASE_DIR / "output"
PIPELINE_LOG = BASE_DIR / "pipeline_log.json"


def get_step_scripts():
    """Get all step scripts in order."""
    return [
        ("01_download_fineweb.py", "FineWeb Language Quality"),
        ("02_download_code_reasoning.py", "Code Reasoning (Stack, CodeSearchNet, APPS)"),
        ("03_download_swe_bench.py", "SWE-bench Engineering Debugging"),
        ("04_download_github_pr.py", "GitHub PR Discussions"),
        ("05_download_stackoverflow.py", "Stack Overflow Discussions"),
        ("06_generate_synthetic_reasoning.py", "Synthetic Reasoning"),
        ("07_generate_natural_language.py", "Natural Language Reasoning"),
        ("08_merge_datasets.py", "Merge All Sources"),
    ]


def run_step(script_name: str, description: str, skip: bool = False) -> bool:
    """Run a single pipeline step."""
    script_path = BASE_DIR / script_name
    
    if skip:
        logger.info(f"⊘ SKIPPED: {description}")
        return True
    
    if not script_path.exists():
        logger.error(f"✗ Script not found: {script_path}")
        return False
    
    logger.info(f"\n{'=' * 60}")
    logger.info(f"STEP: {description}")
    logger.info(f"Script: {script_name}")
    logger.info(f"{'=' * 60}")
    
    start_time = time.time()
    
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(BASE_DIR),
            capture_output=False,
            timeout=3600,  # 1 hour per step
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            logger.info(f"✓ COMPLETED in {elapsed:.1f}s")
            return True
        else:
            logger.error(f"✗ FAILED (exit code {result.returncode}) in {elapsed:.1f}s")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error(f"✗ TIMEOUT after 3600s")
        return False
    except Exception as e:
        logger.error(f"✗ ERROR: {e}")
        return False


def generate_pipeline_report(step_results: dict, total_time: float):
    """Generate a pipeline execution report."""
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_time_seconds": total_time,
        "total_time_minutes": total_time / 60,
        "steps": step_results,
        "summary": {
            "total_steps": len(step_results),
            "completed": sum(1 for v in step_results.values() if v),
            "failed": sum(1 for v in step_results.values() if not v),
        }
    }
    
    # Write report
    with open(PIPELINE_LOG, "w") as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    logger.info(f"\n{'=' * 60}")
    logger.info("PIPELINE SUMMARY")
    logger.info(f"{'=' * 60}")
    logger.info(f"Total time: {total_time/60:.1f} minutes")
    logger.info(f"Completed: {report['summary']['completed']}/{report['summary']['total_steps']} steps")
    
    if report['summary']['failed'] > 0:
        logger.warning(f"Failed steps: {report['summary']['failed']}")
        for step, success in step_results.items():
            if not success:
                logger.warning(f"  - {step}")
    else:
        logger.info("✓ All steps completed successfully!")
    
    logger.info(f"Report saved to: {PIPELINE_LOG}")
    
    return report


def main():
    parser = argparse.ArgumentParser(description="Dataset Generation Pipeline")
    parser.add_argument(
        "--total-samples",
        type=int,
        default=100000,
        help="Total samples for merged dataset (default: 100000)"
    )
    parser.add_argument(
        "--skip-steps",
        type=str,
        default="",
        help="Comma-separated step numbers to skip (e.g., '01,02')"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from last failed step"
    )
    args = parser.parse_args()
    
    skip_steps = set(args.skip_steps.split(",")) if args.skip_steps else set()
    
    logger.info("=" * 60)
    logger.info("DATASET GENERATION PIPELINE")
    logger.info("=" * 60)
    logger.info(f"Target samples: {args.total_samples:,}")
    logger.info(f"Skip steps: {skip_steps if skip_steps else 'None'}")
    logger.info(f"Output dir: {OUTPUT_DIR}")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check for resume
    step_results = {}
    start_steps = 0
    
    if args.resume and PIPELINE_LOG.exists():
        with open(PIPELINE_LOG, "r") as f:
            prev_report = json.load(f)
        
        logger.info(f"\nResuming from previous run...")
        for step, success in prev_report["steps"].items():
            step_results[step] = success
            if not success:
                start_steps = list(step_results.keys()).index(step)
                logger.info(f"  Will resume from step: {step}")
                break
    
    # Get all steps
    steps = get_step_scripts()
    
    total_start = time.time()
    
    for i, (script, description) in enumerate(steps):
        step_num = script.split("_")[0]
        
        # Skip already completed steps when resuming
        if step_num in step_results:
            run_step(script, description, skip=True)
            continue
        
        # Skip requested steps
        skip = step_num in skip_steps
        
        success = run_step(script, description, skip=skip)
        step_results[script] = success
        
        if not success and not skip:
            logger.warning(f"Stopping pipeline due to failure in {description}")
            break
    
    total_time = time.time() - total_start
    
    # Generate report
    report = generate_pipeline_report(step_results, total_time)
    
    # Check if merged dataset exists
    merged_file = OUTPUT_DIR / "merged_dataset.jsonl"
    if merged_file.exists():
        sample_count = sum(1 for _ in open(merged_file))
        file_size = merged_file.stat().st_size / (1024 * 1024)  # MB
        logger.info(f"\n✓ Final dataset: {merged_file}")
        logger.info(f"  Samples: {sample_count:,}")
        logger.info(f"  Size: {file_size:.1f} MB")
    
    return 0 if report['summary']['failed'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

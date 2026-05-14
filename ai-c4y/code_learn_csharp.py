"""
code_learn_csharp.py — Entry point for the BVMS C# Codebase RAG Pipeline.

Usage examples:
  python code_learn_csharp.py --phase index
  python code_learn_csharp.py --phase all
  python code_learn_csharp.py --phase index --focus "**/VoyageManagement/**"
  python code_learn_csharp.py --phase all --mode incremental
  python code_learn_csharp.py --phase all --mode incremental --changed-files "Core/Business/Foo.cs,Core/Domain/Bar.cs"
  git diff --name-only origin/main HEAD | python code_learn_csharp.py --phase all --mode incremental --from-stdin
  python code_learn_csharp.py --phase index --cloud
  python code_learn_csharp.py --phase all --cloud
"""

import argparse
import asyncio
import os
import sys

from dotenv import load_dotenv

load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser(
        description="BVMS C# Codebase RAG Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--phase",
        choices=["index", "document", "enrich", "synthesize", "all"],
        default="all",
        help="Phase(s) to run (default: all)",
    )
    parser.add_argument(
        "--mode",
        choices=["full", "incremental"],
        default="full",
        help="full = process all files; incremental = only changed files + their dependents",
    )
    parser.add_argument(
        "--focus",
        default=None,
        help="Comma-separated glob patterns — overrides CIA_FOCUS_ONLY_FILES for this run",
    )
    parser.add_argument(
        "--changed-files",
        default=None,
        help="Comma-separated changed .cs file paths for incremental mode",
    )
    parser.add_argument(
        "--from-stdin",
        action="store_true",
        help="Read changed file paths from stdin (one per line) — use with git diff output",
    )
    parser.add_argument(
        "--cloud",
        action="store_true",
        help="Force all LLM requests through OpenRouter (skips local Ollama entirely)",
    )
    return parser.parse_args()


async def main():
    args = parse_args()

    # Inline import here so load_dotenv() runs before any module-level os.getenv() calls
    from src.CSharpManifest import CSharpManifest
    from src.CSharpCodebaseWorkflow import (
        build_codebase_index,
        write_csharp_documents,
        enrich_with_cross_references,
        synthesize_workflow_documents,
        CSHARP_CODEBASE_PATH,
        DEFAULT_INDEX_PATH,
    )

    if args.focus:
        os.environ["CIA_FOCUS_ONLY_FILES"] = args.focus

    codebase_path = os.getenv("CIA_CODEBASE_PATH", CSHARP_CODEBASE_PATH)
    manifest = CSharpManifest()

    # ------------------------------------------------------------------
    # Incremental mode: reset changed files (+ dependents) in manifest
    # ------------------------------------------------------------------
    if args.mode == "incremental":
        changed: list[str] = []

        if args.from_stdin:
            changed = [line.strip() for line in sys.stdin if line.strip().endswith(".cs")]
        elif args.changed_files:
            changed = [f.strip() for f in args.changed_files.split(",") if f.strip()]
        else:
            raw = os.popen("git diff --name-only origin/main HEAD").read()
            changed = [ln.strip() for ln in raw.splitlines() if ln.strip().endswith(".cs")]

        if changed:
            print(f"[Incremental] {len(changed)} changed .cs file(s) detected.")
            expanded: set[str] = set(changed)
            if os.path.exists(DEFAULT_INDEX_PATH):
                try:
                    import json
                    with open(DEFAULT_INDEX_PATH, "r", encoding="utf-8") as f:
                        index = json.load(f)
                    for fp in changed:
                        expanded.update(manifest.get_dependents(fp, index))
                except Exception as exc:
                    print(f"[Incremental] Could not expand dependents: {exc}")

            if len(expanded) > 50:
                print(
                    f"[Incremental] WARNING: expanded to {len(expanded)} files (> 50). "
                    "Consider --mode=full for large changesets."
                )
            print(f"[Incremental] Resetting {len(expanded)} file(s) for re-processing.")
            for fp in expanded:
                manifest.reset_file(fp)
            manifest.save()
        else:
            print("[Incremental] No changed .cs files detected. Nothing to do.")
            return

    # ------------------------------------------------------------------
    # Phase execution
    # ------------------------------------------------------------------
    run_index     = args.phase in ("index", "all")
    run_document  = args.phase in ("document", "all")
    run_enrich    = args.phase in ("enrich", "all")
    run_synthesize = args.phase in ("synthesize", "all")

    if run_index:
        if not codebase_path:
            print("ERROR: CIA_CODEBASE_PATH is not set. Cannot run Phase 1.")
            sys.exit(1)
        await build_codebase_index(codebase_path=codebase_path, manifest=manifest, force_cloud=args.cloud)

    if run_document:
        if not codebase_path:
            print("ERROR: CIA_CODEBASE_PATH is not set. Cannot run Phase 2.")
            sys.exit(1)
        await write_csharp_documents(codebase_path=codebase_path, manifest=manifest, force_cloud=args.cloud)

    if run_enrich:
        await enrich_with_cross_references(manifest=manifest, force_cloud=args.cloud)

    if run_synthesize:
        await synthesize_workflow_documents(manifest=manifest)

    print("\n[Pipeline] Done.")


if __name__ == "__main__":
    asyncio.run(main())

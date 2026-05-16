"""
rag_learn_csharp.py — Entry point for the BVMS C# Codebase RAG Pipeline.

Usage examples:
  python rag_learn_csharp.py --phase index --cloud 25
  python rag_learn_csharp.py --phase document --cloud 25
  python rag_learn_csharp.py --phase enrich --cloud 25
  python rag_learn_csharp.py --phase synthesize --cloud 25
  python rag_learn_csharp.py --phase chunk
  python rag_learn_csharp.py --phase insert-quick --local 10 --table n8n_documents_bvms_code_quick


  python rag_learn_csharp.py --phase all
  python rag_learn_csharp.py --phase index --focus "**/VoyageManagement/**"
  python rag_learn_csharp.py --phase all --mode incremental
  python rag_learn_csharp.py --phase all --mode incremental --changed-files "Core/Business/Foo.cs,Core/Domain/Bar.cs"
  git diff --name-only origin/main HEAD | python rag_learn_csharp.py --phase all --mode incremental --from-stdin
  python rag_learn_csharp.py --phase index --cloud
  python rag_learn_csharp.py --phase index --cloud 5
  python rag_learn_csharp.py --phase all --cloud 3
  python rag_learn_csharp.py --phase index --local
  python rag_learn_csharp.py --phase index --local 3
  python rag_learn_csharp.py --phase chunk
  python rag_learn_csharp.py --phase insert
  python rag_learn_csharp.py --phase insert-quick
  python rag_learn_csharp.py --phase insert-quick --cloud 20
  python rag_learn_csharp.py --phase insert-quick --local 5 --table bvms-backend-v2
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
        choices=["index", "document", "enrich", "synthesize", "chunk", "insert", "insert-quick", "all"],
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
        nargs="?",
        const=1,
        type=int,
        default=None,
        metavar="N",
        help="Force all LLM calls through OpenRouter. Optional N sets concurrency (default: 1). Example: --cloud 5",
    )
    parser.add_argument(
        "--local",
        nargs="?",
        const=1,
        type=int,
        default=None,
        metavar="N",
        help="Force all LLM calls through local Ollama. Optional N sets concurrency (default: 1). Example: --local 3",
    )
    parser.add_argument(
        "--table",
        default=None,
        metavar="TABLE_NAME",
        help="Override the target Supabase table for insert / insert-quick (default: CIA_RAG_TABLE_NAME env var).",
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
        chunk_for_rag,
        insert_rag_chunks,
        insert_rag_chunks_quick,
        CSHARP_CODEBASE_PATH,
        DEFAULT_INDEX_PATH,
    )

    if args.focus:
        os.environ["CIA_FOCUS_ONLY_FILES"] = args.focus

    if args.cloud and args.local:
        print("ERROR: --cloud and --local are mutually exclusive.")
        sys.exit(1)

    force_cloud = args.cloud is not None
    force_local = args.local is not None
    concurrency = args.cloud if force_cloud else (args.local if force_local else 1)

    if force_cloud:
        from src.agents.models.OpenRouter import OpenRouter as _OR
        _OR.set_concurrency(concurrency)
        print(f"[Cloud] Routing all LLM calls to OpenRouter (concurrency={concurrency})")
    elif force_local:
        print(f"[Local] Routing all LLM calls to Ollama (concurrency={concurrency})")

    codebase_path = os.getenv("CIA_CODEBASE_PATH", CSHARP_CODEBASE_PATH)
    manifest = CSharpManifest()
    incremental_files: list[str] | None = None  # None = full mode (no restriction)

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
            incremental_files = list(expanded)
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
    run_chunk     = args.phase in ("chunk", "all")
    run_insert    = args.phase in ("insert", "all")
    run_insert_quick = args.phase in ("insert-quick",)

    if run_index:
        if not codebase_path:
            print("ERROR: CIA_CODEBASE_PATH is not set. Cannot run Phase 1.")
            sys.exit(1)
        await build_codebase_index(codebase_path=codebase_path, manifest=manifest, force_cloud=force_cloud, force_local=force_local, concurrency=concurrency, focus_patterns=incremental_files)

    if run_document:
        if not codebase_path:
            print("ERROR: CIA_CODEBASE_PATH is not set. Cannot run Phase 2.")
            sys.exit(1)
        await write_csharp_documents(codebase_path=codebase_path, manifest=manifest, force_cloud=force_cloud, force_local=force_local, concurrency=concurrency)

    if run_enrich:
        await enrich_with_cross_references(manifest=manifest, force_cloud=force_cloud, force_local=force_local, concurrency=concurrency)

    if run_synthesize:
        await synthesize_workflow_documents(manifest=manifest, force_cloud=force_cloud, force_local=force_local, concurrency=concurrency)

    if run_chunk:
        await chunk_for_rag()

    if run_insert:
        await insert_rag_chunks(force_cloud=force_cloud, force_local=force_local, concurrency=concurrency, table_name=args.table)

    if run_insert_quick:
        await insert_rag_chunks_quick(concurrency=concurrency, table_name=args.table)

    print("\n[Pipeline] Done.")


if __name__ == "__main__":
    asyncio.run(main())

"""
cia_config.py

Shared configuration, constants, and index I/O utilities used across all
CIA (Codebase Intelligence Analysis) pipeline phases.
"""

import json
import os

from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------------------------
# Configuration from env
# -------------------------------------------------------------------

CSHARP_CODEBASE_PATH             = os.getenv("CIA_CODEBASE_PATH", "")
CSHARP_FOCUS_ONLY_FILES          = os.getenv("CIA_FOCUS_ONLY_FILES", "")
CSHARP_IGNORE_FILES              = os.getenv(
    "CIA_IGNORE_FILES",
    "**/Migrations/**,**/*.Designer.cs,**/obj/**,**/bin/**"
    ",**/*.Tests/**,**/*.Test/**,**/Tests/**,**/Test/**"
    ",**/*Tests.cs,**/*Test.cs,**/*Spec.cs",
)
CSHARP_LARGE_FILE_LINE_THRESHOLD = int(os.getenv("CIA_LARGE_FILE_THRESHOLD", 200))
OPENROUTER_SYNTHESIS_MODEL       = os.getenv("CIA_OPENROUTER_MODEL", "qwen/qwen3-32b")
OPENROUTER_CRITICAL_MODEL        = os.getenv("CIA_OPENROUTER_CRITICAL_MODEL", "google/gemini-2.5-pro")
CLOUD_BATCH_DELAY                = float(os.getenv("CIA_CLOUD_BATCH_DELAY", "2.0"))
BATCH_SIZE                       = int(os.getenv("CIA_BATCH_SIZE", "10"))

DEFAULT_INDEX_PATH                  = os.getenv("CIA_INDEX_PATH",                   "wip/csharp-index.json")
DEFAULT_RAW_DOCS_FOLDER             = os.getenv("CIA_RAW_DOCS_FOLDER",              "wip/csharp-docs/raw")
DEFAULT_ENRICHED_FOLDER             = os.getenv("CIA_ENRICHED_DOCS_FOLDER",         "wip/csharp-docs/enriched")
DEFAULT_WORKFLOWS_FOLDER            = os.getenv("CIA_WORKFLOWS_FOLDER",             "wip/csharp-docs/workflows")
DEFAULT_RAG_CHUNKS_FOLDER           = os.getenv("CIA_RAG_CHUNKS_FOLDER",            "wip/csharp-docs/rag-chunks")
DEFAULT_RAG_DONE_FOLDER             = os.getenv("CIA_RAG_DONE_FOLDER",              "wip/csharp-docs/rag-done")
DEFAULT_RAG_DONE_QUICK_FOLDER       = os.getenv("CIA_RAG_DONE_QUICK_FOLDER",        "wip/csharp-docs/rag-done-quick")
DEFAULT_DISCOVERED_WORKFLOWS_PATH   = os.getenv("CIA_DISCOVERED_WORKFLOWS_PATH",    "wip/csharp-docs/discovered-workflows.json")

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------

# Architecture layers ordered by processing priority (Domain first)
LAYER_PRIORITY = {
    "Domain": 0,
    "Business": 1,
    "Infrastructure": 2,
    "API": 3,
    "ExternalClient": 4,
    "Functions": 5,
    "CronJobs": 6,
    "Other": 7,
}

# Handler verb → verb-cluster mapping for workflow grouping
VERB_CLUSTERS = {
    "ReadFlows":        ["get", "search", "find", "list", "query", "fetch", "load"],
    "WriteFlows":       ["create", "update", "delete", "add", "remove", "set", "save"],
    "CalculationFlows": ["calculate", "compute", "estimate", "evaluate", "recalculate"],
    "TransitionFlows":  ["complete", "approve", "cancel", "send", "submit", "confirm", "close", "reopen"],
    "SyncFlows":        ["sync", "import", "export", "migrate", "refresh", "transfer"],
}

# Priority critical flows for Phase 4 Pass B — always deep-dived regardless of scoring.
#
# Matching uses token-set logic on the CamelCase-tokenized class name + file path:
#   required_tokens  — ALL must be present (narrows scope)
#   any_tokens       — AT LEAST ONE must be present (identifies the flow)
PRIORITY_CRITICAL_FLOWS = [
    {
        "name": "CalculateVoyagePnL",
        "module": "VoyageManagement",
        "required_tokens": ["calculate"],
        "any_tokens": ["pnl", "profit", "voyage", "estimate"],
    },
    {
        "name": "CreateVoyageFromEstimate",
        "module": "VoyageManagement",
        "required_tokens": ["voyage", "estimate"],
        "any_tokens": ["create", "from", "transition", "convert"],
    },
    {
        "name": "VoyageLifecycle",
        "module": "VoyageManagement",
        "required_tokens": ["voyage"],
        "any_tokens": ["complete", "cancel", "close", "lifecycle", "finalize", "reopen"],
    },
    {
        "name": "BunkerCostCalculation",
        "module": "BunkerOrder",
        "required_tokens": ["bunker"],
        "any_tokens": ["cost", "calculate", "order", "price", "qty", "quantity"],
    },
    {
        "name": "CommissionPayment",
        "module": "Finance",
        "required_tokens": [],
        "any_tokens": ["commission", "payment", "invoice", "settlement", "receivable", "payable"],
    },
    {
        "name": "ETSEmissions",
        "module": "Finance",
        "required_tokens": [],
        "any_tokens": ["ets", "emission", "carbon", "ghg", "greenhouse", "eu"],
    },
]

# -------------------------------------------------------------------
# Index I/O utilities (used by all phases)
# -------------------------------------------------------------------


def _load_discovered_flows(path: str = None) -> list[dict]:
    """Load dynamically discovered workflows from wip/discovered-workflows.json.

    Returns an empty list if the file does not exist yet (first run before
    workflow-identify has been executed).  The caller is responsible for
    merging these with the static PRIORITY_CRITICAL_FLOWS list.
    """
    if path is None:
        path = DEFAULT_DISCOVERED_WORKFLOWS_PATH
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [d for d in data if isinstance(d, dict)]
    except Exception:
        return []


def _load_index(index_path: str) -> dict:
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_index(index: dict, index_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(index_path)), exist_ok=True)
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

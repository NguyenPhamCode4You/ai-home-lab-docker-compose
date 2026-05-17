import json
import re

from .Task import Task
from .models.Ollama import Ollama
from .constants import OLLAMA_CODE_MODEL

# Returned when the LLM output cannot be parsed as JSON after two attempts.
FALLBACK_RESULT = {
    "class_name": "",
    "namespace": "",
    "file_type": "Other",
    "architecture_layer": "Other",
    "handler_verb": "",
    "methods": [],
    "using_imports": [],
    "injected_services": [],
    "entities_referenced": [],
    "external_clients_used": [],
    "is_critical": False,
}

_STRICT_SUFFIX = (
    "\n\nIMPORTANT: Output ONLY the raw JSON object. "
    "No markdown code fences. No explanation. Start your response with {{ and end with }}."
)


class CSharpFileAnalyzer(Task):
    """
    Phase 1 agent. Extracts structural metadata JSON from a single .cs file.

    Receives:
      context  = full .cs file content
      question = relative file path (used for logging only)

    Returns via analyze(): a parsed dict with class metadata.
    Retries once with stricter instructions on JSON parse failure.
    Falls back to file_type='Other' on second failure — never blocks the pipeline.
    """

    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "csharp-file-analyzer")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama(model=OLLAMA_CODE_MODEL))
        kwargs["instruction_template"] = kwargs.get(
            "instruction_template",
            """
You are a C# code analysis tool. Extract structural metadata from the C# file below.
Respond with ONLY a valid JSON object — no markdown fences, no explanation, no commentary.

The JSON must contain these fields:
  class_name            string   primary class or interface name defined in this file
  namespace             string   fully qualified namespace of the primary class
  file_type             string   one of: Handler, Entity, Dto, Service, Controller, Validator, ExternalClient, Function, Middleware, Configuration, Other
  architecture_layer    string   one of: Domain, Business, Infrastructure, API, ExternalClient, Functions, CronJobs, Other
  handler_verb          string   verb extracted from the class name (Get/Create/Update/Delete/Calculate/Complete/Cancel/Sync/etc.) — empty string if not a handler
  methods               array    each item has: name (string), return_type (string), is_public (bool), parameters (string array), calls (string array of key method/property calls inside the method body)
  using_imports         array    each using directive namespace as a string
  injected_services     array    constructor-injected service, repository, or DbContext type names as strings
  entities_referenced   array    entity and DTO class names referenced anywhere in this file
  external_clients_used array    HTTP client, integration service, or external API type names that are called
  is_critical           bool     always false (the pipeline sets this later based on usage analysis)

C# file to analyze:
{context}
""",
        )
        super().__init__(**kwargs)

    def _extract_json(self, text: str) -> dict | None:
        """Try to extract a JSON object from raw LLM output, stripping fences if present."""
        text = text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```\s*$", "", text)
        text = text.strip()
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        return None

    async def analyze(self, file_content: str, rel_path: str = "") -> dict:
        """
        Run the analyzer and return a parsed metadata dict.

        Retries once with a stricter prompt on JSON parse failure.
        Returns a fallback dict with file_type='Other' on second failure so the
        pipeline is never blocked by a single unparseable file.
        """
        result_text = await self.run(context=file_content, question=rel_path)
        parsed = self._extract_json(result_text)
        if parsed is not None:
            return parsed

        print(f"[CSharpFileAnalyzer] JSON parse failed for {rel_path!r}, retrying with stricter prompt...")
        original_template = self.instruction_template
        self.instruction_template = original_template + _STRICT_SUFFIX
        result_text = await self.run(context=file_content, question=rel_path)
        self.instruction_template = original_template

        parsed = self._extract_json(result_text)
        if parsed is not None:
            return parsed

        print(f"[CSharpFileAnalyzer] FALLBACK (unparseable output): {rel_path!r}")
        fallback = dict(FALLBACK_RESULT)
        if rel_path:
            stem = re.sub(r"\.cs$", "", rel_path.replace("\\", "/").split("/")[-1])
            fallback["class_name"] = stem
        return fallback

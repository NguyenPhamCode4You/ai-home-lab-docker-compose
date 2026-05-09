# AI Orchestra & RAG Agent — Improvement Roadmap

## 1. Memory Management & Compression

**Current problems:**

- `str(context)[:self.max_context_chars]` in `Task.py` is a brutal character-slice that cuts mid-sentence
- History is included raw — older turns consume token budget that could be used for RAG context
- No cross-request session memory; each request is stateless
- `KnowledgeCompression` is defined but never used anywhere in the pipeline

**Improvements:**

### a) Sliding summary memory (rolling compression)

Instead of hard-slicing old history, compress old turns with `KnowledgeCompression` when the buffer exceeds a threshold:

```python
# In get_chat_history_string or a dedicated MemoryManager class
if accumulated_tokens > COMPRESS_THRESHOLD:
    old_turns_text = "..."  # older half of history
    compressed = await KnowledgeCompression().run(context=old_turns_text)
    # Replace old turns with the compressed summary
```

### b) Two-tier history: compressed summary + recent verbatim

- Keep last N turns verbatim (for conversational fluency)
- Compress everything older into a single "session summary" string
- Store it server-side by `session_id` (in-memory dict or Redis)

### c) Query-guided context trimming (semantic truncation)

Instead of `context[:max_tokens]`, filter only relevant document sections against the question before passing to the LLM. `DocumentRanking` already does this per-doc — wire it into `Task.stream()` as a pre-step for very large contexts.

### d) Wire `context_chunk_size` with compression

When `Task` splits into multiple chunks (the "First/Second recall" iterations), compress previous chunk responses before feeding as context into the next chunk. Currently each chunk is independent — they lose accumulated insight from prior iterations.

---

## 2. Multi-Step Working for Complex Tasks

**Current problems:**

- `AssistantOrchestra` is single-pass: route → execute → summarize
- No planning step — `QuestionForwarder` decides everything in one shot with no iteration
- If an agent gives a poor answer, nothing retries or refines
- The orchestra cannot break a task into ordered sub-tasks with explicit dependencies

**Improvements:**

### a) Add a Planner step before `QuestionForwarder`

For complex queries, first emit a structured plan:

```
Step 1: Retrieve BVMS module X documentation  → BVMS-General
Step 2: Get relevant code snippets             → BVMS-Code
Step 3: Generate sequence diagram              → Diagram Assistant
```

Then execute each step, passing the output of step N as context into step N+1.

### b) ReAct-style loop in `AssistantOrchestra`

```python
# Pseudocode
while not task_complete and iteration < MAX_STEPS:
    action = await planner.decide_next_action(state)
    result = await agents[action.agent].stream(action.question, context=state.context)
    state.update(result)
    task_complete = await planner.is_done(state)
```

The planner is itself a small Ollama call that outputs `DONE` or `CALL agent X with question Y`.

### c) Depend-aware agent ordering

Currently agents are sorted by mention index in `QuestionForwarder`'s text output. Instead, have the forwarder emit explicit `depends_on: [agent_name]` metadata so dependent agents only run after their upstream dependencies resolve.

### d) Self-critique / reflection step

After `FinalThoughtSummarizer`, add an optional `CritiqueAgent` that asks: _"Is the answer complete? What is missing?"_ — if incomplete, it triggers one more targeted round filling the identified gap.

---

## 3. Parallelism of Agents

**Current problems:**

- `AssistantOrchestra` runs agents sequentially with `await asyncio.sleep(2)` between each
- `DocumentRanking` calls the LLM per document, one at a time — the single biggest latency bottleneck
- `SupabaseVectorStore.query()` uses synchronous `requests.post`, blocking the async event loop

**Improvements:**

### a) Parallel independent agents in Orchestra

Detect which agents have no context dependency (`context_awareness: False`) and run them concurrently:

```python
independent = [(n, q) for n, q, _ in agent_questions if not agents[n]["context_awareness"]]
dependent   = [(n, q) for n, q, _ in agent_questions if agents[n]["context_awareness"]]

# Run independent agents concurrently
results = await asyncio.gather(*[run_agent(n, q) for n, q in independent])
# Then run context-dependent agents sequentially with accumulated context
```

### b) Batch document ranking

Replace the serial per-document ranking loop in `RagAssistant` with `asyncio.gather`:

```python
scores = await asyncio.gather(*[
    self.document_ranking.run(context=doc, question=question)
    for doc in document_list
])
```

This alone could reduce RAG latency **5–10×** for 200 documents.

### c) Async vector store

`SupabaseVectorStore` uses blocking `requests` — swap to `httpx.AsyncClient` (already used in `Ollama.py`). This unblocks the event loop during embedding queries.

### d) Parallel multi-agent RAG queries

When the orchestra routes to both BVMS-General and BVMS-Code (both query Supabase), the two vector store lookups can run in parallel before any LLM call starts, front-loading the I/O wait.

---

## 4. Hardware Management & Auto Request Routing

**Current problems:**

- All model names are hardcoded strings in `rag_orchestra.py`
- Single Ollama URL — no failover
- A ranking task (`gemma3:4b`) and a generation task (`qwen3.5:9b`) compete for the same GPU with no awareness
- `ChatGpt`, `Gemini`, `Perplexity` backends exist in `src/agents/models/` but are never used as fallbacks

**Improvements:**

### a) Model router / capability registry

Map task type → preferred model → fallback chain:

```python
MODEL_REGISTRY = {
    "ranking":    [Ollama(model="gemma3:4b"),  Ollama(model="gemma3:2b")],
    "generation": [Ollama(model="qwen3.5:9b"), ChatGpt(model="gpt-4o-mini")],
    "diagram":    [Ollama(model="qwen3.5:9b"), ChatGpt()],
}
```

If the local model times out or returns HTTP 503, automatically fall back to the next in the list (cloud as backstop).

### b) Health-check + load balancer for Ollama

Ollama exposes `/api/tags` and `/api/ps` (running models). Poll these to pick the least-loaded node:

```python
async def get_available_model(candidates: list) -> str:
    for model in candidates:
        running = await ollama_ps()  # GET /api/ps
        if model not in running or gpu_load() < THRESHOLD:
            return model
    return candidates[-1]  # fallback to last option
```

### c) Task-complexity → model-size routing

- Short classification / ranking questions → small model (`gemma3:4b`)
- Long generation / code tasks → large model (`qwen3.5:9b` or cloud)

Wire this into `QuestionForwarder`: its output could include a `complexity: low|medium|high` tag that the orchestra uses to select model size before invoking each agent.

### d) Multiple Ollama node support

Support a list of Ollama URLs with round-robin or least-loaded routing:

```python
OLLAMA_NODES = [
    "http://192.168.1.10:11434",
    "http://192.168.1.11:11434",
]
```

The `Ollama` model class checks `/api/ps` on each node and picks the one with the fewest active model loads.

### e) Graceful timeout degradation

Wrap every `Task.run()` with a timeout + retry that demotes to a smaller or cloud model automatically — avoids the current `httpx.Timeout(80.0)` silently failing end users with a blank stream.

---

## 5. GraphRAG — Knowledge Graph for Better Retrieval

**Current problem:**
The current RAG pipeline treats every document chunk as an isolated flat vector. It retrieves by cosine similarity to the query embedding but has no awareness of _relationships between entities_ (e.g., a BVMS module → calls → another module, a workflow → uses → an API endpoint). This means:

- Multi-hop questions ("What modules does the booking flow touch, and what do each of them do?") require multiple separate RAG calls and rely on the LLM to mentally connect the dots
- Semantically related chunks that use different terminology are missed if their embeddings are distant
- No global understanding of the knowledge structure (which topics cluster, which are central vs peripheral)

**Improvement: Build a Knowledge Graph on top of Supabase**

The idea is to extract entities and relationships from your BVMS documents during ingestion and store them as a graph. At query time, use graph traversal to enrich the retrieved context beyond pure vector similarity.

### Graph Schema (nodes and edges in Supabase)

```
Nodes table:  id, label (e.g. "BVMS Module", "API Endpoint", "Workflow"), name, summary, embedding
Edges table:  source_id, target_id, relation (e.g. "calls", "uses", "triggers", "part_of"), weight
```

### Step 1 — Entity & relation extraction during ingestion (`rag_learn.py`)

Use a small LLM (or `SimpleEntityExtractor.py` already in `src/agents/`) to extract from each chunk:

```
Entities: [VoyagerBookingService, CreateReservationAPI, PassengerModule]
Relations: VoyagerBookingService → calls → CreateReservationAPI
           VoyagerBookingService → uses → PassengerModule
```

Store these as rows in the `nodes` and `edges` tables alongside the existing vector chunks.

### Step 2 — Graph-augmented retrieval at query time

1. **Vector search** → get top-K chunks (current behavior)
2. **Entity linking** → identify which graph nodes appear in the top-K results
3. **Graph expansion** → traverse 1–2 hops from those nodes via the `edges` table to pull in related chunks that vector search missed
4. **Re-rank the merged set** with `DocumentRanking` → feed to `GeneralRagAnswer`

```python
# Pseudocode in RagAssistant.stream()
vector_chunks = vector_store.get_documents_string(question, ...)
linked_nodes  = graph_store.find_entities_in_chunks(vector_chunks)
expanded      = graph_store.expand_neighbors(linked_nodes, hops=2)
merged_context = deduplicate(vector_chunks + expanded)
```

### Step 3 — Global summaries for high-level questions

Pre-compute community summaries (group of tightly connected nodes) using graph clustering (e.g., Louvain algorithm). For broad questions like "give me an overview of the booking system", retrieve the community summary instead of raw chunks — this is the core idea behind Microsoft's GraphRAG paper.

### Practical tools

- **Graph storage**: Supabase (PostgreSQL with `ltree` or `pgRouting`) or a dedicated store like Neo4j/Memgraph
- **Entity extraction**: `SimpleEntityExtractor.py` already exists in `src/agents/` — extend it to also extract relations
- **Graph traversal**: PostgreSQL recursive CTEs for small graphs; Neo4j Cypher for larger ones
- **Reference implementation**: [microsoft/graphrag](https://github.com/microsoft/graphrag) for the community-summary approach

### Expected benefits

| Scenario                                 | Flat RAG                | GraphRAG                 |
| ---------------------------------------- | ----------------------- | ------------------------ |
| "What does module X do?"                 | Good                    | Good                     |
| "What modules does workflow Y touch?"    | Poor (misses hops)      | Good                     |
| "Give an overview of the booking system" | Poor (scattered chunks) | Good (community summary) |
| "How does A connect to B?"               | Poor                    | Good (path query)        |

---

## Priority Order

| #   | Improvement                                                        | Effort | Impact                                              |
| --- | ------------------------------------------------------------------ | ------ | --------------------------------------------------- |
| 1   | **Parallel document ranking** (`asyncio.gather` in `RagAssistant`) | Low    | Huge — cuts RAG latency 5–10×                       |
| 2   | **Async `SupabaseVectorStore`** (swap `requests` → `httpx`)        | Low    | Unblocks event loop                                 |
| 3   | **Parallel independent agents** in Orchestra                       | Medium | Better UX on multi-agent queries                    |
| 4   | **Sliding summary memory** using existing `KnowledgeCompression`   | Medium | Richer long conversations                           |
| 5   | **Model fallback chain** (local → cloud)                           | Medium | Reliability on GPU contention                       |
| 6   | **GraphRAG** — entity/relation extraction + graph expansion        | High   | Qualitatively better retrieval on complex questions |
| 7   | **Planner + ReAct loop** for complex tasks                         | High   | True multi-step capability                          |
| 8   | **Complexity-based model routing**                                 | Medium | GPU efficiency                                      |

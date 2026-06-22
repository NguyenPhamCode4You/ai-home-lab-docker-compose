# Domain Expert Model Training Pipeline from Enterprise Source Code

## Goal

Build a small but highly capable domain expert model (4B–12B) that understands:

- Maritime business domain
- Company workflows
- Software architecture
- Design decisions
- Business rules
- Operational constraints
- Critical thinking and tradeoff analysis

The objective is not to create a documentation chatbot, but an AI assistant capable of reasoning like a senior engineer, solution architect, or domain expert.

---

# Core Principle

Most enterprise knowledge is not found in documentation.

Typically:

- 20% is in Confluence, Wiki, ADRs, and documents
- 80% is hidden inside:
  - Service interactions
  - Database schemas
  - Business rules
  - Workflow implementations
  - Bug fixes
  - Historical design decisions
  - Git history

The pipeline should focus on extracting this hidden knowledge.

---

# Stage 1: Build a Company Knowledge Graph

## Objective

Convert source code into a structured representation of the system.

Instead of treating code as text, extract relationships between components.

---

## Extract

### Services

Example:

```java
VoyageService
CargoService
FuelOptimizationService
PortCallService
```

Extract:

```json
{
  "service": "VoyageService",
  "calls": ["FuelOptimizationService", "PortService"],
  "writes": ["Voyage", "Route"],
  "reads": ["WeatherForecast"],
  "events": ["VoyageApproved"]
}
```

---

### Database Entities

```sql
Voyage
Cargo
Vessel
Port
```

Extract:

```json
{
  "table": "Voyage",
  "relations": ["Vessel", "Cargo", "Port"]
}
```

---

### API Endpoints

```http
POST /voyages
```

Extract:

```json
{
  "endpoint": "/voyages",
  "service": "VoyageService",
  "entities": ["Voyage", "Route"]
}
```

---

## Output

A company-wide graph containing:

- Service graph
- Database graph
- API graph
- Event graph
- Domain entity graph

This becomes the foundation for all later reasoning.

---

# Stage 2: Extract Business Rules

## Objective

Identify the business logic encoded in software.

Business rules often represent years of domain knowledge.

---

## Examples

Code:

```java
if(vessel.age > 25)
```

Extract:

```json
{
  "rule": "Vessels older than 25 years require additional approval."
}
```

---

Code:

```java
if(voyage.status != APPROVED)
```

Extract:

```json
{
  "rule": "Only approved voyages can proceed to execution."
}
```

---

## What to Look For

Search for:

```text
if statements
validation rules
authorization logic
workflow gates
pricing logic
scheduling logic
regulatory constraints
```

---

## Expected Output

```text
500–5000+ business rules
```

These become high-value training data.

---

# Stage 3: Extract Workflows

## Objective

Understand how business processes execute across the system.

---

## Example Workflow

Voyage Creation

```text
Controller
 ↓
VoyageService
 ↓
Validation
 ↓
RouteEngine
 ↓
Database
 ↓
Event Publication
```

---

Extract:

```json
{
  "workflow": "Create Voyage",
  "steps": [
    "Validate request",
    "Create voyage",
    "Calculate route",
    "Persist data",
    "Publish event"
  ]
}
```

---

## Generate Training Questions

Examples:

```text
Explain the voyage creation workflow.

What are failure points?

How would you scale this workflow?

What monitoring should exist?
```

---

## Output

A library of:

- Business workflows
- System workflows
- Operational workflows

---

# Stage 4: Extract Domain Vocabulary

## Objective

Teach the model industry-specific language.

---

## Maritime Examples

```text
Demurrage
Laytime
Charter Party
Bunker
Ballast Voyage
Deadweight
Port Call
```

---

Extract:

```json
{
  "term": "Demurrage",
  "definition": "Penalty charged when loading or unloading exceeds agreed time."
}
```

---

## Output

A domain glossary.

This dramatically improves expert-level responses.

---

# Stage 5: Extract Design Decisions

## Objective

Understand why the architecture exists.

This is where senior architect knowledge appears.

---

## Detect Patterns

Search for:

```text
Strategy
Factory
Saga
CQRS
Event Sourcing
Outbox
Circuit Breaker
Caching
Retry
```

---

## Generate Reasoning

Prompt:

```text
Why was this pattern chosen?

What alternatives existed?

What tradeoffs were accepted?
```

---

Example:

```json
{
  "decision": "Saga Pattern",
  "reason": "Voyage operations span multiple services.",
  "alternative": "Two-phase commit",
  "tradeoff": "Eventual consistency"
}
```

---

## Output

Architecture Decision Records (ADRs)

These are extremely valuable for training architect-level reasoning.

---

# Stage 6: Mine Historical Decisions from Git

## Objective

Capture senior engineer thinking that never made it into documentation.

Git history often contains years of design evolution.

---

## Sources

```bash
git log
git blame
pull requests
code reviews
commit messages
```

---

## Examples

Commit:

```text
Refactor scheduler to reduce database contention
```

Extract:

```json
{
  "problem": "Database contention",
  "solution": "Scheduler redesign",
  "reasoning": "Improved throughput under peak load"
}
```

---

Commit:

```text
Fix race condition in fuel optimization workflow
```

Extract:

```json
{
  "problem": "Concurrency issue",
  "solution": "Locking strategy",
  "reasoning": "Prevent inconsistent calculations"
}
```

---

## Output

A historical engineering knowledge base containing:

- Problems
- Solutions
- Tradeoffs
- Lessons learned

---

# Generating Expert-Level Training Data

After Stages 1–6 are complete, use a stronger teacher model to generate reasoning examples.

---

## Knowledge Questions

```text
Explain VoyageService.

What is demurrage?

How does fuel optimization work?
```

---

## Workflow Questions

```text
Describe voyage approval workflow.

What services participate?

What can fail?
```

---

## Architecture Questions

```text
Why was Saga chosen?

What are scalability bottlenecks?

How would you redesign this?
```

---

## Critical Thinking Questions

```text
What are weaknesses in the current architecture?

What risks exist?

What assumptions are dangerous?
```

---

## Product Questions

```text
What feature gaps exist?

How could competitors outperform us?

What should be built next?
```

---

## Business Questions

```text
How does this workflow create customer value?

How does it generate revenue?

What KPIs should be monitored?
```

---

# Dataset Structure

Recommended distribution:

| Dataset Type       | Percentage |
| ------------------ | ---------- |
| Knowledge          | 30%        |
| Workflow           | 20%        |
| Architecture       | 20%        |
| Critical Thinking  | 15%        |
| Product Strategy   | 10%        |
| Business Reasoning | 5%         |

---

# Recommended Scale

For a serious enterprise assistant:

```text
50,000 – 150,000 examples
```

Good target:

```text
100,000 examples
```

---

# Training Strategy

Do not rely solely on fine-tuning.

Recommended architecture:

```text
Confluence
       ↓

Source Code
       ↓

Knowledge Extraction
       ↓

Vector Database
       ↓

RAG Retrieval
       ↓

Gemma/Qwen Fine-Tuning
       ↓

Domain Expert Assistant
```

---

# Final Goal

The model should answer:

- What does this system do?
- Why was it designed this way?
- What business problem does it solve?
- What tradeoffs exist?
- How can it scale globally?
- What risks exist?
- How should it evolve?

The target outcome is an AI assistant that behaves like a combination of:

- Senior Software Engineer
- Solution Architect
- Product Architect
- Domain Expert
- Technical Lead

rather than a simple documentation search engine.

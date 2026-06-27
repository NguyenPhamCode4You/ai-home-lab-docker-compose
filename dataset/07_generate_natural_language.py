"""
Step 07: Generate natural language reasoning dataset.
10% of final dataset - general language with reasoning patterns.
Covers technical documentation, incident reports, and engineering blog posts.
"""

import os
import json
import random
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── Natural language reasoning scenarios ────────────────────────────────────
NL_SCENARIOS = [
    {
        "topic": "Technical Documentation",
        "problem": "Write documentation for a new API endpoint that handles user authentication.",
        "reasoning": """Observation:
Need to document a new authentication API endpoint.

Known facts:
- Endpoint: POST /api/auth/login
- Accepts: email, password
- Returns: JWT token, refresh token
- Rate limited: 10 requests/minute

Unknowns:
- Token expiration time
- Refresh token rotation policy
- Account lockout policy

Assumptions:
- Passwords are hashed with bcrypt
- JWT uses RS256 algorithm
- HTTPS is required

Plan:
1. Document the endpoint URL and method
2. List request parameters with types
3. Show success and error response examples
4. Document rate limiting
5. Include security considerations

Checkpoint:
Documentation covers all public API surface.

If fail:
Missing security details - add token storage recommendations.

Next step:
Review with security team for accuracy.""",
    },
    {
        "topic": "Incident Report",
        "problem": "Write an incident report for a production outage that lasted 2 hours.",
        "reasoning": """Observation:
Production outage lasted 2 hours affecting all users.

Known facts:
- Started at 14:32 UTC
- All users affected globally
- Services: API gateway, user service, payment service
- No data loss reported

Unknowns:
- Root cause at time of incident
- Full timeline of events
- Impact on pending transactions

Assumptions:
- Monitoring alerts fired but were missed
- No recent deployments in the affected services

Plan:
1. Establish timeline of events
2. Identify the triggering event
3. Document response actions
4. Determine root cause
5. List remediation steps

Checkpoint:
Timeline is complete and verified with logs.

If fail:
Missing log data for first 15 minutes - check backup logs.

Next step:
Schedule post-incident review with all teams involved.""",
    },
    {
        "topic": "Engineering Blog Post",
        "problem": "Write a blog post about migrating from monolith to microservices.",
        "reasoning": """Observation:
Need to document our monolith to microservices migration experience.

Known facts:
- Started with a 200k line codebase
- Team of 15 engineers
- Migration took 8 months
- Zero downtime during migration

Unknowns:
- How other teams approached similar migrations
- Best practices we discovered

Assumptions:
- Readers are technical leads or architects
- Readers have similar scale applications

Plan:
1. Describe the starting point and motivations
2. Outline the migration strategy
3. Document key technical decisions
4. Share lessons learned and pitfalls
5. Provide actionable recommendations

Checkpoint:
All technical claims are verified with metrics.

If fail:
Need more performance data - request from DevOps team.

Next step:
Share draft with team that executed the migration.""",
    },
    {
        "topic": "Architecture Review",
        "problem": "Review the proposed architecture for a real-time chat application.",
        "reasoning": """Observation:
Proposed architecture uses WebSocket for real-time messaging.

Known facts:
- Expected: 100k concurrent users
- Message throughput: 10k messages/second
- Required: message persistence, delivery guarantees

Unknowns:
- Geographic distribution of users
- Media sharing requirements
- Read receipts and typing indicators

Assumptions:
- Messages should be delivered in order per conversation
- Offline message storage is required

Plan:
1. Evaluate WebSocket scaling approach
2. Consider message queue for persistence
3. Review database schema for message storage
4. Assess horizontal scaling strategy
5. Identify single points of failure

Checkpoint:
Architecture covers all functional requirements.

If fail:
Missing consideration for message deduplication - add to review.

Next step:
Schedule architecture review meeting with the team.""",
    },
    {
        "topic": "Code Migration Plan",
        "problem": "Plan migration from Python 2 to Python 3 for a large codebase.",
        "reasoning": """Observation:
Need to migrate a large Python codebase from Python 2 to Python 3.

Known facts:
- Codebase: 500k lines of Python
- Dependencies: 50+ third-party packages
- Test coverage: 60%
- Timeline: 6 months

Unknowns:
- Which dependencies don't support Python 3
- Custom code patterns that need changes

Assumptions:
- Python 3.11 is the target version
- Functionality must remain identical
- CI/CD pipeline must support both versions during transition

Plan:
1. Audit dependencies for Python 3 compatibility
2. Run 2to3 automated tool on codebase
3. Fix remaining manual changes
4. Update CI/CD to test both versions
5. Gradual cutover strategy

Checkpoint:
All tests pass on Python 3.11.

If fail:
Some dependencies still Python 2 only - find alternatives or fork.

Next step:
Create detailed migration checklist with priorities.""",
    },
]


def generate_natural_language_samples(num_samples: int = 10000) -> str:
    """
    Generate natural language reasoning samples.
    
    These cover:
    - Technical documentation
    - Incident reports
    - Engineering blog posts
    - Architecture reviews
    - Migration plans
    """
    logger.info(f"Generating {num_samples} natural language reasoning samples...")
    
    output_file = OUTPUT_DIR / "natural_language_reasoning.jsonl"
    written = 0
    
    with open(output_file, "w", encoding="utf-8") as f:
        for i in range(num_samples):
            scenario = random.choice(NL_SCENARIOS)
            
            # Add variation to each sample
            variations = [
                f"\n\nContext: This is for internal team documentation.",
                f"\n\nContext: This is for public engineering blog.",
                f"\n\nContext: This is for stakeholder communication.",
                f"\n\nContext: This is for technical review process.",
                f"\n\nContext: This is for onboarding new team members.",
            ]
            
            sample = {
                "source": "natural_language_synthetic",
                "domain": "natural_language",
                "topic": scenario["topic"],
                "instance_id": f"nl-synthetic-{i}",
                "problem": scenario["problem"] + random.choice(variations),
                "reasoning_type": "natural_language_reasoning",
                "reasoning": scenario["reasoning"],
            }
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            written += 1
            
            if (i + 1) % 2000 == 0:
                logger.info(f"  Generated {i + 1:,} samples...")
    
    logger.info(f"Natural language complete: {num_samples} samples written")
    return str(output_file)


def main():
    logger.info("=" * 60)
    logger.info("Step 07: Natural Language Reasoning Dataset")
    logger.info("=" * 60)
    
    output_file = generate_natural_language_samples()
    logger.info(f"Output: {output_file}")
    
    return output_file


if __name__ == "__main__":
    main()

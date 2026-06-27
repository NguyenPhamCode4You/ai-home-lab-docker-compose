"""
Step 06: Generate synthetic reasoning dataset.
This is the BIGGEST dataset source - generate millions of reasoning samples.
Focus on engineering workflows: observation → hypothesis → verification → revision.
"""

import os
import json
import random
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── Engineering reasoning scenarios ──────────────────────────────────────────
DOMAINS = {
    "software_debugging": {
        "label": "Software Debugging",
        "scenarios": [
            {
                "problem": "{tech} application returns {error} after {action}.",
                "reasoning_template": """Observation:
{tech} application produces {error} after {action}.

Possible causes:
- Configuration mismatch between environments
- Dependency version incompatibility
- Resource exhaustion (memory, connections, file handles)
- Race condition in concurrent code

Check:
1. Compare configuration files across environments
2. Verify dependency versions match requirements
3. Monitor resource usage during the operation
4. Check for unhandled exceptions in logs

Hypothesis:
The error stems from a {specific_cause}.

Verification:
{verification_step}

Result:
{verification_result}

Hypothesis rejected:
{rejected_hypothesis}

New hypothesis:
{new_hypothesis}

Alternative plan:
{alternative_plan}

Next investigation:
{next_investigation}""",
            },
            {
                "problem": "Code works in development but fails in {environment}.",
                "reasoning_template": """Observation:
Code passes all local tests but fails in {environment}.

Possible causes:
- Environment variable differences
- File system case sensitivity (Windows vs Linux)
- Path separator differences (\\ vs /)
- Timezone or locale settings
- Network configuration differences

Check:
1. Diff environment variables between dev and {environment}
2. Check file paths for case sensitivity issues
3. Verify timezone settings match expectations
4. Review CI/CD pipeline configuration

Hypothesis:
File path case sensitivity is causing the failure.

Verification:
Compare file system behavior between local and {environment}.

Result:
Linux file system is case-sensitive, Windows is not.

Hypothesis rejected:
Environment variables are actually matching.

New hypothesis:
The issue is in the path construction logic.

Alternative plan:
Use os.path.join or pathlib for cross-platform paths.

Next investigation:
Audit all file path constructions in the codebase.""",
            },
            {
                "problem": "API endpoint responds correctly for small requests but fails for large payloads.",
                "reasoning_template": """Observation:
API works for small payloads but fails with large data.

Possible causes:
- Request body size limit configured
- Memory allocation failure
- Timeout before response completes
- Buffer overflow in processing

Check:
1. Check server configuration for max body size
2. Monitor memory usage during large requests
3. Add timing logs to identify timeout point
4. Review buffer sizes in processing pipeline

Hypothesis:
Request body size limit is being enforced.

Verification:
Check server config for maxContentLength or similar settings.

Result:
Config shows limit of 1MB, test payload is 5MB.

Hypothesis rejected:
Memory is not the issue (plenty available).

New hypothesis:
The limit is enforced at the reverse proxy level.

Alternative plan:
Increase limit at both application and proxy level.

Next investigation:
Check nginx/Apache configuration for client_max_body_size.""",
            },
        ],
    },
    "devops_infrastructure": {
        "label": "DevOps & Infrastructure",
        "scenarios": [
            {
                "problem": "Docker container exits with code {exit_code} immediately after start.",
                "reasoning_template": """Observation:
Container exits with code {exit_code} within seconds of starting.

Possible causes:
- ENTRYPOINT script completes without running the app
- Missing required configuration or environment variables
- Application crash due to unhandled exception
- Port already in use
- Permission denied on required files

Check:
1. docker logs <container_id> for any output
2. docker inspect for exit code and error message
3. Check Dockerfile ENTRYPOINT and CMD
4. Verify all required environment variables are set

Hypothesis:
ENTRYPOINT script finishes without exec-ing the application.

Verification:
docker logs shows empty output, exit code 0.

Result:
Container exited cleanly, not a crash.

Hypothesis rejected:
Application crash is not the cause (no error in logs).

New hypothesis:
The ENTRYPOINT script has a bug where it exits before starting the app.

Alternative plan:
Fix ENTRYPOINT to use exec form: exec ["python", "app.py"]

Next investigation:
Review Dockerfile ENTRYPOINT and ensure it uses exec.""",
            },
            {
                "problem": "Kubernetes pod stuck in {state} state.",
                "reasoning_template": """Observation:
Pod is in {state} state for more than {duration}.

Possible causes:
- Image pull failure (wrong tag, registry auth)
- Liveness/readiness probe failing
- Resource limits exceeded (OOMKilled)
- Pending: no nodes with sufficient resources
- ConfigMap/Secret not found

Check:
1. kubectl describe pod <pod> for events
2. kubectl logs <pod> for application errors
3. kubectl get events --namespace <ns> for cluster events
4. Check resource quotas in namespace

Hypothesis:
Image pull is failing due to authentication.

Verification:
kubectl describe pod shows: "Failed to pull image: unauthorized"

Result:
Confirmed registry authentication issue.

Hypothesis rejected:
Resource limits are not the issue.

New hypothesis:
ImagePullSecrets not configured correctly.

Alternative plan:
1. Verify secret exists: kubectl get secret <name>
2. Add imagePullSecrets to pod spec
3. Test with docker login first

Next investigation:
Check if the registry credentials are valid and not expired.""",
            },
            {
                "problem": "CI/CD pipeline fails at {stage} stage with {error}.",
                "reasoning_template": """Observation:
Pipeline fails at {stage} stage with error: {error}.

Possible causes:
- Dependency not cached or downloaded
- Environment variable not set in CI config
- Permission issue with deployment target
- Version mismatch between local and CI
- Cache corruption

Check:
1. Compare CI environment with local development
2. Verify all required environment variables
3. Check dependency installation logs
4. Review recent changes to pipeline configuration

Hypothesis:
Dependency cache is corrupted or missing.

Verification:
Check cache key and recent cache updates.

Result:
Cache key changed due to requirements.txt modification.

Hypothesis rejected:
Environment variables are all set correctly.

New hypothesis:
The dependency installation is failing silently.

Alternative plan:
Add verbose logging to dependency installation step.

Next investigation:
Run the failing step locally with CI environment variables.""",
            },
        ],
    },
    "api_integration": {
        "label": "API Integration",
        "scenarios": [
            {
                "problem": "Third-party API returns {error} intermittently.",
                "reasoning_template": """Observation:
Third-party API returns {error} on approximately {percentage}% of requests.

Possible causes:
- Rate limiting by the API provider
- Network instability between our servers and theirs
- API version deprecation
- Input data format mismatch on edge cases
- Server-side timeout on their end

Check:
1. Check API provider status page and documentation
2. Review our request rate vs their limits
3. Add request/response logging with timestamps
4. Test with different input data patterns

Hypothesis:
We're hitting their rate limit.

Verification:
Check response headers for rate limit info (X-RateLimit-Remaining).

Result:
X-RateLimit-Remaining shows 0 before failures start.

Hypothesis rejected:
Network is stable (ping to their servers is consistent).

New hypothesis:
We need to implement exponential backoff with jitter.

Alternative plan:
1. Implement retry with exponential backoff
2. Add request queuing to stay under rate limits
3. Cache responses where possible

Next investigation:
Review their API documentation for rate limit headers and retry-after values.""",
            },
            {
                "problem": "Webhook delivery failing to {endpoint}.",
                "reasoning_template": """Observation:
Webhooks are not being delivered to {endpoint} successfully.

Possible causes:
- Endpoint URL is incorrect or DNS resolution failing
- SSL/TLS certificate issue
- Timeout before webhook completes processing
- Authentication/authorization failure
- Payload format mismatch

Check:
1. Verify endpoint URL is accessible from webhook provider
2. Check SSL certificate validity
3. Review webhook provider's delivery logs
4. Test endpoint with curl/wget from webhook server

Hypothesis:
Endpoint is timing out during processing.

Verification:
Add timing logs at webhook handler entry and completion.

Result:
Processing takes 15 seconds, webhook timeout is 10 seconds.

Hypothesis rejected:
SSL certificate is valid and DNS resolves correctly.

New hypothesis:
The webhook handler does synchronous processing that takes too long.

Alternative plan:
1. Acknowledge webhook immediately
2. Process payload asynchronously via message queue
3. Return 200 OK within timeout

Next investigation:
Implement async processing pattern and test with slow payloads.""",
            },
        ],
    },
    "database_troubleshooting": {
        "label": "Database Troubleshooting",
        "scenarios": [
            {
                "problem": "Database query that works locally takes {duration} in production.",
                "reasoning_template": """Observation:
Query executes in {local_time} locally but {duration} in production.

Possible causes:
- Different query execution plan (statistics outdated)
- Missing indexes in production
- Different data volume or distribution
- Connection pool contention
- Different database configuration (work_mem, shared_buffers)

Check:
1. EXPLAIN ANALYZE on both environments
2. Compare index definitions
3. Check table statistics freshness
4. Compare database configuration parameters

Hypothesis:
Production statistics are outdated, causing bad execution plan.

Verification:
Run ANALYZE on production tables and re-check EXPLAIN.

Result:
After ANALYZE, query plan changed and performance improved 10x.

Hypothesis rejected:
Indexes are the same on both environments.

New hypothesis:
The query planner chose a sequential scan due to stale statistics.

Alternative plan:
1. Schedule regular ANALYZE jobs
2. Consider partial indexes for frequently queried subsets
3. Review query for potential optimization

Next investigation:
Set up pg_stat_statements to monitor query performance over time.""",
            },
            {
                "problem": "Database connection pool exhausted under load.",
                "reasoning_template": """Observation:
Application throws connection pool exhausted error under {load_level} load.

Possible causes:
- Connections not being returned to pool
- Connection leak in error paths
- Pool size too small for concurrent requests
- Long-running queries holding connections
- Connection validation timeout

Check:
1. Monitor active vs idle connections in pool
2. Check for connections not being closed in error handlers
3. Review pool configuration (min/max connections)
4. Identify longest-running queries

Hypothesis:
Connections are leaked in error paths (not returned to pool).

Verification:
Add connection tracking and check for unclosed connections in exception handlers.

Result:
Found 3 code paths where connections are not closed on exception.

Hypothesis rejected:
Pool size is adequate for normal operation.

New hypothesis:
Connection leak combined with burst traffic causes exhaustion.

Alternative plan:
1. Fix connection leaks in all error paths
2. Add connection timeout and validation
3. Implement circuit breaker for database connections

Next investigation:
Add connection pool metrics to monitoring dashboard.""",
            },
        ],
    },
    "performance_optimization": {
        "label": "Performance Optimization",
        "scenarios": [
            {
                "problem": "Application response time degraded from {fast_time} to {slow_time}.",
                "reasoning_template": """Observation:
Response time increased from {fast_time} to {slow_time} after {change}.

Possible causes:
- New code path added with O(n²) complexity
- N+1 query problem introduced
- Missing cache for frequently accessed data
- Synchronous operation that should be async
- Memory pressure causing GC pauses

Check:
1. Profile the application with APM tool
2. Compare execution paths before and after {change}
3. Check database query count per request
4. Monitor memory usage and GC frequency

Hypothesis:
N+1 query problem introduced in the new feature.

Verification:
APM shows {query_count} database queries for a single page load.

Result:
Confirmed N+1: 1 query for list + N queries for related data.

Hypothesis rejected:
Memory usage is normal, no GC pressure.

New hypothesis:
Eager loading the related data would reduce queries from N+1 to 2.

Alternative plan:
1. Use eager loading / JOIN queries
2. Add database query caching
3. Implement pagination to limit result sets

Next investigation:
Benchmark the optimized query and monitor production performance.""",
            },
        ],
    },
    "security_vulnerability": {
        "label": "Security Vulnerability",
        "scenarios": [
            {
                "problem": "Security scanner reports {vulnerability} in {tech} dependencies.",
                "reasoning_template": """Observation:
Security scanner flagged {vulnerability} in {tech} dependencies.

Possible causes:
- Outdated dependency version with known CVE
- Transitive dependency (indirect) with vulnerability
- False positive from scanner
- Misconfiguration exposing sensitive data

Check:
1. Verify the CVE is applicable to our usage
2. Check if we're using the vulnerable function/feature
3. Review dependency tree for transitive dependencies
4. Check scanner documentation for known false positives

Hypothesis:
The vulnerability applies because we use the affected function.

Verification:
Review CVE details and confirm our code path triggers the issue.

Result:
Confirmed: our code calls the vulnerable function with untrusted input.

Hypothesis rejected:
Not a false positive - the CVE is applicable.

New hypothesis:
Upgrading to the patched version will fix the issue.

Alternative plan:
1. Check if a patched version exists
2. Test upgrade in staging environment
3. Review changelog for breaking changes
4. If no patch, implement mitigation

Next investigation:
Test the upgrade in staging and run full test suite.""",
            },
        ],
    },
    "deployment_failure": {
        "label": "Deployment Failure",
        "scenarios": [
            {
                "problem": "Deployment to {environment} fails with {error}.",
                "reasoning_template": """Observation:
Deployment to {environment} fails with: {error}.

Possible causes:
- Environment-specific configuration missing
- Resource limits exceeded in target environment
- Permission/role mismatch for deployment service account
- Dependency not available in target environment
- Database migration conflict

Check:
1. Compare deployment logs between successful and failed deployments
2. Verify service account permissions in {environment}
3. Check resource quotas and limits
4. Review recent changes to deployment configuration

Hypothesis:
Service account lacks permissions in {environment}.

Verification:
Check IAM/RBAC policies for the deployment service account.

Result:
Service account missing {environment}-specific role binding.

Hypothesis rejected:
Resource limits are sufficient (plenty of CPU/memory available).

New hypothesis:
The deployment role was not replicated to {environment}.

Alternative plan:
1. Add role binding for deployment service account
2. Verify with kubectl auth can-i --as=<service-account>
3. Retry deployment

Next investigation:
Document the required roles for each environment.""",
            },
        ],
    },
    "code_review": {
        "label": "Code Review",
        "scenarios": [
            {
                "problem": "Code review: {issue} in {tech} implementation.",
                "reasoning_template": """Observation:
Code review identified {issue} in {tech} implementation.

This approach won't work because {reason}.
Instead, we should consider {alternative}.

Maybe we can also {additional_improvement}.
I tested the alternative approach locally.

Actually, there's a deeper issue: {deeper_issue}.
The root cause is {root_cause}.

Alternative plan:
1. Refactor the affected module
2. Add proper error handling
3. Include unit tests for the edge cases

Next investigation:
Review similar patterns across the codebase for consistency.""",
            },
        ],
    },
    "architecture_decision": {
        "label": "Architecture Decision",
        "scenarios": [
            {
                "problem": "Architecture decision: {tech} vs {alternative_tech} for {use_case}.",
                "reasoning_template": """Observation:
Need to choose between {tech} and {alternative_tech} for {use_case}.

Possible approaches:
- Use {tech}: {tech_pro}
- Use {alternative_tech}: {alternative_pro}
- Use both: {tech} for {part_a}, {alternative_tech} for {part_b}

Check:
1. Compare performance characteristics for our workload
2. Evaluate team familiarity and learning curve
3. Consider long-term maintenance burden
4. Check ecosystem and community support

Hypothesis:
{tech} is better because {reason}.

Verification:
Build a proof of concept with both approaches.

Result:
{tech} POC shows {metric} improvement in {aspect}.

Hypothesis rejected:
{alternative_tech} has better developer experience but worse performance.

New hypothesis:
Use {tech} as primary with {alternative_tech} for specific subtasks.

Alternative plan:
1. Start with {tech} for core functionality
2. Evaluate {alternative_tech} for specific use cases
3. Document decision rationale for future reference

Next investigation:
Create architecture decision record (ADR) documenting the choice.""",
            },
        ],
    },
    "incident_response": {
        "label": "Incident Response",
        "scenarios": [
            {
                "problem": "Production incident: {symptom} affecting {scope}.",
                "reasoning_template": """Observation:
Production incident: {symptom} affecting {scope}.

Immediate actions:
1. Assess severity and scope
2. Check monitoring dashboards
3. Review recent deployments and changes
4. Check upstream dependencies

Possible causes:
- Recent deployment introduced regression
- Upstream service outage
- Database performance degradation
- Network partition
- Resource exhaustion

Check:
1. Compare metrics before and after incident start
2. Check deployment timeline for recent changes
3. Verify upstream service health
4. Monitor resource utilization trends

Hypothesis:
Recent deployment caused the issue.

Verification:
Rollback the last deployment and monitor.

Result:
Metrics return to normal after rollback.

Hypothesis rejected:
Upstream services are healthy.

New hypothesis:
The deployment introduced a memory leak that manifests under load.

Alternative plan:
1. Keep rollback in place
2. Investigate the specific commit that introduced the issue
3. Add memory monitoring alerts

Next investigation:
Conduct post-incident review and add appropriate monitoring.""",
            },
        ],
    },
}

# ─── Fill-in values for scenarios ──────────────────────────────────────────────
FILL_VALUES = {
    "tech": ["Python", "Node.js", "Go", "Rust", "Java", "C#", "TypeScript"],
    "error": ["HTTP 500", "HTTP 502", "HTTP 503", "timeout", "connection refused", "segmentation fault"],
    "action": ["deployment", "data import", "user login", "file upload", "API call", "database query"],
    "specific_cause": ["configuration error", "race condition", "memory leak", "timeout", "dependency issue"],
    "verification_step": ["Check configuration files and compare with working environment.", "Review error logs for stack traces.", "Test with minimal reproduction case."],
    "verification_result": ["Configuration mismatch confirmed.", "Stack trace points to specific function.", "Minimal case reproduces the issue."],
    "rejected_hypothesis": "Initial assumption about root cause was incorrect.",
    "new_hypothesis": "The issue stems from a different code path or dependency.",
    "alternative_plan": "Try alternative approach and compare results.",
    "next_investigation": "Trace the execution path and verify each assumption.",
    "environment": ["staging", "production", "CI/CD", "development", "QA"],
    "duration": ["5 minutes", "10 minutes", "30 minutes", "1 hour"],
    "exit_code": ["1", "137", "139", "255"],
    "state": ["CrashLoopBackOff", "Pending", "ImagePullBackOff", "Running (but unready)"],
    "stage": ["build", "test", "deploy", "integration", "smoke test"],
    "percentage": ["5", "10", "15", "20", "25"],
    "endpoint": ["https://api.example.com/webhook", "https://hooks.slack.com/services/xxx", "https://internal.service.local/notify"],
    "local_time": ["50ms", "100ms", "200ms"],
    "query_count": ["150", "500", "1000"],
    "load_level": ["normal", "peak", "burst", "sustained high"],
    "fast_time": ["50ms", "100ms", "200ms"],
    "slow_time": ["5s", "30s", "2min"],
    "change": ["recent deployment", "data growth", "new feature", "dependency update"],
    "vulnerability": ["CVE-2024-XXXX", "SQL injection", "XSS", "CSRF", "SSRF"],
    "tech": ["Express.js", "Django", "Flask", "FastAPI", "Spring Boot", "ASP.NET"],
    "alternative_tech": ["FastAPI", "Django", "Spring Boot", "Express.js", "Rails", "Gin"],
    "use_case": ["REST API", "microservice", "data processing", "real-time communication", "batch processing"],
    "issue": ["potential security flaw", "performance bottleneck", "memory leak", "race condition", "null pointer"],
    "symptom": ["high CPU usage", "memory exhaustion", "connection timeouts", "data corruption", "service unavailability"],
    "scope": ["all users", "specific region", "internal services", "API consumers", "background jobs"],
}


def fill_template(template: str) -> str:
    """Fill in a template with random values."""
    result = template
    for key, values in FILL_VALUES.items():
        placeholder = "{" + key + "}"
        if placeholder in result:
            result = result.replace(placeholder, random.choice(values))
    return result


def generate_synthetic_reasoning(num_samples: int = 50000) -> str:
    """
    Generate synthetic reasoning samples for training.
    
    This is the biggest dataset source. We generate samples that follow
    real engineering reasoning patterns:
    - Observation → Hypothesis → Verification → Result → Revision
    - Self-correction patterns
    - Alternative approach exploration
    """
    logger.info(f"Generating {num_samples} synthetic reasoning samples...")
    
    output_file = OUTPUT_DIR / "synthetic_reasoning.jsonl"
    written = 0
    
    # Collect all scenarios across all domains
    all_scenarios = []
    for domain_key, domain_data in DOMAINS.items():
        for scenario in domain_data["scenarios"]:
            all_scenarios.append({
                "domain": domain_key,
                "domain_label": domain_data["label"],
                "problem_template": scenario["problem"],
                "reasoning_template": scenario["reasoning_template"],
            })
    
    with open(output_file, "w", encoding="utf-8") as f:
        for i in range(num_samples):
            scenario = random.choice(all_scenarios)
            
            # Fill in templates with random values
            problem = fill_template(scenario["problem_template"])
            reasoning = fill_template(scenario["reasoning_template"])
            
            sample = {
                "source": "synthetic",
                "domain": scenario["domain"],
                "domain_label": scenario["domain_label"],
                "instance_id": f"synthetic-{i}",
                "problem": problem,
                "reasoning_type": "engineering_reasoning",
                "reasoning": reasoning,
                "format": "observation_hypothesis",
            }
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            
            if (i + 1) % 5000 == 0:
                logger.info(f"  Generated {i + 1:,} samples...")
    
    logger.info(f"Synthetic reasoning complete: {num_samples} samples written")
    return str(output_file)


def main():
    logger.info("=" * 60)
    logger.info("Step 06: Synthetic Reasoning Dataset Generation")
    logger.info("=" * 60)
    
    output_file = generate_synthetic_reasoning(num_samples=50000)
    logger.info(f"Output: {output_file}")
    
    return output_file


if __name__ == "__main__":
    main()

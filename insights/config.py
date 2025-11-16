# Configuration and KQL Queries for Application Insights Dashboard

# Refresh interval in seconds
REFRESH_INTERVAL = 5

# KQL Queries for different dashboard metrics
KQL_QUERIES = {
    # Total requests in the time range
    'total_requests': """
        requests
        | summarize total_requests = count()
    """,
    
    # Failed requests count
    'failed_requests': """
        requests
        | where success == false
        | summarize failed_requests = count()
    """,
    
    # Average response time
    'avg_response_time': """
        requests
        | summarize avg_response_time = avg(duration)
    """,
    
    # Error rate percentage
    'error_rate': """
        requests
        | summarize 
            total = count(),
            failed = sum(iff(success == false, 1, 0))
        | project error_rate = (failed * 100.0 / total)
    """,
    
    # Availability percentage
    'availability': """
        requests
        | summarize 
            total = count(),
            successful = sum(iff(success == true, 1, 0))
        | project availability = (successful * 100.0 / total)
    """,
    
    # Max memory usage
    'memory_usage': """
        performanceCounters
        | where name == "Private Bytes"
        | summarize max_memory_mb = max(value) / 1024 / 1024
    """,
    
    # Memory usage timeline (by minute)
    'memory_timeline': """
        performanceCounters
        | where name == "Private Bytes"
        | summarize memory_mb = max(value) / 1024 / 1024 by timestamp = bin(timestamp, 1m)
        | order by timestamp asc
    """,
    
    # Max CPU percentage
    'cpu_percentage': """
        performanceCounters
        | where name == "% Processor Time" or name == "Processor Time"
        | summarize max_cpu = max(value)
    """,
    
    # CPU usage timeline (by minute)
    'cpu_timeline': """
        performanceCounters
        | where name == "% Processor Time" or name == "Processor Time"
        | summarize cpu_percentage = max(value) by timestamp = bin(timestamp, 1m)
        | order by timestamp asc
    """,
    
    # Request timeline (by minute)
    'request_timeline': """
        requests
        | summarize request_count = count() by timestamp = bin(timestamp, 1m)
        | order by timestamp asc
    """,
    
    # Response time trend (by minute)
    'response_time_trend': """
        requests
        | summarize avg_duration = avg(duration) by timestamp = bin(timestamp, 1m)
        | order by timestamp asc
    """,
    
    # Top operations by request count
    'top_operations': """
        requests
        | where url !has "healthz"
        | where (url has "orderrequest") or (url has "masterdata")
        | summarize count = count() by operation_Name
        | top 8 by count
        | order by count desc
    """,
    
    # Top slowest operations by average duration
    'slowest_operations': """
        requests
        | where url !has "healthz"
        | where (url has "orderrequest") or (url has "masterdata")
        | summarize avg_duration = avg(duration), count = count() by operation_Name
        | top 8 by avg_duration
        | order by avg_duration desc
    """,
    
    # Errors by status code
    'errors_by_status': """
        requests
        | where success == false
        | summarize error_count = count() by resultCode
        | order by error_count desc
    """,
    
    # Top exceptions
    'top_exceptions': """
        exceptions
        | summarize 
            exception_count = count(),
            first_seen = min(timestamp),
            last_seen = max(timestamp),
            affected_operations = dcount(operation_Name)
        by type, outerMessage, method, problemId
        | top 10 by exception_count
        | order by exception_count desc
        | project type, outerMessage, method, exception_count, affected_operations, first_seen, last_seen, problemId
    """,
    
    # Requests by location (country/region)
    'requests_by_location': """
        requests
        | summarize request_count = count() by client_CountryOrRegion
        | where isnotempty(client_CountryOrRegion)
        | order by request_count desc
    """,
    
    # Recent requests detail (last 15 minutes)
    'recent_requests': """
        requests
        | where timestamp >= ago(15m)
        | where url !has "healthz"
        | where (url has "orderrequest") or (url has "masterdata")
        | project timestamp, name, url, success, resultCode, duration, performanceBucket, client_City, cloud_RoleInstance, cloud_RoleName
        | order by timestamp desc
        | take 200
    """,
    
    # Request duration distribution
    'duration_distribution': """
        requests
        | summarize 
            count = count() by duration_bucket = bin(duration, 100)
        | order by duration_bucket asc
    """,
    
    # Availability by operation
    'availability_by_operation': """
        requests
        | summarize 
            total = count(),
            success_count = sum(iff(success == true, 1, 0))
        by operation_name
        | project operation_name, success_rate = (success_count * 100.0 / total)
        | order by success_rate asc
    """,
    
    # Dependencies - Slow calls
    'slow_dependencies': """
        dependencies
        | summarize 
            avg_duration = avg(duration),
            count = count()
        by target, type
        | where avg_duration > 500
        | order by avg_duration desc
    """,
    
    # Custom events count
    'custom_events': """
        customEvents
        | summarize event_count = count() by name
        | top 10 by event_count
        | order by event_count desc
    """,
}

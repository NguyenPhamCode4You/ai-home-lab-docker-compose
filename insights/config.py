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
    
    # Average memory usage
    'memory_usage': """
        performanceCounters
        | where name == "Available Bytes" or name == "Private Bytes"
        | summarize avg_memory_mb = avg(value) / 1024 / 1024
    """,
    
    # Average CPU percentage
    'cpu_percentage': """
        performanceCounters
        | where name == "% Processor Time" or name == "Processor Time"
        | summarize avg_cpu = avg(value)
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
        | summarize count = count() by operation_Name
        | top 10 by count
        | order by count desc
    """,
    
    # Errors by status code
    'errors_by_status': """
        requests
        | where success == false
        | summarize error_count = count() by resultCode
        | order by error_count desc
    """,
    
    # Response time percentiles (P50, P95, P99)
    'percentile_response_time': """
        requests
        | summarize 
            p50 = percentile(duration, 50),
            p95 = percentile(duration, 95),
            p99 = percentile(duration, 99)
        | project 
            percentile = pack_all(),
            duration_ms = pack_all()
        | mvexpand percentile, duration_ms
    """,
    
    # Alternative percentile query (simpler)
    'percentile_response_time_alt': """
        requests
        | extend percentile = case(
            1 == 1, 'P50',
            1 == 0, 'P95',
            'P99'
        )
        | summarize percentile = 'P50', duration_ms = percentile(duration, 50)
        | union (requests | summarize percentile = 'P95', duration_ms = percentile(duration, 95))
        | union (requests | summarize percentile = 'P99', duration_ms = percentile(duration, 99))
    """,
    
    # Top exceptions
    'top_exceptions': """
        exceptions
        | summarize exception_count = count() by type, outerMessage
        | top 10 by exception_count
        | order by exception_count desc
    """,
    
    # Requests by location (country/region)
    'requests_by_location': """
        requests
        | summarize request_count = count() by client_CountryOrRegion
        | where isnotempty(client_CountryOrRegion)
        | order by request_count desc
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

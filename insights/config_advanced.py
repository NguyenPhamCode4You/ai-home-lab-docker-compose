"""
Advanced configuration and customization options for the Application Insights Dashboard
"""

# Dashboard Configuration
DASHBOARD_CONFIG = {
    "title": "Application Insights Dashboard",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Refresh and Performance Settings
REFRESH_INTERVAL = 5  # seconds
MAX_RETRIES = 3
QUERY_TIMEOUT = 30  # seconds

# Time Range Options
TIME_RANGES = {
    "1 Hour": 1,
    "2 Hours": 2,
    "4 Hours": 4,
    "8 Hours": 8,
    "12 Hours": 12,
    "24 Hours": 24,
    "48 Hours": 48,
    "7 Days": 168,
}

# Chart Color Schemes
COLOR_SCHEMES = {
    "default": "Viridis",
    "categorical": "Plotly",
    "status": {
        "success": "#00CC96",
        "warning": "#FFA15A",
        "error": "#EF553B",
        "info": "#636EFA",
    }
}

# Thresholds for health indicators
THRESHOLDS = {
    "error_rate_warning": 5.0,  # percentage
    "error_rate_critical": 10.0,  # percentage
    "response_time_warning": 1000,  # milliseconds
    "response_time_critical": 5000,  # milliseconds
    "availability_warning": 95.0,  # percentage
    "availability_critical": 90.0,  # percentage
}

# KQL Queries Configuration
KQL_QUERIES = {
    # ============= CORE METRICS =============
    
    'total_requests': """
        requests
        | summarize total_requests = count()
    """,
    
    'failed_requests': """
        requests
        | where success == false
        | summarize failed_requests = count()
    """,
    
    'avg_response_time': """
        requests
        | summarize avg_response_time = avg(duration)
    """,
    
    'error_rate': """
        requests
        | summarize 
            total = count(),
            failed = sum(iff(success == false, 1, 0))
        | project error_rate = (failed * 100.0 / total)
    """,
    
    'availability_rate': """
        requests
        | summarize 
            total = count(),
            success = sum(iff(success == true, 1, 0))
        | project availability = (success * 100.0 / total)
    """,
    
    # ============= TIME SERIES METRICS =============
    
    'request_timeline': """
        requests
        | summarize request_count = count() by timestamp = bin(timestamp, 1m)
        | order by timestamp asc
    """,
    
    'response_time_trend': """
        requests
        | summarize avg_duration = avg(duration) by timestamp = bin(timestamp, 1m)
        | order by timestamp asc
    """,
    
    'error_rate_timeline': """
        requests
        | summarize 
            total = count(),
            failed = sum(iff(success == false, 1, 0))
        by timestamp = bin(timestamp, 1m)
        | project timestamp, error_rate = (failed * 100.0 / total)
        | order by timestamp asc
    """,
    
    # ============= OPERATION METRICS =============
    
    'top_operations': """
        requests
        | summarize count = count() by operation_name
        | top 10 by count
        | order by count desc
    """,
    
    'operation_success_rate': """
        requests
        | summarize 
            total = count(),
            success = sum(iff(success == true, 1, 0))
        by operation_name
        | project operation_name, success_rate = round((success * 100.0 / total), 2)
        | top 10 by success_rate asc
    """,
    
    'operation_avg_duration': """
        requests
        | summarize 
            avg_duration = avg(duration),
            count = count()
        by operation_name
        | where count > 0
        | order by avg_duration desc
    """,
    
    # ============= ERROR METRICS =============
    
    'errors_by_status': """
        requests
        | where success == false
        | summarize error_count = count() by result_code
        | order by error_count desc
    """,
    
    'top_exceptions': """
        exceptions
        | summarize 
            exception_count = count(),
            last_occurrence = max(timestamp)
        by type, outerMessage
        | top 10 by exception_count
        | order by exception_count desc
    """,
    
    'exceptions_by_severity': """
        exceptions
        | summarize exception_count = count() by severityLevel
        | order by exception_count desc
    """,
    
    # ============= PERFORMANCE METRICS =============
    
    'percentile_response_time_alt': """
        let data = requests | project duration;
        let p50 = toscalar(data | summarize percentile(duration, 50));
        let p95 = toscalar(data | summarize percentile(duration, 95));
        let p99 = toscalar(data | summarize percentile(duration, 99));
        union
            (range i from 0 to 0 step 1 | project percentile = 'P50', duration_ms = p50),
            (range i from 0 to 0 step 1 | project percentile = 'P95', duration_ms = p95),
            (range i from 0 to 0 step 1 | project percentile = 'P99', duration_ms = p99)
    """,
    
    'duration_distribution': """
        requests
        | summarize count = count() by duration_bucket = bin(duration, 100)
        | order by duration_bucket asc
    """,
    
    'slow_requests': """
        requests
        | where duration > 1000
        | summarize 
            count = count(),
            avg_duration = avg(duration),
            max_duration = max(duration)
        by operation_name
        | order by avg_duration desc
    """,
    
    # ============= DEPENDENCY METRICS =============
    
    'slow_dependencies': """
        dependencies
        | where type != "InProc"
        | summarize 
            avg_duration = avg(duration),
            count = count(),
            failed_count = sum(iff(success == false, 1, 0))
        by target, type
        | where avg_duration > 100
        | project target, type, avg_duration, count, failed_count, success_rate = round(((count - failed_count) * 100.0 / count), 2)
        | order by avg_duration desc
    """,
    
    'dependency_success_rate': """
        dependencies
        | summarize 
            total = count(),
            success = sum(iff(success == true, 1, 0))
        by target
        | project target, success_rate = round((success * 100.0 / total), 2)
        | order by success_rate asc
    """,
    
    # ============= CUSTOM EVENTS & METRICS =============
    
    'custom_events': """
        customEvents
        | summarize event_count = count() by name
        | top 10 by event_count
        | order by event_count desc
    """,
    
    'page_views': """
        pageViews
        | summarize view_count = count() by name
        | top 10 by view_count
        | order by view_count desc
    """,
    
    # ============= AVAILABILITY METRICS =============
    
    'availability_tests': """
        availabilityResults
        | summarize 
            total = count(),
            success = sum(iff(success == true, 1, 0)),
            avg_duration = avg(duration)
        by name
        | project name, availability_rate = round((success * 100.0 / total), 2), avg_duration, total
        | order by availability_rate asc
    """,
}

# Dashboard Layout Configuration
DASHBOARD_LAYOUT = {
    "metrics_row": {
        "metric_cards": [
            {"key": "total_requests", "title": "Total Requests", "format": "{:,.0f}"},
            {"key": "failed_requests", "title": "Failed Requests", "format": "{:,.0f}"},
            {"key": "avg_response_time", "title": "Avg Response Time", "format": "{:.0f}ms"},
            {"key": "error_rate", "title": "Error Rate", "format": "{:.2f}%"},
        ]
    },
    "charts": [
        {
            "title": "📈 Request Timeline",
            "query": "request_timeline",
            "type": "line",
            "columns": {"x": "timestamp", "y": "request_count"},
            "height": 400,
        },
        {
            "title": "📉 Response Time Trend",
            "query": "response_time_trend",
            "type": "line",
            "columns": {"x": "timestamp", "y": "avg_duration"},
            "height": 400,
        },
        {
            "title": "🎯 Request Distribution by Operation",
            "query": "top_operations",
            "type": "bar",
            "columns": {"x": "operation_name", "y": "count"},
            "height": 400,
        },
        {
            "title": "⚠️ Error Distribution by Status",
            "query": "errors_by_status",
            "type": "pie",
            "columns": {"values": "error_count", "names": "result_code"},
            "height": 400,
        },
    ]
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}

# Feature Flags
FEATURES = {
    "enable_auto_refresh": True,
    "enable_export_data": True,
    "enable_advanced_filters": False,
    "enable_annotations": False,
    "enable_custom_alerts": False,
}

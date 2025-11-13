# BVMS Logging and Monitoring with Azure Application Insights

## Introduction

This documentation provides a comprehensive overview of how the BVMS (Bunker Vessel Management System) application implements logging and monitoring using Azure Application Insights. It is based on the transcript of a meeting discussing the setup, implementation, and best practices for system and application logging in production environments. The goal is to ensure robust monitoring, quick troubleshooting, and maintenance support for the BVMS application.

The session covered the distinction between system and application logs, the use of Serilog for application logging, key features of Azure Application Insights, and strategies for post-production monitoring.

## Types of Logs

BVMS utilizes two primary types of logs to monitor system health and application behavior:

| Log Type             | Description                                                                                              | Responsibility   | Automatic Generation | Examples                                                                     |
| -------------------- | -------------------------------------------------------------------------------------------------------- | ---------------- | -------------------- | ---------------------------------------------------------------------------- |
| **System Logs**      | Automatically generated logs from the Azure environment for infrastructure-related issues.               | Azure Platform   | Yes                  | Failed API calls, SQL query errors, database connection issues.              |
| **Application Logs** | Custom logs written by developers to track business logic, user actions, and heavy processing functions. | Development Team | No                   | Logs for functions like `CalculateConsecutiveVoyage`, user estimate updates. |

- **System Logs**: Provided out-of-the-box when the Application Insights SDK is integrated into frontend and backend. These include metrics on API failures, database calls, and overall system health.
- **Application Logs**: Require explicit implementation using logging libraries. These are crucial for debugging application-specific issues and are the focus for developers to enhance.

## Implementation of Application Logging

### Serilog Integration

BVMS uses **Serilog**, a mature logging library for .NET, to handle application logs. Serilog allows flexible output configurations and structured logging.

- **Key Features**:

  - Supports multiple sinks (outputs): Console, File, and Application Insights.
  - Enables structured logging with customizable output templates.
  - Dependency injection of `ILogger` for easy integration into code.

- **Usage in Code**:

  - Inject `ILogger` into classes or methods.
  - Use for heavy processing functions, e.g., `CalculateConsecutiveVoyage`.
  - Example: Log messages with context, such as function names and custom messages, to trace execution flow.

- **Output Destinations**:
  - **Console**: For local development.
  - **File**: For persistent local storage.
  - **Application Insights**: For production monitoring (primary in Azure environments).

Developers are encouraged to increase the volume of application logs, especially for business-critical and computationally intensive operations, to facilitate better monitoring and debugging.

## Azure Application Insights Features

Azure Application Insights is the central tool for monitoring BVMS in production. It provides real-time insights, historical data, and customizable dashboards. The SDK is integrated into both frontend and backend, enabling automatic correlation and tracing.

### Application Map

- **Purpose**: Provides a quick overview of all application components and their health status.
- **Key Metrics**:
  - Component health (e.g., APIs like Voyage API, Master API).
  - Request counts, failure rates, and database calls over time (e.g., last 24 hours).
  - Example: Voyage API with <1% error rate, Master API with 4% error rate; 700 DB calls for Voyage, 800 for Master.
- **Use Case**: Identify overall system health and spot failing components.

### Live Metrics

- **Purpose**: Real-time monitoring of application performance during active requests.
- **Key Metrics**:
  - Request duration, CPU usage, RAM consumption.
  - Failed requests and incoming request rates.
- **Use Case**: Monitor during high-impact operations (e.g., CPU spikes during heavy calculations like consecutive voyage processing). Helps detect issues like memory leaks leading to application crashes.

### Search (Transaction Search)

- **Purpose**: Elastic search across all logs for quick retrieval.
- **Capabilities**:
  - Search by text (e.g., "consecutive"), correlation ID, or time range.
  - Displays logs with context, including request details and associated traces.
- **Use Case**: Find specific logs for debugging, e.g., logs related to estimate updates or failed requests. Supports end-to-end tracing via correlation IDs.

### Failures

- **Purpose**: Dedicated view for analyzing failed requests.
- **Key Metrics**:
  - Total failures over time, most failing APIs, failure rates.
  - Filter by time (e.g., last 24 hours).
- **Use Case**: Identify problematic APIs for optimization, e.g., APIs with high failure rates requiring fixes.

### Custom Queries (KQL - Kusto Query Language)

- **Purpose**: Advanced querying for custom log analysis.
- **Capabilities**:
  - Write KQL queries for specific data extraction.
  - AI assistance for generating KQL.
  - Examples:
    - Find requests in the last 15 minutes excluding health checks.
    - Calculate average response times, error rates, or slowest APIs.
- **Use Case**: Perform detailed analysis, e.g., identify slow requests or error patterns. Useful for creating custom metrics like "requests by location."

### Workbooks

- **Purpose**: Custom dashboards for visualizing data.
- **Capabilities**:
  - Drag-and-drop components to build charts and reports.
  - Pre-built workbooks (e.g., requests by location) and custom ones.
  - AI-generated visualizations.
- **Use Case**: Create tailored dashboards, e.g., showing request trends, error distributions, or top APIs by call volume.

### Alerts

- **Purpose**: Automated notifications for critical issues.
- **Setup**:
  - Define metrics (e.g., failed requests > threshold).
  - Set thresholds (e.g., >20 failures in a time frame).
  - Actions: Email notifications or Azure app push notifications.
- **Use Case**: Notify maintainers of issues like high failure rates. Alerts can be tested against historical data to refine thresholds.

## Correlation ID and End-to-End Tracing

- **Definition**: A unique identifier automatically assigned by the Application Insights SDK to each frontend request.
- **Functionality**:
  - Propagates through the entire request lifecycle (frontend → backend → database).
  - Enables tracing of user actions across components.
- **Benefits**:
  - Simplifies debugging by linking logs to specific user requests.
  - Supports support ticket integration: Capture correlation ID on frontend failures and send to maintenance teams.
- **Implementation**: No developer action required; handled by SDK. Useful in microservices or multi-environment setups.

## Monitoring and Maintenance Strategy

- **Post-Production Monitoring**:

  - Developers rotate as "scheduling maintainers" to monitor the application for initial days after launch.
  - Focus on Application Map for health overview, Live Metrics for real-time issues, and Search for log investigation.

- **Key Responsibilities**:

  - Monitor for performance degradation (e.g., high CPU/RAM).
  - Investigate failures and correlate with application logs.
  - Use custom KQL and workbooks for deeper analysis.

- **Permissions and Access**:
  - Maintainers added as "log monitoring readers" in Application Insights.
  - Separate access for development vs. production environments.
  - Potential for custom tools/dashboards to limit permissions and enhance security.

## Best Practices

- **Increase Application Logs**: Prioritize logging for heavy business functions to provide traceability.
- **Leverage Correlation IDs**: Use for support tickets and end-to-end debugging.
- **Set Up Alerts**: Configure for critical thresholds to enable proactive responses.
- **Use Custom Queries**: Regularly query logs for insights on performance and errors.
- **Environment Separation**: Ensure logs are directed to appropriate Application Insights instances (dev, staging, production).
- **Permissions Management**: Restrict access to sensitive logs; consider custom dashboards for developers.

## Future Enhancements and Discussion Points

- **Custom Frontend Modules**: Implement logic to capture user IDs, actions, and correlation IDs on failures for automated support tickets.
- **User Activity Logging**: Log user steps (e.g., inputs, calculations) to aid debugging without violating privacy.
- **Separate Monitoring Tools**: Develop custom dashboards or tools for developers to view logs without full Application Insights access.
- **Microservices Considerations**: Ensure correlation IDs work across multiple machines/services.
- **Privacy and Security**: Avoid capturing sensitive user data; focus on technical traces.
- **Rollback and Mitigation**: Post-log analysis, define processes for rollbacks, database reverts, or quick fixes based on identified issues.

## Conclusion

Implementing Azure Application Insights for BVMS provides a robust framework for logging and monitoring, combining automatic system insights with developer-driven application logs. By following the outlined practices, the team can ensure reliable production operations, quick issue resolution, and continuous improvement. Regular training on these tools and iterative enhancements will further strengthen the monitoring capabilities.

This documentation encapsulates the key discussions from the meeting. For further details, refer to the original transcript or contact the development team.

---

_Generated based on meeting transcript: LoggingMonitoringforBVMS_transcription.md_

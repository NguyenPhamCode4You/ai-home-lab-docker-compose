# Azure Application Insights Streamlit Dashboard

A real-time Streamlit dashboard for monitoring Azure Application Insights with multiple KQL queries and auto-refresh capabilities.

## Features

✅ **Real-time Monitoring**: Auto-refresh every 5 seconds
✅ **Multiple KQL Queries**: 14+ pre-configured KQL queries for comprehensive insights
✅ **Interactive Charts**: Beautiful Plotly visualizations including:

- Request timeline (line chart)
- Response time trends
- Operation distribution (bar chart)
- Error distribution by status (pie chart)
- Response time percentiles (P50, P95, P99)
- Exception details (data table)

✅ **Key Metrics**:

- Total Requests
- Failed Requests
- Average Response Time
- Error Rate

✅ **Configurable Time Range**: Select lookback period from 1 to 24 hours
✅ **Azure AD Authentication**: Secure connection using Client Secret credentials

## Prerequisites

- Python 3.8 or higher
- Azure subscription with Application Insights resource
- Azure AD application with appropriate permissions

## Installation

### 1. Clone or Download the Project

```bash
cd insights
```

### 2. Create Virtual Environment (Optional but Recommended)

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Azure Setup

### 1. Get Your Application Insights Details

1. Go to Azure Portal (https://portal.azure.com)
2. Navigate to your Application Insights resource
3. Go to **Settings** > **Properties**
4. Copy your **Application ID** (Resource ID)

### 2. Create Azure AD Application

1. Go to **Azure Active Directory** > **App registrations** > **New registration**
2. Enter a name (e.g., "Insights Dashboard")
3. Click **Register**
4. In the new app registration:
   - Go to **Overview** and copy the **Application (client) ID**
   - Go to **Certificates & secrets** > **New client secret**
   - Copy the client secret value (save it immediately)
   - Copy the **Tenant ID** from Overview

### 3. Grant Permissions

1. Go to **API permissions** in your app registration
2. Click **Add a permission** > **APIs my organization uses**
3. Search for **"Azure Monitor"** and select it
4. Under **Delegated permissions**, select **Data.Read**
5. Click **Add permissions**

### 4. Set Up .env File (Optional)

Create a `.env` file in the `insights` folder:

```env
AZURE_APP_ID=your_application_insights_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
AZURE_TENANT_ID=your_tenant_id
```

## Usage

### Run the Dashboard

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the Dashboard

1. **Configure Azure Connection** (in sidebar):

   - Expand "Azure Connection" section
   - Enter your credentials (Application Insights ID, Client ID, Client Secret, Tenant ID)
   - Click "Connect to Azure" button

2. **Set Time Range** (in sidebar):

   - Use the slider to select how many hours back to analyze (1-24 hours)

3. **View Metrics**:
   - Top row shows summary metrics
   - Multiple charts display various insights
   - Charts auto-refresh every 5 seconds

## Dashboard Sections

### 1. Summary Metrics

- **Total Requests**: Total number of requests in the time period
- **Failed Requests**: Count of failed requests
- **Avg Response Time**: Average duration in milliseconds
- **Error Rate**: Percentage of failed requests

### 2. Request Timeline

Line chart showing request count over time (1-minute buckets)

### 3. Response Time Trend

Line chart showing average response time evolution over time

### 4. Request Distribution by Operation

Bar chart showing top 10 operations by request count

### 5. Error Distribution by Status

Pie chart showing errors grouped by HTTP status codes

### 6. Response Time Percentiles

Bar chart showing P50, P95, and P99 response times

### 7. Exception Details

Data table showing top exceptions with counts

## KQL Queries Included

The dashboard includes the following pre-configured KQL queries:

1. **total_requests** - Total request count
2. **failed_requests** - Failed request count
3. **avg_response_time** - Average request duration
4. **error_rate** - Percentage of failed requests
5. **request_timeline** - Requests over time (1-minute bins)
6. **response_time_trend** - Response time over time
7. **top_operations** - Top 10 operations by count
8. **errors_by_status** - Error distribution by HTTP status
9. **percentile_response_time** - P50, P95, P99 durations
10. **top_exceptions** - Top 10 exceptions
11. **duration_distribution** - Response time distribution
12. **availability_by_operation** - Success rate by operation
13. **slow_dependencies** - Dependencies with >500ms avg duration
14. **custom_events** - Top custom events

## Customization

### Adding Custom Queries

Edit `config.py` and add your KQL query to the `KQL_QUERIES` dictionary:

```python
KQL_QUERIES = {
    'your_query_name': """
        requests
        | where success == true
        | summarize count() by operation_name
    """,
    # ... existing queries
}
```

Then add a new section in `app.py` to display the results:

```python
result = st.session_state.connector.execute_kql(
    KQL_QUERIES['your_query_name'],
    time_range
)
if result is not None and len(result) > 0:
    fig = px.bar(result, x='operation_name', y='count_')
    st.plotly_chart(fig, use_container_width=True)
```

### Changing Refresh Interval

Edit `config.py`:

```python
REFRESH_INTERVAL = 10  # Change from 5 to 10 seconds
```

### Styling

Modify the CSS in the `<style>` tag in `app.py` to customize colors, fonts, and layout.

## Troubleshooting

### "Connection Failed" Error

- Verify all Azure credentials are correct
- Check that the Azure AD app has proper permissions
- Ensure the Application Insights ID is in the correct format

### No Data Showing

- Confirm that there is actual data in your Application Insights resource
- Check the time range selection - increase hours if needed
- Try running a simple test query directly in Azure Portal

### Import Errors

- Ensure all packages are installed: `pip install -r requirements.txt`
- Verify you're using the correct Python environment

## Advanced: Running in Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t insights-dashboard .
docker run -p 8501:8501 insights-dashboard
```

## Performance Considerations

- **Auto-refresh**: Set to 5 seconds but can be increased for better performance
- **Time Range**: Larger time ranges may take longer to query
- **Number of Queries**: More KQL queries mean more API calls per refresh

## API Limits

Azure Monitor has rate limits. The default 5-second refresh with ~10 queries means ~120 API calls per minute. Most Application Insights plans support this, but verify your quotas.

## License

MIT License - Feel free to modify and use as needed.

## Support

For issues with Streamlit: https://docs.streamlit.io/
For Azure Monitor KQL: https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/
For Azure Identity: https://github.com/Azure/azure-sdk-for-python

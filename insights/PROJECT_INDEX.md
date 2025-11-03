# Azure Application Insights Streamlit Dashboard - Project Index

## 📁 Project Structure

```
insights/
├── app.py                          # Main Streamlit application
├── config.py                       # KQL queries and basic configuration
├── config_advanced.py              # Advanced settings and customization
├── utils.py                        # Azure connection helper class
├── utils_enhanced.py               # Enhanced utilities with export functionality
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker container definition
├── docker-compose.yml              # Docker Compose configuration
├── .env.example                    # Environment variables template
├── README.md                       # Full documentation
├── QUICKSTART.md                   # 5-minute quick start guide
├── DEPLOYMENT.md                   # Production deployment guide
└── PROJECT_INDEX.md               # This file
```

---

## 📚 Documentation Files

### README.md

**Complete Reference Guide**

- Feature overview
- Installation instructions
- Azure setup guide (step-by-step)
- Usage instructions
- Dashboard sections description
- 14+ pre-configured KQL queries
- Customization examples
- Troubleshooting guide
- Docker deployment basics

### QUICKSTART.md

**Get Started in 5 Minutes**

- Fast installation
- Quick Azure credential setup
- Immediate dashboard launch
- Customization examples
- Docker quick start
- Performance tips

### DEPLOYMENT.md

**Production Deployment Guide**

- Local development setup
- Docker single container deployment
- Docker Compose deployment
- Production options:
  - Azure Container Instances (ACI)
  - Azure App Service
  - Kubernetes
  - GitHub Actions CI/CD
- Scaling strategies
- Monitoring & logging
- Backup & disaster recovery
- Security best practices

---

## 🔧 Core Application Files

### app.py

**Main Streamlit Application**

- Page configuration and styling
- Session state management
- Sidebar configuration:
  - Azure connection input
  - Time range selector
  - Last refresh indicator
- Dashboard layout:
  - 4 summary metrics (top row)
  - 6+ interactive charts
  - Auto-refresh mechanism (5-second intervals)
- Error handling and user guidance

**Key Features:**

- Real-time metric calculations
- Interactive Plotly charts
- Auto-refresh with countdown
- Azure credentials input validation
- Responsive layout

### config.py

**Query and Configuration Management**

- `REFRESH_INTERVAL`: Set auto-refresh rate (default: 5 seconds)
- `KQL_QUERIES`: Dictionary of 14+ pre-configured queries:
  - **Core Metrics**: total_requests, failed_requests, avg_response_time, error_rate
  - **Time Series**: request_timeline, response_time_trend
  - **Operations**: top_operations, availability_by_operation
  - **Errors**: errors_by_status, top_exceptions
  - **Performance**: percentile_response_time, duration_distribution
  - **Dependencies**: slow_dependencies
  - **Custom Events**: custom_events

### config_advanced.py

**Advanced Customization Options**

- Dashboard styling configuration
- Performance and refresh settings
- Time range options
- Color schemes
- Health indicator thresholds
- Feature flags
- Logging configuration
- Layout templates

### utils.py

**Azure Connectivity**

- `AzureInsightsConnector` class:
  - Initialization with credentials
  - KQL query execution
  - Result conversion to pandas DataFrame
  - Connection testing
  - Error handling and logging

### utils_enhanced.py

**Advanced Utilities**

- Everything from utils.py plus:
  - CSV export functionality
  - Excel export functionality
  - Enhanced error tracking
  - Better logging

---

## 🐳 Docker Files

### Dockerfile

**Container Image Definition**

- Python 3.11 slim base image
- Dependencies installation
- Port 8501 exposure
- Health check configuration
- Streamlit startup command

### docker-compose.yml

**Docker Compose Orchestration**

- Single service: insights-dashboard
- Port mapping: 8501:8501
- Environment variables support
- Volume mounting for .env
- Network configuration
- Auto-restart policy

---

## 📋 Configuration Files

### .env.example

**Environment Variables Template**

- AZURE_APP_ID
- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET
- AZURE_TENANT_ID

Copy to `.env` and fill in your credentials.

### requirements.txt

**Python Dependencies**

```
streamlit==1.28.1
pandas==2.1.3
plotly==5.17.0
azure-identity==1.14.0
azure-monitor-query==1.2.1
python-dotenv==1.0.0
requests==2.31.0
```

---

## 🚀 Quick Start Paths

### Path 1: Local Development (5 minutes)

```bash
pip install -r requirements.txt
# Add credentials via Streamlit UI
streamlit run app.py
```

### Path 2: Docker Single Container

```bash
docker build -t insights-dashboard .
docker run -p 8501:8501 --env-file .env insights-dashboard
```

### Path 3: Docker Compose

```bash
docker-compose up -d
```

---

## 📊 Dashboard Components

### Summary Metrics (Top Row)

- **Total Requests**: `KQL_QUERIES['total_requests']`
- **Failed Requests**: `KQL_QUERIES['failed_requests']`
- **Avg Response Time**: `KQL_QUERIES['avg_response_time']`
- **Error Rate**: `KQL_QUERIES['error_rate']`

### Charts (Auto-Refresh Every 5 Seconds)

1. **Request Timeline** (Line Chart)

   - X: Timestamp (1-minute bins)
   - Y: Request count
   - Query: `request_timeline`

2. **Response Time Trend** (Line Chart)

   - X: Timestamp (1-minute bins)
   - Y: Average duration
   - Query: `response_time_trend`

3. **Request Distribution by Operation** (Bar Chart)

   - X: Operation name
   - Y: Request count
   - Query: `top_operations`

4. **Error Distribution by Status** (Pie Chart)

   - Values: Error count
   - Names: HTTP status codes
   - Query: `errors_by_status`

5. **Response Time Percentiles** (Bar Chart)

   - X: Percentile (P50, P95, P99)
   - Y: Duration in ms
   - Query: `percentile_response_time_alt`

6. **Exception Details** (Data Table)
   - Type, Message, Count
   - Query: `top_exceptions`

---

## 🔑 Available KQL Queries

### Core Metrics

- `total_requests` - Total request count
- `failed_requests` - Failed request count
- `avg_response_time` - Average duration
- `error_rate` - Error percentage
- `availability_rate` - Success percentage

### Time Series

- `request_timeline` - Requests over time (1m bins)
- `response_time_trend` - Avg duration over time
- `error_rate_timeline` - Error rate over time

### Operations

- `top_operations` - Top 10 operations by count
- `operation_success_rate` - Success rate per operation
- `operation_avg_duration` - Avg duration per operation

### Errors & Exceptions

- `errors_by_status` - Errors by HTTP status code
- `top_exceptions` - Top 10 exceptions
- `exceptions_by_severity` - Exception severity distribution

### Performance

- `percentile_response_time_alt` - P50, P95, P99 latencies
- `duration_distribution` - Response time distribution
- `slow_requests` - Requests > 1 second

### Dependencies

- `slow_dependencies` - Slow external calls (>100ms avg)
- `dependency_success_rate` - Success rate per dependency

### Custom

- `custom_events` - Top custom events
- `page_views` - Top page views
- `availability_tests` - Availability test results

---

## 🔐 Azure Setup Checklist

- [ ] Get Application Insights Resource ID from Azure Portal
- [ ] Create Azure AD App Registration
- [ ] Copy Client ID from app registration
- [ ] Create Client Secret and copy value
- [ ] Copy Tenant ID from app registration
- [ ] Grant "Azure Monitor Data Reader" permission
- [ ] Fill in .env or use Streamlit UI input
- [ ] Test connection with "Connect to Azure" button

---

## 💡 Customization Ideas

1. **Add Custom KQL Query**

   - Edit `config.py` KQL_QUERIES
   - Add new visualization in `app.py`

2. **Change Refresh Rate**

   - Edit `REFRESH_INTERVAL` in config.py

3. **Modify Chart Types**

   - Change `px.line()` to `px.area()`, `px.bar()`, etc.

4. **Add Filters**

   - Add dropdowns in sidebar to filter operations, time ranges, etc.

5. **Export Data**

   - Use `utils_enhanced.py` export functions
   - Add download button in `app.py`

6. **Styling**
   - Modify CSS in `<style>` tag in app.py
   - Adjust color schemes in config_advanced.py

---

## 🐛 Troubleshooting

| Issue              | File to Check                | Solution                              |
| ------------------ | ---------------------------- | ------------------------------------- |
| Import errors      | requirements.txt             | Run `pip install -r requirements.txt` |
| Connection failed  | .env or app.py sidebar       | Verify Azure credentials              |
| No data            | config.py queries            | Check Application Insights has data   |
| Slow performance   | config.py                    | Increase REFRESH_INTERVAL             |
| Docker build fails | Dockerfile, requirements.txt | Check Python version and deps         |

---

## 📈 Performance Benchmarks

| Time Range | Query Time | API Calls | Refresh Interval     |
| ---------- | ---------- | --------- | -------------------- |
| 1 hour     | < 1s       | ~10       | 5s (OK)              |
| 24 hours   | 1-3s       | ~10       | 5s (OK)              |
| 7 days     | 3-5s       | ~10       | 10-15s (recommended) |
| 30 days    | 5-10s      | ~10       | 30s (recommended)    |

---

## 🔗 Useful Links

- **Streamlit Docs**: https://docs.streamlit.io/
- **Azure Monitor KQL**: https://docs.microsoft.com/azure/data-explorer/kusto/query/
- **Azure SDK Python**: https://github.com/Azure/azure-sdk-for-python
- **Plotly Charts**: https://plotly.com/python/
- **Docker Docs**: https://docs.docker.com/
- **Application Insights**: https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview

---

## 📝 File Modification Guide

### To Add a New Chart:

1. Add KQL query to `config.py` `KQL_QUERIES`
2. Add chart rendering code in `app.py` dashboard section
3. Use `st.session_state.connector.execute_kql()` to get data
4. Use `px.*` (plotly express) to create visualization
5. Use `st.plotly_chart()` to display

### To Add a Custom Metric:

1. Create KQL query in `config.py`
2. Execute in `app.py` metric section
3. Use `st.metric()` for display
4. Add appropriate formatting

### To Change Refresh Rate:

Edit `config.py`:

```python
REFRESH_INTERVAL = 10  # Change from 5
```

---

## 🎯 Next Steps

1. ✅ **Install** dependencies: `pip install -r requirements.txt`
2. ✅ **Configure** Azure credentials (via .env or UI)
3. ✅ **Run** app: `streamlit run app.py`
4. ✅ **Access** dashboard: http://localhost:8501
5. ✅ **Explore** pre-built visualizations
6. ✅ **Customize** queries and charts
7. ✅ **Deploy** using Docker or cloud platform

---

## 📞 Support

For detailed setup help, see:

- QUICKSTART.md (fastest way to get running)
- README.md (comprehensive reference)
- DEPLOYMENT.md (production setup)

For issues:

- Check logs in app.py error messages
- Review Azure credentials in sidebar
- Verify Application Insights has data
- Check time range is not too far back

---

**Last Updated:** November 2024
**Version:** 1.0.0
**Status:** Production Ready ✅

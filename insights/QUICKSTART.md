# Quick Start Guide - Azure Application Insights Dashboard

## 5-Minute Setup

### Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

### Step 2: Get Azure Credentials (2 minutes)

1. **Application Insights ID:**

   - Go to Azure Portal → Application Insights resource
   - Copy the Resource ID from Properties

2. **Azure AD Credentials:**
   - Go to Azure Portal → Azure Active Directory → App registrations → New registration
   - Name: "Insights Dashboard" → Register
   - Copy: Client ID, Tenant ID
   - Create a client secret and copy the value

### Step 3: Run the Dashboard (1 minute)

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

### Step 4: Configure Connection (1 minute)

1. Open sidebar → "Azure Connection"
2. Enter your 4 credentials
3. Click "Connect to Azure"
4. Set your desired time range
5. Watch the dashboard auto-refresh!

---

## What You Get

### Summary Metrics (Top Row)

- **Total Requests**: How many requests in the period
- **Failed Requests**: Requests that failed
- **Avg Response Time**: How fast responses are
- **Error Rate**: Percentage of failures

### Charts (Auto-Refreshing Every 5 Seconds)

1. **Request Timeline**: See request volume over time
2. **Response Time Trend**: Track performance changes
3. **Top Operations**: Which endpoints get the most traffic
4. **Error Distribution**: What errors are happening
5. **Response Time Percentiles**: P50, P95, P99 latencies
6. **Exception Details**: Top occurring exceptions

---

## Customization Examples

### Change Refresh Rate

Edit `config.py`:

```python
REFRESH_INTERVAL = 10  # from 5 seconds to 10 seconds
```

### Add Custom Query

Edit `config.py`, add to `KQL_QUERIES`:

```python
'my_custom_query': """
    requests
    | where operation_name == "MyEndpoint"
    | summarize count() by bin(timestamp, 1m)
"""
```

Edit `app.py`, add new chart:

```python
result = st.session_state.connector.execute_kql(
    KQL_QUERIES['my_custom_query'],
    time_range
)
if result is not None and len(result) > 0:
    st.plotly_chart(px.line(result, x='timestamp', y='count_'))
```

### Use .env File

1. Copy `.env.example` to `.env`
2. Fill in credentials
3. Modify `app.py` to load from .env (optional enhancement)

---

## Troubleshooting

| Problem             | Solution                                                 |
| ------------------- | -------------------------------------------------------- |
| "Import not found"  | Run `pip install -r requirements.txt`                    |
| "Connection Failed" | Verify credentials are correct                           |
| "No Data"           | Check Application Insights has data & correct time range |
| "Slow refresh"      | Increase `REFRESH_INTERVAL` in config.py                 |
| Port 8501 in use    | Change with `--server.port 8502` flag                    |

---

## Docker Quick Start

```bash
# Build image
docker build -t insights-dashboard .

# Create .env file with credentials
cp .env.example .env
# Edit .env with your values

# Run container
docker run -p 8501:8501 --env-file .env insights-dashboard

# Or with docker-compose
docker-compose up
```

Visit: `http://localhost:8501`

---

## Advanced: Update Credentials at Runtime

The app loads credentials from the sidebar input, so you can:

- Change credentials without restarting
- Switch between different App Insights resources
- Test queries against different environments

---

## Performance Tips

✅ For **1-hour** lookback: Very fast (< 2 seconds per refresh)
✅ For **24-hour** lookback: Still fast (< 5 seconds per refresh)
⚠️ For **7-day+** lookback: May take longer, increase refresh interval

Reduce number of queries:

- Edit `app.py` and comment out some charts
- Queries run in parallel for efficiency

---

## Next Steps

1. ✅ Explore the pre-built dashboards
2. ✅ Add custom queries for your needs
3. ✅ Deploy with Docker for production use
4. ✅ Schedule Docker container for 24/7 monitoring

See `README.md` for complete documentation.

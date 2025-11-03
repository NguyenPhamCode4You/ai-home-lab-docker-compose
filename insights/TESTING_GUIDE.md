# Testing & Validation Guide

## Local Testing

### 1. Verify Installation

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Verify all packages installed
pip list | grep -E "streamlit|plotly|pandas|azure"

# Should see:
# azure-identity
# azure-monitor-query
# pandas
# plotly
# streamlit
```

### 2. Test Azure Connection

```python
# Test Python REPL
python

# Run these commands:
from utils import AzureInsightsConnector

# Test with dummy credentials first
connector = AzureInsightsConnector(
    app_id="test",
    client_id="test",
    client_secret="test",
    tenant_id="test"
)

# Should fail (expected - credentials don't exist)
# But it verifies the import works
```

### 3. Test Streamlit App (Without Azure)

```bash
# This will start but connection will fail - that's OK for now
streamlit run app.py

# Verify:
# ✓ Browser opens to http://localhost:8501
# ✓ Warning message about Azure connection appears
# ✓ Can interact with sidebar
```

### 4. Test With Real Azure Credentials

1. Fill in `.env` with real credentials:

   ```
   AZURE_APP_ID=your_real_id
   AZURE_CLIENT_ID=your_real_id
   AZURE_CLIENT_SECRET=your_real_secret
   AZURE_TENANT_ID=your_real_tenant_id
   ```

2. Restart Streamlit

3. Click "Connect to Azure" in sidebar

4. Should see:
   - ✓ "Connected successfully" message
   - ✓ Metrics begin to populate
   - ✓ Charts render with data
   - ✓ Auto-refresh countdown starts

---

## Docker Testing

### 1. Build Image

```bash
docker build -t insights-dashboard:test .

# Output should show:
# Successfully built [image_id]
# Successfully tagged insights-dashboard:test
```

### 2. Run Container

```bash
# Create test .env
cp .env.example .env.test
# Edit .env.test with credentials

# Run container
docker run -p 8501:8501 --env-file .env.test insights-dashboard:test

# Output should show:
# 2024-XX-XX XX:XX:XX Streamlit app is running...
```

### 3. Test Access

```bash
# In another terminal
curl http://localhost:8501/_stcore/health

# Should return:
# {"status": "ok"}
```

### 4. Docker Compose Test

```bash
# Start with compose
docker-compose up

# Should see:
# insights-dashboard is running...
# Available at http://localhost:8501
```

---

## Performance Testing

### 1. Measure Query Response Times

Add this to `app.py` temporarily:

```python
import time

start_time = time.time()
result = st.session_state.connector.execute_kql(
    KQL_QUERIES['total_requests'],
    "ago(1h)"
)
elapsed = time.time() - start_time
st.write(f"Query took {elapsed:.2f} seconds")
```

**Expected:**

- 1 hour data: < 1 second
- 24 hour data: 1-3 seconds
- 7 day data: 3-5 seconds

### 2. Test Memory Usage

```bash
# Monitor while dashboard is running
# On Windows:
tasklist /v | findstr streamlit

# On macOS/Linux:
ps aux | grep streamlit

# Check memory usage - should be:
# < 200 MB at startup
# < 500 MB with active charts
```

### 3. Test CPU Usage

Dashboard should use minimal CPU when idle.

**Expected:**

- Idle (between refreshes): < 1% CPU
- During refresh: 5-10% CPU spike
- After refresh: < 1% CPU

---

## Data Validation

### 1. Verify Query Results

```python
# Check DataFrame structure
result = connector.execute_kql(
    'requests | count',
    'ago(1h)'
)

# Verify:
# ✓ Not empty
# ✓ Correct column names
# ✓ Data types correct
# ✓ No NaN values
```

### 2. Verify Chart Rendering

- All 6 charts should render without errors
- Charts should have proper labels and titles
- Hover information should work
- Zoom/pan should work
- Legend should display correctly

### 3. Verify Metrics Display

Check top-row metrics:

- ✓ Total Requests shows number
- ✓ Failed Requests shows number
- ✓ Avg Response Time shows ms
- ✓ Error Rate shows percentage

---

## Auto-Refresh Testing

### 1. Verify 5-Second Refresh

```python
# Add debug output to app.py
st.write(f"Refresh time: {datetime.now().strftime('%H:%M:%S')}")

# Watch sidebar "Last Refresh" time
# Should update every 5 seconds
```

### 2. Verify Data Changes

Monitor one metric:

- Request count should change between refreshes
- Response time should fluctuate
- Error count may increase/decrease
- If data changes → refresh is working ✓

### 3. Verify No Stale Data

Create a test script:

```python
from datetime import datetime
from config import REFRESH_INTERVAL

for i in range(12):  # 60 seconds of refreshes
    print(f"Refresh {i+1}: {datetime.now()}")
    time.sleep(REFRESH_INTERVAL)
```

---

## Error Handling Testing

### 1. Test Invalid Credentials

- Enter bad credentials in sidebar
- Click "Connect to Azure"
- Should show error message (not crash)
- App should remain responsive

### 2. Test Network Disconnection

- Disable internet connection
- Click "Connect to Azure"
- Should show connection error
- App should recover when internet returns

### 3. Test Empty Results

- Select time range with no data
- Should show "No data available" gracefully
- Charts should not break
- Metrics should show "N/A"

### 4. Test Query Errors

Manually create a bad query in `config.py`:

```python
'bad_query': "invalid kql syntax"
```

- App should show error message
- Other charts should still work
- App should not crash

---

## Cross-Browser Testing

Test in different browsers:

| Browser | Status | Notes            |
| ------- | ------ | ---------------- |
| Chrome  | ✓      | Best performance |
| Firefox | ✓      | Works well       |
| Safari  | ✓      | Works well       |
| Edge    | ✓      | Works well       |
| IE11    | ✗      | Not supported    |

---

## Accessibility Testing

### 1. Color Contrast

- Verify all text is readable
- Charts have sufficient contrast
- Color-blind mode shows fine
  (Streamlit handles this)

### 2. Keyboard Navigation

- Tab through sidebar controls
- Enter key activates buttons
- Escape closes any modals

### 3. Mobile Responsiveness

- Test on mobile browser
- Sidebar should collapse
- Charts should reflow
- Touch interactions work

---

## Load Testing

### 1. Multiple Concurrent Users

Use Apache Bench (ab):

```bash
# Test with 10 concurrent users for 1 minute
ab -c 10 -t 60 http://localhost:8501

# Expected:
# Should handle 10 users without crashes
# Response times < 2 seconds
# No errors > 5%
```

### 2. Sustained Load Test

```bash
# Test with 5 concurrent users for 10 minutes
ab -c 5 -t 600 http://localhost:8501

# Monitor:
# Memory usage stable?
# CPU usage reasonable?
# Any memory leaks?
```

---

## Security Testing

### 1. Credential Exposure

- Verify `.env` not in git repository
- Verify credentials not in source code
- Check logs don't contain credentials
- Verify secrets not in docker image

### 2. Input Validation

- Try SQL injection in sidebar text inputs
- Should be safe (Streamlit sanitizes)
- Try XSS in any user inputs
- Should be safe

### 3. HTTPS/TLS

For production, ensure:

- [ ] Dashboard behind HTTPS
- [ ] Valid SSL certificate
- [ ] Credentials transmitted securely

---

## Regression Testing Checklist

Before deploying new changes:

- [ ] All dependencies still install
- [ ] App starts without errors
- [ ] Azure connection works
- [ ] All 6 charts render
- [ ] All 4 metrics display
- [ ] Auto-refresh works (5 sec)
- [ ] Time range selection works
- [ ] Sidebar configuration works
- [ ] Error messages appear appropriately
- [ ] No performance degradation
- [ ] All charts interactive (zoom, pan, hover)
- [ ] Docker build succeeds
- [ ] Docker container starts
- [ ] Docker Compose works

---

## Testing Metrics

| Metric                    | Target  | Acceptable Range |
| ------------------------- | ------- | ---------------- |
| Query Response Time (1h)  | < 1s    | < 2s             |
| Query Response Time (24h) | 1-3s    | < 5s             |
| Memory Usage (Idle)       | < 200MB | < 300MB          |
| Memory Usage (Active)     | < 500MB | < 750MB          |
| CPU Usage (Idle)          | < 1%    | < 3%             |
| CPU Usage (Refresh)       | 5-10%   | < 20%            |
| Dashboard Load Time       | < 2s    | < 5s             |
| Chart Render Time         | < 500ms | < 1s             |
| Error Rate                | < 1%    | < 5%             |
| Uptime                    | 99.5%   | > 98%            |

---

## Troubleshooting Test Failures

### Dashboard Won't Start

```bash
# Check Python version
python --version  # Should be 3.8+

# Check if port is in use
# Windows:
netstat -ano | findstr 8501
# macOS/Linux:
lsof -i :8501

# Try different port
streamlit run app.py --server.port 8502
```

### Charts Not Rendering

- Check browser console for JavaScript errors
- Verify data returned from queries
- Check internet connection
- Try hard refresh (Ctrl+Shift+R)

### Auto-Refresh Not Working

- Check `REFRESH_INTERVAL` in config.py
- Verify Streamlit version (>= 1.28)
- Check browser console
- Try clearing browser cache

### Out of Memory

- Reduce time range (query less data)
- Increase `REFRESH_INTERVAL`
- Reduce number of charts
- Restart the app

---

## CI/CD Pipeline Testing

If deploying with GitHub Actions:

```yaml
- name: Run Tests
  run: |
    pip install -r requirements.txt
    pytest tests/ || true  # Optional
    python -m py_compile app.py
    python -m py_compile utils.py
```

---

## Documentation Testing

- [ ] QUICKSTART.md steps work
- [ ] README.md instructions accurate
- [ ] DEPLOYMENT.md processes verified
- [ ] Code comments are accurate
- [ ] Examples in docs run without error

---

## Final Validation Checklist

- [ ] App installs and runs without errors
- [ ] All features working as documented
- [ ] Performance acceptable
- [ ] Security concerns addressed
- [ ] Error handling robust
- [ ] Documentation accurate
- [ ] Docker deployment verified
- [ ] Ready for production use

---

**Test Date:** ******\_\_\_\_******
**Tester:** ******\_\_\_\_******
**Status:** [ ] Pass [ ] Fail
**Notes:** ******\_\_\_\_******

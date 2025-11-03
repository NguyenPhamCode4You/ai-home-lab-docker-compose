import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from config import KQL_QUERIES, REFRESH_INTERVAL
# from utils import AzureInsightsConnector
from utils_managed_identity import AzureInsightsConnector

# Page config
st.set_page_config(
    page_title="Application Insights Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .header-title {
        color: #0078d4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'connector' not in st.session_state:
    st.session_state.connector = None

# Sidebar Configuration
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("---")

# Azure Connection Details
with st.sidebar.expander("Azure Connection", expanded=False):
    app_id = st.text_input("Application Insights ID", type="password", key="app_id")
    client_id = st.text_input("Client ID", type="password", key="client_id")
    client_secret = st.text_input("Client Secret", type="password", key="client_secret")
    tenant_id = st.text_input("Tenant ID", type="password", key="tenant_id")
    
    if st.button("Connect to Azure"):
        with st.spinner("Connecting to Azure..."):
            st.session_state.connector = AzureInsightsConnector(
                app_id=app_id,
                client_id=client_id,
                client_secret=client_secret,
                tenant_id=tenant_id
            )
            st.success("✅ Connected successfully!")

# Time range selection
with st.sidebar.expander("Time Range", expanded=True):
    hours = st.slider("Select hours to look back:", 1, 24, 1)
    st.session_state.hours_lookback = hours

# Auto-refresh indicator
st.sidebar.markdown("---")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Last Refresh", st.session_state.last_refresh.strftime("%H:%M:%S"))
with col2:
    st.metric("Refresh Rate", f"{REFRESH_INTERVAL}s")

# Main Dashboard
st.markdown('<div class="header-title">📊 Application Insights Dashboard</div>', unsafe_allow_html=True)
st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

if st.session_state.connector is None:
    st.warning("⚠️ Please configure Azure connection in the sidebar first.")
    st.info("""
    **Setup Instructions:**
    1. Provide your Azure credentials (App ID, Client ID, Client Secret, Tenant ID)
    2. Click 'Connect to Azure' to establish connection
    3. The dashboard will automatically refresh every 5 seconds
    """)
else:
    try:
        # Get time range
        time_range = f"ago({st.session_state.hours_lookback}h)"
        
        # Create columns for main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Total Requests
            result = st.session_state.connector.execute_kql(
                KQL_QUERIES['total_requests'],
                time_range
            )
            if result is not None and len(result) > 0:
                total_reqs = result.iloc[0]['total_requests']
                st.metric("Total Requests", f"{int(total_reqs):,}")
            else:
                st.metric("Total Requests", "N/A")
        
        with col2:
            # Failed Requests
            result = st.session_state.connector.execute_kql(
                KQL_QUERIES['failed_requests'],
                time_range
            )
            if result is not None and len(result) > 0:
                failed_reqs = result.iloc[0]['failed_requests']
                st.metric("Failed Requests", f"{int(failed_reqs):,}")
            else:
                st.metric("Failed Requests", "N/A")
        
        with col3:
            # Average Response Time
            result = st.session_state.connector.execute_kql(
                KQL_QUERIES['avg_response_time'],
                time_range
            )
            if result is not None and len(result) > 0:
                avg_time = result.iloc[0]['avg_response_time']
                st.metric("Avg Response Time", f"{avg_time:.0f}ms")
            else:
                st.metric("Avg Response Time", "N/A")
        
        with col4:
            # Error Rate
            result = st.session_state.connector.execute_kql(
                KQL_QUERIES['error_rate'],
                time_range
            )
            if result is not None and len(result) > 0:
                error_rate = result.iloc[0]['error_rate']
                st.metric("Error Rate", f"{error_rate:.2f}%")
            else:
                st.metric("Error Rate", "N/A")
        
        st.markdown("---")
        
        # Charts Row 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Request Timeline")
            result = st.session_state.connector.execute_kql(
                KQL_QUERIES['request_timeline'],
                time_range
            )
            if result is not None and len(result) > 0:
                fig = px.line(
                    result,
                    x='timestamp',
                    y='request_count',
                    title="Requests Over Time",
                    labels={'request_count': 'Request Count', 'timestamp': 'Time'}
                )
                fig.update_layout(hovermode='x unified', height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        with col2:
            st.subheader("📉 Response Time Trend")
            result = st.session_state.connector.execute_kql(
                KQL_QUERIES['response_time_trend'],
                time_range
            )
            if result is not None and len(result) > 0:
                fig = px.line(
                    result,
                    x='timestamp',
                    y='avg_duration',
                    title="Average Response Time Over Time",
                    labels={'avg_duration': 'Avg Duration (ms)', 'timestamp': 'Time'}
                )
                fig.update_layout(hovermode='x unified', height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        st.markdown("---")
        
        # Charts Row 2
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Request Distribution by Operation")
            result = st.session_state.connector.execute_kql(
                KQL_QUERIES['top_operations'],
                time_range
            )
            if result is not None and len(result) > 0:
                fig = px.bar(
                    result,
                    x='operation_name',
                    y='count',
                    title="Top Operations",
                    labels={'count': 'Request Count', 'operation_name': 'Operation'},
                    color='count',
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        with col2:
            st.subheader("⚠️ Error Distribution by Status")
            result = st.session_state.connector.execute_kql(
                KQL_QUERIES['errors_by_status'],
                time_range
            )
            if result is not None and len(result) > 0:
                fig = px.pie(
                    result,
                    values='error_count',
                    names='result_code',
                    title="Errors by Status Code",
                    labels={'error_count': 'Error Count', 'result_code': 'Status Code'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        st.markdown("---")
        
        # Charts Row 3
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 P95/P99 Response Times")
            result = st.session_state.connector.execute_kql(
                KQL_QUERIES['percentile_response_time'],
                time_range
            )
            if result is not None and len(result) > 0:
                fig = px.bar(
                    result,
                    x='percentile',
                    y='duration_ms',
                    title="Response Time Percentiles",
                    labels={'duration_ms': 'Duration (ms)', 'percentile': 'Percentile'},
                    color='percentile',
                    color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96']
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        with col1:
            st.subheader("🔍 Exception Details")
            result = st.session_state.connector.execute_kql(
                KQL_QUERIES['top_exceptions'],
                time_range
            )
            if result is not None and len(result) > 0:
                st.dataframe(result, use_container_width=True, height=300)
            else:
                st.info("No exceptions found")
        
        # Auto-refresh mechanism
        placeholder = st.empty()
        
        # Placeholder for refresh countdown
        with st.spinner(f"⏳ Next refresh in {REFRESH_INTERVAL} seconds..."):
            time.sleep(REFRESH_INTERVAL)
        
        st.session_state.last_refresh = datetime.now()
        st.rerun()
    
    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        st.info("Please verify your Azure credentials and try again.")

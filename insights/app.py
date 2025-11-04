import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv
from config import KQL_QUERIES, REFRESH_INTERVAL
from utils_connection_string import AzureInsightsConnector

# Load environment variables from .env file
load_dotenv()

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
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 10  # Default 10 seconds

# Load credentials from environment
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
AZURE_APP_ID = os.getenv("AZURE_APP_ID")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")

# Check if all credentials are loaded
credentials_loaded = all([AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_APP_ID, AZURE_TENANT_ID])

# Sidebar Configuration
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("---")

# Azure Connection Details
with st.sidebar.expander("🔐 Azure Connection", expanded=False):
    if credentials_loaded:
        st.info("✅ Credentials loaded from .env file")
        st.text_input("Client ID", value=AZURE_CLIENT_ID[:20] + "...", disabled=True, key="display_client_id")
        st.text_input("Client Secret", value="•" * 20, disabled=True, key="display_secret")
        st.text_input("App ID", value=AZURE_APP_ID, disabled=True, key="display_app_id")
        st.text_input("Tenant ID", value=AZURE_TENANT_ID[:20] + "...", disabled=True, key="display_tenant_id")
    else:
        st.error("❌ Missing credentials in .env file!")
        st.warning("Please add: AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_APP_ID, AZURE_TENANT_ID")
        AZURE_CLIENT_ID = st.text_input("Client ID", key="manual_client_id")
        AZURE_CLIENT_SECRET = st.text_input("Client Secret", type="password", key="manual_secret")
        AZURE_APP_ID = st.text_input("App ID", key="manual_app_id")
        AZURE_TENANT_ID = st.text_input("Tenant ID", key="manual_tenant_id")
    
    if st.button("🔗 Connect to Azure Application Insights"):
        if not all([AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_APP_ID, AZURE_TENANT_ID]):
            st.error("❌ Please provide all 4 credentials")
        else:
            with st.spinner("Connecting to Application Insights..."):
                try:
                    st.session_state.connector = AzureInsightsConnector(
                        client_id=AZURE_CLIENT_ID,
                        client_secret=AZURE_CLIENT_SECRET,
                        app_id=AZURE_APP_ID,
                        tenant_id=AZURE_TENANT_ID
                    )
                    # Test connection
                    if st.session_state.connector.test_connection():
                        st.session_state.last_refresh = datetime.now()
                        st.success(f"✅ Connected successfully!")
                    else:
                        st.error(f"❌ Connection test failed: {st.session_state.connector.get_last_error()}")
                except Exception as e:
                    st.error(f"❌ Connection failed: {str(e)}")

# Time range selection
with st.sidebar.expander("⏱️ Time Range", expanded=True):
    hours = st.slider("Select hours to look back:", 1, 24, 1)
    st.session_state.hours_lookback = hours

# Refresh rate selection
with st.sidebar.expander("🔄 Auto-Refresh Settings", expanded=True):
    refresh_options = {
        "5 seconds": 5,
        "10 seconds": 10,
        "30 seconds": 30,
        "60 seconds": 60,
        "5 minutes": 300
    }
    
    selected_refresh = st.selectbox(
        "Refresh Rate:",
        options=list(refresh_options.keys()),
        index=1  # Default to 10 seconds
    )
    
    st.session_state.refresh_interval = refresh_options[selected_refresh]

# Auto-refresh indicator
st.sidebar.markdown("---")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Last Refresh", st.session_state.last_refresh.strftime("%H:%M:%S"))
with col2:
    st.metric("Refresh Rate", selected_refresh)

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
                    x='operation_Name',
                    y='count',
                    title="Top Operations",
                    labels={'count': 'Request Count', 'operation_Name': 'Operation'},
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
                    names='resultCode',
                    title="Errors by Status Code",
                    labels={'error_count': 'Error Count', 'resultCode': 'Status Code'}
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
        
        # Get refresh interval from session state
        refresh_interval = st.session_state.refresh_interval
        
        # Placeholder for refresh countdown
        if refresh_interval >= 60:
            refresh_display = f"{refresh_interval // 60} minute(s)"
        else:
            refresh_display = f"{refresh_interval} seconds"
        
        with st.spinner(f"⏳ Next refresh in {refresh_display}..."):
            time.sleep(refresh_interval)
        
        st.session_state.last_refresh = datetime.now()
        st.rerun()
    
    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        st.info("Please verify your Azure credentials and try again.")

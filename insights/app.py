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
        
        # Compact metrics in one row with 5 columns
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Fetch all metrics
        total_reqs_result = st.session_state.connector.execute_kql(KQL_QUERIES['total_requests'], time_range)
        avg_time_result = st.session_state.connector.execute_kql(KQL_QUERIES['avg_response_time'], time_range)
        availability_result = st.session_state.connector.execute_kql(KQL_QUERIES['availability'], time_range)
        memory_result = st.session_state.connector.execute_kql(KQL_QUERIES['memory_usage'], time_range)
        cpu_result = st.session_state.connector.execute_kql(KQL_QUERIES['cpu_percentage'], time_range)
        
        with col1:
            if total_reqs_result is not None and len(total_reqs_result) > 0:
                st.metric("📊 Requests", f"{int(total_reqs_result.iloc[0]['total_requests']):,}", label_visibility="visible")
            else:
                st.metric("📊 Requests", "N/A")

        with col2:
            if avg_time_result is not None and len(avg_time_result) > 0:
                st.metric("⚡ Avg Time", f"{avg_time_result.iloc[0]['avg_response_time']:.0f}ms", label_visibility="visible")
            else:
                st.metric("⚡ Avg Time", "N/A")

        with col3:
            if availability_result is not None and len(availability_result) > 0:
                st.metric("✅ Availability", f"{availability_result.iloc[0]['availability']:.2f}%", label_visibility="visible")
            else:
                st.metric("✅ Availability", "N/A")
        
        with col4:
            if memory_result is not None and len(memory_result) > 0:
                memory_mb = memory_result.iloc[0]['avg_memory_mb']
                if memory_mb >= 1024:
                    st.metric("💾 Memory", f"{memory_mb/1024:.1f} GB", label_visibility="visible")
                else:
                    st.metric("💾 Memory", f"{memory_mb:.0f} MB", label_visibility="visible")
            else:
                st.metric("💾 Memory", "N/A")
        
        with col5:
            if cpu_result is not None and len(cpu_result) > 0:
                st.metric("⚙️ CPU", f"{cpu_result.iloc[0]['avg_cpu']:.1f}%", label_visibility="visible")
            else:
                st.metric("⚙️ CPU", "N/A")
        
        st.markdown("---")
        
        # Combined Request Timeline & Response Time Trend
        st.subheader("📈 Request & Response Time Trends")
        request_timeline = st.session_state.connector.execute_kql(KQL_QUERIES['request_timeline'], time_range)
        response_time_trend = st.session_state.connector.execute_kql(KQL_QUERIES['response_time_trend'], time_range)
        
        if request_timeline is not None and len(request_timeline) > 0 and response_time_trend is not None and len(response_time_trend) > 0:
            # Limit to exactly 30 bars by sampling evenly
            total_bars = 30
            
            if len(request_timeline) > total_bars:
                # Take every Nth row to get exactly 30 bars
                step = len(request_timeline) // total_bars
                request_timeline = request_timeline.iloc[::step][:total_bars]
                response_time_trend = response_time_trend.iloc[::step][:total_bars]
            
            # Create stacked bar chart without scaling
            fig = go.Figure()
            
            # Add request count bar chart (blue) - base layer
            fig.add_trace(go.Bar(
                x=request_timeline['timestamp'],
                y=request_timeline['request_count'],
                name='Request Count',
                marker=dict(color='#636EFA', opacity=0.8),
                hovertemplate='<b>Request Count</b><br>%{y:,.0f}<extra></extra>'
            ))
            
            # Add response time bar chart (red) - stacked on top with actual values
            fig.add_trace(go.Bar(
                x=response_time_trend['timestamp'],
                y=response_time_trend['avg_duration'],
                name='Avg Response Time (ms)',
                marker=dict(color='#EF553B', opacity=0.8),
                hovertemplate='<b>Avg Response Time</b><br>%{y:.0f} ms<extra></extra>'
            ))
            
            # Update layout for stacked bars
            fig.update_layout(
                barmode='stack',
                xaxis=dict(title='Time', showgrid=False),
                yaxis=dict(
                    title='Request Count + Response Time (ms)', 
                    showgrid=True,
                    gridcolor='rgba(128, 128, 128, 0.2)'
                ),
                hovermode='x unified',
                height=350,
                margin=dict(l=50, r=50, t=30, b=40),
                legend=dict(
                    orientation='h', 
                    yanchor='bottom', 
                    y=1.02, 
                    xanchor='right', 
                    x=1,
                    bgcolor='rgba(0,0,0,0)'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available")
        
        st.markdown("---")
        
        # Compact 3-column layout for remaining charts
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🎯 Top Operations")
            result = st.session_state.connector.execute_kql(KQL_QUERIES['top_operations'], time_range)
            if result is not None and len(result) > 0:
                fig = px.bar(
                    result,
                    x='operation_Name',
                    y='count',
                    labels={'count': 'Count', 'operation_Name': 'Operation'},
                    color='count',
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=300, showlegend=False, margin=dict(l=10, r=10, t=30, b=10))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        with col2:
            st.subheader("⚠️ Error Status")
            result = st.session_state.connector.execute_kql(KQL_QUERIES['errors_by_status'], time_range)
            if result is not None and len(result) > 0:
                # Define color mapping based on error severity
                def get_error_color(code):
                    code_str = str(code)
                    if code_str.startswith('5'):  # 5xx - Server errors (most severe)
                        return '#DC143C'  # Crimson red
                    elif code_str in ['400', '401', '403']:  # Auth/Permission errors
                        return '#FF4500'  # Orange red
                    elif code_str == '404':  # Not found (less severe)
                        return '#4169E1'  # Royal blue
                    elif code_str.startswith('4'):  # Other 4xx client errors
                        return '#FFA500'  # Orange
                    else:
                        return '#808080'  # Gray for unknown
                
                # Create color list for each status code
                colors = [get_error_color(code) for code in result['resultCode']]
                
                fig = px.pie(
                    result,
                    values='error_count',
                    names='resultCode',
                    labels={'error_count': 'Count', 'resultCode': 'Code'},
                    color_discrete_sequence=colors
                )
                fig.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        with col3:
            st.subheader("📊 Percentiles")
            result = st.session_state.connector.execute_kql(KQL_QUERIES['percentile_response_time'], time_range)
            if result is not None and len(result) > 0:
                fig = px.bar(
                    result,
                    x='percentile',
                    y='duration_ms',
                    labels={'duration_ms': 'ms', 'percentile': 'P'},
                    color='percentile',
                    color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96']
                )
                fig.update_layout(height=300, showlegend=False, margin=dict(l=10, r=10, t=30, b=10))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        st.markdown("---")
        
        # World Map and Exception Details
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🌍 Requests by Location")
            location_result = st.session_state.connector.execute_kql(KQL_QUERIES['requests_by_location'], time_range)
            if location_result is not None and len(location_result) > 0:
                # Create world map with bubble markers
                fig = px.scatter_geo(
                    location_result,
                    locations='client_CountryOrRegion',
                    locationmode='country names',
                    size='request_count',
                    hover_name='client_CountryOrRegion',
                    hover_data={'request_count': ':,', 'client_CountryOrRegion': False},
                    size_max=60,
                    color='request_count',
                    color_continuous_scale='Plasma',  # More vivid color scale
                    labels={'request_count': 'Requests'}
                )
                fig.update_layout(
                    height=350,
                    margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor='rgba(14,17,23,1)',  # Dark background
                    plot_bgcolor='rgba(14,17,23,1)',
                    font=dict(color='white'),
                    geo=dict(
                        bgcolor='rgba(14,17,23,1)',  # Match Streamlit dark theme
                        showland=True,
                        landcolor='rgb(30, 35, 45)',  # Dark land
                        showocean=True,
                        oceancolor='rgb(20, 23, 30)',  # Darker ocean
                        showcountries=True,
                        countrycolor='rgb(80, 80, 80)',  # Gray borders
                        coastlinecolor='rgb(60, 60, 60)',
                        showlakes=True,
                        lakecolor='rgb(20, 23, 30)',
                        projection_type='natural earth',
                        showframe=False
                    ),
                    coloraxis_colorbar=dict(
                        title=dict(text='Requests', font=dict(color='white')),
                        tickfont=dict(color='white')
                    )
                )
                # Make markers glow effect
                fig.update_traces(
                    marker=dict(
                        line=dict(width=1, color='rgba(255, 255, 255, 0.3)'),
                        opacity=0.9
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No location data available")
        
        with col2:
            st.subheader("🔍 Exceptions")
            result = st.session_state.connector.execute_kql(KQL_QUERIES['top_exceptions'], time_range)
            if result is not None and len(result) > 0:
                st.dataframe(result, use_container_width=True, height=350)
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

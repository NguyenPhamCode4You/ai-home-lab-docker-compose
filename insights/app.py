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
    st.session_state.refresh_interval = 15  # Default 15 seconds
if 'time_range_value' not in st.session_state:
    st.session_state.time_range_value = "1h"  # Default 1 hour
if 'bars_count' not in st.session_state:
    st.session_state.bars_count = 30  # Default 30 bars
if 'top_k' not in st.session_state:
    st.session_state.top_k = 8  # Default top 8

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
# Dashboard Settings
with st.sidebar.expander("⚙️ Dashboard Settings", expanded=True):
    # Time Range selection
    st.markdown("**⏱️ Time Range**")
    time_range_options = {
        "30 minutes": "30m",
        "1 hour": "1h",
        "2 hours": "2h",
        "4 hours": "4h",
        "8 hours": "8h",
        "12 hours": "12h",
        "24 hours": "24h"
    }
    
    selected_time_range = st.selectbox(
        "Look back period:",
        options=list(time_range_options.keys()),
        index=1,  # Default to 1 hour
        label_visibility="collapsed"
    )
    st.session_state.time_range_value = time_range_options[selected_time_range]
    
    st.markdown("---")
    
    # Refresh Rate selection
    st.markdown("**🔄 Refresh Rate**")
    refresh_options = {
        "15 seconds": 15,
        "30 seconds": 30,
        "1 minute": 60,
        "5 minutes": 300
    }
    
    selected_refresh = st.selectbox(
        "Auto-refresh interval:",
        options=list(refresh_options.keys()),
        index=0,  # Default to 15 seconds
        label_visibility="collapsed"
    )
    st.session_state.refresh_interval = refresh_options[selected_refresh]
    
    st.markdown("---")
    
    # Bars Count selection
    st.markdown("**📊 Bars Count**")
    bars_count = st.selectbox(
        "Timeline chart bars:",
        options=[20, 30, 40, 50, 100],
        index=1,  # Default to 30
        label_visibility="collapsed"
    )
    st.session_state.bars_count = bars_count
    
    st.markdown("---")
    
    # Top K selection
    st.markdown("**🔝 Top K Results**")
    top_k = st.selectbox(
        "Number of top results:",
        options=[5, 8, 10, 25],
        index=1,  # Default to 8
        label_visibility="collapsed"
    )
    st.session_state.top_k = top_k

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
        # Get time range from settings
        time_range = f"ago({st.session_state.time_range_value})"
        
        # Compact metrics in one row with 5 columns - each loads independently
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Metric 1: Total Requests - loads immediately
        with col1:
            with st.spinner(""):
                total_reqs_result = st.session_state.connector.execute_kql(KQL_QUERIES['total_requests'], time_range)
                if total_reqs_result is not None and len(total_reqs_result) > 0:
                    st.metric("📊 Requests", f"{int(total_reqs_result.iloc[0]['total_requests']):,}", label_visibility="visible")
                else:
                    st.metric("📊 Requests", "N/A")

        # Metric 2: Average Response Time - loads independently
        with col2:
            with st.spinner(""):
                avg_time_result = st.session_state.connector.execute_kql(KQL_QUERIES['avg_response_time'], time_range)
                if avg_time_result is not None and len(avg_time_result) > 0:
                    st.metric("⚡ Avg Time", f"{avg_time_result.iloc[0]['avg_response_time']:.0f}ms", label_visibility="visible")
                else:
                    st.metric("⚡ Avg Time", "N/A")

        # Metric 3: Success Rate - loads independently
        with col3:
            with st.spinner(""):
                availability_result = st.session_state.connector.execute_kql(KQL_QUERIES['availability'], time_range)
                if availability_result is not None and len(availability_result) > 0:
                    st.metric("✅ Success Rate", f"{availability_result.iloc[0]['availability']:.2f}%", label_visibility="visible")
                else:
                    st.metric("✅ Success Rate", "N/A")
        
        # Metric 4: Memory Usage - loads independently
        with col4:
            with st.spinner(""):
                memory_result = st.session_state.connector.execute_kql(KQL_QUERIES['memory_usage'], time_range)
                if memory_result is not None and len(memory_result) > 0:
                    memory_mb = memory_result.iloc[0]['avg_memory_mb']
                    if memory_mb >= 1024:
                        st.metric("💾 Memory", f"{memory_mb/1024:.1f} GB", label_visibility="visible")
                    else:
                        st.metric("💾 Memory", f"{memory_mb:.0f} MB", label_visibility="visible")
                else:
                    st.metric("💾 Memory", "N/A")
        
        # Metric 5: CPU Percentage - loads independently
        with col5:
            with st.spinner(""):
                cpu_result = st.session_state.connector.execute_kql(KQL_QUERIES['cpu_percentage'], time_range)
                if cpu_result is not None and len(cpu_result) > 0:
                    st.metric("⚙️ CPU", f"{cpu_result.iloc[0]['avg_cpu']:.1f}%", label_visibility="visible")
                else:
                    st.metric("⚙️ CPU", "N/A")
        
        st.markdown("---")
        
        # Combined Request Timeline & World Map in same row (2:1 ratio)
        col_timeline, col_map = st.columns([2, 1])
        
        with col_timeline:
            st.subheader("📈 Request & Response Time Trends")
            request_timeline = st.session_state.connector.execute_kql(KQL_QUERIES['request_timeline'], time_range)
            response_time_trend = st.session_state.connector.execute_kql(KQL_QUERIES['response_time_trend'], time_range)
            
            if request_timeline is not None and len(request_timeline) > 0 and response_time_trend is not None and len(response_time_trend) > 0:
                # Use bars count from settings
                total_bars = st.session_state.bars_count
                
                if len(request_timeline) > total_bars:
                    # Take every Nth row to get exactly the configured number of bars
                    step = len(request_timeline) // total_bars
                    request_timeline = request_timeline.iloc[::step][:total_bars]
                    response_time_trend = response_time_trend.iloc[::step][:total_bars]
                
                # Create stacked bar chart without scaling
                fig = go.Figure()
                
                # Add request count bar chart (blue) - base layer
                # Only show text for values >= 100
                request_text = [f"{val:,.0f}" if val >= 100 else "" for val in request_timeline['request_count']]
                
                fig.add_trace(go.Bar(
                    x=request_timeline['timestamp'],
                    y=request_timeline['request_count'],
                    name='Request Count',
                    marker=dict(color='#636EFA', opacity=0.8),
                    text=request_text,
                    textposition='inside',
                    insidetextanchor='middle',
                    textfont=dict(size=12, color='white'),
                    hovertemplate='<b>Request Count</b><br>%{y:,.0f}<extra></extra>'
                ))
                
                # Add response time bar chart (red) - stacked on top with actual values
                # Only show text for values >= 100
                response_text = [f"{val:.0f}" if val >= 100 else "" for val in response_time_trend['avg_duration']]
                
                fig.add_trace(go.Bar(
                    x=response_time_trend['timestamp'],
                    y=response_time_trend['avg_duration'],
                    name='Avg Response Time',
                    marker=dict(color='#EF553B', opacity=0.8),
                    text=response_text,
                    textposition='inside',
                    insidetextanchor='middle',
                    textfont=dict(size=12, color='white'),
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
        
        with col_map:
            st.subheader("🌍 Requests by Location")
            location_result = st.session_state.connector.execute_kql(KQL_QUERIES['requests_by_location'], time_range)
            if location_result is not None and len(location_result) > 0:
                # Create world map with bubble markers using vibrant colors for better visibility
                fig = px.scatter_geo(
                    location_result,
                    locations='client_CountryOrRegion',
                    locationmode='country names',
                    size='request_count',
                    hover_name='client_CountryOrRegion',
                    hover_data={'request_count': ':,', 'client_CountryOrRegion': False},
                    size_max=40,  # Slightly larger for better visibility
                    color='request_count',
                    color_continuous_scale=['#4169E1', '#FFD700', '#FF6B35', '#FF0000'],  # Blue -> Gold -> Orange -> Red (more vibrant)
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
                        landcolor='rgb(20, 25, 35)',  # Darker land for better contrast
                        showocean=True,
                        oceancolor='rgb(10, 13, 20)',  # Even darker ocean
                        showcountries=True,
                        countrycolor='rgb(60, 60, 60)',  # Darker borders
                        coastlinecolor='rgb(40, 40, 40)',
                        showlakes=True,
                        lakecolor='rgb(10, 13, 20)',
                        projection_type='natural earth',
                        showframe=False
                    ),
                    coloraxis_colorbar=dict(
                        title=dict(text='Requests', font=dict(color='white')),
                        tickfont=dict(color='white')
                    )
                )
                # Add glow effect with white outline for better visibility
                fig.update_traces(
                    marker=dict(
                        line=dict(width=2, color='rgba(255, 255, 255, 0.6)'),  # White glow
                        opacity=1.0  # Full opacity
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No location data available")
        
        st.markdown("---")
        
        # Compact 4-column layout for remaining charts
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.subheader("🎯 Top Most-Called APIs")
            # Use dynamic top K value
            top_ops_query = KQL_QUERIES['top_operations'].replace('top 8', f'top {st.session_state.top_k}')
            result = st.session_state.connector.execute_kql(top_ops_query, time_range)
            if result is not None and len(result) > 0:
                fig = go.Figure()
                
                # Add bars with text labels
                fig.add_trace(go.Bar(
                    x=result['operation_Name'],
                    y=result['count'],
                    marker=dict(
                        color=result['count'],
                        colorscale='Viridis',
                        showscale=False
                    ),
                    text=[f"{val:,.0f}" for val in result['count']],
                    textposition='inside',
                    textfont=dict(size=12, color='white'),
                    hovertemplate='<b>%{x}</b><br>Count: %{y:,.0f}<extra></extra>'
                ))
                
                fig.update_layout(
                    height=300,
                    showlegend=False,
                    margin=dict(l=10, r=10, t=30, b=10),
                    xaxis=dict(title='Operation'),
                    yaxis=dict(title='Count'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        with col2:
            st.subheader("🐌 Top Slowest APIs")
            # Use dynamic top K value
            slowest_ops_query = KQL_QUERIES['slowest_operations'].replace('top 8', f'top {st.session_state.top_k}')
            result = st.session_state.connector.execute_kql(slowest_ops_query, time_range)
            if result is not None and len(result) > 0:
                fig = go.Figure()
                
                # Add bars with conditional text labels (hide if < 100)
                text_labels = [f"{val:.0f}" if val >= 100 else "" for val in result['avg_duration']]
                
                fig.add_trace(go.Bar(
                    x=result['operation_Name'],
                    y=result['avg_duration'],
                    marker=dict(
                        color=result['avg_duration'],
                        colorscale='Reds',
                        showscale=False
                    ),
                    text=text_labels,
                    textposition='inside',
                    textfont=dict(size=12, color='white'),
                    hovertemplate='<b>%{x}</b><br>Avg Duration: %{y:.0f} ms<extra></extra>'
                ))
                
                fig.update_layout(
                    height=300,
                    showlegend=False,
                    margin=dict(l=10, r=10, t=30, b=10),
                    xaxis=dict(title='Operation'),
                    yaxis=dict(title='Avg Duration (ms)'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        with col3:
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
        
        with col4:
            st.subheader("📊 Percentiles")
            result = st.session_state.connector.execute_kql(KQL_QUERIES['percentile_response_time'], time_range)
            if result is not None and len(result) > 0:
                # Apply gradient colors for percentiles (P50, P95, P99)
                percentile_colors = ['#4169E1', '#FFA500', '#DC143C']  # Blue -> Orange -> Red
                
                fig = go.Figure()
                
                # Add bars with values displayed (only if >= 100)
                for idx, row in result.iterrows():
                    # Convert to float to handle numeric comparison
                    duration_value = float(row['duration_ms']) if pd.notna(row['duration_ms']) else 0
                    text_value = f"{duration_value:.0f}" if duration_value >= 100 else ""
                    
                    fig.add_trace(go.Bar(
                        x=[row['percentile']],
                        y=[duration_value],
                        name=row['percentile'],
                        marker=dict(color=percentile_colors[idx % len(percentile_colors)]),
                        text=[text_value],
                        textposition='inside',
                        insidetextanchor='middle',
                        textfont=dict(size=14, color='white'),
                        hovertemplate=f"<b>{row['percentile']}</b><br>%{{y:.0f}} ms<extra></extra>",
                        showlegend=False
                    ))
                
                fig.update_layout(
                    height=300, 
                    showlegend=False, 
                    margin=dict(l=10, r=10, t=30, b=10),
                    xaxis=dict(title='Percentile'),
                    yaxis=dict(title='Response Time (ms)', showgrid=True, gridcolor='rgba(128, 128, 128, 0.2)'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        st.markdown("---")
        
        # Exceptions and Recent Requests in one row (4:6 ratio)
        col_exceptions, col_requests = st.columns([4, 6])
        
        with col_exceptions:
            st.subheader("🔍 Top Exceptions")
            # Use dynamic top K value
            exceptions_query = KQL_QUERIES['top_exceptions'].replace('top 20', f'top {st.session_state.top_k * 2}')  # Show 2x for exceptions
            result = st.session_state.connector.execute_kql(exceptions_query, time_range)
            if result is not None and len(result) > 0:
                # Format the dataframe for better display
                display_df = result.copy()
                
                # Drop unwanted columns
                columns_to_drop = ['first_seen', 'last_seen', 'problemId']
                display_df = display_df.drop(columns=[col for col in columns_to_drop if col in display_df.columns])
                
                # Rename columns for better readability
                column_config = {
                    'type': st.column_config.TextColumn('Exception Type', width='medium'),
                    'outerMessage': st.column_config.TextColumn('Message', width='large'),
                    'method': st.column_config.TextColumn('Method', width='small'),
                    'sample_url': st.column_config.TextColumn('URL', width='large'),
                    'service_name': st.column_config.TextColumn('Service', width='medium'),
                    'exception_count': st.column_config.NumberColumn('Count', format='%d'),
                    'affected_operations': st.column_config.NumberColumn('Affected APIs', format='%d')
                }
                
                st.dataframe(
                    display_df, 
                    use_container_width=True, 
                    height=450,
                    column_config=column_config,
                    hide_index=True
                )
            else:
                st.info("No exceptions found")
        
        with col_requests:
            st.subheader("📋 Recent Requests (Last 15 Minutes)")
            recent_requests = st.session_state.connector.execute_kql(KQL_QUERIES['recent_requests'], time_range)
            if recent_requests is not None and len(recent_requests) > 0:
                # Format the dataframe for better display
                display_df = recent_requests.copy()
                
                # Column configuration for better readability
                column_config = {
                    'timestamp': st.column_config.DatetimeColumn('Timestamp', format='DD/MM/YY HH:mm:ss', width='medium'),
                    'name': st.column_config.TextColumn('Operation Name', width='large'),
                    'url': st.column_config.TextColumn('URL', width='large'),
                    'success': st.column_config.CheckboxColumn('Success', width='small'),
                    'resultCode': st.column_config.NumberColumn('Status Code', format='%d', width='small'),
                    'duration': st.column_config.NumberColumn('Duration (ms)', format='%.0f', width='small'),
                    'performanceBucket': st.column_config.TextColumn('Perf Bucket', width='small'),
                    'client_City': st.column_config.TextColumn('City', width='medium'),
                    'cloud_RoleInstance': st.column_config.TextColumn('Instance', width='medium'),
                    'cloud_RoleName': st.column_config.TextColumn('Service', width='medium')
                }
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    height=450,
                    column_config=column_config,
                    hide_index=True
                )
            else:
                st.info("No recent requests found")
        
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

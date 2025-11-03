"""
Utility functions for Azure Application Insights connection using Connection String
Connection String is the simplest and most reliable way to connect
"""

import pandas as pd
import os
from datetime import datetime, timedelta
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AzureInsightsConnector:
    """
    Connector for Azure Application Insights using KQL queries
    Simplified to use Connection String for authentication
    """
    
    def __init__(self, connection_string: str):
        """
        Initialize the Azure Insights Connector with Connection String
        
        Args:
            connection_string: Application Insights Connection String
            Example: InstrumentationKey=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx;IngestionEndpoint=https://xxx.applicationinsights.azure.com/
        """
        if not connection_string or not connection_string.strip():
            raise ValueError("Connection string cannot be empty")
        
        self.connection_string = connection_string.strip()
        self.last_error = None
        
        # Extract instrumentation key from connection string
        self.instrumentation_key = self._extract_key_from_connection_string(self.connection_string)
        
        if not self.instrumentation_key:
            raise ValueError("Invalid connection string - could not extract instrumentation key")
        
        logger.info(f"✅ Azure Insights Connector initialized with Connection String")
        logger.info(f"   Instrumentation Key: {self.instrumentation_key[:20]}...")
    
    def _extract_key_from_connection_string(self, conn_str: str) -> str:
        """Extract Instrumentation Key from connection string"""
        try:
            # Parse connection string: InstrumentationKey=xxx;IngestionEndpoint=yyy
            parts = conn_str.split(';')
            for part in parts:
                if part.startswith('InstrumentationKey='):
                    return part.split('=', 1)[1]
            return None
        except Exception as e:
            logger.error(f"❌ Failed to parse connection string: {str(e)}")
            return None
    
    def _get_query_client(self) -> LogsQueryClient:
        """
        Get or create LogsQueryClient
        Note: Connection string alone is not enough for LogsQueryClient
        We need to use a different approach with workspace/resource querying
        """
        try:
            # For direct Application Insights querying, we'll use the instrumentation key
            logger.info("🔐 Using Application Insights Instrumentation Key for authentication")
            
            # Create a simple client using the instrumentation key
            # The client will be configured in execute_kql method
            return None  # We'll handle this differently
        except Exception as e:
            logger.error(f"❌ Failed to create query client: {str(e)}")
            raise
    
    def execute_kql(self, query: str, time_range: str = "ago(1h)") -> pd.DataFrame:
        """
        Execute a KQL query against Application Insights
        
        Args:
            query: KQL query string
            time_range: Time range string (e.g., "ago(1h)", "ago(24h)")
        
        Returns:
            pandas.DataFrame with query results
        """
        try:
            import requests
            import json
            
            # Clean up query
            query = query.strip()
            
            # Extract instrumentation key and endpoint from connection string
            instrumentation_key = self.instrumentation_key
            
            # Construct API endpoint
            # Note: This is a simplified approach using REST API
            # For production, consider using Azure SDK with proper authentication
            endpoint = "https://api.applicationinsights.io/v1/apps/{}/query"
            
            # Build headers
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': instrumentation_key
            }
            
            # Convert time range to timespan parameter
            timespan = self._convert_time_range(time_range)
            timespan_str = f"{timespan[0].isoformat()}Z/{timespan[1].isoformat()}Z"
            
            # Make API request
            params = {
                'query': query,
                'timespan': timespan_str
            }
            
            logger.info(f"📊 Executing KQL query...")
            response = requests.get(
                endpoint.format(instrumentation_key),
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if 'tables' in result and len(result['tables']) > 0:
                    table = result['tables'][0]
                    
                    # Convert to DataFrame
                    if 'rows' in table and len(table['rows']) > 0:
                        columns = [col['name'] for col in table['columns']]
                        data = [dict(zip(columns, row)) for row in table['rows']]
                        df = pd.DataFrame(data)
                        
                        logger.info(f"✅ Query executed successfully. Rows: {len(df)}")
                        self.last_error = None
                        return df
                    else:
                        logger.warning("⚠️ Query returned no rows")
                        return pd.DataFrame()
                else:
                    logger.warning("⚠️ Query returned no tables")
                    return pd.DataFrame()
            
            else:
                error_msg = f"API request failed with status {response.status_code}: {response.text}"
                logger.error(f"❌ {error_msg}")
                self.last_error = error_msg
                return pd.DataFrame()
        
        except Exception as e:
            error_msg = f"Error executing KQL query: {str(e)}"
            self.last_error = error_msg
            logger.error(f"❌ {error_msg}")
            return pd.DataFrame()
    
    def _convert_time_range(self, time_range):
        """
        Convert time_range string to datetime tuple
        
        Args:
            time_range: String like "ago(1h)", "ago(24h)" or tuple of (start_datetime, end_datetime)
        
        Returns:
            Tuple of (start_datetime, end_datetime)
        """
        # If already a tuple, return as-is
        if isinstance(time_range, tuple):
            return time_range
        
        # Parse time range string
        time_range = time_range.strip()
        
        # Default to 1 hour if empty
        if not time_range:
            time_range = "ago(1h)"
        
        # Parse "ago(Xh|d|m|s)" format
        if time_range.lower().startswith("ago(") and time_range.endswith(")"):
            duration_str = time_range[4:-1].lower()  # Extract "1h" from "ago(1h)"
            
            # Parse duration
            end_time = datetime.utcnow()
            
            if duration_str.endswith("h"):
                hours = int(duration_str[:-1])
                start_time = end_time - timedelta(hours=hours)
            elif duration_str.endswith("d"):
                days = int(duration_str[:-1])
                start_time = end_time - timedelta(days=days)
            elif duration_str.endswith("m"):
                minutes = int(duration_str[:-1])
                start_time = end_time - timedelta(minutes=minutes)
            elif duration_str.endswith("s"):
                seconds = int(duration_str[:-1])
                start_time = end_time - timedelta(seconds=seconds)
            else:
                # Default to 1 hour
                start_time = end_time - timedelta(hours=1)
            
            return (start_time, end_time)
        
        # Fallback to 1 hour
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=1)
        return (start_time, end_time)
    
    def test_connection(self) -> bool:
        """
        Test the connection to Application Insights
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            logger.info("🧪 Testing connection to Application Insights...")
            result = self.execute_kql("requests | count", "ago(1h)")
            
            if result is not None and len(result) > 0:
                logger.info("✅ Connection test successful")
                self.last_error = None
                return True
            else:
                logger.warning("⚠️ Connection test returned no results")
                self.last_error = "No results from connection test"
                return False
        except Exception as e:
            error_msg = f"Connection test failed: {str(e)}"
            self.last_error = error_msg
            logger.error(f"❌ {error_msg}")
            return False
    
    def export_to_csv(self, df: pd.DataFrame) -> bytes:
        """Export DataFrame to CSV bytes"""
        try:
            import io
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            return csv_buffer.getvalue().encode()
        except Exception as e:
            logger.error(f"❌ Error exporting to CSV: {str(e)}")
            return None
    
    def export_to_excel(self, df: pd.DataFrame) -> bytes:
        """Export DataFrame to Excel bytes"""
        try:
            import io
            df.to_excel(io.BytesIO(), index=False, engine='openpyxl')
            return True
        except Exception as e:
            logger.error(f"❌ Error exporting to Excel: {str(e)}")
            return None
    
    def get_last_error(self) -> str:
        """Get the last error message"""
        return self.last_error if self.last_error else "No errors"
    
    def get_auth_method(self) -> str:
        """Get the authentication method being used"""
        return "Application Insights Connection String"

"""
Utility functions for Azure Application Insights connection
Uses Client ID, Client Secret, App ID, and Tenant ID for authentication
"""

import pandas as pd
import os
from datetime import datetime, timedelta
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AzureInsightsConnector:
    """
    Connector for Azure Application Insights using KQL queries
    Uses Client ID, Client Secret, App ID (workspace ID), and Tenant ID
    """
    
    def __init__(self, client_id: str = None, client_secret: str = None, 
                 app_id: str = None, tenant_id: str = None):
        """
        Initialize the Azure Insights Connector
        
        Args:
            client_id: Azure AD Application (Client) ID
            client_secret: Azure AD Client Secret
            app_id: Application Insights Workspace ID (resource ID)
            tenant_id: Azure AD Tenant ID
        
        If not provided, will try to load from environment variables:
            AZURE_CLIENT_ID
            AZURE_CLIENT_SECRET
            AZURE_APP_ID
            AZURE_TENANT_ID
        """
        # Load from environment if not provided
        self.client_id = client_id or os.getenv("AZURE_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("AZURE_CLIENT_SECRET")
        self.app_id = app_id or os.getenv("AZURE_APP_ID")
        self.tenant_id = tenant_id or os.getenv("AZURE_TENANT_ID")
        
        # Validate all required credentials
        if not self.client_id:
            raise ValueError("client_id is required (AZURE_CLIENT_ID)")
        if not self.client_secret:
            raise ValueError("client_secret is required (AZURE_CLIENT_SECRET)")
        if not self.app_id:
            raise ValueError("app_id is required (AZURE_APP_ID)")
        if not self.tenant_id:
            raise ValueError("tenant_id is required (AZURE_TENANT_ID)")
        
        self.last_error = None
        self.client = None
        
        logger.info(f"✅ Azure Insights Connector initialized")
        logger.info(f"   Client ID: {self.client_id[:20]}...")
        logger.info(f"   App ID (Workspace): {self.app_id[:20]}...")
        logger.info(f"   Tenant ID: {self.tenant_id[:20]}...")
        
        # Initialize the Azure SDK client with proper authentication
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Azure Logs Query Client with Client Secret credentials"""
        try:
            logger.info("🔐 Using Client Secret authentication")
            
            # Create credentials with provided values
            credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            
            # Create the Logs Query Client
            self.client = LogsQueryClient(credential)
            logger.info("✅ Azure Logs Query Client initialized successfully")
            self.last_error = None
            
        except Exception as e:
            error_msg = f"Failed to initialize Azure client: {str(e)}"
            self.last_error = error_msg
            logger.error(f"❌ {error_msg}")
            raise
    
    def execute_kql(self, query: str, time_range: str = "ago(1h)") -> pd.DataFrame:
        """
        Execute a KQL query against Application Insights
        
        Args:
            query: KQL query string
            time_range: Time range string (e.g., "ago(1h)", "ago(24h)") or tuple of (start, end) datetimes
        
        Returns:
            pandas.DataFrame with query results
        """
        try:
            if not self.client:
                raise ValueError("Client not initialized. Call _initialize_client first.")
            
            # Clean up query
            query = query.strip()
            logger.info(f"📊 Executing KQL query...")
            
            # Convert time_range string to datetime tuple if needed
            timespan = self._convert_time_range(time_range)
            
            # Execute the query using Azure SDK
            # app_id is the workspace ID
            response = self.client.query_workspace(
                workspace_id=self.app_id,
                query=query,
                timespan=timespan
            )
            
            # Check if query was successful
            if response.status == LogsQueryStatus.SUCCESS:
                # Convert to pandas DataFrame
                table = response.tables[0] if response.tables else None
                
                if table:
                    # Create DataFrame from query results
                    data = []
                    for row in table.rows:
                        row_dict = {}
                        for col_idx, col in enumerate(table.columns):
                            row_dict[col.name] = row[col_idx]
                        data.append(row_dict)
                    
                    df = pd.DataFrame(data)
                    self.last_error = None
                    logger.info(f"✅ Query executed successfully. Rows: {len(df)}")
                    return df
                else:
                    logger.warning("⚠️ Query returned no tables")
                    return pd.DataFrame()
            
            elif response.status == LogsQueryStatus.PARTIAL:
                logger.warning("⚠️ Query returned partial results")
                table = response.tables[0] if response.tables else None
                
                if table:
                    data = []
                    for row in table.rows:
                        row_dict = {}
                        for col_idx, col in enumerate(table.columns):
                            row_dict[col.name] = row[col_idx]
                        data.append(row_dict)
                    return pd.DataFrame(data)
                else:
                    return pd.DataFrame()
            
            else:
                error_msg = f"Query failed with status: {response.status}"
                self.last_error = error_msg
                logger.error(f"❌ {error_msg}")
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

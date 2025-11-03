"""
Utility functions for Azure Application Insights connection and data retrieval
Supports both Client Secret and Managed Identity authentication
"""

import pandas as pd
import os
from datetime import datetime, timedelta
from azure.identity import ClientSecretCredential, ManagedIdentityCredential, DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AzureInsightsConnector:
    """
    Connector for Azure Application Insights using KQL queries
    Supports multiple authentication methods:
    1. Managed Identity (recommended)
    2. Client Secret (development)
    3. Default Azure Credential (fallback)
    """
    
    def __init__(self, app_id: str, client_id: str = None, client_secret: str = None, tenant_id: str = None):
        """
        Initialize the Azure Insights Connector
        
        Args:
            app_id: Application Insights Resource ID
            client_id: Azure AD Client ID or Managed Identity Client ID
            client_secret: Azure AD Client Secret (optional - for non-managed identity)
            tenant_id: Azure AD Tenant ID (optional - for client secret auth)
        """
        self.app_id = app_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.last_error = None
        self.auth_method = self._detect_auth_method()
        
        # Initialize Azure credentials and client
        self._initialize_client()
    
    def _detect_auth_method(self) -> str:
        """Detect which authentication method to use"""
        
        # Check if running in Azure (Managed Identity available)
        if self._is_running_in_azure():
            logger.info("ℹ️ Running in Azure - Managed Identity available")
            if self.client_id:
                return "managed_identity_user_assigned"
            else:
                return "managed_identity_system_assigned"
        
        # Check for client secret
        if self.client_secret and self.tenant_id:
            return "client_secret"
        
        # Try default credential (Azure CLI, Azure PowerShell, etc.)
        return "default_credential"
    
    def _is_running_in_azure(self) -> bool:
        """Check if running in Azure environment"""
        # Check for Azure-specific environment variables
        azure_indicators = [
            'WEBSITE_INSTANCE_ID',  # App Service
            'HOSTNAME',  # Container Instances
            'MSI_ENDPOINT',  # Managed Identity endpoint
            'IMDS_ENDPOINT',  # Instance Metadata Service
        ]
        return any(indicator in os.environ for indicator in azure_indicators)
    
    def _convert_time_range(self, time_range):
        """
        Convert time_range string to Azure SDK compatible format
        
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
    
    def _initialize_client(self):
        """Initialize Azure Logs Query Client with appropriate credentials"""
        try:
            if self.auth_method == "client_secret":
                logger.info("🔐 Using Client Secret authentication")
                credentials = ClientSecretCredential(
                    tenant_id=self.tenant_id,
                    client_id=self.client_id,
                    client_secret=self.client_secret
                )
            
            elif self.auth_method == "managed_identity_user_assigned":
                logger.info("🔐 Using Managed Identity (user-assigned) authentication")
                credentials = ManagedIdentityCredential(
                    client_id=self.client_id
                )
            
            elif self.auth_method == "managed_identity_system_assigned":
                logger.info("🔐 Using Managed Identity (system-assigned) authentication")
                credentials = ManagedIdentityCredential()
            
            else:  # default_credential
                logger.info("🔐 Using Default Azure Credential")
                credentials = DefaultAzureCredential()
            
            # Create Logs Query Client
            self.client = LogsQueryClient(credentials)
            self.last_error = None
            logger.info(f"✅ Azure Logs Query Client initialized ({self.auth_method})")
            
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"❌ Failed to initialize Azure client: {str(e)}")
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
            # Clean up query - remove extra whitespace
            query = query.strip()
            
            # Convert time_range string to datetime tuple if needed
            timespan = self._convert_time_range(time_range)
            
            # Execute the query
            response = self.client.query_workspace(
                workspace_id=self.app_id,
                query=query,
                timespan=timespan
            )
            
            # Check if query was successful
            if response.status == LogsQueryStatus.SUCCESS:
                # Convert to pandas DataFrame
                table = response.tables[0]
                
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
            
            elif response.status == LogsQueryStatus.PARTIAL:
                logger.warning("⚠️ Query returned partial results")
                table = response.tables[0]
                
                data = []
                for row in table.rows:
                    row_dict = {}
                    for col_idx, col in enumerate(table.columns):
                        row_dict[col.name] = row[col_idx]
                    data.append(row_dict)
                
                return pd.DataFrame(data)
            
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
    
    def execute_kql_raw(self, query: str, timespan=None):
        """
        Execute a raw KQL query without modification
        
        Args:
            query: Raw KQL query string
            timespan: Azure timespan format
        
        Returns:
            Raw response from Azure Logs Query API
        """
        try:
            response = self.client.query_workspace(
                workspace_id=self.app_id,
                query=query,
                timespan=timespan
            )
            self.last_error = None
            return response
        
        except Exception as e:
            error_msg = f"Error executing raw KQL query: {str(e)}"
            self.last_error = error_msg
            logger.error(f"❌ {error_msg}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test the connection to Azure Application Insights
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
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
        """
        Export DataFrame to CSV bytes
        
        Args:
            df: pandas DataFrame to export
        
        Returns:
            CSV data as bytes
        """
        try:
            import io
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            return csv_buffer.getvalue().encode()
        except Exception as e:
            logger.error(f"❌ Error exporting to CSV: {str(e)}")
            return None
    
    def export_to_excel(self, df: pd.DataFrame) -> bytes:
        """
        Export DataFrame to Excel bytes
        
        Args:
            df: pandas DataFrame to export
        
        Returns:
            Excel data as bytes
        """
        try:
            import io
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            return excel_buffer.getvalue()
        except Exception as e:
            logger.error(f"❌ Error exporting to Excel: {str(e)}")
            return None
    
    def get_last_error(self) -> str:
        """Get the last error message"""
        return self.last_error if self.last_error else "No errors"
    
    def get_auth_method(self) -> str:
        """Get the authentication method being used"""
        return self.auth_method

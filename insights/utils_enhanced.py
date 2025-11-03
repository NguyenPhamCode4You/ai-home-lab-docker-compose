"""
Enhanced utilities with export functionality and better error handling
"""

import pandas as pd
from azure.identity import ClientSecretCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from datetime import datetime
import logging
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AzureInsightsConnector:
    """
    Connector for Azure Application Insights using KQL queries
    """
    
    def __init__(self, app_id: str, client_id: str, client_secret: str, tenant_id: str):
        """
        Initialize the Azure Insights Connector
        
        Args:
            app_id: Application Insights Resource ID or name
            client_id: Azure AD Client ID
            client_secret: Azure AD Client Secret
            tenant_id: Azure AD Tenant ID
        """
        self.app_id = app_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.last_error = None
        
        # Initialize Azure credentials and client
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Azure Logs Query Client with credentials"""
        try:
            # Create credentials
            credentials = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            
            # Create Logs Query Client
            self.client = LogsQueryClient(credentials)
            self.last_error = None
            logger.info("✅ Azure Logs Query Client initialized successfully")
            
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"❌ Failed to initialize Azure client: {str(e)}")
            raise
    
    def execute_kql(self, query: str, time_range: str = "ago(1h)") -> pd.DataFrame:
        """
        Execute a KQL query against Application Insights
        
        Args:
            query: KQL query string
            time_range: Time range string (e.g., "ago(1h)", "ago(24h)")
        
        Returns:
            pandas.DataFrame with query results or empty DataFrame on error
        """
        try:
            # Clean up query - remove extra whitespace
            query = query.strip()
            
            # Execute the query
            response = self.client.query_workspace(
                workspace_id=self.app_id,
                query=query,
                timespan=time_range
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
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            return excel_buffer.getvalue()
        except Exception as e:
            logger.error(f"❌ Error exporting to Excel: {str(e)}")
            return None
    
    def get_last_error(self) -> str:
        """Get the last error message"""
        return self.last_error if self.last_error else "No errors"

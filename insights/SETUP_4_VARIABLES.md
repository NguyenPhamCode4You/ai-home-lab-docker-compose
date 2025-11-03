# ✅ Simplified: 4 Variables Instead of Connection String

## What Changed

**Before**: Used complex connection string parsing
**After**: Simple 4 variables - much cleaner!

## The 4 Variables You Need

1. **AZURE_CLIENT_ID** - Your app's Client ID
2. **AZURE_CLIENT_SECRET** - Your app's Client Secret
3. **AZURE_APP_ID** - Application Insights Workspace ID
4. **AZURE_TENANT_ID** - Your Azure Tenant ID

## Where to Get Each Value

### 1. AZURE_CLIENT_ID

- Azure Portal → Azure Active Directory → App registrations
- Find your app → Click on it
- Copy "Application (client) ID"

### 2. AZURE_CLIENT_SECRET

- Azure Portal → Azure Active Directory → App registrations
- Your app → Certificates & secrets
- Click "+ New client secret"
- Copy the secret value (only visible once!)

### 3. AZURE_APP_ID

- Azure Portal → Application Insights → Your resource
- Click "Properties" in left sidebar
- Copy "Resource ID"
- Example: `/subscriptions/xxx/resourcegroups/yyy/providers/microsoft.insights/components/zzz`

### 4. AZURE_TENANT_ID

- Azure Portal → Azure Active Directory → Properties
- Copy "Tenant ID"

## Update .env File

```properties
AZURE_CLIENT_ID=29c2635a-eacc-4b91-a42c-5d27e6f94aed
AZURE_CLIENT_SECRET=your-actual-secret-here
AZURE_APP_ID=6007bd8c-172b-4f67-a5ca-a2ee435688e9
AZURE_TENANT_ID=62e57f8d-3ff6-42b9-afb0-26f21f40e9c9
```

## Important: Grant Permissions

Your app needs "Monitoring Data Reader" role on Application Insights:

1. Azure Portal → Application Insights → Your resource
2. Access Control (IAM) → Add role assignment
3. Role: "Monitoring Data Reader"
4. Members: Your service principal (use the Client ID to find it)
5. Click "Review + assign"

## Run Dashboard

```bash
streamlit run app.py
```

1. Open sidebar → "🔐 Azure Connection"
2. Click "🔗 Connect to Azure Application Insights"
3. ✅ Dashboard loads with your data!

## Files Updated

1. **`utils_connection_string.py`** - Now uses 4 variables
2. **`.env`** - Simple 4-variable format
3. **`app.py`** - Updated to pass 4 variables

## Benefits

| Feature          | Before           | After           |
| ---------------- | ---------------- | --------------- |
| Setup Complexity | High             | Simple          |
| Parsing Needed   | Yes              | No              |
| Variables        | 1 complex string | 4 simple values |
| Error Handling   | Complex          | Easy            |
| Readability      | Hard to debug    | Clear           |

## Example .env

```properties
# Azure Credentials
AZURE_CLIENT_ID=29c2635a-eacc-4b91-a42c-5d27e6f94aed
AZURE_CLIENT_SECRET=MyClientSecret123!
AZURE_APP_ID=6007bd8c-172b-4f67-a5ca-a2ee435688e9
AZURE_TENANT_ID=62e57f8d-3ff6-42b9-afb0-26f21f40e9c9
```

Done! Much cleaner now 🎉

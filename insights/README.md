# Quick Start: Using Managed Identity

## Your Situation

✅ You have: Managed Identity with Client ID  
✅ You don't have: Client Secret (and that's GOOD!)

---

## What You Need to Do (3 Steps)

### Step 1: Update .env File

Your current `.env`:

```env
AZURE_APP_ID=6007xxx
AZURE_TENANT_ID=62e57xxx
AZURE_CLIENT_ID=29c2xxx
AZURE_CLIENT_SECRET=  # Leave empty for Managed Identity!
```

That's it! **Leave AZURE_CLIENT_SECRET blank or empty.**

### Step 2: Grant Permissions

Your Managed Identity needs permission to read Application Insights:

1. Go to **Azure Portal**
2. Find your **Application Insights resource**
3. Click **Access Control (IAM)**
4. Click **+ Add role assignment**
5. Select role: **"Monitoring Data Reader"** or **"Log Analytics Reader"**
6. Assign to: Your Managed Identity (search for its name)
7. Click **Save**

### Step 3: Update Code (Use New utils File)

Option A: Replace `utils.py` with `utils_managed_identity.py`:

```bash
# In insights folder:
copy utils_managed_identity.py utils.py
```

Option B: Or just use the new file:

- Edit `app.py`
- Change: `from utils import AzureInsightsConnector`
- To: `from utils_managed_identity import AzureInsightsConnector`

---

## Run the Dashboard

```bash
pip install -r requirements.txt
streamlit run app.py
```

That's it! The new `utils_managed_identity.py` will:

1. ✅ Detect you're using Managed Identity
2. ✅ Automatically use the right authentication
3. ✅ No Client Secret needed!

---

## How It Works

The new code automatically:

```
Checks environment → Uses Managed Identity → No secret required ✅
```

If running on:

- ✅ **Azure VM** → Uses system-assigned or user-assigned identity
- ✅ **App Service** → Uses identity
- ✅ **Container Instances** → Uses identity
- ✅ **Local development** → Falls back to Azure CLI credentials

---

## Authentication Priority

The new code tries in this order:

1. **Managed Identity (Recommended)**

   - System-assigned (if available)
   - User-assigned (if Client ID provided)

2. **Client Secret (if provided)**

   - Falls back to this if no managed identity available

3. **Default Azure Credential (Fallback)**
   - Azure CLI
   - Azure PowerShell
   - Visual Studio
   - VS Code

---

## Benefits

✅ **No Client Secret to manage**  
✅ **Works on Azure automatically**  
✅ **Secure - no credentials in .env**  
✅ **Automatic token refresh**  
✅ **No rotation needed**

---

## What If It Still Doesn't Work?

❌ **"Connection failed"**

- Check role assignment was granted
- Wait 1-2 minutes for permissions to propagate
- Check Application Insights exists and is accessible

❌ **"Unauthorized"**

- Verify Managed Identity has "Monitoring Data Reader" role
- Make sure it's on the Application Insights resource
- Click "Grant admin consent" if prompted

❌ **"Token failed"**

- Check you're running on Azure or have Azure CLI logged in
- Verify Managed Identity is properly configured

---

## Key Difference: Old vs New

### Old Way (Client Secret)

```python
from azure.identity import ClientSecretCredential

credentials = ClientSecretCredential(
    tenant_id="your-tenant",
    client_id="your-client-id",
    client_secret="your-secret-here"  # ⚠️ Secret in .env
)
```

### New Way (Managed Identity)

```python
from azure.identity import ManagedIdentityCredential

credentials = ManagedIdentityCredential(
    client_id="your-client-id"  # ✅ No secret!
)
```

---

## File to Use

Use **`utils_managed_identity.py`** instead of `utils.py`

It automatically:

- Detects Managed Identity
- Falls back to Client Secret if needed
- Supports both authentication methods

---

## Summary

| Step | Action                                  | Time  |
| ---- | --------------------------------------- | ----- |
| 1    | Update .env (leave CLIENT_SECRET blank) | 1 min |
| 2    | Grant permissions in Azure Portal       | 2 min |
| 3    | Use new utils_managed_identity.py       | 1 min |
| 4    | Run streamlit                           | -     |

**Total: 4 minutes** ✅

---

## Questions?

See `MANAGED_IDENTITY_GUIDE.md` for detailed explanations.

You're all set! 🚀

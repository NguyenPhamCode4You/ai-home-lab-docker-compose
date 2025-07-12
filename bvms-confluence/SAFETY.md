# 🔒 SAFETY DOCUMENTATION

## READ-ONLY GUARANTEE

This Confluence exporter project is designed with **complete safety** in mind. Here's our safety guarantee:

### ✅ What This Project DOES

1. **READ ONLY**: Only reads data from your Confluence space
2. **LOCAL FILES**: Creates Markdown files on your local computer only
3. **GET REQUESTS**: Uses only HTTP GET requests to the Confluence API
4. **NO MODIFICATIONS**: Never calls any API endpoints that modify data
5. **EXPORT ONLY**: Purely an export/backup tool

### ❌ What This Project NEVER DOES

1. **NO WRITING**: Never writes data back to Confluence
2. **NO DELETING**: Never deletes any Confluence content
3. **NO UPDATING**: Never updates any Confluence pages
4. **NO CREATING**: Never creates new pages in Confluence
5. **NO POST/PUT/DELETE**: Never uses HTTP methods that modify data

## API Permissions Required

The scripts only need **READ permissions** on your Confluence space:

- View pages
- Read page content
- Access space information

**No write permissions are needed or used.**

## Code Safety Features

### 1. HTTP Method Restrictions

```python
# Only GET requests are used
response = requests.get(api_url, auth=auth, params=params)
# Never: POST, PUT, DELETE, PATCH
```

### 2. Read-Only API Endpoints

All API calls use read-only endpoints:

- `/wiki/rest/api/space/{spaceKey}` - Read space info
- `/wiki/rest/api/content` - Read page content
- No write endpoints are called

### 3. Safety Warnings

Every script displays safety warnings on startup:

```
⚠️  READ-ONLY MODE: This script will NOT modify your Confluence space ⚠️
   - Only reads pages from Confluence
   - Creates local Markdown files only
   - Your Confluence data remains unchanged
```

### 4. Local File Operations Only

```python
# Only writes to local filesystem
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
# Never writes to Confluence
```

## Verification Steps

To verify the safety of these scripts:

1. **Review the code**: All source code is available for inspection
2. **Check API calls**: Only GET requests to read-only endpoints
3. **Monitor network traffic**: Use tools like Wireshark to verify only GET requests
4. **Test with limited token**: Create an API token with read-only permissions

## API Token Best Practices

For maximum safety:

1. **Create a dedicated API token** just for this exporter
2. **Use a read-only account** if possible
3. **Revoke the token** after exporting if desired
4. **Monitor API usage** in your Atlassian admin panel

## Emergency Safety

If you're concerned about safety:

1. **Test on a non-production space first**
2. **Review all code before running**
3. **Use a read-only API token**
4. **Monitor the first few page exports**

## Support

If you have any concerns about the safety of these scripts:

1. Review the source code (all files are readable)
2. Test with a single page first
3. Use network monitoring tools to verify behavior
4. Create an issue in the repository for questions

**Remember: These scripts are designed to be 100% safe for your Confluence data.**

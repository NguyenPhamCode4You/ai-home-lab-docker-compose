# Azure Front Door Cache Troubleshooting Guide

## Incident Summary

**Date**: November 16, 2025  
**Severity**: High (Application unavailable via Front Door)  
**Resolution Time**: ~30 minutes  
**Root Cause**: Cached responses with incorrect Application Insights configuration

---

## Problem Description

After enabling Azure Front Door caching and deploying an application configuration change, the application became inaccessible through the Front Door domain, while the direct App Service URL continued to work normally.

### Initial Setup

- **Architecture**: Azure Front Door → App Service (Next.js application)
- **Application Insights**: Already configured in App Service environment variables
- **Status**: Working correctly

### Changes Made

1. Enabled caching on Azure Front Door route
2. Updated the application and reloaded (standard F5 refresh)
3. Discovered Application Insights ID mismatch:
   - Environment variable had correct ID
   - Next.js build configuration had different (incorrect) ID
4. Fixed the Application Insights ID in pipeline
5. Deployed via pipeline

### Symptoms After Deployment

- ✅ Direct App Service URL: **Working**
- ❌ Front Door domain: **Blank page, loading forever**
- 🔄 Hard refresh (Ctrl+Shift+R): **Still not working**

---

## Root Cause Analysis

### What Actually Happened

1. **Cache Poisoning During Initial Deployment**

   - When caching was first enabled, Front Door cached responses
   - The cached responses contained the **incorrect Application Insights ID**
   - These cached responses were distributed across all Front Door POPs globally

2. **Configuration Fix Was Ignored**

   - When the pipeline deployed the corrected configuration
   - Front Door continued serving cached responses (with wrong config)
   - The origin (App Service) had correct config, but Front Door never reached it

3. **Cache Propagation Delay**
   - Cache purge operations take 20-30 minutes to complete globally
   - During this time, some POPs served cached content, others didn't
   - This created inconsistent behavior

### Why Direct URL Worked But Front Door Didn't

| Access Method                | Result     | Reason                                     |
| ---------------------------- | ---------- | ------------------------------------------ |
| Direct App Service URL       | ✅ Working | Bypasses Front Door cache entirely         |
| Front Door domain            | ❌ Failed  | Served cached responses with wrong config  |
| Front Door + `?nocache=true` | ✅ Working | Query parameter bypassed cache, hit origin |

---

## Troubleshooting Steps Taken

### ❌ Attempted Fixes (Didn't Work Immediately)

1. **Disabled caching on Front Door route**

   - **Why it didn't work**: Existing cached content was still being served
   - Disabling only prevents new caching, doesn't purge existing cache

2. **Removed Application Insights ID from environment variables**

   - **Why it didn't work**: Changes weren't reflected due to cached responses

3. **Restarted App Service**
   - **Why it didn't work**: Front Door wasn't reaching the App Service (serving cached content)

### ✅ Solution That Worked

1. **Purged Front Door cache** (via Azure Portal)

   - Took 20-30 minutes to complete globally
   - No immediate success indication in portal

2. **Used cache bypass query parameter**

   - Accessed: `https://yourdomain.azurefd.net/?nocache=true`
   - Immediately worked because it bypassed cache
   - Confirmed origin was healthy

3. **Waited for cache purge completion**
   - After ~30 minutes, normal URLs worked again
   - Re-added Application Insights ID to environment variables
   - Restarted App Service
   - Verified with hard refresh (Ctrl+Shift+R)

---

## Best Practices & Prevention

### ⚠️ Common Misconception

**"I should not enable caching on Front Door"** - **INCORRECT**

Caching is beneficial and should be used. The issue was the deployment process, not caching itself.

### ✅ Correct Approach

#### 1. **Safe Deployment Process with Caching Enabled**

```yaml
# Add to your deployment pipeline
steps:
  - task: Deploy App Service

  - task: Purge Front Door Cache
    condition: always()
    inputs:
      contentPaths: "/*"

  - task: Wait for Cache Purge
    # Wait 5 minutes for propagation

  - task: Verify Deployment
    # Test Front Door URL
```

#### 2. **Configuration Change Checklist**

Before deploying configuration changes:

- [ ] Identify if changes affect cached responses
- [ ] Plan for cache purge after deployment
- [ ] Have rollback plan ready
- [ ] Monitor cache purge completion

#### 3. **Testing Strategy**

```bash
# Test direct origin
curl https://your-app.azurewebsites.net

# Test Front Door (normal)
curl https://your-domain.azurefd.net

# Test Front Door (bypass cache)
curl https://your-domain.azurefd.net/?nocache=true

# Check cache status
curl -I https://your-domain.azurefd.net
# Look for: X-Cache: TCP_HIT or TCP_MISS
```

#### 4. **Cache Configuration Recommendations**

```yaml
# Front Door cache settings
caching:
  enabled: true
  queryStringCachingBehavior: IgnoreSpecifiedQueryStrings
  queryParameters:
    - nocache
    - debug
    - bypass
  cacheDuration: PT1H # 1 hour for most content
```

#### 5. **Emergency Cache Purge**

**Via Azure Portal:**

1. Front Door → Your profile → Endpoints
2. Click "Purge cache"
3. Enter content paths (e.g., `/*` for all)
4. Wait 20-30 minutes

**Via Azure CLI:**

```bash
az afd endpoint purge \
  --resource-group <rg-name> \
  --profile-name <profile-name> \
  --endpoint-name <endpoint-name> \
  --content-paths "/*"
```

**Via Pipeline:**

```yaml
- task: AzureCLI@2
  displayName: "Purge Front Door Cache"
  inputs:
    azureSubscription: "Your-Service-Connection"
    scriptType: "bash"
    scriptLocation: "inlineScript"
    inlineScript: |
      az afd endpoint purge \
        --resource-group $(resourceGroup) \
        --profile-name $(frontDoorProfile) \
        --endpoint-name $(endpointName) \
        --content-paths "/*"
```

---

## When to Purge Cache

### ✅ Always Purge After:

- Configuration changes (API keys, connection strings, feature flags)
- Application Insights ID changes
- Authentication/authorization changes
- Significant UI/UX changes
- Breaking bug fixes

### ⚠️ Consider Purging After:

- Major feature deployments
- API contract changes
- Security updates

### ❌ No Need to Purge:

- Backend logic changes (not affecting responses)
- Database schema updates
- Internal service refactoring

---

## Cache Headers Best Practices

### For Next.js Applications

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: "/_next/static/:path*",
        headers: [
          {
            key: "Cache-Control",
            value: "public, max-age=31536000, immutable",
          },
        ],
      },
      {
        source: "/api/:path*",
        headers: [
          {
            key: "Cache-Control",
            value: "no-cache, no-store, must-revalidate",
          },
        ],
      },
    ];
  },
};
```

### For App Service Configuration

```json
{
  "WEBSITE_CACHE_CONTROL": "no-cache",
  "APPINSIGHTS_INSTRUMENTATIONKEY": "your-correct-key",
  "APPLICATIONINSIGHTS_CONNECTION_STRING": "your-correct-connection-string"
}
```

---

## Monitoring & Alerts

### Recommended Azure Monitor Alerts

1. **Front Door Cache Hit Ratio Drop**

   - Alert if cache hit ratio < 70%
   - May indicate cache purge or configuration issues

2. **Front Door Error Rate Spike**

   - Alert if 5xx errors > 1%
   - May indicate origin issues masked by cache

3. **App Service Response Time**
   - Alert if P95 > 2 seconds
   - Cache should reduce load, monitor origin separately

### Useful Queries (Application Insights)

```kusto
// Check Application Insights ID in use
traces
| where timestamp > ago(1h)
| extend AppInsightsId = tostring(customDimensions.AppInsightsInstrumentationKey)
| summarize count() by AppInsightsId

// Front Door cache performance
requests
| where timestamp > ago(1h)
| extend CacheStatus = tostring(customDimensions["X-Cache"])
| summarize HitRate = countif(CacheStatus == "TCP_HIT") * 100.0 / count()
```

---

## Quick Reference

### Cache Bypass Methods

| Method            | Use Case        | Example                                           |
| ----------------- | --------------- | ------------------------------------------------- |
| Query parameter   | Quick testing   | `?nocache=true`                                   |
| Request header    | API testing     | `Cache-Control: no-cache`                         |
| Private/incognito | User testing    | Open incognito window                             |
| Hard refresh      | Browser testing | Ctrl+Shift+R (Windows/Linux)<br>Cmd+Shift+R (Mac) |

### Cache Purge Time Expectations

| Scope            | Time          |
| ---------------- | ------------- |
| Single file      | 5-10 minutes  |
| Directory        | 10-20 minutes |
| Full site (`/*`) | 20-30 minutes |

### Useful Azure CLI Commands

```bash
# Check Front Door status
az afd endpoint show \
  --resource-group <rg> \
  --profile-name <profile> \
  --endpoint-name <endpoint>

# List all routes
az afd route list \
  --resource-group <rg> \
  --profile-name <profile> \
  --endpoint-name <endpoint>

# Show cache settings for a route
az afd route show \
  --resource-group <rg> \
  --profile-name <profile> \
  --endpoint-name <endpoint> \
  --route-name <route>
```

---

## Lessons Learned

### ✅ Do's

- ✅ **Keep caching enabled** - it's crucial for performance
- ✅ **Always purge cache after config changes**
- ✅ **Use cache-bypass parameters for testing**
- ✅ **Wait for purge completion (20-30 min) before declaring failure**
- ✅ **Test both Front Door and direct URLs**
- ✅ **Monitor Application Insights for configuration issues**

### ❌ Don'ts

- ❌ **Don't panic and disable caching** - it's not the problem
- ❌ **Don't expect immediate cache purge** - it takes time
- ❌ **Don't deploy config changes without purge plan**
- ❌ **Don't forget to verify environment variables vs build-time configs**
- ❌ **Don't skip hard refresh testing** (Ctrl+Shift+R)

---

## Related Issues to Watch For

### Application Insights Configuration Mismatch

- **Build-time config**: Set in Next.js environment variables during build
- **Runtime config**: Set in App Service environment variables
- **Ensure both match** or use runtime-only configuration

### Front Door Caching Behavior

- Default cache duration varies by response headers
- Missing `Cache-Control` headers may result in unexpected caching
- Private data should have `Cache-Control: private` or `no-cache`

### Azure Portal UI Lag

- Cache purge may appear to take longer in portal than actual propagation
- Use testing (with cache-bypass) to verify actual cache state

---

## Additional Resources

- [Azure Front Door Caching](https://learn.microsoft.com/en-us/azure/frontdoor/front-door-caching)
- [Cache Purge Documentation](https://learn.microsoft.com/en-us/azure/frontdoor/standard-premium/how-to-cache-purge)
- [Next.js Caching Strategies](https://nextjs.org/docs/app/building-your-application/caching)
- [Application Insights Configuration](https://learn.microsoft.com/en-us/azure/azure-monitor/app/nodejs)

---

## Contact & Support

If you encounter similar issues:

1. Check this document first
2. Verify cache purge has completed (wait 30 minutes)
3. Test with cache bypass: `?nocache=true`
4. Check Application Insights for configuration errors
5. Contact DevOps team if issue persists

---

**Document Version**: 1.0  
**Last Updated**: November 16, 2025  
**Next Review**: After next major deployment incident

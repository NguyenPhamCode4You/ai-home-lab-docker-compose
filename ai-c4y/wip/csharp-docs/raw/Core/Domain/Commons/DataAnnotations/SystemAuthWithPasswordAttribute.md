# SystemAuthWithPasswordAttribute

## Purpose
Authorization filter attribute that enforces system-level authentication by validating `X-System-Username` and `X-System-Password` request headers against values defined in application configuration. Exists to secure controllers or actions requiring credential-based access for system integrations or internal tooling without implementing OAuth or session-based auth.

## Business Responsibility
Defines the authentication boundary for system-level endpoints using static header credentials. Critical for preventing unauthorized access to protected operations; misconfiguration causes immediate 500 errors for all affected endpoints, blocking access until resolved. Operates as a lightweight guard with no database or external service calls, relying solely on application configuration for credential evaluation.

## Members

### 1. OnAuthorization — Entry point for request authentication and short-circuit logic
```csharp
public void OnAuthorization(AuthorizationFilterContext context)
{
    var configuration = context.HttpContext.RequestServices.GetRequiredService<IConfiguration>();

    if (!context.HttpContext.Request.Headers.TryGetValue("X-System-Username", out var username) ||
        !context.HttpContext.Request.Headers.TryGetValue("X-System-Password", out var password))
    {
        context.Result = new UnauthorizedObjectResult(new
        {
            success = false,
            message = "System authentication required. X-System-Username and X-System-Password headers are missing."
        });
        return;
    }

    var configUsername = configuration["SystemAuthWithPassword:Username"];
    var configPassword = configuration["SystemAuthWithPassword:Password"];

    if (string.IsNullOrEmpty(configUsername) || string.IsNullOrEmpty(configPassword))
    {
        context.Result = new ObjectResult(new
        {
            success = false,
            message = "System authentication is not configured properly."
        })
        {
            StatusCode = 500
        };
        return;
    }

    if (username != configUsername || password != configPassword)
    {
        context.Result = new UnauthorizedObjectResult(new
        {
            success = false,
            message = "Invalid system credentials."
        });
        return;
    }
}
```
**Explanation**: Resolves `IConfiguration` via the request DI scope to load credentials. Performs three-stage validation: 1) Verifies presence of required headers, returning 401 if missing. 2) Validates configuration completeness, returning 500 if credentials are undefined (preventing fallback to null/empty matches). 3) Compares request headers against config values using direct string comparison. Short-circuits the pipeline via `context.Result` on any failure; allows execution to proceed only if all checks pass.

## Dependencies
- `IAuthorizationFilter` — Implements the ASP.NET Core filter pipeline contract; enables attribute application to action/method level for granular security control without global registration overhead.
- `IConfiguration` — Loads `SystemAuthWithPassword` credential pairs from `appsettings`; resolved via `RequestServices` rather than constructor injection due to attribute instantiation model and lack of DI scope during filter registration.
- `AuthorizationFilterContext` — Provides access to `HttpContext.Request` for header extraction and `Result` property for injecting unauthorized/error responses directly into the MVC pipeline.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]
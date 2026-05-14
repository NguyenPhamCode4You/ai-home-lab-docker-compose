# ClaimConstants and QueryFilter

## Purpose
Centralizes constant definitions for authentication claim keys, HTTP header names, and query pagination defaults. `ClaimConstants` defines the canonical string keys used across identity flows, while `QueryFilter` provides standard pagination parameters.

## Business Responsibility
Owns the contract for claim and header key names (`x-*` prefix convention) and pagination defaults. `ClaimConstants` is **critical** for identity extraction; any mismatch here breaks authentication, authorization, or tracing. Notably, `ClaimConstants` contains a typo in `PERMISSTTIONS` that creates a consumer hazard. `QueryFilter` is **low-criticality** but ensures consistency in list query behavior across repositories.

---
IF OTHER (helper/extension/utility):

## Members

### USER_ID — Identity claim key for user subject.
```csharp
public const string USER_ID = "x-user-id";
```
**Explanation**: Maps to `x-user-id`. Used to extract the authenticated user's unique identifier from JWT claims or HTTP headers. Core to all identity resolution logic.

### USER_EMAIL — Login email claim key.
```csharp
public const string USER_EMAIL = "x-user-email";
```
**Explanation**: Maps to `x-user-email`. Extracts the user's email address from identity context. Used for notifications, audit logging, and user lookup.

### USER_NAME — Display name claim key.
```csharp
public const string USER_NAME = "x-user-name";
```
**Explanation**: Maps to `x-user-name`. Stores the user's preferred display name for UI rendering and greetings.

### FULL_NAME — Complete name claim key.
```csharp
public const string FULL_NAME = "x-full-name";
```
**Explanation**: Maps to `x-full-name`. Holds the user's full legal or formatted name. Used in reports and official documentation.

### AVATAR — Profile image key.
```csharp
public const string AVATAR = "x-avatar";
```
**Explanation**: Maps to `x-avatar`. Contains a URL or key reference to the user's profile image.

### APP_ID — Client application identifier.
```csharp
public const string APP_ID = "x-app-id";
```
**Explanation**: Maps to `x-app-id`. Identifies the requesting application or client in multi-app environments.

### ORG_ID — Tenant/Organization identifier.
```csharp
public const string ORG_ID = "x-org-id";
```
**Explanation**: Maps to `x-org-id`. Multi-tenancy key used to scope data and permissions to the correct organization.

### ROLES — Role claim key.
```csharp
public const string ROLES = "x-role";
```
**Explanation**: Maps to `x-role`. Contains the user's assigned roles for role-based access control (RBAC).

### RIGHTS — Granular rights claim key.
```csharp
public const string RIGHTS = "x-right";
```
**Explanation**: Maps to `x-right`. Stores fine-grained permissions or capabilities beyond standard roles.

### PERMISSTTIONS — Permission claim key.
```csharp
public const string PERMISSTTIONS = "x-permission";
```
**Explanation**: Maps to `x-permission`. **Hazard**: Constant name contains a typo (`PERMISSTTIONS` with double `T`). Consumers must reference `ClaimConstants.PERMISSSTTIONS` to access the value. This breaks intellisense discovery and risks typos in usage.

### ISSUED_AT — Token issuance timestamp key.
```csharp
public const string ISSUED_AT = "x-iat";
```
**Explanation**: Maps to `x-iat`. Standard JWT `iat` claim. Used for token age validation and audit trails.

### EXPIRES_AT — Token expiration timestamp key.
```csharp
public const string EXPIRES_AT = "x-exp";
```
**Explanation**: Maps to `x-exp`. Standard JWT `exp` claim. Determines token validity window.

### CHANNEL — Interaction channel identifier.
```csharp
public const string CHANNEL = "x-channel";
```
**Explanation**: Maps to `x-channel`. Contextual data indicating the source channel (e.g., web, mobile, api). Used for analytics or channel-specific routing.

### REQUEST_ID — Correlation ID key.
```csharp
public const string REQUEST_ID = "x-request-id";
```
**Explanation**: Maps to `x-request-id`. Unique identifier for tracing distributed requests across services.

### DefaultPageNumber — Inclusive pagination start index.
```csharp
public const int DefaultPageNumber = 1;
```
**Explanation**: Default value `1`. Enforces 1-based pagination indexing across all list operations. Prevents `0` or `null` page values from causing offset errors.

### DefaultPageSize — Standard result limit.
```csharp
public const int DefaultPageSize = 20;
```
**Explanation**: Default value `20`. Applied when `pageSize` is omitted in API requests or repository queries. Balances payload size with performance.

---
## Dependencies
None.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]
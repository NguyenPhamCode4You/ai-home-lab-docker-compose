# BBC-BVMS Backend — Developer Onboarding Guide

> **Audience**: New developers joining the BVMS backend team.
> **Last Updated**: April 2026 | **.NET 8.0** | **CQRS + MediatR Architecture**

---

## Table of Contents

1. [Code Structure & Design Patterns](#1-code-structure--design-patterns)
   - [1.1 Solution Overview](#11-solution-overview)
   - [1.2 Layered Architecture](#12-layered-architecture)
   - [1.3 Core/Domain Layer](#13-coredomain-layer)
   - [1.4 Core/Business Layer](#14-corebusiness-layer)
   - [1.5 Core/Infrastructure Layer](#15-coreinfrastructure-layer)
   - [1.6 API Layer](#16-api-layer)
   - [1.7 External Clients](#17-external-clients)
   - [1.8 Azure Functions](#18-azure-functions)
   - [1.9 Key Design Patterns Summary](#19-key-design-patterns-summary)
2. [Where to Put Code](#2-where-to-put-code)
   - [2.1 Decision Flowchart](#21-decision-flowchart)
   - [2.2 Adding a New Feature (Step-by-Step)](#22-adding-a-new-feature-step-by-step)
   - [2.3 Adding a New External Client](#23-adding-a-new-external-client)
   - [2.4 Adding a New Azure Function](#24-adding-a-new-azure-function)
   - [2.5 File Naming Conventions](#25-file-naming-conventions)
3. [Testing Guidelines](#3-testing-guidelines)
   - [3.1 Testing Stack](#31-testing-stack)
   - [3.2 Unit Tests](#32-unit-tests)
   - [3.3 Integration Tests](#33-integration-tests)
   - [3.4 External Client Tests](#34-external-client-tests)
   - [3.5 Test Naming Conventions](#35-test-naming-conventions)
   - [3.6 CI Pipeline & Test Execution](#36-ci-pipeline--test-execution)
4. [Discussion & Improvements](#4-discussion--improvements)
   - [4.1 Current Strengths](#41-current-strengths)
   - [4.2 Known Gaps & Improvement Areas](#42-known-gaps--improvement-areas)
   - [4.3 Recommendations for New Developers](#43-recommendations-for-new-developers)

---

## 1. Code Structure & Design Patterns

### 1.1 Solution Overview

The solution (`BBC-BVMS.sln`) contains **~30 projects** organized into five logical groups:

```
BBC-BVMS.sln
│
├── Core/                          ← Heart of the application
│   ├── Domain/                    ← Entities, DTOs, Enums, Constants
│   ├── Business/                  ← CQRS Handlers, Validators, Services
│   ├── Infrastructure/            ← DbContext, Middleware, Security, DI
│   ├── Business.UnitTest/         ← Unit tests for business logic
│   ├── Business.IntegrationTest/  ← End-to-end integration tests
│   └── Infrastructure.UnitTest/   ← Unit tests for infrastructure
│
├── APIs/                          ← REST API entry points
│   ├── MasterData/                ← Vessel, Port, BusinessPartner APIs
│   ├── OrderRequest/              ← Voyage, Shipment, Estimate APIs
│   └── FileStorage/               ← File management APIs
│
├── ExternalClients/               ← 3rd-party service adapters
│   ├── SednaClient/               ← Email service (OAuth2)
│   ├── WfosClient/                ← Vessel reporting
│   ├── BusinessCentralClient/     ← ERP integration
│   ├── RoutingEngineClient/       ← Route calculation
│   ├── AzureService/              ← Blob storage
│   ├── MicrosoftGraphClient/      ← Azure AD
│   ├── DaDeskClient/              ← Port calls
│   ├── PdfExportClient/           ← PDF generation
│   ├── EmailParserClient/         ← Email parsing
│   ├── BVMSAzureFunctionsClient/  ← Azure Functions caller
│   └── BBCDataService/            ← Legacy BBC data
│
├── Functions/                     ← Azure Functions (Timer/HTTP triggers)
│   ├── CurrencySync/
│   ├── WfosSync/
│   ├── ConsecutiveVoyages/
│   └── FailedJobMonitoring/
│
└── CronJobs/                      ← Background services
    ├── CurrencyCronService/
    └── WfosCronService/
```

### 1.2 Layered Architecture

The project follows a **Clean Architecture** pattern with strict dependency direction:

```
┌───────────────────────────────────────────────────────────────────┐
│  APIs (MasterData, OrderRequest, FileStorage)                     │
│  → Thin controllers, delegates everything to MediatR handlers     │
└───────────────┬───────────────────────────────────────────────────┘
                │ depends on
┌───────────────▼───────────────────────────────────────────────────┐
│  Core.Business                                                     │
│  → CQRS Handlers, FluentValidation, Background Services, SignalR  │
└───────────────┬───────────────────────────────────────────────────┘
                │ depends on
┌───────────────▼───────────────────────────────────────────────────┐
│  Core.Infrastructure                                               │
│  → EF Core DbContext, AutoMapper, Middleware, Security, DI Setup  │
└───────────────┬───────────────────────────────────────────────────┘
                │ depends on
┌───────────────▼───────────────────────────────────────────────────┐
│  Core.Domain                                                       │
│  → Entities, DTOs, Enums, Constants (NO dependencies)             │
└───────────────────────────────────────────────────────────────────┘

External Clients → Referenced by Core.Infrastructure (registered in DI)
Azure Functions  → Reference Core.Business + Core.Infrastructure
```

**Rule**: Dependencies only flow **downward**. Domain has zero external dependencies.

---

### 1.3 Core/Domain Layer

The Domain layer defines the data structures used everywhere in the application. It contains **no logic** — only shapes.

#### Entity Hierarchy

All database entities inherit from a base class chain:

```csharp
TrackedEntity            ← Id, CreatedOn, CreatedById, ModifiedOn, ModifiedById
    └── BaseEntity       ← IsDeleted, DeletedOn, DeletedById, SoftDelete()
        └── TenantedEntity  ← TenantId (multi-tenant isolation)
```

- **`TrackedEntity`**: Use when you need audit fields but no soft-delete.
- **`BaseEntity`**: Use for most entities (includes soft-delete support).
- **`TenantedEntity`**: Use when data must be isolated per tenant.

> **Important**: Never set audit fields manually (`CreatedOn`, `CreatedById`, etc.). The `DataContext` populates them automatically from the user's JWT token and system time.

#### Folder Structure

```
Core/Domain/
├── VoyageManagement/          ← 46 entities (Voyage, Shipment, Itinerary, etc.)
│   ├── Entities/
│   └── Dtos/
├── MasterData/                ← 25 entities (Vessel, Port, BusinessPartner, etc.)
│   ├── Entities/
│   └── Dtos/
├── FinanceData/               ← Invoice, P&L, Payment entities
├── BunkerOrder/               ← Fuel management entities
├── OrderRequest/              ← Request entities
├── UserManagement/            ← User, Role, RefreshToken entities
├── TaskAlert/                 ← Rules engine entities (Rule, Task, Alert)
├── FileStorage/               ← File entities
├── Constants/                 ← Global enums and constants
└── Commons/                   ← Shared DTO base classes, ApiException, ApiResponse
```

#### Column Attributes

Use custom column attributes instead of raw EF annotations for consistency:

| Attribute             | DB Type         | Use Case                      |
| --------------------- | --------------- | ----------------------------- |
| `[TinyString]`        | `varchar(30)`   | Short codes, abbreviations    |
| `[SmallString]`       | `varchar(150)`  | Names, titles                 |
| `[StandardString]`    | `varchar(550)`  | Default text fields           |
| `[LongString]`        | `varchar(2500)` | Long descriptions, comments   |
| `[EnumString]`        | `varchar(150)`  | Enum values stored as strings |
| `[StandardDecimal]`   | `decimal(18,4)` | Financial/measurement data    |
| `[PrecisionDecimal]`  | `decimal(18,8)` | High-precision calculations   |
| `[GeoGraphicDecimal]` | `decimal(10,6)` | Latitude/longitude            |
| `[StandardInteger]`   | `int`           | General integers              |
| `[TinyInteger]`       | `tinyint`       | Small range values (0-255)    |

> See `Documents/Column_Attribute_Usage_Guides.md` for full details.

#### DTO Conventions

Each domain area has two DTO variants:

- **`{Entity}ReducedDto`** — Minimal fields for search/list views.
- **`{Entity}Dto` or `{Entity}CrudDto`** — Full fields for create/read/update views.

```csharp
// For search results (fewer fields, faster)
public class ShipmentReducedDto : BaseDto
{
    public string? ShipmentCode { get; set; }
    public Guid? CargoTypeId { get; set; }
}

// For CRUD operations (full detail)
public class ShipmentDto : BaseDto
{
    public int ShipmentNumber { get; set; }
    public Guid? CargoTypeId { get; set; }
    public string? ShipmentCode { get; set; }
    public List<ShipmentCommissionDto> Commissions { get; set; }
    public List<ShipmentProfitAndLossItemDto> ProfitAndLossItems { get; set; }
    // ... many more fields
}
```

#### Versioning & Concurrency

Entities that support optimistic concurrency implement `IVersionedEntity`:

```csharp
public class VoyageEntity : TenantedEntity, IVersionedEntity
{
    // IVersionedEntity enables concurrency detection
    // Use [VersionIgnore] to exclude fields from version calculation
}
```

---

### 1.4 Core/Business Layer

The Business layer is where **all business logic lives**. It uses the **CQRS pattern** with **MediatR** for handler dispatch.

#### The Handler Pattern (Most Important Pattern to Learn)

Every operation is a **single file** containing nested `Request` and `Response` classes:

```csharp
// File: Core/Business/VoyageManagement/Voyage/GetVoyageById.cs
public class GetVoyageById
{
    // 1. Request — What input does this handler need?
    public class Request : IRequest<VoyageCrudDto>
    {
        public Guid Id { get; set; }
    }

    // 2. Response — The handler logic (constructor-injected via DI)
    public class Response(
        DataContext context,
        IMapper mapper) : IRequestHandler<Request, VoyageCrudDto>
    {
        public async Task<VoyageCrudDto> Handle(
            Request request, CancellationToken cancellationToken)
        {
            // Load from DB
            VoyageEntity voyage = context.Voyages
                .AsNoTracking()
                .Include(e => e.Shipments)
                .FirstOrDefault(e => e.Id == request.Id)
                    ?? throw new ApiException(ErrorCode.DATA_NOT_FOUND);

            // Map to DTO and return
            return mapper.Map<VoyageCrudDto>(voyage);
        }
    }
}
```

**Why this pattern?**

- Each operation is isolated and testable.
- MediatR auto-discovers handlers — no manual routing needed.
- Adding a new operation = adding a new file. No existing code changes.

#### Handler Types by Convention

| Prefix          | Purpose               | HTTP Method |
| --------------- | --------------------- | ----------- |
| `Get{X}ById`    | Single item read      | GET         |
| `Search{X}`     | Paginated list/search | POST        |
| `Create{X}`     | Create new item       | POST        |
| `Update{X}ById` | Update existing item  | PUT         |
| `Delete{X}`     | Soft-delete item      | DELETE      |
| `Calculate{X}`  | Compute derived data  | (internal)  |
| `Complete{X}`   | Status transition     | PUT/PATCH   |

#### Folder Structure

```
Core/Business/
├── VoyageManagement/
│   ├── Voyage/                ← 40+ handlers
│   │   ├── GetVoyageById.cs
│   │   ├── UpdateVoyageById.cs
│   │   ├── SearchVoyages.cs
│   │   ├── CreateVoyageFromEstimate.cs
│   │   ├── CalculateVoyage.cs
│   │   └── CompleteVoyage.cs
│   ├── Shipment/
│   ├── Estimate/
│   ├── BunkerLot/
│   ├── Itinerary/
│   ├── VesselReport/
│   ├── Services/              ← Domain services (complex cross-entity logic)
│   └── AutoMapper/            ← Mapping profiles for this domain
│
├── MasterData/
│   ├── Vessel/
│   ├── Port/
│   ├── BusinessPartner/
│   └── ... (20+ more)
│
├── Finance/
├── OrderRequest/
│
├── Validator/                 ← FluentValidation validators (cross-cutting)
│   ├── ShipmentValidator.cs
│   ├── ShipmentCommissionValidator.cs
│   └── ...
│
├── DataSynchronization/       ← External system sync logic
├── BackgroundServices/        ← Async processing services
├── Hubs/                      ← SignalR hubs for real-time updates
├── Services/                  ← Utility/shared services
│
└── Setup.cs                   ← DI registration for entire Business layer
```

#### Validation with FluentValidation

Validators are defined in `Core/Business/Validator/` and auto-registered via assembly scanning:

```csharp
public class ShipmentValidator : AbstractValidator<ShipmentEntity>
{
    public ShipmentValidator()
    {
        RuleForEach(x => x.Commissions).ChildRules(commission =>
        {
            commission.RuleFor(c => c.CommissionablePartnerType)
                .NotEmpty().WithMessage("Commission type cannot be empty.");
            commission.RuleFor(c => c.BusinessPartnerId)
                .NotEmpty().WithMessage("Commission counterparty cannot be empty.");
        });

        RuleForEach(x => x.ProfitAndLossItems).ChildRules(item =>
        {
            item.When(i => i.Type == ProfitAndLossIdentifierEnum.MiscellaneousExpense.ToString(), () =>
            {
                item.RuleFor(i => i.Description)
                    .NotEmpty().WithSeverity(Severity.Error)
                    .WithMessage("Description (Misc. Expense) cannot be empty.");
            });
        });
    }
}
```

Validators can return **Errors** (block save) or **Warnings** (display to user but allow save).

#### Background Services & Real-Time Updates

- **`IVoyageBackgroundService`** — Post-save tasks for voyages (recalculation, sync).
- **`IRuleEvaluationBackgroundService`** — Task alert rule processing.
- **`IMediatorBackgroundService`** — Fire-and-forget MediatR sends.
- **`EntityHub` (SignalR)** — Push real-time entity change notifications to frontend.

#### DI Registration (`Setup.cs`)

```csharp
public static class Setup
{
    public static void Configure(IServiceCollection services, IConfiguration configuration)
    {
        // Auto-register all MediatR handlers in this assembly
        services.AddMediatR(cfg =>
            cfg.RegisterServicesFromAssembly(typeof(Setup).Assembly));

        // Auto-register all FluentValidation validators
        services.AddValidatorsFromAssembly(typeof(Setup).Assembly);

        // Register domain services
        services.AddScoped<IVoyageBackgroundService, VoyageBackgroundService>();
        services.AddScoped<IAuditService, AuditService>();
        services.AddScoped<IVoyageNumberService, VoyageNumberService>();
        // ... more registrations
    }
}
```

---

### 1.5 Core/Infrastructure Layer

The Infrastructure layer handles **all cross-cutting concerns**: database, authentication, mapping, middleware, and external service wiring.

#### DbContext

```csharp
public partial class DataContext : IdentityDbContext<UserEntity, RoleEntity, string>
{
    // Master Data
    public DbSet<VesselEntity> Vessels { get; set; }
    public DbSet<PortEntity> Ports { get; set; }

    // Voyage Management
    public DbSet<VoyageEntity> Voyages { get; set; }
    public DbSet<ShipmentEntity> Shipments { get; set; }

    // 100+ DbSets total...
}
```

Key features:

- **Global Query Filters**: Auto-applied per tenant (`TenantId`) and soft-delete (`IsDeleted = false`).
- **Audit Tracking**: `SaveChangesAsync` auto-populates `CreatedOn`, `CreatedById`, `ModifiedOn`, `ModifiedById`.
- **Table Naming Convention**: `{module}_{tablename}` (e.g., `masterdata_vessels`, `voyagemanagement_voyages`).
- **TPH Inheritance**: Used for polymorphic entities like `BaseProfitAndLossItemEntity`.

#### AutoMapper

Mapping profiles live in `Core/Infrastructure/AutoMapper/`:

```csharp
public class MappingProfile : Profile
{
    public MappingProfile()
    {
        CreateMap<VesselEntity, VesselDto>();
        CreateMap<VesselCreateDto, VesselEntity>();
        CreateMap<VoyageEntity, VoyageCrudDto>();
        // 100+ mappings...
    }
}
```

#### Middleware

```
Core/Infrastructure/Middlewares/
├── HttpRequestMiddleware.cs    ← Global exception handler + Correlation ID
├── ModelValidationMiddleware.cs ← Model state validation → ApiResponse<ApiError>
└── APIMiddleware.cs            ← API-level concerns
```

**HttpRequestMiddleware** — Every request gets a **Correlation ID** (either from `X-CorrelationId` header or auto-generated), logged with Serilog, and returned in the response headers.

**Error Handling Chain:**

```
Exception thrown anywhere
    → HttpRequestMiddleware catches it
    → Transforms via .TransformToApiResponseWithError()
    → Returns ApiResponse<ApiError> with ErrorCode
    → HTTP 400 (business error) or 403 (unauthorized) or 500 (unexpected)
```

#### Folder Structure

```
Core/Infrastructure/
├── DbContext/
│   ├── DataContext.cs           ← Main DbContext (100+ DbSets)
│   ├── AuditContext.cs          ← Audit trail context
│   ├── Changelog/               ← EF Core migrations
│   └── DataContextPartial/     ← Table configurations (partial classes)
├── AutoMapper/                  ← Mapping profiles
├── Middlewares/                  ← HTTP pipeline middleware
├── Security/                    ← JWT auth, policies, user context
├── ContextAccessor/             ← Tenant & user claims extraction
├── Cache/                       ← Caching strategies
├── DataSynchronization/         ← External system sync
├── EmailClient/                 ← Email sending
├── RabbitMessageQueue/          ← RabbitMQ integration
├── TemplateRenderer/            ← Document template rendering
├── EFCore/                      ← EF Core extensions
├── Configuration/               ← App configuration helpers
└── Setup.cs                     ← DI registration for infrastructure
```

---

### 1.6 API Layer

API projects are **thin wrappers** around MediatR. Controllers do three things:

1. Accept and validate HTTP input.
2. `await _mediator.Send(new Handler.Request { ... })`.
3. Wrap the result in `ApiResponse<T>.Success(result)`.

#### Controller Pattern

```csharp
[ApiController]
[Authorize]
[Route("[controller]")]
public class VesselsController : ControllerBase
{
    private readonly IMediator _mediator;

    public VesselsController(IMediator mediator) => _mediator = mediator;

    [HttpPost]
    [Authorize(Policy = Policies.VesselData.Create)]
    public async Task<ApiResponse<VesselDto>> CreateVessel(
        [FromBody] VesselCreateDto createParams)
    {
        var result = await _mediator.Send(
            new CreateVessel.Request { BodyData = createParams });
        return ApiResponse<VesselDto>.Success(result);
    }

    [HttpGet("{vesselId}")]
    [Authorize(Policy = Policies.VesselData.ViewRight)]
    public async Task<ApiResponse<VesselDto>> GetVesselById(Guid vesselId)
    {
        var result = await _mediator.Send(
            new GetVesselById.Request { Id = vesselId });
        return ApiResponse<VesselDto>.Success(result);
    }

    [HttpPost("Search")]
    [Authorize(Policy = Policies.VesselData.ViewRight)]
    public async Task<ApiResponse<PagedResult<VesselReducedDto>>> SearchVessel(
        [FromBody] VesselSearchDto searchParams)
    {
        var result = await _mediator.Send(
            new SearchVessel.Request { SearchParams = searchParams });
        return ApiResponse<PagedResult<VesselReducedDto>>.Success(result);
    }

    [HttpPut("{vesselId}")]
    [Authorize(Policy = Policies.VesselData.Update)]
    public async Task<ApiResponse<VesselDto>> UpdateVesselById(
        Guid vesselId, [FromBody] VesselUpdateDto updateParams)
    {
        var result = await _mediator.Send(
            new UpdateVesselById.Request { Id = vesselId, Body = updateParams });
        return ApiResponse<VesselDto>.Success(result);
    }

    [HttpDelete("{vesselId}")]
    [Authorize(Policy = Policies.VesselData.Delete)]
    public async Task<ApiResponse<bool>> DeleteVessel(Guid vesselId)
    {
        var result = await _mediator.Send(
            new DeleteVessel.Request { Id = vesselId });
        return ApiResponse<bool>.Success(result);
    }
}
```

#### Response Envelope

All API responses are wrapped in `ApiResponse<T>`:

```csharp
{
    "isSuccess": true,
    "traceId": "abc-123",
    "result": { /* actual data */ }
}

// Error response:
{
    "isSuccess": false,
    "result": {
        "errorCode": "DATA_NOT_FOUND",
        "errorMessage": "Voyage with given ID does not exist."
    }
}
```

Paginated responses use `PagedResult<T>`:

```csharp
{
    "isSuccess": true,
    "result": {
        "currentPage": 1,
        "pageSize": 20,
        "totalCounts": 150,
        "items": [ ... ]
    }
}
```

#### Authorization Policies

Every endpoint is protected with fine-grained policies:

```csharp
[Authorize(Policy = Policies.VesselData.Create)]    // Create permission
[Authorize(Policy = Policies.VesselData.ViewRight)]  // Read permission
[Authorize(Policy = Policies.VesselData.Update)]     // Update permission
[Authorize(Policy = Policies.VesselData.Delete)]     // Delete permission
```

#### `Program.cs` Startup Order

```csharp
// 1. Infrastructure (DB, Auth, Middleware)
Core.Infrastructure.Setup.Configure(builder.Services, builder.Configuration);
// 2. External Clients
BusinessCentralClient.Setup.Configure(builder.Services, builder.Configuration);
// 3. Business Logic (MediatR, Validators, Services)
Core.Business.Setup.Configure(builder.Services, builder.Configuration);
// 4. Controllers & Swagger
builder.Services.AddControllers();
builder.Services.AddSwaggerGen(...);
// 5. Serilog + Application Insights logging
// 6. Service validation (ValidateScopes, ValidateOnBuild)
// 7. Database warmup (CanConnectAsync)
// 8. Middleware pipeline
Core.Infrastructure.Setup.Configure(app, builder.Configuration);
// 9. Map controllers & SignalR hubs
app.MapControllers();
app.MapHub<EntityHub>("/EntityHub");
```

---

### 1.7 External Clients

Each external client follows a consistent pattern:

```
ExternalClients/{ClientName}/
├── {ClientName}Service.cs      ← Main service class
├── {ClientName}Configuration.cs ← Config POCO
├── Setup.cs                     ← DI registration with Configure()
├── Models/                      ← Request/response models
└── {ClientName}.csproj
```

**Common Pattern:**

1. Configuration is read from `appsettings.json`.
2. Service is registered as a singleton or scoped in `Setup.Configure()`.
3. Authentication (OAuth2, API Key, Basic Auth) is handled internally.
4. Token caching with thread-safe refresh logic.

```csharp
// Registration pattern (in Setup.cs):
public static class Setup
{
    public static IServiceCollection Configure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddSingleton<SednaClientService>(provider =>
        {
            var config = new SendaClientConfiguration
            {
                Url = configuration["Sedna:ApiUrl"],
                ApiKey = configuration["Sedna:ApiKey"],
                // ...
            };
            return new SednaClientService(config, httpClient, loggerFactory);
        });
        return services;
    }
}
```

---

### 1.8 Azure Functions

Azure Functions are used for **scheduled tasks** (timer triggers) with optional **manual HTTP triggers**.

```
Functions/
├── CurrencySync/
│   ├── CurrencySyncFunction.cs      ← Trigger definitions
│   └── CurrencySyncService.cs       ← Business logic
├── WfosSync/
├── ConsecutiveVoyages/
├── FailedJobMonitoring/
├── Program.cs                        ← DI setup (same as API but with Functions worker)
└── host.json
```

**Pattern**: Each function has a `*Function.cs` (trigger definitions) and a `*Service.cs` (logic). The function class is thin — it delegates to the service.

```csharp
[Function("CurrencySyncCronJob")]
public async Task RunTimerTrigger(
    [TimerTrigger("%CurrencyJob:CronExpression%")] TimerInfo timerInfo,
    CancellationToken cancellationToken)
{
    _logger.LogInformation("Currency sync started at {time}", DateTime.UtcNow);
    await ExecuteSynchronization(cancellationToken);
}

// Optional manual trigger:
[Function("CurrencySyncRequest")]
public async Task<HttpResponseData> RunHttpTrigger(
    [HttpTrigger(AuthorizationLevel.Function, "post", Route = "currency/sync")]
    HttpRequestData req, CancellationToken cancellationToken)
{
    await ExecuteSynchronization(cancellationToken);
    // ... return response
}
```

Functions share the same `Core.Business` and `Core.Infrastructure` layers as the APIs.

---

### 1.9 Key Design Patterns Summary

| Pattern                     | Where                          | Purpose                                        |
| --------------------------- | ------------------------------ | ---------------------------------------------- |
| **CQRS + MediatR**          | Core/Business handlers         | Separate read/write, isolated operations       |
| **Repository (DbContext)**  | Core/Infrastructure            | EF Core DbContext as Unit of Work              |
| **Multi-Tenancy**           | TenantedEntity + Query Filters | Tenant isolation at entity and DB level        |
| **Soft Delete**             | BaseEntity.SoftDelete()        | Never hard-delete, use IsDeleted flag          |
| **AutoMapper**              | Core/Infrastructure            | Entity ↔ DTO transformation                    |
| **FluentValidation**        | Core/Business/Validator        | Business rule validation (errors + warnings)   |
| **Adapter Pattern**         | ExternalClients                | Consistent interface for 3rd-party services    |
| **TPH Inheritance**         | Domain entities                | Polymorphic entities with discriminator column |
| **Optimistic Concurrency**  | IVersionedEntity               | Version number validation before save          |
| **Correlation ID Tracking** | HttpRequestMiddleware          | Request tracing across services                |
| **SignalR Hub**             | Core/Business/Hubs             | Real-time notifications to frontend            |
| **Background Services**     | IVoyageBackgroundService, etc. | Fire-and-forget async processing               |

---

## 2. Where to Put Code

### 2.1 Decision Flowchart

```
"I need to add something new"
    │
    ├─ Is it a database table/column?
    │   └─ Core/Domain/{Module}/Entities/ → Create entity or add property
    │      Then: Core/Infrastructure/DbContext/ → Add DbSet + migration
    │
    ├─ Is it a DTO for frontend?
    │   └─ Core/Domain/{Module}/Dtos/ → Create or modify DTO
    │      Then: Core/Infrastructure/AutoMapper/ → Add/update mapping
    │
    ├─ Is it a new API endpoint (CRUD/Search)?
    │   └─ Core/Business/{Module}/{Entity}/ → Create handler file
    │      Then: APIs/{ApiProject}/Controllers/ → Add controller action
    │
    ├─ Is it business logic or calculation?
    │   └─ Core/Business/{Module}/Services/ → Create or extend service
    │      Or: Core/Business/{Module}/{Entity}/ → Create Calculate{X} handler
    │
    ├─ Is it input validation?
    │   └─ Core/Business/Validator/ → Create or extend FluentValidation validator
    │
    ├─ Is it a 3rd-party integration?
    │   └─ ExternalClients/{ClientName}/ → Create new client project
    │      Then: Core/Infrastructure/Setup.cs → Wire DI
    │
    ├─ Is it a scheduled task?
    │   └─ Functions/{TaskName}/ → Create Function + Service
    │
    ├─ Is it a new enum or constant?
    │   └─ Core/Domain/Constants/ → Add to existing or create new
    │
    └─ Is it middleware or cross-cutting?
        └─ Core/Infrastructure/Middlewares/ → Create middleware
```

### 2.2 Adding a New Feature (Step-by-Step)

**Example: Adding a new "Claim" entity to VoyageManagement.**

#### Step 1: Domain — Define Entity

```csharp
// Core/Domain/VoyageManagement/Entities/ClaimEntity.cs
public class ClaimEntity : TenantedEntity
{
    [StandardString]
    public string? ClaimNumber { get; set; }

    [EnumString(typeof(ClaimStatusEnum))]
    public string Status { get; set; } = ClaimStatusEnum.Open.ToString();

    [StandardDecimal]
    public decimal? Amount { get; set; }

    public Guid? VoyageId { get; set; }
    public VoyageEntity? Voyage { get; set; }
}
```

#### Step 2: Domain — Define DTOs

```csharp
// Core/Domain/VoyageManagement/Dtos/ClaimDto.cs
public class ClaimDto : BaseDto
{
    public string? ClaimNumber { get; set; }
    public string? Status { get; set; }
    public decimal? Amount { get; set; }
    public Guid? VoyageId { get; set; }
}

// Core/Domain/VoyageManagement/Dtos/ClaimReducedDto.cs
public class ClaimReducedDto : BaseDto
{
    public string? ClaimNumber { get; set; }
    public string? Status { get; set; }
}
```

#### Step 3: Infrastructure — Register in DbContext

```csharp
// In DataContext.cs:
public DbSet<ClaimEntity> Claims { get; set; }

// In OnModelCreating:
modelBuilder.Entity<ClaimEntity>().ToTable("voyagemanagement_claims");
```

Then generate the EF migration:

```bash
dotnet ef migrations add AddClaimsTable -c DataContext --project ./Core/Infrastructure
```

#### Step 4: Infrastructure — Add AutoMapper Mapping

```csharp
// In MappingProfile.cs:
CreateMap<ClaimEntity, ClaimDto>();
CreateMap<ClaimDto, ClaimEntity>();
CreateMap<ClaimEntity, ClaimReducedDto>();
```

#### Step 5: Business — Create Handlers

```csharp
// Core/Business/VoyageManagement/Claim/GetClaimById.cs
public class GetClaimById
{
    public class Request : IRequest<ClaimDto>
    {
        public Guid Id { get; set; }
    }

    public class Response(DataContext context, IMapper mapper)
        : IRequestHandler<Request, ClaimDto>
    {
        public async Task<ClaimDto> Handle(Request request, CancellationToken ct)
        {
            var claim = context.Claims
                .AsNoTracking()
                .FirstOrDefault(e => e.Id == request.Id)
                    ?? throw new ApiException(ErrorCode.DATA_NOT_FOUND);

            return mapper.Map<ClaimDto>(claim);
        }
    }
}
```

Repeat for `CreateClaim.cs`, `UpdateClaimById.cs`, `SearchClaims.cs`, `DeleteClaim.cs`.

#### Step 6: API — Add Controller

```csharp
// APIs/OrderRequest/Controllers/ClaimsController.cs
[ApiController]
[Authorize]
[Route("[controller]")]
public class ClaimsController : ControllerBase
{
    private readonly IMediator _mediator;

    public ClaimsController(IMediator mediator) => _mediator = mediator;

    [HttpGet("{claimId}")]
    [Authorize(Policy = Policies.Claims.ViewRight)]
    public async Task<ApiResponse<ClaimDto>> GetClaimById(Guid claimId)
    {
        var result = await _mediator.Send(new GetClaimById.Request { Id = claimId });
        return ApiResponse<ClaimDto>.Success(result);
    }

    // ... CRUD endpoints
}
```

#### Step 7: Tests — Write Unit Tests

```csharp
// Core/Business.UnitTest/VoyageManagement/GetClaimByIdTests.cs
public class GetClaimByIdTests : IDisposable
{
    private readonly TestContext _context;
    private readonly IMapper _mapper;

    public GetClaimByIdTests()
    {
        _context = ContextGenerator.GetTestContext();
        _mapper = new Mapper(new MapperConfiguration(cfg =>
            cfg.AddProfile<MappingProfile>()));
    }

    [Fact]
    public async Task Handle_ShouldReturnClaim_WhenIdExists() { /* ... */ }

    [Fact]
    public async Task Handle_ShouldThrowApiException_WhenIdNotFound() { /* ... */ }

    public void Dispose() => _context?.Dispose();
}
```

### 2.3 Adding a New External Client

1. Create a new project: `ExternalClients/{ClientName}/`
2. Add `{ClientName}Service.cs`, `{ClientName}Configuration.cs`, `Setup.cs`
3. Reference in `Core/Infrastructure` project
4. Register in `Core/Infrastructure/Setup.cs`
5. Add config section to `appsettings.json`
6. Create test project: `ExternalClients/{ClientName}.UnitTest/`

### 2.4 Adding a New Azure Function

1. Create a folder: `Functions/{FunctionName}/`
2. Create `{FunctionName}Function.cs` (trigger definitions)
3. Create `{FunctionName}Service.cs` (business logic)
4. Register the service in `Functions/Program.cs`
5. Add scheduling config to `local.settings.json`

### 2.5 File Naming Conventions

| File Type       | Convention                     | Example                            |
| --------------- | ------------------------------ | ---------------------------------- |
| Entity          | `{Name}Entity.cs`              | `VoyageEntity.cs`                  |
| DTO             | `{Name}Dto.cs`                 | `VoyageCrudDto.cs`                 |
| Reduced DTO     | `{Name}ReducedDto.cs`          | `VoyageReducedDto.cs`              |
| Handler         | `{Verb}{Entity}.cs`            | `GetVoyageById.cs`                 |
| Validator       | `{Entity}Validator.cs`         | `ShipmentValidator.cs`             |
| Controller      | `{Entity}sController.cs`       | `VesselsController.cs`             |
| External Client | `{Name}ClientService.cs`       | `SednaClientService.cs`            |
| Configuration   | `{Name}ClientConfiguration.cs` | `SendaClientConfiguration.cs`      |
| DI Setup        | `Setup.cs`                     | `Setup.cs` (in each module)        |
| Azure Function  | `{Name}Function.cs`            | `CurrencySyncFunction.cs`          |
| Test            | `{HandlerName}Tests.cs`        | `GetBunkerOrderDetailByIdTests.cs` |
| Test Builder    | `{Entity}Builder.cs`           | `TcoBuilder.cs`                    |

---

## 3. Testing Guidelines

### 3.1 Testing Stack

| Tool                      | Version  | Purpose                          |
| ------------------------- | -------- | -------------------------------- |
| **xUnit**                 | 2.9.3    | Test framework (all projects)    |
| **Moq**                   | 4.20.70  | Mocking dependencies             |
| **FluentAssertions**      | 6.12–7.0 | Readable assertion syntax        |
| **EF Core InMemory**      | 8.0.15   | Database isolation in unit tests |
| **WebApplicationFactory** | 8.0.15   | Full API integration testing     |
| **Coverlet**              | 3.2–6.0  | Code coverage collection         |

### 3.2 Unit Tests

**Location**: `Core/Business.UnitTest/` and `Core/Infrastructure.UnitTest/`

**How unit tests work in this project:**

1. **Create an in-memory database** via `ContextGenerator.GetTestContext()`.
2. **Seed test data** using `SeedingService.SeedMasterData()`, `SeedingService.SeedShipmentData()`, etc.
3. **Mock external dependencies** (IMediator, background services) using Moq.
4. **Instantiate the handler directly** (not through DI).
5. **Call `Handle()`** and assert the result.

```csharp
public class GetBunkerOrderDetailByIdTests : IDisposable
{
    private readonly TestContext _context;
    private readonly IMapper _mapper;
    private readonly Mock<IMediator> _mediatorMock;

    public GetBunkerOrderDetailByIdTests()
    {
        // 1. Create in-memory DB
        _context = ContextGenerator.GetTestContext();

        // 2. Seed test data
        SeedingService.SeedMasterData(_context);
        BunkerOrderItemsSeedingService.SeedBunkerOrderData(_context);

        // 3. Set up AutoMapper
        _mapper = new Mapper(new MapperConfiguration(cfg =>
            cfg.AddProfile<BunkerLotMappingProfile>()));

        // 4. Mock dependencies
        _mediatorMock = new Mock<IMediator>();
        _mediatorMock
            .Setup(m => m.Send(
                It.IsAny<PopulateBunkerOrderInvoiceCosts.Request>(),
                It.IsAny<CancellationToken>()))
            .ReturnsAsync((PopulateBunkerOrderInvoiceCosts.Request req, CancellationToken ct)
                => req.BunkerOrderDto);
    }

    [Fact]
    public async Task Handle_ShouldReturnBunkerOrderDetail_WhenIdExists()
    {
        // Arrange
        var bunkerOrderId = _context.BunkerOrders.First().Id;
        var handler = new GetBunkerOrderDetailById.Handler(
            _context, _mapper, _mediatorMock.Object);
        var request = new GetBunkerOrderDetailById.Request { Id = bunkerOrderId };

        // Act
        var result = await handler.Handle(request, CancellationToken.None);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(bunkerOrderId, result.Id);
    }

    [Fact]
    public async Task Handle_ShouldThrowApiException_WhenIdDoesNotExist()
    {
        var handler = new GetBunkerOrderDetailById.Handler(
            _context, _mapper, _mediatorMock.Object);
        var request = new GetBunkerOrderDetailById.Request { Id = Guid.NewGuid() };

        await Assert.ThrowsAsync<ApiException>(
            () => handler.Handle(request, CancellationToken.None));
    }

    public void Dispose() => _context?.Dispose();
}
```

**Key Test Helpers:**

| Helper                       | Purpose                                          |
| ---------------------------- | ------------------------------------------------ |
| `ContextGenerator`           | Creates in-memory TestContext with mocked tenant |
| `SeedingService`             | Seeds master data, shipments, estimates, etc.    |
| `TestServiceProviderFactory` | Full DI container for tests needing all services |
| `TestUserAccessor`           | Mocked user context with claims                  |
| `DummyMediator`              | No-op MediatR for tests that don't need it       |
| `TcoBuilder` (Builders/)     | Fluent builder for complex test data             |
| `DataPreparationHelper`      | Helper to create required entities in DB         |

#### Writing a New Unit Test — Checklist

- [ ] Create test class implementing `IDisposable`.
- [ ] In constructor: create `TestContext`, seed data, set up mapper, mock dependencies.
- [ ] Name tests: `{MethodName}_{Scenario}_{ExpectedResult}`.
- [ ] Use AAA pattern (Arrange-Act-Assert).
- [ ] Test both happy path and error/edge cases.
- [ ] Dispose context in `Dispose()`.

### 3.3 Integration Tests

**Location**: `Core/Business.IntegrationTest/`

Integration tests use `WebApplicationFactory` to spin up the full API with real DI, then send HTTP requests against it.

**Architecture:**

```
Business.IntegrationTest/
├── Hosts/
│   └── OrderRequestHost.cs   ← WebApplicationFactory<Program>
├── Tests/
│   ├── [Abstract]/
│   │   ├── BaseIntegrationTest.cs   ← Abstract test runner
│   │   └── BaseTestStep.cs          ← Step-based execution
│   └── TestAsRoot/
│       ├── IntegrationTestAsRoot.cs ← Test suite definition
│       └── Steps/
│           ├── GenerateToken.cs          ← Auth step
│           ├── CalculateEstimateFlow/    ← Multi-step flow
│           └── CreateVoyageFlow/         ← Multi-step flow
└── Program.cs                ← CLI entry point for running tests
```

**Key Concepts:**

- **Step-based execution**: Each integration test is a sequence of `BaseTestStep<T>` instances.
- **OrderRequestHost**: Configurable WebApplicationFactory — can override DB, mock email, etc.
- **Golden file testing**: JSON-based test cases with expected responses.
- **HTML reporting**: Tests generate HTML reports for review.
- **Run modes**: `UpdateResponse` (update golden files), `Seed` (seed only), `Test` (verify).

```csharp
// Running integration tests:
// From CLI:
dotnet run --configuration Release -- test -frd True

// This runs IntegrationTestAsRoot which executes:
// 1. GenerateToken (authenticate)
// 2. CalculateEstimateFlow (create + calculate estimate)
// 3. CalculateTcoEstimateFlow (TCO estimate)
// 4. CreateVoyageFlow (create voyage from estimate)
```

### 3.4 External Client Tests

**Location**: `ExternalClients/{Client}.UnitTest/`

These are **live API integration tests** (not unit tests despite the project name). They call real external services using credentials from `appsettings.json`.

**Pattern:**

```csharp
[Collection("ConfigurationCollection")]
public class WfosClientServiceTest
{
    private readonly WfosClientService _client;

    public WfosClientServiceTest(ConfigurationFixture fixture)
    {
        // Build real client from config
        var config = new WfosClientConfiguration { /* from fixture */ };
        _client = new WfosClientService(config, httpClientFactory, loggerFactory);
    }

    [Fact]
    public async Task GetAccessToken_ShouldReturn_Success()
    {
        var token = await _client.GetAccessTokenAsync();
        Assert.NotEmpty(token);
    }
}
```

> **Note**: These tests require valid API credentials and network access. They may fail in CI if credentials are not configured.

### 3.5 Test Naming Conventions

```
{MethodOrHandler}_{WithScenarioOrCondition}_{ShouldExpectedBehavior}
```

**Examples:**

- `Handle_ShouldReturnBunkerOrderDetail_WhenIdExists`
- `CalculateBunkerOrderCosts_WithValidBunkerOrder_ShouldReturnCalculatedCosts`
- `Handle_ShouldThrowApiException_WhenIdDoesNotExist`
- `SoftDelete_TestClass_To_Context`
- `GetDistanceAsync_ValidRequest_ReturnsDistance`

**Folder organization** mirrors the `Core/Business/` structure:

```
Business.UnitTest/
├── BunkerOrder/         ← matches Core/Business/BunkerOrder
├── Finance/
├── MasterData/
├── VoyageManagement/
└── UserManagement/
```

### 3.6 CI Pipeline & Test Execution

The GitLab CI pipeline runs on every merge request to `dev`, `test`, or `prod`:

```yaml
stages:
  - build
  - test

# Build stage
build: # dotnet build BBC-BVMS.sln --configuration Release
check-migration-main: # dotnet ef migrations has-pending-model-changes -c DataContext
check-migration-audit: # dotnet ef migrations has-pending-model-changes -c AuditContext

# Test stage
unitTest.Infrastructure: # dotnet test Core/Infrastructure.UnitTest
unitTest.Business: # dotnet test Core/Business.UnitTest
integrationTest: # dotnet run Core/Business.IntegrationTest -- test
```

**Before submitting a merge request:**

1. Run `dotnet build BBC-BVMS.sln` — ensure it compiles.
2. Run `dotnet test Core/Infrastructure.UnitTest` — infrastructure tests pass.
3. Run `dotnet test Core/Business.UnitTest` — business logic tests pass.
4. Check pending migrations: `dotnet ef migrations has-pending-model-changes -c DataContext --project ./Core/Infrastructure`.

**Tests run serially** (`parallelizeTestCollections: false`) to avoid in-memory database conflicts.

---

## 4. Discussion & Improvements

### 4.1 Current Strengths

**Architecture:**

- Clean CQRS with MediatR keeps handlers small and focused.
- Strict layered architecture prevents circular dependencies.
- Multi-tenancy and soft-delete built into the base entities.
- Consistent patterns — once you learn one handler, you can write any handler.

**Developer Experience:**

- AutoMapper eliminates boilerplate mapping code.
- FluentValidation provides declarative, readable validation rules.
- Column attributes standardize DB schema conventions.
- Existing knowledge base in `Documents/knowledge-base/` with 18 domain docs.

**Observability:**

- Serilog + Application Insights for structured logging.
- Correlation ID tracking across all requests.
- SQL command text captured in telemetry.

**Testing:**

- In-memory database testing with seeding services.
- WebApplicationFactory for realistic integration tests.
- Step-based integration test framework with HTML reporting.
- Builder pattern for complex test data.

### 4.2 Known Gaps & Improvement Areas

#### Testing Gaps

| Area                        | Current State                                 | Recommendation                                             |
| --------------------------- | --------------------------------------------- | ---------------------------------------------------------- |
| **Controller tests**        | No controller-level tests                     | Add simple tests to verify auth policies and routing       |
| **Validation tests**        | Validators exist but few have dedicated tests | Add tests for each FluentValidation validator              |
| **Handler coverage**        | Some modules have tests, many handlers don't  | Prioritize tests for handlers with complex logic           |
| **External client mocking** | External client tests hit real APIs           | Add mock-based unit tests alongside live tests             |
| **Test parallelism**        | Disabled (serial execution)                   | Consider test isolation improvements to enable parallelism |

#### Architecture Observations

| Observation                             | Details                                                                                  | Suggestion                                                                                |
| --------------------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **Handler Response class naming**       | `Response` is used as the handler class name, which can be confusing with HTTP responses | Consider renaming to `Handler` for clarity (e.g., `GetVoyageById.Handler`)                |
| **DbContext direct access in handlers** | Handlers access `DataContext` directly (no repository abstraction)                       | This is fine for this project size; adding repositories would add unnecessary abstraction |
| **Large DataContext**                   | 100+ DbSets in one class                                                                 | Already mitigated with partial classes; consider splitting if it grows further            |
| **Mixed validation locations**          | Some validation in handlers, some in dedicated validators                                | Consolidate to FluentValidation validators where possible                                 |
| **Background service error handling**   | Fire-and-forget background tasks                                                         | Ensure all background services have proper error handling and retry logic                 |

#### Code Quality Suggestions

1. **Consistent error codes**: Review `ErrorCode` enum for duplicates and ensure all new handlers use the correct codes.
2. **Query optimization**: Use `AsNoTracking()` consistently on read-only queries. Some handlers may be missing this.
3. **Nullable reference types**: The project has nullable enabled — ensure new code properly handles nullability.
4. **Global usings**: Use `Usings.cs` files to reduce import boilerplate in new files.

### 4.3 Recommendations for New Developers

#### Before You Write Code

1. **Read the existing handlers** in the module you're working on. Copy the pattern.
2. **Check `Documents/knowledge-base/`** for domain-specific documentation.
3. **Check `Documents/Column_Attribute_Usage_Guides.md`** before adding entity properties.
4. **Check existing DTOs** before creating new ones — there may already be a suitable DTO.

#### While Writing Code

1. **One handler per file**. Never put multiple handlers in one file.
2. **Keep controllers thin**. All logic goes in the handler, not the controller.
3. **Use `AsNoTracking()`** for read-only queries.
4. **Throw `ApiException`** with the appropriate `ErrorCode` — never return raw exceptions.
5. **Follow the naming conventions** in section 2.5.
6. **Always add column attributes** to entity properties — never use raw `string` without `[StandardString]`, etc.
7. **Never manually set audit fields** (`CreatedOn`, `CreatedById`, etc.).

#### After Writing Code

1. **Write unit tests** for every new handler (at minimum: happy path + not-found case).
2. **Run the full test suite** before pushing.
3. **Generate a migration** if you changed entities, and verify it looks correct.
4. **Check the CI pipeline** passes on your merge request.

#### Common Pitfalls

| Pitfall                       | Why It's Wrong                       | What To Do Instead                                        |
| ----------------------------- | ------------------------------------ | --------------------------------------------------------- |
| Adding logic to controllers   | Breaks CQRS pattern, untestable      | Put logic in a MediatR handler                            |
| Creating a new DbContext      | Breaks shared session/transaction    | Use the existing `DataContext`                            |
| Hard-deleting records         | Breaks audit trail and references    | Use `entity.SoftDelete()`                                 |
| Ignoring tenant filters       | Data leak across tenants             | Use `context.BaseQuery<T>()` for filtered queries         |
| Forgetting AutoMapper mapping | Runtime `AutoMapperMappingException` | Add mapping in `MappingProfile.cs` and test it            |
| Not using `CancellationToken` | Operations can't be cancelled        | Always pass `CancellationToken` through the handler chain |

---

## Appendix

### A. Technology Stack Quick Reference

| Layer          | Technology                                         |
| -------------- | -------------------------------------------------- |
| Runtime        | .NET 8.0                                           |
| Web Framework  | ASP.NET Core Minimal Hosting                       |
| CQRS           | MediatR 12.2.0                                     |
| ORM            | Entity Framework Core 8.0.15 (SQL Server)          |
| Validation     | FluentValidation 12.0.0                            |
| Mapping        | AutoMapper 13.0.1                                  |
| Authentication | JWT Bearer + ASP.NET Core Identity                 |
| Logging        | Serilog + Application Insights                     |
| Real-time      | SignalR                                            |
| Message Queue  | RabbitMQ (7.0.0)                                   |
| Email          | MailKit 4.9.0                                      |
| Functions      | Azure Functions (Isolated Worker, .NET 8)          |
| Testing        | xUnit 2.9.3 + Moq 4.20.70 + FluentAssertions 7.0.0 |
| CI/CD          | GitLab CI → AKS deployment                         |

### B. Configuration Files

| File                  | Purpose                                                        |
| --------------------- | -------------------------------------------------------------- |
| `appsettings.json`    | Main configuration (connection strings, external service URLs) |
| `local.settings.json` | Azure Functions local config                                   |
| `host.json`           | Azure Functions host configuration                             |
| `.gitlab-ci.yml`      | CI/CD pipeline definition                                      |
| `xunit.runner.json`   | xUnit test runner config (serial execution)                    |

### C. Useful Commands

```bash
# Build the solution
dotnet build BBC-BVMS.sln

# Run unit tests
dotnet test Core/Infrastructure.UnitTest
dotnet test Core/Business.UnitTest

# Run integration tests
cd Core/Business.IntegrationTest
dotnet run --configuration Release -- test -frd True

# Generate EF migration
dotnet ef migrations add MigrationName -c DataContext --project ./Core/Infrastructure

# Check pending model changes
dotnet ef migrations has-pending-model-changes -c DataContext --project ./Core/Infrastructure

# Run API locally
cd APIs/MasterData
dotnet run

# Run Azure Functions locally
cd Functions
dotnet build
cd bin/Debug/net8.0
func host start
```

### D. Key Documents

| Document                | Location                                                |
| ----------------------- | ------------------------------------------------------- |
| Column Attributes Guide | `Documents/Column_Attribute_Usage_Guides.md`            |
| BVMS Modules Overview   | `Documents/knowledge-base/BVMS-Modules.md`              |
| Database ERD            | `Documents/knowledge-base/BVMS-ERD-Database.md`         |
| Bunker Calculation      | `Documents/knowledge-base/BVMS-Bunker-Calculation.md`   |
| P&L Calculation         | `Documents/knowledge-base/BVMS-PL-Calculation.md`       |
| Voyage P&L              | `Documents/knowledge-base/BVMS-Voyage-PL.md`            |
| Shipment Concept        | `Documents/knowledge-base/BVMS-Shipment-Concept.md`     |
| Azure Infrastructure    | `Documents/knowledge-base/BVMS-Azure-Infrastructure.md` |
| Master Data             | `Documents/knowledge-base/BVMS-Master-Data.md`          |
| EU ETS Calculation      | `Documents/knowledge-base/EU-ETS-Calculation.md`        |
| Deployment Guide        | `Deployment-Azure-Prod.md`                              |
| SQL Migration Scripts   | `Documents/sql-migration-scripts/`                      |

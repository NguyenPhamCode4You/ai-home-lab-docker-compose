# ApiResponse<TClass>

## Purpose
Standardized response envelope for the API layer, carrying success/failure state, payload, and trace context. Provides static factory methods to construct typed success or failure responses without exposing internal state mutation.

## Business Responsibility
Owns the contract for all API responses (`ApiResponse`), ensuring consistent serialization structure and trace correlation across all endpoints. `PagedResult` and `ApiError` are auxiliary types defined here to support list operations and error details respectively. Critical for maintaining a stable client contract and decoupling transport format from domain logic.

---
IF DOMAIN/DTO:

## Members
### 1. Success — Wraps data in a success response envelope
```csharp
public static ApiResponse<TClass> Success(TClass data, string traceId = "")
{
    return new ApiResponse<TClass>
    {
        IsSuccess = true,
        Result = data,
        TraceId = traceId
    };
}
```
**Explanation**: Factory for successful operations. Sets `IsSuccess = true` and assigns the domain payload to `Result`. Accepts optional `traceId` for request correlation, defaulting to empty string if omitted. Ensures consumers always receive a valid envelope with the correct success state.

### 2. Fail — Wraps error details in a failure response envelope
```csharp
public static ApiResponse<ApiError> Fail(ErrorCode errorCode, string? message, string traceId = "")
{
    return new ApiResponse<ApiError>
    {
        IsSuccess = false,
        TraceId = traceId,
        Result = new ApiError
        {
            ErrorCode = errorCode.ToString(),
            ErrorMessage = message,
        }
    };
}
```
**Explanation**: Factory for error responses. Returns an `ApiResponse<ApiError>` with `IsSuccess = false`. Creates an `ApiError` instance mapping the `ErrorCode` enum to its string representation and attaches the human-readable message. Used by handlers to return structured errors to the API layer.

### 3. ApiException Constructors — Translates domain error codes into exceptions
```csharp
public ApiException(ErrorCode error) : base(error.ToString(), new Exception(error.ToString()))
{
}

public ApiException(string message) : base(message, new Exception(ErrorCode.API_ERROR.ToString()))
{
}

public ApiException(ErrorCode error, string message) : base(message, new Exception(error.ToString()))
{
}
```
**Explanation**: Domain exception type used to signal failures that should be converted to `ApiResponse<ApiError>` by global exception handlers. Constructors accept either a structured `ErrorCode` or a raw message, preserving the error code in both the exception message and inner exception for debugging and logging.

---
## Dependencies
- `ApiError` — Referenced in `Fail` factory to construct the result payload for error responses.
- `ErrorCode` — Enum from `Core.Domain.Constants`; referenced in `Fail` factory for error mapping and in `ApiException` constructors to extract error codes.
- `PagedResult<TClass>` — Defined in the same file; referenced elsewhere in the codebase for pagination, but not used internally by `ApiResponse`.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]
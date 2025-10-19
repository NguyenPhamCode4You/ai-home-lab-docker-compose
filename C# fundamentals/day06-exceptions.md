# Day 6: Exception Handling & Best Practices

## 🎯 Learning Objectives

- Understand exception handling internals
- Master try-catch-finally mechanics
- Learn custom exception design
- Use exception filters effectively
- Handle async exceptions correctly
- Understand performance implications

---

## 1. Exception Fundamentals

### Exception Hierarchy

```csharp
System.Object
  └── System.Exception
        ├── SystemException
        │     ├── ArgumentException
        │     ├── InvalidOperationException
        │     ├── NullReferenceException
        │     ├── IndexOutOfRangeException
        │     └── ...
        └── ApplicationException (don't use as base!)
```

### Basic Exception Handling

```csharp
try
{
    // Code that might throw
    int result = Divide(10, 0);
}
catch (DivideByZeroException ex)
{
    // Handle specific exception
    Console.WriteLine($"Cannot divide by zero: {ex.Message}");
}
catch (Exception ex)
{
    // Handle all other exceptions
    Console.WriteLine($"Error: {ex.Message}");
}
finally
{
    // Always executes (cleanup code)
    Console.WriteLine("Cleanup");
}
```

---

## 2. Exception Handling Mechanics

### Multiple Catch Blocks

```csharp
// Order matters - specific to general
try
{
    ProcessFile("data.txt");
}
catch (FileNotFoundException ex)
{
    Console.WriteLine("File not found");
}
catch (UnauthorizedAccessException ex)
{
    Console.WriteLine("Access denied");
}
catch (IOException ex)
{
    Console.WriteLine("IO error");
}
catch (Exception ex)
{
    Console.WriteLine("Unexpected error");
    throw; // Rethrow to preserve stack trace
}
```

### Exception Filters (C# 6.0+)

```csharp
try
{
    ProcessData();
}
catch (Exception ex) when (ex.Message.Contains("timeout"))
{
    Console.WriteLine("Timeout occurred");
    // Only catches if condition is true
}
catch (Exception ex) when (ex is HttpRequestException && Log(ex))
{
    // Can call methods in filter (side effects!)
    HandleHttpError();
}

bool Log(Exception ex)
{
    logger.LogError(ex);
    return true; // Must return bool
}
```

### Finally Block Behavior

```csharp
// Finally ALWAYS executes
public int Method()
{
    try
    {
        return 1; // Finally runs before return!
    }
    finally
    {
        Console.WriteLine("Finally"); // Prints before return
    }
}

// Finally runs even with exception
try
{
    throw new Exception();
}
finally
{
    Console.WriteLine("Cleanup"); // Executes before exception propagates
}

// Finally vs Dispose
FileStream stream = null;
try
{
    stream = File.OpenRead("file.txt");
    // Use stream
}
finally
{
    stream?.Dispose(); // Manual cleanup
}

// Better: using statement
using (FileStream stream = File.OpenRead("file.txt"))
{
    // Use stream
} // Dispose() called automatically
```

---

## 3. Throwing Exceptions

### Throw vs Throw Ex

```csharp
// ✅ GOOD - Preserves stack trace
catch (Exception ex)
{
    throw; // Rethrows original exception with full stack trace
}

// ❌ BAD - Loses original stack trace
catch (Exception ex)
{
    throw ex; // Creates new stack trace from here!
}

// Wrapping exceptions
catch (Exception ex)
{
    throw new CustomException("Operation failed", ex); // Preserves inner exception
}
```

### When to Throw

```csharp
public class BankAccount
{
    private decimal balance;

    public void Withdraw(decimal amount)
    {
        // Validate arguments
        if (amount < 0)
            throw new ArgumentOutOfRangeException(nameof(amount), "Amount cannot be negative");

        // Validate state
        if (amount > balance)
            throw new InvalidOperationException("Insufficient funds");

        balance -= amount;
    }
}
```

### Throwing Best Practices

```csharp
// ✅ Use specific exceptions
throw new ArgumentNullException(nameof(parameter));
throw new ArgumentOutOfRangeException(nameof(index));
throw new InvalidOperationException("Invalid state");

// ❌ Don't use generic exceptions
throw new Exception("Something went wrong"); // Too generic!

// ✅ Provide helpful messages
throw new ArgumentException(
    $"Value must be between {min} and {max}",
    nameof(value));

// ✅ Use paramName for argument exceptions
throw new ArgumentNullException(nameof(customer));
```

---

## 4. Custom Exceptions

### Custom Exception Design

```csharp
// Basic custom exception
[Serializable]
public class InsufficientFundsException : Exception
{
    public decimal Balance { get; }
    public decimal RequestedAmount { get; }

    public InsufficientFundsException() { }

    public InsufficientFundsException(string message) : base(message) { }

    public InsufficientFundsException(string message, Exception innerException)
        : base(message, innerException) { }

    public InsufficientFundsException(decimal balance, decimal requestedAmount)
        : base($"Insufficient funds. Balance: {balance}, Requested: {requestedAmount}")
    {
        Balance = balance;
        RequestedAmount = requestedAmount;
    }

    // Serialization constructor
    protected InsufficientFundsException(SerializationInfo info, StreamingContext context)
        : base(info, context)
    {
        Balance = info.GetDecimal(nameof(Balance));
        RequestedAmount = info.GetDecimal(nameof(RequestedAmount));
    }

    public override void GetObjectData(SerializationInfo info, StreamingContext context)
    {
        base.GetObjectData(info, context);
        info.AddValue(nameof(Balance), Balance);
        info.AddValue(nameof(RequestedAmount), RequestedAmount);
    }
}
```

### Domain-Specific Exceptions

```csharp
public abstract class DomainException : Exception
{
    protected DomainException() { }
    protected DomainException(string message) : base(message) { }
    protected DomainException(string message, Exception innerException)
        : base(message, innerException) { }
}

public class OrderNotFoundException : DomainException
{
    public int OrderId { get; }

    public OrderNotFoundException(int orderId)
        : base($"Order with ID {orderId} was not found")
    {
        OrderId = orderId;
    }
}

public class ProductOutOfStockException : DomainException
{
    public int ProductId { get; }
    public int RequestedQuantity { get; }

    public ProductOutOfStockException(int productId, int requestedQuantity)
        : base($"Product {productId} is out of stock. Requested: {requestedQuantity}")
    {
        ProductId = productId;
        RequestedQuantity = requestedQuantity;
    }
}
```

---

## 5. Async Exception Handling

### Try-Catch with Async

```csharp
public async Task ProcessAsync()
{
    try
    {
        await DoSomethingAsync();
    }
    catch (HttpRequestException ex)
    {
        // Catches exception from async operation
        Logger.LogError(ex);
    }
}
```

### AggregateException

```csharp
// Task.WaitAll can throw AggregateException
Task[] tasks = new[]
{
    Task.Run(() => throw new InvalidOperationException()),
    Task.Run(() => throw new ArgumentException())
};

try
{
    Task.WaitAll(tasks); // Don't use in async code!
}
catch (AggregateException ex)
{
    // Handle multiple exceptions
    foreach (Exception inner in ex.InnerExceptions)
    {
        Console.WriteLine(inner.Message);
    }

    // Or flatten and handle
    ex.Handle(inner =>
    {
        if (inner is InvalidOperationException)
        {
            Console.WriteLine("Invalid operation");
            return true; // Handled
        }
        return false; // Not handled, will rethrow
    });
}

// ✅ BETTER: Use await with Task.WhenAll
try
{
    await Task.WhenAll(tasks);
}
catch (Exception ex)
{
    // Only catches FIRST exception (not aggregate)
    Console.WriteLine(ex.Message);
}
```

### Async Void - The Danger

```csharp
// ❌ DANGEROUS - Exceptions crash the application!
public async void DangerousMethodAsync()
{
    throw new Exception("Unhandled!"); // Crashes app!
}

// ✅ GOOD - Returns Task, exceptions can be caught
public async Task SafeMethodAsync()
{
    throw new Exception("Can be handled");
}

// Usage
try
{
    await SafeMethodAsync(); // Exception caught
}
catch (Exception ex)
{
    // Handles exception
}

// async void is ONLY for event handlers
private async void Button_Click(object sender, EventArgs e)
{
    try
    {
        await ProcessAsync();
    }
    catch (Exception ex)
    {
        MessageBox.Show(ex.Message);
    }
}
```

### Fire-and-Forget Pattern

```csharp
// ❌ BAD - Exceptions lost
_ = ProcessAsync(); // Discarded task, exceptions lost!

// ✅ GOOD - Safe fire-and-forget
public static async void FireAndForget(
    Func<Task> task,
    Action<Exception> errorHandler = null)
{
    try
    {
        await task();
    }
    catch (Exception ex)
    {
        errorHandler?.Invoke(ex);
    }
}

// Usage
FireAndForget(
    async () => await ProcessAsync(),
    ex => Logger.LogError(ex)
);
```

---

## 6. Performance Considerations

### Exception Cost

```csharp
// Exceptions are EXPENSIVE
// - Stack unwinding
// - Stack trace capture
// - Object allocation

// ❌ BAD - Using exceptions for flow control
public int Parse(string input)
{
    try
    {
        return int.Parse(input);
    }
    catch
    {
        return 0; // SLOW for invalid input!
    }
}

// ✅ GOOD - TryParse pattern
public int Parse(string input)
{
    return int.TryParse(input, out int result) ? result : 0;
}
```

### Try Pattern

```csharp
// Standard pattern for operations that may fail
public interface IParser<T>
{
    bool TryParse(string input, out T result);
}

public class IntParser : IParser<int>
{
    public bool TryParse(string input, out int result)
    {
        return int.TryParse(input, out result);
    }
}

// Modern C# - return tuples
public (bool success, int value) TryParse(string input)
{
    if (int.TryParse(input, out int result))
        return (true, result);
    return (false, 0);
}

// Usage
var (success, value) = TryParse("123");
if (success)
{
    Console.WriteLine(value);
}
```

### Avoiding Exceptions

```csharp
// ✅ Validation before operation
public void Withdraw(decimal amount)
{
    if (amount <= 0)
        throw new ArgumentOutOfRangeException(nameof(amount));

    if (amount > balance)
        throw new InvalidOperationException("Insufficient funds");

    balance -= amount;
}

// ✅ Check preconditions
if (File.Exists(path))
{
    File.Delete(path); // Won't throw FileNotFoundException
}

// ✅ Use null-conditional operator
string upper = text?.ToUpper(); // Returns null if text is null

// ✅ Use TryGet pattern
if (dictionary.TryGetValue(key, out var value))
{
    // Use value
}
```

---

## 7. Exception Handling Best Practices

### Guidelines

```csharp
// ✅ DO: Catch specific exceptions
catch (FileNotFoundException ex) { }
catch (UnauthorizedAccessException ex) { }

// ✅ DO: Provide context
throw new InvalidOperationException(
    $"Cannot process order {orderId} in state {currentState}");

// ✅ DO: Use exception filters
catch (HttpRequestException ex) when (ex.StatusCode == HttpStatusCode.NotFound)
{
    // Handle 404
}

// ✅ DO: Preserve stack trace
catch (Exception ex)
{
    LogError(ex);
    throw; // Not throw ex!
}

// ❌ DON'T: Catch and ignore
catch { } // Silent failure - BAD!

// ❌ DON'T: Catch Exception unnecessarily
catch (Exception) { } // Too broad

// ❌ DON'T: Use exceptions for flow control
try
{
    int value = array[index];
}
catch (IndexOutOfRangeException)
{
    // Check bounds instead!
}

// ✅ DO: Use using for cleanup
using var connection = new SqlConnection(connectionString);

// ✅ DO: Document exceptions
/// <summary>
/// Processes the order.
/// </summary>
/// <exception cref="ArgumentNullException">order is null</exception>
/// <exception cref="InvalidOperationException">order is already processed</exception>
public void ProcessOrder(Order order)
{
    // Implementation
}
```

### Global Exception Handling

```csharp
// ASP.NET Core
public class GlobalExceptionHandler : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        var response = exception switch
        {
            ValidationException => (StatusCodes.Status400BadRequest, "Validation error"),
            NotFoundException => (StatusCodes.Status404NotFound, "Not found"),
            UnauthorizedAccessException => (StatusCodes.Status403Forbidden, "Forbidden"),
            _ => (StatusCodes.Status500InternalServerError, "Internal error")
        };

        httpContext.Response.StatusCode = response.Item1;
        await httpContext.Response.WriteAsJsonAsync(
            new { error = response.Item2 },
            cancellationToken);

        return true;
    }
}

// WinForms
Application.ThreadException += (sender, e) =>
{
    MessageBox.Show(e.Exception.Message);
};

// WPF
Application.Current.DispatcherUnhandledException += (sender, e) =>
{
    MessageBox.Show(e.Exception.Message);
    e.Handled = true;
};

// Console App
AppDomain.CurrentDomain.UnhandledException += (sender, e) =>
{
    Console.WriteLine($"Unhandled: {e.ExceptionObject}");
};
```

---

## 8. Interview Questions

### Q1: Difference between throw and throw ex?

**Answer:** `throw` preserves the original stack trace, while `throw ex` creates a new stack trace from the current location. Always use `throw` to rethrow without losing information.

### Q2: When should you NOT catch exceptions?

**Answer:**

- When you can't meaningfully handle it
- For flow control (use TryXXX pattern instead)
- OutOfMemoryException, StackOverflowException (app must terminate)
- In library code unless you add value

### Q3: What is exception filter?

**Answer:** Exception filter (when clause) allows conditional catching based on exception properties. Filter is evaluated without unwinding stack, enabling logging before stack unwind.

### Q4: Why is async void dangerous?

**Answer:** Exceptions in async void methods cannot be caught by caller and crash the application. Only use async void for event handlers. Use async Task for all other async methods.

### Q5: How to handle multiple exceptions from Task.WhenAll?

**Answer:** Task.WhenAll returns AggregateException containing all exceptions. When awaited, only first exception is thrown. Access task.Exception to get all exceptions.

---

## 9. Practical Exercises

### Exercise 1: Implement Result<T> Pattern

Create a Result<T> type that eliminates exceptions for expected failures:

- Success/Failure states
- Error information
- Map/Bind operations

### Exercise 2: Global Exception Handler

Implement middleware that:

- Catches all unhandled exceptions
- Logs with context
- Returns appropriate HTTP status codes
- Includes correlation ID

### Exercise 3: Retry Logic with Exponential Backoff

Create a retry wrapper that:

- Retries on specific exceptions
- Exponential backoff
- Maximum retry count
- Async support

### Exercise 4: Custom Exception Hierarchy

Design exception hierarchy for e-commerce domain:

- Base domain exception
- Specific exceptions for different failures
- Include relevant business data

---

## 10. Key Takeaways

✅ **Exceptions are expensive** - use for exceptional cases
✅ **Use `throw`** not `throw ex` to preserve stack trace
✅ **Exception filters** enable conditional catching
✅ **async void** only for event handlers
✅ **TryXXX pattern** for expected failures
✅ **Catch specific exceptions** not Exception
✅ **Always cleanup** with using or finally
✅ **Document exceptions** in XML comments

---

## Tomorrow's Preview

**Day 7: Collections & Data Structures**

- Collection interfaces deep dive
- List, Dictionary, HashSet internals
- Concurrent collections
- ImmutableCollections
- Big-O complexity analysis

---

**Exception handling done right prevents bugs and improves reliability!** 🛡️

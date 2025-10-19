# Day 8: Async/Await & Task Parallel Library

## 🎯 Learning Objectives

- Understand async/await state machine transformation
- Master Task vs ValueTask
- Learn ConfigureAwait and synchronization context
- Handle cancellation properly with CancellationToken
- Avoid common async pitfalls and deadlocks

---

## 1. Async/Await Fundamentals

### Basic Async Method

```csharp
public async Task<string> DownloadDataAsync(string url)
{
    using HttpClient client = new HttpClient();
    string result = await client.GetStringAsync(url);
    return result;
}

// Usage
string data = await DownloadDataAsync("https://example.com");
```

### What Compiler Generates (State Machine)

```csharp
// Your code:
public async Task<int> GetNumberAsync()
{
    await Task.Delay(1000);
    return 42;
}

// What compiler generates (simplified):
[AsyncStateMachine(typeof(GetNumberAsyncStateMachine))]
public Task<int> GetNumberAsync()
{
    var stateMachine = new GetNumberAsyncStateMachine();
    stateMachine.builder = AsyncTaskMethodBuilder<int>.Create();
    stateMachine.state = -1;
    stateMachine.builder.Start(ref stateMachine);
    return stateMachine.builder.Task;
}

struct GetNumberAsyncStateMachine : IAsyncStateMachine
{
    public int state;
    public AsyncTaskMethodBuilder<int> builder;
    private TaskAwaiter awaiter;

    public void MoveNext()
    {
        int result;
        try
        {
            if (state == 0)
            {
                // Resume after await
                awaiter.GetResult();
                result = 42;
                state = -2;
                builder.SetResult(result);
                return;
            }

            // First call
            awaiter = Task.Delay(1000).GetAwaiter();

            if (awaiter.IsCompleted)
            {
                // Fast path: already completed
                awaiter.GetResult();
                result = 42;
                state = -2;
                builder.SetResult(result);
                return;
            }

            // Suspend and schedule continuation
            state = 0;
            builder.AwaitUnsafeOnCompleted(ref awaiter, ref this);
        }
        catch (Exception ex)
        {
            state = -2;
            builder.SetException(ex);
        }
    }

    public void SetStateMachine(IAsyncStateMachine stateMachine) { }
}
```

---

## 2. Task vs ValueTask

### Task<T>

Reference type, allocated on heap.

```csharp
public async Task<int> GetNumberAsync()
{
    await Task.Delay(100);
    return 42;
}

// Each call allocates a Task<int> object
for (int i = 0; i < 1000; i++)
{
    int result = await GetNumberAsync(); // 1000 Task allocations
}
```

### ValueTask<T>

Struct type, can avoid heap allocation when result is already available.

```csharp
public async ValueTask<int> GetNumberAsync()
{
    // If cached, returns ValueTask<int> without allocation
    if (cache.TryGetValue(key, out int cached))
    {
        return cached; // No Task allocation!
    }

    await Task.Delay(100);
    int result = 42;
    cache[key] = result;
    return result;
}
```

### When to Use ValueTask

```csharp
// ✅ Use ValueTask when:
// - Result is often synchronously available
// - Hot path optimization needed
// - Reducing allocations is critical

public ValueTask<int> GetCachedAsync(int id)
{
    if (cache.TryGetValue(id, out int value))
    {
        return new ValueTask<int>(value); // No heap allocation
    }

    return new ValueTask<int>(FetchFromDatabaseAsync(id));
}

// ❌ DON'T use ValueTask when:
// - Multiple awaits on same ValueTask
// - Storing ValueTask in a field
// - Converting to Task repeatedly

// ❌ BAD
ValueTask<int> vt = GetValueAsync();
int result1 = await vt; // OK
int result2 = await vt; // UNDEFINED BEHAVIOR!

// ✅ GOOD - await once
int result = await GetValueAsync();
```

---

## 3. ConfigureAwait

### Synchronization Context

```csharp
// UI thread (WinForms/WPF)
private async void Button_Click(object sender, EventArgs e)
{
    // Runs on UI thread
    label.Text = "Loading...";

    // awaits capture UI synchronization context
    string data = await DownloadDataAsync();

    // Continuation runs on UI thread (can update UI)
    label.Text = data;
}

// Without ConfigureAwait
public async Task<string> DownloadDataAsync()
{
    await Task.Delay(1000); // Captures context
    // Continuation runs on original context (UI thread)
    return "data";
}

// With ConfigureAwait(false)
public async Task<string> DownloadDataAsync()
{
    await Task.Delay(1000).ConfigureAwait(false); // Don't capture context
    // Continuation runs on thread pool thread
    return "data";
}
```

### ConfigureAwait(false)

```csharp
// ✅ Library code - use ConfigureAwait(false)
public async Task<string> GetDataAsync()
{
    using HttpClient client = new HttpClient();

    // No need for original context
    string result = await client.GetStringAsync(url)
        .ConfigureAwait(false);

    // This code runs on thread pool thread
    return result.ToUpper(); // No UI access needed
}

// ❌ UI code - DON'T use ConfigureAwait(false)
private async void Button_Click(object sender, EventArgs e)
{
    string data = await GetDataAsync()
        .ConfigureAwait(false);

    // BUG: This runs on thread pool, not UI thread!
    label.Text = data; // InvalidOperationException!
}

// ✅ GOOD - No ConfigureAwait in UI code
private async void Button_Click(object sender, EventArgs e)
{
    string data = await GetDataAsync();

    // Runs on UI thread - safe
    label.Text = data;
}
```

### ConfigureAwait Rules

```csharp
// Library/Infrastructure code
public async Task<T> LibraryMethodAsync<T>()
{
    // Always use ConfigureAwait(false)
    await SomeOperationAsync().ConfigureAwait(false);
    await AnotherOperationAsync().ConfigureAwait(false);
    return default(T);
}

// Application/UI code
public async Task ApplicationMethodAsync()
{
    // Never use ConfigureAwait(false)
    await LibraryMethodAsync();
    UpdateUI(); // Need UI context
}

// ASP.NET Core - ConfigureAwait not needed
public async Task<IActionResult> GetData()
{
    // ASP.NET Core doesn't have synchronization context
    var data = await _service.GetDataAsync();
    return Ok(data);
}
```

---

## 4. Cancellation

### CancellationToken

```csharp
public async Task<string> DownloadDataAsync(
    string url,
    CancellationToken cancellationToken = default)
{
    using HttpClient client = new HttpClient();

    // Pass token to async operations
    string result = await client.GetStringAsync(url, cancellationToken);

    // Check for cancellation
    cancellationToken.ThrowIfCancellationRequested();

    // Process data
    return ProcessData(result);
}

// Usage
CancellationTokenSource cts = new CancellationTokenSource();

// Cancel after 5 seconds
cts.CancelAfter(TimeSpan.FromSeconds(5));

try
{
    string data = await DownloadDataAsync(url, cts.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("Operation was cancelled");
}
finally
{
    cts.Dispose();
}
```

### Cancellation Best Practices

```csharp
// ✅ Accept CancellationToken parameter
public async Task ProcessAsync(CancellationToken cancellationToken = default)
{
    // Check periodically in long-running operations
    for (int i = 0; i < 1000; i++)
    {
        cancellationToken.ThrowIfCancellationRequested();
        await ProcessItemAsync(i, cancellationToken);
    }
}

// ✅ Link tokens
CancellationTokenSource cts1 = new CancellationTokenSource();
CancellationTokenSource cts2 = new CancellationTokenSource();

using CancellationTokenSource linked = CancellationTokenSource
    .CreateLinkedTokenSource(cts1.Token, cts2.Token);

// Cancelled when either cts1 or cts2 is cancelled
await ProcessAsync(linked.Token);

// ✅ Register callbacks
cts.Token.Register(() =>
{
    Console.WriteLine("Cancellation requested");
});

// ✅ Timeout pattern
using CancellationTokenSource cts = new CancellationTokenSource(
    TimeSpan.FromSeconds(30));

await DownloadDataAsync(url, cts.Token);
```

---

## 5. Common Async Pitfalls

### Deadlock in Synchronous Code

```csharp
// ❌ DEADLOCK!
public void Method()
{
    // Blocks thread waiting for async operation
    string result = DownloadDataAsync().Result;
    // or
    string result = DownloadDataAsync().GetAwaiter().GetResult();
}

public async Task<string> DownloadDataAsync()
{
    await Task.Delay(1000); // Captures synchronization context
    // Tries to resume on UI thread, but UI thread is blocked!
    return "data";
}

// ✅ FIX 1: Make it async all the way
public async Task MethodAsync()
{
    string result = await DownloadDataAsync();
}

// ✅ FIX 2: Use ConfigureAwait(false) in library code
public async Task<string> DownloadDataAsync()
{
    await Task.Delay(1000).ConfigureAwait(false);
    return "data";
}
```

### Async Void

```csharp
// ❌ DANGEROUS - Can't catch exceptions!
public async void DangerousAsync()
{
    await Task.Delay(100);
    throw new Exception("Uncaught!"); // Crashes app!
}

// ✅ GOOD - Returns Task
public async Task SafeAsync()
{
    await Task.Delay(100);
    throw new Exception("Can be caught");
}

// Only use async void for event handlers
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

### Forgetting to Await

```csharp
// ❌ BAD - Task not awaited (fire-and-forget)
public void ProcessData()
{
    ProcessDataAsync(); // Warning: unawaited task!
    // Method returns immediately, exception lost
}

// ✅ GOOD - Await the task
public async Task ProcessData()
{
    await ProcessDataAsync();
}

// ✅ Explicit fire-and-forget with error handling
public void ProcessData()
{
    _ = ProcessDataAsync().ContinueWith(task =>
    {
        if (task.IsFaulted)
        {
            Logger.LogError(task.Exception);
        }
    }, TaskScheduler.Default);
}
```

### Async Over Sync

```csharp
// ❌ BAD - Fake async
public async Task<int> GetNumberAsync()
{
    return await Task.Run(() => 42); // Wastes thread!
}

// ✅ GOOD - Don't fake async for CPU-bound work
public int GetNumber()
{
    return 42; // Synchronous is fine
}

// ✅ Use async only for I/O-bound operations
public async Task<string> ReadFileAsync()
{
    return await File.ReadAllTextAsync("file.txt");
}
```

### Parallel Async Operations

```csharp
// ❌ SLOW - Sequential execution
public async Task ProcessAllAsync(List<string> urls)
{
    foreach (string url in urls)
    {
        await DownloadAsync(url); // One at a time!
    }
}

// ✅ GOOD - Parallel execution
public async Task ProcessAllAsync(List<string> urls)
{
    List<Task> tasks = urls.Select(url => DownloadAsync(url)).ToList();
    await Task.WhenAll(tasks);
}

// ✅ GOOD - With results
public async Task<List<string>> ProcessAllAsync(List<string> urls)
{
    Task<string>[] tasks = urls.Select(url => DownloadAsync(url)).ToArray();
    string[] results = await Task.WhenAll(tasks);
    return results.ToList();
}

// ✅ GOOD - Process as completed
public async Task ProcessAllAsync(List<string> urls)
{
    List<Task<string>> tasks = urls.Select(url => DownloadAsync(url)).ToList();

    while (tasks.Count > 0)
    {
        Task<string> completed = await Task.WhenAny(tasks);
        tasks.Remove(completed);

        string result = await completed;
        Console.WriteLine(result);
    }
}
```

---

## 6. Task Parallel Library (TPL)

### Task.Run

```csharp
// CPU-bound work on thread pool
Task<int> task = Task.Run(() =>
{
    return ExpensiveComputation();
});

int result = await task;
```

### Task.WhenAll

```csharp
// Wait for all tasks
Task<int> task1 = GetNumberAsync(1);
Task<int> task2 = GetNumberAsync(2);
Task<int> task3 = GetNumberAsync(3);

int[] results = await Task.WhenAll(task1, task2, task3);
// results[0] = task1 result
// results[1] = task2 result
// results[2] = task3 result

// Handle exceptions
try
{
    await Task.WhenAll(task1, task2, task3);
}
catch (Exception ex)
{
    // Only first exception is thrown
    // Access all exceptions from tasks:
    if (task1.IsFaulted) Logger.Log(task1.Exception);
    if (task2.IsFaulted) Logger.Log(task2.Exception);
    if (task3.IsFaulted) Logger.Log(task3.Exception);
}
```

### Task.WhenAny

```csharp
// Wait for first task to complete
Task<int> task1 = GetNumberAsync(1);
Task<int> task2 = GetNumberAsync(2);

Task<int> completed = await Task.WhenAny(task1, task2);
int result = await completed;

// Timeout pattern
Task<string> dataTask = DownloadDataAsync(url);
Task timeoutTask = Task.Delay(TimeSpan.FromSeconds(5));

Task completed = await Task.WhenAny(dataTask, timeoutTask);

if (completed == timeoutTask)
{
    throw new TimeoutException("Operation timed out");
}

string data = await dataTask;
```

### Task.Delay

```csharp
// Async delay (doesn't block thread)
await Task.Delay(TimeSpan.FromSeconds(1));

// Cancellable delay
CancellationTokenSource cts = new CancellationTokenSource();
await Task.Delay(TimeSpan.FromSeconds(10), cts.Token);

// Retry with exponential backoff
public async Task<T> RetryAsync<T>(
    Func<Task<T>> operation,
    int maxRetries = 3)
{
    for (int i = 0; i < maxRetries; i++)
    {
        try
        {
            return await operation();
        }
        catch (Exception) when (i < maxRetries - 1)
        {
            await Task.Delay(TimeSpan.FromSeconds(Math.Pow(2, i)));
        }
    }

    throw new Exception("Max retries exceeded");
}
```

---

## 7. Advanced Patterns

### AsyncLazy<T>

```csharp
public class AsyncLazy<T>
{
    private readonly Lazy<Task<T>> instance;

    public AsyncLazy(Func<Task<T>> factory)
    {
        instance = new Lazy<Task<T>>(() => factory());
    }

    public Task<T> Value => instance.Value;
}

// Usage
AsyncLazy<string> lazyData = new AsyncLazy<string>(
    async () => await DownloadDataAsync());

// First call starts download
string data1 = await lazyData.Value;

// Second call returns same Task (not re-executed)
string data2 = await lazyData.Value;
```

### Async Throttling

```csharp
public class AsyncThrottler
{
    private readonly SemaphoreSlim semaphore;

    public AsyncThrottler(int maxConcurrency)
    {
        semaphore = new SemaphoreSlim(maxConcurrency);
    }

    public async Task<T> ExecuteAsync<T>(Func<Task<T>> operation)
    {
        await semaphore.WaitAsync();
        try
        {
            return await operation();
        }
        finally
        {
            semaphore.Release();
        }
    }
}

// Usage: Limit to 5 concurrent downloads
AsyncThrottler throttler = new AsyncThrottler(5);

List<Task<string>> tasks = urls
    .Select(url => throttler.ExecuteAsync(() => DownloadAsync(url)))
    .ToList();

string[] results = await Task.WhenAll(tasks);
```

---

## 8. Interview Questions

### Q1: What does async/await do?

**Answer:** async/await is compiler transformation that generates a state machine. It allows asynchronous operations without blocking threads. The method returns immediately with a Task, and the state machine resumes when the awaited operation completes.

### Q2: Difference between Task.Result and await?

**Answer:** Task.Result blocks the calling thread until task completes (can cause deadlocks). await doesn't block, yielding control and resuming asynchronously when complete. Always use await in async code.

### Q3: When to use ValueTask instead of Task?

**Answer:** Use ValueTask when result is often synchronously available (e.g., cached), to avoid heap allocation. Don't await ValueTask multiple times or store it. Use Task for most cases.

### Q4: What is ConfigureAwait(false)?

**Answer:** ConfigureAwait(false) tells await not to capture synchronization context. Continuation runs on thread pool instead of original context. Use in library code for performance, never in UI code that needs to update UI.

### Q5: How to handle cancellation?

**Answer:** Accept CancellationToken parameter, pass it to async operations, check Token.IsCancellationRequested or call ThrowIfCancellationRequested() periodically in long-running operations.

---

## 9. Practical Exercises

### Exercise 1: Parallel Download with Progress

- Download multiple URLs concurrently
- Report progress for each
- Handle failures gracefully
- Support cancellation

### Exercise 2: Retry Logic

- Implement retry with exponential backoff
- Maximum retry attempts
- Configurable delay strategy
- Cancellation support

### Exercise 3: Async Producer-Consumer

- Producer adds items asynchronously
- Consumer processes items asynchronously
- Bounded queue
- Graceful shutdown

### Exercise 4: Fix Deadlock

- Given code with deadlock
- Identify the cause
- Fix using async/await properly

---

## 10. Key Takeaways

✅ **async/await** = compiler-generated state machine
✅ **Task** for general use, **ValueTask** for optimization
✅ **ConfigureAwait(false)** in library code
✅ **CancellationToken** for cooperative cancellation
✅ **Avoid async void** except for event handlers
✅ **Always await** - don't block with .Result
✅ **Task.WhenAll** for parallel execution
✅ **Beware of deadlocks** from blocking on async

---

## Tomorrow's Preview

**Day 9: Multithreading & Concurrency**

- Thread fundamentals
- Synchronization primitives
- Thread-safe patterns
- Race conditions and deadlocks
- Parallel LINQ

---

**Master async/await for responsive, scalable applications!** ⚡

# Day 2: Memory Management & Garbage Collection

## 🎯 Learning Objectives

- Understand stack vs heap memory allocation
- Master garbage collection generations and algorithms
- Learn the IDisposable pattern and resource management
- Identify and prevent memory leaks in managed code
- Use modern memory-efficient types (Span<T>, Memory<T>)

---

## 1. Stack vs Heap

### The Stack

**Characteristics:**

- Fast allocation/deallocation (just move stack pointer)
- LIFO (Last In, First Out) structure
- Limited size (~1MB per thread)
- Automatically cleaned up when method returns
- Stores local variables and method parameters

```csharp
void StackExample()
{
    int x = 10;              // Allocated on stack
    double y = 3.14;         // Allocated on stack
    Point p = new Point();   // Value type - on stack

    // When method returns, stack is unwound
    // All local variables automatically cleaned up
}
```

### The Heap

**Characteristics:**

- Slower allocation (managed by GC)
- Large size (limited by system memory)
- Requires garbage collection for cleanup
- Stores reference type objects and static variables
- Managed by the Garbage Collector

```csharp
void HeapExample()
{
    Person person = new Person();  // Object on heap, reference on stack
    int[] array = new int[1000];   // Array on heap, reference on stack
    string s = "Hello";            // String on heap, reference on stack

    // Objects remain on heap after method returns
    // GC will clean up when no longer referenced
}
```

### Memory Layout Example

```csharp
public class Container
{
    public int Value;          // On heap (part of Container)
    public Point Location;     // On heap inline (value type field)
    public Person Owner;       // Reference to another heap object
}

void Example()
{
    int local = 42;           // Stack: 4 bytes
    Container c = new Container();  // Stack: 8 bytes (reference)
                                    // Heap: Object with header + fields

    // Stack layout:
    // [local: 4 bytes]
    // [c reference: 8 bytes] --> points to heap

    // Heap layout:
    // [Object header: 8-16 bytes]
    // [Method table pointer: 8 bytes]
    // [Value: 4 bytes]
    // [Location.X: 4 bytes]
    // [Location.Y: 4 bytes]
    // [Owner reference: 8 bytes] --> points to another heap object
}
```

---

## 2. Garbage Collection Fundamentals

### How GC Works

The .NET Garbage Collector:

1. **Mark** - Identifies which objects are still in use
2. **Compact** - Moves living objects together, freeing memory
3. **Update references** - Updates all references to moved objects

```csharp
// GC roots (starting points for marking):
// - Static fields
// - Local variables on stack
// - CPU registers
// - GC handles
// - Finalization queue

public class GCDemo
{
    private static Person staticPerson; // GC root (static)

    void Method()
    {
        Person local = new Person(); // GC root (local variable)
        // When method exits, 'local' is no longer a root
        // Object becomes eligible for collection
    }
}
```

### GC Generations

**Generation 0 (Gen 0)**

- Newly allocated objects
- Collected most frequently
- Small, fast collection
- Survives → promoted to Gen 1

**Generation 1 (Gen 1)**

- Short-lived objects that survived one collection
- Medium-frequency collection
- Buffer between Gen 0 and Gen 2
- Survives → promoted to Gen 2

**Generation 2 (Gen 2)**

- Long-lived objects
- Collected infrequently
- Expensive, full collection
- Typically application-lifetime objects

```csharp
// Check object generation
object obj = new object();
Console.WriteLine($"Generation: {GC.GetGeneration(obj)}"); // 0

GC.Collect(0); // Force Gen 0 collection
Console.WriteLine($"Generation: {GC.GetGeneration(obj)}"); // 1 (promoted)

GC.Collect(1); // Force Gen 1 collection
Console.WriteLine($"Generation: {GC.GetGeneration(obj)}"); // 2 (promoted)
```

### Large Object Heap (LOH)

Objects >= 85,000 bytes go directly to LOH (Gen 2).

```csharp
// Small object - regular heap
byte[] small = new byte[1000]; // Gen 0

// Large object - LOH (Gen 2 immediately)
byte[] large = new byte[100_000]; // LOH

// LOH is NOT compacted by default (performance)
// Can cause fragmentation
// .NET 4.5.1+: Can compact LOH explicitly
GCSettings.LargeObjectHeapCompactionMode = GCLargeObjectHeapCompactionMode.CompactOnce;
GC.Collect();
```

### GC Modes

**Workstation GC**

- Default for client applications
- One GC thread
- Lower latency for UI responsiveness

**Server GC**

- Default for server applications (ASP.NET Core)
- One GC thread per CPU core
- Higher throughput, higher memory usage

```xml
<!-- Configure in .csproj or runtimeconfig.json -->
<PropertyGroup>
  <ServerGarbageCollection>true</ServerGarbageCollection>
  <ConcurrentGarbageCollection>true</ConcurrentGarbageCollection>
</PropertyGroup>
```

---

## 3. IDisposable Pattern

### Why IDisposable?

Deterministic cleanup of unmanaged resources:

- File handles
- Database connections
- Network sockets
- Graphics handles
- Unmanaged memory

```csharp
// Basic IDisposable implementation
public class ResourceHolder : IDisposable
{
    private IntPtr unmanagedResource; // Unmanaged resource
    private FileStream managedResource; // Managed resource
    private bool disposed = false;

    public ResourceHolder()
    {
        unmanagedResource = // Allocate unmanaged resource
        managedResource = new FileStream("file.txt", FileMode.Open);
    }

    // Public dispose method
    public void Dispose()
    {
        Dispose(disposing: true);
        GC.SuppressFinalize(this); // Prevent finalizer from running
    }

    // Protected dispose method
    protected virtual void Dispose(bool disposing)
    {
        if (!disposed)
        {
            if (disposing)
            {
                // Dispose managed resources
                managedResource?.Dispose();
            }

            // Free unmanaged resources
            if (unmanagedResource != IntPtr.Zero)
            {
                // Free unmanaged memory
                unmanagedResource = IntPtr.Zero;
            }

            disposed = true;
        }
    }

    // Finalizer (destructor)
    ~ResourceHolder()
    {
        Dispose(disposing: false);
    }
}
```

### Using Statement

```csharp
// Traditional using statement
using (var resource = new ResourceHolder())
{
    // Use resource
} // Dispose() called automatically

// C# 8.0+ using declaration
using var resource = new ResourceHolder();
// Use resource
// Dispose() called at end of scope
```

### IAsyncDisposable (C# 8.0+)

```csharp
public class AsyncResourceHolder : IAsyncDisposable
{
    private NetworkStream stream;

    public async ValueTask DisposeAsync()
    {
        if (stream != null)
        {
            await stream.FlushAsync();
            stream.Dispose();
        }
    }
}

// Usage
await using var resource = new AsyncResourceHolder();
// Use resource
// DisposeAsync() called automatically
```

---

## 4. Memory Leaks in Managed Code

### Common Causes

#### 1. Event Handler Leaks

```csharp
// ❌ BAD - Memory leak
public class Publisher
{
    public event EventHandler SomethingHappened;

    public void RaiseEvent()
    {
        SomethingHappened?.Invoke(this, EventArgs.Empty);
    }
}

public class Subscriber
{
    public Subscriber(Publisher publisher)
    {
        publisher.SomethingHappened += OnSomethingHappened;
        // LEAK: Publisher keeps Subscriber alive!
    }

    private void OnSomethingHappened(object sender, EventArgs e)
    {
        // Handle event
    }
}

// ✅ GOOD - Unsubscribe
public class Subscriber : IDisposable
{
    private Publisher publisher;

    public Subscriber(Publisher publisher)
    {
        this.publisher = publisher;
        publisher.SomethingHappened += OnSomethingHappened;
    }

    public void Dispose()
    {
        publisher.SomethingHappened -= OnSomethingHappened;
    }

    private void OnSomethingHappened(object sender, EventArgs e)
    {
        // Handle event
    }
}
```

#### 2. Static References

```csharp
// ❌ BAD - Static collection grows forever
public static class Cache
{
    private static Dictionary<string, object> cache = new();

    public static void Add(string key, object value)
    {
        cache[key] = value; // Never removed!
    }
}

// ✅ GOOD - Use weak references or cache eviction
public static class Cache
{
    private static Dictionary<string, WeakReference> cache = new();

    public static void Add(string key, object value)
    {
        cache[key] = new WeakReference(value);
    }

    public static object Get(string key)
    {
        if (cache.TryGetValue(key, out var weakRef))
        {
            return weakRef.Target; // null if collected
        }
        return null;
    }
}
```

#### 3. Timer Leaks

```csharp
// ❌ BAD - Timer keeps object alive
public class Worker
{
    private System.Timers.Timer timer;

    public Worker()
    {
        timer = new System.Timers.Timer(1000);
        timer.Elapsed += OnTimerElapsed;
        timer.Start();
        // LEAK: Timer is GC root, keeps Worker alive!
    }

    private void OnTimerElapsed(object sender, ElapsedEventArgs e)
    {
        // Work
    }
}

// ✅ GOOD - Stop and dispose timer
public class Worker : IDisposable
{
    private System.Timers.Timer timer;

    public Worker()
    {
        timer = new System.Timers.Timer(1000);
        timer.Elapsed += OnTimerElapsed;
        timer.Start();
    }

    public void Dispose()
    {
        timer?.Stop();
        timer?.Dispose();
    }

    private void OnTimerElapsed(object sender, ElapsedEventArgs e)
    {
        // Work
    }
}
```

#### 4. Captured Variables in Closures

```csharp
// ❌ BAD - Closure captures large object
public class DataProcessor
{
    public Action ProcessData()
    {
        var largeData = new byte[1_000_000]; // 1 MB
        // Load data...

        return () =>
        {
            // Only need this
            Console.WriteLine(largeData.Length);
            // But entire largeData is captured!
        };
    }
}

// ✅ GOOD - Capture only what you need
public class DataProcessor
{
    public Action ProcessData()
    {
        var largeData = new byte[1_000_000];
        // Load data...

        int length = largeData.Length; // Extract needed value
        return () =>
        {
            Console.WriteLine(length); // Only captures int
        };
    }
}
```

---

## 5. Modern Memory-Efficient Types

### Span<T> (C# 7.2+)

Stack-only type for working with contiguous memory.

```csharp
// Span over array
int[] array = { 1, 2, 3, 4, 5 };
Span<int> span = array;
Span<int> slice = span.Slice(1, 3); // { 2, 3, 4 }

// Modify through span
slice[0] = 20;
Console.WriteLine(array[1]); // 20 - modified original array

// Stack allocation (no heap allocation!)
Span<byte> stackSpan = stackalloc byte[256];
for (int i = 0; i < stackSpan.Length; i++)
{
    stackSpan[i] = (byte)i;
}
// No GC pressure!

// String slicing without allocation
ReadOnlySpan<char> text = "Hello, World!".AsSpan();
ReadOnlySpan<char> hello = text.Slice(0, 5); // "Hello"
ReadOnlySpan<char> world = text.Slice(7, 5); // "World"
```

### Memory<T>

Heap-friendly alternative to Span<T>.

```csharp
// Memory can be stored in fields (unlike Span)
public class DataBuffer
{
    private Memory<byte> buffer;

    public DataBuffer(int size)
    {
        buffer = new byte[size];
    }

    public async Task FillAsync(Stream stream)
    {
        // Can use in async methods (unlike Span)
        int read = await stream.ReadAsync(buffer);
    }

    public Span<byte> GetSpan() => buffer.Span;
}
```

### ArrayPool<T>

Reuse arrays to reduce GC pressure.

```csharp
// ❌ BAD - Allocates new array each time
void ProcessData()
{
    byte[] buffer = new byte[4096]; // Heap allocation
    // Use buffer...
} // Eligible for GC

// ✅ GOOD - Rent from pool
void ProcessData()
{
    byte[] buffer = ArrayPool<byte>.Shared.Rent(4096);
    try
    {
        // Use buffer...
    }
    finally
    {
        ArrayPool<byte>.Shared.Return(buffer);
    }
}

// Even better with span
void ProcessData()
{
    byte[] buffer = ArrayPool<byte>.Shared.Rent(4096);
    try
    {
        Span<byte> span = buffer.AsSpan(0, 4096);
        // Use span...
    }
    finally
    {
        ArrayPool<byte>.Shared.Return(buffer);
    }
}
```

### MemoryPool<T>

Similar to ArrayPool but with IMemoryOwner.

```csharp
void ProcessData()
{
    using IMemoryOwner<byte> owner = MemoryPool<byte>.Shared.Rent(4096);
    Memory<byte> memory = owner.Memory;
    // Use memory...
} // Automatically returned
```

---

## 6. Performance Best Practices

### Reduce Allocations

```csharp
// ❌ BAD - String concatenation in loop
string result = "";
for (int i = 0; i < 1000; i++)
{
    result += i.ToString(); // Many allocations!
}

// ✅ GOOD - Use StringBuilder
var sb = new StringBuilder();
for (int i = 0; i < 1000; i++)
{
    sb.Append(i);
}
string result = sb.ToString();

// ✅ EVEN BETTER - Use Span/stackalloc for small strings
Span<char> buffer = stackalloc char[32];
for (int i = 0; i < 1000; i++)
{
    if (i.TryFormat(buffer, out int written))
    {
        // Use buffer.Slice(0, written)
    }
}
```

### Struct vs Class for Performance

```csharp
// ❌ Allocating many small objects
var points = new List<Point>();
for (int i = 0; i < 1_000_000; i++)
{
    points.Add(new Point { X = i, Y = i }); // If Point is class: 1M heap allocations
}

// ✅ Using struct - no heap allocations
readonly struct Point
{
    public int X { get; }
    public int Y { get; }
    public Point(int x, int y) => (X, Y) = (x, y);
}
// List still allocates, but contains Point VALUES not references
```

### Object Pooling

```csharp
public class ObjectPool<T> where T : class, new()
{
    private readonly ConcurrentBag<T> objects = new();

    public T Rent()
    {
        return objects.TryTake(out T item) ? item : new T();
    }

    public void Return(T item)
    {
        objects.Add(item);
    }
}

// Usage
var pool = new ObjectPool<StringBuilder>();
var sb = pool.Rent();
try
{
    sb.Clear();
    // Use StringBuilder
}
finally
{
    pool.Return(sb);
}
```

---

## 7. Analyzing Memory Issues

### Using dotnet-counters

```bash
# Install
dotnet tool install --global dotnet-counters

# Monitor GC
dotnet-counters monitor -n MyApp --counters System.Runtime

# Watch for:
# - High Gen 2 collection frequency
# - Large heap size
# - High allocation rate
```

### Using dotnet-dump

```bash
# Install
dotnet tool install --global dotnet-dump

# Create dump
dotnet-dump collect -p <pid>

# Analyze
dotnet-dump analyze <dump-file>

# Commands:
# dumpheap -stat        # Object statistics
# gcroot <address>      # Why object is alive
# dumpheap -mt <MT>     # Objects of specific type
```

### Visual Studio Memory Profiler

- Take memory snapshots
- Compare snapshots
- Identify leaked objects
- View allocation call stacks

---

## 8. Interview Questions

### Q1: Explain Stack vs Heap

**Answer:**

- **Stack:** LIFO, fast, automatic cleanup, stores value types and references, limited size (~1MB/thread)
- **Heap:** Managed by GC, slower, stores reference type objects, large size, requires GC for cleanup

### Q2: What are GC generations and why?

**Answer:**
Generational hypothesis: Most objects die young.

- **Gen 0:** New objects, collected frequently (fast)
- **Gen 1:** Survived Gen 0, buffer generation
- **Gen 2:** Long-lived, collected rarely (expensive)
  This optimizes GC by collecting young objects more frequently.

### Q3: When would you use IDisposable?

**Answer:**
When your class holds unmanaged resources:

- File handles, database connections, network sockets
- Native memory allocations
- Graphics resources
  Implement full Dispose pattern with finalizer for safety.

### Q4: What causes memory leaks in .NET?

**Answer:**

- Event handlers not unsubscribed
- Static references to objects
- Unclosed IDisposable objects
- Timers not stopped
- Captured variables in closures
- Cache without eviction

### Q5: What is Span<T> and when to use it?

**Answer:**
Stack-only type for memory-efficient array/string operations:

- Zero-copy slicing
- Stack allocation (stackalloc)
- Better performance (no GC)
- Cannot be boxed, cannot be in fields, cannot cross async boundaries
  Use for high-performance scenarios with contiguous memory.

---

## 9. Practical Exercises

### Exercise 1: Implement a Memory-Efficient String Parser

```csharp
// Parse CSV without allocating strings for each field
// Use ReadOnlySpan<char>
// Measure allocations before/after
```

### Exercise 2: Fix Memory Leaks

```csharp
// Given code with event handler leaks
// Identify and fix all leaks
// Verify with memory profiler
```

### Exercise 3: Optimize with ArrayPool

```csharp
// Refactor method that allocates byte arrays
// Use ArrayPool<T> to eliminate allocations
// Benchmark performance improvement
```

### Exercise 4: Implement Proper Dispose Pattern

```csharp
// Create class with managed and unmanaged resources
// Implement full IDisposable pattern
// Add unit tests
```

---

## 10. Key Takeaways

✅ **Stack** is fast, automatic; **Heap** requires GC
✅ **GC generations** optimize for short-lived objects
✅ **IDisposable** for deterministic cleanup of resources
✅ **Memory leaks** happen even in managed code
✅ **Span<T>** for high-performance, zero-copy operations
✅ **ArrayPool<T>** to reduce GC pressure
✅ **Profile and measure** - don't optimize blindly

---

## Tomorrow's Preview

Tomorrow: **Delegates, Events & Functional Programming**

- Delegate internals and multicast
- Event patterns and best practices
- Func, Action, Predicate
- Lambda expressions and closures
- Expression trees

---

**Keep Practicing!** 💪 Memory management is crucial for building high-performance applications.

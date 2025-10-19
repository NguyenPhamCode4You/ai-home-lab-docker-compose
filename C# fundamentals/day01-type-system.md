# Day 1: Type System & Value vs Reference Types

## 🎯 Learning Objectives

- Understand the CLR type system architecture
- Master the differences between value and reference types
- Learn boxing/unboxing and its performance implications
- Know when to use structs vs classes
- Understand memory layout and object structure

---

## 1. CLR Type System Overview

### The Common Type System (CTS)

The CLR type system is the foundation of .NET. Every type in C# derives from `System.Object`.

```csharp
// Everything is an object
int number = 42;
object obj = number; // Valid - int derives from object
Console.WriteLine(obj.GetType()); // System.Int32
```

### Type Categories

1. **Value Types** - Stored on stack (usually), contain actual data
2. **Reference Types** - Stored on heap, contain references to data

---

## 2. Value Types Deep Dive

### Characteristics

- Stored on stack (when local variables) or inline in objects
- Contains actual data
- Derived from `System.ValueType`
- Cannot be null (unless Nullable<T>)
- Passed by value (copy) by default

### Built-in Value Types

```csharp
// Integral types
byte b = 255;           // 8-bit unsigned
sbyte sb = -128;        // 8-bit signed
short s = 32767;        // 16-bit signed
ushort us = 65535;      // 16-bit unsigned
int i = 2147483647;     // 32-bit signed
uint ui = 4294967295;   // 32-bit unsigned
long l = 9223372036854775807;  // 64-bit signed
ulong ul = 18446744073709551615; // 64-bit unsigned

// Floating point
float f = 3.14f;        // 32-bit
double d = 3.14159;     // 64-bit
decimal dec = 3.14159m; // 128-bit (financial calculations)

// Other
bool flag = true;       // Boolean
char c = 'A';          // Unicode character
DateTime dt = DateTime.Now; // Struct!
Guid guid = Guid.NewGuid(); // Struct!
```

### Custom Value Types (Structs)

```csharp
public struct Point
{
    public int X { get; set; }
    public int Y { get; set; }

    public Point(int x, int y)
    {
        X = x;
        Y = y;
    }

    public double DistanceFromOrigin()
    {
        return Math.Sqrt(X * X + Y * Y);
    }
}

// Usage
Point p1 = new Point(3, 4);
Point p2 = p1; // Creates a COPY
p2.X = 10;
Console.WriteLine($"p1.X: {p1.X}, p2.X: {p2.X}"); // p1.X: 3, p2.X: 10
```

### Readonly Structs (C# 7.2+)

```csharp
public readonly struct ImmutablePoint
{
    public int X { get; }
    public int Y { get; }

    public ImmutablePoint(int x, int y)
    {
        X = x;
        Y = y;
    }

    // Compiler ensures no mutations
}
```

### Ref Structs (C# 7.2+)

```csharp
// Can only exist on the stack - cannot be boxed
public ref struct StackOnlyStruct
{
    public Span<byte> Buffer;

    public StackOnlyStruct(Span<byte> buffer)
    {
        Buffer = buffer;
    }
}

// Usage
Span<byte> stackBuffer = stackalloc byte[128];
var stackOnly = new StackOnlyStruct(stackBuffer);
// Cannot: object obj = stackOnly; // Compile error!
// Cannot: List<StackOnlyStruct> list; // Compile error!
```

---

## 3. Reference Types Deep Dive

### Characteristics

- Stored on heap
- Variables hold references (pointers)
- Derived from `System.Object` (but not `System.ValueType`)
- Can be null
- Passed by reference by default

### Common Reference Types

```csharp
// Classes
class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
}

// Strings (immutable reference type)
string s = "Hello";

// Arrays
int[] numbers = { 1, 2, 3 };

// Delegates
Action action = () => Console.WriteLine("Hello");

// Objects
object obj = new object();
```

### Reference Type Example

```csharp
class BankAccount
{
    public decimal Balance { get; set; }

    public void Deposit(decimal amount)
    {
        Balance += amount;
    }
}

// Usage
BankAccount account1 = new BankAccount { Balance = 100 };
BankAccount account2 = account1; // Both reference SAME object
account2.Deposit(50);
Console.WriteLine(account1.Balance); // 150 - SAME object!
```

---

## 4. Boxing and Unboxing

### What is Boxing?

Converting a value type to a reference type (object).

```csharp
int number = 42;        // Value type on stack
object boxed = number;  // BOXING - creates heap object
```

### What Happens During Boxing?

1. Allocate memory on heap
2. Copy value to heap
3. Return reference to heap object

### What is Unboxing?

Converting a boxed value type back to its original type.

```csharp
object boxed = 42;
int unboxed = (int)boxed; // UNBOXING - extract value
```

### Performance Implications

```csharp
// ❌ BAD - Boxing in loop (slow!)
ArrayList list = new ArrayList();
for (int i = 0; i < 1000; i++)
{
    list.Add(i); // BOXES each int!
}

// ✅ GOOD - No boxing (fast!)
List<int> list = new List<int>();
for (int i = 0; i < 1000; i++)
{
    list.Add(i); // No boxing!
}
```

### Hidden Boxing

```csharp
// Hidden boxing examples
int number = 42;

// Boxing happens here:
Console.WriteLine(number); // Boxing!
string s = number.ToString(); // No boxing (specialized method)
string formatted = string.Format("{0}", number); // Boxing!

// Avoid boxing:
Console.WriteLine(number.ToString()); // No boxing
```

---

## 5. Memory Layout

### Value Type Memory Layout

```csharp
struct MyStruct
{
    public int A;    // 4 bytes
    public byte B;   // 1 byte
    public short C;  // 2 bytes
}
// Total: 8 bytes (may include padding)
```

### Reference Type Memory Layout

```csharp
class MyClass
{
    public int A;    // 4 bytes (on heap)
}
// Object on heap:
// - Object header (8-16 bytes)
// - Method table pointer (8 bytes on 64-bit)
// - Field data (4 bytes)
// - Padding
// Reference variable: 8 bytes (on 64-bit system)
```

### Stack vs Heap

```csharp
void Example()
{
    // Stack allocation
    int x = 10;              // 4 bytes on stack
    Point p = new Point();   // 8 bytes on stack

    // Heap allocation
    Person person = new Person(); // Reference (8 bytes) on stack
                                  // Object on heap (header + fields)

    int[] array = new int[100];   // Reference (8 bytes) on stack
                                  // Array object on heap
}
```

---

## 6. When to Use Struct vs Class

### Use Struct When:

✅ Type represents a single value (like coordinates, dimensions)
✅ Size is small (< 16 bytes recommended)
✅ Type is immutable
✅ Type won't be boxed frequently
✅ Semantically represents a value

```csharp
// Good struct examples
public struct Point { public int X, Y; }
public struct Color { public byte R, G, B, A; }
public struct Complex { public double Real, Imaginary; }
```

### Use Class When:

✅ Type represents complex entity
✅ Type needs inheritance
✅ Type is large (> 16 bytes)
✅ Type needs to be null
✅ Type will be mutated frequently

```csharp
// Good class examples
public class Customer { /* many fields */ }
public class Order { /* complex behavior */ }
public abstract class Shape { /* inheritance */ }
```

### The 16-Byte Rule

```csharp
// ❌ BAD - Large struct (84 bytes)
public struct LargeStruct
{
    public long A, B, C, D, E, F, G, H, I, J; // 80 bytes
    public int Z; // 4 bytes
}
// Copying this is expensive!

// ✅ GOOD - Make it a class
public class LargeData
{
    public long A, B, C, D, E, F, G, H, I, J;
    public int Z;
}
// Only copy 8-byte reference
```

---

## 7. Passing Parameters

### By Value (Default)

```csharp
void ModifyValue(int x)
{
    x = 100; // Only modifies local copy
}

void ModifyReference(Person person)
{
    person.Name = "New Name"; // Modifies object (reference copied)
    person = new Person();    // Local reference changed only
}

int num = 42;
ModifyValue(num);
Console.WriteLine(num); // 42 - unchanged

Person p = new Person { Name = "Old" };
ModifyReference(p);
Console.WriteLine(p.Name); // "New Name" - object modified
```

### By Reference (ref)

```csharp
void ModifyByRef(ref int x)
{
    x = 100; // Modifies original variable
}

void ReplaceObject(ref Person person)
{
    person = new Person { Name = "Replaced" }; // Replaces original reference
}

int num = 42;
ModifyByRef(ref num);
Console.WriteLine(num); // 100 - changed!

Person p = new Person { Name = "Old" };
ReplaceObject(ref p);
Console.WriteLine(p.Name); // "Replaced" - reference replaced
```

### Out Parameters

```csharp
bool TryParse(string input, out int result)
{
    result = 0; // Must assign before returning
    return int.TryParse(input, out result);
}

// C# 7.0+ inline declaration
if (int.TryParse("123", out int value))
{
    Console.WriteLine(value); // 123
}
```

### In Parameters (C# 7.2+)

```csharp
void ProcessLargeStruct(in LargeStruct data)
{
    // data is passed by reference (efficient)
    // data is readonly (cannot modify)
    // data.X = 10; // Compile error!
}
```

---

## 8. Nullable Value Types

### Nullable<T>

```csharp
int? nullableInt = null;
int? anotherNullable = 42;

// Nullable is a struct:
struct Nullable<T> where T : struct
{
    private bool hasValue;
    private T value;

    public bool HasValue => hasValue;
    public T Value => hasValue ? value : throw new InvalidOperationException();
}

// Usage
if (nullableInt.HasValue)
{
    Console.WriteLine(nullableInt.Value);
}

// Null-coalescing
int result = nullableInt ?? 0; // 0 if null

// Nullable reference types (C# 8.0+)
#nullable enable
string? nullableString = null; // Can be null
string nonNullableString = "Hello"; // Cannot be null (warning if null)
```

---

## 9. Common Pitfalls

### Pitfall 1: Mutable Structs

```csharp
// ❌ BAD - Mutable struct
public struct MutablePoint
{
    public int X { get; set; }
    public int Y { get; set; }

    public void MoveRight() { X++; } // Mutation!
}

var points = new List<MutablePoint>();
points.Add(new MutablePoint { X = 0, Y = 0 });
points[0].MoveRight(); // No effect! Works on a COPY!

// ✅ GOOD - Immutable struct
public readonly struct ImmutablePoint
{
    public int X { get; }
    public int Y { get; }

    public ImmutablePoint(int x, int y) => (X, Y) = (x, y);
    public ImmutablePoint MoveRight() => new ImmutablePoint(X + 1, Y);
}
```

### Pitfall 2: Default Values

```csharp
public struct Point
{
    public int X { get; set; }
    public int Y { get; set; }

    public Point(int x, int y)
    {
        X = x;
        Y = y;
    }
}

// Structs always have a parameterless constructor
Point p = new Point(); // X=0, Y=0 (not your constructor!)
Point p2 = default(Point); // X=0, Y=0
```

### Pitfall 3: Boxing in Interfaces

```csharp
interface IMovable
{
    void Move(int x, int y);
}

struct Point : IMovable
{
    public int X { get; set; }
    public int Y { get; set; }

    public void Move(int x, int y)
    {
        X += x;
        Y += y;
    }
}

Point p = new Point();
IMovable movable = p; // BOXING!
movable.Move(10, 10); // Modifies BOXED copy
// p is unchanged!
```

---

## 10. Interview Questions

### Question 1: What's the difference between struct and class?

**Answer:**

- **Struct:** Value type, stack allocation (usually), copied by value, no inheritance, cannot be null (unless Nullable<T>), best for small immutable data
- **Class:** Reference type, heap allocation, passed by reference, supports inheritance, can be null, best for complex objects

### Question 2: What is boxing and why is it expensive?

**Answer:**
Boxing converts a value type to a reference type (object). It's expensive because:

1. Allocates memory on the heap
2. Copies the value to the heap
3. Adds object header overhead
4. Triggers garbage collection more frequently
5. Cache performance suffers (heap vs stack)

### Question 3: When should you use a struct?

**Answer:**
Use structs when:

- Type represents a single value (coordinates, dimensions)
- Size is small (< 16 bytes)
- Type is immutable
- Type won't be boxed frequently
- You need stack allocation performance

### Question 4: Can a struct inherit from a class?

**Answer:**
No. Structs can only:

- Implement interfaces
- Implicitly derive from System.ValueType (which derives from System.Object)
- Cannot inherit from other structs or classes
- Cannot be inherited from

### Question 5: What happens when you assign one struct to another?

**Answer:**
A **memberwise copy** is created. All fields are copied to the new struct. They are completely independent afterwards. Changes to one don't affect the other.

---

## 11. Practical Exercises

### Exercise 1: Create an Immutable Point3D Struct

```csharp
// Requirements:
// - Readonly struct
// - X, Y, Z coordinates
// - Methods: Add, Distance, Normalize
// - Overload operators (+, -)
// - Override ToString, Equals, GetHashCode
```

### Exercise 2: Demonstrate Boxing/Unboxing

```csharp
// Write code that:
// 1. Boxes an int
// 2. Unboxes it
// 3. Shows type information
// 4. Demonstrates performance difference with/without boxing
```

### Exercise 3: Fix the Mutable Struct Problem

```csharp
// Given a mutable struct in a collection
// Fix it to work correctly
// Compare performance: struct vs class
```

### Exercise 4: Implement Value Equality

```csharp
// Create a struct Point with:
// - Proper Equals implementation
// - Proper GetHashCode implementation
// - Operator overloads (==, !=)
// - IEquatable<Point> implementation
```

---

## 12. Key Takeaways

✅ **Value types** contain data; **reference types** contain references
✅ **Structs** should be small, immutable, and represent single values
✅ **Boxing** converts value types to reference types (expensive!)
✅ **Avoid mutable structs** - they cause confusing bugs
✅ **Use ref/in parameters** to pass large structs efficiently
✅ **Understand memory layout** to write efficient code
✅ **Choose the right type** based on semantics and performance

---

## 13. Tomorrow's Preview

Tomorrow we'll dive into **Memory Management & Garbage Collection**:

- Stack vs Heap in detail
- GC generations and collection algorithms
- IDisposable pattern and using statements
- Memory leaks in managed code
- Modern memory-efficient types (Span<T>, Memory<T>)

---

## Additional Reading

- [Value Types (C# Reference)](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)
- [Reference Types (C# Reference)](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/reference-types)
- [CLR via C# - Chapter 5: Primitive, Reference, and Value Types](https://www.amazon.com/CLR-via-4th-Developer-Reference/dp/0735667454)

**Time to Practice!** 💪 Implement the exercises and test your understanding.

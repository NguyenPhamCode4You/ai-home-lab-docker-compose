# Day 11: Modern C# Features (C# 7-12)

## 🎯 Learning Objectives

- Master pattern matching evolution (C# 7-11)
- Understand records and init-only properties
- Use nullable reference types effectively
- Leverage global usings and file-scoped namespaces
- Explore raw string literals and required members

---

## 1. Pattern Matching (C# 7.0+)

### Type Pattern (C# 7.0)

```csharp
object obj = "hello";

// Old way
if (obj is string)
{
    string s = (string)obj;
    Console.WriteLine(s.Length);
}

// New way - declare variable
if (obj is string s)
{
    Console.WriteLine(s.Length); // s is in scope
}

// Switch with patterns
switch (obj)
{
    case int i:
        Console.WriteLine($"Integer: {i}");
        break;
    case string s when s.Length > 5:
        Console.WriteLine($"Long string: {s}");
        break;
    case string s:
        Console.WriteLine($"Short string: {s}");
        break;
    case null:
        Console.WriteLine("Null");
        break;
    default:
        Console.WriteLine("Other type");
        break;
}
```

### Switch Expressions (C# 8.0)

```csharp
// Old switch statement
string GetSeasonOld(int month)
{
    switch (month)
    {
        case 12:
        case 1:
        case 2:
            return "Winter";
        case 3:
        case 4:
        case 5:
            return "Spring";
        case 6:
        case 7:
        case 8:
            return "Summer";
        case 9:
        case 10:
        case 11:
            return "Fall";
        default:
            throw new ArgumentException("Invalid month");
    }
}

// New switch expression
string GetSeason(int month) => month switch
{
    12 or 1 or 2 => "Winter",
    >= 3 and <= 5 => "Spring",
    >= 6 and <= 8 => "Summer",
    >= 9 and <= 11 => "Fall",
    _ => throw new ArgumentException("Invalid month")
};
```

### Property Pattern (C# 8.0)

```csharp
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Address Address { get; set; }
}

public class Address
{
    public string City { get; set; }
    public string State { get; set; }
}

// Property pattern
string GetDiscount(Person person) => person switch
{
    { Age: < 18 } => "Youth discount",
    { Age: >= 65 } => "Senior discount",
    { Address: { State: "CA" } } => "CA resident discount",
    { Address.City: "Seattle" } => "Seattle discount",
    _ => "No discount"
};

// Tuple pattern
string Classify(int x, int y) => (x, y) switch
{
    (0, 0) => "Origin",
    (0, _) => "X-axis",
    (_, 0) => "Y-axis",
    (var a, var b) when a == b => "Diagonal",
    _ => "Other"
};
```

### Positional Pattern (C# 8.0)

```csharp
public class Point
{
    public int X { get; }
    public int Y { get; }

    public Point(int x, int y) => (X, Y) = (x, y);

    public void Deconstruct(out int x, out int y) => (x, y) = (X, Y);
}

string Classify(Point point) => point switch
{
    (0, 0) => "Origin",
    (0, _) => "Y-axis",
    (_, 0) => "X-axis",
    var (x, y) when x == y => "Diagonal",
    _ => "Other"
};
```

### Relational and Logical Patterns (C# 9.0)

```csharp
// Relational patterns
string GetTaxRate(decimal income) => income switch
{
    < 10_000 => "0%",
    >= 10_000 and < 50_000 => "10%",
    >= 50_000 and < 100_000 => "20%",
    >= 100_000 => "30%"
};

// Not pattern
if (obj is not null)
{
    // obj is not null
}

// And pattern
if (value is >= 0 and <= 100)
{
    // value is between 0 and 100
}

// Or pattern
if (value is < 0 or > 100)
{
    // value is outside range
}
```

### List Patterns (C# 11.0)

```csharp
int[] numbers = { 1, 2, 3, 4, 5 };

// List patterns
string Describe(int[] array) => array switch
{
    [] => "Empty",
    [1] => "Single one",
    [1, 2] => "One and two",
    [1, .., 5] => "Starts with 1, ends with 5",
    [1, .., var last] => $"Starts with 1, ends with {last}",
    [var first, .. var rest] => $"First: {first}, Rest: {rest.Length}",
    _ => "Other"
};
```

---

## 2. Records (C# 9.0)

### Record Declaration

```csharp
// Record with properties
public record Person(string FirstName, string LastName, int Age);

// Equivalent to:
public record Person
{
    public string FirstName { get; init; }
    public string LastName { get; init; }
    public int Age { get; init; }

    public Person(string firstName, string lastName, int age)
    {
        FirstName = firstName;
        LastName = lastName;
        Age = age;
    }

    // Auto-generated: Equals, GetHashCode, ToString, Deconstruct, With
}

// Usage
Person person = new Person("John", "Doe", 30);
Person person2 = person with { Age = 31 }; // Non-destructive mutation

// Deconstruction
var (firstName, lastName, age) = person;

// Value equality
Person person3 = new Person("John", "Doe", 30);
Console.WriteLine(person == person3); // True (value equality!)
```

### Record Struct (C# 10.0)

```csharp
// Readonly record struct
public readonly record struct Point(int X, int Y);

// Mutable record struct
public record struct MutablePoint(int X, int Y);

MutablePoint p1 = new(1, 2);
p1.X = 10; // Allowed (mutable)

// Record class vs record struct
record class PersonClass(string Name); // Reference type
record struct PersonStruct(string Name); // Value type
```

### Record with Methods

```csharp
public record Person(string FirstName, string LastName)
{
    public string FullName => $"{FirstName} {LastName}";

    public Person WithFullName(string fullName)
    {
        string[] parts = fullName.Split(' ');
        return this with { FirstName = parts[0], LastName = parts[1] };
    }
}
```

---

## 3. Init-Only Properties (C# 9.0)

### Init Accessor

```csharp
public class Person
{
    public string Name { get; init; }
    public int Age { get; init; }
}

// Can set during initialization
Person person = new Person
{
    Name = "John",
    Age = 30
};

// Cannot set after initialization
// person.Name = "Jane"; // Compile error!

// Constructor can still set
public class Person
{
    public string Name { get; init; }

    public Person(string name)
    {
        Name = name; // OK in constructor
    }
}
```

### Required Members (C# 11.0)

```csharp
public class Person
{
    public required string Name { get; init; }
    public required int Age { get; init; }
    public string? Email { get; init; }
}

// Must set required properties
Person person = new Person
{
    Name = "John", // Required
    Age = 30       // Required
    // Email is optional
};

// Compile error if missing required property
// Person invalid = new Person { Name = "John" }; // Error: Age required
```

---

## 4. Nullable Reference Types (C# 8.0)

### Enabling Nullable Context

```csharp
// Enable in .csproj
<PropertyGroup>
  <Nullable>enable</Nullable>
</PropertyGroup>

// Or in code
#nullable enable

// Non-nullable reference type (default)
string name = "John"; // Cannot be null

// Nullable reference type
string? nullableName = null; // Can be null

// Compiler warnings
string? GetName() => null;

string name = GetName(); // Warning: Converting null to non-nullable
```

### Null-Forgiving Operator

```csharp
string? nullableString = GetString();

// Warning: Dereference of a possibly null reference
int length = nullableString.Length;

// Suppress warning (you know it's not null)
int length = nullableString!.Length;

// Better: Check for null
if (nullableString != null)
{
    int length = nullableString.Length; // No warning
}

// Or null-conditional
int? length = nullableString?.Length;
```

### Nullable Annotations

```csharp
public class Person
{
    // Non-nullable - must be initialized
    public string Name { get; set; } = string.Empty;

    // Nullable - can be null
    public string? MiddleName { get; set; }

    // AllowNull - can accept null but never returns null
    [AllowNull]
    public string Email
    {
        get => email;
        set => email = value ?? string.Empty;
    }
    private string email = string.Empty;

    // NotNull - parameter/return value is never null
    [return: NotNull]
    public string? GetNameOrDefault([NotNull] string? name)
    {
        return name ?? "Unknown";
    }
}
```

---

## 5. Global Usings (C# 10.0)

### Global Using Directives

```csharp
// GlobalUsings.cs
global using System;
global using System.Collections.Generic;
global using System.Linq;
global using System.Threading.Tasks;

// Now available in all files
// No need to repeat using directives

// Implicit global usings (enabled by default in .NET 6+)
<PropertyGroup>
  <ImplicitUsings>enable</ImplicitUsings>
</PropertyGroup>

// Adds common usings automatically based on project type
```

### File-Scoped Namespaces (C# 10.0)

```csharp
// Old way
namespace MyApp.Models
{
    public class Person
    {
        public string Name { get; set; }
    }
}

// New way - file-scoped namespace
namespace MyApp.Models;

public class Person
{
    public string Name { get; set; }
}
// No extra indentation!
```

---

## 6. String Improvements

### Raw String Literals (C# 11.0)

```csharp
// Old way - escaped
string json = "{\"name\":\"John\",\"age\":30}";
string path = "C:\\Users\\John\\Documents";

// New way - raw string literal
string json = """{"name":"John","age":30}""";
string path = """C:\Users\John\Documents""";

// Multi-line
string html = """
    <div>
        <h1>Hello</h1>
        <p>World</p>
    </div>
    """;

// With interpolation
int age = 30;
string json = $$"""
    {
        "name": "John",
        "age": {{age}}
    }
    """;

// Multiple $ for nested braces
string template = $$$"""
    {
        "template": "{{value}}",
        "example": {{{age}}}
    }
    """;
```

### UTF-8 String Literals (C# 11.0)

```csharp
// UTF-8 string literal
ReadOnlySpan<byte> utf8 = "Hello"u8;

// Instead of
ReadOnlySpan<byte> utf8 = Encoding.UTF8.GetBytes("Hello");
```

---

## 7. Other Modern Features

### Target-Typed New (C# 9.0)

```csharp
// Old way
Dictionary<string, List<int>> dict = new Dictionary<string, List<int>>();

// New way
Dictionary<string, List<int>> dict = new();

// In initialization
Person person = new() { Name = "John", Age = 30 };

// In return
public Person CreatePerson() => new() { Name = "John", Age = 30 };
```

### Static Abstract Members (C# 11.0)

```csharp
public interface INumber<T> where T : INumber<T>
{
    static abstract T Zero { get; }
    static abstract T operator +(T left, T right);
}

public struct MyNumber : INumber<MyNumber>
{
    public int Value { get; set; }

    public static MyNumber Zero => new() { Value = 0 };

    public static MyNumber operator +(MyNumber left, MyNumber right)
    {
        return new MyNumber { Value = left.Value + right.Value };
    }
}

// Generic math
T Add<T>(T a, T b) where T : INumber<T>
{
    return a + b; // Works for any type implementing INumber<T>
}
```

### Lambda Improvements (C# 10.0-12.0)

```csharp
// Natural type for lambdas (C# 10)
var parse = (string s) => int.Parse(s);

// Attributes on lambdas (C# 10)
var action = [Obsolete] () => Console.WriteLine("Old");

// Default parameters (C# 12)
var greet = (string name = "World") => $"Hello, {name}!";

// Ref returns (C# 12)
var getRef = (ref int x) => ref x;
```

### Primary Constructors (C# 12.0)

```csharp
// Class with primary constructor
public class Person(string name, int age)
{
    public string Name => name;
    public int Age => age;

    public void PrintInfo()
    {
        Console.WriteLine($"{name} is {age} years old");
    }
}

// Usage
Person person = new("John", 30);

// Struct with primary constructor
public struct Point(int x, int y)
{
    public readonly int X = x;
    public readonly int Y = y;

    public readonly double DistanceFromOrigin()
    {
        return Math.Sqrt(x * x + y * y);
    }
}
```

### Collection Expressions (C# 12.0)

```csharp
// Array
int[] numbers = [1, 2, 3, 4, 5];

// List
List<int> list = [1, 2, 3, 4, 5];

// Span
Span<int> span = [1, 2, 3, 4, 5];

// Spread operator
int[] first = [1, 2, 3];
int[] second = [4, 5, 6];
int[] combined = [..first, ..second]; // [1, 2, 3, 4, 5, 6]

// With conditions
int[] numbers = [1, .. (includeTwo ? [2] : []), 3];
```

---

## 8. Interview Questions

### Q1: What are records and when to use them?

**Answer:** Records are reference types with value-based equality, immutability by default (init properties), and built-in with-expressions. Use for DTOs, value objects, immutable data models.

### Q2: Explain nullable reference types

**Answer:** C# 8.0 feature enabling compile-time null-safety for reference types. Reference types are non-nullable by default, use ? for nullable. Helps prevent NullReferenceException at compile time.

### Q3: What is pattern matching?

**Answer:** Feature allowing complex conditional logic based on type, shape, and value of data. Includes type patterns, property patterns, positional patterns, list patterns. Makes code more concise and readable.

### Q4: Difference between record and class?

**Answer:** Records have value-based equality (classes: reference equality), immutability by default, built-in ToString/GetHashCode/Equals, with-expressions for non-destructive mutation, and deconstruction.

### Q5: What are primary constructors?

**Answer:** C# 12 feature allowing constructor parameters directly in class/struct declaration. Parameters are available throughout type, reducing boilerplate code.

---

## 9. Practical Exercises

### Exercise 1: Convert to Modern C#

Refactor old C# code using:

- File-scoped namespaces
- Records
- Pattern matching
- Init properties

### Exercise 2: Nullable Reference Types

Enable nullable reference types in existing project:

- Fix all warnings
- Add appropriate null checks
- Use nullable annotations correctly

### Exercise 3: Pattern Matching

Implement state machine using:

- Switch expressions
- Property patterns
- Guard clauses

### Exercise 4: Records vs Classes

Compare performance and behavior:

- Value equality
- Memory allocation
- Immutability patterns

---

## 10. Key Takeaways

✅ **Pattern matching** simplifies complex conditionals
✅ **Records** for immutable value objects
✅ **Nullable reference types** prevent null errors
✅ **Init properties** for immutability
✅ **Global usings** reduce boilerplate
✅ **Raw strings** for literals with special characters
✅ **Primary constructors** reduce ceremony
✅ **Modern C#** = less code, more clarity

---

## Tomorrow's Preview

**Day 12: Design Patterns & SOLID Principles**

- SOLID principles in depth
- Creational patterns
- Structural patterns
- Behavioral patterns
- Dependency Injection

---

**Modern C# makes code cleaner and safer!** ✨

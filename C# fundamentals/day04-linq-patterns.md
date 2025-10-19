# Day 4: LINQ & Advanced Query Patterns

## 🎯 Learning Objectives

- Understand LINQ internals and deferred execution
- Master query syntax vs method syntax
- Learn IEnumerable vs IQueryable differences
- Create custom LINQ operators
- Optimize LINQ performance

---

## 1. LINQ Fundamentals

### What is LINQ?

Language Integrated Query - unified syntax for querying different data sources.

```csharp
// Query syntax
var query = from person in people
            where person.Age > 18
            orderby person.Name
            select person.Name;

// Method syntax (same query)
var query = people
    .Where(person => person.Age > 18)
    .OrderBy(person => person.Name)
    .Select(person => person.Name);
```

### LINQ Providers

- **LINQ to Objects** - In-memory collections (IEnumerable<T>)
- **LINQ to SQL / Entity Framework** - Database queries (IQueryable<T>)
- **LINQ to XML** - XML documents (XDocument, XElement)
- **LINQ to Entities** - Entity Framework Core
- **Parallel LINQ (PLINQ)** - Parallel processing

---

## 2. Deferred Execution

### Deferred vs Immediate Execution

```csharp
List<int> numbers = new() { 1, 2, 3, 4, 5 };

// Deferred execution - query not executed yet
IEnumerable<int> query = numbers.Where(x => x > 2);

numbers.Add(6); // Add more data

// Executed when enumerated
foreach (int n in query) // Executes NOW
{
    Console.WriteLine(n); // 3, 4, 5, 6 (includes 6!)
}

// Immediate execution - executes immediately
List<int> result = numbers.Where(x => x > 2).ToList();

numbers.Add(7); // This won't be in result

Console.WriteLine(result.Count); // 4 (doesn't include 7)
```

### Query Re-execution

```csharp
List<int> numbers = new() { 1, 2, 3 };
var query = numbers.Where(x => x > 1);

// First enumeration
foreach (int n in query)
{
    Console.WriteLine(n); // 2, 3
}

numbers.Add(4);

// Second enumeration - query re-executed!
foreach (int n in query)
{
    Console.WriteLine(n); // 2, 3, 4
}
```

### When Execution Happens

```csharp
// Deferred: Where, Select, OrderBy, GroupBy, Join, etc.
var deferred = numbers.Where(x => x > 2); // Not executed

// Immediate: ToList, ToArray, ToDictionary, Count, First, Single, etc.
var immediate = numbers.Where(x => x > 2).ToList(); // Executed immediately
int count = numbers.Count(x => x > 2); // Executed immediately
int first = numbers.First(x => x > 2); // Executed immediately
```

---

## 3. IEnumerable<T> vs IQueryable<T>

### IEnumerable<T>

In-memory queries, executed on the client.

```csharp
public interface IEnumerable<T> : IEnumerable
{
    IEnumerator<T> GetEnumerator();
}

// Example
List<Person> people = GetPeople(); // In memory
IEnumerable<Person> adults = people.Where(p => p.Age > 18);

// Where is: Func<Person, bool>
// Executes in C# on loaded data
```

### IQueryable<T>

Database queries, executed on the server.

```csharp
public interface IQueryable<T> : IEnumerable<T>, IQueryable
{
    Type ElementType { get; }
    Expression Expression { get; }
    IQueryProvider Provider { get; }
}

// Example
IQueryable<Person> people = dbContext.Persons; // Not loaded yet
IQueryable<Person> adults = people.Where(p => p.Age > 18);

// Where is: Expression<Func<Person, bool>>
// Translated to SQL and executed on database
```

### Key Differences

```csharp
// IEnumerable - Loads all data, then filters in memory
IEnumerable<Person> people = dbContext.Persons.AsEnumerable();
var adults = people.Where(p => p.Age > 18); // Filters in C#
// SQL: SELECT * FROM Persons (all records!)
// Then filters in memory

// IQueryable - Filters on database
IQueryable<Person> people = dbContext.Persons;
var adults = people.Where(p => p.Age > 18); // Translates to SQL
// SQL: SELECT * FROM Persons WHERE Age > 18

// ⚠️ Mixing IEnumerable and IQueryable
var query = dbContext.Persons // IQueryable
    .AsEnumerable() // Converts to IEnumerable - loads all data!
    .Where(p => p.Age > 18); // Filters in memory
// BAD: Loads entire table!

// ✅ GOOD: Keep IQueryable until the end
var query = dbContext.Persons // IQueryable
    .Where(p => p.Age > 18) // Still IQueryable
    .OrderBy(p => p.Name) // Still IQueryable
    .ToList(); // Executes query, returns List<Person>
```

---

## 4. Standard Query Operators

### Filtering

```csharp
// Where - filter elements
var adults = people.Where(p => p.Age >= 18);

// OfType - filter by type
object[] mixed = { 1, "hello", 2, "world", 3 };
var numbers = mixed.OfType<int>(); // { 1, 2, 3 }
var strings = mixed.OfType<string>(); // { "hello", "world" }
```

### Projection

```csharp
// Select - transform elements
var names = people.Select(p => p.Name);

// SelectMany - flatten nested collections
var allPhones = people.SelectMany(p => p.PhoneNumbers);

// Example: Get all phone numbers from all people
class Person
{
    public string Name { get; set; }
    public List<string> PhoneNumbers { get; set; }
}

List<Person> people = new()
{
    new() { Name = "Alice", PhoneNumbers = new() { "111", "222" } },
    new() { Name = "Bob", PhoneNumbers = new() { "333" } }
};

var phones = people.SelectMany(p => p.PhoneNumbers);
// Result: { "111", "222", "333" }

// With index
var indexed = people.Select((p, index) => new { Index = index, Name = p.Name });
```

### Sorting

```csharp
// OrderBy, OrderByDescending
var sorted = people.OrderBy(p => p.Age);
var descending = people.OrderByDescending(p => p.Age);

// ThenBy - secondary sort
var sorted = people
    .OrderBy(p => p.LastName)
    .ThenBy(p => p.FirstName);

// Reverse
var reversed = people.Reverse();
```

### Grouping

```csharp
// GroupBy - group by key
var grouped = people.GroupBy(p => p.City);

foreach (var group in grouped)
{
    Console.WriteLine($"City: {group.Key}");
    foreach (var person in group)
    {
        Console.WriteLine($"  {person.Name}");
    }
}

// GroupBy with result selector
var cityCounts = people.GroupBy(
    p => p.City,
    (city, persons) => new { City = city, Count = persons.Count() }
);
```

### Joining

```csharp
class Person { public int Id { get; set; } public string Name { get; set; } }
class Order { public int PersonId { get; set; } public string Product { get; set; } }

List<Person> people = new()
{
    new() { Id = 1, Name = "Alice" },
    new() { Id = 2, Name = "Bob" }
};

List<Order> orders = new()
{
    new() { PersonId = 1, Product = "Laptop" },
    new() { PersonId = 1, Product = "Mouse" },
    new() { PersonId = 2, Product = "Keyboard" }
};

// Inner join
var query = people.Join(
    orders,
    person => person.Id,
    order => order.PersonId,
    (person, order) => new { person.Name, order.Product }
);
// Result: { Alice, Laptop }, { Alice, Mouse }, { Bob, Keyboard }

// Group join (left join)
var groupJoin = people.GroupJoin(
    orders,
    person => person.Id,
    order => order.PersonId,
    (person, personOrders) => new
    {
        Person = person.Name,
        Orders = personOrders.Select(o => o.Product).ToList()
    }
);
```

### Set Operations

```csharp
int[] numbers1 = { 1, 2, 3, 4, 5 };
int[] numbers2 = { 3, 4, 5, 6, 7 };

// Union - all unique elements
var union = numbers1.Union(numbers2); // 1,2,3,4,5,6,7

// Intersect - common elements
var intersect = numbers1.Intersect(numbers2); // 3,4,5

// Except - elements in first but not second
var except = numbers1.Except(numbers2); // 1,2

// Distinct - remove duplicates
int[] duplicates = { 1, 2, 2, 3, 3, 3 };
var unique = duplicates.Distinct(); // 1,2,3

// DistinctBy (C# 10+)
var distinctPeople = people.DistinctBy(p => p.Name);
```

### Aggregation

```csharp
int[] numbers = { 1, 2, 3, 4, 5 };

// Count, Sum, Average, Min, Max
int count = numbers.Count(); // 5
int sum = numbers.Sum(); // 15
double avg = numbers.Average(); // 3.0
int min = numbers.Min(); // 1
int max = numbers.Max(); // 5

// Aggregate - custom aggregation
int product = numbers.Aggregate((a, b) => a * b); // 120
string text = new[] { "Hello", "World" }.Aggregate((a, b) => a + " " + b);

// Aggregate with seed
int sumFrom10 = numbers.Aggregate(10, (acc, n) => acc + n); // 25
```

### Quantifiers

```csharp
int[] numbers = { 1, 2, 3, 4, 5 };

// Any - at least one matches
bool hasEven = numbers.Any(n => n % 2 == 0); // true

// All - all match
bool allPositive = numbers.All(n => n > 0); // true

// Contains
bool hasThree = numbers.Contains(3); // true
```

### Element Operators

```csharp
int[] numbers = { 1, 2, 3, 4, 5 };

// First - first element (exception if empty)
int first = numbers.First(); // 1
int firstEven = numbers.First(n => n % 2 == 0); // 2

// FirstOrDefault - first or default (no exception)
int firstOrDefault = numbers.FirstOrDefault(n => n > 10); // 0 (default)

// Single - exactly one element (exception if 0 or >1)
int[] single = { 42 };
int value = single.Single(); // 42

// SingleOrDefault - exactly one or default
int singleOrDefault = numbers.SingleOrDefault(n => n > 10); // 0

// Last, LastOrDefault
int last = numbers.Last(); // 5

// ElementAt, ElementAtOrDefault
int third = numbers.ElementAt(2); // 3
```

---

## 5. Query Syntax vs Method Syntax

### Query Syntax

```csharp
var query = from person in people
            where person.Age > 18
            orderby person.Name
            select new { person.Name, person.Age };
```

### Method Syntax (Equivalent)

```csharp
var query = people
    .Where(person => person.Age > 18)
    .OrderBy(person => person.Name)
    .Select(person => new { person.Name, person.Age });
```

### Complex Query Comparison

```csharp
// Query syntax
var query1 = from person in people
             join order in orders on person.Id equals order.PersonId
             where order.Amount > 100
             group order by person.Name into personOrders
             select new
             {
                 Name = personOrders.Key,
                 TotalAmount = personOrders.Sum(o => o.Amount)
             };

// Method syntax
var query2 = people
    .Join(orders,
          person => person.Id,
          order => order.PersonId,
          (person, order) => new { person, order })
    .Where(x => x.order.Amount > 100)
    .GroupBy(x => x.person.Name)
    .Select(g => new
    {
        Name = g.Key,
        TotalAmount = g.Sum(x => x.order.Amount)
    });
```

### When to Use Each

- **Query syntax:** Complex joins and grouping (more readable)
- **Method syntax:** Simple queries, chaining, better IntelliSense

---

## 6. Custom LINQ Operators

### Extension Methods

```csharp
public static class LinqExtensions
{
    // ForEach operator
    public static void ForEach<T>(this IEnumerable<T> source, Action<T> action)
    {
        foreach (T item in source)
        {
            action(item);
        }
    }

    // Batch operator - split into batches
    public static IEnumerable<IEnumerable<T>> Batch<T>(
        this IEnumerable<T> source, int size)
    {
        T[] batch = null;
        int count = 0;

        foreach (T item in source)
        {
            if (batch == null)
                batch = new T[size];

            batch[count++] = item;

            if (count == size)
            {
                yield return batch;
                batch = null;
                count = 0;
            }
        }

        if (batch != null && count > 0)
            yield return batch.Take(count);
    }

    // WhereNot - inverse of Where
    public static IEnumerable<T> WhereNot<T>(
        this IEnumerable<T> source, Func<T, bool> predicate)
    {
        return source.Where(x => !predicate(x));
    }

    // TakeUntil - take until condition met
    public static IEnumerable<T> TakeUntil<T>(
        this IEnumerable<T> source, Func<T, bool> predicate)
    {
        foreach (T item in source)
        {
            yield return item;
            if (predicate(item))
                break;
        }
    }

    // MaxBy - C# 6+ version
    public static T MaxBy<T, TKey>(
        this IEnumerable<T> source,
        Func<T, TKey> selector) where TKey : IComparable<TKey>
    {
        return source.OrderByDescending(selector).First();
    }
}

// Usage
numbers.ForEach(n => Console.WriteLine(n));
var batches = numbers.Batch(10);
var filtered = numbers.WhereNot(n => n % 2 == 0);
```

---

## 7. Performance Optimization

### Avoid Multiple Enumeration

```csharp
// ❌ BAD - Multiple enumeration
var query = people.Where(p => p.Age > 18);
int count = query.Count(); // Enumerates
var list = query.ToList(); // Enumerates again!

// ✅ GOOD - Single enumeration
var list = people.Where(p => p.Age > 18).ToList();
int count = list.Count;
```

### Avoid Unnecessary ToList()

```csharp
// ❌ BAD - Unnecessary materialization
var adults = people.Where(p => p.Age > 18).ToList();
var names = adults.Select(p => p.Name).ToList();
var sorted = names.OrderBy(n => n).ToList();

// ✅ GOOD - Defer until needed
var sorted = people
    .Where(p => p.Age > 18)
    .Select(p => p.Name)
    .OrderBy(n => n)
    .ToList(); // Materialize once at the end
```

### Use Any() instead of Count()

```csharp
// ❌ BAD - Enumerates entire sequence
if (people.Where(p => p.Age > 18).Count() > 0)
{
    // ...
}

// ✅ GOOD - Stops at first match
if (people.Any(p => p.Age > 18))
{
    // ...
}
```

### Use FirstOrDefault() instead of Where().FirstOrDefault()

```csharp
// ❌ BAD - Creates intermediate collection
var person = people.Where(p => p.Id == 123).FirstOrDefault();

// ✅ GOOD - Stops at first match
var person = people.FirstOrDefault(p => p.Id == 123);
```

### Avoid Closures in LINQ

```csharp
// ❌ BAD - Closure created for each iteration
for (int i = 0; i < 10; i++)
{
    var query = numbers.Where(n => n > i); // Captures 'i'
}

// ✅ GOOD - Extract predicate outside loop
Func<int, int, bool> greaterThan = (n, threshold) => n > threshold;
for (int i = 0; i < 10; i++)
{
    int threshold = i;
    var query = numbers.Where(n => greaterThan(n, threshold));
}
```

### Parallel LINQ (PLINQ)

```csharp
// Sequential
var result = numbers
    .Where(n => IsExpensiveCheck(n))
    .Select(n => ExpensiveTransform(n))
    .ToList();

// Parallel
var result = numbers
    .AsParallel()
    .Where(n => IsExpensiveCheck(n))
    .Select(n => ExpensiveTransform(n))
    .ToList();

// Control parallelism
var result = numbers
    .AsParallel()
    .WithDegreeOfParallelism(4) // Max 4 threads
    .WithExecutionMode(ParallelExecutionMode.ForceParallelism)
    .Where(n => IsExpensiveCheck(n))
    .ToList();

// Preserve order
var result = numbers
    .AsParallel()
    .AsOrdered() // Maintain order (slower)
    .Select(n => ExpensiveTransform(n))
    .ToList();
```

---

## 8. Common Pitfalls

### Pitfall 1: Modifying Collection During Enumeration

```csharp
// ❌ THROWS InvalidOperationException
List<int> numbers = new() { 1, 2, 3, 4, 5 };
foreach (int n in numbers)
{
    if (n % 2 == 0)
        numbers.Remove(n); // Exception!
}

// ✅ FIX - Create new list
numbers = numbers.Where(n => n % 2 != 0).ToList();

// ✅ FIX - Use ToList() to snapshot
foreach (int n in numbers.ToList())
{
    if (n % 2 == 0)
        numbers.Remove(n);
}
```

### Pitfall 2: Null Reference in Query

```csharp
// ❌ Potential NullReferenceException
var names = people.Select(p => p.Address.City);

// ✅ FIX - Null-conditional operator
var names = people.Select(p => p.Address?.City);

// ✅ FIX - Where clause
var names = people
    .Where(p => p.Address != null)
    .Select(p => p.Address.City);
```

### Pitfall 3: Mixing IQueryable and IEnumerable

```csharp
// ❌ BAD - Loads all data before filtering
var query = dbContext.Persons
    .AsEnumerable() // Converts to IEnumerable - executes query!
    .Where(p => p.Age > 18); // Filters in memory

// ✅ GOOD - Keep IQueryable
var query = dbContext.Persons
    .Where(p => p.Age > 18) // Translated to SQL
    .AsEnumerable(); // Convert only at the end if needed
```

---

## 9. Interview Questions

### Q1: What is deferred execution?

**Answer:** Query is not executed when defined, but when enumerated (foreach, ToList, Count, etc.). Allows query to see latest data and enables query composition. Exception: Aggregation methods execute immediately.

### Q2: Difference between IEnumerable and IQueryable?

**Answer:**

- **IEnumerable<T>:** LINQ to Objects, Func delegates, executes in memory (client-side)
- **IQueryable<T>:** LINQ to SQL/EF, Expression trees, translates to SQL (server-side)

### Q3: Why use Any() instead of Count() > 0?

**Answer:** Any() stops enumeration at first match (O(1) best case). Count() enumerates entire sequence (O(n) always). For large collections or database queries, Any() is much more efficient.

### Q4: When does a LINQ query execute?

**Answer:**

- **Deferred operators:** When enumerated (Where, Select, OrderBy, GroupBy)
- **Immediate operators:** Immediately (ToList, ToArray, Count, First, Single, Sum)

### Q5: How to optimize LINQ queries?

**Answer:**

- Avoid multiple enumeration (materialize once with ToList())
- Use Any() instead of Count() > 0
- Use FirstOrDefault() with predicate instead of Where().First()
- Keep IQueryable as long as possible for database queries
- Use AsParallel() for CPU-intensive operations on large collections

---

## 10. Practical Exercises

### Exercise 1: Build a Query Builder

Create a fluent API for building dynamic queries with multiple optional filters.

### Exercise 2: Implement Custom LINQ Operators

- DistinctBy (pre-C# 10)
- MaxBy / MinBy (pre-C# 9)
- Batch
- Window (sliding window)

### Exercise 3: Optimize a Slow Query

Given inefficient LINQ code, identify and fix performance issues.

### Exercise 4: PLINQ Performance Analysis

Compare sequential vs parallel LINQ for different scenarios and measure speedup.

---

## 11. Key Takeaways

✅ **Deferred execution** delays query until enumeration
✅ **IQueryable** translates to SQL; **IEnumerable** executes in memory
✅ **Avoid multiple enumeration** - materialize once when needed
✅ **Use Any() over Count()** for existence checks
✅ **Custom operators** extend LINQ with extension methods
✅ **PLINQ** parallelizes operations but has overhead
✅ **Keep IQueryable** until the end for database queries

---

## Tomorrow's Preview

**Day 5: Generics & Constraints**

- Generic type parameters and constraints
- Covariance and contravariance
- Generic methods vs generic types
- Performance benefits
- Common generic patterns

---

**LINQ is powerful - master it for elegant, efficient code!** 💪

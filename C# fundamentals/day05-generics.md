# Day 5: Generics & Constraints

## 🎯 Learning Objectives

- Master generic type parameters and constraints
- Understand covariance and contravariance
- Learn generic methods vs generic types
- Explore performance benefits of generics
- Study common generic patterns

---

## 1. Generic Fundamentals

### Why Generics?

Before generics (C# 1.0):

```csharp
// ❌ ArrayList - requires boxing and casting
ArrayList list = new ArrayList();
list.Add(1); // Boxing int to object
list.Add("hello"); // Type safety issue!
int value = (int)list[0]; // Unboxing and casting
string text = (string)list[1]; // Runtime type checking
```

With generics (C# 2.0+):

```csharp
// ✅ List<T> - type-safe, no boxing
List<int> numbers = new List<int>();
numbers.Add(1); // No boxing
// numbers.Add("hello"); // Compile error!
int value = numbers[0]; // No casting
```

### Generic Classes

```csharp
// Generic class with one type parameter
public class Container<T>
{
    private T value;

    public Container(T value)
    {
        this.value = value;
    }

    public T GetValue() => value;
    public void SetValue(T value) => this.value = value;
}

// Usage
Container<int> intContainer = new Container<int>(42);
Container<string> stringContainer = new Container<string>("Hello");

// C# 9.0+ target-typed new
Container<int> container = new(42);
```

### Generic Methods

```csharp
// Generic method
public T Max<T>(T a, T b) where T : IComparable<T>
{
    return a.CompareTo(b) > 0 ? a : b;
}

// Type inference
int max = Max(5, 10); // Type inferred as int
string maxStr = Max("apple", "banana"); // Type inferred as string

// Explicit type arguments
int max2 = Max<int>(5, 10);
```

### Multiple Type Parameters

```csharp
public class Pair<TFirst, TSecond>
{
    public TFirst First { get; set; }
    public TSecond Second { get; set; }

    public Pair(TFirst first, TSecond second)
    {
        First = first;
        Second = second;
    }
}

// Usage
var pair = new Pair<int, string>(1, "One");
var coordinates = new Pair<double, double>(10.5, 20.3);
```

---

## 2. Generic Constraints

### Where Clauses

```csharp
// Struct constraint - T must be value type
public class ValueContainer<T> where T : struct
{
    private T value;
    // Can only use with int, double, DateTime, custom structs, etc.
}

// Class constraint - T must be reference type
public class ReferenceContainer<T> where T : class
{
    private T value;
    // Can use with string, object, custom classes, etc.
}

// Constructor constraint - T must have parameterless constructor
public class Factory<T> where T : new()
{
    public T Create()
    {
        return new T(); // Requires parameterless constructor
    }
}

// Base class constraint
public class Repository<T> where T : Entity
{
    public void Save(T entity)
    {
        // Can access Entity members
        entity.Id = Guid.NewGuid();
    }
}

// Interface constraint
public class Sorter<T> where T : IComparable<T>
{
    public T[] Sort(T[] array)
    {
        Array.Sort(array); // Requires IComparable
        return array;
    }
}

// Multiple constraints
public class Manager<T> where T : Entity, IValidatable, new()
{
    public T CreateAndValidate()
    {
        T entity = new T(); // new() constraint
        entity.Id = Guid.NewGuid(); // Entity constraint
        entity.Validate(); // IValidatable constraint
        return entity;
    }
}
```

### Constraint Combinations

```csharp
// Multiple type parameters with different constraints
public class Cache<TKey, TValue>
    where TKey : notnull
    where TValue : class, new()
{
    private Dictionary<TKey, TValue> cache = new();

    public TValue GetOrCreate(TKey key)
    {
        if (!cache.TryGetValue(key, out TValue value))
        {
            value = new TValue();
            cache[key] = value;
        }
        return value;
    }
}
```

### Unmanaged Constraint (C# 7.3+)

```csharp
// T must be unmanaged type (no references)
public class UnsafeBuffer<T> where T : unmanaged
{
    private T[] buffer;

    public unsafe void ProcessWithPointer()
    {
        fixed (T* ptr = buffer)
        {
            // Can use pointers with unmanaged types
        }
    }
}

// Valid: int, double, structs with only unmanaged fields
UnsafeBuffer<int> intBuffer = new();
UnsafeBuffer<Point> pointBuffer = new(); // If Point has only int fields

// Invalid: string, object, any type with references
// UnsafeBuffer<string> stringBuffer = new(); // Compile error
```

### Notnull Constraint (C# 8.0+)

```csharp
// T must be non-nullable type
public class NotNullContainer<T> where T : notnull
{
    public void Process(T value)
    {
        // value cannot be null
        Console.WriteLine(value.GetHashCode()); // Safe
    }
}
```

---

## 3. Covariance and Contravariance

### Covariance (out keyword)

More derived type can be assigned to less derived type.

```csharp
// Covariant interface
public interface IReadOnlyRepository<out T>
{
    T Get(int id);
    IEnumerable<T> GetAll(); // Covariant return types
    // void Add(T item); // ERROR: T in input position
}

// Implementation
public class AnimalRepository : IReadOnlyRepository<Animal> { }
public class DogRepository : IReadOnlyRepository<Dog> { }

// Covariance in action
IReadOnlyRepository<Dog> dogRepo = new DogRepository();
IReadOnlyRepository<Animal> animalRepo = dogRepo; // Valid!
// Can assign Dog repository to Animal repository

Animal animal = animalRepo.Get(1); // Returns Dog, but typed as Animal
```

### Contravariance (in keyword)

Less derived type can be assigned to more derived type.

```csharp
// Contravariant interface
public interface IWriter<in T>
{
    void Write(T item); // Contravariant parameter
    // T Read(); // ERROR: T in output position
}

// Implementation
public class AnimalWriter : IWriter<Animal> { }

// Contravariance in action
IWriter<Animal> animalWriter = new AnimalWriter();
IWriter<Dog> dogWriter = animalWriter; // Valid!
// Can assign Animal writer to Dog writer

dogWriter.Write(new Dog()); // Works - Dog is an Animal
```

### Built-in Variance Examples

```csharp
// IEnumerable<out T> - covariant
IEnumerable<Dog> dogs = new List<Dog>();
IEnumerable<Animal> animals = dogs; // Valid

// IComparer<in T> - contravariant
IComparer<Animal> animalComparer = /* ... */;
IComparer<Dog> dogComparer = animalComparer; // Valid

// Func<out TResult> - covariant result
Func<Dog> dogFactory = () => new Dog();
Func<Animal> animalFactory = dogFactory; // Valid

// Action<in T> - contravariant parameter
Action<Animal> animalAction = (a) => Console.WriteLine(a);
Action<Dog> dogAction = animalAction; // Valid
```

### Variance Rules

```csharp
// ✅ VALID Covariance (out)
public interface IProducer<out T>
{
    T Produce();
    IEnumerable<T> ProduceMany();
}

// ❌ INVALID Covariance
public interface IInvalidProducer<out T>
{
    void Consume(T item); // ERROR: T in input position
    T Property { get; set; } // ERROR: setter uses T in input position
}

// ✅ VALID Contravariance (in)
public interface IConsumer<in T>
{
    void Consume(T item);
}

// ❌ INVALID Contravariance
public interface IInvalidConsumer<in T>
{
    T Produce(); // ERROR: T in output position
    T Property { get; } // ERROR: getter uses T in output position
}
```

---

## 4. Generic Performance

### No Boxing

```csharp
// ❌ ArrayList - Boxing value types
ArrayList list = new ArrayList();
for (int i = 0; i < 1000; i++)
{
    list.Add(i); // Boxes each int (1000 heap allocations!)
}

// ✅ List<T> - No boxing
List<int> list = new List<int>();
for (int i = 0; i < 1000; i++)
{
    list.Add(i); // No boxing!
}
```

### Type Safety

```csharp
// ❌ ArrayList - Runtime errors
ArrayList list = new ArrayList();
list.Add(1);
list.Add("hello");
int value = (int)list[1]; // InvalidCastException at runtime!

// ✅ List<T> - Compile-time safety
List<int> list = new List<int>();
list.Add(1);
// list.Add("hello"); // Compile error!
int value = list[0]; // Type-safe
```

### JIT Optimization

```csharp
// Generic types are JIT-compiled per unique type combination
List<int> intList; // One JIT compilation
List<string> stringList; // Another JIT compilation
List<int> anotherIntList; // Reuses same code as intList

// Reference types share code
List<string> list1;
List<object> list2;
List<Person> list3;
// All reference types share the same compiled code
```

---

## 5. Common Generic Patterns

### Repository Pattern

```csharp
public interface IRepository<T> where T : class
{
    T GetById(int id);
    IEnumerable<T> GetAll();
    void Add(T entity);
    void Update(T entity);
    void Delete(int id);
}

public class Repository<T> : IRepository<T> where T : class
{
    private readonly DbContext context;
    private readonly DbSet<T> dbSet;

    public Repository(DbContext context)
    {
        this.context = context;
        this.dbSet = context.Set<T>();
    }

    public T GetById(int id) => dbSet.Find(id);
    public IEnumerable<T> GetAll() => dbSet.ToList();
    public void Add(T entity) => dbSet.Add(entity);
    public void Update(T entity) => context.Entry(entity).State = EntityState.Modified;
    public void Delete(int id)
    {
        T entity = dbSet.Find(id);
        if (entity != null)
            dbSet.Remove(entity);
    }
}
```

### Factory Pattern

```csharp
public interface IFactory<T>
{
    T Create();
}

public class SimpleFactory<T> : IFactory<T> where T : new()
{
    public T Create()
    {
        return new T();
    }
}

public class ConfigurableFactory<T> : IFactory<T> where T : class
{
    private readonly Func<T> creator;

    public ConfigurableFactory(Func<T> creator)
    {
        this.creator = creator;
    }

    public T Create()
    {
        return creator();
    }
}
```

### Builder Pattern

```csharp
public class Builder<T> where T : class, new()
{
    private T instance = new T();

    public Builder<T> With(Action<T> action)
    {
        action(instance);
        return this;
    }

    public T Build()
    {
        return instance;
    }
}

// Usage
var person = new Builder<Person>()
    .With(p => p.Name = "John")
    .With(p => p.Age = 30)
    .With(p => p.Email = "john@example.com")
    .Build();
```

### Option/Maybe Pattern

```csharp
public struct Option<T>
{
    private readonly T value;
    private readonly bool hasValue;

    private Option(T value)
    {
        this.value = value;
        this.hasValue = true;
    }

    public static Option<T> Some(T value) => new Option<T>(value);
    public static Option<T> None() => default;

    public bool IsSome => hasValue;
    public bool IsNone => !hasValue;

    public T Value => hasValue ? value : throw new InvalidOperationException("No value");

    public T ValueOr(T defaultValue) => hasValue ? value : defaultValue;

    public Option<TResult> Map<TResult>(Func<T, TResult> mapper)
    {
        return hasValue ? Option<TResult>.Some(mapper(value)) : Option<TResult>.None();
    }

    public Option<TResult> Bind<TResult>(Func<T, Option<TResult>> binder)
    {
        return hasValue ? binder(value) : Option<TResult>.None();
    }
}

// Usage
Option<int> some = Option<int>.Some(42);
Option<int> none = Option<int>.None();

int value = some.ValueOr(0); // 42
int value2 = none.ValueOr(0); // 0

Option<string> mapped = some.Map(x => x.ToString()); // Some("42")
Option<string> mappedNone = none.Map(x => x.ToString()); // None
```

### Result Pattern

```csharp
public class Result<T, TError>
{
    private readonly T value;
    private readonly TError error;
    private readonly bool isSuccess;

    private Result(T value)
    {
        this.value = value;
        this.isSuccess = true;
    }

    private Result(TError error)
    {
        this.error = error;
        this.isSuccess = false;
    }

    public static Result<T, TError> Success(T value) => new Result<T, TError>(value);
    public static Result<T, TError> Failure(TError error) => new Result<T, TError>(error);

    public bool IsSuccess => isSuccess;
    public bool IsFailure => !isSuccess;

    public T Value => isSuccess ? value : throw new InvalidOperationException();
    public TError Error => !isSuccess ? error : throw new InvalidOperationException();

    public Result<TResult, TError> Map<TResult>(Func<T, TResult> mapper)
    {
        return isSuccess
            ? Result<TResult, TError>.Success(mapper(value))
            : Result<TResult, TError>.Failure(error);
    }

    public TResult Match<TResult>(Func<T, TResult> success, Func<TError, TResult> failure)
    {
        return isSuccess ? success(value) : failure(error);
    }
}

// Usage
Result<int, string> DivideResult(int a, int b)
{
    if (b == 0)
        return Result<int, string>.Failure("Division by zero");
    return Result<int, string>.Success(a / b);
}

var result = Divide(10, 2);
string message = result.Match(
    success: value => $"Result: {value}",
    failure: error => $"Error: {error}"
);
```

---

## 6. Advanced Generic Techniques

### Recursive Generics

```csharp
// Fluent API with proper return type
public abstract class FluentBuilder<TSelf> where TSelf : FluentBuilder<TSelf>
{
    public TSelf SetName(string name)
    {
        // Set name
        return (TSelf)this;
    }
}

public class PersonBuilder : FluentBuilder<PersonBuilder>
{
    public PersonBuilder SetAge(int age)
    {
        // Set age
        return this;
    }
}

// Chaining works correctly
var builder = new PersonBuilder()
    .SetName("John") // Returns PersonBuilder
    .SetAge(30);     // Returns PersonBuilder
```

### Generic Constraints with Type Parameters

```csharp
// Ensure TKey can be used as dictionary key
public class Cache<TKey, TValue> where TKey : notnull
{
    private Dictionary<TKey, TValue> dictionary = new();
}

// Ensure TValue can be compared with TKey
public class Indexer<TKey, TValue>
    where TKey : IComparable<TKey>
    where TValue : IComparable<TKey>
{
    public bool IsMatch(TKey key, TValue value)
    {
        return value.CompareTo(key) == 0;
    }
}
```

### Default Generic Values

```csharp
public class Initializer<T>
{
    public T GetDefault()
    {
        return default(T);
        // default(T) returns:
        // - null for reference types
        // - 0 for numeric types
        // - false for bool
        // - default constructor for structs
    }

    public T[] CreateArray(int size)
    {
        T[] array = new T[size];
        // Array elements initialized to default(T)
        return array;
    }
}
```

---

## 7. Interview Questions

### Q1: What problem do generics solve?

**Answer:** Generics provide:

1. **Type safety** - Compile-time type checking
2. **Performance** - No boxing/unboxing for value types
3. **Code reuse** - Single implementation works with multiple types
4. **Cleaner code** - No casting required

### Q2: Explain covariance and contravariance

**Answer:**

- **Covariance (out):** Can assign more derived to less derived. Used for output (return values). Example: IEnumerable<Dog> to IEnumerable<Animal>
- **Contravariance (in):** Can assign less derived to more derived. Used for input (parameters). Example: IComparer<Animal> to IComparer<Dog>

### Q3: What constraints can you apply to generic types?

**Answer:**

- `where T : struct` - Value type
- `where T : class` - Reference type
- `where T : new()` - Parameterless constructor
- `where T : BaseClass` - Base class
- `where T : Interface` - Interface
- `where T : unmanaged` - Unmanaged type
- `where T : notnull` - Non-nullable

### Q4: Why are generics faster than using object?

**Answer:**

1. **No boxing** for value types (no heap allocation)
2. **No casting** (compiler knows exact type)
3. **JIT optimization** (specialized code per type)
4. **Better cache locality** (value types stored inline)

### Q5: Can you have a generic constraint on another generic parameter?

**Answer:** Yes! Example:

```csharp
public class Converter<TSource, TTarget>
    where TTarget : TSource // TTarget must inherit from TSource
{
}
```

---

## 8. Practical Exercises

### Exercise 1: Generic Stack Implementation

Implement a generic Stack<T> with:

- Push, Pop, Peek operations
- Count property
- IsEmpty check
- Enumeration support

### Exercise 2: Generic Repository with Specifications

Create a repository pattern with:

- Generic specification pattern
- Fluent query building
- Covariant read operations

### Exercise 3: Result/Either Monad

Implement a full Result<T, TError> type with:

- Map, Bind, Match methods
- Async versions
- LINQ query syntax support

### Exercise 4: Type-Safe Builder Pattern

Create a fluent builder using recursive generics that ensures:

- Compile-time validation of required properties
- Strong typing throughout the chain
- Immutable final result

---

## 9. Key Takeaways

✅ **Generics** provide type safety and performance
✅ **Constraints** limit and enable type capabilities
✅ **Covariance (out)** for return types
✅ **Contravariance (in)** for parameters
✅ **No boxing** for value types improves performance
✅ **Common patterns** like Repository, Factory, Option, Result
✅ **JIT optimization** creates specialized code per type

---

## Tomorrow's Preview

**Day 6: Exception Handling & Best Practices**

- Exception handling internals
- Try-catch-finally mechanics
- Custom exceptions
- Exception filters
- Async exception handling
- Performance considerations

---

**Generics are the foundation of modern C# - master them!** 🎯

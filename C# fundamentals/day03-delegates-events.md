# Day 3: Delegates, Events & Functional Programming

## 🎯 Learning Objectives

- Master delegate internals and invocation lists
- Understand events and the event pattern
- Learn Func, Action, and Predicate delegates
- Deep dive into lambda expressions and closures
- Explore expression trees fundamentals

---

## 1. Delegates Fundamentals

### What is a Delegate?

A delegate is a type-safe function pointer - a reference to a method.

```csharp
// Delegate declaration
public delegate int MathOperation(int x, int y);

// Methods matching the signature
public int Add(int x, int y) => x + y;
public int Subtract(int x, int y) => x - y;

// Usage
MathOperation operation = Add;
int result = operation(5, 3); // 8

operation = Subtract;
result = operation(5, 3); // 2
```

### Delegate Internals

```csharp
// What the compiler generates:
public sealed class MathOperation : System.MulticastDelegate
{
    public MathOperation(object target, IntPtr method);
    public int Invoke(int x, int y);
    public IAsyncResult BeginInvoke(int x, int y, AsyncCallback callback, object state);
    public int EndInvoke(IAsyncResult result);
}

// Each delegate instance contains:
// - Target: The object instance (null for static methods)
// - Method: Pointer to the method
// - InvocationList: Chain of delegates (for multicast)
```

### Multicast Delegates

```csharp
public delegate void Logger(string message);

void LogToConsole(string message) => Console.WriteLine($"Console: {message}");
void LogToFile(string message) => File.AppendAllText("log.txt", $"{message}\n");

// Combine delegates
Logger logger = LogToConsole;
logger += LogToFile; // Multicast delegate

logger("Hello"); // Calls BOTH methods

// Remove delegate
logger -= LogToConsole;
logger("World"); // Only calls LogToFile

// Get invocation list
Delegate[] delegates = logger.GetInvocationList();
foreach (Logger log in delegates.Cast<Logger>())
{
    log("Individual");
}
```

### Multicast Delegate Return Values

```csharp
public delegate int Calculator(int x, int y);

int Add(int x, int y) { Console.WriteLine("Add"); return x + y; }
int Multiply(int x, int y) { Console.WriteLine("Multiply"); return x * y; }

Calculator calc = Add;
calc += Multiply;

// ⚠️ Only returns result from LAST delegate
int result = calc(3, 4); // Prints "Add\nMultiply", returns 12 (not 7!)

// To get all results:
int[] results = calc.GetInvocationList()
    .Cast<Calculator>()
    .Select(c => c(3, 4))
    .ToArray(); // [7, 12]
```

### Delegates with Exceptions

```csharp
public delegate void Action();

void Method1() => Console.WriteLine("Method1");
void Method2() => throw new Exception("Error in Method2");
void Method3() => Console.WriteLine("Method3");

Action action = Method1;
action += Method2;
action += Method3;

// ⚠️ Exception stops invocation chain
try
{
    action(); // Method1 executes, Method2 throws, Method3 NEVER runs
}
catch (Exception ex)
{
    Console.WriteLine(ex.Message);
}

// To invoke all even if exceptions:
foreach (Action a in action.GetInvocationList())
{
    try
    {
        a();
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Error: {ex.Message}");
    }
}
```

---

## 2. Built-in Delegates

### Action<T> - No Return Value

```csharp
// Action: void method with 0-16 parameters
Action action = () => Console.WriteLine("No parameters");
Action<int> printInt = x => Console.WriteLine(x);
Action<int, string> print = (x, s) => Console.WriteLine($"{s}: {x}");

action();
printInt(42);
print(42, "Answer");
```

### Func<T> - With Return Value

```csharp
// Func: method with return value, 0-16 parameters
// Last type parameter is RETURN TYPE
Func<int> getNumber = () => 42;
Func<int, int> square = x => x * x;
Func<int, int, int> add = (x, y) => x + y;
Func<string, int, bool> contains = (s, n) => s.Contains(n.ToString());

int num = getNumber(); // 42
int squared = square(5); // 25
int sum = add(3, 4); // 7
bool hasDigit = contains("hello123", 1); // true
```

### Predicate<T> - Boolean Test

```csharp
// Predicate: Func<T, bool> - used for testing
Predicate<int> isEven = x => x % 2 == 0;
Predicate<string> isEmpty = s => string.IsNullOrEmpty(s);

bool even = isEven(4); // true
bool empty = isEmpty(""); // true

// Used in List.FindAll, Array.FindAll, etc.
List<int> numbers = new() { 1, 2, 3, 4, 5, 6 };
List<int> evenNumbers = numbers.FindAll(isEven); // [2, 4, 6]
```

### Comparison<T> - Compare Two Values

```csharp
// Comparison: (T, T) => int
Comparison<int> descendingOrder = (x, y) => y.CompareTo(x);

List<int> numbers = new() { 3, 1, 4, 1, 5, 9 };
numbers.Sort(descendingOrder); // [9, 5, 4, 3, 1, 1]
```

---

## 3. Events

### Event Pattern

```csharp
// EventArgs subclass for custom data
public class PriceChangedEventArgs : EventArgs
{
    public decimal OldPrice { get; }
    public decimal NewPrice { get; }

    public PriceChangedEventArgs(decimal oldPrice, decimal newPrice)
    {
        OldPrice = oldPrice;
        NewPrice = newPrice;
    }
}

// Publisher
public class Stock
{
    private string symbol;
    private decimal price;

    // Event delegate
    public event EventHandler<PriceChangedEventArgs> PriceChanged;

    public string Symbol
    {
        get => symbol;
        set => symbol = value;
    }

    public decimal Price
    {
        get => price;
        set
        {
            if (price != value)
            {
                decimal oldPrice = price;
                price = value;
                OnPriceChanged(new PriceChangedEventArgs(oldPrice, value));
            }
        }
    }

    // Protected virtual method to raise event
    protected virtual void OnPriceChanged(PriceChangedEventArgs e)
    {
        PriceChanged?.Invoke(this, e);
    }
}

// Subscriber
public class StockMonitor
{
    public StockMonitor(Stock stock)
    {
        stock.PriceChanged += OnPriceChanged;
    }

    private void OnPriceChanged(object sender, PriceChangedEventArgs e)
    {
        Stock stock = (Stock)sender;
        Console.WriteLine($"{stock.Symbol}: {e.OldPrice} -> {e.NewPrice}");
    }
}

// Usage
Stock stock = new Stock { Symbol = "MSFT", Price = 100 };
StockMonitor monitor = new StockMonitor(stock);
stock.Price = 105; // Triggers event: "MSFT: 100 -> 105"
```

### Custom Event Accessors

```csharp
public class Stock
{
    private EventHandler<PriceChangedEventArgs> priceChanged;

    public event EventHandler<PriceChangedEventArgs> PriceChanged
    {
        add
        {
            Console.WriteLine("Subscriber added");
            priceChanged += value;
        }
        remove
        {
            Console.WriteLine("Subscriber removed");
            priceChanged -= value;
        }
    }

    protected virtual void OnPriceChanged(PriceChangedEventArgs e)
    {
        priceChanged?.Invoke(this, e);
    }
}
```

### Thread-Safe Event Raising

```csharp
// ❌ BAD - Race condition
public event EventHandler MyEvent;

protected void OnMyEvent()
{
    // Between null check and invoke, subscriber could unsubscribe!
    if (MyEvent != null)
        MyEvent(this, EventArgs.Empty); // Potential NullReferenceException
}

// ✅ GOOD - Copy to local variable
protected void OnMyEvent()
{
    EventHandler handler = MyEvent; // Atomic read
    handler?.Invoke(this, EventArgs.Empty);
}

// ✅ EVEN BETTER - Null-conditional operator
protected void OnMyEvent()
{
    MyEvent?.Invoke(this, EventArgs.Empty); // Thread-safe
}
```

### Weak Event Pattern

Prevents memory leaks from event subscriptions.

```csharp
// Using WeakEventManager (WPF/WinForms)
public class WeakEventExample
{
    public void Subscribe(Stock stock)
    {
        WeakEventManager<Stock, PriceChangedEventArgs>
            .AddHandler(stock, nameof(Stock.PriceChanged), OnPriceChanged);
    }

    private void OnPriceChanged(object sender, PriceChangedEventArgs e)
    {
        // Handle event
    }
}

// Custom weak event implementation
public class WeakEventSubscription<TEventArgs> : IDisposable where TEventArgs : EventArgs
{
    private WeakReference subscriberRef;
    private Action<object, TEventArgs> handler;

    public WeakEventSubscription(object subscriber, Action<object, TEventArgs> handler)
    {
        this.subscriberRef = new WeakReference(subscriber);
        this.handler = handler;
    }

    public void Invoke(object sender, TEventArgs e)
    {
        object subscriber = subscriberRef.Target;
        if (subscriber != null)
        {
            handler(sender, e);
        }
    }

    public bool IsAlive => subscriberRef.IsAlive;

    public void Dispose()
    {
        subscriberRef = null;
        handler = null;
    }
}
```

---

## 4. Lambda Expressions

### Lambda Syntax

```csharp
// Expression lambda: (parameters) => expression
Func<int, int> square = x => x * x;
Func<int, int, int> add = (x, y) => x + y;

// Statement lambda: (parameters) => { statements }
Func<int, int> squareWithLog = x =>
{
    Console.WriteLine($"Squaring {x}");
    return x * x;
};

// No parameters
Func<int> getRandom = () => Random.Shared.Next();

// Type inference
Func<int, bool> isEven = x => x % 2 == 0; // x type inferred

// Explicit types
Func<int, bool> isEvenExplicit = (int x) => x % 2 == 0;

// Discard parameters (C# 9.0+)
Func<int, int, int> getFirst = (x, _) => x;
```

### Lambda Captures (Closures)

```csharp
// Capturing outer variables
int factor = 10;
Func<int, int> multiply = x => x * factor; // Captures 'factor'

Console.WriteLine(multiply(5)); // 50

factor = 20;
Console.WriteLine(multiply(5)); // 100 - Uses current value!

// What the compiler generates:
class DisplayClass
{
    public int factor; // Captured variable

    public int MultiplyMethod(int x)
    {
        return x * this.factor;
    }
}

// Equivalent to:
DisplayClass closure = new DisplayClass { factor = 10 };
Func<int, int> multiply = closure.MultiplyMethod;
```

### Closure Pitfalls

```csharp
// ❌ COMMON MISTAKE - Loop variable capture
var actions = new List<Action>();
for (int i = 0; i < 5; i++)
{
    actions.Add(() => Console.WriteLine(i)); // Captures 'i' by reference!
}

foreach (var action in actions)
{
    action(); // Prints: 5, 5, 5, 5, 5 (all same!)
}

// ✅ FIX - Copy to local variable
var actions = new List<Action>();
for (int i = 0; i < 5; i++)
{
    int local = i; // Copy to local
    actions.Add(() => Console.WriteLine(local));
}

foreach (var action in actions)
{
    action(); // Prints: 0, 1, 2, 3, 4
}

// Note: foreach in C# 5.0+ doesn't have this issue
var actions = new List<Action>();
foreach (var item in Enumerable.Range(0, 5))
{
    actions.Add(() => Console.WriteLine(item)); // Safe in C# 5.0+
}
```

### Lambda Performance

```csharp
// Instance method - no allocation
class Calculator
{
    public int Add(int x, int y) => x + y;

    public void Example()
    {
        Func<int, int, int> func = Add; // No closure, no allocation
    }
}

// Static lambda - allocated once
class Calculator
{
    private static readonly Func<int, int, int> addFunc = (x, y) => x + y;

    public void Example()
    {
        Func<int, int, int> func = addFunc; // Reuse cached instance
    }
}

// Capturing lambda - allocates closure
class Calculator
{
    public void Example()
    {
        int factor = 10;
        Func<int, int> multiply = x => x * factor; // Allocates closure object
    }
}
```

---

## 5. Expression Trees

### What are Expression Trees?

Expression trees represent code as data structures.

```csharp
// Lambda expression
Func<int, int> square = x => x * x;

// Expression tree
Expression<Func<int, int>> squareExpr = x => x * x;

// Inspect the tree
Console.WriteLine(squareExpr); // x => (x * x)
Console.WriteLine(squareExpr.Body); // (x * x)
Console.WriteLine(squareExpr.Parameters[0].Name); // x

// Compile and execute
Func<int, int> compiled = squareExpr.Compile();
int result = compiled(5); // 25
```

### Building Expression Trees Manually

```csharp
// Build: x => x * x
ParameterExpression param = Expression.Parameter(typeof(int), "x");
BinaryExpression multiply = Expression.Multiply(param, param);
Expression<Func<int, int>> lambda = Expression.Lambda<Func<int, int>>(multiply, param);

Func<int, int> compiled = lambda.Compile();
Console.WriteLine(compiled(5)); // 25

// Build: (x, y) => x + y
ParameterExpression x = Expression.Parameter(typeof(int), "x");
ParameterExpression y = Expression.Parameter(typeof(int), "y");
BinaryExpression add = Expression.Add(x, y);
Expression<Func<int, int, int>> addLambda =
    Expression.Lambda<Func<int, int, int>>(add, x, y);

// Build method call: person => person.Name.Length > 5
ParameterExpression person = Expression.Parameter(typeof(Person), "person");
MemberExpression nameProp = Expression.Property(person, "Name");
MemberExpression lengthProp = Expression.Property(nameProp, "Length");
ConstantExpression five = Expression.Constant(5);
BinaryExpression comparison = Expression.GreaterThan(lengthProp, five);
Expression<Func<Person, bool>> predicate =
    Expression.Lambda<Func<Person, bool>>(comparison, person);
```

### Expression Tree Visitors

```csharp
// Custom visitor to replace parameters
public class ParameterReplacer : ExpressionVisitor
{
    private readonly ParameterExpression source;
    private readonly ParameterExpression target;

    public ParameterReplacer(ParameterExpression source, ParameterExpression target)
    {
        this.source = source;
        this.target = target;
    }

    protected override Expression VisitParameter(ParameterExpression node)
    {
        return node == source ? target : base.VisitParameter(node);
    }
}

// Usage: Combine predicates
Expression<Func<Person, bool>> predicate1 = p => p.Age > 18;
Expression<Func<Person, bool>> predicate2 = p => p.Name.StartsWith("A");

// Combine with AND
var parameter = Expression.Parameter(typeof(Person), "p");
var body1 = new ParameterReplacer(predicate1.Parameters[0], parameter)
    .Visit(predicate1.Body);
var body2 = new ParameterReplacer(predicate2.Parameters[0], parameter)
    .Visit(predicate2.Body);
var combined = Expression.AndAlso(body1, body2);
var combinedLambda = Expression.Lambda<Func<Person, bool>>(combined, parameter);

// Now: p => (p.Age > 18) AndAlso p.Name.StartsWith("A")
```

### Expression Trees in LINQ

```csharp
// IQueryable uses expression trees
IQueryable<Person> query = dbContext.Persons
    .Where(p => p.Age > 18) // Expression tree
    .OrderBy(p => p.Name);  // Expression tree

// Expression tree is analyzed and converted to SQL:
// SELECT * FROM Persons WHERE Age > 18 ORDER BY Name
```

---

## 6. Advanced Delegate Patterns

### Command Pattern with Delegates

```csharp
public class CommandInvoker
{
    private Stack<Action> undoStack = new();
    private Stack<Action> redoStack = new();

    public void Execute(Action doAction, Action undoAction)
    {
        doAction();
        undoStack.Push(undoAction);
        redoStack.Clear();
    }

    public void Undo()
    {
        if (undoStack.Count > 0)
        {
            Action undo = undoStack.Pop();
            undo();
            redoStack.Push(undo);
        }
    }

    public void Redo()
    {
        if (redoStack.Count > 0)
        {
            Action redo = redoStack.Pop();
            redo();
            undoStack.Push(redo);
        }
    }
}

// Usage
var invoker = new CommandInvoker();
int value = 0;

invoker.Execute(
    doAction: () => value = 10,
    undoAction: () => value = 0
);

Console.WriteLine(value); // 10
invoker.Undo();
Console.WriteLine(value); // 0
```

### Observer Pattern with Events

```csharp
public class Subject
{
    public event EventHandler<DataEventArgs> DataChanged;

    protected virtual void OnDataChanged(DataEventArgs e)
    {
        DataChanged?.Invoke(this, e);
    }
}

public class Observer : IDisposable
{
    private Subject subject;

    public Observer(Subject subject)
    {
        this.subject = subject;
        subject.DataChanged += OnDataChanged;
    }

    private void OnDataChanged(object sender, DataEventArgs e)
    {
        Console.WriteLine($"Data changed: {e.Data}");
    }

    public void Dispose()
    {
        subject.DataChanged -= OnDataChanged;
    }
}
```

### Strategy Pattern with Func

```csharp
public class Calculator
{
    private Func<int, int, int> operation;

    public void SetOperation(Func<int, int, int> operation)
    {
        this.operation = operation;
    }

    public int Execute(int a, int b)
    {
        return operation(a, b);
    }
}

// Usage
var calc = new Calculator();

calc.SetOperation((x, y) => x + y);
Console.WriteLine(calc.Execute(5, 3)); // 8

calc.SetOperation((x, y) => x * y);
Console.WriteLine(calc.Execute(5, 3)); // 15
```

---

## 7. Interview Questions

### Q1: What is a delegate?

**Answer:** A delegate is a type-safe function pointer that holds references to one or more methods. It's a reference type that defines a method signature and can reference any method with a matching signature. Delegates support multicast (invoking multiple methods).

### Q2: What's the difference between Func and Action?

**Answer:**

- **Action:** Delegate that returns void (no return value), supports 0-16 parameters
- **Func:** Delegate that returns a value, supports 0-16 parameters, last type parameter is return type

### Q3: Explain the event pattern in C#

**Answer:** Standard event pattern includes:

- EventArgs-derived class for event data
- event keyword for encapsulation
- Protected virtual OnEventName method to raise event
- EventHandler<TEventArgs> delegate type
- Null-conditional operator for thread-safe invocation

### Q4: What is a closure and how does it work?

**Answer:** A closure is when a lambda expression captures variables from its outer scope. The compiler generates a class to hold the captured variables, and the lambda becomes a method on that class. All lambdas capturing the same variables share the same closure object.

### Q5: What are expression trees used for?

**Answer:** Expression trees represent code as data structures that can be analyzed, modified, and compiled at runtime. Primary use: LINQ providers (like Entity Framework) analyze expression trees to generate SQL queries. Also used for dynamic query building and code generation.

---

## 8. Practical Exercises

### Exercise 1: Implement an Event-Based Calculator

- Create Calculator class with events for each operation
- Implement subscribers that log operations
- Add undo/redo functionality using delegates

### Exercise 2: Build a Predicate Combiner

- Combine multiple Predicate<T> with AND/OR logic
- Use expression trees for IQueryable support
- Create fluent API for building complex predicates

### Exercise 3: Create a Custom Event Manager

- Implement weak event pattern to prevent leaks
- Thread-safe event subscription/unsubscription
- Support for async event handlers

### Exercise 4: Expression Tree Query Builder

- Build LINQ-like query API using expression trees
- Support Where, OrderBy, Select operations
- Translate expressions to different formats (SQL, JSON)

---

## 9. Key Takeaways

✅ **Delegates** are type-safe function pointers supporting multicast
✅ **Events** provide encapsulated publish-subscribe pattern
✅ **Closures** capture outer variables, creating hidden classes
✅ **Lambda** expressions provide concise delegate syntax
✅ **Expression trees** represent code as data for runtime analysis
✅ **Beware** of closure pitfalls and memory leaks from events

---

## Tomorrow's Preview

**Day 4: LINQ & Advanced Query Patterns**

- LINQ internals and deferred execution
- Query syntax vs method syntax
- IEnumerable vs IQueryable
- Custom LINQ operators
- Performance optimization

---

**Master these concepts - they're fundamental to modern C#!** 🚀

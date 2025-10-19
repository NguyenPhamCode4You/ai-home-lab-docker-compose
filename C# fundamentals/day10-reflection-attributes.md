# Day 10: Reflection & Attributes

## 🎯 Learning Objectives

- Master Reflection API for runtime type inspection
- Create and use custom attributes
- Understand dynamic type and DLR
- Compile expressions at runtime
- Load and inspect assemblies

---

## 1. Reflection Basics

### Type Information

```csharp
// Get Type object
Type type1 = typeof(string);
Type type2 = "hello".GetType();
Type type3 = Type.GetType("System.String");

// Type properties
Console.WriteLine(type1.Name); // String
Console.WriteLine(type1.FullName); // System.String
Console.WriteLine(type1.Assembly); // mscorlib
Console.WriteLine(type1.IsClass); // true
Console.WriteLine(type1.IsValueType); // false
Console.WriteLine(type1.IsSealed); // true
Console.WriteLine(type1.IsAbstract); // false

// Base type and interfaces
Type baseType = type1.BaseType; // System.Object
Type[] interfaces = type1.GetInterfaces(); // IComparable, IEnumerable, etc.
```

### Creating Instances

```csharp
// Using Activator
Type type = typeof(StringBuilder);
object instance = Activator.CreateInstance(type);

// With constructor parameters
object instance = Activator.CreateInstance(
    typeof(StringBuilder),
    new object[] { "Initial text" });

// Generic version
T instance = Activator.CreateInstance<T>();

// Using constructor info
Type type = typeof(Person);
ConstructorInfo ctor = type.GetConstructor(new[] { typeof(string), typeof(int) });
object person = ctor.Invoke(new object[] { "John", 30 });
```

---

## 2. Members Inspection

### Properties

```csharp
Type type = typeof(Person);

// Get all properties
PropertyInfo[] properties = type.GetProperties();

foreach (PropertyInfo prop in properties)
{
    Console.WriteLine($"{prop.Name}: {prop.PropertyType}");
    Console.WriteLine($"  Can Read: {prop.CanRead}");
    Console.WriteLine($"  Can Write: {prop.CanWrite}");
}

// Get specific property
PropertyInfo nameProp = type.GetProperty("Name");

// Get/Set value
Person person = new Person { Name = "John", Age = 30 };
object value = nameProp.GetValue(person); // "John"
nameProp.SetValue(person, "Jane");
```

### Methods

```csharp
Type type = typeof(string);

// Get all methods
MethodInfo[] methods = type.GetMethods();

// Get specific method
MethodInfo substring = type.GetMethod("Substring", new[] { typeof(int), typeof(int) });

// Invoke method
string text = "Hello World";
object result = substring.Invoke(text, new object[] { 0, 5 }); // "Hello"

// Static method
MethodInfo parseMethod = typeof(int).GetMethod("Parse", new[] { typeof(string) });
object number = parseMethod.Invoke(null, new object[] { "42" });
```

### Fields

```csharp
Type type = typeof(MyClass);

// Get all fields (including private)
FieldInfo[] fields = type.GetFields(
    BindingFlags.Public |
    BindingFlags.NonPublic |
    BindingFlags.Instance);

foreach (FieldInfo field in fields)
{
    Console.WriteLine($"{field.Name}: {field.FieldType}");
    Console.WriteLine($"  Is Private: {field.IsPrivate}");
    Console.WriteLine($"  Is Static: {field.IsStatic}");
}

// Get/Set field value
FieldInfo field = type.GetField("privateField", BindingFlags.NonPublic | BindingFlags.Instance);
object value = field.GetValue(instance);
field.SetValue(instance, newValue);
```

---

## 3. Custom Attributes

### Creating Attributes

```csharp
// Attribute class
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method,
                AllowMultiple = false,
                Inherited = true)]
public class DocumentationAttribute : Attribute
{
    public string Description { get; set; }
    public string Author { get; set; }
    public string Version { get; set; }

    public DocumentationAttribute(string description)
    {
        Description = description;
    }
}

// Using attribute
[Documentation("User management class", Author = "John", Version = "1.0")]
public class UserManager
{
    [Documentation("Gets user by ID")]
    public User GetUser(int id)
    {
        return null;
    }
}
```

### Reading Attributes

```csharp
Type type = typeof(UserManager);

// Check if attribute exists
bool hasAttribute = type.IsDefined(typeof(DocumentationAttribute), false);

// Get single attribute
DocumentationAttribute attr = type.GetCustomAttribute<DocumentationAttribute>();
Console.WriteLine($"{attr.Description} by {attr.Author}");

// Get all attributes
object[] attributes = type.GetCustomAttributes(false);

foreach (object attr in attributes)
{
    if (attr is DocumentationAttribute doc)
    {
        Console.WriteLine(doc.Description);
    }
}

// Get attribute from method
MethodInfo method = type.GetMethod("GetUser");
DocumentationAttribute methodAttr = method.GetCustomAttribute<DocumentationAttribute>();
```

### Common Built-in Attributes

```csharp
// Obsolete
[Obsolete("Use NewMethod instead", false)]
public void OldMethod() { }

// Conditional (only compiled in Debug)
[Conditional("DEBUG")]
public void DebugLog(string message) { }

// Caller information
public void Log(
    [CallerMemberName] string memberName = "",
    [CallerFilePath] string filePath = "",
    [CallerLineNumber] int lineNumber = 0)
{
    Console.WriteLine($"{filePath}({lineNumber}): {memberName}");
}

// Serialization
[Serializable]
public class Person
{
    public string Name { get; set; }

    [NonSerialized]
    private string tempData;
}
```

---

## 4. Dynamic Type

### Dynamic Keyword

```csharp
// Dynamic type - resolved at runtime
dynamic value = 5;
Console.WriteLine(value); // 5

value = "hello";
Console.WriteLine(value.Length); // 5 (string length)

value = new[] { 1, 2, 3 };
Console.WriteLine(value[0]); // 1

// Dynamic method calls
dynamic calc = new Calculator();
int result = calc.Add(5, 3); // Resolved at runtime

// ExpandoObject - dynamic property bag
dynamic person = new ExpandoObject();
person.Name = "John";
person.Age = 30;
person.SayHello = (Action)(() => Console.WriteLine($"Hello, I'm {person.Name}"));

person.SayHello(); // "Hello, I'm John"
```

### DynamicObject

```csharp
public class DynamicDictionary : DynamicObject
{
    private Dictionary<string, object> dictionary = new Dictionary<string, object>();

    // Get dynamic member
    public override bool TryGetMember(GetMemberBinder binder, out object result)
    {
        return dictionary.TryGetValue(binder.Name, out result);
    }

    // Set dynamic member
    public override bool TrySetMember(SetMemberBinder binder, object value)
    {
        dictionary[binder.Name] = value;
        return true;
    }

    // Invoke dynamic method
    public override bool TryInvokeMember(
        InvokeMemberBinder binder,
        object[] args,
        out object result)
    {
        if (binder.Name == "GetValue")
        {
            result = dictionary[(string)args[0]];
            return true;
        }

        result = null;
        return false;
    }
}

// Usage
dynamic dict = new DynamicDictionary();
dict.Name = "John";
dict.Age = 30;
Console.WriteLine(dict.Name); // "John"
```

---

## 5. Assembly Loading

### Loading Assemblies

```csharp
// Load from file
Assembly assembly = Assembly.LoadFrom("MyLibrary.dll");

// Load from byte array
byte[] bytes = File.ReadAllBytes("MyLibrary.dll");
Assembly assembly = Assembly.Load(bytes);

// Load by name
Assembly assembly = Assembly.Load("System.Collections");

// Get executing assembly
Assembly current = Assembly.GetExecutingAssembly();

// Get types in assembly
Type[] types = assembly.GetTypes();

foreach (Type type in types)
{
    Console.WriteLine(type.FullName);
}
```

### Plugin Architecture

```csharp
public interface IPlugin
{
    string Name { get; }
    void Execute();
}

public class PluginLoader
{
    public List<IPlugin> LoadPlugins(string pluginDirectory)
    {
        List<IPlugin> plugins = new List<IPlugin>();

        string[] files = Directory.GetFiles(pluginDirectory, "*.dll");

        foreach (string file in files)
        {
            try
            {
                Assembly assembly = Assembly.LoadFrom(file);

                foreach (Type type in assembly.GetTypes())
                {
                    if (typeof(IPlugin).IsAssignableFrom(type) && !type.IsInterface)
                    {
                        IPlugin plugin = (IPlugin)Activator.CreateInstance(type);
                        plugins.Add(plugin);
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error loading {file}: {ex.Message}");
            }
        }

        return plugins;
    }
}
```

---

## 6. Performance Considerations

### Caching Type Information

```csharp
// ❌ SLOW - Reflection every time
public object GetProperty(object obj, string propertyName)
{
    PropertyInfo prop = obj.GetType().GetProperty(propertyName);
    return prop.GetValue(obj);
}

// ✅ FAST - Cache PropertyInfo
private static ConcurrentDictionary<string, PropertyInfo> propertyCache
    = new ConcurrentDictionary<string, PropertyInfo>();

public object GetProperty(object obj, string propertyName)
{
    Type type = obj.GetType();
    string key = $"{type.FullName}.{propertyName}";

    PropertyInfo prop = propertyCache.GetOrAdd(key, _ =>
        type.GetProperty(propertyName));

    return prop.GetValue(obj);
}
```

### Compiled Delegates

```csharp
// ❌ SLOW - Reflection invoke
PropertyInfo prop = type.GetProperty("Name");
object value = prop.GetValue(instance); // Slow!

// ✅ FAST - Compiled delegate
public static class PropertyAccessor<T>
{
    private static readonly ConcurrentDictionary<string, Func<T, object>> getters
        = new ConcurrentDictionary<string, Func<T, object>>();

    public static Func<T, object> GetPropertyGetter(string propertyName)
    {
        return getters.GetOrAdd(propertyName, name =>
        {
            PropertyInfo prop = typeof(T).GetProperty(name);
            ParameterExpression param = Expression.Parameter(typeof(T), "obj");
            MemberExpression property = Expression.Property(param, prop);
            UnaryExpression convert = Expression.Convert(property, typeof(object));

            return Expression.Lambda<Func<T, object>>(convert, param).Compile();
        });
    }
}

// Usage
var getter = PropertyAccessor<Person>.GetPropertyGetter("Name");
object value = getter(person); // Fast!
```

---

## 7. Practical Applications

### Object Mapper

```csharp
public class SimpleMapper
{
    public TTarget Map<TSource, TTarget>(TSource source)
        where TTarget : new()
    {
        TTarget target = new TTarget();

        PropertyInfo[] sourceProps = typeof(TSource).GetProperties();
        PropertyInfo[] targetProps = typeof(TTarget).GetProperties();

        foreach (PropertyInfo sourceProp in sourceProps)
        {
            PropertyInfo targetProp = Array.Find(targetProps,
                p => p.Name == sourceProp.Name &&
                     p.PropertyType == sourceProp.PropertyType);

            if (targetProp != null && targetProp.CanWrite)
            {
                object value = sourceProp.GetValue(source);
                targetProp.SetValue(target, value);
            }
        }

        return target;
    }
}

// Usage
PersonDto dto = mapper.Map<Person, PersonDto>(person);
```

### Dependency Injection Container

```csharp
public class SimpleContainer
{
    private Dictionary<Type, Type> registrations = new Dictionary<Type, Type>();
    private Dictionary<Type, object> singletons = new Dictionary<Type, object>();

    public void Register<TInterface, TImplementation>()
    {
        registrations[typeof(TInterface)] = typeof(TImplementation);
    }

    public void RegisterSingleton<TInterface>(TInterface instance)
    {
        singletons[typeof(TInterface)] = instance;
    }

    public T Resolve<T>()
    {
        return (T)Resolve(typeof(T));
    }

    private object Resolve(Type type)
    {
        // Check singletons
        if (singletons.TryGetValue(type, out object singleton))
        {
            return singleton;
        }

        // Get implementation type
        if (!registrations.TryGetValue(type, out Type implementationType))
        {
            implementationType = type;
        }

        // Get constructor
        ConstructorInfo constructor = implementationType
            .GetConstructors()
            .OrderByDescending(c => c.GetParameters().Length)
            .First();

        // Resolve constructor parameters
        ParameterInfo[] parameters = constructor.GetParameters();
        object[] arguments = new object[parameters.Length];

        for (int i = 0; i < parameters.Length; i++)
        {
            arguments[i] = Resolve(parameters[i].ParameterType);
        }

        // Create instance
        return constructor.Invoke(arguments);
    }
}
```

### Validation Framework

```csharp
[AttributeUsage(AttributeTargets.Property)]
public class RequiredAttribute : ValidationAttribute
{
    public override bool IsValid(object value)
    {
        return value != null && value.ToString() != string.Empty;
    }
}

[AttributeUsage(AttributeTargets.Property)]
public class RangeAttribute : ValidationAttribute
{
    public int Min { get; set; }
    public int Max { get; set; }

    public override bool IsValid(object value)
    {
        if (value is int intValue)
        {
            return intValue >= Min && intValue <= Max;
        }
        return false;
    }
}

public class Validator
{
    public List<string> Validate(object obj)
    {
        List<string> errors = new List<string>();
        Type type = obj.GetType();

        foreach (PropertyInfo prop in type.GetProperties())
        {
            foreach (ValidationAttribute attr in
                prop.GetCustomAttributes<ValidationAttribute>())
            {
                object value = prop.GetValue(obj);

                if (!attr.IsValid(value))
                {
                    errors.Add($"{prop.Name}: {attr.ErrorMessage}");
                }
            }
        }

        return errors;
    }
}

// Usage
public class Person
{
    [Required(ErrorMessage = "Name is required")]
    public string Name { get; set; }

    [Range(Min = 0, Max = 150, ErrorMessage = "Age must be between 0 and 150")]
    public int Age { get; set; }
}

Validator validator = new Validator();
List<string> errors = validator.Validate(person);
```

---

## 8. Interview Questions

### Q1: What is reflection and when to use it?

**Answer:** Reflection is runtime type inspection and manipulation. Use for: plugins, serialization, ORM, DI containers, validation frameworks. Avoid in performance-critical code due to overhead.

### Q2: Performance impact of reflection?

**Answer:** Reflection is 10-100x slower than direct access. Mitigate by: caching Type/PropertyInfo, using compiled expressions, using source generators (C# 9+), avoiding in hot paths.

### Q3: Difference between GetType() and typeof()?

**Answer:** GetType() is instance method, returns runtime type. typeof() is compile-time operator, returns Type object for known type. GetType() is virtual, typeof() is not.

### Q4: What is dynamic type?

**Answer:** dynamic bypasses compile-time type checking, resolves members at runtime using DLR. Useful for COM interop, dynamic languages interop, but loses IntelliSense and type safety.

### Q5: How to create custom attribute?

**Answer:** Inherit from Attribute, use AttributeUsage to specify targets. Access with GetCustomAttribute/GetCustomAttributes. Common for metadata, validation, serialization control.

---

## 9. Practical Exercises

### Exercise 1: Object Cloner

Deep clone objects using reflection, handling:

- Circular references
- Collections
- Private fields

### Exercise 2: JSON Serializer

Simple JSON serializer using reflection:

- Serialize objects to JSON
- Deserialize JSON to objects
- Handle nested objects

### Exercise 3: Query Builder

Dynamic query builder:

- Build LINQ expressions from strings
- Support multiple conditions
- Type-safe compilation

### Exercise 4: Performance Comparison

Benchmark:

- Direct property access
- Reflection
- Cached reflection
- Compiled expressions

---

## 10. Key Takeaways

✅ **Reflection** enables runtime type inspection
✅ **Cache** Type/MemberInfo for performance
✅ **Compiled expressions** faster than reflection
✅ **Custom attributes** for metadata
✅ **Dynamic** for runtime binding
✅ **Avoid** reflection in hot paths
✅ **Source generators** better than reflection when possible

---

## Tomorrow's Preview

**Day 11: Modern C# Features (C# 7-12)**

- Pattern matching evolution
- Records and init properties
- Nullable reference types
- Global usings
- Raw string literals

---

**Reflection is powerful but use wisely!** 🔍

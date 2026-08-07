# Java 8 & Modern Java

Java 8 was one of the biggest releases in Java's history.

It fundamentally changed how Java developers write code by introducing:

- Lambda Expressions
- Functional Interfaces
- Method References
- Stream API
- Optional
- New Date & Time API
- Default Methods

Later Java versions (9–21) introduced additional improvements, but Java 8 remains the foundation of modern Java
development.

This chapter provides an overview of these features. The next two chapters will dive much deeper into **Streams** and
**Concurrency**.

______________________________________________________________________

# Why Java 8?

Before Java 8, Java code was often verbose.

Example

```java
Collections.sort(names, new Comparator<String>() {

    @Override
    public int compare(String a, String b) {
        return a.compareTo(b);
    }

});
```

Java 8 introduced Lambdas.

```java
Collections.sort(names, (a, b) -> a.compareTo(b));
```

Much shorter.

Much cleaner.

______________________________________________________________________

# Lambda Expressions

A Lambda Expression is an anonymous function.

Syntax

```java
(parameters) -> expression
```

or

```java
(parameters) -> {

    // multiple statements

}
```

______________________________________________________________________

# Example

Without Lambda

```java
Runnable task = new Runnable() {

    @Override
    public void run() {
        System.out.println("Running...");
    }

};
```

With Lambda

```java
Runnable task = () -> System.out.println("Running...");
```

______________________________________________________________________

# Lambda Examples

No parameters

```java
() -> System.out.println("Hello");
```

One parameter

```java
x -> x * x
```

Multiple parameters

```java
(a, b) -> a + b
```

Multiple statements

```java
(a, b) -> {

    int sum = a + b;

    return sum;

}
```

______________________________________________________________________

# Benefits of Lambdas

- Less boilerplate
- Easier to read
- Functional programming support
- Better integration with Streams

______________________________________________________________________

# Functional Interfaces

A Functional Interface contains exactly **one abstract method**.

Example

```java
@FunctionalInterface
interface Calculator {

    int calculate(int a, int b);

}
```

Implementation

```java
Calculator add =
    (a, b) -> a + b;

System.out.println(add.calculate(10, 20));
```

Output

```
30
```

We'll explore Functional Interfaces in detail in the next chapter.

______________________________________________________________________

# Built-in Functional Interfaces

Java provides several commonly used interfaces.

| Interface | Method | Purpose |
|-----------|---------|----------|
| Predicate<T> | test() | Returns boolean |
| Function\<T,R> | apply() | Transforms values |
| Consumer<T> | accept() | Consumes values |
| Supplier<T> | get() | Produces values |

Example

```java
Predicate<Integer> even =
    n -> n % 2 == 0;

System.out.println(even.test(4));
```

Output

```
true
```

______________________________________________________________________

# Method References

Sometimes a Lambda simply calls an existing method.

Instead of

```java
names.forEach(name ->
    System.out.println(name));
```

Use

```java
names.forEach(System.out::println);
```

Cleaner.

More readable.

______________________________________________________________________

# Types of Method References

Static method

```java
Integer::parseInt
```

Instance method of a particular object

```java
printer::print
```

Instance method of an arbitrary object

```java
String::toUpperCase
```

Constructor reference

```java
Employee::new
```

______________________________________________________________________

# Optional

One of the biggest sources of bugs in Java is

```
NullPointerException
```

Java 8 introduced

```java
Optional
```

to represent values that may or may not exist.

______________________________________________________________________

# Creating Optional

```java
Optional<String> name =
    Optional.of("Java");
```

Nullable value

```java
Optional<String> name =
    Optional.ofNullable(value);
```

Empty Optional

```java
Optional<String> name =
    Optional.empty();
```

______________________________________________________________________

# Checking Values

Instead of

```java
if(name != null){

}
```

Use

```java
if(optional.isPresent()){

}
```

______________________________________________________________________

# Retrieving Values

```java
String value =
    optional.get();
```

Dangerous if empty.

Better

```java
String value =
    optional.orElse("Unknown");
```

Or

```java
String value =
    optional.orElseGet(() -> "Guest");
```

______________________________________________________________________

# ifPresent()

```java
optional.ifPresent(
    System.out::println
);
```

Executes only if a value exists.

______________________________________________________________________

# Common Optional Methods

```java
isPresent()

isEmpty()

orElse()

orElseGet()

orElseThrow()

ifPresent()

map()

filter()
```

______________________________________________________________________

# When to Use Optional

Good

Method return values.

```java
Optional<User> findUser()
```

Avoid

Fields

```java
Optional<String> name;
```

Method parameters

```java
save(Optional<User> user)
```

Use Optional primarily as a return type.

______________________________________________________________________

# Date & Time API

Before Java 8

```java
Date

Calendar
```

These classes were difficult to use.

Java 8 introduced

```
java.time
```

______________________________________________________________________

# LocalDate

```java
LocalDate today =
    LocalDate.now();

System.out.println(today);
```

Output

```
2026-08-07
```

______________________________________________________________________

# LocalTime

```java
LocalTime now =
    LocalTime.now();
```

______________________________________________________________________

# LocalDateTime

```java
LocalDateTime now =
    LocalDateTime.now();
```

______________________________________________________________________

# Creating Specific Dates

```java
LocalDate date =
    LocalDate.of(2025, 1, 1);
```

______________________________________________________________________

# Useful Operations

```java
today.plusDays(5);

today.minusMonths(2);

today.plusYears(1);
```

______________________________________________________________________

# Date Formatting

```java
DateTimeFormatter formatter =
    DateTimeFormatter.ofPattern(
        "dd-MM-yyyy"
    );

String formatted =
    today.format(formatter);
```

Output

```
07-08-2026
```

______________________________________________________________________

# Streams (Overview)

Streams process collections efficiently.

Example

```java
List<String> names =
    List.of("Alice", "Bob", "Charlie");
```

Without Streams

```java
for(String name : names){

    System.out.println(name);

}
```

With Streams

```java
names.stream()
     .forEach(System.out::println);
```

Streams will be covered in depth in the next chapter.

______________________________________________________________________

# Parallel Streams

Normal Stream

```java
numbers.stream()
```

Parallel Stream

```java
numbers.parallelStream()
```

Useful for CPU-intensive operations on large datasets.

Use carefully.

Parallel isn't always faster.

______________________________________________________________________

# Default Methods

Interfaces can now contain implementations.

```java
interface Vehicle {

    default void start() {

        System.out.println("Starting");

    }

}
```

This helps maintain backward compatibility.

______________________________________________________________________

# Static Methods in Interfaces

```java
interface MathUtil {

    static int square(int x){

        return x * x;

    }

}
```

Usage

```java
MathUtil.square(5);
```

______________________________________________________________________

# Modern Java Features (Post Java 8)

Although Java 8 is still the baseline for many enterprise applications, newer versions introduced several improvements.

______________________________________________________________________

## var (Java 10)

```java
var name = "Java";
```

Compiler infers the type.

Equivalent to

```java
String name = "Java";
```

Use it when the type is obvious.

______________________________________________________________________

## Records (Java 16)

Instead of

```java
class Employee {

    private final String name;
    private final int age;

    // constructor
    // getters
    // equals()
    // hashCode()
    // toString()

}
```

Use

```java
record Employee(
    String name,
    int age
) {}
```

Perfect for immutable data objects.

______________________________________________________________________

## Switch Expressions (Java 14)

Old

```java
switch(day){

    case MONDAY:
        return 1;

    default:
        return 0;

}
```

Modern

```java
int value = switch(day){

    case MONDAY -> 1;

    default -> 0;

};
```

Cleaner.

______________________________________________________________________

## Text Blocks (Java 15)

Instead of

```java
String json =
"{\"name\":\"Java\"}";
```

Use

```java
String json = """
{
    "name":"Java"
}
""";
```

Much more readable.

______________________________________________________________________

# Common Mistakes

## Overusing Optional

Wrong

```java
Optional<String> name;
```

Optional isn't intended for fields.

______________________________________________________________________

## Calling get()

Wrong

```java
optional.get();
```

Without checking.

Prefer

```java
orElse()

orElseThrow()
```

______________________________________________________________________

## Using Parallel Streams Everywhere

Parallel Streams introduce thread overhead.

Use them only when performance testing justifies it.

______________________________________________________________________

## Replacing Every Loop with Streams

Sometimes

```java
for
```

loops are simpler and easier to read.

Choose readability first.

______________________________________________________________________

# Best Practices

✅ Prefer Lambdas over anonymous classes when appropriate.

✅ Use Method References for readability.

✅ Return Optional instead of null.

✅ Use the `java.time` package for all new code.

✅ Keep Streams readable.

✅ Adopt modern language features where they improve clarity.

______________________________________________________________________

# Interview Deep Dive

## Question

What are the major features introduced in Java 8?

### Answer

Java 8 introduced Lambda Expressions, Functional Interfaces, Method References, Stream API, Optional, the new Date &
Time API (`java.time`), and Default Methods in interfaces. These features simplified Java code and enabled a more
functional programming style.

______________________________________________________________________

## Question

What is Optional, and why was it introduced?

### Answer

`Optional` is a container object that may or may not contain a value. It was introduced to reduce
`NullPointerException`s and make the absence of a value explicit. It is most commonly used as a method return type.

______________________________________________________________________

## Question

What is a Functional Interface?

### Answer

A Functional Interface is an interface containing exactly one abstract method. It serves as the target type for Lambda
Expressions and Method References. The `@FunctionalInterface` annotation helps the compiler enforce this rule.

______________________________________________________________________

## Question

What is the difference between a Lambda Expression and a Method Reference?

### Answer

A Lambda Expression provides an inline implementation of a functional interface.

A Method Reference is a shorthand used when an existing method already matches the required functional interface
signature, improving readability.

______________________________________________________________________

## Question

Why was the `java.time` package introduced?

### Answer

The older `Date` and `Calendar` APIs were mutable, difficult to use, and error-prone. The `java.time` package introduced
immutable, thread-safe, and more intuitive classes such as `LocalDate`, `LocalTime`, and `LocalDateTime`.

______________________________________________________________________

# Practice Questions

1. What were the major features introduced in Java 8?
1. What is a Lambda Expression?
1. What is a Functional Interface?
1. What is a Method Reference?
1. What is Optional?
1. Why is Optional preferred over returning null?
1. What classes are available in the `java.time` package?
1. What are Default Methods?
1. What are Records, and when would you use them?
1. When should you use Parallel Streams?

______________________________________________________________________

# Summary

Java 8 transformed Java into a more expressive and modern language.

In this chapter, you learned:

- Lambda Expressions
- Functional Interfaces
- Method References
- Optional
- Date & Time API
- Stream API (overview)
- Default Methods
- Modern Java features like `var`, Records, Switch Expressions, and Text Blocks

These features are widely used in modern Java applications and frequently appear in interviews. While this chapter
introduced the concepts, the next chapter focuses entirely on the **Stream API**, one of the most important and
interview-heavy features introduced in Java 8.

______________________________________________________________________

# Next

[Stream API](11-stream-api.md)

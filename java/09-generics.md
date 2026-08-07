# Generics

Generics are one of the most powerful features introduced in Java 5.

Before Generics, Java collections could store **any object**, making code error-prone and requiring explicit type
casting.

Generics solved this by bringing **compile-time type safety**.

This chapter covers:

- Why Generics exist
- Generic classes
- Generic methods
- Bounded types
- Wildcards
- Type Erasure
- PECS Principle
- Common interview questions

______________________________________________________________________

# Why Generics?

Imagine this code before Java 5.

```java
List list = new ArrayList();

list.add("Java");
list.add(100);

String language = (String) list.get(0);
```

Nothing prevents adding different types.

The compiler doesn't complain.

The error occurs at runtime.

______________________________________________________________________

# Runtime Problem

```java
List list = new ArrayList();

list.add(100);

String value = (String) list.get(0);
```

Output

```
ClassCastException
```

This is exactly what Generics prevent.

______________________________________________________________________

# Generic Collection

```java
List<String> languages =
    new ArrayList<>();

languages.add("Java");
languages.add("Python");
```

Now this is illegal

```java
languages.add(100);
```

Compilation error.

Much safer.

______________________________________________________________________

# Benefits of Generics

- Compile-time type safety
- Eliminates explicit casting
- Cleaner code
- Better readability
- Fewer runtime errors

______________________________________________________________________

# Generic Syntax

```java
List<String> names =
    new ArrayList<>();
```

Here

```
String
```

is called the

**Type Parameter**.

______________________________________________________________________

# Common Generic Types

```java
List<Integer>

List<String>

Map<Integer,String>

Set<Employee>

Queue<Order>
```

______________________________________________________________________

# Generic Class

Example

```java
class Box<T> {

    private T value;

    public void set(T value) {
        this.value = value;
    }

    public T get() {
        return value;
    }

}
```

Usage

```java
Box<String> box = new Box<>();

box.set("Java");

System.out.println(box.get());
```

Output

```
Java
```

______________________________________________________________________

# Another Example

```java
Box<Integer> box = new Box<>();

box.set(100);

System.out.println(box.get());
```

Output

```
100
```

Same class.

Different types.

______________________________________________________________________

# Multiple Type Parameters

```java
class Pair<K, V> {

    private K key;
    private V value;

}
```

Usage

```java
Pair<Integer, String> pair =
    new Pair<>();
```

Examples

```
K → Integer

V → String
```

______________________________________________________________________

# Generic Method

Methods can also be generic.

```java
public class Printer {

    public static <T> void print(T value) {

        System.out.println(value);

    }

}
```

Usage

```java
Printer.print("Java");

Printer.print(100);

Printer.print(true);
```

One method.

Many types.

______________________________________________________________________

# Generic Return Type

```java
public static <T> T first(T a, T b) {

    return a;

}
```

Usage

```java
String value =
    first("Java", "Python");
```

______________________________________________________________________

# Type Inference

Java usually infers the type automatically.

Instead of

```java
Box<String> box =
    new Box<String>();
```

Java 7+

```java
Box<String> box =
    new Box<>();
```

This is called the **Diamond Operator**.

______________________________________________________________________

# Bounded Generics

Sometimes we want to restrict allowed types.

Example

```java
class Calculator<T extends Number> {

}
```

Allowed

```java
Calculator<Integer>

Calculator<Double>

Calculator<Float>
```

Not allowed

```java
Calculator<String>
```

Compilation error.

______________________________________________________________________

# Why Bounded Types?

Suppose we want to calculate averages.

```java
class Statistics<T extends Number> {

}
```

Now every object inside the class is guaranteed to be numeric.

______________________________________________________________________

# Multiple Bounds

Java allows multiple bounds.

```java
<T extends Animal & Runnable>
```

Rules

- Class first
- Interfaces later

Correct

```java
<T extends Animal & Runnable>
```

Wrong

```java
<T extends Runnable & Animal>
```

______________________________________________________________________

# Wildcards

Very important interview topic.

Three types.

```
?

? extends

? super
```

______________________________________________________________________

# Unbounded Wildcard

```java
List<?> list;
```

Means

```
List of anything.
```

Useful when reading data.

______________________________________________________________________

# Upper Bounded Wildcard

```java
List<? extends Number>
```

Accepts

```
List<Integer>

List<Double>

List<Float>
```

______________________________________________________________________

Example

```java
public void print(
    List<? extends Number> list){

}
```

Works

```java
print(List<Integer>);

print(List<Double>);
```

______________________________________________________________________

# Lower Bounded Wildcard

```java
List<? super Integer>
```

Accepts

```
List<Integer>

List<Number>

List<Object>
```

______________________________________________________________________

# PECS Principle

One of the highest-frequency interview questions.

PECS means

```
Producer

Extends

Consumer

Super
```

______________________________________________________________________

# Producer

If a collection **produces** values,

use

```java
extends
```

Example

```java
List<? extends Number>
```

You read values.

______________________________________________________________________

# Consumer

If a collection **consumes** values,

use

```java
super
```

Example

```java
List<? super Integer>
```

You insert values.

______________________________________________________________________

# Example

Reading numbers

```java
void print(
    List<? extends Number> numbers){

}
```

Writing numbers

```java
void add(
    List<? super Integer> numbers){

}
```

______________________________________________________________________

# Why Not Just Use Object?

Bad

```java
List<Object>
```

Does **not** accept

```java
List<String>
```

Very common interview trick.

Example

```java
List<String> names =
    new ArrayList<>();

List<Object> objects =
    names;
```

Compilation error.

Generics are **invariant**.

______________________________________________________________________

# Type Erasure

Perhaps the most important Generics interview topic.

Generics exist only at **compile time**.

At runtime,

the JVM removes generic information.

Example

```java
List<String>

List<Integer>
```

Both become

```java
List
```

after compilation.

This process is called

**Type Erasure**.

______________________________________________________________________

# Why Type Erasure?

Backwards compatibility.

Old Java code written before Java 5 still works.

______________________________________________________________________

# Limitation of Type Erasure

This is illegal

```java
if(obj instanceof List<String>)
```

Because generic type information no longer exists.

Correct

```java
if(obj instanceof List)
```

______________________________________________________________________

# Cannot Create Generic Arrays

Illegal

```java
T[] array = new T[10];
```

Compilation error.

______________________________________________________________________

# Cannot Instantiate Type Parameter

Wrong

```java
T value = new T();
```

Compiler error.

The compiler doesn't know what `T` actually is.

______________________________________________________________________

# Raw Types

Old Java

```java
List list =
    new ArrayList();
```

Avoid.

Use

```java
List<String> list =
    new ArrayList<>();
```

Raw types bypass compile-time type checking.

______________________________________________________________________

# Generic Interface

```java
interface Repository<T> {

    void save(T object);

    T find();

}
```

Implementation

```java
class UserRepository
    implements Repository<User> {

}
```

Common in Spring Data.

______________________________________________________________________

# Comparable

Real-world example

```java
class Employee
    implements Comparable<Employee> {

}
```

Notice

Generics define

what the interface works with.

______________________________________________________________________

# Common Mistakes

## Using Raw Types

Wrong

```java
List list =
    new ArrayList();
```

Always specify the type.

______________________________________________________________________

## Using Object Everywhere

Avoid

```java
Object value;
```

Use Generics instead.

______________________________________________________________________

## Confusing extends with super

Remember

```
Producer → extends

Consumer → super
```

PECS.

______________________________________________________________________

## Forgetting Diamond Operator

Old

```java
new ArrayList<String>();
```

Modern

```java
new ArrayList<>();
```

______________________________________________________________________

# Best Practices

✅ Always use Generics.

✅ Avoid raw types.

✅ Program to interfaces.

✅ Use bounded types when appropriate.

✅ Remember PECS.

✅ Prefer compile-time safety over runtime casting.

______________________________________________________________________

# Interview Deep Dive

## Question

What are Generics?

### Answer

Generics allow classes, interfaces, and methods to operate on different types while providing compile-time type safety.
They eliminate explicit casting, improve readability, and reduce runtime `ClassCastException`s.

______________________________________________________________________

## Question

Why were Generics introduced?

### Answer

Generics were introduced to provide compile-time type checking, eliminate unnecessary type casting, and make collections
safer and easier to use by ensuring they contain only the intended type of objects.

______________________________________________________________________

## Question

What is Type Erasure?

### Answer

Type Erasure is the process by which the Java compiler removes generic type information during compilation. At runtime,
generic types such as `List<String>` and `List<Integer>` are treated simply as `List`, preserving backward compatibility
with older Java versions.

______________________________________________________________________

## Question

What is PECS?

### Answer

PECS stands for **Producer Extends, Consumer Super**.

- Use `? extends T` when the collection produces values that you want to read.
- Use `? super T` when the collection consumes values that you want to write.

This guideline helps design flexible and type-safe APIs.

______________________________________________________________________

## Question

Why can't we create `new T()`?

### Answer

Because of Type Erasure, the actual type represented by `T` is not available at runtime. The compiler cannot determine
which constructor to invoke, so creating `new T()` is not allowed.

______________________________________________________________________

# Practice Questions

1. What are Generics?
1. Why were Generics introduced?
1. What are the advantages of Generics?
1. What is a generic class?
1. What is a generic method?
1. What is the Diamond Operator?
1. What are bounded Generics?
1. Explain `?`, `? extends`, and `? super`.
1. What is PECS?
1. What is Type Erasure, and why is it necessary?

______________________________________________________________________

# Summary

Generics make Java code safer, cleaner, and more reusable by enforcing type safety at compile time.

In this chapter, you learned:

- Generic classes
- Generic methods
- Type parameters
- Bounded types
- Wildcards
- PECS
- Type Erasure
- Raw types
- Common interview questions

Generics are used throughout the Java ecosystem—from the Collections Framework to Spring Data repositories and
functional programming APIs. Understanding them deeply will make your code more expressive and help you answer some of
the most common Java interview questions with confidence.

______________________________________________________________________

# Next

[Java 8 & Modern Java](10-java-8-and-modern-java.md)

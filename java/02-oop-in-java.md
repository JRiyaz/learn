# OOP in Java

Object-Oriented Programming (OOP) is the foundation of Java.

Almost every Java interview begins with OOP questions because understanding OOP is essential for writing clean,
maintainable, and scalable applications.

This chapter focuses on **how OOP is implemented in Java**, not just the theoretical definitions.

______________________________________________________________________

# Why OOP?

Imagine you're building an e-commerce application.

Without OOP, you might end up with hundreds of unrelated variables and functions.

```java
String customerName;
String customerEmail;
String customerAddress;

void placeOrder(){}

void cancelOrder(){}

void updateAddress(){}
```

As the application grows, managing related data and behavior becomes difficult.

OOP solves this by grouping related data and behavior together.

```java
class Customer {

    String name;
    String email;
    String address;

    void placeOrder() {}

    void cancelOrder() {}

    void updateAddress() {}

}
```

Now everything related to a customer exists in one place.

______________________________________________________________________

# The Four Pillars of OOP

Java's object-oriented design is built around four core principles.

- Encapsulation
- Abstraction
- Inheritance
- Polymorphism

We'll introduce them here and study each in detail in later chapters.

______________________________________________________________________

# What is a Class?

A class is a blueprint for creating objects.

Think of it as a template.

Example

```java
class Employee {

    String name;
    int age;

    void work() {
        System.out.println("Working...");
    }

}
```

The class itself doesn't represent an actual employee.

It's only a definition.

______________________________________________________________________

# What is an Object?

An object is an instance of a class.

Creating an object

```java
Employee emp = new Employee();
```

Now `emp` is a real object in memory.

You can store data inside it.

```java
emp.name = "Riyaz";
emp.age = 28;
```

Call methods

```java
emp.work();
```

______________________________________________________________________

# Multiple Objects

One class can create many objects.

```java
Employee e1 = new Employee();
Employee e2 = new Employee();
Employee e3 = new Employee();
```

Each object has its own state.

```java
e1.name = "Alice";
e2.name = "Bob";
e3.name = "Charlie";
```

Changing one object doesn't affect the others.

______________________________________________________________________

# Object State and Behavior

Every object has two things.

## State

Data stored inside the object.

```java
String name;
int age;
double salary;
```

______________________________________________________________________

## Behavior

Actions performed by the object.

```java
work();

login();

logout();

calculateSalary();
```

______________________________________________________________________

# Creating a Simple Class

```java
class Car {

    String brand;
    String model;
    int year;

    void start() {
        System.out.println("Car started");
    }

}
```

Using it

```java
public class Main {

    public static void main(String[] args) {

        Car car = new Car();

        car.brand = "Toyota";
        car.model = "Camry";
        car.year = 2023;

        car.start();

    }

}
```

______________________________________________________________________

# The new Keyword

```java
Car car = new Car();
```

The `new` keyword:

- Allocates memory.
- Creates the object.
- Calls the constructor.
- Returns a reference.

Without `new`, no object exists.

______________________________________________________________________

# Reference Variables

```java
Car car = new Car();
```

Here,

```
car
```

doesn't store the object itself.

It stores a **reference** to the object.

```
car
  │
  ▼
+----------------+
| brand          |
| model          |
| year           |
+----------------+
```

______________________________________________________________________

# Assigning References

```java
Car c1 = new Car();

Car c2 = c1;
```

Now both variables point to the same object.

```
c1 ─┐
    │
    ▼
  Object
    ▲
    │
c2 ─┘
```

Changing through one reference affects the same object.

```java
c1.brand = "BMW";

System.out.println(c2.brand);
```

Output

```
BMW
```

______________________________________________________________________

# this Keyword

Inside a class,

`this`

refers to the current object.

Example

```java
class Student {

    String name;

    void setName(String name) {
        this.name = name;
    }

}
```

Without `this`

```java
name = name;
```

Both refer to the method parameter.

Nothing changes.

Using `this`

```java
this.name = name;
```

clearly refers to the object's field.

______________________________________________________________________

# Methods

Methods define behavior.

```java
class Calculator {

    int add(int a, int b) {
        return a + b;
    }

}
```

Usage

```java
Calculator calc = new Calculator();

int result = calc.add(10, 20);
```

______________________________________________________________________

# Instance Variables

Variables inside objects.

```java
class User {

    String name;
    int age;

}
```

Every object has its own copy.

______________________________________________________________________

# Local Variables

Variables inside methods.

```java
void print() {

    int x = 10;

}
```

Local variables exist only while the method executes.

______________________________________________________________________

# Instance Methods

Require an object.

```java
class User {

    void login() {
        System.out.println("Logged in");
    }

}
```

Usage

```java
User user = new User();

user.login();
```

______________________________________________________________________

# Static Methods

Belong to the class.

```java
class MathUtil {

    static int square(int x) {
        return x * x;
    }

}
```

Usage

```java
MathUtil.square(5);
```

No object required.

______________________________________________________________________

# Instance vs Static

Instance

```java
Employee emp = new Employee();

emp.work();
```

Static

```java
Math.max(10,20);
```

Rule of thumb

If a method depends on object data,

don't make it static.

______________________________________________________________________

# Static Variables

Shared by all objects.

```java
class Employee {

    static String company = "OpenAI";

}
```

Every employee shares the same value.

```java
Employee e1 = new Employee();
Employee e2 = new Employee();

System.out.println(e1.company);
System.out.println(e2.company);
```

Output

```
OpenAI
OpenAI
```

Changing it

```java
Employee.company = "Tech Corp";
```

affects all objects.

______________________________________________________________________

# final Keyword

Used to prevent modification.

Variable

```java
final int MAX_USERS = 100;
```

Method

```java
final void print() {

}
```

Cannot be overridden.

Class

```java
final class Utility {

}
```

Cannot be inherited.

______________________________________________________________________

# Object Initialization

Bad

```java
Employee emp = new Employee();

emp.name = "John";
emp.age = 25;
```

Better

```java
Employee emp = new Employee("John", 25);
```

We'll learn constructors in the next chapter.

______________________________________________________________________

# Object Lifecycle

```
new

↓

Memory Allocated

↓

Constructor Executes

↓

Object Used

↓

No References Exist

↓

Garbage Collector Removes Object
```

This is why Java developers don't manually free memory.

______________________________________________________________________

# Garbage Collection (High Level)

Objects become eligible for garbage collection when nothing references them.

```java
Employee emp = new Employee();

emp = null;
```

Now the object can be removed later by the JVM.

Garbage collection timing is **not deterministic**.

______________________________________________________________________

# Common Mistakes

## Forgetting `new`

Wrong

```java
Employee emp;

emp.name = "John";
```

This causes a compilation error because `emp` doesn't reference an object.

Correct

```java
Employee emp = new Employee();
```

______________________________________________________________________

## Confusing Static and Instance Members

Wrong

```java
Employee.companyName = "ABC";
```

if `companyName` is not static.

Use an object for instance fields.

______________________________________________________________________

## Returning Too Much Data

Avoid classes with dozens of public fields.

Encapsulation (next chapter) solves this.

______________________________________________________________________

## Using `==` for Objects

Wrong

```java
String a = new String("Java");
String b = new String("Java");

System.out.println(a == b);
```

Correct

```java
System.out.println(a.equals(b));
```

We'll discuss this in more detail later.

______________________________________________________________________

# Best Practices

✅ Keep classes focused on a single responsibility.

✅ Prefer meaningful class names.

✅ Keep methods small.

✅ Hide implementation details.

✅ Initialize objects properly.

✅ Minimize mutable state.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between a class and an object?

### Answer

A class is a blueprint or template that defines the properties and behavior of an entity. It does not occupy memory for
actual data until an object is created.

An object is a runtime instance of a class. Each object has its own state (fields) and behavior (methods), occupies
memory, and can interact with other objects independently.

______________________________________________________________________

## Question

What is the difference between instance variables and static variables?

### Answer

Instance variables belong to individual objects, so each object has its own copy.

Static variables belong to the class itself and are shared among all instances. If one object changes a static variable,
the updated value is visible to every other object.

______________________________________________________________________

## Question

What does the `new` keyword do?

### Answer

The `new` keyword allocates memory for an object, invokes the appropriate constructor to initialize it, and returns a
reference to the newly created object.

______________________________________________________________________

# Practice Questions

1. What is Object-Oriented Programming?
1. What is the difference between a class and an object?
1. What is the purpose of the `new` keyword?
1. What is the difference between instance and static members?
1. Explain the `this` keyword.
1. What is object state and behavior?
1. What is garbage collection?
1. When does an object become eligible for garbage collection?
1. What is the difference between local variables and instance variables?
1. What is the purpose of the `final` keyword?

______________________________________________________________________

# Summary

In this chapter, you learned the core building blocks of Object-Oriented Programming in Java:

- Classes
- Objects
- Object creation
- References
- State and behavior
- Instance vs static members
- `this`
- `final`
- Object lifecycle
- Garbage collection (high level)

These concepts are fundamental because every Java framework—from Spring Boot to Hibernate—builds upon them.

In the next chapter, we'll explore **constructors**, object initialization, constructor overloading, constructor
chaining, immutable objects, and common interview questions around object creation.

______________________________________________________________________

# Next

[Classes, Objects & Constructors](03-classes-objects-and-constructors.md)

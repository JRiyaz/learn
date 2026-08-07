# Access Modifiers & Packages

One of the primary goals of Object-Oriented Programming is **encapsulation**.

Encapsulation means:

> Hide implementation details and expose only what is necessary.

Java achieves this using **Access Modifiers**.

Every Java interview—from junior to senior—includes questions on access modifiers because they determine how classes,
methods, constructors, and variables can be accessed.

______________________________________________________________________

# Why Access Modifiers Matter

Imagine this class.

```java
class BankAccount {

    double balance;

}
```

Now any code can do this.

```java
BankAccount account = new BankAccount();

account.balance = -100000;
```

That's dangerous.

Instead,

```java
class BankAccount {

    private double balance;

}
```

Now nobody can directly modify the balance.

Only the class itself controls how balance changes.

This is encapsulation.

______________________________________________________________________

# Four Access Modifiers

Java provides four levels of access.

| Modifier | Same Class | Same Package | Subclass | Other Package |
|-----------|------------|--------------|----------|---------------|
| private | ✅ | ❌ | ❌ | ❌ |
| default | ✅ | ✅ | ❌ | ❌ |
| protected | ✅ | ✅ | ✅ | ❌\* |
| public | ✅ | ✅ | ✅ | ✅ |

\* Protected members are accessible from subclasses in different packages.

______________________________________________________________________

# 1. private

The most restrictive modifier.

Accessible only inside the same class.

```java
class Employee {

    private String name;

}
```

Allowed

```java
class Employee {

    private String name;

    void print() {
        System.out.println(name);
    }

}
```

Not allowed

```java
Employee emp = new Employee();

emp.name = "Riyaz";
```

Compilation error.

______________________________________________________________________

# Why Use private?

Suppose salary should never become negative.

Wrong

```java
employee.salary = -5000;
```

Correct

```java
class Employee {

    private double salary;

    public void setSalary(double salary) {

        if (salary >= 0) {
            this.salary = salary;
        }

    }

}
```

Now validation happens automatically.

______________________________________________________________________

# 2. Default (Package-Private)

If no modifier is specified,

Java uses **default access**.

```java
class Employee {

    String department;

}
```

No keyword.

This member is accessible only inside the same package.

Example

Package

```
company.hr
```

Employee.java

```java
class Employee {

    String department = "HR";

}
```

Manager.java

```java
class Manager {

    void print() {

        Employee emp = new Employee();

        System.out.println(emp.department);

    }

}
```

Works because both classes are in the same package.

______________________________________________________________________

# 3. protected

Protected is slightly more flexible.

Accessible

- Same class
- Same package
- Subclasses

Example

```java
class Animal {

    protected void eat() {

        System.out.println("Eating");

    }

}
```

Subclass

```java
class Dog extends Animal {

    void print() {

        eat();

    }

}
```

Works.

______________________________________________________________________

# protected Across Packages

Package

```
animals
```

```java
public class Animal {

    protected void eat() {

    }

}
```

Package

```
pets
```

```java
public class Dog extends Animal {

    void print() {

        eat();

    }

}
```

Works because Dog inherits Animal.

But

```java
Animal animal = new Animal();

animal.eat();
```

Doesn't work from another package.

______________________________________________________________________

# 4. public

Accessible everywhere.

```java
public class Employee {

    public String name;

}
```

Any package.

Any class.

Can access it.

______________________________________________________________________

# Access Modifier Summary

## private

```
Current Class Only
```

______________________________________________________________________

## default

```
Current Package
```

______________________________________________________________________

## protected

```
Current Package

+

Child Classes
```

______________________________________________________________________

## public

```
Everywhere
```

______________________________________________________________________

# Access Modifiers on Methods

```java
class Calculator {

    public int add(int a,int b){

        return a+b;

    }

}
```

Anyone can call

```java
Calculator calc = new Calculator();

calc.add(10,20);
```

______________________________________________________________________

Private Method

```java
class UserService {

    public void login() {

        validate();

    }

    private void validate() {

    }

}
```

Outside code

cannot call

```java
validate();
```

______________________________________________________________________

# Access Modifiers on Constructors

Public

```java
public Employee(){

}
```

Anyone can create objects.

______________________________________________________________________

Private Constructor

```java
class Database {

    private Database(){

    }

}
```

No object can be created.

Useful for

- Singleton Pattern
- Utility Classes

______________________________________________________________________

Example

```java
class MathUtil {

    private MathUtil(){}

}
```

Nobody should create

```java
new MathUtil();
```

because all methods are static.

______________________________________________________________________

# Access Modifiers on Classes

Only two are allowed for top-level classes.

```
public

default
```

This is illegal.

```java
private class Employee {

}
```

Also illegal

```java
protected class Employee {

}
```

______________________________________________________________________

# Encapsulation

One of the most important OOP principles.

Bad

```java
class Employee {

    public double salary;

}
```

Anyone can modify salary.

______________________________________________________________________

Good

```java
class Employee {

    private double salary;

    public double getSalary(){

        return salary;

    }

    public void setSalary(double salary){

        if(salary>=0){

            this.salary = salary;

        }

    }

}
```

Now

all updates go through validation.

______________________________________________________________________

# Getters

Getter returns a value.

```java
public String getName(){

    return name;

}
```

______________________________________________________________________

# Setters

Setter updates a value.

```java
public void setName(String name){

    this.name = name;

}
```

______________________________________________________________________

# JavaBeans Convention

Private fields.

Public getters.

Public setters.

```java
private String name;

public String getName(){

}

public void setName(String name){

}
```

Spring Boot

Hibernate

Jackson

All rely heavily on this convention.

______________________________________________________________________

# Packages

Packages organize related classes.

Without packages

```
5000 Java files

inside one folder
```

Chaos.

Packages solve this.

______________________________________________________________________

# Package Declaration

Always the first statement.

```java
package com.company.employee;
```

Example

```java
package com.riyaz.backend.auth;
```

______________________________________________________________________

# Import

Without import

```java
java.util.ArrayList list =
    new java.util.ArrayList();
```

With import

```java
import java.util.ArrayList;
```

Now

```java
ArrayList<String> list =
    new ArrayList<>();
```

Much cleaner.

______________________________________________________________________

# Import Entire Package

```java
import java.util.*;
```

Works.

But avoid it in production.

Prefer

```java
import java.util.List;

import java.util.Map;
```

Explicit imports improve readability.

______________________________________________________________________

# Naming Packages

Convention

Lowercase.

Good

```
com.company.auth

com.company.user

com.company.service
```

Bad

```
Employee

USER

JAVA
```

______________________________________________________________________

# Typical Spring Boot Structure

```
src

└── main

    └── java

        └── com

            └── company

                ├── controller

                ├── service

                ├── repository

                ├── entity

                ├── dto

                ├── config

                ├── security

                └── exception
```

You'll see this in almost every Spring Boot project.

______________________________________________________________________

# When Should Something Be private?

Almost always.

Good practice:

Start with

```
private
```

Increase visibility only when necessary.

This principle is called

**Least Privilege**.

______________________________________________________________________

# Common Mistakes

## Making Everything public

Wrong

```java
public String name;

public int age;

public double salary;
```

Encapsulation is lost.

______________________________________________________________________

## Using Getters and Setters for Everything

Don't automatically generate setters.

Ask

Should this field change?

Example

Employee ID usually shouldn't.

```java
private final int employeeId;
```

No setter.

______________________________________________________________________

## Forgetting Packages

Keeping every class in one package leads to poor project organization.

______________________________________________________________________

## Using Wildcard Imports Everywhere

Avoid

```java
import java.util.*;
```

Prefer explicit imports.

______________________________________________________________________

# Best Practices

✅ Keep fields private.

✅ Expose behavior, not data.

✅ Organize classes into logical packages.

✅ Minimize public APIs.

✅ Follow JavaBeans naming conventions.

✅ Use package names in lowercase.

______________________________________________________________________

# Interview Deep Dive

## Question

What is encapsulation?

### Answer

Encapsulation is the process of hiding an object's internal implementation and exposing only the operations necessary
for external interaction. In Java, this is typically achieved using private fields and public methods (getters, setters,
or business methods) that control access to those fields.

______________________________________________________________________

## Question

Why should fields usually be private?

### Answer

Private fields prevent external code from modifying an object's internal state directly. This allows the class to
validate input, enforce business rules, maintain invariants, and change its internal implementation without affecting
other parts of the application.

______________________________________________________________________

## Question

What is the difference between protected and default access?

### Answer

Default (package-private) members are accessible only within the same package.

Protected members are accessible within the same package and also from subclasses, even if those subclasses are located
in different packages.

______________________________________________________________________

## Question

Can a top-level class be private?

### Answer

No. Top-level classes can only be `public` or package-private (default). Only nested classes can be declared `private`,
`protected`, or `public`.

______________________________________________________________________

## Question

Why do Spring Boot and Hibernate prefer private fields?

### Answer

Private fields support encapsulation and allow frameworks to interact with objects through constructors, getters,
setters, or reflection while preserving control over the object's state.

______________________________________________________________________

# Practice Questions

1. What are the four access modifiers in Java?
1. What is the difference between `private` and `protected`?
1. What is package-private access?
1. Why should fields usually be private?
1. What is encapsulation?
1. Why do we use getters and setters?
1. Can constructors be private?
1. Can a top-level class be protected?
1. What is the purpose of packages?
1. Why should wildcard imports generally be avoided?

______________________________________________________________________

# Summary

Access modifiers are the foundation of encapsulation in Java.

In this chapter, you learned:

- `private`, `default`, `protected`, and `public`
- Access control for classes, methods, fields, and constructors
- Encapsulation
- Getters and setters
- JavaBeans conventions
- Packages and imports
- Package organization best practices

Strong Java developers expose **behavior**, not **internal state**. By keeping fields private and organizing code into
well-structured packages, you create applications that are easier to maintain, extend, and test.

______________________________________________________________________

# Next

[Inheritance, Polymorphism & Abstraction](05-inheritance-polymorphism-abstraction.md)

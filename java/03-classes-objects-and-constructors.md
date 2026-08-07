# Classes, Objects & Constructors

Constructors are one of the most frequently asked Java interview topics.

Every object in Java is created using a constructor.

Understanding constructors is essential because almost every Java framework (Spring Boot, Hibernate, JPA, Jackson, etc.)
relies heavily on them.

______________________________________________________________________

# What is a Constructor?

A constructor is a special method that is automatically called when an object is created.

Its purpose is to initialize the object.

Example

```java
class Employee {

    Employee() {
        System.out.println("Employee Created");
    }

}
```

Creating an object

```java
Employee emp = new Employee();
```

Output

```
Employee Created
```

The constructor executes automatically.

______________________________________________________________________

# Constructor Characteristics

A constructor

- Has the same name as the class.
- Has no return type.
- Executes automatically.
- Can be overloaded.
- Cannot be overridden.
- Can call another constructor.

______________________________________________________________________

# Constructor vs Method

Constructor

```java
class Employee {

    Employee() {

    }

}
```

Method

```java
class Employee {

    void Employee() {

    }

}
```

Notice

Methods have return types.

Constructors do not.

______________________________________________________________________

# Default Constructor

If you don't create any constructor, Java provides one automatically.

Example

```java
class User {

}
```

Java internally creates

```java
User() {

}
```

This is called the **default constructor**.

______________________________________________________________________

# Important Rule

The compiler provides a default constructor **only if you don't create any constructor yourself.**

Example

```java
class User {

    User(String name) {

    }

}
```

Now this is invalid

```java
User user = new User();
```

Compilation error

Because Java no longer creates the default constructor.

______________________________________________________________________

# No-Argument Constructor

This is different from the compiler-generated constructor.

You write it yourself.

```java
class Employee {

    Employee() {

        System.out.println("Employee Created");

    }

}
```

______________________________________________________________________

# Parameterized Constructor

Most objects need initial values.

Example

```java
class Employee {

    String name;

    int age;

    Employee(String name, int age) {

        this.name = name;
        this.age = age;

    }

}
```

Usage

```java
Employee emp = new Employee("Riyaz", 28);
```

______________________________________________________________________

# Why Constructors Matter

Without constructors

```java
Employee emp = new Employee();

emp.name = "Riyaz";
emp.age = 28;
```

With constructors

```java
Employee emp = new Employee("Riyaz", 28);
```

Cleaner.

Safer.

Less error-prone.

______________________________________________________________________

# Using this

Parameters often have the same names as fields.

```java
class User {

    String name;

    User(String name) {

        this.name = name;

    }

}
```

Without `this`

```java
name = name;
```

Nothing happens.

The parameter simply assigns to itself.

______________________________________________________________________

# Constructor Overloading

Multiple constructors can exist.

```java
class User {

    User() {

    }

    User(String name) {

    }

    User(String name, int age) {

    }

}
```

Java automatically chooses the correct constructor.

______________________________________________________________________

# Example

```java
User u1 = new User();

User u2 = new User("Riyaz");

User u3 = new User("Riyaz", 28);
```

______________________________________________________________________

# Constructor Chaining

One constructor can call another.

Using

```java
this()
```

Example

```java
class Employee {

    String name;
    int age;

    Employee() {
        this("Unknown", 0);
    }

    Employee(String name, int age) {
        this.name = name;
        this.age = age;
    }

}
```

Now

```java
Employee emp = new Employee();
```

internally becomes

```java
Employee("Unknown",0)
```

______________________________________________________________________

# Rules for this()

Must be the first statement.

Correct

```java
Employee() {

    this("Unknown");

}
```

Wrong

```java
Employee() {

    System.out.println();

    this("Unknown");

}
```

Compilation error.

______________________________________________________________________

# Calling Parent Constructor

Use

```java
super()
```

Example

```java
class Animal {

    Animal() {
        System.out.println("Animal");
    }

}

class Dog extends Animal {

    Dog() {
        super();
        System.out.println("Dog");
    }

}
```

Output

```
Animal

Dog
```

We'll study inheritance later.

______________________________________________________________________

# Constructor Execution Order

Example

```java
class Parent {

    Parent() {
        System.out.println("Parent");
    }

}

class Child extends Parent {

    Child() {
        System.out.println("Child");
    }

}
```

Output

```
Parent

Child
```

Parent constructor always executes first.

______________________________________________________________________

# Initializing Objects Properly

Bad

```java
Employee emp = new Employee();

emp.name = "Alice";

emp.age = 25;

emp.salary = 50000;
```

Better

```java
Employee emp =
    new Employee("Alice",25,50000);
```

Object is always valid.

______________________________________________________________________

# Copy Constructor Pattern

Java doesn't have built-in copy constructors like C++.

We usually write our own.

```java
class Employee {

    String name;

    int age;

    Employee(Employee other) {

        this.name = other.name;

        this.age = other.age;

    }

}
```

Usage

```java
Employee e1 = new Employee("Riyaz",28);

Employee e2 = new Employee(e1);
```

Now

```
e2
```

contains the same values.

______________________________________________________________________

# Constructor vs Setter

Constructor

```java
Employee emp =
    new Employee("Riyaz",28);
```

Setter

```java
Employee emp = new Employee();

emp.setName("Riyaz");

emp.setAge(28);
```

Use constructors when fields are mandatory.

Use setters for optional updates.

______________________________________________________________________

# Immutable Objects

One of the most important interview topics.

Example

```java
final class Employee {

    private final String name;

    private final int age;

    Employee(String name,int age){

        this.name = name;

        this.age = age;

    }

    public String getName(){

        return name;

    }

    public int getAge(){

        return age;

    }

}
```

Notice

No setters.

Once created,

the object never changes.

Benefits

- Thread-safe
- Easy to reason about
- Safer
- Reliable

______________________________________________________________________

# Constructor Initialization Blocks

Less common but asked occasionally.

```java
class Demo {

    {

        System.out.println("Instance Block");

    }

    Demo(){

        System.out.println("Constructor");

    }

}
```

Output

```
Instance Block

Constructor
```

Initialization block executes before constructor.

______________________________________________________________________

# Static Initialization Block

Runs only once.

```java
class Config {

    static {

        System.out.println("Loaded");

    }

}
```

Useful for

- loading configuration
- initializing static resources

______________________________________________________________________

# Order of Execution

```
Static Variables

↓

Static Block

↓

Instance Variables

↓

Instance Block

↓

Constructor
```

Frequently asked interview question.

______________________________________________________________________

# Builder Pattern (Introduction)

Suppose

```java
Employee(
name,
age,
salary,
email,
phone,
address,
manager,
department
)
```

Not very readable.

Builder Pattern

```java
Employee employee =
    new Employee.Builder()
        .setName("Riyaz")
        .setAge(28)
        .setSalary(50000)
        .build();
```

Much cleaner.

We'll discuss Builder in design patterns.

______________________________________________________________________

# Common Mistakes

## Forgetting to initialize fields

Wrong

```java
Employee(String name){

}
```

Correct

```java
this.name = name;
```

______________________________________________________________________

## Too Many Constructors

Avoid

```java
Employee()

Employee(String)

Employee(String,int)

Employee(String,int,double)

Employee(String,int,double,String)
```

Prefer Builder Pattern.

______________________________________________________________________

## Heavy Constructors

Bad

```java
Employee(){

    connectDatabase();

    callAPI();

    readFile();

}
```

Constructors should initialize objects,

not perform business logic.

______________________________________________________________________

## Returning Values

Wrong

```java
Employee(){

    return;

}
```

Constructors never return values.

______________________________________________________________________

# Best Practices

✅ Keep constructors simple.

✅ Initialize mandatory fields.

✅ Validate input.

✅ Prefer immutable objects.

✅ Avoid complex logic.

✅ Use constructor chaining.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between a constructor and a method?

### Answer

A constructor initializes an object and is invoked automatically when an object is created. It has the same name as the
class and does not declare a return type.

A method defines behavior, can have any valid name, declares a return type (or `void`), and must be called explicitly.

______________________________________________________________________

## Question

Why do we use `this` inside constructors?

### Answer

The `this` keyword refers to the current object. Inside constructors, it is commonly used to distinguish instance
variables from constructor parameters when they have the same name.

______________________________________________________________________

## Question

What is constructor overloading?

### Answer

Constructor overloading means defining multiple constructors in the same class with different parameter lists. It allows
objects to be initialized in different ways while using the same class.

______________________________________________________________________

## Question

What is constructor chaining?

### Answer

Constructor chaining is the process of calling one constructor from another using `this()` or calling the parent class
constructor using `super()`. It reduces duplicate initialization code and improves maintainability.

______________________________________________________________________

## Question

Why are immutable classes useful?

### Answer

Immutable classes cannot change after creation. They are inherently thread-safe, easier to reason about, safer to share
between threads, and commonly used in Java libraries, such as `String` and wrapper classes.

______________________________________________________________________

# Practice Questions

1. What is a constructor?
1. What is the difference between a default constructor and a no-argument constructor?
1. Can constructors be overloaded?
1. Can constructors be overridden?
1. What is constructor chaining?
1. What is the purpose of `this()`?
1. What is the purpose of `super()`?
1. Why should constructors avoid heavy business logic?
1. What is a copy constructor?
1. What are immutable objects, and why are they useful?

______________________________________________________________________

# Summary

Constructors are responsible for creating valid objects.

In this chapter, you learned:

- Constructors and their characteristics
- Default and parameterized constructors
- Constructor overloading
- Constructor chaining
- `this()` and `super()`
- Copy constructor pattern
- Immutable objects
- Static and instance initialization blocks
- Builder Pattern (introduction)

Mastering constructors is essential because nearly every Java framework uses them extensively for dependency injection,
object creation, and configuration.

______________________________________________________________________

# Next

[Access Modifiers & Packages](04-access-modifiers-and-packages.md)

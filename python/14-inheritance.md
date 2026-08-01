# File: python/14-inheritance.md

# Python Advanced - Lesson 14

# Inheritance - Reusing and Extending Behaviour

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced OOP
>
> **Lesson:** 14
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 90 Minutes

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why inheritance exists
- The "is-a" relationship
- Parent and child classes
- Method inheritance
- Method overriding
- Using `super()`
- Constructor inheritance
- When inheritance should and should not be used
- Production examples

______________________________________________________________________

# Why Does Inheritance Exist?

Imagine you're building an HR system.

Every employee has:

- ID
- Name
- Email

Developers also have:

- Programming language

Managers have:

- Team size

A beginner might write:

```python
class Developer:

    def __init__(self, id, name, email, language):

        self.id = id
        self.name = name
        self.email = email
        self.language = language


class Manager:

    def __init__(self, id, name, email, team_size):

        self.id = id
        self.name = name
        self.email = email
        self.team_size = team_size
```

Notice the duplication.

```
id

name

email
```

appear in every class.

______________________________________________________________________

# The Problem

Duplicated code leads to:

- More maintenance
- Higher chance of bugs
- Repeated logic
- Difficult refactoring

Inheritance allows us to define common behaviour once.

______________________________________________________________________

# The "is-a" Relationship

Inheritance models an **is-a** relationship.

Examples

```
Developer is an Employee

Manager is an Employee

Dog is an Animal

Car is a Vehicle
```

Notice that each child **is a** specialised version of its parent.

______________________________________________________________________

# Creating a Parent Class

```python
class Employee:

    def __init__(self, id, name, email):

        self.id = id

        self.name = name

        self.email = email
```

This contains everything common to all employees.

______________________________________________________________________

# Creating a Child Class

```python
class Developer(Employee):

    pass
```

The syntax

```python
(Employee)
```

means

```
Developer inherits Employee
```

______________________________________________________________________

# Inheriting Methods

```python
class Employee:

    def introduce(self):

        print("I am an employee.")
```

```python
class Developer(Employee):

    pass
```

Usage

```python
developer = Developer()

developer.introduce()
```

Output

```
I am an employee.
```

The method is inherited automatically.

______________________________________________________________________

# Constructor Inheritance

Consider this class.

```python
class Employee:

    def __init__(self, name):

        self.name = name
```

Child class

```python
class Developer(Employee):

    pass
```

Usage

```python
developer = Developer("Alice")

print(developer.name)
```

Output

```
Alice
```

Python automatically inherits the parent's constructor if the child doesn't define one.

______________________________________________________________________

# Adding Child-Specific Behaviour

Developers need one extra field.

```python
class Employee:

    def __init__(self, name):

        self.name = name
```

```python
class Developer(Employee):

    def __init__(self, name, language):

        self.name = name

        self.language = language
```

This works.

But something is wrong.

______________________________________________________________________

# The Problem

Notice this line.

```python
self.name = name
```

We're rewriting logic that already exists.

This violates the DRY principle.

(Don't Repeat Yourself)

______________________________________________________________________

# Introducing super()

Python provides

```python
super()
```

to access the parent class.

Example

```python
class Employee:

    def __init__(self, name):

        self.name = name
```

```python
class Developer(Employee):

    def __init__(self, name, language):

        super().__init__(name)

        self.language = language
```

Usage

```python
developer = Developer(
    "Alice",
    "Python"
)

print(developer.name)

print(developer.language)
```

Output

```
Alice

Python
```

______________________________________________________________________

# What Does super() Do?

When Python sees

```python
super().__init__(name)
```

it executes

```python
Employee.__init__(self, name)
```

But you don't need to pass `self`.

Python does that automatically.

______________________________________________________________________

# Method Overriding

A child class can replace a parent's method.

Parent

```python
class Employee:

    def work(self):

        print("Working...")
```

Child

```python
class Developer(Employee):

    def work(self):

        print("Writing Python code.")
```

Usage

```python
developer = Developer()

developer.work()
```

Output

```
Writing Python code.
```

The child overrides the parent's implementation.

______________________________________________________________________

# Calling the Parent Method

Sometimes you want both behaviours.

```python
class Employee:

    def work(self):

        print("Starting work.")
```

```python
class Developer(Employee):

    def work(self):

        super().work()

        print("Writing backend APIs.")
```

Output

```
Starting work.

Writing backend APIs.
```

This extends the parent's behaviour instead of replacing it completely.

______________________________________________________________________

# Visualising Inheritance

```
          Employee
         /        \
        /          \
 Developer      Manager
```

Both classes inherit common functionality.

______________________________________________________________________

# isinstance()

Python provides

```python
isinstance()
```

to check object types.

```python
developer = Developer(
    "Alice",
    "Python"
)

print(isinstance(
    developer,
    Developer
))

print(isinstance(
    developer,
    Employee
))
```

Output

```
True

True
```

A `Developer` is also an `Employee`.

______________________________________________________________________

# issubclass()

To compare classes instead of objects,

use

```python
issubclass()
```

```python
print(
    issubclass(
        Developer,
        Employee
    )
)
```

Output

```
True
```

______________________________________________________________________

# When Should You Use Inheritance?

Good examples

```
Employee
    ↓
Developer

Vehicle
    ↓
Car

Animal
    ↓
Dog
```

Each child is a specialised version of its parent.

______________________________________________________________________

# When Should You Avoid Inheritance?

Suppose you have:

```
User
```

and

```
Database
```

Should you write

```
User(Database)
```

No.

A user is **not** a database.

Instead,

the user **has a** database connection.

This is composition, which we'll study later.

______________________________________________________________________

# Production Example

Imagine a notification system.

```python
class Notification:

    def send(self):

        raise NotImplementedError
```

Child classes

```python
class EmailNotification(Notification):

    def send(self):

        print("Sending email")
```

```python
class SMSNotification(Notification):

    def send(self):

        print("Sending SMS")
```

Every notification shares the same interface,

but each implements it differently.

______________________________________________________________________

# Production Insight

Inheritance is used in many Python frameworks.

Examples include:

Django

```python
class UserView(View):
    ...
```

Flask

```python
class MyCommand(AppGroup):
    ...
```

Exception hierarchy

```python
Exception

↓

ValueError

↓

UnicodeError
```

However,

modern Python encourages **composition over inheritance** for many designs because it produces more flexible and loosely
coupled code.

______________________________________________________________________

# Best Practices

✅ Use inheritance only for genuine **is-a** relationships.

✅ Reuse common behaviour through the parent class.

✅ Use `super()` instead of duplicating code.

✅ Keep inheritance hierarchies shallow.

❌ Don't inherit simply to reuse unrelated code.

❌ Don't create deep inheritance chains.

______________________________________________________________________

# Questions

### Question

> What is inheritance?

### Answer

Inheritance allows one class to reuse and extend the behaviour of another class. The child class automatically inherits
the attributes and methods of the parent class and may override or extend them.

______________________________________________________________________

### Question

> What does `super()` do?

### Answer

`super()` provides access to the parent class. It is commonly used to call the parent's constructor or methods without
explicitly referring to the parent class by name.

______________________________________________________________________

### Question

> When should inheritance be avoided?

### Answer

Inheritance should be avoided when there is no true **is-a** relationship. In such cases, composition is usually a
better design because it creates looser coupling and greater flexibility.

______________________________________________________________________

# Practical Lesson

Create a file:

```
inheritance_examples.py
```

```python
class Employee:

    def __init__(self, name):

        self.name = name

    def introduce(self):

        print(f"I am {self.name}.")


class Developer(Employee):

    def __init__(self, name, language):

        super().__init__(name)

        self.language = language

    def introduce(self):

        super().introduce()

        print(
            f"I write {self.language}."
        )


developer = Developer(
    "Alice",
    "Python"
)

developer.introduce()
```

Expected Output

```
I am Alice.

I write Python.
```

______________________________________________________________________

# Questions

## Question 1

What is inheritance?

### Answer

Inheritance is an object-oriented mechanism that allows one class to acquire and extend the attributes and methods of
another class.

______________________________________________________________________

## Question 2

What is the difference between a parent class and a child class?

### Answer

A parent class defines shared behaviour, while a child class inherits that behaviour and may add new functionality or
override existing methods.

______________________________________________________________________

## Question 3

Why should `super()` be used?

### Answer

`super()` allows child classes to reuse the parent's implementation, reducing duplication and making code easier to
maintain.

______________________________________________________________________

## Question 4

What is method overriding?

### Answer

Method overriding occurs when a child class provides its own implementation of a method already defined in the parent
class.

______________________________________________________________________

## Question 5

What is the "is-a" relationship?

### Answer

It describes a situation where a child class is a specialised version of its parent class, such as a `Developer` being
an `Employee`.

______________________________________________________________________

# Assignment

## Exercise 1

Create a `Vehicle` class.

Create `Car` and `Bike` classes that inherit from it.

Add one method unique to each child.

______________________________________________________________________

## Exercise 2

Override a method in the child class and call the parent's version using `super()`.

Observe the order of execution.

______________________________________________________________________

## Exercise 3

Use `isinstance()` and `issubclass()` to verify the inheritance relationships.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why inheritance exists.
- ✅ The "is-a" relationship.
- ✅ Parent and child classes.
- ✅ Constructor inheritance.
- ✅ Method overriding.
- ✅ How `super()` works.
- ✅ `isinstance()` and `issubclass()`.
- ✅ Production best practices for using inheritance.

______________________________________________________________________

# What's Next

**File:** [15-Multiple-Inheritance-MRO](15-multiple-inheritance-mro.md)

Topics:

- Multiple Inheritance
- The Diamond Problem
- Method Resolution Order (MRO)
- `super()` in Multiple Inheritance
- `mro()` and `__mro__`
- Cooperative Multiple Inheritance
- Production Examples

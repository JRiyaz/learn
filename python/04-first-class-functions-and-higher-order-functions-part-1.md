# File: python/04-first-class-functions-and-higher-order-functions-part-1.md

# Python Advanced - Lesson 04 (Part 1)
# First-Class Functions & Higher-Order Functions

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 04 (Part 1)
>
> **Difficulty:** ⭐⭐⭐☆☆
>
> **Estimated Time:** 60 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- What first-class functions are
- Why functions are objects in Python
- Assigning functions to variables
- Passing functions as arguments
- Returning functions from functions
- What higher-order functions are
- Why these concepts are the foundation of decorators

---

# Why Should You Learn This?

Many Python features are built on one simple idea:

> **Functions are objects.**

Once you understand this, concepts like:

- Decorators
- FastAPI Dependency Injection
- Middleware
- Callbacks
- Event Handlers
- Functional Programming

become much easier to understand.

---

# Theory

In Python, functions are **first-class objects**.

That means a function can:

- Be assigned to a variable
- Be passed as an argument
- Be returned from another function
- Be stored inside data structures
- Be treated like any other object

For example:

```python
def greet():
    print("Hello")
```

Most beginners think `greet` is just a function.

Internally, it's also an object.

```
Function Object

↓

greet
```

---

# Example 1 - Functions are Objects

```python
def greet():
    print("Hello!")

# Print the function object itself.
print(greet)
```

Output

```
<function greet at 0x...>
```

Notice something important.

The function did **not** execute.

Python printed the function object.

Now compare it with:

```python
def greet():
    print("Hello!")

# Parentheses execute the function.
greet()
```

Output

```
Hello!
```

---

# Function vs Function Call

This distinction is extremely important.

```python
greet
```

means

```
The function object
```

Whereas

```python
greet()
```

means

```
Execute the function
```

Think of it like this:

```
Remote Control

↓

TV

Remote Control Button

↓

TV Turns On
```

Owning the remote isn't the same as pressing the button.

Similarly, referring to a function isn't the same as calling it.

---

# Example 2 - Assigning a Function to a Variable

```python
def greet():
    print("Hello!")

# Store the function object.
say_hello = greet

# Execute through the new variable.
say_hello()
```

Output

```
Hello!
```

Visualization

```
        Function Object

             ▲
             │
      greet      say_hello
```

Both variables point to the same function object.

---

# Example 3 - Multiple References

```python
def multiply(a, b):
    return a * b

operation = multiply

print(operation(5, 6))
```

Output

```
30
```

Again,

no new function was created.

Only another reference.

---

# Passing Functions as Arguments

Since functions are objects,

they can be passed to another function.

Example:

```python
def greet():
    print("Welcome!")

def execute(func):
    func()

execute(greet)
```

Output

```
Welcome!
```

Notice carefully:

```python
execute(greet)
```

NOT

```python
execute(greet())
```

Why?

Because we want to pass the function itself,

not the result of executing it.

---

# Example 4

```python
def square(number):
    return number * number

def calculate(value, operation):
    """
    Apply any operation passed to this function.
    """
    return operation(value)

result = calculate(5, square)

print(result)
```

Output

```
25
```

Visualization

```
calculate()

↓

operation

↓

square()

↓

25
```

The `calculate()` function doesn't know how to square numbers.

It simply executes whichever function it receives.

---

# Returning Functions

Just as functions can receive functions,

they can also return them.

Example:

```python
def choose_operation():

    def greet():
        print("Hello!")

    return greet

function = choose_operation()

function()
```

Output

```
Hello!
```

Here,

`choose_operation()` returns the function object.

It does **not** execute it.

---

# Higher-Order Functions

A **Higher-Order Function** is simply a function that:

- Accepts another function as an argument, **or**
- Returns another function.

Examples:

```
map()

filter()

sorted()

reduce()

custom decorators
```

All of these are higher-order functions.

---

# Example 5

```python
def cube(number):
    return number ** 3

def process(value, operation):
    return operation(value)

print(process(3, cube))
```

Output

```
27
```

The `process()` function is a higher-order function because it accepts another function.

---

# Why Are Higher-Order Functions Useful?

Imagine writing this:

```python
calculate_square()

calculate_cube()

calculate_double()

calculate_half()

calculate_percentage()
```

You would need many separate functions.

Instead,

one reusable function can perform any operation.

```python
process(value, operation)
```

The behaviour changes depending on the function passed to it.

This makes code:

- Reusable
- Flexible
- Easier to maintain

---

# Production Insight

Suppose you're building a logging utility.

Instead of writing:

```python
log_user_creation()

log_order_creation()

log_payment_creation()
```

You can write one reusable function.

```python
def log_execution(task):
    print("Starting...")

    task()

    print("Finished.")
```

Usage:

```python
def create_user():
    print("Creating user...")

log_execution(create_user)
```

Output

```
Starting...

Creating user...

Finished.
```

This pattern is widely used in:

- FastAPI middleware
- Flask request hooks
- Authentication wrappers
- Retry mechanisms
- Transaction management
- Performance monitoring

In the next lesson, you'll see that **decorators are built using this exact idea**.

---

# Questions

### Question

> What does it mean that functions are first-class objects?

### Answer

> In Python, functions are first-class objects, meaning they can be treated like any other object. They can be assigned to variables, passed as arguments, returned from other functions and stored inside data structures. This flexibility enables powerful features such as decorators, callbacks and dependency injection.

---

### Question

> What is a higher-order function?

### Answer

> A higher-order function is a function that either accepts another function as an argument or returns a function. Python's `map()`, `filter()` and custom decorators are common examples.

---

# Practical Lesson

Create a file:

```
function_objects.py
```

Write the following program.

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def calculate(a, b, operation):
    """
    Execute whichever function
    is passed as 'operation'.
    """
    return operation(a, b)

print(calculate(10, 5, add))

print(calculate(10, 5, subtract))
```

Expected Output

```
15

5
```

Now create another function:

```python
def multiply(a, b):
    return a * b
```

Without changing `calculate()`,

use it to multiply two numbers.

---


# Practical Example - Dependency Injection Using Closures

Imagine you're building a backend application.

Many functions need access to a database connection.

Instead of creating the database connection inside every function, we can inject it.

---

## Without Dependency Injection

```python
class Database:
    def get_users(self):
        return ["Alice", "Bob", "Charlie"]


def get_users():
    """
    BAD DESIGN

    This function creates its own dependency.
    It is tightly coupled to the Database class.
    """

    db = Database()

    return db.get_users()


print(get_users())
```

### Problems

- Difficult to test
- Cannot easily replace the database
- Function is tightly coupled to one implementation

---

## Manual Dependency Injection

```python
class Database:
    def get_users(self):
        return ["Alice", "Bob", "Charlie"]


def get_users(db):
    """
    GOOD DESIGN

    The database is injected from outside.
    """

    return db.get_users()


database = Database()

print(get_users(database))
```

Output

```
['Alice', 'Bob', 'Charlie']
```

Now `get_users()` doesn't care where the database came from.

It simply uses the object it receives.

This is Dependency Injection.

---

## Dependency Injection Using Closures

Closures can "remember" dependencies.

```python
class Database:

    def get_users(self):
        return ["Alice", "Bob", "Charlie"]


def create_user_service(database):
    """
    'database' is captured by the closure.
    """

    def get_users():
        return database.get_users()

    return get_users


db = Database()

# Inject the dependency once.
user_service = create_user_service(db)

print(user_service())
```

Output

```
['Alice', 'Bob', 'Charlie']
```

### Visualization

```
Database Instance

        │
        ▼

create_user_service()

        │
        ▼

Closure remembers database

        │
        ▼

user_service()

        │
        ▼

database.get_users()
```

The `user_service` function continues to access the same `database` object even after `create_user_service()` has finished executing.

---

## Why Is This Useful?

Suppose you want to test your code.

Instead of connecting to a real database, inject a fake one.

```python
class FakeDatabase:

    def get_users(self):
        return ["Test User"]


fake_db = FakeDatabase()

user_service = create_user_service(fake_db)

print(user_service())
```

Output

```
['Test User']
```

Notice that `create_user_service()` didn't change at all.

Only the injected dependency changed.

This makes testing much easier.

---

# How FastAPI Uses This Idea

FastAPI automates dependency injection.

Instead of manually passing dependencies, you write:

```python
from fastapi import Depends


def get_database():
    return Database()


@app.get("/users")
def get_users(db: Database = Depends(get_database)):
    return db.get_users()
```

Here's what happens behind the scenes:

1. A request comes to `/users`.
2. FastAPI sees `Depends(get_database)`.
3. It calls `get_database()` to create or retrieve a `Database` instance.
4. It passes that instance as the `db` argument.
5. Your `get_users()` function simply uses `db`.

Conceptually, it's similar to this manual version:

```python
db = get_database()

get_users(db)
```

FastAPI just performs these steps automatically.

---

# Key Takeaway

Dependency Injection is not about a special library.

It's a design pattern where a function receives the objects it needs instead of creating them itself.

Closures demonstrate how dependencies can be "remembered" and reused, while frameworks like FastAPI automate the injection process to keep your code clean, testable, and loosely coupled.



# Questions

## Question 1

What are first-class functions?

### Answer

First-class functions are functions that can be treated like any other object. They can be assigned to variables, passed as arguments, returned from functions and stored in collections.

---

## Question 2

What is the difference between `greet` and `greet()`?

### Answer

`greet` refers to the function object.

`greet()` executes the function and returns its result.

---

## Question 3

What is a higher-order function?

### Answer

A higher-order function is a function that accepts another function as an argument, returns a function, or both.

---

## Question 4

Why do we pass `square` instead of `square()`?

### Answer

`square` passes the function object.

`square()` executes the function immediately and passes its return value instead.

---

## Question 5

Are all higher-order functions first-class functions?

### Answer

Higher-order functions rely on Python's support for first-class functions. A higher-order function is simply a function that uses first-class functions by accepting or returning them.

---

# Assignment

## Exercise 1

Create three mathematical functions:

- Add
- Multiply
- Divide

Write one generic function that accepts any of these operations as an argument.

---

## Exercise 2

Store three functions inside a list.

Iterate through the list and execute each function.

---

## Exercise 3

Write a function that returns another function which always adds 10 to its input.

Example:

```python
add_ten = create_adder()

print(add_ten(5))
```

Expected Output

```
15
```

---

# Summary

In this lesson, you learned:

- ✅ Functions are objects in Python.
- ✅ Functions can be assigned to variables.
- ✅ Functions can be passed as arguments.
- ✅ Functions can be returned from other functions.
- ✅ Higher-order functions either accept or return functions.
- ✅ These concepts form the foundation for decorators and many backend frameworks.

---

# What's Next

**File:**
[04-First-Class-Functions-and-Higher-Order-Functions-part-2](04-first-class-functions-and-higher-order-functions-part-2.md)

Topics:

- Built-in Higher-Order Functions (`map`, `filter`, `sorted`)
- Lambda Functions
- Function Factories
- Callbacks
- Preparing for Decorators
- Production Examples

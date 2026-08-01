# File: python/03-legb-scope-and-variable-resolution-part-1.md

# Python Advanced - Lesson 03 (Part 1)

# LEGB Scope & Variable Resolution

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 03 (Part 1)
>
> **Difficulty:** ⭐⭐⭐☆☆
>
> **Estimated Time:** 60 Minutes

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What scope is
- Why Python needs scopes
- The LEGB Rule
- Local Scope
- Enclosing Scope
- Global Scope
- Built-in Scope
- Variable Shadowing
- How Python decides which variable to use

______________________________________________________________________

# Why Should You Learn Scope?

One of the most common Python interview questions is:

> **How does Python resolve variables?**

Many developers answer:

> "Python checks the local variable."

That answer is incomplete.

Python follows a well-defined search order called the **LEGB Rule**.

Understanding it is essential because it directly affects:

- Functions
- Closures
- Decorators
- FastAPI Dependency Injection
- Async Programming
- Class Design

______________________________________________________________________

# What is Scope?

A **scope** is the region of your program where a variable is accessible.

Think of scope as a room.

```
Kitchen

↓

Knife
Plate
Glass
```

If you're inside the kitchen, you can use those objects.

Outside the kitchen, you cannot.

Variables work exactly the same way.

______________________________________________________________________

# Example 1

```python
name = "Riyaz"

def greet():
    print(name)

greet()
```

Output

```
Riyaz
```

Question:

How can `greet()` access `name`?

Because Python searched outside the function after not finding a local variable.

We'll soon learn the exact order.

______________________________________________________________________

# The LEGB Rule

Whenever Python encounters a variable,

it searches in this order:

```
L

↓

E

↓

G

↓

B
```

Which means

```
Local

↓

Enclosing

↓

Global

↓

Built-in
```

The moment Python finds the variable,

it stops searching.

______________________________________________________________________

# 1. Local Scope

Local scope means

> Variables created inside the current function.

Example

```python
def greet():
    message = "Hello"

    print(message)

greet()
```

Visualization

```
Function greet()

↓

message

↓

"Hello"
```

Only this function can access `message`.

______________________________________________________________________

# Example 2

```python
def greet():
    message = "Hello"

greet()

print(message)
```

Output

```
NameError
```

Why?

Because `message` only exists inside the function.

When the function finishes,

its local scope disappears.

______________________________________________________________________

# Local Variables Live Only During Function Execution

Example

```python
def calculate():

    total = 100

    print(total)

calculate()
```

After the function returns,

Python destroys the local scope.

This is one reason local variables are memory efficient.

______________________________________________________________________

# 2. Global Scope

Variables created outside every function belong to the global scope.

Example

```python
country = "India"

def show():

    print(country)

show()
```

Output

```
India
```

Visualization

```
Global Scope

↓

country

↓

India



Function

↓

Python doesn't find "country"

↓

Looks in Global Scope

↓

Found
```

______________________________________________________________________

# Example 3

```python
language = "Python"

def developer():

    print(language)

developer()
```

Python searches

```
Local

↓

Global

↓

Found
```

______________________________________________________________________

# 3. Built-in Scope

Python has another scope.

Built-in.

Example

```python
numbers = [1, 2, 3]

print(len(numbers))
```

Question

Where did `len()` come from?

You didn't define it.

Python did.

Functions like

```
print()

len()

sum()

max()

min()

range()

type()

id()
```

all belong to the Built-in scope.

Visualization

```
Built-in Scope

↓

print

↓

len

↓

sum

↓

range

↓

type
```

Every Python program automatically has access to them.

______________________________________________________________________

# Example 4

```python
numbers = [1, 2, 3]

print(max(numbers))
```

Python searches

```
Local

↓

Global

↓

Built-in

↓

Found
```

______________________________________________________________________

# Variable Shadowing

This is another common interview topic.

Suppose you have

```python
name = "Riyaz"

def greet():

    name = "Alice"

    print(name)

greet()

print(name)
```

Output

```
Alice

Riyaz
```

Question

Why?

Visualization

```
Global

↓

name

↓

Riyaz



Function

↓

name

↓

Alice
```

The local variable **shadows**

(or hides)

the global variable.

Python always checks Local Scope first.

______________________________________________________________________

# Example 5

```python
city = "Bangalore"

def office():

    city = "Hyderabad"

    print(city)

office()

print(city)
```

Output

```
Hyderabad

Bangalore
```

Two completely different variables.

______________________________________________________________________

# Production Insight

Suppose you're writing a FastAPI application.

```python
DATABASE_URL = "postgres://localhost"

def connect():

    print(DATABASE_URL)
```

`DATABASE_URL` is a global configuration.

Every function can read it.

Now imagine someone writes

```python
DATABASE_URL = "sqlite.db"
```

inside another function.

Instead of changing the global variable,

they accidentally create a **local variable**.

The application continues using the original global configuration, leading to confusing bugs.

Understanding scope helps avoid mistakes like these.

______________________________________________________________________

# Questions

### Question

> Explain the LEGB Rule.

### Answer

> Python resolves variables using the LEGB Rule. It first searches the Local scope, then the Enclosing scope, followed by the Global scope, and finally the Built-in scope. The search stops as soon as the variable is found.

______________________________________________________________________

### Question

> What is variable shadowing?

### Answer

> Variable shadowing occurs when a variable in an inner scope has the same name as one in an outer scope. The inner variable temporarily hides the outer variable within that scope, but it does not modify or replace the outer variable.

______________________________________________________________________

# Practical Lesson

Create a file

```
scope_demo.py
```

Write the following program.

```python
language = "Python"

def function_one():

    language = "Java"

    print("Function One:", language)

def function_two():

    print("Function Two:", language)

print("Global:", language)

function_one()

function_two()

print("Global:", language)
```

Before running it,

predict every output.

Then execute it and compare your prediction.

______________________________________________________________________

# Questions

## Question 1

What does LEGB stand for?

### Answer

- Local
- Enclosing
- Global
- Built-in

This is the exact order Python follows when resolving variable names.

______________________________________________________________________

## Question 2

Can a function access a global variable?

### Answer

Yes.

If Python does not find the variable in the local scope, it searches the global scope.

______________________________________________________________________

## Question 3

Why does the following code raise an error?

```python
def greet():

    message = "Hello"

greet()

print(message)
```

### Answer

`message` is a local variable.

It only exists while `greet()` is executing.

After the function finishes, the local scope is destroyed.

______________________________________________________________________

## Question 4

What is variable shadowing?

### Answer

Variable shadowing occurs when a variable in an inner scope has the same name as a variable in an outer scope.

The inner variable hides the outer variable within that scope.

______________________________________________________________________

## Question 5

Where does `len()` come from?

### Answer

`len()` belongs to Python's Built-in scope.

It is automatically available in every Python program.

______________________________________________________________________

# Assignment

## Exercise 1

Create one global variable and one local variable with the same name.

Predict the output before executing the program.

______________________________________________________________________

## Exercise 2

Use the following built-in functions and identify which scope they belong to:

- `print()`
- `sum()`
- `type()`
- `max()`
- `range()`

______________________________________________________________________

## Exercise 3

Create three functions.

Give each one a variable named `count`.

Verify that changing one does not affect the others.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What a scope is.
- ✅ Why Python uses scopes.
- ✅ The LEGB Rule.
- ✅ Local Scope.
- ✅ Global Scope.
- ✅ Built-in Scope.
- ✅ Variable Shadowing.
- ✅ How Python resolves variable names.

______________________________________________________________________

# What's Next

**File:** [03-LEGB-Scope-and-Variable-Resolution-part-2](03-legb-scope-and-variable-resolution-part-2.md)

Topics:

- Enclosing Scope
- Nested Functions
- Closures
- `global`
- `nonlocal`
- Real-world Closure Examples
- Common Scope Bugs
- Production Examples

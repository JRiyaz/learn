# File: python/python-advanced-03-legb-scope-and-variable-resolution-part-2.md

# Python Advanced - Lesson 03 (Part 2)
# Enclosing Scope, `global`, `nonlocal` & Closures

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 03 (Part 2)
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 60-75 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- What Enclosing Scope is
- How nested functions work
- What `global` does
- What `nonlocal` does
- The difference between `global` and `nonlocal`
- What a Closure is
- Where closures are used in real backend applications

---

# Theory

In the previous lesson, we learned three parts of the LEGB rule:

```
L → E → G → B

Local
Enclosing
Global
Built-in
```

We already covered:

- Local
- Global
- Built-in

Now let's learn the missing piece:

**Enclosing Scope**

---

# What is Enclosing Scope?

An enclosing scope exists when a function is defined inside another function.

Example:

```python
def outer():

    message = "Hello"

    def inner():
        print(message)

    inner()

outer()
```

Output

```
Hello
```

Question:

How can `inner()` access `message`?

Because `message` belongs to the **enclosing function**.

---

Visualization

```
outer()

↓

message = "Hello"

↓

inner()

↓

print(message)
```

Python searches

```
Local

↓

Enclosing

↓

Found
```

---

# Example 1

```python
def company():

    company_name = "OpenAI"

    def employee():

        print(company_name)

    employee()

company()
```

Output

```
OpenAI
```

Python searches

```
Local

↓

Enclosing

↓

Found
```

---

# Nested Functions

Functions can be defined inside other functions.

```python
def outer():

    print("Outer Function")

    def inner():

        print("Inner Function")

    inner()

outer()
```

Output

```
Outer Function

Inner Function
```

Nested functions are commonly used for:

- Closures
- Decorators
- Encapsulation
- Helper functions

---

# What Happens if Python Cannot Find a Variable?

Example

```python
country = "India"

def outer():

    city = "Bangalore"

    def inner():

        print(country)

    inner()

outer()
```

Python searches

```
Local

↓

Enclosing

↓

Global

↓

Found
```

This demonstrates the complete LEGB search order.

---

# Modifying a Global Variable

Consider the following code.

```python
count = 10

def increase():

    count = count + 1

increase()
```

Output

```
UnboundLocalError
```

Why?

Python sees

```python
count = count + 1
```

and assumes `count` is a **local variable** because it is assigned inside the function.

However, it tries to read it before it has been assigned.

---

# The `global` Keyword

If you want to modify a global variable inside a function, use `global`.

```python
count = 10

def increase():

    global count

    count += 1

increase()

print(count)
```

Output

```
11
```

Now Python knows you mean the global variable.

---

Visualization

```
Global Scope

↓

count = 10

↓

increase()

↓

global count

↓

Modify Global Variable
```

---

# When Should You Use `global`?

Technically, you can.

Practically, you should avoid it whenever possible.

Why?

Global variables make code:

- Harder to test
- Harder to debug
- Harder to maintain

Instead, prefer:

- Function parameters
- Return values
- Classes
- Dependency Injection

---

# The `nonlocal` Keyword

`nonlocal` is used with **enclosing variables**.

Consider this example.

```python
def outer():

    count = 0

    def inner():

        nonlocal count

        count += 1

        print(count)

    inner()
    inner()

outer()
```

Output

```
1

2
```

Without `nonlocal`, this raises an error for the same reason we saw with `global`.

---

Visualization

```
outer()

↓

count = 0

↓

inner()

↓

nonlocal count

↓

Modify Enclosing Variable
```

---

# Difference Between `global` and `nonlocal`

| Keyword | Modifies |
|----------|----------|
| `global` | Global variable |
| `nonlocal` | Variable in the enclosing function |

Remember:

```
global

↓

Global Scope



nonlocal

↓

Enclosing Scope
```

---

# What is a Closure?

A closure is one of Python's most powerful features.

Definition:

> A closure is a function that remembers variables from its enclosing scope even after the enclosing function has finished executing.

This sounds complicated.

Let's understand it with an example.

---

# Example 2

```python
def greeting(message):

    def say_hello():

        print(message)

    return say_hello

hello = greeting("Welcome!")

hello()
```

Output

```
Welcome!
```

Question:

`greeting()` has already finished.

How does `say_hello()` still know `message`?

Because Python stored that variable inside the closure.

---

Visualization

```
greeting()

↓

message = "Welcome!"

↓

return say_hello

↓

greeting() ends

↓

say_hello still remembers message
```

This "remembering" behaviour is called a **closure**.

---

# Example 3 — Creating a Counter

```python
def counter():

    count = 0

    def increment():

        nonlocal count

        count += 1

        return count

    return increment

my_counter = counter()

print(my_counter())

print(my_counter())

print(my_counter())
```

Output

```
1

2

3
```

Even though `counter()` finished long ago, the variable `count` still exists because the closure keeps it alive.

---

# Why Are Closures Useful?

Closures allow functions to maintain private state without using global variables.

They are commonly used in:

- Decorators
- Callback functions
- Event handlers
- Function factories
- Dependency injection
- Caching

---

# Production Insight

Imagine you're building a simple request counter.

```python
def request_counter():

    total = 0

    def count():

        nonlocal total

        total += 1

        return total

    return count

counter = request_counter()
```

Each time a request is processed:

```python
print(counter())
```

Output

```
1
2
3
...
```

The `total` variable remains private.

Nothing outside the closure can modify it directly.

Closures are also heavily used when writing decorators, which you'll learn in the next lessons.

---

# Interview Deep Dive

### Interviewer

> What is the difference between `global` and `nonlocal`?

### Weak Answer

> One is for global variables and the other is for local variables.

This answer is incorrect because `nonlocal` does **not** work with local variables.

---

### Strong Answer

> `global` allows a function to modify variables defined at the module level. `nonlocal` allows an inner function to modify variables defined in its enclosing function. `nonlocal` only works inside nested functions.

---

### Interviewer

> What is a closure?

### Weak Answer

> A nested function.

This is incomplete.

---

### Strong Answer

> A closure is a function that retains access to variables from its enclosing scope even after the enclosing function has completed execution. This allows the function to maintain state without relying on global variables.

---

# Practical Lesson

Create a file:

```
closure_demo.py
```

Write the following program.

```python
def multiplier(number):

    def multiply(value):

        return number * value

    return multiply

double = multiplier(2)

triple = multiplier(3)

print(double(10))

print(triple(10))
```

Expected Output

```
20

30
```

Try creating:

```python
quadruple = multiplier(4)
```

Predict the output before running it.

---

# Interview Questions

## Question 1

What is an enclosing scope?

### Answer

An enclosing scope is the scope of an outer function that contains a nested function. Inner functions can access variables defined in this scope.

---

## Question 2

What does the `global` keyword do?

### Answer

It tells Python that a variable refers to the module-level global variable, allowing the function to modify it.

---

## Question 3

What does the `nonlocal` keyword do?

### Answer

It allows a nested function to modify a variable defined in its enclosing function.

---

## Question 4

What is a closure?

### Answer

A closure is a function that remembers and retains access to variables from its enclosing scope even after the enclosing function has finished executing.

---

## Question 5

Can `nonlocal` modify a global variable?

### Answer

No.

`nonlocal` only works with variables in an enclosing function.

To modify a global variable, use `global`.

---

# Assignment

## Exercise 1

Write a nested function where the inner function reads a variable from the enclosing function.

---

## Exercise 2

Create a counter using a closure that returns:

```
1
2
3
4
...
```

each time it is called.

---

## Exercise 3

Create a function named `power(exponent)` that returns another function.

Example:

```python
square = power(2)

cube = power(3)

print(square(5))

print(cube(5))
```

Expected Output

```
25

125
```

Implement it using a closure.

---

# Summary

In this lesson, you learned:

- ✅ What an enclosing scope is.
- ✅ How nested functions work.
- ✅ How Python searches variables using the complete LEGB rule.
- ✅ How the `global` keyword modifies module-level variables.
- ✅ How the `nonlocal` keyword modifies variables in an enclosing function.
- ✅ What closures are and how they preserve state.
- ✅ Why closures are widely used in decorators, callbacks and backend applications.

---

# What's Next

**File:**

`python/python-advanced-04-first-class-functions-and-higher-order-functions-part-1.md`

Topics:

- First-Class Functions
- Assigning Functions to Variables
- Passing Functions as Arguments
- Returning Functions
- Higher-Order Functions
- Real-world Backend Examples
- Interview Questions

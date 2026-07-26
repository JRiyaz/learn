# File: python/08-lambda-functions.md

# Python Advanced - Lesson 08
# Lambda Functions - Anonymous Functions in Python

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 08
>
> **Difficulty:** ⭐⭐⭐☆☆
>
> **Estimated Time:** 60 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- What lambda functions are
- Why Python introduced lambda functions
- Lambda syntax
- When to use lambda instead of `def`
- Common built-in functions that use lambdas
- Production use cases
- Common interview questions and mistakes

---

# Theory

A lambda function is an **anonymous function**.

Anonymous simply means it has **no explicit name**.

Normal function:

```python
def square(number):
    return number * number
```

Lambda:

```python
square = lambda number: number * number
```

Both behave the same.

```python
print(square(5))
```

Output

```
25
```

---

# Why Do Lambda Functions Exist?

Sometimes a function is only needed once.

Imagine sorting users.

```python
users = [
    {"name": "Alice", "age": 32},
    {"name": "Bob", "age": 21},
    {"name": "Charlie", "age": 28}
]
```

Without lambda:

```python
def get_age(user):
    return user["age"]

users.sort(key=get_age)
```

This works.

But `get_age()` is never used again.

Lambda avoids creating a temporary function.

```python
users.sort(key=lambda user: user["age"])
```

---

# Lambda Syntax

```
lambda arguments: expression
```

Examples

One argument

```python
square = lambda x: x * x
```

Two arguments

```python
add = lambda a, b: a + b
```

Three arguments

```python
average = lambda a, b, c: (a + b + c) / 3
```

---

# Lambda Can Only Contain One Expression

Valid

```python
lambda x: x * 2
```

Invalid

```python
lambda x:

    print(x)

    return x
```

If you need multiple statements, use `def`.

---

# Lambda with sorted()

Sort by age.

```python
users = [
    {"name": "Alice", "age": 32},
    {"name": "Bob", "age": 21},
    {"name": "Charlie", "age": 28}
]

result = sorted(
    users,
    key=lambda user: user["age"]
)

print(result)
```

---

# Sorting by Multiple Fields

Suppose two users have the same age.

```python
users = [
    {"name": "John", "age": 25},
    {"name": "Adam", "age": 25},
    {"name": "Chris", "age": 22}
]
```

Sort by:

1. Age
2. Name

```python
result = sorted(
    users,
    key=lambda user: (user["age"], user["name"])
)

print(result)
```

Python compares tuples from left to right.

---

# Lambda with map()

```python
prices = [100, 200, 300]

result = map(
    lambda price: price * 1.18,
    prices
)

print(list(result))
```

Output

```
[118.0, 236.0, 354.0]
```

---

# Lambda with filter()

```python
numbers = [1,2,3,4,5,6]

result = filter(
    lambda number: number % 2 == 0,
    numbers
)

print(list(result))
```

Output

```
[2,4,6]
```

---

# Lambda with max()

```python
employees = [
    {"name":"Alice","salary":50000},
    {"name":"Bob","salary":75000},
    {"name":"Chris","salary":65000}
]

highest = max(
    employees,
    key=lambda employee: employee["salary"]
)

print(highest)
```

Output

```python
{'name': 'Bob', 'salary': 75000}
```

---

# Lambda with min()

```python
cheapest = min(
    employees,
    key=lambda employee: employee["salary"]
)
```

---

# Lambda with Multiple Iterables

```python
numbers1 = [1,2,3]
numbers2 = [10,20,30]

result = map(
    lambda x, y: x + y,
    numbers1,
    numbers2
)

print(list(result))
```

Output

```
[11,22,33]
```

---

# Lambda vs def

Use **lambda** when:

- Small transformation
- Sorting
- Filtering
- Mapping
- Temporary callback

Use **def** when:

- Business logic
- Multiple statements
- Error handling
- Documentation is required
- Function is reused

A good rule is:

> If you can't understand the lambda at a glance, use `def`.

---

# Common Mistake

Avoid writing complex lambdas.

Poor

```python
lambda x: (x * 5 if x % 2 == 0 else x * 10 if x > 100 else x + 20)
```

Better

```python
def calculate(x):

    if x % 2 == 0:
        return x * 5

    if x > 100:
        return x * 10

    return x + 20
```

Readable code is easier to maintain.

---

# Production Insight

Lambda functions appear throughout backend codebases.

Examples include:

- Sorting API responses
- Ordering database results after retrieval
- Transforming streamed data
- Data validation pipelines
- Background task scheduling
- Event processing

Although lambdas are common, production code should favour readability over brevity. Many engineering teams discourage complex lambdas in code reviews.

---

# Questions

### Question

> When should you use a lambda instead of a normal function?

### Answer

Use a lambda for short, single-expression functions that are used temporarily, such as sorting, filtering or mapping. For reusable or complex logic, use a normal function defined with `def`.

---

### Question

> Why can't a lambda contain multiple statements?

### Answer

Python intentionally restricts lambda functions to a single expression to keep them concise and readable. Multi-step logic should be written using `def`.

---

### Question

> Are lambda functions faster than normal functions?

### Answer

No. Lambda functions and normal functions are implemented similarly. The choice between them is about readability and convenience, not performance.

---

# Practical Lesson

Create a file:

```
lambda_examples.py
```

```python
employees = [
    {"name": "Alice", "salary": 50000},
    {"name": "Bob", "salary": 75000},
    {"name": "Chris", "salary": 65000}
]

highest_paid = max(
    employees,
    key=lambda employee: employee["salary"]
)

print(highest_paid)
```

Modify the program to:

- Find the employee with the lowest salary.
- Sort employees by name.
- Sort employees by salary in descending order.

---

# Questions

## Question 1

What is a lambda function?

### Answer

A lambda function is an anonymous function that consists of a single expression and returns its result automatically.

---

## Question 2

Can a lambda contain multiple statements?

### Answer

No. A lambda can contain only one expression.

---

## Question 3

What is the most common use of lambda functions?

### Answer

Providing short callback functions for operations such as `sorted()`, `map()`, `filter()`, `min()` and `max()`.

---

## Question 4

Should complex business logic be written using lambda?

### Answer

No. Complex or reusable logic should be implemented with a normal function using `def`.

---

## Question 5

Does a lambda function have a name?

### Answer

A lambda function is anonymous. Although it can be assigned to a variable, it is created without an explicit function name.

---

# Assignment

## Exercise 1

Sort a list of dictionaries by two different fields using a lambda.

---

## Exercise 2

Use `map()` with two lists to calculate the product of corresponding values.

---

## Exercise 3

Use `max()` and `min()` with a lambda to find the highest and lowest scoring students from a list of dictionaries.

---

# Summary

In this lesson, you learned:

- ✅ Why lambda functions exist.
- ✅ Lambda syntax.
- ✅ When to use lambda and when to use `def`.
- ✅ Advanced sorting with lambdas.
- ✅ Using lambdas with `map()`, `filter()`, `max()` and `min()`.
- ✅ Production best practices.

---

# What's Next

**File:**
[09-Context-Managers-part-1](09-context-managers-part-1.md)

Topics:

- Why Context Managers Exist
- The `with` Statement
- The Context Manager Protocol
- `__enter__()` and `__exit__()`
- Building Your First Context Manager
- File Handling Internals
- Production Examples

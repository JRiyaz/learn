# File: python/02-reference-counting-and-garbage-collection-part-2.md

# Python Advanced - Lesson 02 (Part 2)

# Shallow Copy, Deep Copy & The Mutable Default Argument Bug

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 02 (Part 2)
>
> **Difficulty:** ⭐⭐⭐☆☆
>
> **Estimated Time:** 60-75 Minutes

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why assignment is not copying
- What shallow copy actually copies
- What deep copy actually copies
- When to use each copy technique
- The famous mutable default argument bug
- How to avoid accidental shared state in production code

______________________________________________________________________

# Theory

In the previous lesson, we learned:

```python
a = [1, 2, 3]
b = a
```

does **not** create another list.

It only creates another reference.

The question now becomes:

> **How do we actually create a copy?**

Python provides several ways to copy objects.

However, not all copies are the same.

Understanding the difference is extremely important because many production bugs happen due to incorrect copying.

______________________________________________________________________

# Example 1 — Assignment is NOT Copying

```python
# Create one list.
users = ["Alice", "Bob"]

# This does NOT create another list.
# Both variables point to the same object.
backup = users

# Modify the list using 'backup'.
backup.append("Charlie")

print(users)
print(backup)
```

Output

```
['Alice', 'Bob', 'Charlie']
['Alice', 'Bob', 'Charlie']
```

Visualization

```
        List Object

+-------------------------+
| Alice Bob Charlie       |
+-------------------------+
         ▲          ▲
         │          │
      users      backup
```

There is still only one list.

______________________________________________________________________

# Example 2 — Creating a Shallow Copy

Python provides several ways.

```python
users = ["Alice", "Bob"]

# Create a NEW list object.
backup = users.copy()

backup.append("Charlie")

print(users)

print(backup)
```

Output

```
['Alice', 'Bob']

['Alice', 'Bob', 'Charlie']
```

Visualization

```
users

↓

+----------------+
| Alice Bob      |
+----------------+

backup

↓

+--------------------------+
| Alice Bob Charlie        |
+--------------------------+
```

Now there are two different list objects.

______________________________________________________________________

# Another Way

```python
backup = list(users)
```

or

```python
backup = users[:]
```

All three create a **shallow copy**.

______________________________________________________________________

# What is a Shallow Copy?

A shallow copy creates

- A **new outer object**
- But keeps references to the inner objects

Let's see why that matters.

______________________________________________________________________

# Example 3 — Nested Lists

```python
employees = [

    ["Alice", 25],

    ["Bob", 30]
]

backup = employees.copy()

# Modify the first employee.
backup[0][1] = 99

print(employees)

print(backup)
```

Output

```
[['Alice', 99], ['Bob', 30]]

[['Alice', 99], ['Bob', 30]]
```

Wait...

We copied it!

Why did both change?

______________________________________________________________________

Visualization

```
employees

↓

+----------------------+
|   *        *         |
+----------------------+
    │        │
    ▼        ▼
[Alice,25] [Bob,30]



backup

↓

+----------------------+
|   *        *         |
+----------------------+
    │        │
    ▼        ▼
[Alice,25] [Bob,30]
```

Only the outer list was copied.

The inner lists are still shared.

This is exactly what a **shallow copy** means.

______________________________________________________________________

# Deep Copy

Python provides another module.

```python
import copy
```

Use

```python
copy.deepcopy()
```

to recursively copy everything.

______________________________________________________________________

# Example 4

```python
import copy

employees = [

    ["Alice", 25],

    ["Bob", 30]
]

# Deep copy creates completely independent objects.
backup = copy.deepcopy(employees)

backup[0][1] = 99

print(employees)

print(backup)
```

Output

```
[['Alice', 25], ['Bob', 30]]

[['Alice', 99], ['Bob', 30]]
```

Visualization

```
employees

↓

Outer List

↓

Inner Lists



backup

↓

Another Outer List

↓

Another Set of Inner Lists
```

Nothing is shared anymore.

______________________________________________________________________

# When Should You Use Shallow Copy?

Good for

- Flat lists
- Flat dictionaries
- Simple objects
- Small configuration objects

Example

```python
colors = ["Red", "Green", "Blue"]

backup = colors.copy()
```

Perfectly fine.

______________________________________________________________________

# When Should You Use Deep Copy?

Whenever nested mutable objects exist.

Examples

```python
Company

↓

Departments

↓

Employees

↓

Addresses
```

or

```python
JSON Data

↓

Lists

↓

Dictionaries

↓

Lists
```

Deep copy prevents accidental modification of shared data.

______________________________________________________________________

# The Famous Mutable Default Argument Bug

This is one of the most common Python interview questions.

Consider this function.

```python
def add_user(name, users=[]):
    """
    BAD EXAMPLE

    'users' is created only once,
    when the function is defined.
    """

    users.append(name)

    return users
```

Looks harmless.

Now call it.

```python
print(add_user("Alice"))

print(add_user("Bob"))

print(add_user("Charlie"))
```

Output

```
['Alice']

['Alice', 'Bob']

['Alice', 'Bob', 'Charlie']
```

Most developers expect

```
['Alice']

['Bob']

['Charlie']
```

Why didn't that happen?

______________________________________________________________________

# Why?

Default arguments are evaluated only **once**, when the function is created.

Python does NOT create a new list every time.

Visualization

```
Function

↓

users

↓

[]
```

Every function call reuses that same list.

______________________________________________________________________

# Correct Solution

```python
def add_user(name, users=None):
    """
    GOOD EXAMPLE

    Use None as the default value.
    Create a new list only when needed.
    """

    if users is None:
        users = []

    users.append(name)

    return users
```

Now

```python
print(add_user("Alice"))

print(add_user("Bob"))

print(add_user("Charlie"))
```

Output

```
['Alice']

['Bob']

['Charlie']
```

Every call gets a new list.

______________________________________________________________________

# Production Insight

Imagine a FastAPI application.

```python
def create_filters(filters={}):
    ...
```

Everything works during testing.

After deploying,

User A modifies filters.

Suddenly,

User B sees User A's filters.

Why?

Because every request is sharing the same dictionary.

This bug has caused real production issues.

The correct implementation is:

```python
def create_filters(filters=None):

    if filters is None:
        filters = {}

    ...
```

Whenever you see a mutable default argument (`[]`, `{}`, `set()`), treat it as a warning sign.

______________________________________________________________________

# Questions

### Question

> Explain the difference between a shallow copy and a deep copy.

### Answer

> A shallow copy creates a new outer container but keeps references to the nested objects. Therefore, changes to nested mutable objects are reflected in both copies. A deep copy recursively duplicates every nested object, ensuring the copied structure is completely independent of the original.

______________________________________________________________________

### Question

> Why are mutable default arguments dangerous?

### Answer

> Default arguments are evaluated only once when the function is defined, not every time it is called. If the default value is mutable, such as a list or dictionary, every function call shares the same object, which can lead to unexpected state being preserved across calls.

______________________________________________________________________

# Practical Lesson

Create a file:

```
copy_demo.py
```

Write the following program.

```python
import copy

student = {
    "name": "Alice",
    "marks": [80, 90]
}

print("=" * 40)
print("Original")
print(student)

print("=" * 40)
print("Shallow Copy")

shallow = student.copy()

shallow["marks"].append(100)

print(student)

print(shallow)

print("=" * 40)
print("Deep Copy")

deep = copy.deepcopy(student)

deep["marks"].append(200)

print(student)

print(deep)
```

Observe carefully:

- Which objects change?
- Why?
- Which objects remain independent?

Understanding this example will make shallow vs deep copy intuitive.

______________________________________________________________________

# Questions

## Question 1

What is copied during a shallow copy?

### Answer

Only the outer container is copied.

Nested mutable objects are still shared between the original and the copy.

______________________________________________________________________

## Question 2

When should you use `deepcopy()`?

### Answer

When the object contains nested mutable objects (lists, dictionaries, sets, custom objects) that must be completely
independent from the original.

______________________________________________________________________

## Question 3

Why is the following code dangerous?

```python
def func(data=[]):
    ...
```

### Answer

Because the list is created only once when the function is defined.

Every function call shares the same list, leading to unexpected behaviour.

______________________________________________________________________

## Question 4

Does `list.copy()` perform a deep copy?

### Answer

No.

It performs a shallow copy.

Only the outer list is copied.

______________________________________________________________________

## Question 5

Name three ways to create a shallow copy of a list.

### Answer

```python
list.copy()

list(original)

original[:]
```

______________________________________________________________________

# Assignment

## Exercise 1

Create a nested dictionary.

Create a shallow copy.

Modify an inner list.

Observe the result.

______________________________________________________________________

## Exercise 2

Repeat Exercise 1 using `copy.deepcopy()`.

Observe the difference.

______________________________________________________________________

## Exercise 3

Write a function that uses a mutable default argument.

Call it three times.

Explain why the output changes.

Then rewrite the function using `None` as the default argument.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Assignment does not create a copy.
- ✅ A shallow copy duplicates only the outer container.
- ✅ Nested mutable objects remain shared in a shallow copy.
- ✅ A deep copy recursively duplicates every nested object.
- ✅ Mutable default arguments are evaluated only once.
- ✅ Using `None` as a default argument avoids shared state bugs.

______________________________________________________________________

# What's Next

**File:** [03-LEGB-Scope-and-Variable-Resolution-part-1](03-legb-scope-and-variable-resolution-part-1.md)

Topics:

- Local Scope
- Enclosing Scope
- Global Scope
- Built-in Scope
- Variable Shadowing
- `global`
- `nonlocal`
- Real-world examples from FastAPI and Flask
- Common questions

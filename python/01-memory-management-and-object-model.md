# File: python/python-advanced-01-memory-management-and-object-model.md

# Python Advanced - Lesson 01
# Memory Management & Python Object Model

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 01
>
> **Difficulty:** ⭐⭐☆☆☆ (Intermediate)
>
> **Estimated Time:** 45-60 Minutes

---

# Learning Objectives

By the end of this lesson you will understand:

- How Python stores objects in memory
- Difference between variables and objects
- What `id()` actually returns
- Mutable vs Immutable objects
- Difference between `==` and `is`
- Why modifying one variable sometimes changes another
- Common interview questions around object references

---

# Prerequisites

- Basic Python syntax
- Variables
- Functions
- Lists
- Dictionaries

---

# Why This Topic Matters

Many developers memorize Python syntax but never learn **how Python actually works internally**.

Understanding Python's object model helps you:

- Avoid bugs caused by mutable objects
- Write memory-efficient code
- Understand decorators
- Understand generators
- Learn AsyncIO faster
- Answer Python interview questions confidently

This lesson is the foundation for everything we'll learn later.

---

# 1. Everything in Python is an Object

One of Python's biggest design principles is:

> **Everything is an object.**

Examples:

```python
10
10.5
"Hello"
True
[1, 2, 3]
{"name": "Riyaz"}
print
len
my_function
MyClass
```

Everything above is an object.

---

## What is an Object?

An object has three important things:

- Identity
- Type
- Value

Example:

```python
age = 25
```

Internally Python creates something similar to:

```
Object

Identity : 1407282932
Type     : int
Value    : 25
```

---

# 2. Variables Don't Store Data

This is one of the biggest misconceptions.

Many people think:

```
age

+------+
|  25  |
+------+
```

This is NOT what Python does.

Python actually stores:

```
          Object

    +-----------------+
    | Type : int      |
    | Value: 25       |
    +-----------------+
            ▲
            │
          age
```

The variable **doesn't contain the value**.

It only points to an object.

Think of a variable as a **label**.

---

# Example 1

```python
# Create an integer object.
x = 10

# 'y' does NOT create another integer object.
# It simply points to the same object.
y = x

print(id(x))
print(id(y))
```

Expected Output (IDs will differ on your machine):

```
140710429920528
140710429920528
```

Both variables reference the same object.

Visualization:

```
            +-----------+
            |  int 10   |
            +-----------+
              ▲      ▲
              │      │
              x      y
```

---

# 3. Understanding id()

Python provides a built-in function:

```python
id(object)
```

It returns the **identity** of an object.

Example:

```python
name = "Python"

print(id(name))
```

Think of it like this:

```
House

Address:
221 Baker Street
```

The **house** is the object.

The **address** is the object's identity.

`id()` returns the address (identity), **not** the value.

---

# 4. Lists Behave Differently

Let's create a list.

```python
# Create one list object.
numbers = [1, 2, 3]

# Create another reference to the same object.
another = numbers

print(id(numbers))
print(id(another))
```

Output:

```
Same ID
```

Visualization:

```
         List Object

     +-------------+
     |1|2|3|
     +-------------+
         ▲      ▲
         │      │
    numbers   another
```

Only one list exists.

---

# Example 2

```python
numbers = [1, 2, 3]

another = numbers

# Append modifies the EXISTING list.
another.append(4)

print(numbers)
print(another)
```

Output:

```
[1, 2, 3, 4]
[1, 2, 3, 4]
```

Why?

Because there is only one list.

```
          +------------------+
          |1|2|3|4|
          +------------------+
              ▲         ▲
              │         │
          numbers   another
```

---

# 5. Mutable vs Immutable Objects

This is one of the most asked interview topics.

---

## Immutable Objects

Cannot change after creation.

Examples:

- int
- float
- bool
- tuple
- str
- frozenset

Example:

```python
text = "Python"

text[0] = "J"
```

Output:

```
TypeError
```

Because strings cannot be modified.

---

## Mutable Objects

Can change after creation.

Examples:

- list
- dict
- set

Example:

```python
numbers = [1, 2, 3]

numbers.append(4)

print(numbers)
```

Output:

```
[1, 2, 3, 4]
```

The original object changed.

---

# 6. Immutable Objects Create New Objects

Example:

```python
x = 10

print(id(x))

# x + 1 creates a NEW integer object.
x = x + 1

print(id(x))
```

The IDs will be different.

Visualization:

Before

```
x
│
▼
10
```

After

```
10

11
▲
│
x
```

The integer `10` never changed.

Python created a new object `11`.

---

# 7. == vs is

This is another favourite interview question.

Example:

```python
a = [1, 2, 3]

b = [1, 2, 3]

print(a == b)

print(a is b)
```

Output:

```
True

False
```

Why?

### ==

Compares values.

```
[1,2,3]

[1,2,3]

Same contents
```

---

### is

Compares identity.

```
Object A

Object B

Different objects
```

Even if two objects contain the same data, they are still different objects.

---

# Example

```python
a = [1, 2]

b = a

print(a == b)

print(a is b)
```

Output:

```
True

True
```

Both variables point to the exact same object.

---

# Best Practice

Use:

```python
if value is None:
    print("No value")
```

Instead of:

```python
if value == None:
    print("No value")
```

Reason:

There is only one `None` object.

Identity comparison is the recommended Python style.

---

# Production Example

Suppose a FastAPI endpoint caches a list.

```python
cached_users = []

def get_users():
    return cached_users
```

If another function does:

```python
users = get_users()

users.append("Riyaz")
```

The cache has now changed because both variables reference the same list.

This is a common source of bugs in production systems.

---

# Common Mistakes

### Mistake 1

Assuming assignment copies an object.

Wrong:

```python
b = a
```

Correct understanding:

```
b points to the same object as a
```

---

### Mistake 2

Using `is` for value comparison.

Wrong:

```python
name1 is name2
```

Correct:

```python
name1 == name2
```

---

### Mistake 3

Thinking integers change.

Wrong:

```
10 becomes 11
```

Correct:

```
10 stays 10

11 is a brand new object
```

---

# Interview Questions

## Question 1

Predict the output.

```python
x = [1, 2]

y = x

x.append(3)

print(y)
```

---

## Question 2

Predict the output.

```python
a = [1, 2, 3]

b = [1, 2, 3]

print(a == b)

print(a is b)
```

---

## Question 3

Predict the output.

```python
name = "Python"

print(id(name))

name = name + "3"

print(id(name))
```

Will the IDs be the same?

Why?

---

## Question 4

Predict the output.

```python
x = {"name": "Riyaz"}

y = x

y["age"] = 28

print(x)
```

---

## Question 5

Why is the following recommended?

```python
if value is None:
    ...
```

Instead of:

```python
if value == None:
    ...
```

---

# Assignment

Without using Google, answer these questions in your own words:

1. What is an object?
2. What does a variable store?
3. Why are lists mutable?
4. Why are strings immutable?
5. Difference between `==` and `is`.
6. Why did `numbers` change when `another.append()` was called?

---

# Answers

## Answer 1

Output:

```python
[1, 2, 3]
```

### Explanation

`x` and `y` both reference the same list object.

Calling `append()` modifies the existing list instead of creating a new one.

---

## Answer 2

Output:

```python
True

False
```

### Explanation

`==` compares values.

`is` compares object identity.

The two lists contain the same values but are different objects in memory.

---

## Answer 3

The IDs will be different.

### Explanation

Strings are immutable.

When you write:

```python
name = name + "3"
```

Python creates a brand-new string object (`"Python3"`). The original `"Python"` object is unchanged, and `name` now points to the new object.

---

## Answer 4

Output:

```python
{'name': 'Riyaz', 'age': 28}
```

### Explanation

`x` and `y` reference the same dictionary object. Updating the dictionary through `y` changes the shared object, so `x` sees the update as well.

---

## Answer 5

`None` is a singleton object in Python—there is only one instance of it.

Using `is` checks whether the object is that exact singleton, making it both idiomatic and reliable.

---

# Summary

In this lesson you learned:

- ✅ Everything in Python is an object.
- ✅ Variables store references, not the actual data.
- ✅ `id()` returns an object's identity.
- ✅ Assignment creates another reference, not a copy.
- ✅ Mutable objects can change in place.
- ✅ Immutable objects result in new objects when "modified".
- ✅ `==` compares values, while `is` compares object identity.
- ✅ `is None` is the recommended way to check for `None`.

---

# Key Takeaways

Before moving on, make sure you can confidently explain:

- Why `x = y` does **not** create a copy.
- Why `append()` changes both variables when they reference the same list.
- Why integers and strings get new object IDs after operations like `x = x + 1` or `name = name + "3"`.
- The difference between identity (`is`) and equality (`==`).

If you can explain these concepts without looking at the notes, you're ready for the next lesson.

---

# Next Lesson

**File:**
`python/python-advanced-02-reference-counting-garbage-collection-and-copying.md`

Topics:

- Reference Counting
- Garbage Collection
- `sys.getrefcount()`
- `del`
- Circular References
- Shallow Copy vs Deep Copy
- The Mutable Default Argument Bug (one of Python's most famous interview questions)

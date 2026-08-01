# File: python/34-dict-deep-dive-part-1.md

# Python Built-in Types

# Dictionary (`dict`) Deep Dive - Part 1: Fundamentals, Hash Tables & Core Operations

> **Course:** Backend Engineering Roadmap
>
> **Module:** Built-in Types
>
> **Lesson:** 34
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 4 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `dict` | Python 1.0 |
| Dictionary Comprehensions | Python 2.7 |
| Ordered Dictionary Implementation | Python 3.6 (CPython), Python 3.7+ (Language Guarantee) |
| Dictionary Merge Operator (`|`) | Python 3.9 |

### Important Python Version Changes

- Prior to Python 3.7, dictionaries should not be relied upon to preserve insertion order.
- From **Python 3.7 onwards**, insertion order is guaranteed by the language specification.
- Modern dictionaries are both memory efficient and extremely fast.

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What a dictionary is
- Why dictionaries are so fast
- Hash tables
- Keys and values
- Hashing
- Dictionary internals
- Dictionary operations
- Dictionary methods
- Dictionary views
- Time complexity
- Production best practices

______________________________________________________________________

# Recap

Previously we learned about tuples.

Tuples are:

- Ordered
- Immutable
- Hashable (if their contents are hashable)

Today's topic is the **Dictionary**, arguably the most important data structure in Python.

______________________________________________________________________

# Why Dictionaries Matter

Almost every backend application uses dictionaries.

Examples include:

- JSON objects
- HTTP headers
- API responses
- Configuration files
- User sessions
- JWT payloads
- Caches
- Database records

If you open a FastAPI or Flask project, you'll find dictionaries everywhere.

______________________________________________________________________

# What is a Dictionary?

A dictionary stores **key-value pairs**.

```python
user = {

    "name": "Alice",

    "age": 30,

    "city": "Bengaluru",

}
```

Think of it as a lookup table.

```
"name"

↓

"Alice"
```

Instead of searching sequentially,

Python jumps directly to the value.

______________________________________________________________________

# Real World Analogy

Imagine a library.

Without a catalogue,

finding a book means checking every shelf.

```
Book 1

↓

Book 2

↓

Book 3

↓

...
```

Slow.

Now imagine a digital catalogue.

```
Book ID

↓

Shelf Location
```

Instant lookup.

A dictionary works in a similar way.

______________________________________________________________________

# Dictionary Structure

```
+-------------------------------+

| "name" → "Alice"              |

| "age"  → 30                   |

| "city" → "Bengaluru"          |

+-------------------------------+
```

Every key maps to exactly one value.

______________________________________________________________________

# Creating Dictionaries

Literal syntax

```python
user = {

    "name": "Alice",

    "age": 30,

}
```

Constructor

```python
user = dict(

    name="Alice",

    age=30,

)
```

From tuples

```python
user = dict(

    [

        ("name", "Alice"),

        ("age", 30),

    ]

)
```

______________________________________________________________________

# Accessing Values

```python
user = {

    "name": "Alice",

    "age": 30,

}

print(user["name"])
```

Output

```text
Alice
```

Complexity

```
Average

O(1)
```

______________________________________________________________________

# Updating Values

```python
user["age"] = 31

print(user)
```

Output

```text
{'name': 'Alice', 'age': 31}
```

______________________________________________________________________

# Adding New Keys

```python
user["country"] = "India"

print(user)
```

Output

```text
{

'name':'Alice',

'age':31,

'country':'India'

}
```

______________________________________________________________________

# Deleting Keys

```python
del user["age"]

print(user)
```

Output

```text
{'name': 'Alice'}
```

______________________________________________________________________

# pop()

```python
user = {

    "name": "Alice",

    "age": 30,

}

age = user.pop("age")

print(age)

print(user)
```

Output

```text
30

{'name':'Alice'}
```

Useful when you need the removed value.

______________________________________________________________________

# popitem()

Removes the last inserted item.

```python
user = {

    "name": "Alice",

    "age": 30,

}

print(user.popitem())
```

Output

```text
('age', 30)
```

Since Python 3.7,

this follows insertion order.

______________________________________________________________________

# clear()

```python
user.clear()

print(user)
```

Output

```text
{}
```

______________________________________________________________________

# The Biggest Question

Why are dictionaries so fast?

The answer is:

```
Hash Tables
```

______________________________________________________________________

# What is a Hash Table?

A hash table converts a key into a number.

Example

```
"username"

↓

Hash Function

↓

928374923

↓

Memory Slot

↓

Stored Value
```

Instead of checking every key,

Python computes the hash,

then jumps directly to the correct location.

______________________________________________________________________

# Visualising

Without hashing

```
Alice

↓

Bob

↓

Charlie

↓

David

↓

Emma
```

Python searches sequentially.

Complexity

```
O(n)
```

______________________________________________________________________

With hashing

```
"Alice"

↓

Hash

↓

Bucket 25

↓

Value
```

Complexity

```
Average O(1)
```

______________________________________________________________________

# hash()

Python exposes the hash function.

```python
print(hash("Python"))
```

Output

```text
-5032819734...
```

Your output will differ.

Hash values are intentionally randomised between Python processes for many built-in types like strings.

______________________________________________________________________

# Why Randomised?

Security.

Without randomisation,

an attacker could deliberately create many collisions.

Hash randomisation helps reduce certain denial-of-service attacks.

______________________________________________________________________

# Hashable Objects

Only immutable objects are normally hashable.

Examples

```python
hash("Python")

hash(100)

hash((1, 2))
```

Valid.

______________________________________________________________________

# Unhashable Objects

```python
hash([1, 2])
```

Output

```text
TypeError
```

Lists are mutable.

Their hash could change.

______________________________________________________________________

# Dictionary Keys

Valid keys

```python
"Python"

100

3.14

True

None

(1, 2)
```

Invalid keys

```python
[]

{}

set()
```

These mutable objects cannot be dictionary keys.

______________________________________________________________________

# Why?

Suppose

```
Hash

↓

Bucket 25
```

Then

the key changes.

Now

```
Hash

↓

Bucket 90
```

The dictionary would lose track of the key.

Therefore,

mutable objects cannot be used.

______________________________________________________________________

# Dictionary Lookup

Suppose

```python
user = {

    "name": "Alice"

}
```

Lookup

```python
print(user["name"])
```

Internally

```
"name"

↓

hash()

↓

Bucket

↓

Compare Key

↓

Return Value
```

Notice

Python does **not** compare every key.

______________________________________________________________________

# KeyError

Suppose

```python
print(user["salary"])
```

Output

```text
KeyError
```

The key does not exist.

______________________________________________________________________

# get()

Safer alternative.

```python
print(

    user.get("salary")

)
```

Output

```text
None
```

Default value

```python
print(

    user.get(

        "salary",

        0

    )

)
```

Output

```text
0
```

______________________________________________________________________

# Why Use get()?

Imagine processing JSON.

```python
payload = {

    "username": "alice"

}
```

Instead of

```python
payload["email"]
```

which raises an exception,

use

```python
payload.get("email")
```

Much safer.

______________________________________________________________________

# Membership Testing

```python
print(

    "name" in user

)
```

Output

```text
True
```

Complexity

```
Average

O(1)
```

______________________________________________________________________

# Iterating

Keys

```python
for key in user:

    print(key)
```

______________________________________________________________________

# keys()

```python
for key in user.keys():

    print(key)
```

Equivalent,

but more explicit.

______________________________________________________________________

# values()

```python
for value in user.values():

    print(value)
```

Output

```text
Alice

30
```

______________________________________________________________________

# items()

Most common.

```python
for key, value in user.items():

    print(key, value)
```

Output

```text
name Alice

age 30
```

______________________________________________________________________

# Dictionary Views

Many developers think

```python
user.keys()
```

returns a list.

It does not.

```python
print(type(user.keys()))
```

Output

```text
<class 'dict_keys'>
```

This is a **dynamic view**.

______________________________________________________________________

# Dynamic View Example

```python
user = {

    "name": "Alice"

}

keys = user.keys()

print(keys)

user["age"] = 30

print(keys)
```

Output

```text
dict_keys(['name'])

dict_keys(['name', 'age'])
```

The view updates automatically.

______________________________________________________________________

# Time Complexity

| Operation | Complexity |
|------------|------------|
| Lookup | Average O(1) |
| Insert | Average O(1) |
| Update | Average O(1) |
| Delete | Average O(1) |
| Membership | Average O(1) |
| Iteration | O(n) |

Worst-case complexity can degrade if many hash collisions occur, but modern Python dictionaries are designed to minimise
this.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using

```python
user["email"]
```

when the key may not exist.

Prefer

```python
user.get("email")
```

______________________________________________________________________

## Mistake 2

Using mutable keys.

Wrong

```python
cache = {

    [1, 2]: "data"

}
```

______________________________________________________________________

## Mistake 3

Assuming `keys()` returns a list.

It returns a dynamic view.

If you need a list,

use

```python
list(user.keys())
```

______________________________________________________________________

## Mistake 4

Iterating only over keys,

then performing another lookup.

Instead of

```python
for key in user:

    print(key, user[key])
```

Prefer

```python
for key, value in user.items():

    print(key, value)
```

One lookup instead of two.

______________________________________________________________________

# Best Practices

✅ Use meaningful key names.

✅ Prefer `get()` when a key may be absent.

✅ Use `items()` when both keys and values are required.

✅ Use immutable objects as dictionary keys.

✅ Keep keys consistent throughout your application.

❌ Don't catch `KeyError` when `get()` is sufficient.

❌ Don't use mutable objects as keys.

______________________________________________________________________

# Production Insight

Dictionaries power many backend frameworks.

FastAPI request body

```python
payload = {

    "username": "alice",

    "email": "alice@example.com"

}
```

JWT payload

```python
payload = {

    "sub": "123",

    "role": "admin"

}
```

HTTP headers

```python
headers = {

    "Authorization": token,

    "Content-Type": "application/json"

}
```

Configuration

```python
config = {

    "host": "localhost",

    "port": 5432

}
```

Understanding dictionaries is essential because most backend data eventually becomes a dictionary.

______________________________________________________________________

# Questions

### Question

> Why are dictionary lookups usually O(1)?

### Answer

Because dictionaries use hash tables. Python computes the key's hash value and uses it to locate the appropriate bucket
instead of searching every key sequentially.

______________________________________________________________________

### Question

> Why can't lists be dictionary keys?

### Answer

Lists are mutable. If their contents changed after insertion, their hash value would change, making them impossible to
locate reliably in the hash table.

______________________________________________________________________

### Question

> When should you use `get()` instead of square bracket access?

### Answer

Use `get()` when missing keys are expected or acceptable. Use square brackets when the key must exist and its absence
indicates a programming error.

______________________________________________________________________

### Question

> What does `items()` return?

### Answer

A dynamic view of key-value pairs that can be iterated efficiently and reflects changes made to the dictionary.

______________________________________________________________________

# Practical Lesson

Create:

```text
dictionary_basics.py
```

```python
# Create a dictionary
user = {
    "name": "Alice",
    "age": 30,
}

# Safe lookup
print(user.get("email", "Not Provided"))

# Add a new key
user["country"] = "India"

# Update an existing key
user["age"] = 31

# Iterate through key-value pairs
for key, value in user.items():
    print(f"{key}: {value}")

# Membership test
print("name" in user)

# Remove a value
removed_age = user.pop("age")

print(f"Removed age: {removed_age}")
print(user)
```

Expected Output

```text
Not Provided

name: Alice
age: 31
country: India

True

Removed age: 31

{'name': 'Alice', 'country': 'India'}
```

______________________________________________________________________

# Questions

## Question 1

Why are dictionaries generally faster than lists for lookups?

### Answer

Dictionaries use hash tables, allowing direct access to values using hash computations instead of sequential searches.

______________________________________________________________________

## Question 2

Why should dictionary keys usually be immutable?

### Answer

Immutable objects produce stable hash values, allowing Python to locate them reliably in the hash table.

______________________________________________________________________

## Question 3

What is the difference between `pop()` and `del`?

### Answer

`pop()` removes a key and returns its value, while `del` simply removes the key without returning the value.

______________________________________________________________________

## Question 4

Why is `items()` preferred when iterating over both keys and values?

### Answer

It provides both the key and value in a single iteration, avoiding an additional dictionary lookup.

______________________________________________________________________

## Question 5

Do `keys()`, `values()` and `items()` return lists?

### Answer

No. They return dynamic view objects that reflect changes made to the dictionary.

______________________________________________________________________

# Assignment

## Exercise 1

Create a simple inventory system using dictionaries.

Support:

- Add product
- Update quantity
- Remove product
- Display inventory

______________________________________________________________________

## Exercise 2

Count the frequency of every word in a paragraph using a dictionary.

______________________________________________________________________

## Exercise 3

Given a list of employee dictionaries, group employees by department using a dictionary.

______________________________________________________________________

## Exercise 4

Create a configuration loader that safely reads optional settings using `get()` and sensible default values.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What dictionaries are.
- ✅ Why hash tables make them fast.
- ✅ How hashing works at a high level.
- ✅ Dictionary creation and modification.
- ✅ Safe lookups with `get()`.
- ✅ Dictionary views.
- ✅ Time complexity.
- ✅ Production use cases.
- ✅ Common interview topics.

______________________________________________________________________

# What's Next

**File:** [35-Dict-Deep-Dive-part-2](35-dict-deep-dive-part-2.md)

Topics:

- Hash collisions
- Collision resolution
- Dictionary resizing
- Insertion order
- Dictionary merging
- `setdefault()`
- `update()`
- `fromkeys()`
- Dictionary comprehensions
- Performance optimisations
- Production patterns
- Advanced interview questions

> **This is the most important dictionary lesson.** We'll dive into how CPython handles collisions, why dictionaries remain fast at scale, and how senior engineers use advanced dictionary patterns in production.

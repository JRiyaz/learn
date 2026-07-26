# File: python/36-set-and-frozenset.md

# Python Built-in Types
# Set (`set`) & FrozenSet (`frozenset`) Deep Dive

> **Course:** Backend Engineering Roadmap
>
> **Module:** Built-in Types
>
> **Lesson:** 36
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 4 Hours

---

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `set` | Python 2.4 |
| `frozenset` | Python 2.4 |
| Set Comprehensions | Python 2.7 |

### Important Python Version Changes

- Sets were introduced in Python 2.4.
- Before Python 2.4, developers often used dictionaries to simulate sets.
- Modern Python sets are highly optimised hash-table based data structures.
- Like dictionaries, sets benefit from continuous performance improvements in CPython.

---

# Learning Objectives

By the end of this lesson, you will understand:

- What sets are
- Why sets exist
- How sets work internally
- Hash tables revisited
- Hashable objects
- Set operations
- `frozenset`
- Performance characteristics
- Production use cases
- Best practices

---

# Recap

In the previous lessons, we explored dictionaries.

A dictionary stores:

```
Key

↓

Value
```

A set is similar internally, but stores **only unique values**.

Think of a dictionary as:

```
Key → Value
```

and a set as:

```
Value
```

---

# Why Do Sets Exist?

Suppose you have one million usernames.

You want to answer one question:

> "Does this username already exist?"

Using a list:

```python
if username in usernames:
    ...
```

Python checks each username one by one.

Time Complexity

```
O(n)
```

Using a set:

```python
if username in usernames:
    ...
```

Time Complexity

```
Average O(1)
```

The code looks identical.

The performance difference is enormous.

---

# What is a Set?

A set is an **unordered collection of unique hashable objects**.

Example

```python
users = {

    "Alice",

    "Bob",

    "Charlie",

}
```

Notice

No duplicate values.

---

# Duplicate Removal

```python
numbers = {

    1,

    2,

    2,

    3,

    3,

    3,

}

print(numbers)
```

Output

```text
{1, 2, 3}
```

Duplicates are automatically removed.

---

# Characteristics

Sets are:

✅ Mutable

✅ Unordered

✅ Contain unique elements

✅ Fast membership testing

✅ Built on hash tables

---

# Internal Representation

Like dictionaries,

sets use hash tables.

```
"Python"

↓

hash()

↓

Bucket

↓

Stored
```

Unlike dictionaries,

there is no associated value.

```
Dictionary

↓

Key → Value


Set

↓

Value
```

---

# Why Are Sets Unordered?

Because elements are stored according to their hash values,

not according to insertion order.

Therefore,

never write code that depends on the display order of a set.

Example

```python
languages = {

    "Python",

    "Go",

    "Rust",

}
```

The printed order may differ from what you wrote.

---

# Creating Sets

Literal

```python
languages = {

    "Python",

    "Go",

    "Rust",

}
```

Constructor

```python
numbers = set(

    [1, 2, 3]

)
```

From a string

```python
letters = set("banana")

print(letters)
```

Output

```text
{'a', 'b', 'n'}
```

---

# Empty Set

A very common mistake.

Wrong

```python
empty = {}

print(type(empty))
```

Output

```text
<class 'dict'>
```

Correct

```python
empty = set()

print(type(empty))
```

Output

```text
<class 'set'>
```

---

# Hashable Elements

Like dictionary keys,

set elements must be hashable.

Valid

```python
numbers = {

    1,

    2,

    3,

}
```

Also valid

```python
points = {

    (10, 20),

    (30, 40),

}
```

---

# Invalid Elements

```python
values = {

    [1, 2]

}
```

Output

```text
TypeError:
unhashable type: 'list'
```

Lists are mutable.

---

# add()

```python
users = {

    "Alice"

}

users.add("Bob")

print(users)
```

---

# update()

Add multiple values.

```python
users = {

    "Alice"

}

users.update(

    [

        "Bob",

        "Charlie",

    ]

)

print(users)
```

---

# remove()

```python
users = {

    "Alice",

    "Bob",

}

users.remove("Bob")

print(users)
```

If the element doesn't exist,

Python raises

```text
KeyError
```

---

# discard()

Safer alternative.

```python
users.discard("Charlie")
```

No exception.

Very useful when removal is optional.

---

# pop()

```python
numbers = {

    1,

    2,

    3,

}

value = numbers.pop()

print(value)
```

Important

`pop()` removes an **arbitrary** element.

Do **not** assume which element will be removed.

---

# clear()

```python
users.clear()

print(users)
```

Output

```text
set()
```

---

# Membership Testing

The biggest advantage of sets.

```python
users = {

    "Alice",

    "Bob",

}

print(

    "Bob" in users

)
```

Complexity

```
Average O(1)
```

---

# Union

Combine two sets.

```python
backend = {

    "Python",

    "Go",

}

frontend = {

    "JavaScript",

    "TypeScript",

}

print(

    backend | frontend

)
```

Output

```text
{'Python', 'Go', 'JavaScript', 'TypeScript'}
```

Equivalent

```python
backend.union(frontend)
```

---

# Intersection

Common elements.

```python
a = {

    1,

    2,

    3,

}

b = {

    2,

    3,

    4,

}

print(a & b)
```

Output

```text
{2, 3}
```

Equivalent

```python
a.intersection(b)
```

---

# Difference

Items only in one set.

```python
a = {

    1,

    2,

    3,

}

b = {

    2,

    3,

}

print(a - b)
```

Output

```text
{1}
```

---

# Symmetric Difference

Items present in exactly one set.

```python
a = {

    1,

    2,

    3,

}

b = {

    3,

    4,

    5,

}

print(a ^ b)
```

Output

```text
{1, 2, 4, 5}
```

---

# Visualising Set Operations

```
A = {1,2,3}

B = {3,4,5}


Union

{1,2,3,4,5}


Intersection

{3}


Difference (A-B)

{1,2}


Symmetric Difference

{1,2,4,5}
```

---

# Subset

```python
a = {

    1,

    2,

}

b = {

    1,

    2,

    3,

}

print(a <= b)
```

Output

```text
True
```

Equivalent

```python
a.issubset(b)
```

---

# Superset

```python
print(b >= a)
```

Equivalent

```python
b.issuperset(a)
```

---

# Disjoint

No common elements.

```python
backend = {

    "Python",

    "Go",

}

frontend = {

    "React",

    "Angular",

}

print(

    backend.isdisjoint(frontend)

)
```

Output

```text
True
```

---

# Set Comprehensions

```python
squares = {

    n * n

    for n in range(5)

}

print(squares)
```

Output

```text
{0, 1, 4, 9, 16}
```

---

# FrozenSet

A `frozenset` is an **immutable set**.

Example

```python
permissions = frozenset(

    [

        "read",

        "write",

    ]

)

print(permissions)
```

Unlike sets,

elements cannot be added or removed.

---

# Why Does FrozenSet Exist?

Because immutable objects are hashable.

This means

```python
roles = {

    frozenset(

        [

            "read",

            "write",

        ]

    )

}
```

is valid.

Normal sets cannot be elements of another set.

---

# Set vs FrozenSet

| Feature | Set | FrozenSet |
|----------|-----|-----------|
| Mutable | ✅ | ❌ |
| Hashable | ❌ | ✅ |
| Add Elements | ✅ | ❌ |
| Remove Elements | ✅ | ❌ |
| Dictionary Key | ❌ | ✅ |

---

# Time Complexity

| Operation | Complexity |
|------------|------------|
| Add | Average O(1) |
| Remove | Average O(1) |
| Membership | Average O(1) |
| Union | O(len(a)+len(b)) |
| Intersection | O(min(len(a), len(b))) |
| Difference | O(len(a)) |
| Iteration | O(n) |

---

# Common Mistakes

## Mistake 1

Creating an empty set incorrectly.

Wrong

```python
{}
```

Correct

```python
set()
```

---

## Mistake 2

Using lists inside a set.

```python
{

    [1, 2]

}
```

Produces

```text
TypeError
```

---

## Mistake 3

Assuming sets preserve order.

Never depend on iteration order.

---

## Mistake 4

Using `remove()` when an element may not exist.

Prefer

```python
discard()
```

if missing elements are acceptable.

---

# Best Practices

✅ Use sets for membership testing.

✅ Use sets to remove duplicates.

✅ Use set operations instead of manual loops.

✅ Use `discard()` when removal is optional.

✅ Use `frozenset` for immutable collections that need to be hashable.

❌ Don't use sets when element order matters.

❌ Don't use sets for indexed access.

❌ Don't store mutable objects in sets.

---

# Production Insight

Sets are extremely common in backend systems.

Removing duplicate email addresses

```python
emails = set(email_list)
```

Checking permissions

```python
required = {

    "read",

    "write",

}

user_permissions = {

    "read",

    "write",

    "delete",

}

if required <= user_permissions:
    print("Access granted")
```

Finding duplicate request IDs

```python
seen = set()

for request_id in requests:

    if request_id in seen:
        print("Duplicate")

    seen.add(request_id)
```

Filtering processed Kafka message IDs

```python
processed = set()

if message.id not in processed:

    processed.add(message.id)
```

Backend engineers frequently use sets to reduce algorithms from **O(n²)** to **O(n)**.

---

# Questions

### Question

> Why is membership testing faster in a set than in a list?

### Answer

Sets use hash tables, allowing average O(1) lookups. Lists perform sequential searches, resulting in O(n) time.

---

### Question

> Why can't lists be stored in a set?

### Answer

Lists are mutable and therefore unhashable. Set elements must have stable hash values.

---

### Question

> When would you choose a `frozenset`?

### Answer

When you need an immutable set that can be used as a dictionary key, cached safely, or shared without modification.

---

### Question

> Why doesn't `set.pop()` remove the "first" element?

### Answer

Sets are unordered collections. `pop()` removes an arbitrary element rather than the first inserted one.

---

### Question

> Give a production use case for sets.

### Answer

Sets are commonly used for duplicate detection, permission checks, cache lookups, and fast membership testing in large datasets.

---

# Practical Lesson

Create:

```text
set_examples.py
```

```python
# Remove duplicates
numbers = [1, 2, 2, 3, 3, 4]

unique_numbers = set(numbers)

print(unique_numbers)

# Membership testing
users = {"Alice", "Bob"}

print("Bob" in users)

# Set operations
backend = {"Python", "Go"}

frontend = {"JavaScript", "TypeScript"}

print(backend | frontend)

# Duplicate detection
seen = set()

for value in [1, 2, 2, 3]:

    if value in seen:
        print(f"Duplicate: {value}")

    seen.add(value)

# FrozenSet
permissions = frozenset({"read", "write"})

print(permissions)
```

Expected Output

```text
{1, 2, 3, 4}

True

{'Python', 'Go', 'JavaScript', 'TypeScript'}

Duplicate: 2

frozenset({'read', 'write'})
```

---

# Questions

## Question 1

Why are sets faster than lists for membership testing?

### Answer

Because sets use hash tables, allowing average O(1) lookups, whereas lists require sequential searches.

---

## Question 2

What is the difference between `remove()` and `discard()`?

### Answer

`remove()` raises a `KeyError` if the element is missing, while `discard()` silently does nothing.

---

## Question 3

When should you use a `frozenset`?

### Answer

Use a `frozenset` when the collection should be immutable and hashable, such as when using it as a dictionary key or set element.

---

## Question 4

Can a set contain duplicate values?

### Answer

No. Duplicate values are automatically removed when inserted.

---

## Question 5

When should you use a set instead of a list?

### Answer

When uniqueness is required or when frequent membership testing is needed for better performance.

---

# Assignment

## Exercise 1

Given two large lists of user IDs:

- Find common users.
- Find users unique to each list.
- Find all unique users.

Implement the solution using set operations.

---

## Exercise 2

Implement a duplicate file detector.

Given a list of file hashes, identify duplicate files efficiently using sets.

---

## Exercise 3

Build a permission system.

Users have different permissions stored as sets.

Implement checks for:

- Required permissions
- Missing permissions
- Extra permissions

using set operations.

---

## Exercise 4

Given a stream of API request IDs, detect duplicate requests in real time using a set. Compare the algorithm with an equivalent list-based implementation and explain the difference in time complexity.

---

# Summary

In this lesson, you learned:

- ✅ What sets are.
- ✅ How sets work internally.
- ✅ Why sets use hash tables.
- ✅ Set operations.
- ✅ `frozenset`.
- ✅ Performance characteristics.
- ✅ Production use cases.
- ✅ Best practices.
- ✅ Senior backend interview topics.

---

# What's Next

**File:**
[37-Numeric-Types-Deep-Dive](37-numeric-types-deep-dive.md)

Topics:

- `int`
- `float`
- `bool`
- `decimal.Decimal`
- `fractions.Fraction`
- `complex`
- IEEE 754 floating-point representation
- Numeric precision
- Rounding behaviour
- Arithmetic pitfalls
- Production best practices
- Performance considerations

> **Note:** This lesson goes far beyond basic arithmetic. We'll explore how Python represents numbers internally, why floating-point errors occur, when to use `Decimal` instead of `float`, and how senior backend engineers make the right choice for financial and scientific applications.

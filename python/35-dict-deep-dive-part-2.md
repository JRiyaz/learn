# File: python/35-dict-deep-dive-part-2.md

# Python Built-in Types

# Dictionary (`dict`) Deep Dive - Part 2: Internals, Advanced Operations & Production Patterns

> **Course:** Backend Engineering Roadmap
>
> **Module:** Built-in Types
>
> **Lesson:** 35
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 4.5 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `dict.update()` | Python 1.0 |
| `dict.setdefault()` | Python 2.0 |
| Dictionary Comprehensions | Python 2.7 |
| Ordered Dictionaries (Language Guarantee) | Python 3.7 |
| Merge Operator (`|`) | Python 3.9 |

### Important Python Version Changes

- Python 3.7 guarantees insertion order.
- Python 3.9 introduced dictionary merging using `|` and `|=`.
- CPython continuously improves dictionary memory usage and lookup performance.

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Hash collisions
- Collision resolution
- Dictionary resizing
- Insertion order
- Dictionary comprehensions
- `update()`
- `setdefault()`
- `fromkeys()`
- Dictionary merging
- Performance considerations
- Production patterns

______________________________________________________________________

# Recap

In Part 1, we learned:

- What dictionaries are
- Hash tables
- Hashable objects
- Dictionary methods
- Dictionary views
- Time complexity

In this lesson, we'll explore how dictionaries remain fast even under heavy workloads and learn advanced dictionary
patterns used in production systems.

______________________________________________________________________

# Hash Collisions

Earlier, we learned that Python computes a hash value.

```
Key

↓

hash()

↓

Bucket
```

But what happens if two different keys produce the same bucket?

This is called a **hash collision**.

______________________________________________________________________

# Collision Example

Imagine a simplified hash table.

```
Bucket 0

Bucket 1

Bucket 2

Bucket 3
```

Suppose

```
"apple"

↓

Bucket 2
```

Later,

```
"orange"

↓

Bucket 2
```

Now two keys want the same location.

______________________________________________________________________

# Does This Break the Dictionary?

No.

Python has collision resolution strategies that allow multiple keys to coexist safely.

Although the exact implementation is complex and CPython-specific, the important point is:

- Python detects collisions.
- It continues searching for another suitable location.
- Lookups remain extremely fast in normal situations.

As backend engineers, you rarely need to know the exact probing algorithm, but you should understand that collisions are
expected and efficiently handled.

______________________________________________________________________

# Why Don't We See Slow Dictionaries?

Because:

- Good hash functions distribute keys well.
- Python automatically resizes dictionaries.
- Hash randomisation reduces malicious collision attacks.

This keeps average lookup performance close to **O(1)**.

______________________________________________________________________

# Dictionary Resizing

Suppose a dictionary starts small.

```
+----+----+----+----+

|    | A  | B  |    |

+----+----+----+----+
```

Eventually it becomes crowded.

```
+----+----+----+----+

| C  | A  | B  | D  |

+----+----+----+----+
```

More collisions begin to occur.

Instead of allowing performance to degrade,

Python creates a larger hash table.

```
Old Table

↓

Create Larger Table

↓

Recalculate Positions

↓

Continue
```

This process is called **resizing**.

______________________________________________________________________

# Why Resize?

Without resizing,

more collisions would occur,

causing slower lookups.

Resizing helps maintain fast average performance.

______________________________________________________________________

# Insertion Order

Modern Python preserves insertion order.

Example

```python
user = {
    "name": "Alice",
    "age": 30,
    "city": "London",
}

print(user)
```

Output

```text
{
    'name': 'Alice',
    'age': 30,
    'city': 'London'
}
```

Notice

The keys appear in the order they were inserted.

______________________________________________________________________

# Updating Doesn't Change Order

```python
user = {
    "name": "Alice",
    "age": 30,
}

user["age"] = 31

print(user)
```

Output

```text
{'name': 'Alice', 'age': 31}
```

The key stays in the same position.

______________________________________________________________________

# Removing and Re-Inserting

```python
user = {
    "name": "Alice",
    "age": 30,
}

del user["name"]

user["name"] = "Alice"

print(user)
```

Output

```text
{'age': 30, 'name': 'Alice'}
```

Re-inserting places the key at the end.

______________________________________________________________________

# update()

Merge one dictionary into another.

```python
user = {
    "name": "Alice"
}

user.update({
    "age": 30,
    "city": "London",
})

print(user)
```

Output

```text
{
    'name': 'Alice',
    'age': 30,
    'city': 'London'
}
```

______________________________________________________________________

# Overwriting Values

```python
settings = {
    "timeout": 30
}

settings.update({
    "timeout": 60
})

print(settings)
```

Output

```text
{'timeout': 60}
```

Existing keys are replaced.

______________________________________________________________________

# Merge Operator (`|`)

Python 3.9 introduced a cleaner syntax.

```python
defaults = {
    "timeout": 30
}

custom = {
    "retries": 5
}

config = defaults | custom

print(config)
```

Output

```text
{
    'timeout': 30,
    'retries': 5
}
```

Unlike `update()`,

the original dictionaries remain unchanged.

______________________________________________________________________

# Merge Assignment (`|=`)

```python
config = {
    "timeout": 30
}

config |= {
    "retries": 5
}

print(config)
```

This modifies the existing dictionary.

______________________________________________________________________

# setdefault()

One of the most misunderstood dictionary methods.

Suppose

```python
counts = {}
```

Normally

```python
if "apple" not in counts:
    counts["apple"] = 0
```

Using `setdefault()`

```python
counts = {}

counts.setdefault("apple", 0)

print(counts)
```

Output

```text
{'apple': 0}
```

______________________________________________________________________

# Existing Keys

```python
counts = {
    "apple": 5
}

counts.setdefault("apple", 0)

print(counts)
```

Output

```text
{'apple': 5}
```

Nothing changes.

______________________________________________________________________

# Production Example

Grouping users.

```python
users = [
    ("Engineering", "Alice"),
    ("Engineering", "Bob"),
    ("HR", "Carol"),
]

departments = {}

for department, employee in users:
    departments.setdefault(
        department,
        []
    ).append(employee)

print(departments)
```

Output

```text
{
    'Engineering': ['Alice', 'Bob'],
    'HR': ['Carol']
}
```

______________________________________________________________________

# fromkeys()

Create multiple keys with the same value.

```python
permissions = dict.fromkeys(
    ["read", "write", "delete"],
    False
)

print(permissions)
```

Output

```text
{
    'read': False,
    'write': False,
    'delete': False
}
```

______________________________________________________________________

# A Common Pitfall

Consider

```python
data = dict.fromkeys(
    ["a", "b", "c"],
    []
)
```

Looks reasonable.

Now

```python
data["a"].append(1)

print(data)
```

Output

```text
{
    'a': [1],
    'b': [1],
    'c': [1]
}
```

Why?

All keys share the same list object.

Always be careful when using mutable default values.

______________________________________________________________________

# Dictionary Comprehensions

Create dictionaries elegantly.

```python
squares = {
    n: n * n
    for n in range(5)
}

print(squares)
```

Output

```text
{
    0: 0,
    1: 1,
    2: 4,
    3: 9,
    4: 16
}
```

______________________________________________________________________

# Conditional Comprehensions

```python
even_squares = {
    n: n * n
    for n in range(10)
    if n % 2 == 0
}

print(even_squares)
```

Output

```text
{
    0: 0,
    2: 4,
    4: 16,
    6: 36,
    8: 64
}
```

______________________________________________________________________

# Reversing a Dictionary

```python
user = {
    "Alice": 101,
    "Bob": 102,
}

reverse = {
    value: key
    for key, value in user.items()
}

print(reverse)
```

Output

```text
{
    101: 'Alice',
    102: 'Bob'
}
```

This only works if the values are unique.

______________________________________________________________________

# Time Complexity

| Operation | Complexity |
|------------|------------|
| Lookup | Average O(1) |
| Insert | Average O(1) |
| Update | Average O(1) |
| Delete | Average O(1) |
| Resize | O(n) |
| Iteration | O(n) |
| Merge | O(n) |

Resizing is infrequent, so overall performance remains excellent.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using `fromkeys()` with mutable values.

```python
dict.fromkeys(keys, [])
```

Every key shares the same list.

______________________________________________________________________

## Mistake 2

Using `setdefault()` when simple assignment is clearer.

Don't overuse it.

______________________________________________________________________

## Mistake 3

Depending on insertion order in Python versions before 3.7.

Only Python 3.7+ guarantees insertion order.

______________________________________________________________________

## Mistake 4

Repeatedly rebuilding dictionaries inside tight loops.

Where possible,

reuse existing dictionaries.

______________________________________________________________________

# Best Practices

✅ Use dictionary comprehensions for simple transformations.

✅ Prefer `|` when merging dictionaries without modifying the originals.

✅ Use `update()` for in-place updates.

✅ Use `setdefault()` for grouping operations.

✅ Be careful with mutable default values.

❌ Don't use `fromkeys()` with mutable objects.

❌ Don't rely on dictionary ordering in code targeting Python versions before 3.7.

______________________________________________________________________

# Production Insight

Dictionaries are heavily used in backend applications.

Configuration merging

```python
config = defaults | environment | user_settings
```

Grouping database results

```python
employees = {}

for department, employee in rows:
    employees.setdefault(
        department,
        []
    ).append(employee)
```

Building lookup tables

```python
users_by_id = {
    user.id: user
    for user in users
}
```

Caching

```python
cache = {
    user.id: user
}
```

Senior backend engineers often use dictionaries to convert repeated database lookups from **O(n)** to **O(1)**.

______________________________________________________________________

# Questions

### Question

> What is a hash collision?

### Answer

A hash collision occurs when two different keys map to the same location in the hash table. Python resolves collisions
internally while maintaining fast average lookup performance.

______________________________________________________________________

### Question

> Why does Python resize dictionaries?

### Answer

As dictionaries become crowded, collisions become more frequent. Resizing creates a larger table, reducing collisions
and maintaining efficient lookups.

______________________________________________________________________

### Question

> When would you use `setdefault()`?

### Answer

It's useful when grouping or accumulating values where keys may not yet exist, such as grouping employees by department.

______________________________________________________________________

### Question

> What is the difference between `update()` and `|`?

### Answer

`update()` modifies the existing dictionary, while `|` creates a new merged dictionary, leaving the originals unchanged.

______________________________________________________________________

### Question

> Why is `dict.fromkeys(keys, [])` dangerous?

### Answer

Because every key references the same list object. Modifying one value affects all keys.

______________________________________________________________________

# Practical Lesson

Create:

```text
dictionary_advanced.py
```

```python
# Merge dictionaries
defaults = {
    "host": "localhost",
    "port": 5432,
}

environment = {
    "port": 5433,
}

config = defaults | environment

print(config)

# Group employees
employees = [
    ("Engineering", "Alice"),
    ("Engineering", "Bob"),
    ("HR", "Carol"),
]

groups = {}

for department, employee in employees:
    groups.setdefault(
        department,
        []
    ).append(employee)

print(groups)

# Dictionary comprehension
squares = {
    n: n * n
    for n in range(5)
}

print(squares)
```

Expected Output

```text
{
    'host': 'localhost',
    'port': 5433
}

{
    'Engineering': ['Alice', 'Bob'],
    'HR': ['Carol']
}

{
    0: 0,
    1: 1,
    2: 4,
    3: 9,
    4: 16
}
```

______________________________________________________________________

# Questions

## Question 1

What is a hash collision?

### Answer

It occurs when two different keys map to the same hash table location. Python resolves collisions internally while
maintaining efficient lookups.

______________________________________________________________________

## Question 2

What is the difference between `update()` and `|`?

### Answer

`update()` modifies the existing dictionary. The `|` operator creates a new merged dictionary.

______________________________________________________________________

## Question 3

When should you use `setdefault()`?

### Answer

When building grouped collections or initialising missing keys without writing explicit existence checks.

______________________________________________________________________

## Question 4

Why is `dict.fromkeys(keys, [])` usually a bug?

### Answer

Because every key shares the same mutable list instance, causing unexpected side effects when one list is modified.

______________________________________________________________________

## Question 5

Why are dictionary comprehensions useful?

### Answer

They provide a concise, readable, and efficient way to construct dictionaries from existing iterables.

______________________________________________________________________

# Assignment

## Exercise 1

Read a CSV file of employees and group them by department using `setdefault()`.

______________________________________________________________________

## Exercise 2

Implement a simple in-memory cache where user IDs are keys and user records are values. Support:

- Add
- Update
- Delete
- Lookup

______________________________________________________________________

## Exercise 3

Merge three configuration dictionaries:

- Default configuration
- Environment-specific configuration
- User configuration

Ensure user values override all others.

______________________________________________________________________

## Exercise 4

Given a list of products, create a dictionary that maps each product ID to the corresponding product using a dictionary
comprehension. Compare lookup performance with searching through the original list.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ How Python handles hash collisions.
- ✅ Why dictionaries resize.
- ✅ How insertion order works.
- ✅ Advanced dictionary methods.
- ✅ Dictionary comprehensions.
- ✅ Dictionary merging.
- ✅ Common production patterns.
- ✅ Performance considerations.
- ✅ Senior backend interview topics.

______________________________________________________________________

# What's Next

**File:** [36-Set-and-Frozenset](36-set-and-frozenset.md)

Topics:

- What is a set?
- How sets work internally
- Hash tables revisited
- Set operations
- Union, intersection, difference
- Symmetric difference
- Frozenset
- Performance
- Real-world backend use cases
- Production best practices

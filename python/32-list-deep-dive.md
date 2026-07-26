# File: python/32-list-deep-dive.md

# Python Built-in Types
# List (`list`) Deep Dive

> **Course:** Backend Engineering Roadmap
>
> **Module:** Built-in Types
>
> **Lesson:** 32
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 4 Hours

---

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `list` | Python 1.0 |
| List Comprehensions | Python 2.0 |
| Extended Iterable Unpacking | Python 3.0 |
| `list.copy()` | Python 3.3 |
| Assignment Expressions (`:=`) (often used with comprehensions) | Python 3.8 |

### Important Python Version Changes

- Lists have existed since the earliest versions of Python.
- Python 3 introduced several improvements to list comprehensions and unpacking.
- Although the API has remained stable, CPython has continuously improved list performance internally.

---

# Learning Objectives

By the end of this lesson, you will understand:

- What a Python list really is
- How lists are stored internally
- Why lists are called dynamic arrays
- Memory allocation and resizing
- List mutability
- List methods
- Copying lists correctly
- Sorting with TimSort
- Time complexity
- Performance considerations
- Production best practices

---

# Recap

In the previous lessons, we completed the **String Deep Dive**, covering:

- String internals
- Unicode
- String methods
- Formatting
- Encoding
- Performance
- Production best practices

Unlike strings, **lists are mutable**, making them one of the most important data structures in Python.

---

# Why Are Lists Important?

Lists are everywhere in backend development.

Examples:

- Database query results
- JSON arrays
- API responses
- Queue processing
- Batch jobs
- Pagination
- CSV rows
- Caching
- Background task processing

If you write Python, you will use lists every day.

---

# What is a List?

A list is an **ordered, mutable collection of objects**.

```python
numbers = [10, 20, 30]
```

A list can store almost anything.

```python
data = [

    10,

    "Python",

    3.14,

    True,

    None,

]
```

Unlike many programming languages, Python lists can contain different object types.

---

# Characteristics of Lists

Lists are:

✅ Ordered

✅ Mutable

✅ Dynamic

✅ Allow duplicate values

✅ Support indexing

✅ Support slicing

---

# Internal Representation

A common misconception is that a list stores the actual objects.

It does **not**.

Instead, a list stores **references (pointers)** to objects.

Example

```python
numbers = [10, 20, 30]
```

Internally

```
numbers

↓

+-------+-------+-------+

|   •   |   •   |   •   |

+-------+-------+-------+

    |       |       |

    ↓       ↓       ↓

   10      20      30
```

The integers live elsewhere in memory.

The list only stores references.

---

# Why Is This Important?

Consider

```python
a = [1, 2, 3]

b = a
```

Memory

```
        +-------------+

a ----> | 1 | 2 | 3 |

        +-------------+

^

|

b
```

Both variables point to the same list.

Modifying one affects the other.

```python
b.append(4)

print(a)
```

Output

```text
[1, 2, 3, 4]
```

---

# Dynamic Arrays

Internally,

Python lists are implemented as **dynamic arrays**.

Unlike a fixed-size array,

they automatically grow when needed.

Imagine a bookshelf.

```
+----+----+----+

| A  | B  | C  |

+----+----+----+
```

Need another book.

Python creates a larger shelf.

```
+----+----+----+----+----+

| A  | B  | C  |    |    |

+----+----+----+----+----+
```

Copies the references,

then continues.

---

# Why Not Resize Every Time?

Imagine adding one million items.

If Python resized after every append,

performance would be terrible.

Instead,

Python allocates extra space.

Example

```
Current Size

↓

100

Allocated Capacity

↓

128
```

The next 28 appends require no resizing.

---

# Amortised O(1)

People often ask:

"Why is append O(1) if resizing happens?"

Because resizing is rare.

Suppose

```
Append

↓

No Resize

↓

Append

↓

No Resize

↓

Append

↓

Resize Once

↓

Many More Appends
```

Most appends are extremely fast.

Average complexity

```
O(1)
```

This is called **amortised constant time**.

---

# Creating Lists

```python
numbers = [1, 2, 3]

names = list(("Alice", "Bob"))

letters = list("Python")
```

Output

```text
['P', 'y', 't', 'h', 'o', 'n']
```

---

# Indexing

```python
names = [

    "Alice",

    "Bob",

    "Charlie"

]

print(names[0])
```

Output

```text
Alice
```

Negative indexing

```python
print(names[-1])
```

Output

```text
Charlie
```

---

# Slicing

Exactly like strings.

```python
numbers = [10, 20, 30, 40, 50]

print(numbers[1:4])
```

Output

```text
[20, 30, 40]
```

Reverse

```python
print(numbers[::-1])
```

Output

```text
[50, 40, 30, 20, 10]
```

---

# Mutability

Unlike strings,

lists can be modified.

```python
numbers = [1, 2, 3]

numbers[0] = 100

print(numbers)
```

Output

```text
[100, 2, 3]
```

---

# append()

Adds one element.

```python
users = ["Alice"]

users.append("Bob")

print(users)
```

Output

```text
['Alice', 'Bob']
```

Complexity

```
Amortised O(1)
```

---

# extend()

Adds multiple elements.

```python
a = [1, 2]

b = [3, 4]

a.extend(b)

print(a)
```

Output

```text
[1, 2, 3, 4]
```

---

# append() vs extend()

```python
a = [1, 2]

a.append([3, 4])

print(a)
```

Output

```text
[1, 2, [3, 4]]
```

Whereas

```python
a = [1, 2]

a.extend([3, 4])

print(a)
```

Output

```text
[1, 2, 3, 4]
```

favourite Questions.

---

# insert()

```python
numbers = [1, 3]

numbers.insert(1, 2)

print(numbers)
```

Output

```text
[1, 2, 3]
```

Complexity

```
O(n)
```

because existing elements must shift.

---

# remove()

Removes first matching value.

```python
numbers = [1, 2, 3, 2]

numbers.remove(2)

print(numbers)
```

Output

```text
[1, 3, 2]
```

---

# pop()

Removes by index.

```python
numbers = [1, 2, 3]

value = numbers.pop()

print(value)
```

Output

```text
3
```

Last element

```
O(1)
```

Middle element

```
O(n)
```

---

# clear()

```python
numbers = [1, 2, 3]

numbers.clear()

print(numbers)
```

Output

```text
[]
```

---

# Membership Testing

```python
users = [

    "Alice",

    "Bob",

]

print("Bob" in users)
```

Output

```text
True
```

Complexity

```
O(n)
```

Python searches sequentially.

---

# Sorting

```python
numbers = [5, 2, 4, 1]

numbers.sort()

print(numbers)
```

Output

```text
[1, 2, 4, 5]
```

---

# sorted()

Unlike

```python
sort()
```

it returns a new list.

```python
numbers = [3, 1, 2]

result = sorted(numbers)

print(numbers)

print(result)
```

Output

```text
[3, 1, 2]

[1, 2, 3]
```

---

# TimSort

Python uses **TimSort**.

TimSort is:

- Stable
- Very fast
- Optimised for partially sorted data

Time complexity

Best

```
O(n)
```

Average

```
O(n log n)
```

Worst

```
O(n log n)
```

---

# key Parameter

Sort users by age.

```python
users = [

    {"name": "Alice", "age": 30},

    {"name": "Bob", "age": 22},

]

users.sort(

    key=lambda user: user["age"]

)

print(users)
```

Production code frequently uses `key`.

---

# Reverse Sorting

```python
numbers = [1, 5, 2]

numbers.sort(reverse=True)

print(numbers)
```

Output

```text
[5, 2, 1]
```

---

# Shallow Copy

```python
a = [1, 2, 3]

b = a.copy()
```

Memory

```
a

↓

+-------------+

|1|2|3|

+-------------+

b

↓

+-------------+

|1|2|3|

+-------------+
```

Two different list objects.

---

# Nested Lists

```python
a = [[1], [2]]

b = a.copy()

b[0].append(99)

print(a)
```

Output

```text
[[1, 99], [2]]
```

Why?

Only the outer list was copied.

Inner lists are shared.

We covered deep copies earlier in the course.

---

# List Comprehension

Already introduced earlier,

but worth revisiting.

```python
numbers = [1, 2, 3, 4]

squares = [

    n * n

    for n in numbers

]

print(squares)
```

Output

```text
[1, 4, 9, 16]
```

Use comprehensions when they improve readability.

---

# Time Complexity Summary

| Operation | Complexity |
|------------|------------|
| Index | O(1) |
| Assignment | O(1) |
| Append | Amortised O(1) |
| Pop Last | O(1) |
| Insert Middle | O(n) |
| Remove | O(n) |
| Search | O(n) |
| Sort | O(n log n) |
| Slice | O(k) |
| Copy | O(n) |

---

# Common Mistakes

## Mistake 1

Using

```python
b = a
```

when a copy was intended.

---

## Mistake 2

Using

```python
insert(0, value)
```

inside large loops.

Every insertion shifts the remaining elements.

---

## Mistake 3

Using lists for frequent membership testing.

```python
if username in users:
```

With one million users,

this becomes expensive.

Use a set instead.

---

## Mistake 4

Using

```python
sort()
```

when the original order must be preserved.

Use

```python
sorted()
```

instead.

---

# Best Practices

✅ Use `append()` for growing lists.

✅ Use `extend()` to merge iterables.

✅ Prefer `sorted()` when you need to preserve the original list.

✅ Use `key=` instead of writing custom comparison logic.

✅ Use list comprehensions for simple transformations.

❌ Don't use lists when uniqueness is required.

❌ Don't use lists for frequent membership checks on large datasets.

---

# Production Insight

Lists are one of the most common data structures in backend systems.

Examples include:

- Results from SQL queries

```python
users = cursor.fetchall()
```

- FastAPI responses

```python
return users
```

- JSON arrays

```json
[
  {
    "id": 1
  },
  {
    "id": 2
  }
]
```

- Processing batches of Kafka messages.

- Collecting log entries before writing them to storage.

Choosing the right operations on lists can significantly affect application performance.

---

# Questions

### Question

> Why is `append()` considered O(1) if lists sometimes resize?

### Answer

Because Python over-allocates memory. Most appends don't require resizing, making the average (amortised) complexity O(1).

---

### Question

> What is the difference between `append()` and `extend()`?

### Answer

`append()` adds a single object to the end of the list, while `extend()` iterates over another iterable and adds each element individually.

---

### Question

> Why is membership testing in a list O(n)?

### Answer

Because Python searches elements sequentially until it finds a match or reaches the end of the list.

---

### Question

> Why is Python's sort stable?

### Answer

A stable sort preserves the relative order of elements with equal keys, allowing multiple sorting passes without losing previous ordering.

---

# Practical Lesson

Create:

```text
list_examples.py
```

```python
# List creation
numbers = [5, 3, 1]

# Append a new element
numbers.append(4)

# Insert at a specific position
numbers.insert(0, 10)

# Sort the list
numbers.sort()

print(numbers)

# Demonstrate append vs extend
items = [1, 2]

items.append([3, 4])
print(items)

items = [1, 2]
items.extend([3, 4])
print(items)

# Demonstrate copying
original = ["Alice", "Bob"]
copy = original.copy()

copy.append("Charlie")

print(original)
print(copy)
```

Expected Output

```text
[1, 3, 4, 5, 10]

[1, 2, [3, 4]]

[1, 2, 3, 4]

['Alice', 'Bob']

['Alice', 'Bob', 'Charlie']
```

---

# Questions

## Question 1

Why are Python lists called dynamic arrays?

### Answer

Because they automatically resize as elements are added, unlike fixed-size arrays.

---

## Question 2

Why is `append()` usually faster than `insert(0, value)`?

### Answer

`append()` typically adds an element to unused capacity at the end, while inserting at the beginning shifts every existing element.

---

## Question 3

What is the difference between `sort()` and `sorted()`?

### Answer

`sort()` modifies the original list in place, whereas `sorted()` returns a new sorted list and leaves the original unchanged.

---

## Question 4

Why does a shallow copy not protect nested objects?

### Answer

A shallow copy duplicates only the outer list. Nested mutable objects are still shared between both lists.

---

## Question 5

When should you use a list instead of a set?

### Answer

Use a list when element order matters, duplicates are allowed, or indexed access is required.

---

# Assignment

## Exercise 1

Implement a student management program that supports:

- Add student
- Remove student
- Update student
- Display all students

Use only lists.

---

## Exercise 2

Sort a list of dictionaries representing employees by:

- Age
- Salary
- Name

using the `key` parameter.

---

## Exercise 3

Read a CSV file into a list of dictionaries and sort the records by multiple fields.

---

## Exercise 4

Measure the execution time of:

- `append()`
- `insert(0, value)`

for 100,000 operations and compare the results.

---

# Summary

In this lesson, you learned:

- ✅ How Python lists are implemented internally.
- ✅ Why lists are dynamic arrays.
- ✅ Why `append()` is amortised O(1).
- ✅ The most important list methods.
- ✅ Sorting with TimSort.
- ✅ Shallow copying.
- ✅ Performance characteristics of list operations.
- ✅ Production use cases.
- ✅ Common interview topics.

---

# What's Next

**File:**
[33-Tuple-Deep-Dive](33-tuple-deep-dive.md)

Topics:

- What is a tuple?
- Tuple internals
- Immutability
- Memory efficiency
- Packing and unpacking
- Hashability
- Named tuples (recap)
- Tuple vs List
- Performance comparisons
- Production examples

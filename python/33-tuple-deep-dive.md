# File: python/33-tuple-deep-dive.md

# Python Built-in Types

# Tuple (`tuple`) Deep Dive

> **Course:** Backend Engineering Roadmap
>
> **Module:** Built-in Types
>
> **Lesson:** 33
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 3 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `tuple` | Python 1.0 |
| Tuple Packing | Python 1.0 |
| Tuple Unpacking | Python 1.0 |
| Extended Iterable Unpacking | Python 3.0 |

### Important Python Version Changes

- Tuples have existed since the first release of Python.
- Python 3 introduced **extended unpacking** (`*rest`), making tuple unpacking much more flexible.
- Tuples are still one of the fastest and most memory-efficient built-in data structures.

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What a tuple is
- Why tuples exist
- Tuple internals
- Tuple immutability
- Tuple packing and unpacking
- Extended unpacking
- Hashability
- Tuple methods
- Tuple vs List
- Performance considerations
- Production best practices

______________________________________________________________________

# Recap

In the previous lesson, we learned about Python Lists.

Lists are:

- Ordered
- Mutable
- Dynamic

Today's topic is the **Tuple**.

Although tuples look very similar to lists, they serve a completely different purpose.

Understanding when to use each is a common senior backend interview topic.

______________________________________________________________________

# Why Do Tuples Exist?

A common beginner question is:

> "If lists already exist, why do we need tuples?"

The answer is:

A tuple represents **data that should not change**.

Examples:

- Database primary key
- Geographic coordinates
- RGB colour values
- Date (year, month, day)
- Configuration values
- Function return values

If the data should remain constant, a tuple communicates that intent.

______________________________________________________________________

# What is a Tuple?

A tuple is an **ordered, immutable collection of objects**.

Example:

```python
coordinates = (10, 20)

print(coordinates)
```

Output

```text
(10, 20)
```

Like lists, tuples:

- Preserve order
- Allow duplicate values
- Support indexing
- Support slicing

Unlike lists, they **cannot be modified** after creation.

______________________________________________________________________

# Tuple Characteristics

Tuples are:

✅ Ordered

✅ Immutable

✅ Faster than lists for many operations

✅ Memory efficient

✅ Hashable (if all elements are hashable)

______________________________________________________________________

# Internal Representation

Like lists,

tuples do **not** store objects directly.

They store references.

```
tuple

↓

+-------+-------+-------+

|   •   |   •   |   •   |

+-------+-------+-------+

    |       |       |

    ↓       ↓       ↓

   10      20      30
```

This is similar to lists.

The major difference is that the tuple's size cannot change after creation.

______________________________________________________________________

# Why Are Tuples Immutable?

Suppose

```python
point = (10, 20)

point[0] = 100
```

Output

```text
TypeError:
'tuple' object does not support item assignment
```

Python prevents modification.

This gives several advantages:

- Predictable behaviour
- Thread safety
- Hashability
- Performance optimisations

______________________________________________________________________

# Creating Tuples

Using parentheses

```python
numbers = (1, 2, 3)
```

Using the constructor

```python
numbers = tuple([1, 2, 3])
```

From a string

```python
letters = tuple("Python")

print(letters)
```

Output

```text
('P', 'y', 't', 'h', 'o', 'n')
```

______________________________________________________________________

# Single Element Tuple

A common beginner mistake.

Wrong

```python
value = (10)

print(type(value))
```

Output

```text
<class 'int'>
```

Correct

```python
value = (10,)

print(type(value))
```

Output

```text
<class 'tuple'>
```

The comma creates the tuple.

Not the parentheses.

______________________________________________________________________

# Empty Tuple

```python
empty = ()

print(type(empty))
```

Output

```text
<class 'tuple'>
```

______________________________________________________________________

# Indexing

```python
languages = (

    "Python",

    "Go",

    "Rust",

)

print(languages[1])
```

Output

```text
Go
```

Negative indexing

```python
print(languages[-1])
```

Output

```text
Rust
```

______________________________________________________________________

# Slicing

```python
numbers = (10, 20, 30, 40, 50)

print(numbers[1:4])
```

Output

```text
(20, 30, 40)
```

Reverse

```python
print(numbers[::-1])
```

Output

```text
(50, 40, 30, 20, 10)
```

Like strings,

slicing creates a new tuple.

______________________________________________________________________

# Tuple Packing

Packing means combining multiple values into one tuple.

```python
person = "Alice", 30, "Engineer"

print(person)
```

Output

```text
('Alice', 30, 'Engineer')
```

Notice

No parentheses are required.

The comma performs the packing.

______________________________________________________________________

# Tuple Unpacking

Python can unpack tuples automatically.

```python
person = ("Alice", 30)

name, age = person

print(name)
print(age)
```

Output

```text
Alice
30
```

Very common in production code.

______________________________________________________________________

# Extended Unpacking

Python 3 introduced extended unpacking.

```python
numbers = (1, 2, 3, 4, 5)

first, *middle, last = numbers

print(first)
print(middle)
print(last)
```

Output

```text
1
[2, 3, 4]
5
```

Notice

`middle` becomes a list.

Not a tuple.

______________________________________________________________________

# Swapping Variables

One of Python's nicest features.

Instead of

```python
temp = a
a = b
b = temp
```

Simply write

```python
a = 10
b = 20

a, b = b, a
```

Internally,

Python uses tuple packing and unpacking.

______________________________________________________________________

# Returning Multiple Values

Functions often return multiple values.

```python
def get_user():

    return "Alice", 30
```

Usage

```python
name, age = get_user()

print(name)
print(age)
```

Python automatically packs the return values into a tuple.

______________________________________________________________________

# Tuple Methods

Tuples have only two methods.

______________________________________________________________________

# count()

```python
numbers = (1, 2, 2, 3)

print(numbers.count(2))
```

Output

```text
2
```

______________________________________________________________________

# index()

```python
numbers = (10, 20, 30)

print(numbers.index(20))
```

Output

```text
1
```

______________________________________________________________________

# Why So Few Methods?

Lists have many methods because they are mutable.

Tuples cannot change.

Therefore,

methods like

- append()
- extend()
- remove()
- insert()

do not exist.

______________________________________________________________________

# Tuple Concatenation

```python
a = (1, 2)

b = (3, 4)

print(a + b)
```

Output

```text
(1, 2, 3, 4)
```

A new tuple is created.

______________________________________________________________________

# Tuple Repetition

```python
print(("Hi",) * 3)
```

Output

```text
('Hi', 'Hi', 'Hi')
```

______________________________________________________________________

# Membership Testing

```python
users = (

    "Alice",

    "Bob",

)

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

Like lists,

membership requires sequential search.

______________________________________________________________________

# Hashability

One of the biggest differences between tuples and lists.

List

```python
users = [1, 2]

data = {

    users: "Admin"

}
```

Output

```text
TypeError:
unhashable type: 'list'
```

Tuple

```python
users = (1, 2)

data = {

    users: "Admin"

}

print(data)
```

Output

```text
{(1, 2): 'Admin'}
```

______________________________________________________________________

# Why Are Tuples Hashable?

Because immutable objects can safely produce a hash.

If an object changed after being used as a dictionary key,

the dictionary would become inconsistent.

______________________________________________________________________

# Nested Mutable Objects

Immutability only applies to the tuple itself.

Example

```python
data = (

    [1, 2],

    [3, 4],

)

data[0].append(99)

print(data)
```

Output

```text
([1, 2, 99], [3, 4])
```

Why?

The tuple is immutable,

but the list inside it is still mutable.

This is a favourite interview question.

______________________________________________________________________

# Tuple vs List

| Feature | Tuple | List |
|----------|-------|------|
| Mutable | ❌ | ✅ |
| Ordered | ✅ | ✅ |
| Hashable | Usually | ❌ |
| Memory Usage | Lower | Higher |
| Speed | Faster | Slightly Slower |
| Append | ❌ | ✅ |
| Insert | ❌ | ✅ |
| Remove | ❌ | ✅ |

______________________________________________________________________

# Performance

Creating tuples is generally slightly faster than lists.

Memory usage is also lower because tuples don't need extra capacity for resizing.

However,

choose a tuple **because it represents immutable data**, not just because it's slightly faster.

Readability and correctness matter more than micro-optimisations.

______________________________________________________________________

# Time Complexity

| Operation | Complexity |
|------------|------------|
| Index | O(1) |
| Slice | O(k) |
| Search | O(n) |
| Count | O(n) |
| Concatenation | O(n) |
| Membership | O(n) |

______________________________________________________________________

# Common Mistakes

## Mistake 1

Forgetting the comma.

Wrong

```python
item = (5)
```

Correct

```python
item = (5,)
```

______________________________________________________________________

## Mistake 2

Trying to modify a tuple.

```python
point[0] = 50
```

Produces

```text
TypeError
```

______________________________________________________________________

## Mistake 3

Assuming nested objects become immutable.

Only the tuple itself is immutable.

Objects inside it may still change.

______________________________________________________________________

## Mistake 4

Using tuples everywhere for performance.

Choose tuples because the data should remain constant,

not because they are slightly faster.

______________________________________________________________________

# Best Practices

✅ Use tuples for fixed collections of values.

✅ Return multiple values using tuples.

✅ Use tuple unpacking to improve readability.

✅ Use tuples as dictionary keys when appropriate.

❌ Don't store frequently changing data in tuples.

❌ Don't rely on tuple immutability if it contains mutable objects.

______________________________________________________________________

# Production Insight

Tuples appear frequently in backend systems.

Examples:

Returning multiple values

```python
def authenticate():

    return user, token
```

Database coordinates

```python
location = (12.9716, 77.5946)
```

Dictionary keys

```python
cache = {

    ("GET", "/users"): response

}
```

Multiple-value iteration

```python
for name, age in users:
    print(name, age)
```

Python's own standard library returns tuples in many APIs because they clearly communicate that the returned values
should not be modified.

______________________________________________________________________

# Questions

### Question

> What is the difference between a tuple and a list?

### Answer

A tuple is immutable and generally more memory-efficient, while a list is mutable and designed for collections that
change over time.

______________________________________________________________________

### Question

> Why can tuples be dictionary keys but lists cannot?

### Answer

Tuples are immutable and hashable (provided all their elements are hashable), making them safe dictionary keys. Lists
are mutable, so their hash value could change.

______________________________________________________________________

### Question

> Does tuple immutability guarantee that its contents cannot change?

### Answer

No. If a tuple contains mutable objects such as lists, those objects can still be modified.

______________________________________________________________________

### Question

> Why do functions often return tuples?

### Answer

Tuples provide a simple and efficient way to return multiple related values while signalling that the returned structure
itself should not be modified.

______________________________________________________________________

# Practical Lesson

Create:

```text
tuple_examples.py
```

```python
# Packing values
employee = ("Alice", 30, "Engineer")

# Unpacking
name, age, role = employee

print(name)
print(age)
print(role)

# Extended unpacking
numbers = (10, 20, 30, 40, 50)

first, *middle, last = numbers

print(first)
print(middle)
print(last)

# Tuple as dictionary key
cache = {
    ("GET", "/users"): "Cached Response"
}

print(cache[("GET", "/users")])

# Tuple containing a mutable object
data = ([1, 2],)

data[0].append(3)

print(data)
```

Expected Output

```text
Alice
30
Engineer

10
[20, 30, 40]
50

Cached Response

([1, 2, 3],)
```

______________________________________________________________________

# Questions

## Question 1

Why are tuples immutable?

### Answer

Immutability provides predictable behaviour, enables hashing, reduces memory overhead and makes tuples suitable for
fixed collections of data.

______________________________________________________________________

## Question 2

What is tuple packing?

### Answer

Packing is the automatic creation of a tuple from multiple comma-separated values.

______________________________________________________________________

## Question 3

What is tuple unpacking?

### Answer

Unpacking assigns individual tuple elements to separate variables in a single statement.

______________________________________________________________________

## Question 4

Can a tuple contain mutable objects?

### Answer

Yes. The tuple itself cannot change, but mutable objects stored inside it can still be modified.

______________________________________________________________________

## Question 5

When should you choose a tuple over a list?

### Answer

When the collection represents fixed, unchanging data or needs to be hashable for use as a dictionary key or set
element.

______________________________________________________________________

# Assignment

## Exercise 1

Write a function that returns a student's:

- Name
- Marks
- Grade

using a tuple, then unpack the returned values.

______________________________________________________________________

## Exercise 2

Implement a simple cache where the key is a tuple of:

- HTTP method
- URL
- Query parameters

Store and retrieve cached responses.

______________________________________________________________________

## Exercise 3

Demonstrate the difference between a tuple containing integers and a tuple containing lists. Explain why one is
completely immutable while the other is not.

______________________________________________________________________

## Exercise 4

Create a program that swaps the values of three variables using tuple unpacking without using a temporary variable.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What tuples are and why they exist.
- ✅ How tuples differ from lists.
- ✅ Tuple packing and unpacking.
- ✅ Extended unpacking.
- ✅ Hashability and dictionary keys.
- ✅ Performance and memory characteristics.
- ✅ Common interview topics.
- ✅ Production use cases.

______________________________________________________________________

# What's Next

**File:** [34-Dict-Deep-Dive-part-1](34-dict-deep-dive-part-1.md)

Topics:

- What is a dictionary?
- Hash tables
- How dictionaries work internally
- Hashing
- Dictionary operations
- Dictionary methods
- Time complexity
- Common pitfalls
- Production examples

> **Note:** Dictionaries are one of Python's most important data structures. To cover them properly—including hash tables, collision handling, resizing, ordering, views, merging, and production patterns—we'll split the topic into **two parts**.

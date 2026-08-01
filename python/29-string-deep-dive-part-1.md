# File: python/29-string-deep-dive-part-1.md

# Python Built-in Types

# String (`str`) Deep Dive - Part 1: Foundations & Internals

> **Course:** Backend Engineering Roadmap
>
> **Module:** Built-in Types
>
> **Lesson:** 29
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 2.5 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `str` | Python 1.0 |
| Unicode `str` by default | Python 3.0 |
| f-strings (covered in Part 2) | Python 3.6 |

### Important Python Version Changes

Python 2 had two text types:

- `str` → bytes
- `unicode` → Unicode text

Python 3 simplified this:

- `str` → Unicode text
- `bytes` → Binary data

Understanding this distinction is essential when working with APIs, databases, files and network programming.

______________________________________________________________________

# Learning Objectives

By the end of this lesson you will understand:

- What a Python string really is
- Unicode fundamentals
- `str` vs `bytes`
- Why strings are immutable
- String interning
- Identity vs equality
- Indexing
- Slicing
- Iteration
- Membership testing
- Time complexity
- Production best practices

______________________________________________________________________

# Why Are Strings Important?

Almost every backend application processes text.

Examples include:

- HTTP requests
- JSON
- SQL queries
- JWT tokens
- Email addresses
- URLs
- Log files
- CSV data
- XML
- HTML
- Configuration files

A solid understanding of strings improves both correctness and performance.

______________________________________________________________________

# What Is a String?

A string is an **immutable sequence of Unicode characters**.

```python
name = "Alice"
```

Think of a string as:

```
"Alice"

↓

Sequence

↓

['A', 'l', 'i', 'c', 'e']
```

Unlike a list, each character cannot be modified after the string is created.

______________________________________________________________________

# Unicode

Computers understand numbers, not letters.

Unicode assigns every character a unique code point.

Examples:

| Character | Code Point |
|-----------|-----------:|
| A | U+0041 |
| a | U+0061 |
| ₹ | U+20B9 |
| 😀 | U+1F600 |

Because Python 3 strings are Unicode, they can represent text from virtually every language.

```python
city = "Bengaluru"
emoji = "😀"
currency = "₹"
```

______________________________________________________________________

# Unicode vs Encoding

Unicode defines **what** a character is.

Encoding defines **how** that character is stored as bytes.

Example:

```
Character

↓

Unicode

↓

UTF-8 Encoding

↓

Bytes

↓

Disk / Network
```

Python automatically converts between Unicode strings and bytes when you explicitly encode or decode.

We'll cover encoding in depth in Part 2.

______________________________________________________________________

# str vs bytes

This is one of the most common interview questions.

```python
text = "Hello"

data = b"Hello"
```

Type check:

```python
print(type(text))
print(type(data))
```

Output:

```
<class 'str'>
<class 'bytes'>
```

### Think of it this way

```
str

↓

Human-readable text
```

```
bytes

↓

Raw binary data
```

When reading a file or receiving data from a socket, you often get bytes that must be decoded into a string.

______________________________________________________________________

# Why Are Strings Immutable?

Attempting to modify a character raises an error.

```python
name = "Alice"

name[0] = "B"
```

Output:

```
TypeError
```

Instead:

```python
name = "Alice"

name = "B" + name[1:]

print(name)
```

Output:

```
Blice
```

A new string object is created.

______________________________________________________________________

# Benefits of Immutability

Immutability provides several advantages:

- Thread safety
- Hashability
- Predictable behaviour
- Optimisations inside CPython
- Cached hash values

Because strings cannot change, they are safe to use as dictionary keys.

```python
users = {
    "alice": 1,
    "bob": 2,
}
```

______________________________________________________________________

# String Interning

CPython sometimes reuses identical string objects to save memory.

```python
a = "python"
b = "python"

print(a is b)
```

Output (usually):

```
True
```

Both variables often reference the same object.

______________________________________________________________________

# Why Intern Strings?

Without interning:

```
"python"

↓

Object 1

"python"

↓

Object 2
```

With interning:

```
"python"

↓

Single Object

↑      ↑

a      b
```

This reduces memory usage and speeds up comparisons.

______________________________________________________________________

# sys.intern()

You can explicitly intern strings.

```python
import sys

a = sys.intern("backend")
b = sys.intern("backend")

print(a is b)
```

Output:

```
True
```

Interning is useful when the same strings occur many thousands of times (e.g. identifiers or tokens).

______________________________________________________________________

# Identity vs Equality

Another common interview topic.

```python
a = "hello"
b = "hello"
```

Equality:

```python
print(a == b)
```

Checks whether the values are equal.

Identity:

```python
print(a is b)
```

Checks whether both variables refer to the same object.

Always use:

```python
==
```

to compare strings.

Do not rely on:

```python
is
```

______________________________________________________________________

# Indexing

Every character has an index.

```
H  e  l  l  o

0  1  2  3  4
```

Access:

```python
text = "Hello"

print(text[1])
```

Output:

```
e
```

Negative indexing:

```
H  e  l  l  o

-5 -4 -3 -2 -1
```

```python
print(text[-1])
```

Output:

```
o
```

______________________________________________________________________

# Slicing

Syntax:

```python
text[start:stop:step]
```

Example:

```python
text = "Backend"

print(text[0:4])
```

Output:

```
Back
```

______________________________________________________________________

# Omitting Values

Beginning:

```python
text[:4]
```

End:

```python
text[4:]
```

Entire string:

```python
text[:]
```

______________________________________________________________________

# Step

```python
text = "Backend"

print(text[::2])
```

Output:

```
Bcek
```

Reverse:

```python
print(text[::-1])
```

Output:

```
dnekcaB
```

______________________________________________________________________

# Why Doesn't Slicing Modify the Original String?

```python
text = "Python"

part = text[:3]
```

Memory:

```
"Python"

↓

New String

↓

"Pyt"
```

Strings are immutable, so slicing always creates a new string object.

______________________________________________________________________

# Iterating Over Strings

```python
word = "API"

for char in word:
    print(char)
```

Output:

```
A
P
I
```

This works because strings implement the iterator protocol.

______________________________________________________________________

# Membership Testing

```python
text = "Backend Engineering"

print("Backend" in text)
```

Output:

```
True
```

Checking for absence:

```python
print("Java" not in text)
```

Output:

```
True
```

Membership testing is highly optimised in CPython.

______________________________________________________________________

# String Comparison

Strings are compared lexicographically.

```python
print("apple" < "banana")
```

Output:

```
True
```

Comparison is based on Unicode code points.

Be aware that uppercase and lowercase letters have different code points.

```python
print("Apple" < "apple")
```

Output:

```
True
```

______________________________________________________________________

# Time Complexity

| Operation | Complexity |
|-----------|------------|
| Indexing | O(1) |
| Slicing | O(k) |
| Concatenation (`+`) | O(n) |
| Membership (`in`) | O(n) |
| Length (`len`) | O(1) |
| Iteration | O(n) |

Understanding these complexities helps you write efficient code.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using `is` for string comparison.

```python
if username is "admin":
```

Incorrect.

Use:

```python
if username == "admin":
```

______________________________________________________________________

## Mistake 2

Assuming slicing modifies the original string.

It always creates a new string.

______________________________________________________________________

## Mistake 3

Confusing `str` with `bytes`.

Remember:

```
Text

↓

str
```

```
Binary

↓

bytes
```

______________________________________________________________________

# Best Practices

✅ Treat strings as immutable values.

✅ Use `==` for comparison.

✅ Use Unicode (`str`) for application logic.

✅ Decode bytes as early as possible and encode as late as possible.

✅ Learn slicing well—it appears frequently in interviews.

______________________________________________________________________

# Production Insight

Backend engineers work with strings constantly:

- Parsing URLs
- Reading HTTP headers
- Processing JSON
- Building SQL queries (prefer parameterised queries!)
- Logging
- Authentication tokens
- Environment variables

A strong understanding of string fundamentals makes all of these tasks easier and less error-prone.

______________________________________________________________________

# Questions

### Question

> Why are Python strings immutable?

### Answer

Immutability makes strings hashable, thread-safe and allows CPython to optimise memory usage and cache hash values.

______________________________________________________________________

### Question

> What is the difference between `str` and `bytes`?

### Answer

`str` represents Unicode text, while `bytes` represents raw binary data. Text must be encoded into bytes before
transmission or storage and decoded back into text when read.

______________________________________________________________________

### Question

> What is string interning?

### Answer

String interning is an optimisation where identical strings share the same object in memory, reducing memory usage and
improving comparison performance.

______________________________________________________________________

### Question

> Why is indexing O(1) but slicing O(k)?

### Answer

Indexing directly accesses one character, while slicing creates a new string by copying `k` characters.

______________________________________________________________________

# Assignment

1. Explain the difference between `==` and `is` using string examples.
1. Write a program that reverses a string using slicing.
1. Demonstrate positive and negative indexing on the string `"OpenAI"`.
1. Create examples showing why strings can be used as dictionary keys.
1. Experiment with `sys.intern()` and observe object identities using `id()`.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What a Python string is.
- ✅ Unicode fundamentals.
- ✅ The difference between `str` and `bytes`.
- ✅ Why strings are immutable.
- ✅ String interning.
- ✅ Identity vs equality.
- ✅ Indexing and slicing.
- ✅ Iteration and membership testing.
- ✅ Time complexity of common operations.
- ✅ Production and interview insights.

______________________________________________________________________

# What's Next

**File:** [30-String-Deep-Dive-part-2](30-string-deep-dive-part-2.md)

Topics:

- Essential string methods
- Searching and replacing
- Splitting and joining
- Formatting (`%`, `.format()`, f-strings)
- Encoding and decoding
- Production examples
- Performance tips

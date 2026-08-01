# File: python/30-string-deep-dive-part-2.md

# Python Built-in Types

# String (`str`) Deep Dive - Part 2: Methods, Formatting & Encoding

> **Course:** Backend Engineering Roadmap
>
> **Module:** Built-in Types
>
> **Lesson:** 30
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 3 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `split()` | Python 1.0 |
| `join()` | Python 1.6 |
| `partition()` | Python 2.5 |
| `str.format()` | Python 2.6 |
| f-strings | Python 3.6 |
| `removeprefix()` | Python 3.9 |
| `removesuffix()` | Python 3.9 |

### Important Python Version Changes

- `%` formatting is legacy but still appears in older codebases.
- `.format()` was introduced to provide a more flexible formatting API.
- **f-strings** are now the preferred formatting approach because they are concise, readable and generally the fastest.

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- String searching
- String splitting
- Joining strings efficiently
- Replacing text
- Prefix and suffix checking
- String formatting
- f-strings
- Encoding & decoding
- Common production patterns
- Performance best practices

______________________________________________________________________

# Recap

Previously we learned:

- What a string is
- Unicode
- `str` vs `bytes`
- Immutability
- String interning
- Indexing
- Slicing
- Iteration
- Time complexity

Now we'll learn how professional backend engineers manipulate strings every day.

______________________________________________________________________

# Why Learn String Methods?

Imagine writing a backend API.

Incoming request

```
"   john@example.com   "
```

Desired output

```
john@example.com
```

Or

```
"apple,banana,orange"
```

Needs to become

```
["apple", "banana", "orange"]
```

String methods solve these everyday problems.

______________________________________________________________________

# strip()

One of the most frequently used methods.

Removes whitespace from both ends.

```python
text = "   Hello World   "

print(text.strip())
```

Output

```
Hello World
```

Notice

The original string is unchanged.

______________________________________________________________________

# lstrip()

Removes only leading whitespace.

```python
text = "   Python"

print(text.lstrip())
```

Output

```
Python
```

______________________________________________________________________

# rstrip()

Removes trailing whitespace.

```python
text = "Python   "

print(text.rstrip())
```

Output

```
Python
```

______________________________________________________________________

# Production Example

User input

```python
username = input().strip()
```

Without `.strip()`

```
"admin "

≠

"admin"
```

A simple trailing space could cause authentication failures.

______________________________________________________________________

# split()

Splits a string into a list.

```python
text = "apple,banana,orange"

print(text.split(","))
```

Output

```
['apple', 'banana', 'orange']
```

______________________________________________________________________

# Default Behaviour

Without an argument

```python
text = "Python   is   awesome"

print(text.split())
```

Output

```
['Python', 'is', 'awesome']
```

Multiple spaces are handled automatically.

______________________________________________________________________

# maxsplit

```python
text = "A-B-C-D"

print(text.split("-", 2))
```

Output

```
['A', 'B', 'C-D']
```

Only two splits occur.

______________________________________________________________________

# rsplit()

Splits from the right.

```python
path = "logs/app/server.log"

print(path.rsplit("/", 1))
```

Output

```
['logs/app', 'server.log']
```

Useful for file paths.

______________________________________________________________________

# splitlines()

Splits text into lines.

```python
text = "Line1\nLine2\nLine3"

print(text.splitlines())
```

Output

```
['Line1', 'Line2', 'Line3']
```

Common when reading log files.

______________________________________________________________________

# join()

The opposite of `split()`.

```python
words = [

    "Python",

    "Backend",

    "API"

]

print(" ".join(words))
```

Output

```
Python Backend API
```

______________________________________________________________________

# Why Doesn't join() Belong to list?

This often confuses beginners.

Instead of

```python
words.join(" ")
```

Python uses

```python
" ".join(words)
```

Reason:

The separator performs the joining.

Think

```
Separator

↓

Insert Between Items
```

______________________________________________________________________

# join() vs +

Suppose

```python
result = ""

for word in words:

    result += word
```

Python repeatedly creates new string objects.

Memory

```
A

↓

AB

↓

ABC

↓

ABCD
```

Many temporary strings are created.

______________________________________________________________________

# Efficient Version

```python
result = "".join(words)
```

Python calculates the required memory once and builds the final string efficiently.

______________________________________________________________________

# Favourite Questions

Why is

```python
"".join(...)
```

faster?

Because it allocates memory once instead of repeatedly creating intermediate strings.

______________________________________________________________________

# replace()

Replace text.

```python
text = "Hello World"

print(

    text.replace(

        "World",

        "Python"

    )

)
```

Output

```
Hello Python
```

______________________________________________________________________

# Replace Limited Occurrences

```python
text = "one one one"

print(

    text.replace(

        "one",

        "two",

        2

    )

)
```

Output

```
two two one
```

______________________________________________________________________

# find()

Locate a substring.

```python
text = "Backend Engineer"

print(

    text.find(

        "Engineer"

    )

)
```

Output

```
8
```

______________________________________________________________________

# Missing Substring

```python
print(

    text.find(

        "Java"

    )

)
```

Output

```
-1
```

No exception is raised.

______________________________________________________________________

# index()

Looks similar.

```python
print(

    text.index(

        "Engineer"

    )

)
```

Output

```
8
```

But if missing

```python
text.index("Java")
```

Output

```
ValueError
```

______________________________________________________________________

# find() vs index()

| Method | Not Found |
|----------|-----------|
| `find()` | Returns `-1` |
| `index()` | Raises `ValueError` |

### Rule

If "not found" is expected,

use

```python
find()
```

If missing data indicates a bug,

use

```python
index()
```

______________________________________________________________________

# count()

```python
text = "banana"

print(

    text.count("a")

)
```

Output

```
3
```

______________________________________________________________________

# startswith()

```python
filename = "report.pdf"

print(

    filename.startswith(

        "report"

    )

)
```

Output

```
True
```

______________________________________________________________________

# endswith()

```python
print(

    filename.endswith(

        ".pdf"

    )

)
```

Output

```
True
```

______________________________________________________________________

# Production Example

Validate uploaded files.

```python
if not filename.endswith(".csv"):

    raise ValueError("CSV expected")
```

> **Note:** In production, don't rely solely on the filename extension. Validate the file's content or MIME type as well.

______________________________________________________________________

# removeprefix()

Python 3.9+

```python
url = "https://example.com"

print(

    url.removeprefix(

        "https://"

    )

)
```

Output

```
example.com
```

______________________________________________________________________

# removesuffix()

```python
filename = "report.csv"

print(

    filename.removesuffix(

        ".csv"

    )

)
```

Output

```
report
```

Cleaner than manual slicing.

______________________________________________________________________

# partition()

Splits only once.

```python
email = "user@example.com"

print(

    email.partition("@")

)
```

Output

```
(

'user',

'@',

'example.com'

)
```

______________________________________________________________________

# Why Use partition()?

Unlike

```python
split("@")
```

the result always contains exactly three elements.

Very useful when parsing key-value strings.

______________________________________________________________________

# String Formatting

Python has three styles.

```
%

↓

format()

↓

f-string
```

______________________________________________________________________

# Old Style (%)

```python
name = "Alice"

print(

    "Hello %s" % name

)
```

Output

```
Hello Alice
```

Still found in older codebases.

______________________________________________________________________

# format()

```python
name = "Alice"

age = 30

print(

    "Name: {}, Age: {}".format(

        name,

        age

    )

)
```

Output

```
Name: Alice, Age: 30
```

______________________________________________________________________

# Named Arguments

```python
print(

    "Name: {name}, Age: {age}".format(

        name="Alice",

        age=30

    )

)
```

More readable.

______________________________________________________________________

# f-Strings

Recommended.

```python
name = "Alice"

age = 30

print(

    f"{name} is {age} years old"

)
```

Output

```
Alice is 30 years old
```

______________________________________________________________________

# Why f-Strings?

Advantages

- Cleaner
- Faster
- Easier to read
- Supports expressions

Example

```python
price = 50

tax = 5

print(

    f"Total = {price + tax}"

)
```

Output

```
Total = 55
```

______________________________________________________________________

# Formatting Numbers

```python
price = 1234.56789

print(f"{price:.2f}")
```

Output

```
1234.57
```

______________________________________________________________________

# Thousands Separator

```python
amount = 1000000

print(f"{amount:,}")
```

Output

```
1,000,000
```

______________________________________________________________________

# Alignment

```python
name = "Python"

print(f"|{name:<10}|")
print(f"|{name:^10}|")
print(f"|{name:>10}|")
```

Output

```
|Python    |
|  Python  |
|    Python|
```

Useful when generating reports.

______________________________________________________________________

# Encoding

Remember

```
String

↓

Unicode
```

Before sending data over a network,

Python converts it into bytes.

______________________________________________________________________

# encode()

```python
text = "Hello"

data = text.encode("utf-8")

print(data)
```

Output

```
b'Hello'
```

______________________________________________________________________

# decode()

```python
data = b"Hello"

print(

    data.decode(

        "utf-8"

    )

)
```

Output

```
Hello
```

______________________________________________________________________

# Visualising

```
String

↓

encode()

↓

Bytes

↓

Network

↓

decode()

↓

String
```

This process occurs constantly in web applications.

______________________________________________________________________

# Production Example

FastAPI Request

```
Client

↓

HTTP Bytes

↓

Decode

↓

Python String

↓

Process Request

↓

Encode

↓

Response Bytes

↓

Client
```

Understanding this flow helps explain why encoding errors occur.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using `+` inside large loops.

Prefer

```python
"".join(...)
```

______________________________________________________________________

## Mistake 2

Using `index()` when missing values are normal.

Use

```python
find()
```

instead.

______________________________________________________________________

## Mistake 3

Forgetting to decode bytes.

```python
b"Hello"

!=

"Hello"
```

______________________________________________________________________

## Mistake 4

Using old `%` formatting in new projects.

Prefer f-strings.

______________________________________________________________________

# Best Practices

✅ Use `.strip()` for user input.

✅ Use `.split()` to parse delimited text.

✅ Use `"separator".join()` for concatenation.

✅ Prefer `find()` when searching optional text.

✅ Prefer f-strings for formatting.

✅ Encode at system boundaries and decode immediately after reading bytes.

______________________________________________________________________

# Production Insight

Backend developers constantly use these methods:

| Method | Typical Use |
|----------|-------------|
| `strip()` | User input, config values |
| `split()` | CSV, headers, query strings |
| `join()` | SQL placeholders, logs, CSV generation |
| `replace()` | Sanitisation, templates |
| `startswith()` | URL routing |
| `endswith()` | File validation |
| `partition()` | Parsing key/value pairs |
| `encode()` | HTTP, sockets, files |
| `decode()` | Network responses |

These account for the majority of string manipulation in production applications.

______________________________________________________________________

# Questions

### Question

> Why is `"".join()` faster than repeated `+` concatenation?

### Answer

Because `join()` allocates memory once for the final string, whereas repeated `+` creates many temporary string objects.

______________________________________________________________________

### Question

> What is the difference between `find()` and `index()`?

### Answer

`find()` returns `-1` if the substring is absent, while `index()` raises a `ValueError`.

______________________________________________________________________

### Question

> Why are f-strings preferred?

### Answer

They are more readable, generally faster and support inline expressions.

______________________________________________________________________

### Question

> What is the difference between encoding and decoding?

### Answer

Encoding converts a Unicode string into bytes, while decoding converts bytes back into a Unicode string.

______________________________________________________________________

# Practical Lesson

Create a file:

```
string_methods.py
```

```python
# Cleaning user input
username = "  alice  "

print(username.strip())


# Splitting CSV
csv = "apple,banana,orange"

print(csv.split(","))


# Joining values
items = ["Python", "FastAPI", "Docker"]

print(" | ".join(items))


# Searching
text = "Backend Engineer"

print(text.find("Engineer"))
print(text.startswith("Back"))


# Formatting
name = "Alice"
score = 96.5

print(f"{name} scored {score:.1f}%")


# Encoding
message = "Hello"

encoded = message.encode("utf-8")
decoded = encoded.decode("utf-8")

print(encoded)
print(decoded)
```

Expected Output

```
alice

['apple', 'banana', 'orange']

Python | FastAPI | Docker

8

True

Alice scored 96.5%

b'Hello'

Hello
```

______________________________________________________________________

# Questions

## Question 1

Why is `join()` generally preferred over repeated string concatenation?

### Answer

It performs a single memory allocation, making it more efficient for combining many strings.

______________________________________________________________________

## Question 2

When should you use `partition()` instead of `split()`?

### Answer

When you need exactly one split and a guaranteed three-element result.

______________________________________________________________________

## Question 3

What is the difference between `split()` and `splitlines()`?

### Answer

`split()` separates text using a specified delimiter, while `splitlines()` separates text based on line boundaries.

______________________________________________________________________

## Question 4

Why are `encode()` and `decode()` important in backend development?

### Answer

Network communication, files and many external systems operate on bytes, while Python application logic typically uses
Unicode strings.

______________________________________________________________________

## Question 5

Which string formatting method should modern Python projects prefer?

### Answer

f-strings, because they are concise, readable and generally offer the best performance.

______________________________________________________________________

# Assignment

## Exercise 1

Given:

```python
text = "   Python,FastAPI,Docker,Kubernetes   "
```

Produce:

```python
["Python", "FastAPI", "Docker", "Kubernetes"]
```

using appropriate string methods.

______________________________________________________________________

## Exercise 2

Write a program that extracts the username and domain from:

```python
"riyaz@example.com"
```

using `partition()`.

______________________________________________________________________

## Exercise 3

Create a formatted invoice using f-strings that displays:

- Product name
- Quantity
- Unit price
- Total
- Two decimal places
- Right-aligned columns

______________________________________________________________________

## Exercise 4

Read a UTF-8 encoded text file, decode its contents, replace every occurrence of `"ERROR"` with `"WARNING"`, and write
the modified content back using UTF-8 encoding.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Essential string manipulation methods.
- ✅ Searching and replacing text.
- ✅ Efficient string concatenation using `join()`.
- ✅ The differences between `find()` and `index()`.
- ✅ Modern string formatting with f-strings.
- ✅ Unicode encoding and decoding.
- ✅ Common production patterns for backend applications.

______________________________________________________________________

# What's Next

**File:** [31-String-Deep-Dive-part-3](31-string-deep-dive-part-3.md)

Topics:

- String performance
- `+` vs `join()` benchmarks
- `io.StringIO`
- Common string algorithms
- Regular expressions (`re`)
- Security considerations (SQL injection, escaping)
- JSON and logging
- Production patterns
- Advanced interview questions
- Final string assignments

```
```

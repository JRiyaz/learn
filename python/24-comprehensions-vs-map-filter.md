# File: python/24-comprehensions-vs-map-filter.md

# Python Functional Programming - Part 2

# Comprehensions vs `map()` and `filter()`

> **Course:** Backend Engineering Roadmap
>
> **Module:** Functional Python
>
> **Lesson:** 2
>
> **Difficulty:** ⭐⭐⭐☆☆
>
> **Estimated Time:** 130 Minutes

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| List Comprehensions | Python 2.0 |
| Dictionary Comprehensions | Python 2.7 |
| Set Comprehensions | Python 2.7 |
| Generator Expressions | Python 2.4 |
| `map()` | Python 1.0 |
| `filter()` | Python 1.0 |

### Important Python 3 Changes

- List comprehensions in Python 3 have their own local scope. In Python 2, the loop variable leaked into the surrounding scope.
- `map()` and `filter()` return lazy iterators instead of lists.
- Dictionary and set comprehensions are now widely preferred over manual loops for building collections.

These improvements make Python 3 comprehensions both safer and more memory efficient.

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What comprehensions are
- List comprehensions
- Dictionary comprehensions
- Set comprehensions
- Generator expressions
- Nested comprehensions
- Comprehensions vs `map()`
- Comprehensions vs `filter()`
- Performance considerations
- Production best practices

______________________________________________________________________

# Recap

Previously we learned

```python
map()
```

```python
filter()
```

```python
reduce()
```

Although these functions are still important,

modern Python code uses **comprehensions** much more frequently.

If you examine production code on GitHub,

list comprehensions appear far more often than `map()`.

Understanding why is important.

______________________________________________________________________

# What is a Comprehension?

A comprehension is a concise way of creating a new collection.

Instead of writing

```python
result = []

for number in numbers:

    result.append(number)
```

Python lets us write

```python
result = [

    number

    for number in numbers

]
```

The result is identical.

______________________________________________________________________

# Why Were Comprehensions Introduced?

Before Python 2.0,

creating lists required explicit loops.

Example

```python
squares = []

for number in range(5):

    squares.append(number ** 2)
```

Comprehensions made this pattern shorter,

more readable,

and often slightly faster.

______________________________________________________________________

# List Comprehension Syntax

General syntax

```python
[
    expression

    for item in iterable
]
```

Think of it as

```
Take every item

↓

Apply expression

↓

Build list
```

______________________________________________________________________

# Example

```python
numbers = [1, 2, 3, 4]

squares = [

    number ** 2

    for number in numbers

]

print(squares)
```

Output

```
[1, 4, 9, 16]
```

______________________________________________________________________

# Equivalent Loop

```python
squares = []

for number in numbers:

    squares.append(

        number ** 2

    )
```

Both produce the same result.

______________________________________________________________________

# Filtering in a Comprehension

Comprehensions can filter data.

```python
numbers = [

    1,

    2,

    3,

    4,

    5,

    6

]

evens = [

    number

    for number in numbers

    if number % 2 == 0

]

print(evens)
```

Output

```
[2, 4, 6]
```

______________________________________________________________________

# Visualising a List Comprehension

```
Numbers

↓

Filter (optional)

↓

Transform

↓

New List
```

______________________________________________________________________

# Transform and Filter Together

```python
numbers = [

    1,

    2,

    3,

    4

]

result = [

    number * 10

    for number in numbers

    if number % 2 == 0

]

print(result)
```

Output

```
[20, 40]
```

______________________________________________________________________

# Conditional Expressions

You can use an inline `if...else`.

```python
numbers = [

    1,

    2,

    3,

    4

]

labels = [

    "Even"

    if number % 2 == 0

    else "Odd"

    for number in numbers

]

print(labels)
```

Output

```
['Odd', 'Even', 'Odd', 'Even']
```

Notice

This is different from the filtering syntax.

Filtering

```python
[
    x

    for x in numbers

    if condition
]
```

Conditional expression

```python
[
    value1

    if condition

    else value2

    for x in numbers
]
```

This distinction is a common interview question.

______________________________________________________________________

# Nested Comprehensions

Example

```python
matrix = [

    [1, 2],

    [3, 4],

    [5, 6]

]

flattened = [

    value

    for row in matrix

    for value in row

]

print(flattened)
```

Output

```
[1, 2, 3, 4, 5, 6]
```

Execution order

```
Row

↓

Each Value

↓

Append
```

______________________________________________________________________

# When Nested Comprehensions Become Hard to Read

This is acceptable

```python
[
    value

    for row in matrix

    for value in row
]
```

This is often difficult to read

```python
[
    ...

    for ...

    if ...

    for ...

    if ...

]
```

When comprehensions become complex,

prefer normal loops.

Readability always wins.

______________________________________________________________________

# Dictionary Comprehensions

Python 2.7 introduced dictionary comprehensions.

Syntax

```python
{
    key: value

    for item in iterable
}
```

Example

```python
numbers = [

    1,

    2,

    3

]

squares = {

    number: number ** 2

    for number in numbers

}

print(squares)
```

Output

```
{
    1: 1,

    2: 4,

    3: 9
}
```

______________________________________________________________________

# Filtering Dictionaries

```python
prices = {

    "Keyboard": 40,

    "Mouse": 15,

    "Monitor": 200

}

expensive = {

    item: price

    for item, price in prices.items()

    if price >= 50

}

print(expensive)
```

Output

```
{
    'Monitor': 200
}
```

______________________________________________________________________

# Set Comprehensions

Python 2.7 also introduced set comprehensions.

Syntax

```python
{
    expression

    for item in iterable
}
```

Example

```python
numbers = [

    1,

    2,

    2,

    3,

    3,

    4

]

unique = {

    number

    for number in numbers

}

print(unique)
```

Output

```
{
    1,

    2,

    3,

    4
}
```

Duplicate values are automatically removed.

______________________________________________________________________

# Generator Expressions

Generator expressions look similar to list comprehensions.

Instead of

```python
[
    ...
]
```

they use

```python
(
    ...
)
```

Example

```python
numbers = (

    number ** 2

    for number in range(5)

)

print(numbers)
```

Output

```
<generator object ...>
```

Just like `map()`,

generators are lazy.

______________________________________________________________________

# Why Use Generator Expressions?

Suppose

```
100 million rows
```

List comprehension

```
Entire list

↓

Memory
```

Generator expression

```
One value

↓

Processed

↓

Next value
```

This dramatically reduces memory usage.

______________________________________________________________________

# Example

```python
numbers = (

    number ** 2

    for number in range(5)

)

for value in numbers:

    print(value)
```

Output

```
0

1

4

9

16
```

Values are produced one at a time.

______________________________________________________________________

# Comprehensions vs map()

Suppose we double numbers.

Using `map()`

```python
result = list(

    map(

        lambda x: x * 2,

        numbers

    )

)
```

Using a comprehension

```python
result = [

    x * 2

    for x in numbers

]
```

The comprehension is generally easier to read.

______________________________________________________________________

# Comprehensions vs filter()

Using `filter()`

```python
result = list(

    filter(

        lambda x: x > 10,

        numbers

    )

)
```

Comprehension

```python
result = [

    x

    for x in numbers

    if x > 10

]
```

Again,

the comprehension is often preferred.

______________________________________________________________________

# When map() Is Better

Suppose a named function already exists.

```python
def normalise(name):

    return name.strip().title()
```

Then

```python
result = map(

    normalise,

    names

)
```

is concise and avoids introducing a lambda.

______________________________________________________________________

# When Comprehensions Are Better

Most simple transformations.

Example

```python
[
    x * 2

    for x in numbers
]
```

is usually more readable than

```python
map(

    lambda x: x * 2,

    numbers

)
```

______________________________________________________________________

# Generator Expression vs List Comprehension

List

```python
[
    x ** 2

    for x in range(1_000_000)
]
```

Memory

```
One million values
```

Generator

```python
(

    x ** 2

    for x in range(1_000_000)

)
```

Memory

```
One value at a time
```

Choose based on whether you need random access or sequential processing.

______________________________________________________________________

# Performance Considerations

Generally

- List comprehensions are faster than equivalent `for` loops for building lists.
- Generator expressions use much less memory.
- `map()` may be slightly faster when used with built-in functions (e.g. `str`, `int`, `abs`) because the looping occurs in optimised C code.
- For lambda-based transformations, list comprehensions are often both faster and easier to read.

Always benchmark critical code instead of assuming.

______________________________________________________________________

# Production Example - API Response

Suppose an API returns

```python
users = [

    {

        "id": 1,

        "name": "Alice"

    },

    {

        "id": 2,

        "name": "Bob"

    }

]
```

Extract names.

```python
names = [

    user["name"]

    for user in users

]
```

______________________________________________________________________

# Production Example - File Processing

Large log file

```python
lines = (

    line.strip()

    for line in open(

        "server.log"

    )

)
```

Each line is processed lazily.

Memory usage stays low.

> **Note:** We'll later learn that opening files should normally use a context manager (`with open(...)`) to ensure the file is closed correctly. This example focuses on generator expressions.

______________________________________________________________________

# Production Example - FastAPI

Suppose you fetch products.

```python
products = repository.get_products()
```

Return only available products.

```python
available = [

    product

    for product in products

    if product.in_stock
]
```

This pattern is common in service layers.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Creating complicated comprehensions.

If it spans several conditions and loops,

consider using a normal loop.

______________________________________________________________________

## Mistake 2

Using a list comprehension only for side effects.

Bad

```python
[
    print(number)

    for number in numbers
]
```

Comprehensions should build collections,

not perform actions.

______________________________________________________________________

## Mistake 3

Converting generators into lists immediately.

```python
list(

    x

    for x in data

)
```

This often defeats the memory benefits of a generator.

______________________________________________________________________

# Best Practices

✅ Prefer list comprehensions for simple transformations.

✅ Use dictionary comprehensions for dictionary construction.

✅ Use set comprehensions when uniqueness is required.

✅ Use generator expressions for large datasets.

✅ Prioritise readability over brevity.

❌ Don't create deeply nested comprehensions.

❌ Don't use comprehensions solely for side effects.

______________________________________________________________________

# Production Insight

Modern Python codebases heavily favour comprehensions because they are:

- Readable
- Concise
- Efficient
- Idiomatic

You'll frequently encounter:

```python
[user.id for user in users]
```

```python
{
    user.id: user

    for user in users
}
```

```python
(
    row

    for row in csv_reader
)
```

Frameworks such as Django, FastAPI, SQLAlchemy and Pandas often use comprehensions to transform query results, API
responses and collections.

______________________________________________________________________

# Questions

### Question

> What is the difference between a list comprehension and a generator expression?

### Answer

A list comprehension creates the entire list immediately, while a generator expression produces values lazily, one at a
time, making it more memory efficient.

______________________________________________________________________

### Question

> Why are comprehensions generally preferred over `map()` and `filter()`?

### Answer

For simple transformations and filtering, comprehensions are usually more readable and are considered more idiomatic in
modern Python.

______________________________________________________________________

### Question

> When would you use `map()` instead of a comprehension?

### Answer

When applying an existing named function to every element or when working with multiple iterables, `map()` can be
concise and efficient.

______________________________________________________________________

### Question

> Why shouldn't comprehensions be used for side effects?

### Answer

Their purpose is to create collections. Using them only to execute actions wastes memory and makes the code less clear
than a standard loop.

______________________________________________________________________

# Practical Lesson

Create a file:

```
comprehensions_examples.py
```

```python
# List comprehension
numbers = [1, 2, 3, 4, 5]

squares = [

    number ** 2

    for number in numbers

]

print(squares)


# Dictionary comprehension
prices = {

    "Keyboard": 40,

    "Mouse": 15,

    "Monitor": 200

}

discounted = {

    item: price * 0.9

    for item, price in prices.items()

}

print(discounted)


# Set comprehension
duplicates = [

    1,

    2,

    2,

    3,

    4,

    4

]

unique = {

    value

    for value in duplicates

}

print(unique)


# Generator expression
generator = (

    number ** 2

    for number in range(5)

)

for value in generator:

    print(value)
```

Expected Output

```
[1, 4, 9, 16, 25]

{'Keyboard': 36.0, 'Mouse': 13.5, 'Monitor': 180.0}

{1, 2, 3, 4}

0
1
4
9
16
```

______________________________________________________________________

# Questions

## Question 1

What is a list comprehension?

### Answer

A concise syntax for creating a new list by iterating over an iterable and optionally filtering or transforming its
elements.

______________________________________________________________________

## Question 2

When should you use a generator expression?

### Answer

When processing large datasets sequentially without needing all values in memory at once.

______________________________________________________________________

## Question 3

What is the difference between filtering and a conditional expression inside a comprehension?

### Answer

A filtering `if` determines whether an element is included, while an inline `if...else` chooses which value is produced
for every element.

______________________________________________________________________

## Question 4

Why are dictionary comprehensions useful?

### Answer

They provide a concise and efficient way to construct dictionaries from existing iterables while optionally transforming
keys and values.

______________________________________________________________________

## Question 5

Why are list comprehensions generally preferred over `map()` with `lambda`?

### Answer

They are usually easier to read, more idiomatic and often perform similarly or better for simple transformations.

______________________________________________________________________

# Assignment

## Exercise 1

Given

```python
numbers = [1, 2, 3, 4, 5, 6]
```

Create:

- A list of cubes.
- A list containing only odd numbers.
- A list that labels each number as `"Even"` or `"Odd"`.

______________________________________________________________________

## Exercise 2

Given

```python
employees = {
    "Alice": 65000,
    "Bob": 48000,
    "Charlie": 72000
}
```

Create a dictionary containing only employees earning at least `50000`.

______________________________________________________________________

## Exercise 3

Read a text file and create a generator expression that yields only non-empty, stripped lines.

______________________________________________________________________

## Exercise 4

Rewrite the following using:

- A `for` loop
- `map()`
- A list comprehension

```python
numbers = [10, 20, 30]

# Multiply every number by 5
```

Compare readability and explain which version you would use in production.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What comprehensions are and why they exist.
- ✅ How to use list, dictionary and set comprehensions.
- ✅ How generator expressions enable lazy evaluation.
- ✅ The differences between comprehensions and `map()`/`filter()`.
- ✅ Performance and memory trade-offs.
- ✅ Production best practices for writing idiomatic Python.

______________________________________________________________________

# What's Next

**File:** [25-Zip-Enumerate-Any-All](25-zip-enumerate-any-all.md)

Topics:

- `zip()`
- `enumerate()`
- `any()`
- `all()`
- Unpacking with `zip()`
- Practical Iteration Patterns
- Lazy Evaluation
- Production Examples
- Performance Considerations

> **Why next?**
>
> These four built-in functions are among the most frequently used tools in professional Python code. They appear constantly in backend services, ETL pipelines, API development and interview questions because they make iteration cleaner, safer and more expressive.

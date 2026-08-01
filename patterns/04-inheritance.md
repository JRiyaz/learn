# Software Design & Design Patterns - Part 04

# Inheritance

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Inheritance is
- Why Inheritance exists
- The problems it solves
- Real-world backend examples
- Types of inheritance in Python
- Advantages and disadvantages
- When to use Inheritance
- When NOT to use Inheritance

______________________________________________________________________

# The Problem

Let's continue building our **Library Management System**.

Initially, we have a `Book`.

```python id="inh0401"
class Book:

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def display(self):
        print(self.title)
```

Everything works.

______________________________________________________________________

# New Requirement

The business now wants to support:

- Printed Books
- E-Books
- Audio Books

A junior developer copies the code.

```python id="inh0402"
class PrintedBook:

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def display(self):
        print(self.title)
```

```python id="inh0403"
class EBook:

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def display(self):
        print(self.title)
```

```python id="inh0404"
class AudioBook:

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def display(self):
        print(self.title)
```

______________________________________________________________________

# What's the Problem?

Every class

contains the same code.

If tomorrow

you add

```python id="inh0405"
self.isbn
```

you must modify

every class.

This violates

the

**Don't Repeat Yourself (DRY)**

principle.

______________________________________________________________________

# The Idea

Ask yourself:

What is common?

All three types

have:

- Title
- Author
- Display method

Only some behavior

is different.

Instead of copying code,

let's reuse it.

______________________________________________________________________

# This Is Inheritance

Inheritance allows

one class

to inherit

properties and behavior

from another class.

Think of it as

a parent-child relationship.

```text id="inh0406"
Book

↓

PrintedBook

↓

EBook

↓

AudioBook
```

Each child

gets everything

from the parent,

and can also

add its own behavior.

______________________________________________________________________

# Refactored Code

```python id="inh0407"
class Book:

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def display(self):
        print(self.title)
```

Now inherit.

```python id="inh0408"
class PrintedBook(Book):
    pass
```

```python id="inh0409"
class EBook(Book):
    pass
```

```python id="inh0410"
class AudioBook(Book):
    pass
```

Suddenly,

all three classes

already have:

- title
- author
- display()

without writing them again.

______________________________________________________________________

# Adding New Behavior

Each child

can add

its own functionality.

```python id="inh0411"
class EBook(Book):

    def download(self):
        print("Downloading...")
```

```python id="inh0412"
class AudioBook(Book):

    def play(self):
        print("Playing audiobook...")
```

Now

every child

shares common behavior

while adding

its own features.

______________________________________________________________________

# Method Overriding

A child class

can replace

a parent's implementation.

Example

```python id="inh0413"
class Book:

    def get_type(self):
        return "Book"
```

Override it.

```python id="inh0414"
class EBook(Book):

    def get_type(self):
        return "E-Book"
```

Now

```python id="inh0415"
ebook.get_type()
```

returns

```text id="inh0416"
E-Book
```

instead of

```text id="inh0417"
Book
```

______________________________________________________________________

# The `super()` Function

Sometimes

you want

to reuse

the parent's logic.

Example

```python id="inh0418"
class Book:

    def __init__(
        self,
        title,
        author,
    ):
        self.title = title
        self.author = author
```

Child

```python id="inh0419"
class EBook(Book):

    def __init__(
        self,
        title,
        author,
        file_size,
    ):
        super().__init__(
            title,
            author,
        )

        self.file_size = file_size
```

`super()`

calls

the parent class

instead of duplicating code.

______________________________________________________________________

# Types of Inheritance

Python supports:

## Single Inheritance

```text id="inh0420"
Book

↓

EBook
```

______________________________________________________________________

## Multilevel Inheritance

```text id="inh0421"
Book

↓

DigitalBook

↓

EBook
```

______________________________________________________________________

## Multiple Inheritance

```text id="inh0422"
Downloadable

↘

EBook

↗

Searchable
```

Python supports it,

but use it carefully.

We'll discuss why later.

______________________________________________________________________

# Real Backend Example

Suppose you're building

payment providers.

```python id="inh0423"
class PaymentProvider:

    def validate(self):
        ...

    def pay(self):
        ...
```

Then

```python id="inh0424"
class StripeProvider(
    PaymentProvider
):
    ...
```

```python id="inh0425"
class RazorpayProvider(
    PaymentProvider
):
    ...
```

All providers

share common behavior,

while implementing

their own payment logic.

______________________________________________________________________

# FastAPI Example

FastAPI developers

often create

a base schema.

```python id="inh0426"
class BaseUser(BaseModel):

    name: str
```

Then

```python id="inh0427"
class UserCreate(
    BaseUser
):
    password: str
```

```python id="inh0428"
class UserResponse(
    BaseUser
):
    id: int
```

The common fields

are reused

through inheritance.

______________________________________________________________________

# Advantages

Inheritance helps you:

✅ Reuse code

✅ Reduce duplication

✅ Create logical hierarchies

✅ Simplify maintenance

______________________________________________________________________

# The Dark Side

Many beginners

start using inheritance

for everything.

Eventually,

they create

deep inheritance trees.

```text id="inh0429"
Object

↓

LibraryItem

↓

Book

↓

DigitalBook

↓

PremiumBook

↓

SpecialEditionBook
```

Now,

changing one class

can affect

many others.

This becomes difficult

to maintain.

______________________________________________________________________

# A Better Alternative?

Modern software

often prefers

**Composition**

over Inheritance.

We'll study that

in the next lesson.

______________________________________________________________________

# When Should You Use Inheritance?

Use inheritance

when there is

a genuine

**IS-A**

relationship.

Examples:

- EBook **is a** Book
- AudioBook **is a** Book
- UserCreate **is a** BaseUser
- CustomException **is an** Exception

These are

natural hierarchies.

______________________________________________________________________

# When NOT to Use Inheritance

Don't use inheritance

simply to reuse code.

Suppose

an Order Service

needs:

- Logger
- Database
- Email Service

This is **not**

an inheritance relationship.

The service

**has a**

logger.

It **has a**

database.

It does **not**

**is a**

logger.

Composition

is the correct choice.

______________________________________________________________________

# Best Practices

✅ Use inheritance for true "IS-A" relationships.

✅ Keep inheritance hierarchies shallow.

✅ Reuse common behavior.

✅ Override only when necessary.

✅ Use `super()` to avoid duplication.

______________________________________________________________________

# Common Mistakes

### Using Inheritance Only for Code Reuse

Just because two classes

share some code

doesn't mean

they should inherit.

______________________________________________________________________

### Deep Class Hierarchies

Deep inheritance trees

become difficult

to understand

and maintain.

______________________________________________________________________

### Forgetting `super()`

Developers sometimes

rewrite parent logic

instead of reusing it.

______________________________________________________________________

### Multiple Inheritance Everywhere

Python supports it,

but excessive multiple inheritance

can make code confusing.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Inheritance, and when should you use it?

Inheritance is an object-oriented programming technique where a child class inherits data and behavior from a parent
class. It promotes code reuse and helps model natural "IS-A" relationships. Developers should use inheritance when
objects share a genuine hierarchical relationship, such as `EBook` extending `Book` or custom exceptions extending
Python's `Exception`. It should not be used merely to reuse code, as composition is often a better choice for loosely
coupled backend systems.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Inheritance is
- Why it exists
- Method overriding
- `super()`
- Types of inheritance
- FastAPI examples
- Advantages
- Disadvantages
- When to use it
- When not to use it

______________________________________________________________________

# What's Next

[Polymorphism](05-polymorphism.md)

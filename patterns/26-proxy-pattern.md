# Software Design & Design Patterns - Part 26

# Proxy Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Proxy Pattern is
- Why the Proxy Pattern exists
- The problems it solves
- Virtual, Protection, and Remote Proxies
- Real-world backend examples
- FastAPI examples
- SQLAlchemy Lazy Loading
- When NOT to use the Proxy Pattern

______________________________________________________________________

# Before We Start

Imagine

your application

stores

10 million books.

A user requests

one book.

Should your application

immediately load:

- Book
- Author
- Reviews
- Borrow History
- Recommendations
- Audit Logs

Probably not.

Loading everything

would be expensive.

Instead,

load

only

what's needed.

This is one place

where

the Proxy Pattern

appears.

______________________________________________________________________

# The Problem

Let's continue

our

**Library Management System**.

We have

a book.

```python id="proxy2601"
class Book:

    def load(self):

        print(
            "Loading book..."
        )
```

Loading

a book

takes

5 seconds.

A developer writes

```python id="proxy2602"
book = Book()
```

The object

loads immediately.

Even if

the user

never reads it.

______________________________________________________________________

# Another Problem

Suppose

every request

loads

a Machine Learning model.

```python id="proxy2603"
model = AIModel()
```

Loading

takes

15 seconds.

Many requests

never use

the model.

Why load it

every time?

______________________________________________________________________

# Another Problem

Suppose

only

administrators

should access

audit logs.

But

every user

can directly create

```python id="proxy2604"
AuditService()
```

Security

becomes difficult.

______________________________________________________________________

# The Idea

Instead of

using

the real object,

place

another object

in front of it.

That object

controls

access

to the real object.

______________________________________________________________________

# What is the Proxy Pattern?

The **Proxy Pattern** says:

> **Provide a placeholder or representative for another object to control access to it.**

The proxy

looks

like

the real object,

but performs

extra work

before delegating

to it.

______________________________________________________________________

# Without Proxy

```text id="proxy2605"
Client

↓

Book
```

______________________________________________________________________

# With Proxy

```text id="proxy2606"
Client

↓

BookProxy

↓

Book
```

The client

doesn't know

whether

it's talking

to the proxy

or

the real object.

______________________________________________________________________

# Step 1

Create

the real object.

```python id="proxy2607"
class Book:

    def load(self):

        print(
            "Book Loaded"
        )
```

______________________________________________________________________

# Step 2

Create

the proxy.

```python id="proxy2608"
class BookProxy:

    def __init__(self):

        self.book = None
```

______________________________________________________________________

# Step 3

Load lazily.

```python id="proxy2609"
class BookProxy:

    def load(self):

        if self.book is None:

            self.book = Book()

        self.book.load()
```

Notice

what happened.

The real object

is created

only

when needed.

______________________________________________________________________

# Using the Proxy

```python id="proxy2610"
book = BookProxy()

print(
    "Application Started"
)
```

No book

is loaded.

Later,

```python id="proxy2611"
book.load()
```

Now,

the real object

is created.

This is called

**Lazy Loading**.

______________________________________________________________________

# Types of Proxies

The Proxy Pattern

has several variants.

______________________________________________________________________

# 1. Virtual Proxy

Creates

expensive objects

only

when needed.

Examples:

- Large images
- ML models
- Database records
- Videos

______________________________________________________________________

# 2. Protection Proxy

Controls

access

to an object.

Example

```python id="proxy2612"
if not current_user.is_admin:

    raise PermissionError
```

Only

authorized users

can reach

the real object.

______________________________________________________________________

# 3. Remote Proxy

Represents

an object

living

on another machine.

Example

Your application

calls

a payment service

through

an HTTP client.

The client

acts

as a proxy

for

the remote service.

______________________________________________________________________

# Real Backend Example

Suppose

our application

downloads

PDF reports.

Instead of

downloading

immediately,

create

a proxy.

The report

downloads

only

when

the user

actually opens it.

______________________________________________________________________

# SQLAlchemy Example

One of the most famous

Proxy Pattern

implementations.

Suppose

you query

a book.

```python id="proxy2613"
book = session.get(
    Book,
    1,
)
```

Later,

you access

```python id="proxy2614"
book.author
```

Only now

does SQLAlchemy

query

the Author table.

This is called

**Lazy Loading**.

Internally,

SQLAlchemy

uses

proxy-like objects

to delay

database queries.

______________________________________________________________________

# FastAPI Example

Suppose

your endpoint

needs

an expensive

AI model.

Instead of

loading

the model

during startup,

create

a proxy

that loads

the model

the first time

it's used.

Subsequent requests

reuse

the loaded model.

______________________________________________________________________

# AI/ML Example

Loading

a Large Language Model

may require:

- GPU memory
- Tokenizer
- Model weights

Instead of

doing this

at startup,

a proxy

can delay

loading

until

the first inference request.

______________________________________________________________________

# Caching Proxy

Another common

real-world proxy.

```text id="proxy2615"
Client

↓

Cache Proxy

↓

Database
```

If data

exists

in cache,

the database

is never called.

Redis-based caching

often follows

this idea.

______________________________________________________________________

# Proxy vs Decorator

A classic

interview question.

| Proxy | Decorator |
| --------------------------- | ------------------------- |
| Controls access | Adds behavior |
| Usually same responsibility | Adds new responsibilities |
| May delay object creation | Enhances existing object |

Example

Authentication

↓

Proxy

Logging

↓

Decorator

______________________________________________________________________

# Proxy vs Adapter

| Proxy | Adapter |
| --------------- | ------------------- |
| Controls access | Converts interfaces |
| Same interface | Different interface |

______________________________________________________________________

# Benefits

Proxy gives you:

✅ Lazy loading

✅ Access control

✅ Caching

✅ Remote communication

✅ Better performance

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Extra layer

❌ Slight complexity

❌ Harder debugging

______________________________________________________________________

# Real Company Example

Suppose

Netflix

shows

movie posters.

When browsing,

it doesn't

download

full-size images.

Instead,

it loads

small thumbnails.

Only

when you open

the movie,

the large image

is fetched.

A proxy

helps delay

expensive operations.

______________________________________________________________________

# When NOT to Use Proxy

Don't create

a proxy

for

every object.

If

object creation

is cheap

and

no access control

is required,

a proxy

adds

unnecessary complexity.

______________________________________________________________________

# Best Practices

✅ Use proxies for expensive resources.

✅ Hide lazy loading from callers.

✅ Keep the proxy interface identical to the real object.

✅ Use proxies for caching and security when appropriate.

______________________________________________________________________

# Common Mistakes

### Putting Business Logic in the Proxy

The proxy

controls access.

Business rules

belong

elsewhere.

______________________________________________________________________

### Different Interfaces

The proxy

should behave

exactly

like

the real object.

______________________________________________________________________

### Ignoring Performance

A poorly designed proxy

can actually

reduce performance.

Measure first.

______________________________________________________________________

### Confusing Proxy with Decorator

Decorator

adds behavior.

Proxy

controls access.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Proxy Pattern, and where is it commonly used?

The Proxy Pattern is a structural design pattern that provides a placeholder or representative for another object,
allowing it to control access before delegating requests to the real object. It is commonly used for lazy loading,
access control, caching, and remote communication. Real-world examples include SQLAlchemy's lazy-loaded relationships,
Redis caching layers, authentication proxies, API gateways, and HTTP clients communicating with remote services.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Proxy Pattern is
- Why it exists
- Virtual, Protection, and Remote Proxies
- SQLAlchemy lazy loading
- FastAPI example
- AI/ML example
- Proxy vs Decorator
- Proxy vs Adapter
- Best practices

______________________________________________________________________

# What's Next

[State Pattern](27-state-pattern.md)

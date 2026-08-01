# Software Design & Design Patterns - Part 15

# Singleton Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Singleton Pattern is
- Why the Singleton Pattern exists
- The problems it solves
- Real-world backend examples
- Python implementations
- Thread safety considerations
- When to use the Singleton Pattern
- When NOT to use the Singleton Pattern

______________________________________________________________________

# The Problem

Let's continue with our **Library Management System**.

Every service

needs logging.

A developer writes

```python
class Logger:

    def log(
        self,
        message,
    ):
        print(message)
```

Then,

inside every service,

they create

a new logger.

```python
class BookService:

    def __init__(self):
        self.logger = Logger()
```

```python
class MemberService:

    def __init__(self):
        self.logger = Logger()
```

```python
class PaymentService:

    def __init__(self):
        self.logger = Logger()
```

```python
class NotificationService:

    def __init__(self):
        self.logger = Logger()
```

______________________________________________________________________

# What's the Problem?

Imagine

your application

contains

100 services.

You now have

100 logger objects.

Do we really need

100 loggers?

No.

One logger

is enough

for the entire application.

______________________________________________________________________

# Another Example

Suppose

your application

loads configuration.

```python
config = load_config()
```

Now,

every service

loads it again.

```python
config = load_config()
```

Again.

```python
config = load_config()
```

Again.

Configuration

is read

dozens of times.

______________________________________________________________________

# Real Problems

Creating multiple instances

may cause:

❌ Wasted memory

❌ Slower startup

❌ Duplicate initialization

❌ Multiple database pools

❌ Multiple cache connections

Some objects

should exist

only once.

______________________________________________________________________

# This Is Where Singleton Helps

The **Singleton Pattern** says:

> **Ensure a class has only one instance and provide a global access point to it.**

Instead of

creating

multiple objects,

reuse

the same object.

______________________________________________________________________

# Without Singleton

```text
BookService

↓

Logger #1
```

```text
MemberService

↓

Logger #2
```

```text
PaymentService

↓

Logger #3
```

Many objects.

______________________________________________________________________

# With Singleton

```text
BookService

↘

MemberService

↘

PaymentService

↓

One Logger
```

Every service

uses

the same object.

______________________________________________________________________

# Simple Python Implementation

```python
class Logger:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(
                cls
            )

        return cls._instance
```

Now,

```python
logger1 = Logger()

logger2 = Logger()
```

______________________________________________________________________

# Verify

```python
print(
    logger1 is logger2
)
```

Output

```text
True
```

Both variables

reference

the same object.

______________________________________________________________________

# Configuration Example

Instead of

loading configuration

every time,

create

one configuration object.

```python
class Config:

    _instance = None
```

Load

the configuration

once.

Reuse it

everywhere.

______________________________________________________________________

# Real Backend Example

Suppose

our application

loads

```text
config.yaml
```

Loading

the file

every request

would be inefficient.

Instead,

load it

once

during startup

and reuse

the same object.

______________________________________________________________________

# Another Backend Example

Suppose

your application

creates

an expensive

Machine Learning model.

```python
model = load_model()
```

Loading

the model

takes

10 seconds.

Should

every request

load

another model?

Absolutely not.

One shared instance

is enough.

______________________________________________________________________

# FastAPI Example

FastAPI applications

often create

shared objects

during startup.

Example:

- Configuration
- HTTP clients
- AI models
- Cache clients

Instead of creating them

inside every request,

they're created once

and reused.

Although FastAPI

doesn't require

the Singleton Pattern,

the idea

is very similar.

______________________________________________________________________

# Logging Example

Python already provides

a logging module.

```python
import logging

logger = logging.getLogger(
    __name__
)
```

Even if

multiple modules

request

the same logger,

Python returns

the same logger instance

for that name.

This is

a practical example

of Singleton-like behavior.

______________________________________________________________________

# Database Connections

Should

database connections

be singletons?

Many beginners

think so.

Actually,

**No.**

Applications usually use

a

**Connection Pool**

instead.

Each request

borrows

a connection

and returns it

to the pool.

One connection

for every request

would become

a bottleneck.

______________________________________________________________________

# Thread Safety

Suppose

two threads

execute

```python
Logger()
```

at exactly

the same time.

Without protection,

both threads

might create

different objects.

A production-ready

Singleton

must be

thread-safe.

We'll usually rely

on framework support

instead of

implementing this ourselves.

______________________________________________________________________

# Advantages

Using Singleton

gives you:

✅ One shared instance

✅ Lower memory usage

✅ Faster initialization

✅ Shared application state

______________________________________________________________________

# Disadvantages

Singletons also have drawbacks.

❌ Hidden global state

❌ Harder unit testing

❌ Tighter coupling

❌ Difficult lifecycle management

This is why

many developers

avoid using them

unless necessary.

______________________________________________________________________

# Modern Alternative

Instead of

writing

your own Singleton,

modern frameworks

prefer

Dependency Injection.

Create

the object

once,

then inject it

where needed.

FastAPI

does exactly this

for many shared resources.

______________________________________________________________________

# When Should You Use Singleton?

Good candidates:

- Configuration
- Logger
- Metrics collector
- Feature flag manager
- ML model
- Shared HTTP client

These objects

benefit

from having

a single instance.

______________________________________________________________________

# When NOT to Use Singleton

Don't use Singleton

for:

- Database Sessions
- Request objects
- User objects
- Shopping carts
- Orders

These objects

represent

individual requests

or users.

Each should have

its own instance.

______________________________________________________________________

# Singleton vs Global Variable

A common misconception.

Global variable

```python
logger = Logger()
```

Singleton

```python
Logger()
```

Both provide

shared access,

but Singleton

controls

how many instances

can exist.

______________________________________________________________________

# Best Practices

✅ Use Singleton only for shared application resources.

✅ Prefer Dependency Injection when possible.

✅ Make initialization lazy if expensive.

✅ Keep shared state immutable where possible.

______________________________________________________________________

# Common Mistakes

### Making Everything a Singleton

Not every class

needs to exist

only once.

______________________________________________________________________

### Using Singleton for Database Sessions

Sessions

should be

request-scoped,

not global.

______________________________________________________________________

### Ignoring Thread Safety

Production systems

must consider

multiple threads

and processes.

______________________________________________________________________

### Hiding Dependencies

Overusing Singleton

can make dependencies

invisible,

making testing

more difficult.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Singleton Pattern, and when should you use it?

The Singleton Pattern is a creational design pattern that ensures a class has only one instance throughout the
application's lifetime while providing a global access point to that instance. It is useful for shared resources such as
configuration, logging, metrics collection, and machine learning models. However, it should not be used for
request-specific or user-specific objects like database sessions or shopping carts. In modern backend applications,
Dependency Injection often replaces explicit Singleton implementations by creating shared instances during application
startup.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Singleton Pattern is
- Why it exists
- Python implementation
- Backend examples
- FastAPI example
- Advantages
- Disadvantages
- Best practices
- When to use it

______________________________________________________________________

# What's Next

[Strategy Pattern](16-strategy-pattern.md)

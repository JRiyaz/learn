# Software Design & Design Patterns - Part 11

# Interface Segregation Principle (ISP)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Interface Segregation Principle (ISP) is
- Why ISP exists
- The problem ISP solves
- Fat interfaces vs focused interfaces
- How Python approaches interfaces
- Real-world backend examples
- FastAPI examples
- Protocols and Abstract Base Classes (ABC)
- When NOT to use ISP

______________________________________________________________________

# The Problem

Let's continue with our **Library Management System**.

Your application supports different notification services.

A developer designs the following interface.

```python
from abc import ABC, abstractmethod

class NotificationService(ABC):

    @abstractmethod
    def send_email(self):
        ...

    @abstractmethod
    def send_sms(self):
        ...

    @abstractmethod
    def send_whatsapp(self):
        ...

    @abstractmethod
    def send_push(self):
        ...
```

Looks good.

Or does it?

______________________________________________________________________

# Email Notification

Now,

the developer implements

Email notifications.

```python
class EmailService(
    NotificationService
):

    def send_email(self):
        print("Email Sent")

    def send_sms(self):
        raise NotImplementedError

    def send_whatsapp(self):
        raise NotImplementedError

    def send_push(self):
        raise NotImplementedError
```

______________________________________________________________________

# SMS Notification

```python
class SMSService(
    NotificationService
):

    def send_email(self):
        raise NotImplementedError

    def send_sms(self):
        print("SMS Sent")

    def send_whatsapp(self):
        raise NotImplementedError

    def send_push(self):
        raise NotImplementedError
```

______________________________________________________________________

# What's the Problem?

Every implementation

is forced

to implement methods

it doesn't need.

The result?

Lots of

```python
raise NotImplementedError
```

This is usually

a design smell.

______________________________________________________________________

# Another Example

Suppose

we support

storage providers.

```python
class Storage:

    def upload(self):
        ...

    def download(self):
        ...

    def stream_video(self):
        ...

    def compress(self):
        ...
```

Now,

you implement

Local Storage.

Does it support

video streaming?

Maybe not.

Does it support

compression?

Maybe not.

Again,

you're forced

to implement

methods

you don't need.

______________________________________________________________________

# This Is What ISP Solves

The **Interface Segregation Principle** states:

> **Clients should not be forced to depend on methods they do not use.**

Instead of

one large interface,

create

smaller,

focused interfaces.

______________________________________________________________________

# Bad Design

```text
NotificationService

↓

Email

SMS

WhatsApp

Push

Slack

Teams

Telegram
```

One giant interface.

Every implementation

depends on everything.

______________________________________________________________________

# Better Design

Split responsibilities.

```python
class EmailSender(ABC):

    @abstractmethod
    def send_email(
        self,
        message,
    ):
        ...
```

```python
class SMSSender(ABC):

    @abstractmethod
    def send_sms(
        self,
        message,
    ):
        ...
```

```python
class PushSender(ABC):

    @abstractmethod
    def send_push(
        self,
        message,
    ):
        ...
```

Now,

each implementation

only supports

what it actually needs.

______________________________________________________________________

# Real Backend Example

Suppose

your application

supports

file storage.

Instead of

```python
class Storage:

    def upload(self):
        ...

    def download(self):
        ...

    def stream(self):
        ...

    def resize_image(self):
        ...
```

Split it.

```python
UploadStorage
```

```python
DownloadStorage
```

```python
VideoStreamingStorage
```

Each implementation

remains focused.

______________________________________________________________________

# Python's Way

Unlike Java,

Python

doesn't require

formal interfaces.

Instead,

Python encourages

Duck Typing.

If an object

has

```python
upload()
```

then

it's acceptable

wherever

an uploader

is expected.

This naturally

encourages

smaller interfaces.

______________________________________________________________________

# Protocols (Python 3.8+)

Modern Python

introduces

Protocols.

Example

```python
from typing import Protocol

class PaymentProvider(
    Protocol
):

    def pay(
        self,
        amount: float,
    ) -> None:
        ...
```

Now,

any class

implementing

```python
pay()
```

matches the protocol,

even without inheritance.

This is one reason

Protocols

are becoming popular

in modern Python.

______________________________________________________________________

# Abstract Base Classes

Sometimes,

you want

a stricter contract.

Python provides

ABCs.

Example

```python
from abc import (
    ABC,
    abstractmethod,
)
```

Use ABCs

when you want

to enforce

required methods.

Use Protocols

when you care

about behavior

rather than inheritance.

______________________________________________________________________

# FastAPI Example

Suppose

your endpoint

uploads files.

Bad

```python
class Storage:

    def upload(self):
        ...

    def delete(self):
        ...

    def stream(self):
        ...

    def resize(self):
        ...
```

Better

```python
Uploader
```

The endpoint

only needs

```python
upload()
```

Why require

everything else?

______________________________________________________________________

# Another Example

Suppose

our recommendation engine

needs only

```python
predict()
```

It doesn't care

whether

the AI model

can:

- Train
- Export
- Quantize
- Fine-tune

Those belong

in separate interfaces.

______________________________________________________________________

# Benefits of ISP

Applying ISP gives you:

✅ Smaller interfaces

✅ Easier testing

✅ Better flexibility

✅ Less coupling

✅ Cleaner implementations

______________________________________________________________________

# ISP and Microservices

Interestingly,

ISP also appears

at the API level.

Bad API

```text
POST /everything
```

Better APIs

```text
POST /books

POST /members

POST /payments
```

Each endpoint

serves

a focused purpose.

Although ISP

is an OOP principle,

the same thinking

improves

REST API design.

______________________________________________________________________

# When NOT to Use ISP

Don't split

every interface

into

dozens

of tiny interfaces.

Example

```python
BookNameGetter
```

```python
BookTitleGetter
```

```python
BookISBNGetter
```

This creates

unnecessary complexity.

Interfaces

should be

small,

but meaningful.

______________________________________________________________________

# Best Practices

✅ Keep interfaces focused.

✅ Group related behavior.

✅ Use Protocols for flexible designs.

✅ Use ABCs when strict contracts are needed.

✅ Avoid forcing implementations to support unused methods.

______________________________________________________________________

# Common Mistakes

### Giant Interfaces

Large interfaces

usually violate ISP.

______________________________________________________________________

### Too Many Tiny Interfaces

Splitting everything

creates

confusing designs.

______________________________________________________________________

### Misusing Inheritance

Don't inherit

just to satisfy

an interface.

______________________________________________________________________

### Ignoring Duck Typing

Python already

encourages

small,

behavior-focused designs.

Take advantage of it.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Interface Segregation Principle?

The Interface Segregation Principle states that clients should not be forced to depend on methods they do not use.
Instead of creating large interfaces with many unrelated methods, developers should design smaller, focused interfaces
that represent a single capability. In Python, this principle is commonly implemented using duck typing, Protocols, or
Abstract Base Classes. Following ISP reduces coupling, simplifies implementations, and makes code easier to extend and
maintain.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What ISP is
- Why it exists
- Fat interfaces vs focused interfaces
- Protocols
- Abstract Base Classes
- FastAPI examples
- Backend examples
- Best practices
- Common mistakes

______________________________________________________________________

# What's Next

[Dependency Inversion Principle (DIP)](12-dependency-inversion-principle.md)

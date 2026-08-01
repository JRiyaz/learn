# Software Design & Design Patterns - Part 10

# Liskov Substitution Principle (LSP)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Liskov Substitution Principle (LSP) is
- Why LSP exists
- The problem LSP solves
- How bad inheritance breaks applications
- Real-world backend examples
- FastAPI examples
- How LSP relates to inheritance and polymorphism
- When NOT to use inheritance

______________________________________________________________________

# The Problem

Let's continue with our **Library Management System**.

We already have a `Book` class.

A developer writes:

```python
class Book:

    def borrow(self):
        print("Book Borrowed")
```

Now,

the library introduces

**Reference Books**.

Business Rule:

> Reference books **cannot** be borrowed.

A junior developer thinks,

> "ReferenceBook is a Book, so let's inherit."

```python
class ReferenceBook(Book):

    def borrow(self):
        raise Exception(
            "Reference books cannot be borrowed."
        )
```

Everything compiles.

But...

______________________________________________________________________

# Somewhere Else in the Application

Another developer writes

a reusable function.

```python
def issue_book(book):

    book.borrow()

    print("Success")
```

It works for

```python
Book()
```

But now,

someone passes

```python
ReferenceBook()
```

The application crashes.

______________________________________________________________________

# What's the Problem?

The function

expects

every Book

to support borrowing.

But one subclass

changes

that expectation.

Now,

code that worked before

starts failing.

______________________________________________________________________

# This Is an LSP Violation

The child class

cannot safely replace

the parent class.

That breaks

the Liskov Substitution Principle.

______________________________________________________________________

# What is LSP?

The **Liskov Substitution Principle** states:

> **Objects of a subclass should be replaceable with objects of the superclass without changing the correctness of the program.**

That's a long definition.

Let's simplify it.

______________________________________________________________________

# Simple Meaning

If

```text
EBook

IS A

Book
```

then

everywhere

a `Book`

is expected,

an `EBook`

should work

without breaking anything.

If it doesn't,

inheritance

was probably

the wrong choice.

______________________________________________________________________

# Another Example

Suppose

your payment system

has

```python
class PaymentProvider:

    def pay(
        self,
        amount,
    ):
        ...
```

Stripe

implements

```python
pay()
```

Razorpay

implements

```python
pay()
```

PayPal

implements

```python
pay()
```

Now,

the checkout service

can safely use

any provider.

That follows LSP.

______________________________________________________________________

# Bad Example

Suppose

someone writes

```python
class BrokenProvider(
    PaymentProvider
):

    def pay(
        self,
        amount,
    ):
        raise Exception(
            "Payments not supported."
        )
```

Why inherit

from `PaymentProvider`

if the provider

can't process payments?

The inheritance

doesn't make sense.

______________________________________________________________________

# Real Backend Example

Suppose

we build

storage providers.

```python
class Storage:

    def upload(
        self,
        file,
    ):
        ...
```

Implementations

```python
S3Storage
```

```python
AzureStorage
```

```python
GoogleCloudStorage
```

Every implementation

supports

```python
upload()
```

The caller

doesn't care

which provider

it receives.

That is

proper LSP.

______________________________________________________________________

# Bad Storage Example

Imagine

someone creates

```python
class ReadOnlyStorage(
    Storage
):

    def upload(
        self,
        file,
    ):
        raise Exception(
            "Uploads disabled."
        )
```

Now,

code expecting

a Storage object

can suddenly fail.

That's an LSP violation.

______________________________________________________________________

# FastAPI Example

Suppose

your endpoint

receives

a storage service.

```python
@app.post("/upload")
def upload(

    storage,

):

    storage.upload(file)
```

The endpoint

should work

whether

the storage is

- AWS S3
- Azure Blob
- Google Cloud Storage

If one implementation

throws

"Not Supported"

the abstraction

is broken.

______________________________________________________________________

# Why Does This Happen?

Developers often think

> "These classes look similar."

Similarity

is not enough.

Inheritance requires

behavioral compatibility.

______________________________________________________________________

# The Rectangle & Square Example

You may have seen

the famous

Rectangle/Square example.

While academically useful,

it's not a common problem

for backend engineers.

In real backend development,

LSP violations usually appear in:

- Payment providers
- Storage providers
- Notification services
- Authentication providers
- Database repositories

These examples

are much more relevant.

______________________________________________________________________

# How to Avoid LSP Violations

Ask yourself:

> If I replace

```text
Parent
```

with

```text
Child
```

will the application

still behave correctly?

If the answer is

"No,"

don't use inheritance.

______________________________________________________________________

# LSP and Polymorphism

Polymorphism

only works

when LSP

is respected.

Otherwise,

you end up writing

```python
if isinstance(
    provider,
    BrokenProvider,
):
    ...
```

Once you start

checking

for specific subclasses,

your design

is already in trouble.

______________________________________________________________________

# When NOT to Use Inheritance

If a subclass

needs to:

- Disable methods
- Throw "Not Supported"
- Ignore parent behavior
- Change business meaning

it's usually

a sign

that inheritance

is the wrong choice.

Composition

is often better.

______________________________________________________________________

# Best Practices

✅ Child classes should honor the parent's contract.

✅ Every subclass should behave as users expect.

✅ Use inheritance only for genuine "IS-A" relationships.

✅ Prefer composition when behavior differs significantly.

______________________________________________________________________

# Common Mistakes

### Throwing "Not Supported"

If a subclass

cannot perform

the parent's behavior,

it probably

shouldn't inherit

from that parent.

______________________________________________________________________

### Changing Business Rules

Child classes

should extend behavior,

not contradict it.

______________________________________________________________________

### Using Inheritance for Code Reuse

Code reuse alone

is not enough

to justify inheritance.

______________________________________________________________________

### Ignoring Behavioral Compatibility

Inheritance

is about behavior,

not just shared fields.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Liskov Substitution Principle?

The Liskov Substitution Principle states that objects of a subclass should be replaceable with objects of the superclass
without changing the correctness of the program. In practice, this means child classes must honor the behavior and
expectations established by their parent class. If replacing a parent object with a child object causes failures or
unexpected behavior, the inheritance hierarchy is likely incorrect. LSP is essential for reliable polymorphism and
extensible object-oriented designs.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What LSP is
- Why it exists
- Real backend examples
- FastAPI example
- Common LSP violations
- How to avoid incorrect inheritance
- Best practices

______________________________________________________________________

# What's Next

[Interface Segregation Principle (ISP)](11-interface-segregation-principle.md)

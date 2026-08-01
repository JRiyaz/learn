# Software Design & Design Patterns - Part 02

# Abstraction

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Abstraction is
- Why Abstraction exists
- The problem it solves
- How Abstraction works in backend applications
- Real-world Python examples
- FastAPI examples
- When to use Abstraction
- When NOT to use it

______________________________________________________________________

# The Problem

Let's continue building our **Library Management System**.

We have a requirement:

> Members should be able to borrow books.

A junior developer writes this.

```python
class Book:

    def __init__(self, title):
        self.title = title
        self.available = True

    def borrow(self):
        if self.available:
            print("Checking member...")
            print("Checking overdue books...")
            print("Checking borrowing limit...")
            print("Updating database...")
            print("Creating audit log...")
            print("Sending notification...")
            self.available = False
```

The method works.

But imagine you're the developer using this class.

Do you really need to know **all six steps**?

No.

You only care about one thing.

```python
book.borrow()
```

______________________________________________________________________

# What's the Problem?

Suppose tomorrow,

the business changes the process.

Now borrowing also needs to:

- Verify membership expiry
- Check reservation queue
- Calculate rental fee
- Update recommendation engine
- Publish Kafka event

Every caller still writes

```python
book.borrow()
```

They shouldn't care

about what happens internally.

______________________________________________________________________

# This Is Where Abstraction Helps

Abstraction means:

> **Hide unnecessary implementation details and expose only what users need.**

The caller doesn't need to know:

- Database queries
- Cache updates
- Kafka events
- Logging
- Notifications

They only need one simple action.

```python
book.borrow()
```

______________________________________________________________________

# Real-World Example

Think about driving a car.

You press:

```text
Start Button
```

Do you know exactly how:

- Fuel injection works?
- Spark plugs ignite?
- The starter motor spins?
- The ECU communicates?

No.

You don't need to.

The car hides all those details.

That's **Abstraction**.

______________________________________________________________________

# Another Real-World Example

ATM Machine.

You choose:

```text
Withdraw Money
```

Behind the scenes,

the ATM:

- Verifies your PIN
- Contacts the bank
- Checks your balance
- Updates the database
- Dispenses cash
- Prints a receipt

You don't need to know any of this.

You simply press

```text
Withdraw
```

______________________________________________________________________

# Backend Example

Suppose your application sends emails.

Without abstraction:

```python
connect_to_smtp()

authenticate()

build_email()

send_email()

close_connection()
```

Every developer

must remember

all five steps.

______________________________________________________________________

# Better Design

```python
email_service.send(
    to="user@example.com",
    subject="Book Borrowed",
    body="Enjoy reading!"
)
```

The complexity

is hidden.

The interface

is simple.

______________________________________________________________________

# FastAPI Example

Suppose you have an endpoint.

```python
@app.post("/borrow/{book_id}")
def borrow_book(book_id: int):
    library_service.borrow(book_id)
```

Notice something.

The endpoint doesn't know:

- SQL queries
- Cache updates
- Notifications
- Audit logging

It delegates everything to

```python
library_service.borrow()
```

The endpoint sees only

the abstraction.

______________________________________________________________________

# Database Example

Suppose you use SQLAlchemy.

You write

```python
session.add(book)

session.commit()
```

Do you know exactly how SQLAlchemy:

- Generates SQL?
- Opens database connections?
- Manages transactions?

No.

SQLAlchemy abstracts

those implementation details.

______________________________________________________________________

# Payment Gateway Example

Suppose your application supports Stripe.

You write

```python
payment_service.pay(
    amount=500
)
```

Tomorrow,

the company switches to Razorpay.

Your code remains

exactly the same.

Only the implementation changes.

The abstraction stays stable.

______________________________________________________________________

# What Should Be Hidden?

Good candidates for abstraction:

- Database logic
- Network calls
- File operations
- External APIs
- Cache operations
- Logging
- Email sending
- Payment processing

The caller

doesn't need to know

how they're implemented.

______________________________________________________________________

# What Should Be Exposed?

Expose only

what another developer

actually needs.

Example

Good

```python
book.borrow()
```

Bad

```python
check_member()

update_database()

send_email()

update_cache()

publish_event()
```

One operation.

One intention.

______________________________________________________________________

# Does Abstraction Mean Less Code?

No.

In fact,

the implementation

may become larger.

But the **public interface**

becomes much simpler.

Simple interfaces

are easier to:

- Learn
- Test
- Maintain
- Extend

______________________________________________________________________

# When NOT to Use Abstraction

Don't create abstractions

for very small applications.

Bad example:

```python
class MathService:

    def add(self, a, b):
        return a + b
```

A simple function

is much better.

Don't hide complexity

that doesn't exist.

______________________________________________________________________

# Best Practices

✅ Hide implementation details.

✅ Keep public interfaces simple.

✅ Expose business operations, not technical steps.

✅ Change implementation without changing the public API.

______________________________________________________________________

# Common Mistakes

### Exposing Too Much

If callers need to know

every internal step,

your abstraction isn't helping.

______________________________________________________________________

### Creating Useless Wrappers

Avoid classes

that simply call

another function

without adding value.

______________________________________________________________________

### Mixing Business Logic Everywhere

Business logic

should live behind

clear abstractions,

not be duplicated

across endpoints.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Abstraction in Object-Oriented Programming?

Abstraction is the process of hiding implementation details while exposing only the functionality that users need. It
allows developers to interact with simple, well-defined interfaces without understanding the underlying complexity. In
backend applications, abstractions are commonly used for services such as database access, payment gateways, email
sending, caching, and external APIs. This makes the code easier to maintain, test, and extend.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Abstraction is
- Why it exists
- The problem it solves
- Real-world examples
- FastAPI example
- SQLAlchemy example
- When to use it
- When not to use it

______________________________________________________________________

# What's Next

[Encapsulation](03-encapsulation.md)

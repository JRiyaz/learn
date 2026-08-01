# Software Design & Design Patterns - Part 09

# Open/Closed Principle (OCP)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Open/Closed Principle (OCP) is
- The problem OCP solves
- Why modifying existing code is risky
- How to extend software without changing existing code
- Real-world backend examples
- FastAPI examples
- How OCP leads to the Strategy and Factory patterns
- When NOT to overuse OCP

______________________________________________________________________

# The Problem

Let's continue building our **Library Management System**.

When a member borrows a book,

the library sends a notification.

Initially,

the business only wants Email.

A developer writes:

```python
class NotificationService:

    def send(
        self,
        message,
        notification_type,
    ):

        if notification_type == "email":
            print("Sending Email")
```

Everything works.

______________________________________________________________________

# One Month Later...

The business says

> "Customers also want SMS."

The developer modifies the code.

```python
if notification_type == "email":
    ...

elif notification_type == "sms":
    ...
```

______________________________________________________________________

# Another Month Later...

Now support:

- WhatsApp
- Slack
- Microsoft Teams

The code becomes

```python
if notification_type == "email":
    ...

elif notification_type == "sms":
    ...

elif notification_type == "whatsapp":
    ...

elif notification_type == "slack":
    ...

elif notification_type == "teams":
    ...
```

Every new notification

requires editing

the same class.

______________________________________________________________________

# What's the Problem?

Imagine this code

is already running

in production.

Every time

you modify it,

you risk introducing bugs.

Suppose

while adding Slack,

you accidentally break Email.

Now,

a feature

that worked yesterday

stops working today.

This happens

more often

than you might think.

______________________________________________________________________

# The Cost of Modifying Existing Code

Every modification introduces risk.

Examples:

- New bugs
- Regression issues
- Merge conflicts
- Difficult testing
- Unexpected side effects

As software grows,

modifying existing code

becomes increasingly expensive.

______________________________________________________________________

# What is OCP?

The **Open/Closed Principle** states:

> **Software entities should be open for extension but closed for modification.**

This sentence

confuses many developers.

Let's break it down.

______________________________________________________________________

# Open for Extension

We should be able

to add

new functionality.

Example:

Today

```text
Email
```

Tomorrow

```text
Email

SMS
```

Next month

```text
Email

SMS

WhatsApp
```

Adding new behavior

should be easy.

______________________________________________________________________

# Closed for Modification

Adding new behavior

should **not require changing**

existing,

working code.

If possible,

existing classes

should remain untouched.

______________________________________________________________________

# How Do We Achieve This?

Instead of

checking

notification types,

let each notification

know

how to send itself.

______________________________________________________________________

# Step 1

Create an abstraction.

```python
class Notification:

    def send(
        self,
        message,
    ):
        raise NotImplementedError
```

______________________________________________________________________

# Step 2

Implement Email.

```python
class EmailNotification(
    Notification
):

    def send(
        self,
        message,
    ):
        print(
            "Sending Email"
        )
```

______________________________________________________________________

# Step 3

Implement SMS.

```python
class SMSNotification(
    Notification
):

    def send(
        self,
        message,
    ):
        print(
            "Sending SMS"
        )
```

______________________________________________________________________

# Step 4

Notification Service

```python
class NotificationService:

    def send(

        self,

        provider,

        message,

    ):

        provider.send(message)
```

Notice something.

The service

never changes.

______________________________________________________________________

# Adding WhatsApp

Need WhatsApp?

Create a new class.

```python
class WhatsAppNotification(
    Notification
):

    def send(
        self,
        message,
    ):
        print(
            "Sending WhatsApp"
        )
```

Did we modify

NotificationService?

No.

We simply

extended

the system.

That is exactly

what OCP encourages.

______________________________________________________________________

# Another Backend Example

Suppose

our library

supports

only Stripe.

```python
if provider == "stripe":
    ...
```

Later,

Razorpay arrives.

```python
elif provider == "razorpay":
    ...
```

Later,

PayPal.

```python
elif provider == "paypal":
    ...
```

Eventually,

the method

contains

ten payment providers.

A better solution

is to create

one class

per provider.

The checkout service

never changes.

______________________________________________________________________

# FastAPI Example

Suppose

you support

multiple storage providers.

Your endpoint

shouldn't contain

```python
if storage == "s3":
    ...

elif storage == "azure":
    ...

elif storage == "gcs":
    ...
```

Instead,

inject

the appropriate

storage provider.

```python
storage.upload(file)
```

Tomorrow,

adding Backblaze

requires

only a new class.

The endpoint

stays unchanged.

______________________________________________________________________

# OCP and Design Patterns

Many famous patterns

exist primarily

to implement OCP.

Examples:

- Strategy Pattern
- Factory Pattern
- Decorator Pattern
- Observer Pattern

You'll notice

that almost all of them

allow us

to add behavior

without modifying

existing classes.

______________________________________________________________________

# Real Company Example

Imagine Netflix

supports

multiple recommendation algorithms.

Instead of

rewriting

the recommendation service

every month,

engineers create

new recommendation strategies.

The service

simply executes

the selected strategy.

______________________________________________________________________

# Benefits of OCP

Following OCP gives you:

✅ Easier maintenance

✅ Fewer regression bugs

✅ Easier testing

✅ Better scalability

✅ Safer deployments

______________________________________________________________________

# When NOT to Apply OCP

Don't design

for problems

that don't exist.

Suppose

your application

will always

send Email

and nothing else.

Creating

ten abstractions

would only

make the code

more complicated.

Keep it simple

until change

becomes likely.

______________________________________________________________________

# Best Practices

✅ Extend behavior

instead of modifying it.

✅ Prefer polymorphism

over large `if-elif` blocks.

✅ Design around abstractions.

✅ Let new features

be added

through new classes.

______________________________________________________________________

# Common Mistakes

### Predicting Every Future Requirement

Don't create

dozens of abstractions

for hypothetical features.

Design for

probable change,

not imaginary change.

______________________________________________________________________

### Giant Conditional Statements

Large

`if-elif`

blocks

are often

a sign

that OCP

is being violated.

______________________________________________________________________

### Changing Stable Code

If working code

changes

every time

a feature is added,

consider redesigning it.

______________________________________________________________________

### Confusing OCP with "Never Modify Code"

OCP doesn't mean

code should never change.

It means

well-designed parts

shouldn't require modification

every time

new behavior

is introduced.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Open/Closed Principle?

The Open/Closed Principle states that software should be open for extension but closed for modification. This means
developers should be able to add new functionality without changing existing, working code. OCP is commonly achieved
using abstractions, polymorphism, and design patterns such as Strategy and Factory. Following OCP reduces regression
bugs, simplifies testing, and makes software easier to extend as business requirements evolve.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What OCP is
- Why modifying existing code is risky
- How to extend behavior safely
- Backend examples
- FastAPI example
- Relationship with design patterns
- Benefits
- Common mistakes

______________________________________________________________________

# What's Next

[Liskov Substitution Principle (LSP)](10-liskov-substitution-principle.md)

# Software Design & Design Patterns - Part 05

# Polymorphism

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Polymorphism is
- Why Polymorphism exists
- The problem it solves
- Method overriding
- Duck Typing in Python
- Real-world backend examples
- FastAPI examples
- When to use Polymorphism
- When NOT to use it

______________________________________________________________________

# The Problem

Let's continue building our **Library Management System**.

The library now supports multiple notification channels.

- Email
- SMS
- WhatsApp

A junior developer writes the following code.

```python id="poly0501"
def send_notification(
    notification_type,
    message,
):

    if notification_type == "email":
        print(
            f"Email: {message}"
        )

    elif notification_type == "sms":
        print(
            f"SMS: {message}"
        )

    elif notification_type == "whatsapp":
        print(
            f"WhatsApp: {message}"
        )
```

It works.

______________________________________________________________________

# New Requirement

The business grows.

Now it also wants:

- Slack
- Microsoft Teams
- Push Notifications
- Discord
- Telegram

The function becomes

larger and larger.

```python id="poly0502"
if notification == "email":
    ...

elif notification == "sms":
    ...

elif notification == "whatsapp":
    ...

elif notification == "slack":
    ...

elif notification == "teams":
    ...

elif notification == "telegram":
    ...
```

Every new notification type

requires modifying

the existing function.

______________________________________________________________________

# What's the Problem?

Problems:

❌ Huge `if-elif` blocks

❌ Difficult to extend

❌ Difficult to test

❌ High chance of bugs

❌ Violates the Open/Closed Principle (we'll learn this soon)

There must be

a better way.

______________________________________________________________________

# The Idea

Instead of asking

"What type are you?"

ask the object

to do the work.

Every notification

knows

how to send itself.

______________________________________________________________________

# This Is Polymorphism

Polymorphism means:

> **Different objects can respond to the same method call in different ways.**

The caller

doesn't need to know

what type of object it is.

It simply calls

the same method.

______________________________________________________________________

# Refactored Design

```python id="poly0503"
class EmailNotification:

    def send(
        self,
        message,
    ):
        print(
            f"Email: {message}"
        )
```

```python id="poly0504"
class SMSNotification:

    def send(
        self,
        message,
    ):
        print(
            f"SMS: {message}"
        )
```

```python id="poly0505"
class WhatsAppNotification:

    def send(
        self,
        message,
    ):
        print(
            f"WhatsApp: {message}"
        )
```

______________________________________________________________________

# Using Polymorphism

Now

the caller writes

```python id="poly0506"
notification.send(
    "Book borrowed."
)
```

Notice something.

The caller

doesn't care whether

it's:

- Email
- SMS
- WhatsApp
- Slack

It simply calls

```python id="poly0507"
send()
```

Each object

behaves differently.

______________________________________________________________________

# Method Overriding

Polymorphism

is often achieved

through

method overriding.

Example

```python id="poly0508"
class Notification:

    def send(
        self,
        message,
    ):
        pass
```

Child

```python id="poly0509"
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

Another child

```python id="poly0510"
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

Same method.

Different behavior.

______________________________________________________________________

# Python's Superpower

Unlike Java,

Python doesn't require

a common parent class.

Suppose we write

```python id="poly0511"
class Email:

    def send(
        self,
        message,
    ):
        print(message)
```

And

```python id="poly0512"
class Slack:

    def send(
        self,
        message,
    ):
        print(message)
```

Now

```python id="poly0513"
def notify(
    service,
    message,
):
    service.send(message)
```

Works for both.

Why?

Because Python follows

**Duck Typing**.

______________________________________________________________________

# Duck Typing

Python's philosophy is:

> **If it walks like a duck and quacks like a duck, treat it as a duck.**

Meaning:

Python doesn't ask

"What class are you?"

It asks

"Can you do this?"

If the object

has

```python id="poly0514"
send()
```

Python is happy.

This is one reason

Python code

often looks cleaner

than Java code.

______________________________________________________________________

# Real Backend Example

Suppose your application

supports multiple

payment providers.

```python id="poly0515"
stripe.pay()
```

```python id="poly0516"
razorpay.pay()
```

```python id="poly0517"
paypal.pay()
```

The checkout service

simply calls

```python id="poly0518"
provider.pay()
```

No `if-elif` block.

No provider checks.

______________________________________________________________________

# AI/ML Example

Suppose your application

supports different

AI models.

```python id="poly0519"
model.predict(data)
```

Whether it's:

- OpenAI
- Anthropic
- Local Llama

The caller

uses the same method.

Different behavior.

______________________________________________________________________

# FastAPI Example

Suppose your application

stores files.

```python id="poly0520"
storage.upload(file)
```

Today

you use

AWS S3.

Tomorrow

you switch

to Azure Blob Storage.

The endpoint

doesn't change.

Only the object changes.

______________________________________________________________________

# Why Is This Powerful?

Adding a new provider

becomes easy.

Just create

another class.

No existing code

needs modification.

This is why

large applications

heavily rely

on polymorphism.

______________________________________________________________________

# When NOT to Use Polymorphism

Don't create

ten classes

for two simple functions.

If your application

will never support

multiple implementations,

simple code

is often better.

______________________________________________________________________

# Best Practices

✅ Program against behavior,

not concrete types.

✅ Avoid `if-elif`

based on object types.

✅ Give related objects

the same method names.

✅ Keep implementations

independent.

______________________________________________________________________

# Common Mistakes

### Checking Object Types

Bad

```python id="poly0521"
if isinstance(
    provider,
    Stripe,
):
    ...
```

If you need

many type checks,

you're probably

not using polymorphism effectively.

______________________________________________________________________

### Different Method Names

Bad

```python id="poly0522"
email.send_email()

sms.send_sms()

slack.post_message()
```

Better

```python id="poly0523"
provider.send()
```

The caller

doesn't care

about the implementation.

______________________________________________________________________

### Forgetting Duck Typing

In Python,

a common base class

is often unnecessary.

Behavior matters

more than inheritance.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Polymorphism, and how is it used in Python?

Polymorphism allows different objects to respond to the same method call in their own way. Instead of checking an
object's type, the caller simply invokes a common method, and each object provides its own implementation. In Python,
polymorphism is commonly achieved through method overriding and Duck Typing, where an object is accepted based on the
behavior it provides rather than its inheritance hierarchy. This makes backend applications more extensible and reduces
the need for large conditional statements.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Polymorphism is
- Why it exists
- Method overriding
- Duck Typing
- Backend examples
- FastAPI examples
- When to use it
- When not to use it

______________________________________________________________________

# What's Next

[Composition vs Inheritance](06-composition-vs-inheritance.md)

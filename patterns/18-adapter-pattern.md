# Software Design & Design Patterns - Part 18

# Adapter Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Adapter Pattern is
- Why the Adapter Pattern exists
- The problem it solves
- How to integrate third-party services
- Real-world backend examples
- FastAPI examples
- AI/ML examples
- When NOT to use the Adapter Pattern

______________________________________________________________________

# Before We Start

One thing you'll notice

during your career is:

**You rarely control third-party APIs.**

Instead,

your application must adapt

to whatever interface

they expose.

This is exactly

the problem

the Adapter Pattern solves.

______________________________________________________________________

# The Problem

Let's continue with our **Library Management System**.

Initially,

the application

uses Stripe.

The payment service

looks like this.

```python
class StripePayment:

    def pay(
        self,
        amount,
    ):

        print(
            f"Paid ₹{amount}"
        )
```

Business logic

calls

```python
stripe.pay(500)
```

Everything works.

______________________________________________________________________

# New Requirement

The company

expands to India.

It now wants

Razorpay.

Unfortunately,

Razorpay's SDK

looks like this.

```python
class RazorpayClient:

    def make_payment(
        self,
        value,
    ):

        print(
            f"Paid ₹{value}"
        )
```

Notice something.

Stripe uses

```python
pay()
```

Razorpay uses

```python
make_payment()
```

Different method names.

______________________________________________________________________

# Another Provider

Suppose

PayPal's SDK

looks like this.

```python
class PayPalClient:

    def process(
        self,
        amount,
    ):

        print(
            f"Paid ₹{amount}"
        )
```

Now,

every payment provider

uses

different APIs.

______________________________________________________________________

# First Attempt

A developer writes

```python
if provider == "stripe":

    stripe.pay(amount)

elif provider == "razorpay":

    razorpay.make_payment(
        amount
    )

elif provider == "paypal":

    paypal.process(amount)
```

It works.

But...

______________________________________________________________________

# What's the Problem?

Every new provider

changes

the business logic.

Problems:

❌ Huge conditional statements

❌ Tight coupling

❌ Difficult testing

❌ Difficult maintenance

Business logic

now knows

every SDK.

______________________________________________________________________

# The Idea

Instead of changing

our application,

let's adapt

the external SDK

to match

our application.

______________________________________________________________________

# What is the Adapter Pattern?

The **Adapter Pattern** says:

> **Convert the interface of one class into another interface that clients expect.**

In simple words,

an Adapter

acts like

a translator.

______________________________________________________________________

# Real-World Example

Imagine

you travel

from India

to the United States.

Your laptop charger

has an Indian plug.

The wall socket

accepts

an American plug.

You don't

buy

a new laptop.

You use

an adapter.

The laptop

doesn't change.

The wall socket

doesn't change.

The adapter

connects them.

______________________________________________________________________

# Step 1

Define

what

our application expects.

```python
from abc import (
    ABC,
    abstractmethod,
)

class PaymentProvider(
    ABC
):

    @abstractmethod
    def pay(
        self,
        amount,
    ):
        ...
```

______________________________________________________________________

# Step 2

Stripe

already matches.

```python
class StripePayment(
    PaymentProvider
):

    def pay(
        self,
        amount,
    ):

        print(
            f"Paid ₹{amount}"
        )
```

______________________________________________________________________

# Step 3

Create

an adapter

for Razorpay.

```python
class RazorpayAdapter(
    PaymentProvider
):

    def __init__(
        self,
        client,
    ):

        self.client = client

    def pay(
        self,
        amount,
    ):

        self.client.make_payment(
            amount
        )
```

Notice

what happened.

Our application

calls

```python
pay()
```

The adapter

translates it

to

```python
make_payment()
```

______________________________________________________________________

# Step 4

PayPal Adapter

```python
class PayPalAdapter(
    PaymentProvider
):

    def __init__(
        self,
        client,
    ):

        self.client = client

    def pay(
        self,
        amount,
    ):

        self.client.process(
            amount
        )
```

Again,

our application

still calls

```python
pay()
```

______________________________________________________________________

# Using the Adapter

```python
provider = RazorpayAdapter(
    RazorpayClient()
)

provider.pay(500)
```

Business logic

doesn't know

anything

about

`make_payment()`.

______________________________________________________________________

# Real Backend Example

Suppose

your application

supports

multiple cloud providers.

AWS SDK

```python
upload_file()
```

Azure SDK

```python
upload_blob()
```

Google Cloud

```python
upload_from_file()
```

Your application

shouldn't know

these differences.

Create adapters.

Expose

one method.

```python
upload()
```

______________________________________________________________________

# AI/ML Example

Suppose

your application

supports

multiple LLMs.

OpenAI

```python
client.responses.create(...)
```

Anthropic

```python
client.messages.create(...)
```

Local Llama

```python
model.generate(...)
```

Your application

should simply call

```python
llm.generate(prompt)
```

Adapters

hide

the differences

between SDKs.

This is a common pattern

in AI platforms.

______________________________________________________________________

# FastAPI Example

Suppose

your endpoint

uploads files.

```python
storage.upload(file)
```

Behind the scenes,

the storage adapter

could be using

- AWS S3
- Azure Blob
- Google Cloud Storage
- Local Disk

The endpoint

never changes.

______________________________________________________________________

# Adapter vs Strategy

This is a common interview question.

Both patterns

allow interchangeable behavior,

but they solve

different problems.

| Strategy | Adapter |
| ------------------------------ | ----------------------------------- |
| Chooses between algorithms | Converts one interface into another |
| You design all implementations | Third-party APIs already exist |
| Behavior changes | Interface changes |

Example:

Payment algorithm

↓

Strategy

Third-party SDK

↓

Adapter

______________________________________________________________________

# Benefits

Using Adapter gives you:

✅ Third-party SDK isolation

✅ Cleaner business logic

✅ Easier provider replacement

✅ Easier testing

✅ Consistent interfaces

______________________________________________________________________

# Real Company Example

Suppose

your company

integrates

three shipping providers.

Each provider

returns

different JSON.

Instead of

making

your entire application

understand

three response formats,

each adapter

converts

the provider's response

into

one internal model.

The rest

of the application

works

with a single format.

______________________________________________________________________

# When NOT to Use Adapter

If you control

both sides

of the interface,

you usually

don't need

an adapter.

Simply design

the interface correctly

from the beginning.

Adapters

are most useful

when integrating

external systems

that you cannot change.

______________________________________________________________________

# Best Practices

✅ Keep adapters thin.

✅ Hide third-party SDKs.

✅ Convert external models into internal models.

✅ Keep business logic independent of vendor APIs.

______________________________________________________________________

# Common Mistakes

### Putting Business Logic Inside Adapters

Adapters

translate interfaces.

They should not

contain

business rules.

______________________________________________________________________

### Exposing Third-Party SDKs

Don't let

vendor-specific classes

spread

throughout

your application.

Keep them

inside the adapter.

______________________________________________________________________

### Creating Huge Adapters

Each adapter

should adapt

one integration,

not an entire platform.

______________________________________________________________________

### Confusing Adapter with Strategy

Remember:

Strategy changes

behavior.

Adapter changes

interfaces.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Adapter Pattern, and where is it commonly used?

The Adapter Pattern is a structural design pattern that converts the interface of one class into another interface
expected by the client. It allows applications to integrate third-party libraries and external services without changing
business logic. The pattern is commonly used with payment gateways, cloud storage providers, shipping APIs,
authentication providers, and AI model SDKs, where each external system exposes a different interface.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Adapter Pattern is
- Why it exists
- Backend examples
- FastAPI example
- AI/ML example
- Adapter vs Strategy
- Benefits
- Common mistakes

______________________________________________________________________

# What's Next

[Decorator Pattern](19-decorator-pattern.md)

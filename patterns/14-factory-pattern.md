# Software Design & Design Patterns - Part 14

# Factory Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Factory Pattern is
- Why the Factory Pattern exists
- The problem it solves
- How object creation becomes a maintenance problem
- Real-world backend examples
- FastAPI examples
- Advantages and disadvantages
- When NOT to use the Factory Pattern

______________________________________________________________________

# The Problem

Let's continue with our **Library Management System**.

The library allows users to pay fines.

Initially,

the application supports

only **Stripe**.

A developer writes

```python
class StripePayment:

    def pay(
        self,
        amount,
    ):
        print(
            f"Paid ₹{amount} using Stripe."
        )
```

The service uses it.

```python
class PaymentService:

    def process_payment(
        self,
        amount,
    ):

        payment = StripePayment()

        payment.pay(amount)
```

Everything works.

______________________________________________________________________

# New Requirement

The business expands to India.

Now,

payments must support:

- Stripe
- Razorpay

The developer updates

the service.

```python
class PaymentService:

    def process_payment(

        self,

        provider,

        amount,

    ):

        if provider == "stripe":

            payment = StripePayment()

        elif provider == "razorpay":

            payment = RazorpayPayment()

        payment.pay(amount)
```

______________________________________________________________________

# Another Requirement

The company expands again.

Now,

support:

- PayPal
- Square
- PayU
- Cashfree

The method becomes

```python
if provider == "stripe":
    ...

elif provider == "razorpay":
    ...

elif provider == "paypal":
    ...

elif provider == "square":
    ...

elif provider == "payu":
    ...

elif provider == "cashfree":
    ...
```

______________________________________________________________________

# What's the Problem?

The business logic

is now responsible for

creating objects.

Ask yourself.

Should

`PaymentService`

know

how to create

every payment provider?

No.

Its responsibility

is to process payments,

not decide

which object

to instantiate.

______________________________________________________________________

# Another Problem

Suppose

creating

`StripePayment`

becomes complicated.

```python
payment = StripePayment(

    api_key,

    timeout,

    retry_policy,

    logger,

    metrics,

    cache,

)
```

Now,

every place

creating Stripe objects

must know

all these details.

Object creation

has become

business logic.

______________________________________________________________________

# This Is Where the Factory Pattern Helps

The **Factory Pattern** says:

> **Move object creation into a dedicated class or function.**

Instead of

every class

creating objects,

let one component

handle object creation.

______________________________________________________________________

# Without Factory

```text
PaymentService

↓

Creates Stripe

↓

Creates Razorpay

↓

Creates PayPal
```

The service

knows

too much.

______________________________________________________________________

# With Factory

```text
PaymentService

↓

PaymentFactory

↓

Stripe

↓

Razorpay

↓

PayPal
```

The service

only knows

about

the factory.

______________________________________________________________________

# Step 1

Create

the payment providers.

```python
class StripePayment:

    def pay(
        self,
        amount,
    ):
        print(
            "Stripe Payment"
        )
```

```python
class RazorpayPayment:

    def pay(
        self,
        amount,
    ):
        print(
            "Razorpay Payment"
        )
```

______________________________________________________________________

# Step 2

Create

the factory.

```python
class PaymentFactory:

    @staticmethod
    def create(

        provider,

    ):

        if provider == "stripe":
            return StripePayment()

        if provider == "razorpay":
            return RazorpayPayment()

        raise ValueError(
            "Unsupported provider."
        )
```

Notice something.

Only one class

contains

the object creation logic.

______________________________________________________________________

# Step 3

Use the factory.

```python
class PaymentService:

    def process_payment(

        self,

        provider,

        amount,

    ):

        payment = PaymentFactory.create(
            provider
        )

        payment.pay(amount)
```

The service

doesn't know

how objects

are created.

______________________________________________________________________

# Adding PayPal

Tomorrow,

the business adds

PayPal.

Which class changes?

Only

```python
PaymentFactory
```

The business logic

inside

`PaymentService`

remains unchanged.

______________________________________________________________________

# Real Backend Example

Suppose

our application

stores files.

Depending on configuration,

we want

different storage providers.

```text
Development

↓

Local Storage
```

```text
Production

↓

AWS S3
```

```text
Enterprise

↓

Azure Blob Storage
```

Instead of writing

```python
if ENV == "dev":
    ...

elif ENV == "prod":
    ...
```

everywhere,

create

a Storage Factory.

______________________________________________________________________

# FastAPI Example

Suppose

our application

supports

multiple databases.

Configuration

decides

whether to use:

- PostgreSQL
- MySQL
- SQLite

During startup,

a factory creates

the correct repository.

The rest

of the application

doesn't care

which database

is being used.

______________________________________________________________________

# SQLAlchemy Example

Many developers

don't realize

they already use

a factory.

```python
SessionLocal = sessionmaker(
    ...
)
```

`sessionmaker`

is a factory.

It creates

database sessions

for you.

You never instantiate

the session

manually.

______________________________________________________________________

# Another Example

Suppose

your AI application

supports

multiple models.

```python
model = ModelFactory.create(
    "openai"
)
```

Tomorrow

```python
model = ModelFactory.create(
    "anthropic"
)
```

Or

```python
model = ModelFactory.create(
    "llama"
)
```

The caller

never changes.

______________________________________________________________________

# Factory vs Simple Function

Some developers ask,

"Why not use

a function?"

Good question.

Instead of

```python
PaymentFactory.create()
```

you could write

```python
create_payment_provider()
```

For small applications,

that's perfectly fine.

A dedicated factory class

becomes useful

when creation logic

grows

or multiple factories

exist.

______________________________________________________________________

# Benefits of Factory Pattern

Using a Factory gives you:

✅ Centralized object creation

✅ Cleaner business logic

✅ Easier maintenance

✅ Easier testing

✅ Easier configuration

______________________________________________________________________

# Factory and SOLID

The Factory Pattern

helps implement

multiple SOLID principles.

| Principle | Benefit |
| --------- | ------------------------------------------------ |
| SRP | Object creation is separated from business logic |
| OCP | Add new implementations easily |
| DIP | Return abstractions instead of concrete classes |

______________________________________________________________________

# When NOT to Use Factory

Don't introduce

a factory

for every object.

Bad

```python
UserFactory.create()
```

```python
BookFactory.create()
```

```python
AddressFactory.create()
```

when

all they do is

```python
return User()
```

Simple constructors

are perfectly fine.

Factories become valuable

when object creation

contains logic.

______________________________________________________________________

# Best Practices

✅ Use factories when object creation becomes complex.

✅ Keep business logic separate from creation logic.

✅ Return abstractions whenever possible.

✅ Keep factory methods focused.

______________________________________________________________________

# Common Mistakes

### Factory for Everything

Not every object

needs a factory.

______________________________________________________________________

### Putting Business Logic Inside the Factory

Factories should create objects,

not execute business rules.

______________________________________________________________________

### Duplicating Factory Logic

Keep object creation

in one place.

Avoid

multiple copies

of the same logic.

______________________________________________________________________

### Returning Different Interfaces

A factory should return

objects

that follow

the same contract.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Factory Pattern, and when should you use it?

The Factory Pattern is a creational design pattern that centralizes object creation in a dedicated factory instead of
creating objects throughout the application. It is useful when object creation becomes complex, depends on
configuration, or varies based on runtime conditions. By separating object creation from business logic, the Factory
Pattern improves maintainability, supports the Open/Closed Principle, and makes it easier to introduce new
implementations without changing existing business code.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Factory Pattern is
- Why it exists
- How it separates object creation
- Backend examples
- FastAPI example
- SQLAlchemy example
- Benefits
- Common mistakes
- When to use it

______________________________________________________________________

# What's Next

[Singleton Pattern](15-singleton-pattern.md)

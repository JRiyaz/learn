# Software Design & Design Patterns - Part 16

# Strategy Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Strategy Pattern is
- Why the Strategy Pattern exists
- The problem it solves
- How to eliminate large `if-elif` statements
- Real-world backend examples
- FastAPI examples
- How the Strategy Pattern relates to OCP and DIP
- When NOT to use the Strategy Pattern

______________________________________________________________________

# Before We Start

If I had to choose **one design pattern** that every backend engineer should master, it would be the **Strategy
Pattern**.

Why?

Because you'll find it almost everywhere:

- Payment Gateways
- Notification Services
- Authentication Providers
- AI Models
- Recommendation Engines
- File Storage
- Search Algorithms
- Discount Calculations

After this lesson, you'll start recognizing the Strategy Pattern in many frameworks and production codebases.

______________________________________________________________________

# The Problem

Let's continue with our **Library Management System**.

The library charges a fine when a member returns a book late.

Initially,

the application supports only **Credit Card** payments.

A developer writes:

```python
class PaymentService:

    def pay(
        self,
        amount,
    ):

        print(
            f"Paid ₹{amount} using Credit Card."
        )
```

Everything works.

______________________________________________________________________

# New Requirement

The business grows.

Now it supports:

- Credit Card
- UPI
- Net Banking

The developer updates the code.

```python
class PaymentService:

    def pay(

        self,

        payment_type,

        amount,

    ):

        if payment_type == "credit_card":

            print("Credit Card")

        elif payment_type == "upi":

            print("UPI")

        elif payment_type == "net_banking":

            print("Net Banking")
```

______________________________________________________________________

# Another Requirement

Now support:

- Wallet
- PayPal
- Stripe
- Razorpay

The method grows again.

```python
if payment == "credit_card":
    ...

elif payment == "upi":
    ...

elif payment == "wallet":
    ...

elif payment == "paypal":
    ...

elif payment == "stripe":
    ...

elif payment == "razorpay":
    ...
```

______________________________________________________________________

# What's the Problem?

Every new payment method

requires changing

the existing code.

Problems:

❌ Huge `if-elif` blocks

❌ Difficult testing

❌ Violates OCP

❌ Difficult maintenance

❌ High risk of regression bugs

There must be

a better solution.

______________________________________________________________________

# The Idea

Instead of asking

> "Which payment method should I execute?"

let each payment method

know

how to process itself.

The caller

simply says

```python
payment.pay(amount)
```

without caring

which implementation

is being used.

______________________________________________________________________

# What is the Strategy Pattern?

The **Strategy Pattern** says:

> **Define a family of algorithms, encapsulate each one, and make them interchangeable.**

That definition

sounds complicated.

Let's simplify it.

Instead of writing

one huge method,

create

one class

per algorithm.

Then choose

the appropriate class

at runtime.

______________________________________________________________________

# Step 1

Create

an abstraction.

```python
from abc import (
    ABC,
    abstractmethod,
)

class PaymentStrategy(
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

Implement

Credit Card.

```python
class CreditCardPayment(
    PaymentStrategy
):

    def pay(
        self,
        amount,
    ):

        print(
            f"Paid ₹{amount} using Credit Card."
        )
```

______________________________________________________________________

# Step 3

Implement

UPI.

```python
class UPIPayment(
    PaymentStrategy
):

    def pay(
        self,
        amount,
    ):

        print(
            f"Paid ₹{amount} using UPI."
        )
```

______________________________________________________________________

# Step 4

Implement

PayPal.

```python
class PayPalPayment(
    PaymentStrategy
):

    def pay(
        self,
        amount,
    ):

        print(
            f"Paid ₹{amount} using PayPal."
        )
```

______________________________________________________________________

# Step 5

Update

PaymentService.

```python
class PaymentService:

    def __init__(
        self,
        strategy,
    ):

        self.strategy = strategy

    def pay(
        self,
        amount,
    ):

        self.strategy.pay(
            amount
        )
```

Notice something.

There are

no

`if-elif`

statements.

______________________________________________________________________

# Using the Strategy

Credit Card

```python
payment = PaymentService(
    CreditCardPayment()
)

payment.pay(500)
```

UPI

```python
payment = PaymentService(
    UPIPayment()
)

payment.pay(500)
```

PayPal

```python
payment = PaymentService(
    PayPalPayment()
)

payment.pay(500)
```

The caller changes.

The service

doesn't.

______________________________________________________________________

# Adding Razorpay

Tomorrow,

the business adds

Razorpay.

Create

one class.

```python
class RazorpayPayment(
    PaymentStrategy
):

    def pay(
        self,
        amount,
    ):
        ...
```

Done.

Did we modify

`PaymentService`?

No.

We simply

added

another strategy.

______________________________________________________________________

# Real Backend Example

Suppose

our application

sends notifications.

Instead of

```python
if channel == "email":
    ...

elif channel == "sms":
    ...

elif channel == "slack":
    ...
```

Create:

- EmailStrategy
- SMSStrategy
- SlackStrategy

The notification service

calls

```python
strategy.send(message)
```

______________________________________________________________________

# AI/ML Example

Suppose

your application

supports different

LLMs.

```python
model.generate(
    prompt
)
```

Possible strategies:

- OpenAI
- Anthropic
- Gemini
- Llama
- Mistral

The application

doesn't know

which model

is being used.

It simply calls

```python
generate()
```

This is one reason

AI frameworks

often resemble

the Strategy Pattern.

______________________________________________________________________

# FastAPI Example

Suppose

your application

supports multiple

authentication methods.

- JWT
- OAuth2
- API Key
- SAML

Instead of

```python
if auth == "jwt":
    ...

elif auth == "oauth":
    ...
```

inject

the appropriate

authentication strategy.

The endpoint

remains unchanged.

______________________________________________________________________

# Strategy + Factory

A common interview question.

Developers often combine

Strategy

and

Factory.

Example

```text
Request

↓

Factory

↓

Choose Strategy

↓

Execute Strategy
```

The Factory

creates

the correct strategy.

The Strategy

executes

the behavior.

You'll often see

both patterns

used together.

______________________________________________________________________

# Strategy and SOLID

The Strategy Pattern

implements

multiple SOLID principles.

| Principle | Benefit |
| --------- | -------------------------------------------------- |
| OCP | Add new strategies without modifying existing code |
| DIP | Depend on abstractions |
| SRP | Each strategy has one responsibility |

______________________________________________________________________

# Benefits

Using the Strategy Pattern gives you:

✅ No giant `if-elif` blocks

✅ Easy extensibility

✅ Better testing

✅ Cleaner code

✅ Easier maintenance

______________________________________________________________________

# When NOT to Use Strategy

Suppose

your application

will always

use

one payment provider.

Creating

five strategy classes

would be unnecessary.

Use the Strategy Pattern

when

multiple interchangeable behaviors

exist

or are likely to exist.

______________________________________________________________________

# Best Practices

✅ One class per strategy.

✅ Give every strategy the same interface.

✅ Inject the strategy.

✅ Keep the context unaware of implementation details.

______________________________________________________________________

# Common Mistakes

### Giant Strategy Classes

Each strategy

should focus

on one algorithm.

______________________________________________________________________

### Using Strategy for Fixed Behavior

If behavior

never changes,

a simple method

is usually enough.

______________________________________________________________________

### Mixing Strategy Selection with Business Logic

Selecting

a strategy

and executing

a strategy

are different responsibilities.

Factories

often handle

selection.

______________________________________________________________________

### Reintroducing `if-elif`

If your Strategy Pattern

still contains

large conditional blocks,

you're probably

moving the problem

instead of solving it.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Strategy Pattern, and when should you use it?

The Strategy Pattern is a behavioral design pattern that defines a family of algorithms, encapsulates each one into its
own class, and makes them interchangeable. Instead of using large conditional statements, the application delegates
behavior to a strategy object selected at runtime. This pattern is commonly used for payment gateways, authentication
providers, storage providers, AI models, and notification systems. It supports the Open/Closed Principle by allowing new
behaviors to be added without modifying existing business logic.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Strategy Pattern is
- Why it exists
- How it removes `if-elif` blocks
- Backend examples
- FastAPI example
- AI/ML example
- Strategy + Factory
- Best practices
- Common mistakes

______________________________________________________________________

# What's Next

[Observer Pattern](17-observer-pattern.md)

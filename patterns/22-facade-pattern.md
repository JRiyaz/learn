# Software Design & Design Patterns - Part 22

# Facade Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Facade Pattern is
- Why the Facade Pattern exists
- The problem it solves
- How to simplify complex subsystems
- Real-world backend examples
- FastAPI examples
- Microservices examples
- When NOT to use the Facade Pattern

______________________________________________________________________

# Before We Start

Imagine you're buying a book online.

From your perspective,

you click

**Buy Now**.

That's it.

Behind the scenes,

the system performs:

- Validate inventory
- Process payment
- Update stock
- Generate invoice
- Send email
- Send SMS
- Publish Kafka event
- Update analytics
- Create shipment

One click.

Nine different systems.

How?

A **Facade**.

______________________________________________________________________

# The Problem

Let's continue with our

**Library Management System**.

When a member borrows a book,

our endpoint performs

many operations.

```python id="fac2201"
@app.post("/borrow")
def borrow_book():

    inventory.check()

    payment.collect_fine()

    repository.save()

    email.send()

    sms.send()

    analytics.update()

    audit.log()

    kafka.publish()

    cache.clear()
```

Everything works.

______________________________________________________________________

# What's the Problem?

Every endpoint

needs to know

about:

- Inventory
- Payment
- Email
- SMS
- Analytics
- Cache
- Kafka
- Audit

The endpoint

has become

the orchestrator

of the entire application.

Problems:

❌ Too many dependencies

❌ Difficult testing

❌ Hard to understand

❌ Tight coupling

______________________________________________________________________

# The Idea

Instead of

calling

eight services,

call

one service.

That service

internally

coordinates

everything.

______________________________________________________________________

# What is the Facade Pattern?

The **Facade Pattern** says:

> **Provide a simplified interface to a complex subsystem.**

Instead of exposing

many objects,

provide

one simple entry point.

______________________________________________________________________

# Without Facade

```text id="fac2202"
Endpoint

↓

Inventory

↓

Payment

↓

Repository

↓

Email

↓

SMS

↓

Analytics

↓

Kafka

↓

Cache
```

______________________________________________________________________

# With Facade

```text id="fac2203"
Endpoint

↓

BorrowFacade

↓

Inventory

Payment

Repository

Email

SMS

Analytics

Kafka

Cache
```

The endpoint

knows

only one class.

______________________________________________________________________

# Step 1

Create

individual services.

```python id="fac2204"
class InventoryService:

    def reserve(self):
        print("Reserved")
```

```python id="fac2205"
class PaymentService:

    def collect(self):
        print("Collected")
```

```python id="fac2206"
class EmailService:

    def send(self):
        print("Email Sent")
```

______________________________________________________________________

# Step 2

Create

the Facade.

```python id="fac2207"
class BorrowFacade:

    def __init__(

        self,

        inventory,

        payment,

        email,

    ):

        self.inventory = inventory

        self.payment = payment

        self.email = email
```

______________________________________________________________________

# Step 3

Expose

one method.

```python id="fac2208"
class BorrowFacade:

    ...

    def borrow(self):

        self.inventory.reserve()

        self.payment.collect()

        self.email.send()

        print(
            "Borrow Complete"
        )
```

______________________________________________________________________

# Step 4

Use it.

```python id="fac2209"
facade.borrow()
```

The caller

doesn't know

about

Inventory,

Payment,

or Email.

______________________________________________________________________

# Real Backend Example

Suppose

an Order Service

needs to:

- Validate inventory
- Process payment
- Reserve stock
- Send confirmation
- Publish events

Instead of

calling

five services,

create

```text id="fac2210"
CheckoutFacade
```

Your endpoint becomes

```python id="fac2211"
checkout.borrow()
```

Simple.

______________________________________________________________________

# FastAPI Example

Bad

```python id="fac2212"
@app.post("/orders")

↓

Inventory

↓

Payment

↓

Notification

↓

Audit

↓

Cache
```

Better

```python id="fac2213"
@app.post("/orders")

↓

CheckoutFacade
```

The endpoint

becomes

clean

and readable.

______________________________________________________________________

# Microservices Example

Suppose

your API Gateway

receives

a request.

Internally,

it communicates with

- User Service
- Order Service
- Payment Service
- Shipping Service
- Notification Service

To the client,

it's just

one API.

The gateway

acts like

a Facade.

______________________________________________________________________

# AI/ML Example

Suppose

your AI pipeline

requires:

- Prompt validation
- Prompt templating
- LLM call
- Output parsing
- Moderation
- Logging
- Metrics

Instead of

calling

each component,

create

```text id="fac2214"
LLMFacade
```

Now,

your application

simply calls

```python id="fac2215"
llm.generate(prompt)
```

The facade

handles

everything else.

______________________________________________________________________

# Facade vs Adapter

This interview question

confuses many developers.

| Facade | Adapter |
| ----------------------- | ------------------------ |
| Simplifies a system | Converts an interface |
| Works with many objects | Usually wraps one object |
| Hides complexity | Translates compatibility |

Example

Facade

↓

"One button"

↓

Many services

Adapter

↓

Translate

Stripe API

↓

Your API

______________________________________________________________________

# Facade vs Factory

| Factory | Facade |
| ----------------------- | ------------------------ |
| Creates objects | Uses objects |
| Focuses on construction | Focuses on orchestration |

Factory answers:

> **What object should I create?**

Facade answers:

> **How do I use these objects together?**

______________________________________________________________________

# Benefits

Facade gives you:

✅ Simpler APIs

✅ Less coupling

✅ Easier testing

✅ Cleaner endpoints

✅ Better readability

______________________________________________________________________

# Drawbacks

Facade also introduces:

❌ One extra layer

❌ Can become a God Object

if too many responsibilities

are added.

______________________________________________________________________

# Common Mistake

Some developers

create

```python
ApplicationFacade
```

that performs

everything

in the system.

Eventually,

it becomes

another God Class.

Instead,

create

small facades

for

specific workflows.

Examples:

- CheckoutFacade
- BorrowFacade
- UserRegistrationFacade
- PaymentFacade

______________________________________________________________________

# Real Company Example

Suppose

Netflix

starts streaming

a movie.

Behind one click,

it performs:

- Authentication
- Recommendation lookup
- CDN selection
- DRM validation
- Analytics
- Billing
- Logging

The client

calls

one endpoint.

Internally,

many systems

work together.

This orchestration

is a Facade.

______________________________________________________________________

# When NOT to Use Facade

Don't create

a facade

if

the subsystem

already has

a simple interface.

Adding another layer

would provide

no value.

______________________________________________________________________

# Best Practices

✅ Keep facades workflow-oriented.

✅ Hide subsystem complexity.

✅ Keep business rules inside services.

✅ Let the facade orchestrate,

not own everything.

______________________________________________________________________

# Common Mistakes

### Turning Facade into Business Logic

The facade

coordinates.

It should not

contain

all business rules.

______________________________________________________________________

### Giant Facades

Create

multiple small facades,

not

one massive one.

______________________________________________________________________

### Confusing Facade with Service

A service

implements

business logic.

A facade

coordinates

multiple services.

______________________________________________________________________

### Using Facade Everywhere

Only introduce

a facade

when clients

must interact

with multiple subsystems.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Facade Pattern, and where is it commonly used?

The Facade Pattern is a structural design pattern that provides a simplified interface to a complex subsystem. Instead
of exposing multiple components directly to the client, a facade coordinates them behind a single, easy-to-use
interface. It is commonly used in backend applications to orchestrate workflows involving multiple services, such as
checkout, user registration, payment processing, and AI pipelines. API gateways are also real-world examples of the
Facade Pattern.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Facade Pattern is
- Why it exists
- Backend examples
- FastAPI example
- Microservices example
- AI/ML example
- Facade vs Adapter
- Facade vs Factory
- Best practices

______________________________________________________________________

# What's Next

[Command Pattern](23-command-pattern.md)

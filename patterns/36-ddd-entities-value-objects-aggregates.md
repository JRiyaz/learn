# Software Architecture - Part 36

# Domain-Driven Design (DDD): Entities, Value Objects & Aggregates

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What an Entity is
- What a Value Object is
- The difference between Entities and Value Objects
- What an Aggregate is
- What an Aggregate Root is
- Why Aggregates exist
- Real-world backend examples
- FastAPI examples
- AI/ML examples
- Common interview questions

______________________________________________________________________

# Before We Start

In the previous lesson,

we learned

that

DDD is about

modeling

the business.

Now,

we'll learn

the building blocks

used

to model

that business.

These concepts

appear

frequently

in senior backend

and system design

interviews.

______________________________________________________________________

# The Building Blocks

Tactical DDD

contains

many concepts.

Today,

we'll cover

the three

most important.

```text id="ddd3601"
Entity

↓

Value Object

↓

Aggregate
```

Almost every

DDD application

is built

using

these three.

______________________________________________________________________

# What is an Entity?

An **Entity**

is an object

that has

a unique identity.

Even if

its attributes

change,

it is still

the same object.

Identity

is what matters.

______________________________________________________________________

# Library Example

Suppose

we have

a book.

```python id="ddd3602"
Book

ID = 101

Title = Clean Code
```

Tomorrow,

someone updates

the title.

```python id="ddd3603"
Book

ID = 101

Title = Clean Code (2nd Edition)
```

Is it

the same book?

Yes.

Because

its identity

(ID)

did not change.

______________________________________________________________________

# Another Example

A library member

changes

their address.

```text id="ddd3604"
Before

↓

John

↓

Address A
```

Later

```text id="ddd3605"
John

↓

Address B
```

Same member.

Different address.

Identity

remains.

Therefore,

Member

is an Entity.

______________________________________________________________________

# Entity Example

```python id="ddd3606"
class Book:

    def __init__(

        self,

        book_id,

        title,

    ):

        self.id = book_id

        self.title = title
```

Notice

identity

comes first.

______________________________________________________________________

# What is a Value Object?

A **Value Object**

has

no identity.

Only

its values

matter.

Two Value Objects

with

the same values

are considered

equal.

______________________________________________________________________

# Example

Address

```text id="ddd3607"
Street

City

Country
```

Suppose

two people

live

at

the same address.

The address

doesn't need

an identity.

Only

its value

matters.

______________________________________________________________________

# Value Object Example

```python id="ddd3608"
from dataclasses import (
    dataclass,
)

@dataclass(frozen=True)
class Address:

    street: str

    city: str

    country: str
```

Notice

```python id="ddd3609"
frozen=True
```

Value Objects

should usually

be immutable.

______________________________________________________________________

# Why Immutable?

Suppose

an address changes.

Instead of

modifying

the existing object,

create

a new one.

Old

```text id="ddd3610"
Address A
```

↓

New

```text id="ddd3611"
Address B
```

This prevents

unexpected side effects.

______________________________________________________________________

# Entity vs Value Object

One of

the most common

interview questions.

| Entity | Value Object |
| ------------------ | ------------------------ |
| Has identity | No identity |
| Mutable | Usually immutable |
| Compared by ID | Compared by values |
| Represents a thing | Represents a description |

Examples

Entities

- Book
- Member
- Order
- User

Value Objects

- Address
- Money
- Date Range
- Coordinates

______________________________________________________________________

# What is an Aggregate?

Imagine

an Order.

It contains

```text id="ddd3612"
Order

↓

Order Items

↓

Shipping Address

↓

Payment
```

Should

other objects

directly modify

Order Items?

No.

Everything

should go

through

the Order.

This entire group

is called

an Aggregate.

______________________________________________________________________

# Aggregate

An Aggregate

is

a cluster

of related objects

treated

as

one unit.

The Aggregate

protects

business rules.

______________________________________________________________________

# Aggregate Root

Every Aggregate

has

one entry point.

This is

the

**Aggregate Root**.

Example

```text id="ddd3613"
Order

↓

Items

↓

Payment

↓

Shipment
```

Only

the Order

can be accessed

directly.

Everything else

is managed

through it.

______________________________________________________________________

# Library Example

Suppose

our domain

contains

```text id="ddd3614"
Loan

↓

Loan Items

↓

Fine
```

The Aggregate Root

is

```text id="ddd3615"
Loan
```

The application

shouldn't

modify

Loan Items

directly.

______________________________________________________________________

# Example

Bad

```python id="ddd3616"
loan_item.status = "RETURNED"
```

Good

```python id="ddd3617"
loan.return_item(
    item_id
)
```

The Loan

enforces

business rules.

______________________________________________________________________

# Why Aggregates?

Suppose

a loan

cannot contain

more than

10 books.

Where

should

that rule live?

Inside

Loan.

Not

inside

Loan Item.

The Aggregate Root

protects

business invariants.

______________________________________________________________________

# Business Invariants

An **Invariant**

is

a rule

that must

always

remain true.

Example

```text id="ddd3618"
Loan

↓

Maximum 10 Books
```

No matter

who calls

the application,

the rule

must never

be violated.

______________________________________________________________________

# FastAPI Example

Endpoint

↓

```python id="ddd3619"
loan.borrow_book()
```

Not

```python id="ddd3620"
loan.items.append(...)
```

The endpoint

always

works

through

the Aggregate Root.

______________________________________________________________________

# Repository and Aggregate

Repositories

should retrieve

Aggregates,

not

individual internal objects.

Example

```python id="ddd3621"
LoanRepository

↓

Loan Aggregate
```

Not

```python id="ddd3622"
LoanItemRepository
```

unless

LoanItem

is

its own Aggregate.

______________________________________________________________________

# AI/ML Example

Suppose

an AI Training Job.

```text id="ddd3623"
Training Job

↓

Datasets

↓

Metrics

↓

Model Version
```

The Aggregate Root

is

```text id="ddd3624"
Training Job
```

Business rules

such as

"Only one active training run"

belong

inside

the Training Job.

______________________________________________________________________

# Another Example

Bank Account.

```text id="ddd3625"
Account

↓

Transactions
```

Should

transactions

change

the balance

directly?

No.

The Account

controls

all balance updates.

Account

is

the Aggregate Root.

______________________________________________________________________

# Aggregate vs Database Table

A common misconception.

An Aggregate

is **not**

a database table.

One Aggregate

may involve

multiple tables.

Conversely,

one table

may contain

multiple aggregates

depending

on the domain.

DDD models

the business,

not

the schema.

______________________________________________________________________

# Aggregate Size

A common mistake

is creating

very large aggregates.

Bad

```text id="ddd3626"
Company

↓

Departments

↓

Employees

↓

Projects

↓

Payroll

↓

Benefits

↓

Assets
```

This aggregate

would be

too large.

Instead,

split it

into

multiple aggregates.

______________________________________________________________________

# Benefits

DDD building blocks

provide:

✅ Better business modeling

✅ Protected business rules

✅ Clear ownership

✅ Easier maintenance

✅ Better consistency

______________________________________________________________________

# Drawbacks

They also introduce:

❌ More modeling effort

❌ More classes

❌ Higher learning curve

______________________________________________________________________

# Real Company Example

Suppose

an airline.

Aggregate

```text id="ddd3627"
Flight

↓

Passengers

↓

Seats
```

Only

the Flight

can assign

a seat.

A Passenger

cannot

change

its seat

independently.

This guarantees

business consistency.

______________________________________________________________________

# When NOT to Use Aggregates

Don't create

Aggregates

for

simple CRUD data.

Example

```text id="ddd3628"
Country

Currency

Language
```

These

may simply

be lookup data.

No complex

business rules

exist.

______________________________________________________________________

# Best Practices

✅ Give every Entity a stable identity.

✅ Make Value Objects immutable.

✅ Keep Aggregates small.

✅ Protect business invariants inside the Aggregate Root.

______________________________________________________________________

# Common Mistakes

### IDs for Everything

Not every object

needs

an ID.

Only

Entities

require identity.

______________________________________________________________________

### Mutable Value Objects

Changing

shared Value Objects

can introduce

subtle bugs.

Prefer immutability.

______________________________________________________________________

### Bypassing the Aggregate Root

Never modify

internal entities

directly.

Always

go through

the Aggregate Root.

______________________________________________________________________

### Giant Aggregates

Large aggregates

cause

performance issues,

locking problems,

and

complexity.

Design

small,

cohesive aggregates.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between an Entity, a Value Object, and an Aggregate in DDD?

An Entity is an object with a unique identity that remains the same even when its attributes change, such as a User or
Order. A Value Object has no identity and is defined entirely by its values, such as an Address or Money; it is
typically immutable. An Aggregate is a cluster of related domain objects treated as a single consistency boundary, with
one Aggregate Root acting as the only entry point for modifications. The Aggregate Root enforces business invariants and
protects the integrity of the entire aggregate.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What an Entity is
- What a Value Object is
- Entity vs Value Object
- What an Aggregate is
- Aggregate Root
- Business Invariants
- FastAPI example
- AI/ML example
- Best practices

______________________________________________________________________

# 🧠 DDD Progress

You now understand the core building blocks of Tactical DDD:

- ✅ Entities
- ✅ Value Objects
- ✅ Aggregates
- ✅ Aggregate Roots

Next, we'll cover **Domain Events**, which are one of the most powerful concepts in modern backend systems and a key
building block for Event-Driven Architecture and Microservices.

______________________________________________________________________

# What's Next

[Domain Events](37-domain-events.md)

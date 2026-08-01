# Software Design & Design Patterns - Part 27

# State Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the State Pattern is
- Why the State Pattern exists
- The problem it solves
- State transitions
- Finite State Machines (FSM)
- Real-world backend examples
- FastAPI examples
- Workflow engine examples
- When NOT to use the State Pattern

______________________________________________________________________

# Before We Start

Imagine

an online library.

A borrowed book

can be in

one of these states.

```text id="state2701"
Available

↓

Reserved

↓

Borrowed

↓

Returned

↓

Available
```

The actions

allowed

depend

on

the current state.

For example,

can you

return

a book

that is

already available?

No.

Can you

borrow

a lost book?

No.

Behavior

depends

on state.

______________________________________________________________________

# The Problem

A developer writes

the following.

```python id="state2702"
class Book:

    def borrow(self):

        if self.status == "AVAILABLE":

            self.status = "BORROWED"
```

Everything works.

______________________________________________________________________

# Another Requirement

Now

support

more states.

- Reserved
- Lost
- Damaged
- Under Repair

The code grows.

```python id="state2703"
if status == "AVAILABLE":
    ...

elif status == "BORROWED":
    ...

elif status == "RESERVED":
    ...

elif status == "LOST":
    ...

elif status == "DAMAGED":
    ...

elif status == "REPAIR":
    ...
```

______________________________________________________________________

# Another Method

Now

implement

```python id="state2704"
return_book()
```

Again,

another huge

`if-elif`.

Soon,

every method

checks

the state.

______________________________________________________________________

# What's the Problem?

The object

contains

too many

conditional statements.

Problems:

❌ Difficult maintenance

❌ Duplicated state logic

❌ Hard to add new states

❌ Violates OCP

______________________________________________________________________

# The Idea

Instead of

asking

which state

the object

is in,

let

the current state

decide

what happens.

Each state

becomes

its own class.

______________________________________________________________________

# What is the State Pattern?

The **State Pattern** says:

> **Allow an object to alter its behavior when its internal state changes.**

Instead of

large conditionals,

delegate

behavior

to

state objects.

______________________________________________________________________

# Without State Pattern

```text id="state2705"
Book

↓

if status

↓

if status

↓

if status
```

______________________________________________________________________

# With State Pattern

```text id="state2706"
Book

↓

Current State

↓

BorrowState

↓

ReturnState

↓

ReservedState
```

The object

delegates

behavior

to

its state.

______________________________________________________________________

# Step 1

Create

the abstraction.

```python id="state2707"
from abc import (
    ABC,
    abstractmethod,
)

class BookState(
    ABC
):

    @abstractmethod
    def borrow(
        self,
        book,
    ):
        ...
```

______________________________________________________________________

# Step 2

Available State.

```python id="state2708"
class AvailableState(
    BookState
):

    def borrow(
        self,
        book,
    ):

        print(
            "Borrowed"
        )

        book.state = BorrowedState()
```

Notice

the state

changes itself.

______________________________________________________________________

# Step 3

Borrowed State.

```python id="state2709"
class BorrowedState(
    BookState
):

    def borrow(
        self,
        book,
    ):

        raise Exception(
            "Already Borrowed"
        )
```

______________________________________________________________________

# Step 4

Book Context.

```python id="state2710"
class Book:

    def __init__(self):

        self.state = AvailableState()

    def borrow(self):

        self.state.borrow(
            self
        )
```

______________________________________________________________________

# Using It

```python id="state2711"
book = Book()

book.borrow()
```

Output

```text id="state2712"
Borrowed
```

Call

```python id="state2713"
book.borrow()
```

again,

and

the behavior

changes automatically.

No

`if-elif`

required.

______________________________________________________________________

# State Transitions

A state

can move

to another state.

Example

```text id="state2714"
Available

↓

Borrowed

↓

Returned

↓

Available
```

This forms

a

**Finite State Machine (FSM).**

______________________________________________________________________

# Real Backend Example

Suppose

an order

has

these states.

```text id="state2715"
Created

↓

Paid

↓

Packed

↓

Shipped

↓

Delivered
```

The actions

available

depend

on

the current state.

For example,

only

a

Paid Order

can be packed.

______________________________________________________________________

# Payment Example

A payment

might be

```text id="state2716"
Pending

↓

Authorized

↓

Captured

↓

Refunded

↓

Failed
```

Instead of

large

conditional statements,

each payment state

implements

its own behavior.

______________________________________________________________________

# FastAPI Example

Suppose

your endpoint

changes

an order status.

Instead of

```python id="state2717"
if status == ...
```

delegate

to

the current state.

Business rules

remain

inside

the state classes.

______________________________________________________________________

# AI/ML Example

Suppose

an ML job

moves through

these stages.

```text id="state2718"
Queued

↓

Running

↓

Completed

↓

Archived
```

Each state

allows

different operations.

For example,

only

Running

jobs

can be cancelled.

______________________________________________________________________

# Workflow Engines

Workflow engines

such as:

- Airflow
- Temporal
- Camunda

manage

state transitions

between

workflow steps.

Although

their implementations

are more advanced,

the underlying idea

is closely related

to the State Pattern.

______________________________________________________________________

# State vs Strategy

This interview question

is extremely common.

| State | Strategy |
| ------------------------------ | -------------------------- |
| Behavior changes automatically | Behavior chosen externally |
| Internal state decides | Caller decides |
| Represents lifecycle | Represents algorithms |

Example

Strategy

↓

Choose

Stripe

or

PayPal

State

↓

Order

becomes

Paid

then

Shipped

______________________________________________________________________

# State vs Finite State Machine

The State Pattern

is often used

to implement

Finite State Machines.

FSM

defines

the states

and transitions.

State Pattern

implements

the behavior

for each state.

______________________________________________________________________

# Benefits

State gives you:

✅ Eliminates large conditionals

✅ Easy to add states

✅ Cleaner business logic

✅ Better extensibility

______________________________________________________________________

# Drawbacks

It also introduces:

❌ More classes

❌ More objects

❌ More abstraction

for simple workflows.

______________________________________________________________________

# Real Company Example

Suppose

Uber

tracks

a ride.

```text id="state2719"
Requested

↓

Accepted

↓

Driver Arriving

↓

In Progress

↓

Completed
```

Each state

allows

different actions.

For example,

only

an

Accepted Ride

can be cancelled

by the driver.

______________________________________________________________________

# When NOT to Use State

Suppose

an object

has

only

two simple states.

```text id="state2720"
ON

OFF
```

Using

multiple classes

would likely

be unnecessary.

Simple

conditional logic

may be enough.

______________________________________________________________________

# Best Practices

✅ One class per state.

✅ Let states manage transitions.

✅ Keep state-specific rules inside state classes.

✅ Avoid exposing transition logic everywhere.

______________________________________________________________________

# Common Mistakes

### Giant State Classes

Each state

should represent

one state only.

______________________________________________________________________

### State Logic Inside Context

If

the context

contains

many

`if-elif`

checks,

the pattern

isn't being used effectively.

______________________________________________________________________

### Invalid Transitions

Prevent

illegal transitions,

such as

moving directly

from

Created

to

Delivered.

______________________________________________________________________

### Confusing State with Strategy

Remember

Strategy

is selected

by the caller.

State

changes

during

the object's lifecycle.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the State Pattern, and where is it commonly used?

The State Pattern is a behavioral design pattern that allows an object to change its behavior as its internal state
changes. Instead of relying on large conditional statements, each state is represented by its own class, and the current
state determines how operations behave. The pattern is commonly used in workflow engines, order processing, payment
processing, document lifecycles, job schedulers, and finite state machines where valid operations depend on the current
state.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the State Pattern is
- Why it exists
- State transitions
- Finite State Machines
- Backend examples
- FastAPI example
- Workflow engine example
- State vs Strategy
- Best practices

______________________________________________________________________

# What's Next

[Mediator Pattern](28-mediator-pattern.md)

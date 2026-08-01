# Software Design & Design Patterns - Part 07

# SOLID Principles Overview

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What SOLID is
- Why SOLID was introduced
- The problems SOLID solves
- The five SOLID principles
- How SOLID relates to Design Patterns
- How SOLID is used in FastAPI and backend development
- Why every senior backend engineer should know SOLID

______________________________________________________________________

# The Problem

Let's continue with our **Library Management System**.

Initially, your application only supports creating books.

A developer writes:

```python id="solid0701"
class LibraryService:

    def create_book(
        self,
        book,
    ):
        print("Book Created")
```

Simple.

Everything is fine.

______________________________________________________________________

# Six Months Later...

The application grows.

New requirements arrive.

- Update books
- Delete books
- Borrow books
- Return books
- Calculate fines
- Generate reports
- Export CSV
- Send emails
- Send SMS
- Process payments
- Log activities
- Update cache
- Publish Kafka events

The developer keeps adding methods.

______________________________________________________________________

# The Result

```python id="solid0702"
class LibraryService:

    def create_book(self):
        ...

    def update_book(self):
        ...

    def delete_book(self):
        ...

    def send_email(self):
        ...

    def send_sms(self):
        ...

    def process_payment(self):
        ...

    def generate_report(self):
        ...

    def export_csv(self):
        ...

    def publish_event(self):
        ...

    def update_cache(self):
        ...
```

______________________________________________________________________

# What's the Problem?

One class

is now responsible for:

- Books
- Notifications
- Payments
- Reports
- Cache
- Events
- Logging

Problems:

❌ Difficult to understand

❌ Difficult to maintain

❌ Difficult to test

❌ Difficult to extend

❌ Bugs appear frequently

This is commonly known as a

**God Class**.

______________________________________________________________________

# Why Does This Happen?

As software grows,

developers naturally keep adding code

to existing classes.

Over time,

those classes become responsible

for everything.

The application still works,

but changing it becomes risky.

______________________________________________________________________

# The Solution

Experienced software engineers

faced these problems

for decades.

They realized that

well-designed software

followed a common set of principles.

Those principles became known as

**SOLID**.

______________________________________________________________________

# What is SOLID?

SOLID is a collection of

**five software design principles**

that help developers build software that is:

- Easy to maintain
- Easy to extend
- Easy to test
- Easy to understand

Notice something important.

SOLID is **not**:

- A framework
- A library
- A Python feature

It is simply

a set of design principles.

______________________________________________________________________

# What Does SOLID Stand For?

```text id="solid0703"
S → Single Responsibility Principle

O → Open/Closed Principle

L → Liskov Substitution Principle

I → Interface Segregation Principle

D → Dependency Inversion Principle
```

We'll study

each principle

in detail

over the next five lessons.

______________________________________________________________________

# Think About a Hospital

Imagine

one doctor

trying to do everything.

- Heart surgery
- Eye surgery
- Dentistry
- Pediatrics
- Radiology

Would that scale?

No.

Hospitals have specialists.

Software should too.

Each class

should have

a focused responsibility.

This idea

appears repeatedly

throughout SOLID.

______________________________________________________________________

# Why Backend Engineers Need SOLID

Backend applications

rarely stay the same.

Today

you support

Stripe.

Tomorrow

Razorpay.

Next month

PayPal.

Then

Apple Pay.

Business requirements

change constantly.

SOLID helps

your code evolve

without becoming chaotic.

______________________________________________________________________

# SOLID and Design Patterns

Design patterns

are built

using SOLID principles.

For example:

| Pattern | SOLID Principle Used |
| -------------------- | -------------------- |
| Strategy | OCP, DIP |
| Factory | OCP, DIP |
| Repository | SRP, DIP |
| Decorator | OCP |
| Observer | OCP |
| Dependency Injection | DIP |

This is why

we're learning SOLID

before design patterns.

______________________________________________________________________

# SOLID in FastAPI

Suppose you have

an endpoint.

```python id="solid0704"
@app.post("/borrow")
def borrow_book():
    ...
```

Inside,

you shouldn't:

- Save the database
- Send emails
- Process payments
- Log everything
- Publish Kafka events

Instead,

the endpoint should

coordinate

specialized services.

This is exactly

what SOLID encourages.

______________________________________________________________________

# Does SOLID Mean More Classes?

A common misconception.

Some developers think

SOLID means

creating

dozens of classes.

That's incorrect.

SOLID means

creating

the **right responsibilities**.

Sometimes

one class

is enough.

Sometimes

ten classes

are justified.

______________________________________________________________________

# Does Every Project Need SOLID?

No.

Suppose you're writing

a script

to convert CSV to JSON.

Using

Repository,

Factory,

Strategy,

and Dependency Injection

would be unnecessary.

SOLID becomes valuable when:

- The project is large
- The project will evolve
- Multiple developers work together
- The application lives for years

Most backend systems

meet these conditions.

______________________________________________________________________

# A Quick Overview

## S

One class.

One responsibility.

______________________________________________________________________

## O

Extend behavior

without modifying

existing code.

______________________________________________________________________

## L

Child classes

should work

where parent classes

are expected.

______________________________________________________________________

## I

Don't force classes

to implement methods

they don't need.

______________________________________________________________________

## D

Depend on abstractions,

not concrete implementations.

We'll learn

each one

with real backend examples.

______________________________________________________________________

# Throughout the Next Lessons

For every SOLID principle,

we'll follow

the same approach.

```text id="solid0705"
Real Problem

↓

Bad Code

↓

Problems

↓

SOLID Principle

↓

Refactored Code

↓

FastAPI Example

↓

Interview Question
```

We'll never

learn a principle

without first understanding

the problem

it solves.

______________________________________________________________________

# Best Practices

✅ Apply SOLID gradually.

✅ Let business requirements drive your design.

✅ Keep classes focused.

✅ Prefer maintainability over clever code.

✅ Use SOLID to simplify code, not complicate it.

______________________________________________________________________

# Common Mistakes

### Memorizing SOLID

Understanding the acronym

isn't enough.

Understand

the problem

behind each principle.

______________________________________________________________________

### Applying SOLID Everywhere

Small scripts

don't need

enterprise architecture.

______________________________________________________________________

### Creating Classes Without Purpose

More classes

don't automatically mean

better software.

______________________________________________________________________

### Ignoring Simplicity

SOLID should make

your software

easier,

not harder,

to understand.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What are the SOLID principles, and why are they important?

SOLID is a set of five object-oriented design principles that help developers create software that is maintainable,
extensible, testable, and easy to understand. The principles encourage focused responsibilities, extensible designs,
proper inheritance, small interfaces, and dependency on abstractions instead of concrete implementations. Together, they
reduce coupling, improve flexibility, and form the foundation of many modern design patterns used in backend
development.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What SOLID is
- Why it exists
- The five principles
- How SOLID relates to design patterns
- FastAPI examples
- Why backend engineers rely on SOLID

______________________________________________________________________

# What's Next

[Single Responsibility Principle (SRP)](08-single-responsibility-principle.md)

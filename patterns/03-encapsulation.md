# Software Design & Design Patterns - Part 03

# Encapsulation

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Encapsulation is
- Why Encapsulation exists
- The problems it solves
- How to protect object state
- Python's approach to encapsulation
- Real-world backend examples
- FastAPI examples
- When to use Encapsulation
- When NOT to use it

______________________________________________________________________

# The Problem

Let's continue with our **Library Management System**.

We have a `Book` object.

A junior developer writes:

```python
class Book:

    def __init__(self, title):
        self.title = title
        self.available = True
```

Somewhere else in the application...

```python
book = Book("Clean Code")

book.available = False
```

Another developer writes:

```python
book.available = "YES"
```

Another one writes:

```python
book.available = 100
```

Someone even writes:

```python
book.available = None
```

The application still runs.

But now your data is inconsistent.

______________________________________________________________________

# What's the Problem?

Every developer

can directly modify

the internal state

of the object.

Nothing prevents someone from writing invalid data.

Your object has

**no control**

over itself.

______________________________________________________________________

# Imagine a Bank Account

Suppose you have

```python
account.balance = 1000
```

What happens if someone writes

```python
account.balance = -500000
```

Or

```python
account.balance = "One Million"
```

Should that be allowed?

Of course not.

The object should decide

how its own data changes.

______________________________________________________________________

# This Is Encapsulation

Encapsulation means:

> **Keep an object's data together with the rules that modify it.**

Instead of allowing anyone

to change data directly,

provide controlled methods.

______________________________________________________________________

# Better Design

Instead of

```python
book.available = False
```

write

```python
book.borrow()
```

Instead of

```python
book.available = True
```

write

```python
book.return_book()
```

Now the object decides

what is allowed.

______________________________________________________________________

# Refactored Code

```python
class Book:

    def __init__(self, title):
        self.title = title
        self.available = True

    def borrow(self):

        if not self.available:
            raise Exception(
                "Book already borrowed."
            )

        self.available = False

    def return_book(self):
        self.available = True
```

Now,

nobody can accidentally

change the book's state

without using

the correct business logic.

______________________________________________________________________

# Another Real Example

Suppose you're building

a payment system.

Bad

```python
payment.status = "SUCCESS"
```

Any developer

can mark

a failed payment

as successful.

______________________________________________________________________

# Better

```python
payment.mark_successful()
```

Inside the method,

you can:

- Validate the payment
- Write audit logs
- Notify users
- Update metrics

The caller doesn't need

to know

these internal steps.

______________________________________________________________________

# Python and Encapsulation

Languages like Java

provide keywords such as

```text
private

protected

public
```

Python is different.

Python follows the philosophy:

> "We are all responsible developers."

Instead of strict access control,

Python uses

**naming conventions**.

______________________________________________________________________

# Public Attributes

```python
class Book:

    def __init__(self):
        self.title = "Clean Code"
```

Accessible everywhere.

______________________________________________________________________

# Protected Attributes

Convention:

```python
self._title
```

The single underscore means:

> "This is an internal attribute. Please don't access it directly."

Python doesn't stop you,

but other developers understand

it shouldn't be modified casually.

______________________________________________________________________

# Private Attributes

Convention:

```python
self.__balance
```

Double underscores trigger

**name mangling**.

Example

```python
class Account:

    def __init__(self):
        self.__balance = 100
```

This becomes internally

something similar to

```python
_Account__balance
```

It makes accidental access harder,

although it isn't true security.

______________________________________________________________________

# Properties

Sometimes,

you want to allow reading

but control writing.

Example

```python
class Book:

    def __init__(self):
        self._copies = 5

    @property
    def copies(self):
        return self._copies
```

The caller writes

```python
print(book.copies)
```

without knowing

how the value

is stored internally.

______________________________________________________________________

# Setter Example

```python
class Book:

    def __init__(self):
        self._copies = 5

    @property
    def copies(self):
        return self._copies

    @copies.setter
    def copies(self, value):

        if value < 0:
            raise ValueError(
                "Copies cannot be negative."
            )

        self._copies = value
```

Now

```python
book.copies = -5
```

raises an error.

The object protects itself.

______________________________________________________________________

# FastAPI Example

Suppose an endpoint

updates a user's role.

Bad

```python
user.role = "ADMIN"
```

Better

```python
user.promote_to_admin()
```

Inside,

the object can:

- Verify permissions
- Log the change
- Update audit records
- Send notifications

The endpoint

doesn't need

to know

those details.

______________________________________________________________________

# SQLAlchemy Example

When using SQLAlchemy,

developers often encapsulate

business rules

inside model methods

or service classes

instead of letting

every endpoint

modify database objects directly.

This keeps the rules

in one place.

______________________________________________________________________

# Encapsulation Is Not About Hiding Everything

A common misconception is:

> "Every variable must be private."

Not true.

Only protect data

that must remain valid.

Simple data

doesn't always need

special protection.

______________________________________________________________________

# When NOT to Use Encapsulation

Don't create

getter and setter methods

for every variable

without a reason.

Bad

```python
user.get_name()

user.set_name()
```

If there is

no validation,

a normal public attribute

is often simpler

and more Pythonic.

______________________________________________________________________

# Best Practices

✅ Protect important business state.

✅ Expose meaningful methods.

✅ Keep validation inside the object.

✅ Use properties when validation is required.

✅ Follow Python naming conventions.

______________________________________________________________________

# Common Mistakes

### Making Everything Public

Critical business data

should not be freely modified.

______________________________________________________________________

### Making Everything Private

Python encourages simplicity.

Protect only what needs protection.

______________________________________________________________________

### Duplicating Validation

Validation should live

inside the object,

not in every endpoint

or service.

______________________________________________________________________

### Using Getters and Setters Everywhere

Unlike Java,

Python favors properties

and direct attribute access

when no validation is needed.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Encapsulation, and how is it implemented in Python?

Encapsulation is the practice of keeping an object's data together with the methods that operate on it, ensuring that
the object's internal state can only be modified through controlled behavior. This helps maintain valid business rules
and prevents inconsistent data. Python implements encapsulation primarily through naming conventions (`_protected`,
`__private`) and the `@property` decorator, allowing developers to expose a clean interface while controlling access and
validation.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Encapsulation is
- Why it exists
- Public, protected, and private attributes
- Properties and setters
- Backend examples
- FastAPI example
- When to use it
- When not to use it

______________________________________________________________________

# What's Next

[Inheritance](04-inheritance.md)

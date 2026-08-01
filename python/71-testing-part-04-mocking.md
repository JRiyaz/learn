# File: python/71-testing-part-04-mocking.md

# Testing

# Part 4: Mocking – Isolating External Dependencies in Tests

> **Course:** Backend Engineering Roadmap
>
> **Module:** Testing
>
> **Lesson:** 71
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 12–14 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What mocking is
- Why mocking is necessary
- Test doubles
- Mocks vs Stubs vs Fakes vs Spies
- The `unittest.mock` module
- `Mock`
- `MagicMock`
- `patch()`
- Mocking return values
- Mocking exceptions
- Verifying interactions
- Common mistakes
- Production best practices

______________________________________________________________________

# Recap

In the previous lesson, we learned how fixtures help us reuse test setup.

However, fixtures don't solve another important problem.

Suppose we want to test:

```python
class PaymentService:

    def charge(self, amount):

        ...
```

Internally it calls:

- Stripe
- Database
- Email service
- Redis

Running a unit test should **not**:

- Charge a real credit card
- Send a real email
- Modify a real database
- Call an external API

Instead, we replace those dependencies with fake objects.

This technique is called **mocking**.

______________________________________________________________________

# What is Mocking?

Mocking is the practice of replacing a real dependency with a controllable object during testing.

Instead of:

```
Test

↓

Real Database
```

we use:

```
Test

↓

Mock Database
```

The application behaves as though the dependency exists, but nothing external actually happens.

______________________________________________________________________

# Why Mock?

Consider this function:

```python
def send_invoice():

    email_service.send()
```

Without mocking:

```
Run Test

↓

Send Real Email
```

Problems:

- Slow
- Expensive
- Difficult to reproduce
- Depends on external systems

With mocking:

```
Run Test

↓

Pretend Email Was Sent
```

The test becomes:

- Fast
- Deterministic
- Independent

______________________________________________________________________

# Unit Tests Should Be Isolated

A unit test should verify **one unit of behaviour**.

It should not fail because:

- PostgreSQL is unavailable
- Redis is down
- The network is slow
- Stripe has an outage

External systems belong in integration tests.

______________________________________________________________________

# Test Doubles

"Test Double" is the general term for objects that replace real dependencies.

```
Test Double

├── Dummy
├── Stub
├── Fake
├── Spy
└── Mock
```

Each serves a different purpose.

______________________________________________________________________

# Dummy

A dummy object exists only because an argument is required.

Example:

```python
def save_user(

    repository,

    logger

):
    ...
```

If the logger isn't relevant:

```python
logger = object()
```

It satisfies the interface but is never used.

______________________________________________________________________

# Stub

A stub returns predefined values.

```python
class StubRepository:

    def get_user(

        self,

        user_id

    ):

        return {

            "id": user_id,

            "name": "Alice"

        }
```

The behaviour never changes.

______________________________________________________________________

# Fake

A fake contains a simplified implementation.

Example:

```python
class FakeRepository:

    def __init__(self):

        self.users = {}

    def save(

        self,

        user

    ):

        self.users[user["id"]] = user
```

Unlike a stub, it contains working logic.

In-memory databases are common examples.

______________________________________________________________________

# Spy

A spy records interactions.

Example:

```
Was send_email() called?

↓

How many times?

↓

With what arguments?
```

Spies help verify behaviour.

______________________________________________________________________

# Mock

A mock both:

- Simulates behaviour
- Verifies interactions

It can answer questions such as:

- Was this method called?
- How many times?
- With which arguments?

______________________________________________________________________

# unittest.mock

Python's standard mocking library:

```python
from unittest.mock import Mock
```

______________________________________________________________________

# Creating a Mock

```python
from unittest.mock import Mock


database = Mock()
```

Calling:

```python
database.save()
```

does nothing.

No exception.

No database.

Just a mock object.

______________________________________________________________________

# Returning Values

Example:

```python
repository = Mock()

repository.get_user.return_value = {

    "id": 1,

    "name": "Alice"
}
```

Now:

```python
repository.get_user(1)
```

returns:

```python
{

    "id": 1,

    "name": "Alice"
}
```

without executing any real code.

______________________________________________________________________

# Raising Exceptions

Mocks can simulate failures.

```python
repository = Mock()

repository.save.side_effect = RuntimeError(

    "Database unavailable"

)
```

Calling:

```python
repository.save()
```

raises the configured exception.

This allows error handling to be tested safely.

______________________________________________________________________

# Verifying Calls

Suppose:

```python
email.send(
    "alice@example.com"
)
```

Test:

```python
email.send.assert_called_once()
```

Verify arguments:

```python
email.send.assert_called_once_with(

    "alice@example.com"

)
```

These assertions ensure the interaction occurred as expected.

______________________________________________________________________

# MagicMock

`MagicMock` extends `Mock`.

It automatically supports Python magic methods.

Example:

```python
from unittest.mock import MagicMock


cache = MagicMock()

len(cache)
```

works without additional configuration.

Use `MagicMock` when mocking objects that behave like containers, iterators, or context managers.

______________________________________________________________________

# patch()

Often the code creates dependencies internally.

Example:

```python
service = EmailService()
```

Instead of modifying the source code, temporarily replace it.

```python
from unittest.mock import patch
```

Example:

```python
with patch(

    "app.email.EmailService"

):

    ...
```

During the block:

```
Real Object

↓

Mock Object
```

Afterwards:

```
Original Object Restored
```

______________________________________________________________________

# Where to Patch

This is one of the most common sources of confusion.

Suppose:

```python
# email.py

class EmailService:

    ...
```

```python
# users.py

from email import EmailService
```

When testing:

```python
users.EmailService
```

should be patched.

**Patch where the object is looked up, not where it was originally defined.**

______________________________________________________________________

# Backend Example

```python
class UserService:

    def register(

        self,

        email

    ):

        self.email_service.send(

            email

        )
```

Test:

```python
from unittest.mock import Mock


email = Mock()

service = UserService(

    email
)

service.register(

    "alice@example.com"

)

email.send.assert_called_once_with(

    "alice@example.com"

)
```

No real email is sent.

The behaviour is verified.

______________________________________________________________________

# Mocking Multiple Dependencies

```
UserService

↓

Repository (Mock)

↓

Email (Mock)

↓

Logger (Mock)
```

Each dependency is controlled independently.

The test focuses only on `UserService`.

______________________________________________________________________

# Over-Mocking

Avoid mocking everything.

Bad:

```
Service

↓

Repository (Mock)

↓

Database Driver (Mock)

↓

Socket (Mock)

↓

OS (Mock)
```

At this point, the test may no longer represent realistic behaviour.

Mock only external dependencies that are outside the unit under test.

______________________________________________________________________

# Mock vs Fake

Example:

Fake:

```python
FakeRepository()

↓

Actually Stores Data
```

Mock:

```python
Mock()

↓

Only Pretends
```

Choose the approach that best fits the behaviour you need to verify.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Mocking the class being tested.

Only mock its dependencies.

______________________________________________________________________

## Mistake 2

Patching the wrong import location.

______________________________________________________________________

## Mistake 3

Verifying implementation details instead of behaviour.

______________________________________________________________________

## Mistake 4

Creating overly complicated mock configurations.

______________________________________________________________________

## Mistake 5

Using mocks instead of integration tests for verifying external systems.

______________________________________________________________________

# Best Practices

✅ Mock external dependencies.

✅ Keep mocks simple.

✅ Verify observable behaviour.

✅ Prefer dependency injection over excessive patching.

✅ Use fakes when realistic behaviour is beneficial.

❌ Don't mock Python itself.

❌ Don't test the mocking library.

______________________________________________________________________

# Production Insight

Large backend services commonly depend on:

- PostgreSQL
- Redis
- Kafka
- Payment gateways
- Object storage
- Email providers

Unit tests replace these dependencies with mocks.

Integration tests then verify communication with the real systems.

This separation keeps unit tests fast while ensuring production integrations are also validated.

______________________________________________________________________

# Questions

### Question

> What is mocking?

### Answer

Mocking replaces a real dependency with a controllable object during testing.

______________________________________________________________________

### Question

> Why should external services be mocked in unit tests?

### Answer

To keep tests fast, deterministic, and independent of network or infrastructure failures.

______________________________________________________________________

### Question

> What is the difference between a fake and a mock?

### Answer

A fake contains a simplified working implementation, while a mock primarily simulates behaviour and records
interactions.

______________________________________________________________________

### Question

> When should `patch()` be used?

### Answer

When the code under test creates or looks up dependencies that cannot easily be injected.

______________________________________________________________________

### Question

> Why is "patch where the object is looked up" important?

### Answer

Because Python uses the imported reference within the module under test. Patching the original definition may not affect
the object actually being used.

______________________________________________________________________

# Practical Lesson

Create:

```text
app/

├── email.py

├── user_service.py

└── tests/

    └── test_user_service.py
```

Implement:

- `EmailService`
- `UserService`

Write tests that:

- Replace `EmailService` with a `Mock`.
- Verify `send()` is called once.
- Verify the correct email address is used.
- Simulate an exception from `send()`.
- Confirm `UserService` handles the failure correctly.

Then create a second version using `patch()` instead of constructor injection and compare the two approaches.

______________________________________________________________________

# Knowledge Check

## Question 1

Why are mocks valuable in unit testing?

### Answer

They isolate the unit under test from external systems, making tests fast, reliable, and deterministic.

______________________________________________________________________

## Question 2

When should a fake be preferred over a mock?

### Answer

When a lightweight working implementation better represents the dependency, such as an in-memory repository used across
many tests.

______________________________________________________________________

## Question 3

What is the biggest advantage of dependency injection when using mocks?

### Answer

Dependencies can be replaced directly without relying on runtime patching, resulting in simpler and more explicit tests.

______________________________________________________________________

## Question 4

Why can excessive mocking become a problem?

### Answer

Over-mocked tests may verify implementation details instead of behaviour, making them brittle and reducing confidence in
real-world behaviour.

______________________________________________________________________

## Question 5

How should unit and integration tests divide responsibilities?

### Answer

Unit tests mock external systems to verify business logic, while integration tests verify that the application
communicates correctly with real external services.

______________________________________________________________________

# Assignment

## Exercise 1

Take one service from your Flask or FastAPI project.

Replace its repository with a `Mock` and verify all expected interactions.

______________________________________________________________________

## Exercise 2

Write tests that simulate:

- Successful API call.
- Network timeout.
- Database failure.
- Email sending failure.

Use `side_effect` where appropriate.

______________________________________________________________________

## Exercise 3

Create an in-memory fake repository and compare the readability of tests using a fake versus a mock.

Document when each approach is preferable.

______________________________________________________________________

## Exercise 4

Review one of your existing test suites.

Identify every use of `patch()`.

For each case, determine whether constructor injection could replace patching and simplify the test.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What mocking is.
- ✅ Why unit tests use mocks.
- ✅ Test doubles (dummy, stub, fake, spy, mock).
- ✅ `Mock` and `MagicMock`.
- ✅ `return_value` and `side_effect`.
- ✅ Verifying interactions.
- ✅ `patch()`.
- ✅ The importance of patching the correct location.
- ✅ Production mocking best practices.

______________________________________________________________________

# Next Lesson

**File:** [72-testing-part-05-monkeypatch](72-testing-part-05-monkeypatch.md)

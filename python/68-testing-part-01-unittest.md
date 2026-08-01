# File: python/67-testing-part-01-unittest.md

# Testing

# Part 1: unittest – Writing Reliable Automated Tests in Python

> **Course:** Backend Engineering Roadmap
>
> **Module:** Testing
>
> **Lesson:** 68
>
> **Difficulty:** ⭐⭐⭐☆☆
>
> **Estimated Time:** 8–10 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why automated testing is important
- Types of software testing
- Test pyramid
- Unit testing fundamentals
- The `unittest` module
- Test cases
- Assertions
- Test lifecycle
- Test discovery
- Best practices
- Common mistakes

______________________________________________________________________

# Recap

So far, we've focused on writing production-quality Python applications.

But writing good code is only half the job.

The next question is:

> **How do we know our code still works after making changes?**

Imagine a simple function:

```python
def add(a, b):
    return a + b
```

Today it works correctly.

Tomorrow another developer changes it to:

```python
def add(a, b):
    return a - b
```

The code still runs.

No syntax errors.

No exceptions.

But the behaviour is now incorrect.

Testing helps us detect these regressions automatically.

______________________________________________________________________

# What is Testing?

Testing is the process of verifying that software behaves as expected.

Instead of manually checking every feature after each change, we write programs that test other programs.

```
Source Code

↓

Test

↓

Pass / Fail
```

A passing test increases confidence that the code behaves correctly.

______________________________________________________________________

# Why Automated Testing?

Suppose your backend contains:

- 120 API endpoints
- 250 database queries
- 600 business functions

Would you manually test everything before every deployment?

Obviously not.

Automated tests provide:

- Repeatability
- Speed
- Reliability
- Confidence during refactoring

______________________________________________________________________

# Manual vs Automated Testing

Manual testing:

```
Developer

↓

Run Application

↓

Click Buttons

↓

Observe Results
```

Automated testing:

```
Run Test Suite

↓

Hundreds of Tests

↓

Few Seconds

↓

Pass / Fail
```

Automation allows tests to be executed frequently and consistently.

______________________________________________________________________

# Types of Testing

Software testing exists at multiple levels.

```
Acceptance Tests

↑

Integration Tests

↑

Unit Tests
```

Each level answers a different question.

______________________________________________________________________

## Unit Tests

Question:

> Does one small piece of code work correctly?

Example:

```python
calculate_tax()
```

Only this function is tested.

______________________________________________________________________

## Integration Tests

Question:

> Do multiple components work together?

Example:

```
API

↓

Database

↓

Redis

↓

Message Queue
```

______________________________________________________________________

## End-to-End Tests

Question:

> Does the complete application work?

Example:

```
Browser

↓

API

↓

Database

↓

Payment Gateway

↓

Response
```

These tests are slower but validate the entire workflow.

______________________________________________________________________

# The Test Pyramid

A common testing strategy is the Test Pyramid.

```
        End-to-End
           ▲
     Integration
           ▲
       Unit Tests
```

Characteristics:

| Level | Quantity | Speed |
|---------|----------|-------|
| Unit | Many | Fast |
| Integration | Some | Moderate |
| End-to-End | Few | Slow |

Most tests should be unit tests because they execute quickly and isolate failures.

______________________________________________________________________

# Why unittest?

Python includes a built-in testing framework:

```python
unittest
```

Advantages:

- Included with Python
- No additional installation
- Mature
- Well documented
- Object-oriented design

Although many modern projects use `pytest`, understanding `unittest` provides a solid foundation because `pytest` builds
upon many of the same testing concepts.

______________________________________________________________________

# Your First Test

Suppose we have:

```python
def add(a, b):

    return a + b
```

Create:

```python
import unittest


def add(a, b):

    return a + b


class TestMath(

    unittest.TestCase

):

    def test_add(self):

        result = add(2, 3)

        self.assertEqual(

            result,

            5
        )


if __name__ == "__main__":

    unittest.main()
```

Running this test produces:

```
.

----------------------------------------------------------------

Ran 1 test

OK
```

______________________________________________________________________

# Understanding TestCase

Every test class inherits from:

```python
unittest.TestCase
```

It provides:

- Assertions
- Setup methods
- Cleanup methods
- Test execution support

Think of it as the foundation for all unit tests.

______________________________________________________________________

# Test Naming

A test method should begin with:

```python
test_
```

Example:

```python
def test_login():
```

Not:

```python
def login_test():
```

The framework discovers tests based on this naming convention.

______________________________________________________________________

# Assertions

Assertions verify expected behaviour.

Example:

```python
self.assertEqual(

    add(1, 2),

    3
)
```

If the values differ:

```
Test Fails
```

If they match:

```
Test Passes
```

______________________________________________________________________

# Common Assertions

| Assertion | Purpose |
|------------|----------|
| `assertEqual()` | Equality |
| `assertNotEqual()` | Inequality |
| `assertTrue()` | Value is `True` |
| `assertFalse()` | Value is `False` |
| `assertIsNone()` | Value is `None` |
| `assertIsNotNone()` | Value is not `None` |
| `assertIn()` | Membership |
| `assertRaises()` | Exception checking |

______________________________________________________________________

# Testing Exceptions

Suppose:

```python
def divide(a, b):

    return a / b
```

Test:

```python
class TestMath(

    unittest.TestCase

):

    def test_divide_by_zero(self):

        with self.assertRaises(

            ZeroDivisionError

        ):

            divide(5, 0)
```

The test passes only if the expected exception is raised.

______________________________________________________________________

# Test Lifecycle

Every test is independent.

Execution:

```
setUp()

↓

Test Method

↓

tearDown()
```

This prevents one test from affecting another.

______________________________________________________________________

# setUp()

Executed before every test.

```python
class TestUser(

    unittest.TestCase

):

    def setUp(self):

        self.users = []
```

Each test begins with a fresh list.

______________________________________________________________________

# tearDown()

Executed after every test.

Example:

```python
def tearDown(self):

    self.connection.close()
```

Useful for cleaning temporary resources.

______________________________________________________________________

# Running Tests

Execute a single file:

```bash
python test_math.py
```

Or discover tests automatically:

```bash
python -m unittest
```

Search a directory:

```bash
python -m unittest discover
```

The framework automatically finds test files following its naming conventions.

______________________________________________________________________

# Backend Example

Suppose we have:

```python
class UserService:

    def is_adult(

        self,

        age

    ):

        return age >= 18
```

Test:

```python
class TestUserService(

    unittest.TestCase

):

    def setUp(self):

        self.service = UserService()

    def test_adult(self):

        self.assertTrue(

            self.service.is_adult(20)

        )

    def test_minor(self):

        self.assertFalse(

            self.service.is_adult(15)

        )
```

Each rule is verified independently.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Testing multiple behaviours in one test.

______________________________________________________________________

## Mistake 2

Tests depending on execution order.

______________________________________________________________________

## Mistake 3

Sharing mutable state between tests.

______________________________________________________________________

## Mistake 4

Writing overly complex tests.

______________________________________________________________________

## Mistake 5

Skipping edge cases such as empty inputs, invalid values, and exceptions.

______________________________________________________________________

# Best Practices

✅ Keep each test focused on one behaviour.

✅ Give tests descriptive names.

✅ Ensure tests are independent.

✅ Test both expected and unexpected inputs.

✅ Prefer readable tests over clever tests.

❌ Don't write tests that depend on other tests.

❌ Don't duplicate production logic inside tests.

______________________________________________________________________

# Production Insight

In production backend systems, automated tests are typically executed:

```
Developer Pushes Code

↓

Continuous Integration

↓

Run Unit Tests

↓

Run Integration Tests

↓

Build Application

↓

Deploy
```

If the tests fail, the deployment pipeline usually stops automatically.

Testing therefore becomes part of the delivery process rather than an afterthought.

______________________________________________________________________

# Questions

### Question

> What is the purpose of a unit test?

### Answer

To verify that a small, isolated piece of code behaves correctly.

______________________________________________________________________

### Question

> Why should unit tests be independent?

### Answer

Independent tests can run in any order and failures are easier to diagnose.

______________________________________________________________________

### Question

> Why are assertions used?

### Answer

Assertions compare the actual result with the expected result and determine whether the test passes or fails.

______________________________________________________________________

### Question

> What is the purpose of `setUp()`?

### Answer

It prepares a fresh environment before each test method executes.

______________________________________________________________________

### Question

> Why are most tests in the Test Pyramid unit tests?

### Answer

Because they execute quickly, are inexpensive to maintain, and isolate failures effectively.

______________________________________________________________________

# Practical Lesson

Create a project:

```text
calculator/

├── calculator.py

└── test_calculator.py
```

Implement:

- `add()`
- `subtract()`
- `multiply()`
- `divide()`

Write unit tests for:

- Normal inputs.
- Negative numbers.
- Zero.
- Division by zero.
- Large values.

Run the tests using:

```bash
python -m unittest
```

______________________________________________________________________

# Knowledge Check

## Question 1

Why is automated testing preferred over manual testing for regression testing?

### Answer

Because automated tests can be executed repeatedly, consistently, and quickly after every code change.

______________________________________________________________________

## Question 2

What makes a good unit test?

### Answer

A good unit test is small, independent, deterministic, easy to read, and verifies one specific behaviour.

______________________________________________________________________

## Question 3

Why should production logic not be duplicated inside tests?

### Answer

If the test repeats the same logic as the implementation, both may contain the same defect, reducing the test's
effectiveness.

______________________________________________________________________

## Question 4

What role does `unittest.TestCase` play?

### Answer

It provides the base functionality for writing tests, including assertions, setup and teardown methods, and integration
with the test runner.

______________________________________________________________________

## Question 5

Why should edge cases be included in unit tests?

### Answer

Because many defects occur at boundaries or under unusual inputs rather than during typical execution.

______________________________________________________________________

# Assignment

## Exercise 1

Write unit tests for a utility module from one of your existing projects.

Aim for at least 15 independent test cases.

______________________________________________________________________

## Exercise 2

Identify three edge cases that your current project does not test.

Add unit tests for each.

______________________________________________________________________

## Exercise 3

Refactor one function in your project.

Run the tests before and after the change to verify that behaviour remains unchanged.

______________________________________________________________________

## Exercise 4

Review your test suite and answer:

- Does each test verify only one behaviour?
- Are tests independent?
- Are exception cases covered?
- Are boundary conditions tested?

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why automated testing is important.
- ✅ The different levels of testing.
- ✅ The Test Pyramid.
- ✅ The `unittest` framework.
- ✅ Test cases and assertions.
- ✅ Test lifecycle with `setUp()` and `tearDown()`.
- ✅ Test discovery.
- ✅ Production testing practices.

______________________________________________________________________

# Next Lesson

**File:** [69-testing-part-02-pytest](69-testing-part-02-pytest.md)

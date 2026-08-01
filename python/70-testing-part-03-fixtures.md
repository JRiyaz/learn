# File: python/70-testing-part-03-fixtures.md

# Testing

# Part 3: Fixtures – Reusable Test Setup with pytest

> **Course:** Backend Engineering Roadmap
>
> **Module:** Testing
>
> **Lesson:** 70
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 10–12 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What fixtures are
- Why fixtures exist
- Fixture lifecycle
- Fixture scopes
- Fixture dependencies
- Returning resources from fixtures
- Cleanup with `yield`
- `conftest.py`
- Built-in pytest fixtures
- Best practices
- Common mistakes

______________________________________________________________________

# Recap

In the previous lesson, we learned how to write tests using `pytest`.

Suppose you have 100 tests that require a database connection.

Without fixtures:

```python
def test_user():

    db = Database()

    ...
```

```python
def test_order():

    db = Database()

    ...
```

```python
def test_product():

    db = Database()

    ...
```

The same setup code is repeated everywhere.

This duplication makes tests harder to maintain.

______________________________________________________________________

# What is a Fixture?

A fixture is a reusable piece of code that prepares resources needed by one or more tests.

Think of it as a function that creates a testing environment.

```
Fixture

↓

Creates Resource

↓

Test Uses Resource
```

Instead of each test creating its own setup, pytest creates it automatically.

______________________________________________________________________

# Your First Fixture

```python
import pytest


@pytest.fixture

def number():

    return 10
```

Using the fixture:

```python
def test_number(

    number

):

    assert number == 10
```

Notice something interesting.

The test never calls:

```python
number()
```

Pytest injects the fixture automatically.

______________________________________________________________________

# How Fixture Injection Works

When pytest sees:

```python
def test_sum(

    database,

    cache,

    config

):
```

it performs:

```
Find Fixture

↓

Create Fixture

↓

Pass Result

↓

Run Test
```

The parameter names determine which fixtures are used.

______________________________________________________________________

# Why Fixtures are Better

Without fixtures:

```python
def test_login():

    db = Database()

    user = User()

    ...
```

Repeated hundreds of times.

With fixtures:

```python
@pytest.fixture

def database():

    return Database()
```

Every test simply requests:

```python
database
```

The setup exists in one place.

______________________________________________________________________

# Fixtures Can Depend on Other Fixtures

Example:

```python
@pytest.fixture

def config():

    return Config()
```

```python
@pytest.fixture

def database(

    config

):

    return Database(config)
```

Pytest builds the dependency graph automatically.

```
Config

↓

Database

↓

Test
```

______________________________________________________________________

# Multiple Fixtures

A test can request several fixtures.

```python
def test_order(

    database,

    cache,

    logger

):

    ...
```

Pytest resolves every dependency before executing the test.

______________________________________________________________________

# Fixture Scope

By default:

```python
scope="function"
```

A new fixture instance is created for every test.

Other scopes are available.

| Scope | Lifetime |
|---------|----------|
| function | Every test |
| class | Once per test class |
| module | Once per module |
| package | Once per package |
| session | Entire test session |

______________________________________________________________________

# Function Scope

```
Test A

↓

Create Fixture

↓

Destroy
```

```
Test B

↓

Create New Fixture

↓

Destroy
```

Every test starts with a fresh resource.

This is the safest option.

______________________________________________________________________

# Session Scope

Example:

```python
@pytest.fixture(

    scope="session"

)

def config():

    return load_config()
```

Created only once.

```
Start pytest

↓

Create Config

↓

Run All Tests

↓

Destroy Config
```

Ideal for immutable shared resources.

______________________________________________________________________

# Cleanup with yield

Many resources require cleanup.

Example:

```python
import pytest


@pytest.fixture

def database():

    db = Database()

    yield db

    db.close()
```

Execution order:

```
Create Database

↓

yield

↓

Run Test

↓

Cleanup
```

Everything after `yield` executes after the test finishes, even if the test fails.

______________________________________________________________________

# Temporary Files

Example:

```python
@pytest.fixture

def temp_file():

    file = open(

        "temp.txt",

        "w"

    )

    yield file

    file.close()
```

The cleanup happens automatically.

______________________________________________________________________

# conftest.py

Fixtures shared by multiple test files belong in:

```text
tests/

├── conftest.py

├── test_users.py

├── test_orders.py

└── test_products.py
```

Example:

```python
# conftest.py

import pytest


@pytest.fixture

def config():

    return {

        "debug": False

    }
```

Every test in the directory can use:

```python
config
```

without importing it.

______________________________________________________________________

# Built-in Fixtures

Pytest already provides useful fixtures.

Examples:

```python
tmp_path
```

Temporary directory.

```python
capsys
```

Capture console output.

```python
monkeypatch
```

Modify objects during tests.

We will study `monkeypatch` in a dedicated lesson.

______________________________________________________________________

# Backend Example

Suppose every API test requires:

- Database
- Redis
- Configuration

Instead of repeating setup:

```python
database = Database()

cache = Redis()

config = Config()
```

Create fixtures:

```python
@pytest.fixture

def config():

    ...
```

```python
@pytest.fixture

def database(

    config

):

    ...
```

```python
@pytest.fixture

def cache():

    ...
```

Each test simply requests the required resources.

______________________________________________________________________

# Fixture Dependency Graph

Example:

```
Config

↓

Database

↓

Repository

↓

Service

↓

API Test
```

Pytest creates them in the correct order.

Cleanup occurs in reverse order.

```
API Test

↓

Service

↓

Repository

↓

Database

↓

Config
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Duplicating setup code in every test.

______________________________________________________________________

## Mistake 2

Using session-scoped fixtures for mutable objects.

This can cause tests to influence one another.

______________________________________________________________________

## Mistake 3

Putting unrelated fixtures into one large fixture.

Prefer small, reusable fixtures.

______________________________________________________________________

## Mistake 4

Forgetting cleanup for files, sockets, or database connections.

______________________________________________________________________

## Mistake 5

Creating fixtures that perform unnecessary work for tests that don't use them.

______________________________________________________________________

# Best Practices

✅ Keep fixtures small.

✅ Use descriptive names.

✅ Prefer function scope unless sharing is necessary.

✅ Place shared fixtures in `conftest.py`.

✅ Use `yield` for cleanup.

❌ Don't create one giant "everything" fixture.

❌ Don't share mutable state unnecessarily.

______________________________________________________________________

# Production Insight

Large backend projects may contain thousands of tests.

Fixtures make those test suites maintainable by centralising resource creation.

For example:

```
PostgreSQL Container

↓

Database Fixture

↓

Repository Fixture

↓

Service Fixture

↓

500 Test Cases
```

When the database configuration changes, only the fixture needs updating rather than every test.

______________________________________________________________________

# Questions

### Question

> What is a fixture?

### Answer

A fixture is reusable setup code that prepares resources required by one or more tests.

______________________________________________________________________

### Question

> Why are fixtures preferred over manual setup?

### Answer

They eliminate duplicated setup code, improve readability, and make tests easier to maintain.

______________________________________________________________________

### Question

> Why does pytest inject fixtures automatically?

### Answer

Pytest matches test function parameters to fixture names and creates the required resources before running the test.

______________________________________________________________________

### Question

> When should `yield` be used in a fixture?

### Answer

When a resource needs cleanup after the test, such as closing files, sockets, or database connections.

______________________________________________________________________

### Question

> Why is function scope the default?

### Answer

Because it provides complete isolation by creating a fresh fixture instance for every test.

______________________________________________________________________

# Practical Lesson

Create the following structure:

```text
tests/

├── conftest.py

├── test_users.py

└── test_orders.py
```

Implement:

- A `config` fixture.
- A `database` fixture that depends on `config`.
- A `service` fixture that depends on `database`.
- A session-scoped configuration fixture.
- A fixture using `yield` to clean up a temporary file.

Verify that:

- Fixtures are reused correctly.
- Cleanup executes after every test.

______________________________________________________________________

# Knowledge Check

## Question 1

Why are fixtures considered a form of Dependency Injection?

### Answer

Because pytest creates the required objects and injects them into test functions rather than having tests construct
those objects themselves.

______________________________________________________________________

## Question 2

Why should mutable fixtures rarely use session scope?

### Answer

Because shared mutable state can make tests influence one another, leading to unreliable and difficult-to-debug
failures.

______________________________________________________________________

## Question 3

What is the purpose of `conftest.py`?

### Answer

It stores shared fixtures that pytest automatically discovers and makes available to tests in the same directory
hierarchy.

______________________________________________________________________

## Question 4

In what order are dependent fixtures cleaned up?

### Answer

Fixtures are cleaned up in the reverse order of their creation, ensuring dependent resources are released safely.

______________________________________________________________________

## Question 5

What characteristics make a good fixture?

### Answer

A good fixture is focused, reusable, independent, appropriately scoped, and performs only the setup required for the
tests that use it.

______________________________________________________________________

# Assignment

## Exercise 1

Refactor an existing pytest project to replace duplicated setup code with reusable fixtures.

______________________________________________________________________

## Exercise 2

Move all common fixtures into `conftest.py`.

Verify that no explicit imports are required in the test files.

______________________________________________________________________

## Exercise 3

Create fixtures with the following scopes:

- function
- module
- session

Add logging statements to observe when each fixture is created and destroyed.

______________________________________________________________________

## Exercise 4

Create a fixture that opens a temporary file, writes test data, yields the file object, and removes the file during
cleanup.

Confirm that cleanup occurs even when the test intentionally fails.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What fixtures are.
- ✅ Automatic fixture injection.
- ✅ Fixture dependencies.
- ✅ Fixture scopes.
- ✅ Cleanup with `yield`.
- ✅ Sharing fixtures through `conftest.py`.
- ✅ Built-in pytest fixtures.
- ✅ Production testing practices using fixtures.

______________________________________________________________________

# Next Lesson

**File:** [71-testing-part-04-mocking](71-testing-part-04-mocking.md)

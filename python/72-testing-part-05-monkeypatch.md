# File: python/72-testing-part-05-monkeypatch.md

# Testing

# Part 5: monkeypatch – Temporarily Modifying Runtime Behaviour in Tests

> **Course:** Backend Engineering Roadmap
>
> **Module:** Testing
>
> **Lesson:** 72
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 10–12 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What `monkeypatch` is
- Why `monkeypatch` exists
- `monkeypatch` vs `patch()`
- Replacing functions
- Replacing methods
- Mocking environment variables
- Mocking dictionaries
- Mocking object attributes
- Mocking the current working directory
- Mocking imports
- Common mistakes
- Production best practices

______________________________________________________________________

# Recap

In the previous lesson, we learned how to use:

```python
unittest.mock
```

including:

- Mock
- MagicMock
- patch()

Those tools are excellent for replacing objects.

However, pytest provides another powerful utility:

```python
monkeypatch
```

Unlike `Mock`, `monkeypatch` is designed to **temporarily modify the runtime environment**.

After the test finishes, pytest automatically restores everything.

______________________________________________________________________

# What is monkeypatch?

`monkeypatch` is a built-in pytest fixture that temporarily changes objects during a test.

Examples:

- Replace a function
- Replace an object attribute
- Replace an environment variable
- Replace a dictionary value
- Change the current working directory

After the test completes:

```
Original State

↓

Automatically Restored
```

______________________________________________________________________

# Why Use monkeypatch?

Suppose our application reads:

```python
import os

API_KEY = os.getenv("API_KEY")
```

Should we modify the developer's real environment?

No.

Instead:

```
Test

↓

Temporary Environment

↓

Run

↓

Restore
```

This keeps tests isolated.

______________________________________________________________________

# The monkeypatch Fixture

Every pytest test can request:

```python
def test_example(

    monkeypatch

):

    ...
```

No imports are required.

Pytest automatically provides the fixture.

______________________________________________________________________

# Replacing Attributes

Suppose:

```python
class Config:

    DEBUG = False
```

During the test:

```python
def test_debug(

    monkeypatch

):

    monkeypatch.setattr(

        Config,

        "DEBUG",

        True

    )

    assert Config.DEBUG is True
```

After the test:

```python
Config.DEBUG
```

returns to:

```python
False
```

______________________________________________________________________

# Replacing Functions

Suppose:

```python
def get_time():

    return datetime.now()
```

Testing becomes difficult because the value changes.

Instead:

```python
def fake_time():

    return "2026-01-01"
```

Test:

```python
monkeypatch.setattr(

    app,

    "get_time",

    fake_time

)
```

Now every call uses the fake implementation.

______________________________________________________________________

# Mocking Environment Variables

Production code:

```python
import os


def get_database():

    return os.getenv(

        "DATABASE_URL"

    )
```

Test:

```python
def test_database(

    monkeypatch

):

    monkeypatch.setenv(

        "DATABASE_URL",

        "sqlite:///test.db"

    )

    assert (

        get_database()

        == "sqlite:///test.db"

    )
```

The real environment remains untouched.

______________________________________________________________________

# Removing Environment Variables

Testing missing configuration.

```python
monkeypatch.delenv(

    "DATABASE_URL",

    raising=False

)
```

Useful when verifying startup validation.

______________________________________________________________________

# Modifying Dictionaries

Suppose:

```python
settings = {

    "debug": False

}
```

Test:

```python
monkeypatch.setitem(

    settings,

    "debug",

    True

)
```

After the test:

```
Dictionary

↓

Automatically Restored
```

______________________________________________________________________

# Removing Dictionary Entries

Example:

```python
monkeypatch.delitem(

    settings,

    "debug",

    raising=False

)
```

Helpful when testing missing configuration values.

______________________________________________________________________

# Changing the Current Directory

Suppose code depends on:

```python
Path.cwd()
```

Instead of changing your real shell:

```python
monkeypatch.chdir(

    tmp_path

)
```

The test executes in a temporary directory.

______________________________________________________________________

# sys.path Modification

Sometimes tests need temporary imports.

```python
monkeypatch.syspath_prepend(

    "/tmp/plugins"
)
```

The path exists only for the duration of the test.

______________________________________________________________________

# Replacing Instance Methods

Suppose:

```python
class EmailService:

    def send(

        self,

        email

    ):

        ...
```

Fake method:

```python
def fake_send(

    self,

    email

):

    return True
```

Test:

```python
monkeypatch.setattr(

    EmailService,

    "send",

    fake_send

)
```

Every instance now uses:

```python
fake_send()
```

until the test ends.

______________________________________________________________________

# monkeypatch vs patch()

| monkeypatch | patch() |
|--------------|---------|
| Built into pytest | Part of `unittest.mock` |
| Automatically restored | Automatically restored inside context/decorator |
| Excellent for environment changes | Excellent for mocks |
| Simple attribute replacement | Rich mocking features |

Use:

- `patch()` when verifying interactions with mocks.
- `monkeypatch` when temporarily modifying runtime state.

Many projects use both together.

______________________________________________________________________

# Backend Example

Suppose a service loads:

```python
DATABASE_URL
```

during startup.

Production:

```
DATABASE_URL

↓

PostgreSQL
```

Test:

```
DATABASE_URL

↓

SQLite

↓

Run Test

↓

Restore
```

No production configuration is modified.

______________________________________________________________________

# Example: Mocking an API Function

Production:

```python
def fetch_weather():

    ...
```

Test:

```python
def fake_weather():

    return {

        "temperature": 25

    }


def test_weather(

    monkeypatch

):

    monkeypatch.setattr(

        weather,

        "fetch_weather",

        fake_weather

    )

    assert (

        weather.fetch_weather()

        ["temperature"]

        == 25

    )
```

No HTTP request is made.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using `monkeypatch` when dependency injection would be simpler.

______________________________________________________________________

## Mistake 2

Replacing the wrong attribute.

Always patch the object actually used by the code under test.

______________________________________________________________________

## Mistake 3

Using `monkeypatch` to hide design problems.

Frequent monkeypatching may indicate that dependencies are tightly coupled.

______________________________________________________________________

## Mistake 4

Mixing permanent state changes with temporary patches.

______________________________________________________________________

## Mistake 5

Using `monkeypatch` outside pytest.

It is a pytest fixture and is not available in plain Python scripts.

______________________________________________________________________

# Best Practices

✅ Use `monkeypatch` for environment variables.

✅ Use it for temporary runtime changes.

✅ Prefer dependency injection where practical.

✅ Keep patches local to the test.

✅ Let pytest restore state automatically.

❌ Don't modify global state permanently.

❌ Don't overuse monkeypatch to compensate for poor design.

______________________________________________________________________

# Production Insight

Modern backend applications often depend on:

- Environment variables
- Configuration files
- Current working directory
- External SDKs
- System paths

Tests should never modify the developer's machine or CI environment permanently.

`monkeypatch` allows runtime behaviour to be modified safely while guaranteeing that the original state is restored
after each test.

______________________________________________________________________

# Questions

### Question

> What is `monkeypatch`?

### Answer

`monkeypatch` is a built-in pytest fixture that temporarily modifies objects, environment variables, dictionaries, or
other runtime state during a test.

______________________________________________________________________

### Question

> Why is `monkeypatch` useful for environment variables?

### Answer

It allows tests to simulate different environments without changing the real operating system environment.

______________________________________________________________________

### Question

> When should `monkeypatch` be preferred over `patch()`?

### Answer

It is particularly useful for temporarily modifying runtime state such as environment variables, object attributes, or
the current working directory.

______________________________________________________________________

### Question

> Does `monkeypatch` restore changes automatically?

### Answer

Yes. Pytest restores the original state after each test, ensuring isolation.

______________________________________________________________________

### Question

> Why shouldn't `monkeypatch` replace good application design?

### Answer

If many tests require extensive monkeypatching, it often indicates that the code has tightly coupled dependencies and
could benefit from dependency injection or better separation of concerns.

______________________________________________________________________

# Practical Lesson

Create the following project:

```text
config_app/

├── config.py

├── service.py

└── tests/

    └── test_config.py
```

Implement tests that:

1. Replace an environment variable using `setenv()`.
1. Remove an environment variable using `delenv()`.
1. Replace a function using `setattr()`.
1. Modify a dictionary using `setitem()`.
1. Change the working directory using `chdir()`.

Verify that every modification is automatically restored after each test.

______________________________________________________________________

# Knowledge Check

## Question 1

Why is `monkeypatch` considered safer than manually changing global state?

### Answer

Because pytest automatically restores the original state after the test completes, preventing changes from affecting
other tests.

______________________________________________________________________

## Question 2

What types of runtime state can `monkeypatch` modify?

### Answer

It can modify object attributes, functions, methods, environment variables, dictionary entries, the current working
directory, and Python's import path.

______________________________________________________________________

## Question 3

Why is `monkeypatch.setenv()` commonly used in backend testing?

### Answer

Backend applications frequently rely on environment variables for configuration, and `setenv()` allows tests to simulate
different deployment configurations safely.

______________________________________________________________________

## Question 4

When is dependency injection preferable to `monkeypatch`?

### Answer

When dependencies can be supplied directly to the code under test, resulting in simpler, more explicit, and
easier-to-maintain tests.

______________________________________________________________________

## Question 5

Can `monkeypatch` and `Mock` be used together?

### Answer

Yes. `monkeypatch` can replace an object with a `Mock`, combining temporary runtime modification with interaction
verification.

______________________________________________________________________

# Assignment

## Exercise 1

Take one of your FastAPI or Flask projects.

Replace all environment-variable setup in tests with `monkeypatch.setenv()`.

______________________________________________________________________

## Exercise 2

Write tests that simulate:

- Missing configuration.
- Different deployment environments.
- Alternate API endpoints.

using only `monkeypatch`.

______________________________________________________________________

## Exercise 3

Replace a function that normally performs an HTTP request with a fake implementation using `monkeypatch.setattr()`.

Verify that the application behaves correctly without making a network call.

______________________________________________________________________

## Exercise 4

Review your current test suite.

Identify every place where `patch()` is being used solely to change runtime state.

Determine whether `monkeypatch` would provide a simpler solution.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What `monkeypatch` is.
- ✅ How it differs from `patch()`.
- ✅ Replacing attributes and functions.
- ✅ Mocking environment variables.
- ✅ Modifying dictionaries.
- ✅ Changing the working directory.
- ✅ Managing `sys.path`.
- ✅ Production testing practices using `monkeypatch`.

______________________________________________________________________

# Next Lesson

**File:** [73-testing-part-06-coverage](73-testing-part-06-coverage.md)

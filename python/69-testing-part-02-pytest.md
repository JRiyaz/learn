# File: python/69-testing-part-02-pytest.md

# Testing

# Part 2: pytest – Modern Python Testing

> **Course:** Backend Engineering Roadmap
>
> **Module:** Testing
>
> **Lesson:** 69
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 10–12 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why `pytest` has become the standard testing framework
- Differences between `unittest` and `pytest`
- Writing tests without classes
- Test discovery
- Assertions in `pytest`
- Parametrized tests
- Test markers
- Skipping tests
- Expected failures
- Organising test suites
- Production best practices

______________________________________________________________________

# Recap

In the previous lesson, we learned how to write unit tests using Python's built-in `unittest` framework.

Although `unittest` is powerful and widely used, most modern Python projects—including **FastAPI**, **Flask**,
**Django**, **SQLAlchemy**, and many open-source libraries—use **pytest** because it is simpler, more expressive, and
highly extensible.

______________________________________________________________________

# Why pytest?

Imagine testing this function:

```python
def add(a, b):
    return a + b
```

With `unittest`:

```python
import unittest


class TestMath(unittest.TestCase):

    def test_add(self):

        self.assertEqual(add(2, 3), 5)
```

With `pytest`:

```python
def test_add():

    assert add(2, 3) == 5
```

Less boilerplate.

More readable.

______________________________________________________________________

# Installing pytest

```bash
pip install pytest
```

Verify installation:

```bash
pytest --version
```

______________________________________________________________________

# Test Discovery

By default, `pytest` automatically discovers:

Files:

```text
test_*.py

*_test.py
```

Functions:

```python
def test_...():
```

Classes:

```python
class Test...
```

without requiring inheritance from `TestCase`.

______________________________________________________________________

# Your First pytest Test

Application:

```python
def multiply(a, b):

    return a * b
```

Test:

```python
def test_multiply():

    assert multiply(4, 5) == 20
```

Run:

```bash
pytest
```

Output:

```text
====================

1 passed

====================
```

______________________________________________________________________

# Assertions

Unlike `unittest`, `pytest` uses Python's built-in:

```python
assert
```

Example:

```python
assert total == 150
```

If the assertion fails, `pytest` automatically displays a detailed explanation.

Example:

```python
assert 150 == 120
```

Output:

```text
E assert 150 == 120
```

This is one of pytest's biggest usability improvements.

______________________________________________________________________

# Organising Tests

Example project:

```text
inventory/

├── app/

├── tests/

│   ├── test_users.py
│   ├── test_orders.py
│   └── test_products.py

└── pyproject.toml
```

Keeping tests in a dedicated `tests/` directory is the most common convention.

______________________________________________________________________

# Running Tests

Run everything:

```bash
pytest
```

Run one file:

```bash
pytest tests/test_users.py
```

Run one test:

```bash
pytest tests/test_users.py::test_create_user
```

Run quietly:

```bash
pytest -q
```

______________________________________________________________________

# Parametrized Tests

Suppose we want to test multiple inputs.

Without parametrization:

```python
def test_add_one():

    assert add(1, 2) == 3


def test_add_two():

    assert add(5, 8) == 13


def test_add_three():

    assert add(-1, 1) == 0
```

Lots of repetition.

Instead:

```python
import pytest


@pytest.mark.parametrize(

    "a,b,result",

    [

        (1, 2, 3),

        (5, 8, 13),

        (-1, 1, 0)

    ]

)

def test_add(

    a,

    b,

    result

):

    assert add(a, b) == result
```

One test.

Multiple scenarios.

______________________________________________________________________

# Skipping Tests

Sometimes a test is temporarily irrelevant.

```python
import pytest


@pytest.mark.skip

def test_old_feature():

    ...
```

You can also provide a reason:

```python
@pytest.mark.skip(

    reason="Feature removed"
)
```

______________________________________________________________________

# Expected Failures

Occasionally you know a test currently fails because of an existing bug.

```python
@pytest.mark.xfail

def test_known_bug():

    ...
```

The failure is recorded without causing the entire test suite to fail.

______________________________________________________________________

# Markers

Markers group related tests.

Example:

```python
@pytest.mark.database

def test_insert_user():

    ...
```

Run only database tests:

```bash
pytest -m database
```

Useful markers include:

- database
- api
- slow
- integration

______________________________________________________________________

# Comparing unittest and pytest

| Feature | unittest | pytest |
|----------|-----------|--------|
| Built into Python | ✅ | ❌ |
| Uses classes | Usually | Optional |
| Assertions | `assertEqual()` | `assert` |
| Parametrization | Manual | Built-in |
| Plugins | Limited | Extensive |
| Boilerplate | More | Less |

Both frameworks are excellent.

`pytest` is generally preferred for new Python projects.

______________________________________________________________________

# Backend Example

Consider an authentication service.

```python
def authenticate(

    username,

    password

):

    ...
```

A parametrized test can verify many login combinations:

```python
@pytest.mark.parametrize(

    "username,password,success",

    [

        ("alice", "secret", True),

        ("alice", "wrong", False),

        ("bob", "secret", False)

    ]

)

def test_authentication(

    username,

    password,

    success

):

    assert authenticate(

        username,

        password

    ) == success
```

Adding new cases requires only another tuple.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Writing very large test functions.

______________________________________________________________________

## Mistake 2

Duplicating test data instead of using parametrization.

______________________________________________________________________

## Mistake 3

Using markers without documenting them.

______________________________________________________________________

## Mistake 4

Skipping tests permanently instead of fixing them.

______________________________________________________________________

## Mistake 5

Writing tests that depend on execution order.

______________________________________________________________________

# Best Practices

✅ Keep each test focused on one behaviour.

✅ Use parametrization to reduce duplication.

✅ Organise tests by feature.

✅ Give tests descriptive names.

✅ Keep tests deterministic.

❌ Don't hide failing tests with unnecessary skips.

❌ Don't share mutable state between tests.

______________________________________________________________________

# Production Insight

Most modern CI/CD pipelines execute `pytest` automatically.

Typical workflow:

```
Developer Pushes Code

↓

CI Pipeline

↓

pytest

↓

Build

↓

Deploy
```

Many teams configure the pipeline so that **any failing test blocks deployment**, ensuring regressions are caught before
reaching production.

______________________________________________________________________

# Questions

### Question

> Why is `pytest` more popular than `unittest`?

### Answer

Because it requires less boilerplate, has a simpler assertion style, supports powerful features like parametrization,
and has a rich plugin ecosystem.

______________________________________________________________________

### Question

> Why use parametrized tests?

### Answer

They reduce duplicated test code while allowing multiple input combinations to be tested with a single function.

______________________________________________________________________

### Question

> When should `@pytest.mark.skip` be used?

### Answer

Only when a test genuinely cannot be executed, such as on unsupported platforms or while a feature is temporarily
unavailable.

______________________________________________________________________

### Question

> What is the purpose of markers?

### Answer

Markers categorise tests so subsets (such as database or slow tests) can be executed independently.

______________________________________________________________________

### Question

> Can `pytest` run `unittest` tests?

### Answer

Yes. `pytest` can discover and execute many existing `unittest` test cases, making migration easier.

______________________________________________________________________

# Practical Lesson

Create:

```text
tests/

├── test_math.py

├── test_string.py

└── test_validation.py
```

Implement:

- Multiple test functions.
- At least one parametrized test.
- One skipped test.
- One expected-failure test.
- One custom marker named `slow`.

Run:

```bash
pytest
```

Then run only the `slow` tests.

______________________________________________________________________

# Knowledge Check

## Question 1

Why do many Python projects prefer `pytest` over `unittest`?

### Answer

Its concise syntax, powerful features, and extensive plugin ecosystem improve developer productivity while keeping tests
easy to read.

______________________________________________________________________

## Question 2

What advantage does using `assert` provide in `pytest`?

### Answer

`pytest` automatically rewrites assertions to produce detailed failure messages without requiring specialised assertion
methods.

______________________________________________________________________

## Question 3

Why should parametrized tests be preferred over duplicated test functions?

### Answer

They reduce repetition, improve maintainability, and make it easier to add new test scenarios.

______________________________________________________________________

## Question 4

What is the difference between `skip` and `xfail`?

### Answer

`skip` prevents a test from running, while `xfail` runs the test but treats an expected failure as non-blocking.

______________________________________________________________________

## Question 5

Why should tests remain deterministic?

### Answer

A test should produce the same result every time it runs under the same conditions, making failures reliable and easier
to investigate.

______________________________________________________________________

# Assignment

## Exercise 1

Install `pytest` and migrate five existing `unittest` tests to `pytest`.

______________________________________________________________________

## Exercise 2

Replace duplicated tests in one of your projects with a single parametrized test.

______________________________________________________________________

## Exercise 3

Create custom markers:

- `database`
- `api`
- `slow`

Run each group independently.

______________________________________________________________________

## Exercise 4

Compare one `unittest` file and its equivalent `pytest` version.

Identify which approach is more readable and explain why.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why `pytest` is the preferred testing framework for many Python projects.
- ✅ How test discovery works.
- ✅ Assertions using `assert`.
- ✅ Parametrized tests.
- ✅ Test markers.
- ✅ Skipping tests.
- ✅ Expected failures.
- ✅ Production testing practices with `pytest`.

______________________________________________________________________

# Next Lesson

**File:** [70-testing-part-03-fixtures](70-testing-part-03-fixtures.md)

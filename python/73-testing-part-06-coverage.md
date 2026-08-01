# File: python/73-testing-part-06-coverage.md

# Testing

# Part 6: Test Coverage – Measuring What Your Tests Actually Execute

> **Course:** Backend Engineering Roadmap
>
> **Module:** Testing
>
> **Lesson:** 73
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 8–10 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What test coverage is
- Why coverage matters
- Line coverage
- Branch coverage
- Statement coverage
- Coverage reports
- Using `coverage.py`
- Using `pytest-cov`
- Reading HTML coverage reports
- Coverage limitations
- Production best practices

______________________________________________________________________

# Recap

So far we've learned how to write tests using:

- `unittest`
- `pytest`
- Fixtures
- Mocking
- `monkeypatch`

But an important question remains.

> **How much of our application is actually being tested?**

Imagine a backend service with:

- 25 Python modules
- 300 functions
- 15,000 lines of code

Your test suite passes.

Does that mean every line has been tested?

Not necessarily.

This is where **test coverage** becomes valuable.

______________________________________________________________________

# What is Test Coverage?

Test coverage measures how much of your source code is executed while running tests.

```
Application

↓

Run Tests

↓

Measure Executed Code

↓

Coverage Report
```

Coverage answers questions such as:

- Which files were executed?
- Which lines were never executed?
- Which branches were skipped?

______________________________________________________________________

# Why Coverage Matters

Suppose you write:

```python
def discount(price, is_member):

    if is_member:
        return price * 0.9

    return price
```

Your only test is:

```python
def test_member_discount():

    assert discount(100, True) == 90
```

The test passes.

However:

```python
discount(100, False)
```

has never been executed.

Coverage highlights this missing path.

______________________________________________________________________

# Coverage is Not the Same as Quality

High coverage does **not** automatically mean good tests.

Example:

```python
def add(a, b):

    return a + b
```

Poor test:

```python
def test_add():

    add(2, 3)
```

The function executed.

Coverage:

```
100%
```

But nothing was verified.

A meaningful test would be:

```python
def test_add():

    assert add(2, 3) == 5
```

Coverage measures execution, not correctness.

______________________________________________________________________

# Types of Coverage

Several metrics are commonly used.

______________________________________________________________________

## Line Coverage

Measures how many executable lines were run.

Example:

```python
def sign(x):

    if x > 0:
        return "positive"

    return "zero_or_negative"
```

If only:

```python
sign(5)
```

is tested:

```
Line Coverage

↓

Most lines executed

↓

Return path partially tested
```

______________________________________________________________________

## Branch Coverage

Branch coverage measures every possible decision path.

Example:

```python
if age >= 18:

    allow()

else:

    deny()
```

To achieve full branch coverage:

```
age = 20

↓

allow()

AND

age = 15

↓

deny()
```

Every branch must execute.

______________________________________________________________________

## Statement Coverage

Statement coverage measures whether each executable statement has been run at least once.

Although similar to line coverage, branch coverage provides a more complete picture for conditional logic.

______________________________________________________________________

# Installing coverage.py

Install:

```bash
pip install coverage
```

Run tests:

```bash
coverage run -m pytest
```

Generate report:

```bash
coverage report
```

Example:

```text
Name                Stmts   Miss  Cover

---------------------------------------

service.py            80      6    92%

models.py             40      0   100%
```

______________________________________________________________________

# HTML Reports

Generate an HTML report:

```bash
coverage html
```

Output:

```text
htmlcov/

    index.html
```

Open:

```text
htmlcov/index.html
```

The report displays:

- Covered lines (green)
- Missed lines (red)
- Coverage percentage per file

This makes it easy to identify untested code.

______________________________________________________________________

# Using pytest-cov

Most pytest projects use the plugin:

```bash
pip install pytest-cov
```

Run:

```bash
pytest --cov=app
```

Example:

```text
----------- coverage -----------

TOTAL

91%
```

Generate HTML:

```bash
pytest --cov=app --cov-report=html
```

______________________________________________________________________

# Reading a Coverage Report

Example:

```text
Name

service.py

Coverage

78%
```

Questions to ask:

- Which lines are uncovered?
- Are they important?
- Are error paths tested?
- Are edge cases covered?

Coverage reports help prioritise new tests.

______________________________________________________________________

# Missing Branches

Example:

```python
def validate(age):

    if age < 0:

        raise ValueError()

    return age
```

Only testing:

```python
validate(20)
```

misses:

```python
validate(-1)
```

Coverage identifies the missing branch.

______________________________________________________________________

# Backend Example

Consider an authentication service.

```python
def login(

    username,

    password

):

    ...
```

Possible paths:

```
Correct Password

↓

Success
```

```
Wrong Password

↓

Authentication Error
```

```
Locked Account

↓

Permission Error
```

```
Missing User

↓

Not Found
```

A complete test suite should exercise all meaningful paths.

______________________________________________________________________

# Excluding Code

Some lines should not count towards coverage.

Example:

```python
if TYPE_CHECKING:

    ...
```

or

```python
if __name__ == "__main__":

    main()
```

Coverage tools support exclusion rules for such cases.

Use exclusions sparingly and document why they exist.

______________________________________________________________________

# Setting Coverage Thresholds

Many CI pipelines enforce minimum coverage.

Example:

```bash
pytest --cov=app --cov-fail-under=90
```

If coverage drops below:

```
90%
```

the build fails.

This prevents test quality from gradually declining.

______________________________________________________________________

# Why 100% Coverage Isn't Always Necessary

Imagine this function:

```python
def connect():

    ...
```

Some error paths may only occur if:

- The operating system fails.
- Disk hardware becomes unavailable.
- A third-party library raises an unexpected exception.

Trying to cover every theoretical path can produce tests that add little value.

Aim to cover:

- Business logic
- Edge cases
- Error handling
- Validation
- Critical workflows

rather than chasing a perfect percentage.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Treating coverage percentage as the only quality metric.

______________________________________________________________________

## Mistake 2

Writing meaningless tests just to increase coverage.

______________________________________________________________________

## Mistake 3

Ignoring uncovered error paths.

______________________________________________________________________

## Mistake 4

Never reviewing HTML reports.

______________________________________________________________________

## Mistake 5

Assuming 100% coverage guarantees bug-free software.

______________________________________________________________________

# Best Practices

✅ Use coverage as a guide, not a goal.

✅ Review uncovered branches regularly.

✅ Prioritise business-critical code.

✅ Include negative and edge-case tests.

✅ Integrate coverage into CI.

❌ Don't chase 100% coverage at the expense of useful tests.

❌ Don't ignore low coverage in critical modules.

______________________________________________________________________

# Production Insight

Most production teams combine:

```
pytest

↓

Coverage Measurement

↓

Coverage Threshold

↓

CI/CD Pipeline
```

A typical pipeline may require:

- Overall coverage above 90%
- No decrease from the previous release
- Coverage reports uploaded as build artifacts
- Pull requests to include tests for newly added code

Coverage becomes a continuous quality metric rather than a one-time report.

______________________________________________________________________

# Questions

### Question

> What does test coverage measure?

### Answer

It measures which parts of the source code are executed while running the test suite.

______________________________________________________________________

### Question

> Does high coverage guarantee correct software?

### Answer

No. Coverage only measures execution, not whether the tests verify correct behaviour.

______________________________________________________________________

### Question

> Why is branch coverage often more valuable than line coverage?

### Answer

Because it verifies that all decision paths, such as both sides of an `if` statement, have been exercised.

______________________________________________________________________

### Question

> Why should HTML coverage reports be reviewed?

### Answer

They visually identify uncovered lines and branches, making it easier to prioritise additional tests.

______________________________________________________________________

### Question

> Why are coverage thresholds useful in CI?

### Answer

They prevent overall test coverage from decreasing over time as the codebase evolves.

______________________________________________________________________

# Practical Lesson

Create a small project containing:

```text
calculator/

├── calculator.py

├── test_calculator.py

└── pyproject.toml
```

Implement functions with:

- Conditional logic
- Error handling
- Validation

Run:

```bash
pytest --cov=calculator
```

Generate:

```bash
pytest --cov=calculator --cov-report=html
```

Open the HTML report and identify:

- Uncovered lines
- Missing branches
- Opportunities for new tests

Then write additional tests until all meaningful branches are exercised.

______________________________________________________________________

# Knowledge Check

## Question 1

Why is 100% line coverage not sufficient?

### Answer

Because code may execute without being meaningfully verified, and many logical branches may still remain untested.

______________________________________________________________________

## Question 2

What is the main benefit of branch coverage?

### Answer

It ensures that different execution paths through conditional logic are tested, increasing confidence in program
behaviour.

______________________________________________________________________

## Question 3

When should uncovered code be investigated?

### Answer

Whenever it belongs to important business logic, validation, error handling, or frequently used functionality.

______________________________________________________________________

## Question 4

Why should coverage reports be included in CI pipelines?

### Answer

They provide continuous feedback about testing quality and prevent coverage from decreasing as new code is added.

______________________________________________________________________

## Question 5

How should developers use coverage metrics responsibly?

### Answer

As a tool for identifying testing gaps rather than as the sole measure of software quality.

______________________________________________________________________

# Assignment

## Exercise 1

Install `pytest-cov` in one of your existing projects.

Generate both terminal and HTML coverage reports.

______________________________________________________________________

## Exercise 2

Identify the five least-covered functions in your project.

Write meaningful tests for each and compare the reports before and after.

______________________________________________________________________

## Exercise 3

Configure your project so that the test suite fails when coverage drops below 90%.

Verify the behaviour by intentionally removing a test.

______________________________________________________________________

## Exercise 4

Review your HTML coverage report.

For every uncovered branch, decide whether it should:

- Be tested,
- Be excluded with justification, or
- Be removed as dead code.

Document your reasoning.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What test coverage measures.
- ✅ The difference between line, branch, and statement coverage.
- ✅ How to use `coverage.py`.
- ✅ How to use `pytest-cov`.
- ✅ How to generate HTML reports.
- ✅ Why coverage is not the same as test quality.
- ✅ How CI pipelines enforce coverage thresholds.
- ✅ Production best practices for maintaining healthy test coverage.

______________________________________________________________________

# Next Lesson

**File:** [74-testing-part-07-integration-testing](74-testing-part-07-integration-testing.md)

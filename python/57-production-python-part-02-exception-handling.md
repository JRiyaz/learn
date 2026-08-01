# File: python/57-production-python-part-02-exception-handling.md

# Production Python

# Part 2: Exception Handling – Building Reliable and Resilient Python Applications

> **Course:** Backend Engineering Roadmap
>
> **Module:** Production Python
>
> **Lesson:** 57
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 10–12 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why exception handling exists
- Python's exception hierarchy
- Exception propagation
- The exception handling flow
- `try`, `except`, `else`, and `finally`
- Raising exceptions correctly
- Chaining exceptions
- Re-raising exceptions
- Exception handling strategies in production systems
- Common anti-patterns
- Backend examples
- Best practices
- questions

______________________________________________________________________

# Recap

Every backend application interacts with unreliable systems.

For example:

- PostgreSQL
- Redis
- External APIs
- File systems
- Message brokers
- Cloud storage

All of them can fail.

A production application is not expected to prevent every failure.

Instead, it is expected to:

- Detect failures
- Handle them appropriately
- Recover where possible
- Fail gracefully where necessary

That is the purpose of exception handling.

______________________________________________________________________

# Errors vs Exceptions

Many developers use these terms interchangeably.

They are related but not identical.

An **error** is a problem.

An **exception** is the mechanism Python uses to report many runtime problems.

Example:

```python
10 / 0
```

Python reports

```text
ZeroDivisionError
```

This exception communicates that something unexpected occurred.

______________________________________________________________________

# Python Exception Hierarchy

Python exceptions form an inheritance tree.

```text
BaseException

├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   ├── OverflowError
    │   └── FloatingPointError
    │
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    │
    ├── OSError
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   └── TimeoutError
    │
    ├── ValueError
    ├── TypeError
    ├── RuntimeError
    └── ...
```

Most application code should catch exceptions derived from:

```python
Exception
```

Avoid catching:

```python
BaseException
```

because it includes exceptions used to terminate the program.

______________________________________________________________________

# What Happens When an Exception Occurs?

Suppose:

```python
def divide():

    return 10 / 0


divide()
```

Execution becomes

```
divide()

↓

ZeroDivisionError

↓

No Handler Found

↓

Program Terminates
```

If no matching exception handler exists,

Python unwinds the call stack.

______________________________________________________________________

# Stack Unwinding

Consider

```python
main()

↓

service()

↓

repository()

↓

database()
```

If

```python
database()
```

raises an exception,

Python searches upward.

```
database()

↓

repository()

↓

service()

↓

main()
```

The first matching handler catches it.

If none exists,

the application crashes.

______________________________________________________________________

# Basic Exception Handling

```python
try:

    value = 10 / 0

except ZeroDivisionError:

    print("Cannot divide by zero.")
```

Flow

```
try

↓

Exception?

↓

Yes

↓

except

↓

Continue
```

______________________________________________________________________

# Multiple Exception Handlers

```python
try:

    ...

except ValueError:

    ...

except TypeError:

    ...

except KeyError:

    ...
```

Python evaluates them from top to bottom.

The first matching handler executes.

______________________________________________________________________

# Catching Multiple Exceptions

Instead of:

```python
except ValueError:

    ...

except TypeError:

    ...
```

you may write

```python
except (ValueError, TypeError):

    ...
```

Useful when the recovery strategy is identical.

______________________________________________________________________

# The `else` Block

Many developers never use:

```python
else
```

Example

```python
try:

    number = int(text)

except ValueError:

    print("Invalid input.")

else:

    print(number)
```

The `else` block executes only if no exception occurs.

This keeps success logic separate from error handling.

______________________________________________________________________

# The `finally` Block

Some resources must always be released.

Example:

- Files
- Database connections
- Network sockets
- Locks

Use:

```python
finally
```

Example

```python
file = open("data.txt")

try:

    process(file)

finally:

    file.close()
```

Whether an exception occurs or not,

the file is closed.

______________________________________________________________________

# Execution Flow

```
try

↓

Exception?

↓

No

↓

else

↓

finally
```

or

```
try

↓

Exception

↓

except

↓

finally
```

Notice:

`finally` always executes.

______________________________________________________________________

# Raising Exceptions

Python allows you to signal problems explicitly.

```python
raise ValueError(

    "Age cannot be negative."
)
```

This is preferable to returning special values like:

```python
-1
```

or

```python
None
```

when those values could be ambiguous.

______________________________________________________________________

# Re-Raising Exceptions

Suppose you want to log an exception but allow higher-level code to handle it.

```python
try:

    process_payment()

except PaymentError:

    logger.exception("Payment failed.")

    raise
```

Notice

```python
raise
```

without specifying an exception.

This preserves the original traceback.

______________________________________________________________________

# Exception Chaining

Sometimes one exception causes another.

Example

```python
try:

    load_config()

except FileNotFoundError as exc:

    raise RuntimeError(

        "Application startup failed."

    ) from exc
```

Output

```text
RuntimeError

The above exception was the direct cause of:

FileNotFoundError
```

Exception chaining preserves the original context.

______________________________________________________________________

# Backend Example

Suppose

```
API

↓

Service

↓

Repository

↓

Database
```

Database layer

```python
raise ConnectionError(...)
```

Repository

logs additional context,

then re-raises.

Service

translates the failure into a business-level exception.

API

returns

```
HTTP 503
```

The original cause remains visible in logs.

______________________________________________________________________

# What Should You Catch?

Good

```python
except FileNotFoundError:
```

Good

```python
except ValueError:
```

Acceptable (top-level boundary)

```python
except Exception:
```

Avoid

```python
except:
```

or

```python
except BaseException:
```

These hide serious problems like:

- KeyboardInterrupt
- SystemExit

______________________________________________________________________

# Anti-Pattern: Silent Failures

Bad

```python
try:

    process()

except Exception:

    pass
```

The application ignores failures completely.

Debugging becomes nearly impossible.

______________________________________________________________________

# Anti-Pattern: Returning Error Codes

Instead of

```python
return -1
```

Prefer

```python
raise ValueError(...)
```

Exceptions clearly communicate failure.

______________________________________________________________________

# Anti-Pattern: Broad Catching

Bad

```python
except Exception:

    print("Something went wrong.")
```

This discards valuable information.

At minimum,

log the exception.

______________________________________________________________________

# Production Strategy

In large systems,

exceptions are handled at different layers.

```
Database

↓

Repository

↓

Service

↓

API Boundary
```

Lower layers:

- Add context
- Re-raise

Upper layers:

- Convert to HTTP responses
- Retry
- Log
- Alert
- Recover where appropriate

______________________________________________________________________

# Exception Translation

Suppose PostgreSQL raises

```python
UniqueViolation
```

Your service layer may translate it into

```python
UserAlreadyExistsError
```

Higher layers no longer depend on PostgreSQL-specific exceptions.

This improves abstraction.

______________________________________________________________________

# Logging Exceptions

Always prefer

```python
logger.exception(
    "User creation failed."
)
```

over

```python
logger.error(
    "User creation failed."
)
```

inside an `except` block.

`logger.exception()` automatically records the traceback.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using

```python
except:
```

______________________________________________________________________

## Mistake 2

Ignoring exceptions with

```python
pass
```

______________________________________________________________________

## Mistake 3

Returning magic values instead of raising exceptions.

______________________________________________________________________

## Mistake 4

Losing the original traceback by raising a completely new exception without chaining.

______________________________________________________________________

## Mistake 5

Handling exceptions too early.

Sometimes it is better to let them propagate to the appropriate layer.

______________________________________________________________________

# Best Practices

✅ Catch the most specific exception possible.

✅ Release resources using `finally`.

✅ Use `else` for success logic.

✅ Re-raise exceptions after logging when appropriate.

✅ Preserve context using exception chaining.

❌ Don't suppress exceptions silently.

❌ Don't use exceptions for normal control flow.

❌ Don't catch `BaseException`.

______________________________________________________________________

# Production Insight

Well-designed backend systems have clear exception boundaries.

For example:

```
Database Driver

↓

Repository

↓

Service

↓

REST API

↓

HTTP Response
```

Each layer has a different responsibility.

The repository understands database errors.

The service understands business rules.

The API understands HTTP.

Keeping these concerns separate makes systems easier to maintain, test, and evolve.

______________________________________________________________________

# Questions

### Question

> What is stack unwinding?

### Answer

It is the process by which Python walks back through the call stack searching for a matching exception handler after an
exception is raised.

______________________________________________________________________

### Question

> Why use `finally`?

### Answer

Because it guarantees cleanup code executes regardless of whether an exception occurs.

______________________________________________________________________

### Question

> Why re-raise an exception?

### Answer

To allow higher-level code to handle it while preserving the original traceback and execution context.

______________________________________________________________________

### Question

> What is exception chaining?

### Answer

It links a new exception to the original cause using `raise ... from ...`, preserving debugging information.

______________________________________________________________________

### Question

> Why avoid `except:`?

### Answer

Because it catches exceptions such as `KeyboardInterrupt` and `SystemExit`, making programs difficult to terminate
correctly.

______________________________________________________________________

# Practical Lesson

Create

```text
exception_flow.py
```

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def repository():

    raise FileNotFoundError("users.csv not found")


def service():

    try:

        repository()

    except FileNotFoundError as exc:

        logger.exception("Repository failed.")

        raise RuntimeError(

            "User service unavailable."

        ) from exc


def main():

    try:

        service()

    except RuntimeError:

        logger.exception("Application failed.")


if __name__ == "__main__":

    main()
```

Observe:

- Stack unwinding.
- Exception chaining.
- Logging at different layers.
- The final traceback.

______________________________________________________________________

# Questions

## Question 1

What is the difference between `except Exception` and `except BaseException`?

### Answer

`Exception` catches application-level runtime errors, whereas `BaseException` also catches system-level exceptions such
as `KeyboardInterrupt` and `SystemExit`, which are usually not intended to be intercepted.

______________________________________________________________________

## Question 2

When should `finally` be used?

### Answer

Whenever resources such as files, sockets, database connections, or locks must be released regardless of success or
failure.

______________________________________________________________________

## Question 3

Why is exception chaining important?

### Answer

It preserves the original cause of a failure while allowing higher layers to raise more meaningful exceptions.

______________________________________________________________________

## Question 4

Why should applications avoid silent exception handling?

### Answer

Because hidden failures make debugging, monitoring, and recovery significantly more difficult.

______________________________________________________________________

## Question 5

How should exceptions flow through a layered backend architecture?

### Answer

Lower layers should raise or translate technical exceptions, while higher layers should convert them into user-facing
responses, retries, or operational actions.

______________________________________________________________________

# Assignment

## Exercise 1

Create a three-layer application:

- Repository
- Service
- API

Raise an exception in the repository.

Translate it in the service.

Handle it in the API.

______________________________________________________________________

## Exercise 2

Rewrite code that returns error codes (`None`, `-1`, etc.) to use exceptions instead.

______________________________________________________________________

## Exercise 3

Create an example demonstrating:

- `try`
- `except`
- `else`
- `finally`

Explain the execution order.

______________________________________________________________________

## Exercise 4

Review one of your existing Flask or FastAPI projects.

Identify where exceptions are:

- Raised
- Logged
- Translated
- Converted into HTTP responses

Suggest improvements based on this lesson.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Python's exception hierarchy.
- ✅ Stack unwinding.
- ✅ `try`, `except`, `else`, and `finally`.
- ✅ Raising and re-raising exceptions.
- ✅ Exception chaining.
- ✅ Layered exception handling.
- ✅ Production exception handling strategies.
- ✅ Common anti-patterns and best practices.

______________________________________________________________________

# Next Lesson

**File:** [58-production-python-part-03-custom-exceptions](58-production-python-part-03-custom-exceptions.md)

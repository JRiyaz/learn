# 6. Exception Handling & Error Management

**Previous:** [5. Python Collections & Data Structures](./05-python-collections.md)

**Next:** [7. Python Modules, Packages & Virtual Environments](./07-python-modules-packages.md)

______________________________________________________________________

## Objectives

By the end of this chapter, you should be able to:

- Explain Python's exception hierarchy.
- Understand `BaseException` vs `Exception`.
- Use `try`, `except`, `else`, and `finally` correctly.
- Raise exceptions explicitly.
- Create custom exception classes.
- Understand exception chaining with `raise from`.
- Explain bare `raise` vs `raise SomeException`.
- Understand traceback information.
- Distinguish expected business errors from programming errors.
- Design exception handling appropriate for backend services.
- Avoid common exception-handling mistakes.
- Explain how exceptions interact with cleanup and context managers.

______________________________________________________________________

# 1. What Is an Exception?

An exception represents an abnormal condition detected during program execution.

Example:

```python
result = 10 / 0
```

raises:

```text
ZeroDivisionError
```

Instead of allowing the application to terminate immediately, Python provides mechanisms for handling exceptions.

______________________________________________________________________

# 2. Exception Hierarchy

Python exceptions are organized into a class hierarchy.

At the top is:

```python
BaseException
```

Important branches include:

```text
BaseException
├── Exception
│   ├── ValueError
│   ├── TypeError
│   ├── KeyError
│   ├── IndexError
│   ├── RuntimeError
│   └── ...
├── KeyboardInterrupt
├── SystemExit
└── GeneratorExit
```

Application code normally catches subclasses of:

```python
Exception
```

rather than `BaseException`.

______________________________________________________________________

# 3. Why Not Catch `BaseException`?

Consider:

```python
try:
    ...
except BaseException:
    ...
```

This also catches exceptions such as:

- `KeyboardInterrupt`
- `SystemExit`
- `GeneratorExit`

These generally represent control-flow signals that application code should not silently consume.

Prefer:

```python
except Exception:
    ...
```

when a broad catch is genuinely required.

Even then, broad catches should have a clear purpose.

______________________________________________________________________

# 4. Basic `try` / `except`

Example:

```python
try:
    value = int(user_input)
except ValueError:
    value = 0
```

If conversion fails, the `ValueError` handler executes.

Only put operations that can reasonably raise the expected exception inside the `try` block.

Avoid wrapping an entire large function in one giant `try`.

______________________________________________________________________

# 5. Multiple Exception Types

You can handle several exception types:

```python
try:
    process()
except (ValueError, TypeError):
    handle_invalid_input()
```

This is useful when different exception types require the same recovery behavior.

______________________________________________________________________

# 6. Different Handlers

Different errors can have different handling:

```python
try:
    process()
except ValueError:
    handle_validation_error()
except KeyError:
    handle_missing_key()
except TimeoutError:
    handle_timeout()
```

Order matters when exception classes have inheritance relationships.

Catch more specific exceptions before broader ones.

______________________________________________________________________

# 7. Exception Matching

Suppose:

```python
class AppError(Exception):
    pass


class ValidationError(AppError):
    pass
```

Then:

```python
try:
    ...
except AppError:
    ...
```

also catches:

```python
ValidationError
```

Therefore, if you need different behavior:

```python
except ValidationError:
    ...
except AppError:
    ...
```

is the appropriate order.

______________________________________________________________________

# 8. The `else` Block

`else` executes only when the `try` block completes without raising an exception.

Example:

```python
try:
    value = int(user_input)
except ValueError:
    handle_invalid_input()
else:
    process(value)
```

This can make exception boundaries clearer.

The `else` block is not executed if an exception is raised in the `try`.

______________________________________________________________________

# 9. The `finally` Block

`finally` is used for cleanup.

```python
resource = acquire()

try:
    use(resource)
finally:
    release(resource)
```

The cleanup code executes whether the protected operation succeeds or raises.

Context managers provide a cleaner reusable abstraction for many such cases.

______________________________________________________________________

# 10. Complete Exception Structure

Python supports:

```python
try:
    operation()
except SomeError:
    recover()
else:
    success()
finally:
    cleanup()
```

Execution:

### Success

```text
try → else → finally
```

### Exception handled

```text
try → except → finally
```

### Exception not handled

```text
try → finally → exception propagates
```

This is an important interview concept.

______________________________________________________________________

# 11. Raising Exceptions

You can explicitly raise an exception:

```python
if age < 0:
    raise ValueError("age cannot be negative")
```

Raising exceptions allows invalid states to be rejected at the point where they are detected.

______________________________________________________________________

# 12. Raising an Existing Exception

Inside an exception handler:

```python
try:
    operation()
except ValueError:
    raise
```

A bare:

```python
raise
```

re-raises the currently handled exception while preserving its traceback context.

This is different from constructing a new exception.

______________________________________________________________________

# 13. `raise` vs `raise e`

Consider:

```python
try:
    operation()
except Exception as e:
    raise
```

This preserves the active exception's traceback.

Using:

```python
raise e
```

re-raises the exception object explicitly and can alter how traceback information is presented.

For simple re-raising, prefer:

```python
raise
```

______________________________________________________________________

# 14. Exception Chaining

Suppose a low-level exception occurs:

```python
try:
    load_from_database()
except DatabaseError as exc:
    raise UserRepositoryError("Could not load user") from exc
```

The new exception preserves the original exception as its cause.

This is called explicit exception chaining.

It helps explain:

```text
high-level failure
        caused by
low-level failure
```

without exposing low-level implementation details directly to every caller.

______________________________________________________________________

# 15. `raise from None`

Sometimes you intentionally want to hide implicit exception context:

```python
try:
    value = int(data)
except ValueError:
    raise ValidationError("Invalid value") from None
```

This suppresses the displayed exception context.

Use this when the lower-level exception is not useful to the caller and the higher-level error is sufficient.

Do not use it to hide useful debugging information indiscriminately.

______________________________________________________________________

# 16. Custom Exceptions

Create domain-specific exceptions when callers need to distinguish application failures.

Example:

```python
class ApplicationError(Exception):
    pass


class UserNotFoundError(ApplicationError):
    pass


class UserAlreadyExistsError(ApplicationError):
    pass
```

Usage:

```python
raise UserNotFoundError("User does not exist")
```

This is clearer than raising generic `Exception`.

______________________________________________________________________

# 17. Custom Exception Hierarchy

A useful hierarchy can look like:

```python
class ApplicationError(Exception):
    pass


class ValidationError(ApplicationError):
    pass


class NotFoundError(ApplicationError):
    pass


class ConflictError(ApplicationError):
    pass
```

Higher layers can catch:

```python
except ApplicationError:
    ...
```

while specific callers can catch:

```python
except NotFoundError:
    ...
```

This creates a controlled error taxonomy.

______________________________________________________________________

# 18. Exception Messages

Good exception messages explain:

- What failed
- Which operation failed
- Relevant non-sensitive context

Example:

```python
raise ValueError(
    f"Invalid page size: {page_size}"
)
```

Avoid putting:

- Passwords
- Access tokens
- API keys
- Sensitive personal data
- Full secrets

into exception messages or logs.

______________________________________________________________________

# 19. Tracebacks

A traceback shows the path through the program that led to an exception.

Example:

```text
Traceback (most recent call last):
  ...
ValueError: invalid value
```

Tracebacks are valuable for debugging because they identify:

- Exception type
- Exception message
- Call stack
- Source location

Do not destroy useful traceback context unnecessarily.

______________________________________________________________________

# 20. Logging Exceptions

In backend applications, logging should capture sufficient diagnostic information.

For example, Python's logging module provides:

```python
logger.exception("Failed to process request")
```

inside an exception handler.

This records the exception and traceback.

Avoid:

```python
logger.error(str(exc))
```

when you need the traceback as well.

Also avoid logging sensitive values.

______________________________________________________________________

# 21. Catch Only What You Can Handle

This is a key principle.

Bad:

```python
try:
    process_order()
except Exception:
    return None
```

This can hide:

- Programming bugs
- Database failures
- Network failures
- Configuration errors
- Unexpected states

Better:

```python
try:
    process_order()
except PaymentTimeout:
    retry_or_fail_gracefully()
```

Catch an exception when you have a meaningful recovery or translation strategy.

______________________________________________________________________

# 22. Broad Exception Handling

Sometimes:

```python
except Exception:
```

is appropriate.

Examples include:

- A top-level API boundary
- Worker boundary
- Background task supervisor
- Logging boundary
- Process-level error reporting

Even there, you should generally:

1. Log the failure appropriately.
1. Preserve diagnostic information.
1. Return a safe response if necessary.
1. Avoid silently continuing in a corrupted state.

______________________________________________________________________

# 23. Exception Handling at Layer Boundaries

A backend application may have:

```text
API
 ↓
Service
 ↓
Repository
 ↓
Database
```

A low-level exception does not always need to propagate unchanged through every layer.

For example:

```python
DatabaseTimeout
```

could become:

```python
UserRepositoryError
```

and eventually an appropriate API-level response.

Use exception translation when it creates a useful abstraction boundary.

______________________________________________________________________

# 24. Don't Over-Translate Exceptions

Do not convert every exception into:

```python
ApplicationError("Something went wrong")
```

because that destroys useful distinctions.

Good translation preserves the important meaning:

```python
DatabaseTimeout
    ↓
RepositoryUnavailable
```

rather than:

```python
Everything
    ↓
GenericError
```

______________________________________________________________________

# 25. Business Exceptions vs Programming Errors

This distinction is extremely important.

### Business/domain error

An expected condition in application behavior.

Examples:

```text
UserNotFound
InsufficientBalance
OrderAlreadyCancelled
InvalidStateTransition
```

These may be handled deliberately.

### Programming error

A bug or invalid assumption in the implementation.

Examples:

```text
AttributeError
IndexError
NameError
unexpected TypeError
```

These generally should not be silently converted into normal business responses.

______________________________________________________________________

# 26. Exception Handling and Transactions

Consider:

```python
try:
    create_order()
    charge_payment()
except Exception:
    rollback()
    raise
```

The transaction boundary must be designed carefully.

If an external payment succeeds but the database transaction fails, a simple rollback cannot undo the external payment.

This is why distributed transaction behavior, idempotency and compensation are important backend concepts.

______________________________________________________________________

# 27. Exception Handling and Context Managers

Context managers are often better for cleanup:

```python
with transaction():
    create_order()
    update_inventory()
```

The context manager can perform commit/rollback logic based on whether the block raised an exception.

This separates lifecycle handling from business logic.

______________________________________________________________________

# 28. Exception Handling in Generators

Generators can use normal exception handling:

```python
def records():
    try:
        yield load_records()
    finally:
        cleanup()
```

Closing or exhausting the generator can trigger cleanup paths.

For resource lifecycle management, a context manager is often clearer.

______________________________________________________________________

# 29. Exceptions in Async Code

Exceptions raised inside an async function can be handled normally:

```python
async def fetch_user():
    try:
        return await repository.get_user()
    except TimeoutError:
        ...
```

When using concurrent task APIs, understand whether exceptions:

- Propagate immediately
- Are collected
- Cancel sibling tasks
- Are wrapped or aggregated

The exact behavior depends on the concurrency primitive being used.

At interview level, understand that asynchronous exception propagation must be considered across task boundaries.

______________________________________________________________________

# 30. Exception Handling in Background Workers

A worker loop should not accidentally die because one task fails.

For example:

```python
while True:
    task = get_task()

    try:
        process(task)
    except RetryableError:
        schedule_retry(task)
    except Exception:
        record_failure(task)
```

The worker boundary may need broad exception handling, but individual failures should be classified appropriately.

______________________________________________________________________

# 31. Retryable vs Non-Retryable Errors

Not every exception should trigger a retry.

Potentially retryable:

- Temporary network timeout
- Transient service unavailable
- Temporary database connection issue

Usually not automatically retryable:

- Validation error
- Authentication failure
- Permission denial
- Invalid request
- Duplicate business operation

Retry policy should consider:

- Idempotency
- Backoff
- Maximum attempts
- Timeout
- Error type
- System load

______________________________________________________________________

# 32. Common Exception-Handling Mistakes

## Mistake 1 — Bare `except`

```python
try:
    ...
except:
    ...
```

This catches `BaseException` subclasses such as `KeyboardInterrupt` and `SystemExit`.

Prefer a specific exception or:

```python
except Exception:
```

when a broad application boundary is justified.

______________________________________________________________________

## Mistake 2 — Swallowing errors

```python
except Exception:
    pass
```

This hides failures and makes debugging difficult.

______________________________________________________________________

## Mistake 3 — Returning `None` for every error

```python
except Exception:
    return None
```

This makes failure indistinguishable from a legitimate `None` result.

______________________________________________________________________

## Mistake 4 — Catching too much

A huge `try` block makes it unclear which operation failed and can accidentally handle unrelated errors.

______________________________________________________________________

## Mistake 5 — Logging and re-raising at every layer

This can create duplicate log entries.

Decide which layer owns logging and which layer owns exception translation.

______________________________________________________________________

## Mistake 6 — Logging sensitive data

Never include secrets or sensitive information in exception messages or logs.

______________________________________________________________________

# 33. Backend Error-Handling Strategy

A practical backend strategy is:

### At the low-level boundary

Raise meaningful technical exceptions.

### At the service boundary

Translate technical failures into domain-level failures when appropriate.

### At the API boundary

Map known domain errors to appropriate HTTP responses.

### At the application boundary

Log unexpected failures with traceback information and return a safe generic response.

The exact architecture depends on the application.

______________________________________________________________________

# 34. Interview Questions & Answers

## Q1. What is an exception?

**Answer:**

An exception is an object representing an abnormal condition during execution.

Python raises exceptions when operations fail and provides `try`/`except` mechanisms for handling them.

______________________________________________________________________

## Q2. What is the difference between `BaseException` and `Exception`?

**Answer:**

`Exception` is the base class for most application-level exceptions.

`BaseException` also includes control-flow exceptions such as `KeyboardInterrupt`, `SystemExit`, and `GeneratorExit`.

Application code should generally catch `Exception`, not `BaseException`.

______________________________________________________________________

## Q3. Explain `try`, `except`, `else`, and `finally`.

**Answer:**

- `try`: code that may raise.
- `except`: handles selected exceptions.
- `else`: executes if `try` succeeds.
- `finally`: executes when leaving the construct and is commonly used for cleanup.

______________________________________________________________________

## Q4. When does `else` execute?

**Answer:**

Only when the `try` block completes without raising an exception.

______________________________________________________________________

## Q5. When does `finally` execute?

**Answer:**

It executes when leaving the `try` statement, including normal completion and exception paths.

______________________________________________________________________

## Q6. What is the difference between `raise` and `raise e`?

**Answer:**

A bare `raise` re-raises the currently handled exception and preserves the active traceback context.

`raise e` explicitly raises the exception object and can change traceback presentation.

For simple re-raising inside an exception handler, use:

```python
raise
```

______________________________________________________________________

## Q7. What is exception chaining?

**Answer:**

Exception chaining connects a higher-level exception to the original cause:

```python
except DatabaseError as exc:
    raise RepositoryError("Database operation failed") from exc
```

It preserves useful causal information.

______________________________________________________________________

## Q8. What does `raise from None` do?

**Answer:**

It suppresses the displayed exception context from the lower-level exception.

It is useful when the higher-level exception is the intended public error representation.

______________________________________________________________________

## Q9. Why create custom exceptions?

**Answer:**

Custom exceptions provide meaningful application-specific error types that callers can catch and handle precisely.

______________________________________________________________________

## Q10. Why shouldn't you use `except:` casually?

**Answer:**

Bare `except` catches `BaseException`, including control-flow exceptions such as `KeyboardInterrupt` and `SystemExit`.

It can also hide serious failures.

______________________________________________________________________

## Q11. When is `except Exception` appropriate?

**Answer:**

It can be appropriate at a deliberate boundary such as an API handler, worker supervisor or logging boundary where
unexpected failures must be captured.

It should not be used indiscriminately around ordinary business logic.

______________________________________________________________________

## Q12. Why should `try` blocks be small?

**Answer:**

A small `try` block makes it clear which operation can raise the expected exception.

A large block can accidentally catch errors from unrelated operations and make debugging harder.

______________________________________________________________________

## Q13. How should exceptions be handled across backend layers?

**Answer:**

Technical exceptions can be translated into domain-level exceptions at appropriate abstraction boundaries, and domain
exceptions can be mapped to API-level responses.

Do not unnecessarily destroy the original meaning.

______________________________________________________________________

## Q14. What is the difference between a business exception and a programming error?

**Answer:**

A business exception represents an expected domain condition, such as insufficient balance.

A programming error generally indicates a bug or violated implementation assumption and should usually not be silently
treated as a normal business response.

______________________________________________________________________

## Q15. How should exceptions be logged?

**Answer:**

At the appropriate application boundary, log enough context and traceback information for diagnosis without exposing
sensitive data.

For Python logging, `logger.exception()` is useful inside an exception handler when traceback information is needed.

______________________________________________________________________

## Q16. Should every exception be retried?

**Answer:**

No.

Retries should be limited to appropriate transient failures and must consider idempotency, backoff, timeout and maximum
attempts.

______________________________________________________________________

## Q17. Why can retrying a non-idempotent operation be dangerous?

**Answer:**

The first operation may have succeeded even if the client received a timeout.

Retrying it could create a duplicate order, payment or other side effect.

______________________________________________________________________

## Q18. Why is returning `None` from every exception handler bad?

**Answer:**

It hides failures and makes a genuine `None` result indistinguishable from an error.

Callers lose the ability to handle different failure cases correctly.

______________________________________________________________________

## Q19. Why is `except Exception: pass` dangerous?

**Answer:**

It silently discards failures, making production problems difficult to detect and debug.

______________________________________________________________________

## Q20. How are context managers related to exception handling?

**Answer:**

A context manager's `__exit__` method runs when leaving the context, including exception paths.

This allows it to perform cleanup or commit/rollback logic reliably.

______________________________________________________________________

# 35. Scenario-Based Questions

## Scenario 1 — API Returns 500 for Invalid User Input

An endpoint does:

```python
try:
    age = int(payload["age"])
except Exception:
    raise InternalServerError()
```

A client sends:

```text
"age": "abc"
```

**Question:** What is wrong?

**Answer:**

The code catches too broadly and treats a validation problem as an internal server failure.

A better design is to catch the specific conversion/validation failure and return the application's appropriate
validation response.

______________________________________________________________________

## Scenario 2 — Worker Dies After One Failed Task

A worker loop is:

```python
while True:
    task = get_task()
    process(task)
```

One task raises an exception and the worker stops.

**Question:** What would you consider?

**Answer:**

Introduce an intentional worker-level exception boundary:

```python
while True:
    task = get_task()

    try:
        process(task)
    except RetryableError:
        schedule_retry(task)
    except Exception:
        record_failure(task)
```

The exact policy should distinguish retryable, permanent and unexpected failures.

______________________________________________________________________

## Scenario 3 — Database Error Leaks Into API

A repository raises:

```python
psycopg2.OperationalError
```

and the API layer exposes its raw message to the client.

**Question:** Why is this undesirable?

**Answer:**

It leaks infrastructure details and may expose sensitive information.

Translate the technical error into an application-level error and return a safe client-facing message while preserving
diagnostic details internally.

______________________________________________________________________

## Scenario 4 — Payment Retry Creates Duplicate Payment

A payment request times out. The application retries automatically.

The original request actually succeeded.

**Question:** What should the design include?

**Answer:**

Use an idempotency strategy so repeated requests with the same logical operation do not create duplicate side effects.

Also classify which failures are safe to retry and use appropriate backoff.

______________________________________________________________________

## Scenario 5 — Cleanup Is Skipped

Code:

```python
resource = acquire()

try:
    process(resource)
except Exception:
    return
release(resource)
```

**Question:** What happens if `process()` fails?

**Answer:**

The function returns before `release(resource)`, causing a resource leak.

Use `finally`:

```python
resource = acquire()

try:
    process(resource)
finally:
    release(resource)
```

or, preferably, a context manager when the resource supports one.

______________________________________________________________________

# 36. Practice Exercises

## Exercise 1 — Specific Exception Handling

Write a function that converts a value to an integer.

Requirements:

- Handle invalid numeric input.
- Do not catch unrelated exceptions.
- Return a meaningful result or raise a domain-specific validation exception.

______________________________________________________________________

## Exercise 2 — Custom Exception Hierarchy

Create:

```python
ApplicationError
ValidationError
NotFoundError
ConflictError
```

Make the three specific errors inherit from `ApplicationError`.

Demonstrate catching both a specific exception and the common base class.

______________________________________________________________________

## Exercise 3 — Exception Translation

Simulate:

```text
DatabaseError
    ↓
RepositoryError
    ↓
API response
```

Use:

```python
raise ... from ...
```

to preserve the causal relationship.

______________________________________________________________________

## Exercise 4 — Cleanup

Write code that acquires a resource and guarantees cleanup even when processing raises an exception.

Implement it first with `try/finally`.

Then rewrite it using a context manager.

______________________________________________________________________

## Exercise 5 — Worker Error Policy

Design a worker loop that classifies:

- Retryable error
- Permanent business error
- Unexpected programming error

Explain what should happen for each.

______________________________________________________________________

## Exercise 6 — Retry Safety

Design a hypothetical order-creation API that may time out.

Explain how you would prevent a retry from creating duplicate orders.

Focus on:

- Idempotency
- Retry conditions
- Timeouts
- Backoff
- Maximum attempts

______________________________________________________________________

# 37. Quick Revision

| Concept | Key Point |
|---|---|
| Exception | Runtime error/abnormal condition object |
| `BaseException` | Root of Python exception hierarchy |
| `Exception` | Base for most application exceptions |
| `try` | Code that may raise |
| `except` | Handles selected exceptions |
| `else` | Runs when `try` succeeds |
| `finally` | Cleanup/finalization path |
| `raise` | Explicitly raises an exception |
| Bare `raise` | Re-raises active exception |
| `raise from` | Explicit exception chaining |
| `raise from None` | Suppresses displayed context |
| Custom exception | Application-specific error type |
| Traceback | Execution path leading to exception |
| `logger.exception()` | Logs exception with traceback |
| Specific catch | Preferred when recovery is known |
| Broad catch | Appropriate only at deliberate boundaries |
| Business error | Expected domain condition |
| Programming error | Bug/invalid implementation assumption |
| Retryable error | Failure that may succeed later |
| Idempotency | Safe repeated logical operation |
| Context manager | Structured setup/cleanup |

______________________________________________________________________

# 38. Completion Checklist

Before moving to File 7, make sure you can explain:

- [ ] What an exception is
- [ ] Python exception hierarchy
- [ ] `BaseException`
- [ ] `Exception`
- [ ] Why `BaseException` is rarely caught
- [ ] `try`
- [ ] `except`
- [ ] `else`
- [ ] `finally`
- [ ] Exception matching
- [ ] Specific vs broad exception handling
- [ ] `raise`
- [ ] Bare `raise`
- [ ] `raise e`
- [ ] Exception chaining
- [ ] `raise from`
- [ ] `raise from None`
- [ ] Custom exception classes
- [ ] Custom exception hierarchy
- [ ] Tracebacks
- [ ] Logging exceptions
- [ ] Exception boundaries
- [ ] Exception translation
- [ ] Business errors vs programming errors
- [ ] Exceptions and transactions
- [ ] Exceptions and context managers
- [ ] Exceptions in async code
- [ ] Worker exception handling
- [ ] Retryable vs non-retryable errors
- [ ] Idempotency
- [ ] Common exception-handling mistakes
- [ ] Secure exception messages/logging

______________________________________________________________________

# 39. Interview Readiness Test

Without looking at the notes, answer these aloud:

1. Explain Python's exception hierarchy.
1. What is the difference between `BaseException` and `Exception`?
1. Why should you generally avoid catching `BaseException`?
1. Explain `try`, `except`, `else`, and `finally`.
1. When does `else` execute?
1. When does `finally` execute?
1. Why should a `try` block generally be small?
1. What is the difference between `raise` and `raise e`?
1. What is exception chaining?
1. Why use `raise ... from ...`?
1. What does `raise from None` do?
1. Why create custom exceptions?
1. When is `except Exception` appropriate?
1. Why is `except Exception: pass` dangerous?
1. How should exceptions be translated across backend layers?
1. What is the difference between a business exception and a programming error?
1. How should exceptions be logged?
1. Should every exception be retried?
1. Why is retrying a non-idempotent operation dangerous?
1. How would you design exception handling in a background worker?
1. How do context managers help with exception safety?
1. How would you prevent database implementation details from leaking through an API?

If you can answer these clearly and implement the exercises without relying heavily on the notes, this chapter is
complete.

______________________________________________________________________

**Previous:** [5. Python Collections & Data Structures](./05-python-collections.md)

**Next:** [7. Python Modules, Packages & Virtual Environments](./07-python-modules-packages.md)

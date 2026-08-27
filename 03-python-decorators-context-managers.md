# 3. Decorators & Context Managers

**Previous:** [2. Functions & Functional Programming](./02-python-functions.md)

**Next:** [4. Iterators, Generators & Lazy Evaluation](./04-python-iterators-generators.md)

______________________________________________________________________

## Objectives

By the end of this chapter, you should be able to:

- Explain what decorators are and why they work.
- Write function decorators from scratch.
- Preserve wrapped-function metadata with `functools.wraps`.
- Understand decorator execution vs decorated-function execution.
- Write decorators that accept arguments.
- Explain multiple decorators and their order.
- Understand closures and how decorators use them.
- Understand class-based decorators at interview level.
- Explain context managers and the `with` statement.
- Understand `__enter__` and `__exit__`.
- Create custom context managers.
- Use `contextlib.contextmanager`.
- Handle exceptions and cleanup correctly.
- Explain practical backend use cases for decorators and context managers.

______________________________________________________________________

# 1. What Is a Decorator?

A decorator is a callable that takes another callable and returns a callable with additional or modified behavior.

Example:

```python
def log_call(func):
    def wrapper():
        print("Calling function")
        result = func()
        print("Function completed")
        return result

    return wrapper
```

It can be applied using:

```python
@log_call
def greet():
    print("Hello")
```

Conceptually:

```python
greet = log_call(greet)
```

The `@decorator` syntax is therefore syntactic sugar for reassignment.

______________________________________________________________________

# 2. Why Decorators Matter

Decorators are useful when the same behavior must be applied consistently around many functions.

Common examples:

- Logging
- Authentication
- Authorization
- Timing
- Metrics
- Caching
- Retries
- Validation
- Transactions
- Tracing
- Rate limiting

Backend frameworks use decorators heavily for routing and configuration.

______________________________________________________________________

# 3. Basic Decorator Pattern

A typical decorator looks like:

```python
from functools import wraps


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Before
        result = func(*args, **kwargs)
        # After
        return result

    return wrapper
```

The important pieces are:

1. Receive the original function.
1. Define a wrapper.
1. Accept the original function's arguments.
1. Call the original function.
1. Return the result.
1. Return the wrapper.

______________________________________________________________________

# 4. Logging Decorator

```python
from functools import wraps


def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")

        result = func(*args, **kwargs)

        print(f"Completed {func.__name__}")

        return result

    return wrapper
```

Usage:

```python
@log_call
def add(a, b):
    return a + b
```

Now:

```python
add(10, 20)
```

executes logging around the original function.

______________________________________________________________________

# 5. `*args` and `**kwargs` in Decorators

A decorator often does not know the signature of the function it is wrapping.

Therefore:

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
```

allows the wrapper to accept arbitrary positional and keyword arguments.

This is one reason understanding function arguments is important before learning decorators.

______________________________________________________________________

# 6. The Metadata Problem

Consider:

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
```

After:

```python
@decorator
def greet():
    """Say hello."""
    return "hello"
```

the decorated name may expose metadata belonging to `wrapper`.

For example:

```python
print(greet.__name__)
```

may produce:

```text
wrapper
```

This can hurt:

- Debugging
- Documentation
- Introspection
- Framework tooling

______________________________________________________________________

# 7. `functools.wraps`

Use:

```python
from functools import wraps


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
```

`wraps` preserves useful metadata from the original function.

Important attributes include:

- `__name__`
- `__qualname__`
- `__doc__`
- `__module__`
- `__annotations__`

It also sets `__wrapped__`, which helps introspection tools access the original callable.

______________________________________________________________________

# 8. Decorator Execution vs Function Execution

Consider:

```python
def decorator(func):
    print("Decorating", func.__name__)

    def wrapper(*args, **kwargs):
        print("Calling")
        return func(*args, **kwargs)

    return wrapper


@decorator
def greet():
    print("Hello")
```

The decoration step occurs when the function definition is executed.

Therefore:

```text
Decorating greet
```

happens while the module/function definition is being processed.

The wrapper body executes later when:

```python
greet()
```

is called.

This distinction is a common interview question.

______________________________________________________________________

# 9. Preserving Return Values

A decorator should normally preserve the wrapped function's return value.

Correct:

```python
def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return wrapper
```

If the wrapper forgets to return:

```python
def wrapper(*args, **kwargs):
    func(*args, **kwargs)
```

the decorated function will return `None`.

This is a common source of subtle bugs.

______________________________________________________________________

# 10. Decorators and Exceptions

A decorator can observe or handle exceptions:

```python
def log_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print("Function failed")
            raise

    return wrapper
```

The bare:

```python
raise
```

re-raises the original exception.

In production applications, use structured logging instead of `print`.

______________________________________________________________________

# 11. Decorators With Arguments

Sometimes the decorator itself needs configuration:

```python
@retry(max_attempts=3)
def call_service():
    ...
```

This requires another function layer.

Example:

```python
from functools import wraps


def retry(max_attempts):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise

        return wrapper

    return decorator
```

______________________________________________________________________

# 12. Three Layers of a Parameterized Decorator

For:

```python
@retry(max_attempts=3)
def call_service():
    ...
```

there are three conceptual layers.

### Layer 1 — Configuration

```python
retry(max_attempts=3)
```

returns a decorator.

### Layer 2 — Decoration

The returned decorator receives:

```python
call_service
```

### Layer 3 — Invocation

The resulting wrapper executes when:

```python
call_service()
```

is called.

______________________________________________________________________

# 13. Multiple Decorators

You can stack decorators:

```python
@decorator_a
@decorator_b
def process():
    ...
```

This is equivalent to:

```python
process = decorator_a(
    decorator_b(process)
)
```

Therefore `decorator_b` is applied first, and `decorator_a` wraps the result.

______________________________________________________________________

# 14. Decorator Execution Order

If:

```python
@first
@second
def work():
    print("work")
```

then the call structure is:

```text
first wrapper
    ↓
second wrapper
    ↓
work
    ↓
second wrapper after
    ↓
first wrapper after
```

This is why decorator order matters.

It is particularly important when combining:

- Authentication
- Caching
- Transactions
- Metrics
- Retry

______________________________________________________________________

# 15. Closures and Decorators

Decorators commonly use closures.

Example:

```python
def make_multiplier(multiplier):
    def multiply(value):
        return value * multiplier

    return multiply
```

The returned function retains access to:

```text
multiplier
```

from its enclosing scope.

Decorators use the same principle:

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
```

`wrapper` retains access to `func`.

______________________________________________________________________

# 16. Closure State

A closure can retain state:

```python
def counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment
```

Usage:

```python
c = counter()

print(c())
print(c())
```

Output:

```text
1
2
```

The enclosing state remains available to the returned function.

______________________________________________________________________

# 17. Class-Based Decorators

A class can be callable if it implements `__call__`.

```python
class LogCalls:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Calling")
        return self.func(*args, **kwargs)
```

Usage:

```python
@LogCalls
def greet():
    return "hello"
```

Conceptually:

```python
greet = LogCalls(greet)
```

Class-based decorators are useful when explicit object state is convenient.

______________________________________________________________________

# 18. Decorator State and Concurrency

A decorator can maintain mutable state:

```python
def count_calls(func):
    count = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        return func(*args, **kwargs)

    return wrapper
```

In a multi-threaded or concurrent backend, that state may be accessed by multiple executions.

Do not assume closure state is automatically thread-safe.

Consider:

- Locks
- Atomic operations
- Per-request state
- External counters
- Metrics libraries

depending on the requirement.

______________________________________________________________________

# 19. Decorators and Async Functions

An important backend consideration is whether the wrapped function is synchronous or asynchronous.

For an async function, an async wrapper may be required:

```python
def decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)

    return wrapper
```

A decorator that performs asynchronous work must itself be able to `await`.

A production decorator may need separate handling for sync and async callables.

______________________________________________________________________

# 20. Common Decorator Mistakes

### Forgetting `wraps`

Metadata becomes misleading.

### Forgetting to return

The decorated function unexpectedly returns `None`.

### Incorrect async handling

The wrapper does not correctly await the coroutine.

### Swallowing exceptions

Bad:

```python
try:
    return func()
except Exception:
    return None
```

This can hide production failures.

### Retrying non-idempotent operations

Retrying an operation such as order creation or payment can create duplicates if the operation is not designed for safe
retry.

______________________________________________________________________

# 21. What Is a Context Manager?

A context manager controls setup and cleanup around a block of code.

The familiar syntax is:

```python
with resource() as value:
    use(value)
```

Common examples:

```python
with open("file.txt") as file:
    data = file.read()
```

The file is closed when the context is exited.

______________________________________________________________________

# 22. Why Context Managers Matter

Context managers are useful for resources with a clear lifecycle:

- Files
- Database transactions
- Locks
- Connections
- Temporary resources
- Sessions

The general lifecycle is:

```text
Acquire
   ↓
Use resource
   ↓
Release / cleanup
```

They provide a clean abstraction for setup and cleanup.

______________________________________________________________________

# 23. `__enter__` and `__exit__`

A class can implement the context-manager protocol:

```python
class Resource:
    def __enter__(self):
        print("Acquire")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Release")
```

Usage:

```python
with Resource() as resource:
    print("Using resource")
```

Conceptually:

1. Create the context manager.
1. Call `__enter__`.
1. Execute the `with` body.
1. Call `__exit__`.

______________________________________________________________________

# 24. What Does `__enter__` Return?

The value returned by `__enter__` is assigned to the variable after `as`.

```python
with Resource() as resource:
    ...
```

The variable receives:

```python
Resource().__enter__()
```

It does not have to be the context-manager object itself.

Example:

```python
class Database:
    def __enter__(self):
        return self.connection
```

______________________________________________________________________

# 25. What Does `__exit__` Receive?

The common signature is:

```python
def __exit__(self, exc_type, exc_value, traceback):
    ...
```

If the body succeeds:

```text
exc_type     = None
exc_value    = None
traceback    = None
```

If an exception occurs, these contain information about the exception.

______________________________________________________________________

# 26. Exception Suppression

`__exit__` can suppress an exception by returning a truthy value.

Example:

```python
class IgnoreError:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return True
```

Then:

```python
with IgnoreError():
    raise ValueError("problem")
```

the exception can be suppressed.

This should be used carefully.

Unexpected application exceptions should normally propagate.

______________________________________________________________________

# 27. Cleanup During Exceptions

A major benefit of context managers is that `__exit__` runs when leaving the context, including exception paths.

This makes context managers appropriate for deterministic cleanup.

For example:

```python
with resource:
    risky_operation()
```

can ensure resource cleanup even if `risky_operation()` raises.

______________________________________________________________________

# 28. Custom Database Transaction Context Manager

A simplified transaction manager could look like:

```python
class DatabaseTransaction:
    def __enter__(self):
        self.transaction = begin_transaction()
        return self.transaction

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            commit()
        else:
            rollback()

        return False
```

Usage:

```python
with DatabaseTransaction():
    create_user()
    create_order()
```

If the block succeeds:

```text
commit
```

If it raises:

```text
rollback
```

The exact implementation depends on the database library.

______________________________________________________________________

# 29. `contextlib.contextmanager`

You do not always need to implement `__enter__` and `__exit__` manually.

`contextlib.contextmanager` allows a generator-based context manager.

```python
from contextlib import contextmanager


@contextmanager
def resource():
    print("Acquire")

    try:
        yield "resource"
    finally:
        print("Release")
```

Usage:

```python
with resource() as value:
    print(value)
```

The code before `yield` represents setup.

The code after `yield`, inside `finally`, represents cleanup.

______________________________________________________________________

# 30. Why `finally` Matters

Use:

```python
try:
    yield resource
finally:
    cleanup()
```

rather than relying only on normal execution.

The `finally` block executes on both successful and exceptional exits.

This is particularly important for:

- Connections
- Locks
- Files
- Temporary resources
- Transactions

______________________________________________________________________

# 31. Context Managers and Locks

Locks are a classic use case.

Instead of:

```python
lock.acquire()

try:
    update_shared_state()
finally:
    lock.release()
```

use:

```python
with lock:
    update_shared_state()
```

The context-manager form makes ownership and release explicit.

______________________________________________________________________

# 32. Context Managers vs `try/finally`

Manual lifecycle management:

```python
resource = acquire()

try:
    use(resource)
finally:
    release(resource)
```

Context-manager approach:

```python
with managed_resource() as resource:
    use(resource)
```

The second form is more reusable and communicates lifecycle intent clearly.

______________________________________________________________________

# 33. Decorators vs Context Managers

They solve different problems.

### Decorator

Wraps a callable:

```python
@log_call
def process():
    ...
```

Good for behavior around function invocation.

### Context manager

Wraps a block:

```python
with transaction():
    ...
```

Good for resource lifecycle around a block of code.

Sometimes both can be used together, but they should not be confused.

______________________________________________________________________

# 34. Backend Relevance

### Decorators

Common in:

- API routing
- Authentication
- Authorization
- Logging
- Metrics
- Tracing
- Retry
- Caching
- Transactions

### Context managers

Common in:

- Database transactions
- Database sessions
- Locks
- Files
- Connections
- Temporary resources

Understanding both helps when reading framework and infrastructure code.

______________________________________________________________________

# 35. Interview Questions & Answers

## Q1. What is a decorator?

**Answer:**

A decorator is a callable that receives another callable and returns a callable with additional or modified behavior.

```python
@log_call
def process():
    ...
```

is conceptually:

```python
process = log_call(process)
```

______________________________________________________________________

## Q2. Why do decorators commonly use `*args` and `**kwargs`?

**Answer:**

The decorator may wrap functions with different signatures.

Using:

```python
def wrapper(*args, **kwargs):
```

allows the wrapper to forward arbitrary positional and keyword arguments.

______________________________________________________________________

## Q3. Why should `functools.wraps` be used?

**Answer:**

It preserves useful metadata from the original function, such as its name, documentation and annotations.

Without it, the wrapper can obscure the original callable during debugging and introspection.

______________________________________________________________________

## Q4. What is the difference between decorator execution and wrapper execution?

**Answer:**

The decorator executes when the decorated function definition is evaluated.

The wrapper executes when the resulting decorated function is called.

______________________________________________________________________

## Q5. Explain a decorator with arguments.

**Answer:**

A parameterized decorator requires an outer function for configuration.

For:

```python
@retry(max_attempts=3)
def call():
    ...
```

the outer function receives the configuration and returns the actual decorator. That decorator receives `call` and
returns the wrapper.

______________________________________________________________________

## Q6. What is the order of stacked decorators?

**Answer:**

For:

```python
@a
@b
def f():
    ...
```

Python applies them as:

```python
f = a(b(f))
```

So `b` is applied first and `a` wraps the result.

______________________________________________________________________

## Q7. How do decorators use closures?

**Answer:**

The wrapper function closes over the original function:

```python
def decorator(func):
    def wrapper():
        return func()
    return wrapper
```

The wrapper retains access to `func` after `decorator()` has returned.

______________________________________________________________________

## Q8. Can a class be used as a decorator?

**Answer:**

Yes.

A class can receive the function in `__init__` and implement `__call__` to behave as a callable wrapper.

______________________________________________________________________

## Q9. What should you consider when decorating an async function?

**Answer:**

The wrapper must understand coroutine behavior.

If the decorator needs to await the original function, the wrapper should be async:

```python
async def wrapper(*args, **kwargs):
    return await func(*args, **kwargs)
```

______________________________________________________________________

## Q10. What is a context manager?

**Answer:**

A context manager defines setup and cleanup behavior around a block used with `with`.

It is commonly used for files, locks, database transactions and connections.

______________________________________________________________________

## Q11. What are `__enter__` and `__exit__`?

**Answer:**

`__enter__` runs when entering the `with` block and returns the value assigned after `as`.

`__exit__` runs when leaving the block and receives exception information if an exception occurred.

______________________________________________________________________

## Q12. When is `__exit__` called?

**Answer:**

It is called when leaving the `with` block, including when the block raises an exception.

This makes it suitable for deterministic cleanup.

______________________________________________________________________

## Q13. Can `__exit__` suppress an exception?

**Answer:**

Yes.

Returning a truthy value from `__exit__` suppresses the exception.

This should be used carefully because accidentally swallowing exceptions can hide failures.

______________________________________________________________________

## Q14. What is `contextlib.contextmanager`?

**Answer:**

It allows a context manager to be written using a generator.

Code before `yield` represents setup, while cleanup can be placed in a `finally` block around the `yield`.

______________________________________________________________________

## Q15. Why is `finally` important?

**Answer:**

`finally` executes during normal completion and exception paths, making it appropriate for cleanup.

______________________________________________________________________

## Q16. What is the difference between a decorator and a context manager?

**Answer:**

A decorator wraps a callable.

A context manager wraps a block of code and manages a resource or lifecycle around that block.

______________________________________________________________________

## Q17. Why is retrying inside a decorator not always safe?

**Answer:**

The operation may not be idempotent.

Retrying a read is different from retrying an operation that creates an order or payment.

Retries need to consider idempotency, error classification, timeout and backoff.

______________________________________________________________________

## Q18. What happens if a decorator forgets to return the wrapped function's result?

**Answer:**

The decorated function can unexpectedly return `None`.

The wrapper normally needs:

```python
return func(*args, **kwargs)
```

unless intentionally changing the return contract.

______________________________________________________________________

## Q19. Can decorator state cause concurrency problems?

**Answer:**

Yes.

Mutable state in a closure or decorator object can be accessed by multiple threads/tasks.

It may require synchronization or a different design.

______________________________________________________________________

## Q20. Give backend examples of context managers.

**Answer:**

Examples include:

- Database transactions
- Database sessions
- Locks
- Files
- Network connections
- Temporary resources

The key benefit is reliable lifecycle management.

______________________________________________________________________

# 36. Scenario-Based Questions

## Scenario 1 — Decorator Breaks Framework Metadata

A decorator wraps a FastAPI endpoint and framework introspection behaves incorrectly.

**Question:** What would you inspect?

**Answer:**

Check whether the decorator uses:

```python
@wraps(func)
```

Also verify that the decorator preserves the expected sync/async behavior and does not unintentionally change the
callable contract.

______________________________________________________________________

## Scenario 2 — Async Decorator Returns a Coroutine

You use a normal wrapper around an async function.

**Question:** What can go wrong?

**Answer:**

The wrapper returns the coroutine produced by the original function.

If the decorator itself needs to perform asynchronous work or await the result, it needs an async wrapper:

```python
async def wrapper(*args, **kwargs):
    return await func(*args, **kwargs)
```

______________________________________________________________________

## Scenario 3 — Retry Creates Duplicate Orders

An endpoint retries after a timeout. The first request actually succeeded, but the response was lost. The retry creates
another order.

**Question:** What is the underlying problem?

**Answer:**

The operation is not safely idempotent.

A robust design should consider:

- Idempotency keys
- Duplicate detection
- Transaction boundaries
- Which errors are retryable
- Timeout semantics
- Backoff

A retry loop alone is not sufficient.

______________________________________________________________________

## Scenario 4 — Database Connection Is Not Released

A developer manually acquires a connection:

```python
connection = acquire_connection()

process(connection)
```

but cleanup is not guaranteed if `process()` raises.

**Question:** What design would help?

**Answer:**

Use a context manager that owns the connection lifecycle:

```python
with connection_manager() as connection:
    process(connection)
```

The context manager can guarantee cleanup on normal and exceptional exits.

______________________________________________________________________

## Scenario 5 — Lock Remains Held

Code does:

```python
lock.acquire()

update_state()

lock.release()
```

`update_state()` raises an exception.

**Question:** What happens?

**Answer:**

`lock.release()` is skipped and the lock may remain held.

Prefer:

```python
with lock:
    update_state()
```

so the lock is released when leaving the block.

______________________________________________________________________

# 37. Practice Exercises

## Exercise 1 — Logging Decorator

Implement:

```python
@log_call
def add(a, b):
    return a + b
```

Requirements:

- Log the function name before execution.
- Log it after execution.
- Preserve the return value.
- Preserve metadata using `functools.wraps`.

______________________________________________________________________

## Exercise 2 — Timing Decorator

Implement:

```python
@measure_time
def process():
    ...
```

Requirements:

- Measure execution duration.
- Log the duration.
- Preserve the return value.
- Preserve metadata.

______________________________________________________________________

## Exercise 3 — Parameterized Decorator

Implement:

```python
@retry(max_attempts=3)
def unstable_operation():
    ...
```

Requirements:

- Retry on an exception.
- Stop after the configured number of attempts.
- Re-raise the final exception.
- Explain why arbitrary operations should not automatically be retried.

______________________________________________________________________

## Exercise 4 — Custom Context Manager

Create:

```python
with Timer() as timer:
    expensive_operation()
```

Requirements:

- Record start time in `__enter__`.
- Calculate elapsed time in `__exit__`.
- Display/log the elapsed time.
- Do not suppress exceptions.

______________________________________________________________________

## Exercise 5 — Generator-Based Context Manager

Rewrite the timer using:

```python
@contextmanager
def timer():
    ...
```

Ensure cleanup happens in `finally`.

______________________________________________________________________

## Exercise 6 — Transaction Context Manager

Design:

```python
with transaction():
    create_user()
    update_account()
```

Behavior:

- Begin on entry.
- Commit if successful.
- Roll back if an exception occurs.
- Never silently suppress unexpected exceptions.

______________________________________________________________________

# 38. Quick Revision

| Concept | Key Point |
|---|---|
| Decorator | Wraps/configures a callable |
| `@decorator` | Equivalent to reassignment |
| Wrapper | Callable returned by a decorator |
| `*args/**kwargs` | Generic argument forwarding |
| `functools.wraps` | Preserves wrapped-function metadata |
| Parameterized decorator | Outer function returns a decorator |
| Stacked decorators | `@a @b f` becomes `a(b(f))` |
| Closure | Inner function retains enclosing bindings |
| Class decorator | Callable object can act as decorator |
| Async decorator | Must account for coroutine execution |
| Context manager | Controls setup/cleanup around a block |
| `with` | Enters and exits a context |
| `__enter__` | Setup / value returned after `as` |
| `__exit__` | Cleanup / exception handling |
| `contextmanager` | Generator-based context manager |
| `finally` | Reliable cleanup path |
| Exception suppression | Truthy `__exit__` can suppress |
| Decorator vs context manager | Callable behavior vs block/resource lifecycle |

______________________________________________________________________

# 39. Completion Checklist

Before moving to File 4, make sure you can explain:

- [ ] What a decorator is
- [ ] `@decorator` syntax
- [ ] Basic decorator implementation
- [ ] `*args` and `**kwargs` in wrappers
- [ ] Why `functools.wraps` matters
- [ ] `__wrapped__`
- [ ] Decorator execution timing
- [ ] Wrapper execution timing
- [ ] Preserving return values
- [ ] Exception handling in decorators
- [ ] Parameterized decorators
- [ ] Multiple decorators
- [ ] Decorator order
- [ ] Closures
- [ ] Closure state
- [ ] Class-based decorators
- [ ] Decorator state and concurrency
- [ ] Sync vs async decorators
- [ ] Common decorator mistakes
- [ ] Context-manager protocol
- [ ] `with`
- [ ] `__enter__`
- [ ] `__exit__`
- [ ] Exception handling in `__exit__`
- [ ] Exception suppression
- [ ] `contextlib.contextmanager`
- [ ] `try/finally`
- [ ] Database transaction context managers
- [ ] Lock context managers
- [ ] Decorator vs context manager
- [ ] Retry/idempotency considerations

______________________________________________________________________

# 40. Interview Readiness Test

Without looking at the notes, answer these aloud:

1. What is a decorator?
1. What does `@decorator` translate to?
1. Why do decorator wrappers commonly use `*args` and `**kwargs`?
1. Why should you use `functools.wraps`?
1. When does decorator code execute?
1. When does wrapper code execute?
1. How do you create a parameterized decorator?
1. Explain the order of two stacked decorators.
1. How do closures enable decorators?
1. Can a class be a decorator?
1. What changes when decorating an async function?
1. What is a context manager?
1. What do `__enter__` and `__exit__` do?
1. What does the `as` variable receive?
1. How does `__exit__` receive exception information?
1. How can a context manager suppress an exception?
1. Why is `finally` important for cleanup?
1. When would you use a context manager instead of a decorator?
1. Why is a retry decorator potentially dangerous for non-idempotent operations?
1. How would you design a database transaction context manager?

If you can answer these clearly and implement the exercises without relying on the notes, this chapter is complete.

______________________________________________________________________

**Previous:** [2. Functions & Functional Programming](./02-python-functions.md)

**Next:** [4. Iterators, Generators & Lazy Evaluation](./04-python-iterators-generators.md)

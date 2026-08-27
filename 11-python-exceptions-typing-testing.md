# 11. Typing & Testing

**Previous:** [10. Python Concurrency & AsyncIO](./10-python-concurrency.md)

**Next:** [12. HTTP, TCP/IP, TLS & Networking](./12-http-networking.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain why type hints are useful in Python backend development.
- Understand common typing constructs used in production code.
- Use `Optional`, `Union`, `Literal`, `TypedDict`, generics, and `Protocol`.
- Understand the difference between runtime behavior and static type checking.
- Write clear type annotations for functions and classes.
- Understand pytest's basic execution and assertion model.
- Create and use fixtures.
- Understand mocking and when to use it.
- Understand `monkeypatch`.
- Distinguish unit, integration, and API testing.
- Design a practical backend testing strategy.
- Identify when a test is too coupled to implementation details.
- Answer common interview questions around Python typing and testing.

______________________________________________________________________

# 1. Why Type Hints Matter

Python is dynamically typed, but production Python code can still benefit significantly from type annotations.

Example:

```python
def calculate_total(price: float, quantity: int) -> float:
    return price * quantity
```

Type hints can improve:

- Readability
- IDE support
- Static analysis
- Refactoring
- Documentation
- Team collaboration

They do not automatically enforce types at runtime.

______________________________________________________________________

# 2. Type Hints Are Not Runtime Validation

Consider:

```python
def add(a: int, b: int) -> int:
    return a + b
```

The annotation does not automatically prevent:

```python
add("hello", "world")
```

Whether this fails depends on the operation itself.

Static type checkers can identify incorrect calls before runtime.

This distinction is important:

```text
Type hints
    ↓
Static analysis / developer tooling

Runtime validation
    ↓
Explicit validation / framework / library
```

______________________________________________________________________

# 3. Function Annotations

Basic annotations:

```python
def get_user(user_id: int) -> dict:
    ...
```

You can annotate:

- Parameters
- Return values
- Variables
- Class attributes

Example:

```python
user_id: int = 10
name: str = "Riyaz"
```

______________________________________________________________________

# 4. `Optional`

`Optional[T]` means a value can be `T` or `None`.

Example:

```python
from typing import Optional


def find_user(user_id: int) -> Optional[str]:
    ...
```

Modern Python can also express this as:

```python
def find_user(user_id: int) -> str | None:
    ...
```

Conceptually:

```text
Optional[str]
=
str | None
```

______________________________________________________________________

# 5. `Union`

`Union` means a value may have one of several types.

Example:

```python
from typing import Union


def parse_id(value: Union[int, str]):
    ...
```

Modern Python can express this as:

```python
def parse_id(value: int | str):
    ...
```

Prefer modern syntax when the project's Python version supports it.

______________________________________________________________________

# 6. `Literal`

`Literal` restricts a type to specific values.

Example:

```python
from typing import Literal


Status = Literal["pending", "completed", "failed"]
```

Then:

```python
def update_status(status: Status):
    ...
```

This communicates that arbitrary strings are not valid values.

Useful for:

- Status fields
- Modes
- Configuration options
- API parameters

______________________________________________________________________

# 7. `TypedDict`

A `TypedDict` describes the expected structure of a dictionary.

Example:

```python
from typing import TypedDict


class UserData(TypedDict):
    id: int
    name: str
    email: str
```

Then:

```python
def create_user(data: UserData):
    ...
```

This is especially useful when working with dictionary-shaped data.

Important:

> `TypedDict` does not create a runtime dictionary subclass with validation.

It primarily provides information to static type checkers.

______________________________________________________________________

# 8. Generics

Generics allow code to work with multiple types while preserving type relationships.

Example:

```python
from typing import TypeVar


T = TypeVar("T")


def first(items: list[T]) -> T:
    return items[0]
```

If passed:

```python
first([1, 2, 3])
```

the type checker can infer:

```text
int
```

For:

```python
first(["a", "b"])
```

it can infer:

```text
str
```

______________________________________________________________________

# 9. Generic Classes

Example:

```python
from typing import Generic, TypeVar


T = TypeVar("T")


class Repository(Generic[T]):
    def get(self, item_id: int) -> T:
        ...
```

A concrete repository can be conceptually:

```python
Repository[User]
Repository[Order]
```

Generics are particularly useful for reusable infrastructure components.

______________________________________________________________________

# 10. `Protocol`

A Protocol describes a structural interface.

Example:

```python
from typing import Protocol


class Publisher(Protocol):
    def publish(self, event: str) -> None:
        ...
```

A class can satisfy this contract without explicitly inheriting from `Publisher`.

This aligns naturally with Python's duck-typing style.

______________________________________________________________________

# 11. Why Protocols Help Backend Code

Suppose:

```python
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
```

A Protocol can describe only the behavior the service needs.

Production:

```text
PostgresUserRepository
```

Tests:

```text
FakeUserRepository
```

Both can satisfy the same structural contract.

This reduces coupling to concrete implementations.

______________________________________________________________________

# 12. Typing and API Models

Backend frameworks frequently combine type annotations with request/response models.

For example:

```python
def get_user(user_id: int) -> UserResponse:
    ...
```

Type annotations can communicate the expected API contract.

However, type annotations alone should not be confused with runtime input validation.

______________________________________________________________________

# 13. Static Type Checkers

Common static analysis tools include:

- mypy
- pyright

A type checker analyzes annotations without necessarily executing the application.

Example:

```python
name: str = 10
```

A static type checker can flag this as a type error.

The exact rules depend on the checker and configuration.

______________________________________________________________________

# 14. Gradual Typing

Python allows projects to adopt typing incrementally.

A legacy codebase can start with:

```python
def calculate_total(price, quantity):
    ...
```

and gradually move toward:

```python
def calculate_total(price: float, quantity: int) -> float:
    ...
```

You do not need to type every part of a large codebase simultaneously.

A practical strategy is to type:

- Public APIs
- Core business logic
- Shared utilities
- Frequently modified modules
- Complex data structures

______________________________________________________________________

# 15. Type Aliases

Type aliases can make complicated types easier to understand.

Example:

```python
UserId = int
```

or:

```python
UserIds = list[int]
```

More complex examples can use aliases to improve readability.

Use meaningful names rather than aliases that hide important type information.

______________________________________________________________________

# 16. pytest

`pytest` is a popular Python testing framework.

A basic test:

```python
def add(a, b):
    return a + b


def test_add():
    assert add(2, 3) == 5
```

Run tests with:

```bash
pytest
```

The test passes if the assertion succeeds.

______________________________________________________________________

# 17. Test Discovery

pytest automatically discovers tests according to naming conventions.

Common patterns include:

```text
test_*.py
*_test.py
```

and functions/classes with test-oriented names.

Following standard naming conventions makes test execution predictable.

______________________________________________________________________

# 18. Assertions

pytest commonly uses plain Python assertions:

```python
assert result == expected
```

Examples:

```python
assert response.status_code == 200
assert user.name == "Riyaz"
assert len(items) == 3
```

pytest provides useful failure information when assertions fail.

______________________________________________________________________

# 19. Testing Exceptions

Use:

```python
import pytest


def divide(a, b):
    if b == 0:
        raise ValueError("cannot divide by zero")


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

You can also inspect the exception when the exact message or attributes matter.

______________________________________________________________________

# 20. Fixtures

Fixtures provide reusable test setup.

Example:

```python
import pytest


@pytest.fixture
def user():
    return {
        "id": 1,
        "name": "Riyaz",
    }


def test_user(user):
    assert user["id"] == 1
```

Fixtures help avoid repeating setup logic across tests.

______________________________________________________________________

# 21. Fixture Scope

Fixtures can have different scopes, depending on how often they should be created.

Common scopes include:

- `function`
- `class`
- `module`
- `package`
- `session`

For example:

```python
@pytest.fixture(scope="module")
def database():
    ...
```

Choose the narrowest scope that makes sense unless there is a clear reason to share state.

______________________________________________________________________

# 22. Fixture Cleanup

Fixtures can use `yield` for setup and cleanup.

Example:

```python
@pytest.fixture
def resource():
    connection = create_connection()

    yield connection

    connection.close()
```

This is useful for resources such as:

- Database connections
- Temporary files
- Test servers
- Clients

______________________________________________________________________

# 23. Fixture Composition

Fixtures can depend on other fixtures.

Example:

```python
@pytest.fixture
def repository():
    ...


@pytest.fixture
def service(repository):
    return UserService(repository)
```

This can create a reusable dependency graph for tests.

Avoid creating excessively complicated fixture hierarchies because they can make tests difficult to understand.

______________________________________________________________________

# 24. Parameterized Tests

pytest supports parameterization.

Example:

```python
import pytest


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, 2),
        (2, 4),
        (3, 6),
    ],
)
def test_double(value, expected):
    assert value * 2 == expected
```

This allows one test function to cover multiple cases.

______________________________________________________________________

# 25. Mocking

Mocking replaces a dependency with a controlled test double.

Example:

```python
from unittest.mock import Mock


repository = Mock()
repository.get_by_id.return_value = {"id": 1}
```

Then code using the repository can be tested without calling a real database.

______________________________________________________________________

# 26. Why Mock?

Mocking can help when a dependency is:

- Slow
- Expensive
- External
- Non-deterministic
- Difficult to reproduce
- Unavailable during unit tests

Examples:

- Payment providers
- External HTTP APIs
- Email services
- Message brokers

______________________________________________________________________

# 27. Mocking Too Much

Mocking everything is not a good testing strategy.

If a test mocks every dependency and verifies every internal method call, it can become tightly coupled to
implementation details.

Then a harmless refactoring can break many tests.

Prefer testing observable behavior where possible.

______________________________________________________________________

# 28. `unittest.mock`

Python's standard library includes:

```python
unittest.mock
```

Useful tools include:

```python
Mock
MagicMock
patch
AsyncMock
```

`AsyncMock` is particularly useful when testing async functions.

______________________________________________________________________

# 29. Patching

Example:

```python
from unittest.mock import patch


with patch("module.send_email") as mock_send:
    ...
```

The important rule is:

> Patch where the dependency is looked up, not necessarily where it was originally defined.

This is a frequent Python testing interview question.

______________________________________________________________________

# 30. `monkeypatch`

pytest provides the `monkeypatch` fixture.

It can temporarily change:

- Attributes
- Environment variables
- Dictionary values
- Working directory
- Functions

Example:

```python
def test_env(monkeypatch):
    monkeypatch.setenv("APP_MODE", "test")

    assert os.getenv("APP_MODE") == "test"
```

pytest automatically restores the change after the test.

______________________________________________________________________

# 31. Mock vs Monkeypatch

They are related but not identical.

### Mock

Primarily creates a test double and records/intercepts interactions.

### Monkeypatch

Temporarily changes an object, environment variable, mapping or other state for the duration of a test.

They can be used together.

______________________________________________________________________

# 32. Unit Testing

A unit test focuses on a relatively small unit of behavior.

Example:

```text
OrderService.calculate_total()
```

A unit test should ideally be:

- Fast
- Deterministic
- Isolated
- Easy to diagnose

Dependencies may be replaced with fakes or mocks when appropriate.

______________________________________________________________________

# 33. Integration Testing

Integration tests verify that multiple components work together.

Examples:

```text
Application
    ↓
PostgreSQL
```

or:

```text
Application
    ↓
Redis
```

Integration tests are slower than pure unit tests but catch problems that isolated unit tests cannot.

______________________________________________________________________

# 34. API Testing

API tests exercise an application through its HTTP interface.

For example:

```text
HTTP request
    ↓
API endpoint
    ↓
Service
    ↓
Database
```

API tests can verify:

- Status codes
- Response body
- Headers
- Authentication
- Validation
- Error behavior
- Database effects

______________________________________________________________________

# 35. Unit vs Integration vs API Tests

| Test type | Scope | Typical speed |
|---|---|---|
| Unit | Small isolated behavior | Fast |
| Integration | Multiple components | Medium |
| API | External HTTP contract | Medium/Slow |

A healthy test suite usually contains a mix rather than only one category.

______________________________________________________________________

# 36. Testing Strategy

A practical backend testing strategy can look like:

```text
Many
  ↓
Unit tests
  ↓
Integration tests
  ↓
API / end-to-end tests
  ↓
Few
```

The exact ratio depends on the application.

The principle is:

> Keep fast tests numerous and use broader tests where integration behavior matters.

______________________________________________________________________

# 37. What Should You Test?

Focus on behavior that matters.

Examples:

### Business rules

```text
Discount calculation
Order state transitions
Permission checks
```

### Error behavior

```text
Invalid input
Missing resource
Unauthorized operation
External failure
```

### Data behavior

```text
Repository queries
Transactions
Constraints
```

### API behavior

```text
Request validation
Response schema
Status codes
Authentication
```

______________________________________________________________________

# 38. What Should You Avoid Testing?

Avoid tests that merely duplicate implementation details.

For example, if a function internally calls:

```python
helper_a()
helper_b()
helper_c()
```

you usually should not assert every internal call unless those interactions are part of the behavior that matters.

Prefer:

```text
Input
  ↓
Behavior
  ↓
Expected result
```

______________________________________________________________________

# 39. Test Isolation

Tests should not unexpectedly depend on:

- Execution order
- Another test's mutable state
- Developer machine configuration
- Production services
- Current time
- Randomness

Isolation improves reliability and makes failures easier to reproduce.

______________________________________________________________________

# 40. Testing External Services

Do not make your unit-test suite depend on real third-party services.

Instead, use:

- Mocks
- Fakes
- Local test servers
- Contract tests
- Dedicated integration environments

For critical integrations, broader integration/contract testing can validate that your assumptions about the external
service remain correct.

______________________________________________________________________

# 41. Testing Database Code

Database tests should cover both behavior and integration.

Examples:

```text
Correct query behavior
Transaction behavior
Constraints
Rollback behavior
Concurrency-sensitive behavior
```

For integration tests, use an isolated test database or controlled database environment rather than accidentally sharing
production data.

______________________________________________________________________

# 42. Testing Async Code

Async code needs async-aware testing.

For example, pytest can be extended with async testing tools such as:

```text
pytest-asyncio
```

Tests should correctly await asynchronous operations.

Do not test an async function by accidentally creating a coroutine and never awaiting it.

______________________________________________________________________

# 43. Testing FastAPI

API tests can exercise FastAPI applications through a test client.

Typical coverage includes:

```text
Request
  ↓
Validation
  ↓
Dependency injection
  ↓
Business logic
  ↓
Response
```

Depending on the test's purpose, database and external dependencies can be real test integrations or controlled test
doubles.

______________________________________________________________________

# 44. Test Naming

Good test names explain the behavior.

Prefer:

```python
def test_create_user_rejects_duplicate_email():
    ...
```

over:

```python
def test_user_1():
    ...
```

A failing test name should help you understand what broke without opening the implementation immediately.

______________________________________________________________________

# 45. Arrange, Act, Assert

A common test structure is:

### Arrange

Prepare inputs and dependencies.

### Act

Execute the behavior.

### Assert

Verify the result.

Example:

```python
def test_total():
    # Arrange
    order = Order(...)

    # Act
    total = order.calculate_total()

    # Assert
    assert total == 100
```

This makes tests easy to scan.

______________________________________________________________________

# 46. Test Doubles

Common test-double categories include:

### Dummy

Passed around but not actually used.

### Stub

Provides predefined responses.

### Fake

Working simplified implementation.

### Mock

Records or verifies interactions.

### Spy

Observes calls/interactions while allowing behavior to occur.

You do not need to use these terms mechanically, but understanding the distinctions helps in interviews.

______________________________________________________________________

# 47. Code Coverage

Coverage measures which code is executed by tests.

High coverage does not automatically mean high-quality tests.

For example:

```python
def divide(a, b):
    ...
```

A test can execute every line without checking important edge cases.

Use coverage as a signal, not as the sole measure of test quality.

______________________________________________________________________

# 48. Testing Error Paths

Senior engineers should explicitly test failure paths.

Examples:

- Invalid input
- Database failure
- Timeout
- Authentication failure
- Duplicate resource
- External service error
- Unexpected dependency response

Production failures often occur outside the happy path.

______________________________________________________________________

# 49. Testing Retries and Timeouts

If application code has retry behavior:

```text
Attempt 1 → failure
Attempt 2 → failure
Attempt 3 → success
```

tests should verify:

- Number of attempts
- Delay/backoff behavior where relevant
- Final failure behavior
- Exception propagation
- Idempotency implications

Similarly, timeout behavior should be tested without making tests unnecessarily slow.

______________________________________________________________________

# 50. Testing Strategy for a Senior Backend Engineer

When asked:

> "How do you test a backend service?"

A strong answer should include:

1. Unit tests for business logic.
1. Integration tests for database/cache/message-broker interactions.
1. API tests for HTTP contracts.
1. Mocks/fakes for expensive or external dependencies where appropriate.
1. Failure-path testing.
1. Async testing where required.
1. Isolation and deterministic tests.
1. CI execution.
1. Coverage as a supporting metric rather than the only quality measure.

______________________________________________________________________

# 51. Common Testing Mistakes

## Mistake 1 — Testing implementation instead of behavior

Tests become brittle.

______________________________________________________________________

## Mistake 2 — Mocking everything

Tests can pass while the real components do not work together.

______________________________________________________________________

## Mistake 3 — No integration tests

Database, serialization, configuration and integration issues can escape detection.

______________________________________________________________________

## Mistake 4 — Testing only happy paths

Production bugs often happen on failure paths.

______________________________________________________________________

## Mistake 5 — Shared mutable test state

Tests become order-dependent.

______________________________________________________________________

## Mistake 6 — Overly broad fixtures

A huge fixture hierarchy makes tests difficult to understand.

______________________________________________________________________

## Mistake 7 — Ignoring async behavior

An unawaited coroutine can make a test appear to work while testing almost nothing.

______________________________________________________________________

# 52. Interview Questions & Answers

## Q1. Why use type hints in Python?

**Answer:**

Type hints improve readability, IDE support, static analysis, refactoring and documentation.

They do not automatically enforce types at runtime.

______________________________________________________________________

## Q2. Are Python type hints enforced at runtime?

**Answer:**

Not by Python itself.

Runtime validation requires explicit checks or a framework/library that performs validation.

______________________________________________________________________

## Q3. What is `Optional[str]`?

**Answer:**

It represents a value that can be either `str` or `None`.

Modern Python can express it as:

```python
str | None
```

______________________________________________________________________

## Q4. What is `Union`?

**Answer:**

It represents a type that can contain one of several types.

For example:

```python
int | str
```

______________________________________________________________________

## Q5. What is `Literal`?

**Answer:**

`Literal` restricts a value to specific allowed literal values.

Example:

```python
Literal["pending", "completed"]
```

______________________________________________________________________

## Q6. What is `TypedDict`?

**Answer:**

`TypedDict` describes the expected keys and value types of a dictionary-shaped object for static type checking.

It does not itself provide runtime validation.

______________________________________________________________________

## Q7. What are generics?

**Answer:**

Generics allow reusable code to preserve relationships between input and output types.

For example:

```python
def first(items: list[T]) -> T:
    ...
```

______________________________________________________________________

## Q8. What is a Protocol?

**Answer:**

A Protocol describes a structural interface.

A class can satisfy it by providing compatible behavior without explicitly inheriting from the Protocol.

______________________________________________________________________

## Q9. ABC vs Protocol?

**Answer:**

An ABC is generally an explicit inheritance-based contract.

A Protocol provides structural typing, allowing compatible classes to satisfy the contract without inheritance.

______________________________________________________________________

## Q10. What is pytest?

**Answer:**

pytest is a Python testing framework that provides simple assertions, fixtures, parameterization and a large ecosystem
of plugins.

______________________________________________________________________

## Q11. What is a pytest fixture?

**Answer:**

A fixture provides reusable test setup and optionally cleanup.

It can be injected into test functions by declaring it as an argument.

______________________________________________________________________

## Q12. Why use fixture scopes?

**Answer:**

Fixture scope controls how often the fixture is created.

It can reduce expensive setup, but overly broad scopes can introduce shared-state problems.

______________________________________________________________________

## Q13. What is mocking?

**Answer:**

Mocking replaces a dependency with a controlled test double so the test can isolate the behavior under test.

______________________________________________________________________

## Q14. When should you mock?

**Answer:**

Mock dependencies when they are expensive, external, slow, non-deterministic or when isolation is important.

Do not mock everything.

______________________________________________________________________

## Q15. What is monkeypatch?

**Answer:**

pytest's `monkeypatch` fixture temporarily modifies attributes, environment variables, mappings and similar state during
a test and restores the changes afterward.

______________________________________________________________________

## Q16. Mock vs monkeypatch?

**Answer:**

A mock is primarily a test double used to control behavior and/or inspect interactions.

Monkeypatch is a mechanism for temporarily replacing or modifying something during a test.

______________________________________________________________________

## Q17. What does "patch where it is looked up" mean?

**Answer:**

If a module imports a dependency into its own namespace, patch the name used by that module rather than blindly patching
the original definition.

The goal is to replace the object where the code under test resolves it.

______________________________________________________________________

## Q18. Unit vs integration testing?

**Answer:**

Unit tests focus on isolated behavior and are generally fast.

Integration tests verify interactions between multiple real components, such as an application and database.

______________________________________________________________________

## Q19. What is API testing?

**Answer:**

API testing exercises the application through its HTTP interface and verifies request handling, validation, responses,
status codes and relevant integration behavior.

______________________________________________________________________

## Q20. What makes a good unit test?

**Answer:**

It should generally be:

- Focused
- Fast
- Deterministic
- Isolated
- Easy to understand
- Focused on observable behavior

______________________________________________________________________

## Q21. Why is mocking everything bad?

**Answer:**

It can make tests tightly coupled to implementation details and can allow integration bugs to go undetected.

______________________________________________________________________

## Q22. What is Arrange-Act-Assert?

**Answer:**

It is a common test structure:

```text
Arrange → prepare
Act     → execute
Assert  → verify
```

It makes tests easier to read.

______________________________________________________________________

## Q23. What is a fake?

**Answer:**

A fake is a simplified working implementation used in tests.

For example, an in-memory repository can act as a fake database repository.

______________________________________________________________________

## Q24. What is a stub?

**Answer:**

A stub provides predefined responses needed by the test.

______________________________________________________________________

## Q25. What is a mock?

**Answer:**

A mock is a test double that can provide controlled behavior and record/verify interactions.

______________________________________________________________________

## Q26. What is test isolation?

**Answer:**

Tests should not unexpectedly depend on another test's state, execution order, environment or external services.

______________________________________________________________________

## Q27. Is high code coverage enough?

**Answer:**

No.

Coverage indicates which code executed, not whether the tests verify important behavior and edge cases.

______________________________________________________________________

## Q28. How would you test an external payment provider?

**Answer:**

Use mocks/fakes for unit tests, then use controlled integration or contract tests to verify the real integration
behavior where appropriate.

______________________________________________________________________

## Q29. How would you test database code?

**Answer:**

Use unit tests for business logic around the repository and integration tests against an isolated test database for real
query, transaction and constraint behavior.

______________________________________________________________________

## Q30. How do you test async code?

**Answer:**

Use async-aware test support and ensure coroutines are actually awaited.

Verify both successful and failure/cancellation behavior where relevant.

______________________________________________________________________

## Q31. What should a senior backend engineer include in a testing strategy?

**Answer:**

A combination of unit, integration and API tests; appropriate test doubles; failure-path testing; deterministic
isolation; async testing; CI execution; and coverage as a supporting metric.

______________________________________________________________________

## Q32. How do you test retry logic?

**Answer:**

Control the dependency so specific attempts fail or succeed, then verify the number of attempts, final result/error and
relevant backoff/idempotency behavior.

______________________________________________________________________

## Q33. How do you test timeout behavior without making tests slow?

**Answer:**

Mock or control the dependency's timing/failure behavior rather than actually waiting for long real-world timeouts.

______________________________________________________________________

## Q34. What is the difference between testing behavior and implementation?

**Answer:**

Behavior-focused tests verify what the system should do.

Implementation-focused tests verify internal details such as exact helper calls.

Behavior-focused tests are generally more resilient to refactoring.

______________________________________________________________________

# 53. Scenario-Based Questions

## Scenario 1 — Type Hint vs Runtime Validation

You have:

```python
def create_user(age: int):
    ...
```

A client sends:

```json
{"age": "abc"}
```

**Question:** Will the type hint automatically reject it?

**Answer:**

Not by Python itself.

Runtime validation must be provided by the API framework or explicit validation logic.

______________________________________________________________________

## Scenario 2 — Typed Dictionary

An API receives:

```python
{
    "id": 10,
    "name": "Riyaz",
    "email": "..."
}
```

Developers frequently access incorrect keys and values.

**Question:** What typing feature can describe this dictionary structure?

**Answer:**

`TypedDict`.

It allows static type checkers to understand expected keys and value types.

______________________________________________________________________

## Scenario 3 — Repository Testing

`UserService` calls a PostgreSQL repository.

Unit tests are slow because every test connects to PostgreSQL.

**Question:** What would you do?

**Answer:**

Use a fake or mock repository for unit tests.

Then maintain separate integration tests against an isolated database to verify actual database behavior.

______________________________________________________________________

## Scenario 4 — Over-Mocked Test

A test verifies:

```python
repository.get_by_id.assert_called_once_with(1)
validator.validate.assert_called_once()
mapper.map.assert_called_once()
```

A harmless refactoring breaks the test.

**Question:** What is wrong?

**Answer:**

The test is heavily coupled to implementation details.

Where possible, verify the observable behavior rather than every internal call.

______________________________________________________________________

## Scenario 5 — Shared Fixture State

Tests pass individually but fail when the entire suite runs.

**Question:** What could be happening?

**Answer:**

Possible causes include:

- Shared mutable fixture state
- Incorrect fixture scope
- Tests depending on execution order
- Global state not being reset

Inspect fixture scopes and test isolation.

______________________________________________________________________

## Scenario 6 — Async Test

A test contains:

```python
def test_fetch_user():
    result = fetch_user()
    assert result["id"] == 1
```

where `fetch_user()` is async.

**Question:** What is wrong?

**Answer:**

Calling the async function produces a coroutine rather than the final result.

The test must use async-aware testing and await the coroutine.

______________________________________________________________________

## Scenario 7 — Patch Doesn't Work

The developer patches:

```python
external_module.send_email
```

but the code under test imported it directly:

```python
from external_module import send_email
```

The real function is still called.

**Question:** Why?

**Answer:**

The code under test looks up `send_email` in its own module namespace.

Patch the name where it is looked up.

______________________________________________________________________

## Scenario 8 — High Coverage, Production Bugs

The project has 95% code coverage but frequently discovers production failures.

**Question:** How is that possible?

**Answer:**

Coverage only indicates that code executed.

Tests may still fail to verify:

- Important business rules
- Failure paths
- Integration behavior
- Edge cases
- Concurrency behavior
- External-service interactions

Coverage is a metric, not proof of correctness.

______________________________________________________________________

## Scenario 9 — Testing a Payment API

A payment provider is slow and occasionally unavailable.

**Question:** How would you structure tests?

**Answer:**

Use controlled mocks/fakes for unit tests.

Use dedicated integration/contract tests to validate the actual provider integration.

Test:

- Success
- Timeout
- Provider failure
- Retry
- Duplicate request/idempotency behavior
- Invalid responses

______________________________________________________________________

# 54. Practice Exercises

## Exercise 1 — Type a Service

Take a small backend service and add type annotations for:

- Inputs
- Outputs
- Class attributes
- Repository dependencies
- Configuration values

Run a static type checker and fix the important errors.

______________________________________________________________________

## Exercise 2 — `TypedDict`

Define a `TypedDict` for:

```text
User
Order
API response metadata
```

Use them in function signatures.

______________________________________________________________________

## Exercise 3 — Generics

Implement:

```python
Repository[T]
```

with:

```python
get(id) -> T
```

Create conceptual user and order repositories.

______________________________________________________________________

## Exercise 4 — Protocol

Define:

```python
RepositoryProtocol
```

and create:

```text
PostgresRepository
FakeRepository
```

Use both with a service.

______________________________________________________________________

## Exercise 5 — pytest Fixtures

Create fixtures for:

- Test user
- Repository
- Service

Compose the fixtures so the service receives the repository.

______________________________________________________________________

## Exercise 6 — Parameterized Testing

Write parameterized tests for a function that validates:

- Valid input
- Empty input
- Boundary values
- Invalid input

______________________________________________________________________

## Exercise 7 — Mocking

Create a service that calls an external email client.

Unit test the service without sending a real email.

Verify the important behavior without asserting unnecessary internal details.

______________________________________________________________________

## Exercise 8 — Monkeypatch

Write a function that reads an environment variable.

Use `monkeypatch` to test different environment configurations.

______________________________________________________________________

## Exercise 9 — Integration Test

Create a repository integration test against an isolated test database.

Verify:

- Insert
- Read
- Update
- Transaction rollback

______________________________________________________________________

## Exercise 10 — API Test

Create an API endpoint and test:

- Success response
- Validation failure
- Missing resource
- Unauthorized request
- Internal dependency failure

______________________________________________________________________

## Exercise 11 — Async Test

Create an async service.

Write tests for:

- Success
- Timeout
- Cancellation
- Dependency failure

Ensure all coroutines are correctly awaited.

______________________________________________________________________

## Exercise 12 — Testing Strategy Review

Take a backend project and classify its tests into:

```text
Unit
Integration
API
```

Identify:

- Over-mocked tests
- Missing failure-path tests
- Missing integration tests
- Shared-state problems
- Important untested business rules

______________________________________________________________________

# 55. Quick Revision

| Concept | Key Point |
|---|---|
| Type hint | Documents expected types and enables static analysis |
| Runtime validation | Separate from annotations |
| `Optional` | `T | None` |
| `Union` | One of multiple types |
| `Literal` | Restricts to specific literal values |
| `TypedDict` | Describes dictionary structure for typing |
| Generic | Preserves relationships between types |
| Protocol | Structural interface |
| Static checker | Finds typing issues without normal runtime execution |
| pytest | Python testing framework |
| Fixture | Reusable test setup/cleanup |
| Fixture scope | Controls fixture lifetime |
| Parameterization | Runs one test over multiple cases |
| Mock | Controlled test double/interactions |
| Monkeypatch | Temporarily modifies state/attributes |
| Unit test | Isolated behavior |
| Integration test | Multiple real components |
| API test | Tests through HTTP interface |
| Fake | Simplified working implementation |
| Stub | Predefined response |
| Spy | Observes interactions |
| Arrange-Act-Assert | Common test structure |
| Test isolation | Tests avoid unexpected shared state |
| Coverage | Measures executed code, not test quality |
| Failure-path testing | Verifies error behavior |
| Async testing | Tests asynchronous behavior correctly |

______________________________________________________________________

# 56. Completion Checklist

Before moving to File 12, make sure you can explain:

- [ ] Why type hints are useful
- [ ] Runtime validation vs type hints
- [ ] Function annotations
- [ ] `Optional`
- [ ] Modern `T | None`
- [ ] `Union`
- [ ] `Literal`
- [ ] `TypedDict`
- [ ] Generics
- [ ] Generic classes
- [ ] Protocols
- [ ] ABC vs Protocol
- [ ] Static type checking
- [ ] mypy/pyright overview
- [ ] Gradual typing
- [ ] Type aliases
- [ ] pytest basics
- [ ] Test discovery
- [ ] Assertions
- [ ] Testing exceptions
- [ ] Fixtures
- [ ] Fixture scopes
- [ ] Fixture cleanup
- [ ] Fixture composition
- [ ] Parameterized tests
- [ ] Mocking
- [ ] `unittest.mock`
- [ ] Patching
- [ ] Patch where looked up
- [ ] `monkeypatch`
- [ ] Mock vs monkeypatch
- [ ] Unit testing
- [ ] Integration testing
- [ ] API testing
- [ ] Test strategy
- [ ] Test isolation
- [ ] External service testing
- [ ] Database testing
- [ ] Async testing
- [ ] FastAPI testing
- [ ] Test naming
- [ ] Arrange-Act-Assert
- [ ] Test doubles
- [ ] Code coverage
- [ ] Failure-path testing
- [ ] Retry/timeout testing
- [ ] Senior-level testing strategy
- [ ] Common testing mistakes

______________________________________________________________________

# 57. Interview Readiness Test

Answer these aloud without looking at the notes:

1. Why use type hints in Python?
1. Are Python type hints enforced at runtime?
1. What is `Optional[str]`?
1. What is `Union`?
1. What is `Literal`?
1. What is `TypedDict`?
1. What are generics?
1. Why would you use a generic repository?
1. What is a Protocol?
1. ABC vs Protocol?
1. What is gradual typing?
1. What do mypy and pyright do?
1. What is pytest?
1. How does pytest discover tests?
1. What is a fixture?
1. Why would you use a fixture instead of duplicating setup code?
1. What are fixture scopes?
1. What is fixture cleanup?
1. What is parameterized testing?
1. What is mocking?
1. When should you mock?
1. Why is mocking everything a bad idea?
1. What is `monkeypatch`?
1. Mock vs monkeypatch?
1. What does "patch where it is looked up" mean?
1. What is a unit test?
1. What is an integration test?
1. What is API testing?
1. What makes a good unit test?
1. What is test isolation?
1. What are dummy, stub, fake, mock and spy?
1. What is Arrange-Act-Assert?
1. Is high code coverage enough?
1. How would you test a database repository?
1. How would you test an external payment provider?
1. How would you test async code?
1. How would you test retry logic?
1. How would you test timeout behavior?
1. What should a senior backend testing strategy contain?
1. A test suite has 95% coverage but production bugs continue. What would you investigate?
1. A mock-based test breaks after a harmless refactor. What does that tell you?
1. Tests pass individually but fail as a suite. How would you investigate?
1. A patch is not intercepting the dependency. How would you diagnose the import/lookup location?

If you can answer these clearly and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [10. Python Concurrency & AsyncIO](./10-python-concurrency.md)

**Next:** [12. HTTP, TCP/IP, TLS & Networking](./12-http-networking.md)

# File: python/58-production-python-part-03-custom-exceptions.md

# Production Python
# Part 3: Custom Exceptions – Designing Domain-Specific Error Handling

> **Course:** Backend Engineering Roadmap
>
> **Module:** Production Python
>
> **Lesson:** 58
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 8–10 Hours

---

# Learning Objectives

By the end of this lesson, you will understand:

- Why custom exceptions exist
- When built-in exceptions are insufficient
- Designing exception hierarchies
- Domain-driven exceptions
- Exception translation
- Exception inheritance
- Carrying additional context
- Production error handling strategies
- Best practices
- questions

---

# Recap

In the previous lesson, we learned:

- Python's exception hierarchy
- Stack unwinding
- `try`
- `except`
- `else`
- `finally`
- Exception chaining
- Re-raising exceptions

However, production applications rarely expose raw exceptions such as:

```python
ValueError
```

or

```python
KeyError
```

Instead, they define exceptions that represent the **business domain**.

---

# Why Custom Exceptions?

Imagine an e-commerce application.

A customer attempts to purchase an item.

Possible failures:

- Product does not exist.
- Product is out of stock.
- Payment fails.
- User account is suspended.
- Discount coupon expired.

Could you raise:

```python
ValueError
```

for every one of these?

Technically yes.

But should you?

No.

The exception should describe **what actually happened**.

---

# The Problem with Built-in Exceptions

Consider:

```python
raise ValueError(
    "Invalid operation."
)
```

What does that mean?

- Invalid product?
- Invalid payment?
- Invalid user?
- Invalid coupon?

The exception carries very little meaning.

---

# Domain-Specific Exceptions

Instead:

```python
raise ProductOutOfStockError()
```

Immediately,

every developer understands the problem.

This improves:

- Readability
- Debugging
- Logging
- API responses
- Testing

---

# Creating Your First Custom Exception

```python
class ProductError(Exception):
    pass
```

Now:

```python
raise ProductError(
    "Unable to process product."
)
```

Your exception behaves exactly like built-in exceptions.

---

# Why Inherit from `Exception`?

Always inherit application exceptions from:

```python
Exception
```

Avoid:

```python
BaseException
```

because it represents exceptions that control Python's execution, such as:

- `KeyboardInterrupt`
- `SystemExit`

---

# Exception Hierarchies

One custom exception is useful.

A hierarchy is even better.

Example:

```text
ApplicationError

├── ProductError
│   ├── ProductNotFoundError
│   └── ProductOutOfStockError
│
├── PaymentError
│   ├── PaymentDeclinedError
│   └── PaymentTimeoutError
│
└── UserError
    ├── UserNotFoundError
    └── UserSuspendedError
```

Now developers can catch:

```python
except ProductError:
```

or

```python
except ProductOutOfStockError:
```

depending on the required level of specificity.

---

# Example

```python
class ProductError(Exception):
    pass


class ProductNotFoundError(ProductError):
    pass


class ProductOutOfStockError(ProductError):
    pass
```

Usage

```python
raise ProductOutOfStockError(
    "Laptop is unavailable."
)
```

---

# Catching Parent Exceptions

```python
try:

    purchase()

except ProductError:

    print("Product problem.")
```

This catches:

- `ProductNotFoundError`
- `ProductOutOfStockError`

because both inherit from:

```python
ProductError
```

---

# Adding Context

Exceptions can carry useful information.

Example

```python
class ProductNotFoundError(Exception):

    def __init__(

        self,

        product_id

    ):

        self.product_id = product_id

        super().__init__(

            f"Product {product_id} not found."

        )
```

Usage

```python
raise ProductNotFoundError(101)
```

Output

```text
Product 101 not found.
```

Now the exception contains structured information.

---

# Accessing Exception Data

```python
try:

    raise ProductNotFoundError(101)

except ProductNotFoundError as exc:

    print(exc.product_id)
```

Output

```text
101
```

This is useful for:

- Logging
- Monitoring
- Retry logic
- API responses

---

# Backend Example

Suppose:

```
Client

↓

API

↓

Service

↓

Repository

↓

PostgreSQL
```

The database raises:

```python
UniqueViolation
```

The repository translates it:

```python
raise UserAlreadyExistsError()
```

The API layer now depends only on your application's exception hierarchy,

not on PostgreSQL internals.

---

# Exception Translation

Database layer

```python
raise ConnectionError(...)
```

Repository

```python
raise DatabaseUnavailableError()

from exc
```

Service

```python
raise OrderCreationError()

from exc
```

API

```
HTTP 503
```

Each layer speaks its own language.

---

# Avoid Database Exceptions in Business Logic

Bad

```python
except IntegrityError:

    ...
```

inside business logic.

Better

```python
except UserAlreadyExistsError:

    ...
```

The service layer should not know which database engine you use.

---

# Mapping Exceptions to HTTP Responses

Imagine a REST API.

```
UserNotFoundError

↓

404
```

```
AuthenticationError

↓

401
```

```
PermissionDeniedError

↓

403
```

```
ValidationError

↓

400
```

```
PaymentDeclinedError

↓

402
```

```
DatabaseUnavailableError

↓

503
```

Your API becomes predictable.

---

# Base Application Exception

Many production systems define:

```python
class ApplicationError(Exception):
    pass
```

Every custom exception inherits from it.

Benefits:

- Easy global handling
- Central logging
- Unified error reporting

Hierarchy

```text
ApplicationError

├── ValidationError

├── AuthenticationError

├── AuthorizationError

├── DatabaseError

├── PaymentError

└── InventoryError
```

---

# Custom Exception with Metadata

Example

```python
class PaymentDeclinedError(

    Exception

):

    def __init__(

        self,

        order_id,

        reason

    ):

        self.order_id = order_id

        self.reason = reason

        super().__init__(

            f"Payment declined for order {order_id}: {reason}"

        )
```

Usage

```python
raise PaymentDeclinedError(

    order_id=123,

    reason="Insufficient funds"

)
```

---

# Logging Custom Exceptions

```python
try:

    process_payment()

except PaymentError:

    logger.exception(

        "Payment processing failed."

    )

    raise
```

The logger records:

- Exception type
- Message
- Traceback

This is much more useful than generic errors.

---

# Testing Custom Exceptions

```python
import pytest


def test_invalid_product():

    with pytest.raises(

        ProductNotFoundError

    ):

        find_product(999)
```

Custom exceptions make tests more expressive.

---

# Common Mistakes

## Mistake 1

Creating too many exceptions.

Bad

```text
InvalidEmailCharacterError
```

when

```text
ValidationError
```

would suffice.

---

## Mistake 2

Using built-in exceptions for business logic.

---

## Mistake 3

Losing the original cause by not using

```python
raise ... from ...
```

---

## Mistake 4

Creating unrelated exceptions without a common base class.

---

## Mistake 5

Adding unnecessary complexity.

Not every error requires its own exception type.

Design a hierarchy that reflects the business domain.

---

# Best Practices

✅ Create a common base exception for your application.

✅ Group related exceptions into hierarchies.

✅ Include useful context.

✅ Translate infrastructure exceptions.

✅ Preserve original exceptions with chaining.

❌ Don't expose database-specific exceptions outside the data layer.

❌ Don't create dozens of tiny exception classes without clear value.

---

# Production Insight

Large backend systems rarely expose third-party exceptions.

Instead,

each architectural layer translates lower-level failures into domain-specific exceptions.

Example

```
PostgreSQL

↓

psycopg Error

↓

Repository

↓

UserAlreadyExistsError

↓

Service

↓

Business Logic

↓

API

↓

HTTP 409 Conflict
```

This decouples your application from implementation details and makes future migrations much easier.

---

# Questions

### Question

> Why create custom exceptions?

### Answer

Because they communicate domain-specific failures more clearly than generic built-in exceptions and make applications easier to understand and maintain.

---

### Question

> Why create an exception hierarchy?

### Answer

It allows related exceptions to be grouped together so callers can handle either specific failures or broader categories of errors.

---

### Question

> Why should services avoid database-specific exceptions?

### Answer

Because business logic should depend on domain concepts rather than implementation details of a specific database or library.

---

### Question

> Why use exception chaining?

### Answer

To preserve the original cause of a failure while presenting a more meaningful exception at a higher architectural layer.

---

### Question

> What information should a custom exception carry?

### Answer

Only information that helps callers, logs, or monitoring systems understand and respond to the failure, such as identifiers or error reasons.

---

# Practical Lesson

Create:

```text
exceptions.py
```

```python
class ApplicationError(Exception):
    """Base class for all application exceptions."""


class InventoryError(ApplicationError):
    """Base inventory exception."""


class ProductNotFoundError(InventoryError):

    def __init__(self, product_id):

        self.product_id = product_id

        super().__init__(

            f"Product {product_id} not found."

        )


class ProductOutOfStockError(InventoryError):

    def __init__(

        self,

        product_id,

        available

    ):

        self.product_id = product_id

        self.available = available

        super().__init__(

            f"Product {product_id} has only {available} items remaining."

        )
```

Create a service that raises these exceptions and an API layer that catches them and converts them into simulated HTTP responses.

---

# Questions

## Question 1

Why are custom exceptions preferred over generic exceptions in business logic?

### Answer

They express domain-specific failures, improve readability, and make error handling more precise and maintainable.

---

## Question 2

What are the benefits of an exception hierarchy?

### Answer

It enables callers to catch either broad categories of errors or specific exceptions while keeping the design organised.

---

## Question 3

Why should infrastructure exceptions be translated?

### Answer

To prevent implementation details from leaking into higher layers and to keep business logic independent of external libraries.

---

## Question 4

Should every possible failure have its own exception class?

### Answer

No. Exceptions should represent meaningful business concepts. Too many highly specific exceptions make systems harder to maintain.

---

## Question 5

What is the purpose of a base `ApplicationError`?

### Answer

It provides a single root for all application-specific exceptions, making global handling, logging, and monitoring much easier.

---

# Assignment

## Exercise 1

Design a complete exception hierarchy for an e-commerce application.

Include:

- User
- Authentication
- Product
- Inventory
- Payment
- Order
- Shipping

---

## Exercise 2

Modify one of your Flask or FastAPI projects.

Replace generic exceptions with domain-specific exceptions.

---

## Exercise 3

Translate database exceptions into application exceptions in the repository layer.

Ensure the service layer never catches database-specific exceptions directly.

---

## Exercise 4

Implement a global exception handler that maps your custom exceptions to simulated HTTP status codes.

Document why each mapping is appropriate.

---

# Summary

In this lesson, you learned:

- ✅ Why custom exceptions improve production code.
- ✅ How to design exception hierarchies.
- ✅ How to carry additional context in exceptions.
- ✅ Exception translation across architectural layers.
- ✅ Mapping domain exceptions to HTTP responses.
- ✅ Testing and logging custom exceptions.
- ✅ Best practices for maintainable error handling.

---

# Next Lesson

**File:**
[59-production-python-part-04-typing-module](59-production-python-part-04-typing-module.md)

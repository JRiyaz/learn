# File: python/17-abstract-base-classes.md

# Python Advanced - Lesson 17

# Abstract Base Classes (ABC) - Defining Contracts for Classes

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced OOP
>
> **Lesson:** 17
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 100 Minutes

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why Abstract Base Classes (ABCs) exist
- The problem ABCs solve
- What an abstract class is
- What an abstract method is
- The `abc` module
- `ABC` and `@abstractmethod`
- Enforcing contracts
- Runtime enforcement
- Polymorphism with ABCs
- ABCs vs normal base classes
- ABCs vs duck typing
- Production use cases

______________________________________________________________________

# Why Do Abstract Base Classes Exist?

Imagine you're building a notification system.

You know every notification should support:

- Sending
- Validation
- Logging

You create a base class.

```python
class Notification:

    def send(self):

        pass
```

Developers inherit it.

```python
class EmailNotification(Notification):

    pass
```

The problem?

Nothing forces developers to implement `send()`.

Someone may accidentally forget.

```python
notification = EmailNotification()

notification.send()
```

The method does nothing.

This bug may go unnoticed until production.

______________________________________________________________________

# The Problem

Suppose your application supports:

- Email
- SMS
- Push Notifications
- Slack Notifications

Every notification **must** implement

```python
send()
```

But Python doesn't enforce this automatically.

This is exactly why Abstract Base Classes exist.

______________________________________________________________________

# What is an Abstract Base Class?

An Abstract Base Class (ABC) is a class that **cannot be instantiated directly**.

Instead, it defines a contract that child classes must follow.

Think of it as a blueprint.

```
Notification

↓

EmailNotification

↓

SMSNotification

↓

PushNotification
```

Every child promises to implement the required behaviour.

______________________________________________________________________

# The abc Module

Python provides the built-in `abc` module.

```python
from abc import ABC, abstractmethod
```

- `ABC` marks a class as abstract.
- `@abstractmethod` marks methods that subclasses must implement.

______________________________________________________________________

# Creating an Abstract Base Class

```python
from abc import ABC, abstractmethod


class Notification(ABC):

    @abstractmethod
    def send(self):

        pass
```

This class is now abstract.

______________________________________________________________________

# Instantiating an Abstract Class

```python
notification = Notification()
```

Output

```
TypeError:
Can't instantiate abstract class Notification
with abstract method send
```

Python prevents this.

Why?

Because an abstract class represents an incomplete implementation.

______________________________________________________________________

# Implementing the Abstract Method

```python
from abc import ABC, abstractmethod


class Notification(ABC):

    @abstractmethod
    def send(self):

        pass


class EmailNotification(Notification):

    def send(self):

        print("Sending email")
```

Usage

```python
email = EmailNotification()

email.send()
```

Output

```
Sending email
```

Now the contract has been satisfied.

______________________________________________________________________

# Forgetting to Implement

Suppose a developer writes

```python
class SMSNotification(Notification):

    pass
```

Then

```python
sms = SMSNotification()
```

Output

```
TypeError:
Can't instantiate abstract class
SMSNotification with abstract method send
```

Python immediately reports the mistake.

This is much safer than discovering the error later.

______________________________________________________________________

# Multiple Abstract Methods

An abstract class may define several methods.

```python
from abc import ABC, abstractmethod


class Repository(ABC):

    @abstractmethod
    def create(self):

        pass

    @abstractmethod
    def update(self):

        pass

    @abstractmethod
    def delete(self):

        pass
```

Every subclass must implement all three.

______________________________________________________________________

# Abstract Methods Can Have Implementations

An abstract method may still contain code.

```python
from abc import ABC, abstractmethod


class Logger(ABC):

    @abstractmethod
    def log(self):

        print("Preparing log...")
```

Child class

```python
class ConsoleLogger(Logger):

    def log(self):

        super().log()

        print("Writing to console")
```

Output

```
Preparing log...

Writing to console
```

The method remains abstract because subclasses are still required to override it.

______________________________________________________________________

# ABCs Define Contracts

Think of an ABC as a formal agreement.

```
Repository

Must implement:

✔ create()

✔ update()

✔ delete()
```

Any subclass that fails to honour the agreement cannot be instantiated.

______________________________________________________________________

# Polymorphism with ABCs

Suppose every payment gateway inherits from a common ABC.

```python
from abc import ABC, abstractmethod


class PaymentGateway(ABC):

    @abstractmethod
    def pay(self, amount):

        pass
```

Implementations

```python
class StripeGateway(PaymentGateway):

    def pay(self, amount):

        print(f"Charging £{amount} using Stripe")
```

```python
class PayPalGateway(PaymentGateway):

    def pay(self, amount):

        print(f"Charging £{amount} using PayPal")
```

Business logic

```python
def checkout(gateway, amount):

    gateway.pay(amount)
```

Usage

```python
checkout(
    StripeGateway(),
    100
)

checkout(
    PayPalGateway(),
    200
)
```

Output

```
Charging £100 using Stripe

Charging £200 using PayPal
```

The checkout function doesn't care which gateway it receives.

It only depends on the contract.

______________________________________________________________________

# ABC vs Normal Base Class

Normal Base Class

```python
class Animal:

    def speak(self):

        print("Animal")
```

Subclasses may override the method.

But they don't have to.

______________________________________________________________________

Abstract Base Class

```python
class Animal(ABC):

    @abstractmethod
    def speak(self):

        pass
```

Now every subclass **must** implement `speak()`.

______________________________________________________________________

# ABC vs Duck Typing

Python is famous for duck typing.

> "If it walks like a duck and quacks like a duck, treat it like a duck."

Example

```python
class Dog:

    def speak(self):

        print("Woof")
```

```python
class Cat:

    def speak(self):

        print("Meow")
```

Function

```python
def make_sound(animal):

    animal.speak()
```

This works even without inheritance.

______________________________________________________________________

# So Why Use ABCs?

Duck typing is flexible.

ABCs provide explicit contracts.

Duck Typing

- Flexible
- Minimal boilerplate
- Common in small projects

Abstract Base Classes

- Clear API expectations
- Runtime enforcement
- Better for large teams
- Easier to understand large codebases

Many production systems use both approaches depending on the situation.

______________________________________________________________________

# ABCs in the Standard Library

Many Python standard library classes are abstract.

Examples include:

```
collections.abc.Iterable

collections.abc.Sequence

collections.abc.Mapping

io.IOBase
```

When you implement these interfaces correctly, your classes behave like built-in Python objects.

______________________________________________________________________

# Production Example - Repository Pattern

```python
from abc import ABC, abstractmethod


class UserRepository(ABC):

    @abstractmethod
    def get_user(self, user_id):

        pass
```

Implementation

```python
class PostgreSQLRepository(UserRepository):

    def get_user(self, user_id):

        print("Fetching from PostgreSQL")
```

Another implementation

```python
class MongoRepository(UserRepository):

    def get_user(self, user_id):

        print("Fetching from MongoDB")
```

The service layer depends only on the abstract contract.

It doesn't care which database is used.

______________________________________________________________________

# Production Example - Storage Providers

```python
class Storage(ABC):

    @abstractmethod
    def upload(self, file):

        pass
```

Implementations

```
S3Storage

AzureStorage

GoogleCloudStorage
```

Each provider implements the same interface.

Switching providers requires minimal changes to business logic.

______________________________________________________________________

# Best Practices

✅ Use ABCs when multiple implementations must share a common interface.

✅ Keep abstract classes focused on behaviour, not implementation details.

✅ Prefer composition together with ABCs.

✅ Use meaningful method names.

❌ Don't create abstract classes with dozens of methods.

❌ Don't use ABCs when duck typing is sufficient.

______________________________________________________________________

# Production Insight

Large backend systems often depend on abstractions rather than concrete implementations.

A typical architecture looks like this.

```
Controller

↓

Service

↓

Repository (ABC)

↓

PostgreSQLRepository

MongoRepository

RedisRepository
```

The service only knows about the `Repository` contract.

This allows developers to:

- Replace implementations
- Mock repositories during testing
- Add new storage engines
- Reduce coupling

This principle is often summarised as:

> **Depend upon abstractions, not concrete implementations.**

______________________________________________________________________

# Questions

### Question

> What is an Abstract Base Class?

### Answer

An Abstract Base Class is a class that cannot be instantiated directly and defines one or more abstract methods that
subclasses must implement.

______________________________________________________________________

### Question

> What is the purpose of `@abstractmethod`?

### Answer

`@abstractmethod` marks a method that must be implemented by all concrete subclasses. Python prevents instantiation of
subclasses that fail to implement these methods.

______________________________________________________________________

### Question

> When would you use an ABC instead of a normal base class?

### Answer

Use an ABC when multiple classes must follow the same interface and you want Python to enforce that contract at runtime.

______________________________________________________________________

### Question

> What is the difference between ABCs and duck typing?

### Answer

Duck typing relies on an object's behaviour without requiring inheritance. ABCs explicitly define and enforce a shared
interface. Duck typing offers flexibility, while ABCs provide stronger guarantees and clearer contracts.

______________________________________________________________________

# Practical Lesson

Create a file:

```
abc_examples.py
```

```python
from abc import ABC, abstractmethod


class PaymentGateway(ABC):

    @abstractmethod
    def pay(self, amount):

        pass


class StripeGateway(PaymentGateway):

    def pay(self, amount):

        print(
            f"Charging £{amount} via Stripe"
        )


class PayPalGateway(PaymentGateway):

    def pay(self, amount):

        print(
            f"Charging £{amount} via PayPal"
        )


def checkout(gateway, amount):

    gateway.pay(amount)


checkout(
    StripeGateway(),
    50
)

checkout(
    PayPalGateway(),
    75
)
```

Expected Output

```
Charging £50 via Stripe

Charging £75 via PayPal
```

Now comment out one of the `pay()` implementations and observe the error when creating an instance.

______________________________________________________________________

# Questions

## Question 1

What is an Abstract Base Class?

### Answer

An Abstract Base Class defines a common interface for subclasses and cannot be instantiated directly.

______________________________________________________________________

## Question 2

What does `@abstractmethod` do?

### Answer

It marks a method that every concrete subclass must implement before it can be instantiated.

______________________________________________________________________

## Question 3

Can an abstract method contain code?

### Answer

Yes. An abstract method may include a partial implementation, but subclasses are still required to override it.

______________________________________________________________________

## Question 4

Why are ABCs useful in large applications?

### Answer

They enforce consistent interfaces, reduce implementation errors, and allow different components to be substituted
without changing business logic.

______________________________________________________________________

## Question 5

Should you always use ABCs instead of duck typing?

### Answer

No. Duck typing is often sufficient for simple or highly dynamic code. ABCs are most valuable when explicit contracts
and runtime enforcement improve maintainability.

______________________________________________________________________

# Assignment

## Exercise 1

Create an abstract class called `Shape` with an abstract method:

```python
area()
```

Implement:

- `Circle`
- `Rectangle`

Calculate and print their areas.

______________________________________________________________________

## Exercise 2

Create an abstract `Database` class with:

- `connect()`
- `disconnect()`

Implement:

- `MySQLDatabase`
- `PostgreSQLDatabase`

______________________________________________________________________

## Exercise 3

Build a file storage abstraction.

Create:

- `Storage` (ABC)
- `LocalStorage`
- `S3Storage`

Each should implement:

```python
upload(file)
```

______________________________________________________________________

## Exercise 4

Refactor one of your earlier composition examples so that the injected dependency is an Abstract Base Class instead of a
concrete implementation.

Explain why this improves extensibility and testing.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why Abstract Base Classes exist.
- ✅ How `ABC` and `@abstractmethod` enforce contracts.
- ✅ The difference between normal base classes and ABCs.
- ✅ How ABCs support polymorphism.
- ✅ The trade-offs between ABCs and duck typing.
- ✅ Production uses such as repositories, payment gateways and storage providers.
- ✅ Best practices for designing extensible object-oriented systems.

______________________________________________________________________

# What's Next

**File:** [18-Mixins](18-mixins.md)

Topics:

- What Are Mixins?
- Why Mixins Exist
- Mixins vs Inheritance
- Mixins vs Composition
- Designing Reusable Behaviour
- Cooperative Mixins with `super()`
- Production Examples (Django, SQLAlchemy, FastAPI)
- Best Practices

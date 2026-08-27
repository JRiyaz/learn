# 09. Advanced Python OOP

**Previous:** [08. Python OOP & Object Model](./08-python-oop.md)

**Next:** [10. Python Concurrency & AsyncIO](./10-python-concurrency.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain multiple inheritance and why it can become difficult to maintain.
- Understand Python's Method Resolution Order (MRO).
- Explain how `super()` works.
- Use cooperative multiple inheritance correctly.
- Understand Abstract Base Classes (ABCs).
- Explain the difference between inheritance, mixins, and composition.
- Understand descriptors and where they are useful.
- Explain `__slots__` and its trade-offs.
- Understand the role of `__new__` versus `__init__`.
- Explain what metaclasses are and when they are appropriate.
- Explain duck typing.
- Understand structural typing with `Protocol`.
- Relate these concepts to real Python backend frameworks and libraries.
- Answer senior-level interview questions about Python's object model without relying on memorized definitions.

______________________________________________________________________

# 1. Multiple Inheritance

Python allows a class to inherit from multiple parent classes.

```python
class Logger:
    def log(self, message):
        print(message)


class Metrics:
    def record(self, name):
        print(f"recording {name}")


class Service(Logger, Metrics):
    pass
```

`Service` gets behavior from both `Logger` and `Metrics`.

Multiple inheritance can be useful, but it introduces questions such as:

- Which implementation should Python choose?
- What happens when two parents define the same method?
- How should parent initialization be handled?
- How should a common base class be initialized?

These questions are handled largely through Python's **MRO** and `super()`.

______________________________________________________________________

# 2. Method Resolution Order (MRO)

The Method Resolution Order defines the order in which Python searches classes for an attribute or method.

For:

```python
class A:
    pass


class B(A):
    pass


class C(B):
    pass
```

The MRO is conceptually:

```text
C → B → A → object
```

You can inspect it with:

```python
print(C.mro())
```

or:

```python
print(C.__mro__)
```

______________________________________________________________________

# 3. Why MRO Matters

Consider:

```python
class A:
    def run(self):
        print("A")


class B(A):
    def run(self):
        print("B")


class C(A):
    def run(self):
        print("C")


class D(B, C):
    pass
```

Calling:

```python
D().run()
```

uses the MRO to determine which implementation is selected.

```python
D.mro()
```

will show the search order.

The important interview point is:

> Python does not simply search the left-most parent recursively. Multiple inheritance follows a well-defined MRO.

______________________________________________________________________

# 4. C3 Linearization

Python uses **C3 linearization** to calculate the MRO.

You do not usually need to perform C3 calculations manually in a backend interview, but you should understand the goals:

- Preserve local precedence order.
- Preserve parent class ordering.
- Maintain a consistent hierarchy.
- Avoid visiting the same class multiple times.

A useful senior-level answer is:

> Python's MRO uses C3 linearization to create a consistent method lookup order for multiple inheritance.

______________________________________________________________________

# 5. `super()`

`super()` is commonly misunderstood.

It does not simply mean:

> Call my direct parent.

Instead, it means approximately:

> Continue method lookup according to the MRO from the current class.

Example:

```python
class A:
    def process(self):
        print("A")


class B(A):
    def process(self):
        print("B")
        super().process()
```

Calling:

```python
B().process()
```

produces:

```text
B
A
```

______________________________________________________________________

# 6. `super()` With Multiple Inheritance

Consider:

```python
class A:
    def process(self):
        print("A")


class B(A):
    def process(self):
        print("B")
        super().process()


class C(A):
    def process(self):
        print("C")
        super().process()


class D(B, C):
    def process(self):
        print("D")
        super().process()
```

The MRO is:

```text
D → B → C → A → object
```

Therefore:

```python
D().process()
```

produces:

```text
D
B
C
A
```

This is the basis of **cooperative multiple inheritance**.

______________________________________________________________________

# 7. Cooperative Multiple Inheritance

Classes intended to participate in a multiple-inheritance hierarchy should generally cooperate by calling:

```python
super()
```

rather than directly naming a parent.

Prefer:

```python
super().process()
```

over:

```python
A.process(self)
```

when the class is designed for cooperative inheritance.

Direct parent calls can bypass the MRO and cause another class in the hierarchy to be skipped.

______________________________________________________________________

# 8. Constructor Cooperation

The same principle applies to `__init__`.

Example:

```python
class Base:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LoggingMixin:
    def __init__(self, **kwargs):
        self.logger = "logger"
        super().__init__(**kwargs)


class Service(LoggingMixin, Base):
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        super().__init__(**kwargs)
```

Cooperative constructors are especially important when mixins are involved.

The signatures need to be designed consistently.

______________________________________________________________________

# 9. Abstract Base Classes

Python provides Abstract Base Classes through the `abc` module.

```python
from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def save(self, item):
        pass
```

A subclass must implement the abstract method before it can normally be instantiated.

```python
class UserRepository(Repository):
    def save(self, item):
        print("saving user")
```

______________________________________________________________________

# 10. Why Use ABCs?

ABCs are useful when you want to explicitly define an inheritance-based contract.

For example:

```python
class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount):
        ...
```

Different implementations can then provide:

```python
class StripeProcessor(PaymentProcessor):
    ...


class MockProcessor(PaymentProcessor):
    ...
```

This communicates intent clearly.

______________________________________________________________________

# 11. ABC vs Normal Base Class

A normal base class may provide reusable behavior without requiring subclasses to implement particular methods.

An ABC can explicitly state:

> Concrete subclasses must provide this behavior.

This is useful when a family of implementations shares a formal contract.

______________________________________________________________________

# 12. Mixins

A mixin is a small class designed to provide reusable behavior to another class through inheritance.

Example:

```python
class AuditMixin:
    def audit(self, message):
        print(f"AUDIT: {message}")


class UserService(AuditMixin):
    def create_user(self, user):
        self.audit("creating user")
```

A mixin usually represents **behavior**, not a complete domain object.

Good mixins tend to be:

- Small
- Focused
- Reusable
- Stateless or minimally stateful
- Designed to cooperate with other classes

______________________________________________________________________

# 13. Mixin vs Base Class

A base class often represents an abstraction or conceptual parent.

A mixin usually represents an optional capability.

For example:

```text
Base class:
    Repository

Mixin:
    LoggingMixin
    CachingMixin
    AuditMixin
```

A repository may fundamentally be a repository, while logging or auditing is additional behavior.

______________________________________________________________________

# 14. Mixin Design Rules

A good mixin should avoid assuming too much about the consuming class.

Avoid a mixin that secretly requires:

```python
self.some_random_attribute
```

without documenting or enforcing the requirement.

If the mixin depends on another behavior, cooperative `super()` and clearly defined interfaces can help.

______________________________________________________________________

# 15. Descriptors

A descriptor is an object that defines one or more of:

```python
__get__
__set__
__delete__
```

Descriptors customize attribute access.

A simplified descriptor:

```python
class PositiveNumber:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("must be positive")
        instance.__dict__[self.name] = value
```

Usage:

```python
class Product:
    price = PositiveNumber()
```

Now:

```python
product = Product()
product.price = 100
```

passes through the descriptor.

______________________________________________________________________

# 16. Why Descriptors Matter

Descriptors are an important building block in Python.

They are used heavily by frameworks and libraries.

Examples include concepts behind:

- Properties
- ORM fields
- Validation
- Lazy attributes
- Managed attributes

You do not need to write descriptors every day, but understanding them helps explain how Python frameworks implement
declarative APIs.

______________________________________________________________________

# 17. `property` Is Descriptor-Based

Consider:

```python
class User:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name
```

`property` itself participates in Python's descriptor protocol.

Therefore:

> A property is a practical, built-in use of descriptor behavior.

______________________________________________________________________

# 18. Data vs Non-Data Descriptors

A descriptor defining `__set__` or `__delete__` is generally a **data descriptor**.

A descriptor defining only `__get__` is a **non-data descriptor**.

This distinction matters because Python's attribute lookup rules treat them differently.

For senior interviews, understand the practical point:

- Data descriptors can take precedence over instance attributes.
- Non-data descriptors can be shadowed by an instance attribute.

______________________________________________________________________

# 19. `__slots__`

`__slots__` allows a class to declare a fixed set of instance attributes.

Example:

```python
class User:
    __slots__ = ("name", "email")

    def __init__(self, name, email):
        self.name = name
        self.email = email
```

Depending on the class hierarchy and design, instances may not have a normal `__dict__`.

______________________________________________________________________

# 20. Why Use `__slots__`?

Potential benefits include:

- Lower per-instance memory overhead.
- Preventing arbitrary new attributes.
- Potentially improving memory efficiency for large numbers of small objects.

Example use case:

```text
Millions of lightweight objects
```

where per-object memory overhead matters.

______________________________________________________________________

# 21. `__slots__` Trade-offs

`__slots__` is not a universal optimization.

Trade-offs can include:

- Less flexibility.
- More complicated inheritance behavior.
- Interaction with multiple inheritance.
- Some tooling/library expectations may depend on `__dict__`.
- Weak-reference support may need explicit consideration.

Measure before using it as a performance optimization.

______________________________________________________________________

# 22. `__new__` vs `__init__`

These methods have different responsibilities.

### `__new__`

Responsible for creating/returning an instance.

### `__init__`

Initializes an already-created instance.

Conceptually:

```text
__new__ → create instance
       ↓
__init__ → initialize instance
```

______________________________________________________________________

# 23. Example of `__new__`

```python
class Example:
    def __new__(cls):
        print("creating")
        return super().__new__(cls)

    def __init__(self):
        print("initializing")
```

Calling:

```python
Example()
```

runs:

```text
creating
initializing
```

______________________________________________________________________

# 24. When Is `__new__` Useful?

Common use cases include:

- Immutable types
- Controlling instance creation
- Singleton-like patterns
- Specialized object construction
- Subclassing immutable built-in types

You generally should not override `__new__` unless there is a specific reason.

______________________________________________________________________

# 25. Immutable Objects and `__new__`

For immutable types, the object must generally be created with the required value before initialization can modify
anything.

This is why `__new__` is particularly relevant when subclassing immutable built-ins such as:

```python
str
tuple
int
```

______________________________________________________________________

# 26. Metaclasses

A metaclass is the class of a class.

Normally:

```python
class User:
    pass
```

means `User` is an instance of a metaclass, normally `type`.

Conceptually:

```text
object instances
        ↓
     User
        ↓
      type
```

A metaclass controls aspects of class creation.

______________________________________________________________________

# 27. Simple Metaclass Example

```python
class Meta(type):
    def __new__(mcls, name, bases, namespace):
        print(f"Creating {name}")
        return super().__new__(mcls, name, bases, namespace)


class User(metaclass=Meta):
    pass
```

When `User` is defined, the metaclass participates in creating the class object.

______________________________________________________________________

# 28. Why Metaclasses Exist

Metaclasses can be used to:

- Modify class creation.
- Register classes.
- Enforce class-level conventions.
- Generate attributes.
- Implement framework behavior.

However:

> Metaclasses are powerful and should be used sparingly.

Many problems that appear to require metaclasses can be solved more simply with:

- Functions
- Decorators
- Class decorators
- Descriptors
- Composition
- `__init_subclass__`

______________________________________________________________________

# 29. `__init_subclass__`

Before reaching for a metaclass, consider:

```python
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"Registered: {cls.__name__}")
```

Every subclass can trigger this hook.

For many framework-style registration problems, this is simpler than a custom metaclass.

______________________________________________________________________

# 30. Duck Typing

Duck typing focuses on behavior rather than explicit inheritance.

The idea is:

> If an object provides the required behavior, it can be used.

Example:

```python
def send(message_sender):
    message_sender.send("hello")
```

The function does not necessarily care whether `message_sender` inherits from a particular class.

It cares that it provides:

```python
send(...)
```

______________________________________________________________________

# 31. Duck Typing in Backend Code

This is common in Python applications.

For example:

```python
def publish(publisher, event):
    publisher.publish(event)
```

`publisher` could be:

- Kafka publisher
- RabbitMQ publisher
- Test fake
- In-memory publisher

As long as the expected method exists.

This can make testing and dependency substitution easier.

______________________________________________________________________

# 32. Protocols

`typing.Protocol` provides a way to describe structural interfaces for static type checking.

Example:

```python
from typing import Protocol


class Publisher(Protocol):
    def publish(self, event: str) -> None:
        ...
```

A class does not need to explicitly inherit from `Publisher`.

If it provides the expected structure, type checkers can treat it as compatible.

______________________________________________________________________

# 33. ABC vs Protocol

This distinction is highly interview-relevant.

### ABC

Primarily communicates an explicit inheritance-based contract.

```python
class Repository(ABC):
    ...
```

A concrete implementation normally inherits from it.

### Protocol

Describes a structural contract.

```python
class Repository(Protocol):
    ...
```

A class can satisfy the protocol without explicitly inheriting from it.

A concise interview answer:

> ABCs are generally nominal/inheritance-oriented contracts, while Protocols enable structural typing.

______________________________________________________________________

# 34. Duck Typing vs Protocol

They are closely related but operate at different levels.

### Duck typing

Runtime programming style:

```python
obj.method()
```

If the object supports the behavior, use it.

### Protocol

Adds an explicit structural interface that static type checkers can understand.

So Protocol can provide type-safe documentation around a duck-typed design.

______________________________________________________________________

# 35. Practical Backend Example — Repository Contract

Using a Protocol:

```python
from typing import Protocol


class UserRepository(Protocol):
    def get_by_id(self, user_id: int):
        ...


class PostgresUserRepository:
    def get_by_id(self, user_id: int):
        ...


class FakeUserRepository:
    def get_by_id(self, user_id: int):
        ...
```

A service can depend on the behavior:

```python
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
```

This reduces coupling to a concrete repository implementation.

______________________________________________________________________

# 36. Practical Backend Example — Mixins

A framework-style class may combine behavior:

```python
class LoggingMixin:
    def log(self, message):
        print(message)


class CacheMixin:
    def invalidate_cache(self, key):
        print(f"invalidate {key}")


class UserService(LoggingMixin, CacheMixin):
    pass
```

This can be convenient for cross-cutting behavior, but composition may be preferable when the behavior has significant
state or complex dependencies.

______________________________________________________________________

# 37. Inheritance vs Composition

A recurring senior-level question is:

> Should I use inheritance or composition?

Prefer inheritance when there is a strong and stable **is-a** relationship and polymorphic behavior is central.

Prefer composition when an object **has-a** dependency or behavior.

Example:

```python
class OrderService:
    def __init__(self, repository, notifier):
        self.repository = repository
        self.notifier = notifier
```

This is often easier to test and evolve than creating a large inheritance hierarchy.

______________________________________________________________________

# 38. Advanced OOP in Real Backend Frameworks

You may encounter these concepts indirectly in frameworks and libraries.

### ORM systems

Descriptors and metaprogramming can help model fields and relationships.

### Validation libraries

Descriptors, class creation hooks and generated metadata can support declarative validation.

### Dependency injection

Protocols and abstract interfaces can define service boundaries.

### Framework base classes

Inheritance and `super()` are common in extension mechanisms.

### Test doubles

Duck typing and Protocols make it easier to substitute implementations.

______________________________________________________________________

# 39. Common Interview Traps

## Trap 1 — "`super()` means parent"

Not exactly.

It follows the MRO.

______________________________________________________________________

## Trap 2 — "Multiple inheritance always means bad design"

Not necessarily.

Mixins and framework extension points are legitimate uses.

______________________________________________________________________

## Trap 3 — "`__slots__` makes objects faster"

Not necessarily.

Its most common benefit is reduced per-instance memory overhead.

______________________________________________________________________

## Trap 4 — "`__init__` creates the object"

`__new__` participates in object creation; `__init__` initializes the instance.

______________________________________________________________________

## Trap 5 — "Protocol requires inheritance"

No.

Protocols support structural typing.

______________________________________________________________________

## Trap 6 — "Metaclasses should be used for everything"

No.

They are advanced machinery and should normally be used only when simpler mechanisms are insufficient.

______________________________________________________________________

# 40. Interview Questions & Answers

## Q1. What is multiple inheritance?

**Answer:**

Multiple inheritance allows a class to inherit from more than one parent class.

It can be useful for combining focused behavior, especially mixins, but it introduces method-resolution and
initialization complexity.

______________________________________________________________________

## Q2. What is MRO?

**Answer:**

MRO, or Method Resolution Order, is the order Python uses to search classes for attributes and methods.

It becomes particularly important with inheritance hierarchies involving multiple parents.

You can inspect it with:

```python
MyClass.mro()
```

______________________________________________________________________

## Q3. What algorithm does Python use for MRO?

**Answer:**

Python uses C3 linearization to calculate a consistent method resolution order for multiple inheritance.

For most interviews, explaining its purpose is more important than manually calculating the algorithm.

______________________________________________________________________

## Q4. Does `super()` call the direct parent?

**Answer:**

Not necessarily.

`super()` continues lookup according to the MRO from the current class.

That distinction is important in multiple inheritance.

______________________________________________________________________

## Q5. Why should cooperative multiple inheritance use `super()`?

**Answer:**

Using `super()` allows every class in the MRO to participate in the call chain.

Directly calling a named parent can bypass another class in the MRO.

______________________________________________________________________

## Q6. What is a mixin?

**Answer:**

A mixin is a small class that provides reusable behavior to another class through inheritance.

It usually represents an optional capability rather than a complete domain abstraction.

______________________________________________________________________

## Q7. What is an Abstract Base Class?

**Answer:**

An ABC defines an explicit inheritance-oriented contract and can require subclasses to implement abstract methods.

Python provides this through the `abc` module.

______________________________________________________________________

## Q8. What is a descriptor?

**Answer:**

A descriptor is an object implementing methods such as `__get__`, `__set__`, or `__delete__` to control attribute
access.

Descriptors are a fundamental mechanism behind features such as properties and are widely useful in framework
implementations.

______________________________________________________________________

## Q9. What is the difference between a data descriptor and a non-data descriptor?

**Answer:**

A data descriptor implements `__set__` or `__delete__` in addition to `__get__`, while a non-data descriptor may only
implement `__get__`.

Data descriptors generally have precedence over instance attributes during attribute lookup.

______________________________________________________________________

## Q10. What is `__slots__`?

**Answer:**

`__slots__` declares a fixed set of instance attributes and can reduce per-instance memory overhead.

It also restricts arbitrary attribute creation unless the class hierarchy provides the required storage.

______________________________________________________________________

## Q11. When would you use `__slots__`?

**Answer:**

Potentially when an application creates very large numbers of small objects and memory overhead matters.

It should be measured and used deliberately because it reduces flexibility and can complicate inheritance or library
integration.

______________________________________________________________________

## Q12. What is the difference between `__new__` and `__init__`?

**Answer:**

`__new__` participates in creating and returning the instance.

`__init__` initializes an instance that has already been created.

`__new__` is especially relevant when dealing with immutable types or customized object creation.

______________________________________________________________________

## Q13. What is a metaclass?

**Answer:**

A metaclass is the class of a class.

The default metaclass is `type`.

Metaclasses can customize class creation, but they are advanced machinery and should generally be avoided when simpler
mechanisms are sufficient.

______________________________________________________________________

## Q14. What are alternatives to metaclasses?

**Answer:**

Depending on the problem, alternatives include:

- Functions
- Decorators
- Class decorators
- Descriptors
- `__init_subclass__`
- Composition

Choosing a simpler mechanism generally improves maintainability.

______________________________________________________________________

## Q15. What is duck typing?

**Answer:**

Duck typing focuses on whether an object supports the required behavior rather than whether it inherits from a
particular class.

For example, code can call `publisher.publish()` without requiring a specific publisher base class.

______________________________________________________________________

## Q16. What is a Protocol?

**Answer:**

A `typing.Protocol` describes a structural interface for static type checking.

A class can satisfy the protocol by providing the expected methods and attributes without explicitly inheriting from the
protocol.

______________________________________________________________________

## Q17. ABC vs Protocol?

**Answer:**

ABCs are generally inheritance-based contracts.

Protocols provide structural contracts that can be satisfied implicitly.

For dependency boundaries, Protocols can reduce coupling to concrete implementations.

______________________________________________________________________

## Q18. When would you choose composition over inheritance?

**Answer:**

Use composition when the relationship is primarily "has-a" or when you want to replace dependencies independently.

Composition usually reduces coupling and makes testing easier.

______________________________________________________________________

## Q19. Why can multiple inheritance become difficult?

**Answer:**

It can create:

- Complex MROs
- Ambiguous-looking behavior
- Constructor coordination problems
- Tight coupling between parent classes
- Difficult-to-understand method chains

Focused mixins and cooperative `super()` can make legitimate multiple inheritance manageable.

______________________________________________________________________

## Q20. What happens if one class in a cooperative hierarchy does not call `super()`?

**Answer:**

The cooperative chain can stop at that class.

Another class later in the MRO may never receive the call.

This is why all participating classes need to follow compatible cooperative-inheritance conventions.

______________________________________________________________________

## Q21. Why are descriptors important for backend engineers?

**Answer:**

They help explain how Python frameworks implement managed attributes.

ORM fields, properties, validation mechanisms and other declarative APIs can rely on descriptor behavior.

______________________________________________________________________

## Q22. Why is `__slots__` not automatically a performance optimization?

**Answer:**

Its primary advantage is often memory reduction per instance.

Whether it improves runtime performance depends on the workload and implementation details.

You should measure rather than assume.

______________________________________________________________________

## Q23. Why might `__new__` be needed for immutable objects?

**Answer:**

Immutable objects cannot be modified after creation in the same way mutable objects can.

Therefore, required state often needs to be established as part of object creation, which is where `__new__`
participates.

______________________________________________________________________

## Q24. How would you explain Protocols to a team using dependency injection?

**Answer:**

I would define the behavior the service needs as a Protocol and type the dependency against that Protocol.

Concrete implementations and test fakes can satisfy the contract without inheriting from a shared base class.

This reduces coupling and makes substitution easier.

______________________________________________________________________

## Q25. When would you avoid a metaclass?

**Answer:**

I would avoid it when a decorator, `__init_subclass__`, descriptor, composition or ordinary class design solves the
problem.

Metaclasses increase conceptual complexity and can make debugging and maintenance harder.

______________________________________________________________________

# 41. Scenario-Based Questions

## Scenario 1 — `super()` Surprise

You have:

```python
class A:
    def run(self):
        print("A")


class B(A):
    def run(self):
        print("B")
        super().run()


class C(A):
    def run(self):
        print("C")
        super().run()


class D(B, C):
    def run(self):
        print("D")
        super().run()
```

**Question:** What does `D().run()` print?

**Answer:**

The MRO is:

```text
D → B → C → A → object
```

Therefore the output is:

```text
D
B
C
A
```

This demonstrates why `super()` follows the MRO rather than simply calling the direct parent.

______________________________________________________________________

## Scenario 2 — Broken Cooperative Inheritance

Suppose `B.run()` changes to:

```python
def run(self):
    print("B")
    A.run(self)
```

**Question:** What problem can this cause?

**Answer:**

It bypasses the MRO.

In the previous hierarchy, `C.run()` can be skipped entirely.

Direct parent calls are therefore dangerous in cooperative multiple inheritance.

______________________________________________________________________

## Scenario 3 — Repository Dependency

You have:

```python
class UserService:
    def __init__(self, repository):
        self.repository = repository
```

The production implementation uses PostgreSQL and tests use an in-memory fake.

**Question:** Would you use inheritance?

**Answer:**

Not necessarily.

A `Protocol` can define the required repository behavior:

```python
class UserRepository(Protocol):
    def get_by_id(self, user_id: int):
        ...
```

Both implementations can satisfy the protocol without sharing an inheritance hierarchy.

______________________________________________________________________

## Scenario 4 — Millions of Lightweight Objects

A service creates millions of small objects containing only two or three fields and memory consumption is a concern.

**Question:** Would `__slots__` be worth investigating?

**Answer:**

Yes.

`__slots__` can reduce per-instance memory overhead.

However, benchmark the actual application and consider compatibility requirements before introducing it.

______________________________________________________________________

## Scenario 5 — Framework Registration

You want every subclass of a base class to automatically register itself.

**Question:** Do you need a metaclass?

**Answer:**

Not necessarily.

`__init_subclass__` may provide a much simpler implementation.

A metaclass should be considered only if the requirements genuinely involve class-creation control that simpler
mechanisms cannot handle cleanly.

______________________________________________________________________

## Scenario 6 — Cross-Cutting Logging

Several classes need a small reusable logging behavior.

**Question:** Could a mixin work?

**Answer:**

Yes.

A small `LoggingMixin` can be appropriate if the behavior is simple and the inheritance relationship remains
understandable.

If logging requires complex state or dependencies, composition may be cleaner.

______________________________________________________________________

## Scenario 7 — Attribute Validation

A framework wants assignment to a field to automatically validate the value.

**Question:** What Python mechanism could support this?

**Answer:**

A descriptor can intercept attribute access and assignment.

This is one reason descriptors are important to understand when working with Python frameworks and ORMs.

______________________________________________________________________

## Scenario 8 — Abstract Service Contract

Several payment implementations must expose:

```python
charge(amount)
refund(transaction_id)
```

**Question:** Would an ABC or Protocol be appropriate?

**Answer:**

Both can be appropriate, depending on the design.

An ABC is useful when you want an explicit inheritance-based contract and potentially shared implementation.

A Protocol is useful when you want structural typing and loose coupling to implementations.

______________________________________________________________________

# 42. Practice Exercises

## Exercise 1 — MRO

Create:

```text
A
├── B
└── C
    ↓
    D(B, C)
```

Give `A`, `B`, `C`, and `D` methods with the same name.

Print:

```python
D.mro()
```

Predict the method-call order before running the program.

______________________________________________________________________

## Exercise 2 — Cooperative `super()`

Create a multiple-inheritance hierarchy where every class calls:

```python
super()
```

Verify that every implementation in the MRO participates.

Then replace one `super()` call with a direct parent call and observe the difference.

______________________________________________________________________

## Exercise 3 — Mixin

Create:

```python
LoggingMixin
CachingMixin
UserService
```

Use the mixins to add logging and cache invalidation behavior.

Keep each mixin small and focused.

______________________________________________________________________

## Exercise 4 — ABC Repository

Create:

```python
Repository
InMemoryRepository
```

Make `Repository` an ABC with an abstract `save()` method.

Attempt to instantiate the abstract class and observe the result.

______________________________________________________________________

## Exercise 5 — Descriptor

Implement a descriptor that validates that a username:

- Is a string.
- Is not empty.
- Has a maximum length.

Use it in a `User` class.

______________________________________________________________________

## Exercise 6 — `__slots__`

Create two equivalent classes:

```python
RegularUser
SlottedUser
```

Create a large number of instances and compare memory behavior.

Do not assume the result—measure it.

______________________________________________________________________

## Exercise 7 — `__new__`

Create a subclass of `str` that normalizes the value during object creation.

Investigate why `__new__` is required rather than relying only on `__init__`.

______________________________________________________________________

## Exercise 8 — Protocol

Define:

```python
class Publisher(Protocol):
    def publish(self, event: str) -> None:
        ...
```

Create:

```python
KafkaPublisher
FakePublisher
```

Use both with a service typed against `Publisher`.

______________________________________________________________________

## Exercise 9 — Refactoring

Take an inheritance-heavy design and identify where composition would reduce coupling.

Write down:

- Current inheritance
- Problems
- Proposed composition
- Benefits
- Trade-offs

______________________________________________________________________

# 43. Quick Revision

| Concept | Key Point |
|---|---|
| Multiple inheritance | A class can inherit from multiple parents |
| MRO | Defines method/attribute lookup order |
| C3 | Algorithm used to calculate Python's MRO |
| `super()` | Continues lookup through the MRO |
| Cooperative inheritance | Classes participate through `super()` |
| ABC | Explicit inheritance-oriented contract |
| Mixin | Small reusable behavior class |
| Descriptor | Controls attribute access |
| Data descriptor | Descriptor with `__set__` or `__delete__` |
| Non-data descriptor | Typically implements `__get__` only |
| `__slots__` | Restricts declared instance attributes and can reduce memory overhead |
| `__new__` | Participates in instance creation |
| `__init__` | Initializes an existing instance |
| Metaclass | Class used to create/control classes |
| `__init_subclass__` | Hook for subclass creation |
| Duck typing | Focus on supported behavior |
| Protocol | Structural typing contract |
| Composition | Build objects from dependencies/behaviors |
| Inheritance | Reuse/extend through an is-a relationship |

______________________________________________________________________

# 44. Completion Checklist

Before moving to the next topic, make sure you can explain:

- [ ] Multiple inheritance
- [ ] MRO
- [ ] C3 linearization
- [ ] `super()`
- [ ] Cooperative multiple inheritance
- [ ] Cooperative constructors
- [ ] Abstract Base Classes
- [ ] ABC vs normal base class
- [ ] Mixins
- [ ] Mixin vs base class
- [ ] Descriptor protocol
- [ ] Data vs non-data descriptors
- [ ] `property` as a descriptor
- [ ] `__slots__`
- [ ] `__slots__` trade-offs
- [ ] `__new__`
- [ ] `__new__` vs `__init__`
- [ ] Immutable object construction
- [ ] Metaclasses
- [ ] `__init_subclass__`
- [ ] Alternatives to metaclasses
- [ ] Duck typing
- [ ] Protocols
- [ ] ABC vs Protocol
- [ ] Duck typing vs Protocol
- [ ] Inheritance vs composition
- [ ] Practical backend uses of advanced OOP
- [ ] Common advanced OOP interview traps

______________________________________________________________________

# 45. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is multiple inheritance?
1. Explain MRO.
1. What is C3 linearization?
1. What does `super()` actually do?
1. Why is `super()` important in multiple inheritance?
1. Explain cooperative multiple inheritance.
1. What happens when one class fails to call `super()`?
1. What is an Abstract Base Class?
1. When would you use an ABC?
1. What is a mixin?
1. Mixin vs base class?
1. What is a descriptor?
1. What is the difference between a data and non-data descriptor?
1. Why is `property` related to descriptors?
1. What is `__slots__`?
1. Why can `__slots__` reduce memory usage?
1. What are the trade-offs of `__slots__`?
1. What is the difference between `__new__` and `__init__`?
1. When would you override `__new__`?
1. What is a metaclass?
1. Why should metaclasses be used carefully?
1. What is `__init_subclass__`?
1. What is duck typing?
1. What is a Protocol?
1. ABC vs Protocol?
1. Duck typing vs Protocol?
1. When would you prefer composition over inheritance?
1. Give a backend example where a Protocol is useful.
1. Give a backend example where a descriptor could be useful.
1. Give a legitimate use case for a mixin.
1. Explain the output of a multiple-inheritance `super()` chain.
1. How would you diagnose a broken cooperative inheritance hierarchy?
1. When would you investigate `__slots__` in production?
1. When would you avoid a metaclass?
1. How would you explain all of this to another senior engineer in terms of maintainability and trade-offs?

If you can answer these clearly and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [08. Python OOP & Object Model](./08-python-oop.md)

**Next:** [10. Python Concurrency & AsyncIO](./10-python-concurrency.md)

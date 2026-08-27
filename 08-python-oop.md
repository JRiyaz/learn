# 8. Python OOP & Design Principles

**Previous:** [7. Python Modules, Packages & Virtual Environments](./07-python-modules-packages.md)

**Next:** [9. Python Memory Management & Internals](./09-python-advanced-oop.md)

______________________________________________________________________

## Objectives

By the end of this chapter, you should be able to:

- Explain classes and objects clearly.
- Understand instance attributes, class attributes, and methods.
- Explain `self` and object state.
- Understand `__init__` and object construction.
- Explain instance methods, class methods, and static methods.
- Understand inheritance and method overriding.
- Explain polymorphism and duck typing.
- Understand encapsulation and Python's conventions for visibility.
- Explain `@property`.
- Understand `super()`.
- Explain method resolution order (MRO).
- Understand multiple inheritance at interview level.
- Explain composition vs inheritance.
- Understand abstract base classes and protocols conceptually.
- Apply SOLID principles to Python backend code.
- Recognize common OOP design mistakes.
- Answer common Python OOP interview questions confidently.

______________________________________________________________________

# 1. What Is Object-Oriented Programming?

Object-oriented programming organizes software around objects that combine:

- State
- Behavior

For example:

```python
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def display_name(self):
        return self.name
```

An object created from this class contains state:

```python
user = User(1, "Riyaz")
```

and behavior:

```python
user.display_name()
```

______________________________________________________________________

# 2. Class vs Object

A class defines a structure and behavior.

An object is an instance of that class.

Example:

```python
class User:
    pass


user1 = User()
user2 = User()
```

Here:

```text
User → class
user1 → object
user2 → object
```

`user1` and `user2` are separate instances.

______________________________________________________________________

# 3. `__init__`

`__init__` initializes an object's state after the object has been created.

Example:

```python
class User:
    def __init__(self, name):
        self.name = name
```

Usage:

```python
user = User("Riyaz")
```

The object's `name` attribute is initialized during construction.

A common interview detail:

> `__init__` initializes an already-created instance; it is not technically the method that allocates the object.

Object creation is associated with `__new__`.

______________________________________________________________________

# 4. `self`

`self` refers to the current instance.

Example:

```python
class User:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello {self.name}"
```

When:

```python
user.greet()
```

is called, Python passes the instance to the method.

Conceptually:

```python
User.greet(user)
```

The name `self` is a convention, not a language keyword, but it should almost always be used.

______________________________________________________________________

# 5. Instance Attributes

Attributes stored on an individual object are instance attributes.

```python
class User:
    def __init__(self, name):
        self.name = name
```

Then:

```python
a = User("Alice")
b = User("Bob")
```

have independent:

```python
a.name
b.name
```

values.

______________________________________________________________________

# 6. Class Attributes

A class attribute belongs to the class and is shared through the class unless shadowed by an instance attribute.

Example:

```python
class User:
    role = "user"
```

Then:

```python
User.role
```

and normally:

```python
user.role
```

both access the class attribute.

Be careful with mutable class attributes.

______________________________________________________________________

# 7. Mutable Class Attribute Trap

This is dangerous:

```python
class User:
    permissions = []

    def add_permission(self, permission):
        self.permissions.append(permission)
```

Instances can unintentionally share the same list.

Prefer:

```python
class User:
    def __init__(self):
        self.permissions = []
```

Now every instance gets its own list.

This is a very common interview question.

______________________________________________________________________

# 8. Instance Methods

Normal methods operate on an instance.

```python
class User:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello {self.name}"
```

The first parameter is conventionally:

```python
self
```

It gives the method access to the object's state.

______________________________________________________________________

# 9. Class Methods

A class method receives the class rather than an instance.

Use:

```python
@classmethod
```

Example:

```python
class User:
    def __init__(self, name):
        self.name = name

    @classmethod
    def anonymous(cls):
        return cls("Anonymous")
```

Usage:

```python
user = User.anonymous()
```

The first parameter is conventionally:

```python
cls
```

______________________________________________________________________

# 10. Common Uses of Class Methods

Class methods are useful for:

- Alternative constructors
- Factory methods
- Operations related to class-level state
- Polymorphic construction

Example:

```python
class User:
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"]
        )
```

______________________________________________________________________

# 11. Static Methods

A static method does not automatically receive `self` or `cls`.

Use:

```python
@staticmethod
```

Example:

```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b
```

Usage:

```python
MathUtils.add(1, 2)
```

A static method is simply namespaced inside the class.

If the operation does not need object or class state, a standalone function may sometimes be clearer.

______________________________________________________________________

# 12. Instance vs Class vs Static Method

| Method | First automatic argument | Typical purpose |
|---|---|---|
| Instance method | `self` | Instance state/behavior |
| Class method | `cls` | Class-level behavior/factories |
| Static method | None | Utility logically grouped with class |

Interviewers often ask this directly.

______________________________________________________________________

# 13. Encapsulation

Encapsulation means controlling how an object's internal state is accessed and modified.

Python does not enforce private fields in the same way as some languages.

Instead, Python uses conventions and name mangling.

Example:

```python
class User:
    def __init__(self):
        self._name = "Riyaz"
```

A single underscore means:

> This is intended for internal use.

It is a convention.

______________________________________________________________________

# 14. Double Underscore and Name Mangling

Example:

```python
class User:
    def __init__(self):
        self.__token = "secret"
```

Python name-mangles the attribute to something similar to:

```text
_User__token
```

This is not true security or access control.

It mainly helps avoid accidental name collisions, especially with inheritance.

______________________________________________________________________

# 15. Properties

A property allows method-like behavior to be accessed like an attribute.

Example:

```python
class User:
    def __init__(self, age):
        self._age = age

    @property
    def age(self):
        return self._age
```

Usage:

```python
user.age
```

instead of:

```python
user.age()
```

______________________________________________________________________

# 16. Property Setter

You can define controlled assignment:

```python
class User:
    def __init__(self, age):
        self.age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("age cannot be negative")

        self._age = value
```

Now validation is centralized.

______________________________________________________________________

# 17. Why Use Properties?

Properties are useful when:

- Validation is required.
- A value is derived.
- You want to preserve an attribute-like API.
- You need controlled access.

They allow internal implementation to change without necessarily changing the public API.

______________________________________________________________________

# 18. Inheritance

Inheritance allows a class to derive behavior from another class.

Example:

```python
class Animal:
    def speak(self):
        return "sound"


class Dog(Animal):
    def speak(self):
        return "bark"
```

`Dog` inherits from `Animal` and overrides `speak`.

______________________________________________________________________

# 19. Method Overriding

A subclass can redefine an inherited method.

```python
class Animal:
    def speak(self):
        return "sound"


class Dog(Animal):
    def speak(self):
        return "bark"
```

Calling:

```python
Dog().speak()
```

uses the subclass implementation.

______________________________________________________________________

# 20. `super()`

`super()` allows a class to access behavior from its parent according to the method resolution order.

Example:

```python
class Animal:
    def __init__(self, name):
        self.name = name


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
```

This avoids directly hard-coding the parent class name.

______________________________________________________________________

# 21. Why Prefer `super()`?

`super()` supports cooperative inheritance.

It is especially important with multiple inheritance because Python can follow the MRO rather than simply calling one
hard-coded parent.

______________________________________________________________________

# 22. Polymorphism

Polymorphism means different objects can provide compatible behavior through a common interface.

Example:

```python
class Dog:
    def speak(self):
        return "bark"


class Cat:
    def speak(self):
        return "meow"


def make_sound(animal):
    return animal.speak()
```

The function does not need to know the concrete type.

______________________________________________________________________

# 23. Duck Typing

Python often relies on duck typing:

> If an object supports the required behavior, its concrete type may not matter.

Example:

```python
def process(writer):
    writer.write("hello")
```

Any object implementing a compatible `write()` method can potentially be used.

This is one reason Python code can be flexible without deep inheritance hierarchies.

______________________________________________________________________

# 24. Composition

Composition means building an object using other objects rather than inheriting their behavior.

Example:

```python
class UserService:
    def __init__(self, repository):
        self.repository = repository
```

The service has a repository.

This is a "has-a" relationship.

______________________________________________________________________

# 25. Composition vs Inheritance

Inheritance:

```text
Dog is an Animal
```

Composition:

```text
UserService has a Repository
```

Composition is often preferable when behavior should be replaceable or independently testable.

Backend applications frequently use composition for:

- Services
- Repositories
- Clients
- Caches
- Validators
- Message publishers

______________________________________________________________________

# 26. Dependency Injection

Composition naturally leads to dependency injection.

Instead of:

```python
class UserService:
    def __init__(self):
        self.repository = UserRepository()
```

prefer when appropriate:

```python
class UserService:
    def __init__(self, repository):
        self.repository = repository
```

Then:

```python
repository = UserRepository()
service = UserService(repository)
```

This makes the service easier to:

- Test
- Replace
- Configure
- Reuse

______________________________________________________________________

# 27. Abstract Base Classes

Python provides abstract base classes through:

```python
from abc import ABC, abstractmethod
```

Example:

```python
class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount):
        pass
```

A concrete implementation can provide:

```python
class StripeProcessor(PaymentProcessor):
    def charge(self, amount):
        ...
```

Abstract classes define expected interfaces.

______________________________________________________________________

# 28. Abstract Classes vs Duck Typing

Abstract base classes explicitly define an inheritance-based contract.

Duck typing relies on behavior.

### ABC

```python
class Repository(ABC):
    @abstractmethod
    def get(self, id):
        ...
```

### Duck typing

```python
def load(repository):
    return repository.get(1)
```

The best approach depends on project requirements and team conventions.

______________________________________________________________________

# 29. Protocols

Python's typing system also provides structural interfaces through `Protocol`.

Conceptually:

```python
from typing import Protocol


class Repository(Protocol):
    def get(self, user_id: int):
        ...
```

A class does not necessarily need to inherit from `Repository` if it provides compatible behavior.

This fits naturally with duck typing and static type checking.

For modern Python backend development, understand both ABCs and protocols.

______________________________________________________________________

# 30. Method Resolution Order

Python determines method lookup order using the Method Resolution Order (MRO).

Example:

```python
class A:
    ...


class B(A):
    ...


class C(A):
    ...


class D(B, C):
    ...
```

You can inspect it with:

```python
D.mro()
```

or:

```python
D.__mro__
```

Python uses C3 linearization to determine the order.

______________________________________________________________________

# 31. Multiple Inheritance

Python supports:

```python
class Child(ParentA, ParentB):
    ...
```

Multiple inheritance can be useful but can also increase complexity.

Potential problems include:

- Confusing MRO
- Diamond inheritance
- Coupled parent classes
- Difficult initialization

Use it deliberately.

______________________________________________________________________

# 32. Diamond Inheritance

Example:

```text
      A
     / \
    B   C
     \ /
      D
```

`B` and `C` inherit from `A`.

`D` inherits from both `B` and `C`.

Python's MRO determines the method lookup order and allows cooperative multiple inheritance when classes correctly use
`super()`.

______________________________________________________________________

# 33. Cooperative Multiple Inheritance

Consider:

```python
class A:
    def process(self):
        print("A")
        super().process()
```

and similarly structured classes.

Using:

```python
super()
```

allows the next class in the MRO to participate.

Hard-coding:

```python
A.process(self)
```

can bypass the cooperative MRO.

______________________________________________________________________

# 34. `object`

In modern Python, normal classes ultimately derive from:

```python
object
```

For example:

```python
class User:
    pass
```

is effectively based on `object`.

This provides fundamental object behavior.

______________________________________________________________________

# 35. Special Methods / Dunder Methods

Python objects can customize language behavior using special methods.

Examples:

```python
__init__
__str__
__repr__
__len__
__eq__
__lt__
__iter__
__next__
__enter__
__exit__
```

These integrate objects with Python's language features.

______________________________________________________________________

# 36. `__str__` vs `__repr__`

`__str__` is intended for a readable representation.

`__repr__` is intended to provide a more developer-oriented representation.

Example:

```python
class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"User(user_id={self.user_id!r})"
```

Good representations make debugging and logging easier.

______________________________________________________________________

# 37. Equality

Objects can define equality with:

```python
__eq__
```

Example:

```python
class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented

        return self.user_id == other.user_id
```

Be careful when implementing equality because it can affect hashing and dictionary/set behavior.

______________________________________________________________________

# 38. Hashing and Equality

If an object is used as a dictionary key or set element, its hashing/equality contract matters.

The important rule is:

> Objects that compare equal should have the same hash value.

Mutable objects used as hash keys can cause correctness problems if their hash-relevant state changes.

This connects OOP design with the collections chapter.

______________________________________________________________________

# 39. SOLID Principles

SOLID is a group of object-oriented design principles.

The five principles are:

- Single Responsibility Principle
- Open/Closed Principle
- Liskov Substitution Principle
- Interface Segregation Principle
- Dependency Inversion Principle

You should understand these conceptually and be able to recognize them in backend code.

______________________________________________________________________

# 40. Single Responsibility Principle

A class should have a focused responsibility.

Bad:

```python
class UserService:
    def create_user(self):
        ...

    def send_email(self):
        ...

    def generate_pdf(self):
        ...

    def save_to_database(self):
        ...
```

This class has many unrelated responsibilities.

Better separation might be:

```text
UserService
EmailService
PdfGenerator
UserRepository
```

The goal is cohesive responsibilities, not creating a class for every tiny operation.

______________________________________________________________________

# 41. Open/Closed Principle

Software should generally be open for extension but closed for unnecessary modification.

Suppose payment behavior is represented by implementations:

```python
class PaymentProcessor:
    ...
```

New payment methods can be added through new implementations rather than repeatedly changing a giant conditional block.

The principle is about reducing modification of stable code when adding behavior.

______________________________________________________________________

# 42. Liskov Substitution Principle

Subtypes should be usable wherever their base type is expected without breaking the expected behavior.

A subclass should honor the contract established by the abstraction.

If:

```python
Bird
```

defines behavior requiring all birds to fly, introducing:

```python
Penguin
```

may reveal a poor abstraction.

The problem is often the base abstraction itself.

______________________________________________________________________

# 43. Interface Segregation Principle

Clients should not be forced to depend on methods they do not need.

Instead of:

```python
class HugeRepositoryInterface:
    create()
    read()
    update()
    delete()
    export()
    archive()
    ...
```

consider smaller focused interfaces when the application benefits from them.

Python's duck typing and protocols can make this particularly natural.

______________________________________________________________________

# 44. Dependency Inversion Principle

High-level business logic should depend on abstractions rather than concrete low-level implementations.

Example:

```python
class UserService:
    def __init__(self, repository):
        self.repository = repository
```

The service depends on repository behavior rather than constructing a specific database implementation internally.

This supports testing and replaceability.

______________________________________________________________________

# 45. OOP in Backend Architecture

A typical backend can use:

```text
API layer
    ↓
Service layer
    ↓
Repository layer
    ↓
Infrastructure
```

Classes can represent:

- Domain entities
- Services
- Repositories
- External clients
- Configuration
- Validation components

However, not every function needs to become a class.

Python supports procedural, functional and object-oriented styles.

Use the simplest abstraction that fits the problem.

______________________________________________________________________

# 46. OOP and Testing

Composition improves testing.

Example:

```python
class UserService:
    def __init__(self, repository):
        self.repository = repository
```

A test can provide a fake:

```python
fake_repository = FakeRepository()

service = UserService(fake_repository)
```

This avoids requiring a real database for every unit test.

Dependency injection therefore improves testability.

______________________________________________________________________

# 47. Common OOP Mistakes

## Mistake 1 — Overusing inheritance

Not every relationship is an "is-a" relationship.

Prefer composition when appropriate.

______________________________________________________________________

## Mistake 2 — Giant classes

A class with dozens of unrelated responsibilities is difficult to maintain.

______________________________________________________________________

## Mistake 3 — Mutable class attributes

Shared mutable state can accidentally leak between instances.

______________________________________________________________________

## Mistake 4 — Using static methods for everything

A static method is not automatically better than a normal function.

Use it when class namespace grouping provides value.

______________________________________________________________________

## Mistake 5 — Misusing private attributes

Double underscore is not security.

It is name mangling.

______________________________________________________________________

## Mistake 6 — Deep inheritance hierarchies

Deep inheritance can make behavior and MRO difficult to reason about.

______________________________________________________________________

## Mistake 7 — Calling concrete dependencies internally

This makes replacement and testing harder.

Prefer dependency injection where it provides value.

______________________________________________________________________

# 48. Interview Questions & Answers

## Q1. What is a class?

**Answer:**

A class defines attributes and behavior used to create objects.

It acts as a blueprint/type for instances.

______________________________________________________________________

## Q2. What is an object?

**Answer:**

An object is an instance of a class containing state and behavior.

______________________________________________________________________

## Q3. What is `self`?

**Answer:**

`self` is the conventional name for the current instance passed to an instance method.

______________________________________________________________________

## Q4. What does `__init__` do?

**Answer:**

It initializes an instance after it has been created.

Object allocation is associated with `__new__`.

______________________________________________________________________

## Q5. What is the difference between instance and class attributes?

**Answer:**

Instance attributes belong to individual objects.

Class attributes are associated with the class and can be shared through instances unless shadowed.

______________________________________________________________________

## Q6. Why are mutable class attributes dangerous?

**Answer:**

All instances can access the same mutable object, causing changes made through one instance to affect another
unexpectedly.

______________________________________________________________________

## Q7. What is a class method?

**Answer:**

A method decorated with `@classmethod` that receives the class as its first argument, conventionally `cls`.

It is commonly used for alternative constructors and class-level behavior.

______________________________________________________________________

## Q8. What is a static method?

**Answer:**

A method decorated with `@staticmethod` that does not automatically receive an instance or class.

It is useful for behavior logically grouped with a class but independent of object/class state.

______________________________________________________________________

## Q9. What is encapsulation in Python?

**Answer:**

It means organizing and controlling access to object state.

Python primarily relies on conventions such as `_name` and mechanisms such as name mangling for `__name`.

______________________________________________________________________

## Q10. What is name mangling?

**Answer:**

Double-underscore attributes are transformed internally to reduce accidental name collisions, for example:

```text
__token
```

inside `User` becomes similar to:

```text
_User__token
```

It is not a security mechanism.

______________________________________________________________________

## Q11. What is a property?

**Answer:**

A property exposes method-backed behavior through attribute syntax.

It is useful for validation, computed values and controlled access.

______________________________________________________________________

## Q12. What is inheritance?

**Answer:**

Inheritance allows a class to derive behavior and structure from another class.

______________________________________________________________________

## Q13. What is method overriding?

**Answer:**

A subclass provides its own implementation of an inherited method.

______________________________________________________________________

## Q14. What is `super()`?

**Answer:**

`super()` provides access to behavior from the next class in the MRO.

It is especially important for cooperative inheritance and multiple inheritance.

______________________________________________________________________

## Q15. What is polymorphism?

**Answer:**

Polymorphism allows different objects to be used through compatible behavior or interfaces.

______________________________________________________________________

## Q16. What is duck typing?

**Answer:**

Duck typing focuses on whether an object supports the required operations rather than requiring a particular concrete
type.

______________________________________________________________________

## Q17. What is composition?

**Answer:**

Composition builds an object using other objects.

For example:

```python
UserService(repository)
```

means the service has a repository dependency.

______________________________________________________________________

## Q18. Composition vs inheritance?

**Answer:**

Inheritance models an "is-a" relationship.

Composition models a "has-a" relationship.

Composition is often more flexible for backend dependencies and testing.

______________________________________________________________________

## Q19. What is dependency injection?

**Answer:**

Dependency injection means providing dependencies to an object rather than having the object construct them internally.

It improves replaceability and testability.

______________________________________________________________________

## Q20. What is an abstract base class?

**Answer:**

An ABC defines an explicit inheritance-based interface/contract and can require subclasses to implement abstract
methods.

______________________________________________________________________

## Q21. What is a Protocol?

**Answer:**

A `typing.Protocol` describes a structural interface.

A class can satisfy the protocol by providing compatible behavior without necessarily inheriting from it.

______________________________________________________________________

## Q22. What is MRO?

**Answer:**

MRO, or Method Resolution Order, determines the order in which Python searches classes for attributes and methods.

It can be inspected with:

```python
Class.mro()
```

______________________________________________________________________

## Q23. What is C3 linearization?

**Answer:**

C3 linearization is the algorithm Python uses to calculate a consistent MRO for multiple inheritance.

You mainly need to understand that it determines a predictable cooperative method lookup order.

______________________________________________________________________

## Q24. What is multiple inheritance?

**Answer:**

A class inherits from multiple parent classes.

It can be useful but increases complexity, especially around MRO and initialization.

______________________________________________________________________

## Q25. What is the difference between `__str__` and `__repr__`?

**Answer:**

`__str__` is intended for a user-friendly representation.

`__repr__` is intended to be a more developer-oriented representation useful for debugging.

______________________________________________________________________

## Q26. Why does equality affect hashing?

**Answer:**

Objects that compare equal must have the same hash value if they are used in hash-based collections.

Incorrect `__eq__`/`__hash__` implementations can cause dictionary/set bugs.

______________________________________________________________________

## Q27. What is SRP?

**Answer:**

Single Responsibility Principle says a class should have a focused responsibility rather than accumulating unrelated
reasons to change.

______________________________________________________________________

## Q28. What is Dependency Inversion?

**Answer:**

High-level business logic should depend on abstractions rather than concrete low-level implementations.

Dependency injection is a common technique for achieving this.

______________________________________________________________________

# 49. Scenario-Based Questions

## Scenario 1 — Shared User State

You create:

```python
class User:
    permissions = []
```

Two users are created. Adding a permission to one user changes the other user's permissions.

**Question:** Why?

**Answer:**

`permissions` is a mutable class attribute shared through the class.

Create the list in `__init__` instead:

```python
class User:
    def __init__(self):
        self.permissions = []
```

______________________________________________________________________

## Scenario 2 — Service Is Hard to Test

You have:

```python
class UserService:
    def __init__(self):
        self.repository = PostgreSQLUserRepository()
```

Unit tests now require a real database.

**Question:** What would you change?

**Answer:**

Inject the repository:

```python
class UserService:
    def __init__(self, repository):
        self.repository = repository
```

Tests can provide a fake/mock repository.

______________________________________________________________________

## Scenario 3 — Huge Conditional Payment Service

A class contains:

```python
if provider == "stripe":
    ...
elif provider == "paypal":
    ...
elif provider == "razorpay":
    ...
elif provider == "..."
```

and keeps growing.

**Question:** What OOP/design approach could improve it?

**Answer:**

Define a common payment interface/contract and provide separate implementations.

For example:

```python
class PaymentProcessor:
    def charge(self, amount):
        ...
```

Then inject the appropriate implementation.

This can improve separation of responsibilities and extensibility.

______________________________________________________________________

## Scenario 4 — Inheritance Is Becoming Complex

A backend has six levels of inheritance and developers struggle to understand which implementation executes.

**Question:** What would you consider?

**Answer:**

Consider replacing parts of the hierarchy with composition.

Extract independent behaviors into collaborators and inject them where required.

______________________________________________________________________

## Scenario 5 — Incorrect Subclass Behavior

A subclass overrides a method but violates assumptions made by callers of the base class.

**Question:** Which SOLID principle is relevant?

**Answer:**

The Liskov Substitution Principle.

The subclass should honor the behavioral contract expected from the base abstraction.

______________________________________________________________________

## Scenario 6 — Static Method Everywhere

A developer converts every helper into:

```python
@staticmethod
```

inside a class.

**Question:** Is this automatically good OOP?

**Answer:**

No.

If a function does not need class or instance state and has no meaningful relationship to the class, a module-level
function may be simpler and clearer.

______________________________________________________________________

# 50. Practice Exercises

## Exercise 1 — User Class

Create a `User` class with:

- `id`
- `name`
- `email`
- `is_active`

Add:

```python
activate()
deactivate()
```

methods.

______________________________________________________________________

## Exercise 2 — Alternative Constructor

Add:

```python
@classmethod
def from_dict(cls, data):
    ...
```

to construct a user from a dictionary.

______________________________________________________________________

## Exercise 3 — Property Validation

Create a property:

```python
email
```

that validates the value before assigning it.

______________________________________________________________________

## Exercise 4 — Repository Injection

Create:

```python
UserService(repository)
```

where the repository is injected instead of instantiated internally.

Write a fake repository for unit testing.

______________________________________________________________________

## Exercise 5 — Payment Strategy

Create a common payment contract and two implementations.

Example:

```text
PaymentProcessor
    ├── StripeProcessor
    └── PayPalProcessor
```

Inject the processor into an order/payment service.

______________________________________________________________________

## Exercise 6 — Composition Refactor

Start with an inheritance-heavy design.

Refactor at least one relationship into composition.

Explain why the new design is easier to change or test.

______________________________________________________________________

## Exercise 7 — MRO

Create a small multiple-inheritance example.

Inspect:

```python
Class.mro()
```

Predict the method lookup order before running it.

______________________________________________________________________

## Exercise 8 — SOLID Review

Take a backend service you have written before.

Identify:

- One SRP violation
- One dependency-inversion opportunity
- One place where composition could replace inheritance
- One interface that could be smaller

______________________________________________________________________

# 51. Quick Revision

| Concept | Key Point |
|---|---|
| Class | Defines object structure/behavior |
| Object | Instance of a class |
| `self` | Current instance |
| `__init__` | Initializes instance state |
| `__new__` | Associated with object creation |
| Instance attribute | Per-object state |
| Class attribute | Associated with class |
| Instance method | Receives `self` |
| Class method | Receives `cls` |
| Static method | Receives neither automatically |
| Encapsulation | Controls/organizes access to state |
| `_name` | Internal-use convention |
| `__name` | Name mangling |
| `property` | Attribute-style controlled behavior |
| Inheritance | "Is-a" relationship |
| Composition | "Has-a" relationship |
| Polymorphism | Common behavior across different objects |
| Duck typing | Behavior over concrete type |
| `super()` | Uses next class in MRO |
| MRO | Method lookup order |
| Multiple inheritance | Multiple base classes |
| ABC | Explicit inheritance-based contract |
| Protocol | Structural typing contract |
| `__str__` | User-friendly representation |
| `__repr__` | Developer/debug representation |
| `__eq__` | Equality behavior |
| `__hash__` | Hashing behavior |
| SRP | Focused responsibility |
| OCP | Extend without unnecessary modification |
| LSP | Subtypes honor base contract |
| ISP | Focused interfaces |
| DIP | Depend on abstractions |
| Dependency injection | Provide dependencies externally |

______________________________________________________________________

# 52. Completion Checklist

Before moving to File 9, make sure you can explain:

- [ ] Classes and objects
- [ ] `self`
- [ ] `__init__`
- [ ] `__new__`
- [ ] Instance attributes
- [ ] Class attributes
- [ ] Mutable class attribute trap
- [ ] Instance methods
- [ ] Class methods
- [ ] Static methods
- [ ] Encapsulation
- [ ] Single underscore convention
- [ ] Double underscore/name mangling
- [ ] Properties
- [ ] Property setters
- [ ] Inheritance
- [ ] Method overriding
- [ ] `super()`
- [ ] Polymorphism
- [ ] Duck typing
- [ ] Composition
- [ ] Composition vs inheritance
- [ ] Dependency injection
- [ ] Abstract base classes
- [ ] Protocols
- [ ] MRO
- [ ] C3 linearization
- [ ] Multiple inheritance
- [ ] Diamond inheritance
- [ ] Cooperative inheritance
- [ ] Dunder methods
- [ ] `__str__`
- [ ] `__repr__`
- [ ] `__eq__`
- [ ] `__hash__`
- [ ] Hash/equality contract
- [ ] SOLID principles
- [ ] Backend OOP architecture
- [ ] OOP and testability
- [ ] Common OOP design mistakes

______________________________________________________________________

# 53. Interview Readiness Test

Without looking at the notes, answer these aloud:

1. What is a class?
1. What is an object?
1. What is `self`?
1. What does `__init__` do?
1. What is the role of `__new__`?
1. What is the difference between instance and class attributes?
1. Why are mutable class attributes dangerous?
1. Explain instance, class and static methods.
1. What is encapsulation in Python?
1. What is name mangling?
1. Is `__private` actually private?
1. What is a property and when would you use one?
1. What is inheritance?
1. What is method overriding?
1. What does `super()` do?
1. What is polymorphism?
1. What is duck typing?
1. What is composition?
1. Composition vs inheritance: when would you choose each?
1. What is dependency injection?
1. What is an abstract base class?
1. What is a Protocol?
1. What is MRO?
1. What is C3 linearization?
1. Explain multiple inheritance and the diamond problem.
1. Why is cooperative `super()` important?
1. What is the difference between `__str__` and `__repr__`?
1. How do `__eq__` and `__hash__` interact?
1. Explain the five SOLID principles.
1. Give a backend example of Dependency Inversion.
1. Why does composition improve testing?
1. When can OOP make Python code worse rather than better?

If you can answer these clearly and implement the exercises without relying heavily on the notes, this chapter is
complete.

______________________________________________________________________

**Previous:** [7. Python Modules, Packages & Virtual Environments](./07-python-modules-packages.md)

**Next:** [9. Python Memory Management & Internals](./09-python-advanced-oop.md)

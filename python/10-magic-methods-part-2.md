# File: python/10-magic-methods-part-2.md

# Python Advanced - Lesson 10 (Part 2)
# Magic Methods - Customising Object Behaviour

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Object Model & Memory
>
> **Lesson:** 10 (Part 2)
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 90 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- Why object representation matters
- The difference between `__str__()` and `__repr__()`
- How `__len__()` works
- How Python determines truthiness using `__bool__()`
- How object equality works with `__eq__()`
- Comparison magic methods
- Hashing and `__hash__()`
- Operator overloading
- Production use cases
- Common interview questions

---

# Recap

In Part 1, we learned about an object's lifecycle.

```
__new__()

↓

__init__()

↓

Object Used

↓

__del__()
```

Now we'll learn how Python decides:

- How an object is printed
- Whether two objects are equal
- Whether an object is "truthy"
- How objects are compared
- How operators like `+` work

---

# __str__() — Human-Friendly Representation

Suppose we create a simple class.

```python
class User:

    def __init__(self, name):

        self.name = name


user = User("Alice")

print(user)
```

Output

```
<__main__.User object at 0x1042ab4c0>
```

Not very useful.

Python doesn't know how to display your object.

---

# Defining __str__()

```python
class User:

    def __init__(self, name):

        self.name = name

    def __str__(self):

        return f"User(name={self.name})"
```

```python
user = User("Alice")

print(user)
```

Output

```
User(name=Alice)
```

Much more readable.

---

# When is __str__() Called?

Python automatically calls it when you use:

```python
print(user)

str(user)

f"{user}"
```

You almost never call:

```python
user.__str__()
```

directly.

---

# __repr__() — Developer Representation

Imagine debugging.

```python
users = [
    User("Alice"),
    User("Bob")
]

print(users)
```

Without `__repr__()`:

```
[<User object>, <User object>]
```

Not helpful.

---

# Defining __repr__()

```python
class User:

    def __init__(self, name):

        self.name = name

    def __repr__(self):

        return f"User(name='{self.name}')"
```

Now:

```python
users = [
    User("Alice"),
    User("Bob")
]

print(users)
```

Output

```
[User(name='Alice'), User(name='Bob')]
```

---

# __str__() vs __repr__()

```python
class User:

    def __init__(self, name):

        self.name = name

    def __str__(self):

        return f"Hello {self.name}"

    def __repr__(self):

        return f"User(name='{self.name}')"
```

```python
user = User("Alice")

print(user)

print(repr(user))
```

Output

```
Hello Alice

User(name='Alice')
```

---

# When Should You Use Each?

Use `__str__()` for:

- End users
- Logs
- CLI output

Use `__repr__()` for:

- Developers
- Debugging
- Interactive shell
- Logging collections

---

# __len__()

Python uses `__len__()` whenever you call:

```python
len(object)
```

Example

```python
class Team:

    def __init__(self):

        self.members = [
            "Alice",
            "Bob",
            "Chris"
        ]

    def __len__(self):

        return len(self.members)
```

```python
team = Team()

print(len(team))
```

Output

```
3
```

---

# __bool__()

Every object in Python has a truth value.

Example

```python
if []:

    print("True")
```

Nothing prints because an empty list is False.

You can customise this.

```python
class BankAccount:

    def __init__(self, balance):

        self.balance = balance

    def __bool__(self):

        return self.balance > 0
```

Usage

```python
account = BankAccount(100)

if account:

    print("Account has funds")
```

Output

```
Account has funds
```

---

# __eq__()

Suppose we compare two users.

```python
class User:

    def __init__(self, id):

        self.id = id
```

```python
user1 = User(1)
user2 = User(1)

print(user1 == user2)
```

Output

```
False
```

Why?

Because Python compares object identity by default.

---

# Custom Equality

```python
class User:

    def __init__(self, id):

        self.id = id

    def __eq__(self, other):

        return self.id == other.id
```

Now

```python
print(User(1) == User(1))
```

Output

```
True
```

---

# Comparison Magic Methods

Python provides several comparison methods.

| Method | Operator |
|---------|----------|
| `__lt__()` | `<` |
| `__le__()` | `<=` |
| `__gt__()` | `>` |
| `__ge__()` | `>=` |

Example

```python
class Product:

    def __init__(self, price):

        self.price = price

    def __lt__(self, other):

        return self.price < other.price
```

```python
print(Product(10) < Product(20))
```

Output

```
True
```

---

# __hash__()

Hash values are used by:

- Dictionaries
- Sets

Example

```python
class User:

    def __init__(self, id):

        self.id = id

    def __hash__(self):

        return hash(self.id)
```

Now objects with the same identifier can participate correctly in hash-based collections when combined with a compatible `__eq__()` implementation.

A key rule:

> If you override `__eq__()`, you should also consider whether you need a matching `__hash__()` implementation. Objects that compare equal should produce the same hash value.

---

# Operator Overloading

Operators are simply magic methods.

| Operator | Magic Method |
|-----------|--------------|
| `+` | `__add__()` |
| `-` | `__sub__()` |
| `*` | `__mul__()` |
| `/` | `__truediv__()` |

Example

```python
class Money:

    def __init__(self, amount):

        self.amount = amount

    def __add__(self, other):

        return Money(
            self.amount + other.amount
        )

    def __repr__(self):

        return f"Money({self.amount})"
```

```python
wallet = Money(50)

bonus = Money(25)

print(wallet + bonus)
```

Output

```
Money(75)
```

Python internally performs something similar to:

```python
wallet.__add__(bonus)
```

---

# Production Insight

Magic methods are used throughout modern Python frameworks.

Examples include:

Dataclasses

```python
@dataclass
class User:
    ...
```

Python automatically generates methods like:

- `__init__()`
- `__repr__()`
- `__eq__()`

ORM Models

Database models often implement custom equality and representation methods to make debugging easier.

Collections

Custom collection classes frequently implement:

```python
__len__()

__iter__()

__contains__()
```

Numeric Types

Libraries such as NumPy overload operators so mathematical expressions behave naturally.

---

# Best Practices

✅ Keep `__repr__()` unambiguous.

✅ Keep `__str__()` user-friendly.

✅ Ensure objects that compare equal also produce the same hash.

✅ Only overload operators when the behaviour is intuitive.

❌ Avoid surprising behaviour.

For example:

```python
user1 + user2
```

only makes sense if adding two users has a clear meaning.

---

# Questions

### Question

> What is the difference between `__str__()` and `__repr__()`?

### Answer

`__str__()` provides a human-readable representation intended for end users, while `__repr__()` provides a developer-focused representation useful for debugging and interactive sessions. If `__str__()` is not implemented, Python falls back to `__repr__()`.

---

### Question

> Why should `__eq__()` and `__hash__()` usually be implemented together?

### Answer

Hash-based collections such as dictionaries and sets rely on equal objects having identical hash values. If objects compare equal but have different hashes, collection behaviour becomes inconsistent.

---

### Questions

> What is operator overloading?

### Answer

Operator overloading allows custom objects to define the behaviour of operators such as `+`, `-` and `<` by implementing the corresponding magic methods like `__add__()` and `__lt__()`.

---

# Practical Lesson

Create a file:

```
magic_methods_examples.py
```

```python
class Employee:

    def __init__(self, name, salary):

        self.name = name
        self.salary = salary

    def __repr__(self):

        return (
            f"Employee(name='{self.name}', "
            f"salary={self.salary})"
        )

    def __eq__(self, other):

        return self.salary == other.salary

    def __lt__(self, other):

        return self.salary < other.salary
```

```python
employee1 = Employee("Alice", 50000)

employee2 = Employee("Bob", 60000)

print(employee1)

print(employee1 == employee2)

print(employee1 < employee2)
```

Expected Output

```
Employee(name='Alice', salary=50000)

False

True
```

---

# Questions

## Question 1

What is the purpose of `__str__()`?

### Answer

It provides a human-readable string representation of an object, typically used by `print()` and `str()`.

---

## Question 2

When is `__repr__()` used?

### Answer

It is used for debugging, interactive sessions and as the fallback representation when `__str__()` is not implemented.

---

## Question 3

What does `__len__()` do?

### Answer

It defines the value returned by the built-in `len()` function for an object.

---

## Question 4

Why is `__bool__()` useful?

### Answer

It allows a class to define when its instances should evaluate to `True` or `False` in Boolean contexts.

---

## Question 5

What is operator overloading?

### Answer

Operator overloading allows custom classes to define how operators such as `+`, `-`, `<` and `==` behave by implementing the corresponding magic methods.

---

## Question 6

Why should `__eq__()` and `__hash__()` be consistent?

### Answer

Because dictionaries and sets rely on equal objects producing the same hash value. Violating this rule can lead to incorrect behaviour in hash-based collections.

---

# Assignment

## Exercise 1

Create a `Book` class with custom `__str__()` and `__repr__()` methods.

Print a single object and a list of objects to observe the difference.

---

## Exercise 2

Create a `ShoppingCart` class that implements `__len__()`.

Return the number of products in the cart.

---

## Exercise 3

Create a `Wallet` class that overloads the `+` operator using `__add__()`.

Adding two wallets should return a new wallet containing the combined balance.

---

## Exercise 4

Create a `Student` class that compares students by GPA using `__lt__()`.

Sort a list of students using the built-in `sorted()` function.

---

# Summary

In this lesson, you learned:

- ✅ The difference between `__str__()` and `__repr__()`.
- ✅ How `__len__()` customises the `len()` function.
- ✅ How `__bool__()` controls truthiness.
- ✅ How `__eq__()` defines object equality.
- ✅ How comparison magic methods work.
- ✅ Why `__hash__()` matters for dictionaries and sets.
- ✅ How operator overloading makes custom classes behave like built-in types.
- ✅ Production best practices for implementing magic methods.

---

# What's Next

**File:**
[11-Dataclasses](11-dataclasses.md)

Topics:

- Why Dataclasses Exist
- `@dataclass`
- Automatically Generated Magic Methods
- `field()`
- `default_factory`
- Frozen Dataclasses
- Ordered Dataclasses
- Dataclass Inheritance
- Production Examples

```

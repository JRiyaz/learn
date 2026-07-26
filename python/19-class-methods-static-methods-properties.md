# File: python/19-class-methods-static-methods-properties.md

# Python Advanced - Lesson 19
# Instance Methods, Class Methods, Static Methods & Properties

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced OOP
>
> **Lesson:** 19
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 110 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- The three types of methods in Python
- Instance methods
- Class methods
- Static methods
- The `@property` decorator
- Property setters and deleters
- Read-only properties
- When to use each method type
- Production examples

---

# Why Does Python Have Different Method Types?

Imagine you're building an Employee Management System.

Some operations work on an individual employee.

```
Employee

↓

calculate_salary()
```

Some operations affect the whole company.

```
Employee

↓

total_employees
```

Some operations don't need either.

```
validate_email()
```

Python provides different method types because they operate on different kinds of data.

---

# The Three Method Types

| Method Type | First Parameter | Operates On |
|--------------|----------------|-------------|
| Instance Method | `self` | Individual object |
| Class Method | `cls` | Class |
| Static Method | None | Neither object nor class |

Think of it like this.

```
Object

↓

Instance Method
```

```
Class

↓

Class Method
```

```
Independent Utility

↓

Static Method
```

---

# Instance Methods

These are the methods you've been using throughout this course.

Example

```python
class Employee:

    def __init__(self, name):

        self.name = name

    def introduce(self):

        print(f"My name is {self.name}")
```

Usage

```python
employee = Employee("Alice")

employee.introduce()
```

Output

```
My name is Alice
```

---

# Understanding self

When Python executes

```python
employee.introduce()
```

it internally performs something similar to

```python
Employee.introduce(employee)
```

Therefore,

```python
self
```

is simply the current object.

---

# Class Variables

Before understanding class methods,

we need class variables.

```python
class Employee:

    company = "OpenAI"
```

Every object shares this variable.

```python
employee1 = Employee()

employee2 = Employee()

print(employee1.company)

print(employee2.company)
```

Output

```
OpenAI

OpenAI
```

---

# Instance Variables vs Class Variables

```python
class Employee:

    company = "OpenAI"

    def __init__(self, name):

        self.name = name
```

Each object gets its own

```
name
```

All objects share

```
company
```

---

# Class Methods

Sometimes you need to work with the class itself.

Python provides

```python
@classmethod
```

Example

```python
class Employee:

    company = "OpenAI"

    @classmethod
    def company_name(cls):

        return cls.company
```

Usage

```python
print(Employee.company_name())
```

Output

```
OpenAI
```

---

# Understanding cls

When Python executes

```python
Employee.company_name()
```

it internally performs something similar to

```python
Employee.company_name(Employee)
```

Therefore,

```python
cls
```

is the class itself.

---

# Counting Objects

Class methods are commonly used with class variables.

```python
class Employee:

    total = 0

    def __init__(self, name):

        self.name = name

        Employee.total += 1

    @classmethod
    def total_employees(cls):

        return cls.total
```

Usage

```python
Employee("Alice")

Employee("Bob")

print(Employee.total_employees())
```

Output

```
2
```

---

# Alternative Constructors

One of the most common uses of class methods is creating alternative constructors.

Suppose data comes from a CSV file.

```
Alice,30
```

Instead of manually splitting every line,

we create another constructor.

```python
class Employee:

    def __init__(self, name, age):

        self.name = name

        self.age = age

    @classmethod
    def from_csv(cls, data):

        name, age = data.split(",")

        return cls(name, int(age))
```

Usage

```python
employee = Employee.from_csv(
    "Alice,30"
)

print(employee.name)

print(employee.age)
```

Output

```
Alice

30
```

---

# Why Use cls Instead of Employee?

Notice

```python
return cls(...)
```

instead of

```python
return Employee(...)
```

Why?

Because subclasses should also work correctly.

Example

```python
class Manager(Employee):

    pass
```

Now

```python
manager = Manager.from_csv(
    "Bob,45"
)
```

returns a

```
Manager
```

not an `Employee`.

This is why `cls` is preferred.

---

# Static Methods

Some methods belong inside a class,

but don't need either

- object
- class

Python provides

```python
@staticmethod
```

Example

```python
class Employee:

    @staticmethod
    def is_adult(age):

        return age >= 18
```

Usage

```python
print(
    Employee.is_adult(25)
)
```

Output

```
True
```

---

# Why Not Use a Normal Function?

You certainly could.

```python
def is_adult(age):

    return age >= 18
```

However,

if the function logically belongs to the class,

keeping it there improves organisation.

---

# Comparing Method Types

```python
class Example:

    def instance(self):

        ...

    @classmethod
    def class_method(cls):

        ...

    @staticmethod
    def static_method():

        ...
```

| Method | Accesses self | Accesses cls |
|---------|---------------|--------------|
| Instance | ✅ | Indirectly |
| Class | ❌ | ✅ |
| Static | ❌ | ❌ |

---

# Introducing @property

Suppose we have

```python
class Circle:

    def __init__(self, radius):

        self.radius = radius

    def area(self):

        return 3.14159 * self.radius ** 2
```

Usage

```python
circle = Circle(5)

print(circle.area())
```

This works.

But conceptually,

area behaves like an attribute,

not an action.

---

# Using @property

```python
class Circle:

    def __init__(self, radius):

        self.radius = radius

    @property
    def area(self):

        return 3.14159 * self.radius ** 2
```

Usage

```python
circle = Circle(5)

print(circle.area)
```

Output

```
78.53975
```

Notice

No parentheses.

---

# Why Use Properties?

Properties allow us to expose computed values as attributes.

Users write

```python
circle.area
```

instead of

```python
circle.area()
```

The implementation remains hidden.

---

# Property Setter

Suppose we want to validate radius.

```python
class Circle:

    def __init__(self, radius):

        self.radius = radius

    @property
    def radius(self):

        return self._radius

    @radius.setter
    def radius(self, value):

        if value <= 0:

            raise ValueError(
                "Radius must be positive."
            )

        self._radius = value
```

Usage

```python
circle = Circle(10)

circle.radius = 15
```

Works.

```python
circle.radius = -5
```

Raises

```
ValueError
```

---

# Why Use _radius?

Notice

```python
self._radius
```

instead of

```python
self.radius
```

If we wrote

```python
self.radius = value
```

inside the setter,

it would call the setter again,

creating infinite recursion.

The underscore indicates an internal implementation detail.

---

# Read-Only Properties

Simply omit the setter.

```python
class Rectangle:

    def __init__(self, width, height):

        self.width = width

        self.height = height

    @property
    def area(self):

        return self.width * self.height
```

Usage

```python
rectangle = Rectangle(4, 6)

print(rectangle.area)
```

Attempting

```python
rectangle.area = 50
```

raises

```
AttributeError
```

---

# Property Deleter

Properties can also define delete behaviour.

```python
class User:

    def __init__(self, email):

        self._email = email

    @property
    def email(self):

        return self._email

    @email.deleter
    def email(self):

        print("Removing email")

        del self._email
```

Usage

```python
user = User("alice@example.com")

del user.email
```

Output

```
Removing email
```

Deleters are relatively uncommon in production code.

---

# Production Example - Validation

```python
class Product:

    def __init__(self, price):

        self.price = price

    @property
    def price(self):

        return self._price

    @price.setter
    def price(self, value):

        if value < 0:

            raise ValueError(
                "Price cannot be negative."
            )

        self._price = value
```

Validation now happens automatically.

---

# Production Example - Alternative Constructors

Suppose an API returns JSON.

```python
{
    "name": "Alice",
    "age": 30
}
```

```python
class User:

    def __init__(self, name, age):

        self.name = name

        self.age = age

    @classmethod
    def from_dict(cls, data):

        return cls(
            data["name"],
            data["age"]
        )
```

Many frameworks use this pattern.

---

# Production Example - Static Methods

```python
class PasswordValidator:

    @staticmethod
    def is_strong(password):

        return (
            len(password) >= 8
        )
```

The validation belongs conceptually to the class,

but doesn't require object state.

---

# Choosing the Right Method

| Requirement | Use |
|-------------|-----|
| Needs object data | Instance Method |
| Needs class data | Class Method |
| Alternative constructor | Class Method |
| Utility function related to the class | Static Method |
| Computed attribute | Property |
| Attribute validation | Property Setter |

---

# Common Mistakes

## Mistake 1

Using a static method that needs instance data.

```python
@staticmethod
def greet():

    print(self.name)
```

This fails because `self` doesn't exist.

---

## Mistake 2

Hardcoding the class name in a class method.

```python
return Employee(...)
```

Prefer

```python
return cls(...)
```

This supports inheritance.

---

## Mistake 3

Performing expensive database queries inside a property.

```python
@property
def orders(self):

    ...
```

Properties should generally feel like attribute access.

If a property performs slow network or database operations, the API can become surprising.

---

# Best Practices

✅ Use instance methods for object behaviour.

✅ Use class methods for alternative constructors.

✅ Use static methods for class-related utilities.

✅ Use properties to validate or compute attributes.

✅ Keep property access lightweight.

❌ Don't overuse static methods.

❌ Don't hide expensive operations behind properties.

---

# Production Insight

You'll encounter these patterns frequently in backend frameworks.

Examples include:

**Pydantic**

```python
Model.model_validate(...)
```

Class methods are commonly used to construct models from different sources.

**SQLAlchemy**

Model classes often use class-level methods for querying and object creation.

**Django**

Model managers expose class-level behaviour, while model instances expose instance methods.

Properties are widely used for:

- Computed fields
- Validation
- Derived values
- Backward-compatible APIs

---

# Questions

### Question

> What is the difference between an instance method, class method and static method?

### Answer

An instance method operates on an object and receives `self`. A class method operates on the class and receives `cls`. A static method receives neither and is used for utility behaviour logically related to the class.

---

### Question

> When should you use a class method?

### Answer

Class methods are commonly used for alternative constructors, operations involving class-level state and behaviour that should respect inheritance by using `cls`.

---

### Question

> Why use `@property` instead of a getter method?

### Answer

`@property` provides a clean attribute-style interface while allowing validation or computed values behind the scenes. It also lets the implementation evolve without changing the public API.

---

### Question

> Why should class methods use `cls` instead of the class name?

### Answer

Using `cls` allows subclasses to inherit the method correctly. Calling the method on a subclass returns an instance of that subclass instead of always creating the base class.

---

# Practical Lesson

Create a file:

```
method_types_examples.py
```

```python
class Employee:

    company = "OpenAI"

    def __init__(self, name, salary):

        self.name = name
        self.salary = salary

    def introduce(self):

        print(f"I am {self.name}")

    @classmethod
    def from_csv(cls, data):

        name, salary = data.split(",")

        return cls(
            name,
            int(salary)
        )

    @staticmethod
    def valid_salary(amount):

        return amount >= 0

    @property
    def monthly_salary(self):

        return self.salary / 12


employee = Employee.from_csv(
    "Alice,60000"
)

employee.introduce()

print(employee.monthly_salary)

print(
    Employee.valid_salary(5000)
)
```

Expected Output

```
I am Alice

5000.0

True
```

---

# Questions

## Question 1

What is an instance method?

### Answer

An instance method operates on a specific object and receives `self` as its first parameter.

---

## Question 2

When should you use a class method?

### Answer

Use a class method for alternative constructors, operations on class-level state or behaviour that should work correctly with inheritance.

---

## Question 3

When should you use a static method?

### Answer

Use a static method for utility functionality that logically belongs to a class but does not require access to either the instance or the class.

---

## Question 4

What problem does `@property` solve?

### Answer

It allows methods to be exposed as attributes while supporting validation, computed values and implementation changes without affecting callers.

---

## Question 5

Why is `cls` preferred over the class name inside a class method?

### Answer

Because `cls` supports inheritance. Calling the method on a subclass creates instances of that subclass instead of always creating the base class.

---

# Assignment

## Exercise 1

Create a `Student` class with:

- An instance method `introduce()`
- A class method `from_csv()`
- A static method `is_valid_age()`

Test each method.

---

## Exercise 2

Create a `BankAccount` class with a `balance` property.

Use a setter to prevent negative balances.

---

## Exercise 3

Implement a read-only `full_name` property for a `Person` class using `first_name` and `last_name`.

---

## Exercise 4

Explain why the following should be an instance method, class method or static method:

- Calculate a customer's yearly reward points.
- Create a customer from API response data.
- Validate an email address format.
- Return the company's registered name.

---

# Summary

In this lesson, you learned:

- ✅ The differences between instance, class and static methods.
- ✅ How `self` and `cls` work internally.
- ✅ Why class methods are ideal for alternative constructors.
- ✅ When static methods are appropriate.
- ✅ How `@property` creates computed attributes.
- ✅ How property setters validate data.
- ✅ When to create read-only properties.
- ✅ Production best practices for method design.

---

# What's Next

**File:**
[20-Descriptors](20-descriptors.md)

Topics:

- What Descriptors Are
- Descriptor Protocol
- `__get__()`
- `__set__()`
- `__delete__()`
- How `@property` Works Internally
- Data vs Non-Data Descriptors
- Attribute Lookup Order
- Production Examples (ORMs, Validation, Pydantic)

> **Why next?**
>
> You have now learned `@property`. The natural next step is understanding **descriptors**, because `property` itself is implemented using Python's descriptor protocol. Once descriptors make sense, `__slots__` becomes much easier to understand.

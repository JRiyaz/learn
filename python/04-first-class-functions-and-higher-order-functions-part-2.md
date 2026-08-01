# File: python/04-first-class-functions-and-higher-order-functions-part-2.md

# Python Advanced - Lesson 04 (Part 2)

# Lambda Functions, Built-in Higher-Order Functions & Callbacks

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 04 (Part 2)
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 75 Minutes

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What lambda functions are
- When to use lambda functions
- The built-in higher-order functions:
  - `map()`
  - `filter()`
  - `sorted()`
- What callbacks are
- How these concepts are used in backend applications
- Why decorators are built on these concepts

______________________________________________________________________

# Theory

In the previous lesson, we learned that functions are first-class objects.

That means we can:

- Pass functions as arguments
- Return functions
- Store functions in variables

Now let's look at some powerful tools that use this feature.

______________________________________________________________________

# Lambda Functions

A **lambda function** is an anonymous (unnamed) function.

Instead of writing:

```python
def square(number):
    return number * number
```

you can write:

```python
square = lambda number: number * number
```

Both produce the same result.

```python
print(square(5))
```

Output

```
25
```

______________________________________________________________________

# Lambda Syntax

```
lambda parameters: expression
```

Example

```python
multiply = lambda a, b: a * b

print(multiply(4, 5))
```

Output

```
20
```

______________________________________________________________________

# When Should You Use Lambda?

Use lambda for:

- Small functions
- One-line operations
- Sorting
- Mapping
- Filtering

Avoid lambda for:

- Large business logic
- Multiple statements
- Complex conditions

If the function is longer than one expression, use `def`.

______________________________________________________________________

# Example 1 - Sorting by Age

Suppose you have:

```python
users = [

    {"name": "Alice", "age": 28},

    {"name": "Bob", "age": 21},

    {"name": "Charlie", "age": 35}
]
```

Sort by age.

```python
users.sort(key=lambda user: user["age"])

print(users)
```

Output

```python
[
    {'name': 'Bob', 'age': 21},
    {'name': 'Alice', 'age': 28},
    {'name': 'Charlie', 'age': 35}
]
```

Without lambda, you would need another function just to return the age.

______________________________________________________________________

# The map() Function

`map()` applies a function to every item in an iterable.

General syntax:

```python
map(function, iterable)
```

______________________________________________________________________

# Example 2

```python
numbers = [1, 2, 3, 4]

def square(number):
    return number * number

result = map(square, numbers)

print(list(result))
```

Output

```
[1, 4, 9, 16]
```

Visualization

```
1 ─┐
2 ─┼──► square() ─► 1
3 ─┤              4
4 ─┘              9
                  16
```

______________________________________________________________________

# Using Lambda with map()

```python
numbers = [1, 2, 3, 4]

result = map(lambda number: number * number, numbers)

print(list(result))
```

Output

```
[1, 4, 9, 16]
```

______________________________________________________________________

# The filter() Function

`filter()` keeps only the items that satisfy a condition.

General syntax

```python
filter(function, iterable)
```

The function must return:

- `True` → Keep the item
- `False` → Remove the item

______________________________________________________________________

# Example 3

```python
numbers = [1, 2, 3, 4, 5, 6]

def is_even(number):
    return number % 2 == 0

result = filter(is_even, numbers)

print(list(result))
```

Output

```
[2, 4, 6]
```

Visualization

```
1 → False ❌

2 → True ✅

3 → False ❌

4 → True ✅

5 → False ❌

6 → True ✅
```

______________________________________________________________________

# Using Lambda with filter()

```python
numbers = [1, 2, 3, 4, 5, 6]

result = filter(

    lambda number: number % 2 == 0,

    numbers
)

print(list(result))
```

Output

```
[2, 4, 6]
```

______________________________________________________________________

# The sorted() Function

The `sorted()` function returns a new sorted list.

Example

```python
numbers = [7, 2, 10, 1]

result = sorted(numbers)

print(result)
```

Output

```
[1, 2, 7, 10]
```

The original list remains unchanged.

______________________________________________________________________

# Example 4 - Sorting by Name Length

```python
names = [

    "John",

    "Christopher",

    "Amy"
]

result = sorted(

    names,

    key=lambda name: len(name)
)

print(result)
```

Output

```
['Amy', 'John', 'Christopher']
```

The `key` function tells Python **how** to compare items.

______________________________________________________________________

# Callbacks

A callback is simply a function that is passed to another function and executed later.

Example

```python
def notify():
    print("Task Completed")


def perform_task(callback):

    print("Working...")

    callback()


perform_task(notify)
```

Output

```
Working...

Task Completed
```

Here,

`notify` is the callback.

______________________________________________________________________

# Example 5 - Payment Processing

```python
def payment_success():
    print("Email sent to customer.")


def process_payment(callback):

    print("Processing payment...")

    print("Payment Successful.")

    callback()


process_payment(payment_success)
```

Output

```
Processing payment...

Payment Successful.

Email sent to customer.
```

Callbacks are everywhere in backend systems.

______________________________________________________________________

# Why Not Just Use a Normal Function?

Suppose you write:

```python
def process_payment():

    print("Processing...")

    print("Send Email")

    print("Update Inventory")

    print("Generate Invoice")
```

Now every payment always performs the same actions.

Instead,

callbacks allow different behaviour.

```python
process_payment(send_email)

process_payment(update_inventory)

process_payment(generate_invoice)
```

The payment logic stays the same.

Only the callback changes.

This makes code reusable and flexible.

______________________________________________________________________

# Production Insight

Imagine you're writing a logging utility.

```python
def execute(task):

    print("Starting Task")

    result = task()

    print("Task Finished")

    return result
```

Now any business logic can be passed in.

```python
def create_user():

    print("Creating User...")

execute(create_user)
```

Output

```
Starting Task

Creating User...

Task Finished
```

This pattern is extremely common in:

- FastAPI middleware
- Database transactions
- Retry mechanisms
- Authentication wrappers
- Event-driven systems
- Background task execution

Decorators use exactly the same idea.

______________________________________________________________________

# Questions

### Question

> What is a lambda function?

### Answer

> A lambda function is an anonymous function defined using the `lambda` keyword. It consists of a single expression and is commonly used for short-lived operations such as sorting, mapping and filtering. For complex logic, a normal function defined with `def` is preferred.

______________________________________________________________________

### Question

> What is the difference between `map()` and `filter()`?

### Answer

> `map()` transforms every element in an iterable by applying a function to each item. `filter()` removes elements that do not satisfy a condition. Both return iterator objects in Python 3.

______________________________________________________________________

### Question

> What is a callback?

### Answer

> A callback is a function passed as an argument to another function so that it can be executed later. Callbacks allow behaviour to be customised without modifying the calling function.

______________________________________________________________________

# Practical Lesson

Create a file:

```
callback_demo.py
```

Write the following program.

```python
def send_sms():
    print("SMS Sent")


def send_email():
    print("Email Sent")


def notify(callback):
    """
    Execute any notification method.
    """
    print("Starting Notification")

    callback()

    print("Notification Finished")


notify(send_sms)

notify(send_email)
```

Expected Output

```
Starting Notification

SMS Sent

Notification Finished

Starting Notification

Email Sent

Notification Finished
```

Now create another callback:

```python
def send_push_notification():
    print("Push Notification Sent")
```

Use it with `notify()` without modifying the `notify()` function.

______________________________________________________________________

# Questions

## Question 1

What is a lambda function?

### Answer

A lambda function is an anonymous function that contains a single expression. It is commonly used for short, simple
operations.

______________________________________________________________________

## Question 2

When should you use a normal function instead of a lambda?

### Answer

Use a normal function when the logic is complex, spans multiple statements, or requires documentation and better
readability.

______________________________________________________________________

## Question 3

What does `map()` return in Python 3?

### Answer

It returns a **map object**, which is an iterator. To view the values, convert it to a list or iterate over it.

Example:

```python
result = map(str, [1, 2, 3])

print(list(result))
```

______________________________________________________________________

## Question 4

What is the purpose of `filter()`?

### Answer

`filter()` removes elements that do not satisfy a condition. The filtering function must return `True` or `False`.

______________________________________________________________________

## Question 5

What is a callback?

### Answer

A callback is a function passed to another function so it can be executed later, allowing the caller to customise
behaviour without changing the implementation.

______________________________________________________________________

# Assignment

## Exercise 1

Create a list of dictionaries representing employees.

Sort them by salary using `sorted()` and a lambda function.

______________________________________________________________________

## Exercise 2

Use `map()` to convert a list of temperatures from Celsius to Fahrenheit.

______________________________________________________________________

## Exercise 3

Use `filter()` to extract only users whose age is greater than 18.

______________________________________________________________________

## Exercise 4

Create a generic `process_order(callback)` function.

Write three callbacks:

- Send Email
- Generate Invoice
- Update Inventory

Pass each callback to `process_order()`.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What lambda functions are.
- ✅ When to use lambda functions.
- ✅ How `map()` transforms data.
- ✅ How `filter()` removes unwanted data.
- ✅ How `sorted()` uses a key function.
- ✅ What callbacks are.
- ✅ Why callbacks and higher-order functions are widely used in backend development.

______________________________________________________________________

# What's Next

**File:** [05-Decorators-part-1](05-decorators-part-1.md)

Topics:

- Why Decorators Exist
- Function Wrapping
- Writing Your First Decorator
- `*args` and `**kwargs`
- Preserving Return Values
- Real-world Examples

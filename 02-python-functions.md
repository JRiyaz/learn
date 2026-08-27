# 2. Functions & Functional Programming

**Previous:** [1. Python Runtime, Objects, Memory & Scope](./01-python-core.md)

**Next:** [3. Decorators & Context Managers](./03-python-decorators-context-managers.md)

______________________________________________________________________

## Objectives

By the end of this chapter, you should be able to:

- Explain why functions are first-class objects in Python.
- Understand positional, keyword, default, positional-only, and keyword-only arguments.
- Explain `*args`, `**kwargs`, and argument unpacking.
- Understand Python's argument-binding rules.
- Explain the mutable-default-argument trap.
- Understand return values and function contracts.
- Use lambda functions appropriately.
- Explain higher-order functions.
- Understand `map`, `filter`, `reduce`, `zip`, `enumerate`, `any`, and `all`.
- Use comprehensions and generator expressions effectively.
- Understand useful `functools` and `itertools` utilities.
- Design clear function APIs suitable for backend code.
- Explain the trade-offs of functional-style programming in Python.

______________________________________________________________________

# 1. Functions Are First-Class Objects

Python functions are objects.

A function can be:

- Assigned to a variable
- Passed to another function
- Returned from another function
- Stored in a list or dictionary
- Used as a callback

Example:

```python
def greet(name):
    return f"Hello, {name}"


say_hello = greet

print(say_hello("Riyaz"))
```

Both names refer to the same function object.

This property is fundamental to:

- Decorators
- Callbacks
- Higher-order functions
- Dependency injection
- Framework APIs

______________________________________________________________________

# 2. Function Objects

Functions have attributes and metadata.

```python
def greet():
    pass

print(greet.__name__)
```

Output:

```text
greet
```

You can inspect a function with:

```python
dir(greet)
```

You do not need to memorize every function attribute. The important concept is that a function is a normal Python object
with behavior and metadata.

______________________________________________________________________

# 3. Positional Arguments

Consider:

```python
def create_user(name, age):
    return {
        "name": name,
        "age": age,
    }
```

You can pass arguments by position:

```python
create_user("Riyaz", 30)
```

The first argument binds to `name` and the second to `age`.

Positional arguments are concise, but too many positional parameters can make APIs difficult to understand.

______________________________________________________________________

# 4. Keyword Arguments

Arguments can also be passed by parameter name:

```python
create_user(
    name="Riyaz",
    age=30,
)
```

Keyword arguments improve readability and allow the caller to change the order:

```python
create_user(
    age=30,
    name="Riyaz",
)
```

They are particularly useful when several parameters have similar types.

______________________________________________________________________

# 5. Mixing Positional and Keyword Arguments

This is valid:

```python
create_user("Riyaz", age=30)
```

But positional arguments must appear before keyword arguments.

This is invalid:

```python
create_user(name="Riyaz", 30)
```

because a positional argument cannot follow a keyword argument.

______________________________________________________________________

# 6. Default Arguments

Python allows default values:

```python
def connect(host, port=5432):
    ...
```

Now:

```python
connect("localhost")
```

uses:

```text
port = 5432
```

while:

```python
connect("localhost", 3306)
```

overrides the default.

Default values are part of the function's API contract.

______________________________________________________________________

# 7. Mutable Default Argument Trap

One of the most important Python interview questions is:

```python
def add_item(item, items=[]):
    items.append(item)
    return items
```

Consider:

```python
print(add_item("a"))
print(add_item("b"))
```

The result is effectively:

```text
['a']
['a', 'b']
```

The list is created when the function definition is evaluated and reused when the argument is omitted.

______________________________________________________________________

# 8. Correct Pattern for Mutable Defaults

Use `None` as a sentinel:

```python
def add_item(item, items=None):
    if items is None:
        items = []

    items.append(item)
    return items
```

Now each call without an explicit `items` gets a new list.

This pattern is especially important in reusable backend utilities.

______________________________________________________________________

# 9. `*args`

`*args` collects additional positional arguments into a tuple.

```python
def add_all(*args):
    return sum(args)
```

Usage:

```python
add_all(1, 2, 3)
```

Inside the function:

```python
args
```

is a tuple.

```python
def show(*args):
    print(type(args))
```

Output:

```text
<class 'tuple'>
```

The name `args` is conventional; `*` is what performs the collection.

______________________________________________________________________

# 10. `**kwargs`

`**kwargs` collects additional keyword arguments into a dictionary.

```python
def create_user(**kwargs):
    print(kwargs)
```

Usage:

```python
create_user(
    name="Riyaz",
    age=30,
)
```

Inside the function:

```python
{
    "name": "Riyaz",
    "age": 30,
}
```

Again, `kwargs` is conventional; `**` is what performs the collection.

______________________________________________________________________

# 11. `*args` and `**kwargs` Together

You can combine them:

```python
def log_call(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)
```

Usage:

```python
log_call(10, 20, name="Riyaz")
```

This pattern is common in:

- Decorators
- Wrappers
- Generic adapters
- Framework internals

______________________________________________________________________

# 12. Positional Argument Unpacking

The `*` operator can also unpack an iterable during a function call.

```python
def add(a, b, c):
    return a + b + c


values = [10, 20, 30]

print(add(*values))
```

The list is unpacked into:

```python
add(10, 20, 30)
```

______________________________________________________________________

# 13. Keyword Argument Unpacking

A mapping can be unpacked with `**`:

```python
def create_user(name, age):
    return {
        "name": name,
        "age": age,
    }


data = {
    "name": "Riyaz",
    "age": 30,
}

create_user(**data)
```

The dictionary keys must correspond to accepted keyword parameters.

This pattern is common when passing validated data between backend layers.

______________________________________________________________________

# 14. Positional-Only Parameters

Python supports positional-only parameters using `/`.

```python
def calculate(a, b, /):
    return a + b
```

This is valid:

```python
calculate(10, 20)
```

This is invalid:

```python
calculate(a=10, b=20)
```

Parameters before `/` are positional-only.

______________________________________________________________________

# 15. Keyword-Only Parameters

A `*` can force following parameters to be keyword-only.

```python
def create_user(name, *, active=True):
    ...
```

This is valid:

```python
create_user("Riyaz", active=False)
```

This is invalid:

```python
create_user("Riyaz", False)
```

Keyword-only parameters are useful for optional configuration because they make calls self-documenting.

______________________________________________________________________

# 16. Complete Function Signature

Python can combine all these forms:

```python
def example(
    positional,
    /,
    normal,
    *args,
    keyword_only,
    **kwargs,
):
    ...
```

The rules are:

- Before `/`: positional-only
- Between `/` and `*`: positional-or-keyword
- `*args`: additional positional arguments
- After `*args`: keyword-only parameters
- `**kwargs`: additional keyword arguments

Do not make signatures complex without a reason.

______________________________________________________________________

# 17. Argument Binding

Python binds arguments to parameters according to the function signature.

Consider:

```python
def greet(name, age):
    ...
```

These are valid:

```python
greet("Riyaz", 30)

greet(name="Riyaz", age=30)

greet("Riyaz", age=30)
```

This is invalid:

```python
greet("Riyaz", name="Another")
```

because `name` receives two values.

Understanding binding helps diagnose Python `TypeError` messages quickly.

______________________________________________________________________

# 18. Return Values

Functions can return any Python object.

```python
def get_user():
    return {
        "id": 1,
        "name": "Riyaz",
    }
```

A function can return multiple values:

```python
def get_coordinates():
    return 10, 20
```

This returns a tuple:

```python
(10, 20)
```

Therefore:

```python
x, y = get_coordinates()
```

uses tuple unpacking.

______________________________________________________________________

# 19. `return` vs `print`

These are different operations.

```python
def add(a, b):
    print(a + b)
```

This prints the result but returns `None`.

Prefer:

```python
def add(a, b):
    return a + b
```

when the caller needs to use the result.

Backend business logic should generally return values rather than print them.

______________________________________________________________________

# 20. Functions Without `return`

If execution reaches the end of a function without returning a value:

```python
def do_something():
    pass
```

the function returns:

```python
None
```

______________________________________________________________________

# 21. Lambda Functions

A lambda is an anonymous function expression.

```python
square = lambda x: x * x
```

For simple expressions, this can be useful as a callback:

```python
users.sort(key=lambda user: user["age"])
```

Avoid complex lambdas. If the logic needs explanation, use a named function.

______________________________________________________________________

# 22. Higher-Order Functions

A higher-order function accepts another function as an argument, returns a function, or both.

Example:

```python
def apply_operation(value, operation):
    return operation(value)


def double(value):
    return value * 2


print(apply_operation(10, double))
```

Functions such as:

```python
sorted()
map()
filter()
```

work with callable objects.

______________________________________________________________________

# 23. `map`

`map()` applies a function to every item.

```python
numbers = [1, 2, 3]

result = map(lambda x: x * 2, numbers)
```

In Python 3, `map()` returns an iterator.

Convert it to a list if required:

```python
list(result)
```

For simple transformations, a comprehension is often clearer:

```python
[x * 2 for x in numbers]
```

______________________________________________________________________

# 24. `filter`

`filter()` keeps items for which a predicate is true.

```python
numbers = [1, 2, 3, 4, 5]

result = filter(lambda x: x % 2 == 0, numbers)

print(list(result))
```

Output:

```text
[2, 4]
```

A comprehension is often more readable:

```python
[x for x in numbers if x % 2 == 0]
```

______________________________________________________________________

# 25. `reduce`

`reduce()` repeatedly combines values into one result.

```python
from functools import reduce

numbers = [1, 2, 3, 4]

result = reduce(lambda a, b: a + b, numbers)

print(result)
```

Result:

```text
10
```

For common aggregation, prefer readable built-ins:

```python
sum(numbers)
```

Use `reduce()` when repeated pairwise reduction is genuinely the clearest expression.

______________________________________________________________________

# 26. `zip`

`zip()` combines corresponding elements.

```python
names = ["Alice", "Bob", "Carol"]
scores = [90, 80, 95]

result = zip(names, scores)

print(list(result))
```

Conceptually:

```text
Alice → 90
Bob   → 80
Carol → 95
```

It is useful for:

- Combining related sequences
- Iterating over multiple collections
- Building dictionaries

Example:

```python
dict(zip(names, scores))
```

By default, `zip()` stops when the shortest input is exhausted.

______________________________________________________________________

# 27. `enumerate`

Instead of manually maintaining an index:

```python
index = 0

for user in users:
    print(index, user)
    index += 1
```

use:

```python
for index, user in enumerate(users):
    print(index, user)
```

You can choose a starting index:

```python
enumerate(users, start=1)
```

This is idiomatic and less error-prone.

______________________________________________________________________

# 28. `any` and `all`

`any()` returns `True` if at least one item is truthy.

```python
values = [False, False, True]

any(values)  # True
```

`all()` returns `True` if every item is truthy.

```python
values = [True, True, True]

all(values)  # True
```

Both can short-circuit.

For example:

```python
any(check(user) for user in users)
```

can stop as soon as a truthy result is found.

______________________________________________________________________

# 29. Comprehensions

Python supports:

- List comprehensions
- Set comprehensions
- Dictionary comprehensions
- Generator expressions

List:

```python
squares = [x * x for x in range(5)]
```

Set:

```python
unique = {x.lower() for x in names}
```

Dictionary:

```python
mapping = {x: x * x for x in range(5)}
```

Generator expression:

```python
squares = (x * x for x in range(5))
```

______________________________________________________________________

# 30. Comprehensions vs Loops

Comprehensions are excellent for simple transformations and filtering.

Good:

```python
active_ids = [
    user["id"]
    for user in users
    if user["active"]
]
```

Avoid extremely complex comprehensions.

Readable code is more important than reducing line count.

______________________________________________________________________

# 31. Generator Expressions

A generator expression is lazy:

```python
values = (x * x for x in range(1_000_000))
```

Unlike:

```python
values = [x * x for x in range(1_000_000)]
```

the generator does not construct all results immediately.

This can reduce memory usage.

Example:

```python
total = sum(x * x for x in range(1_000_000))
```

The intermediate values can be produced lazily.

Generators are covered in more depth in File 4.

______________________________________________________________________

# 32. `functools`

The `functools` module provides utilities for working with functions.

Interview-relevant tools include:

- `wraps`
- `partial`
- `lru_cache`
- `cache`
- `reduce`
- `singledispatch` overview

`wraps` and decorators are covered more deeply in File 3.

______________________________________________________________________

# 33. `functools.partial`

`partial()` creates a new callable with some arguments pre-filled.

```python
from functools import partial


def multiply(a, b):
    return a * b


double = partial(multiply, 2)

print(double(10))
```

Conceptually:

```python
double(10)
```

behaves like:

```python
multiply(2, 10)
```

______________________________________________________________________

# 34. `functools.lru_cache`

`lru_cache` caches function results.

```python
from functools import lru_cache


@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)
```

Caching can dramatically improve repeated deterministic computations.

Trade-offs include:

- Memory usage
- Cache invalidation
- Stale values
- Argument requirements
- Process-local scope

Do not treat `lru_cache` as a replacement for Redis or another distributed cache.

______________________________________________________________________

# 35. `itertools`

`itertools` provides efficient iterator-building utilities.

Important tools include:

- `chain`
- `islice`
- `product`
- `permutations`
- `combinations`
- `groupby`
- `count`
- `cycle`
- `repeat`

Example:

```python
from itertools import chain

first = [1, 2]
second = [3, 4]

for value in chain(first, second):
    print(value)
```

These utilities are particularly useful for lazy data processing.

______________________________________________________________________

# 36. Functional Programming in Backend Code

Functional techniques can make backend code easier to compose.

### Transforming data

```python
user_ids = [user["id"] for user in users]
```

### Filtering data

```python
active_users = [
    user
    for user in users
    if user["active"]
]
```

### Passing behavior

```python
sorted(users, key=lambda user: user["created_at"])
```

### Reusable operation

```python
def transform_users(users, transform):
    return [transform(user) for user in users]
```

However, do not force functional constructs where a normal loop is clearer.

______________________________________________________________________

# 37. Function API Design

Function signatures are part of API design.

Compare:

```python
def create_user(name, age, active, role):
    ...
```

with:

```python
def create_user(
    name,
    *,
    age,
    active=True,
    role="user",
):
    ...
```

The second makes optional/configuration parameters explicit.

This is useful in:

- Service-layer functions
- Repository functions
- Utility functions
- Internal libraries
- Framework integrations

______________________________________________________________________

# 38. Common Function Design Mistakes

## Too many parameters

A function with many unrelated parameters may indicate mixed responsibilities.

Consider:

- A dataclass
- A request/domain object
- Splitting responsibilities
- Explicit keyword-only parameters

Do not blindly replace every parameter list with a dictionary. Structured types preserve clarity and validation.

______________________________________________________________________

## Hidden side effects

A function called:

```python
calculate_total()
```

should not unexpectedly modify global state or perform network operations.

Make side effects explicit where possible.

______________________________________________________________________

## Overusing `*args` and `**kwargs`

They provide flexibility but can reduce:

- Readability
- Type safety
- IDE assistance
- Validation
- API clarity

Use them when generic behavior is genuinely required.

______________________________________________________________________

# 39. Backend Relevance

These concepts are directly useful in backend engineering.

### Function signatures

Used to design:

- Service APIs
- Repository methods
- Utility functions
- Dependency-injection functions

### Higher-order functions

Useful for:

- Decorators
- Callbacks
- Sorting
- Validation pipelines

### Lazy evaluation

Useful for:

- Streaming
- Large datasets
- File processing
- Memory-efficient pipelines

### Function caching

Useful for:

- Expensive deterministic computations
- Repeated configuration lookups
- Process-local memoization

### Functional transformations

Useful for:

- Request/response transformations
- Data normalization
- Filtering
- Serialization preparation

______________________________________________________________________

# 40. Interview Questions & Answers

## Q1. Are functions objects in Python?

**Answer:**

Yes. Functions are first-class objects.

They can be assigned to variables, passed as arguments, returned from functions, and stored in collections.

This enables decorators, callbacks and higher-order functions.

______________________________________________________________________

## Q2. What does "first-class function" mean?

**Answer:**

It means functions can be treated like other values.

They can be:

- Assigned to variables
- Passed as arguments
- Returned from functions
- Stored in data structures

______________________________________________________________________

## Q3. Explain positional and keyword arguments.

**Answer:**

Positional arguments are matched by position:

```python
create_user("Riyaz", 30)
```

Keyword arguments are matched by parameter name:

```python
create_user(name="Riyaz", age=30)
```

Keyword arguments improve readability and can make calls less error-prone.

______________________________________________________________________

## Q4. What are `*args` and `**kwargs`?

**Answer:**

`*args` collects additional positional arguments into a tuple.

`**kwargs` collects additional keyword arguments into a dictionary.

They are especially useful in decorators, wrappers, adapters and generic APIs.

______________________________________________________________________

## Q5. What is the mutable default argument problem?

**Answer:**

Default parameter values are evaluated when the function is defined, not on every call.

Therefore:

```python
def add(item, items=[]):
    items.append(item)
    return items
```

reuses the same list when `items` is omitted.

Use `None` and create the list inside the function.

______________________________________________________________________

## Q6. What is the difference between `*args` and `*values`?

**Answer:**

In a function definition:

```python
def f(*args):
    ...
```

`*args` collects positional arguments.

In a function call:

```python
f(*values)
```

`*` unpacks an iterable into positional arguments.

The same syntax has different roles depending on context.

______________________________________________________________________

## Q7. What are positional-only parameters?

**Answer:**

Parameters before `/` are positional-only:

```python
def add(a, b, /):
    return a + b
```

They cannot be supplied by keyword.

______________________________________________________________________

## Q8. What are keyword-only parameters?

**Answer:**

Parameters after `*` must be supplied by keyword:

```python
def create_user(name, *, active=True):
    ...
```

This improves readability for optional configuration.

______________________________________________________________________

## Q9. What is a higher-order function?

**Answer:**

A higher-order function accepts a function as an argument, returns a function, or both.

This is common in decorators, callbacks, sorting and transformation pipelines.

______________________________________________________________________

## Q10. What is a lambda?

**Answer:**

A lambda is an anonymous function expression.

```python
lambda x: x * 2
```

It is useful for short callbacks. Complex logic should normally use a named function.

______________________________________________________________________

## Q11. What does `map()` return in Python 3?

**Answer:**

It returns an iterator that lazily applies a function to each item.

It does not immediately create a list.

______________________________________________________________________

## Q12. What does `filter()` return?

**Answer:**

It returns an iterator containing values for which the predicate evaluates as true.

______________________________________________________________________

## Q13. When would you use `reduce()`?

**Answer:**

Use it when repeatedly combining a sequence into a single result is the clearest solution.

For common operations, built-ins such as `sum`, `min`, and `max` are generally clearer.

______________________________________________________________________

## Q14. What happens when `zip()` receives iterables of different lengths?

**Answer:**

Normal `zip()` stops when the shortest iterable is exhausted.

If you need to continue to the longest iterable, use `itertools.zip_longest()`.

______________________________________________________________________

## Q15. Why use `enumerate()`?

**Answer:**

It provides the index and value together:

```python
for index, value in enumerate(values):
    ...
```

It avoids manually maintaining a counter.

______________________________________________________________________

## Q16. What is the difference between `any()` and `all()`?

**Answer:**

`any()` returns true if at least one item is truthy.

`all()` returns true if every item is truthy.

Both can short-circuit.

______________________________________________________________________

## Q17. What is a generator expression?

**Answer:**

It creates values lazily:

```python
(x * x for x in values)
```

This can reduce memory usage because values do not need to be materialized all at once.

______________________________________________________________________

## Q18. When would you prefer a comprehension over `map()`?

**Answer:**

For straightforward transformations, comprehensions are often easier to read:

```python
[x * 2 for x in values]
```

The important consideration is readability and intent.

______________________________________________________________________

## Q19. What is `functools.partial()`?

**Answer:**

It creates a new callable with some arguments pre-filled.

```python
double = partial(multiply, 2)
```

Then:

```python
double(5)
```

behaves like:

```python
multiply(2, 5)
```

______________________________________________________________________

## Q20. What is `lru_cache`?

**Answer:**

It caches function results based on arguments.

It is useful for expensive deterministic computations that are repeatedly called.

It is process-local and therefore is not a replacement for a shared distributed cache.

______________________________________________________________________

## Q21. Why can hidden side effects make functions difficult to maintain?

**Answer:**

A function becomes harder to reason about if its name suggests a calculation but it also modifies global state, writes
to a database, or makes network calls.

Separating pure computation from side effects improves testing and predictability.

______________________________________________________________________

## Q22. Why should you avoid excessive `*args` and `**kwargs`?

**Answer:**

They can hide the function's contract and reduce readability, type checking, IDE assistance and validation.

Use them where generic behavior is actually required.

______________________________________________________________________

## Q23. What is the difference between `return` and `print`?

**Answer:**

`return` gives a value to the caller and exits the function.

`print` writes to stdout and normally returns `None`.

Backend logic should generally return values rather than print them.

______________________________________________________________________

## Q24. How would you design a function with many optional parameters?

**Answer:**

First identify whether the parameters represent distinct responsibilities.

Potential solutions include:

- Keyword-only parameters
- A dataclass
- A validated request/domain object
- Splitting responsibilities

Avoid hiding everything inside an untyped dictionary just to reduce the parameter count.

______________________________________________________________________

# 41. Scenario-Based Questions

## Scenario 1 — Function State Leaks Between Requests

A backend helper contains:

```python
def collect_event(event, events=[]):
    events.append(event)
    return events
```

Different requests unexpectedly see previous request data.

**Answer:**

The default list is shared across calls where `events` is omitted.

Use:

```python
def collect_event(event, events=None):
    if events is None:
        events = []

    events.append(event)
    return events
```

For request-scoped state, make ownership explicit.

______________________________________________________________________

## Scenario 2 — API Function Has Too Many Parameters

You find:

```python
create_order(
    user_id,
    product_id,
    quantity,
    address,
    city,
    state,
    country,
    coupon,
    currency,
)
```

**Question:** What would you consider?

**Answer:**

Determine whether the parameters represent distinct responsibilities.

Potential improvements:

- A validated request/domain object
- A dataclass
- Smaller functions
- Keyword-only parameters
- Separating order creation from unrelated concerns

Do not blindly replace the parameters with a dictionary.

______________________________________________________________________

## Scenario 3 — `map()` Makes Code Hard to Read

You see:

```python
result = list(
    map(
        lambda user: normalize(
            enrich(
                validate(user)
            )
        ),
        users,
    )
)
```

**Question:** Would you keep it?

**Answer:**

Probably not.

A loop or named helper functions may make the processing pipeline easier to understand and debug.

Functional programming is a tool, not a requirement.

______________________________________________________________________

## Scenario 4 — Cached Function Returns Stale Data

A function uses:

```python
@lru_cache(maxsize=128)
def get_user(user_id):
    return load_user_from_database(user_id)
```

The database changes but the application keeps returning old values.

**Answer:**

`lru_cache` is returning the previously cached result.

This illustrates the need for an explicit invalidation strategy.

For multi-process or multi-instance services, `lru_cache` also does not provide shared cache state.

______________________________________________________________________

# 42. Practice Exercises

## Exercise 1 — Argument Binding

Write:

```python
def create_user(...):
    ...
```

Requirements:

- `name` should be positional.
- `age` should be keyword-only.
- `active=True` by default.

Demonstrate valid and invalid calls.

______________________________________________________________________

## Exercise 2 — `*args`

Implement:

```python
def average(*numbers):
    ...
```

Requirements:

- Accept any number of numeric arguments.
- Return the average.
- Handle empty input explicitly.

______________________________________________________________________

## Exercise 3 — `**kwargs`

Implement:

```python
def build_query(**filters):
    ...
```

Convert:

```python
build_query(status="active", role="admin")
```

into a readable SQL-like filter representation.

Do not construct executable SQL.

______________________________________________________________________

## Exercise 4 — Comprehensions

Given:

```python
users = [
    {"id": 1, "active": True},
    {"id": 2, "active": False},
    {"id": 3, "active": True},
]
```

Produce:

1. IDs of active users.
1. A set of active IDs.
1. A dictionary mapping ID to active status.

______________________________________________________________________

## Exercise 5 — `zip`

Given:

```python
names = ["Alice", "Bob", "Carol"]
scores = [90, 80, 95]
```

Create:

```python
{
    "Alice": 90,
    "Bob": 80,
    "Carol": 95,
}
```

without manually indexing the lists.

______________________________________________________________________

## Exercise 6 — Closure Preview

Implement:

```python
make_multiplier(3)
```

so that:

```python
triple = make_multiplier(3)

triple(10)  # 30
```

The deeper closure/decorator discussion continues in the next chapter.

______________________________________________________________________

# 43. Quick Revision

| Concept | Key Point |
|---|---|
| First-class function | Functions are objects |
| Positional argument | Matched by position |
| Keyword argument | Matched by parameter name |
| Default argument | Created/evaluated at function definition |
| `*args` | Collects positional arguments into a tuple |
| `**kwargs` | Collects keyword arguments into a dictionary |
| `*values` | Unpacks positional arguments |
| `**data` | Unpacks keyword arguments |
| `/` | Marks positional-only parameters |
| `*` in signature | Marks following parameters keyword-only |
| Lambda | Anonymous function expression |
| Higher-order function | Accepts/returns functions |
| `map` | Lazy transformation |
| `filter` | Lazy filtering |
| `reduce` | Repeated reduction |
| `zip` | Combines corresponding elements |
| `enumerate` | Index + value |
| `any` | At least one truthy |
| `all` | Every item truthy |
| Comprehension | Concise collection construction |
| Generator expression | Lazy computation |
| `partial` | Pre-fills function arguments |
| `lru_cache` | Process-local function-result cache |
| `itertools` | Iterator-building utilities |

______________________________________________________________________

# 44. Completion Checklist

Before moving to File 3, make sure you can explain:

- [ ] Functions as first-class objects
- [ ] Positional arguments
- [ ] Keyword arguments
- [ ] Default arguments
- [ ] Mutable default argument trap
- [ ] `*args`
- [ ] `**kwargs`
- [ ] Argument unpacking
- [ ] Positional-only parameters
- [ ] Keyword-only parameters
- [ ] Argument binding
- [ ] Return values
- [ ] `return` vs `print`
- [ ] Lambda
- [ ] Higher-order functions
- [ ] `map`
- [ ] `filter`
- [ ] `reduce`
- [ ] `zip`
- [ ] `enumerate`
- [ ] `any`
- [ ] `all`
- [ ] List/set/dict comprehensions
- [ ] Generator expressions
- [ ] `functools.partial`
- [ ] `functools.lru_cache`
- [ ] Purpose of `itertools`
- [ ] Function API design
- [ ] Side effects
- [ ] When functional style improves readability
- [ ] When functional style hurts readability

______________________________________________________________________

# 45. Interview Readiness Test

Without looking at the notes, answer these aloud:

1. What does it mean that functions are first-class objects?
1. Explain positional vs keyword arguments.
1. What is the mutable default argument problem?
1. Explain `*args` and `**kwargs`.
1. What is the difference between `*values` and `*args`?
1. What are positional-only and keyword-only parameters?
1. What is a higher-order function?
1. When would you use a lambda?
1. What does `map()` return in Python 3?
1. What does `filter()` return?
1. What happens when `zip()` receives differently sized iterables?
1. Why is `enumerate()` preferable to manually maintaining an index?
1. When would you prefer a comprehension over `map()`?
1. What is a generator expression and why is it useful?
1. What does `lru_cache` do?
1. Why should you be careful using process-local caches in backend applications?
1. Why can too much `*args`/`**kwargs` hurt API clarity?
1. How would you design a function with many optional parameters?

If you can answer these clearly and implement the exercises without relying heavily on notes, this chapter is complete.

______________________________________________________________________

**Previous:** [00. Course Index](./00-index.md)

**Next:** [3. Decorators & Context Managers](./03-python-decorators-context-managers.md)

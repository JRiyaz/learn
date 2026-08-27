# 4. Iterators, Generators & Lazy Evaluation

**Previous:** [3. Decorators & Context Managers](./03-python-decorators-context-managers.md)

**Next:** [5. Python Collections & Data Structures](./05-python-collections.md)

______________________________________________________________________

## Objectives

By the end of this chapter, you should be able to:

- Explain the difference between an iterable and an iterator.
- Understand the iterator protocol.
- Explain `iter()` and `next()`.
- Understand `StopIteration`.
- Write custom iterators.
- Explain generators and `yield`.
- Understand generator execution and suspension.
- Use generator functions and generator expressions.
- Explain lazy evaluation and why it matters for backend systems.
- Understand `yield from`.
- Understand generator cleanup and `close()`.
- Explain generator exceptions at interview level.
- Choose between lists, iterators, and generators appropriately.
- Recognize common iterator/generator interview traps.

______________________________________________________________________

# 1. Iterable vs Iterator

These two terms are related but not identical.

### Iterable

An iterable is an object that can provide an iterator.

Examples:

```python
list
tuple
str
dict
set
range
```

You can generally call:

```python
iter(obj)
```

on an iterable.

### Iterator

An iterator is an object that produces values one at a time.

It implements the iterator protocol:

```python
__iter__()
__next__()
```

The most important distinction is:

> An iterable can produce an iterator; an iterator produces the next value.

______________________________________________________________________

# 2. Example: List vs List Iterator

A list is iterable:

```python
numbers = [1, 2, 3]

iterator = iter(numbers)
```

The iterator produces values:

```python
next(iterator)  # 1
next(iterator)  # 2
next(iterator)  # 3
```

After all values have been consumed:

```python
next(iterator)
```

raises:

```text
StopIteration
```

The list itself is not consumed by these operations.

The iterator maintains the current iteration position.

______________________________________________________________________

# 3. The Iterator Protocol

An iterator generally implements:

```python
__iter__()
__next__()
```

Example:

```python
class Counter:
    def __init__(self, limit):
        self.current = 0
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration

        value = self.current
        self.current += 1
        return value
```

Usage:

```python
counter = Counter(3)

for value in counter:
    print(value)
```

Output:

```text
0
1
2
```

______________________________________________________________________

# 4. Why Does an Iterator Return Itself From `__iter__`?

For an iterator:

```python
iterator.__iter__()
```

normally returns the iterator itself.

This allows:

```python
iter(iterator) is iterator
```

to be true.

This is an important iterator-protocol property.

An iterable that is not itself an iterator can instead return a new iterator.

______________________________________________________________________

# 5. `iter()` and `next()`

Python provides built-in functions:

```python
iter(obj)
```

and:

```python
next(iterator)
```

Conceptually:

```python
iter(obj)
```

calls the object's iteration protocol.

And:

```python
next(iterator)
```

requests the next value.

You normally use `for` loops instead of calling `next()` manually, but understanding these primitives is important for
interviews.

______________________________________________________________________

# 6. How a `for` Loop Works

Conceptually:

```python
for value in iterable:
    process(value)
```

is similar to:

```python
iterator = iter(iterable)

while True:
    try:
        value = next(iterator)
    except StopIteration:
        break

    process(value)
```

The actual implementation is optimized, but this mental model is excellent for understanding iteration.

______________________________________________________________________

# 7. `StopIteration`

`StopIteration` signals that an iterator has no more values.

Example:

```python
iterator = iter([1, 2])

print(next(iterator))
print(next(iterator))

next(iterator)
```

The third call raises `StopIteration`.

A `for` loop handles this automatically.

You normally should not write:

```python
for value in values:
    try:
        ...
    except StopIteration:
        ...
```

because the loop already handles normal iterator exhaustion.

______________________________________________________________________

# 8. Stateful Iterators

An iterator usually maintains iteration state.

Example:

```python
class Counter:
    def __init__(self, limit):
        self.current = 0
        self.limit = limit
```

Each call to:

```python
next(counter)
```

changes the iterator's state.

Therefore, iterators are generally single-pass objects.

______________________________________________________________________

# 9. Iterator Consumption

Consider:

```python
iterator = iter([1, 2, 3])

print(list(iterator))
print(list(iterator))
```

The first call consumes the iterator.

The second call produces:

```python
[]
```

This is an important difference from reusable collections such as lists.

A generator behaves similarly.

______________________________________________________________________

# 10. Iterable Can Produce Multiple Iterators

A list is reusable:

```python
numbers = [1, 2, 3]

first = iter(numbers)
second = iter(numbers)
```

These are separate iterators.

Therefore:

```python
next(first)
next(second)
```

can both produce:

```text
1
```

The list stores the data, while each iterator maintains its own traversal state.

______________________________________________________________________

# 11. What Is a Generator?

A generator is a convenient way to create an iterator.

Generators are commonly written using `yield`.

Example:

```python
def numbers():
    yield 1
    yield 2
    yield 3
```

Calling:

```python
result = numbers()
```

does not immediately execute the body.

It returns a generator object.

______________________________________________________________________

# 12. Generator Execution

Consider:

```python
def numbers():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")
```

When:

```python
generator = numbers()
```

is executed, the function body does not run normally.

When:

```python
next(generator)
```

is called, execution starts and pauses at the first `yield`.

The next `next()` resumes execution from where it stopped.

______________________________________________________________________

# 13. `yield` vs `return`

A `return` exits a function.

A `yield` pauses a generator and produces a value.

Example:

```python
def generate_numbers():
    yield 1
    yield 2
    yield 3
```

Each `yield` produces a value while preserving the generator's execution state.

A generator can eventually finish with:

```python
return
```

which results in `StopIteration`.

______________________________________________________________________

# 14. Generator State

A generator remembers:

- Local variables
- Current execution position
- Exception state
- Other execution context needed to resume

Example:

```python
def counter():
    value = 0

    while value < 3:
        yield value
        value += 1
```

The value of `value` is retained between calls to `next()`.

This is why generators are useful for incremental processing.

______________________________________________________________________

# 15. Generator vs List

Compare:

```python
def get_numbers():
    return [x for x in range(1_000_000)]
```

with:

```python
def generate_numbers():
    for x in range(1_000_000):
        yield x
```

The list version materializes all values.

The generator version produces values as requested.

This can significantly reduce memory usage when only one item or a small portion needs to be processed at a time.

______________________________________________________________________

# 16. Lazy Evaluation

Lazy evaluation means computation is deferred until the result is actually needed.

Example:

```python
numbers = (x * 2 for x in range(10))
```

The multiplication does not need to happen for all ten values immediately.

Values are produced as the generator is consumed.

This is especially useful for:

- Large datasets
- Streaming
- File processing
- ETL pipelines
- Log processing
- API pagination
- Database result processing

______________________________________________________________________

# 17. Generator Expressions

A generator expression resembles a list comprehension but uses parentheses:

```python
numbers = (x * 2 for x in range(10))
```

List comprehension:

```python
numbers = [x * 2 for x in range(10)]
```

The list creates the collection immediately.

The generator expression produces values lazily.

______________________________________________________________________

# 18. Generator Expressions With `sum`

A common pattern is:

```python
total = sum(
    x * x
    for x in range(1_000_000)
)
```

There is no need to create a million-element intermediate list.

This is both readable and memory-efficient.

______________________________________________________________________

# 19. Generator Functions

A function containing `yield` is a generator function.

Example:

```python
def read_lines(file):
    for line in file:
        yield line.strip()
```

The function returns a generator object when called.

It does not need to load the entire file into memory.

______________________________________________________________________

# 20. Streaming Large Files

Avoid:

```python
with open("large.log") as file:
    lines = file.readlines()

for line in lines:
    process(line)
```

when the file can be very large.

Prefer:

```python
with open("large.log") as file:
    for line in file:
        process(line)
```

or a generator-based transformation:

```python
def cleaned_lines(file):
    for line in file:
        yield line.strip()
```

This supports streaming-style processing.

______________________________________________________________________

# 21. Generator Pipelines

Generators can be chained:

```python
def read_users(source):
    for user in source:
        yield user


def active_users(users):
    for user in users:
        if user["active"]:
            yield user


def user_ids(users):
    for user in users:
        yield user["id"]
```

Then:

```python
ids = user_ids(
    active_users(
        read_users(source)
    )
)
```

Each stage can process one item at a time.

This avoids materializing every intermediate result.

______________________________________________________________________

# 22. Generator Pipelines and Memory

Suppose a source contains one million records.

A list pipeline may create:

```text
source list
    ↓
filtered list
    ↓
transformed list
```

which can consume significant memory.

A generator pipeline can process:

```text
one record
    ↓
filter
    ↓
transform
    ↓
output
```

without storing all intermediate values.

This is one of the most useful practical benefits of generators.

______________________________________________________________________

# 23. `yield from`

`yield from` delegates iteration to another iterable.

Example:

```python
def numbers():
    yield from [1, 2, 3]
```

This is roughly equivalent to:

```python
def numbers():
    for value in [1, 2, 3]:
        yield value
```

`yield from` is especially useful for composing generators.

______________________________________________________________________

# 24. Nested Generator Composition

Consider:

```python
def first():
    yield 1
    yield 2


def second():
    yield 3
    yield 4


def combined():
    yield from first()
    yield from second()
```

Usage:

```python
list(combined())
```

produces:

```python
[1, 2, 3, 4]
```

This keeps generator composition concise.

______________________________________________________________________

# 25. `yield from` and Return Values

A generator can return a value:

```python
def child():
    yield 1
    return "done"
```

When using:

```python
yield from child()
```

the delegated generator's return value can be captured internally.

This is an advanced generator detail. You should understand the concept for interviews, but you do not need to memorize
complicated generator-control patterns unless your role specifically requires them.

______________________________________________________________________

# 26. Generator `send()`

Generators can receive values using:

```python
generator.send(value)
```

Example:

```python
def receiver():
    value = yield
    print(value)
```

Usage:

```python
g = receiver()

next(g)
g.send("hello")
```

Output:

```text
hello
```

This is an advanced generator capability.

For typical Python backend interviews, understand that generators can communicate bidirectionally, but prioritize normal
`yield` usage.

______________________________________________________________________

# 27. Generator `throw()`

A generator can receive an exception through:

```python
generator.throw(...)
```

This allows external code to inject an exception at the generator's suspension point.

This is mainly useful for advanced coroutine-style patterns.

Modern async Python generally uses `async`/`await` rather than manually building coroutine systems with generator
methods.

______________________________________________________________________

# 28. Generator `close()`

A generator can be closed:

```python
generator.close()
```

This requests termination of the generator.

If the generator has a `finally` block, cleanup can occur there.

Example:

```python
def resource_generator():
    try:
        yield "resource"
    finally:
        print("cleanup")
```

The `finally` block is important for generator cleanup.

______________________________________________________________________

# 29. Generator Exceptions

Generators can contain normal exception handling:

```python
def process():
    try:
        yield "data"
    finally:
        cleanup()
```

When the generator is exhausted or closed, cleanup logic can run.

This makes generator design important when generators own resources.

However, resource ownership should generally be explicit and context managers are often a clearer abstraction for
lifecycle management.

______________________________________________________________________

# 30. Infinite Generators

Generators can represent unbounded sequences:

```python
def counter():
    value = 0

    while True:
        yield value
        value += 1
```

This does not create an infinite list.

It produces one value at a time.

You must consume it with a terminating condition.

For example:

```python
for value in counter():
    if value == 10:
        break
```

______________________________________________________________________

# 31. `itertools.count`

Python provides an equivalent utility:

```python
from itertools import count

for value in count():
    if value == 10:
        break
```

The `itertools` module provides many efficient iterator utilities.

______________________________________________________________________

# 32. `iter(callable, sentinel)`

`iter()` has a second form:

```python
iter(callable, sentinel)
```

It repeatedly calls the callable until the returned value equals the sentinel.

Example:

```python
from functools import partial

with open("data.txt", "rb") as file:
    for chunk in iter(partial(file.read, 4096), b""):
        process(chunk)
```

This is a useful pattern for reading data in chunks without loading the entire resource.

______________________________________________________________________

# 33. Lazy Iteration in Backend Systems

Generators are especially useful for:

### Large query results

Process records incrementally.

### File uploads/downloads

Stream chunks instead of materializing the entire payload.

### Log processing

Process lines one at a time.

### ETL

Build transformations as lazy stages.

### Pagination

Generate pages/items progressively.

### Data pipelines

Connect producers and consumers without large intermediate lists.

______________________________________________________________________

# 34. Generator vs Async Generator

A normal generator uses:

```python
yield
```

An async generator uses:

```python
async def
```

with:

```python
yield
```

Example:

```python
async def stream_items():
    for item in items:
        yield item
```

Async generators are consumed using:

```python
async for item in stream_items():
    ...
```

They are useful when producing values involves asynchronous operations.

______________________________________________________________________

# 35. Generator vs Coroutine

Do not treat these as identical.

A generator primarily provides iteration and can suspend at `yield`.

A coroutine represents asynchronous computation and is normally written using:

```python
async def
```

and:

```python
await
```

Modern Python backend applications generally use native coroutines for asynchronous I/O.

Generators remain extremely useful for synchronous lazy iteration.

______________________________________________________________________

# 36. Common Iterator and Generator Mistakes

## Mistake 1 — Reusing an exhausted iterator

```python
iterator = iter([1, 2, 3])

list(iterator)
list(iterator)
```

The second result is empty.

______________________________________________________________________

## Mistake 2 — Converting a huge generator to a list

```python
list(huge_generator())
```

This defeats the memory advantage of lazy evaluation.

______________________________________________________________________

## Mistake 3 — Creating an infinite generator without a termination condition

```python
sum(counter())
```

never finishes.

______________________________________________________________________

## Mistake 4 — Assuming every iterable is an iterator

A list is iterable but is not itself an iterator.

```python
iter(items)
```

creates an iterator.

______________________________________________________________________

## Mistake 5 — Overusing generators

Generators are not automatically better.

If the dataset is small and needs to be traversed multiple times, a list may be simpler and more appropriate.

______________________________________________________________________

# 37. Backend Design Considerations

When deciding between a list and generator, ask:

### Do I need all values immediately?

Use a list when immediate materialization is useful.

### Is the dataset potentially large?

Consider a generator.

### Do I need multiple passes?

A reusable collection may be more appropriate.

### Do I need random access?

A list or another indexed structure is usually better.

### Is the source streaming?

A generator/iterator is often a natural fit.

### Is processing asynchronous?

Consider an async iterator or async generator.

The right abstraction depends on consumption requirements, not just memory optimization.

______________________________________________________________________

# 38. Interview Questions & Answers

## Q1. What is an iterable?

**Answer:**

An iterable is an object that can provide an iterator, generally through `iter(obj)`.

Examples include lists, tuples, strings, dictionaries, sets and ranges.

______________________________________________________________________

## Q2. What is an iterator?

**Answer:**

An iterator is an object that produces values one at a time through the iterator protocol:

```python
__iter__()
__next__()
```

It maintains traversal state and raises `StopIteration` when exhausted.

______________________________________________________________________

## Q3. What is the difference between an iterable and an iterator?

**Answer:**

An iterable can produce an iterator.

An iterator itself produces the next value and maintains iteration state.

A list is iterable; `iter(list)` returns an iterator.

______________________________________________________________________

## Q4. Why does an iterator return itself from `__iter__()`?

**Answer:**

Because the iterator is already the object responsible for traversal.

Therefore:

```python
iter(iterator) is iterator
```

normally holds.

______________________________________________________________________

## Q5. How does a `for` loop work conceptually?

**Answer:**

It obtains an iterator with `iter()` and repeatedly calls `next()` until `StopIteration` occurs.

Conceptually:

```python
iterator = iter(values)

while True:
    try:
        value = next(iterator)
    except StopIteration:
        break
```

______________________________________________________________________

## Q6. What is `StopIteration`?

**Answer:**

It signals that an iterator has no more values.

A `for` loop catches this internally and terminates normally.

______________________________________________________________________

## Q7. What is a generator?

**Answer:**

A generator is a convenient iterator implementation, usually created by a function containing `yield`.

It produces values lazily and preserves execution state between yields.

______________________________________________________________________

## Q8. When does a generator function execute?

**Answer:**

Calling a generator function returns a generator object without executing the function body normally.

Execution begins when the generator is advanced, such as with `next()` or a `for` loop.

______________________________________________________________________

## Q9. What is the difference between `yield` and `return`?

**Answer:**

`return` exits the function.

`yield` produces a value and suspends generator execution so it can resume later.

______________________________________________________________________

## Q10. Why are generators memory-efficient?

**Answer:**

They produce values on demand instead of materializing the entire result set.

This is useful for large datasets and streaming pipelines.

______________________________________________________________________

## Q11. What happens when a generator is exhausted?

**Answer:**

Further attempts to retrieve values raise `StopIteration`.

For loops handle this automatically.

______________________________________________________________________

## Q12. Are generators reusable?

**Answer:**

Normally, no.

A generator is an iterator and is consumed as it is advanced.

If you need another traversal, create a new generator or use a reusable iterable.

______________________________________________________________________

## Q13. What is lazy evaluation?

**Answer:**

Lazy evaluation delays computation until the result is actually requested.

Generator expressions and generator functions provide a common form of lazy evaluation in Python.

______________________________________________________________________

## Q14. What is `yield from`?

**Answer:**

`yield from` delegates iteration to another iterable or generator.

```python
def combined():
    yield from first()
    yield from second()
```

It is useful for composing generators.

______________________________________________________________________

## Q15. What is an async generator?

**Answer:**

An async generator is defined with `async def` and uses `yield`.

It can be consumed with:

```python
async for item in generator:
    ...
```

It is useful when values are produced as part of asynchronous operations.

______________________________________________________________________

## Q16. What is the difference between a generator and a coroutine?

**Answer:**

A generator is primarily an iteration mechanism that can suspend at `yield`.

A coroutine represents asynchronous computation and is normally written with `async def` and `await`.

______________________________________________________________________

## Q17. Can a generator be infinite?

**Answer:**

Yes.

```python
def counter():
    value = 0

    while True:
        yield value
        value += 1
```

It produces values indefinitely and must be consumed with an appropriate stopping condition.

______________________________________________________________________

## Q18. What is `iter(callable, sentinel)`?

**Answer:**

It repeatedly calls a callable and yields its results until the returned value equals the sentinel.

It is useful for chunked reads and similar repeated-call patterns.

______________________________________________________________________

## Q19. When should you not use a generator?

**Answer:**

When you need:

- Random access
- Multiple independent passes
- Immediate materialization
- Simple small collections

A list or another reusable collection may be clearer.

______________________________________________________________________

## Q20. Why can converting a generator to a list be problematic?

**Answer:**

It forces all values to be generated and stored in memory.

For a large or infinite generator, this can cause excessive memory usage or never terminate.

______________________________________________________________________

# 39. Scenario-Based Questions

## Scenario 1 — API Uses Too Much Memory

An endpoint loads one million database records into a list before returning/processing them.

**Question:** What would you consider?

**Answer:**

If the processing can be incremental, use streaming/lazy iteration or database pagination.

For example, process records in batches or expose a streaming response where appropriate.

The goal is to avoid unnecessary materialization of the entire dataset.

______________________________________________________________________

## Scenario 2 — Generator Works Once

A developer writes:

```python
records = generate_records()

for record in records:
    process(record)

for record in records:
    audit(record)
```

The second loop processes nothing.

**Question:** Why?

**Answer:**

`records` is a generator iterator and has already been exhausted.

If two passes are required, either:

- Create a new generator for each pass.
- Materialize the data if appropriate.
- Redesign the pipeline.

______________________________________________________________________

## Scenario 3 — Large File Processing

You need to process a 20 GB log file.

**Question:** Would you use `read()` followed by `splitlines()`?

**Answer:**

Not normally.

That would potentially load a huge amount of data into memory.

Prefer line-by-line iteration or chunked processing:

```python
with open("large.log") as file:
    for line in file:
        process(line)
```

______________________________________________________________________

## Scenario 4 — Generator Pipeline

You need:

```text
raw records
    ↓
filter active
    ↓
extract IDs
    ↓
send downstream
```

There may be millions of records.

**Question:** What Python feature fits naturally?

**Answer:**

A generator pipeline.

Each stage can consume and produce one item at a time, avoiding large intermediate lists.

______________________________________________________________________

## Scenario 5 — Async Data Stream

An application receives records from an asynchronous source and should process them as they arrive.

**Question:** Would a normal generator be sufficient?

**Answer:**

If producing the values requires asynchronous operations, use an async iterator or async generator:

```python
async def records():
    ...
    yield record
```

and consume it with:

```python
async for record in records():
    ...
```

______________________________________________________________________

# 40. Practice Exercises

## Exercise 1 — Custom Iterator

Implement:

```python
RangeIterator(5)
```

so that:

```python
list(RangeIterator(5))
```

returns:

```python
[0, 1, 2, 3, 4]
```

Implement the iterator protocol manually.

______________________________________________________________________

## Exercise 2 — Generator Version

Rewrite the previous exercise using a generator function.

Compare the implementation complexity.

______________________________________________________________________

## Exercise 3 — Lazy File Pipeline

Create a pipeline:

```text
file
 ↓
strip lines
 ↓
ignore empty lines
 ↓
yield only ERROR lines
```

Do not load the whole file into memory.

______________________________________________________________________

## Exercise 4 — Generator Pipeline

Given:

```python
users = [
    {"id": 1, "active": True},
    {"id": 2, "active": False},
    {"id": 3, "active": True},
]
```

Create a lazy pipeline that:

1. Filters active users.
1. Extracts IDs.
1. Produces the IDs one at a time.

______________________________________________________________________

## Exercise 5 — Chunk Reader

Implement a generator:

```python
read_chunks(file, chunk_size)
```

that yields chunks until the file is exhausted.

______________________________________________________________________

## Exercise 6 — Infinite Generator

Implement:

```python
counter(start=0)
```

that produces:

```text
0, 1, 2, 3, ...
```

Then consume only the first 10 values.

______________________________________________________________________

## Exercise 7 — `yield from`

Create two generators and combine them with:

```python
yield from
```

Verify that the resulting generator produces all values in the correct order.

______________________________________________________________________

# 41. Quick Revision

| Concept | Key Point |
|---|---|
| Iterable | Can provide an iterator |
| Iterator | Produces next values and maintains state |
| `iter()` | Gets an iterator |
| `next()` | Requests next value |
| `StopIteration` | Signals exhaustion |
| `for` | Uses iterator protocol internally |
| Generator | Convenient iterator using `yield` |
| `yield` | Produces value and suspends execution |
| `return` | Terminates function/generator |
| Lazy evaluation | Computes values when needed |
| Generator expression | Lazy comprehension-style expression |
| `yield from` | Delegates iteration |
| `send()` | Sends value into generator |
| `throw()` | Injects exception into generator |
| `close()` | Requests generator termination |
| Async generator | Async producer consumed with `async for` |
| Single-pass | Iterators are normally consumed |
| Pipeline | Multiple lazy transformations |
| `iter(callable, sentinel)` | Repeated calls until sentinel |

______________________________________________________________________

# 42. Completion Checklist

Before moving to File 5, make sure you can explain:

- [ ] Iterable vs iterator
- [ ] Iterator protocol
- [ ] `__iter__`
- [ ] `__next__`
- [ ] `iter()`
- [ ] `next()`
- [ ] `StopIteration`
- [ ] How `for` works conceptually
- [ ] Stateful iterators
- [ ] Iterator consumption
- [ ] Reusable iterables
- [ ] Generator functions
- [ ] Generator objects
- [ ] Generator execution
- [ ] `yield`
- [ ] `yield` vs `return`
- [ ] Generator state
- [ ] Lazy evaluation
- [ ] Generator expressions
- [ ] Generator pipelines
- [ ] `yield from`
- [ ] Generator `send`
- [ ] Generator `throw`
- [ ] Generator `close`
- [ ] Generator cleanup
- [ ] Infinite generators
- [ ] `iter(callable, sentinel)`
- [ ] Async generators
- [ ] Generator vs coroutine
- [ ] When generators are appropriate
- [ ] When lists are more appropriate
- [ ] Memory implications of materializing iterators

______________________________________________________________________

# 43. Interview Readiness Test

Without looking at the notes, answer these aloud:

1. What is an iterable?
1. What is an iterator?
1. What is the difference between them?
1. Explain the iterator protocol.
1. Why does `__iter__()` return `self` for an iterator?
1. How does a `for` loop use `iter()` and `next()`?
1. What is `StopIteration`?
1. What is a generator?
1. When does a generator function actually execute?
1. Explain `yield` vs `return`.
1. Why are generators memory-efficient?
1. What happens when a generator is exhausted?
1. Are generators reusable?
1. What is lazy evaluation?
1. Explain `yield from`.
1. What are `send()`, `throw()`, and `close()`?
1. How would you process a 20 GB file efficiently?
1. How would you build a lazy transformation pipeline for millions of records?
1. When would you choose a list instead of a generator?
1. What is the difference between a generator and an async generator?

If you can answer these clearly and implement the exercises without relying heavily on the notes, this chapter is
complete.

______________________________________________________________________

**Previous:** [3. Decorators & Context Managers](./03-python-decorators-context-managers.md)

**Next:** [5. Python Collections & Data Structures](./05-python-collections.md)

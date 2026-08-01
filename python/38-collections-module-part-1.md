# File: python/38-collections-module-part-1.md

# Python Standard Library

# Collections Module - Part 1: `deque`, `Counter` & `defaultdict`

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Standard Library
>
> **Lesson:** 38
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 5 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `collections` module | Python 2.4 |
| `deque` | Python 2.4 |
| `defaultdict` | Python 2.5 |
| `Counter` | Python 2.7 |

### Important Python Version Changes

- `collections` has grown significantly over the years.
- Python 3.7+ guarantees dictionary insertion order, reducing the need for `OrderedDict` in many situations.
- The data structures in `collections` are highly optimised and should generally be preferred over writing custom implementations.

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why the `collections` module exists
- When built-in collections are not enough
- `deque`
- `Counter`
- `defaultdict`
- Internal implementation
- Performance comparisons
- Production use cases
- Best practices

______________________________________________________________________

# Recap

In the previous lesson, we explored Python's numeric types:

- `int`
- `float`
- `bool`
- `Decimal`
- `Fraction`
- `complex`

Now we'll begin exploring one of Python's most useful standard library modules.

______________________________________________________________________

# Why Does `collections` Exist?

Python already provides:

- list
- tuple
- dict
- set

So why create another module?

Because some problems appear so frequently that specialised data structures provide:

- Cleaner code
- Better performance
- Fewer bugs

Instead of writing your own implementation, Python already provides one.

______________________________________________________________________

# Real Backend Example

Imagine a web server processing requests.

Requests arrive continuously.

```
Request 1

↓

Request 2

↓

Request 3

↓

Request 4
```

Should we use a list?

Maybe.

But there is a better option.

______________________________________________________________________

# Introducing `deque`

`deque` stands for

```
Double Ended Queue
```

It allows efficient insertion and removal from **both ends**.

______________________________________________________________________

# Import

```python
from collections import deque
```

______________________________________________________________________

# Creating a Deque

```python
from collections import deque

queue = deque()

queue.append("Alice")

queue.append("Bob")

print(queue)
```

Output

```text
deque(['Alice', 'Bob'])
```

______________________________________________________________________

# Queue Behaviour (FIFO)

A queue follows:

```
First In

↓

First Out
```

Example

```python
from collections import deque

queue = deque()

queue.append("Task A")

queue.append("Task B")

queue.append("Task C")

print(queue.popleft())
```

Output

```text
Task A
```

______________________________________________________________________

# Stack Behaviour (LIFO)

A deque can also behave like a stack.

```
Last In

↓

First Out
```

```python
stack = deque()

stack.append("A")

stack.append("B")

stack.append("C")

print(stack.pop())
```

Output

```text
C
```

______________________________________________________________________

# Why Not Use a List?

Consider removing the first element.

```python
numbers = [1, 2, 3]

numbers.pop(0)
```

Complexity

```
O(n)
```

Every remaining element must shift.

______________________________________________________________________

With a deque

```python
queue = deque([1, 2, 3])

queue.popleft()
```

Complexity

```
O(1)
```

No shifting.

______________________________________________________________________

# Internal Representation

A list is a dynamic array.

```
+----+----+----+----+

| A | B | C | D |

+----+----+----+----+
```

Removing from the front requires shifting.

A deque is implemented differently.

Conceptually

```
+-----+

|Block|

+-----+

↓

+-----+

|Block|

+-----+

↓

+-----+

|Block|

+-----+
```

Appending or removing from either end only updates the end blocks.

______________________________________________________________________

# appendleft()

```python
queue = deque()

queue.append("Bob")

queue.appendleft("Alice")

print(queue)
```

Output

```text
deque(['Alice', 'Bob'])
```

______________________________________________________________________

# extend()

```python
queue = deque(["A"])

queue.extend(["B", "C"])

print(queue)
```

Output

```text
deque(['A', 'B', 'C'])
```

______________________________________________________________________

# extendleft()

```python
queue = deque(["C"])

queue.extendleft(["B", "A"])

print(queue)
```

Output

```text
deque(['A', 'B', 'C'])
```

Notice something interesting.

`extendleft()` inserts each element on the left one at a time, so the iterable appears reversed.

______________________________________________________________________

# rotate()

One unique feature.

```python
queue = deque([1, 2, 3, 4])

queue.rotate(1)

print(queue)
```

Output

```text
deque([4, 1, 2, 3])
```

Rotate left

```python
queue.rotate(-1)
```

______________________________________________________________________

# Maximum Length

Useful for fixed-size buffers.

```python
logs = deque(maxlen=3)

logs.append("Log 1")
logs.append("Log 2")
logs.append("Log 3")
logs.append("Log 4")

print(logs)
```

Output

```text
deque(['Log 2', 'Log 3', 'Log 4'])
```

Old entries disappear automatically.

______________________________________________________________________

# Production Example

Store the last 100 API requests.

```python
from collections import deque

recent_requests = deque(maxlen=100)

recent_requests.append(request)
```

No cleanup code required.

______________________________________________________________________

# Time Complexity

| Operation | List | Deque |
|------------|------|--------|
| Append Right | O(1) | O(1) |
| Pop Right | O(1) | O(1) |
| Append Left | O(n) | O(1) |
| Pop Left | O(n) | O(1) |
| Index Middle | O(1) | O(n) |

Notice:

Lists are better for random indexing.

Deques are better for queues.

______________________________________________________________________

# Counter

Counting items manually is common.

Example

```python
text = "banana"

counts = {}

for letter in text:

    counts[letter] = counts.get(letter, 0) + 1
```

Works.

But Python already solved this problem.

______________________________________________________________________

# Using Counter

```python
from collections import Counter

text = "banana"

counts = Counter(text)

print(counts)
```

Output

```text
Counter({

'a': 3,

'n': 2,

'b': 1

})
```

______________________________________________________________________

# Accessing Counts

```python
print(counts["a"])
```

Output

```text
3
```

Missing elements

```python
print(counts["z"])
```

Output

```text
0
```

Unlike dictionaries,

missing keys don't raise `KeyError`.

______________________________________________________________________

# most_common()

```python
text = "mississippi"

counts = Counter(text)

print(

    counts.most_common(2)

)
```

Output

```text
[('i', 4), ('s', 4)]
```

Extremely useful.

______________________________________________________________________

# Updating a Counter

```python
counts = Counter()

counts.update("apple")

counts.update("banana")

print(counts)
```

______________________________________________________________________

# Counter Arithmetic

```python
a = Counter(a=3, b=1)

b = Counter(a=1, b=5)

print(a + b)
```

Output

```text
Counter({

'b':6,

'a':4

})
```

Counters support addition, subtraction, intersection and union.

______________________________________________________________________

# Production Example

Count HTTP response codes.

```python
from collections import Counter

responses = [

    200,

    200,

    404,

    500,

    200,

]

counts = Counter(responses)

print(counts)
```

Output

```text
Counter({

200:3,

404:1,

500:1

})
```

______________________________________________________________________

# defaultdict

Earlier,

we wrote

```python
groups = {}

for department, employee in rows:

    groups.setdefault(

        department,

        []

    ).append(employee)
```

`defaultdict` makes this cleaner.

______________________________________________________________________

# Creating One

```python
from collections import defaultdict

groups = defaultdict(list)
```

Whenever a missing key is accessed,

Python automatically creates an empty list.

______________________________________________________________________

# Example

```python
from collections import defaultdict

employees = defaultdict(list)

employees["Engineering"].append("Alice")

employees["Engineering"].append("Bob")

employees["HR"].append("Carol")

print(employees)
```

Output

```text
defaultdict(

<class 'list'>,

{

'Engineering': ['Alice', 'Bob'],

'HR': ['Carol']

}

)
```

______________________________________________________________________

# Why Does This Work?

Normally

```python
data = {}

data["Engineering"].append("Alice")
```

Output

```text
KeyError
```

With `defaultdict(list)`

Python automatically executes

```python
data["Engineering"] = []
```

before appending.

______________________________________________________________________

# Other Default Factories

Integer

```python
counts = defaultdict(int)
```

Every missing key starts at

```text
0
```

Set

```python
connections = defaultdict(set)
```

Every missing key starts with

```python
set()
```

______________________________________________________________________

# Counting Example

```python
from collections import defaultdict

counts = defaultdict(int)

for letter in "banana":

    counts[letter] += 1

print(counts)
```

Output

```text
defaultdict(

<class 'int'>,

{

'b':1,

'a':3,

'n':2

}

)
```

______________________________________________________________________

# Time Complexity

| Structure | Lookup | Insert | Delete |
|------------|---------|---------|---------|
| Counter | O(1) | O(1) | O(1) |
| defaultdict | O(1) | O(1) | O(1) |
| deque (Ends) | O(1) | O(1) | O(1) |

All inherit their excellent average-case performance from Python's underlying hash tables or deque implementation.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using a list as a queue.

```python
queue.pop(0)
```

Prefer

```python
deque.popleft()
```

______________________________________________________________________

## Mistake 2

Manually counting items.

```python
counts = {}

...
```

Prefer

```python
Counter()
```

______________________________________________________________________

## Mistake 3

Repeatedly checking dictionary keys.

```python
if key not in groups:

    groups[key] = []
```

Prefer

```python
defaultdict(list)
```

______________________________________________________________________

## Mistake 4

Using a deque for frequent random indexing.

Lists are more appropriate when indexed access is the primary operation.

______________________________________________________________________

# Best Practices

✅ Use `deque` for queues and sliding windows.

✅ Use `Counter` for frequency analysis.

✅ Use `defaultdict` when keys are created dynamically.

✅ Use `maxlen` for rolling buffers.

❌ Don't use `list.pop(0)` for queue implementations.

❌ Don't manually count items when `Counter` already solves the problem.

❌ Don't replace every dictionary with a `defaultdict`; use it only when automatic initialisation is beneficial.

______________________________________________________________________

# Production Insight

These three data structures appear frequently in production backend systems.

**`deque`**

- Job queues
- Request buffers
- Sliding windows
- Rate limiting
- Log retention

**`Counter`**

- HTTP status code analysis
- API usage statistics
- Error frequency
- Word counting
- Event aggregation

**`defaultdict`**

- Grouping SQL query results
- Building graph structures
- Adjacency lists
- Categorising log events
- Indexing records by key

Many production systems become both shorter and faster simply by replacing custom implementations with these specialised
data structures.

______________________________________________________________________

# Questions

### Question

> Why is `deque.popleft()` faster than `list.pop(0)`?

### Answer

Lists are dynamic arrays, so removing the first element requires shifting all remaining elements. A deque is optimised
for insertion and removal at both ends, making `popleft()` an O(1) operation.

______________________________________________________________________

### Question

> When would you use `Counter`?

### Answer

Whenever frequency counting is required, such as counting API responses, log levels, words, or user events. It is
simpler and less error-prone than manually maintaining a dictionary.

______________________________________________________________________

### Question

> What problem does `defaultdict` solve?

### Answer

It automatically creates default values for missing keys, eliminating repetitive existence checks and reducing
boilerplate code.

______________________________________________________________________

### Question

> Why shouldn't a deque replace every list?

### Answer

Because deques optimise end operations, not random indexing. Lists provide faster indexed access and are generally a
better choice when queue behaviour is not required.

______________________________________________________________________

# Practical Lesson

Create:

```text
collections_examples.py
```

```python
from collections import Counter
from collections import defaultdict
from collections import deque

# -----------------------------
# deque example
# -----------------------------
requests = deque(maxlen=3)

requests.append("GET /users")
requests.append("POST /login")
requests.append("GET /health")
requests.append("GET /products")

print(requests)

# -----------------------------
# Counter example
# -----------------------------
status_codes = [200, 200, 404, 500, 200]

counts = Counter(status_codes)

print(counts)

print(counts.most_common(1))

# -----------------------------
# defaultdict example
# -----------------------------
employees = defaultdict(list)

employees["Engineering"].append("Alice")
employees["Engineering"].append("Bob")
employees["HR"].append("Carol")

print(employees)
```

Expected Output

```text
deque([
    'POST /login',
    'GET /health',
    'GET /products'
])

Counter({
    200: 3,
    404: 1,
    500: 1
})

[(200, 3)]

defaultdict(
    <class 'list'>,
    {
        'Engineering': ['Alice', 'Bob'],
        'HR': ['Carol']
    }
)
```

______________________________________________________________________

# Questions

## Question 1

When should you use a `deque` instead of a list?

### Answer

Use a `deque` when your application frequently inserts or removes elements from the beginning or end of a sequence, such
as queues and sliding windows.

______________________________________________________________________

## Question 2

What advantages does `Counter` provide over a normal dictionary?

### Answer

It automatically counts frequencies, returns `0` for missing keys, supports arithmetic operations and provides
convenience methods like `most_common()`.

______________________________________________________________________

## Question 3

What is the purpose of `defaultdict`?

### Answer

It automatically initialises missing keys using a default factory, reducing repetitive existence checks and simplifying
grouping and counting logic.

______________________________________________________________________

## Question 4

Why is `deque(maxlen=N)` useful?

### Answer

It automatically maintains a fixed-size buffer by discarding the oldest elements when new ones are added.

______________________________________________________________________

## Question 5

Why isn't a `deque` ideal for random indexing?

### Answer

Although indexing is supported, deques are optimised for operations at both ends rather than fast random access. Lists
remain the better choice for frequent indexed access.

______________________________________________________________________

# Assignment

## Exercise 1

Implement a task scheduler using `deque`.

Support:

- Add task
- Process next task
- View pending tasks

______________________________________________________________________

## Exercise 2

Read an application log file and use `Counter` to calculate:

- Number of `INFO` messages
- Number of `WARNING` messages
- Number of `ERROR` messages

Display the results sorted by frequency.

______________________________________________________________________

## Exercise 3

Given a list of employees, group them by department using:

- A normal dictionary
- `setdefault()`
- `defaultdict(list)`

Compare the readability of all three implementations.

______________________________________________________________________

## Exercise 4

Implement a rolling buffer that stores only the last 50 API requests using `deque(maxlen=50)`. Simulate 100 incoming
requests and verify that only the newest 50 remain.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why the `collections` module exists.
- ✅ When to use `deque`.
- ✅ Internal behaviour of `deque`.
- ✅ How `Counter` simplifies frequency counting.
- ✅ How `defaultdict` eliminates repetitive key initialisation.
- ✅ Performance characteristics.
- ✅ Production use cases.
- ✅ Common interview topics.

______________________________________________________________________

# What's Next

**File:** [39-Collections-Module-part-2](39-collections-module-part-2.md)

Topics:

- `namedtuple`
- `OrderedDict`
- `ChainMap`
- `UserDict`
- `UserList`
- `UserString`
- Choosing the right collection
- Advanced production patterns
- Performance trade-offs

> **Note:** We'll also discuss which `collections` types are still highly relevant today and which have become less common due to improvements in modern Python.

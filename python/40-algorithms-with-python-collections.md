# File: python/40-algorithms-with-python-collections.md

# Python Algorithms
# Algorithms with Python Collections: Solving Real Backend Problems

> **Course:** Backend Engineering Roadmap
>
> **Module:** Algorithms with Python Collections
>
> **Lesson:** 40
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 6 Hours

---

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `dict` | Python 1.0 |
| `set` | Python 2.4 |
| `deque` | Python 2.4 |
| `Counter` | Python 2.7 |
| `defaultdict` | Python 2.5 |

---

# Learning Objectives

By the end of this lesson, you will understand:

- How to choose the correct data structure
- How collections improve algorithm performance
- Frequency counting
- Grouping
- Deduplication
- Sliding window algorithms
- Top-K problems
- Breadth-First Search (BFS)
- Caching
- Production backend applications

---

# Recap

Over the previous lessons you learned the individual data structures.

Now comes the most important question.

> **Which one should I choose?**

Senior engineers don't memorise APIs.

They recognise patterns.

Choosing the right collection often changes an algorithm from:

```
O(n²)

↓

O(n)
```

without changing the business logic.

---

# Think Like an Engineer

Before writing code, ask:

1. Do I need ordering?
2. Do I need uniqueness?
3. Do I need fast lookup?
4. Do I need counting?
5. Do I need grouping?
6. Do I need queue behaviour?
7. Do I need stack behaviour?

Choosing the answer usually determines the data structure.

---

# Data Structure Selection Guide

| Problem | Best Choice |
|----------|-------------|
| Fast lookup | `dict` |
| Remove duplicates | `set` |
| Count occurrences | `Counter` |
| Group data | `defaultdict` |
| Queue | `deque` |
| Stack | `list` or `deque` |
| Fixed-size buffer | `deque(maxlen=N)` |

This table is worth memorising.

---

# Pattern 1: Fast Lookups

Suppose we have

```python
users = [
    {"id": 101, "name": "Alice"},
    {"id": 102, "name": "Bob"},
    {"id": 103, "name": "Carol"},
]
```

Finding user `103`

Naive approach

```python
def find_user(users, user_id):
    for user in users:
        if user["id"] == user_id:
            return user
```

Complexity

```
O(n)
```

---

# Better Solution

Create a lookup table.

```python
users_by_id = {
    user["id"]: user
    for user in users
}

print(users_by_id[103])
```

Complexity

```
Build:

O(n)

Lookup:

O(1)
```

---

# Production Example

Database query

```sql
SELECT id, name
FROM users;
```

Instead of repeatedly scanning the list,

build

```python
user_lookup = {
    row.id: row
    for row in rows
}
```

Thousands of lookups become nearly instantaneous.

---

# Pattern 2: Duplicate Detection

Suppose

```python
emails = [

    "a@test.com",

    "b@test.com",

    "a@test.com",

]
```

Detect duplicates.

Wrong

```python
duplicates = []

for email in emails:

    if email in duplicates:
        ...

    duplicates.append(email)
```

Complexity

```
O(n²)
```

---

# Better

```python
seen = set()

duplicates = set()

for email in emails:

    if email in seen:
        duplicates.add(email)

    else:
        seen.add(email)

print(duplicates)
```

Complexity

```
O(n)
```

---

# Production Example

Webhook deduplication.

```python
processed = set()

if webhook_id in processed:

    ignore()

else:

    processed.add(webhook_id)
```

Very common.

---

# Pattern 3: Frequency Counting

Suppose

```
404

404

500

200

200

200
```

Instead of

```python
counts = {}

for code in responses:

    counts[code] = counts.get(code, 0) + 1
```

Use

```python
from collections import Counter

counts = Counter(responses)
```

Cleaner.

Less error-prone.

---

# Production Example

Analyse API responses.

```python
Counter(

response.status_code

for response in logs

)
```

Output

```text
Counter({

200: 1400,

404: 32,

500: 5

})
```

---

# Pattern 4: Grouping

Input

```python
employees = [

("Engineering", "Alice"),

("HR", "Bob"),

("Engineering", "Carol")

]
```

Goal

```
Engineering

↓

Alice

Carol


HR

↓

Bob
```

---

# Using defaultdict

```python
from collections import defaultdict

groups = defaultdict(list)

for department, employee in employees:

    groups[department].append(employee)
```

Result

```python
{

"Engineering":

["Alice", "Carol"],

"HR":

["Bob"]

}
```

Complexity

```
O(n)
```

---

# Production Example

Grouping database rows.

```python
orders_by_customer = defaultdict(list)

for order in orders:

    orders_by_customer[
        order.customer_id
    ].append(order)
```

---

# Pattern 5: Sliding Window

Suppose

We only care about

the last

```
100

requests
```

Instead of manually removing old entries,

use

```python
from collections import deque

recent = deque(maxlen=100)
```

Every new request

```python
recent.append(request)
```

Old entries disappear automatically.

---

# Production Example

Store recent logs.

```
Last

1000

errors
```

Perfect use case for

```python
deque(maxlen=1000)
```

---

# Pattern 6: Top-K Problems

Question

```
Top 5

most common

searches
```

Instead of sorting manually,

```python
from collections import Counter

counts = Counter(searches)

print(

counts.most_common(5)

)
```

Output

```text
[
("Python", 210),

("FastAPI", 170),

...
]
```

---

# Production Example

Most common

- URLs
- API endpoints
- Countries
- Browsers
- Errors

---

# Pattern 7: Breadth-First Search (BFS)

Graphs appear everywhere.

Examples

- Social networks
- Road maps
- Service dependencies
- Workflow engines

BFS requires a queue.

---

# Why Not a List?

```
pop(0)

↓

O(n)
```

Instead

```
deque

↓

popleft()

↓

O(1)
```

---

# BFS Example

```python
from collections import deque

graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": [],
    "D": [],
}

queue = deque(["A"])
visited = set()

while queue:
    node = queue.popleft()

    if node in visited:
        continue

    print(node)

    visited.add(node)

    queue.extend(graph[node])
```

Output

```text
A
B
C
D
```

---

# Pattern 8: Caching

Suppose

calculating

```python
get_user_permissions()
```

takes

```
300 ms
```

Repeated calls waste resources.

---

# Simple Cache

```python
cache = {}

def get_permissions(user_id):

    if user_id not in cache:

        cache[user_id] = expensive_lookup(user_id)

    return cache[user_id]
```

Complexity

```
Lookup

↓

O(1)
```

---

# Production Example

Common caches

```
JWT Claims

↓

User Profiles

↓

Feature Flags

↓

Configuration

↓

Database Metadata
```

Almost always backed by dictionaries.

---

# Pattern 9: Membership Filtering

Suppose

```
1 million

blocked IPs
```

Need to determine

```
Is this IP blocked?
```

Wrong

```python
if ip in blocked_list:
```

Complexity

```
O(n)
```

Better

```python
blocked = set(blocked_ips)

if ip in blocked:
```

Complexity

```
Average O(1)
```

---

# Choosing the Right Collection

| Problem | Wrong Choice | Better Choice |
|----------|-------------|---------------|
| Queue | List | `deque` |
| Deduplication | List | `set` |
| Counting | Dictionary | `Counter` |
| Grouping | Dictionary | `defaultdict` |
| Lookup | List | `dict` |
| Sliding Window | List | `deque(maxlen)` |

Notice that "wrong" often means "less suitable", not "incorrect".

---

# Performance Comparison

| Problem | Naive | Optimised |
|----------|-------|-----------|
| Lookup | O(n) | O(1) |
| Membership | O(n) | O(1) |
| Queue Pop | O(n) | O(1) |
| Duplicate Detection | O(n²) | O(n) |
| Grouping | Verbose | O(n) |
| Counting | Manual | O(n) |

---

# Real Backend Case Study

Imagine an API receives

```
250,000

requests/hour
```

Requirements

- Detect duplicate request IDs
- Count status codes
- Store last 500 requests
- Group requests by customer
- Cache user information

Ideal solution

```python
processed_ids = set()

status_counts = Counter()

recent_requests = deque(maxlen=500)

requests_by_customer = defaultdict(list)

user_cache = {}
```

Five specialised collections.

Each solves one problem efficiently.

---

# Common Mistakes

## Mistake 1

Using a list everywhere.

Python provides specialised data structures for a reason.

---

## Mistake 2

Optimising too early.

Don't introduce complexity unless the workload requires it.

---

## Mistake 3

Ignoring algorithmic complexity.

Replacing an O(n²) solution with O(n) often has a greater impact than micro-optimisations.

---

## Mistake 4

Building lookup dictionaries repeatedly.

If the underlying data hasn't changed, reuse the lookup table.

---

# Best Practices

✅ Choose data structures based on access patterns.

✅ Convert lists into sets when repeated membership tests are required.

✅ Use `Counter` instead of manual counting.

✅ Use `defaultdict` for grouping.

✅ Use `deque` for queue-like behaviour.

✅ Profile before optimising.

❌ Don't use nested loops when a hash table can solve the problem.

❌ Don't choose a collection because it's familiar; choose it because it matches the algorithm.

---

# Production Insight

Many backend performance improvements come from selecting the right collection—not from changing programming languages or adding hardware.

For example:

- Converting repeated list lookups to a dictionary can reduce latency dramatically.
- Replacing `list.pop(0)` with `deque.popleft()` can remove a bottleneck in queue processing.
- Using a `set` for deduplication can reduce processing from quadratic to linear time.

These improvements are simple, readable, and scale well.

---

# Questions

### Question

> How can you improve repeated lookups in a list of database records?

### Answer

Build a dictionary keyed by the unique identifier. This converts repeated O(n) searches into O(1) average-case lookups after an initial O(n) preprocessing step.

---

### Question

> When should you use a `set` instead of a `list`?

### Answer

When uniqueness or frequent membership testing is required. Sets provide average O(1) membership tests compared with O(n) for lists.

---

### Question

> Why is `deque` preferred for BFS?

### Answer

Breadth-first search repeatedly removes elements from the front of a queue. `deque.popleft()` is O(1), while `list.pop(0)` is O(n).

---

### Question

> How would you group database rows by customer?

### Answer

Use `defaultdict(list)` and append each row to the list associated with its customer ID.

---

### Question

> What is the biggest optimisation opportunity in many Python applications?

### Answer

Choosing the correct data structure and algorithm. Reducing time complexity from O(n²) to O(n) usually has a much larger impact than low-level code optimisations.

---

# Practical Lesson

Create:

```text
backend_collections_patterns.py
```

```python
from collections import Counter, defaultdict, deque

# -----------------------------
# Fast lookup
# -----------------------------
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]

user_lookup = {user["id"]: user for user in users}

print(user_lookup[2])

# -----------------------------
# Duplicate detection
# -----------------------------
seen = set()

for request_id in [100, 101, 100, 102]:

    if request_id in seen:
        print(f"Duplicate request: {request_id}")

    seen.add(request_id)

# -----------------------------
# Counter
# -----------------------------
responses = Counter([200, 200, 404, 500, 200])

print(responses)

# -----------------------------
# defaultdict
# -----------------------------
orders = defaultdict(list)

orders[1].append("Order-001")
orders[1].append("Order-002")

print(orders)

# -----------------------------
# Sliding window
# -----------------------------
recent = deque(maxlen=3)

for request in range(5):
    recent.append(request)

print(recent)
```

Expected Output

```text
{'id': 2, 'name': 'Bob'}

Duplicate request: 100

Counter({
    200: 3,
    404: 1,
    500: 1
})

defaultdict(
    <class 'list'>,
    {
        1: ['Order-001', 'Order-002']
    }
)

deque([2, 3, 4], maxlen=3)
```

---

# Questions

## Question 1

How do you optimise repeated lookups in a collection?

### Answer

Create a dictionary keyed by a unique identifier to achieve average O(1) lookups.

---

## Question 2

Why is a `set` ideal for duplicate detection?

### Answer

Because membership tests and insertions are average O(1), allowing duplicate detection in linear time.

---

## Question 3

When should `Counter` be preferred over a normal dictionary?

### Answer

When counting frequencies, as it simplifies the code and provides useful methods such as `most_common()`.

---

## Question 4

What is the ideal data structure for implementing a queue?

### Answer

`collections.deque`, because it supports O(1) insertion and removal from both ends.

---

## Question 5

Why is choosing the correct data structure often more important than micro-optimisations?

### Answer

Because improving an algorithm's time complexity (for example, O(n²) to O(n)) typically provides much greater performance gains than small implementation tweaks.

---

# Assignment

## Exercise 1

You receive 1 million log entries containing user IDs.

Implement:

- Fast user lookup
- Duplicate detection
- User activity counts

Choose the appropriate collection for each task and explain why.

---

## Exercise 2

Build a rate limiter.

Requirements:

- Store only the last 100 requests per user.
- Efficiently add new requests.
- Remove the oldest requests automatically.

Use `deque(maxlen=100)`.

---

## Exercise 3

Given a list of products:

- Group them by category.
- Count products in each category.
- Find the top three largest categories.

Use `defaultdict` and `Counter`.

---

## Exercise 4

Implement a graph traversal using BFS.

Requirements:

- Use `deque`.
- Track visited nodes using a `set`.
- Explain why each collection was chosen.

---

# Summary

In this lesson, you learned:

- ✅ How experienced engineers choose the right collection.
- ✅ Common algorithmic patterns in backend systems.
- ✅ Lookup tables with dictionaries.
- ✅ Deduplication with sets.
- ✅ Counting with `Counter`.
- ✅ Grouping with `defaultdict`.
- ✅ Sliding windows with `deque`.
- ✅ BFS using queues.
- ✅ Caching strategies.
- ✅ Performance-oriented thinking.

---

# Module Summary – Built-in Types, Collections & Algorithms

Lessons **29–40** covered:

- String internals
- Lists
- Tuples
- Dictionaries
- Sets
- Numeric types
- The `collections` module
- Practical algorithmic patterns

You now have a solid understanding of Python's core data structures, their internal behaviour, and how to apply them effectively in production backend systems.

---

# What's Next

**Phase 2 – Advanced Python Runtime & Concurrency**

**File:**
[41-Concurrency-part-1-Processes-vs-Threads](41-concurrency-part-1-processes-vs-threads.md)

Topics:

- Why concurrency matters
- Concurrency vs parallelism
- Processes vs threads
- Operating system scheduling
- Context switching
- CPU-bound vs I/O-bound workloads
- The Global Interpreter Lock (GIL) introduction
- Backend production examples

> **This marks the beginning of one of the most important sections of the course.** We'll move beyond language syntax into how Python interacts with the operating system, how high-performance backend services handle thousands of requests, and why understanding concurrency is essential for senior backend engineers.

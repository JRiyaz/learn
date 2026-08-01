# File: python/66-production-python-part-12-memory-optimization.md

# Production Python

# Part 11: Memory Optimization – Writing Memory-Efficient Python Applications

> **Course:** Backend Engineering Roadmap
>
> **Module:** Production Python
>
> **Lesson:** 66
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 10–12 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- How Python uses memory
- Why memory optimisation matters
- Common causes of excessive memory usage
- Memory allocation in CPython
- Object overhead
- Memory-efficient data structures
- Lazy evaluation
- Streaming large datasets
- Object pooling and reuse
- Detecting memory leaks
- Production best practices

______________________________________________________________________

# Recap

Most developers think about performance in terms of execution time.

However, memory is just as important.

Consider these two programs:

```python
Program A

Memory: 60 MB

Execution Time: 3 seconds
```

```python
Program B

Memory: 4 GB

Execution Time: 2.8 seconds
```

Although Program B is slightly faster, it is far more expensive to run and may not fit within container or cloud memory
limits.

Efficient software balances both CPU time and memory usage.

______________________________________________________________________

# Why Memory Optimisation Matters

Memory directly affects:

- Application stability
- Infrastructure costs
- Scalability
- Garbage collection frequency
- Cache efficiency
- Container density

For backend services handling thousands of requests, reducing memory consumption often increases throughput and lowers
operational costs.

______________________________________________________________________

# How CPython Uses Memory

Every Python object occupies memory.

Even a simple integer is more than just its numeric value.

```
Python Variable

↓

Reference

↓

PyObject

↓

Metadata

↓

Actual Value
```

Each object stores metadata such as:

- Reference count
- Object type
- Internal flags

This metadata makes Python flexible but increases memory usage.

______________________________________________________________________

# Object Overhead

Example:

```python
x = 10
```

This creates:

```
Variable x

↓

Reference

↓

Integer Object

↓

Metadata + Value
```

The overhead is much larger than the integer itself.

This explains why Python generally uses more memory than languages like C or Go.

______________________________________________________________________

# Lists vs Generators

Suppose we process one million numbers.

List:

```python
numbers = [x for x in range(1_000_000)]
```

Memory:

```
One Million Objects

↓

Stored Simultaneously
```

Generator:

```python
numbers = (
    x for x in range(1_000_000)
)
```

Memory:

```
One Value

↓

Generated On Demand
```

Whenever possible, prefer lazy evaluation for large datasets.

______________________________________________________________________

# Reading Large Files

Bad:

```python
with open("logs.txt") as file:

    data = file.readlines()
```

Entire file:

```
Disk

↓

Memory
```

Good:

```python
with open("logs.txt") as file:

    for line in file:

        process(line)
```

Now only one line is held in memory at a time.

This pattern scales to files of virtually any size.

______________________________________________________________________

# Streaming Data

Suppose an API returns one million records.

Avoid:

```
Database

↓

Load Everything

↓

Process
```

Prefer:

```
Database

↓

Fetch Batch

↓

Process

↓

Fetch Next Batch
```

Streaming reduces peak memory usage dramatically.

______________________________________________________________________

# Choosing the Right Data Structure

Different structures have different memory characteristics.

| Structure | Best Use |
|------------|----------|
| List | Ordered collection |
| Tuple | Immutable data |
| Set | Fast membership checks |
| Dictionary | Key-value lookup |
| deque | Queue operations |

Selecting the appropriate structure improves both memory usage and performance.

______________________________________________________________________

# Tuples vs Lists

Example:

```python
point = (10, 20)
```

A tuple:

- Is immutable.
- Uses less memory.
- Can be hashed.
- Is often slightly faster to create.

If data never changes, a tuple is usually a better choice.

______________________________________________________________________

# __slots__

Regular objects:

```python
class User:

    pass
```

Each instance has:

```
Instance

↓

__dict__

↓

Attributes
```

Using:

```python
class User:

    __slots__ = (
        "id",
        "name",
    )
```

removes the instance dictionary and stores attributes in a fixed layout.

Benefits:

- Lower memory usage.
- Faster attribute access.

Trade-offs:

- No dynamic attributes.
- Reduced flexibility.

We covered `__slots__` in Lesson 25.

______________________________________________________________________

# Avoid Unnecessary Copies

Bad:

```python
users_copy = users[:]
```

This duplicates the list.

Similarly:

```python
sorted_users = sorted(users)
```

creates a new list.

If modifying in place is acceptable:

```python
users.sort()
```

avoids the additional allocation.

Choose the approach that best fits your application's requirements.

______________________________________________________________________

# Caching Carefully

Caching improves speed but increases memory usage.

Example:

```
Database

↓

Cache

↓

Application
```

A cache without limits can become a memory leak.

Always define:

- Maximum size
- Expiration policy
- Eviction strategy

______________________________________________________________________

# Memory Leaks in Python

Python has garbage collection, but memory leaks are still possible.

Examples:

- Global dictionaries that continuously grow.
- Infinite caches.
- Objects stored in long-lived collections.
- Background tasks retaining references.

Garbage collection only frees objects that are no longer reachable.

______________________________________________________________________

# Weak References

Sometimes you want to reference an object without preventing it from being collected.

Python provides the `weakref` module for this purpose.

Conceptually:

```
Strong Reference

↓

Object Stays Alive
```

```
Weak Reference

↓

Object May Be Collected
```

Weak references are commonly used in caches, registries, and observer implementations.

______________________________________________________________________

# Measuring Memory

Useful tools include:

- `tracemalloc`
- `memory_profiler`
- `objgraph`

Example:

```python
import tracemalloc

tracemalloc.start()

# Run application code

snapshot = tracemalloc.take_snapshot()

top = snapshot.statistics("lineno")

for stat in top[:5]:

    print(stat)
```

This identifies where memory allocations occur.

______________________________________________________________________

# Backend Example

Suppose an endpoint exports customer transactions.

Bad approach:

```
Database

↓

Load 2 Million Rows

↓

Create List

↓

Return Response
```

Peak memory usage becomes extremely high.

Better approach:

```
Database

↓

Fetch 1000 Rows

↓

Serialize

↓

Send

↓

Fetch Next Batch
```

The application maintains a nearly constant memory footprint regardless of dataset size.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Loading entire datasets into memory.

______________________________________________________________________

## Mistake 2

Creating unnecessary object copies.

______________________________________________________________________

## Mistake 3

Using lists where generators would suffice.

______________________________________________________________________

## Mistake 4

Building caches without limits.

______________________________________________________________________

## Mistake 5

Ignoring memory growth in long-running services.

______________________________________________________________________

# Best Practices

✅ Stream large datasets.

✅ Use generators for sequential processing.

✅ Prefer tuples for immutable data.

✅ Monitor memory usage regularly.

✅ Limit cache sizes.

✅ Profile memory before optimising.

❌ Don't optimise memory prematurely.

❌ Don't retain references longer than necessary.

______________________________________________________________________

# Production Insight

Memory optimisation becomes increasingly important in containerised environments.

Consider a Kubernetes deployment with a memory limit of:

```
512 MB
```

If a service suddenly allocates:

```
900 MB
```

the container may be terminated due to an Out Of Memory (OOM) condition.

Efficient memory usage is therefore not just about speed—it directly affects application reliability and availability.

______________________________________________________________________

# Questions

### Question

> Why do Python objects consume more memory than their raw values?

### Answer

Because each object stores metadata such as its type and reference count in addition to the actual value.

______________________________________________________________________

### Question

> Why are generators more memory efficient than lists?

### Answer

Generators produce values on demand instead of storing every value in memory simultaneously.

______________________________________________________________________

### Question

> Why is streaming preferable for large datasets?

### Answer

Streaming processes data incrementally, keeping peak memory usage low regardless of the dataset size.

______________________________________________________________________

### Question

> Can Python applications still experience memory leaks?

### Answer

Yes. Long-lived references, unbounded caches, and growing collections can prevent objects from being garbage collected.

______________________________________________________________________

### Question

> When should `__slots__` be considered?

### Answer

When creating many instances of a class with a fixed set of attributes and reduced memory usage is important.

______________________________________________________________________

# Practical Lesson

Create a script that processes a large log file.

Implement two versions:

### Version 1

```python
readlines()
```

Load the entire file into memory.

### Version 2

```python
for line in file:
```

Process the file line by line.

Use `tracemalloc` to compare:

- Peak memory usage
- Total allocations

Document the differences and explain why they occur.

______________________________________________________________________

# Knowledge Check

## Question 1

Why is reducing memory usage valuable even if execution time remains unchanged?

### Answer

Lower memory consumption improves scalability, reduces infrastructure costs, decreases the risk of OOM failures, and
allows more workloads to run on the same hardware.

______________________________________________________________________

## Question 2

When should generators be preferred over lists?

### Answer

When processing data sequentially without requiring all values to be stored or accessed simultaneously.

______________________________________________________________________

## Question 3

Why can caches become memory leaks?

### Answer

Because cached objects remain strongly referenced. Without size limits or eviction policies, memory usage can grow
indefinitely.

______________________________________________________________________

## Question 4

How does `__slots__` reduce memory usage?

### Answer

It removes the per-instance `__dict__` and stores attributes in a fixed layout, reducing object overhead.

______________________________________________________________________

## Question 5

Why is memory profiling an important production activity?

### Answer

It identifies excessive allocations, memory growth, and inefficient data handling before they affect application
stability.

______________________________________________________________________

# Assignment

## Exercise 1

Take one of your Flask or FastAPI services.

Identify every place where an entire dataset is loaded into memory.

Determine whether streaming or batching is possible.

______________________________________________________________________

## Exercise 2

Write two implementations that process one million records:

- One using a list.
- One using a generator.

Measure and compare their memory usage.

______________________________________________________________________

## Exercise 3

Use `tracemalloc` on one of your projects.

Identify the five locations responsible for the largest memory allocations.

______________________________________________________________________

## Exercise 4

Review every cache in your application.

Document:

- Maximum size
- Expiration strategy
- Eviction policy
- Potential memory risks

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ How CPython stores objects in memory.
- ✅ Why object overhead matters.
- ✅ Lists vs generators.
- ✅ Streaming large datasets.
- ✅ Memory-efficient data structures.
- ✅ Using `__slots__`.
- ✅ Avoiding unnecessary copies.
- ✅ Memory leaks and weak references.
- ✅ Measuring memory usage.
- ✅ Production memory optimisation strategies.

______________________________________________________________________

# Module Complete ✅

You have now completed the **Production Python** module.

Across Lessons **56–66**, you've learned how to build Python applications that are not only correct, but also
maintainable, configurable, testable, observable, and efficient in production environments.

The next phase of the roadmap moves from language-level concepts into **backend architecture**, where you'll apply these
Python techniques to design scalable services.

______________________________________________________________________

# Next Lesson

**File:** [68-testing-part-01-unittest](68-testing-part-01-unittest.md)

# File: python/python-advanced-02-reference-counting-and-garbage-collection-part-1.md

# Python Advanced - Lesson 02 (Part 1)
# Reference Counting & Garbage Collection

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 02 (Part 1)
>
> **Difficulty:** ⭐⭐⭐☆☆
>
> **Estimated Time:** 45-60 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- What Reference Counting is
- How Python decides when to destroy an object
- What `del` actually does
- How to use `sys.getrefcount()`
- What Garbage Collection is
- Difference between Reference Counting and Garbage Collection

---

# Why Should You Learn This?

As a backend engineer, you'll work with:

- Large datasets
- Background workers
- FastAPI applications
- Long-running services
- Microservices

Understanding memory management helps you:

- Avoid memory leaks
- Debug unexpected memory usage
- Write efficient applications
- Answer advanced Python interview questions

---

# 1. What Happens When You Create an Object?

Consider this code:

```python
name = "Riyaz"
```

What happens internally?

Python creates:

```
            Object

+----------------------------+
| Type  : str                |
| Value : "Riyaz"            |
| References : 1             |
+----------------------------+
             ▲
             │
           name
```

Notice something new?

```
References : 1
```

Every Python object keeps track of **how many variables are pointing to it**.

This is called **Reference Counting**.

---

# 2. What is Reference Counting?

Every object maintains a count of how many references point to it.

Example:

```python
x = [1, 2, 3]
```

Memory:

```
        List Object

+-----------------------+
| [1,2,3]               |
| Reference Count = 1   |
+-----------------------+
           ▲
           │
           x
```

Now:

```python
y = x
```

Memory becomes:

```
        List Object

+-----------------------+
| [1,2,3]               |
| Reference Count = 2   |
+-----------------------+
          ▲        ▲
          │        │
          x        y
```

No new list was created.

Only the reference count increased.

---

# Example 1

```python
# Create one list object.
numbers = [10, 20, 30]

# 'another' points to the same list.
another = numbers

print(numbers)
print(another)
```

Output:

```
[10, 20, 30]
[10, 20, 30]
```

Although there are two variables, there is only **one object**.

---

# 3. Checking Reference Count

Python provides a module named `sys`.

```python
import sys

numbers = [1, 2, 3]

print(sys.getrefcount(numbers))
```

You might expect:

```
1
```

But you'll likely see something like:

```
2
```

or

```
3
```

### Why?

`sys.getrefcount()` temporarily creates an additional reference while checking the count.

Think of it like this:

```
numbers

↓

Object

↑

sys.getrefcount()
```

So don't expect the "real" count directly.

---

# Example 2

```python
import sys

numbers = [1, 2, 3]

print("Initial:", sys.getrefcount(numbers))

another = numbers

print("After assignment:", sys.getrefcount(numbers))
```

Expected output (numbers may vary slightly):

```
Initial: 2

After assignment: 3
```

Notice how assigning `another = numbers` increased the count.

---

# 4. What Happens When a Variable Goes Away?

Consider:

```python
numbers = [1, 2, 3]

another = numbers

del another
```

Many developers think:

> "The list was deleted."

No.

Only the **reference** was removed.

Memory before:

```
List Object

Reference Count = 2

▲       ▲

numbers another
```

After:

```
List Object

Reference Count = 1

▲

numbers
```

The object still exists because `numbers` is still pointing to it.

---

# Example 3

```python
numbers = [1, 2, 3]

another = numbers

del another

print(numbers)
```

Output:

```
[1, 2, 3]
```

The object wasn't deleted.

Only one reference disappeared.

---

# 5. When Does Python Delete an Object?

Python destroys an object when its reference count becomes **zero**.

Example:

```python
numbers = [1, 2, 3]
```

```
Reference Count = 1
```

Now:

```python
del numbers
```

```
Reference Count = 0
```

No variable points to the object anymore.

Python immediately frees that memory.

---

# Example 4

```python
numbers = [1, 2, 3]

print("Created")

del numbers

print("Deleted")
```

After `del numbers`, the list object is eligible to be destroyed because nothing references it anymore.

---

# Important Note About `del`

Many developers misunderstand `del`.

It **does not** mean:

```
Delete Object
```

It means:

```
Delete Reference
```

Whether the object disappears depends on whether any references remain.

---

# 6. Why Isn't Reference Counting Enough?

Imagine this situation.

```python
class Employee:
    pass

emp1 = Employee()
emp2 = Employee()

emp1.friend = emp2
emp2.friend = emp1
```

Visualization:

```
emp1

↓

Employee A

↓

friend

↓

Employee B

↑

friend

↑

emp2
```

Now remove the variables:

```python
del emp1
del emp2
```

Question:

Should the objects disappear?

At first glance, yes.

But internally:

```
Employee A -----> Employee B

Employee B -----> Employee A
```

They still reference each other.

Reference count never reaches zero.

This is called a **circular reference**.

Reference counting alone cannot clean this up.

---

# 7. Garbage Collector to the Rescue

Python has another mechanism:

**Garbage Collector (GC)**

Its job is to detect objects that are no longer reachable by your program, even if they reference each other.

Think of it as a periodic cleanup worker.

```
Reference Counting

↓

Deletes normal unused objects

↓

Garbage Collector

↓

Finds unreachable cycles

↓

Deletes them
```

Reference Counting works continuously.

Garbage Collection runs periodically.

Together, they keep Python's memory healthy.

---

# Production Insight

Imagine you're building a FastAPI application.

```python
@app.get("/users")
def get_users():
    db = DatabaseConnection()

    return db.fetch_users()
```

Every request creates new objects:

- Request object
- Response object
- Database connection
- Query results

After the request finishes:

- Local variables go out of scope.
- Their reference counts drop.
- Most objects are destroyed immediately.

If objects accidentally keep references to each other (for example, through callbacks, caches, or event handlers), the Garbage Collector helps clean them up.

Understanding this helps you reason about memory usage in long-running applications.

---

# Interview Deep Dive

### Interviewer

> What is the difference between Reference Counting and Garbage Collection?

### Weak Answer

> Python uses garbage collection.

This answer is incomplete.

### Strong Answer

> Python primarily manages memory using **reference counting**, where each object tracks how many references point to it. When the reference count reaches zero, the object is destroyed immediately. However, reference counting alone cannot handle circular references, so Python also includes a cyclic garbage collector that periodically finds and frees unreachable objects involved in reference cycles.

This answer shows that you understand **both** mechanisms and how they complement each other.

---

# Practical Lesson

Create a file named:

```
reference_count_demo.py
```

Write the following code:

```python
import sys

users = ["Alice", "Bob"]

print("Reference Count:", sys.getrefcount(users))

another = users

print("Reference Count:", sys.getrefcount(users))

del another

print("Reference Count:", sys.getrefcount(users))
```

Run it several times.

Observe how the reference count changes as references are added and removed.

Try adding a third variable and predict the output before running it.

---

# Interview Questions

## Question 1

What does `del` actually delete?

### Answer

`del` removes a **reference (variable name)**, not necessarily the object itself.

The object is destroyed only if no references remain.

---

## Question 2

When does Python destroy an object?

### Answer

When its reference count reaches **zero**, meaning no variables or objects reference it anymore.

---

## Question 3

Why isn't reference counting enough?

### Answer

Because it cannot detect **circular references**.

Two or more objects can keep referencing each other, preventing their reference counts from reaching zero even though they are no longer accessible from the program.

---

## Question 4

What is the purpose of the Garbage Collector?

### Answer

The Garbage Collector identifies and removes unreachable objects involved in circular references, which reference counting alone cannot clean up.

---

## Question 5

Why does `sys.getrefcount()` usually return one more reference than expected?

### Answer

Because the object is temporarily passed as an argument to `sys.getrefcount()`, creating an additional temporary reference during the function call.

---

# Assignment

1. Create a list and assign it to three different variables.
2. Print its reference count after each assignment.
3. Remove one variable using `del`.
4. Print the reference count again.
5. Explain why the count changes after each step.

---

# Summary

In this lesson, you learned:

- ✅ Every Python object tracks how many references point to it.
- ✅ This mechanism is called **Reference Counting**.
- ✅ `del` removes a reference, not necessarily the object.
- ✅ Objects are destroyed when their reference count becomes zero.
- ✅ Circular references cannot be cleaned up using reference counting alone.
- ✅ Python's Garbage Collector detects and removes unreachable circular references.

---

# What's Next

**File:**

`python/python-advanced-02-reference-counting-and-garbage-collection-part-2.md`

Topics:

- Shallow Copy
- Deep Copy
- `copy.copy()`
- `copy.deepcopy()`
- Nested Objects
- Mutable Default Argument Bug
- Production Examples
- Interview Questions

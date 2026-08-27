# 5. Python Collections & Data Structures

**Previous:** [4. Iterators, Generators & Lazy Evaluation](./04-python-iterators-generators.md)

**Next:** [6. Exception Handling & Error Management](./06-python-exceptions.md)

______________________________________________________________________

## Objectives

By the end of this chapter, you should be able to:

- Explain the differences between `list`, `tuple`, `set`, and `dict`.
- Understand mutability, ordering, uniqueness, and hashability.
- Choose the right built-in collection for backend problems.
- Understand list, tuple, set, and dictionary operations and their typical complexity.
- Explain dictionary hashing and key requirements.
- Understand why sets and dictionaries provide efficient average-case lookup.
- Use `collections` types such as `Counter`, `defaultdict`, `deque`, and `OrderedDict` at an interview level.
- Understand `namedtuple` and when a dataclass may be preferable.
- Understand collection copying and nested mutable objects.
- Recognize common performance and correctness mistakes.
- Answer common Python collection interview questions confidently.

______________________________________________________________________

# 1. Python's Core Collections

The four built-in collection types you should know extremely well are:

| Type | Ordered | Mutable | Duplicates | Typical Use |
|---|---|---|---|---|
| `list` | Yes | Yes | Yes | Sequence of items |
| `tuple` | Yes | No | Yes | Fixed collection/record |
| `set` | No guaranteed positional order | Yes | No | Uniqueness/membership |
| `dict` | Insertion-ordered | Yes | Keys unique | Key-value lookup |

Python dictionaries preserve insertion order as part of the language specification.

Do not confuse ordering with sorting. A dictionary remembers insertion order; it does not automatically sort its keys.

______________________________________________________________________

# 2. Lists

A list is a mutable, ordered sequence.

```python
users = ["Alice", "Bob", "Carol"]
```

Common operations:

```python
users.append("David")
users.remove("Bob")
users[0]
users[-1]
```

Lists are ideal when:

- Order matters.
- Duplicates are allowed.
- You need indexing.
- You need to modify the collection.

______________________________________________________________________

# 3. List Indexing

Lists support zero-based indexing:

```python
values = [10, 20, 30]

values[0]  # 10
values[1]  # 20
```

Negative indexing:

```python
values[-1]  # 30
values[-2]  # 20
```

Indexing is typically `O(1)`.

______________________________________________________________________

# 4. List Slicing

Example:

```python
values = [0, 1, 2, 3, 4]

values[1:4]
```

returns:

```python
[1, 2, 3]
```

A slice creates a new list.

Therefore, slicing has a cost proportional to the number of elements copied.

For example:

```python
values[:]
```

creates a shallow copy of the list.

______________________________________________________________________

# 5. List Append

```python
values.append(10)
```

adds one item to the end.

Appending is typically amortized `O(1)`.

Python lists over-allocate internal storage so that repeated appends do not require reallocating the underlying array
every time.

______________________________________________________________________

# 6. List Insert

```python
values.insert(0, 10)
```

inserts an item at the beginning.

This is typically `O(n)` because existing elements may need to be shifted.

Therefore, repeatedly inserting at the beginning of a large list can be inefficient.

Use `collections.deque` when you need efficient insertion/removal from both ends.

______________________________________________________________________

# 7. List Remove and Pop

```python
values.remove(10)
```

searches for the first matching value and removes it.

Typical complexity:

```text
O(n)
```

`pop()` without an index:

```python
values.pop()
```

removes and returns the last item and is typically `O(1)`.

But:

```python
values.pop(0)
```

is typically `O(n)` because remaining elements must shift.

______________________________________________________________________

# 8. List Search

Membership:

```python
if user_id in user_ids:
    ...
```

for a list is typically:

```text
O(n)
```

If you perform many membership checks, a set may be more appropriate.

______________________________________________________________________

# 9. Tuples

A tuple is an immutable ordered sequence.

```python
point = (10, 20)
```

It supports:

- Indexing
- Slicing
- Iteration
- Membership checks

But its structure cannot be changed after creation.

You cannot:

```python
point[0] = 100
```

______________________________________________________________________

# 10. Why Use Tuples?

Tuples can communicate that a collection is intended to be fixed.

Example:

```python
coordinates = (10, 20)
```

They are also commonly used for:

- Multiple return values
- Fixed records
- Dictionary keys when their elements are hashable
- Function arguments such as `*args`

______________________________________________________________________

# 11. Tuple Packing and Unpacking

Packing:

```python
point = 10, 20
```

creates:

```python
(10, 20)
```

Unpacking:

```python
x, y = point
```

This is heavily used throughout Python code.

Example:

```python
name, age = ("Riyaz", 30)
```

______________________________________________________________________

# 12. Single-Element Tuple

This is a common interview trap:

```python
value = (10)
```

This is an integer.

A single-element tuple requires a trailing comma:

```python
value = (10,)
```

______________________________________________________________________

# 13. Sets

A set stores unique hashable elements.

```python
ids = {1, 2, 3}
```

Duplicates are removed:

```python
set([1, 1, 2, 2, 3])
```

produces a set containing:

```text
1, 2, 3
```

Sets are excellent for membership testing and set operations.

______________________________________________________________________

# 14. Set Membership

Membership testing:

```python
if user_id in user_ids:
    ...
```

is typically `O(1)` average case for a set.

This is one of the main reasons to convert a collection to a set when you need many membership checks.

______________________________________________________________________

# 15. Set Operations

Important operations include:

### Union

```python
a | b
```

### Intersection

```python
a & b
```

### Difference

```python
a - b
```

### Symmetric difference

```python
a ^ b
```

These are useful for comparing groups of IDs, permissions, tags, features and other unique values.

______________________________________________________________________

# 16. `frozenset`

`frozenset` is an immutable set.

```python
permissions = frozenset({"read", "write"})
```

It can be used as a dictionary key or as an element of another set when its contents are hashable.

A normal mutable set cannot be a dictionary key.

______________________________________________________________________

# 17. Dictionaries

A dictionary maps keys to values.

```python
user = {
    "id": 1,
    "name": "Riyaz",
}
```

Lookup:

```python
user["id"]
```

Safe lookup:

```python
user.get("email")
```

Dictionaries are one of the most important data structures in Python backend development.

______________________________________________________________________

# 18. Dictionary Keys

Dictionary keys must be hashable.

Examples of common valid keys:

```python
str
int
float
tuple
frozenset
```

provided their contents are hashable.

This is invalid:

```python
data = {
    [1, 2]: "value"
}
```

because a list is mutable and unhashable.

______________________________________________________________________

# 19. Hashability

An object is hashable when it has a hash value that remains stable during its lifetime and can participate correctly in
equality comparisons.

Hashable objects can generally be used as:

- Dictionary keys
- Set elements

Examples:

```python
"hello"
42
(1, 2)
```

A mutable list is not hashable:

```python
[1, 2]
```

______________________________________________________________________

# 20. Dictionary Lookup

Conceptually, dictionary lookup uses hashing:

```python
value = data[key]
```

Python computes a hash for the key and uses it to locate the appropriate table entry.

Average-case lookup is typically:

```text
O(1)
```

Worst-case behavior can differ, but Python's hash-table implementation is designed for efficient average-case
operations.

______________________________________________________________________

# 21. Dictionary Insertion Order

Modern Python dictionaries preserve insertion order.

Example:

```python
data = {}

data["a"] = 1
data["b"] = 2
data["c"] = 3
```

Iteration follows:

```text
a
b
c
```

However, insertion order is not the same thing as sorted order.

______________________________________________________________________

# 22. Dictionary Views

These methods return dynamic view objects:

```python
data.keys()
data.values()
data.items()
```

Example:

```python
for key, value in data.items():
    print(key, value)
```

The views are iterable and reflect changes to the dictionary.

______________________________________________________________________

# 23. `dict.get()`

Instead of:

```python
if "name" in user:
    name = user["name"]
else:
    name = None
```

you can use:

```python
name = user.get("name")
```

Or:

```python
name = user.get("name", "Unknown")
```

This is useful when a missing key is expected and should not raise `KeyError`.

______________________________________________________________________

# 24. `setdefault()`

Example:

```python
groups = {}

groups.setdefault("admin", []).append("Riyaz")
```

If `"admin"` does not exist, it creates a default list.

This is useful but can sometimes be less clear than `defaultdict`.

______________________________________________________________________

# 25. Dictionary Comprehensions

Example:

```python
squares = {
    x: x * x
    for x in range(5)
}
```

Output:

```python
{
    0: 0,
    1: 1,
    2: 4,
    3: 9,
    4: 16,
}
```

Use comprehensions for straightforward transformations.

______________________________________________________________________

# 26. Merging Dictionaries

Python supports dictionary unpacking:

```python
defaults = {"timeout": 10}
overrides = {"timeout": 30, "retries": 3}

config = {
    **defaults,
    **overrides,
}
```

Later values override earlier values.

Modern Python also provides dictionary merge operators:

```python
config = defaults | overrides
```

and in-place merging:

```python
defaults |= overrides
```

______________________________________________________________________

# 27. `collections.Counter`

`Counter` counts hashable values.

```python
from collections import Counter

counts = Counter(["error", "info", "error"])
```

Now:

```python
counts["error"]
```

returns:

```text
2
```

Useful for:

- Frequency analysis
- Counting statuses
- Counting events
- Finding most common values

______________________________________________________________________

# 28. `Counter.most_common()`

Example:

```python
counts.most_common(2)
```

returns the most frequent elements.

This is often clearer than manually constructing a frequency dictionary and sorting it.

______________________________________________________________________

# 29. `collections.defaultdict`

`defaultdict` creates a default value when a missing key is accessed.

Example:

```python
from collections import defaultdict

groups = defaultdict(list)

groups["admin"].append("Alice")
groups["admin"].append("Bob")
```

No explicit initialization is required for each key.

Another example:

```python
counts = defaultdict(int)

for value in values:
    counts[value] += 1
```

______________________________________________________________________

# 30. `defaultdict` vs `dict.setdefault`

Compare:

```python
groups = {}

groups.setdefault("admin", []).append("Alice")
```

with:

```python
groups = defaultdict(list)

groups["admin"].append("Alice")
```

`defaultdict` is often cleaner when missing-key initialization is the normal behavior.

______________________________________________________________________

# 31. `collections.deque`

A `deque` is designed for efficient appends and pops from both ends.

```python
from collections import deque

queue = deque()

queue.append("task-1")
queue.append("task-2")

queue.popleft()
```

This is useful for:

- Queues
- Sliding windows
- BFS-style traversal
- Double-ended buffers

For frequent left-side operations, prefer `deque` over a list.

______________________________________________________________________

# 32. `deque` vs List

List:

```python
items.pop(0)
```

typically requires shifting many elements.

Deque:

```python
items.popleft()
```

is designed for efficient removal from the left.

Similarly:

```python
deque.appendleft(value)
```

is efficient for adding to the left.

______________________________________________________________________

# 33. `collections.OrderedDict`

`OrderedDict` was historically important for maintaining insertion order.

Modern regular dictionaries already preserve insertion order.

However, `OrderedDict` still has specialized behavior, including efficient operations such as:

```python
move_to_end()
```

For most new code, use a normal `dict` unless you specifically need `OrderedDict` behavior.

______________________________________________________________________

# 34. `namedtuple`

`namedtuple` creates tuple-like objects with named fields.

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

point = Point(10, 20)

print(point.x)
```

It provides readable field access while retaining tuple-like behavior.

For new application/domain models, a dataclass is often a more flexible choice.

______________________________________________________________________

# 35. Dataclass vs Named Tuple

A dataclass can provide:

- Named fields
- Defaults
- Type annotations
- Mutability or frozen behavior
- Methods
- More flexible domain modeling

Example:

```python
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
```

Use `namedtuple` when tuple semantics are specifically useful.

Use a dataclass when modeling an application object.

______________________________________________________________________

# 36. Collection Copying

Consider:

```python
original = [[1, 2], [3, 4]]

copy = original.copy()
```

This creates a shallow copy.

The outer list is new, but nested lists are shared.

Therefore:

```python
copy[0].append(99)
```

also affects:

```python
original[0]
```

______________________________________________________________________

# 37. Shallow vs Deep Copy

Shallow copy:

```python
copy = original.copy()
```

or:

```python
copy = list(original)
```

copies the outer collection.

Deep copy:

```python
import copy

copy = copy.deepcopy(original)
```

recursively copies nested objects where supported.

Deep copying can be expensive and should not be used automatically.

Prefer explicit construction or immutable structures when appropriate.

______________________________________________________________________

# 38. Collection Complexity

Typical average complexities:

| Operation | List | Set | Dict |
|---|---:|---:|---:|
| Index access | O(1) | N/A | N/A |
| Membership | O(n) | O(1) | O(1) |
| Append | O(1) amortized | O(1) average | O(1) average |
| Insert at beginning | O(n) | N/A | N/A |
| Remove by value | O(n) | O(1) average | O(1) average |
| Key lookup | N/A | N/A | O(1) average |

These are typical/average characteristics, not guarantees for every operation or implementation detail.

______________________________________________________________________

# 39. Choosing the Right Collection

Ask what operation dominates.

### Need ordered indexed access?

Use:

```python
list
```

### Need an immutable sequence?

Use:

```python
tuple
```

### Need unique values and membership checks?

Use:

```python
set
```

### Need key-value lookup?

Use:

```python
dict
```

### Need efficient operations on both ends?

Use:

```python
deque
```

### Need frequency counts?

Use:

```python
Counter
```

### Need automatic default values?

Use:

```python
defaultdict
```

______________________________________________________________________

# 40. Common Collection Mistakes

## Mistake 1 — Using a list for repeated membership checks

Bad for large collections:

```python
for user_id in requested_ids:
    if user_id in all_user_ids:
        ...
```

If `all_user_ids` is a large list, each lookup may be `O(n)`.

Consider:

```python
all_user_ids = set(all_user_ids)
```

if uniqueness and hashable IDs make that appropriate.

______________________________________________________________________

## Mistake 2 — Using a list as a queue

Avoid repeated:

```python
items.pop(0)
```

Use:

```python
deque.popleft()
```

______________________________________________________________________

## Mistake 3 — Assuming dictionary lookup is always exactly O(1)

Dictionary lookup is typically O(1) on average, but hash-table behavior has implementation details and worst-case
considerations.

Interview answers should say "average-case O(1)" rather than absolute "always O(1)".

______________________________________________________________________

## Mistake 4 — Deep-copying everything

Deep copying can consume significant CPU and memory.

Use it intentionally.

______________________________________________________________________

## Mistake 5 — Assuming tuple means deeply immutable

A tuple is immutable as a container, but it can contain mutable objects.

Example:

```python
value = ([1, 2], 3)
```

You cannot replace the first tuple element, but the inner list can still change.

______________________________________________________________________

# 41. Backend Relevance

Collections are everywhere in backend applications.

### Request data

Dictionaries commonly represent structured JSON-like data.

### IDs and membership

Sets are useful for deduplication and membership checks.

### Ordered records

Lists are useful for result collections and sequences.

### Queues

`deque` can be useful for in-process queue-like structures.

### Aggregation

`Counter` and `defaultdict` simplify statistics and grouping.

### Configuration

Dictionaries are frequently used for configuration and lookup tables.

### Domain models

Dataclasses can provide structured representations instead of passing loosely structured dictionaries everywhere.

______________________________________________________________________

# 42. Interview Questions & Answers

## Q1. What is the difference between a list and a tuple?

**Answer:**

A list is mutable; a tuple is immutable.

Both are ordered sequences and support indexing.

Tuples are useful when the structure should not be modified and can also be used as dictionary keys when all contained
values are hashable.

______________________________________________________________________

## Q2. Why is list membership O(n)?

**Answer:**

A list generally needs to inspect elements sequentially until it finds a matching value or reaches the end.

Therefore membership is typically linear time.

______________________________________________________________________

## Q3. Why is set membership typically O(1)?

**Answer:**

Sets use hash tables.

For hashable values, the hash helps locate the relevant table position, giving average-case constant-time membership.

______________________________________________________________________

## Q4. Why is dictionary lookup typically O(1)?

**Answer:**

Dictionaries use hash tables.

A hash of the key is used to locate the corresponding entry, providing average-case constant-time lookup.

______________________________________________________________________

## Q5. Why can't a list be a dictionary key?

**Answer:**

A list is mutable and unhashable.

Dictionary keys need stable hash/equality behavior.

______________________________________________________________________

## Q6. Can a tuple be a dictionary key?

**Answer:**

Yes, if all of its elements are hashable.

For example:

```python
{(1, 2): "point"}
```

is valid.

But:

```python
{([1, 2], 3): "value"}
```

is invalid because the nested list is unhashable.

______________________________________________________________________

## Q7. What is the difference between `set` and `frozenset`?

**Answer:**

`set` is mutable.

`frozenset` is immutable and hashable when its elements are hashable.

A `frozenset` can therefore be used as a dictionary key or nested inside another set.

______________________________________________________________________

## Q8. Why would you use `deque` instead of a list?

**Answer:**

When you frequently add or remove items from both ends.

For example:

```python
deque.popleft()
```

is efficient, while `list.pop(0)` typically requires shifting elements.

______________________________________________________________________

## Q9. What is `defaultdict`?

**Answer:**

`defaultdict` is a dictionary subclass that creates a default value using a supplied factory when a missing key is
accessed.

Example:

```python
groups = defaultdict(list)
```

______________________________________________________________________

## Q10. What is `Counter`?

**Answer:**

`Counter` is a dictionary-like collection designed for counting hashable values.

It is useful for frequency analysis and aggregations.

______________________________________________________________________

## Q11. What is dictionary insertion ordering?

**Answer:**

Modern Python dictionaries preserve insertion order.

This means iteration follows the order in which keys were inserted.

It does not mean keys are sorted.

______________________________________________________________________

## Q12. What is the difference between `dict.get()` and `dict[key]`?

**Answer:**

`dict[key]` raises `KeyError` when the key is absent.

`dict.get(key)` returns `None` by default or a specified default value.

______________________________________________________________________

## Q13. What is a shallow copy?

**Answer:**

A shallow copy creates a new outer collection but keeps references to the same nested objects.

Therefore changes to nested mutable objects can be visible through both collections.

______________________________________________________________________

## Q14. What is a deep copy?

**Answer:**

`copy.deepcopy()` recursively copies nested objects where supported.

It provides more independence but can be expensive and is not always necessary.

______________________________________________________________________

## Q15. Why is `(10,)` different from `(10)`?

**Answer:**

The comma creates the tuple.

```python
(10)
```

is just the integer `10`.

```python
(10,)
```

is a one-element tuple.

______________________________________________________________________

## Q16. Are tuples deeply immutable?

**Answer:**

No.

The tuple structure is immutable, but it can contain mutable objects.

Example:

```python
value = ([1, 2],)
```

The list inside can still be modified.

______________________________________________________________________

## Q17. When would you use a dictionary instead of a list of objects?

**Answer:**

When fast lookup by a key is the dominant operation.

For example, if users are frequently retrieved by ID, a dictionary keyed by ID can be much more efficient than scanning
a list.

______________________________________________________________________

## Q18. When would you use a set?

**Answer:**

When you need uniqueness and/or efficient membership checks.

Examples include:

- Deduplicating IDs
- Permission checks
- Comparing groups
- Tracking visited nodes

______________________________________________________________________

## Q19. Why can converting a list to a set change behavior?

**Answer:**

A set removes duplicates and does not provide list-style positional indexing.

Therefore converting to a set is appropriate only when those semantics are acceptable.

______________________________________________________________________

## Q20. What is the difference between `defaultdict` and `setdefault()`?

**Answer:**

Both can initialize missing dictionary values.

`defaultdict` defines a default factory at the collection level.

`setdefault()` performs initialization for individual key accesses.

`defaultdict` is often clearer when automatic initialization is consistently desired.

______________________________________________________________________

# 43. Scenario-Based Questions

## Scenario 1 — Slow Membership Checks

You receive 500,000 requested IDs and repeatedly check whether each exists in another large list.

**Question:** What would you consider?

**Answer:**

If order and duplicates are not required for the lookup collection, convert it to a set:

```python
existing_ids = set(existing_ids)
```

Membership then becomes average-case `O(1)` rather than list membership's `O(n)`.

______________________________________________________________________

## Scenario 2 — Queue Performance

A worker uses:

```python
tasks = []

tasks.append(task)

task = tasks.pop(0)
```

The queue becomes slow as it grows.

**Question:** What would you change?

**Answer:**

Use:

```python
from collections import deque

tasks = deque()

tasks.append(task)
task = tasks.popleft()
```

A deque is designed for efficient operations at both ends.

______________________________________________________________________

## Scenario 3 — Nested Data Accidentally Changes

A developer writes:

```python
copy = original.copy()
```

and modifies a nested list through `copy`.

The original also changes.

**Question:** Why?

**Answer:**

`.copy()` performs a shallow copy.

The outer list is new, but nested mutable objects are shared.

Use an appropriate deep copy or explicitly construct independent nested objects.

______________________________________________________________________

## Scenario 4 — Using a Set Breaks Output

A developer converts:

```python
users = ["Alice", "Bob", "Alice"]
```

to:

```python
users = set(users)
```

to improve lookup.

Later the API expects duplicates and sequence semantics.

**Question:** What went wrong?

**Answer:**

The conversion changed the data's semantics.

A set removes duplicates and should not be used when multiplicity/order matters.

A separate set can be maintained for lookup while retaining the original list if both semantics are required.

______________________________________________________________________

## Scenario 5 — Configuration Lookup

A service repeatedly retrieves configuration by environment name:

```python
for environment in requested_environments:
    find_config(environment)
```

The implementation scans a list every time.

**Question:** What structure could improve this?

**Answer:**

Build a dictionary keyed by environment:

```python
configs_by_env = {
    config.name: config
    for config in configs
}
```

Then:

```python
configs_by_env[environment]
```

provides average-case constant-time lookup.

______________________________________________________________________

# 44. Practice Exercises

## Exercise 1 — Collection Selection

For each requirement, choose the appropriate collection and explain why:

1. Unique user IDs
1. Ordered API response items
1. Immutable `(latitude, longitude)` pair
1. Lookup user by ID
1. Queue with frequent left-side removal
1. Count HTTP status codes

______________________________________________________________________

## Exercise 2 — Membership Optimization

Given:

```python
existing_ids = [...]
requested_ids = [...]
```

write a solution that efficiently determines which requested IDs do not exist.

Explain the time-complexity difference between using a list and a set for membership.

______________________________________________________________________

## Exercise 3 — Grouping

Given:

```python
users = [
    {"name": "Alice", "role": "admin"},
    {"name": "Bob", "role": "user"},
    {"name": "Carol", "role": "admin"},
]
```

Use `defaultdict` to produce:

```python
{
    "admin": ["Alice", "Carol"],
    "user": ["Bob"],
}
```

______________________________________________________________________

## Exercise 4 — Counting

Given a list of HTTP status codes:

```python
statuses = [200, 200, 404, 500, 200, 404]
```

use `Counter` to find:

- Total count of each status.
- Two most common statuses.

______________________________________________________________________

## Exercise 5 — Queue

Implement a simple task queue using `deque`.

Requirements:

- Add tasks to the right.
- Process tasks from the left.
- Demonstrate why a list with `pop(0)` is less appropriate.

______________________________________________________________________

## Exercise 6 — Shallow Copy

Create:

```python
original = [[1, 2], [3, 4]]
```

Create a shallow copy and demonstrate how modifying a nested list affects both objects.

Then create a deep copy and compare the behavior.

______________________________________________________________________

## Exercise 7 — Dictionary Transformation

Given a list of user objects, create a dictionary keyed by user ID.

Explain why this structure is useful when the application frequently retrieves users by ID.

______________________________________________________________________

# 45. Quick Revision

| Concept | Key Point |
|---|---|
| `list` | Mutable ordered sequence |
| `tuple` | Immutable ordered sequence |
| `set` | Unique hashable values |
| `frozenset` | Immutable set |
| `dict` | Key-value mapping |
| List indexing | Typically O(1) |
| List membership | Typically O(n) |
| List append | O(1) amortized |
| List front insert/remove | Typically O(n) |
| Set membership | O(1) average |
| Dict lookup | O(1) average |
| Hashable | Can participate in stable hashing |
| `Counter` | Frequency counting |
| `defaultdict` | Automatic missing-key defaults |
| `deque` | Efficient operations at both ends |
| `OrderedDict` | Specialized ordered mapping behavior |
| `namedtuple` | Tuple with named fields |
| Dataclass | Flexible structured application model |
| Shallow copy | New outer object, shared nested references |
| Deep copy | Recursively copies nested objects |
| Dict ordering | Insertion order, not sorting |

______________________________________________________________________

# 46. Completion Checklist

Before moving to File 6, make sure you can explain:

- [ ] List vs tuple
- [ ] Set vs frozenset
- [ ] Dictionary fundamentals
- [ ] Mutability
- [ ] Hashability
- [ ] Dictionary keys
- [ ] List indexing
- [ ] List slicing
- [ ] List append
- [ ] List insert
- [ ] List removal
- [ ] List membership complexity
- [ ] Set membership complexity
- [ ] Dictionary lookup complexity
- [ ] Set operations
- [ ] Dictionary ordering
- [ ] Dictionary views
- [ ] `get()`
- [ ] `setdefault()`
- [ ] Dictionary comprehensions
- [ ] Dictionary merging
- [ ] `Counter`
- [ ] `defaultdict`
- [ ] `deque`
- [ ] `OrderedDict`
- [ ] `namedtuple`
- [ ] Dataclass vs namedtuple
- [ ] Shallow copy
- [ ] Deep copy
- [ ] Collection complexity
- [ ] Choosing collections for backend workloads
- [ ] Common collection performance mistakes

______________________________________________________________________

# 47. Interview Readiness Test

Without looking at the notes, answer these aloud:

1. What is the difference between a list and a tuple?
1. Why is list membership O(n)?
1. Why is set membership typically O(1)?
1. Why is dictionary lookup typically O(1)?
1. What does hashable mean?
1. Why can't a list be a dictionary key?
1. Can a tuple be a dictionary key?
1. What is the difference between `set` and `frozenset`?
1. Why would you use `deque` instead of a list?
1. What is `defaultdict`?
1. What is `Counter`?
1. What is the difference between `dict.get()` and `dict[key]`?
1. Does a dictionary preserve insertion order?
1. Is insertion order the same as sorted order?
1. What is a shallow copy?
1. What is a deep copy?
1. Are tuples deeply immutable?
1. When would you choose a set over a list?
1. How would you optimize repeated membership checks over a large collection?
1. How would you design an efficient in-memory lookup by user ID?
1. When would you use `deque`?
1. When would you prefer a dataclass over a `namedtuple`?

If you can answer these clearly and implement the exercises without relying heavily on the notes, this chapter is
complete.

______________________________________________________________________

**Previous:** [4. Iterators, Generators & Lazy Evaluation](./04-python-iterators-generators.md)

**Next:** [6. Exception Handling & Error Management](./06-python-exceptions.md)

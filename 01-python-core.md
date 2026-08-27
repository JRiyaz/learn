# 1. Python Runtime, Objects, Memory & Scope

**Previous:** [00. Course Index](./00-index.md)

**Next:** [2. Functions & Functional Programming](./02-python-functions.md)

______________________________________________________________________

## Objectives

By the end of this chapter, you should be able to:

- Explain Python's object and reference model.
- Distinguish identity, equality, mutability, and hashability.
- Explain Python's practical memory-management model.
- Explain reference counting and cyclic garbage collection in CPython.
- Understand shallow vs deep copying.
- Explain Python's LEGB name-resolution rule.
- Understand `global` and `nonlocal`.
- Understand namespaces and name binding.
- Identify common Python interview traps.
- Discuss these topics at the depth expected from a 5+ year Python backend engineer.

______________________________________________________________________

# 1. Python Runtime & Execution Model

Python is a high-level programming language. For backend interviews, distinguish the language from its common
implementation.

### Python

Python is the programming language and its language semantics.

### CPython

CPython is the most widely used implementation of Python. It is primarily written in C.

### Bytecode

CPython commonly compiles Python source into bytecode before executing it.

A simplified model is:

```text
Python source
    ↓
Parsing / compilation
    ↓
Bytecode
    ↓
Python runtime
    ↓
Objects and operations
```

You do not need to memorize CPython's C source code. Focus on runtime concepts that affect application behavior.

______________________________________________________________________

# 2. Python's Object Model

## 2.1 Everything is an object

Python represents values and many runtime entities as objects.

Examples:

```python
42
"hello"
[1, 2, 3]
{"name": "Riyaz"}
None
True
```

Functions are objects:

```python
def greet():
    return "hello"
```

Classes are also objects:

```python
class User:
    pass
```

This object model enables:

- First-class functions
- Decorators
- Callbacks
- Higher-order functions
- Dynamic behavior

______________________________________________________________________

## 2.2 Identity, type and value

An object can be thought of as having three important characteristics:

### Identity

Identifies the object during its lifetime.

```python
id(obj)
```

### Type

Describes what kind of object it is.

```python
type(obj)
```

### Value

Represents the object's data.

```python
age = 30

print(id(age))
print(type(age))
print(age)
```

______________________________________________________________________

# 3. Names and References

A better Python mental model is:

> A name is bound to an object.

Example:

```python
x = 10
y = x
```

Both names can refer to the same object.

This becomes especially important with mutable objects:

```python
items = [1, 2]
other = items

other.append(3)

print(items)
```

Output:

```python
[1, 2, 3]
```

`other` did not create another list. It became another reference to the same list.

______________________________________________________________________

# 4. Assignment Does Not Mean Copying

Consider:

```python
a = [1, 2, 3]
b = a
```

This does not create an independent list.

Conceptually:

```text
a ──┐
    ├──> [1, 2, 3]
b ──┘
```

Therefore:

```python
b.append(4)

print(a)
```

produces:

```python
[1, 2, 3, 4]
```

If independent state is required, use an appropriate copy or reconstruction strategy.

______________________________________________________________________

# 5. Identity vs Equality

## Equality: `==`

Asks:

> Do these objects compare as equal?

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)
```

Output:

```text
True
```

## Identity: `is`

Asks:

> Are these the same object?

```python
print(a is b)
```

Output:

```text
False
```

The lists contain equal values but are different objects.

______________________________________________________________________

# 6. Why `is None` Is Preferred

Use:

```python
if value is None:
    ...
```

instead of:

```python
if value == None:
    ...
```

The first explicitly checks identity against the `None` singleton and avoids relying on customized equality behavior.

______________________________________________________________________

# 7. `id()`

Python exposes object identity through:

```python
id(obj)
```

Example:

```python
a = []
b = a

print(id(a))
print(id(b))
```

The values will be the same because both names refer to the same object.

Do not write portable application logic that assumes `id()` is a memory address. Its exact representation is
implementation-dependent.

______________________________________________________________________

# 8. Mutable vs Immutable Objects

## Mutable

A mutable object can be changed in place.

Common examples:

- `list`
- `dict`
- `set`
- `bytearray`

Example:

```python
items = [1, 2]
items.append(3)
```

The existing list was modified.

## Immutable

An immutable object cannot be changed in place after creation.

Common examples:

- `int`
- `float`
- `bool`
- `str`
- `tuple`
- `bytes`
- `frozenset`

Example:

```python
x = 10
x += 1
```

The integer representing `10` is not modified. The name is rebound to the resulting value.

______________________________________________________________________

# 9. Immutability and Nested Objects

A tuple is immutable in its structure, but it can contain mutable objects.

```python
data = ([1, 2], 10)
```

This is not allowed:

```python
data[0] = [3, 4]
```

But this is allowed:

```python
data[0].append(3)
```

The tuple remains structurally unchanged while the nested list changes.

______________________________________________________________________

# 10. Why Mutability Matters in Backend Systems

Mutable objects are useful, but shared mutable state can create bugs.

```python
config = {
    "allowed_roles": ["admin", "user"]
}

service_config = config

service_config["allowed_roles"].append("operator")
```

Now `config` has also changed.

This matters in:

- Request handling
- Configuration
- Caches
- ORM objects
- Shared application state
- Concurrent applications

A senior engineer should consider **who owns an object and who is allowed to mutate it**.

______________________________________________________________________

# 11. Hashability

Dictionaries and sets use hashing.

Dictionary keys must be hashable.

This works:

```python
hash("alice")
```

This fails:

```python
hash([1, 2, 3])
```

because lists are unhashable.

Common hashable types include:

- `int`
- `str`
- `bytes`
- `tuple` containing only hashable values
- `frozenset`

Common unhashable types include:

- `list`
- `dict`
- `set`

______________________________________________________________________

# 12. Hashability and Mutability

Mutable objects are generally unsuitable as hash keys because their state can change.

The important interview rule is:

> Dictionary keys and set elements must be hashable.

For custom classes, equality and hashing must also be designed consistently.

If two hashable objects compare equal:

```python
a == b
```

they must have compatible hashes:

```python
hash(a) == hash(b)
```

The reverse is not guaranteed because hash collisions are possible.

______________________________________________________________________

# 13. Python Memory Management

Python manages object memory automatically.

For **CPython**, two important mechanisms are:

1. Reference counting
1. Cyclic garbage collection

A strong interview answer is:

> CPython primarily uses reference counting for object lifetime management and supplements it with cyclic garbage collection to handle unreachable reference cycles.

This is an implementation detail of CPython, not a universal rule for every Python implementation.

______________________________________________________________________

# 14. Reference Counting in CPython

CPython keeps track of references to objects.

Example:

```python
a = []
b = a
```

The list has multiple references.

When:

```python
del a
```

one reference is removed.

When the object is no longer referenced, CPython can generally reclaim it immediately.

______________________________________________________________________

# 15. Reference Cycles

Reference counting alone cannot reclaim a cycle.

Example:

```python
a = []
b = []

a.append(b)
b.append(a)
```

Conceptually:

```text
a → b
↑   ↓
└───┘
```

If the objects become unreachable from the rest of the program, CPython's cyclic garbage collector can detect and
reclaim the cycle.

______________________________________________________________________

# 16. Reference Counting vs Cyclic Garbage Collection

### Reference counting

Tracks references to objects.

When an object's reference count reaches zero, it can generally be reclaimed immediately in CPython.

### Cyclic garbage collection

Handles unreachable groups of objects that reference one another.

A concise interview answer:

> Reference counting handles most object-lifetime cases in CPython, while cyclic garbage collection handles unreachable reference cycles.

______________________________________________________________________

# 17. What Does `del` Actually Do?

Consider:

```python
a = [1, 2, 3]
b = a

del a
```

`del a` removes the name `a`.

It does not necessarily destroy the list because `b` still references it.

A good mental model is:

> `del` removes a binding/reference; it does not mean "force object destruction."

______________________________________________________________________

# 18. Object Lifetime

Consider:

```python
def create_user():
    user = {
        "name": "Riyaz"
    }

    return user
```

The local name `user` disappears after the function returns.

But the dictionary remains alive if the caller stores the returned object:

```python
user = create_user()
```

Object lifetime depends on reachability and the runtime's memory-management behavior.

______________________________________________________________________

# 19. Shallow Copy

A shallow copy creates a new outer object but keeps references to nested objects.

```python
import copy

original = [
    [1, 2],
    [3, 4],
]

shallow = copy.copy(original)

shallow[0].append(99)
```

The nested list is shared, so the change is visible through `original` too.

______________________________________________________________________

# 20. Common Shallow-Copy Techniques

Depending on the object:

```python
copy.copy(obj)
```

For lists:

```python
items.copy()
items[:]
```

For dictionaries:

```python
data.copy()
```

These generally create a new outer container while retaining references to nested objects.

______________________________________________________________________

# 21. Deep Copy

`copy.deepcopy()` recursively copies nested objects where applicable.

```python
import copy

original = [
    [1, 2],
    [3, 4],
]

clone = copy.deepcopy(original)

clone[0].append(99)

print(original)
print(clone)
```

For this example, the nested structures are independent.

However, deep copying can be:

- Expensive
- Memory-intensive
- Difficult with complex object graphs
- Inappropriate for objects representing external resources or shared state

Use it intentionally.

______________________________________________________________________

# 22. Scope in Python

Python name resolution is commonly described using **LEGB**:

1. Local
1. Enclosing
1. Global
1. Built-in

Example:

```python
value = "global"

def outer():
    value = "enclosing"

    def inner():
        value = "local"
        print(value)

    inner()

outer()
```

Output:

```text
local
```

Python finds the nearest applicable binding.

______________________________________________________________________

# 23. Local Scope

Variables assigned inside a function are normally local to that function.

```python
def process():
    value = 10
    print(value)
```

The local `value` does not automatically become a module-level variable.

______________________________________________________________________

# 24. Enclosing Scope

Nested functions can access variables from an enclosing function.

```python
def outer():
    value = 10

    def inner():
        print(value)

    inner()
```

`inner()` finds `value` in the enclosing scope.

Closures are covered more deeply in the functions/decorators chapters.

______________________________________________________________________

# 25. Global Scope

A module-level name belongs to the module's global namespace.

```python
counter = 0

def show():
    print(counter)
```

The function can read the global value because no nearer binding exists.

Assignment requires special attention.

______________________________________________________________________

# 26. Why `counter += 1` Can Raise `UnboundLocalError`

Consider:

```python
counter = 0

def increment():
    counter += 1
```

This raises:

```text
UnboundLocalError
```

Assignment causes Python to treat `counter` as local to the function.

The function therefore tries to read the local `counter` before it has been initialized.

______________________________________________________________________

# 27. `global`

You can explicitly refer to the module-level binding:

```python
counter = 0

def increment():
    global counter
    counter += 1
```

This works.

However, global mutable state should generally be minimized in backend applications because it can make testing,
concurrency reasoning, and state ownership harder.

______________________________________________________________________

# 28. `nonlocal`

`nonlocal` allows a nested function to modify a variable from an enclosing function.

```python
def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment
```

Usage:

```python
counter = make_counter()

print(counter())
print(counter())
```

Output:

```text
1
2
```

The deeper mechanics of closures are covered in later Python function/decorator material.

______________________________________________________________________

# 29. Namespaces

A namespace maps names to objects.

Important namespaces include:

- Local namespace
- Enclosing namespace
- Global/module namespace
- Class namespace
- Built-in namespace

You can inspect namespaces with:

```python
globals()
locals()
```

These are useful for understanding/debugging but are not normally needed in application code.

______________________________________________________________________

# 30. Shadowing Built-ins

Python allows a local or global name to shadow a built-in.

For example:

```python
len = 100
```

Now:

```python
len([1, 2, 3])
```

will fail because `len` refers to the integer rather than the built-in function.

Avoid using important built-in names as variables:

```text
list
dict
str
id
type
len
sum
set
```

______________________________________________________________________

# 31. Common Python Traps

## Trap 1 — `is` vs `==`

`is` is not a faster version of `==`.

- `==` checks equality.
- `is` checks identity.

______________________________________________________________________

## Trap 2 — Mutable Default Arguments

Avoid:

```python
def add_item(item, items=[]):
    items.append(item)
    return items
```

The default list is created once when the function is defined.

Prefer:

```python
def add_item(item, items=None):
    if items is None:
        items = []

    items.append(item)
    return items
```

______________________________________________________________________

## Trap 3 — Aliasing

```python
a = []
b = a
```

Both names reference the same list.

______________________________________________________________________

## Trap 4 — Tuple Immutability

A tuple cannot change its element references, but an object inside it may be mutable.

______________________________________________________________________

## Trap 5 — `del` Does Not Mean "Free This Object"

`del` removes a binding/reference. Other references can keep the object alive.

______________________________________________________________________

## Trap 6 — Immutability Does Not Mean Deep Immutability

A tuple can contain a mutable list.

______________________________________________________________________

# 32. Backend Relevance

These concepts directly affect backend engineering.

### Object references

Help diagnose:

- Unexpected mutations
- Shared state
- Incorrect copying
- Request-data bugs

### Hashability

Important for:

- Cache keys
- Deduplication
- Dictionaries
- Sets
- In-memory indexes

### Memory management

Important when diagnosing:

- Worker memory growth
- Large payloads
- Unbounded caches
- Object retention
- Long-running service behavior

### Scope

Important for:

- Configuration
- Dependency factories
- Closures
- Testing
- Application state

### Copying

Important when:

- Modifying nested configuration
- Processing request data
- Creating derived objects
- Avoiding shared mutable state

______________________________________________________________________

# 33. Interview Questions & Answers

## Q1. What is the difference between a variable and an object in Python?

**Answer:**

A variable is better understood as a name bound to an object.

The object has an identity, type, and value. Multiple names can reference the same object.

```python
a = [1, 2]
b = a
```

Here `a` and `b` reference the same list.

______________________________________________________________________

## Q2. What is the difference between `is` and `==`?

**Answer:**

`==` checks equality, while `is` checks identity.

```python
a = [1, 2]
b = [1, 2]

a == b  # True
a is b  # False
```

Use `is` when identity is what matters, especially:

```python
value is None
```

______________________________________________________________________

## Q3. Why is `is None` preferred over `== None`?

**Answer:**

`None` is a singleton and the intention is to check whether the object is that singleton.

```python
if value is None:
    ...
```

It also avoids relying on custom equality behavior.

______________________________________________________________________

## Q4. What is mutable vs immutable in Python?

**Answer:**

Mutable objects can be changed in place. Immutable objects cannot be changed in place after creation.

Examples:

```text
Mutable:   list, dict, set
Immutable: int, str, tuple, bytes
```

______________________________________________________________________

## Q5. Is a tuple completely immutable?

**Answer:**

The tuple's structure is immutable, but objects referenced by its elements may be mutable.

```python
value = ([1, 2], 10)

value[0].append(3)
```

The tuple was not structurally modified; the nested list was.

______________________________________________________________________

## Q6. Why can't a list normally be a dictionary key?

**Answer:**

Dictionary keys must be hashable. Lists are mutable and therefore unhashable.

A tuple can be a key if every object inside it is hashable.

______________________________________________________________________

## Q7. What is hashability?

**Answer:**

Hashability means an object can provide a stable hash value and equality behavior suitable for use in hash-based
collections such as dictionaries and sets.

If two hashable objects compare equal, they must have equal hashes.

______________________________________________________________________

## Q8. Explain Python memory management.

**Answer:**

Memory management is implementation-dependent.

For CPython, reference counting is the primary object-lifetime mechanism, supplemented by cyclic garbage collection for
unreachable reference cycles.

______________________________________________________________________

## Q9. What is reference counting?

**Answer:**

CPython tracks references to objects. When an object's reference count reaches zero, the object can generally be
reclaimed immediately.

Reference counting alone cannot handle unreachable reference cycles.

______________________________________________________________________

## Q10. What is a reference cycle?

**Answer:**

A reference cycle occurs when objects reference one another in a cycle.

```python
a = []
b = []

a.append(b)
b.append(a)
```

If the objects become unreachable, cyclic garbage collection can identify the cycle and reclaim it.

______________________________________________________________________

## Q11. What does `del` do?

**Answer:**

`del` removes a name binding or reference.

```python
a = []
b = a

del a
```

The list remains alive because `b` still references it.

______________________________________________________________________

## Q12. What is shallow copy vs deep copy?

**Answer:**

A shallow copy creates a new outer object while retaining references to nested objects.

A deep copy recursively copies nested objects where applicable.

```python
import copy

shallow = copy.copy(original)
deep = copy.deepcopy(original)
```

Deep copy can be expensive and is not always appropriate.

______________________________________________________________________

## Q13. Explain LEGB.

**Answer:**

LEGB describes the usual name lookup order:

1. Local
1. Enclosing
1. Global
1. Built-in

Python searches the nearest applicable binding first.

______________________________________________________________________

## Q14. Why can `counter += 1` raise `UnboundLocalError`?

**Answer:**

Because assignment makes Python treat `counter` as local within that function.

```python
counter = 0

def increment():
    counter += 1
```

The function attempts to read its local `counter` before assigning a value to it.

______________________________________________________________________

## Q15. What is the difference between `global` and `nonlocal`?

**Answer:**

`global` refers to a module-level binding.

`nonlocal` refers to a binding in an enclosing function scope.

Use them deliberately because hidden shared state can make backend code harder to reason about.

______________________________________________________________________

## Q16. Why can shared mutable state be dangerous in backend applications?

**Answer:**

Multiple requests, threads, or tasks may observe or modify the same object.

This can cause:

- Unexpected state changes
- Race conditions
- Test pollution
- Request-to-request data leakage
- Difficult debugging

Explicit state ownership is usually safer.

______________________________________________________________________

## Q17. What is aliasing?

**Answer:**

Aliasing occurs when multiple names reference the same object.

```python
a = []
b = a
```

A mutation through `b` is visible through `a`.

______________________________________________________________________

## Q18. What happens when you execute `x += 1` for an integer?

**Answer:**

Integers are immutable. The integer object itself is not modified in place.

The operation produces a resulting value and the name is rebound accordingly.

______________________________________________________________________

## Q19. Does Python always use reference counting?

**Answer:**

No. Reference counting is a CPython implementation detail.

Other Python implementations can use different memory-management strategies.

______________________________________________________________________

## Q20. Why shouldn't application code depend on `id()` values?

**Answer:**

`id()` provides object identity, but its exact representation is implementation-dependent.

Code should use identity checks when necessary rather than assuming `id()` represents a stable memory address.

______________________________________________________________________

## Q21. Can an immutable object contain mutable data?

**Answer:**

Yes.

```python
data = ([1, 2], 10)
```

The tuple is immutable, but its first element is a mutable list.

______________________________________________________________________

## Q22. Why is deep copying not always the best solution to shared-state problems?

**Answer:**

Deep copying can consume significant CPU and memory and may not have the desired semantics for complex objects.

It is often better to explicitly construct the data required by the new operation or use immutable/shared structures
appropriately.

______________________________________________________________________

# 34. Scenario-Based Questions

## Scenario 1 — Unexpected Configuration Change

```python
config = {
    "roles": ["admin", "user"]
}

request_config = config

request_config["roles"].append("operator")
```

**Question:** Why did the original configuration change?

**Answer:**

`request_config` and `config` reference the same dictionary, and the nested list is also shared.

This is an aliasing problem.

______________________________________________________________________

## Scenario 2 — Memory Usage Keeps Growing

A long-running Python worker's memory usage continuously increases.

**Question:** Would you immediately blame garbage collection?

**Answer:**

No.

Investigate:

- Retained references
- Global state
- Unbounded collections
- Caches
- Large request objects
- Object lifetimes
- Reference cycles
- ORM/session lifetime
- Native allocations
- Worker recycling behavior

Garbage collection is only one part of the investigation.

______________________________________________________________________

## Scenario 3 — Two Requests Affect Each Other

An API receives two independent requests, but modifying a nested object during request A changes what request B sees.

**Question:** What would you investigate first?

**Answer:**

Investigate whether both requests share an object.

Check:

- Global/module state
- Caches
- Singleton objects
- Aliasing
- Shallow copies
- Mutable defaults
- Shared configuration

Request-specific state should normally have request-specific ownership.

______________________________________________________________________

## Scenario 4 — Dictionary Key Error

```python
cache = {}

key = [1, 2, 3]

cache[key] = "value"
```

**Question:** What happens and why?

**Answer:**

Python raises `TypeError` because lists are unhashable and therefore cannot be dictionary keys.

If the data can safely be represented immutably, a tuple may work:

```python
key = (1, 2, 3)
```

______________________________________________________________________

## Scenario 5 — Production Bug Caused by Copying

A developer uses:

```python
new_config = old_config.copy()
```

and assumes the entire configuration is independent.

A nested dictionary is later modified and the original configuration changes too.

**Question:** Why?

**Answer:**

`.copy()` creates a shallow copy. The outer dictionary is new, but nested objects are still shared.

The correct solution depends on the required semantics:

- Explicit reconstruction
- Deep copy
- Immutable structures
- Dedicated configuration objects

______________________________________________________________________

# 35. Practice Exercises

## Exercise 1 — Identity vs Equality

Predict:

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)
print(a is b)
print(a is c)
```

Explain each result.

______________________________________________________________________

## Exercise 2 — Aliasing

Predict:

```python
a = {"items": []}
b = a

b["items"].append("python")

print(a)
print(b)
```

Explain why both values changed.

______________________________________________________________________

## Exercise 3 — Shallow Copy

Predict:

```python
import copy

a = [[1, 2], [3, 4]]
b = copy.copy(a)

b[0].append(99)

print(a)
print(b)
```

Then modify the code so the nested structures are independent.

______________________________________________________________________

## Exercise 4 — LEGB

Explain:

```python
value = "global"

def outer():
    value = "enclosing"

    def inner():
        value = "local"
        print(value)

    inner()

outer()
```

Then remove the local assignment and explain what changes.

______________________________________________________________________

## Exercise 5 — `nonlocal`

Implement:

```python
counter = make_counter()

print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

using a closure and `nonlocal`.

______________________________________________________________________

## Exercise 6 — Hashability

Determine which can be dictionary keys:

```python
42
"python"
(1, 2)
(1, [2, 3])
[1, 2]
frozenset({1, 2})
```

Explain every result.

______________________________________________________________________

# 36. Quick Revision

| Concept | Interview Mental Model |
|---|---|
| Python | Language/specification |
| CPython | Common Python implementation |
| Object | Has identity, type and value |
| Name | Bound to an object |
| `==` | Equality |
| `is` | Identity |
| `is None` | Standard singleton identity check |
| Mutable | Can change in place |
| Immutable | Cannot change in place |
| Hashable | Suitable for dict/set hashing |
| `del x` | Removes a binding/reference |
| Reference counting | Primary CPython lifetime mechanism |
| Cyclic GC | Handles unreachable reference cycles |
| Shallow copy | New outer object, shared nested references |
| Deep copy | Recursively copies nested objects where applicable |
| LEGB | Local → Enclosing → Global → Built-in |
| `global` | Module/global binding |
| `nonlocal` | Enclosing-function binding |
| Aliasing | Multiple names reference one object |
| Namespace | Mapping from names to objects |

______________________________________________________________________

# 37. Completion Checklist

Before moving to File 2, make sure you can explain:

- [ ] Python vs CPython
- [ ] Basic Python execution model
- [ ] Python object model
- [ ] Identity, type and value
- [ ] Names and references
- [ ] Assignment vs copying
- [ ] `id()`
- [ ] Identity vs equality
- [ ] `is` vs `==`
- [ ] Why `is None` is preferred
- [ ] Mutable vs immutable objects
- [ ] Nested mutable objects inside immutable containers
- [ ] Hashability
- [ ] Equality and hashing
- [ ] CPython reference counting
- [ ] Cyclic garbage collection
- [ ] Reference cycles
- [ ] `del`
- [ ] Object lifetime
- [ ] Shallow copy
- [ ] Deep copy
- [ ] LEGB
- [ ] Local scope
- [ ] Enclosing scope
- [ ] Global scope
- [ ] `global`
- [ ] `nonlocal`
- [ ] Namespaces
- [ ] Shadowing built-ins
- [ ] Aliasing
- [ ] Mutable default argument trap
- [ ] Backend implications of shared mutable state

______________________________________________________________________

# 38. Interview Readiness Test

Without looking at the notes, answer these aloud:

1. Explain Python's object/reference model in one minute.
1. What is the difference between Python and CPython?
1. Explain `is` vs `==` with an example.
1. Why is `is None` preferred?
1. Explain mutable vs immutable objects.
1. Can an immutable object contain mutable objects?
1. Why can't a list normally be a dictionary key?
1. Explain hashability.
1. How does memory management work in CPython?
1. Reference counting vs cyclic garbage collection?
1. What is a reference cycle?
1. What exactly does `del` do?
1. Explain shallow copy vs deep copy.
1. What is aliasing?
1. Explain LEGB.
1. Why does `counter += 1` sometimes cause `UnboundLocalError`?
1. What is the difference between `global` and `nonlocal`?
1. Why is shared mutable state dangerous in backend applications?
1. How would you investigate unexpected memory growth in a Python worker?
1. Why is `copy.copy()` sometimes insufficient?

If you can answer these clearly and explain the scenarios without looking at the notes, this chapter is complete.

______________________________________________________________________

**Previous:** [00. Course Index](./00-index.md)

**Next:** [2. Functions & Functional Programming](./02-python-functions.md)

# Collections Framework

The Java Collections Framework (JCF) is one of the most important topics in Java interviews.

Almost every coding interview, backend project, and Spring Boot application uses collections extensively.

If you understand the Collections Framework well, you'll write cleaner, faster, and more maintainable code.

This chapter focuses on:

- Choosing the right collection
- Internal working
- Time complexity
- Common interview questions
- Best practices

______________________________________________________________________

# Why Collections?

Suppose you want to store multiple employee names.

Without collections

```java
String emp1 = "Alice";
String emp2 = "Bob";
String emp3 = "Charlie";
```

Not scalable.

Instead

```java
List<String> employees = new ArrayList<>();

employees.add("Alice");
employees.add("Bob");
employees.add("Charlie");
```

Collections allow us to store, manipulate, search, sort, and process groups of objects efficiently.

______________________________________________________________________

# Collections Hierarchy

```
                Iterable
                    │
               Collection
          ┌─────────┼─────────┐
         List       Set      Queue
          │          │          │
   ArrayList    HashSet   PriorityQueue
   LinkedList   TreeSet   ArrayDeque
                LinkedHashSet
```

Separately,

```
Map
│
├── HashMap
├── LinkedHashMap
├── TreeMap
├── Hashtable
└── ConcurrentHashMap
```

Notice

**Map is NOT part of the Collection interface.**

Very common interview question.

______________________________________________________________________

# Collection vs Collections

These names confuse many developers.

## Collection

An interface.

```java
Collection<String> collection;
```

Represents a group of objects.

______________________________________________________________________

## Collections

A utility class.

```java
Collections.sort(list);

Collections.reverse(list);

Collections.shuffle(list);
```

Provides helper methods.

______________________________________________________________________

# Iterable

Every collection implements

```java
Iterable
```

That's why enhanced for-loops work.

```java
for(String name : employees){

    System.out.println(name);

}
```

______________________________________________________________________

# List

A List

- Maintains insertion order
- Allows duplicates
- Supports indexing

Example

```java
List<String> names = new ArrayList<>();

names.add("Alice");
names.add("Bob");
names.add("Alice");
```

Output

```
Alice
Bob
Alice
```

Duplicates are allowed.

______________________________________________________________________

# ArrayList

The most commonly used List implementation.

```java
List<String> list = new ArrayList<>();
```

______________________________________________________________________

# Internal Working

Internally,

ArrayList uses a **dynamic array**.

```
+----+----+----+----+
| A  | B  | C  |    |
+----+----+----+----+
```

When full,

Java creates a larger array and copies elements.

______________________________________________________________________

# Time Complexity

| Operation | Complexity |
|------------|-----------|
| get(index) | O(1) |
| add(end) | O(1) amortized |
| add(beginning) | O(n) |
| remove(beginning) | O(n) |
| search | O(n) |

______________________________________________________________________

# Example

```java
List<Integer> numbers = new ArrayList<>();

numbers.add(10);
numbers.add(20);
numbers.add(30);

System.out.println(numbers.get(1));
```

Output

```
20
```

______________________________________________________________________

# LinkedList

```java
List<String> list =
    new LinkedList<>();
```

Internally

```
Node

↓

Node

↓

Node
```

Each node stores

- Data
- Previous pointer
- Next pointer

(Doubly Linked List)

______________________________________________________________________

# Time Complexity

| Operation | Complexity |
|------------|-----------|
| get(index) | O(n) |
| insert beginning | O(1) |
| insert end | O(1) |
| delete beginning | O(1) |
| search | O(n) |

______________________________________________________________________

# ArrayList vs LinkedList

| Feature | ArrayList | LinkedList |
|----------|-----------|------------|
| Random Access | ⭐⭐⭐⭐⭐ | ⭐ |
| Insert Middle | Slow | Better |
| Memory Usage | Lower | Higher |
| Cache Friendly | Yes | No |

Use ArrayList unless you have a specific reason to use LinkedList.

______________________________________________________________________

# Set

A Set

- Doesn't allow duplicates
- Doesn't support indexing

Example

```java
Set<String> set = new HashSet<>();

set.add("Java");
set.add("Python");
set.add("Java");
```

Output

```
Java
Python
```

Duplicate ignored.

______________________________________________________________________

# HashSet

Most commonly used Set.

```java
Set<Integer> set =
    new HashSet<>();
```

Internally backed by a HashMap.

Order is **not guaranteed**.

______________________________________________________________________

# Time Complexity

| Operation | Complexity |
|------------|-----------|
| add | O(1) average |
| remove | O(1) average |
| contains | O(1) average |

______________________________________________________________________

# LinkedHashSet

Maintains insertion order.

```java
Set<String> set =
    new LinkedHashSet<>();
```

Output

```
Apple
Banana
Orange
```

Exactly the insertion order.

______________________________________________________________________

# TreeSet

Stores elements in sorted order.

```java
TreeSet<Integer> numbers =
    new TreeSet<>();

numbers.add(30);
numbers.add(10);
numbers.add(20);
```

Output

```
10
20
30
```

Internally uses a Red-Black Tree.

______________________________________________________________________

# TreeSet Complexity

| Operation | Complexity |
|------------|-----------|
| add | O(log n) |
| remove | O(log n) |
| contains | O(log n) |

______________________________________________________________________

# Queue

Queue follows

```
FIFO

First In

First Out
```

Example

```java
Queue<String> queue =
    new LinkedList<>();

queue.offer("A");
queue.offer("B");
queue.offer("C");

System.out.println(queue.poll());
```

Output

```
A
```

______________________________________________________________________

# Queue Methods

Add

```java
offer()
```

Remove

```java
poll()
```

Peek

```java
peek()
```

______________________________________________________________________

# PriorityQueue

Elements ordered by priority.

```java
PriorityQueue<Integer> pq =
    new PriorityQueue<>();

pq.add(30);
pq.add(10);
pq.add(20);
```

Output

```
10
20
30
```

Internally implemented using a Binary Heap.

______________________________________________________________________

# Deque

Double-ended queue.

```java
Deque<Integer> deque =
    new ArrayDeque<>();
```

Supports insertion and removal from both ends.

Useful for:

- Stack
- Queue
- Sliding Window problems
- BFS

______________________________________________________________________

# Why ArrayDeque Over Stack?

Legacy

```java
Stack<Integer>
```

Modern

```java
Deque<Integer> stack =
    new ArrayDeque<>();
```

Preferred because it is faster and not synchronized.

______________________________________________________________________

# Map

A Map stores

```
Key

↓

Value
```

Example

```java
Map<Integer,String> employees =
    new HashMap<>();

employees.put(1,"Alice");
employees.put(2,"Bob");
```

Retrieve

```java
employees.get(1);
```

Output

```
Alice
```

______________________________________________________________________

# HashMap

Most important collection in Java.

```java
Map<String,Integer> map =
    new HashMap<>();
```

______________________________________________________________________

# Internal Working (High Level)

A HashMap stores entries in buckets.

```
Key

↓

hashCode()

↓

Bucket

↓

Entry
```

If two keys map to the same bucket,

a collision occurs.

______________________________________________________________________

# Hash Collision

```
Bucket

↓

Entry1

↓

Entry2

↓

Entry3
```

Java handles collisions internally.

(Java 8 may convert long chains into balanced trees.)

______________________________________________________________________

# HashMap Complexity

| Operation | Complexity |
|------------|-----------|
| put | O(1) average |
| get | O(1) average |
| remove | O(1) average |

Worst case

```
O(n)
```

Though uncommon with good hash functions.

______________________________________________________________________

# LinkedHashMap

Maintains insertion order.

```java
Map<Integer,String> map =
    new LinkedHashMap<>();
```

Useful for

- LRU Cache
- Ordered iteration

______________________________________________________________________

# TreeMap

Automatically sorts keys.

```java
TreeMap<Integer,String> map =
    new TreeMap<>();
```

Output

```
Sorted by key
```

Internally

Red-Black Tree.

Complexity

```
O(log n)
```

______________________________________________________________________

# ConcurrentHashMap

Thread-safe HashMap.

```java
ConcurrentHashMap<Integer,String> map =
    new ConcurrentHashMap<>();
```

Designed for concurrent access with better performance than `Hashtable`.

Commonly used in multi-threaded applications.

______________________________________________________________________

# Hashtable

Older synchronized implementation.

```java
Hashtable<Integer,String> table =
    new Hashtable<>();
```

Rarely used in modern applications.

Prefer `ConcurrentHashMap`.

______________________________________________________________________

# equals() and hashCode()

Extremely important.

Suppose

```java
Employee e1 = new Employee(1);

Employee e2 = new Employee(1);
```

Without overriding

```java
equals()
```

and

```java
hashCode()
```

HashSet and HashMap may treat them as different objects even though they represent the same employee.

Whenever you override `equals()`, you **must** also override `hashCode()`.

We'll cover this topic in greater detail in a later chapter.

______________________________________________________________________

# Iterating Over Collections

Using enhanced for-loop

```java
for(String name : names){

    System.out.println(name);

}
```

______________________________________________________________________

Using Iterator

```java
Iterator<String> iterator =
    names.iterator();

while(iterator.hasNext()){

    System.out.println(iterator.next());

}
```

Use an `Iterator` when removing elements during iteration.

______________________________________________________________________

# Common Utility Methods

Sorting

```java
Collections.sort(list);
```

Reverse

```java
Collections.reverse(list);
```

Shuffle

```java
Collections.shuffle(list);
```

Binary Search

```java
Collections.binarySearch(list, 10);
```

Minimum

```java
Collections.min(list);
```

Maximum

```java
Collections.max(list);
```

______________________________________________________________________

# Choosing the Right Collection

| Requirement | Collection |
|-------------|------------|
| Ordered list | ArrayList |
| Frequent insert/delete at ends | LinkedList |
| Unique values | HashSet |
| Sorted unique values | TreeSet |
| FIFO | Queue |
| Priority-based processing | PriorityQueue |
| Key-value lookup | HashMap |
| Ordered map | LinkedHashMap |
| Sorted keys | TreeMap |
| Concurrent key-value store | ConcurrentHashMap |

______________________________________________________________________

# Common Mistakes

## Using LinkedList Everywhere

Most applications perform better with `ArrayList`.

______________________________________________________________________

## Using TreeMap for Fast Lookups

Need fast lookup?

Use `HashMap`.

______________________________________________________________________

## Forgetting equals() and hashCode()

Collections relying on hashing need both methods implemented correctly.

______________________________________________________________________

## Using Stack

Prefer

```java
ArrayDeque
```

______________________________________________________________________

## Depending on HashMap Iteration Order

Never assume `HashMap` preserves insertion order.

Use `LinkedHashMap` if order matters.

______________________________________________________________________

# Best Practices

✅ Program to interfaces (`List`, `Set`, `Map`).

✅ Prefer `ArrayList` over `LinkedList`.

✅ Use `HashMap` for most key-value storage.

✅ Use `TreeMap` only when sorted keys are required.

✅ Use `HashSet` for uniqueness.

✅ Prefer `ArrayDeque` over `Stack`.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between ArrayList and LinkedList?

### Answer

`ArrayList` is backed by a dynamic array, providing O(1) random access and excellent cache locality. It is the preferred
choice for most applications.

`LinkedList` is backed by a doubly linked list, making insertions and deletions at the ends efficient, but random access
is O(n). It also has higher memory overhead due to node references.

______________________________________________________________________

## Question

What is the difference between HashMap and TreeMap?

### Answer

`HashMap` stores entries using hashing and provides average O(1) lookup, insertion, and removal. It does not maintain
any ordering.

`TreeMap` stores entries in a Red-Black Tree, maintaining keys in sorted order. Operations such as `put`, `get`, and
`remove` take O(log n) time.

______________________________________________________________________

## Question

Why is HashMap faster than TreeMap?

### Answer

`HashMap` uses hashing to locate entries directly in buckets, giving average O(1) performance.

`TreeMap` uses a balanced binary search tree, requiring O(log n) traversal for lookups and updates.

______________________________________________________________________

## Question

Why should we program to `List` instead of `ArrayList`?

### Answer

Programming to the `List` interface reduces coupling and makes it easy to switch implementations, such as replacing
`ArrayList` with `LinkedList`, without changing client code.

______________________________________________________________________

## Question

Why are `equals()` and `hashCode()` important?

### Answer

Hash-based collections like `HashMap` and `HashSet` rely on `hashCode()` to determine the bucket where an object belongs
and `equals()` to determine object equality within that bucket. Failing to override them correctly can lead to duplicate
entries, failed lookups, or inconsistent behavior.

______________________________________________________________________

# Practice Questions

1. What is the Java Collections Framework?
1. What is the difference between `Collection` and `Collections`?
1. Why is `Map` not part of the `Collection` interface?
1. Explain the internal working of `ArrayList`.
1. What is the difference between `ArrayList` and `LinkedList`?
1. Explain the internal working of `HashMap`.
1. What is a hash collision, and how does Java handle it?
1. When would you use `TreeMap` instead of `HashMap`?
1. Why is `ArrayDeque` preferred over `Stack`?
1. Why must `equals()` and `hashCode()` be overridden together?

______________________________________________________________________

# Summary

The Java Collections Framework provides efficient, reusable data structures for storing and manipulating groups of
objects.

In this chapter, you learned:

- Collection hierarchy
- `List`, `Set`, `Queue`, and `Map`
- `ArrayList` vs `LinkedList`
- `HashSet`, `LinkedHashSet`, `TreeSet`
- `HashMap`, `LinkedHashMap`, `TreeMap`, `ConcurrentHashMap`
- Internal working and time complexity
- Iteration
- Utility methods
- Choosing the right collection
- Common interview questions

Strong Java developers don't memorize every collection—they understand **how each one works internally**, its
**performance characteristics**, and **when to choose it**.

______________________________________________________________________

# Next

[Generics](09-generics.md)

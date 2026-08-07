# Java Interview Cheatsheet

This file is intended for **last-minute interview revision**.

It doesn't teach Java from scratch.

Instead, it helps you quickly refresh the most frequently asked Java concepts before an interview.

______________________________________________________________________

# Java Basics

### Why Java?

- Platform independent
- Object-oriented
- Strongly typed
- Automatic Garbage Collection
- Huge ecosystem
- Excellent concurrency support

______________________________________________________________________

### Java Compilation Flow

```
.java

↓

javac

↓

.class (Bytecode)

↓

JVM

↓

Machine Code
```

______________________________________________________________________

### JDK vs JRE vs JVM

| JDK | JRE | JVM |
|-----|-----|-----|
| Development Kit | Runtime | Executes Bytecode |
| Contains compiler | Contains JVM | Executes Java code |
| Used for development | Used for running | Handles memory & GC |

______________________________________________________________________

# OOP

### Four Pillars

- Encapsulation
- Inheritance
- Polymorphism
- Abstraction

______________________________________________________________________

### Class vs Object

Class

```
Blueprint
```

Object

```
Instance of class
```

______________________________________________________________________

### Constructor

- Same name as class
- No return type
- Runs automatically
- Initializes objects

______________________________________________________________________

### Constructor vs Method

| Constructor | Method |
|--------------|---------|
| Initializes object | Performs behavior |
| No return type | Has return type |
| Auto invoked | Explicitly called |

______________________________________________________________________

# Access Modifiers

| Modifier | Same Class | Package | Subclass | Everywhere |
|-----------|------------|----------|-----------|-------------|
| private | ✅ | ❌ | ❌ | ❌ |
| default | ✅ | ✅ | ❌ | ❌ |
| protected | ✅ | ✅ | ✅ | ❌\* |
| public | ✅ | ✅ | ✅ | ✅ |

______________________________________________________________________

# Inheritance

Keyword

```java
extends
```

Single inheritance only.

______________________________________________________________________

# Method Overloading

Same method

Different parameters

Compile-time

______________________________________________________________________

# Method Overriding

Child class

Same signature

Runtime

Use

```java
@Override
```

______________________________________________________________________

# Polymorphism

Compile-time

```
Method Overloading
```

Runtime

```
Method Overriding
```

______________________________________________________________________

# Upcasting

```java
Animal animal =
    new Dog();
```

Safe.

Automatic.

______________________________________________________________________

# Downcasting

```java
Dog dog =
    (Dog) animal;
```

Requires explicit cast.

Use

```java
instanceof
```

when appropriate.

______________________________________________________________________

# Abstract Class

Can contain

- Fields
- Constructors
- Methods
- Abstract methods

Cannot instantiate.

______________________________________________________________________

# Interface

Defines a contract.

Supports

- Multiple inheritance
- Default methods
- Static methods

Use for loose coupling.

______________________________________________________________________

# Interface vs Abstract Class

| Interface | Abstract Class |
|------------|----------------|
| Contract | Base implementation |
| Multiple inheritance | Single inheritance |
| No instance state | Can have state |
| No constructors | Constructors allowed |

______________________________________________________________________

# Exception Handling

Hierarchy

```
Throwable

↓

Error

↓

Exception

↓

RuntimeException
```

______________________________________________________________________

### Checked Exception

Compiler checks.

Must handle or declare.

Example

```
IOException
```

______________________________________________________________________

### Unchecked Exception

Runtime.

Example

```
NullPointerException

IllegalArgumentException

ArithmeticException
```

______________________________________________________________________

### throw vs throws

throw

```
Throws exception
```

throws

```
Declares exception
```

______________________________________________________________________

### try-with-resources

Preferred for resources implementing

```
AutoCloseable
```

______________________________________________________________________

# Collections

Hierarchy

```
Collection

↓

List

↓

Set

↓

Queue

Map (Separate)
```

______________________________________________________________________

# List

- Ordered
- Duplicates allowed
- Indexed

Most common

```
ArrayList
```

______________________________________________________________________

# ArrayList

Internal structure

```
Dynamic Array
```

Complexities

```
get()

O(1)
```

```
add()

O(1) amortized
```

```
insert beginning

O(n)
```

______________________________________________________________________

# LinkedList

Internal structure

```
Doubly Linked List
```

Random access

```
O(n)
```

______________________________________________________________________

# Set

- Unique elements
- No duplicates

______________________________________________________________________

# HashSet

Internal

```
HashMap
```

Average

```
O(1)
```

______________________________________________________________________

# TreeSet

Internal

```
Red Black Tree
```

Operations

```
O(log n)
```

Sorted.

______________________________________________________________________

# Queue

FIFO

Methods

```
offer()

poll()

peek()
```

______________________________________________________________________

# PriorityQueue

Internal

```
Binary Heap
```

______________________________________________________________________

# Map

Key

↓

Value

______________________________________________________________________

# HashMap

Internal

```
Buckets

↓

hashCode()

↓

equals()
```

Average

```
O(1)
```

______________________________________________________________________

# LinkedHashMap

Maintains insertion order.

______________________________________________________________________

# TreeMap

Sorted keys.

Internal

```
Red Black Tree
```

Complexity

```
O(log n)
```

______________________________________________________________________

# ConcurrentHashMap

Thread-safe.

Preferred over

```
Hashtable
```

______________________________________________________________________

# equals() and hashCode()

Always override together.

Used by

- HashMap
- HashSet
- LinkedHashMap

______________________________________________________________________

# Generics

Purpose

- Compile-time type safety
- Eliminates casting

______________________________________________________________________

# Wildcards

```
?

? extends

? super
```

Remember

```
PECS

Producer

Extends

Consumer

Super
```

______________________________________________________________________

# Type Erasure

Generic information removed

at runtime.

______________________________________________________________________

# Lambda Expression

```java
(a,b) -> a+b
```

Anonymous function.

______________________________________________________________________

# Functional Interface

Exactly

```
One Abstract Method
```

Examples

```
Predicate

Function

Consumer

Supplier
```

______________________________________________________________________

# Method Reference

```java
System.out::println
```

Cleaner Lambda.

______________________________________________________________________

# Optional

Avoids

```
NullPointerException
```

Useful methods

```
orElse()

orElseGet()

orElseThrow()

ifPresent()

map()
```

______________________________________________________________________

# Date API

Classes

```
LocalDate

LocalTime

LocalDateTime
```

Avoid

```
Date

Calendar
```

for new code.

______________________________________________________________________

# Streams

Pipeline

```
Source

↓

Intermediate

↓

Terminal
```

______________________________________________________________________

Intermediate

```
filter

map

flatMap

sorted

distinct

peek
```

______________________________________________________________________

Terminal

```
collect

reduce

count

forEach

findFirst

anyMatch
```

______________________________________________________________________

Important

Streams are

```
Lazy

Single-use
```

______________________________________________________________________

# Concurrency

### Process

Independent program.

______________________________________________________________________

### Thread

Lightweight execution unit.

______________________________________________________________________

### Runnable vs Thread

Prefer

```
Runnable
```

______________________________________________________________________

### start() vs run()

```
start()

Creates thread
```

```
run()

Normal method
```

______________________________________________________________________

### synchronized

Provides

```
Mutual Exclusion
```

______________________________________________________________________

### volatile

Provides

```
Visibility

NOT Atomicity
```

______________________________________________________________________

### Atomic Classes

```
AtomicInteger

AtomicLong

AtomicBoolean
```

______________________________________________________________________

### ExecutorService

Preferred over

```
new Thread()
```

______________________________________________________________________

### Callable

Returns value.

______________________________________________________________________

### Future

Represents async result.

______________________________________________________________________

### CompletableFuture

Supports

- Chaining
- Combining
- Async pipelines

______________________________________________________________________

# JVM

Memory

```
Heap

Stack

Metaspace
```

______________________________________________________________________

### Heap

Stores

Objects

Shared

______________________________________________________________________

### Stack

Stores

Local Variables

Method Frames

Per Thread

______________________________________________________________________

### Metaspace

Stores

Class Metadata

______________________________________________________________________

# Garbage Collection

Young Generation

↓

Minor GC

Old Generation

↓

Major GC

______________________________________________________________________

Common GC

- G1 (default)
- Parallel GC
- Serial GC
- ZGC

______________________________________________________________________

# Common Errors

```
OutOfMemoryError

StackOverflowError

NullPointerException

ClassCastException

ConcurrentModificationException

IllegalArgumentException
```

Know when and why each occurs.

______________________________________________________________________

# Comparable vs Comparator

Comparable

```
Natural Ordering

compareTo()
```

Comparator

```
Custom Ordering

compare()
```

______________________________________________________________________

# StringBuilder

Mutable

Fast

Preferred for repeated concatenation.

______________________________________________________________________

# StringBuilder vs StringBuffer

| StringBuilder | StringBuffer |
|---------------|--------------|
| Faster | Thread-safe |
| Not synchronized | Synchronized |

______________________________________________________________________

# UUID

Generate unique identifiers.

```java
UUID.randomUUID();
```

______________________________________________________________________

# Enum

Use for fixed constants.

Example

```
Status

Role

Priority
```

______________________________________________________________________

# Immutable Objects

Characteristics

- final class
- final fields
- No setters
- Constructor initialization

Benefits

- Thread-safe
- Easy to reason about
- Safe to share

______________________________________________________________________

# Frequently Asked Interview Questions

## Java Basics

- JDK vs JRE vs JVM
- Heap vs Stack
- Primitive vs Reference types
- String vs StringBuilder
- final vs finally vs finalize
- == vs equals()

______________________________________________________________________

## OOP

- Four pillars
- Constructor vs Method
- Interface vs Abstract Class
- Composition vs Inheritance
- Overloading vs Overriding
- Upcasting vs Downcasting

______________________________________________________________________

## Collections

- ArrayList vs LinkedList
- HashMap vs TreeMap
- HashSet vs TreeSet
- HashMap internal working
- equals() & hashCode()
- ConcurrentHashMap
- PriorityQueue

______________________________________________________________________

## Java 8+

- Lambda
- Functional Interface
- Method Reference
- Optional
- Stream API
- map() vs flatMap()
- filter() vs map()
- reduce()
- groupingBy()
- Parallel Streams

______________________________________________________________________

## Concurrency

- Process vs Thread
- Runnable vs Thread
- start() vs run()
- synchronized
- volatile
- AtomicInteger
- ExecutorService
- Future
- CompletableFuture
- Deadlock
- Race Condition

______________________________________________________________________

## JVM

- JVM Architecture
- Heap vs Stack
- Garbage Collection
- G1 GC
- Minor vs Major GC
- Memory Leak
- OutOfMemoryError
- StackOverflowError

______________________________________________________________________

# 30-Second Revision Before Interview

- Prefer interfaces over implementations.
- Prefer composition over inheritance.
- Override `equals()` and `hashCode()` together.
- Use `ArrayList` by default.
- Use `HashMap` unless ordering or sorting is required.
- Prefer `StringBuilder` for repeated concatenation.
- Use `Optional` as a return type, not as a field.
- Remember **PECS** for Generics.
- Streams are lazy and single-use.
- Prefer `ExecutorService` over manually creating threads.
- Use `CompletableFuture` for modern asynchronous programming.
- Objects live in the Heap; local variables live in the Stack.
- `volatile` provides visibility, not atomicity.
- `synchronized` provides mutual exclusion.
- Always catch specific exceptions instead of generic `Exception`.
- Understand the trade-offs between collections, not just their APIs.

______________________________________________________________________

# Summary

This cheatsheet condenses the highest-value Java concepts into a single revision guide.

If you can confidently explain every topic in this document—along with the "why" behind each concept—you'll be
well-prepared for most Java backend interviews, from mid-level to senior roles.

______________________________________________________________________

# Next

[Java vs Python for Backend Engineers](16-java-vs-python-for-backend-engineers.md)

# JVM Memory & Garbage Collection

Understanding the JVM (Java Virtual Machine) is essential for backend engineers.

It is one of the most commonly asked Java interview topics because it directly affects:

- Performance
- Memory usage
- Application stability
- Debugging
- Production troubleshooting

Even if you never tune the JVM yourself, you should understand **how Java manages memory** and **how Garbage Collection
works**.

______________________________________________________________________

# What is JVM?

JVM stands for **Java Virtual Machine**.

It is the runtime environment responsible for executing Java bytecode.

```
Java Source Code

↓

javac

↓

Bytecode (.class)

↓

JVM

↓

Machine Code

↓

CPU
```

This is why Java is called

> **Write Once, Run Anywhere (WORA)**

The same bytecode can run on Windows, Linux, or macOS as long as a compatible JVM exists.

______________________________________________________________________

# JDK vs JRE vs JVM

One of the most frequently asked interview questions.

```
JDK
│
├── JRE
│     │
│     └── JVM
```

______________________________________________________________________

## JVM

Responsible for

- Loading classes
- Managing memory
- Executing bytecode
- Garbage Collection

______________________________________________________________________

## JRE (Java Runtime Environment)

Contains

- JVM
- Java libraries
- Runtime dependencies

Used only to run Java applications.

______________________________________________________________________

## JDK (Java Development Kit)

Contains

- JRE
- Compiler (`javac`)
- Debugger
- Javadoc
- Development tools

Used to develop Java applications.

______________________________________________________________________

# JVM Architecture

High-level view

```
                 JVM
                  │
    ┌─────────────┼──────────────┐
    │             │              │
 Class Loader  Runtime Data   Execution
               Areas           Engine
```

______________________________________________________________________

# Class Loader

Responsible for loading `.class` files into memory.

Three important class loaders

- Bootstrap ClassLoader
- Platform ClassLoader
- Application ClassLoader

Most interviews only expect a high-level understanding.

______________________________________________________________________

# Runtime Memory Areas

The JVM divides memory into several areas.

```
          JVM Memory

         ┌─────────────┐
         │   Heap      │
         ├─────────────┤
         │   Stack     │
         ├─────────────┤
         │ Metaspace   │
         ├─────────────┤
         │ PC Register │
         ├─────────────┤
         │ Native Stack│
         └─────────────┘
```

The most important ones are:

- Heap
- Stack
- Metaspace

______________________________________________________________________

# Heap Memory

The Heap stores **objects**.

Example

```java
Employee emp =
    new Employee();
```

The object created with `new` lives in the Heap.

```
Stack

↓

Reference

↓

Heap

↓

Employee Object
```

The Heap is shared by all threads.

______________________________________________________________________

# Stack Memory

Each thread has its own Stack.

The Stack stores

- Local variables
- Method parameters
- Method calls
- Object references

Example

```java
void print(){

    int age = 25;

}
```

`age` is stored in the Stack.

______________________________________________________________________

# Stack Frames

Each method call creates a new Stack Frame.

Example

```java
main()

↓

login()

↓

validate()

↓

encrypt()
```

Each method has its own frame.

When a method finishes,

its frame is removed automatically.

______________________________________________________________________

# Heap vs Stack

| Heap | Stack |
|------|-------|
| Stores objects | Stores local variables |
| Shared by threads | One per thread |
| Larger | Smaller |
| Garbage collected | Automatically released |

______________________________________________________________________

# Metaspace

Before Java 8

```
PermGen
```

After Java 8

```
Metaspace
```

Stores

- Class metadata
- Method metadata
- Runtime constants

Unlike Heap,

Metaspace uses native memory.

______________________________________________________________________

# Program Counter (PC Register)

Each thread has its own PC Register.

It stores

```
Current instruction
```

being executed.

Mostly an interview topic.

______________________________________________________________________

# Native Method Stack

Used for native methods written in

- C
- C++

through JNI (Java Native Interface).

Rarely discussed outside advanced JVM interviews.

______________________________________________________________________

# Memory Example

```java
public class Main {

    public static void main(String[] args){

        Employee employee =
            new Employee();

    }

}
```

Memory

```
Stack

employee

↓

Heap

Employee Object
```

The variable lives in the Stack.

The object lives in the Heap.

______________________________________________________________________

# Garbage Collection

Java automatically frees memory.

Unlike C or C++,

you never write

```cpp
delete object;
```

The JVM automatically removes unused objects.

______________________________________________________________________

# Garbage Collector

The Garbage Collector (GC) identifies objects that are no longer reachable and reclaims their memory.

Example

```java
Employee employee =
    new Employee();

employee = null;
```

The object becomes eligible for garbage collection.

______________________________________________________________________

# Reachability

An object is eligible for garbage collection when **no reachable references** point to it.

Example

```java
Employee employee =
    new Employee();

employee = null;
```

No references remain.

The object can be collected.

______________________________________________________________________

# Important Note

Eligible for GC

≠

Immediately removed.

The JVM decides **when** to run Garbage Collection.

This is a common interview trick.

______________________________________________________________________

# Generational Heap

Modern JVMs divide the Heap into generations.

```
Heap

├── Young Generation

└── Old Generation
```

Why?

Because

> Most objects die young.

This observation is known as the **Weak Generational Hypothesis**.

______________________________________________________________________

# Young Generation

New objects are created here.

```
new Employee()

↓

Young Generation
```

Most objects are short-lived.

Examples

- Request objects
- DTOs
- Temporary Strings

______________________________________________________________________

# Old Generation

Objects that survive multiple GC cycles are promoted here.

Examples

- Cache entries
- Long-lived services
- Shared objects

______________________________________________________________________

# Minor GC

Runs on

```
Young Generation
```

Fast.

Frequent.

______________________________________________________________________

# Major (Full) GC

Runs on

```
Entire Heap

↓

Young + Old
```

Slower.

Should occur infrequently.

Too many Full GCs usually indicate memory problems.

______________________________________________________________________

# Common Garbage Collectors

Modern JVMs support several GC algorithms.

______________________________________________________________________

## Serial GC

- Single thread
- Simple
- Good for small applications

______________________________________________________________________

## Parallel GC

- Multiple GC threads
- High throughput
- Long pause times

Good for batch processing.

______________________________________________________________________

## G1 GC (Garbage First)

Default in modern JVMs.

Features

- Predictable pause times
- Region-based heap
- Suitable for large heaps

Most Spring Boot applications use G1.

______________________________________________________________________

## ZGC

Designed for

- Huge heaps
- Extremely low pause times

Suitable for applications requiring minimal latency.

______________________________________________________________________

# Stop-The-World (STW)

Most Garbage Collectors pause application threads while performing certain GC operations.

This is called

```
Stop-The-World
```

Goal

Keep pause times as short as possible.

______________________________________________________________________

# Memory Leak in Java?

Many people think Java cannot have memory leaks.

Wrong.

Example

```java
List<Employee> cache =
    new ArrayList<>();
```

```java
cache.add(new Employee());
```

If objects remain referenced forever,

they cannot be garbage collected.

Memory usage keeps growing.

This is a **memory leak**.

______________________________________________________________________

# OutOfMemoryError

Occurs when the JVM cannot allocate more memory.

Common causes

- Huge collections
- Infinite object creation
- Memory leaks
- Incorrect JVM heap size

Example

```java
List<byte[]> list =
    new ArrayList<>();

while(true){

    list.add(new byte[1024 * 1024]);

}
```

Eventually

```
OutOfMemoryError
```

______________________________________________________________________

# StackOverflowError

Usually caused by infinite recursion.

Example

```java
void print(){

    print();

}
```

Eventually

```
StackOverflowError
```

Each recursive call creates another Stack Frame.

______________________________________________________________________

# finalize()

Older Java versions supported

```java
protected void finalize()
```

It was intended for cleanup before GC.

Today,

`finalize()` is deprecated and should be avoided because it is unpredictable and impacts performance.

Use

- try-with-resources
- `AutoCloseable`

instead.

______________________________________________________________________

# Escape Analysis

Modern JVM optimization.

If an object never escapes a method,

the JVM may allocate it on the stack instead of the heap.

Example

```java
void calculate(){

    Point point = new Point();

}
```

The JVM may optimize away heap allocation.

This optimization is automatic.

______________________________________________________________________

# JVM Memory Diagram

```
                 JVM

        ┌─────────────────┐
        │   Heap          │
        │                 │
        │ Young           │
        │ Old             │
        └─────────────────┘

        ┌─────────────────┐
        │ Stack           │
        │ Thread 1        │
        │ Thread 2        │
        └─────────────────┘

        ┌─────────────────┐
        │ Metaspace       │
        └─────────────────┘
```

______________________________________________________________________

# Common Mistakes

## Thinking `System.gc()` Forces GC

```java
System.gc();
```

It only **requests** Garbage Collection.

The JVM may ignore it.

______________________________________________________________________

## Calling `finalize()`

Deprecated.

Avoid it.

______________________________________________________________________

## Confusing Stack and Heap

Remember

- Objects → Heap
- Local variables → Stack

______________________________________________________________________

## Assuming Java Cannot Leak Memory

Holding references indefinitely prevents objects from being garbage collected.

______________________________________________________________________

# Best Practices

✅ Create short-lived objects when appropriate.

✅ Avoid unnecessary object retention.

✅ Use try-with-resources for resource management.

✅ Prefer immutable objects.

✅ Monitor Heap usage in production.

✅ Understand GC logs when troubleshooting performance.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between JDK, JRE, and JVM?

### Answer

The JVM executes Java bytecode and manages runtime activities such as memory allocation and garbage collection.

The JRE contains the JVM along with the libraries required to run Java applications.

The JDK contains the JRE plus development tools such as the Java compiler (`javac`), debugger, and documentation
generator.

______________________________________________________________________

## Question

What is the difference between Heap and Stack memory?

### Answer

The Heap stores objects and is shared among all threads. It is managed by the Garbage Collector.

The Stack stores local variables, method parameters, and method call information. Each thread has its own stack, and
memory is automatically released when methods return.

______________________________________________________________________

## Question

How does Garbage Collection work?

### Answer

The Garbage Collector identifies objects that are no longer reachable from any live references and reclaims their
memory. Developers do not explicitly free memory; the JVM decides when to perform garbage collection based on its
algorithms and runtime conditions.

______________________________________________________________________

## Question

What is the difference between Minor GC and Major GC?

### Answer

Minor GC collects objects in the Young Generation and is generally fast because most newly created objects are
short-lived.

Major (or Full) GC processes the Old Generation, and sometimes the entire heap, making it more expensive and potentially
causing longer application pauses.

______________________________________________________________________

## Question

Can Java have memory leaks?

### Answer

Yes. A memory leak occurs when objects remain reachable through references that are no longer needed. Because the
Garbage Collector only removes unreachable objects, retaining unnecessary references prevents memory from being
reclaimed.

______________________________________________________________________

# Practice Questions

1. What is the JVM?
1. What is the difference between JDK, JRE, and JVM?
1. Explain the JVM memory areas.
1. What is stored in the Heap?
1. What is stored in the Stack?
1. What is Metaspace?
1. How does Garbage Collection work?
1. What is the Young Generation?
1. What is the difference between Minor GC and Major GC?
1. Can Java applications still have memory leaks? Explain why.

______________________________________________________________________

# Summary

The JVM is responsible for executing Java applications efficiently while managing memory automatically.

In this chapter, you learned:

- JVM architecture
- JDK vs JRE vs JVM
- Heap, Stack, and Metaspace
- Object allocation
- Garbage Collection
- Generational Heap
- Minor and Major GC
- G1 and ZGC
- Stop-The-World pauses
- Memory leaks
- `OutOfMemoryError`
- `StackOverflowError`
- Escape Analysis

A solid understanding of JVM memory and Garbage Collection helps you write more efficient Java applications,
troubleshoot production issues, and confidently answer some of the most common Java backend interview questions.

______________________________________________________________________

# Next

[Common Interview Coding Patterns](14-common-interview-coding-patterns.md)

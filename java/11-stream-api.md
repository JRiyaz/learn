# Stream API

The Stream API, introduced in Java 8, fundamentally changed how developers process collections.

Before Java 8, most collection processing relied on loops, temporary collections, and manual filtering.

Streams allow us to process data in a **declarative**, **functional**, and **readable** way.

Streams are heavily used in:

- Spring Boot
- Hibernate
- Enterprise Java applications
- Backend services
- Interview coding questions

Understanding Streams is essential for modern Java development.

______________________________________________________________________

# What is a Stream?

A Stream is **not a data structure**.

It is a sequence of elements that supports operations such as:

- filtering
- mapping
- sorting
- grouping
- reducing
- collecting

Think of a Stream as a pipeline.

```
Collection

↓

Stream

↓

Operations

↓

Result
```

______________________________________________________________________

# Creating a Stream

From a List

```java
List<String> names =
    List.of("Alice", "Bob", "Charlie");

Stream<String> stream =
    names.stream();
```

______________________________________________________________________

From an Array

```java
String[] names =
    {"Alice", "Bob"};

Stream<String> stream =
    Arrays.stream(names);
```

______________________________________________________________________

Using Stream.of()

```java
Stream<String> stream =
    Stream.of("Java", "Python", "Go");
```

______________________________________________________________________

# Stream Pipeline

Every stream pipeline has three parts.

```
Source

↓

Intermediate Operations

↓

Terminal Operation
```

Example

```java
names.stream()
     .filter(name -> name.startsWith("A"))
     .map(String::toUpperCase)
     .forEach(System.out::println);
```

______________________________________________________________________

# Intermediate Operations

Intermediate operations return another Stream.

Examples

```
filter()

map()

flatMap()

sorted()

distinct()

limit()

skip()

peek()
```

They are **lazy**.

Nothing executes until a terminal operation is called.

______________________________________________________________________

# Terminal Operations

Terminal operations produce the final result.

Examples

```
forEach()

collect()

count()

reduce()

findFirst()

findAny()

anyMatch()

allMatch()

noneMatch()

min()

max()
```

Once a terminal operation runs,

the stream is closed.

______________________________________________________________________

# filter()

Used to keep only matching elements.

Example

```java
List<Integer> numbers =
    List.of(1,2,3,4,5,6);

numbers.stream()
       .filter(n -> n % 2 == 0)
       .forEach(System.out::println);
```

Output

```
2
4
6
```

______________________________________________________________________

# map()

Transforms one value into another.

Example

```java
List<String> names =
    List.of("alice","bob");

names.stream()
     .map(String::toUpperCase)
     .forEach(System.out::println);
```

Output

```
ALICE
BOB
```

______________________________________________________________________

Another Example

```java
List<Integer> numbers =
    List.of(1,2,3);

numbers.stream()
       .map(n -> n * n)
       .forEach(System.out::println);
```

Output

```
1
4
9
```

______________________________________________________________________

# filter() + map()

Very common interview pattern.

```java
List<String> names =
    List.of("Alice","Bob","Charlie");

names.stream()
     .filter(name -> name.length() > 3)
     .map(String::toUpperCase)
     .forEach(System.out::println);
```

Output

```
ALICE
CHARLIE
```

______________________________________________________________________

# sorted()

Sorts elements.

```java
List<Integer> numbers =
    List.of(5,2,1,4);

numbers.stream()
       .sorted()
       .forEach(System.out::println);
```

Output

```
1
2
4
5
```

______________________________________________________________________

Descending Order

```java
numbers.stream()
       .sorted(Comparator.reverseOrder())
       .forEach(System.out::println);
```

______________________________________________________________________

# distinct()

Removes duplicates.

```java
List<Integer> numbers =
    List.of(1,2,2,3,3,4);

numbers.stream()
       .distinct()
       .forEach(System.out::println);
```

Output

```
1
2
3
4
```

______________________________________________________________________

# limit()

Returns first N elements.

```java
numbers.stream()
       .limit(3)
       .forEach(System.out::println);
```

______________________________________________________________________

# skip()

Skips first N elements.

```java
numbers.stream()
       .skip(2)
       .forEach(System.out::println);
```

______________________________________________________________________

# count()

Counts elements.

```java
long count =
    numbers.stream()
           .count();
```

______________________________________________________________________

# collect()

One of the most frequently used terminal operations.

Convert Stream back into a List.

```java
List<String> result =
    names.stream()
         .filter(name -> name.length() > 3)
         .toList();
```

Older Java versions

```java
.collect(Collectors.toList());
```

______________________________________________________________________

# reduce()

Combines all elements into a single result.

Sum

```java
int sum =
    List.of(1,2,3,4)
        .stream()
        .reduce(0, Integer::sum);
```

Output

```
10
```

Product

```java
int product =
    List.of(1,2,3,4)
        .stream()
        .reduce(1, (a,b) -> a*b);
```

Output

```
24
```

______________________________________________________________________

# findFirst()

```java
Optional<String> value =
    names.stream()
         .findFirst();
```

______________________________________________________________________

# findAny()

Useful for parallel streams.

```java
Optional<String> value =
    names.stream()
         .findAny();
```

______________________________________________________________________

# anyMatch()

```java
boolean result =
    names.stream()
         .anyMatch(name ->
             name.startsWith("A"));
```

______________________________________________________________________

# allMatch()

```java
boolean result =
    numbers.stream()
           .allMatch(n -> n > 0);
```

______________________________________________________________________

# noneMatch()

```java
boolean result =
    numbers.stream()
           .noneMatch(n -> n < 0);
```

______________________________________________________________________

# min() and max()

```java
int min =
    numbers.stream()
           .min(Integer::compareTo)
           .get();
```

```java
int max =
    numbers.stream()
           .max(Integer::compareTo)
           .get();
```

______________________________________________________________________

# flatMap()

One of the most asked Stream interview topics.

Suppose

```java
List<List<String>>
```

Example

```java
List<List<String>> data =
    List.of(
        List.of("A","B"),
        List.of("C","D")
    );
```

Without flatMap

```
[[A,B],[C,D]]
```

With flatMap

```java
data.stream()
    .flatMap(List::stream)
    .forEach(System.out::println);
```

Output

```
A
B
C
D
```

______________________________________________________________________

# peek()

Useful for debugging.

```java
numbers.stream()
       .peek(System.out::println)
       .map(n -> n * n)
       .toList();
```

Avoid using `peek()` for business logic.

______________________________________________________________________

# Chaining Operations

Example

```java
List<String> result =
    names.stream()
         .filter(name -> name.length() > 3)
         .map(String::toUpperCase)
         .sorted()
         .toList();
```

Very readable.

______________________________________________________________________

# groupingBy()

One of the most important interview questions.

Example

```java
Map<Integer, List<String>> grouped =
    names.stream()
         .collect(
             Collectors.groupingBy(
                 String::length
             )
         );
```

Output

```
3 -> [Bob]

5 -> [Alice]

7 -> [Charlie]
```

______________________________________________________________________

# counting()

```java
long count =
    names.stream()
         .count();
```

Inside grouping

```java
Map<Integer, Long> result =
    names.stream()
         .collect(
             Collectors.groupingBy(
                 String::length,
                 Collectors.counting()
             )
         );
```

______________________________________________________________________

# joining()

```java
String value =
    names.stream()
         .collect(
             Collectors.joining(", ")
         );
```

Output

```
Alice, Bob, Charlie
```

______________________________________________________________________

# partitioningBy()

Splits into two groups.

```java
Map<Boolean, List<Integer>> result =
    numbers.stream()
           .collect(
               Collectors.partitioningBy(
                   n -> n % 2 == 0
               )
           );
```

Output

```
true

↓

Even Numbers

false

↓

Odd Numbers
```

______________________________________________________________________

# summarizingInt()

```java
IntSummaryStatistics stats =
    numbers.stream()
           .collect(
               Collectors.summarizingInt(
                   Integer::intValue
               )
           );
```

Provides

- count
- sum
- min
- max
- average

______________________________________________________________________

# Lazy Evaluation

Important interview topic.

Example

```java
numbers.stream()
       .filter(n -> n > 5);
```

Nothing happens.

Only when

```java
.count()
```

or another terminal operation is called does execution begin.

______________________________________________________________________

# Streams Cannot Be Reused

Wrong

```java
Stream<String> stream =
    names.stream();

stream.count();

stream.forEach(System.out::println);
```

Output

```
IllegalStateException
```

A stream can be consumed only once.

______________________________________________________________________

# Parallel Streams

Sequential

```java
numbers.stream()
```

Parallel

```java
numbers.parallelStream()
```

Internally uses the ForkJoinPool.

Useful for CPU-intensive operations on large datasets.

Not always faster.

______________________________________________________________________

# Stream vs Collection

| Collection | Stream |
|------------|---------|
| Stores data | Processes data |
| Reusable | One-time use |
| Eager | Lazy |
| Mutable | Doesn't modify source |

______________________________________________________________________

# Common Mistakes

## Using Streams for Everything

Sometimes a simple loop is easier to understand.

Readability comes first.

______________________________________________________________________

## Modifying External Variables

Wrong

```java
int sum = 0;

numbers.stream()
       .forEach(n -> sum += n);
```

Use

```java
reduce()
```

instead.

______________________________________________________________________

## Calling get() on Optional

Wrong

```java
findFirst().get();
```

If no value exists,

an exception is thrown.

Prefer

```java
orElse()

orElseThrow()
```

______________________________________________________________________

## Reusing Streams

A stream is single-use.

Always create a new one.

______________________________________________________________________

# Best Practices

✅ Keep pipelines readable.

✅ Prefer Method References when appropriate.

✅ Avoid side effects.

✅ Use `map()` for transformation.

✅ Use `filter()` for selection.

✅ Use `flatMap()` for nested collections.

✅ Use parallel streams only after performance testing.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between `map()` and `flatMap()`?

### Answer

`map()` transforms each element into another element while maintaining the same structure. For example, a
`Stream<String>` can become a `Stream<Integer>`.

`flatMap()` transforms each element into another stream and then flattens all resulting streams into a single stream. It
is commonly used to process nested collections such as `List<List<T>>`.

______________________________________________________________________

## Question

What is lazy evaluation in Streams?

### Answer

Intermediate Stream operations such as `filter()`, `map()`, and `sorted()` are lazy. They do not execute immediately.
Processing begins only when a terminal operation like `collect()`, `count()`, or `forEach()` is invoked.

______________________________________________________________________

## Question

Why can't a Stream be reused?

### Answer

A Stream represents a one-time traversal of a data source. After a terminal operation completes, the Stream is
considered consumed and closed. Attempting to use it again results in an `IllegalStateException`.

______________________________________________________________________

## Question

What is the difference between `filter()` and `map()`?

### Answer

`filter()` selects elements that satisfy a condition and may reduce the number of elements.

`map()` transforms each element into another value while preserving the number of elements.

______________________________________________________________________

## Question

When should you use Parallel Streams?

### Answer

Parallel Streams are useful for CPU-intensive operations on large datasets where work can be processed independently.
They are not always faster due to thread management overhead and should be adopted only after performance testing.

______________________________________________________________________

# Practice Questions

1. What is a Stream?
1. Explain the Stream pipeline.
1. What are intermediate operations?
1. What are terminal operations?
1. What is the difference between `filter()` and `map()`?
1. Explain `flatMap()`.
1. What is lazy evaluation?
1. Why can't Streams be reused?
1. What is the purpose of `groupingBy()`?
1. When should you use Parallel Streams?

______________________________________________________________________

# Summary

The Stream API enables expressive, functional-style processing of collections while reducing boilerplate code.

In this chapter, you learned:

- Stream creation
- Stream pipelines
- Intermediate and terminal operations
- `filter()`, `map()`, `flatMap()`
- `sorted()`, `distinct()`, `limit()`, `skip()`
- `reduce()`
- `collect()`
- `groupingBy()`, `partitioningBy()`, `joining()`
- Lazy evaluation
- Parallel Streams
- Common interview questions

Streams are one of the defining features of modern Java and appear throughout enterprise applications and interviews.
Mastering them will make your code more concise, expressive, and maintainable.

______________________________________________________________________

# Next

[Multithreading & Concurrency](12-multithreading-and-concurrency.md)

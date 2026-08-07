# Common Interview Coding Patterns

This chapter focuses on Java language features and coding patterns that frequently appear in interviews.

This is **not a Data Structures & Algorithms chapter**.

Instead, it covers the Java APIs, language constructs, and idioms that interviewers expect experienced backend engineers
to know while solving coding problems.

______________________________________________________________________

# Comparable

`Comparable` defines the **natural ordering** of objects.

It is used when a class has one obvious way of being sorted.

Example

```java
public class Employee
        implements Comparable<Employee> {

    private int id;
    private String name;

    public Employee(int id, String name) {
        this.id = id;
        this.name = name;
    }

    @Override
    public int compareTo(Employee other) {
        return Integer.compare(this.id, other.id);
    }

}
```

Usage

```java
List<Employee> employees = new ArrayList<>();

Collections.sort(employees);
```

Objects are sorted by `id`.

______________________________________________________________________

# Comparator

`Comparator` provides **custom sorting**.

Unlike `Comparable`, it doesn't modify the class.

Example

```java
employees.sort(
    Comparator.comparing(Employee::getName)
);
```

Descending

```java
employees.sort(
    Comparator.comparing(Employee::getName)
              .reversed()
);
```

______________________________________________________________________

# Comparable vs Comparator

| Comparable | Comparator |
|------------|------------|
| Natural ordering | Custom ordering |
| `compareTo()` | `compare()` |
| Inside class | Outside class |
| One ordering | Multiple orderings |

______________________________________________________________________

# Sorting Objects

Sort by salary

```java
employees.sort(
    Comparator.comparing(Employee::getSalary)
);
```

Sort descending

```java
employees.sort(
    Comparator.comparing(Employee::getSalary)
              .reversed()
);
```

Multiple fields

```java
employees.sort(
    Comparator.comparing(Employee::getDepartment)
              .thenComparing(Employee::getName)
);
```

______________________________________________________________________

# PriorityQueue

A PriorityQueue removes elements based on priority.

Internally,

it uses a **Binary Heap**.

Example

```java
PriorityQueue<Integer> pq =
    new PriorityQueue<>();

pq.offer(30);
pq.offer(10);
pq.offer(20);

while (!pq.isEmpty()) {

    System.out.println(pq.poll());

}
```

Output

```
10
20
30
```

______________________________________________________________________

# Max Heap

```java
PriorityQueue<Integer> maxHeap =
    new PriorityQueue<>(
        Comparator.reverseOrder()
    );
```

Output

```
30
20
10
```

______________________________________________________________________

# StringBuilder

Strings are immutable.

Example

```java
String text = "";

for (int i = 0; i < 1000; i++) {

    text += i;

}
```

Every concatenation creates a new String.

Very inefficient.

______________________________________________________________________

Use

```java
StringBuilder builder =
    new StringBuilder();

for (int i = 0; i < 1000; i++) {

    builder.append(i);

}

String result =
    builder.toString();
```

Much faster.

______________________________________________________________________

# Common StringBuilder Methods

Append

```java
builder.append("Java");
```

Insert

```java
builder.insert(0, "Hello ");
```

Delete

```java
builder.delete(0, 5);
```

Reverse

```java
builder.reverse();
```

Length

```java
builder.length();
```

______________________________________________________________________

# StringBuilder vs StringBuffer

| StringBuilder | StringBuffer |
|---------------|--------------|
| Not thread-safe | Thread-safe |
| Faster | Slower |
| Preferred | Rarely used |

Use `StringBuilder` unless synchronization is required.

______________________________________________________________________

# Enum

Enums define a fixed set of constants.

Example

```java
enum Status {

    NEW,
    PROCESSING,
    COMPLETED,
    FAILED

}
```

Usage

```java
Status status =
    Status.NEW;
```

______________________________________________________________________

# Enum with Fields

```java
enum Role {

    ADMIN("Administrator"),
    USER("Standard User");

    private final String label;

    Role(String label) {
        this.label = label;
    }

    public String getLabel() {
        return label;
    }

}
```

______________________________________________________________________

# UUID

UUIDs generate globally unique identifiers.

Example

```java
UUID id =
    UUID.randomUUID();

System.out.println(id);
```

Output

```
550e8400-e29b-41d4-a716-446655440000
```

Commonly used for

- User IDs
- Order IDs
- Distributed systems

______________________________________________________________________

# Objects Utility Class

Null-safe comparisons

```java
Objects.equals(a, b);
```

Null check

```java
Objects.requireNonNull(user);
```

Hash

```java
Objects.hash(id, name);
```

______________________________________________________________________

# Arrays Utility Class

Sort

```java
Arrays.sort(numbers);
```

Binary Search

```java
Arrays.binarySearch(numbers, 10);
```

Fill

```java
Arrays.fill(numbers, 0);
```

Convert to String

```java
Arrays.toString(numbers);
```

______________________________________________________________________

# Collections Utility Class

Sort

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

Frequency

```java
Collections.frequency(list, "Java");
```

______________________________________________________________________

# List.of()

Immutable list

```java
List<String> names =
    List.of("Java", "Python");
```

Cannot modify

```java
names.add("Go");
```

Output

```
UnsupportedOperationException
```

______________________________________________________________________

# Map.of()

Immutable map

```java
Map<Integer, String> users =
    Map.of(
        1, "Alice",
        2, "Bob"
    );
```

______________________________________________________________________

# Set.of()

Immutable set

```java
Set<String> skills =
    Set.of("Java", "Spring");
```

______________________________________________________________________

# Optional Patterns

Instead of

```java
if(user != null){

    return user.getName();

}

return "Unknown";
```

Use

```java
return Optional.ofNullable(user)
               .map(User::getName)
               .orElse("Unknown");
```

______________________________________________________________________

# Streams for Common Tasks

Filter

```java
employees.stream()
         .filter(e -> e.getSalary() > 50000)
         .toList();
```

Sort

```java
employees.stream()
         .sorted(
             Comparator.comparing(
                 Employee::getSalary
             )
         )
         .toList();
```

Count

```java
long total =
    employees.stream()
             .count();
```

Group

```java
employees.stream()
         .collect(
             Collectors.groupingBy(
                 Employee::getDepartment
             )
         );
```

______________________________________________________________________

# Frequency Counting

Classic interview pattern.

```java
Map<String, Integer> frequency =
    new HashMap<>();

for (String word : words) {

    frequency.put(
        word,
        frequency.getOrDefault(word, 0) + 1
    );

}
```

______________________________________________________________________

# computeIfAbsent()

Very useful.

```java
Map<String, List<String>> map =
    new HashMap<>();

map.computeIfAbsent(
    "Java",
    key -> new ArrayList<>()
).add("Spring");
```

Avoids explicit null checks.

______________________________________________________________________

# merge()

Updating values

```java
frequency.merge(
    word,
    1,
    Integer::sum
);
```

Cleaner than `getOrDefault()` in many situations.

______________________________________________________________________

# equals() and hashCode()

If two objects are logically equal,

always override both.

Example

```java
@Override
public boolean equals(Object obj) {

    if (this == obj) {
        return true;
    }

    if (!(obj instanceof Employee)) {
        return false;
    }

    Employee other = (Employee) obj;

    return id == other.id;

}
```

```java
@Override
public int hashCode() {

    return Objects.hash(id);

}
```

Essential for

- HashMap
- HashSet
- LinkedHashMap

______________________________________________________________________

# toString()

Useful for debugging.

```java
@Override
public String toString() {

    return "Employee{id=" + id +
           ", name='" + name + "'}";

}
```

Modern IDEs generate this automatically.

______________________________________________________________________

# equals(), hashCode(), and toString()

Most IDEs generate all three together.

Always review generated code before committing.

______________________________________________________________________

# Immutability Pattern

Good

```java
public final class Employee {

    private final int id;
    private final String name;

    public Employee(int id, String name) {

        this.id = id;
        this.name = name;

    }

    public int getId() {

        return id;

    }

    public String getName() {

        return name;

    }

}
```

No setters.

Thread-safe.

______________________________________________________________________

# Defensive Copying

Bad

```java
public List<String> getSkills() {

    return skills;

}
```

Caller can modify it.

Better

```java
public List<String> getSkills() {

    return List.copyOf(skills);

}
```

______________________________________________________________________

# Common Coding Patterns

## Swap Variables

```java
int temp = a;
a = b;
b = temp;
```

______________________________________________________________________

## Reverse String

```java
String reversed =
    new StringBuilder(text)
        .reverse()
        .toString();
```

______________________________________________________________________

## Count Characters

```java
Map<Character, Integer> count =
    new HashMap<>();

for (char c : text.toCharArray()) {

    count.merge(c, 1, Integer::sum);

}
```

______________________________________________________________________

## Remove Duplicates

```java
List<Integer> unique =
    numbers.stream()
           .distinct()
           .toList();
```

______________________________________________________________________

## Sort by Multiple Fields

```java
employees.sort(
    Comparator.comparing(Employee::getDepartment)
              .thenComparing(Employee::getSalary)
              .reversed()
);
```

______________________________________________________________________

# Common Mistakes

## Using == for Strings

Wrong

```java
name == "Java"
```

Correct

```java
name.equals("Java")
```

______________________________________________________________________

## Forgetting equals() and hashCode()

Hash-based collections won't behave correctly.

______________________________________________________________________

## Using String Concatenation in Loops

Prefer

```java
StringBuilder
```

______________________________________________________________________

## Returning Mutable Collections

Return immutable copies when appropriate.

______________________________________________________________________

# Best Practices

✅ Prefer `Comparator.comparing()` over manual comparison.

✅ Use `StringBuilder` for repeated concatenation.

✅ Override `equals()`, `hashCode()`, and `toString()` together.

✅ Use immutable collections when possible.

✅ Use `computeIfAbsent()` and `merge()` for map operations.

✅ Prefer expressive Stream operations over manual loops when readability improves.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between `Comparable` and `Comparator`?

### Answer

`Comparable` defines the natural ordering of a class by implementing the `compareTo()` method. A class can have only one
natural ordering.

`Comparator` defines custom orderings outside the class using the `compare()` method. Multiple comparators can exist for
the same class, allowing different sorting strategies.

______________________________________________________________________

## Question

Why is `StringBuilder` faster than String concatenation?

### Answer

`String` objects are immutable. Every concatenation creates a new object, resulting in unnecessary allocations.

`StringBuilder` maintains a mutable character buffer, allowing multiple append operations without creating intermediate
objects, making it much more efficient for repeated concatenation.

______________________________________________________________________

## Question

When should you use `computeIfAbsent()`?

### Answer

Use `computeIfAbsent()` when you want to initialize a value in a `Map` only if the key doesn't already exist. It
simplifies code by eliminating explicit null checks and is commonly used for grouping values.

______________________________________________________________________

## Question

Why should immutable objects be preferred?

### Answer

Immutable objects are thread-safe, easier to reason about, simpler to cache, and less prone to bugs caused by unintended
state changes.

______________________________________________________________________

## Question

What are some common Java coding patterns interviewers expect?

### Answer

Interviewers commonly expect familiarity with:

- `Comparable` and `Comparator`
- `PriorityQueue`
- `StringBuilder`
- `UUID`
- `Objects` utility methods
- Stream operations
- Frequency counting with `HashMap`
- `computeIfAbsent()` and `merge()`
- Proper implementation of `equals()`, `hashCode()`, and `toString()`

______________________________________________________________________

# Practice Questions

1. What is the difference between `Comparable` and `Comparator`?
1. Why should `StringBuilder` be preferred for repeated concatenation?
1. What is a `PriorityQueue`, and how is it implemented?
1. When should you use an `Enum`?
1. What is a UUID, and why is it useful?
1. What does `Objects.requireNonNull()` do?
1. Explain `computeIfAbsent()` with an example.
1. What is the purpose of `merge()`?
1. Why should `equals()` and `hashCode()` be overridden together?
1. Why should immutable objects be preferred?

______________________________________________________________________

# Summary

This chapter covered practical Java coding patterns that appear frequently in interviews and real-world backend
development.

You learned:

- `Comparable` vs `Comparator`
- `PriorityQueue`
- `StringBuilder`
- `Enum`
- `UUID`
- `Objects`, `Arrays`, and `Collections` utility classes
- Immutable collections
- Common `Map` patterns
- Frequency counting
- `computeIfAbsent()` and `merge()`
- Proper implementation of `equals()`, `hashCode()`, and `toString()`
- Defensive copying and immutability

Mastering these patterns will make your Java solutions cleaner, more idiomatic, and easier to discuss during interviews.

______________________________________________________________________

# Next

[Java Interview Cheatsheet](15-java-interview-cheatsheet.md)

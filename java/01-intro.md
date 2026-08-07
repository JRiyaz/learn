# Java Fundamentals

Welcome to the Java Refresh Course.

This course is designed for experienced software engineers who already understand programming concepts but want to
become comfortable writing Java again for backend interviews.

This is **not** a beginner's Java course.

Instead of spending pages explaining what a variable is, we'll focus on how Java works, why it works that way, and what
interviewers expect you to know.

______________________________________________________________________

# Prerequisites

You should already know:

- Variables
- Loops
- Functions
- Basic OOP
- Collections
- Basic programming concepts

If you've written Python, Java, C#, C++, JavaScript, or Go before, you're ready.

______________________________________________________________________

# What You'll Learn

By the end of this course you'll be comfortable with:

- Reading Java code
- Writing Java code
- Explaining Java concepts
- Solving interview coding problems
- Understanding Spring Boot codebases
- Answering Java interview questions

______________________________________________________________________

# Why Java?

Java remains one of the most popular backend languages because it provides:

- Excellent performance
- Strong type safety
- Huge ecosystem
- Mature tooling
- Great concurrency support
- Enterprise stability

Many large companies use Java for backend systems because of its scalability and maintainability.

______________________________________________________________________

# Java Program Structure

Let's begin with the simplest Java program.

```java
public class Main {

    public static void main(String[] args) {
        System.out.println("Hello World");
    }

}
```

At first glance this looks much more verbose than many other languages.

Let's understand every line.

______________________________________________________________________

# public class Main

```java
public class Main {

}
```

Every Java application consists of classes.

A class is simply a blueprint for creating objects.

Here,

- `public` → accessible from anywhere
- `class` → declares a class
- `Main` → class name

Class names always begin with an uppercase letter by convention.

Examples

```java
User

Employee

OrderService

PaymentController
```

______________________________________________________________________

# main()

```java
public static void main(String[] args)
```

This is the entry point of a Java application.

The JVM starts execution here.

Breakdown:

### public

Accessible by JVM.

### static

Can be called without creating an object.

### void

Returns nothing.

### main

Special method name recognized by JVM.

### String[] args

Command-line arguments.

______________________________________________________________________

# Example

```java
public class Main {

    public static void main(String[] args) {

        System.out.println(args.length);

    }

}
```

Run

```
java Main hello world
```

Output

```
2
```

______________________________________________________________________

# Statements

Every Java statement ends with a semicolon.

```java
int age = 25;

System.out.println(age);

age++;
```

Missing semicolons are one of the most common mistakes beginners make.

______________________________________________________________________

# Comments

Single line

```java
// This is a comment
```

Multi-line

```java
/*
This
is
a
comment
*/
```

Documentation comments

```java
/**
 * Calculates total price
 */
```

Used for generating JavaDocs.

______________________________________________________________________

# Variables

Variables store values.

Syntax

```java
datatype variableName = value;
```

Example

```java
int age = 25;

double salary = 55000.50;

char grade = 'A';

boolean active = true;

String name = "Riyaz";
```

______________________________________________________________________

# Variable Naming

Good

```java
employeeName

totalSalary

customerId
```

Bad

```java
x

abc

test123
```

Use meaningful names.

______________________________________________________________________

# Primitive Data Types

Java has eight primitive data types.

| Type | Size | Example |
|-------|------|----------|
| byte | 1 byte | 100 |
| short | 2 bytes | 200 |
| int | 4 bytes | 500 |
| long | 8 bytes | 100000L |
| float | 4 bytes | 10.5f |
| double | 8 bytes | 20.25 |
| char | 2 bytes | 'A' |
| boolean | JVM dependent | true |

______________________________________________________________________

# int

Most commonly used integer type.

```java
int age = 28;

int count = 100;
```

______________________________________________________________________

# long

Used for larger numbers.

```java
long population = 8000000000L;
```

Notice the suffix

```
L
```

______________________________________________________________________

# float

```java
float price = 10.5f;
```

Requires suffix

```
f
```

______________________________________________________________________

# double

Most common decimal type.

```java
double pi = 3.14159;
```

______________________________________________________________________

# char

Stores a single Unicode character.

```java
char grade = 'A';

char symbol = '$';
```

Uses single quotes.

______________________________________________________________________

# boolean

Only two values.

```java
boolean isAdmin = true;

boolean loggedIn = false;
```

______________________________________________________________________

# Primitive vs Reference Types

Primitive

```java
int

double

char

boolean
```

Reference

```java
String

Array

Object

List

Map

User
```

Primitive variables store values directly.

Reference variables store references to objects.

______________________________________________________________________

# Strings

Strings are objects.

```java
String name = "Riyaz";
```

Useful methods

Length

```java
name.length();
```

Uppercase

```java
name.toUpperCase();
```

Lowercase

```java
name.toLowerCase();
```

Contains

```java
name.contains("iya");
```

Substring

```java
name.substring(0,3);
```

Replace

```java
name.replace("R","K");
```

______________________________________________________________________

# String Immutability

Strings cannot be modified.

Example

```java
String name = "Java";

name.toUpperCase();

System.out.println(name);
```

Output

```
Java
```

Correct

```java
name = name.toUpperCase();
```

Output

```
JAVA
```

We'll discuss why Strings are immutable later in the course.

______________________________________________________________________

# Constants

Use

```java
final
```

Example

```java
final double PI = 3.14159;
```

Cannot be reassigned.

Convention

```java
MAX_USERS

DEFAULT_TIMEOUT

PI
```

Uppercase with underscores.

______________________________________________________________________

# Type Casting

Implicit

```java
int x = 10;

double y = x;
```

Output

```
10.0
```

______________________________________________________________________

Explicit

```java
double pi = 3.14;

int x = (int) pi;
```

Output

```
3
```

Decimal part is lost.

______________________________________________________________________

# Operators

Arithmetic

```java
+

-

*

/

%
```

Example

```java
int a = 10;

int b = 3;

System.out.println(a+b);

System.out.println(a%b);
```

______________________________________________________________________

Comparison

```java
==

!=

>

<

>=

<=
```

______________________________________________________________________

Logical

```java
&&

||

!
```

Example

```java
if(age > 18 && active){

}
```

______________________________________________________________________

# if Statement

```java
int age = 20;

if(age >= 18){

    System.out.println("Adult");

}
```

______________________________________________________________________

if else

```java
if(score >= 50){

    System.out.println("Pass");

}else{

    System.out.println("Fail");

}
```

______________________________________________________________________

else if

```java
if(score >= 90){

    System.out.println("A");

}else if(score >= 75){

    System.out.println("B");

}else{

    System.out.println("C");

}
```

______________________________________________________________________

# switch

Traditional

```java
switch(day){

    case 1:
        System.out.println("Monday");
        break;

    case 2:
        System.out.println("Tuesday");
        break;

    default:
        System.out.println("Invalid");

}
```

Remember

Without `break`, execution falls through to the next case.

______________________________________________________________________

# Loops

for

```java
for(int i=0; i<5; i++){

    System.out.println(i);

}
```

______________________________________________________________________

while

```java
int i = 0;

while(i<5){

    System.out.println(i);

    i++;

}
```

______________________________________________________________________

do while

```java
int i = 0;

do{

    System.out.println(i);

    i++;

}while(i<5);
```

Runs at least once.

______________________________________________________________________

Enhanced for loop

```java
int[] numbers = {1,2,3,4};

for(int num : numbers){

    System.out.println(num);

}
```

Preferred when you don't need the index.

______________________________________________________________________

# Arrays

Declaration

```java
int[] numbers = new int[5];
```

Initialization

```java
int[] numbers = {1,2,3,4,5};
```

Access

```java
System.out.println(numbers[2]);
```

Output

```
3
```

Length

```java
numbers.length
```

Notice

Arrays use

```
length
```

not

```
length()
```

______________________________________________________________________

# Methods

Syntax

```java
returnType methodName(parameters){

}
```

Example

```java
public static int add(int a, int b){

    return a+b;

}
```

Calling

```java
int result = add(10,20);
```

______________________________________________________________________

# Method Overloading

Multiple methods with the same name.

```java
int add(int a,int b){

}

double add(double a,double b){

}

int add(int a,int b,int c){

}
```

Java chooses the correct method based on parameters.

______________________________________________________________________

# static

Static members belong to the class.

Example

```java
public class MathUtil{

    static int square(int x){

        return x*x;

    }

}
```

Usage

```java
MathUtil.square(5);
```

No object required.

______________________________________________________________________

# Common Beginner Mistakes

### Comparing Strings using ==

Wrong

```java
if(name == "Java")
```

Correct

```java
if(name.equals("Java"))
```

______________________________________________________________________

### Forgetting break

```java
switch(day){

    case 1:

    case 2:

}
```

Execution falls through.

______________________________________________________________________

### Forgetting final

Constants should always use

```java
final
```

______________________________________________________________________

### Using float unnecessarily

Prefer

```java
double
```

unless memory is critical.

______________________________________________________________________

# Best Practices

✅ Use meaningful variable names.

✅ Keep methods small.

✅ Prefer `double` over `float`.

✅ Use `final` for constants.

✅ Avoid magic numbers.

✅ One statement per line.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between primitive and reference data types?

### Answer

Primitive data types store actual values directly in memory and include types like `int`, `double`, `char`, and
`boolean`. They are lightweight and have fixed sizes.

Reference data types store references (memory addresses) to objects rather than the objects themselves. Examples include
`String`, arrays, collections, and user-defined classes. Multiple reference variables can point to the same object,
whereas primitive variables always contain their own independent values.

______________________________________________________________________

# Practice Questions

1. Why does Java require a `main()` method?
1. What is the difference between `float` and `double`?
1. Why are Strings immutable?
1. What is `final`?
1. What is type casting?
1. Explain implicit vs explicit casting.
1. Why are arrays fixed in size?
1. Explain `static`.
1. What happens if `break` is omitted in a `switch` statement?
1. What is the difference between primitive and reference types?

______________________________________________________________________

# Summary

In this chapter, you refreshed the core building blocks of Java:

- Java program structure
- Variables and data types
- Primitive vs reference types
- Strings
- Operators
- Control flow
- Arrays
- Methods
- Method overloading
- `static`
- `final`

These fundamentals form the base for everything else in Java. In the next chapter, we'll move into object-oriented
programming, where Java truly starts to shine.

______________________________________________________________________

# Next

[OOP in Java](02-oop-in-java.md)

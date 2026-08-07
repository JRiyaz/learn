# Exception Handling

Exception Handling is one of the core features that makes Java applications reliable.

In real-world applications, things go wrong all the time:

- Database connections fail.
- Files don't exist.
- APIs time out.
- Invalid user input is received.
- Network connections are interrupted.

Instead of crashing the application, Java provides a structured way to detect, handle, and recover from these
situations.

______________________________________________________________________

# What is an Exception?

An exception is an event that interrupts the normal flow of a program.

Example

```java
int result = 10 / 0;
```

Output

```
Exception in thread "main"
java.lang.ArithmeticException: / by zero
```

Instead of continuing execution, the JVM throws an exception.

______________________________________________________________________

# Exception Hierarchy

Everything in Java ultimately inherits from `Throwable`.

```
                Throwable
                /       \
             Error    Exception
                         |
                 RuntimeException
```

The hierarchy is important because different types of problems are handled differently.

______________________________________________________________________

# Throwable

The root class of all errors and exceptions.

It has two major subclasses:

- Error
- Exception

______________________________________________________________________

# Error

Errors represent serious problems that applications generally should **not** try to handle.

Examples

- OutOfMemoryError
- StackOverflowError
- VirtualMachineError

Example

```java
public class Main {

    public static void main(String[] args) {

        throw new OutOfMemoryError();

    }

}
```

Normally,

you should not catch Errors.

______________________________________________________________________

# Exception

Exceptions represent conditions that applications can reasonably recover from.

Examples

- File not found
- Invalid input
- Database connection failure
- Network timeout

These should usually be handled.

______________________________________________________________________

# Checked Exceptions

Checked exceptions are verified by the compiler.

You **must** either:

- Handle them
- Declare them

Example

```java
FileReader reader =
    new FileReader("data.txt");
```

Compilation error

```
Unhandled exception:
FileNotFoundException
```

______________________________________________________________________

# Handling Checked Exceptions

```java
try {

    FileReader reader =
        new FileReader("data.txt");

} catch (FileNotFoundException e) {

    System.out.println("File not found");

}
```

______________________________________________________________________

# Unchecked Exceptions

Unchecked exceptions extend

```java
RuntimeException
```

Compiler does not force handling.

Example

```java
int[] arr = {1,2,3};

System.out.println(arr[10]);
```

Output

```
ArrayIndexOutOfBoundsException
```

______________________________________________________________________

# Common Runtime Exceptions

| Exception | Cause |
|-----------|-------|
| NullPointerException | Using null reference |
| ArithmeticException | Divide by zero |
| IllegalArgumentException | Invalid argument |
| NumberFormatException | Invalid number conversion |
| IndexOutOfBoundsException | Invalid index |
| ClassCastException | Invalid casting |

These are some of the most common interview questions.

______________________________________________________________________

# try-catch

Basic syntax

```java
try {

    int result = 10 / 0;

} catch (ArithmeticException e) {

    System.out.println("Cannot divide by zero");

}
```

Output

```
Cannot divide by zero
```

Program continues.

______________________________________________________________________

# Execution Flow

```
try

↓

Exception?

↓

Yes

↓

Matching catch

↓

Continue
```

If no exception occurs,

the catch block is skipped.

______________________________________________________________________

# Multiple catch Blocks

```java
try {

    int[] arr = {1};

    System.out.println(arr[5]);

} catch (ArithmeticException e) {

    System.out.println("Math Error");

} catch (ArrayIndexOutOfBoundsException e) {

    System.out.println("Invalid Index");

}
```

Java executes the first matching catch block.

______________________________________________________________________

# Catching Parent Exception

Wrong order

```java
try {

} catch (Exception e) {

} catch (ArithmeticException e) {

}
```

Compilation error.

Because

```
Exception
```

already catches everything.

Correct

```java
try {

} catch (ArithmeticException e) {

} catch (Exception e) {

}
```

Always catch specific exceptions first.

______________________________________________________________________

# finally

The finally block executes whether an exception occurs or not.

```java
try {

    System.out.println("Try");

} finally {

    System.out.println("Finally");

}
```

Output

```
Try

Finally
```

______________________________________________________________________

# finally with Exception

```java
try {

    int x = 10 / 0;

} catch (ArithmeticException e) {

    System.out.println("Error");

} finally {

    System.out.println("Cleanup");

}
```

Output

```
Error

Cleanup
```

Useful for releasing resources.

______________________________________________________________________

# throw

Used to manually throw an exception.

```java
public void withdraw(double amount){

    if(amount < 0){

        throw new IllegalArgumentException(
            "Amount cannot be negative");

    }

}
```

______________________________________________________________________

# throws

Declares that a method may throw an exception.

```java
public void readFile()
    throws IOException {

}
```

The caller must handle it.

______________________________________________________________________

# throw vs throws

`throw`

Throws an exception.

```java
throw new RuntimeException();
```

______________________________________________________________________

`throws`

Declares an exception.

```java
void test()
throws IOException
```

Very common interview question.

______________________________________________________________________

# Propagation

Exceptions move upward through the call stack.

Example

```java
void c(){

    throw new RuntimeException();

}

void b(){

    c();

}

void a(){

    b();

}
```

If

`a()`

doesn't handle it,

the JVM eventually handles it.

______________________________________________________________________

# Stack Trace

Example

```java
Exception in thread "main"

java.lang.NullPointerException

at Test.c()

at Test.b()

at Test.a()
```

Read from top to bottom.

It shows exactly where the exception occurred.

Learning to read stack traces is an essential backend skill.

______________________________________________________________________

# try-with-resources

One of the best Java features.

Without it

```java
FileReader reader = null;

try {

    reader = new FileReader("test.txt");

} finally {

    if(reader != null){

        reader.close();

    }

}
```

______________________________________________________________________

With try-with-resources

```java
try(FileReader reader =
        new FileReader("test.txt")){

    // use reader

}
```

Java automatically closes the resource.

Cleaner.

Safer.

Preferred.

______________________________________________________________________

# AutoCloseable

Try-with-resources works with classes implementing

```java
AutoCloseable
```

Examples

- FileReader
- BufferedReader
- InputStream
- OutputStream
- Scanner
- Connection

______________________________________________________________________

# Custom Exceptions

Sometimes built-in exceptions aren't enough.

Example

```java
class InsufficientBalanceException
        extends Exception {

    public InsufficientBalanceException(
        String message){

        super(message);

    }

}
```

Usage

```java
if(balance < amount){

    throw new InsufficientBalanceException(
        "Not enough balance");

}
```

______________________________________________________________________

# Checked vs Runtime Custom Exceptions

Checked

```java
extends Exception
```

Caller must handle.

______________________________________________________________________

Unchecked

```java
extends RuntimeException
```

Caller may handle.

______________________________________________________________________

# When to Use RuntimeException

Good examples

- Invalid arguments
- Invalid state
- Programming errors
- Null values

______________________________________________________________________

# When to Use Checked Exceptions

Good examples

- File operations
- Database access
- Network communication
- External services

If the caller can reasonably recover,

a checked exception is often appropriate.

______________________________________________________________________

# Exception Chaining

Wrap one exception inside another.

```java
try {

    // database operation

} catch(SQLException e){

    throw new RuntimeException(
        "Database failed", e);

}
```

Useful because the original cause is preserved.

______________________________________________________________________

# Best Practices

## Catch Specific Exceptions

Bad

```java
catch(Exception e)
```

Good

```java
catch(IOException e)
```

______________________________________________________________________

## Never Ignore Exceptions

Wrong

```java
catch(Exception e){

}
```

Silent failures are difficult to debug.

______________________________________________________________________

## Preserve the Cause

Good

```java
throw new RuntimeException(
    "Payment failed", e);
```

______________________________________________________________________

## Use Meaningful Messages

Bad

```java
throw new RuntimeException();
```

Good

```java
throw new RuntimeException(
    "Customer ID not found");
```

______________________________________________________________________

## Don't Use Exceptions for Normal Flow

Bad

```java
try{

    list.get(100);

}catch(Exception e){

}
```

Better

```java
if(index < list.size()){

}
```

Exceptions should represent exceptional situations.

______________________________________________________________________

# Common Mistakes

## Catching Exception Everywhere

Avoid

```java
catch(Exception e)
```

unless absolutely necessary.

______________________________________________________________________

## Swallowing Exceptions

Never

```java
catch(Exception e){

}
```

At least

- log it
- rethrow it
- handle it

______________________________________________________________________

## Throwing Generic Exception

Avoid

```java
throw new Exception();
```

Prefer specific exception types.

______________________________________________________________________

## Printing Stack Trace in Production

Avoid

```java
e.printStackTrace();
```

Use a logging framework instead.

Example

```java
logger.error("Payment failed", e);
```

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between checked and unchecked exceptions?

### Answer

Checked exceptions are verified at compile time, and the compiler requires them to be either handled using a `try-catch`
block or declared using `throws`. They typically represent recoverable conditions such as file or network failures.

Unchecked exceptions extend `RuntimeException`. The compiler does not require them to be handled. They usually represent
programming errors such as null references, invalid arguments, or array index issues.

______________________________________________________________________

## Question

What is the difference between `throw` and `throws`?

### Answer

`throw` is used to explicitly throw an exception from within a method.

`throws` is used in a method signature to declare that the method may throw one or more exceptions, leaving the
responsibility of handling them to the caller.

______________________________________________________________________

## Question

What is the purpose of the `finally` block?

### Answer

The `finally` block contains cleanup code that executes regardless of whether an exception occurs. It is commonly used
to release resources such as files, database connections, or network sockets.

______________________________________________________________________

## Question

Why is try-with-resources preferred?

### Answer

Try-with-resources automatically closes resources that implement `AutoCloseable`, reducing boilerplate code and
preventing resource leaks. It is safer and cleaner than manually closing resources in a `finally` block.

______________________________________________________________________

## Question

Why should we avoid catching `Exception`?

### Answer

Catching the generic `Exception` class hides the specific cause of failures, makes debugging harder, and can
unintentionally catch exceptions that should be handled differently. It's better to catch the most specific exception
possible.

______________________________________________________________________

# Practice Questions

1. What is an exception?
1. What is the difference between `Error` and `Exception`?
1. What is the difference between checked and unchecked exceptions?
1. Explain `try`, `catch`, and `finally`.
1. What is the difference between `throw` and `throws`?
1. What is exception propagation?
1. What is a stack trace?
1. What is try-with-resources?
1. When should you create a custom exception?
1. Why should you avoid swallowing exceptions?

______________________________________________________________________

# Summary

Exception handling is about building reliable applications that fail gracefully and recover when possible.

In this chapter, you learned:

- Exception hierarchy
- Checked vs unchecked exceptions
- `try`, `catch`, and `finally`
- `throw` vs `throws`
- Exception propagation
- Stack traces
- Try-with-resources
- Custom exceptions
- Exception handling best practices

Mastering exception handling is essential because every production Java application interacts with databases, files,
APIs, and external systems where failures are inevitable. The goal is not to prevent every failure, but to handle
failures cleanly, communicate them clearly, and keep the application stable.

______________________________________________________________________

# Next

[Collections Framework](08-collections-framework.md)

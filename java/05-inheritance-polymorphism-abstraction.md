# Inheritance, Polymorphism & Abstraction

These three concepts are at the heart of Object-Oriented Programming.

Nearly every Java interview includes questions on them because they form the basis of framework design, reusable code,
and runtime behavior.

Frameworks like Spring Boot, Hibernate, and even the Java Collections Framework make extensive use of inheritance,
interfaces, and polymorphism.

______________________________________________________________________

# Inheritance

Inheritance allows one class to acquire the properties and behavior of another class.

Instead of rewriting common code, we reuse it.

Example

```java
class Animal {

    void eat() {
        System.out.println("Eating...");
    }

}
```

```java
class Dog extends Animal {

    void bark() {
        System.out.println("Barking...");
    }

}
```

Usage

```java
Dog dog = new Dog();

dog.eat();

dog.bark();
```

Output

```
Eating...

Barking...
```

Dog inherited `eat()` from Animal.

______________________________________________________________________

# Why Use Inheritance?

Without inheritance

```java
class Dog {

    void eat(){}

}

class Cat {

    void eat(){}

}

class Lion {

    void eat(){}

}
```

Duplicate code.

With inheritance

```java
class Animal {

    void eat(){}

}

class Dog extends Animal {}

class Cat extends Animal {}

class Lion extends Animal {}
```

Cleaner.

Reusable.

Maintainable.

______________________________________________________________________

# Terminology

```
Animal
```

Parent Class

Base Class

Superclass

```
Dog
```

Child Class

Derived Class

Subclass

All mean the same thing.

______________________________________________________________________

# extends Keyword

Inheritance uses

```java
extends
```

Example

```java
class Vehicle {

}

class Car extends Vehicle {

}
```

Java supports only **single inheritance** for classes.

A class cannot extend multiple classes.

This is illegal

```java
class C extends A, B {

}
```

______________________________________________________________________

# Constructor Execution

Parent constructors execute first.

Example

```java
class Animal {

    Animal() {
        System.out.println("Animal");
    }

}
```

```java
class Dog extends Animal {

    Dog() {
        System.out.println("Dog");
    }

}
```

Usage

```java
new Dog();
```

Output

```
Animal

Dog
```

______________________________________________________________________

# super()

`super`

refers to the parent class.

Calling parent constructor

```java
class Animal {

    Animal(String type){

    }

}
```

```java
class Dog extends Animal {

    Dog(){

        super("Dog");

    }

}
```

`super()` must be the first statement.

______________________________________________________________________

# Accessing Parent Members

```java
class Animal {

    String type = "Animal";

}
```

```java
class Dog extends Animal {

    void print() {

        System.out.println(super.type);

    }

}
```

______________________________________________________________________

# Method Overriding

One of the most important interview topics.

Parent

```java
class Animal {

    void sound() {
        System.out.println("Animal Sound");
    }

}
```

Child

```java
class Dog extends Animal {

    @Override
    void sound() {
        System.out.println("Bark");
    }

}
```

Usage

```java
Dog dog = new Dog();

dog.sound();
```

Output

```
Bark
```

______________________________________________________________________

# @Override

Always use

```java
@Override
```

Benefits

- Compile-time validation
- Better readability
- Prevents accidental mistakes

______________________________________________________________________

# Rules of Overriding

Same method name

✔

Same parameters

✔

Compatible return type

✔

Cannot reduce visibility

✔

Cannot override final methods

✔

Cannot override static methods

✔

______________________________________________________________________

# Method Overloading vs Overriding

Overloading

```java
class MathUtil {

    int add(int a,int b){}

    double add(double a,double b){}

}
```

Same class.

Different parameters.

Compile-time.

______________________________________________________________________

Overriding

```java
class Animal {

    void sound(){}

}

class Dog extends Animal {

    @Override

    void sound(){}

}
```

Different classes.

Same method signature.

Runtime.

______________________________________________________________________

# Polymorphism

Polymorphism means

> One interface, many implementations.

The same method behaves differently depending on the object.

Example

```java
class Animal {

    void sound() {
        System.out.println("Animal");
    }

}
```

```java
class Dog extends Animal {

    @Override
    void sound() {
        System.out.println("Bark");
    }

}
```

```java
class Cat extends Animal {

    @Override
    void sound() {
        System.out.println("Meow");
    }

}
```

______________________________________________________________________

# Runtime Polymorphism

```java
Animal a1 = new Dog();

Animal a2 = new Cat();

a1.sound();

a2.sound();
```

Output

```
Bark

Meow
```

Notice

The variable type is

```java
Animal
```

But Java executes the correct implementation.

This is **Dynamic Method Dispatch**.

______________________________________________________________________

# Dynamic Method Dispatch

Java determines which overridden method to execute **at runtime**, not compile time.

```
Reference Type

↓

Actual Object

↓

Correct Method Executes
```

One of the most frequently asked interview questions.

______________________________________________________________________

# Upcasting

Converting child to parent.

```java
Dog dog = new Dog();

Animal animal = dog;
```

or

```java
Animal animal = new Dog();
```

Automatic.

Safe.

No cast required.

______________________________________________________________________

# Why Upcasting?

Allows generic code.

Example

```java
void makeSound(Animal animal){

    animal.sound();

}
```

Now

```java
makeSound(new Dog());

makeSound(new Cat());
```

No duplicate methods.

______________________________________________________________________

# Downcasting

Parent to child.

```java
Animal animal = new Dog();

Dog dog = (Dog) animal;
```

Requires explicit casting.

______________________________________________________________________

# Dangerous Downcasting

```java
Animal animal = new Animal();

Dog dog = (Dog) animal;
```

Compiles.

Fails at runtime.

```
ClassCastException
```

______________________________________________________________________

# instanceof

Safely check before downcasting.

```java
if(animal instanceof Dog){

    Dog dog = (Dog) animal;

}
```

Recommended.

______________________________________________________________________

# Object Class

Every Java class automatically extends

```java
Object
```

Even if you don't write it.

Example

```java
class Employee {

}
```

Actually becomes

```java
class Employee extends Object {

}
```

______________________________________________________________________

# Important Object Methods

Every class inherits

```java
toString()

equals()

hashCode()

getClass()

clone()

wait()

notify()

notifyAll()
```

You'll override several of these regularly.

______________________________________________________________________

# Abstraction

Abstraction means

> Show only essential behavior while hiding implementation details.

Example

Driving a car.

You use

- Steering
- Brake
- Accelerator

You don't need to know how the engine works.

That's abstraction.

______________________________________________________________________

# Abstract Class

Example

```java
abstract class Animal {

    abstract void sound();

}
```

Cannot create objects.

Wrong

```java
Animal animal = new Animal();
```

Compilation error.

______________________________________________________________________

# Concrete Class

```java
class Dog extends Animal {

    @Override
    void sound() {

        System.out.println("Bark");

    }

}
```

Now

```java
Dog dog = new Dog();
```

Works.

______________________________________________________________________

# Abstract Method

No implementation.

```java
abstract void sound();
```

Child classes must implement it.

______________________________________________________________________

# Abstract Class Can Have Normal Methods

```java
abstract class Animal {

    void eat(){

        System.out.println("Eating");

    }

    abstract void sound();

}
```

Perfectly valid.

______________________________________________________________________

# When To Use Abstract Classes

Good when

- Common implementation exists.
- Common fields exist.
- Some methods are shared.
- Some methods vary.

______________________________________________________________________

# Real Example

```java
abstract class Payment {

    void validate() {
        System.out.println("Validation");
    }

    abstract void pay();

}
```

```java
class CreditCardPayment extends Payment {

    @Override
    void pay() {

        System.out.println("Paid using Credit Card");

    }

}
```

```java
class UpiPayment extends Payment {

    @Override
    void pay() {

        System.out.println("Paid using UPI");

    }

}
```

______________________________________________________________________

# Final Keyword

Prevent inheritance.

```java
final class Utility {

}
```

Cannot extend.

______________________________________________________________________

Prevent overriding.

```java
class Animal {

    final void eat(){

    }

}
```

Child cannot override.

______________________________________________________________________

# Composition vs Inheritance

Very important interview topic.

Inheritance

```
Car

↓

Vehicle
```

"is-a"

Relationship.

______________________________________________________________________

Composition

```
Car

↓

Engine
```

"has-a"

Relationship.

Example

```java
class Engine {

}
```

```java
class Car {

    private Engine engine = new Engine();

}
```

Most modern applications prefer **composition** because it provides better flexibility and lower coupling.

A common interview phrase is:

> **Favor Composition over Inheritance.**

______________________________________________________________________

# Common Mistakes

## Confusing Overloading and Overriding

Overloading

Same class.

Different parameters.

Overriding

Child class.

Same signature.

______________________________________________________________________

## Downcasting Without Checking

Wrong

```java
Dog dog = (Dog) animal;
```

Always use

```java
instanceof
```

when appropriate.

______________________________________________________________________

## Using Inheritance Everywhere

Not every relationship is inheritance.

Sometimes composition is a better design.

______________________________________________________________________

## Forgetting @Override

Always use it.

The compiler catches mistakes early.

______________________________________________________________________

# Best Practices

✅ Prefer composition over inheritance.

✅ Use `@Override`.

✅ Keep inheritance hierarchies shallow.

✅ Program to abstractions.

✅ Use polymorphism to eliminate `if-else` chains.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between method overloading and method overriding?

### Answer

Method overloading occurs within the same class by defining multiple methods with the same name but different parameter
lists. It is resolved at compile time.

Method overriding occurs when a subclass provides its own implementation of a method defined in its parent class using
the same method signature. It is resolved at runtime through dynamic method dispatch.

______________________________________________________________________

## Question

What is runtime polymorphism?

### Answer

Runtime polymorphism occurs when a parent reference points to a child object, and the JVM decides which overridden
method to execute at runtime based on the actual object type rather than the reference type.

______________________________________________________________________

## Question

Why is Java called a single inheritance language?

### Answer

Java allows a class to extend only one parent class. This avoids problems like the Diamond Problem found in multiple
inheritance. However, Java supports multiple inheritance of behavior through interfaces.

______________________________________________________________________

## Question

What is the difference between abstraction and encapsulation?

### Answer

Abstraction focuses on exposing only the essential behavior while hiding implementation details.

Encapsulation focuses on protecting an object's internal state by restricting direct access and controlling
modifications through methods.

______________________________________________________________________

## Question

Why is composition generally preferred over inheritance?

### Answer

Composition creates loosely coupled designs where objects collaborate instead of depending on rigid inheritance
hierarchies. It improves flexibility, testability, and maintainability while avoiding many inheritance-related issues.

______________________________________________________________________

# Practice Questions

1. What is inheritance?
1. What is method overriding?
1. What is runtime polymorphism?
1. What is dynamic method dispatch?
1. What is upcasting?
1. What is downcasting?
1. What is `instanceof`?
1. What is abstraction?
1. What is the difference between abstraction and encapsulation?
1. Why is composition preferred over inheritance?

______________________________________________________________________

# Summary

Inheritance, polymorphism, and abstraction enable Java developers to build flexible, reusable, and maintainable
applications.

In this chapter, you learned:

- Inheritance with `extends`
- `super`
- Method overriding
- Runtime polymorphism
- Dynamic method dispatch
- Upcasting and downcasting
- `instanceof`
- The `Object` class
- Abstract classes and methods
- Composition vs inheritance

These concepts form the backbone of object-oriented design and are heavily used throughout the Java ecosystem. In the
next chapter, we'll explore **Interfaces vs Abstract Classes**, one of the highest-frequency Java interview topics and a
cornerstone of modern Java application design.

______________________________________________________________________

# Next

[Interfaces vs Abstract Classes](06-interfaces-vs-abstract-classes.md)

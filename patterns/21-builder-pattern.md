# Software Design & Design Patterns - Part 21

# Builder Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Builder Pattern is
- Why the Builder Pattern exists
- The problem it solves
- Fluent interfaces
- Method chaining
- Real-world backend examples
- FastAPI and SQLAlchemy examples
- When NOT to use the Builder Pattern

______________________________________________________________________

# Before We Start

Imagine you're ordering a pizza.

Sometimes you want:

- Small
- Thin crust
- Cheese

Sometimes:

- Large
- Stuffed crust
- Extra cheese
- Mushrooms
- Olives

Would you create

a constructor like this?

```python
Pizza(

    size,

    crust,

    cheese,

    olives,

    mushrooms,

    onions,

    pepperoni,

    extra_cheese,

    sauce,

    ...
)
```

Probably not.

This is exactly

the kind of problem

the Builder Pattern solves.

______________________________________________________________________

# The Problem

Let's continue with our

**Library Management System**.

We want

to generate

a borrowing report.

The report

contains

many optional fields.

A developer writes

```python
class Report:

    def __init__(

        self,

        title,

        include_books,

        include_members,

        include_fines,

        include_statistics,

        include_graphs,

        include_history,

        export_pdf,

        export_excel,

        watermark,

    ):
        ...
```

______________________________________________________________________

# What's the Problem?

The constructor

has become

huge.

Problems:

❌ Hard to read

❌ Hard to remember

❌ Many optional parameters

❌ Easy to pass arguments incorrectly

Imagine

this call.

```python
Report(

    "Monthly",

    True,

    False,

    True,

    False,

    True,

    False,

    True,

    False,

    "CONFIDENTIAL",
)
```

Can you immediately

tell

what each

`True`

or

`False`

means?

Probably not.

______________________________________________________________________

# Another Problem

Tomorrow,

the business

adds

another option.

```python
include_recommendations
```

Now,

every place

creating

a Report

must change.

______________________________________________________________________

# The Idea

Instead of

passing

everything

to the constructor,

build

the object

step by step.

______________________________________________________________________

# What is the Builder Pattern?

The **Builder Pattern** says:

> **Separate the construction of a complex object from its representation.**

Instead of

one massive constructor,

use

small methods

to configure

the object.

______________________________________________________________________

# Without Builder

```text
Constructor

↓

10 Parameters
```

______________________________________________________________________

# With Builder

```text
Report Builder

↓

Title

↓

Statistics

↓

Graphs

↓

Export PDF

↓

Build
```

Much easier

to understand.

______________________________________________________________________

# Step 1

Create

the object.

```python
class Report:

    def __init__(self):

        self.title = None

        self.include_books = False

        self.include_graphs = False

        self.export_pdf = False
```

______________________________________________________________________

# Step 2

Create

the builder.

```python
class ReportBuilder:

    def __init__(self):

        self.report = Report()
```

______________________________________________________________________

# Step 3

Add

configuration methods.

```python
class ReportBuilder:

    def title(
        self,
        title,
    ):

        self.report.title = title

        return self
```

Notice

the return value.

```python
return self
```

This enables

method chaining.

______________________________________________________________________

# More Builder Methods

```python
def include_books(self):

    self.report.include_books = True

    return self
```

```python
def export_pdf(self):

    self.report.export_pdf = True

    return self
```

______________________________________________________________________

# Final Step

```python
def build(self):

    return self.report
```

______________________________________________________________________

# Using the Builder

```python
report = (

    ReportBuilder()

    .title("Monthly Report")

    .include_books()

    .export_pdf()

    .build()

)
```

Notice

how readable

the code becomes.

______________________________________________________________________

# Fluent Interface

The Builder Pattern

often uses

a

**Fluent Interface**.

Meaning

every method

returns

the object itself.

Example

```python
builder

.title(...)

.export_pdf()

.include_books()

.build()
```

This is called

method chaining.

______________________________________________________________________

# SQLAlchemy Example

You've already used

the Builder Pattern.

Example

```python
query = (

    session

    .query(Book)

    .filter(Book.id == 1)

    .order_by(Book.title)

    .limit(10)

)
```

Every method

returns

the query object.

This is

a Builder-style API.

______________________________________________________________________

# FastAPI Example

FastAPI

also uses

a fluent style

in many places.

Example

```python
app.include_router(
    router
)
```

Libraries such as

Pydantic,

SQLAlchemy,

and LangChain

frequently expose

Builder-like APIs

to make configuration

more readable.

______________________________________________________________________

# AI/ML Example

Suppose

you're configuring

an LLM.

Instead of

```python
Model(

    temperature,

    max_tokens,

    top_p,

    timeout,

    retries,

    streaming,

)
```

You could write

```python
model = (

    ModelBuilder()

    .temperature(0.7)

    .max_tokens(500)

    .streaming(True)

    .build()

)
```

This is easier

to read

and extend.

______________________________________________________________________

# Builder vs Constructor

| Constructor | Builder |
| ----------------- | ------------------------ |
| Few parameters | Many optional parameters |
| Simple objects | Complex objects |
| One-step creation | Step-by-step creation |
| Hard to extend | Easy to extend |

______________________________________________________________________

# Builder vs Factory

Another common

interview question.

| Factory | Builder |
| ------------------------------ | --------------------------------- |
| Chooses which object to create | Configures how an object is built |
| Returns ready-made objects | Builds objects step by step |
| Focuses on creation logic | Focuses on configuration |

Example

```text
Factory

↓

Create Car
```

Builder

↓

Configure Car

↓

Color

↓

Engine

↓

Seats

↓

Build

______________________________________________________________________

# Benefits

Builder gives you:

✅ Readable code

✅ No huge constructors

✅ Easy extension

✅ Fluent APIs

✅ Optional configuration

______________________________________________________________________

# Drawbacks

Builder also introduces:

❌ More classes

❌ More code

❌ Unnecessary complexity

for simple objects.

______________________________________________________________________

# When NOT to Use Builder

Suppose

your class

contains

three required fields.

```python
Book(

    title,

    author,

    isbn,
)
```

A Builder

would only

make the code

longer.

Use Builder

when objects

have many

optional settings

or complicated

construction logic.

______________________________________________________________________

# Best Practices

✅ Use Builder for complex object construction.

✅ Keep builder methods focused.

✅ Return `self` for method chaining.

✅ Validate required fields inside `build()`.

______________________________________________________________________

# Common Mistakes

### Using Builder for Simple Objects

Not every class

needs a builder.

______________________________________________________________________

### Skipping Validation

The `build()`

method

should verify

that all required fields

are present.

______________________________________________________________________

### Mixing Business Logic

Builders

construct objects.

They should not

execute business workflows.

______________________________________________________________________

### Returning Incomplete Objects

Always ensure

`build()`

returns

a valid object.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Builder Pattern, and when should you use it?

The Builder Pattern is a creational design pattern that constructs complex objects step by step instead of using large
constructors with many parameters. It is especially useful when objects have numerous optional fields or require a
sequence of configuration steps. Builder often supports fluent interfaces through method chaining, making object
creation more readable and maintainable. Libraries such as SQLAlchemy demonstrate Builder-style APIs through chained
query construction.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Builder Pattern is
- Why it exists
- Fluent interfaces
- Method chaining
- SQLAlchemy example
- FastAPI example
- AI/ML example
- Builder vs Factory
- Builder vs Constructor
- Best practices

______________________________________________________________________

# What's Next

[Facade Pattern](22-facade-pattern.md)

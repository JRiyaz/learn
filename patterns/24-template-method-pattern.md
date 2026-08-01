# Software Design & Design Patterns - Part 24

# Template Method Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Template Method Pattern is
- Why the Template Method Pattern exists
- The problem it solves
- Fixed workflow vs customizable steps
- Real-world backend examples
- FastAPI examples
- AI/ML examples
- Template Method vs Strategy
- When NOT to use the Template Method Pattern

______________________________________________________________________

# Before We Start

Imagine

your library supports

different ways

to import books.

- CSV
- Excel
- JSON

Although

the file formats

are different,

the workflow

is always the same.

```text id="tmp2401"
Read File

↓

Validate

↓

Transform

↓

Save Database

↓

Generate Report
```

Only

some steps

change.

This is exactly

what the Template Method Pattern solves.

______________________________________________________________________

# The Problem

A developer writes

three classes.

CSV

```python id="tmp2402"
class CSVImporter:

    def import_books(self):

        read_csv()

        validate()

        transform()

        save()

        report()
```

Excel

```python id="tmp2403"
class ExcelImporter:

    def import_books(self):

        read_excel()

        validate()

        transform()

        save()

        report()
```

JSON

```python id="tmp2404"
class JSONImporter:

    def import_books(self):

        read_json()

        validate()

        transform()

        save()

        report()
```

______________________________________________________________________

# What's the Problem?

Almost

every line

is duplicated.

Only

the reading step

changes.

Tomorrow,

the business says

every import

must also:

- Write audit logs
- Send notifications

Now,

three classes

must change.

______________________________________________________________________

# The Idea

Move

the common workflow

into

one base class.

Allow

child classes

to customize

only

the steps

that differ.

______________________________________________________________________

# What is the Template Method Pattern?

The **Template Method Pattern** says:

> **Define the skeleton of an algorithm in a base class while allowing subclasses to override specific steps.**

The workflow

stays fixed.

Individual steps

remain customizable.

______________________________________________________________________

# The Workflow

```text id="tmp2405"
Read

↓

Validate

↓

Transform

↓

Save

↓

Report
```

Every importer

follows

this sequence.

______________________________________________________________________

# Step 1

Create

the template.

```python id="tmp2406"
from abc import (
    ABC,
    abstractmethod,
)

class Importer(
    ABC
):

    def import_books(self):

        self.read()

        self.validate()

        self.transform()

        self.save()

        self.report()
```

Notice

the algorithm

is fixed.

______________________________________________________________________

# Step 2

Allow

customization.

```python id="tmp2407"
class Importer(
    ABC
):

    @abstractmethod
    def read(self):
        ...
```

______________________________________________________________________

# Step 3

Provide

default behavior.

```python id="tmp2408"
def validate(self):

    print(
        "Validation"
    )
```

```python id="tmp2409"
def save(self):

    print(
        "Saved"
    )
```

```python id="tmp2410"
def report(self):

    print(
        "Report Generated"
    )
```

______________________________________________________________________

# Step 4

CSV Importer

```python id="tmp2411"
class CSVImporter(
    Importer
):

    def read(self):

        print(
            "Reading CSV"
        )
```

______________________________________________________________________

# Step 5

JSON Importer

```python id="tmp2412"
class JSONImporter(
    Importer
):

    def read(self):

        print(
            "Reading JSON"
        )
```

______________________________________________________________________

# Using It

```python id="tmp2413"
CSVImporter().import_books()
```

Output

```text id="tmp2414"
Reading CSV

Validation

Saved

Report Generated
```

Tomorrow,

run

```python id="tmp2415"
JSONImporter()
```

Same workflow.

Different implementation.

______________________________________________________________________

# Another Backend Example

Suppose

your application

supports

different authentication providers.

Workflow

is always

```text id="tmp2416"
Validate Request

↓

Authenticate

↓

Generate Token

↓

Audit
```

Only

the authentication step

changes.

______________________________________________________________________

# AI/ML Example

Suppose

your application

supports

multiple models.

Every prediction

follows

the same pipeline.

```text id="tmp2417"
Preprocess

↓

Predict

↓

Postprocess

↓

Log Metrics
```

The

`predict()`

method

changes

between models.

Everything else

stays identical.

______________________________________________________________________

# FastAPI Example

Suppose

you have

multiple report generators.

Workflow

```text id="tmp2418"
Authenticate

↓

Load Data

↓

Generate Report

↓

Upload

↓

Notify User
```

Different reports

override

only

the generation step.

______________________________________________________________________

# Hooks

The Template Method Pattern

often introduces

**Hooks**.

Hooks

are optional methods

that child classes

may override.

Example

```python id="tmp2419"
def before_save(self):
    pass
```

Some importers

override it.

Others don't.

Hooks provide

customization

without changing

the workflow.

______________________________________________________________________

# Template Method vs Strategy

This interview question

appears frequently.

| Template Method | Strategy |
| ---------------------------- | -------------------------- |
| Uses inheritance | Uses composition |
| Fixed workflow | Replaceable algorithms |
| Base class controls sequence | Context delegates behavior |

Template Method

↓

Same workflow

Different steps

Strategy

↓

Different algorithms

Chosen at runtime

______________________________________________________________________

# Real Backend Example

Suppose

every payment

requires

```text id="tmp2420"
Validate

↓

Authorize

↓

Process

↓

Audit
```

Stripe

implements

its own

authorization.

PayPal

implements

a different

authorization.

The workflow

never changes.

______________________________________________________________________

# Benefits

Template Method gives you:

✅ Eliminates duplicated workflows

✅ Enforces processing order

✅ Easy customization

✅ Cleaner inheritance

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Inheritance coupling

❌ Less flexibility

than Strategy

❌ Harder runtime changes

______________________________________________________________________

# Real Company Example

Suppose

Netflix

supports

multiple video encoders.

Workflow

```text id="tmp2421"
Read Video

↓

Encode

↓

Generate Thumbnail

↓

Upload

↓

Notify
```

Different codecs

override

the encoding step.

Everything else

remains identical.

______________________________________________________________________

# When NOT to Use Template Method

Suppose

every implementation

has

a completely

different workflow.

Then

forcing

inheritance

creates

more problems

than it solves.

Strategy

is often

the better choice.

______________________________________________________________________

# Best Practices

✅ Keep the template method stable.

✅ Override only necessary steps.

✅ Use hooks for optional behavior.

✅ Avoid changing the workflow frequently.

______________________________________________________________________

# Common Mistakes

### Overriding the Entire Template

If every subclass

rewrites

the entire algorithm,

Template Method

provides

little value.

______________________________________________________________________

### Too Many Hooks

Hooks

should remain

optional,

not become

required customization.

______________________________________________________________________

### Confusing Strategy with Template

Template Method

uses inheritance.

Strategy

uses composition.

______________________________________________________________________

### Making the Base Class Too Large

Keep the template

focused

on one workflow.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Template Method Pattern, and when should you use it?

The Template Method Pattern is a behavioral design pattern that defines the overall structure of an algorithm in a base
class while allowing subclasses to customize specific steps. It is useful when multiple implementations share the same
workflow but differ in only a few operations. Common use cases include data import pipelines, authentication workflows,
report generation, and machine learning inference pipelines. Unlike the Strategy Pattern, Template Method relies on
inheritance rather than composition.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Template Method Pattern is
- Why it exists
- Fixed workflows
- Hooks
- Backend examples
- FastAPI example
- AI/ML example
- Template vs Strategy
- Best practices

______________________________________________________________________

# What's Next

[Chain of Responsibility Pattern](25-chain-of-responsibility-pattern.md)

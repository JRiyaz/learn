# Software Design & Design Patterns - Part 29

# CQRS (Command Query Responsibility Segregation)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What CQRS is
- Why CQRS exists
- The problems it solves
- Commands vs Queries
- Read Models and Write Models
- Real-world backend examples
- FastAPI examples
- Event-Driven Architecture integration
- When NOT to use CQRS

______________________________________________________________________

# Before We Start

Imagine

our **Library Management System**.

Users perform

two very different kinds

of operations.

## Write Operations

- Add Book
- Borrow Book
- Return Book
- Pay Fine

These

change

the system.

______________________________________________________________________

## Read Operations

- Search Books
- View Borrow History
- List Members
- View Analytics

These

only

retrieve data.

Should

both

be handled

by

the same model?

CQRS says

not necessarily.

______________________________________________________________________

# The Problem

A developer writes

one service.

```python id="cqrs2901"
class LibraryService:

    def add_book(self):
        ...

    def borrow_book(self):
        ...

    def return_book(self):
        ...

    def search_books(self):
        ...

    def list_members(self):
        ...

    def dashboard(self):
        ...
```

Everything

is mixed together.

______________________________________________________________________

# Another Problem

Suppose

borrowing a book

requires

many validations.

```text id="cqrs2902"
Validate Member

↓

Check Inventory

↓

Calculate Fine

↓

Update Database

↓

Publish Event
```

Searching books

needs

none

of these.

It simply

executes

a fast query.

Yet

both operations

share

the same layer.

______________________________________________________________________

# Another Problem

Your application

has

10 million books.

Users perform

100 writes

per minute.

But

500,000 searches

per minute.

Should

the read side

and

the write side

scale

together?

Probably not.

______________________________________________________________________

# The Idea

Separate

operations

that

modify data

from operations

that

read data.

______________________________________________________________________

# What is CQRS?

**CQRS**

stands for

**Command Query Responsibility Segregation.**

It says:

> **Separate commands (writes) from queries (reads).**

______________________________________________________________________

# Command

A command

changes state.

Examples:

- Create Book
- Borrow Book
- Delete Book
- Pay Fine

Commands

usually return

success,

failure,

or an identifier.

______________________________________________________________________

# Query

A query

does **not**

change state.

Examples:

- Search Books
- Get Book Details
- List Borrowed Books
- Dashboard

Queries

return data

and

should not

modify

the system.

______________________________________________________________________

# Traditional Architecture

```text id="cqrs2903"
API

↓

Service

↓

Repository

↓

Database
```

Both reads

and writes

use

the same path.

______________________________________________________________________

# CQRS Architecture

```text id="cqrs2904"
Commands

↓

Command Handler

↓

Write Database
```

```text id="cqrs2905"
Queries

↓

Query Handler

↓

Read Database
```

The two paths

are independent.

______________________________________________________________________

# Command Example

```python id="cqrs2906"
class BorrowBookCommand:

    def __init__(

        self,

        book_id,

        member_id,

    ):

        self.book_id = book_id

        self.member_id = member_id
```

______________________________________________________________________

# Command Handler

```python id="cqrs2907"
class BorrowBookHandler:

    def handle(

        self,

        command,

    ):

        print(
            "Borrowing Book"
        )
```

The handler

contains

business rules.

______________________________________________________________________

# Query Example

```python id="cqrs2908"
class SearchBooksQuery:

    def __init__(
        self,
        keyword,
    ):

        self.keyword = keyword
```

______________________________________________________________________

# Query Handler

```python id="cqrs2909"
class SearchBooksHandler:

    def handle(
        self,
        query,
    ):

        return [
            "Clean Code",
            "Design Patterns",
        ]
```

Notice

no business rules.

Only

data retrieval.

______________________________________________________________________

# Real Backend Example

Suppose

your write database

is

PostgreSQL.

```text id="cqrs2910"
Commands

↓

PostgreSQL
```

Searching books

uses

Elasticsearch.

```text id="cqrs2911"
Queries

↓

Elasticsearch
```

Each side

uses

the technology

best suited

for its workload.

______________________________________________________________________

# FastAPI Example

Commands

```python id="cqrs2912"
@app.post("/books")
```

↓

Create Book

Queries

```python id="cqrs2913"
@app.get("/books")
```

↓

Search Books

Different handlers.

Different responsibilities.

______________________________________________________________________

# Event-Driven Architecture

CQRS

is often combined

with events.

Example

```text id="cqrs2914"
Borrow Book

↓

Write Database

↓

Publish Event

↓

Update Search Index

↓

Update Analytics
```

The read model

is updated

asynchronously.

______________________________________________________________________

# Read Model

The read model

is optimized

for queries.

Example

```text id="cqrs2915"
Book

↓

Author

↓

Availability

↓

Rating
```

Everything needed

for searching

is already prepared.

No expensive joins

during requests.

______________________________________________________________________

# Write Model

The write model

is optimized

for correctness.

It focuses on:

- Validation
- Transactions
- Business rules
- Consistency

Not

fast searching.

______________________________________________________________________

# Real Company Example

Amazon

doesn't use

the same database design

for:

- Checkout
- Product Search

Checkout

requires

strong consistency.

Search

requires

speed.

CQRS

allows

each side

to evolve

independently.

______________________________________________________________________

# CQRS + Event Sourcing

CQRS

is frequently paired

with

Event Sourcing.

Commands

create events.

Queries

build

read models

from those events.

We'll study

Event Sourcing

next.

______________________________________________________________________

# CQRS vs CRUD

| CRUD | CQRS |
| ------------------------------- | ------------------------ |
| Same model for reads and writes | Separate models |
| Simple architecture | Specialized architecture |
| Easier to start | Better scalability |

______________________________________________________________________

# Benefits

CQRS gives you:

✅ Independent scaling

✅ Faster queries

✅ Cleaner business logic

✅ Better separation of responsibilities

✅ Flexible storage technologies

______________________________________________________________________

# Drawbacks

CQRS also introduces:

❌ More code

❌ More infrastructure

❌ Eventual consistency

❌ More operational complexity

______________________________________________________________________

# Eventual Consistency

One important concept.

Suppose

a user

borrows a book.

The write

succeeds immediately.

The search index

updates

two seconds later.

For a short time,

the read model

may not

reflect

the latest write.

This is called

**Eventual Consistency**.

Understanding this concept

is essential

when working

with CQRS.

______________________________________________________________________

# When NOT to Use CQRS

Don't use CQRS

for:

- Small CRUD applications
- Simple admin panels
- Personal projects
- Applications with minimal traffic

CQRS shines

when

read workloads

and write workloads

have

very different requirements.

______________________________________________________________________

# Best Practices

✅ Separate command and query handlers.

✅ Keep commands focused on business rules.

✅ Keep queries optimized for reads.

✅ Design read models for consumer needs.

______________________________________________________________________

# Common Mistakes

### Returning Large Objects from Commands

Commands

should generally

return

status

or identifiers,

not

complex read models.

______________________________________________________________________

### Business Logic Inside Queries

Queries

retrieve data.

Business rules

belong

to commands.

______________________________________________________________________

### Premature CQRS

Don't introduce

CQRS

before

the application

actually needs it.

______________________________________________________________________

### Ignoring Eventual Consistency

Teams

must understand

that read models

may briefly

lag behind

writes.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is CQRS, and when should you use it?

CQRS (Command Query Responsibility Segregation) is an architectural pattern that separates operations that modify data
(commands) from operations that read data (queries). Commands enforce business rules and update the write model, while
queries retrieve optimized read models without changing application state. CQRS is commonly used in large-scale systems
where read and write workloads differ significantly, often alongside Event-Driven Architecture and Event Sourcing. It
should generally be avoided in simple CRUD applications due to the added complexity.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What CQRS is
- Commands vs Queries
- Read and Write models
- FastAPI example
- Event-Driven integration
- Eventual consistency
- Benefits
- Common mistakes

______________________________________________________________________

# What's Next

[Event Sourcing](30-event-sourcing.md)

# Software Design & Design Patterns - Part 20

# Repository Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Repository Pattern is
- Why the Repository Pattern exists
- The problem it solves
- Repository vs Service vs Model
- Real-world backend examples
- FastAPI + SQLAlchemy implementation
- Testing with repositories
- When NOT to use the Repository Pattern

______________________________________________________________________

# Before We Start

If you're preparing for

Python Backend interviews,

this is one of

the most important patterns

you'll encounter.

You'll hear terms like:

- Repository
- DAO (Data Access Object)
- Data Layer
- Persistence Layer

Many companies

use these terms

slightly differently,

but the core idea

is the same.

______________________________________________________________________

# The Problem

Let's continue with our

**Library Management System**.

We create an endpoint.

```python id="rep2001"
@app.post("/books")
def create_book():

    ...
```

A junior developer writes

everything

inside the endpoint.

```python id="rep2002"
@app.post("/books")
def create_book(book):

    db.execute(...)

    db.commit()

    logger.info(...)

    cache.delete(...)

    return {
        "status": "success"
    }
```

Everything works.

______________________________________________________________________

# Another Endpoint

Now,

we also need

```text
GET /books
```

The developer writes

another query.

```python id="rep2003"
db.execute(
    "SELECT ..."
)
```

______________________________________________________________________

# Another Endpoint

```text
DELETE /books/{id}
```

Again,

another query.

______________________________________________________________________

# Six Months Later...

The application

contains

database queries

inside

every endpoint.

Problems:

❌ SQL duplicated everywhere

❌ Hard to test

❌ Business logic mixed with SQL

❌ Database changes affect many files

______________________________________________________________________

# Ask Yourself

Should

the endpoint

know

how SQL works?

Should

the service

know

whether

we use:

- PostgreSQL
- MySQL
- MongoDB

No.

Business logic

shouldn't care

about persistence details.

______________________________________________________________________

# The Idea

Separate

database access

into

its own layer.

The service

asks

for data.

The repository

knows

how to retrieve it.

______________________________________________________________________

# What is the Repository Pattern?

The **Repository Pattern** says:

> **Encapsulate data access behind a collection-like interface.**

In simple words,

the repository

hides

database details

from

the rest

of the application.

______________________________________________________________________

# Bad Architecture

```text id="rep2004"
Endpoint

↓

SQL

↓

Database
```

Every endpoint

contains SQL.

______________________________________________________________________

# Better Architecture

```text id="rep2005"
Endpoint

↓

Service

↓

Repository

↓

Database
```

Each layer

has

one responsibility.

______________________________________________________________________

# Responsibilities

## Endpoint

- Validate request
- Return response

______________________________________________________________________

## Service

- Business rules
- Business workflow

______________________________________________________________________

## Repository

- SQL
- ORM
- Database queries

______________________________________________________________________

## Database

- Store data

______________________________________________________________________

# Step 1

Create

the repository.

```python id="rep2006"
class BookRepository:

    def save(
        self,
        book,
    ):
        ...
```

______________________________________________________________________

# Step 2

Add methods.

```python id="rep2007"
class BookRepository:

    def save(self, book):
        ...

    def get_by_id(
        self,
        book_id,
    ):
        ...

    def delete(
        self,
        book_id,
    ):
        ...

    def list_books(self):
        ...
```

Notice

there is

no business logic.

Only

database operations.

______________________________________________________________________

# Step 3

Business Service

```python id="rep2008"
class LibraryService:

    def __init__(
        self,
        repository,
    ):

        self.repository = repository

    def borrow_book(
        self,
        book_id,
    ):

        book = self.repository.get_by_id(
            book_id
        )

        if not book:
            raise Exception(
                "Book Not Found"
            )

        # Business Rules

        self.repository.save(book)
```

Notice

the service

doesn't know

SQL.

______________________________________________________________________

# FastAPI Example

```python id="rep2009"
@app.post("/books")
def create_book(

    service=Depends(
        get_library_service
    ),

):
    service.add_book(...)
```

The endpoint

doesn't know

about

SQLAlchemy.

______________________________________________________________________

# SQLAlchemy Repository

Example

```python id="rep2010"
class BookRepository:

    def __init__(
        self,
        session,
    ):
        self.session = session

    def get_by_id(
        self,
        book_id,
    ):

        return (
            self.session
            .query(Book)
            .filter(
                Book.id == book_id
            )
            .first()
        )
```

Only

the repository

contains

ORM code.

______________________________________________________________________

# Another Example

Suppose

the database changes

from

PostgreSQL

to

MongoDB.

Which class changes?

Only

```text
BookRepository
```

Everything else

continues working.

______________________________________________________________________

# Repository vs Service

This question

appears frequently

in interviews.

| Repository | Service |
| ------------------- | --------------------- |
| Database operations | Business logic |
| SQL / ORM | Business workflow |
| CRUD | Business rules |
| Talks to database | Talks to repositories |

______________________________________________________________________

# Repository vs Model

Another common confusion.

```text
Book Model

↓

Represents data
```

```text
Book Repository

↓

Retrieves data
```

The model

is

the object.

The repository

finds

the object.

______________________________________________________________________

# Repository vs DAO

Some companies

use

DAO

(Data Access Object)

instead.

Simplified comparison:

| DAO | Repository |
| ------------- | -------------------------- |
| Low-level SQL | Domain-focused data access |
| Table-centric | Business entity-centric |

Many teams

use the terms

interchangeably.

Know both.

______________________________________________________________________

# Testing Becomes Easy

Without Repository

you need

a real database.

With Repository

inject

a fake one.

```python id="rep2011"
class FakeBookRepository:

    def get_by_id(
        self,
        book_id,
    ):

        return Book(
            id=1,
            title="Clean Code"
        )
```

Now

```python id="rep2012"
service = LibraryService(
    FakeBookRepository()
)
```

No database.

Fast tests.

______________________________________________________________________

# Real Backend Example

Suppose

our application

needs

to retrieve books.

Today

the data comes

from PostgreSQL.

Tomorrow

the company

uses Elasticsearch

for searching.

The service

still calls

```python id="rep2013"
repository.search_books(...)
```

Only

the repository

changes.

______________________________________________________________________

# Repository and SOLID

Repository

supports

multiple SOLID principles.

| Principle | Benefit |
| --------- | --------------------------------------- |
| SRP | Database logic separated |
| DIP | Service depends on abstraction |
| OCP | Easy to replace database implementation |

______________________________________________________________________

# Does Every Project Need Repositories?

No.

Suppose

you're writing

a small CRUD API

with

three endpoints.

Using repositories

may introduce

unnecessary layers.

As applications grow,

repositories

provide

significant benefits.

______________________________________________________________________

# Common Mistakes

### Putting Business Logic Inside Repository

Bad

```python id="rep2014"
def borrow_book():
    ...
```

Repositories

should not

contain

business rules.

______________________________________________________________________

### Returning HTTP Responses

Repositories

should never

know

about

FastAPI,

Flask,

or HTTP.

______________________________________________________________________

### Calling SQL from Services

Once SQL

starts appearing

inside services,

the architecture

begins to deteriorate.

______________________________________________________________________

### One Repository for Everything

Avoid

```python
Repository
```

that handles:

- Books
- Users
- Payments
- Orders

Create

focused repositories.

______________________________________________________________________

# Best Practices

✅ One repository per aggregate/domain.

✅ Keep repositories focused on persistence.

✅ Inject repositories into services.

✅ Keep SQL/ORM code inside repositories.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Repository Pattern, and why is it useful?

The Repository Pattern separates database access from business logic by encapsulating all persistence operations inside
repository classes. Services interact with repositories instead of directly writing SQL or ORM queries. This improves
maintainability, testability, and flexibility, allowing the underlying database implementation to change with minimal
impact on business logic. Repository is one of the most widely used patterns in enterprise backend applications.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Repository Pattern is
- Why it exists
- Repository vs Service
- Repository vs Model
- Repository vs DAO
- FastAPI + SQLAlchemy examples
- Testing with repositories
- Best practices

______________________________________________________________________

# 🚀 Milestone Reached

You now understand the design patterns that you'll encounter most frequently in real-world Python backend development:

- Factory
- Singleton
- Strategy
- Observer
- Adapter
- Decorator
- Repository

From here, we'll move into more advanced patterns that are common in large-scale systems, microservices, and enterprise
applications.

______________________________________________________________________

# What's Next

[Builder Pattern](21-builder-pattern.md)

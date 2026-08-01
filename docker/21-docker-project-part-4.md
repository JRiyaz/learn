# Docker - Part 21

# Docker Project - Part 4

# Implementing CRUD Operations

______________________________________________________________________

# Introduction

In the previous chapter,

we connected FastAPI to PostgreSQL.

Now,

we'll implement the application's business logic.

By the end of this chapter,

our API will support:

- Create a book
- Get all books
- Get a book by ID
- Update a book
- Delete a book
- Borrow a book
- Return a book

We'll keep the architecture simple but follow patterns that scale well to larger applications.

______________________________________________________________________

# Request Flow

```text id="crud001"
HTTP Request

↓

FastAPI Route

↓

CRUD Layer

↓

SQLModel

↓

PostgreSQL
```

The routes handle HTTP,

while the CRUD layer handles database operations.

______________________________________________________________________

# Why a CRUD Layer?

Instead of writing SQL directly inside route handlers,

we separate responsibilities.

```text id="crud002"
Routes

↓

HTTP

↓

CRUD

↓

Database
```

This makes the code easier to test and maintain.

______________________________________________________________________

# CRUD File

Create

```text id="crud003"
crud.py
```

______________________________________________________________________

# Create Book

```python id="crud004"
from sqlmodel import Session

from .models import Book
from .schemas import BookCreate


def create_book(
    session: Session,
    book_data: BookCreate
) -> Book:

    book = Book.model_validate(
        book_data
    )

    session.add(book)

    session.commit()

    session.refresh(book)

    return book
```

Notice

```python id="crud005"
Book.model_validate()
```

This is the modern SQLModel approach.

______________________________________________________________________

# Get All Books

```python id="crud006"
from sqlmodel import select


def get_books(
    session: Session
):

    statement = select(Book)

    return session.exec(
        statement
    ).all()
```

______________________________________________________________________

# Get Book by ID

```python id="crud007"
def get_book(
    session: Session,
    book_id: int
):

    return session.get(
        Book,
        book_id
    )
```

Using

```python id="crud008"
session.get()
```

is efficient for primary-key lookups.

______________________________________________________________________

# Update Book

```python id="crud009"
def update_book(
    session: Session,
    book: Book,
    data: BookCreate
):

    book.title = data.title

    book.author = data.author

    session.add(book)

    session.commit()

    session.refresh(book)

    return book
```

______________________________________________________________________

# Delete Book

```python id="crud010"
def delete_book(
    session: Session,
    book: Book
):

    session.delete(book)

    session.commit()
```

Simple

and efficient.

______________________________________________________________________

# Borrow Book

Business rule

```text id="crud011"
Available?

↓

Yes

↓

Borrow

↓

Unavailable
```

______________________________________________________________________

Implementation

```python id="crud012"
def borrow_book(
    session: Session,
    book: Book
):

    if not book.available:

        return None

    book.available = False

    session.add(book)

    session.commit()

    session.refresh(book)

    return book
```

______________________________________________________________________

# Return Book

```python id="crud013"
def return_book(
    session: Session,
    book: Book
):

    book.available = True

    session.add(book)

    session.commit()

    session.refresh(book)

    return book
```

______________________________________________________________________

# Route Structure

Create

```text id="crud014"
routes.py
```

All API endpoints

will live here.

______________________________________________________________________

# API Router

```python id="crud015"
from fastapi import APIRouter

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)
```

______________________________________________________________________

# Create Endpoint

```python id="crud016"
@router.post("/")
def create(
    book: BookCreate,
    session: SessionDep
):

    return create_book(
        session,
        book
    )
```

The route

delegates

to the CRUD layer.

______________________________________________________________________

# List Endpoint

```python id="crud017"
@router.get("/")
def list_books(
    session: SessionDep
):

    return get_books(
        session
    )
```

______________________________________________________________________

# Get Endpoint

```python id="crud018"
from fastapi import HTTPException


@router.get("/{book_id}")
def get(
    book_id: int,
    session: SessionDep
):

    book = get_book(
        session,
        book_id
    )

    if book is None:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book
```

______________________________________________________________________

# Update Endpoint

```python id="crud019"
@router.put("/{book_id}")
def update(
    book_id: int,
    data: BookCreate,
    session: SessionDep
):

    book = get_book(
        session,
        book_id
    )

    if book is None:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return update_book(
        session,
        book,
        data
    )
```

______________________________________________________________________

# Delete Endpoint

```python id="crud020"
@router.delete("/{book_id}")
def delete(
    book_id: int,
    session: SessionDep
):

    book = get_book(
        session,
        book_id
    )

    if book is None:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    delete_book(
        session,
        book
    )

    return {

        "message":

        "Book deleted"

    }
```

______________________________________________________________________

# Borrow Endpoint

```python id="crud021"
@router.post("/{book_id}/borrow")
def borrow(
    book_id: int,
    session: SessionDep
):

    book = get_book(
        session,
        book_id
    )

    if book is None:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    result = borrow_book(
        session,
        book
    )

    if result is None:

        raise HTTPException(
            status_code=400,
            detail="Book already borrowed"
        )

    return result
```

______________________________________________________________________

# Return Endpoint

```python id="crud022"
@router.post("/{book_id}/return")
def return_book_endpoint(
    book_id: int,
    session: SessionDep
):

    book = get_book(
        session,
        book_id
    )

    if book is None:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return return_book(
        session,
        book
    )
```

______________________________________________________________________

# Register Router

Inside

```text id="crud023"
main.py
```

```python id="crud024"
from .routes import router

app.include_router(
    router
)
```

The API is now active.

______________________________________________________________________

# Testing Endpoints

Create a book

```http id="crud025"
POST /books
```

Retrieve all books

```http id="crud026"
GET /books
```

Borrow

```http id="crud027"
POST /books/1/borrow
```

Return

```http id="crud028"
POST /books/1/return
```

Delete

```http id="crud029"
DELETE /books/1
```

______________________________________________________________________

# Request Lifecycle

```text id="crud030"
Client

↓

FastAPI

↓

CRUD

↓

Session

↓

PostgreSQL

↓

Response
```

Each request

uses a fresh session.

______________________________________________________________________

# Current Architecture

```text id="crud031"
Routes

↓

CRUD

↓

SQLModel

↓

PostgreSQL
```

Redis

and

Kafka

will be integrated next.

______________________________________________________________________

# Common Mistakes

### Mixing HTTP and Database Logic

Keep HTTP handling inside routes

and database logic inside the CRUD layer.

______________________________________________________________________

### Forgetting `session.refresh()`

Refreshing the model ensures database-generated values (such as IDs) are available after committing.

______________________________________________________________________

### Returning 200 for Missing Resources

Use

```text id="crud032"
404
```

when a resource doesn't exist.

______________________________________________________________________

### Sharing Sessions

Continue using

one session

per request.

______________________________________________________________________

# Best Practices

- Keep routes thin.
- Keep CRUD functions focused.
- Use SQLModel models.
- Raise appropriate HTTP exceptions.
- Separate business logic from HTTP logic.
- Keep database operations reusable.

______________________________________________________________________

# Hands-on Exercise

1. Implement `create_book()`.
1. Implement `get_books()`.
1. Implement `get_book()`.
1. Implement `update_book()`.
1. Implement `delete_book()`.
1. Implement borrow and return logic.
1. Register the router.
1. Test every endpoint using Swagger UI.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should database logic be separated from FastAPI route handlers?

Separating database logic into a dedicated CRUD or repository layer improves maintainability, testability, and code
reuse. Route handlers remain focused on HTTP concerns such as request validation and response formatting, while database
operations can be reused by other parts of the application and tested independently.

______________________________________________________________________

# Summary

In this chapter, you learned:

- CRUD layer design
- Creating books
- Reading books
- Updating books
- Deleting books
- Borrow and return business logic
- FastAPI routing
- HTTP exception handling
- Router registration
- Clean architecture principles

Our application now performs full CRUD operations against PostgreSQL.

In the next chapter, we'll integrate **Redis caching** to reduce database queries and improve API performance.

______________________________________________________________________

## Next File

[Docker Project - Part 5](22-docker-project-part-5.md)

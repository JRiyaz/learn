# SQL Library Management System Project - Part 2

## Introduction

In Part 1, we built the database schema.

Current tables:

```text id="sqlp201"
Authors

↓

Books

↓

Borrow Records

↑

Members
```

Now it's time to build the application's core functionality.

In this chapter we'll implement:

- Complete CRUD Operations
- Searching
- Filtering
- Sorting
- Pagination
- JOIN Queries
- Transactions
- Validation

This is where you'll use most of the SQL queries learned throughout the course.

______________________________________________________________________

# CRUD Architecture

```text id="sqlp202"
Client

↓

Library API

↓

CRUD Layer

↓

SQLAlchemy / SQLModel

↓

PostgreSQL
```

Each function will perform one responsibility.

______________________________________________________________________

# Create Author

**crud.py**

```python
from sqlmodel import Session


def create_author(
    session: Session,
    name: str,
    country: str
):

    author = Author(
        name=name,
        country=country
    )

    session.add(author)
    session.commit()
    session.refresh(author)

    return author
```

______________________________________________________________________

# Create Book

```python
def create_book(
    session: Session,
    title: str,
    published_year: int,
    author_id: int
):

    book = Book(
        title=title,
        published_year=published_year,
        author_id=author_id
    )

    session.add(book)

    session.commit()

    session.refresh(book)

    return book
```

______________________________________________________________________

# Register Member

```python
def register_member(
    session: Session,
    name: str,
    email: str
):

    member = Member(
        name=name,
        email=email
    )

    session.add(member)

    session.commit()

    session.refresh(member)

    return member
```

______________________________________________________________________

# Get All Books

```python
from sqlmodel import select


def get_all_books(
    session: Session
):

    statement = select(Book)

    return session.exec(
        statement
    ).all()
```

______________________________________________________________________

# Get Book by ID

```python
def get_book(
    session: Session,
    book_id: int
):

    statement = (
        select(Book)
        .where(Book.id == book_id)
    )

    return session.exec(
        statement
    ).first()
```

______________________________________________________________________

# Update Book

```python
def update_book(
    session: Session,
    book_id: int,
    title: str
):

    book = get_book(
        session,
        book_id
    )

    if not book:

        return None

    book.title = title

    session.add(book)

    session.commit()

    session.refresh(book)

    return book
```

______________________________________________________________________

# Delete Book

```python
def delete_book(
    session: Session,
    book_id: int
):

    book = get_book(
        session,
        book_id
    )

    if not book:

        return False

    session.delete(book)

    session.commit()

    return True
```

______________________________________________________________________

# Search Books

Search by title.

```python
from sqlmodel import select


def search_books(
    session: Session,
    keyword: str
):

    statement = (
        select(Book)
        .where(
            Book.title.ilike(
                f"%{keyword}%"
            )
        )
    )

    return session.exec(
        statement
    ).all()
```

Example

Search

```text
Clean
```

Returns

```text
Clean Code

Clean Architecture
```

______________________________________________________________________

# Filter Available Books

```python
statement = (
    select(Book)
    .where(
        Book.available == True
    )
)
```

Result

Only books currently available.

______________________________________________________________________

# Filter by Author

```python
statement = (
    select(Book)
    .where(
        Book.author_id == 2
    )
)
```

______________________________________________________________________

# Filter by Published Year

```python
statement = (
    select(Book)
    .where(
        Book.published_year >= 2020
    )
)
```

______________________________________________________________________

# Multiple Conditions

```python
statement = (
    select(Book)
    .where(
        Book.available == True
    )
    .where(
        Book.published_year >= 2020
    )
)
```

______________________________________________________________________

# Sorting

Ascending

```python
statement = (
    select(Book)
    .order_by(
        Book.title
    )
)
```

Descending

```python
statement = (
    select(Book)
    .order_by(
        Book.title.desc()
    )
)
```

______________________________________________________________________

# Pagination

First page

```python
statement = (
    select(Book)
    .offset(0)
    .limit(10)
)
```

Second page

```python
statement = (
    select(Book)
    .offset(10)
    .limit(10)
)
```

Pagination is essential when tables contain thousands of rows.

______________________________________________________________________

# INNER JOIN

We want

Book

-

Author

```python
statement = (
    select(
        Book,
        Author
    )
    .join(
        Author,
        Book.author_id == Author.id
    )
)
```

Result

```text
Clean Code

↓

Robert Martin
```

______________________________________________________________________

# Borrowed Books

Let's find every borrowed book.

```python
statement = (
    select(
        BorrowRecord,
        Book,
        Member
    )
    .join(
        Book,
        BorrowRecord.book_id == Book.id
    )
    .join(
        Member,
        BorrowRecord.member_id == Member.id
    )
)
```

Result

```text
Member

↓

Book

↓

Borrow Date
```

This is a practical use of multiple joins.

______________________________________________________________________

# Borrow Book

```python
from datetime import date


def borrow_book(
    session: Session,
    member_id: int,
    book_id: int
):

    book = get_book(
        session,
        book_id
    )

    if not book:

        raise ValueError(
            "Book not found"
        )

    if not book.available:

        raise ValueError(
            "Book already borrowed"
        )

    borrow = BorrowRecord(
        member_id=member_id,
        book_id=book_id,
        borrowed_on=date.today()
    )

    book.available = False

    session.add(borrow)

    session.add(book)

    session.commit()

    session.refresh(borrow)

    return borrow
```

______________________________________________________________________

# Return Book

```python
from datetime import date


def return_book(
    session: Session,
    borrow_id: int
):

    borrow = session.get(
        BorrowRecord,
        borrow_id
    )

    if not borrow:

        raise ValueError(
            "Borrow record not found"
        )

    borrow.returned_on = date.today()

    book = session.get(
        Book,
        borrow.book_id
    )

    book.available = True

    session.add(book)
    session.add(borrow)

    session.commit()
```

______________________________________________________________________

# Why Is This a Transaction?

Returning a book performs two operations.

```text
Update BorrowRecord

+

Update Book
```

Both should succeed together.

If one fails,

rollback.

______________________________________________________________________

# Transaction Example

```python
try:

    borrow.returned_on = date.today()

    book.available = True

    session.commit()

except Exception:

    session.rollback()

    raise
```

This preserves database consistency.

______________________________________________________________________

# Complete Workflow

```text
Register Member

↓

Add Author

↓

Add Book

↓

Borrow Book

↓

Return Book
```

______________________________________________________________________

# Common Mistakes

### Forgetting Availability Check

A borrowed book could be borrowed again.

______________________________________________________________________

### No Transaction

One table updates,

another doesn't.

Database becomes inconsistent.

______________________________________________________________________

### Using DELETE Instead of History

Never delete borrow records.

Keep history.

______________________________________________________________________

### Loading Everything

Always paginate large result sets.

______________________________________________________________________

# Best Practices

- Keep CRUD functions small.
- Validate before modifying data.
- Use transactions for related updates.
- Prefer joins over repeated queries.
- Paginate user-facing lists.
- Never lose historical data.

______________________________________________________________________

# Hands-on Exercise

Extend the project.

1. Search books by author.
1. Filter available books by author.
1. Add pagination to members.
1. Add sorting by published year.
1. Prevent duplicate member emails.
1. Prevent borrowing more than five books at once.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should borrowing a book be performed inside a transaction?

Borrowing a book updates multiple tables. A new record is inserted into `BorrowRecord`, and the corresponding `Book` is
marked as unavailable. If one operation succeeds and the other fails, the database becomes inconsistent. Wrapping both
operations in a transaction ensures atomicity—either both changes are committed or both are rolled back.

______________________________________________________________________

# Summary

In this chapter, you implemented:

- CRUD operations
- Searching
- Filtering
- Sorting
- Pagination
- INNER JOINs
- Borrowing books
- Returning books
- Transactions
- Validation
- Error handling

The application is now fully functional. In the next part, we'll build reporting features using aggregate functions,
`GROUP BY`, `HAVING`, indexes, views, and more advanced SQL queries.

______________________________________________________________________

## Next File

[24-sql-library-management-project-part-3.md](24-sql-library-management-project-part-3.md)

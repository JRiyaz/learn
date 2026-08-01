# SQL Library Management System Project - Part 1

## Project Overview

Congratulations on completing the SQL section!

Now it's time to apply everything you've learned by building a **Library Management System**.

This is not a production microservice.

Instead, it's a **simple but realistic backend project** designed to reinforce every important SQL concept you've
learned.

By the end of this project, you'll understand how SQL is used in a real application.

______________________________________________________________________

# What We'll Build

A Library Management System capable of:

- Managing Books
- Managing Authors
- Managing Members
- Borrowing Books
- Returning Books
- Viewing Borrow History
- Searching Books
- Viewing Statistics

We'll use:

- Python
- SQLAlchemy 2.x
- SQLModel
- PostgreSQL

______________________________________________________________________

# Features

### Book Management

- Add Book
- Update Book
- Delete Book
- Search Book
- View Books

______________________________________________________________________

### Author Management

- Add Author
- View Authors

______________________________________________________________________

### Member Management

- Register Member
- View Members

______________________________________________________________________

### Borrowing

- Borrow Book
- Return Book
- Borrow History

______________________________________________________________________

### Reports

- Most Borrowed Books
- Active Members
- Available Books
- Borrowed Books

______________________________________________________________________

# Concepts Covered

This single project uses almost every SQL topic we've learned.

| Topic | Used |
| ------------------- | ---- |
| CREATE TABLE | ✅ |
| Constraints | ✅ |
| Primary Key | ✅ |
| Foreign Key | ✅ |
| CRUD | ✅ |
| WHERE | ✅ |
| ORDER BY | ✅ |
| LIMIT | ✅ |
| Aggregate Functions | ✅ |
| GROUP BY | ✅ |
| HAVING | ✅ |
| JOIN | ✅ |
| Transactions | ✅ |
| ACID | ✅ |
| Indexes | ✅ |
| Normalization | ✅ |
| SQLAlchemy | ✅ |
| SQLModel | ✅ |
| Relationships | ✅ |

______________________________________________________________________

# Project Architecture

```text id="sqlp001"
Client

↓

Library API

↓

SQLAlchemy

↓

PostgreSQL
```

Unlike the Kafka project,

everything happens inside one application.

______________________________________________________________________

# Suggested Folder Structure

Although all code is included in this Markdown document,

a real project could look like:

```text id="sqlp002"
library_project/

database.py

models.py

schemas.py

crud.py

main.py
```

______________________________________________________________________

# Database Design

Our database consists of four tables.

```text id="sqlp003"
Authors

↓

Books

↓

Borrow Records

↑

Members
```

Relationship

```text id="sqlp004"
Author

1

↓

Many Books

Book

1

↓

Many Borrow Records

Member

1

↓

Many Borrow Records
```

This design follows normalization principles and avoids redundant data.

______________________________________________________________________

# Step 1 — Install Dependencies

```bash id="sqlp005"
pip install sqlmodel

pip install sqlalchemy

pip install psycopg2-binary
```

______________________________________________________________________

# Step 2 — Database Configuration

**database.py**

```python id="sqlp006"
from sqlmodel import SQLModel
from sqlmodel import create_engine


DATABASE_URL = (
    "postgresql://postgres:password@localhost:5432/library_db"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)


def create_db():

    SQLModel.metadata.create_all(engine)
```

______________________________________________________________________

# Step 3 — Author Model

**models.py**

```python id="sqlp007"
from typing import Optional

from sqlmodel import SQLModel
from sqlmodel import Field


class Author(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    name: str

    country: str
```

______________________________________________________________________

# Why Separate Authors?

Bad Design

```text id="sqlp008"
Book

title

author_name
```

The same author is repeated for every book.

Good Design

```text id="sqlp009"
Author

↓

Book
```

One author can write many books.

This avoids duplicate data.

______________________________________________________________________

# Step 4 — Book Model

```python id="sqlp010"
from typing import Optional

from sqlmodel import SQLModel
from sqlmodel import Field


class Book(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    title: str

    published_year: int

    available: bool = True

    author_id: int = Field(
        foreign_key="author.id"
    )
```

Notice

The book stores

```text id="sqlp011"
author_id
```

instead of

```text id="sqlp012"
author_name
```

This is normalization.

______________________________________________________________________

# Step 5 — Member Model

```python id="sqlp013"
from typing import Optional

from sqlmodel import SQLModel
from sqlmodel import Field


class Member(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    name: str

    email: str
```

______________________________________________________________________

# Step 6 — Borrow Record Model

```python id="sqlp014"
from typing import Optional

from datetime import date

from sqlmodel import SQLModel
from sqlmodel import Field


class BorrowRecord(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    member_id: int = Field(
        foreign_key="member.id"
    )

    book_id: int = Field(
        foreign_key="book.id"
    )

    borrowed_on: date

    returned_on: Optional[date] = None
```

This table connects books and members.

______________________________________________________________________

# Why Create BorrowRecord?

Bad

```text id="sqlp015"
Book

borrowed_by
```

A book can be borrowed many times.

Instead,

create a separate table.

This creates a proper one-to-many relationship and preserves borrowing history.

______________________________________________________________________

# Creating Tables

**main.py**

```python id="sqlp016"
from database import create_db

create_db()
```

Run

```bash id="sqlp017"
python main.py
```

Four tables are created.

______________________________________________________________________

# Step 7 — Creating a Session

```python id="sqlp018"
from sqlmodel import Session

from database import engine


with Session(engine) as session:

    pass
```

Every database operation uses a session.

______________________________________________________________________

# Insert an Author

```python id="sqlp019"
author = Author(

    name="Robert Martin",

    country="USA"

)

session.add(author)

session.commit()

session.refresh(author)
```

______________________________________________________________________

# Insert a Book

```python id="sqlp020"
book = Book(

    title="Clean Code",

    published_year=2008,

    author_id=author.id

)

session.add(book)

session.commit()

session.refresh(book)
```

______________________________________________________________________

# Insert a Member

```python id="sqlp021"
member = Member(

    name="Alice",

    email="alice@example.com"

)

session.add(member)

session.commit()
```

______________________________________________________________________

# Borrow a Book

```python id="sqlp022"
from datetime import date


borrow = BorrowRecord(

    member_id=member.id,

    book_id=book.id,

    borrowed_on=date.today()

)

session.add(borrow)

book.available = False

session.commit()
```

Notice

We also updated

```text id="sqlp023"
available = False
```

This prevents multiple users from borrowing the same copy simultaneously.

______________________________________________________________________

# Current Database

```text id="sqlp024"
Author

↓

Book

↓

Borrow Record

↑

Member
```

Everything is connected using foreign keys.

______________________________________________________________________

# Common Mistakes

### Storing Author Names in Books

Store the author's ID instead.

______________________________________________________________________

### Forgetting Foreign Keys

Relationships become impossible to enforce.

______________________________________________________________________

### No Borrow Table

You lose borrowing history.

______________________________________________________________________

### Not Updating Availability

The same book could appear available even after being borrowed.

______________________________________________________________________

# Best Practices

- Normalize your schema.
- Use foreign keys to maintain integrity.
- Separate entities into different tables.
- Keep borrowing history instead of overwriting data.
- Use SQLModel models to represent tables.

______________________________________________________________________

# Hands-on Exercise

Extend the project.

1. Add a `phone_number` column to `Member`.
1. Add a `genre` column to `Book`.
1. Add a `created_at` field to all tables.
1. Insert three authors.
1. Insert five books.
1. Register three members.
1. Borrow two books.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why do we create a separate `BorrowRecord` table instead of storing the member ID directly in the `Book`
table?

A book can be borrowed many times by different members over its lifetime. Storing a single `member_id` in the `Book`
table would only represent the current borrower and would lose historical data. A separate `BorrowRecord` table models
the borrowing events, preserves history, and supports reporting such as borrow counts, active loans, and member
activity.

______________________________________________________________________

# Summary

In this part, you built:

- Database configuration
- Four normalized tables
- Foreign key relationships
- SQLModel models
- Database sessions
- Initial data insertion
- Book borrowing

In the next part, we'll implement complete CRUD operations, filtering, sorting, joins, and search functionality.

______________________________________________________________________

## Next File

[24-sql-library-management-project-part-2.md](24-sql-library-management-project-part-2.md)

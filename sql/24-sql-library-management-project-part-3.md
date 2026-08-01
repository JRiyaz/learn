# SQL Library Management System Project - Part 3

## Introduction

Our Library Management System is now fully functional.

Users can:

- Register Members
- Add Authors
- Add Books
- Borrow Books
- Return Books

Now let's build something every real application needs:

**Reports and Analytics**

In this chapter we'll cover:

- Aggregate Functions
- GROUP BY
- HAVING
- Subqueries
- Views
- Indexes
- Advanced JOINs
- SQL Functions
- Transactions
- Performance Optimization

These are the queries commonly used by dashboards and admin panels.

______________________________________________________________________

# Current Database

```text id="sql301"
Authors

↓

Books

↓

Borrow Records

↑

Members
```

______________________________________________________________________

# Library Dashboard

Imagine an admin dashboard.

```text id="sql302"
Total Books

Available Books

Borrowed Books

Total Members

Most Popular Books

Most Active Members
```

We'll build all of these.

______________________________________________________________________

# Total Books

```python
from sqlalchemy import func
from sqlmodel import select

statement = (
    select(
        func.count(Book.id)
    )
)

total_books = session.exec(
    statement
).one()
```

Example Output

```text
250
```

______________________________________________________________________

# Total Members

```python
statement = (
    select(
        func.count(Member.id)
    )
)

total_members = session.exec(
    statement
).one()
```

______________________________________________________________________

# Available Books

```python
statement = (
    select(
        func.count(Book.id)
    )
    .where(
        Book.available == True
    )
)
```

______________________________________________________________________

# Borrowed Books

```python
statement = (
    select(
        func.count(Book.id)
    )
    .where(
        Book.available == False
    )
)
```

______________________________________________________________________

# Most Borrowed Books

Count borrow records.

```python
statement = (
    select(
        Book.title,
        func.count(
            BorrowRecord.id
        ).label(
            "borrow_count"
        )
    )
    .join(
        BorrowRecord,
        Book.id == BorrowRecord.book_id
    )
    .group_by(
        Book.id,
        Book.title
    )
    .order_by(
        func.count(
            BorrowRecord.id
        ).desc()
    )
)
```

Result

```text
Clean Code

18 Times
```

______________________________________________________________________

# Understanding GROUP BY

At this point, it's useful to visualize how `GROUP BY` works.

______________________________________________________________________

# Top 5 Books

```python
statement = (
    statement.limit(5)
)
```

______________________________________________________________________

# Most Active Members

```python
statement = (
    select(
        Member.name,
        func.count(
            BorrowRecord.id
        ).label(
            "books"
        )
    )
    .join(
        BorrowRecord,
        Member.id == BorrowRecord.member_id
    )
    .group_by(
        Member.id,
        Member.name
    )
    .order_by(
        func.count(
            BorrowRecord.id
        ).desc()
    )
)
```

______________________________________________________________________

# Average Books Borrowed

```python
statement = (
    select(
        func.avg(
            BorrowRecord.book_id
        )
    )
)
```

> **Note:** This query is shown only to demonstrate the `AVG()` function. In a real library application, averaging `book_id` values is meaningless because IDs are identifiers, not measurements. A more useful average would be *average borrow duration* or *average books borrowed per member*.

______________________________________________________________________

# Oldest Book

```python
statement = (
    select(Book)
    .order_by(
        Book.published_year
    )
    .limit(1)
)
```

______________________________________________________________________

# Newest Book

```python
statement = (
    select(Book)
    .order_by(
        Book.published_year.desc()
    )
    .limit(1)
)
```

______________________________________________________________________

# HAVING

Find authors with more than three books.

```python
statement = (
    select(
        Author.name,
        func.count(Book.id)
    )
    .join(
        Book,
        Author.id == Book.author_id
    )
    .group_by(
        Author.id,
        Author.name
    )
    .having(
        func.count(Book.id) > 3
    )
)
```

______________________________________________________________________

# Why HAVING?

`WHERE`

↓

Filters rows

`GROUP BY`

↓

Creates groups

`HAVING`

↓

Filters groups

______________________________________________________________________

# Subquery

Find books borrowed at least once.

```python
subquery = (
    select(
        BorrowRecord.book_id
    )
).subquery()

statement = (
    select(Book)
    .where(
        Book.id.in_(
            select(subquery.c.book_id)
        )
    )
)
```

______________________________________________________________________

# Correlated Subquery

Find books that have never been borrowed.

```python
from sqlalchemy import exists

statement = (
    select(Book)
    .where(
        ~exists(
            select(BorrowRecord.id)
            .where(
                BorrowRecord.book_id == Book.id
            )
        )
    )
)
```

______________________________________________________________________

# SQL Functions

Uppercase book titles.

```python
statement = (
    select(
        func.upper(
            Book.title
        )
    )
)
```

______________________________________________________________________

# String Length

```python
statement = (
    select(
        func.length(
            Book.title
        )
    )
)
```

______________________________________________________________________

# Current Date

```python
statement = (
    select(
        func.current_date()
    )
)
```

______________________________________________________________________

# Create a View

Imagine the database contains this view.

```sql
CREATE VIEW borrowed_books AS

SELECT

    b.title,

    m.name,

    br.borrowed_on

FROM borrow_record br

JOIN book b
ON br.book_id = b.id

JOIN member m
ON br.member_id = m.id;
```

Now the application can query

```sql
SELECT * FROM borrowed_books;
```

Views simplify complex reporting queries.

______________________________________________________________________

# Indexes

Searching books by title frequently?

Create an index.

```sql
CREATE INDEX idx_book_title

ON book(title);
```

Searching becomes much faster for large tables.

______________________________________________________________________

# Composite Index

Frequently search

```text
author_id

+

published_year
```

```sql
CREATE INDEX idx_author_year

ON book(author_id, published_year);
```

______________________________________________________________________

# Explain Query

Check query performance.

```sql
EXPLAIN ANALYZE

SELECT *

FROM book

WHERE title='Clean Code';
```

Always analyze slow queries before adding indexes.

______________________________________________________________________

# Transaction Example

Suppose

Member borrows a book.

We must

- Create BorrowRecord
- Update Book

```python
try:

    borrow = BorrowRecord(...)

    book.available = False

    session.add(borrow)

    session.add(book)

    session.commit()

except Exception:

    session.rollback()

    raise
```

Atomic operations keep the database consistent.

______________________________________________________________________

# Dashboard Flow

```text
Books

↓

Borrow Records

↓

GROUP BY

↓

Dashboard
```

______________________________________________________________________

# Common Mistakes

### Index Everything

Indexes improve reads but slow inserts and updates.

Create indexes only where they provide measurable value.

______________________________________________________________________

### Using HAVING Instead of WHERE

Use `WHERE` before grouping.

Use `HAVING` after grouping.

______________________________________________________________________

### Ignoring Query Plans

Always inspect expensive queries.

______________________________________________________________________

### Selecting Unnecessary Columns

Select only the columns your application needs.

______________________________________________________________________

# Best Practices

- Use aggregate functions for reports.
- Group data properly.
- Filter grouped results with `HAVING`.
- Use indexes wisely.
- Analyze query performance.
- Keep reporting queries separate from CRUD operations.

______________________________________________________________________

# Hands-on Exercise

Extend the project.

1. Find the top 10 borrowed books.
1. Find members who never borrowed a book.
1. Find books never borrowed.
1. Find authors with more than five books.
1. Create a view for active loans.
1. Add indexes to frequently searched columns.
1. Compare query plans before and after indexing.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why shouldn't you create indexes on every column?

Indexes speed up read operations but require additional storage and maintenance. Every insert, update, and delete must
also update the relevant indexes, which slows write operations. Good indexing focuses on columns that are frequently
used in `WHERE`, `JOIN`, `ORDER BY`, or `GROUP BY` clauses, based on actual query patterns rather than indexing
everything.

______________________________________________________________________

# Summary

In this chapter, you implemented:

- Aggregate functions
- GROUP BY
- HAVING
- Subqueries
- Correlated subqueries
- SQL functions
- Views
- Indexes
- Query analysis
- Reporting dashboard queries
- Performance optimization

Your Library Management System now supports both day-to-day operations and administrative reporting.

______________________________________________________________________

## Next File

[24-sql-library-management-project-part-4.md](24-sql-library-management-project-part-4.md)

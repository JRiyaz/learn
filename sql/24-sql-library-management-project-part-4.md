# SQL Library Management System Project - Part 4 (Final)

## Introduction

Congratulations!

You have successfully built a complete **Library Management System** using:

- PostgreSQL
- SQL
- SQLAlchemy 2.x
- SQLModel

This project combined almost every SQL concept learned throughout the course.

In this final chapter, we'll:

- Run the complete application
- Review the complete workflow
- Discuss improvements
- Cover production considerations
- Review interview questions
- Summarize everything learned

______________________________________________________________________

# Complete Architecture

```text
                    Client

                      │

                      ▼

              Library Application

                      │

        ┌─────────────┼─────────────┐

        ▼             ▼             ▼

     CRUD        Reports       Search

        │             │             │

        └─────────────┼─────────────┘

                      ▼

                 SQLAlchemy

                      ▼

                  PostgreSQL
```

Unlike the Kafka project,

this application communicates directly with PostgreSQL.

______________________________________________________________________

# Complete Database Schema

```text
Authors

id
name
country

        │

        ▼

Books

id
title
published_year
available
author_id

        │

        ▼

BorrowRecord

id
member_id
book_id
borrowed_on
returned_on

        ▲

        │

Members

id
name
email
```

This schema follows normalization principles.

______________________________________________________________________

# Application Workflow

```text
Register Author

↓

Add Books

↓

Register Member

↓

Borrow Book

↓

Return Book

↓

Reports

↓

Dashboard
```

______________________________________________________________________

# Running the Project

Create database

```bash
createdb library_db
```

Run

```bash
python main.py
```

The tables are created automatically.

______________________________________________________________________

# Insert Sample Data

Authors

```python
create_author(

    session,

    "Robert Martin",

    "USA"

)

create_author(

    session,

    "Martin Fowler",

    "UK"

)
```

Books

```python
create_book(

    session,

    "Clean Code",

    2008,

    1

)

create_book(

    session,

    "Refactoring",

    1999,

    2

)
```

Members

```python
register_member(

    session,

    "Alice",

    "alice@example.com"

)

register_member(

    session,

    "Bob",

    "bob@example.com"

)
```

______________________________________________________________________

# Borrow Flow

```text
Member

↓

Book Exists?

↓

Available?

↓

Create Borrow Record

↓

Update Book

↓

Commit Transaction
```

______________________________________________________________________

# Return Flow

```text
Borrow Record

↓

Update Return Date

↓

Book Available

↓

Commit
```

______________________________________________________________________

# Search Flow

```text
Search

↓

WHERE

↓

ORDER BY

↓

LIMIT

↓

Results
```

______________________________________________________________________

# Reporting Flow

```text
Borrow Records

↓

JOIN

↓

GROUP BY

↓

COUNT

↓

Dashboard
```

______________________________________________________________________

# SQL Concepts Used

| Concept | Used |
| ------------- | ---- |
| CREATE TABLE | ✅ |
| INSERT | ✅ |
| UPDATE | ✅ |
| DELETE | ✅ |
| SELECT | ✅ |
| WHERE | ✅ |
| ORDER BY | ✅ |
| LIMIT | ✅ |
| GROUP BY | ✅ |
| HAVING | ✅ |
| COUNT | ✅ |
| AVG | ✅ |
| MAX | ✅ |
| MIN | ✅ |
| INNER JOIN | ✅ |
| Subquery | ✅ |
| Transactions | ✅ |
| Foreign Keys | ✅ |
| Indexes | ✅ |
| Views | ✅ |
| SQL Functions | ✅ |
| SQLAlchemy | ✅ |
| SQLModel | ✅ |

______________________________________________________________________

# Example Dashboard

```text
---------------------------------

Library Dashboard

---------------------------------

Books

250

Available

190

Borrowed

60

Members

80

Top Book

Clean Code

Most Active Member

Alice

---------------------------------
```

______________________________________________________________________

# Data Integrity Rules

The application enforces:

- A book must belong to an existing author.
- A borrow record must reference an existing member.
- A borrow record must reference an existing book.
- A borrowed book cannot be borrowed again until returned.
- A returned book becomes available again.

These rules maintain data consistency.

______________________________________________________________________

# Performance Improvements

As data grows,

consider:

### Indexes

```sql
CREATE INDEX idx_book_title

ON book(title);
```

______________________________________________________________________

### Pagination

Avoid

```python
select(Book)
```

Prefer

```python
select(Book)

.limit(20)

.offset(0)
```

______________________________________________________________________

### Views

Frequently used reports

↓

Views

↓

Faster application code

______________________________________________________________________

### Query Analysis

Always inspect

```sql
EXPLAIN ANALYZE
```

before optimizing queries.

______________________________________________________________________

# Security Improvements

Avoid SQL Injection

Always use parameterized queries through SQLAlchemy or SQLModel.

Avoid

```python
query = f"

SELECT *

FROM book

WHERE id = {id}

"
```

Prefer ORM expressions or bound parameters.

______________________________________________________________________

# Production Improvements

If this application were deployed,

consider adding:

- FastAPI REST API
- Authentication
- Authorization
- Pagination
- Logging
- Alembic Migrations
- Docker
- Docker Compose
- Unit Tests
- Integration Tests
- CI/CD

We'll cover these topics later in the roadmap.

______________________________________________________________________

# Common Interview Questions

## Why Normalize?

Reduce redundancy.

Improve consistency.

______________________________________________________________________

## Why Foreign Keys?

Maintain referential integrity.

______________________________________________________________________

## Why Transactions?

Ensure multiple related operations succeed or fail together.

______________________________________________________________________

## Why Use JOIN Instead of Multiple Queries?

Reduce unnecessary database round trips.

Leverage relational database capabilities.

______________________________________________________________________

## Why Use Indexes?

Improve read performance for frequently queried columns.

______________________________________________________________________

## Why Not Index Every Column?

Indexes slow inserts, updates, and deletes.

Use them where query patterns justify the cost.

______________________________________________________________________

## Why Use SQLAlchemy?

- Safer queries
- Cleaner code
- Database abstraction
- Easier maintenance

______________________________________________________________________

# Mini Interview

## Question

How would you improve this application for production?

### Answer

I would:

- Expose REST APIs using FastAPI.
- Add authentication and authorization.
- Use Alembic for schema migrations.
- Containerize with Docker.
- Add structured logging.
- Write unit and integration tests.
- Configure connection pooling.
- Add caching for frequently accessed data.
- Monitor database performance and optimize queries.

______________________________________________________________________

# Suggested Extensions

Try implementing these yourself.

1. Multiple copies of the same book.
1. Book reservations.
1. Late return tracking.
1. Fine calculation.
1. Book categories.
1. Publisher table.
1. Search by author.
1. Search by publication year.
1. Member borrowing limits.
1. Admin dashboard.

These features reinforce database modeling and SQL skills.

______________________________________________________________________

# Final Revision

You should now understand:

✓ Database Design

✓ Normalization

✓ CRUD

✓ WHERE

✓ ORDER BY

✓ LIMIT

✓ Aggregations

✓ GROUP BY

✓ HAVING

✓ Joins

✓ Subqueries

✓ Transactions

✓ ACID

✓ Views

✓ Indexes

✓ SQL Functions

✓ SQLAlchemy

✓ SQLModel

✓ Relationships

✓ Performance Optimization

______________________________________________________________________

# Course Review Questions

1. Why normalize databases?
1. What is a primary key?
1. What is a foreign key?
1. Why use transactions?
1. Difference between `WHERE` and `HAVING`?
1. When should you use `GROUP BY`?
1. Why use indexes?
1. What is a view?
1. Why use joins?
1. Why use SQLAlchemy instead of raw SQL?
1. How do you prevent SQL injection?
1. When should you paginate results?
1. Why should borrowing a book be transactional?
1. How would you optimize a slow query?
1. What improvements would you make for production?

______________________________________________________________________

# Final Project Summary

In this project, you built a realistic Library Management System that demonstrated:

- Relational database design
- Table relationships
- CRUD operations
- Searching, filtering, and sorting
- Pagination
- Joins
- Aggregate reporting
- Transactions
- Views
- Indexes
- SQL functions
- SQLAlchemy and SQLModel integration
- Database performance considerations

This project ties together the SQL concepts covered throughout the course and serves as a strong foundation before
moving on to larger backend systems and distributed architectures.

______________________________________________________________________

# What's Next?

The next technology project should be **Redis**.

We'll build a **URL Shortener with Analytics** that covers:

- Redis Strings
- Hashes
- Sets
- Sorted Sets
- TTL
- Counters
- Caching
- Rate Limiting
- Connection Pooling
- Redis-py

______________________________________________________________________

## Next File

[Database Scaling Masterclass - Part 1](25.db-scaling-part-1.md)

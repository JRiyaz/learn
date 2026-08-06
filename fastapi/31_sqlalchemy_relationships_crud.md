# SQLAlchemy Relationships & CRUD Patterns

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 9 - Database Integration
>
> **File:** `31_sqlalchemy_relationships_crud.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Database Relationships
- One-to-One Relationships
- One-to-Many Relationships
- Many-to-Many Relationships
- Foreign Keys
- SQLAlchemy `relationship()`
- CRUD Repository Pattern
- Service Layer Integration
- Production Best Practices

______________________________________________________________________

# Why Relationships Matter

Real-world databases rarely contain a single table.

Example

```
Users

Orders

Products

Categories

Payments
```

These tables are connected through relationships.

______________________________________________________________________

# Types of Relationships

The most common database relationships are

```
One-to-One
```

```
One-to-Many
```

```
Many-to-Many
```

______________________________________________________________________

# One-to-One

Example

```
User

↓

Profile
```

Each user has exactly one profile.

Each profile belongs to exactly one user.

______________________________________________________________________

# Database Structure

```
users

id

name
```

```
profiles

id

user_id

bio
```

`profiles.user_id`

references

```
users.id
```

______________________________________________________________________

# One-to-Many

Example

```
Customer

↓

Orders
```

One customer

↓

Many orders.

Each order belongs to exactly one customer.

______________________________________________________________________

# Database Structure

```
customers

id
```

```
orders

id

customer_id
```

______________________________________________________________________

# Many-to-Many

Example

```
Students

↓

Courses
```

One student

↓

Many courses.

One course

↓

Many students.

______________________________________________________________________

# Junction Table

```
students

↓

student_courses

↓

courses
```

The junction (association) table stores the relationships.

______________________________________________________________________

# Foreign Key

A foreign key links one table to another.

Example

```python
from sqlalchemy import ForeignKey
```

```python
customer_id = mapped_column(

    ForeignKey(

        "customers.id"

    )
)
```

______________________________________________________________________

# relationship()

`relationship()` connects ORM models.

Example

```python
from sqlalchemy.orm import relationship
```

______________________________________________________________________

# One-to-Many Example

Customer

```python
class Customer(

    Base

):

    __tablename__ = "customers"

    id: Mapped[int]

    orders = relationship(

        "Order",

        back_populates="customer"
    )
```

Order

```python
class Order(

    Base

):

    __tablename__ = "orders"

    customer_id = mapped_column(

        ForeignKey(

            "customers.id"
        )
    )

    customer = relationship(

        "Customer",

        back_populates="orders"
    )
```

______________________________________________________________________

# Relationship Flow

```
Customer

↓

Orders

↓

Order

↓

Customer
```

Navigation works in both directions.

______________________________________________________________________

# One-to-One Example

```python
profile = relationship(

    "Profile",

    uselist=False
)
```

`uselist=False`

indicates a single related object.

______________________________________________________________________

# Many-to-Many Example

```
Student

↓

Association Table

↓

Course
```

SQLAlchemy uses a secondary table to represent the association.

______________________________________________________________________

# CRUD Pattern

Typical repository methods

```
Create

Read

Update

Delete
```

______________________________________________________________________

# Create

```python
def create(

    db,

    user

):

    db.add(

        user

    )

    db.commit()

    db.refresh(

        user

    )

    return user
```

______________________________________________________________________

# Read

```python
def get(

    db,

    user_id

):

    return db.get(

        User,

        user_id
    )
```

______________________________________________________________________

# Update

```python
user.name = "Riyaz"

db.commit()

db.refresh(

    user
)
```

______________________________________________________________________

# Delete

```python
db.delete(

    user
)

db.commit()
```

______________________________________________________________________

# Repository Pattern

```
Route

↓

Service

↓

Repository

↓

Database
```

Repositories contain database operations only.

______________________________________________________________________

# Service Pattern

```
Route

↓

Service

↓

Repository
```

Services

- Validate business rules
- Coordinate repositories
- Manage workflows

Repositories

- Execute database queries

______________________________________________________________________

# Example Flow

```
POST /orders

↓

Route

↓

OrderService

↓

OrderRepository

↓

Database
```

______________________________________________________________________

# Transactions

Creating an order may involve

```
Order

↓

Order Items

↓

Inventory

↓

Payment
```

All changes should succeed together,

or all be rolled back.

______________________________________________________________________

# Lazy Loading

Default behavior

```
Customer

↓

Orders

↓

Loaded Later
```

Related data is fetched when accessed.

______________________________________________________________________

# Eager Loading

```
Customer

+

Orders

↓

Single Query
```

Useful when related objects are definitely needed.

SQLAlchemy commonly uses

```python
selectinload()
```

or

```python
joinedload()
```

for eager loading.

______________________________________________________________________

# N+1 Query Problem

Bad

```
Customers

↓

100 Queries

↓

Orders
```

One query for customers,

then one query per customer.

______________________________________________________________________

# Better

```
Customers

↓

Single Query

↓

Orders
```

Eager loading reduces unnecessary database round-trips.

______________________________________________________________________

# Cascading

Deleting a parent may affect children.

Example

```
Customer Deleted

↓

Orders Deleted
```

or

```
Deletion Prevented
```

Choose cascade behavior carefully.

______________________________________________________________________

# ORM vs API Models

Database

```
Customer

↓

Order
```

API

```
CustomerResponse

↓

OrderResponse
```

Keep ORM entities separate from API schemas.

______________________________________________________________________

# Common Mistakes

❌ Performing business logic inside repositories

❌ Returning ORM objects directly from APIs

❌ Ignoring transactions

❌ Creating circular relationships unnecessarily

❌ Causing N+1 query problems

______________________________________________________________________

# Production Best Practices

- Use repositories for database access.
- Use services for business logic.
- Model relationships explicitly.
- Use eager loading when appropriate.
- Avoid unnecessary lazy loading.
- Keep transactions consistent.
- Separate ORM models from API schemas.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why do large FastAPI applications commonly use both a service layer and a repository layer?**

### Answer

The repository layer focuses only on data access,

while the service layer implements business rules.

Benefits include:

- Better separation of concerns.
- Easier testing.
- Reusable business logic.
- Cleaner route handlers.
- Easier maintenance.
- Reduced duplication.

This layered architecture scales much better than placing SQL queries directly inside API endpoints.

______________________________________________________________________

# Summary

In this chapter you learned:

- Database Relationships
- Foreign Keys
- `relationship()`
- CRUD Operations
- Repository Pattern
- Service Layer
- Transactions
- Lazy Loading
- Eager Loading
- Production Best Practices

SQLAlchemy relationships allow Python objects to represent real-world database relationships, while repository and
service patterns keep FastAPI applications organized and maintainable.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What are database relationships?
1. What is a foreign key?
1. What does `relationship()` do?

______________________________________________________________________

## Relationships

4. What is a one-to-one relationship?
1. What is a one-to-many relationship?
1. What is a many-to-many relationship?

______________________________________________________________________

## SQLAlchemy

7. What is `back_populates` used for?
1. What does `uselist=False` indicate?
1. What is the purpose of an association table?

______________________________________________________________________

## Architecture

10. What responsibilities belong in repositories?
01. What responsibilities belong in services?
01. Why should route handlers avoid SQL queries?

______________________________________________________________________

## Performance

13. What is the N+1 query problem?
01. When should eager loading be used?
01. What is lazy loading?

______________________________________________________________________

## Scenario-Based

16. Your application loads 100 customers, then executes 100 additional queries to load each customer's orders. What performance issue is occurring, and how would you solve it?
01. Your repository validates business rules before saving data. Why is this considered poor separation of concerns?
01. Your API deletes a customer record, but related orders remain orphaned. How can relationship configuration help manage this?
01. Your application exposes SQLAlchemy ORM models directly in API responses. What long-term maintenance and security problems can this cause?
01. Your team is debating whether to place all SQL queries directly inside FastAPI routes or introduce repository and service layers. What architectural advantages do the additional layers provide?

______________________________________________________________________

# Next

[Alembic Migrations](32_alembic_migrations.md)

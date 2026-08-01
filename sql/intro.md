# Database Fundamentals

## Introduction

Before writing SQL queries, it's important to understand how relational databases work. Many interview questions don't
start with `SELECT` or `JOIN`; they begin by testing your understanding of database fundamentals.

A strong grasp of these concepts makes advanced SQL, query optimization, indexing, and system design much easier to
understand.

______________________________________________________________________

# What is a Database?

A **database** is an organized collection of data that allows efficient storage, retrieval, modification, and management
of information.

Instead of storing information in files scattered across a system, databases organize data into structured formats that
support fast searching, updates, relationships, and transactions.

Example:

Instead of storing employee information in multiple Excel files:

```
Employee_1.xlsx
Employee_2.xlsx
Employee_3.xlsx
...
```

A relational database stores everything in structured tables.

```
Employees
------------------------------
ID | Name  | Department | Salary
------------------------------
1  | Alice | HR         | 60000
2  | Bob   | IT         | 85000
3  | John  | Finance    | 90000
```

______________________________________________________________________

# Why Do We Need Databases?

Without databases:

- Data becomes duplicated.
- Updating information is difficult.
- Searching is slow.
- Multiple users cannot safely modify data.
- Relationships between data become hard to maintain.
- Data consistency is difficult to guarantee.

Databases solve these problems by providing:

- Structured storage
- Efficient querying
- Data integrity
- Concurrency control
- Security
- Backup and recovery
- Transactions

______________________________________________________________________

# Relational Database (RDBMS)

A **Relational Database Management System (RDBMS)** stores information in **tables** that can be connected using
relationships.

Examples:

- PostgreSQL
- MySQL
- Oracle Database
- Microsoft SQL Server
- SQLite

Each table represents one type of entity.

Example:

```
Customers

ID | Name
------------
1  | Alice
2  | Bob

Orders

ID | CustomerID | Amount
-------------------------
1  | 1          | 250
2  | 2          | 100
3  | 1          | 500
```

Notice that `CustomerID` connects the two tables.

______________________________________________________________________

# RDBMS vs NoSQL

| RDBMS | NoSQL |
| --------------------------- | ------------------------------------------------------------- |
| Stores data in tables | Stores data in documents, key-value pairs, graphs, or columns |
| Fixed schema | Flexible schema |
| Strong consistency | Often prioritizes scalability |
| Uses SQL | Database-specific query languages |
| Excellent for relationships | Excellent for massive horizontal scaling |

### When is an RDBMS a good choice?

- Banking systems
- E-commerce
- Hospital management
- HR systems
- Inventory management
- ERP software

### When is NoSQL a good choice?

- Caching
- Event logging
- Social media feeds
- IoT telemetry
- Real-time analytics

______________________________________________________________________

# Table

A table is a collection of related data arranged into rows and columns.

Example:

```
Employees

+----+--------+------------+
| ID | Name   | Department |
+----+--------+------------+
| 1  | Alice  | HR         |
| 2  | Bob    | IT         |
| 3  | John   | Finance    |
+----+--------+------------+
```

Think of a table as a spreadsheet where every row represents one record.

______________________________________________________________________

# Row

A **row** represents one complete record.

Example:

```
2 | Bob | IT
```

This entire line is one row.

______________________________________________________________________

# Column

A **column** represents one attribute of the data.

Example:

```
ID
Name
Department
Salary
```

Each column stores one specific type of information.

______________________________________________________________________

# Entity

An entity represents a real-world object.

Examples:

- Student
- Employee
- Product
- Customer
- Order

Typically, one entity maps to one table.

______________________________________________________________________

# Attributes

Attributes describe an entity.

Example:

Employee

Attributes:

- Employee ID
- Name
- Salary
- Department
- Email

These become the columns of the table.

______________________________________________________________________

# Relationship

Relationships connect entities.

Example:

```
Customer

1 Alice

Orders

Order 101
Order 102
Order 103
```

One customer can have multiple orders.

This is called a **One-to-Many** relationship.

______________________________________________________________________

# Keys

Keys uniquely identify records and establish relationships.

Common keys:

- Primary Key
- Foreign Key
- Candidate Key
- Composite Key
- Alternate Key
- Surrogate Key
- Natural Key

The detailed discussion of these keys will be covered in upcoming lessons.

______________________________________________________________________

# Primary Key

A Primary Key uniquely identifies each row.

Example:

```
EmployeeID

1
2
3
4
```

Characteristics:

- Unique
- Cannot be NULL
- One Primary Key per table

______________________________________________________________________

# Foreign Key

A Foreign Key creates a relationship between two tables.

Example:

```
Employees

EmployeeID
1
2

Departments

DepartmentID
10
20

Employees

EmployeeID | DepartmentID
--------------------------
1          | 10
2          | 20
```

The `DepartmentID` in the Employees table references the Departments table.

______________________________________________________________________

# Candidate Key

A Candidate Key is any column (or combination of columns) that can uniquely identify a row.

Example:

```
EmployeeID
Email
PassportNumber
```

Each of these could uniquely identify an employee.

One candidate key is chosen as the Primary Key.

______________________________________________________________________

# Composite Key

A Composite Key is made from multiple columns.

Example:

```
StudentID
CourseID
```

Together they uniquely identify an enrollment.

______________________________________________________________________

# Constraints

Constraints ensure the correctness of data.

Common constraints:

- PRIMARY KEY
- FOREIGN KEY
- UNIQUE
- CHECK
- NOT NULL
- DEFAULT

These will be covered in depth later in the course.

______________________________________________________________________

# Entity Relationship (ER) Diagram

An ER diagram visually represents entities and their relationships.

Example:

```
Customer
---------
CustomerID
Name

      |
      | 1
      |
      | *
Orders
---------
OrderID
CustomerID
Amount
```

This indicates that one customer can have many orders.

______________________________________________________________________

# Basic Database Design Principles

A good database design should:

- Avoid duplicate data
- Maintain consistency
- Support efficient queries
- Be easy to extend
- Preserve data integrity

Poor design often leads to slow queries, inconsistent information, and maintenance challenges.

______________________________________________________________________

# Common Mistakes

- Using duplicate data across multiple tables.
- Storing multiple values in a single column.
- Forgetting relationships between tables.
- Choosing unstable values as identifiers.
- Ignoring data integrity.

______________________________________________________________________

# Best Practices

- Design tables around real-world entities.
- Keep tables focused on a single purpose.
- Use meaningful column names.
- Choose stable primary keys.
- Model relationships explicitly instead of duplicating data.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why do relational databases use Primary Keys and Foreign Keys?

A Primary Key uniquely identifies each row in a table, ensuring every record can be referenced unambiguously. A Foreign
Key links records across tables while maintaining referential integrity, preventing invalid references and reducing data
duplication. Together, they enable normalized database designs that are easier to query, maintain, and scale.

______________________________________________________________________

# Practice Questions

### Conceptual

1. What problem does a database solve compared to file storage?
1. Explain the difference between RDBMS and NoSQL.
1. What is a table?
1. What is a row?
1. What is a column?
1. What is an entity?
1. What is an attribute?
1. Why are relationships important?
1. What is a Primary Key?
1. What is a Foreign Key?

### Scenario-Based

1. Design tables for a library management system.
1. Design a database for an online shopping website.
1. Identify possible entities for a food delivery application.

______________________________________________________________________

# Hands-on Exercise

Design a simple database for a university containing:

- Students
- Courses
- Instructors
- Enrollments

Identify:

- Entities
- Attributes
- Primary Keys
- Relationships

Do not write SQL yet. Focus only on the database design.

______________________________________________________________________

# Cheat Sheet

```
Database
    ↓
Tables
    ↓
Rows
    ↓
Columns

Entity
    ↓
Table

Attribute
    ↓
Column

Relationship
    ↓
Foreign Key

Unique Identifier
    ↓
Primary Key
```

______________________________________________________________________

# Summary

In this lesson, you learned:

- What a database is
- Why databases exist
- RDBMS vs NoSQL
- Tables, rows, and columns
- Entities and attributes
- Relationships
- Primary Keys
- Foreign Keys
- Candidate Keys
- Composite Keys
- Constraints (overview)
- ER diagrams
- Basic database design principles

These concepts form the foundation for every SQL query you'll write throughout the rest of this course.

______________________________________________________________________

## Next File

[ACID, Transactions & Normalization](02-acid-transactions-normalization.md)

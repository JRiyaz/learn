# Database Fundamentals (SQL vs NoSQL)

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand how databases work, when to choose SQL or NoSQL, and confidently answer database-related System Design interview questions.

______________________________________________________________________

# Introduction

Almost every backend application

stores data.

The first major design decision is

```
Which database

should I use?
```

Many candidates answer

```
MongoDB

because it scales.

```

or

```
MySQL

because it's popular.
```

Interviewers

don't want

database names.

They want

reasoning.

______________________________________________________________________

# What Is A Database?

A database

is a system

that stores,

retrieves,

updates,

and deletes data.

Example

```
User Registers

↓

Application

↓

Database

↓

User Saved
```

Every modern application

depends on

a database.

______________________________________________________________________

# Two Major Categories

```
SQL

(Relational)

↓

Structured
```

```
NoSQL

(Non-Relational)

↓

Flexible
```

Both

solve different problems.

______________________________________________________________________

# SQL Databases

Examples

- PostgreSQL
- MySQL
- MariaDB
- Oracle
- Microsoft SQL Server

SQL databases

store data

in

tables.

Example

Users

| id | name | email |
|----|------|--------|
|1|Riyaz|riyaz@email.com|

______________________________________________________________________

# NoSQL Databases

Examples

- MongoDB
- Cassandra
- DynamoDB
- Couchbase
- Redis
- HBase

Data

doesn't have to be stored

in tables.

Example

```
{
  "id":101,
  "name":"Riyaz",
  "skills":[
      "Python",
      "FastAPI"
  ]
}
```

Much more flexible.

______________________________________________________________________

# SQL Characteristics

SQL databases provide

- Fixed schema
- ACID transactions
- Joins
- Relationships
- Strong consistency

Excellent for

structured business data.

______________________________________________________________________

# NoSQL Characteristics

NoSQL databases provide

- Flexible schema
- Horizontal scaling
- High availability
- Massive throughput
- Eventual consistency (often)

Excellent for

large-scale distributed systems.

______________________________________________________________________

# Example

## Banking System

Tables

```
Accounts

Transactions

Customers

Loans
```

Relationships

matter.

Transactions

must be

correct.

Choose

```
SQL
```

______________________________________________________________________

# Example

## Instagram

Post

may contain

```
Images

Videos

Comments

Tags

Metadata

```

Schema

changes frequently.

Choose

```
NoSQL
```

(or a combination)

______________________________________________________________________

# Structured vs Flexible

SQL

```
Every row

same structure
```

NoSQL

```
Document A

↓

Different Fields

↓

Document B
```

No migrations

for many schema changes.

______________________________________________________________________

# SQL Example

```
Users

+-----------+
| ID        |
| Name      |
| Email     |
+-----------+
```

Every record

has

the same columns.

______________________________________________________________________

# MongoDB Example

```
{
"name":"Alice"
}
```

```
{
"name":"Bob",
"phone":"123456789"
}
```

Both documents

can coexist.

______________________________________________________________________

# ACID

Interviewers

love asking this.

ACID means

```
Atomicity

Consistency

Isolation

Durability
```

Let's understand

each.

______________________________________________________________________

# Atomicity

Either

everything succeeds

or

nothing succeeds.

Example

Bank Transfer

```
Debit

↓

Credit
```

Cannot

debit

without

crediting.

______________________________________________________________________

# Consistency

Database

always remains

valid.

Rules

are never violated.

Example

Balance

cannot become

negative

if

business rules

prevent it.

______________________________________________________________________

# Isolation

Multiple users

can perform

transactions

without interfering

with one another.

______________________________________________________________________

# Durability

Once committed,

data survives

power failures,

server crashes,

and restarts.

______________________________________________________________________

# BASE

Many NoSQL systems

follow

```
Basically Available

↓

Soft State

↓

Eventually Consistent
```

Instead of

strict ACID.

______________________________________________________________________

# SQL Relationships

SQL excels

at relationships.

Example

```
Customer

↓

Orders

↓

Order Items

↓

Payments
```

Joins

are simple.

______________________________________________________________________

# Joins

Example

```
Users

JOIN

Orders
```

Retrieve

all orders

for one user.

SQL databases

optimize

these operations.

______________________________________________________________________

# Why Joins Are Hard In NoSQL

NoSQL

usually prefers

denormalization.

Instead of

joining,

duplicate

some information.

This improves

performance

at scale.

______________________________________________________________________

# Normalization

Store

data

once.

Example

```
User

↓

Orders

↓

Products
```

No duplication.

Advantages

- Less redundancy
- Easier updates

Disadvantages

- More joins

______________________________________________________________________

# Denormalization

Duplicate

data

to improve

performance.

Example

```
Order

↓

Customer Name
```

Even though

Customer table

already exists.

Advantages

- Faster reads

Disadvantages

- Duplicate data
- Harder updates

______________________________________________________________________

# SQL Scaling

Typically

starts with

Vertical Scaling.

```
Bigger Server
```

Eventually

Read Replicas

Partitioning

Sharding

may be introduced.

______________________________________________________________________

# NoSQL Scaling

Designed

for

Horizontal Scaling.

```
Node A

↓

Node B

↓

Node C
```

Scale out

more naturally.

______________________________________________________________________

# CAP Theorem (High Level)

Distributed databases

cannot guarantee

all three

at the same time.

```
Consistency

Availability

Partition Tolerance
```

We'll cover

CAP Theorem

in its own chapter.

______________________________________________________________________

# SQL Use Cases

Excellent for

- Banking
- Payments
- ERP
- CRM
- Inventory
- Payroll
- Accounting
- Booking systems

Anywhere

transactions

matter.

______________________________________________________________________

# NoSQL Use Cases

Excellent for

- Social media
- Logging
- IoT
- Chat
- Analytics
- Recommendation systems
- Product catalogs
- Content management

______________________________________________________________________

# Polyglot Persistence

Modern applications

often use

multiple databases.

Example

```
MySQL

↓

Orders
```

```
MongoDB

↓

Product Catalog
```

```
Redis

↓

Cache
```

```
Elasticsearch

↓

Search
```

Choose

the best tool

for each problem.

______________________________________________________________________

# SQL vs NoSQL

| Feature | SQL | NoSQL |
|---------|-----|--------|
| Schema | Fixed | Flexible |
| Scaling | Vertical (primarily) | Horizontal |
| Transactions | Strong | Limited / Varies |
| Joins | Excellent | Limited |
| Consistency | Strong | Often Eventual |
| Relationships | Excellent | Limited |
| Flexibility | Lower | Higher |

Remember

there is

no winner.

Only

trade-offs.

______________________________________________________________________

# Common Interview Questions

## Which database should I choose?

Wrong answer

```
MongoDB
```

Correct answer

```
It depends

on

requirements.
```

Always explain

why.

______________________________________________________________________

## Can SQL scale?

Yes.

With

- Read Replicas
- Partitioning
- Sharding
- Caching

SQL databases

scale much better

than many candidates think.

______________________________________________________________________

## Can NoSQL support transactions?

Yes.

Some NoSQL databases

support transactions,

although capabilities

vary by implementation.

Interview answers

should avoid assuming

all NoSQL databases

behave identically.

______________________________________________________________________

## Can one application use multiple databases?

Absolutely.

This is

very common

in production.

______________________________________________________________________

# Real Examples

## Amazon

May use

```
Relational DB

↓

Orders
```

```
DynamoDB

↓

Shopping Cart
```

```
Redis

↓

Cache
```

______________________________________________________________________

## Instagram

May use

```
Relational DB

↓

Accounts
```

```
Distributed Storage

↓

Media
```

```
Redis

↓

Feed Cache
```

______________________________________________________________________

## Banking

Mostly

```
SQL
```

Because

transactions

are critical.

______________________________________________________________________

# Common Mistakes

## SQL Doesn't Scale

False.

It scales well,

just differently.

______________________________________________________________________

## MongoDB Is Always Better

False.

Depends

on

requirements.

______________________________________________________________________

## Ignoring Transactions

Never choose

based only

on performance.

______________________________________________________________________

## Choosing Technology First

Requirements

come first.

Technology

comes later.

______________________________________________________________________

# Best Practices

✅ Gather requirements before choosing a database.

✅ Consider consistency requirements.

✅ Think about scalability.

✅ Evaluate relationships.

✅ Discuss trade-offs.

✅ Remember that modern systems often use multiple databases.

______________________________________________________________________

# Interview Deep Dive

## Question

When would you choose SQL over NoSQL?

### Answer

Choose SQL when the application requires strong consistency, complex relationships, joins, and reliable transactions,
such as banking, payments, inventory, or reservation systems.

______________________________________________________________________

## Question

When would you choose NoSQL?

### Answer

Choose NoSQL when the application requires flexible schemas, high write throughput, horizontal scalability, or handles
rapidly changing and semi-structured data, such as social media, analytics, or large content platforms.

______________________________________________________________________

## Question

Is SQL better than NoSQL?

### Answer

Neither is universally better. The correct choice depends on the application's functional and non-functional
requirements, including consistency, scalability, query patterns, and data model.

______________________________________________________________________

# Practice Exercise

For each application,

choose

SQL,

NoSQL,

or

Multiple Databases,

and explain why.

Applications

1. Banking System
1. WhatsApp
1. Instagram
1. Netflix
1. Food Delivery
1. Ride Sharing
1. Hospital Management
1. Online Shopping
1. URL Shortener
1. Learning Management System

Discuss

- Data relationships
- Consistency requirements
- Scalability
- Expected traffic
- Trade-offs

______________________________________________________________________

# Summary

Choosing a database is one of the most important decisions in System Design.

The strongest engineers

- Understand application requirements
- Evaluate trade-offs
- Select technologies based on business needs
- Know that SQL and NoSQL complement each other rather than compete

Mastering these concepts will help you justify database decisions confidently during interviews.

______________________________________________________________________

# Next

[Database Indexing](11-database-indexing.md)

# Alembic Migrations

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 9 - Database Integration
>
> **File:** `32_alembic_migrations.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Database Migrations are
- Why Alembic is Needed
- Installing Alembic
- Initializing Alembic
- Alembic Project Structure
- Creating Migrations
- Applying Migrations
- Rolling Back Migrations
- Migration Best Practices
- Production Workflow

______________________________________________________________________

# Why Database Migrations?

Imagine your application already has

```
Users Table

↓

Production Database

↓

Millions of Rows
```

Now you need to add

```
email_verified
```

How do you safely modify the database?

This is the purpose of migrations.

______________________________________________________________________

# What is a Migration?

A migration is a **version-controlled change** to the database schema.

Examples

- Create tables
- Add columns
- Remove columns
- Rename columns
- Create indexes
- Add constraints

______________________________________________________________________

# Without Migrations

Developer A

↓

Updates Database

Developer B

↓

Different Database

Production

↓

Different Again

Eventually,

every environment has a different schema.

______________________________________________________________________

# With Migrations

```
Migration Files

↓

Git

↓

Development

↓

Testing

↓

Production
```

Everyone applies the same changes in the same order.

______________________________________________________________________

# What is Alembic?

Alembic is SQLAlchemy's official migration tool.

It

- Tracks schema versions
- Generates migrations
- Applies migrations
- Rolls back changes

______________________________________________________________________

# Installation

```bash
pip install alembic
```

______________________________________________________________________

# Initialize Alembic

Inside the project

```bash
alembic init alembic
```

Creates

```
alembic/

alembic.ini
```

______________________________________________________________________

# Project Structure

```
project/

│

├── alembic/

│

│     env.py

│

│     script.py.mako

│

│     versions/

│

├── alembic.ini

└── app/
```

______________________________________________________________________

# versions/

```
versions/

↓

Migration Files
```

Example

```
001_create_users.py

002_add_email.py

003_create_orders.py
```

Each migration has a unique revision ID.

______________________________________________________________________

# Configure Database URL

Inside

```
alembic.ini
```

Example

```ini
sqlalchemy.url =

postgresql+psycopg://user:password@localhost/app
```

In production, many teams instead configure the URL dynamically in `env.py` using environment variables.

______________________________________________________________________

# Configure Metadata

Inside

```
env.py
```

Set

```python
target_metadata = Base.metadata
```

Alembic compares this metadata with the current database schema.

______________________________________________________________________

# Creating a Migration

Automatic generation

```bash
alembic revision --autogenerate -m "create users table"
```

Alembic compares

```
Models

↓

Database

↓

Migration
```

______________________________________________________________________

# Generated Migration

Typical structure

```python
def upgrade():

    ...
```

```python
def downgrade():

    ...
```

______________________________________________________________________

# upgrade()

Contains

```
Schema Changes

↓

Forward
```

Example

```
Add Column

Create Table

Create Index
```

______________________________________________________________________

# downgrade()

Contains

```
Reverse Changes
```

Example

```
Drop Column

Drop Table

Remove Index
```

Allows rollback.

______________________________________________________________________

# Apply Migrations

Latest version

```bash
alembic upgrade head
```

Flow

```
Current Version

↓

Migration

↓

Latest Version
```

______________________________________________________________________

# Upgrade Specific Revision

```bash
alembic upgrade <revision_id>
```

Useful for controlled deployments.

______________________________________________________________________

# Roll Back One Migration

```bash
alembic downgrade -1
```

Moves back one revision.

______________________________________________________________________

# Roll Back to Revision

```bash
alembic downgrade <revision_id>
```

Database returns to a previous schema version.

______________________________________________________________________

# View Migration History

```bash
alembic history
```

Example

```
001

↓

002

↓

003
```

______________________________________________________________________

# Current Database Version

```bash
alembic current
```

Shows the revision currently applied.

______________________________________________________________________

# Migration Flow

```
Update Models

↓

Generate Migration

↓

Review Migration

↓

Apply Migration

↓

Database Updated
```

______________________________________________________________________

# Autogeneration

Alembic can detect many changes automatically.

Examples

- New Tables
- New Columns
- Removed Columns
- Index Changes

However,

developers should always review generated migrations before applying them.

______________________________________________________________________

# Manual Migrations

Sometimes automatic detection is insufficient.

Examples

- Complex data migrations
- Renaming columns
- Data transformations
- Custom SQL

Manual editing is common.

______________________________________________________________________

# Production Deployment

```
Git Pull

↓

Deploy Application

↓

Run Alembic

↓

Application Starts
```

Many CI/CD pipelines execute migrations during deployment.

______________________________________________________________________

# Data Migrations

Schema migration

```
Add Column
```

Data migration

```
Populate Existing Rows
```

These are often performed together.

______________________________________________________________________

# Transaction Safety

Many databases execute migrations within a transaction.

```
Migration

↓

Success

↓

Commit
```

or

```
Failure

↓

Rollback
```

Behavior depends on the database backend and the operations performed.

______________________________________________________________________

# Migration Naming

Good

```
add_email_to_users
```

Bad

```
update
```

Migration names should clearly describe the schema change.

______________________________________________________________________

# Common Mistakes

❌ Editing old migration files after they have been applied

❌ Skipping migration review

❌ Applying schema changes manually in production

❌ Forgetting downgrade logic

❌ Keeping database schema changes outside version control

______________________________________________________________________

# Production Best Practices

- Commit migration files to Git.
- Review autogenerated migrations.
- Test migrations before production.
- Keep migrations small and focused.
- Write meaningful migration messages.
- Use environment variables for database configuration.
- Never modify applied migrations in shared environments.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should database schema changes be managed through Alembic instead of manually modifying production databases?**

### Answer

Alembic provides a repeatable, version-controlled process for database evolution.

Benefits include:

- Consistent schemas across environments.
- Safe deployment workflows.
- Rollback support.
- Team collaboration.
- Traceable database history.
- Integration with CI/CD pipelines.

Manual schema changes are error-prone, difficult to reproduce, and hard to audit.

______________________________________________________________________

# Summary

In this chapter you learned:

- Database Migrations
- Alembic
- Migration Generation
- Upgrade
- Downgrade
- Version History
- Autogeneration
- Data Migrations
- Production Best Practices

Alembic enables controlled, versioned evolution of database schemas, making it an essential tool for professional
FastAPI applications using SQLAlchemy.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is a database migration?
1. Why are migrations important?
1. What is Alembic?

______________________________________________________________________

## Setup

4. How do you install Alembic?
1. What does `alembic init` create?
1. Why is `target_metadata` configured in `env.py`?

______________________________________________________________________

## Commands

7. How do you generate a migration automatically?
1. What does `alembic upgrade head` do?
1. What does `alembic downgrade -1` do?
1. How do you view migration history?

______________________________________________________________________

## Workflow

11. Why should autogenerated migrations always be reviewed?
01. What is the difference between a schema migration and a data migration?
01. Why should migration files be committed to version control?

______________________________________________________________________

## Production

14. Why shouldn't applied migration files be edited?
01. Why are small, focused migrations preferred?

______________________________________________________________________

## Scenario-Based

16. Your application needs a new `email_verified` column in the `users` table. What workflow would you follow using Alembic?
01. A developer manually adds a column directly in the production database without creating a migration. What problems could this cause for other environments?
01. Alembic generates a migration after you rename a model field, but the generated script drops and recreates the column instead of renaming it. Why should the migration be reviewed before applying it?
01. Your deployment fails halfway through a migration due to a syntax error. How can transactional migrations help reduce the impact?
01. Your team has multiple developers working on the same application. How does Alembic help keep database schemas synchronized across development, staging, and production environments?

______________________________________________________________________

# Next

[Project Structure & Clean Architecture](33_project_structure_clean_architecture.md)

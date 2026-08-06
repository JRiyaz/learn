# Database Migrations with Alembic & Flask-Migrate

> **Course:** Flask for Backend Engineers
>
> **Module:** 4
>
> **File:** `11_migrations_alembic.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Database Migrations are
- Why Migrations are Necessary
- Alembic
- Flask-Migrate
- Migration Workflow
- Creating Migrations
- Applying Migrations
- Rolling Back Migrations
- Migration Scripts
- Production Deployment
- Best Practices

______________________________________________________________________

# Why Do We Need Database Migrations?

Imagine your application starts with this model.

```python
class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )
```

The table is created.

Life is good.

______________________________________________________________________

# Later...

Your product manager says:

> Add an email column.

You update the model.

```python
email = db.Column(
    db.String(255)
)
```

But...

```
Python Model

↓

Updated

↓

Database

↓

Still Old
```

The database schema does **not** update automatically.

______________________________________________________________________

# What is a Migration?

A migration is a **version-controlled change** to your database schema.

Think of it like Git for your database.

```
Model Change

↓

Migration File

↓

Database Updated
```

______________________________________________________________________

# Why Not Use create_all()?

Many beginners use:

```python
db.create_all()
```

Problems

- Doesn't remove columns
- Doesn't rename columns
- Doesn't alter existing constraints
- Doesn't track schema history

Production applications use migrations instead.

______________________________________________________________________

# What is Alembic?

**Alembic** is the official migration tool for SQLAlchemy.

Responsibilities

- Detect schema changes
- Generate migration scripts
- Upgrade databases
- Downgrade databases
- Track schema versions

______________________________________________________________________

# What is Flask-Migrate?

Flask-Migrate integrates Alembic with Flask.

It provides convenient CLI commands.

Install

```bash
pip install flask-migrate
```

______________________________________________________________________

# Initialize Extension

extensions.py

```python
from flask_migrate import Migrate

migrate = Migrate()
```

Application Factory

```python
migrate.init_app(
    app,
    db
)
```

______________________________________________________________________

# Initialize Migration Repository

Run once.

```bash
flask db init
```

Creates

```
migrations/

↓

versions/

↓

env.py

↓

alembic.ini
```

______________________________________________________________________

# Migration Workflow

```
Update Model

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

# Create First Migration

```bash
flask db migrate \
-m "Create users table"
```

Alembic compares

```
Models

↓

Database

↓

Generate SQL
```

______________________________________________________________________

# Apply Migration

```bash
flask db upgrade
```

Database schema is updated.

______________________________________________________________________

# Example

Before

```
users

id

name
```

Migration

↓

After

```
users

id

name

email
```

______________________________________________________________________

# Migration Files

Example

```
migrations/

↓

versions/

↓

23ab4_create_users.py
```

Each migration is versioned.

______________________________________________________________________

# Inside a Migration

Example

```python
def upgrade():

    op.add_column(
        "users",
        sa.Column(
            "email",
            sa.String(255)
        )
    )
```

Downgrade

```python
def downgrade():

    op.drop_column(
        "users",
        "email"
    )
```

______________________________________________________________________

# Upgrade

```
Database

↓

Old Version

↓

Upgrade

↓

New Version
```

Command

```bash
flask db upgrade
```

______________________________________________________________________

# Downgrade

```
New Version

↓

Downgrade

↓

Previous Version
```

Command

```bash
flask db downgrade
```

Useful during development and testing.

______________________________________________________________________

# Migration History

View current revision

```bash
flask db current
```

View history

```bash
flask db history
```

______________________________________________________________________

# Multiple Developers

Developer A

↓

Adds Email

Developer B

↓

Adds Phone

Each creates a migration.

Git merges both migration files.

______________________________________________________________________

# Migration Conflicts

Sometimes two developers modify the schema simultaneously.

Example

```
Migration A

↓

Migration B

↓

Conflict
```

Alembic supports merge migrations to resolve multiple migration heads.

______________________________________________________________________

# Renaming Columns

Alembic may not always detect renames automatically.

Example

```
username

↓

name
```

Auto-generated migration might

```
Drop Column

↓

Create New Column
```

instead of renaming.

Always review generated migrations.

______________________________________________________________________

# Data Migrations

Not all migrations change schema.

Sometimes

```
Old Values

↓

Transform Data

↓

New Values
```

Migration scripts can also modify data.

______________________________________________________________________

# Production Deployment Flow

```
Git Pull

↓

Deploy Application

↓

Run

flask db upgrade

↓

Application Ready
```

Migrations should be part of the deployment process.

______________________________________________________________________

# Backup First

Before production migrations

```
Database

↓

Backup

↓

Migration

↓

Success
```

If something fails,

restore from backup.

______________________________________________________________________

# Rolling Back

If deployment fails

```
Application

↓

Rollback Code

↓

Downgrade Migration (when appropriate)

↓

Restore Service
```

Downgrades should be planned carefully because not every schema change is easily reversible.

______________________________________________________________________

# Migration Best Practices

Small migrations

Good

```
Add Email
```

Bad

```
200 Schema Changes
```

Small migrations are easier to review and troubleshoot.

______________________________________________________________________

# Review Generated SQL

Never blindly execute migrations.

Check

- Column Types
- Constraints
- Indexes
- Foreign Keys
- Data Loss

______________________________________________________________________

# Zero-Downtime Considerations

For large production systems,

avoid breaking changes.

Instead of

```
Rename Column
```

Use

```
Add New Column

↓

Copy Data

↓

Update Application

↓

Remove Old Column
```

This reduces deployment risk.

______________________________________________________________________

# Common Mistakes

❌ Using `create_all()` in production

❌ Never reviewing generated migrations

❌ Combining dozens of unrelated changes into one migration

❌ Forgetting database backups

❌ Editing applied migration history without understanding the impact

______________________________________________________________________

# Production Best Practices

- Use Flask-Migrate.
- Keep migrations small.
- Review generated migrations.
- Back up production databases.
- Version control migration files.
- Test migrations before production.
- Avoid destructive schema changes during peak traffic.
- Coordinate migrations with application deployments.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should production Flask applications use Alembic instead of `db.create_all()`?**

### Answer

`db.create_all()` only creates missing tables.

It does not:

- Track schema versions
- Modify existing tables
- Remove columns
- Rename columns
- Manage schema evolution

Alembic provides version-controlled database migrations.

Benefits include:

1. Reproducible schema changes.
1. Upgrade and downgrade support.
1. Team collaboration through version-controlled migration files.
1. Safer production deployments.
1. Integration with CI/CD pipelines.

______________________________________________________________________

# Summary

In this chapter you learned:

- Database Migrations
- Alembic
- Flask-Migrate
- Migration Workflow
- Upgrade
- Downgrade
- Migration Scripts
- Merge Conflicts
- Production Deployment
- Best Practices

Database migrations are an essential part of maintaining and evolving production database schemas safely.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is a database migration?
1. Why are migrations necessary?
1. Why isn't `db.create_all()` sufficient for production?

______________________________________________________________________

## Alembic

4. What is Alembic?
1. What is Flask-Migrate?
1. What does `flask db init` create?
1. What does `flask db migrate` do?
1. What does `flask db upgrade` do?

______________________________________________________________________

## Migration Workflow

9. Explain the migration workflow.
1. Why should generated migrations always be reviewed?
1. Why should migrations be committed to version control?

______________________________________________________________________

## Production

12. Why should databases be backed up before migrations?
01. Why are small migrations preferred?
01. Why can destructive schema changes be risky?

______________________________________________________________________

## Team Collaboration

15. What happens when two developers generate migrations at the same time?
01. How can migration conflicts be resolved?

______________________________________________________________________

## Scenario-Based

17. A developer changes a model by adding an `email` column but forgets to run a migration. What happens when the application starts?
01. Your production deployment fails immediately after applying a migration. What recovery steps would you consider?
01. Alembic generates a migration that drops and recreates a column after you renamed it. Why should this migration be reviewed before execution?
01. Your team combines 50 unrelated schema changes into a single migration. Why does this make deployments more difficult?
01. Your application serves millions of users and requires zero-downtime deployments. How would you approach a column rename to minimize disruption?

______________________________________________________________________

# Next

[Authentication](12_authentication.md)

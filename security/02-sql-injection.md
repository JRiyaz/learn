# Security - Part 2

# SQL Injection (SQLi)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What SQL Injection is
- Why it happens
- How attackers exploit it (conceptually)
- How to identify vulnerable Python code
- How to prevent SQL Injection
- Secure implementations using FastAPI and SQLAlchemy
- Best practices
- Common mistakes

______________________________________________________________________

# What is SQL Injection?

SQL Injection (SQLi) is a vulnerability where **untrusted user input becomes part of a SQL query**.

Instead of treating the input as **data**,

the database interprets it as **SQL code**.

This allows an attacker to manipulate the query in unintended ways.

______________________________________________________________________

# Why Does It Happen?

It usually happens when developers build SQL queries using string concatenation or string formatting.

Instead of separating:

- SQL Code
- User Data

they mix them together.

______________________________________________________________________

# Normal Flow

A normal login request.

```text id="sql201"
User

↓

Username = riyaz

↓

Backend

↓

Database
```

Everything works as expected.

______________________________________________________________________

# Vulnerable Flow

```text id="sql202"
User Input

↓

String Concatenation

↓

SQL Query

↓

Database Executes It
```

The database cannot distinguish

between

user input

and

actual SQL.

______________________________________________________________________

# Real-World Example

Suppose your login API receives

```json id="sql203"
{
    "username": "riyaz",
    "password": "mypassword"
}
```

The backend builds this query.

```sql id="sql204"
SELECT *
FROM users
WHERE username = ?
AND password = ?;
```

The important point is:

The **username** and **password**

should always be treated as **values**,

never as SQL syntax.

______________________________________________________________________

# Vulnerable Python Code

❌ **Do NOT write code like this.**

```python
from fastapi import FastAPI
import sqlite3

app = FastAPI()

connection = sqlite3.connect("library.db")
cursor = connection.cursor()

@app.post("/login")
def login(username: str, password: str):

    query = (
        f"SELECT * FROM users "
        f"WHERE username='{username}' "
        f"AND password='{password}'"
    )

    cursor.execute(query)

    return {"message": "Login attempted"}
```

______________________________________________________________________

# Why is This Vulnerable?

The problem is here.

```python
query = (
    f"SELECT * FROM users "
    f"WHERE username='{username}' "
    f"AND password='{password}'"
)
```

The SQL query itself changes

based on user input.

The database receives one large string

and must interpret it.

Whenever user input changes the SQL statement,

you have created the possibility for SQL Injection.

______________________________________________________________________

# The Root Cause

Never think of SQL Injection as

"bad users."

Think of it as

"unsafe query construction."

Bad:

```text id="sql205"
SQL

+

User Input

↓

One String
```

Good:

```text id="sql206"
SQL Statement

↓

Database Driver

↓

Parameters

↓

Database
```

The database driver safely binds the parameters.

______________________________________________________________________

# Secure Solution 1

## Parameterized Queries

The safest approach is parameter binding.

Example

```python
import sqlite3

connection = sqlite3.connect("library.db")
cursor = connection.cursor()

query = """
SELECT *
FROM users
WHERE username = ?
AND password = ?
"""

cursor.execute(query, (username, password))
```

Notice

the SQL statement never changes.

Only the values change.

______________________________________________________________________

# Why is This Safe?

Instead of sending

```text id="sql207"
One SQL String
```

the driver sends

```text id="sql208"
SQL Statement

+

Parameters
```

The database knows

the parameters are **data**,

not SQL commands.

______________________________________________________________________

# Secure Solution 2

## SQLAlchemy ORM

In modern FastAPI applications,

this is the preferred approach.

```python
from sqlalchemy.orm import Session

def login(
    username: str,
    password: str,
    db: Session,
):

    user = (
        db.query(User)
        .filter(
            User.username == username,
            User.password == password,
        )
        .first()
    )

    return user
```

SQLAlchemy automatically creates

parameterized SQL.

You don't manually build SQL strings.

______________________________________________________________________

# Why ORMs Help

Instead of writing

SQL strings,

you work with Python objects.

Example

```text id="sql209"
Python Objects

↓

SQLAlchemy

↓

Parameterized SQL

↓

Database
```

This greatly reduces

the chance of SQL Injection.

______________________________________________________________________

# Additional Protection

Parameterized queries are essential,

but they're not the only defense.

Also use:

- Input validation
- Least-privilege database users
- Logging
- Code reviews
- ORM libraries where appropriate

Security should have multiple layers.

______________________________________________________________________

# Password Storage

Notice something else?

Our earlier examples compared

plain-text passwords.

Production systems should **never** store passwords as plain text.

Instead,

store hashed passwords.

We'll cover:

- bcrypt
- Argon2
- Password hashing

in a later lesson.

______________________________________________________________________

# Common Mistakes

### String Formatting

Avoid

```python
query = f"... {username} ..."
```

______________________________________________________________________

### String Concatenation

Avoid

```python
query = (
    "SELECT * FROM users WHERE username='"
    + username
    + "'"
)
```

______________________________________________________________________

### Assuming Input Validation Is Enough

Input validation is helpful,

but it is **not** a replacement

for parameterized queries.

Always use both.

______________________________________________________________________

### Writing Raw SQL Everywhere

If you're using SQLAlchemy,

prefer ORM queries whenever practical.

Only write raw SQL when necessary,

and parameterize it.

______________________________________________________________________

# Best Practices

✅ Use parameterized queries.

✅ Prefer SQLAlchemy ORM.

✅ Validate incoming data.

✅ Hash passwords.

✅ Give the database user only required permissions.

✅ Log suspicious database errors.

✅ Never trust user input.

______________________________________________________________________

# Quick Comparison

| Unsafe | Safe |
| ------------------------- | --------------------- |
| String concatenation | Parameterized queries |
| f-strings for SQL | SQLAlchemy ORM |
| Plain-text passwords | Password hashing |
| Full database permissions | Least privilege |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is SQL Injection, and how do you prevent it in Python?

SQL Injection occurs when untrusted user input becomes part of a SQL query, allowing the database to interpret the input
as SQL instead of data. The primary defense is to use parameterized queries or an ORM such as SQLAlchemy, which
automatically binds user input as parameters rather than embedding it into the SQL statement. Additional protections
include input validation, least-privilege database accounts, password hashing, and secure coding practices.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What SQL Injection is
- Why it happens
- The root cause
- Vulnerable Python code
- Parameterized queries
- SQLAlchemy ORM
- Best practices
- Common mistakes

______________________________________________________________________

# What's Next

[Cross-Site Scripting (XSS)](03-cross-site-scripting.md)

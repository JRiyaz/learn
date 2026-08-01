# Transactions, Locking & Concurrency

## Introduction

Modern databases are designed to support **thousands or even millions of concurrent users**. Imagine the following
scenarios happening at the same time:

- Two users try to buy the last product in stock.
- Hundreds of customers place orders simultaneously during a flash sale.
- Two ATMs withdraw money from the same bank account.
- Multiple employees update the same customer record.

If a database simply executed all operations without coordination, data would quickly become inconsistent.

To solve this, relational databases provide:

- Transactions
- Locks
- Isolation Levels
- MVCC (Multi-Version Concurrency Control)
- Deadlock Detection

These mechanisms ensure that concurrent operations produce correct and predictable results.

This lecture focuses on **how databases handle concurrent access**, a topic frequently asked in senior backend
interviews.

______________________________________________________________________

# Recap: What is a Transaction?

A **transaction** is a sequence of one or more SQL statements executed as a single logical unit.

A transaction has only two possible outcomes:

- **COMMIT** – Permanently save changes.
- **ROLLBACK** – Undo all changes.

Example

```sql id="txn001"
BEGIN;

UPDATE accounts
SET balance = balance - 1000
WHERE account_id = 1;

UPDATE accounts
SET balance = balance + 1000
WHERE account_id = 2;

COMMIT;
```

If either update fails, the transaction should be rolled back.

______________________________________________________________________

# Why Concurrency Control?

Suppose Account A has ₹10,000.

Two users withdraw ₹8,000 simultaneously.

Without concurrency control:

```text id="txn002"
Initial Balance

10000

↓

Transaction A Reads

10000

↓

Transaction B Reads

10000

↓

Both Withdraw 8000

↓

Final Balance

2000
```

The correct balance should be **₹2,000 after one successful withdrawal**, and the second withdrawal should fail because
only ₹2,000 remains.

Concurrency control prevents such inconsistencies.

______________________________________________________________________

# What is a Lock?

A **lock** temporarily restricts access to data so multiple transactions do not corrupt it.

Conceptually

```text id="txn003"
Transaction A

↓

Locks Row

↓

Updates Row

↓

Commits

↓

Unlocks Row
```

During this time, another transaction may have to wait, depending on the lock type and isolation level.

______________________________________________________________________

# Shared Lock (Read Lock)

A Shared Lock allows multiple transactions to read the same data.

Example

```text id="txn004"
Transaction A

READ

↓

Transaction B

READ
```

Both can read simultaneously.

Updates may be blocked until the shared locks are released, depending on the database system.

______________________________________________________________________

# Exclusive Lock (Write Lock)

An Exclusive Lock allows only one transaction to modify a row.

```text id="txn005"
Transaction A

WRITE

↓

Lock

↓

Transaction B Waits
```

No other transaction can modify the locked row until the lock is released.

______________________________________________________________________

# Row-Level Lock

Many modern databases lock only the affected rows.

Example

```sql id="txn006"
UPDATE employees
SET salary = 90000
WHERE employee_id = 5;
```

Only the row with `employee_id = 5` is locked.

This allows higher concurrency than locking the entire table.

______________________________________________________________________

# Table-Level Lock

Some operations lock an entire table.

Conceptually

```text id="txn007"
Employees Table

↓

Locked

↓

All Writers Wait
```

Table locks reduce concurrency and are generally used only when necessary.

______________________________________________________________________

# Explicit Row Locking

Sometimes an application needs to lock rows before updating them.

Example (PostgreSQL)

```sql id="txn008"
BEGIN;

SELECT *
FROM accounts
WHERE account_id = 1
FOR UPDATE;

UPDATE accounts
SET balance = balance - 1000
WHERE account_id = 1;

COMMIT;
```

`FOR UPDATE` locks the selected rows until the transaction completes.

______________________________________________________________________

# Multi-Version Concurrency Control (MVCC)

PostgreSQL uses **MVCC** instead of blocking readers with writers.

Instead of modifying a row directly:

```text id="txn009"
Old Version

↓

New Version

↓

Readers Continue

↓

Old Version Removed Later
```

Readers continue seeing a consistent snapshot while writers create new row versions.

Benefits:

- Higher concurrency
- Fewer read locks
- Better scalability

Interview Tip:

**MVCC is one of PostgreSQL's biggest performance advantages.**

______________________________________________________________________

# Isolation Levels

Isolation levels define how much one transaction can see changes made by another transaction.

The SQL standard defines four levels:

1. READ UNCOMMITTED
1. READ COMMITTED
1. REPEATABLE READ
1. SERIALIZABLE

Higher isolation generally means greater consistency but lower concurrency.

______________________________________________________________________

# READ UNCOMMITTED

Lowest isolation level.

Transactions may read changes that have **not yet been committed**.

This can lead to **Dirty Reads**.

> Note: PostgreSQL does **not** implement a true READ UNCOMMITTED level. Requests for READ UNCOMMITTED behave like READ COMMITTED.

______________________________________________________________________

# READ COMMITTED

Default isolation level in PostgreSQL.

A transaction sees only committed data.

Dirty Reads are prevented.

However:

- Non-repeatable Reads are possible.
- Phantom Reads are possible.

______________________________________________________________________

# REPEATABLE READ

Rows read once remain consistent throughout the transaction.

Prevents:

- Dirty Reads
- Non-repeatable Reads

Phantom behavior depends on the database implementation. PostgreSQL's implementation is stronger than the SQL standard
in several respects because it is based on MVCC.

______________________________________________________________________

# SERIALIZABLE

Highest isolation level.

Transactions behave as if executed one after another.

Prevents:

- Dirty Reads
- Non-repeatable Reads
- Phantom Reads

Trade-offs:

- Lower concurrency
- Higher overhead
- Possible serialization failures that require retrying the transaction

______________________________________________________________________

# Concurrency Problems

Understanding these anomalies is a favorite interview topic.

______________________________________________________________________

# Dirty Read

Transaction A updates data but has **not committed**.

Transaction B reads the uncommitted value.

Transaction A rolls back.

Transaction B has read data that never actually existed in a committed state.

______________________________________________________________________

# Non-Repeatable Read

Transaction A reads a row.

Transaction B updates and commits the same row.

Transaction A reads the row again and gets a different value.

______________________________________________________________________

# Phantom Read

Transaction A queries:

```sql id="txn010"
SELECT *
FROM employees
WHERE salary > 80000;
```

Transaction B inserts a new employee with salary 90000 and commits.

Transaction A executes the same query again and now sees an extra row.

That new row is called a **phantom**.

______________________________________________________________________

# Isolation Level Comparison

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read\* |
| ---------------- | ---------- | ------------------- | ---------------------------------------------------------------------------- |
| READ UNCOMMITTED | Possible | Possible | Possible |
| READ COMMITTED | Prevented | Possible | Possible |
| REPEATABLE READ | Prevented | Prevented | Database-dependent (PostgreSQL prevents many phantom scenarios through MVCC) |
| SERIALIZABLE | Prevented | Prevented | Prevented |

\*Behavior can vary by database implementation.

______________________________________________________________________

# Deadlock

A deadlock occurs when two or more transactions wait indefinitely for each other.

Example

```text id="txn011"
Transaction A

Locks Row 1

↓

Needs Row 2

----------------

Transaction B

Locks Row 2

↓

Needs Row 1
```

Neither transaction can proceed.

______________________________________________________________________

# Deadlock Resolution

Most databases automatically detect deadlocks.

One transaction is chosen as the **victim** and rolled back.

The application should retry the transaction.

______________________________________________________________________

# Optimistic Locking

Assumes conflicts are rare.

A version number or timestamp is checked before updating.

Example

```text id="txn012"
Version = 5

↓

Update

↓

WHERE version = 5

↓

Increment Version
```

If another transaction has already updated the row, the version changes and the update affects zero rows. The
application can detect the conflict and retry or report it.

Useful for:

- Web applications
- REST APIs
- Low-conflict systems

______________________________________________________________________

# Pessimistic Locking

Assumes conflicts are likely.

Rows are locked before modification.

Example

```sql id="txn013"
SELECT *
FROM accounts
WHERE account_id = 1
FOR UPDATE;
```

Useful for:

- Banking
- Financial systems
- Inventory management

______________________________________________________________________

# SQLAlchemy Transactions

```python id="txn014"
from sqlalchemy.orm import Session

with Session(engine) as session:
    with session.begin():
        employee.salary = 90000
```

If an exception occurs inside `session.begin()`, SQLAlchemy automatically rolls back the transaction.

______________________________________________________________________

# SQLAlchemy Row Locking

```python id="txn015"
stmt = (
    select(Employee)
    .where(Employee.employee_id == 1)
    .with_for_update()
)
```

This generates `SELECT ... FOR UPDATE` on databases that support it.

______________________________________________________________________

# SQLModel Transactions

```python id="txn016"
with Session(engine) as session:
    with session.begin():
        session.add(employee)
```

SQLModel relies on SQLAlchemy's transaction management.

______________________________________________________________________

# Performance Considerations

- Keep transactions as short as possible.
- Avoid user interaction while a transaction is open.
- Lock only the rows you need.
- Commit promptly.
- Retry transactions when serialization failures or deadlocks occur.
- Monitor long-running transactions because they can block cleanup operations in MVCC databases.

______________________________________________________________________

# Common Mistakes

### Long Transactions

Holding locks for a long time reduces concurrency.

______________________________________________________________________

### Ignoring Deadlocks

Applications should catch deadlock exceptions and retry when appropriate.

______________________________________________________________________

### Choosing SERIALIZABLE Unnecessarily

Higher isolation is not always better.

Use the lowest isolation level that satisfies the application's correctness requirements.

______________________________________________________________________

### Forgetting to Roll Back on Errors

Always ensure failed transactions are rolled back.

______________________________________________________________________

# Best Practices

- Keep transactions short.
- Use indexes to reduce lock duration.
- Lock rows instead of tables whenever possible.
- Understand your database's default isolation level.
- Use optimistic locking when conflicts are rare.
- Use pessimistic locking when data integrity is critical.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between optimistic locking and pessimistic locking?

Optimistic locking assumes conflicts are uncommon. It allows concurrent access and detects conflicts during update,
typically using a version number or timestamp. If another transaction has modified the row, the update fails and can be
retried. Pessimistic locking assumes conflicts are likely and locks the data before modification, preventing other
transactions from making conflicting changes. Optimistic locking provides higher concurrency, while pessimistic locking
provides stronger protection for highly contended data.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is a lock?
1. Explain shared and exclusive locks.
1. What is MVCC?
1. Explain the four isolation levels.
1. What is a dirty read?
1. What is a non-repeatable read?
1. What is a phantom read?
1. What is a deadlock?
1. Difference between optimistic and pessimistic locking.
1. Why does PostgreSQL use MVCC?

## Coding

1. Write a transaction for transferring money.
1. Lock rows using `FOR UPDATE`.
1. Simulate a deadlock scenario.
1. Demonstrate optimistic locking using a version column.
1. Demonstrate pessimistic locking.

______________________________________________________________________

# Hands-on Exercise

Create a simple banking database with an `accounts` table.

1. Implement a money transfer transaction.
1. Roll back the transaction when an update fails.
1. Lock rows using `FOR UPDATE`.
1. Experiment with different isolation levels.
1. Observe deadlock behavior using two sessions.
1. Implement optimistic locking with a version column.
1. Rewrite applicable examples using SQLAlchemy.
1. Rewrite applicable examples using SQLModel.

______________________________________________________________________

# Cheat Sheet

```text id="txn017"
Transactions

↓

Locks

Shared
Exclusive

↓

MVCC

↓

Isolation Levels

READ COMMITTED
REPEATABLE READ
SERIALIZABLE

↓

Concurrency Problems

Dirty Read
Non-Repeatable Read
Phantom Read

↓

Deadlock

↓

Optimistic Locking
Pessimistic Locking
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Transactions and concurrency
- Shared and exclusive locks
- Row-level and table-level locking
- `SELECT ... FOR UPDATE`
- MVCC
- Isolation levels
- Dirty reads
- Non-repeatable reads
- Phantom reads
- Deadlocks
- Optimistic locking
- Pessimistic locking
- SQLAlchemy transaction management
- SQLModel transaction management
- Performance considerations
- Interview patterns
- Best practices

You now understand how relational databases maintain correctness and consistency under concurrent workloads—an essential
topic for backend engineering and senior SQL interviews.

______________________________________________________________________

## Next File

[SQL Functions & Auto Increment](11.sql-functions-auto-increment.md)

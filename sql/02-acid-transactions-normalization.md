# ACID, Transactions & Normalization

## Introduction

Databases are trusted to store some of the most critical information in software systems—bank balances, orders,
payments, inventory, healthcare records, and more. Imagine transferring money from one account to another or placing an
order on an e-commerce website. If a system crashes halfway through the operation, the database must still guarantee
that the data remains correct and consistent.

This is where **ACID properties**, **transactions**, and **normalization** become essential. These are among the most
frequently asked SQL interview topics because they demonstrate your understanding of how databases maintain reliability
and integrity.

______________________________________________________________________

# What is a Transaction?

A **transaction** is a sequence of one or more database operations that are treated as a single logical unit of work.

Either **all operations succeed**, or **none of them are applied**.

Example:

Suppose Alice transfers ₹1,000 to Bob.

The transaction consists of two operations:

1. Deduct ₹1,000 from Alice's account.
1. Add ₹1,000 to Bob's account.

If the second operation fails after the first succeeds, the database must undo the first operation to prevent
inconsistent data.

______________________________________________________________________

# Why Do We Need Transactions?

Without transactions:

- Money could disappear during transfers.
- Orders might be created without payment.
- Inventory could become inconsistent.
- Partial updates could corrupt data.

Transactions ensure that data always remains in a valid state.

______________________________________________________________________

# ACID Properties

Every reliable relational database follows the **ACID** principles.

- Atomicity
- Consistency
- Isolation
- Durability

______________________________________________________________________

# Atomicity

**Definition**

A transaction is treated as a single unit.

Either everything succeeds or everything fails.

Example:

```text
Transfer ₹1,000

Step 1:
Deduct from Alice

Step 2:
Add to Bob
```

If Step 2 fails, Step 1 is automatically rolled back.

Think of Atomicity as an **all-or-nothing** rule.

______________________________________________________________________

# Consistency

**Definition**

A transaction moves the database from one valid state to another valid state.

Example:

Before transfer:

```text
Alice = ₹5000
Bob   = ₹3000

Total = ₹8000
```

After transferring ₹1000:

```text
Alice = ₹4000
Bob   = ₹4000

Total = ₹8000
```

The total money remains unchanged.

Consistency ensures that database rules and constraints are never violated.

______________________________________________________________________

# Isolation

**Definition**

Multiple transactions should not interfere with one another.

Imagine two users booking the last movie ticket simultaneously.

Without isolation:

```text
User A buys seat A1

User B buys seat A1
```

Both users could believe they successfully booked the same seat.

Isolation prevents these kinds of conflicts.

______________________________________________________________________

# Durability

**Definition**

Once a transaction is committed, the data is permanently stored.

Even if the server crashes immediately after the commit, the changes are not lost.

Example:

```text
Payment Successful

↓

Power Failure

↓

Payment is still recorded.
```

Databases achieve durability using transaction logs and recovery mechanisms.

______________________________________________________________________

# ACID Summary

| Property | Meaning |
| ----------- | ---------------------------------------- |
| Atomicity | All operations succeed or none do |
| Consistency | Database remains valid |
| Isolation | Concurrent transactions do not interfere |
| Durability | Committed data survives failures |

______________________________________________________________________

# Transaction Lifecycle

```text
BEGIN

↓

Execute SQL Statements

↓

COMMIT
      or
ROLLBACK
```

______________________________________________________________________

# COMMIT

A **COMMIT** permanently saves all changes made during the transaction.

After a commit:

- Changes become visible.
- Changes cannot be automatically undone.

______________________________________________________________________

# ROLLBACK

A **ROLLBACK** cancels all changes made during the transaction.

The database returns to the state before the transaction started.

______________________________________________________________________

# SAVEPOINT

A **SAVEPOINT** allows rolling back only part of a transaction instead of the entire transaction.

Example:

```text
BEGIN

↓

Insert Employee

↓

SAVEPOINT A

↓

Insert Department

↓

Error

↓

ROLLBACK TO A

↓

COMMIT
```

Only the operations after the savepoint are undone.

______________________________________________________________________

# What is Normalization?

Normalization is the process of organizing data to:

- Reduce duplication
- Improve consistency
- Simplify maintenance
- Prevent update anomalies

______________________________________________________________________

# Why Normalize?

Poor database design often leads to:

- Duplicate information
- Difficult updates
- Incorrect data
- Wasted storage

Normalization addresses these problems by structuring data efficiently.

______________________________________________________________________

# First Normal Form (1NF)

A table is in **First Normal Form** if:

- Each column contains atomic (indivisible) values.
- There are no repeating groups.
- Each row is unique.

❌ Not in 1NF

| Student | Subjects |
| ------- | ------------- |
| Alice | Math, Physics |

✅ In 1NF

| Student | Subject |
| ------- | ------- |
| Alice | Math |
| Alice | Physics |

______________________________________________________________________

# Second Normal Form (2NF)

Requirements:

- Must already satisfy 1NF.
- Every non-key column depends on the **entire primary key**, not just part of it.

This mainly applies to tables with composite keys.

______________________________________________________________________

# Third Normal Form (3NF)

Requirements:

- Must satisfy 2NF.
- No transitive dependencies.

Example:

❌

| EmployeeID | DepartmentID | DepartmentName |

Here, `DepartmentName` depends on `DepartmentID`, not directly on `EmployeeID`.

Instead:

Employees

| EmployeeID | DepartmentID |

Departments

| DepartmentID | DepartmentName |

______________________________________________________________________

# Boyce-Codd Normal Form (BCNF)

BCNF is a stricter version of 3NF.

Every determinant in the table must be a candidate key.

For most applications, designing tables up to **3NF** is sufficient.

BCNF becomes useful in more complex database designs.

______________________________________________________________________

# Denormalization

Denormalization intentionally introduces redundancy to improve read performance.

Advantages:

- Faster queries
- Fewer joins

Disadvantages:

- More duplicate data
- Higher storage requirements
- More complex updates

Use denormalization only when performance requirements justify it.

______________________________________________________________________

# Common Interview Questions

### What is the difference between COMMIT and ROLLBACK?

- **COMMIT** permanently saves changes.
- **ROLLBACK** discards changes since the transaction began or since a savepoint.

______________________________________________________________________

### Why is Normalization important?

Normalization reduces redundancy, prevents inconsistencies, and improves data integrity.

______________________________________________________________________

### Should every database be normalized?

Not necessarily.

Highly transactional systems benefit from normalization, while analytics-heavy systems may intentionally denormalize for
performance.

______________________________________________________________________

# Common Mistakes

- Confusing transactions with queries.
- Assuming COMMIT can be undone.
- Over-normalizing small databases.
- Ignoring performance implications of excessive joins.
- Thinking denormalization is always bad.

______________________________________________________________________

# Best Practices

- Keep transactions as short as possible.
- Commit only after all operations succeed.
- Roll back on failure.
- Normalize data up to 3NF unless there is a clear performance reason not to.
- Benchmark before denormalizing.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Explain ACID properties with a banking example.

When transferring money between two bank accounts, both the debit and credit operations must succeed together
(Atomicity). The total amount of money in the system should remain unchanged (Consistency). Simultaneous transfers
should not interfere with one another (Isolation). Once the transfer is completed, it should remain saved even if the
database server crashes immediately afterward (Durability).

______________________________________________________________________

# Practice Questions

### Conceptual

1. What is a transaction?
1. Explain each ACID property.
1. What is the difference between COMMIT and ROLLBACK?
1. What is a SAVEPOINT?
1. What is normalization?
1. Explain 1NF, 2NF, 3NF, and BCNF.
1. What is denormalization?
1. When would you denormalize a database?

### Scenario-Based

1. Design a transaction for an ATM withdrawal.
1. Normalize a student-course database.
1. Explain why an e-commerce checkout should use transactions.

______________________________________________________________________

# Hands-on Exercise

Given the following table:

| Student | Course | Instructor |
| ------- | ----------- | ----------- |
| Alice | SQL, Python | John, David |

1. Convert the table into 1NF.
1. Identify any normalization issues.
1. Redesign the schema up to 3NF.

______________________________________________________________________

# Cheat Sheet

```text
Transaction
    ↓
ACID
├── Atomicity
├── Consistency
├── Isolation
└── Durability

Normalization
├── 1NF
├── 2NF
├── 3NF
└── BCNF

Performance
    ↓
Denormalization (when appropriate)
```

______________________________________________________________________

# Summary

In this lesson, you learned:

- Transactions
- ACID properties
- COMMIT
- ROLLBACK
- SAVEPOINT
- Normalization
- 1NF
- 2NF
- 3NF
- BCNF
- Denormalization
- Interview best practices

These concepts are the foundation for understanding how relational databases ensure correctness, consistency, and
efficient schema design.

______________________________________________________________________

## Next File

[SQL CRUD & Filtering](03-sql-crud-filtering.md)

# 18. SQL Fundamentals

**Previous:** [17. Flask](./17-flask.md)

**Next:** [19. SQL Advanced & Transactions](./19-sql-advanced-transactions.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain relational databases and core SQL concepts.
- Write and reason about common CRUD queries.
- Use filtering, sorting and aggregation correctly.
- Explain and write different types of joins.
- Use subqueries, CTEs, `CASE`, `UNION` and `UNION ALL`.
- Understand `NULL` and SQL's three-valued logic.
- Explain primary keys, foreign keys and common constraints.
- Explain indexes and composite indexes at an interview-ready level.
- Understand transactions and the ACID properties.
- Explain database normalization through 1NF, 2NF and 3NF.
- Recognize when denormalization may be appropriate.
- Understand basic locking, isolation and deadlock concepts.
- Read basic `EXPLAIN` output and reason about query performance.
- Apply SQL concepts to Python backend development.
- Answer common SQL interview questions confidently.

> **Scope note:** This file establishes SQL fundamentals. Deeper transaction/isolation behavior, locking, advanced query optimization and database internals continue in **19. SQL Advanced & Transactions**.

______________________________________________________________________

# 1. What Is a Relational Database?

A relational database stores data in tables made up of:

- Rows
- Columns

Tables can be related through keys.

For example:

```text
users
orders
products
```

An order can reference the user who created it through a foreign key.

______________________________________________________________________

# 2. Table, Row and Column

Consider:

```text
users

id | name  | email
---+-------+----------------
1  | Alice | alice@example.com
2  | Bob   | bob@example.com
```

Here:

- `users` is the table.
- Each horizontal record is a row.
- `id`, `name` and `email` are columns.

A column represents an attribute.

A row represents one record.

______________________________________________________________________

# 3. SQL

SQL stands for Structured Query Language.

It is used to interact with relational databases.

Major categories include:

### DQL

Data Query Language:

```sql
SELECT
```

### DML

Data Manipulation Language:

```sql
INSERT
UPDATE
DELETE
```

### DDL

Data Definition Language:

```sql
CREATE
ALTER
DROP
```

### TCL

Transaction Control Language:

```sql
COMMIT
ROLLBACK
```

The exact classification can vary by convention, but the important interview concept is understanding what each
operation does.

______________________________________________________________________

# 4. SELECT

Basic query:

```sql
SELECT id, name, email
FROM users;
```

Avoid:

```sql
SELECT *
FROM users;
```

in production code when you only need a subset of columns.

Selecting unnecessary columns can increase:

- Database work
- Network transfer
- Serialization cost
- Application memory usage

______________________________________________________________________

# 5. WHERE

`WHERE` filters rows.

```sql
SELECT id, name
FROM users
WHERE active = TRUE;
```

Multiple conditions:

```sql
SELECT *
FROM users
WHERE active = TRUE
  AND age >= 18;
```

______________________________________________________________________

# 6. Comparison Operators

Common operators:

```sql
=
<>
!=
>
<
>=
<=
```

Example:

```sql
SELECT *
FROM products
WHERE price >= 100;
```

______________________________________________________________________

# 7. AND, OR and NOT

Examples:

```sql
WHERE status = 'active'
  AND age >= 18
```

```sql
WHERE status = 'active'
   OR status = 'pending'
```

```sql
WHERE NOT deleted
```

Use parentheses when combining complex conditions:

```sql
WHERE status = 'active'
  AND (role = 'admin' OR role = 'manager')
```

______________________________________________________________________

# 8. IN

`IN` checks membership in a set.

```sql
SELECT *
FROM users
WHERE role IN ('admin', 'manager');
```

It is often cleaner than multiple `OR` conditions.

______________________________________________________________________

# 9. BETWEEN

`BETWEEN` checks whether a value falls within a range.

```sql
SELECT *
FROM products
WHERE price BETWEEN 100 AND 500;
```

For timestamps, be careful with boundary semantics.

For time ranges, a half-open interval is often safer:

```text
>= start
< end
```

instead of relying on inclusive timestamp boundaries.

______________________________________________________________________

# 10. LIKE

`LIKE` performs pattern matching.

```sql
SELECT *
FROM users
WHERE name LIKE 'Ali%';
```

Common wildcards:

```text
%  → zero or more characters
_  → one character
```

Pattern matching can have performance implications, particularly with a leading wildcard:

```sql
WHERE name LIKE '%abc'
```

______________________________________________________________________

# 11. ORDER BY

Sort results:

```sql
SELECT id, name
FROM users
ORDER BY name ASC;
```

Descending:

```sql
ORDER BY created_at DESC;
```

Multiple columns:

```sql
ORDER BY status ASC, created_at DESC;
```

______________________________________________________________________

# 12. LIMIT

Limit the number of rows:

```sql
SELECT *
FROM users
ORDER BY created_at DESC
LIMIT 20;
```

This is commonly used for pagination and bounded queries.

Do not confuse `LIMIT` with a complete pagination strategy.

______________________________________________________________________

# 13. INSERT

Insert a row:

```sql
INSERT INTO users (name, email)
VALUES ('Alice', 'alice@example.com');
```

Always specify the columns when practical rather than relying on implicit column order.

______________________________________________________________________

# 14. UPDATE

Update rows:

```sql
UPDATE users
SET name = 'Alice Smith'
WHERE id = 1;
```

The `WHERE` clause is critical.

Without it:

```sql
UPDATE users
SET name = 'Alice Smith';
```

could update every row.

______________________________________________________________________

# 15. DELETE

Delete rows:

```sql
DELETE FROM users
WHERE id = 1;
```

Again, omitting `WHERE` can delete every matching row in the table.

Production applications should have deliberate deletion and backup/recovery strategies.

______________________________________________________________________

# 16. Aggregate Functions

Common aggregate functions include:

```sql
COUNT()
SUM()
AVG()
MIN()
MAX()
```

Example:

```sql
SELECT COUNT(*)
FROM users;
```

Another example:

```sql
SELECT AVG(price)
FROM products;
```

______________________________________________________________________

# 17. GROUP BY

`GROUP BY` groups rows for aggregation.

Example:

```sql
SELECT status, COUNT(*)
FROM orders
GROUP BY status;
```

Result:

```text
status     count
---------  -----
pending    20
completed  100
cancelled  5
```

______________________________________________________________________

# 18. HAVING

`HAVING` filters groups after aggregation.

Example:

```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 10;
```

A useful distinction:

```text
WHERE  → filters rows before grouping
HAVING → filters groups after grouping
```

______________________________________________________________________

# 19. SQL Execution Order

A simplified logical processing order is:

```text
FROM
JOIN
WHERE
GROUP BY
HAVING
SELECT
ORDER BY
LIMIT
```

The exact internal database execution plan can differ.

The logical order is useful for understanding why aliases and aggregates behave differently in different clauses.

______________________________________________________________________

# 20. DISTINCT

`DISTINCT` removes duplicate result rows.

```sql
SELECT DISTINCT status
FROM orders;
```

It can be useful, but it may require additional database work.

Do not use it simply to hide an incorrect join that is producing duplicates.

______________________________________________________________________

# 21. INNER JOIN

An `INNER JOIN` returns matching rows from both tables.

```sql
SELECT
    users.id,
    users.name,
    orders.id AS order_id
FROM users
INNER JOIN orders
    ON orders.user_id = users.id;
```

Users without matching orders are excluded.

______________________________________________________________________

# 22. LEFT JOIN

A `LEFT JOIN` keeps every row from the left table.

```sql
SELECT
    users.id,
    users.name,
    orders.id AS order_id
FROM users
LEFT JOIN orders
    ON orders.user_id = users.id;
```

Users without orders still appear, with `NULL` for order columns.

This is useful for questions such as:

> Find all users, including users who have never placed an order.

______________________________________________________________________

# 23. RIGHT JOIN

A `RIGHT JOIN` keeps every row from the right table.

It is conceptually the reverse of a `LEFT JOIN`.

Many teams prefer rewriting it as a `LEFT JOIN` by changing table order because that can be easier to read.

______________________________________________________________________

# 24. FULL OUTER JOIN

A `FULL OUTER JOIN` keeps rows from both sides, matching where possible.

Conceptually:

```text
Left-only
+
Matches
+
Right-only
```

Database support varies, so know whether your chosen database supports it.

______________________________________________________________________

# 25. CROSS JOIN

A `CROSS JOIN` creates a Cartesian product.

If:

```text
users = 100 rows
products = 50 rows
```

then:

```sql
CROSS JOIN
```

can produce:

```text
100 × 50 = 5000 rows
```

Use it deliberately.

______________________________________________________________________

# 26. SELF JOIN

A table can join to itself.

Example:

```text
employees
id
name
manager_id
```

Query:

```sql
SELECT
    e.name AS employee,
    m.name AS manager
FROM employees e
LEFT JOIN employees m
    ON e.manager_id = m.id;
```

This is a self join.

______________________________________________________________________

# 27. JOIN Conditions

A join normally needs a relationship condition:

```sql
ON orders.user_id = users.id
```

An incorrect join condition can produce:

- Missing rows
- Duplicate rows
- Cartesian-like explosions
- Incorrect business results

When debugging a query, verify the relationship cardinality.

______________________________________________________________________

# 28. One-to-One, One-to-Many and Many-to-Many

Common relationships:

### One-to-one

```text
user → profile
```

### One-to-many

```text
user → orders
```

### Many-to-many

```text
students ↔ courses
```

Many-to-many relationships are commonly represented using a junction table:

```text
student_courses
```

______________________________________________________________________

# 29. Subqueries

A subquery is a query nested inside another query.

Example:

```sql
SELECT *
FROM users
WHERE id IN (
    SELECT user_id
    FROM orders
);
```

Subqueries can be useful, but joins, CTEs or other formulations may sometimes produce clearer or more efficient queries.

Let the query plan and semantics guide the choice.

______________________________________________________________________

# 30. Correlated Subqueries

A correlated subquery refers to a row from the outer query.

Conceptually:

```sql
SELECT *
FROM users u
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = u.id
);
```

The inner query depends on the current outer row.

`EXISTS` is often useful when you only need to know whether a related row exists.

______________________________________________________________________

# 31. EXISTS

Example:

```sql
SELECT *
FROM users u
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = u.id
);
```

This asks:

> Does at least one order exist for this user?

It can be preferable to joining and then using `DISTINCT` when only existence matters.

______________________________________________________________________

# 32. CTEs

A Common Table Expression uses `WITH`.

Example:

```sql
WITH active_users AS (
    SELECT *
    FROM users
    WHERE active = TRUE
)
SELECT *
FROM active_users;
```

CTEs can improve readability by breaking a complex query into logical steps.

They are not automatically faster than equivalent queries; performance depends on the database and query.

______________________________________________________________________

# 33. Multiple CTEs

You can define multiple CTEs:

```sql
WITH active_users AS (
    ...
),
recent_orders AS (
    ...
)
SELECT ...
FROM active_users
JOIN recent_orders
    ON ...;
```

This can make complex analytical or reporting queries easier to understand.

______________________________________________________________________

# 34. CASE

`CASE` provides conditional expressions.

Example:

```sql
SELECT
    name,
    CASE
        WHEN age >= 18 THEN 'adult'
        ELSE 'minor'
    END AS category
FROM users;
```

It is useful for deriving values in a query.

______________________________________________________________________

# 35. UNION

`UNION` combines compatible result sets and removes duplicate rows.

```sql
SELECT email FROM customers
UNION
SELECT email FROM employees;
```

The participating queries need compatible column structures/types.

______________________________________________________________________

# 36. UNION ALL

`UNION ALL` combines result sets without removing duplicates.

```sql
SELECT email FROM customers
UNION ALL
SELECT email FROM employees;
```

Because it does not perform duplicate elimination, it can be more efficient when duplicates are intentionally allowed.

______________________________________________________________________

# 37. NULL

`NULL` represents an unknown/missing value.

It is not the same as:

```text
0
''
FALSE
```

This is important.

______________________________________________________________________

# 38. NULL Comparisons

This is incorrect:

```sql
WHERE deleted_at = NULL
```

Use:

```sql
WHERE deleted_at IS NULL
```

and:

```sql
WHERE deleted_at IS NOT NULL
```

______________________________________________________________________

# 39. Three-Valued Logic

SQL conditions can evaluate to:

```text
TRUE
FALSE
UNKNOWN
```

`NULL` can produce `UNKNOWN`.

For example:

```sql
5 = NULL
```

does not evaluate to true.

Understanding three-valued logic is important for avoiding subtle filtering bugs.

______________________________________________________________________

# 40. COALESCE

`COALESCE` returns the first non-null value.

Example:

```sql
SELECT COALESCE(display_name, username)
FROM users;
```

If `display_name` is null, `username` is returned.

______________________________________________________________________

# 41. Primary Key

A primary key uniquely identifies a row.

Example:

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100)
);
```

A primary key generally implies uniqueness and non-nullability.

______________________________________________________________________

# 42. Foreign Key

A foreign key represents a relationship between tables.

Example:

```sql
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

This can enforce referential integrity.

______________________________________________________________________

# 43. UNIQUE Constraint

A unique constraint prevents duplicate values for the constrained key/column combination.

Example:

```sql
email VARCHAR(255) UNIQUE
```

This is often appropriate for identifiers such as unique usernames or emails when the domain requires uniqueness.

______________________________________________________________________

# 44. NOT NULL

`NOT NULL` prevents a column from containing `NULL`.

Example:

```sql
name VARCHAR(100) NOT NULL
```

Use it when the domain requires the value to exist.

______________________________________________________________________

# 45. CHECK Constraint

A `CHECK` constraint enforces a condition.

Example:

```sql
price NUMERIC(10, 2) CHECK (price >= 0)
```

Constraints are valuable because important invariants can be enforced at the database boundary.

______________________________________________________________________

# 46. DEFAULT

A default provides a value when one is not explicitly supplied.

Example:

```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

Defaults should reflect genuine domain defaults rather than hiding missing application behavior.

______________________________________________________________________

# 47. Indexes

An index is a database data structure that can speed up lookups and other operations.

Example:

```sql
CREATE INDEX idx_users_email
ON users(email);
```

An index can make queries such as:

```sql
SELECT *
FROM users
WHERE email = 'alice@example.com';
```

more efficient.

______________________________________________________________________

# 48. Index Trade-Off

Indexes are not free.

They can:

- Consume storage
- Increase write cost
- Increase maintenance work
- Affect query planning

The goal is not:

> Add an index to every column.

The goal is:

> Add useful indexes based on actual query patterns.

______________________________________________________________________

# 49. Composite Indexes

A composite index covers multiple columns.

Example:

```sql
CREATE INDEX idx_orders_user_status
ON orders(user_id, status);
```

Column order matters.

The database can often use the leading portion of the index effectively.

Think carefully about common predicates and ordering.

______________________________________________________________________

# 50. Index Selectivity

An index is generally more useful when it can significantly reduce the rows that must be examined.

For example:

```text
country = 'India'
```

may be less selective than:

```text
email = 'unique@example.com'
```

But index usefulness depends on:

- Data distribution
- Query shape
- Table size
- Database optimizer
- Other predicates
- Sort/group requirements

Do not judge an index from column cardinality alone.

______________________________________________________________________

# 51. Query Performance

A slow query can result from:

- Missing indexes
- Poor join conditions
- Large scans
- Returning too many rows
- Expensive sorting
- Inefficient filtering
- N+1 application behavior
- Lock contention
- Resource saturation

Do not assume the query itself is the only problem.

______________________________________________________________________

# 52. EXPLAIN

`EXPLAIN` shows how a database plans to execute a query.

Example:

```sql
EXPLAIN
SELECT *
FROM users
WHERE email = 'alice@example.com';
```

Depending on the database, you may also have an execution/analyze form that provides actual runtime information.

Look for concepts such as:

- Sequential/table scans
- Index scans
- Join strategy
- Estimated rows
- Actual rows
- Sorts
- Cost

______________________________________________________________________

# 53. Sequential Scan vs Index Scan

A sequential scan examines many/all rows.

An index scan can use an index to find relevant rows more directly.

A sequential scan is not automatically bad.

For a small table or a query returning most rows, a sequential scan can be the better plan.

______________________________________________________________________

# 54. Transactions

A transaction groups operations into a logical unit.

Example:

```text
Create order
 ↓
Reduce inventory
 ↓
Create payment record
```

If these operations belong to one atomic business operation, transaction boundaries matter.

______________________________________________________________________

# 55. COMMIT

`COMMIT` makes transaction changes durable according to the database's transaction semantics.

Conceptually:

```text
BEGIN
 ↓
UPDATE
 ↓
INSERT
 ↓
COMMIT
```

______________________________________________________________________

# 56. ROLLBACK

`ROLLBACK` discards uncommitted changes in the current transaction.

```text
BEGIN
 ↓
UPDATE
 ↓
ERROR
 ↓
ROLLBACK
```

______________________________________________________________________

# 57. ACID

ACID describes important transaction properties.

### Atomicity

All operations in the transaction succeed or the transaction is rolled back.

### Consistency

The transaction preserves defined database invariants/constraints.

### Isolation

Concurrent transactions are isolated according to the configured isolation semantics.

### Durability

Committed data survives failures according to the database's durability guarantees.

______________________________________________________________________

# 58. Atomicity Example

Suppose an order operation performs:

```text
1. Create order
2. Decrease inventory
3. Create payment record
```

If step 2 fails and all three operations are part of one transaction, atomicity can prevent a partial committed result.

______________________________________________________________________

# 59. Consistency Example

Suppose:

```text
price >= 0
```

is a database constraint.

A transaction that attempts to store:

```text
price = -10
```

violates the database invariant and should not produce an invalid committed state.

______________________________________________________________________

# 60. Isolation

Isolation determines what concurrent transactions can observe and how they interact.

Common isolation levels include:

```text
Read Uncommitted
Read Committed
Repeatable Read
Serializable
```

The exact behavior and implementation can differ between database systems.

Detailed isolation anomalies are covered further in File 19.

______________________________________________________________________

# 61. Locks — Fundamentals

Databases use locking and other concurrency-control mechanisms to coordinate concurrent operations.

A lock may prevent incompatible operations from proceeding simultaneously.

Conceptually:

```text
Transaction A
   ↓
locks row
   ↓
Transaction B waits
```

Lock behavior depends on the database engine and query.

______________________________________________________________________

# 62. Deadlocks

A deadlock occurs when transactions wait on each other indefinitely until the database detects and resolves the
deadlock, typically by aborting one transaction.

Example:

```text
Transaction A locks Row 1
Transaction B locks Row 2

A waits for Row 2
B waits for Row 1
```

A common prevention technique is consistent lock ordering.

Detailed deadlock analysis is covered in File 19.

______________________________________________________________________

# 63. Normalization

Normalization organizes relational data to reduce unnecessary duplication and update anomalies.

The common normal forms relevant to backend interviews are:

```text
1NF
2NF
3NF
```

You should understand the intent, not merely memorize definitions.

______________________________________________________________________

# 64. First Normal Form — 1NF

A table is generally considered in 1NF when:

- Columns contain atomic values.
- Repeating groups are avoided.
- Each row represents a distinct record.

Bad example:

```text
user_id | phone_numbers
--------+--------------------
1       | 111,222,333
```

A normalized design could use:

```text
users
phones
```

with one phone number per row.

______________________________________________________________________

# 65. Second Normal Form — 2NF

2NF builds on 1NF and removes partial dependency on part of a composite key.

Consider:

```text
order_items
------------------------------
order_id
product_id
product_name
quantity
```

Suppose:

```text
(order_id, product_id)
```

is the composite key.

`product_name` depends only on:

```text
product_id
```

not the whole composite key.

That is a partial dependency.

Move product attributes into:

```text
products
```

______________________________________________________________________

# 66. Third Normal Form — 3NF

3NF removes transitive dependencies among non-key attributes.

Example:

```text
employees
----------------------------
employee_id
department_id
department_name
```

If:

```text
employee_id → department_id
department_id → department_name
```

then `department_name` transitively depends on `employee_id`.

A normalized design separates department information:

```text
employees
departments
```

______________________________________________________________________

# 67. Why Normalize?

Normalization helps:

- Reduce duplicate data
- Prevent inconsistent updates
- Improve data integrity
- Clarify relationships

For example, storing a customer's address in hundreds of order rows can create update anomalies if the address is
intended to be a single current customer attribute.

______________________________________________________________________

# 68. Denormalization

Denormalization intentionally introduces redundancy for a reason.

Possible reasons:

- Faster reads
- Reporting performance
- Reduced expensive joins
- Precomputed values

Example:

```text
orders
---------
customer_name
```

might duplicate customer data.

This can be reasonable when the duplicated value has deliberately defined semantics.

______________________________________________________________________

# 69. Normalization vs Denormalization

Do not treat denormalization as automatically bad.

A practical approach is:

```text
Start with a sound normalized model
        ↓
Measure workload
        ↓
Identify bottleneck
        ↓
Denormalize deliberately
        ↓
Define consistency/update strategy
```

Denormalization introduces maintenance complexity.

______________________________________________________________________

# 70. Constraints vs Application Validation

Important invariants should often be enforced at the database level.

For example:

```text
email UNIQUE
balance >= 0
order.user_id references users.id
```

Application validation improves user experience and produces clearer errors.

Database constraints protect integrity even when multiple application paths or services write to the database.

______________________________________________________________________

# 71. SQL Injection

Never construct SQL by concatenating untrusted input.

Bad:

```python
query = f"SELECT * FROM users WHERE email = '{email}'"
```

Use parameterized queries:

```python
cursor.execute(
    "SELECT * FROM users WHERE email = %s",
    (email,),
)
```

The exact placeholder syntax depends on the database driver.

ORMs can help, but unsafe raw SQL can still introduce SQL injection.

______________________________________________________________________

# 72. N+1 Query Problem

A common backend problem:

```text
1 query → load users

then:
N queries → load orders for each user
```

Total:

```text
1 + N queries
```

This can become expensive.

Solutions include:

- Appropriate joins
- Eager loading
- Batch queries
- Aggregation
- Data-loader patterns

The correct solution depends on the access pattern.

______________________________________________________________________

# 73. Pagination and SQL

Avoid returning unbounded data:

```sql
SELECT *
FROM orders;
```

For large datasets, use bounded queries and a deliberate pagination strategy.

Simple offset pagination:

```sql
SELECT *
FROM orders
ORDER BY id
LIMIT 50 OFFSET 100;
```

For large/high-churn datasets, cursor/keyset pagination may be preferable.

______________________________________________________________________

# 74. Keyset Pagination

Instead of:

```sql
OFFSET 100000
```

you can use a stable ordering key:

```sql
SELECT *
FROM orders
WHERE id > 100000
ORDER BY id
LIMIT 50;
```

This is a simplified example.

Real cursor designs need to consider:

- Stable ordering
- Ties
- Composite sort keys
- Direction
- Cursor encoding

______________________________________________________________________

# 75. NULL and Aggregates

Be aware that aggregates interact with `NULL`.

For example:

```sql
COUNT(*)
```

counts rows.

While:

```sql
COUNT(email)
```

counts non-null `email` values.

This distinction is frequently tested in interviews.

______________________________________________________________________

# 76. COUNT and JOINs

A join can multiply rows.

For example:

```text
User A → 3 orders
```

A joined result contains three rows for User A.

Therefore:

```sql
COUNT(*)
```

after the join may count orders rather than users.

Use the correct aggregation strategy, potentially including:

```sql
COUNT(DISTINCT users.id)
```

when the business question requires unique users.

______________________________________________________________________

# 77. SQL and Python Backend

In a Python backend, SQL can appear through:

- Raw database drivers
- Query builders
- ORMs
- Repository/data-access layers

Regardless of abstraction level, developers should understand the SQL generated by important operations.

An ORM does not eliminate database fundamentals.

______________________________________________________________________

# 78. ORM Awareness

A backend engineer should be able to recognize when ORM code generates:

- Multiple queries
- Large joins
- Missing filters
- Unbounded result sets
- N+1 queries

For performance debugging, inspect actual SQL and database query plans.

______________________________________________________________________

# 79. Transaction Boundary in Backend Code

A transaction should generally correspond to a coherent unit of work.

For example:

```text
API request
 ↓
Service operation
 ↓
BEGIN
 ↓
multiple DB changes
 ↓
COMMIT
```

Do not keep transactions open while performing slow unrelated network calls unless the design specifically requires it.

Long transactions can increase:

- Lock duration
- Resource usage
- Contention
- Failure impact

______________________________________________________________________

# 80. SQL Interview Heuristics

When solving a SQL interview problem:

1. Clarify the expected result.
1. Identify the tables.
1. Identify relationships.
1. Determine required filters.
1. Decide whether aggregation is needed.
1. Choose joins/subqueries/CTEs based on clarity and semantics.
1. Consider `NULL`.
1. Check duplicate-row behavior.
1. Consider indexes/performance.
1. Test edge cases.

Correctness comes before optimization.

______________________________________________________________________

# 81. Common SQL Mistakes

## Mistake 1 — Forgetting `WHERE` in `UPDATE`/`DELETE`

Can affect every row.

## Mistake 2 — Using `= NULL`

Use `IS NULL`.

## Mistake 3 — Accidental Cartesian product

Incorrect joins can explode row counts.

## Mistake 4 — Using `DISTINCT` to hide bad joins

Fix the join relationship instead.

## Mistake 5 — Selecting unnecessary columns

Avoid unnecessary `SELECT *`.

## Mistake 6 — Adding indexes everywhere

Indexes have write/storage costs.

## Mistake 7 — Ignoring transaction boundaries

Partial business operations can produce inconsistent outcomes.

## Mistake 8 — Assuming an ORM removes SQL knowledge requirements

ORM-generated SQL still executes against the database.

______________________________________________________________________

# 82. Interview Questions & Answers

## Q1. What is a relational database?

**Answer:**

A database that organizes data into related tables consisting of rows and columns, with relationships commonly
represented through keys and constraints.

______________________________________________________________________

## Q2. What is SQL?

**Answer:**

SQL is a language used to define, query and manipulate data in relational databases.

______________________________________________________________________

## Q3. What is the difference between `WHERE` and `HAVING`?

**Answer:**

`WHERE` filters rows before grouping.

`HAVING` filters groups after aggregation.

______________________________________________________________________

## Q4. What is the difference between `DELETE` and `DROP`?

**Answer:**

`DELETE` removes rows from a table.

`DROP` removes a database object such as a table itself.

______________________________________________________________________

## Q5. What is `TRUNCATE`?

**Answer:**

`TRUNCATE` removes all rows from a table using database-specific semantics that are generally optimized for removing the
entire table contents.

Its transactional and identity-reset behavior varies by database.

______________________________________________________________________

## Q6. What is an INNER JOIN?

**Answer:**

It returns rows where the join condition matches on both sides.

______________________________________________________________________

## Q7. What is a LEFT JOIN?

**Answer:**

It returns every row from the left table and matching rows from the right table. Missing right-side matches appear as
`NULL`.

______________________________________________________________________

## Q8. What is a CROSS JOIN?

**Answer:**

It creates a Cartesian product of the two input sets.

______________________________________________________________________

## Q9. What is a SELF JOIN?

**Answer:**

It joins a table to itself, commonly used for hierarchical relationships such as employee-manager structures.

______________________________________________________________________

## Q10. Why can joins create duplicate rows?

**Answer:**

Because a one-to-many or many-to-many relationship produces multiple matching rows.

For example, one user with five orders produces five joined rows for that user.

______________________________________________________________________

## Q11. What is a subquery?

**Answer:**

A query nested inside another query.

______________________________________________________________________

## Q12. What is a CTE?

**Answer:**

A Common Table Expression is a named query expression defined with `WITH`, often used to make complex queries easier to
organize.

______________________________________________________________________

## Q13. Is a CTE always faster?

**Answer:**

No.

Performance depends on the database engine and query plan.

Use CTEs primarily for clarity unless performance analysis shows otherwise.

______________________________________________________________________

## Q14. What is `EXISTS` used for?

**Answer:**

It checks whether at least one related row satisfies a condition.

It is useful when you care about existence rather than retrieving all matching rows.

______________________________________________________________________

## Q15. `UNION` vs `UNION ALL`?

**Answer:**

`UNION` removes duplicate rows.

`UNION ALL` preserves duplicates and can avoid the work required for duplicate elimination.

______________________________________________________________________

## Q16. What is `CASE`?

**Answer:**

A conditional SQL expression used to derive values based on conditions.

______________________________________________________________________

## Q17. What is `NULL`?

**Answer:**

`NULL` represents an unknown or missing value.

It is not equivalent to zero, an empty string or false.

______________________________________________________________________

## Q18. Why is `column = NULL` wrong?

**Answer:**

`NULL` participates in SQL's three-valued logic.

Use:

```sql
column IS NULL
```

instead.

______________________________________________________________________

## Q19. What is `COALESCE`?

**Answer:**

It returns the first non-null expression from its arguments.

______________________________________________________________________

## Q20. What is a primary key?

**Answer:**

A key that uniquely identifies rows in a table.

______________________________________________________________________

## Q21. What is a foreign key?

**Answer:**

A constraint that references a key in another table and can enforce referential integrity.

______________________________________________________________________

## Q22. What is a unique constraint?

**Answer:**

It prevents duplicate values for the constrained column or column combination.

______________________________________________________________________

## Q23. What is a check constraint?

**Answer:**

A database constraint that requires a specified condition to be true for stored rows.

______________________________________________________________________

## Q24. What is an index?

**Answer:**

An auxiliary data structure that can improve the efficiency of data access for suitable queries.

______________________________________________________________________

## Q25. Why not index every column?

**Answer:**

Indexes consume storage and add maintenance/write overhead.

The database should be indexed based on actual query and workload patterns.

______________________________________________________________________

## Q26. What is a composite index?

**Answer:**

An index covering multiple columns.

The column order matters because it affects which query predicates/orderings can use the index efficiently.

______________________________________________________________________

## Q27. What is index selectivity?

**Answer:**

It describes how effectively an index predicate distinguishes a small subset of rows from the overall dataset.

Higher selectivity often makes an index more useful, but actual usefulness depends on the complete query and data
distribution.

______________________________________________________________________

## Q28. What is `EXPLAIN`?

**Answer:**

It shows the database's planned execution strategy for a query.

It helps investigate scans, joins, estimated rows, sorting and other operations.

______________________________________________________________________

## Q29. Is a sequential scan always bad?

**Answer:**

No.

For small tables or queries returning a large portion of the table, a sequential scan may be the most efficient plan.

______________________________________________________________________

## Q30. What is a transaction?

**Answer:**

A transaction groups related database operations into a logical unit with defined commit/rollback semantics.

______________________________________________________________________

## Q31. What does ACID stand for?

**Answer:**

Atomicity, Consistency, Isolation and Durability.

______________________________________________________________________

## Q32. Explain atomicity.

**Answer:**

The transaction's operations are treated as one logical unit so a failure can prevent a partial committed result.

______________________________________________________________________

## Q33. Explain consistency.

**Answer:**

A successful transaction preserves the database's defined constraints and invariants.

______________________________________________________________________

## Q34. Explain isolation.

**Answer:**

Isolation defines how concurrent transactions interact and what changes they can observe under a particular isolation
level.

______________________________________________________________________

## Q35. Explain durability.

**Answer:**

Committed changes are preserved according to the database's durability guarantees, including recovery behavior after
failures.

______________________________________________________________________

## Q36. What is normalization?

**Answer:**

Normalization is the process of structuring relational data to reduce unnecessary duplication and prevent update
anomalies.

______________________________________________________________________

## Q37. What is 1NF?

**Answer:**

At a high level, 1NF requires atomic values and avoids repeating groups within a row.

______________________________________________________________________

## Q38. What is 2NF?

**Answer:**

2NF builds on 1NF and removes partial dependencies on part of a composite key.

______________________________________________________________________

## Q39. What is 3NF?

**Answer:**

3NF builds on 2NF and removes transitive dependencies where non-key attributes depend on other non-key attributes.

______________________________________________________________________

## Q40. Why normalize a database?

**Answer:**

To reduce redundant data, improve consistency and avoid insertion, update and deletion anomalies.

______________________________________________________________________

## Q41. What is denormalization?

**Answer:**

Deliberately introducing redundancy to improve read performance or simplify access patterns, with an explicit strategy
for maintaining consistency.

______________________________________________________________________

## Q42. When would you denormalize?

**Answer:**

After identifying a real workload bottleneck or access requirement where reducing joins or precomputing data provides
meaningful benefit.

______________________________________________________________________

## Q43. What is SQL injection?

**Answer:**

A security vulnerability where untrusted input changes the intended SQL statement.

Use parameterized queries rather than string concatenation.

______________________________________________________________________

## Q44. Does an ORM prevent SQL injection automatically?

**Answer:**

ORMs can provide safe parameterization for normal query APIs, but unsafe raw SQL construction can still introduce SQL
injection.

______________________________________________________________________

## Q45. What is the N+1 query problem?

**Answer:**

It occurs when an application performs one query to load a collection and then an additional query for each item.

This can turn one logical operation into many database round trips.

______________________________________________________________________

## Q46. How can you solve N+1 queries?

**Answer:**

Depending on the access pattern:

- Joins
- Eager loading
- Batch queries
- Aggregation
- Data-loader approaches

______________________________________________________________________

## Q47. What is keyset pagination?

**Answer:**

Pagination based on a stable ordering key rather than skipping a large number of rows using `OFFSET`.

It can perform better for large datasets.

______________________________________________________________________

## Q48. Why should transactions not stay open during slow network calls?

**Answer:**

Long transactions can hold locks/resources longer, increase contention and increase the impact of failures.

______________________________________________________________________

## Q49. Why is `SELECT *` often discouraged?

**Answer:**

It may retrieve unnecessary columns, increase data transfer and couple application code to schema changes.

______________________________________________________________________

## Q50. What is the most important SQL optimization rule?

**Answer:**

First make the query correct.

Then measure its actual performance using representative data and tools such as `EXPLAIN`.

Optimize based on evidence rather than assumptions.

______________________________________________________________________

# 83. Scenario-Based Questions

## Scenario 1 — Update Accident

A developer writes:

```sql
UPDATE users
SET active = FALSE;
```

**Question:** What happens?

**Answer:**

Every row may be updated because there is no `WHERE` condition.

This is why destructive SQL should be reviewed carefully and tested against the intended predicate.

______________________________________________________________________

## Scenario 2 — Users Without Orders

You need:

> All users, including users who have never placed an order.

**Question:** Which join would you consider?

**Answer:**

A `LEFT JOIN` from users to orders.

Users without orders will have `NULL` order columns.

______________________________________________________________________

## Scenario 3 — Duplicate Users After Join

A query returns the same user multiple times.

**Question:** What would you investigate before adding `DISTINCT`?

**Answer:**

Check the relationship cardinality and join condition.

If the user has multiple matching orders, duplicates may be expected at the joined-row level.

The query should match the actual business question.

______________________________________________________________________

## Scenario 4 — Slow Email Lookup

You frequently execute:

```sql
SELECT *
FROM users
WHERE email = ?;
```

The table contains millions of rows.

**Question:** What would you investigate?

**Answer:**

Consider whether a suitable index exists on `email`, whether uniqueness is required, and inspect the query plan with
`EXPLAIN`.

______________________________________________________________________

## Scenario 5 — Composite Query

Frequent query:

```sql
SELECT *
FROM orders
WHERE user_id = ?
  AND status = ?
ORDER BY created_at DESC;
```

**Question:** What would you consider?

**Answer:**

Analyze the workload and query plan.

A composite index may help, but its column order should be chosen based on the actual filtering and ordering patterns.

Do not blindly create an index without measurement.

______________________________________________________________________

## Scenario 6 — Normalization

A company stores:

```text
order_id
customer_id
customer_name
customer_email
product_id
product_name
```

in every order row.

**Question:** What concerns exist?

**Answer:**

There is likely significant duplication.

Customer/product attributes may belong in separate normalized tables, while order-specific data remains in order-related
tables.

Whether historical snapshots should be retained is a separate domain decision.

______________________________________________________________________

## Scenario 7 — Denormalization

A reporting endpoint joins six large tables and is too slow.

**Question:** Would you immediately denormalize?

**Answer:**

No.

First measure the query, inspect the execution plan, verify indexes and identify the bottleneck.

If the workload genuinely benefits from precomputed/duplicated data, deliberate denormalization can be considered.

______________________________________________________________________

## Scenario 8 — N+1

An API loads 100 users and then executes one order query for each user.

**Question:** What is the problem?

**Answer:**

The API performs approximately 101 queries.

Use a join, batch query, eager loading or another appropriate strategy.

______________________________________________________________________

## Scenario 9 — NULL Bug

A developer writes:

```sql
SELECT *
FROM users
WHERE deleted_at = NULL;
```

and gets zero rows.

**Question:** Why?

**Answer:**

`NULL` cannot be compared using `=`.

Use:

```sql
WHERE deleted_at IS NULL;
```

______________________________________________________________________

## Scenario 10 — Transaction Boundary

An order service does:

```text
Create order
Update inventory
Call payment API
Commit transaction
```

The payment API takes 10 seconds.

**Question:** What should you investigate?

**Answer:**

Holding a database transaction open across a slow external network call can increase lock duration and resource
contention.

Consider whether payment processing and database state should be coordinated using an appropriate workflow/idempotency
strategy rather than holding a transaction open during the external call.

______________________________________________________________________

# 84. Practice Exercises

## Exercise 1 — CRUD

Create a `users` table and write:

```text
INSERT
SELECT
UPDATE
DELETE
```

queries.

Include appropriate constraints.

______________________________________________________________________

## Exercise 2 — Joins

Create:

```text
users
orders
```

and write queries for:

1. Users with orders.
1. All users including those without orders.
1. Users with more than five orders.
1. Users who have never placed an order.

______________________________________________________________________

## Exercise 3 — Aggregation

Given:

```text
orders
--------
id
user_id
amount
status
```

write queries to find:

- Total orders.
- Total revenue.
- Revenue by user.
- Revenue by status.
- Users with revenue above a threshold.

______________________________________________________________________

## Exercise 4 — CTE

Write a CTE that finds users whose total order value is above a chosen threshold.

Then write the equivalent query without a CTE.

Compare readability.

______________________________________________________________________

## Exercise 5 — NULL

Create records containing `NULL` values.

Test:

```sql
=
IS NULL
IS NOT NULL
COALESCE
COUNT(*)
COUNT(column)
```

Explain the results.

______________________________________________________________________

## Exercise 6 — Index Analysis

Create a large table and test:

```sql
WHERE email = ?
```

with and without an index.

Use `EXPLAIN` to inspect the plans.

______________________________________________________________________

## Exercise 7 — Composite Index

Test:

```sql
WHERE user_id = ?
  AND status = ?
ORDER BY created_at DESC
```

with different composite indexes.

Use `EXPLAIN` to understand which index is useful.

______________________________________________________________________

## Exercise 8 — Normalization

Design a normalized schema for:

```text
Customers
Orders
Products
Order Items
```

Identify:

- Primary keys
- Foreign keys
- Unique constraints
- One-to-many relationships

______________________________________________________________________

## Exercise 9 — SQL Injection

Demonstrate why string-concatenated SQL is unsafe using a controlled local example.

Then rewrite it using parameterized queries.

______________________________________________________________________

## Exercise 10 — N+1

Implement an API that loads users and their orders.

First intentionally create an N+1 implementation.

Then replace it with a batch/join approach.

Measure the number of queries.

______________________________________________________________________

# 85. Quick Revision

| Concept | Key Point |
|---|---|
| Relational DB | Data organized into related tables |
| SQL | Language for relational data |
| `SELECT` | Query data |
| `INSERT` | Add rows |
| `UPDATE` | Modify rows |
| `DELETE` | Remove rows |
| `WHERE` | Filter rows |
| `GROUP BY` | Group rows for aggregation |
| `HAVING` | Filter groups |
| `ORDER BY` | Sort results |
| `DISTINCT` | Remove duplicate result rows |
| `INNER JOIN` | Matching rows |
| `LEFT JOIN` | All left rows + matches |
| `RIGHT JOIN` | All right rows + matches |
| `FULL OUTER JOIN` | All rows from both sides |
| `CROSS JOIN` | Cartesian product |
| `SELF JOIN` | Table joined to itself |
| Subquery | Query inside another query |
| `EXISTS` | Checks whether matching row exists |
| CTE | Named query expression using `WITH` |
| `CASE` | Conditional expression |
| `UNION` | Combines and removes duplicates |
| `UNION ALL` | Combines without duplicate removal |
| `NULL` | Unknown/missing value |
| `COALESCE` | First non-null value |
| Primary key | Unique row identity |
| Foreign key | Referential relationship |
| Unique | Prevents duplicate key values |
| `NOT NULL` | Requires a value |
| `CHECK` | Enforces a condition |
| Index | Speeds suitable access patterns |
| Composite index | Index over multiple columns |
| `EXPLAIN` | Shows query plan |
| Transaction | Logical unit of DB work |
| ACID | Atomicity, Consistency, Isolation, Durability |
| Normalization | Reduces redundancy/anomalies |
| 1NF | Atomic values/no repeating groups |
| 2NF | No partial dependency on composite key |
| 3NF | No transitive non-key dependency |
| Denormalization | Deliberate redundancy |
| SQL injection | Untrusted input alters SQL |
| N+1 | One initial query + one per item |
| Keyset pagination | Pagination using stable position/key |

______________________________________________________________________

# 86. Completion Checklist

Before moving to File 19, make sure you can explain:

- [ ] Relational databases
- [ ] Tables, rows and columns
- [ ] SQL categories
- [ ] `SELECT`
- [ ] `WHERE`
- [ ] Comparison operators
- [ ] `AND`, `OR`, `NOT`
- [ ] `IN`
- [ ] `BETWEEN`
- [ ] `LIKE`
- [ ] `ORDER BY`
- [ ] `LIMIT`
- [ ] `INSERT`
- [ ] `UPDATE`
- [ ] `DELETE`
- [ ] Aggregate functions
- [ ] `GROUP BY`
- [ ] `HAVING`
- [ ] Logical SQL execution order
- [ ] `DISTINCT`
- [ ] INNER JOIN
- [ ] LEFT JOIN
- [ ] RIGHT JOIN
- [ ] FULL OUTER JOIN
- [ ] CROSS JOIN
- [ ] SELF JOIN
- [ ] Join cardinality
- [ ] One-to-one
- [ ] One-to-many
- [ ] Many-to-many
- [ ] Subqueries
- [ ] Correlated subqueries
- [ ] `EXISTS`
- [ ] CTEs
- [ ] Multiple CTEs
- [ ] `CASE`
- [ ] `UNION`
- [ ] `UNION ALL`
- [ ] `NULL`
- [ ] Three-valued logic
- [ ] `COALESCE`
- [ ] Primary keys
- [ ] Foreign keys
- [ ] Unique constraints
- [ ] `NOT NULL`
- [ ] `CHECK`
- [ ] `DEFAULT`
- [ ] Indexes
- [ ] Index trade-offs
- [ ] Composite indexes
- [ ] Index selectivity
- [ ] Query performance
- [ ] `EXPLAIN`
- [ ] Sequential vs index scans
- [ ] Transactions
- [ ] `COMMIT`
- [ ] `ROLLBACK`
- [ ] ACID
- [ ] Isolation basics
- [ ] Lock basics
- [ ] Deadlock basics
- [ ] Normalization
- [ ] 1NF
- [ ] 2NF
- [ ] 3NF
- [ ] Denormalization
- [ ] Constraints vs application validation
- [ ] SQL injection
- [ ] N+1 queries
- [ ] Pagination
- [ ] Keyset pagination
- [ ] SQL in Python backends
- [ ] ORM awareness
- [ ] Transaction boundaries
- [ ] SQL interview heuristics

______________________________________________________________________

# 87. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is a relational database?
1. What is SQL?
1. What is the difference between `WHERE` and `HAVING`?
1. Explain `GROUP BY`.
1. What is the logical SQL execution order?
1. What is an INNER JOIN?
1. What is a LEFT JOIN?
1. When would you use a LEFT JOIN instead of an INNER JOIN?
1. What is a CROSS JOIN?
1. What is a SELF JOIN?
1. Why can joins create duplicate rows?
1. Explain one-to-one, one-to-many and many-to-many relationships.
1. What is a subquery?
1. What is a correlated subquery?
1. What is `EXISTS`?
1. What is a CTE?
1. Is a CTE always faster?
1. What is `CASE`?
1. `UNION` vs `UNION ALL`?
1. What is `NULL`?
1. Why is `column = NULL` incorrect?
1. What is three-valued logic?
1. What does `COALESCE` do?
1. What is a primary key?
1. What is a foreign key?
1. What is a unique constraint?
1. What is a check constraint?
1. What is an index?
1. Why shouldn't you index every column?
1. What is a composite index?
1. Why does composite-index column order matter?
1. What is index selectivity?
1. What does `EXPLAIN` tell you?
1. Is a sequential scan always bad?
1. What is a transaction?
1. Explain ACID.
1. What is atomicity?
1. What is consistency?
1. What is isolation?
1. What is durability?
1. What is normalization?
1. Explain 1NF.
1. Explain 2NF.
1. Explain 3NF.
1. Why normalize a database?
1. What is denormalization?
1. When would you deliberately denormalize?
1. What is SQL injection?
1. Does an ORM completely eliminate SQL injection risk?
1. What is the N+1 query problem?
1. How would you solve N+1 queries?
1. What is keyset pagination?
1. Why can large offsets become expensive?
1. Why shouldn't transactions remain open during slow external API calls?
1. How would you investigate a slow SQL query?
1. How would you decide whether an index is needed?
1. Why can `SELECT *` be problematic?
1. Why should database constraints complement application validation?
1. A query suddenly returns duplicate users after adding a join. How do you debug it?
1. An API endpoint is slow because it performs hundreds of database queries. How do you investigate and fix it?

If you can answer these confidently and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [17. Flask](./17-flask.md)

**Next:** [19. SQL Advanced & Transactions](./19-sql-advanced-transactions.md)

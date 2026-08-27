# 21. SQL Indexes & Query Performance

**Previous:** [19. Database Design & Normalization](./19-database-normalization.md)

**Next:** [22. SQL Transactions](./22-sql-transactions.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain why database indexes exist.
- Understand the basic idea behind B-tree indexes.
- Design and reason about composite indexes.
- Explain index column ordering.
- Understand selectivity.
- Explain covering indexes.
- Read basic query plans.
- Use `EXPLAIN` to investigate queries.
- Diagnose common causes of slow SQL queries.
- Explain index trade-offs.
- Understand why offset pagination becomes expensive.
- Explain cursor/keyset pagination at a practical level.
- Make evidence-based indexing decisions instead of blindly adding indexes.

> **Scope note:** This topic focuses on indexes and SQL query performance. Transaction semantics are covered separately in File 22.

______________________________________________________________________

# 1. Why Do We Need Indexes?

Without an appropriate index, a database may need to inspect a large number of rows to find matching data.

For example:

```sql
SELECT *
FROM users
WHERE email = 'alice@example.com';
```

If `email` is not indexed, the database may need to scan many rows.

An index can provide a much more efficient access path.

Conceptually:

```text
Without useful index
→ inspect many rows

With useful index
→ locate matching entries
→ fetch required rows
```

______________________________________________________________________

# 2. Index Is an Access Path

An index is an additional data structure that helps the database locate rows efficiently.

It is not a replacement for the table.

Think of it like the index of a book:

```text
Book
  ↓
Find topic in index
  ↓
Get page
  ↓
Read content
```

Similarly:

```text
Table
  ↓
Use index
  ↓
Locate matching row identifiers
  ↓
Fetch rows
```

______________________________________________________________________

# 3. Indexes Are Not Free

Every index has a cost.

Indexes generally require:

- Additional storage
- Additional write work
- Maintenance during `INSERT`
- Maintenance during `UPDATE`
- Maintenance during `DELETE`

Therefore:

> More indexes do not automatically mean better performance.

______________________________________________________________________

# 4. B-Tree Overview

B-tree-style indexes are commonly used by relational databases.

At a high level, a B-tree keeps indexed values organized so the database can efficiently navigate toward a desired
range.

For example:

```text
1
10
20
30
40
50
60
70
80
```

A lookup does not need to inspect every value sequentially.

The tree structure helps narrow the search.

______________________________________________________________________

# 5. Why B-Trees Are Useful

B-tree indexes are particularly useful for:

- Equality lookups
- Range queries
- Sorting in compatible cases
- Prefix-based composite-index access patterns

Examples:

```sql
WHERE id = 100
```

```sql
WHERE price > 100
```

```sql
WHERE created_at BETWEEN ... AND ...
```

```sql
ORDER BY created_at
```

Whether an index is actually chosen depends on the database optimizer and query.

______________________________________________________________________

# 6. Index Lookup vs Full Table Scan

Suppose:

```sql
SELECT *
FROM users
WHERE email = 'alice@example.com';
```

Without a useful index:

```text
Table
 ↓
Row 1
Row 2
Row 3
...
Row N
```

The database may scan many rows.

With a suitable index:

```text
Email Index
     ↓
alice@example.com
     ↓
row location
     ↓
table row
```

The exact implementation depends on the database engine.

______________________________________________________________________

# 7. Selectivity

Selectivity describes how effectively a column distinguishes rows.

Consider:

```text
user_id
gender
country
```

A unique `user_id` generally has high selectivity.

A column with only a few possible values may have lower selectivity.

For example:

```text
status = active/inactive
```

may not narrow the result set very much.

______________________________________________________________________

# 8. High vs Low Selectivity

Imagine one million rows.

### High selectivity

```text
email
```

may match one row.

### Low selectivity

```text
is_active
```

may match 800,000 rows.

An index on a low-selectivity column is not automatically useless, but the optimizer may decide a scan is cheaper for a
particular query.

______________________________________________________________________

# 9. Selectivity Is Query-Dependent

Do not reduce index design to:

> "Always index high-cardinality columns."

The usefulness of an index depends on:

- Query predicates
- Data distribution
- Table size
- Result size
- Ordering requirements
- Other indexes
- Statistics
- Database optimizer

A low-cardinality column can still be useful as part of a composite index.

______________________________________________________________________

# 10. Basic Index Creation

Example:

```sql
CREATE INDEX idx_users_email
ON users(email);
```

This creates an index on `email`.

If `email` must be unique, a unique constraint/index may be more appropriate:

```sql
CREATE UNIQUE INDEX idx_users_email
ON users(email);
```

The exact schema should reflect the business rule.

______________________________________________________________________

# 11. Index the Access Pattern

Do not ask only:

> "Which columns should I index?"

Ask:

> "Which queries does the application execute frequently, and how can the database access them efficiently?"

For example:

```sql
SELECT *
FROM orders
WHERE customer_id = 10
ORDER BY created_at DESC;
```

A useful composite index may be more valuable than separate indexes chosen independently.

______________________________________________________________________

# 12. Composite Index

A composite index contains multiple columns.

Example:

```sql
CREATE INDEX idx_orders_customer_created
ON orders(customer_id, created_at);
```

This can help queries that filter by customer and then use creation time.

______________________________________________________________________

# 13. Composite Index Ordering

Column order matters.

These are different:

```text
(customer_id, created_at)
```

and:

```text
(created_at, customer_id)
```

They are not interchangeable.

The useful ordering depends on the query patterns.

______________________________________________________________________

# 14. Leftmost Prefix Principle

For a composite index such as:

```text
(customer_id, created_at, status)
```

the leading portion of the index is important.

Conceptually, it can efficiently support access patterns beginning with:

```text
customer_id
```

and:

```text
customer_id + created_at
```

The exact optimizer behavior depends on the database engine.

Do not assume the index is equally useful for every subset of its columns.

______________________________________________________________________

# 15. Example Composite Index

Query:

```sql
SELECT *
FROM orders
WHERE customer_id = 42
ORDER BY created_at DESC;
```

Potential index:

```sql
CREATE INDEX idx_orders_customer_created
ON orders(customer_id, created_at);
```

The first column narrows the customer.

The second supports the ordering/access pattern.

______________________________________________________________________

# 16. Equality Before Range — Practical Heuristic

A common index-design heuristic is:

```text
Equality predicates
      ↓
Range predicates
      ↓
Ordering / additional filtering
```

For example:

```sql
WHERE customer_id = ?
  AND created_at > ?
ORDER BY created_at
```

may favor:

```text
(customer_id, created_at)
```

But this is a heuristic, not a universal law.

Always validate with the database's query plan.

______________________________________________________________________

# 17. Composite Index Example

Suppose:

```sql
SELECT *
FROM orders
WHERE customer_id = ?
  AND status = ?
ORDER BY created_at DESC;
```

A candidate index might be:

```text
(customer_id, status, created_at)
```

But the optimal design depends on:

- Data distribution
- Query frequency
- Other queries
- Write volume
- Database engine
- Actual execution plan

______________________________________________________________________

# 18. Separate Indexes vs Composite Index

You might consider:

```text
INDEX(customer_id)
INDEX(status)
```

versus:

```text
INDEX(customer_id, status, created_at)
```

They serve different access patterns.

A composite index can sometimes support a specific multi-column query better than independent indexes.

But a composite index also increases storage and write-maintenance cost.

______________________________________________________________________

# 19. Covering Index

A covering index contains all columns needed by a query.

Example query:

```sql
SELECT customer_id, created_at
FROM orders
WHERE customer_id = 42;
```

An index containing the required columns may allow the database to satisfy the query largely or entirely from the index
structure, depending on the database engine.

This can reduce table access.

______________________________________________________________________

# 20. Why Covering Indexes Help

If the index contains all required data:

```text
Query
 ↓
Index
 ↓
Required values
```

rather than:

```text
Query
 ↓
Index
 ↓
Locate row
 ↓
Table
 ↓
Required values
```

This can reduce I/O.

However, covering indexes can become large and expensive to maintain.

______________________________________________________________________

# 21. Index-Only Scan — Overview

Some database engines can execute a query using only an index when the required data is available there and
visibility/storage conditions permit it.

This is often called an index-only scan.

The exact behavior varies by database engine.

______________________________________________________________________

# 22. Query Plans

A query plan describes how the database intends to execute a query.

It can reveal:

- Sequential scans
- Index scans
- Join strategies
- Sort operations
- Estimated row counts
- Cost estimates
- Aggregation strategies

Query plans are essential when diagnosing SQL performance.

______________________________________________________________________

# 23. `EXPLAIN`

Use:

```sql
EXPLAIN
SELECT *
FROM users
WHERE email = 'alice@example.com';
```

The database returns information about the planned execution.

Some databases provide a more detailed execution command such as:

```sql
EXPLAIN ANALYZE
```

which can execute the query and report actual execution information.

Be careful with commands that actually execute queries.

______________________________________________________________________

# 24. Estimated vs Actual Plan

An estimated plan tells you what the optimizer expects.

An actual execution plan can show what happened during execution.

This distinction matters.

For example:

```text
Estimated rows: 10
Actual rows: 1,000,000
```

can indicate that optimizer statistics or assumptions are significantly wrong.

______________________________________________________________________

# 25. Sequential Scan

A sequential scan reads rows from the table sequentially.

It is not automatically bad.

For a small table or a query returning a large percentage of rows, scanning the table may be cheaper than using an
index.

Therefore:

> "Sequential scan = bad" is an incorrect rule.

______________________________________________________________________

# 26. Index Scan

An index scan uses an index to locate relevant rows.

Conceptually:

```text
Index
 ↓
matching row locations
 ↓
table rows
```

It is useful when the index significantly reduces the amount of data that must be examined.

______________________________________________________________________

# 27. Bitmap/Hybrid Strategies — Overview

Some database engines can use bitmap or hybrid access strategies to combine filtering information from indexes or
efficiently retrieve many matching rows.

You do not need engine-specific implementation details for most backend interviews.

The important point is:

> The optimizer can choose different access strategies depending on estimated cost.

______________________________________________________________________

# 28. Query Optimizer

The optimizer chooses an execution plan based on information such as:

- Query structure
- Available indexes
- Table statistics
- Data distribution
- Estimated cardinality
- Join conditions
- Cost models

The optimizer is not simply following a fixed rule like:

```text
index exists → use index
```

______________________________________________________________________

# 29. Why Isn't My Index Being Used?

Possible reasons include:

- The table is small.
- The query returns many rows.
- The index is not selective enough.
- Another plan is cheaper.
- Statistics are stale.
- The query expression prevents effective index use.
- A composite index has an unsuitable column order.
- The cost of random table access is high.
- The optimizer estimates the query incorrectly.

______________________________________________________________________

# 30. Function on Indexed Column

A query such as:

```sql
WHERE LOWER(email) = 'alice@example.com'
```

may not use a normal index on:

```text
email
```

depending on the database.

Possible solutions include:

- Functional/expression indexes where supported.
- Appropriate normalized data.
- Database-specific indexing features.

Do not blindly assume an ordinary index can satisfy every expression involving that column.

______________________________________________________________________

# 31. Leading Wildcard

A query such as:

```sql
WHERE email LIKE '%@example.com'
```

can be difficult for a conventional B-tree index because the search does not begin with a known prefix.

Compare:

```sql
LIKE 'alice%'
```

with:

```sql
LIKE '%alice'
```

The latter generally cannot use a standard B-tree in the same straightforward prefix-search manner.

Database-specific text-search indexes may be more appropriate for some workloads.

______________________________________________________________________

# 32. Implicit Type Conversion

Queries that compare incompatible types can cause conversions that interfere with efficient index usage depending on the
database.

Example:

```text
indexed integer column
vs
string parameter
```

The exact behavior is database-specific.

Use correct parameter types from the application whenever possible.

______________________________________________________________________

# 33. Statistics

The optimizer relies heavily on statistics.

If statistics do not represent current data distribution accurately, the optimizer may choose a poor plan.

This can lead to situations where:

```text
Expected rows ≠ Actual rows
```

Maintaining database statistics is an important part of query performance.

______________________________________________________________________

# 34. Slow Query Diagnosis

When a query is slow, do not immediately add an index.

Use a process:

```text
Reproduce
   ↓
Measure
   ↓
EXPLAIN / execution plan
   ↓
Find expensive operation
   ↓
Check cardinality/statistics
   ↓
Check indexes
   ↓
Rewrite if necessary
   ↓
Measure again
```

______________________________________________________________________

# 35. Common Causes of Slow Queries

Possible causes include:

- Missing indexes
- Poor composite-index ordering
- Large scans
- Returning too many rows
- Expensive joins
- Incorrect join conditions
- Sort operations
- Aggregations over large datasets
- Functions preventing efficient access
- Stale statistics
- Offset pagination
- Excessive application-side data retrieval

______________________________________________________________________

# 36. Select Only What You Need

Avoid:

```sql
SELECT *
```

when the application only needs a few columns.

Prefer:

```sql
SELECT id, email, name
FROM users
WHERE ...
```

Benefits can include:

- Less data transferred
- Less memory usage
- Potentially better index coverage
- Lower application serialization cost

______________________________________________________________________

# 37. Pagination

A common pagination query is:

```sql
SELECT *
FROM orders
ORDER BY created_at DESC
LIMIT 20 OFFSET 100000;
```

As the offset becomes large, the database may still need to process/skip many earlier rows.

Large offsets can therefore become increasingly expensive.

______________________________________________________________________

# 38. Offset Pagination

Advantages:

- Simple API design
- Easy to request arbitrary pages
- Easy to understand

Disadvantages:

- Large offsets can become expensive.
- Results can shift when rows are inserted/deleted between requests.
- Deep pagination may require substantial work.

______________________________________________________________________

# 39. Keyset/Cursor Pagination

Instead of:

```text
OFFSET 100000
```

use a value from the previous page as a cursor.

For example:

```sql
SELECT *
FROM orders
WHERE created_at < ?
ORDER BY created_at DESC
LIMIT 20;
```

For deterministic ordering, use a unique tie-breaker such as `id`.

______________________________________________________________________

# 40. Keyset Pagination With Tie-Breaker

Suppose ordering is:

```sql
ORDER BY created_at DESC, id DESC
```

Then the next-page condition conceptually becomes:

```sql
WHERE
    created_at < :last_created_at
    OR (
        created_at = :last_created_at
        AND id < :last_id
    )
```

This avoids ambiguity when multiple rows have the same timestamp.

______________________________________________________________________

# 41. Offset vs Keyset

| Property | Offset | Keyset/Cursor |
|---|---|---|
| Simple implementation | Excellent | Moderate |
| Deep pagination | Can become expensive | Usually better |
| Stable under concurrent changes | Weaker | Generally better for ordered traversal |
| Jump to arbitrary page | Easy | Difficult |
| Requires cursor state | No | Yes |
| Good for feeds | Sometimes | Often |
| Good for admin tables | Often | Depends |

______________________________________________________________________

# 42. Index for Pagination

For:

```sql
SELECT *
FROM orders
WHERE customer_id = ?
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

a candidate index might follow the access pattern:

```text
(customer_id, created_at, id)
```

The exact index and ordering depend on the database and query.

______________________________________________________________________

# 43. Index Write Cost

When inserting a row, relevant indexes also need to be updated.

For example:

```text
INSERT
 ↓
Table
 ↓
Index 1
 ↓
Index 2
 ↓
Index 3
```

More indexes can mean more write work.

______________________________________________________________________

# 44. Index Storage Cost

Indexes consume disk and memory/cache resources.

A table with many large indexes may consume significantly more storage than the table alone.

This matters for:

- Large tables
- High-write workloads
- Replication
- Backups
- Memory pressure

______________________________________________________________________

# 45. Index Maintenance

Indexes can require maintenance depending on the database engine and workload.

Possible concerns include:

- Bloat
- Fragmentation
- Statistics
- Rebuilding/reorganizing
- Storage growth

The exact maintenance strategy is database-specific.

______________________________________________________________________

# 46. Too Many Indexes

Suppose a table has:

```text
INDEX(a)
INDEX(b)
INDEX(c)
INDEX(d)
INDEX(a,b)
INDEX(a,c)
INDEX(b,c)
```

Some may be redundant or rarely used.

Review:

- Query workload
- Index usage
- Write cost
- Storage
- Duplicate/overlapping indexes

______________________________________________________________________

# 47. Index Redundancy

An index such as:

```text
(a, b)
```

may already support some access patterns that would otherwise motivate:

```text
(a)
```

depending on the database and query.

Do not automatically keep both.

But do not remove an index solely from column-prefix reasoning without checking actual workload and optimizer behavior.

______________________________________________________________________

# 48. Index Ordering and Sorting

An index can sometimes help avoid an explicit sort when its ordering matches the query.

Example:

```sql
WHERE customer_id = ?
ORDER BY created_at DESC
```

with:

```text
(customer_id, created_at)
```

may allow the database to retrieve matching rows in useful order.

The exact behavior depends on database engine and index definition.

______________________________________________________________________

# 49. Composite Index Design Checklist

For a query:

```sql
SELECT ...
FROM orders
WHERE customer_id = ?
  AND status = ?
ORDER BY created_at DESC;
```

ask:

1. Which predicates are equality conditions?
1. Which are ranges?
1. What ordering is required?
1. Which columns are selective?
1. How frequently is the query executed?
1. Can one composite index support the complete access pattern?
1. Is the index too large?
1. What write overhead does it introduce?
1. What does `EXPLAIN` show?
1. Does the actual workload justify it?

______________________________________________________________________

# 50. Query Performance Is More Than Indexes

A query can be slow even when indexes are present.

Consider:

- Poor SQL structure
- Huge result sets
- Expensive joins
- Bad pagination
- Network transfer
- Serialization
- Lock contention
- Connection-pool limitations
- Application-side processing

Indexes are one component of overall performance.

______________________________________________________________________

# 51. N+1 Query Problem

A common backend performance problem is:

```text
1 query for users
+
N queries for orders
```

For 1,000 users:

```text
1 + 1,000 = 1,001 queries
```

This may be much slower than an appropriate join or batch query.

This is not primarily an indexing problem.

______________________________________________________________________

# 52. Query Performance and ORMs

ORMs can hide SQL complexity.

A Python backend engineer should still inspect the generated SQL.

Watch for:

- N+1 queries
- Unnecessary joins
- Selecting too many columns
- Missing filters
- Large result sets
- Unexpected lazy loading

Understanding SQL remains important even when using an ORM.

______________________________________________________________________

# 53. Query Plan Reading — Practical Approach

When reading a plan, ask:

### 1. What is the first expensive operation?

Look for:

- Large scans
- Large sorts
- Expensive joins
- Large aggregations

### 2. Are estimated and actual rows similar?

Large differences may indicate estimation/statistics problems.

### 3. Is an index being used?

If not, understand why before forcing anything.

### 4. How many rows flow between operations?

Large intermediate results can be expensive.

### 5. Where is the time spent?

Focus optimization on the actual bottleneck.

______________________________________________________________________

# 54. Do Not Force Indexes Blindly

Some database systems provide index hints.

They can be useful in exceptional situations but are generally not the first response.

A better process is:

```text
Understand plan
→ understand data
→ verify statistics
→ test alternatives
→ measure
```

The optimizer may have a valid reason for choosing another access path.

______________________________________________________________________

# 55. Performance Investigation Example

Query:

```sql
SELECT *
FROM orders
WHERE customer_id = 42
ORDER BY created_at DESC
LIMIT 20;
```

The query is slow.

Possible investigation:

1. Check table size.
1. Run `EXPLAIN`.
1. Check whether `customer_id` is indexed.
1. Check whether ordering requires a large sort.
1. Consider `(customer_id, created_at)` index.
1. Check actual row counts.
1. Measure before and after.

______________________________________________________________________

# 56. Performance Investigation Example — Large Pagination

Query:

```sql
SELECT *
FROM orders
ORDER BY created_at DESC
LIMIT 20 OFFSET 500000;
```

Potential issue:

The database may need to process a large number of rows before returning the requested page.

Possible solution:

Use keyset/cursor pagination with an appropriate ordering index.

______________________________________________________________________

# 57. Performance Investigation Example — Low Selectivity

Query:

```sql
SELECT *
FROM users
WHERE is_active = TRUE;
```

Suppose 95% of users are active.

An index on `is_active` may not provide much benefit for this particular query.

The optimizer may choose a scan.

The correct response is not automatically:

> "Force the index."

______________________________________________________________________

# 58. Performance Investigation Example — Covering Index

Query:

```sql
SELECT customer_id, created_at
FROM orders
WHERE customer_id = ?;
```

A suitable index containing the required columns may allow the database to avoid reading the base table for the needed
values, depending on engine behavior.

This can reduce I/O.

______________________________________________________________________

# 59. Production Indexing Strategy

A practical strategy:

### Step 1

Identify important queries.

### Step 2

Measure query latency and frequency.

### Step 3

Inspect execution plans.

### Step 4

Identify missing or ineffective access paths.

### Step 5

Design the smallest useful index.

### Step 6

Test with realistic data.

### Step 7

Measure improvement.

### Step 8

Monitor write overhead and storage.

### Step 9

Remove indexes that no longer justify their cost.

______________________________________________________________________

# 60. Senior-Level Perspective

A strong backend engineer should not say:

> "This column is frequently queried, so add an index."

A stronger answer is:

> "I would identify the actual query pattern, inspect the execution plan, understand selectivity and data distribution, choose an index that supports the access pattern, benchmark it on representative data, and verify the additional write/storage cost."

This demonstrates production thinking.

______________________________________________________________________

# 61. Interview Questions & Answers

## Q1. What is a database index?

**Answer:**

An index is an additional data structure that provides an efficient access path to rows, reducing the amount of data the
database may need to inspect for suitable queries.

______________________________________________________________________

## Q2. Why do we need indexes?

**Answer:**

To make appropriate lookups, filtering, ordering and range operations more efficient by avoiding unnecessary scanning of
large portions of a table.

______________________________________________________________________

## Q3. Are indexes free?

**Answer:**

No.

They consume storage and add maintenance overhead to writes such as inserts, updates and deletes.

______________________________________________________________________

## Q4. What is a B-tree index?

**Answer:**

A tree-based ordered index structure that supports efficient lookup and range-oriented access patterns.

______________________________________________________________________

## Q5. What is selectivity?

**Answer:**

Selectivity describes how effectively a predicate narrows the set of matching rows.

______________________________________________________________________

## Q6. Is a low-cardinality column useless for indexing?

**Answer:**

No.

Its usefulness depends on data distribution, query predicates and workload. It can also be valuable as part of a
composite index.

______________________________________________________________________

## Q7. What is a composite index?

**Answer:**

An index containing multiple columns, such as:

```text
(customer_id, created_at)
```

______________________________________________________________________

## Q8. Why does column order matter in a composite index?

**Answer:**

The database organizes the index according to that order, so different leading columns support different access
patterns.

______________________________________________________________________

## Q9. What is the leftmost-prefix principle?

**Answer:**

A composite B-tree index generally provides its strongest direct access support for predicates involving its leading
columns and their prefixes.

______________________________________________________________________

## Q10. What is a covering index?

**Answer:**

An index that contains all the columns required by a query, potentially allowing the database to satisfy the query
without accessing the base table for every row.

______________________________________________________________________

## Q11. What is `EXPLAIN`?

**Answer:**

A command that shows the database's planned execution strategy for a query.

______________________________________________________________________

## Q12. What is `EXPLAIN ANALYZE`?

**Answer:**

In databases that support it, it executes the query while providing actual execution information, allowing comparison
between estimates and reality.

______________________________________________________________________

## Q13. Is a sequential scan always bad?

**Answer:**

No.

For small tables or queries returning a large portion of the table, a sequential scan may be cheaper than using an
index.

______________________________________________________________________

## Q14. Why might an existing index not be used?

**Answer:**

The optimizer may estimate that another plan is cheaper because of table size, selectivity, result size, statistics,
query structure, index ordering or other factors.

______________________________________________________________________

## Q15. What is index selectivity?

**Answer:**

It is the degree to which an indexed predicate reduces the number of matching rows.

______________________________________________________________________

## Q16. How do you choose a composite index?

**Answer:**

Start with actual query patterns and consider equality predicates, ranges, ordering, selectivity, workload frequency,
index size and write cost. Validate with execution plans and benchmarks.

______________________________________________________________________

## Q17. Should equality columns always come before range columns?

**Answer:**

It is a useful practical heuristic for many B-tree index designs, but not an absolute rule. The actual query workload
and execution plan should determine the final design.

______________________________________________________________________

## Q18. What is the N+1 query problem?

**Answer:**

A pattern where one query retrieves parent records and then one additional query is executed for each parent, causing a
large number of database round trips.

______________________________________________________________________

## Q19. Why can `SELECT *` hurt performance?

**Answer:**

It can retrieve unnecessary data, increase I/O and network transfer, increase application memory/serialization work and
make covering-index opportunities less likely.

______________________________________________________________________

## Q20. Why can offset pagination become slow?

**Answer:**

Large offsets can require the database to process or skip many preceding rows before returning the requested page.

______________________________________________________________________

## Q21. What is keyset pagination?

**Answer:**

Pagination based on the values of the last row from the previous page rather than the number of rows to skip.

______________________________________________________________________

## Q22. Why is a tie-breaker important for cursor pagination?

**Answer:**

If the primary ordering column is not unique, a stable secondary column such as `id` provides deterministic ordering and
prevents ambiguous page boundaries.

______________________________________________________________________

## Q23. Offset vs keyset pagination?

**Answer:**

Offset is simpler and supports arbitrary page jumps but can become expensive for deep pages.

Keyset is usually better for ordered traversal of large datasets but requires cursor state and does not naturally
support arbitrary page-number jumps.

______________________________________________________________________

## Q24. What are the main costs of indexes?

**Answer:**

Storage, write overhead, cache/memory usage and maintenance complexity.

______________________________________________________________________

## Q25. Can too many indexes hurt a database?

**Answer:**

Yes.

They consume storage and increase the cost of writes and maintenance. Some may also be redundant.

______________________________________________________________________

## Q26. How would you diagnose a slow query?

**Answer:**

Measure it, inspect the execution plan, identify the expensive operation, verify row estimates and statistics, check
indexes and query structure, make one targeted change, and measure again.

______________________________________________________________________

## Q27. What is an index-only scan?

**Answer:**

A plan where the database can satisfy a query from index data without needing to fetch the corresponding table rows,
when the engine's conditions allow it.

______________________________________________________________________

## Q28. Why might `LIKE '%abc'` not use a normal B-tree efficiently?

**Answer:**

Because the search starts with an unknown prefix, so the ordered index cannot generally narrow the search using a
straightforward prefix lookup.

______________________________________________________________________

## Q29. Why can applying a function to an indexed column affect index usage?

**Answer:**

The expression may no longer match the ordinary index's stored ordering. Some databases support functional/expression
indexes to address this.

______________________________________________________________________

## Q30. What is the role of database statistics?

**Answer:**

Statistics help the optimizer estimate cardinalities and costs so it can choose an execution plan.

______________________________________________________________________

## Q31. What does an estimated-vs-actual row mismatch tell you?

**Answer:**

A significant mismatch can indicate inaccurate statistics, skewed data, or optimizer estimation limitations, potentially
causing a poor plan.

______________________________________________________________________

## Q32. Should you always force an index?

**Answer:**

No.

First understand why the optimizer chose its plan and validate alternatives through measurement.

______________________________________________________________________

## Q33. Can two separate indexes replace one composite index?

**Answer:**

Not necessarily.

They support different access patterns. The optimizer may sometimes combine indexes, but a well-designed composite index
can be more appropriate for a particular multi-column query.

______________________________________________________________________

## Q34. Does every indexed column need to be highly selective?

**Answer:**

No.

Selectivity is important, but query shape, ordering, composite indexes and workload also matter.

______________________________________________________________________

## Q35. Why does index column order matter for sorting?

**Answer:**

If the index ordering aligns with the query's filtering and requested ordering, the database may be able to avoid or
reduce an explicit sort.

______________________________________________________________________

## Q36. What is a covering index trade-off?

**Answer:**

It can reduce table access and improve reads, but making indexes cover more columns increases index size and
write/maintenance cost.

______________________________________________________________________

## Q37. What is the difference between an index and a constraint?

**Answer:**

An index primarily provides an access structure.

A constraint expresses a data-integrity rule such as uniqueness or referential integrity. Some constraints may be
implemented using indexes, depending on the database.

______________________________________________________________________

## Q38. How do ORMs affect SQL performance?

**Answer:**

They can hide generated SQL and accidentally create N+1 queries, excessive joins or oversized result sets. Backend
engineers should inspect generated SQL for important workloads.

______________________________________________________________________

## Q39. Does adding an index always improve a query?

**Answer:**

No.

The optimizer may not use it, and the index can increase write and storage costs.

______________________________________________________________________

## Q40. What is the senior-level approach to indexing?

**Answer:**

Start from measured query patterns, inspect execution plans, understand data distribution and selectivity, design
targeted indexes, benchmark on realistic data, and monitor both read improvements and write/storage costs.

______________________________________________________________________

# 62. Scenario-Based Questions

## Scenario 1 — Slow Email Lookup

You have:

```sql
SELECT *
FROM users
WHERE email = ?;
```

The table contains 20 million users.

**Question:** What would you investigate?

**Answer:**

Check whether `email` has an appropriate unique index, inspect the execution plan, verify statistics and measure the
query under realistic data.

______________________________________________________________________

## Scenario 2 — Index Not Used

You created:

```text
INDEX(status)
```

but:

```sql
SELECT *
FROM orders
WHERE status = 'completed';
```

still performs a sequential scan.

**Question:** Is the database necessarily wrong?

**Answer:**

No.

If most orders are completed, the predicate may have low selectivity and scanning the table may be cheaper.

______________________________________________________________________

## Scenario 3 — Composite Index

Query:

```sql
SELECT *
FROM orders
WHERE customer_id = ?
ORDER BY created_at DESC
LIMIT 20;
```

**Question:** What index would you consider?

**Answer:**

A candidate is:

```text
(customer_id, created_at)
```

Then verify with `EXPLAIN` and representative data.

______________________________________________________________________

## Scenario 4 — Top Query Is Slow

A frequently executed query:

```sql
SELECT *
FROM orders
WHERE customer_id = ?
  AND status = ?
ORDER BY created_at DESC
LIMIT 50;
```

**Question:** What would you investigate?

**Answer:**

Consider a composite index matching the filtering and ordering pattern, such as:

```text
(customer_id, status, created_at)
```

but validate it using the actual data distribution and execution plan.

______________________________________________________________________

## Scenario 5 — Deep Pagination

API request:

```text
?page=10000
&page_size=50
```

causes increasing latency.

**Question:** What would you consider?

**Answer:**

Evaluate keyset/cursor pagination with a stable ordering and suitable index rather than relying on very large offsets.

______________________________________________________________________

## Scenario 6 — Duplicate Timestamp

Cursor pagination uses:

```sql
ORDER BY created_at DESC
```

but many rows have identical timestamps.

**Question:** What should you do?

**Answer:**

Add a deterministic unique tie-breaker, such as:

```sql
ORDER BY created_at DESC, id DESC
```

and use both values for the cursor boundary.

______________________________________________________________________

## Scenario 7 — Covering Index

Query:

```sql
SELECT customer_id, created_at
FROM orders
WHERE customer_id = ?;
```

**Question:** Could a covering index help?

**Answer:**

Yes. An index containing the required columns may allow the database to satisfy the query largely or entirely from the
index, depending on the database engine.

______________________________________________________________________

## Scenario 8 — Many Indexes

A high-write table has 15 indexes.

**Question:** What would you review?

**Answer:**

Review index usage, overlapping/redundant indexes, storage consumption, write latency and whether each index supports an
important workload.

______________________________________________________________________

## Scenario 9 — ORM Performance

An API loads 500 users and then executes one query per user to retrieve orders.

**Question:** What problem do you suspect?

**Answer:**

An N+1 query problem.

Investigate batching, joins, eager loading or other query strategies appropriate to the ORM and access pattern.

______________________________________________________________________

## Scenario 10 — Slow Query After Data Growth

A query was fast with 100,000 rows but became slow after growing to 100 million rows.

**Question:** What would you do?

**Answer:**

Re-measure, inspect the current execution plan, check statistics and data distribution, verify index effectiveness,
examine row estimates and identify whether the workload now requires a different access strategy or pagination approach.

______________________________________________________________________

# 63. Practice Exercises

## Exercise 1 — Basic Index

Create a table with one million users.

Compare:

```sql
SELECT *
FROM users
WHERE email = ?;
```

with and without an email index.

Use `EXPLAIN`.

______________________________________________________________________

## Exercise 2 — Selectivity

Create a table with:

```text
id
status
email
```

where:

- `status` has two values.
- `email` is mostly unique.

Compare the query plans for both columns.

Explain why the optimizer may treat them differently.

______________________________________________________________________

## Exercise 3 — Composite Index

Given:

```sql
SELECT *
FROM orders
WHERE customer_id = ?
ORDER BY created_at DESC
LIMIT 20;
```

test:

```text
INDEX(customer_id)
INDEX(created_at)
INDEX(customer_id, created_at)
```

Compare plans and performance.

______________________________________________________________________

## Exercise 4 — Column Ordering

Compare:

```text
INDEX(customer_id, created_at)
```

with:

```text
INDEX(created_at, customer_id)
```

for several different query patterns.

Explain which queries each supports effectively.

______________________________________________________________________

## Exercise 5 — Covering Index

Create a query that selects only columns contained in an index.

Compare its execution plan with a query that requires additional table columns.

______________________________________________________________________

## Exercise 6 — Top N Pagination

Measure:

```sql
LIMIT 20 OFFSET 100;
```

versus:

```sql
LIMIT 20 OFFSET 500000;
```

Observe how performance changes as the offset grows.

______________________________________________________________________

## Exercise 7 — Keyset Pagination

Implement:

```sql
ORDER BY created_at DESC, id DESC
```

and retrieve the next page using:

```text
last_created_at
last_id
```

Compare it with offset pagination.

______________________________________________________________________

## Exercise 8 — Slow Query Investigation

Take one slow query from a real or sample application.

Document:

1. Query.
1. Baseline latency.
1. Execution plan.
1. Suspected bottleneck.
1. Proposed change.
1. New plan.
1. New latency.
1. Write/storage trade-off.

______________________________________________________________________

## Exercise 9 — Index Cleanup

Create several overlapping indexes.

Use your database's index-usage information to determine which are actually useful.

______________________________________________________________________

## Exercise 10 — ORM Investigation

Use a Python ORM to load a parent collection and related records.

Inspect generated SQL and determine whether an N+1 query occurs.

Then rewrite the access pattern to reduce unnecessary round trips.

______________________________________________________________________

# 64. Quick Revision

| Concept | Key Point |
|---|---|
| Index | Additional access structure |
| Purpose | Efficient data access |
| B-tree | Ordered tree-based index structure |
| Selectivity | How strongly a predicate narrows rows |
| Composite index | Index over multiple columns |
| Column order | Determines useful access patterns |
| Leftmost prefix | Leading composite-index columns matter |
| Covering index | Index contains required query data |
| Index-only scan | Query can potentially be satisfied from index |
| Query plan | Execution strategy |
| `EXPLAIN` | Shows planned execution |
| `EXPLAIN ANALYZE` | Provides actual execution information where supported |
| Sequential scan | Reads table sequentially |
| Index scan | Uses an index to find rows |
| Optimizer | Chooses execution strategy |
| Statistics | Help estimate cardinality/cost |
| Selectivity | Important but workload-dependent |
| N+1 | One parent query + many child queries |
| Offset pagination | Simple but deep offsets can be expensive |
| Keyset pagination | Cursor/value-based pagination |
| Tie-breaker | Makes ordering deterministic |
| Index cost | Storage + write/maintenance overhead |
| Over-indexing | Too many unnecessary indexes |
| Covering trade-off | Faster reads vs larger index |
| Slow-query diagnosis | Measure → plan → identify bottleneck → change → measure |

______________________________________________________________________

# 65. Completion Checklist

Before moving to File 22, make sure you can explain:

- [ ] Why indexes exist
- [ ] Index access paths
- [ ] B-tree overview
- [ ] Index vs table scan
- [ ] Selectivity
- [ ] Cardinality
- [ ] Basic index creation
- [ ] Composite indexes
- [ ] Composite-index column ordering
- [ ] Leftmost-prefix principle
- [ ] Equality vs range predicates
- [ ] Covering indexes
- [ ] Index-only scans overview
- [ ] Query plans
- [ ] `EXPLAIN`
- [ ] `EXPLAIN ANALYZE` overview
- [ ] Sequential scans
- [ ] Index scans
- [ ] Query optimizer
- [ ] Statistics
- [ ] Estimated vs actual rows
- [ ] Why an index may not be used
- [ ] Functions on indexed columns
- [ ] Prefix vs leading-wildcard searches
- [ ] Type-conversion considerations
- [ ] Slow-query diagnosis
- [ ] `SELECT *` considerations
- [ ] Offset pagination
- [ ] Keyset/cursor pagination
- [ ] Cursor tie-breakers
- [ ] Index write cost
- [ ] Index storage cost
- [ ] Index maintenance
- [ ] Redundant indexes
- [ ] N+1 queries
- [ ] ORM-generated SQL
- [ ] Production indexing strategy
- [ ] Index trade-offs
- [ ] Senior-level performance reasoning

______________________________________________________________________

# 66. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is a database index?
1. Why do we need indexes?
1. What are the costs of indexes?
1. What is a B-tree?
1. Why are B-trees useful for range queries?
1. What is selectivity?
1. What is cardinality?
1. Is a low-cardinality column always useless to index?
1. What is a composite index?
1. Why does composite-index column order matter?
1. Explain the leftmost-prefix principle.
1. What index would you consider for `WHERE customer_id = ? ORDER BY created_at DESC`?
1. What is the equality-before-range heuristic?
1. Is equality-before-range an absolute rule?
1. What is a covering index?
1. What is an index-only scan?
1. What is a query execution plan?
1. What does `EXPLAIN` tell you?
1. What is the difference between estimated and actual execution information?
1. Is a sequential scan always bad?
1. Why might an optimizer ignore an index?
1. How do statistics affect query planning?
1. How can a function on an indexed column affect index usage?
1. Why can a leading wildcard make B-tree lookup difficult?
1. How would you diagnose a slow query?
1. Why can `SELECT *` be inefficient?
1. What is the N+1 query problem?
1. Why can ORM-generated SQL cause performance issues?
1. Why can offset pagination become slow?
1. What is keyset pagination?
1. What is cursor pagination?
1. Why is a tie-breaker needed in cursor pagination?
1. What index would you consider for cursor pagination by `created_at, id`?
1. What are the write costs of an index?
1. What are the storage costs of an index?
1. Can too many indexes hurt a database?
1. How do you identify redundant indexes?
1. Can two single-column indexes replace a composite index?
1. How do indexes interact with sorting?
1. What is the role of selectivity in composite indexes?
1. What would you inspect if estimated rows differ greatly from actual rows?
1. Would you force an index if the optimizer chooses a sequential scan?
1. How would you optimize a query returning 90% of a table?
1. How would you optimize a query returning 10 rows from a 100-million-row table?
1. How would you investigate a query that became slow after major data growth?
1. How would you choose indexes for a high-write table?
1. How do covering indexes trade read performance against write/storage cost?
1. What is the difference between query correctness and query performance?
1. Walk through your process for diagnosing a production slow query.
1. Give a senior-level answer to: "Just add an index to fix the slow query."

If you can answer these confidently and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [19. Database Design & Normalization](./19-database-normalization.md)

**Next:** [22. SQL Transactions](./22-sql-transactions.md)

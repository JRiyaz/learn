# 20. Advanced SQL Queries

**Previous:** [19. Database Design & Normalization](./19-database-normalization.md)

**Next:** [21. SQL Indexes & Query Performance](./21-sql-indexes-performance.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Write and explain subqueries.
- Understand correlated subqueries.
- Use `EXISTS` and `IN` appropriately.
- Build readable queries with CTEs.
- Explain and use window functions.
- Use `ROW_NUMBER`, `RANK` and `DENSE_RANK`.
- Use `LAG` and `LEAD`.
- Understand set operations.
- Solve common SQL interview query patterns.
- Recognize duplicate, `NULL`, ordering and tie-handling issues in advanced queries.
- Translate common backend/data problems into SQL.

> **Scope note:** File 18 introduced subqueries and CTEs at a fundamental level. File 19 focused specifically on database design and normalization. This file focuses on **advanced query construction**, especially window functions and interview-style SQL problems. Indexes and query performance are covered separately in File 21.

______________________________________________________________________

# 1. Why Advanced SQL Matters

A backend engineer with 5+ years of experience is often expected to do more than simple CRUD.

You may need to answer questions such as:

- Find the second-highest salary.
- Find the latest order for every customer.
- Find the top three products per category.
- Compare each row with the previous row.
- Find users who have never placed an order.
- Calculate running totals.
- Remove duplicates while keeping the newest record.

These problems often require:

- Subqueries
- CTEs
- Window functions
- Set operations
- Careful filtering and ordering

______________________________________________________________________

# 2. Subqueries

A subquery is a query nested inside another SQL statement.

Example:

```sql
SELECT *
FROM users
WHERE id IN (
    SELECT user_id
    FROM orders
);
```

The inner query produces values used by the outer query.

______________________________________________________________________

# 3. Scalar Subquery

A scalar subquery returns a single value.

Example:

```sql
SELECT
    name,
    (SELECT COUNT(*)
     FROM orders o
     WHERE o.user_id = u.id) AS order_count
FROM users u;
```

The inner query produces one value for each outer row.

Be careful: if a scalar subquery returns multiple rows where only one is expected, the database may raise an error.

______________________________________________________________________

# 4. Subquery in `FROM`

A subquery can act as a derived table.

```sql
SELECT *
FROM (
    SELECT user_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY user_id
) x
WHERE order_count > 5;
```

The outer query operates on the result of the inner query.

A CTE can often make the same logic easier to read.

______________________________________________________________________

# 5. Subquery in `WHERE`

Example:

```sql
SELECT *
FROM products
WHERE price > (
    SELECT AVG(price)
    FROM products
);
```

This finds products whose price is above the average.

______________________________________________________________________

# 6. `IN`

`IN` checks whether a value belongs to a set.

```sql
SELECT *
FROM users
WHERE id IN (
    SELECT user_id
    FROM orders
);
```

This can be useful when the inner query naturally produces a set of identifiers.

______________________________________________________________________

# 7. `NOT IN` and `NULL`

Be careful with:

```sql
NOT IN
```

when the subquery can contain `NULL`.

SQL's three-valued logic can produce surprising results.

For existence-style questions, `NOT EXISTS` is often easier to reason about.

______________________________________________________________________

# 8. `EXISTS`

`EXISTS` checks whether the subquery returns at least one row.

```sql
SELECT *
FROM users u
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = u.id
);
```

The selected value inside `EXISTS` is not important.

The existence of a matching row is what matters.

______________________________________________________________________

# 9. `NOT EXISTS`

Find users with no orders:

```sql
SELECT *
FROM users u
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = u.id
);
```

This is a common interview pattern.

______________________________________________________________________

# 10. `EXISTS` vs `IN`

Both can express membership/existence conditions.

For example:

```sql
WHERE id IN (
    SELECT user_id
    FROM orders
)
```

and:

```sql
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = users.id
)
```

can represent similar logic.

The better choice depends on:

- Query semantics
- `NULL` behavior
- Database optimizer
- Readability
- Data shape

Do not claim that one is universally faster.

______________________________________________________________________

# 11. Correlated Subquery

A correlated subquery references a column from the outer query.

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

The inner query refers to:

```text
u.id
```

from the outer query.

______________________________________________________________________

# 12. Correlated Subquery vs Non-Correlated

### Non-correlated

The inner query can be evaluated independently.

```sql
SELECT AVG(price)
FROM products;
```

### Correlated

The inner query depends on the current outer row.

```sql
SELECT *
FROM products p
WHERE price > (
    SELECT AVG(p2.price)
    FROM products p2
    WHERE p2.category_id = p.category_id
);
```

______________________________________________________________________

# 13. Correlated Subquery Example

Find employees earning more than the average salary in their department:

```sql
SELECT e.*
FROM employees e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department_id = e.department_id
);
```

This is a classic advanced SQL pattern.

A window-function solution can often express the same logic more directly.

______________________________________________________________________

# 14. CTE

A Common Table Expression is defined using `WITH`.

```sql
WITH active_users AS (
    SELECT *
    FROM users
    WHERE active = TRUE
)
SELECT *
FROM active_users;
```

CTEs can make complex queries easier to structure.

______________________________________________________________________

# 15. Multiple CTEs

You can define multiple CTEs:

```sql
WITH active_users AS (
    ...
),
recent_orders AS (
    ...
),
high_value_users AS (
    ...
)
SELECT ...
FROM active_users
JOIN recent_orders
    ON ...
JOIN high_value_users
    ON ...;
```

This can turn a complicated query into logical stages.

______________________________________________________________________

# 16. CTE vs Subquery

Both can express similar logic.

Subquery:

```sql
SELECT *
FROM (
    SELECT ...
) x;
```

CTE:

```sql
WITH x AS (
    SELECT ...
)
SELECT *
FROM x;
```

CTEs are often easier to read when the query contains multiple logical stages or when a named intermediate result
improves clarity.

______________________________________________________________________

# 17. Recursive CTE — Overview

A recursive CTE can reference itself.

Conceptually:

```sql
WITH RECURSIVE hierarchy AS (
    -- anchor
    SELECT ...

    UNION ALL

    -- recursive step
    SELECT ...
    FROM hierarchy
    ...
)
SELECT *
FROM hierarchy;
```

Common uses include:

- Organizational hierarchies
- Tree structures
- Graph-like traversal
- Parent/child relationships

Recursive CTEs are an advanced feature; know the concept for interviews unless the role requires deeper SQL
specialization.

______________________________________________________________________

# 18. Window Functions

A window function performs a calculation across a set of related rows while keeping the individual rows in the result.

This is the key distinction:

```text
GROUP BY
→ combines rows into groups

Window function
→ keeps individual rows
```

______________________________________________________________________

# 19. Basic Window Syntax

General form:

```sql
function(...) OVER (
    PARTITION BY ...
    ORDER BY ...
)
```

Example:

```sql
SELECT
    name,
    department_id,
    salary,
    AVG(salary) OVER (
        PARTITION BY department_id
    ) AS department_avg
FROM employees;
```

Each employee remains a separate row.

______________________________________________________________________

# 20. `PARTITION BY`

`PARTITION BY` divides rows into logical groups for the window calculation.

Example:

```sql
AVG(salary) OVER (
    PARTITION BY department_id
)
```

The average is calculated separately for each department.

It does not collapse rows.

______________________________________________________________________

# 21. `ORDER BY` in a Window

Window ordering defines the sequence used by functions such as:

- `ROW_NUMBER`
- `RANK`
- `DENSE_RANK`
- `LAG`
- `LEAD`
- Running aggregates

Example:

```sql
ROW_NUMBER() OVER (
    PARTITION BY department_id
    ORDER BY salary DESC
)
```

______________________________________________________________________

# 22. `ROW_NUMBER`

`ROW_NUMBER()` assigns a unique sequential number within each partition.

Example:

```sql
SELECT
    name,
    department_id,
    salary,
    ROW_NUMBER() OVER (
        PARTITION BY department_id
        ORDER BY salary DESC
    ) AS row_num
FROM employees;
```

If two employees have the same salary, they still receive different row numbers.

______________________________________________________________________

# 23. `RANK`

`RANK()` gives equal values the same rank.

Example salaries:

```text
100
100
90
80
```

Ranks:

```text
1
1
3
4
```

There is a gap after the tie.

______________________________________________________________________

# 24. `DENSE_RANK`

`DENSE_RANK()` also gives equal values the same rank but does not leave gaps.

For:

```text
100
100
90
80
```

the ranks are:

```text
1
1
2
3
```

______________________________________________________________________

# 25. `ROW_NUMBER` vs `RANK` vs `DENSE_RANK`

| Function | Ties | Example |
|---|---|---|
| `ROW_NUMBER` | Different numbers | 1, 2, 3, 4 |
| `RANK` | Same rank, gaps | 1, 1, 3, 4 |
| `DENSE_RANK` | Same rank, no gaps | 1, 1, 2, 3 |

This is a very common interview question.

______________________________________________________________________

# 26. Top N Per Group

A classic interview problem:

> Find the top three employees by salary in each department.

Use:

```sql
WITH ranked AS (
    SELECT
        e.*,
        ROW_NUMBER() OVER (
            PARTITION BY department_id
            ORDER BY salary DESC
        ) AS rn
    FROM employees e
)
SELECT *
FROM ranked
WHERE rn <= 3;
```

If ties should all be included, consider `RANK()` instead.

______________________________________________________________________

# 27. Latest Row Per Group

Another common pattern:

> Find the latest order for each user.

```sql
WITH ranked AS (
    SELECT
        o.*,
        ROW_NUMBER() OVER (
            PARTITION BY user_id
            ORDER BY created_at DESC, id DESC
        ) AS rn
    FROM orders o
)
SELECT *
FROM ranked
WHERE rn = 1;
```

Including a deterministic tie-breaker such as `id` is important when timestamps can be equal.

______________________________________________________________________

# 28. Second-Highest Value

A common interview question:

> Find the second-highest salary.

One approach:

```sql
SELECT salary
FROM (
    SELECT
        salary,
        DENSE_RANK() OVER (
            ORDER BY salary DESC
        ) AS rnk
    FROM employees
) x
WHERE rnk = 2;
```

`DENSE_RANK()` treats equal salaries as one rank.

______________________________________________________________________

# 29. `LAG`

`LAG()` accesses a previous row in the window ordering.

Example:

```sql
SELECT
    date,
    revenue,
    LAG(revenue) OVER (
        ORDER BY date
    ) AS previous_revenue
FROM daily_revenue;
```

This can be used to calculate changes over time.

______________________________________________________________________

# 30. Calculate Change With `LAG`

```sql
SELECT
    date,
    revenue,
    revenue - LAG(revenue) OVER (
        ORDER BY date
    ) AS revenue_change
FROM daily_revenue;
```

The first row has no previous row, so the result may be `NULL`.

______________________________________________________________________

# 31. `LEAD`

`LEAD()` accesses a following row.

```sql
SELECT
    date,
    revenue,
    LEAD(revenue) OVER (
        ORDER BY date
    ) AS next_revenue
FROM daily_revenue;
```

Useful for comparing the current row with a future row.

______________________________________________________________________

# 32. `LAG` vs `LEAD`

```text
LAG
 ↓
previous row

current row

LEAD
 ↓
next row
```

The ordering determines what "previous" and "next" mean.

______________________________________________________________________

# 33. Windowed Aggregates

Window functions can also perform aggregates.

Example:

```sql
SELECT
    date,
    revenue,
    SUM(revenue) OVER (
        ORDER BY date
    ) AS running_revenue
FROM daily_revenue;
```

This calculates a running total while preserving each daily row.

______________________________________________________________________

# 34. Running Total With Partition

Suppose revenue exists for multiple stores:

```sql
SELECT
    store_id,
    date,
    revenue,
    SUM(revenue) OVER (
        PARTITION BY store_id
        ORDER BY date
    ) AS running_revenue
FROM daily_revenue;
```

Each store gets its own running total.

______________________________________________________________________

# 35. Window Frame — Overview

A window can specify a frame that controls which rows contribute to the calculation.

For example:

```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
```

can explicitly represent a running calculation.

Frame semantics can become subtle when duplicate ordering values exist.

For interviews, understand that:

```text
PARTITION BY → which group
ORDER BY → ordering
frame → which rows in that ordered group
```

______________________________________________________________________

# 36. Set Operations

Set operations combine result sets.

Common operations:

```text
UNION
UNION ALL
INTERSECT
EXCEPT
```

Database support and syntax can vary.

______________________________________________________________________

# 37. `UNION`

`UNION` combines result sets and removes duplicates.

```sql
SELECT email FROM customers
UNION
SELECT email FROM employees;
```

The result contains unique emails.

______________________________________________________________________

# 38. `UNION ALL`

`UNION ALL` keeps duplicates.

```sql
SELECT email FROM customers
UNION ALL
SELECT email FROM employees;
```

It avoids duplicate elimination.

Use it when duplicate preservation is correct for the problem.

______________________________________________________________________

# 39. `INTERSECT`

`INTERSECT` returns rows present in both result sets.

Conceptually:

```text
A ∩ B
```

Example:

```sql
SELECT email FROM customers
INTERSECT
SELECT email FROM employees;
```

This finds emails appearing in both sets where supported.

______________________________________________________________________

# 40. `EXCEPT`

`EXCEPT` returns rows in the first result set that are not in the second.

Conceptually:

```text
A - B
```

Example:

```sql
SELECT email FROM customers
EXCEPT
SELECT email FROM employees;
```

This finds customer emails that do not appear among employees, subject to database semantics.

______________________________________________________________________

# 41. Set Operation Requirements

Set-operation queries generally need compatible result structures.

For example:

```sql
SELECT id, name FROM users
UNION
SELECT id, name FROM admins;
```

works conceptually because both sides return compatible columns.

______________________________________________________________________

# 42. Common Interview Pattern — Find Duplicates

Suppose:

```text
users
id
email
```

Find duplicate emails:

```sql
SELECT email, COUNT(*) AS count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

This is one of the most common SQL interview queries.

______________________________________________________________________

# 43. Common Interview Pattern — Find Duplicate Rows and Keep Latest

Suppose duplicate emails exist and you want to retain the newest row.

```sql
WITH ranked AS (
    SELECT
        u.*,
        ROW_NUMBER() OVER (
            PARTITION BY email
            ORDER BY created_at DESC, id DESC
        ) AS rn
    FROM users u
)
SELECT *
FROM ranked
WHERE rn = 1;
```

For deletion, use a carefully tested transaction and database-specific syntax.

______________________________________________________________________

# 44. Common Interview Pattern — Employees Above Department Average

Using a correlated subquery:

```sql
SELECT e.*
FROM employees e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department_id = e.department_id
);
```

Using a window function:

```sql
WITH x AS (
    SELECT
        e.*,
        AVG(salary) OVER (
            PARTITION BY department_id
        ) AS department_avg
    FROM employees e
)
SELECT *
FROM x
WHERE salary > department_avg;
```

Both express the same business idea.

______________________________________________________________________

# 45. Common Interview Pattern — Top Salary Per Department

```sql
WITH ranked AS (
    SELECT
        e.*,
        DENSE_RANK() OVER (
            PARTITION BY department_id
            ORDER BY salary DESC
        ) AS rnk
    FROM employees e
)
SELECT *
FROM ranked
WHERE rnk = 1;
```

Using `DENSE_RANK()` includes tied top salaries.

______________________________________________________________________

# 46. Common Interview Pattern — Customers With No Orders

Using `NOT EXISTS`:

```sql
SELECT *
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.id
);
```

Another valid approach is a `LEFT JOIN` with a carefully placed `IS NULL` condition.

______________________________________________________________________

# 47. Common Interview Pattern — First Order Per User

```sql
WITH ranked AS (
    SELECT
        o.*,
        ROW_NUMBER() OVER (
            PARTITION BY user_id
            ORDER BY created_at ASC, id ASC
        ) AS rn
    FROM orders o
)
SELECT *
FROM ranked
WHERE rn = 1;
```

The deterministic `id` tie-breaker prevents ambiguous results when timestamps match.

______________________________________________________________________

# 48. Common Interview Pattern — Previous Order

Use `LAG()`:

```sql
SELECT
    user_id,
    created_at,
    LAG(created_at) OVER (
        PARTITION BY user_id
        ORDER BY created_at, id
    ) AS previous_order_at
FROM orders;
```

This can help calculate time between orders.

______________________________________________________________________

# 49. Common Interview Pattern — Gap Between Events

Conceptually:

```sql
SELECT
    user_id,
    created_at,
    created_at
      - LAG(created_at) OVER (
            PARTITION BY user_id
            ORDER BY created_at, id
        ) AS gap
FROM events;
```

The exact date-difference syntax depends on the database.

______________________________________________________________________

# 50. Common Interview Pattern — Running Total

```sql
SELECT
    date,
    amount,
    SUM(amount) OVER (
        ORDER BY date
    ) AS running_total
FROM transactions;
```

If multiple entities exist:

```sql
SUM(amount) OVER (
    PARTITION BY account_id
    ORDER BY date
)
```

______________________________________________________________________

# 51. Common Interview Pattern — Month-over-Month Comparison

A common approach is:

1. Aggregate by month.
1. Use `LAG()` to retrieve the previous month.
1. Calculate the difference or percentage change.

Conceptually:

```sql
WITH monthly AS (
    SELECT
        month,
        SUM(revenue) AS revenue
    FROM sales
    GROUP BY month
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (
        ORDER BY month
    ) AS previous_month_revenue
FROM monthly;
```

______________________________________________________________________

# 52. Common Interview Pattern — Top N Overall vs Top N Per Group

These are different problems.

### Top N overall

```sql
ORDER BY score DESC
LIMIT 10
```

### Top N per group

Use:

```text
PARTITION BY group
+
ROW_NUMBER/RANK/DENSE_RANK
```

Confusing these is a common interview mistake.

______________________________________________________________________

# 53. Common Interview Pattern — Delete Duplicates

A common conceptual solution:

```sql
WITH ranked AS (
    SELECT
        id,
        ROW_NUMBER() OVER (
            PARTITION BY email
            ORDER BY created_at DESC, id DESC
        ) AS rn
    FROM users
)
DELETE ...
WHERE rn > 1;
```

The exact `DELETE` syntax varies by database.

Always verify the rows selected for deletion before executing destructive SQL.

______________________________________________________________________

# 54. `ROW_NUMBER` for Deduplication

`ROW_NUMBER()` is particularly useful when exactly one row must survive per group.

Example:

```text
email              rn
-----------------  --
a@example.com       1
a@example.com       2
a@example.com       3
```

Keep:

```text
rn = 1
```

and treat the rest as duplicates according to the business rule.

______________________________________________________________________

# 55. `RANK` for Competition-Style Ranking

Use `RANK()` when ties should share the same position and subsequent positions should have gaps.

Example:

```text
score   rank
100     1
100     1
90      3
80      4
```

______________________________________________________________________

# 56. `DENSE_RANK` for Distinct Ranking Levels

Use `DENSE_RANK()` when tied values share a rank but the next distinct value receives the next consecutive rank.

Example:

```text
score   dense_rank
100     1
100     1
90      2
80      3
```

______________________________________________________________________

# 57. Deterministic Ordering

When using:

```sql
ROW_NUMBER()
```

or other order-dependent functions, use a deterministic ordering when the business rule requires it.

Instead of:

```sql
ORDER BY created_at DESC
```

you may need:

```sql
ORDER BY created_at DESC, id DESC
```

if timestamps can tie.

______________________________________________________________________

# 58. `NULL` in Advanced Queries

Always consider how `NULL` affects:

- `IN`
- `NOT IN`
- Aggregates
- Ordering
- Comparisons
- Window calculations

For example:

```sql
NOT IN
```

with a `NULL` in the subquery can behave differently from what a developer expects.

`NOT EXISTS` is often a safer expression for existence semantics.

______________________________________________________________________

# 59. Filtering Window Results

In many SQL dialects, window-function results cannot be referenced directly in `WHERE` because `WHERE` is evaluated
before the window calculation.

Therefore, use a CTE or derived table:

```sql
WITH ranked AS (
    SELECT
        ...,
        ROW_NUMBER() OVER (...) AS rn
    FROM ...
)
SELECT *
FROM ranked
WHERE rn <= 3;
```

This is an extremely common interview pattern.

______________________________________________________________________

# 60. Window Functions vs GROUP BY

`GROUP BY`:

```sql
SELECT department_id, AVG(salary)
FROM employees
GROUP BY department_id;
```

returns one row per department.

Window function:

```sql
SELECT
    employee_id,
    department_id,
    salary,
    AVG(salary) OVER (
        PARTITION BY department_id
    )
FROM employees;
```

keeps every employee row and adds the department average.

______________________________________________________________________

# 61. Choosing the Right Technique

| Requirement | Common Technique |
|---|---|
| Membership | `IN` |
| Existence | `EXISTS` |
| Non-existence | `NOT EXISTS` |
| Complex stages | CTE |
| Top N per group | Window function |
| Deduplication | `ROW_NUMBER` |
| Ranking with gaps | `RANK` |
| Ranking without gaps | `DENSE_RANK` |
| Previous row | `LAG` |
| Next row | `LEAD` |
| Running total | Windowed `SUM` |
| Combine sets | `UNION` / `UNION ALL` |
| Common rows | `INTERSECT` |
| Difference between sets | `EXCEPT` |

______________________________________________________________________

# 62. Query Correctness Before Performance

For advanced SQL interviews, first establish:

```text
Correct rows
+
Correct duplicates
+
Correct NULL behavior
+
Correct tie handling
+
Correct ordering
```

Then discuss performance.

Performance optimization belongs primarily to File 21.

______________________________________________________________________

# 63. Advanced SQL Debugging

When an advanced query produces incorrect results:

1. Run each CTE independently.
1. Inspect row counts.
1. Inspect duplicate behavior.
1. Check join cardinality.
1. Check `NULL` behavior.
1. Check ordering.
1. Check window partitions.
1. Check tie-breaking.
1. Compare intermediate results.
1. Only then optimize.

Breaking a query into logical stages is especially useful with CTEs.

______________________________________________________________________

# 64. Common Advanced SQL Mistakes

## Mistake 1 — Using `NOT IN` with nullable data

Use careful `NULL` reasoning; `NOT EXISTS` is often clearer.

## Mistake 2 — Confusing `RANK` and `DENSE_RANK`

Know how ties affect the next rank.

## Mistake 3 — Using `ROW_NUMBER` when ties should be preserved

Use `RANK` or `DENSE_RANK` when the business requirement calls for tied results.

## Mistake 4 — Filtering a window function in `WHERE`

Use a CTE or derived table.

## Mistake 5 — Missing deterministic tie-breakers

Use an additional stable ordering column where necessary.

## Mistake 6 — Assuming CTEs are always faster

CTEs are primarily a query-organization technique unless database-specific behavior says otherwise.

## Mistake 7 — Optimizing before proving correctness

Validate the result first.

______________________________________________________________________

# 65. Interview Questions & Answers

## Q1. What is a subquery?

**Answer:**

A query nested inside another SQL statement.

______________________________________________________________________

## Q2. What is a correlated subquery?

**Answer:**

A subquery that references a value from the outer query.

______________________________________________________________________

## Q3. What is `EXISTS`?

**Answer:**

A predicate that checks whether a subquery returns at least one row.

______________________________________________________________________

## Q4. `EXISTS` vs `IN`?

**Answer:**

`IN` checks membership in a set of values.

`EXISTS` checks whether a matching row exists.

The best choice depends on semantics, `NULL` behavior, data shape and the database optimizer.

______________________________________________________________________

## Q5. Why can `NOT IN` be dangerous with `NULL`?

**Answer:**

SQL's three-valued logic means a `NULL` in the comparison set can cause predicates to evaluate to `UNKNOWN`, producing
results that may surprise developers.

______________________________________________________________________

## Q6. What is a CTE?

**Answer:**

A Common Table Expression is a named query expression defined with `WITH`.

It helps organize complex queries into logical stages.

______________________________________________________________________

## Q7. Is a CTE always faster than a subquery?

**Answer:**

No.

Performance depends on the database and query plan.

Use CTEs for clarity unless measured performance requirements dictate otherwise.

______________________________________________________________________

## Q8. What is a recursive CTE?

**Answer:**

A CTE that references itself, commonly used for hierarchical or tree-like data.

______________________________________________________________________

## Q9. What is a window function?

**Answer:**

A function that performs a calculation across related rows while preserving individual rows in the result.

______________________________________________________________________

## Q10. Window function vs `GROUP BY`?

**Answer:**

`GROUP BY` collapses rows into groups.

A window function calculates across a group while keeping the original rows.

______________________________________________________________________

## Q11. What does `PARTITION BY` do?

**Answer:**

It divides rows into logical groups for a window calculation.

______________________________________________________________________

## Q12. What does window `ORDER BY` do?

**Answer:**

It defines the row sequence used by order-sensitive window functions.

______________________________________________________________________

## Q13. What is `ROW_NUMBER()`?

**Answer:**

It assigns a unique sequential number to rows within each window partition.

______________________________________________________________________

## Q14. What is `RANK()`?

**Answer:**

It assigns equal values the same rank and leaves gaps after ties.

______________________________________________________________________

## Q15. What is `DENSE_RANK()`?

**Answer:**

It assigns equal values the same rank without leaving gaps after ties.

______________________________________________________________________

## Q16. `ROW_NUMBER` vs `RANK`?

**Answer:**

`ROW_NUMBER` gives every row a unique position.

`RANK` gives tied rows the same rank and leaves gaps.

______________________________________________________________________

## Q17. `RANK` vs `DENSE_RANK`?

**Answer:**

Both preserve ties.

`RANK` leaves gaps after ties.

`DENSE_RANK` does not.

______________________________________________________________________

## Q18. How do you find the top three employees per department?

**Answer:**

Use a window function such as:

```sql
ROW_NUMBER() OVER (
    PARTITION BY department_id
    ORDER BY salary DESC
)
```

Then filter the result to the required rank.

Use `RANK`/`DENSE_RANK` if tied salaries should all be included.

______________________________________________________________________

## Q19. How do you find the latest row per group?

**Answer:**

Use:

```sql
ROW_NUMBER() OVER (
    PARTITION BY group_id
    ORDER BY created_at DESC, id DESC
)
```

and select:

```text
row_number = 1
```

______________________________________________________________________

## Q20. What is `LAG()`?

**Answer:**

It accesses a previous row according to the window ordering.

______________________________________________________________________

## Q21. What is `LEAD()`?

**Answer:**

It accesses a following row according to the window ordering.

______________________________________________________________________

## Q22. How do you calculate a running total?

**Answer:**

Use a windowed aggregate:

```sql
SUM(amount) OVER (
    ORDER BY date
)
```

with `PARTITION BY` when separate totals are required per entity.

______________________________________________________________________

## Q23. How do you find the second-highest salary?

**Answer:**

One robust approach is:

```sql
DENSE_RANK() OVER (
    ORDER BY salary DESC
)
```

and filter for rank 2.

This treats tied salaries as the same rank.

______________________________________________________________________

## Q24. How do you find duplicate emails?

**Answer:**

```sql
SELECT email, COUNT(*)
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

______________________________________________________________________

## Q25. How do you keep only the newest row for each duplicate email?

**Answer:**

Use `ROW_NUMBER()` partitioned by email and ordered by newest timestamp, with a deterministic tie-breaker.

______________________________________________________________________

## Q26. What is `UNION`?

**Answer:**

It combines compatible result sets and removes duplicates.

______________________________________________________________________

## Q27. What is `UNION ALL`?

**Answer:**

It combines compatible result sets while preserving duplicates.

______________________________________________________________________

## Q28. What is `INTERSECT`?

**Answer:**

It returns rows common to both result sets where supported.

______________________________________________________________________

## Q29. What is `EXCEPT`?

**Answer:**

It returns rows from the first result set that are absent from the second, subject to database-specific semantics.

______________________________________________________________________

## Q30. Why might a window function need a CTE?

**Answer:**

In many SQL dialects, you cannot filter a window-function result directly in `WHERE`.

The CTE calculates the window value first, and the outer query filters it.

______________________________________________________________________

## Q31. Why are deterministic tie-breakers important?

**Answer:**

If the primary ordering column contains ties, adding a stable secondary column makes which row receives a particular
`ROW_NUMBER` deterministic.

______________________________________________________________________

## Q32. How would you find users with no orders?

**Answer:**

A common solution is:

```sql
WHERE NOT EXISTS (
    SELECT 1
    FROM orders
    WHERE orders.user_id = users.id
)
```

______________________________________________________________________

## Q33. How would you find employees above their department average?

**Answer:**

Use either a correlated subquery or a windowed `AVG()` partitioned by department.

______________________________________________________________________

## Q34. What is the difference between top N overall and top N per group?

**Answer:**

Top N overall applies one ordering to the complete result set.

Top N per group requires partitioning by the group and ranking within each partition.

______________________________________________________________________

## Q35. What is a window frame?

**Answer:**

It defines which rows within the ordered window contribute to a window calculation.

______________________________________________________________________

## Q36. What should you check when a window query gives unexpected results?

**Answer:**

Check:

- `PARTITION BY`
- `ORDER BY`
- Tie-breaking
- Window frame
- `NULL`s
- Duplicate input rows

______________________________________________________________________

## Q37. Can a window function replace every `GROUP BY`?

**Answer:**

No.

They serve different purposes.

`GROUP BY` reduces rows into groups, while window functions preserve row-level results.

______________________________________________________________________

## Q38. Are subqueries always slower than joins?

**Answer:**

No.

The database optimizer may transform queries, and performance depends on the actual query, data and database engine.

______________________________________________________________________

## Q39. Are CTEs always materialized?

**Answer:**

No.

CTE behavior depends on the database and version. Some systems may inline or materialize CTEs depending on the
situation.

______________________________________________________________________

## Q40. What is your approach to an advanced SQL interview problem?

**Answer:**

First define the expected result, identify entities and relationships, establish the required filtering and grouping,
choose an appropriate technique, handle duplicates/`NULL`s/ties, validate intermediate results, and then consider
performance.

______________________________________________________________________

# 66. Scenario-Based Questions

## Scenario 1 — Top Three Products Per Category

You need the top three products by sales in every category.

**Answer:**

Aggregate sales per product/category, then use:

```text
ROW_NUMBER/RANK/DENSE_RANK
+
PARTITION BY category
+
ORDER BY sales DESC
```

Choose the ranking function based on tie requirements.

______________________________________________________________________

## Scenario 2 — Latest Login Per User

A login table contains millions of records.

You need the latest login for every user.

**Answer:**

Use:

```sql
ROW_NUMBER() OVER (
    PARTITION BY user_id
    ORDER BY login_at DESC, id DESC
)
```

and keep rank 1.

______________________________________________________________________

## Scenario 3 — Users With No Activity

You need users who have never created an event.

**Answer:**

Use `NOT EXISTS`:

```sql
SELECT *
FROM users u
WHERE NOT EXISTS (
    SELECT 1
    FROM events e
    WHERE e.user_id = u.id
);
```

______________________________________________________________________

## Scenario 4 — Second-Highest Salary

Several employees have the highest salary.

**Question:** Should the next salary be rank 2?

**Answer:**

If the question means the second-highest **distinct salary**, use `DENSE_RANK()`.

______________________________________________________________________

## Scenario 5 — Previous Purchase

You need to calculate the time between each customer's purchases.

**Answer:**

Use:

```sql
LAG(purchased_at) OVER (
    PARTITION BY customer_id
    ORDER BY purchased_at, id
)
```

Then calculate the difference using database-specific date functions.

______________________________________________________________________

## Scenario 6 — Duplicate Accounts

Users accidentally registered multiple accounts with the same email.

You want to keep the newest account.

**Answer:**

Partition by email and use `ROW_NUMBER()` ordered by creation time descending, with a deterministic ID tie-breaker.

______________________________________________________________________

## Scenario 7 — Department Average

You need each employee's salary and their department's average salary on the same row.

**Answer:**

Use:

```sql
AVG(salary) OVER (
    PARTITION BY department_id
)
```

Do not use `GROUP BY` if you need to retain every employee row.

______________________________________________________________________

## Scenario 8 — Running Account Balance

You have transactions:

```text
account_id
transaction_at
amount
```

**Answer:**

Use:

```sql
SUM(amount) OVER (
    PARTITION BY account_id
    ORDER BY transaction_at, id
)
```

The stable secondary ordering column makes ordering deterministic when timestamps tie.

______________________________________________________________________

## Scenario 9 — `NOT IN` Produces Unexpected Results

A query using:

```sql
WHERE user_id NOT IN (...)
```

returns no rows.

**Answer:**

Investigate whether the subquery contains `NULL`.

For existence semantics, rewrite using `NOT EXISTS` where appropriate.

______________________________________________________________________

## Scenario 10 — Ranking Ties

A leaderboard should assign the same position to users with the same score.

**Answer:**

Use `RANK()` if the next position should skip after a tie.

Use `DENSE_RANK()` if positions should remain consecutive.

______________________________________________________________________

# 67. Practice Exercises

## Exercise 1 — Second Highest Salary

Write three solutions:

1. Subquery.
1. CTE.
1. `DENSE_RANK()`.

Explain how ties are handled.

______________________________________________________________________

## Exercise 2 — Top N Per Department

Find the top three employees by salary per department.

Implement using:

```text
ROW_NUMBER
RANK
DENSE_RANK
```

Compare their behavior with ties.

______________________________________________________________________

## Exercise 3 — Latest Order

Find the latest order for each user.

Add a deterministic tie-breaker.

______________________________________________________________________

## Exercise 4 — First Order

Find each user's first order using `ROW_NUMBER()`.

______________________________________________________________________

## Exercise 5 — No Orders

Find users who have never placed an order using:

```text
NOT EXISTS
LEFT JOIN
```

Compare the queries.

______________________________________________________________________

## Exercise 6 — Department Average

Return:

```text
employee
salary
department_average
difference_from_average
```

using a window function.

______________________________________________________________________

## Exercise 7 — Previous Event

For every user event, return:

```text
user_id
event_time
previous_event_time
```

using `LAG()`.

______________________________________________________________________

## Exercise 8 — Next Event

Use `LEAD()` to return the next event for every user.

______________________________________________________________________

## Exercise 9 — Running Total

Calculate a running total of transactions per account.

______________________________________________________________________

## Exercise 10 — Duplicate Cleanup

Identify duplicate users by email.

Use:

```sql
ROW_NUMBER()
```

to identify which row should survive according to a defined business rule.

Do not execute deletion until you verify the selected rows.

______________________________________________________________________

## Exercise 11 — Set Operations

Create two datasets and demonstrate:

```text
UNION
UNION ALL
INTERSECT
EXCEPT
```

where supported by your database.

______________________________________________________________________

## Exercise 12 — Month-over-Month

Aggregate revenue by month and use `LAG()` to calculate:

```text
current revenue
previous revenue
difference
percentage change
```

Handle a zero/`NULL` previous value correctly.

______________________________________________________________________

# 68. Quick Revision

| Concept | Key Point |
|---|---|
| Subquery | Query nested inside another query |
| Scalar subquery | Returns one value |
| Derived table | Subquery used as a table |
| `IN` | Membership in a set |
| `NOT IN` | Negated membership; beware `NULL` |
| `EXISTS` | Checks whether a row exists |
| `NOT EXISTS` | Checks whether no matching row exists |
| Correlated subquery | References outer query |
| CTE | Named query expression |
| Recursive CTE | Self-referencing CTE |
| Window function | Calculates across rows while preserving them |
| `PARTITION BY` | Defines window groups |
| Window `ORDER BY` | Defines sequence |
| Window frame | Defines rows participating in calculation |
| `ROW_NUMBER` | Unique sequential ranking |
| `RANK` | Ties share rank; gaps |
| `DENSE_RANK` | Ties share rank; no gaps |
| `LAG` | Previous row |
| `LEAD` | Next row |
| Running total | Windowed `SUM` |
| `UNION` | Combine and remove duplicates |
| `UNION ALL` | Combine and preserve duplicates |
| `INTERSECT` | Common rows |
| `EXCEPT` | Rows in first set but not second |
| Top N overall | Global ordering |
| Top N per group | Partition + ranking |
| Deduplication | Often `ROW_NUMBER` |
| Latest per group | Partition + descending order + rank 1 |
| Second distinct value | Often `DENSE_RANK` |
| Deterministic ordering | Stable tie-breaker |
| `GROUP BY` | Collapses rows into groups |
| Window aggregate | Aggregates while preserving rows |

______________________________________________________________________

# 69. Completion Checklist

Before moving to File 21, make sure you can explain and implement:

- [ ] Subqueries
- [ ] Scalar subqueries
- [ ] Derived tables
- [ ] `IN`
- [ ] `NOT IN`
- [ ] `EXISTS`
- [ ] `NOT EXISTS`
- [ ] `NULL` behavior with `NOT IN`
- [ ] Correlated subqueries
- [ ] CTEs
- [ ] Multiple CTEs
- [ ] Recursive CTE overview
- [ ] Window functions
- [ ] `PARTITION BY`
- [ ] Window `ORDER BY`
- [ ] Window frames overview
- [ ] `ROW_NUMBER`
- [ ] `RANK`
- [ ] `DENSE_RANK`
- [ ] Difference between ranking functions
- [ ] `LAG`
- [ ] `LEAD`
- [ ] Running totals
- [ ] Partitioned running totals
- [ ] `UNION`
- [ ] `UNION ALL`
- [ ] `INTERSECT`
- [ ] `EXCEPT`
- [ ] Find duplicates
- [ ] Deduplicate with `ROW_NUMBER`
- [ ] Latest row per group
- [ ] First row per group
- [ ] Top N overall
- [ ] Top N per group
- [ ] Second-highest distinct value
- [ ] Previous-row comparisons
- [ ] Next-row comparisons
- [ ] Month-over-month comparisons
- [ ] Filtering window results with a CTE
- [ ] Deterministic tie-breaking
- [ ] Advanced SQL debugging
- [ ] Common SQL interview patterns

______________________________________________________________________

# 70. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is a subquery?
1. What is a scalar subquery?
1. What is a derived table?
1. What is a correlated subquery?
1. What is the difference between correlated and non-correlated subqueries?
1. What does `IN` do?
1. What does `EXISTS` do?
1. `EXISTS` vs `IN`?
1. Why can `NOT IN` behave unexpectedly with `NULL`?
1. Why is `NOT EXISTS` often useful for non-existence checks?
1. What is a CTE?
1. Why would you use a CTE instead of a nested subquery?
1. Is a CTE always faster?
1. What is a recursive CTE?
1. What is a window function?
1. How is a window function different from `GROUP BY`?
1. What does `PARTITION BY` do?
1. What does window `ORDER BY` do?
1. What is `ROW_NUMBER()`?
1. What is `RANK()`?
1. What is `DENSE_RANK()`?
1. Explain the difference between `ROW_NUMBER`, `RANK` and `DENSE_RANK`.
1. How do you find the top three employees per department?
1. How do you find the latest row per user?
1. How do you find the second-highest distinct salary?
1. What is `LAG()`?
1. What is `LEAD()`?
1. How do you calculate a running total?
1. How do you calculate a previous-period value?
1. What is a window frame?
1. What is `UNION`?
1. What is `UNION ALL`?
1. What is `INTERSECT`?
1. What is `EXCEPT`?
1. How do you find duplicate emails?
1. How do you keep the newest row for each duplicate email?
1. How do you find users with no orders?
1. How do you find employees earning above their department average?
1. How do you find the first order for every customer?
1. How do you calculate the time between consecutive events?
1. Why are deterministic tie-breakers important?
1. Why can't you always filter a window function directly in `WHERE`?
1. How do you solve top N per group?
1. What is the difference between top N overall and top N per group?
1. When would you use `ROW_NUMBER` instead of `RANK`?
1. When would you use `DENSE_RANK`?
1. Can subqueries always be replaced by joins?
1. Can window functions replace every `GROUP BY`?
1. How would you debug an advanced SQL query producing incorrect results?
1. What is your general approach to solving a complex SQL interview problem?

If you can answer these confidently and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [19. Database Design & Normalization](./19-database-normalization.md)

**Next:** [21. SQL Indexes & Query Performance](./21-sql-indexes-performance.md)

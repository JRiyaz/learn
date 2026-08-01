# SQLAlchemy Advanced Queries

## Introduction

Once your models and relationships are defined, the next step is writing efficient queries.

Although SQLAlchemy lets you work with Python objects, every ORM query eventually becomes SQL.

One of the biggest mistakes developers make is treating SQLAlchemy as "magic."

**Every SQLAlchemy query should be understood in terms of the SQL it generates.**

Throughout this chapter, every ORM example includes:

- SQLAlchemy code
- Equivalent SQL
- Performance notes
- Interview tips

Topics covered:

- Select API
- Filtering
- AND / OR / NOT
- IN
- BETWEEN
- LIKE / ILIKE
- NULL handling
- Aliases
- Joins
- Aggregations
- GROUP BY
- HAVING
- Window Functions
- Subqueries
- EXISTS
- CTE
- Raw SQL
- Transactions
- Row Locking

______________________________________________________________________

# The Select API

SQLAlchemy 2.x uses the `select()` construct.

```python id="saq001"
from sqlalchemy import select

stmt = select(Employee)
```

Equivalent SQL

```sql id="saq002"
SELECT *
FROM employees;
```

______________________________________________________________________

# Selecting Specific Columns

Instead of loading the entire object:

```python id="saq003"
stmt = select(
    Employee.employee_id,
    Employee.name
)
```

Equivalent SQL

```sql id="saq004"
SELECT
employee_id,
name
FROM employees;
```

Interview Tip:

Only retrieve the columns you need.

______________________________________________________________________

# Filtering

```python id="saq005"
stmt = (
    select(Employee)
    .where(Employee.salary > 80000)
)
```

Equivalent SQL

```sql id="saq006"
SELECT *
FROM employees
WHERE salary > 80000;
```

______________________________________________________________________

# Multiple Conditions

```python id="saq007"
stmt = (
    select(Employee)
    .where(
        Employee.salary > 80000,
        Employee.department_id == 2
    )
)
```

Equivalent SQL

```sql id="saq008"
SELECT *
FROM employees
WHERE salary > 80000
AND department_id = 2;
```

______________________________________________________________________

# OR Conditions

```python id="saq009"
from sqlalchemy import or_

stmt = (
    select(Employee)
    .where(
        or_(
            Employee.department_id == 1,
            Employee.department_id == 2
        )
    )
)
```

Equivalent SQL

```sql id="saq010"
SELECT *
FROM employees
WHERE department_id = 1
OR department_id = 2;
```

______________________________________________________________________

# NOT Conditions

```python id="saq011"
from sqlalchemy import not_

stmt = (
    select(Employee)
    .where(
        not_(Employee.department_id == 1)
    )
)
```

Equivalent SQL

```sql id="saq012"
SELECT *
FROM employees
WHERE department_id <> 1;
```

______________________________________________________________________

# IN

```python id="saq013"
stmt = (
    select(Employee)
    .where(
        Employee.department_id.in_([1, 2, 3])
    )
)
```

Equivalent SQL

```sql id="saq014"
SELECT *
FROM employees
WHERE department_id IN (1,2,3);
```

______________________________________________________________________

# BETWEEN

```python id="saq015"
stmt = (
    select(Employee)
    .where(
        Employee.salary.between(
            70000,
            90000
        )
    )
)
```

Equivalent SQL

```sql id="saq016"
SELECT *
FROM employees
WHERE salary
BETWEEN 70000
AND 90000;
```

______________________________________________________________________

# LIKE

```python id="saq017"
stmt = (
    select(Employee)
    .where(
        Employee.name.like("A%")
    )
)
```

Equivalent SQL

```sql id="saq018"
SELECT *
FROM employees
WHERE name LIKE 'A%';
```

______________________________________________________________________

# ILIKE (PostgreSQL)

```python id="saq019"
stmt = (
    select(Employee)
    .where(
        Employee.name.ilike("a%")
    )
)
```

Equivalent SQL

```sql id="saq020"
SELECT *
FROM employees
WHERE name ILIKE 'a%';
```

______________________________________________________________________

# NULL Handling

Instead of

```python id="saq021"
Employee.manager_id == None
```

Prefer

```python id="saq022"
stmt = (
    select(Employee)
    .where(
        Employee.manager_id.is_(None)
    )
)
```

Equivalent SQL

```sql id="saq023"
SELECT *
FROM employees
WHERE manager_id IS NULL;
```

Similarly,

```python id="saq024"
Employee.manager_id.is_not(None)
```

becomes

```sql id="saq025"
WHERE manager_id IS NOT NULL;
```

______________________________________________________________________

# Ordering

```python id="saq026"
stmt = (
    select(Employee)
    .order_by(Employee.salary.desc())
)
```

Equivalent SQL

```sql id="saq027"
SELECT *
FROM employees
ORDER BY salary DESC;
```

______________________________________________________________________

# Pagination

```python id="saq028"
stmt = (
    select(Employee)
    .limit(10)
    .offset(20)
)
```

Equivalent SQL

```sql id="saq029"
SELECT *
FROM employees
LIMIT 10 OFFSET 20;
```

Remember from the SQL section:

Large offsets become slow.

______________________________________________________________________

# Table Aliases

Useful for self joins.

```python id="saq030"
from sqlalchemy.orm import aliased

Manager = aliased(Employee)
```

Example

```python id="saq031"
stmt = (
    select(
        Employee.name,
        Manager.name
    )
    .join(
        Manager,
        Employee.manager_id == Manager.employee_id
    )
)
```

Equivalent SQL

```sql id="saq032"
SELECT
e.name,
m.name
FROM employees e
JOIN employees m
ON e.manager_id = m.employee_id;
```

______________________________________________________________________

# INNER JOIN

```python id="saq033"
stmt = (
    select(Employee, Department)
    .join(
        Department,
        Employee.department_id == Department.department_id
    )
)
```

Equivalent SQL

```sql id="saq034"
SELECT *
FROM employees
JOIN departments
ON employees.department_id =
departments.department_id;
```

______________________________________________________________________

# LEFT JOIN

```python id="saq035"
stmt = (
    select(Employee, Department)
    .outerjoin(
        Department
    )
)
```

Equivalent SQL

```sql id="saq036"
SELECT *
FROM employees
LEFT JOIN departments
ON employees.department_id =
departments.department_id;
```

______________________________________________________________________

# Aggregations

Count employees.

```python id="saq037"
from sqlalchemy import func

stmt = (
    select(
        func.count()
    )
)
```

Equivalent SQL

```sql id="saq038"
SELECT COUNT(*)
FROM employees;
```

______________________________________________________________________

# GROUP BY

```python id="saq039"
stmt = (
    select(
        Employee.department_id,
        func.avg(Employee.salary)
    )
    .group_by(
        Employee.department_id
    )
)
```

Equivalent SQL

```sql id="saq040"
SELECT
department_id,
AVG(salary)
FROM employees
GROUP BY department_id;
```

______________________________________________________________________

# HAVING

```python id="saq041"
stmt = (
    select(
        Employee.department_id,
        func.count()
    )
    .group_by(
        Employee.department_id
    )
    .having(
        func.count() > 5
    )
)
```

Equivalent SQL

```sql id="saq042"
SELECT
department_id,
COUNT(*)
FROM employees
GROUP BY department_id
HAVING COUNT(*) > 5;
```

______________________________________________________________________

# Window Functions

```python id="saq043"
from sqlalchemy import func

stmt = (
    select(
        Employee.name,
        func.row_number()
        .over(
            order_by=Employee.salary.desc()
        )
    )
)
```

Equivalent SQL

```sql id="saq044"
SELECT
name,
ROW_NUMBER()
OVER(
ORDER BY salary DESC
)
FROM employees;
```

Any SQL window function (`RANK`, `DENSE_RANK`, `LAG`, `LEAD`, etc.) can be expressed similarly using `.over()`.

______________________________________________________________________

# Scalar Subquery

```python id="saq045"
avg_salary = (
    select(
        func.avg(Employee.salary)
    )
    .scalar_subquery()
)

stmt = (
    select(Employee)
    .where(
        Employee.salary > avg_salary
    )
)
```

Equivalent SQL

```sql id="saq046"
SELECT *
FROM employees
WHERE salary >
(
SELECT AVG(salary)
FROM employees
);
```

______________________________________________________________________

# EXISTS

```python id="saq047"
from sqlalchemy import exists

stmt = (
    select(Customer)
    .where(
        exists(
            select(Order.order_id)
            .where(
                Order.customer_id == Customer.customer_id
            )
        )
    )
)
```

Equivalent SQL

```sql id="saq048"
SELECT *
FROM customers
WHERE EXISTS
(
SELECT 1
FROM orders
WHERE orders.customer_id =
customers.customer_id
);
```

______________________________________________________________________

# Common Table Expressions (CTE)

```python id="saq049"
employee_cte = (
    select(Employee)
    .where(Employee.salary > 80000)
    .cte("high_salary")
)

stmt = select(employee_cte)
```

Equivalent SQL

```sql id="saq050"
WITH high_salary AS
(
SELECT *
FROM employees
WHERE salary > 80000
)
SELECT *
FROM high_salary;
```

______________________________________________________________________

# Executing Raw SQL

Sometimes raw SQL is the best tool.

```python id="saq051"
from sqlalchemy import text

stmt = text(
    """
    SELECT *
    FROM employees
    WHERE salary > :salary
    """
)

rows = session.execute(
    stmt,
    {"salary": 80000}
)
```

Parameterized queries protect against SQL injection.

______________________________________________________________________

# Transactions

```python id="saq052"
with Session(engine) as session:
    with session.begin():

        employee.salary = 95000
```

The transaction commits automatically if no exception occurs.

______________________________________________________________________

# Row Locking

```python id="saq053"
stmt = (
    select(Employee)
    .where(Employee.employee_id == 1)
    .with_for_update()
)
```

Equivalent SQL

```sql id="saq054"
SELECT *
FROM employees
WHERE employee_id = 1
FOR UPDATE;
```

Useful for preventing concurrent updates.

______________________________________________________________________

# Common Mistakes

### Loading Entire Objects

Select only required columns when appropriate.

______________________________________________________________________

### Using Python Filtering

Bad

```python id="saq055"
employees = session.scalars(
    select(Employee)
).all()

filtered = [
    e for e in employees
    if e.salary > 80000
]
```

Always let the database perform filtering.

______________________________________________________________________

### Forgetting EXISTS

Sometimes `EXISTS` is more efficient than joining when you only need to know whether related rows exist.

______________________________________________________________________

### Using Raw SQL Everywhere

Use ORM queries for maintainability.

Use raw SQL only when it provides a clear advantage.

______________________________________________________________________

# Best Practices

- Learn the generated SQL.
- Prefer database-side filtering.
- Use aliases for self joins.
- Use `func` for SQL functions.
- Prefer parameterized SQL.
- Measure query performance with `EXPLAIN`.
- Choose ORM or raw SQL based on the problem, not personal preference.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** When would you choose raw SQL instead of SQLAlchemy ORM?

I would use SQLAlchemy ORM for most CRUD operations and business logic because it improves readability, maintainability,
and integrates well with Python models. However, I would consider raw SQL for highly optimized reporting queries,
database-specific features not easily expressed in the ORM, bulk data operations, or when profiling shows that a
carefully written SQL statement provides a measurable performance benefit. Even then, I would use parameterized queries
to avoid SQL injection.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is the Select API?
1. Why use `select()` instead of the legacy `query()` API?
1. Explain `func`.
1. Explain `aliased()`.
1. How do you perform a LEFT JOIN?
1. How do you write a subquery?
1. What is `scalar_subquery()`?
1. How do you create a CTE?
1. When should you use raw SQL?
1. What does `with_for_update()` do?

## Coding

1. Retrieve employees earning above ₹80,000.
1. Find employees in multiple departments using `IN`.
1. Rank employees by salary.
1. Find employees earning above the company average.
1. Build a reporting CTE.
1. Execute a parameterized raw SQL query.
1. Lock an employee row before updating it.

______________________________________________________________________

# Hands-on Exercise

Build reporting queries for the Employee Management application.

Requirements:

1. Filter employees by salary.
1. Search by employee name.
1. Join employees with departments.
1. Calculate average salary per department.
1. Find employees above the company average.
1. Rank employees by salary.
1. Create a CTE for high earners.
1. Execute the equivalent raw SQL.
1. Compare the generated SQL with handwritten SQL.
1. Inspect the execution plan using `EXPLAIN`.

______________________________________________________________________

# Cheat Sheet

```text id="saq056"
select()

↓

where()

↓

join()

outerjoin()

↓

func()

↓

group_by()

having()

↓

over()

↓

scalar_subquery()

↓

exists()

↓

cte()

↓

text()

↓

with_for_update()
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- SQLAlchemy 2.x Select API
- Filtering
- Boolean conditions
- `IN`
- `BETWEEN`
- `LIKE` / `ILIKE`
- NULL handling
- Aliases
- INNER and LEFT JOINs
- Aggregations
- `GROUP BY`
- `HAVING`
- Window functions
- Scalar subqueries
- `EXISTS`
- CTEs
- Raw SQL execution
- Transactions
- Row locking
- Performance considerations
- Interview patterns
- Best practices

You now have the skills to translate most advanced SQL queries into SQLAlchemy while understanding the SQL generated
underneath.

______________________________________________________________________

## Next File

[SQLAlchemy Performance & Production Patterns](18-sqlalchemy-performance.md)

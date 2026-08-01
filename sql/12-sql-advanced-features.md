# Views, Materialized Views, Triggers & Stored Functions

## Introduction

As applications grow, SQL queries become increasingly complex.

Instead of repeating the same joins and calculations everywhere, databases provide higher-level features such as:

- Views
- Materialized Views
- Stored Functions
- Stored Procedures
- Triggers

These features improve maintainability, encapsulate business logic, and simplify reporting.

They are commonly discussed in backend interviews, especially for PostgreSQL, Oracle, SQL Server, and enterprise
applications.

______________________________________________________________________

# What is a View?

A **View** is a virtual table created from the result of a SQL query.

Unlike a regular table, a view does **not** normally store data. It stores only the SQL query definition.

General syntax

```sql id="vw001"
CREATE VIEW employee_details AS
SELECT
    e.employee_id,
    e.name,
    d.department_name
FROM employees e
JOIN departments d
ON e.department_id = d.department_id;
```

______________________________________________________________________

# Querying a View

Once created, a view behaves like a table.

```sql id="vw002"
SELECT *
FROM employee_details;
```

Applications don't need to know how the data is joined internally.

______________________________________________________________________

# Why Use Views?

Views help to:

- Simplify complex queries
- Hide implementation details
- Restrict access to sensitive columns
- Reuse common queries
- Improve readability

Example

Instead of writing:

```sql id="vw003"
SELECT
e.name,
d.department_name
FROM employees e
JOIN departments d
ON e.department_id = d.department_id;
```

everywhere, developers can simply use:

```sql id="vw004"
SELECT *
FROM employee_details;
```

______________________________________________________________________

# Updating Through Views

Some views are updatable.

Example

```sql id="vw005"
CREATE VIEW active_users AS
SELECT *
FROM users
WHERE active = TRUE;
```

Updating

```sql id="vw006"
UPDATE active_users
SET email = 'alice@example.com'
WHERE user_id = 1;
```

Whether a view is updatable depends on the database engine and the complexity of the view. Simple single-table views are
commonly updatable, while views containing joins, aggregates, or `GROUP BY` often are not.

______________________________________________________________________

# Dropping a View

```sql id="vw007"
DROP VIEW employee_details;
```

______________________________________________________________________

# Materialized View

A Materialized View stores the query result physically.

Unlike a normal view:

- View stores SQL
- Materialized View stores data

Example

```sql id="vw008"
CREATE MATERIALIZED VIEW department_salary AS
SELECT
department_id,
AVG(salary) AS average_salary
FROM employees
GROUP BY department_id;
```

______________________________________________________________________

# Querying a Materialized View

```sql id="vw009"
SELECT *
FROM department_salary;
```

The query is fast because the results are already stored.

______________________________________________________________________

# Refreshing a Materialized View

Underlying table changes do **not** automatically update the materialized view.

Refresh manually.

```sql id="vw010"
REFRESH MATERIALIZED VIEW department_salary;
```

PostgreSQL also supports:

```sql id="vw011"
REFRESH MATERIALIZED VIEW CONCURRENTLY department_salary;
```

`CONCURRENTLY` allows reads during refresh but has additional requirements, such as a unique index on the materialized
view.

______________________________________________________________________

# View vs Materialized View

| View | Materialized View |
| ------------------------------------ | ------------------------------------- |
| Stores SQL | Stores Data |
| Always current | May become stale |
| No storage for result | Requires storage |
| Executes every query | Refresh required |
| Usually slower for expensive queries | Faster for repeated reporting queries |

______________________________________________________________________

# Stored Functions

A Stored Function is reusable SQL logic that returns a value.

Example (PostgreSQL)

```sql id="vw012"
CREATE FUNCTION yearly_salary(
monthly_salary NUMERIC
)
RETURNS NUMERIC
AS
$$
BEGIN
    RETURN monthly_salary * 12;
END;
$$
LANGUAGE plpgsql;
```

Usage

```sql id="vw013"
SELECT yearly_salary(50000);
```

Result

```text id="vw014"
600000
```

______________________________________________________________________

# Functions Returning Tables

Functions can also return multiple rows.

Example

```sql id="vw015"
CREATE FUNCTION it_employees()
RETURNS TABLE(
employee_id INT,
name TEXT
)
AS
$$
SELECT
employee_id,
name
FROM employees
WHERE department_id = 2;
$$
LANGUAGE SQL;
```

Usage

```sql id="vw016"
SELECT *
FROM it_employees();
```

______________________________________________________________________

# Stored Procedures

Procedures are similar to functions but are designed to perform operations rather than return values.

PostgreSQL example

```sql id="vw017"
CREATE PROCEDURE increase_salary()
LANGUAGE plpgsql
AS
$$
BEGIN
    UPDATE employees
    SET salary = salary * 1.05;
END;
$$;
```

Execute

```sql id="vw018"
CALL increase_salary();
```

______________________________________________________________________

# Function vs Procedure

| Function | Procedure |
| --------------------------- | ---------------------------------- |
| Returns a value or table | Primarily performs actions |
| Can be used inside SELECT | Invoked using CALL |
| Often used for calculations | Often used for business operations |

______________________________________________________________________

# What is a Trigger?

A Trigger automatically executes when a database event occurs.

Events include:

- INSERT
- UPDATE
- DELETE

Triggers help automate auditing, validation, and synchronization.

______________________________________________________________________

# BEFORE INSERT Trigger

Example

```sql id="vw019"
CREATE FUNCTION set_created_at()
RETURNS TRIGGER
AS
$$
BEGIN
    NEW.created_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;
```

Create trigger

```sql id="vw020"
CREATE TRIGGER employee_created

BEFORE INSERT

ON employees

FOR EACH ROW

EXECUTE FUNCTION set_created_at();
```

Now every inserted employee automatically receives a timestamp.

______________________________________________________________________

# AFTER UPDATE Trigger

Example

```sql id="vw021"
CREATE FUNCTION log_salary_change()
RETURNS TRIGGER
AS
$$
BEGIN
    INSERT INTO salary_audit(
        employee_id,
        old_salary,
        new_salary,
        changed_at
    )
    VALUES(
        OLD.employee_id,
        OLD.salary,
        NEW.salary,
        CURRENT_TIMESTAMP
    );

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;
```

Trigger

```sql id="vw022"
CREATE TRIGGER salary_audit_trigger

AFTER UPDATE

ON employees

FOR EACH ROW

EXECUTE FUNCTION log_salary_change();
```

______________________________________________________________________

# OLD and NEW

Triggers provide special records.

```text id="vw023"
OLD

↓

Previous Row

-----------------

NEW

↓

Updated Row
```

Used for auditing and validation.

______________________________________________________________________

# BEFORE vs AFTER Triggers

| BEFORE | AFTER |
| ---------------------------- | ---------------------------------------------------- |
| Executes before modification | Executes after modification |
| Can modify NEW values | Commonly used for auditing |
| Can reject operations | Sees final committed row values within the statement |

______________________________________________________________________

# INSTEAD OF Triggers

Some databases support **INSTEAD OF** triggers, primarily on views.

They replace the default INSERT, UPDATE, or DELETE behavior with custom logic.

This is useful for making complex views writable.

Support varies by database system.

______________________________________________________________________

# SQLAlchemy and Views

Views are queried like normal tables.

Example

```python id="vw024"
class EmployeeDetails(Base):
    __tablename__ = "employee_details"

stmt = select(EmployeeDetails)
```

SQLAlchemy does not automatically create views. Views are typically created using migration tools (such as Alembic) or
raw SQL.

______________________________________________________________________

# SQLModel

SQLModel can also map to an existing view as a read-only model.

View creation is usually handled outside SQLModel.

______________________________________________________________________

# Performance Considerations

### Views

- Improve readability.
- Do not automatically improve performance.
- Complex views may still execute expensive queries.

### Materialized Views

- Excellent for reporting.
- Require refresh.
- Consume storage.

### Functions

- Reduce duplicated SQL.
- Keep business rules close to the data when appropriate.
- Avoid placing excessive business logic inside the database.

### Triggers

- Useful for auditing.
- Can make application behavior harder to understand if overused.
- Document trigger behavior clearly.

______________________________________________________________________

# Common Mistakes

### Assuming Views Store Data

Regular views store only the query definition.

______________________________________________________________________

### Forgetting to Refresh Materialized Views

Data becomes outdated.

______________________________________________________________________

### Overusing Triggers

Hidden database logic can complicate debugging.

______________________________________________________________________

### Writing Business Logic Everywhere

Choose the right layer.

Some logic belongs in the application.

Some belongs in the database.

______________________________________________________________________

# Best Practices

- Use views to simplify repeated queries.
- Use materialized views for expensive reporting queries.
- Keep stored functions focused and reusable.
- Use triggers primarily for auditing and data integrity.
- Document every trigger in production systems.
- Monitor refresh time for materialized views.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between a View and a Materialized View?

A View stores only a SQL query definition and executes that query every time it is accessed, so it always reflects the
latest data. A Materialized View stores the query results physically, making reads much faster for expensive queries,
but it must be refreshed to reflect changes in the underlying tables. Materialized Views are commonly used for reporting
and analytics.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is a view?
1. What is a materialized view?
1. Difference between a view and a materialized view.
1. What is a stored function?
1. Difference between a function and a procedure.
1. What is a trigger?
1. Difference between BEFORE and AFTER triggers.
1. What are `OLD` and `NEW`?

## Coding

1. Create a view joining employees and departments.
1. Create a materialized view for department salaries.
1. Refresh the materialized view.
1. Create a function to calculate yearly salary.
1. Create a procedure that increases salaries by 5%.
1. Create a trigger to audit salary updates.

______________________________________________________________________

# Hands-on Exercise

Create:

- Employees
- Departments
- Salary Audit

Tasks:

1. Create a reusable employee view.
1. Create a materialized reporting view.
1. Refresh the materialized view after inserts.
1. Write a stored function.
1. Write a stored procedure.
1. Implement a salary audit trigger.
1. Access the view using SQLAlchemy.
1. Access the view using SQLModel.

______________________________________________________________________

# Cheat Sheet

```text id="vw025"
View
→ Virtual Table

Materialized View
→ Stored Result

Function
→ Returns Value

Procedure
→ Performs Action

Trigger
→ Automatic Execution

Events

INSERT
UPDATE
DELETE
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Views
- Updatable views
- Materialized views
- Refreshing materialized views
- Stored functions
- Functions returning tables
- Stored procedures
- Triggers
- BEFORE and AFTER triggers
- OLD and NEW records
- SQLAlchemy integration
- SQLModel integration
- Performance considerations
- Interview patterns
- Best practices

You now understand how databases encapsulate reusable logic, automate actions, and optimize complex reporting queries
using advanced SQL features.

______________________________________________________________________

## Next File

[Questions Part 1](13.questions-part-1.md)

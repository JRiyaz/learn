# 19. Database Design & Normalization

**Previous:** [18. SQL Fundamentals](./18-sql-fundamentals.md)

**Next:** [20. Advanced SQL Queries](./20-sql-advanced.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain the fundamentals of relational database design.
- Identify unnecessary redundancy in a schema.
- Explain insert, update and delete anomalies.
- Understand functional dependencies.
- Identify candidate keys and primary keys.
- Explain 1NF, 2NF and 3NF clearly in an interview.
- Explain BCNF at an overview level.
- Normalize a practical schema step by step.
- Explain when normalization is beneficial.
- Explain normalization vs denormalization.
- Discuss real-world backend trade-offs when designing a database.

> **Scope note:** File 18 introduced normalization briefly. This is the **dedicated database-design topic** where normalization is covered properly. Advanced SQL query techniques continue in File 20.

______________________________________________________________________

# 1. What Is Database Design?

Database design is the process of deciding:

- What data should be stored.
- How data should be represented.
- Which entities and relationships exist.
- Which constraints should be enforced.
- How tables should be structured.
- How duplication and integrity problems should be controlled.

A good schema should represent the domain accurately while supporting the application's access patterns.

______________________________________________________________________

# 2. Start With the Domain

Before creating tables, identify the important entities and relationships.

For an e-commerce system, you might identify:

```text
Customer
Order
Product
OrderItem
Payment
Address
```

Then ask:

- What does each entity represent?
- What identifies it?
- What relationships exist?
- Which attributes belong to which entity?
- Which values can change independently?

______________________________________________________________________

# 3. Entity vs Attribute

An entity represents something meaningful in the domain.

Example:

```text
Customer
```

Attributes might be:

```text
customer_id
name
email
```

A common design mistake is putting attributes into the wrong entity simply because they appear together in an initial
data source.

Database design should reflect ownership and dependency.

______________________________________________________________________

# 4. Relationships

Common relationships are:

### One-to-one

```text
User → Profile
```

### One-to-many

```text
Customer → Orders
```

### Many-to-many

```text
Students ↔ Courses
```

A many-to-many relationship normally needs a junction/association table.

______________________________________________________________________

# 5. Example Many-to-Many Design

Instead of:

```text
students
courses
```

trying to store multiple course IDs inside a student row, use:

```text
students
courses
student_courses
```

Example:

```text
student_courses
----------------
student_id
course_id
```

The association table represents the relationship.

______________________________________________________________________

# 6. Redundancy

Redundancy means storing the same logical information in multiple places.

Example:

```text
order_id | customer_id | customer_name | customer_email
```

If a customer has 100 orders, their name and email may be repeated across many rows.

Redundancy is not automatically wrong, but uncontrolled redundancy creates consistency and maintenance problems.

______________________________________________________________________

# 7. Why Redundancy Is Dangerous

Suppose:

```text
Customer ID = 10
Customer Name = Alice
```

appears in 100 rows.

Alice changes her name.

If only 99 rows are updated:

```text
Alice Smith
Alice Smith
...
Alice
```

the database contains conflicting representations of the same logical fact.

This is an update anomaly.

______________________________________________________________________

# 8. Data Anomalies

Poorly designed schemas can create three classic anomalies:

- Insert anomaly
- Update anomaly
- Delete anomaly

These anomalies are a major reason normalization exists.

______________________________________________________________________

# 9. Insert Anomaly

An insert anomaly occurs when you cannot insert one piece of information without also providing unrelated information.

Example:

```text
student_course
--------------------------------
student_id
student_name
course_id
course_name
```

Suppose a new course has not yet been assigned to any student.

If the table requires a student row to represent the course, you cannot cleanly store:

```text
course_id = 100
course_name = Databases
```

without inventing unrelated student information.

Separating students and courses solves this design problem.

______________________________________________________________________

# 10. Update Anomaly

An update anomaly occurs when the same logical fact is duplicated and must be updated in multiple rows.

Example:

```text
order_id | customer_id | customer_email
1        | 10          | old@example.com
2        | 10          | old@example.com
3        | 10          | old@example.com
```

Changing the email requires updating multiple rows.

If one update is missed, the database becomes inconsistent.

______________________________________________________________________

# 11. Delete Anomaly

A delete anomaly occurs when deleting one fact accidentally removes another fact that should remain.

Example:

```text
course_id | course_name | student_id
10        | Databases    | 1
```

If this is the only row representing the course and the student leaves, deleting the row could accidentally remove the
information that the course exists.

Separating entities prevents this.

______________________________________________________________________

# 12. Functional Dependency

A functional dependency describes a relationship where one attribute determines another.

Notation:

```text
A → B
```

means:

> If we know A, we can determine B.

Example:

```text
employee_id → employee_name
```

assuming each employee ID identifies exactly one employee.

______________________________________________________________________

# 13. Functional Dependency Example

Suppose:

```text
employee_id = 10
```

always identifies:

```text
employee_name = Alice
department_id = 5
```

Then:

```text
employee_id → employee_name
employee_id → department_id
```

These dependencies help determine whether attributes belong together.

______________________________________________________________________

# 14. Candidate Key

A candidate key is a minimal set of attributes that can uniquely identify a row.

For:

```text
employees
```

possible candidate keys might include:

```text
employee_id
email
```

if both are unique and stable enough to identify employees under the domain rules.

A table can have multiple candidate keys.

______________________________________________________________________

# 15. Primary Key

The primary key is the candidate key selected as the table's primary identifier.

Example:

```sql
CREATE TABLE employees (
    employee_id BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);
```

Here:

```text
employee_id
```

is the primary key.

`email` may also represent a candidate key if the domain guarantees uniqueness.

______________________________________________________________________

# 16. Candidate Key vs Primary Key

The distinction:

```text
Candidate keys
      ↓
Possible unique identifiers
      ↓
Choose one
      ↓
Primary key
```

A candidate key is a conceptual/design property.

A primary key is the chosen key enforced/designated as the table's primary identifier.

______________________________________________________________________

# 17. Natural vs Surrogate Keys

A natural key has business meaning.

Example:

```text
email
```

A surrogate key is an artificial identifier.

Example:

```text
customer_id = 12345
```

Both can be valid.

The decision depends on:

- Stability
- Uniqueness
- Domain semantics
- Key size
- External integrations
- Privacy
- Data lifecycle

______________________________________________________________________

# 18. What Makes a Good Primary Key?

A practical primary key should generally be:

- Unique
- Stable
- Non-null
- Predictable in behavior
- Appropriate for indexing
- Suitable for relationships

Do not assume every business attribute makes a good primary key.

______________________________________________________________________

# 19. First Normal Form — 1NF

1NF generally requires:

- Atomic values.
- No repeating groups.
- Each row represents a distinct record.

Bad:

```text
user_id | phone_numbers
1       | 111,222,333
```

Better:

```text
user_phones
----------------
user_id
phone_number
```

Each phone number becomes a separate row.

______________________________________________________________________

# 20. What Does Atomic Mean?

Atomic does not simply mean:

> "The value is a string."

It means the column represents one value appropriate to the model rather than an uncontrolled collection of values
packed into one field.

For example:

```text
"111,222,333"
```

may be a string technically, but it represents multiple phone numbers.

That is generally a poor relational representation when the phone numbers need to be queried independently.

______________________________________________________________________

# 21. Second Normal Form — 2NF

2NF builds on 1NF.

A relation is in 2NF when non-key attributes depend on the **whole candidate key**, not just part of a composite key.

This matters primarily when the key contains multiple attributes.

______________________________________________________________________

# 22. 2NF Example

Consider:

```text
order_items
--------------------------------
order_id
product_id
product_name
quantity
```

Suppose:

```text
(order_id, product_id)
```

is the key.

Dependencies:

```text
(order_id, product_id) → quantity
product_id → product_name
```

`product_name` depends only on `product_id`, which is only part of the composite key.

That is a partial dependency.

______________________________________________________________________

# 23. Fixing the 2NF Example

Separate product information:

```text
products
----------------
product_id
product_name
```

and keep order-specific information:

```text
order_items
----------------
order_id
product_id
quantity
```

Now:

```text
product_id → product_name
(order_id, product_id) → quantity
```

The attributes are associated with the appropriate determinants.

______________________________________________________________________

# 24. Third Normal Form — 3NF

3NF builds on 2NF.

A common interview-friendly explanation is:

> Non-key attributes should depend on the key, the whole key, and nothing but the key.

More precisely, 3NF removes problematic transitive dependencies under the formal definition.

______________________________________________________________________

# 25. Transitive Dependency

Consider:

```text
employees
--------------------------------
employee_id
department_id
department_name
```

Dependencies:

```text
employee_id → department_id
department_id → department_name
```

Therefore:

```text
employee_id → department_name
```

through `department_id`.

`department_name` is transitively dependent on `employee_id`.

______________________________________________________________________

# 26. Fixing the 3NF Example

Separate department information:

```text
departments
----------------
department_id
department_name
```

and:

```text
employees
----------------
employee_id
department_id
```

Now department details are stored once.

______________________________________________________________________

# 27. 1NF → 2NF → 3NF

A useful interview progression:

```text
1NF
 ↓
Atomic values / no repeating groups

2NF
 ↓
No partial dependency on a composite key

3NF
 ↓
No problematic transitive dependency
```

Do not memorize this without understanding the examples.

______________________________________________________________________

# 28. BCNF Overview

Boyce-Codd Normal Form (BCNF) is stricter than 3NF.

At a high level:

> Every determinant must be a candidate key.

BCNF addresses certain dependency structures that can still exist in a relation satisfying 3NF.

For most backend interviews, an overview is sufficient unless the role specifically emphasizes database theory.

______________________________________________________________________

# 29. Why BCNF Matters

3NF can allow some dependency structures that BCNF would decompose further.

The important interview takeaway is:

```text
BCNF > stricter than 3NF
```

and:

```text
Every determinant should be a candidate key
```

under the standard BCNF formulation.

______________________________________________________________________

# 30. Normalization Example — E-Commerce

Suppose we start with:

```text
orders
--------------------------------------------------------
order_id
customer_id
customer_name
customer_email
product_id
product_name
product_price
quantity
```

There is significant duplication.

Customer and product information are repeated across order items.

______________________________________________________________________

# 31. Step 1 — Identify Entities

Potential entities:

```text
customers
products
orders
order_items
```

This gives us natural boundaries.

______________________________________________________________________

# 32. Step 2 — Customer Table

Create:

```text
customers
-----------------------------
customer_id
customer_name
customer_email
```

Customer attributes now have one primary location.

______________________________________________________________________

# 33. Step 3 — Product Table

Create:

```text
products
-----------------------------
product_id
product_name
current_price
```

Product attributes are separated from order-specific data.

______________________________________________________________________

# 34. Step 4 — Order Table

Create:

```text
orders
-----------------------------
order_id
customer_id
created_at
status
```

An order belongs to a customer.

______________________________________________________________________

# 35. Step 5 — Order Items

Create:

```text
order_items
-----------------------------
order_id
product_id
quantity
unit_price
```

The relationship between orders and products is represented explicitly.

______________________________________________________________________

# 36. Why Store `unit_price` in Order Items?

A common interview question:

> If product price exists in `products`, why store `unit_price` in `order_items`?

Because an order usually needs a historical snapshot of the price used for that purchase.

For example:

```text
Current product price = ₹1200
Historical order price = ₹999
```

The order should not change merely because the current catalog price changes.

This is not careless redundancy.

It represents a different business fact:

```text
products.current_price
vs
order_items.unit_price
```

______________________________________________________________________

# 37. Normalization Does Not Mean "Never Duplicate Data"

This is an important senior-level distinction.

Duplication can be acceptable when two columns represent different facts.

Example:

```text
products.current_price
order_items.unit_price
```

These values may legitimately differ because they describe different points in time/business contexts.

The goal is not to eliminate every repeated value.

The goal is to avoid **unnecessary and ambiguous duplication**.

______________________________________________________________________

# 38. Normalization and Referential Integrity

Normalized designs commonly use foreign keys.

Example:

```sql
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    FOREIGN KEY (customer_id)
        REFERENCES customers(id)
);
```

This ensures the relationship points to a valid customer according to the database's constraint semantics.

______________________________________________________________________

# 39. Normalization and Constraints

Normalization works together with:

- Primary keys
- Foreign keys
- Unique constraints
- `NOT NULL`
- `CHECK` constraints

A well-designed schema expresses important domain rules at the database level where appropriate.

______________________________________________________________________

# 40. Normalization and Indexes

Normalization and indexing solve different problems.

### Normalization

Focuses on:

- Data structure
- Redundancy
- Dependencies
- Integrity

### Indexing

Focuses primarily on:

- Data access performance

A normalized database can still need carefully chosen indexes.

______________________________________________________________________

# 41. Normalization vs Performance

A normalized schema may require joins.

Joins are not inherently bad.

Modern relational databases are designed to perform joins efficiently when the schema, indexes, statistics and queries
are appropriate.

Do not denormalize simply because:

> "Joins are slow."

Measure first.

______________________________________________________________________

# 42. When to Denormalize

Denormalization may be appropriate when:

- A measured read bottleneck exists.
- A high-volume query repeatedly performs expensive joins.
- Precomputed data materially improves latency.
- Reporting workloads need specialized structures.
- A read-heavy access pattern justifies controlled duplication.

Denormalization should be deliberate.

______________________________________________________________________

# 43. Denormalization Trade-Off

Benefits:

- Faster reads in some workloads
- Fewer joins
- Precomputed values
- Simplified read paths

Costs:

- More storage
- More complicated writes
- Synchronization concerns
- Potential stale data
- More complex consistency rules

______________________________________________________________________

# 44. Read Model vs Write Model

Some systems intentionally maintain different representations for different access patterns.

Conceptually:

```text
Normalized write model
        ↓
Events / processing
        ↓
Denormalized read model
```

This can be useful for high-scale or reporting workloads.

You do not need full CQRS knowledge for this topic, but understand the trade-off.

______________________________________________________________________

# 45. Real-World Example — User Address

Suppose a user has:

```text
current_address
```

and orders need to preserve the shipping address at purchase time.

You may have:

```text
users
current_address_id
```

and separately:

```text
orders
shipping_address_snapshot
```

The snapshot is intentionally duplicated because it represents historical state.

This is a business requirement, not necessarily a normalization failure.

______________________________________________________________________

# 46. Schema Design Questions

When designing a table, ask:

1. What entity does this table represent?
1. What uniquely identifies a row?
1. What attributes belong to the entity?
1. What determines each attribute?
1. Which relationships exist?
1. Which values are duplicated?
1. Can duplication create anomalies?
1. Which constraints should be enforced?
1. What queries will the backend execute?
1. What are the expected read/write patterns?

______________________________________________________________________

# 47. Functional Dependencies in Interviews

If asked to normalize a table:

### Step 1

Identify candidate keys.

### Step 2

List important functional dependencies.

### Step 3

Check for repeating/non-atomic values.

### Step 4

Check partial dependencies.

### Step 5

Check transitive dependencies.

### Step 6

Decompose tables while preserving necessary relationships and constraints.

______________________________________________________________________

# 48. Dependency Example

Suppose:

```text
student_id
course_id
student_name
course_name
grade
```

with key:

```text
(student_id, course_id)
```

Dependencies:

```text
student_id → student_name
course_id → course_name
(student_id, course_id) → grade
```

This shows why student and course information should be separated from enrollment-specific information.

______________________________________________________________________

# 49. Resulting Design

Use:

```text
students
----------------
student_id
student_name
```

```text
courses
----------------
course_id
course_name
```

```text
enrollments
----------------
student_id
course_id
grade
```

This is a classic normalization exercise.

______________________________________________________________________

# 50. Lossless Decomposition — Overview

When decomposing a table, you want to be able to reconstruct the meaningful original relationships through joins without
introducing incorrect information.

This is called a **lossless decomposition**.

For a backend interview, understand the concept rather than diving deeply into formal proofs unless the role requires
database theory.

______________________________________________________________________

# 51. Dependency Preservation — Overview

A good decomposition should ideally allow important functional dependencies to be enforced without reconstructing the
original table every time.

This is called **dependency preservation**.

These are useful concepts when discussing formal normalization.

______________________________________________________________________

# 52. Normalization in Production

Production database design is not purely a normalization exercise.

You also need to consider:

- Query patterns
- Traffic volume
- Write frequency
- Data lifecycle
- Historical requirements
- Indexes
- Transaction boundaries
- Operational complexity
- Reporting requirements

A theoretically elegant schema can still be a poor production design if it does not support the actual workload.

______________________________________________________________________

# 53. OLTP vs Reporting

Transactional systems often favor normalized schemas.

Reporting/analytical workloads may favor:

- Denormalized structures
- Aggregated tables
- Materialized views
- Specialized analytical models

The correct design depends on workload.

______________________________________________________________________

# 54. Normalization Decision Framework

Use:

```text
Understand domain
      ↓
Identify entities
      ↓
Identify keys
      ↓
Identify dependencies
      ↓
Normalize
      ↓
Add constraints
      ↓
Analyze query patterns
      ↓
Add indexes
      ↓
Measure performance
      ↓
Denormalize only when justified
```

This is a strong senior-level answer because it balances correctness and performance.

______________________________________________________________________

# 55. Common Database Design Mistakes

## Mistake 1 — Storing lists in a single column

Example:

```text
"python,fastapi,sql"
```

when those values need independent querying.

## Mistake 2 — Repeating entity attributes everywhere

This creates update anomalies.

## Mistake 3 — No primary key

Every important relational entity should have a deliberate identity strategy.

## Mistake 4 — No foreign keys where integrity matters

Relationships can become invalid.

## Mistake 5 — Over-normalization

Excessive decomposition can make simple application queries unnecessarily complex.

## Mistake 6 — Premature denormalization

Do not duplicate data just because you expect joins to be slow.

## Mistake 7 — Confusing historical snapshots with bad redundancy

Historical facts may intentionally duplicate current entity information.

______________________________________________________________________

# 56. Interview Questions & Answers

## Q1. What is database normalization?

**Answer:**

Normalization is a method of structuring relational data to reduce unnecessary redundancy and prevent anomalies while
representing dependencies appropriately.

______________________________________________________________________

## Q2. Why do we normalize databases?

**Answer:**

To reduce unnecessary duplication, improve consistency and prevent insert, update and delete anomalies.

______________________________________________________________________

## Q3. What is redundancy?

**Answer:**

Redundancy is storing the same logical fact in multiple places.

It can cause inconsistent values and unnecessary update work.

______________________________________________________________________

## Q4. What is an insert anomaly?

**Answer:**

A situation where inserting one fact requires unrelated information or is impossible because multiple independent facts
were combined into one table.

______________________________________________________________________

## Q5. What is an update anomaly?

**Answer:**

When the same logical fact is stored in multiple rows and updating it requires modifying multiple locations, creating a
risk of inconsistency.

______________________________________________________________________

## Q6. What is a delete anomaly?

**Answer:**

When deleting one fact unintentionally removes another fact that should remain because both were stored in the same
structure.

______________________________________________________________________

## Q7. What is a functional dependency?

**Answer:**

A dependency where one attribute or set of attributes determines another.

For example:

```text
employee_id → employee_name
```

______________________________________________________________________

## Q8. What is a candidate key?

**Answer:**

A minimal set of attributes that uniquely identifies a row.

______________________________________________________________________

## Q9. Candidate key vs primary key?

**Answer:**

A table can have multiple candidate keys.

The primary key is the candidate key selected as the table's primary identifier.

______________________________________________________________________

## Q10. What is a surrogate key?

**Answer:**

An artificial identifier with no direct business meaning, such as an auto-generated numeric ID or UUID.

______________________________________________________________________

## Q11. What is 1NF?

**Answer:**

At a practical level, 1NF requires atomic values and avoids repeating groups.

______________________________________________________________________

## Q12. What is 2NF?

**Answer:**

2NF requires 1NF and removes partial dependencies of non-key attributes on part of a composite candidate key.

______________________________________________________________________

## Q13. What is 3NF?

**Answer:**

3NF requires 2NF and removes problematic transitive dependencies among non-key attributes.

______________________________________________________________________

## Q14. What is BCNF?

**Answer:**

BCNF is stricter than 3NF and, under its standard formulation, requires every determinant to be a candidate key.

______________________________________________________________________

## Q15. Does 2NF matter if the table has a single-column key?

**Answer:**

Partial dependency on part of a key cannot occur when the key has only one attribute.

Therefore, 2NF concerns are primarily relevant to composite keys.

______________________________________________________________________

## Q16. Give a simple 2NF example.

**Answer:**

If `(order_id, product_id)` is the key and:

```text
product_id → product_name
```

then `product_name` depends on only part of the composite key.

Move product information to a product table.

______________________________________________________________________

## Q17. Give a simple 3NF example.

**Answer:**

If:

```text
employee_id → department_id
department_id → department_name
```

then `department_name` transitively depends on `employee_id`.

Move department details to a separate department table.

______________________________________________________________________

## Q18. Does normalization eliminate all duplicate values?

**Answer:**

No.

It eliminates unnecessary redundancy.

A historical `unit_price` in an order item can intentionally differ from the current product price because they
represent different business facts.

______________________________________________________________________

## Q19. Normalization vs denormalization?

**Answer:**

Normalization reduces unnecessary redundancy and anomalies.

Denormalization deliberately introduces redundancy to improve certain read or operational characteristics.

______________________________________________________________________

## Q20. When would you denormalize?

**Answer:**

After identifying and measuring a real workload bottleneck where reducing joins or precomputing data provides meaningful
benefit.

______________________________________________________________________

## Q21. Is denormalization always faster?

**Answer:**

No.

It may improve particular reads, but it increases write complexity and consistency requirements.

Measure the actual workload.

______________________________________________________________________

## Q22. Why not put everything into one table?

**Answer:**

It creates redundancy, update anomalies, poor data ownership and difficult integrity management.

______________________________________________________________________

## Q23. Why not split every attribute into its own table?

**Answer:**

Over-normalization can make common queries unnecessarily complex and increase join overhead and application complexity.

Database design is a balance.

______________________________________________________________________

## Q24. What is lossless decomposition?

**Answer:**

A decomposition where the original meaningful relation can be reconstructed through appropriate joins without
introducing spurious information.

______________________________________________________________________

## Q25. What is dependency preservation?

**Answer:**

A decomposition is dependency-preserving when important functional dependencies can be enforced using the decomposed
relations without needing to reconstruct the original relation.

______________________________________________________________________

## Q26. Why are foreign keys important in a normalized schema?

**Answer:**

They can enforce referential integrity between related entities.

______________________________________________________________________

## Q27. Normalization vs indexing?

**Answer:**

Normalization primarily addresses data structure, redundancy and integrity.

Indexing primarily improves suitable data-access patterns.

They solve different problems and are often used together.

______________________________________________________________________

## Q28. Does normalization make joins bad?

**Answer:**

No.

Joins are fundamental to relational databases.

A properly indexed normalized schema can support efficient joins.

______________________________________________________________________

## Q29. Why store order item price if product has a price?

**Answer:**

Because the order needs the historical price at purchase time.

Current catalog price and historical transaction price represent different facts.

______________________________________________________________________

## Q30. Why store a shipping-address snapshot?

**Answer:**

An order needs to preserve the address used for that historical shipment even if the user's current address changes.

______________________________________________________________________

## Q31. What is the first thing you identify when designing a table?

**Answer:**

The entity or concept the table represents and what uniquely identifies each row.

______________________________________________________________________

## Q32. How do functional dependencies help database design?

**Answer:**

They show which attributes depend on which determinants, helping identify incorrect grouping and normalization
opportunities.

______________________________________________________________________

## Q33. What is a natural key?

**Answer:**

A key derived from a meaningful business attribute, such as an externally defined identifier.

______________________________________________________________________

## Q34. What is a surrogate key?

**Answer:**

An artificial identifier created specifically to identify a row, such as an integer ID or UUID.

______________________________________________________________________

## Q35. Should email always be a primary key for users?

**Answer:**

Not necessarily.

Email can be unique without being the primary key.

Its suitability depends on whether the business guarantees uniqueness, stability and the desired semantics.

______________________________________________________________________

## Q36. What is a many-to-many relationship?

**Answer:**

A relationship where multiple rows in one entity can relate to multiple rows in another.

It is commonly represented using an association/junction table.

______________________________________________________________________

## Q37. How do you normalize a table in an interview?

**Answer:**

Identify the entities, candidate keys and functional dependencies, then remove repeating groups, partial dependencies
and transitive dependencies while preserving the required relationships.

______________________________________________________________________

## Q38. What is over-normalization?

**Answer:**

Decomposing data beyond what is practical for the application's workload, potentially creating unnecessary joins and
complexity.

______________________________________________________________________

## Q39. What should influence production schema design besides normalization?

**Answer:**

Query patterns, traffic, read/write ratio, indexing, historical requirements, transaction boundaries, operational
complexity and reporting needs.

______________________________________________________________________

## Q40. What is the senior-level view of normalization?

**Answer:**

Start with a logically sound normalized model, enforce important integrity rules, understand access patterns, measure
performance and introduce deliberate denormalization only when the workload justifies its consistency and maintenance
cost.

______________________________________________________________________

# 57. Scenario-Based Questions

## Scenario 1 — Repeated Customer Data

You have:

```text
orders
------------------------------------------------
order_id
customer_id
customer_name
customer_email
```

There are one million orders.

**Question:** What would you change?

**Answer:**

Move customer attributes into a `customers` table and keep `customer_id` as a foreign key in `orders`, assuming the
attributes represent the customer's current state.

Historical snapshots should remain separate when the business requires them.

______________________________________________________________________

## Scenario 2 — Order Price

A developer removes `unit_price` from `order_items` because `products` already has `price`.

**Question:** Is this necessarily correct?

**Answer:**

No.

An order needs the price actually charged at purchase time.

Current product price and historical transaction price represent different facts.

______________________________________________________________________

## Scenario 3 — Student Courses

A table contains:

```text
student_id
student_name
course_id
course_name
grade
```

with:

```text
(student_id, course_id)
```

as the key.

**Question:** Normalize it.

**Answer:**

Create:

```text
students(student_id, student_name)
courses(course_id, course_name)
enrollments(student_id, course_id, grade)
```

This removes partial dependencies.

______________________________________________________________________

## Scenario 4 — Department Data

A table contains:

```text
employee_id
employee_name
department_id
department_name
```

**Question:** What dependency should you identify?

**Answer:**

Likely:

```text
employee_id → department_id
department_id → department_name
```

This indicates a transitive dependency.

Separate department information.

______________________________________________________________________

## Scenario 5 — Comma-Separated Tags

A table stores:

```text
post_id | tags
1       | python,backend,api
```

**Question:** Is this normalized?

**Answer:**

If tags need to be queried, indexed or managed independently, storing them as a comma-separated string is generally not
a good relational design.

Use appropriate tag and association tables.

______________________________________________________________________

## Scenario 6 — Performance Complaint

A developer says:

> "The normalized schema has too many joins, so let's duplicate everything."

**Question:** How would you respond?

**Answer:**

First measure the actual bottleneck.

Check query plans, indexes, query frequency and result sizes.

Then consider targeted denormalization only where it provides a measurable benefit.

______________________________________________________________________

## Scenario 7 — Current vs Historical Address

A user's current address changes after an order is placed.

**Question:** Should the old order show the new address?

**Answer:**

Usually no.

The order should preserve the shipping address relevant to that historical transaction.

That may require an intentional address snapshot.

______________________________________________________________________

## Scenario 8 — Candidate Keys

A table has:

```text
employee_id
email
phone
```

and all three are guaranteed unique.

**Question:** Can there be multiple candidate keys?

**Answer:**

Yes.

Each minimal unique attribute set can be a candidate key.

One is selected as the primary key.

______________________________________________________________________

## Scenario 9 — Delete Anomaly

A course exists only in a row that also represents a student's enrollment.

**Question:** What happens when the student leaves?

**Answer:**

Deleting the enrollment could accidentally remove the only representation of the course.

Separating course and enrollment entities prevents this anomaly.

______________________________________________________________________

## Scenario 10 — Denormalized Read Model

A service has a very high-volume dashboard query requiring expensive joins across many tables.

**Question:** Could denormalization be appropriate?

**Answer:**

Yes, if measurement shows the query is a real bottleneck.

A precomputed or denormalized read model may reduce latency, but the team must define how and when it stays consistent.

______________________________________________________________________

# 58. Practice Exercises

## Exercise 1 — Identify Anomalies

Given:

```text
student_id
student_name
course_id
course_name
instructor_name
grade
```

identify potential:

- Insert anomaly
- Update anomaly
- Delete anomaly

Explain each.

______________________________________________________________________

## Exercise 2 — Functional Dependencies

For:

```text
employee_id
employee_name
department_id
department_name
```

write the likely functional dependencies.

Then identify the transitive dependency.

______________________________________________________________________

## Exercise 3 — Normalize to 3NF

Normalize:

```text
order_id
customer_id
customer_name
customer_email
product_id
product_name
quantity
unit_price
```

into an appropriate set of tables.

______________________________________________________________________

## Exercise 4 — Composite Key

Design:

```text
students
courses
enrollments
```

where a student can take multiple courses and a course can contain multiple students.

Identify:

- Candidate keys
- Primary keys
- Foreign keys

______________________________________________________________________

## Exercise 5 — 1NF

Convert:

```text
user_id | phone_numbers
1       | 111,222,333
```

into a relational representation where phone numbers can be queried independently.

______________________________________________________________________

## Exercise 6 — 2NF

Take:

```text
order_items
order_id
product_id
product_name
quantity
```

Assume `(order_id, product_id)` is the key.

Explain the partial dependency and normalize it.

______________________________________________________________________

## Exercise 7 — 3NF

Take:

```text
employees
employee_id
department_id
department_name
```

Explain the transitive dependency and normalize it.

______________________________________________________________________

## Exercise 8 — Denormalization Decision

Design a normalized schema for a dashboard.

Then identify one query that could potentially benefit from a denormalized read model.

Explain:

- Why
- What you would duplicate
- How consistency would be maintained

______________________________________________________________________

## Exercise 9 — Historical Data

Design an order schema where:

- Product price can change.
- Customer address can change.
- Orders must preserve historical purchase information.

Explain which values should be snapshots and why.

______________________________________________________________________

## Exercise 10 — Schema Review

Review a table with:

```text
user_id
user_name
user_email
order_id
order_total
product_ids
product_names
```

Identify design problems and propose a normalized model.

______________________________________________________________________

# 59. Quick Revision

| Concept | Key Point |
|---|---|
| Database design | Structuring data/entities/relationships for the domain |
| Entity | Meaningful domain concept |
| Relationship | Association between entities |
| Redundancy | Repeated logical information |
| Insert anomaly | Cannot insert one fact without unrelated data |
| Update anomaly | Same fact must be updated in multiple places |
| Delete anomaly | Deleting one fact removes another |
| Functional dependency | One attribute set determines another |
| Candidate key | Minimal unique identifier |
| Primary key | Selected candidate key |
| Natural key | Business-meaningful key |
| Surrogate key | Artificial identifier |
| 1NF | Atomic values/no repeating groups |
| 2NF | No partial dependency on composite key |
| 3NF | No problematic transitive dependency |
| BCNF | Every determinant is a candidate key |
| Normalization | Reduces unnecessary redundancy/anomalies |
| Denormalization | Deliberate redundancy for workload needs |
| Lossless decomposition | Decomposition without spurious reconstruction |
| Dependency preservation | Important dependencies remain enforceable |
| Foreign key | Enforces/represents relationship |
| Historical snapshot | Intentional copy preserving past state |
| Over-normalization | Excessive decomposition |
| Read model | Representation optimized for reading |
| OLTP | Transaction-oriented workload |
| Reporting | Often favors specialized/denormalized structures |

______________________________________________________________________

# 60. Completion Checklist

Before moving to File 20, make sure you can explain:

- [ ] Database design fundamentals
- [ ] Entities
- [ ] Attributes
- [ ] Relationships
- [ ] One-to-one
- [ ] One-to-many
- [ ] Many-to-many
- [ ] Redundancy
- [ ] Insert anomaly
- [ ] Update anomaly
- [ ] Delete anomaly
- [ ] Functional dependencies
- [ ] Candidate keys
- [ ] Primary keys
- [ ] Natural keys
- [ ] Surrogate keys
- [ ] 1NF
- [ ] Atomic values
- [ ] 2NF
- [ ] Partial dependency
- [ ] 3NF
- [ ] Transitive dependency
- [ ] BCNF overview
- [ ] Normalization examples
- [ ] Referential integrity
- [ ] Constraints
- [ ] Normalization vs indexing
- [ ] Normalization vs performance
- [ ] Denormalization
- [ ] When to denormalize
- [ ] Historical snapshots
- [ ] Read models
- [ ] OLTP vs reporting
- [ ] Lossless decomposition overview
- [ ] Dependency preservation overview
- [ ] Production schema trade-offs
- [ ] Common database design mistakes

______________________________________________________________________

# 61. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is database normalization?
1. Why do we normalize databases?
1. What is redundancy?
1. What is an insert anomaly?
1. What is an update anomaly?
1. What is a delete anomaly?
1. Give a real-world example of an update anomaly.
1. What is a functional dependency?
1. Explain `A → B`.
1. What is a candidate key?
1. Candidate key vs primary key?
1. What is a natural key?
1. What is a surrogate key?
1. What makes a good primary key?
1. What is 1NF?
1. What does atomic value mean?
1. What is 2NF?
1. Why are composite keys relevant to 2NF?
1. Give a 2NF example.
1. What is 3NF?
1. What is a transitive dependency?
1. Give a 3NF example.
1. What is BCNF?
1. How is BCNF stricter than 3NF?
1. Does normalization eliminate all duplicate values?
1. Why can order price intentionally duplicate product price?
1. What is normalization vs denormalization?
1. When would you denormalize?
1. Is denormalization always faster?
1. What are the costs of denormalization?
1. What is over-normalization?
1. What is a lossless decomposition?
1. What is dependency preservation?
1. Why are foreign keys important?
1. How do normalization and indexing differ?
1. Does normalization make joins bad?
1. How would you normalize an e-commerce order schema?
1. How would you model many-to-many relationships?
1. How would you preserve historical shipping addresses?
1. How would you decide whether to denormalize a production schema?
1. A table contains comma-separated product IDs. What would you change?
1. A customer name is repeated across millions of orders. What problem can this create?
1. A dashboard query requires six joins and is slow. What would you investigate before denormalizing?
1. How do functional dependencies help you identify table boundaries?
1. Explain 1NF, 2NF and 3NF using one practical example.
1. Why is a historical snapshot not necessarily a normalization violation?
1. What is the difference between current state and historical state?
1. How would you review a database schema for a Python backend?
1. What factors besides normalization influence production database design?
1. Give a senior-level answer to: "Should we normalize everything?"

If you can answer these confidently and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [18. SQL Fundamentals](./18-sql-fundamentals.md)

**Next:** [20. Advanced SQL Queries](./20-sql-advanced.md)

# 24. SQLAlchemy Performance & Async

**Previous:** [23. SQLAlchemy ORM](./23-sqlalchemy-core.md)

**Next:** [25. Database Scaling](./25-database-scaling.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain lazy loading and eager loading.
- Identify and fix the N+1 query problem.
- Explain `joinedload()` and `selectinload()`.
- Choose an appropriate relationship-loading strategy.
- Understand Async SQLAlchemy and `AsyncSession`.
- Explain connection pooling in synchronous and asynchronous applications.
- Compare ORM queries with raw SQL.
- Diagnose common ORM performance problems.
- Optimize database access in a FastAPI application.
- Explain the trade-offs involved in ORM performance decisions.

> **Scope note:** This topic builds on File 23. File 23 covers the SQLAlchemy ORM fundamentals, Session, identity map, unit of work, CRUD, transactions and connection pooling. This file focuses specifically on performance, relationship loading and async SQLAlchemy.

______________________________________________________________________

# 1. Why SQLAlchemy Performance Matters

SQLAlchemy provides a convenient abstraction over relational databases, but ORM code can hide expensive database
operations.

A Python operation such as:

```python
user.orders
```

may result in an additional SQL query.

Therefore:

> ORM code should always be evaluated in terms of the SQL and database work it produces.

______________________________________________________________________

# 2. The Performance Stack

Database performance in a Python backend can be affected by:

```text
FastAPI
  ↓
Application code
  ↓
SQLAlchemy
  ↓
Connection pool
  ↓
Database driver
  ↓
Network
  ↓
Database
```

A slow endpoint is not necessarily caused by SQL itself.

Possible bottlenecks include:

- Too many queries
- Slow queries
- Connection-pool waits
- Network latency
- Serialization
- Excessive application processing

______________________________________________________________________

# 3. Query Count Matters

Consider:

```text
1 request
 ↓
1 query
```

versus:

```text
1 request
 ↓
1 query
 ↓
100 additional queries
```

Even if each individual query is fast, hundreds of database round trips can significantly increase request latency.

This is one reason the N+1 problem is important.

______________________________________________________________________

# 4. Lazy Loading

Lazy loading means a relationship is loaded when it is accessed.

Example:

```python
user = session.get(User, user_id)

orders = user.orders
```

The initial query may load the user:

```sql
SELECT ...
FROM users
WHERE id = ?;
```

Accessing:

```python
user.orders
```

may then trigger another query.

______________________________________________________________________

# 5. Why Lazy Loading Is Convenient

Lazy loading is convenient because related data is retrieved only when needed.

Example:

```python
user = session.get(User, 1)

print(user.email)
```

If orders are never accessed, there may be no need to query them.

This can avoid unnecessary work.

______________________________________________________________________

# 6. The Cost of Lazy Loading

The problem occurs when lazy loading happens repeatedly.

For example:

```python
users = session.scalars(
    select(User)
).all()

for user in users:
    print(user.orders)
```

This can produce:

```text
1 query for users
+
1 query per user
```

That is the N+1 query pattern.

______________________________________________________________________

# 7. N+1 Query Problem

Suppose there are 500 users.

The application performs:

```text
1 query → users

500 queries → orders for each user
```

Total:

```text
501 queries
```

The database may spend much more time handling round trips than necessary.

______________________________________________________________________

# 8. Why N+1 Is Dangerous

N+1 can cause:

- Higher latency
- More database connections/work
- Increased database CPU
- Higher network overhead
- Poor scalability
- Connection-pool pressure

It may remain unnoticed with small development datasets and become severe in production.

______________________________________________________________________

# 9. Detecting N+1

Useful approaches include:

- Enable SQL logging in development.
- Inspect generated SQL.
- Count SQL statements per request.
- Use application tracing.
- Monitor database query metrics.
- Review ORM relationship access patterns.

The first question should often be:

> "How many SQL statements does this endpoint execute?"

______________________________________________________________________

# 10. Eager Loading

Eager loading retrieves related data as part of the planned database access rather than waiting until the relationship
is accessed.

SQLAlchemy provides multiple eager-loading strategies.

Two important ones are:

```python
joinedload()
selectinload()
```

______________________________________________________________________

# 11. `joinedload()`

`joinedload()` loads related objects using a SQL join strategy.

Example:

```python
from sqlalchemy.orm import joinedload

stmt = (
    select(User)
    .options(joinedload(User.orders))
)
```

Conceptually:

```text
users
  JOIN
orders
```

The exact SQL generated depends on the relationship and query.

______________________________________________________________________

# 12. When `joinedload()` Can Be Useful

`joinedload()` can be useful when:

- The relationship is relatively small.
- Related data is needed immediately.
- A join is efficient for the query.
- You want to load related data in the same database round trip.

______________________________________________________________________

# 13. `joinedload()` and One-to-Many Relationships

Suppose:

```text
User
 ├── Order 1
 ├── Order 2
 └── Order 3
```

A join can produce multiple result rows for the same user.

Conceptually:

```text
User 1 | Order 1
User 1 | Order 2
User 1 | Order 3
```

SQLAlchemy must reconstruct the ORM object graph.

This can increase the size of the result set.

______________________________________________________________________

# 14. `unique()` With Joined Collection Loading

When using joined eager loading against a collection, SQLAlchemy can require result de-duplication.

For example:

```python
result = session.execute(
    select(User).options(joinedload(User.orders))
)

users = result.unique().scalars().all()
```

The exact result-processing API depends on how the query is executed.

The important interview concept is:

> A SQL join can produce duplicate parent rows when loading collections.

______________________________________________________________________

# 15. `selectinload()`

`selectinload()` loads related rows using a separate query that uses the parent identities.

Example:

```python
from sqlalchemy.orm import selectinload

stmt = (
    select(User)
    .options(selectinload(User.orders))
)
```

Conceptually:

```text
Query 1:
users

Query 2:
orders WHERE user_id IN (...)
```

______________________________________________________________________

# 16. Why `selectinload()` Helps

Instead of:

```text
1 + N queries
```

you can often get:

```text
2 queries
```

for the parent collection and its related collection.

This can significantly reduce query count.

______________________________________________________________________

# 17. `joinedload()` vs `selectinload()`

| | `joinedload()` | `selectinload()` |
|---|---|---|
| Main strategy | Join | Additional SELECT |
| Round trips | Often fewer | Usually multiple |
| Parent duplication | Possible with collections | Avoids join row multiplication |
| Large collections | Can become expensive | Often a good choice |
| Simple many-to-one | Often useful | Also possible |
| One-to-many | Depends on result size | Frequently useful |

There is no universal winner.

______________________________________________________________________

# 18. Choosing Between Them

Consider:

### `joinedload()`

Useful when:

```text
Small relationship
+
Need related data
+
Join result remains manageable
```

### `selectinload()`

Useful when:

```text
Collection relationship
+
Many related rows
+
Avoiding large joined result sets
```

Always measure with realistic data.

______________________________________________________________________

# 19. Lazy vs Eager Loading

| Strategy | Advantage | Risk |
|---|---|---|
| Lazy | Loads only when needed | N+1 queries |
| Joined eager | Single joined query | Row multiplication |
| Select-in eager | Avoids N+1 without huge join | Additional query |

The right choice depends on the access pattern.

______________________________________________________________________

# 20. Relationship Loading Is Query Design

Do not choose loading strategy simply because:

> "`selectinload` is faster."

Instead ask:

- What data does the endpoint need?
- How many parent rows are returned?
- How many related rows exist?
- What SQL is generated?
- How large is the result?
- How many database round trips occur?

______________________________________________________________________

# 21. Nested Eager Loading

Relationships can be loaded through multiple levels.

For example:

```text
User
 ↓
Orders
 ↓
Items
```

The query options can be composed to load the required object graph.

But avoid eagerly loading large graphs without a clear requirement.

______________________________________________________________________

# 22. Over-Eager Loading

Loading everything can be as problematic as loading too little.

For example:

```text
User
 ├── Orders
 │    ├── Items
 │    │    ├── Product
 │    │    └── Category
 │    └── Payments
 └── Addresses
```

Loading this entire graph for every request can generate:

- Large SQL
- Large result sets
- High memory usage
- Unnecessary database work

Load only what the endpoint actually needs.

______________________________________________________________________

# 23. Select Only Required Columns

Avoid unnecessarily retrieving large objects.

Instead of:

```python
select(User)
```

when you only need:

```text
id
email
```

consider selecting only the required data.

This can reduce:

- Database I/O
- Network transfer
- Python object creation
- Serialization work

______________________________________________________________________

# 24. ORM vs Raw SQL

SQLAlchemy ORM is useful for:

- Domain models
- CRUD
- Relationships
- Unit-of-work behavior
- Maintainability

Raw SQL can be useful when:

- The query is highly specialized.
- Complex database features are needed.
- You need precise SQL control.
- ORM abstraction makes the query harder to express.
- Performance testing demonstrates a meaningful advantage.

______________________________________________________________________

# 25. ORM Does Not Mean Slow

It is incorrect to say:

> "ORM is always slower than raw SQL."

A well-designed ORM query can generate efficient SQL.

Performance depends on:

- Generated SQL
- Query plan
- Number of round trips
- Amount of data
- Database indexes
- Application processing

______________________________________________________________________

# 26. When Raw SQL Is Appropriate

Consider raw SQL when:

```text
Complex analytical query
+
Database-specific feature
+
ORM query becomes difficult to reason about
```

However, do not switch to raw SQL just because a query is slow.

First inspect:

```text
Generated SQL
+
Execution plan
+
Query count
+
Data volume
```

______________________________________________________________________

# 27. SQLAlchemy Async

SQLAlchemy provides asynchronous APIs for applications using Python's async execution model.

Common components include:

```python
AsyncEngine
AsyncSession
```

Example:

```python
from sqlalchemy.ext.asyncio import AsyncSession

async with AsyncSession(engine) as session:
    ...
```

______________________________________________________________________

# 28. Async Engine

An async application should use an appropriate `AsyncEngine`.

Conceptually:

```text
FastAPI
   ↓
AsyncSession
   ↓
AsyncEngine
   ↓
Async database driver
   ↓
Database
```

The database driver must support the async integration being used.

______________________________________________________________________

# 29. AsyncSession

`AsyncSession` provides the ORM Session interface for asynchronous applications.

Example:

```python
async with AsyncSession(engine) as session:
    result = await session.execute(
        select(User)
    )

    users = result.scalars().all()
```

The exact driver and engine configuration depend on the database.

______________________________________________________________________

# 30. Async Is Not Automatically Faster

Async does not make database queries intrinsically faster.

Instead, async can improve concurrency when the application spends time waiting for I/O.

For example:

```text
Request A → waiting for DB
Request B → can make progress
Request C → can make progress
```

rather than blocking an entire execution resource unnecessarily.

______________________________________________________________________

# 31. Async Requires Async-Compatible Components

A common mistake is:

```text
async endpoint
     ↓
synchronous blocking database call
```

This can block the event loop.

For an async application, use an appropriate async SQLAlchemy stack and driver where asynchronous database access is
required.

______________________________________________________________________

# 32. Blocking Calls in Async Code

Avoid performing long blocking operations directly inside an async endpoint.

Examples:

```python
time.sleep(5)
```

or a synchronous blocking database call.

These can block the event loop.

Prefer async-compatible operations or explicitly isolate blocking work when appropriate.

______________________________________________________________________

# 33. Async Session Lifecycle

A common FastAPI pattern is:

```text
Request
 ↓
Create AsyncSession
 ↓
Database operations
 ↓
Commit / Rollback
 ↓
Close
 ↓
Response
```

The Session should have a clear request/unit-of-work lifecycle.

______________________________________________________________________

# 34. Async Session Is Not Globally Shared

Do not treat one `AsyncSession` as a globally shared object across concurrent requests/tasks.

Each concurrent unit of work should have an appropriate Session lifecycle.

Sharing stateful Sessions can lead to:

- Transaction conflicts
- Unexpected state
- Concurrency issues

______________________________________________________________________

# 35. Async SQLAlchemy Example

A simplified dependency:

```python
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session
```

An endpoint can then use the dependency:

```python
@app.get("/users")
async def get_users(
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(User)
    )

    return result.scalars().all()
```

The exact dependency and engine setup depends on the application.

______________________________________________________________________

# 36. Async Transactions

Async transactions can be managed with:

```python
async with session.begin():
    ...
```

Conceptually:

```text
Begin
 ↓
Async database work
 ↓
Commit
```

On failure:

```text
Rollback
```

The same transaction principles from File 22 still apply.

______________________________________________________________________

# 37. Async Commit

Example:

```python
async with AsyncSession(engine) as session:
    user = User(email="alice@example.com")

    session.add(user)

    await session.commit()
```

The async API uses `await` for asynchronous database operations.

______________________________________________________________________

# 38. Async Flush

Similarly:

```python
await session.flush()
```

flushes pending ORM changes through the async database stack.

Remember:

```text
flush ≠ commit
```

This distinction remains the same as synchronous SQLAlchemy.

______________________________________________________________________

# 39. Async Connection Pooling

Async engines can maintain pools of async-compatible database connections.

Conceptually:

```text
AsyncEngine
    ↓
Async Connection Pool
    ↓
Async DB connections
```

Pool sizing still matters.

______________________________________________________________________

# 40. Async Pool Exhaustion

If too many concurrent requests require connections:

```text
Requests
  ↓
Pool capacity exceeded
  ↓
Requests wait
```

This can increase latency.

Possible causes include:

- Slow queries
- Long transactions
- Too much concurrency
- Sessions held too long
- Pool configuration problems

______________________________________________________________________

# 41. Pool Size Is Not Request Count

Suppose:

```text
1,000 concurrent requests
10 DB connections
```

This does not mean all requests need a separate database connection simultaneously.

The pool controls database concurrency.

However, if many requests are actively performing database work at the same time, a small pool can become a bottleneck.

______________________________________________________________________

# 42. Connection Pooling and Database Capacity

Increasing the pool size indefinitely is not a solution.

A database has finite capacity.

Too many concurrent connections can cause:

- CPU pressure
- Memory pressure
- Lock contention
- Context switching
- Reduced throughput

Connection-pool sizing should consider the database's capacity and total application instances.

______________________________________________________________________

# 43. Multiple Application Instances

Suppose:

```text
10 application instances
```

and each has:

```text
pool_size = 20
```

The potential database connection count can be around:

```text
10 × 20 = 200
```

before considering overflow or other connections.

This is an important production scaling consideration.

______________________________________________________________________

# 44. Query Optimization Process

A reliable process is:

```text
Measure
  ↓
Count queries
  ↓
Inspect generated SQL
  ↓
Inspect execution plan
  ↓
Check indexes
  ↓
Check result size
  ↓
Optimize
  ↓
Measure again
```

Do not optimize based only on assumptions.

______________________________________________________________________

# 45. Query Count Optimization

Suppose an endpoint executes:

```text
101 queries
```

First ask:

> Can this be reduced to a small number of well-designed queries?

Fixing query count can produce a much larger improvement than micro-optimizing Python code.

______________________________________________________________________

# 46. Query Result Size

A query returning:

```text
10 rows
```

and a query returning:

```text
1,000,000 rows
```

have very different performance characteristics.

Check:

- Number of rows
- Number of columns
- Payload size
- Serialization time
- Memory usage

______________________________________________________________________

# 47. Pagination and SQLAlchemy

Never load an unbounded collection when the API only needs a page.

Prefer:

```python
select(Order).limit(50)
```

with an appropriate ordering and pagination strategy.

For very large datasets, consider keyset/cursor pagination as discussed in File 21.

______________________________________________________________________

# 48. Bulk Operations

For large data operations, issuing one ORM object operation at a time may be inefficient.

Consider appropriate SQLAlchemy bulk or Core/database-level operations when the workload requires them.

The trade-off is that some ORM behaviors such as normal object tracking may not apply in the same way.

______________________________________________________________________

# 49. ORM Object Construction Cost

ORM queries can create Python objects for each returned row.

For large result sets, this can increase:

- CPU usage
- Memory usage
- Garbage collection pressure

If the application only needs a small projection of data, selecting the required columns can be more efficient.

______________________________________________________________________

# 50. Streaming Large Results

For very large result sets, consider streaming or batched processing rather than loading everything into memory.

For example:

```text
Database
 ↓
Batch 1
 ↓
Process
 ↓
Batch 2
 ↓
Process
```

The exact SQLAlchemy API depends on synchronous/async usage and database driver capabilities.

______________________________________________________________________

# 51. FastAPI Integration

A common FastAPI architecture is:

```text
HTTP request
    ↓
FastAPI dependency
    ↓
Session
    ↓
Service
    ↓
SQLAlchemy
    ↓
Database
```

The Session dependency should have a predictable lifecycle.

______________________________________________________________________

# 52. FastAPI Session Dependency

For synchronous SQLAlchemy:

```python
def get_session():
    with Session(engine) as session:
        yield session
```

For async SQLAlchemy:

```python
async def get_session():
    async with AsyncSession(engine) as session:
        yield session
```

The application can then inject the appropriate Session into endpoints/services.

______________________________________________________________________

# 53. Transaction Ownership in FastAPI

A common pattern is:

```text
Request
 ↓
Session
 ↓
Service
 ↓
Database operations
 ↓
Commit
```

The exact location of commit should be deliberate.

Avoid having every repository function independently commit if several operations must be atomic.

______________________________________________________________________

# 54. FastAPI and Async Database Calls

If an endpoint is:

```python
async def endpoint(...):
```

and it performs asynchronous SQLAlchemy operations:

```python
await session.execute(...)
```

the event loop can continue handling other work while waiting for I/O.

But CPU-heavy work or blocking calls can still block the event loop.

______________________________________________________________________

# 55. Async Does Not Solve N+1

You can still have:

```text
async endpoint
+
AsyncSession
+
N+1 queries
```

Async may allow other tasks to make progress while each query waits, but the application still performs unnecessary
database work.

Fix the query pattern.

______________________________________________________________________

# 56. Async Does Not Solve Slow SQL

A query that takes:

```text
2 seconds
```

is still a 2-second database operation when called asynchronously.

Async improves how the application handles waiting; it does not magically make the database query faster.

______________________________________________________________________

# 57. Sync vs Async SQLAlchemy

| | Synchronous | Asynchronous |
|---|---|---|
| API | `Session` | `AsyncSession` |
| Engine | `Engine` | `AsyncEngine` |
| Query execution | Direct | `await` |
| Best fit | Sync application | Async I/O application |
| Blocking risk | Normal thread/blocking model | Blocking code can block event loop |
| Complexity | Lower | Higher |

Choose based on application architecture and workload rather than assuming async is always superior.

______________________________________________________________________

# 58. ORM vs Raw SQL Decision

Use ORM when:

```text
Standard CRUD
+
Domain models
+
Relationships
+
Maintainability
```

Consider SQL/Core when:

```text
Complex query
+
Precise SQL control
+
Database-specific functionality
+
ORM expression becomes difficult
```

Use performance measurements to guide the decision.

______________________________________________________________________

# 59. Common SQLAlchemy Performance Mistakes

## Mistake 1 — Ignoring N+1

Relationship access inside loops can generate many queries.

## Mistake 2 — Eager loading everything

Large object graphs can be expensive.

## Mistake 3 — Assuming `joinedload()` is always better

Joins can multiply result rows.

## Mistake 4 — Assuming `selectinload()` is always better

It still executes additional queries and transfers data that may not be needed.

## Mistake 5 — Using async with synchronous blocking calls

This can block the event loop.

## Mistake 6 — Making the connection pool huge

The database itself has capacity limits.

## Mistake 7 — Returning huge result sets

Large payloads affect database, network and application performance.

## Mistake 8 — Optimizing without measuring

Always inspect SQL and execution behavior first.

______________________________________________________________________

# 60. Production Performance Checklist

For an important endpoint, ask:

### Database access

- How many SQL statements are executed?
- Are there N+1 queries?
- Are indexes appropriate?
- What does the query plan show?

### ORM

- Is the loading strategy appropriate?
- Are too many ORM objects being created?
- Are unnecessary columns being selected?

### Connections

- Is the pool sized appropriately?
- Are connections held for too long?
- Are there pool waits/timeouts?

### Async

- Is all database work async-compatible?
- Is any blocking code running in the event loop?
- Is `AsyncSession` scoped correctly?

### API

- Is pagination bounded?
- Is the response payload unnecessarily large?
- Is serialization expensive?

______________________________________________________________________

# 61. Performance Optimization Example

Suppose:

```python
users = session.scalars(
    select(User)
).all()

for user in users:
    print(user.orders)
```

There are:

```text
1 + N
```

queries.

Possible improvement:

```python
stmt = (
    select(User)
    .options(selectinload(User.orders))
)

users = session.scalars(stmt).all()
```

Now the relationship can be loaded using a small number of queries instead of one query per user.

______________________________________________________________________

# 62. Performance Optimization Example — Joined Loading

Suppose every user needs a small, single related object such as a profile.

A joined strategy may be appropriate:

```python
stmt = (
    select(User)
    .options(joinedload(User.profile))
)
```

The database can retrieve the user and profile through a join.

Validate the generated query and result size.

______________________________________________________________________

# 63. Performance Optimization Example — Selectin Loading

Suppose:

```text
100 users
+
2,000 orders
```

A join may produce a large repeated parent result.

`selectinload()` can instead use:

```text
Query 1 → 100 users
Query 2 → orders for those users
```

This may be more efficient depending on the workload.

______________________________________________________________________

# 64. Performance Optimization Example — Projection

Instead of:

```python
users = session.scalars(
    select(User)
).all()
```

when the API only needs:

```text
id
name
```

use an appropriate projection:

```python
stmt = select(User.id, User.name)
rows = session.execute(stmt).all()
```

This avoids creating full ORM objects when they are unnecessary.

______________________________________________________________________

# 65. Performance Optimization Example — Async

An async FastAPI endpoint can use:

```python
@app.get("/users")
async def users(session: AsyncSession):
    result = await session.execute(
        select(User)
    )

    return result.scalars().all()
```

The database operation is awaited rather than executed as a blocking synchronous call in the async endpoint.

______________________________________________________________________

# 66. Senior-Level Perspective

A strong backend engineer should not answer:

> "Use `selectinload` because it's faster."

A stronger answer is:

> "I would first identify the endpoint's data-access pattern, measure query count and latency, inspect the generated SQL and execution plans, then choose between lazy loading, `joinedload`, `selectinload`, projections or a Core/raw SQL query based on result cardinality and workload. In an async FastAPI application, I would also ensure the database driver and Session are async-compatible and that no blocking work runs on the event loop."

______________________________________________________________________

# 67. Interview Questions & Answers

## Q1. What is lazy loading?

**Answer:**

Lazy loading retrieves a relationship when the application first accesses it rather than loading it as part of the
original query.

______________________________________________________________________

## Q2. What is eager loading?

**Answer:**

Eager loading explicitly retrieves related data as part of the planned database access, reducing unexpected relationship
queries.

______________________________________________________________________

## Q3. What is N+1?

**Answer:**

A pattern where one query retrieves parent objects and an additional query is executed for each parent to retrieve
related data.

______________________________________________________________________

## Q4. Why is N+1 bad?

**Answer:**

It creates many database round trips and can significantly increase latency, database load and connection-pool pressure.

______________________________________________________________________

## Q5. How do you detect N+1?

**Answer:**

Inspect SQL logs, count queries per request, use tracing/metrics and review relationship access inside loops.

______________________________________________________________________

## Q6. What is `joinedload()`?

**Answer:**

A SQLAlchemy eager-loading strategy that loads related objects using a join.

______________________________________________________________________

## Q7. What is `selectinload()`?

**Answer:**

An eager-loading strategy that retrieves parent objects and then loads related objects using additional SELECT
statements based on the parent identities.

______________________________________________________________________

## Q8. `joinedload()` vs `selectinload()`?

**Answer:**

`joinedload()` uses a join and can be efficient for small relationships, but joins against collections can multiply
result rows.

`selectinload()` uses additional queries and can be effective for collections because it avoids large joined result
sets.

______________________________________________________________________

## Q9. Is `joinedload()` always faster?

**Answer:**

No.

The best strategy depends on relationship cardinality, query shape and result size.

______________________________________________________________________

## Q10. Is `selectinload()` always faster?

**Answer:**

No.

It still performs additional queries and may retrieve data that is not actually needed.

______________________________________________________________________

## Q11. Why can joined loading produce duplicate parent rows?

**Answer:**

A one-to-many join produces one result row for each matching child, so the same parent can appear repeatedly in the SQL
result.

______________________________________________________________________

## Q12. Why might `unique()` be needed?

**Answer:**

When joined eager loading targets a collection, SQLAlchemy may need result de-duplication to reconstruct unique parent
ORM objects.

______________________________________________________________________

## Q13. What is the main risk of over-eager loading?

**Answer:**

Loading large or unnecessary object graphs can increase SQL result size, memory consumption and database/network work.

______________________________________________________________________

## Q14. Does an ORM query mean the database is doing object operations?

**Answer:**

No.

SQLAlchemy translates ORM operations into SQL/database operations and reconstructs Python objects from the results.

______________________________________________________________________

## Q15. Is ORM slower than raw SQL?

**Answer:**

Not necessarily.

A well-designed ORM query can produce efficient SQL. Performance depends on generated SQL, query plan, result size and
number of round trips.

______________________________________________________________________

## Q16. When would you use raw SQL?

**Answer:**

For highly specialized queries, database-specific functionality, precise SQL control or cases where ORM abstraction
becomes unnecessarily complex. Measure before making the switch for performance reasons.

______________________________________________________________________

## Q17. What is Async SQLAlchemy?

**Answer:**

SQLAlchemy's asynchronous API for applications using Python's async execution model, including components such as
`AsyncEngine` and `AsyncSession`.

______________________________________________________________________

## Q18. What is `AsyncSession`?

**Answer:**

The asynchronous SQLAlchemy ORM Session used to manage ORM operations and transactions in an async application.

______________________________________________________________________

## Q19. Does async make SQL queries faster?

**Answer:**

No.

Async primarily improves how the application handles I/O waiting and concurrency. The database query itself is not
automatically faster.

______________________________________________________________________

## Q20. Can async applications still suffer from N+1?

**Answer:**

Yes.

Async does not remove unnecessary database queries.

______________________________________________________________________

## Q21. What happens if you use blocking database calls inside an async endpoint?

**Answer:**

They can block the event loop and prevent other async tasks from making progress efficiently.

______________________________________________________________________

## Q22. What should an async FastAPI application use for SQLAlchemy?

**Answer:**

An appropriate `AsyncEngine`, `AsyncSession` and async-compatible database driver.

______________________________________________________________________

## Q23. Should `AsyncSession` be shared globally?

**Answer:**

No.

It is stateful and should have an appropriate lifecycle per request or unit of work rather than being shared across
concurrent operations.

______________________________________________________________________

## Q24. How does async connection pooling work?

**Answer:**

The async engine can manage a pool of async-compatible database connections that are checked out and returned as
database operations require them.

______________________________________________________________________

## Q25. What causes connection-pool exhaustion?

**Answer:**

High concurrent database demand, slow queries, long transactions, connections/sessions held too long, leaks or
inappropriate pool sizing.

______________________________________________________________________

## Q26. Should you simply increase the pool size?

**Answer:**

No.

The database has finite CPU, memory and connection capacity. Increasing application pools across many instances can
overload the database.

______________________________________________________________________

## Q27. How does multiple-instance deployment affect pool sizing?

**Answer:**

Potential connections are roughly the per-instance pool capacity multiplied by the number of application instances, plus
overflow/other connections.

______________________________________________________________________

## Q28. What is a good SQLAlchemy performance workflow?

**Answer:**

Measure, count queries, inspect generated SQL, inspect execution plans, examine indexes and result sizes, make a
targeted change and measure again.

______________________________________________________________________

## Q29. Why select only required columns?

**Answer:**

It reduces database I/O, network transfer, Python object construction, memory usage and serialization work.

______________________________________________________________________

## Q30. When should you consider Core or raw SQL instead of ORM?

**Answer:**

When a query is highly specialized, requires database-specific features, needs precise SQL control or becomes
unnecessarily difficult to express through the ORM.

______________________________________________________________________

## Q31. What is the difference between query optimization and ORM optimization?

**Answer:**

Query optimization focuses on SQL/database execution.

ORM optimization also considers object construction, relationship loading, query count and Session behavior.

______________________________________________________________________

## Q32. Why is query count important?

**Answer:**

Every database round trip has overhead, so reducing hundreds of unnecessary queries can dramatically improve endpoint
performance.

______________________________________________________________________

## Q33. What is over-fetching?

**Answer:**

Retrieving more rows, columns or related objects than the application actually needs.

______________________________________________________________________

## Q34. Why can loading a large ORM object graph hurt performance?

**Answer:**

It can generate more SQL, transfer more data, create more Python objects and consume more memory.

______________________________________________________________________

## Q35. How does pagination help ORM performance?

**Answer:**

It bounds the amount of data retrieved and processed per request, reducing database, network and application work.

______________________________________________________________________

## Q36. What is keyset pagination?

**Answer:**

Pagination based on the values of the last row rather than large offsets. See File 21 for the detailed SQL discussion.

______________________________________________________________________

## Q37. What is connection-pool pressure?

**Answer:**

The situation where many concurrent operations compete for a limited number of database connections, causing requests to
wait or time out.

______________________________________________________________________

## Q38. Can long transactions cause pool problems?

**Answer:**

Yes.

A transaction that holds a connection for a long time reduces the number of connections available to other requests.

______________________________________________________________________

## Q39. How would you optimize a FastAPI endpoint with 101 SQL queries?

**Answer:**

Identify the query pattern, look for N+1 relationship loading, inspect generated SQL, use appropriate eager loading or
batching, and verify the improvement through measurement.

______________________________________________________________________

## Q40. What is a senior-level answer to "SQLAlchemy is slow"?

**Answer:**

"SQLAlchemy itself is not enough information to diagnose the problem. I would measure query count and latency, inspect
generated SQL and execution plans, check relationship loading, result size, indexes, connection-pool behavior and
transaction duration, then optimize the actual bottleneck."

______________________________________________________________________

# 68. Scenario-Based Questions

## Scenario 1 — N+1

An endpoint loads 1,000 users and accesses:

```python
user.orders
```

for every user.

**Answer:**

Suspect N+1.

Inspect SQL logs and consider `selectinload(User.orders)` or another appropriate loading strategy.

______________________________________________________________________

## Scenario 2 — Huge Join

A user has 50,000 orders and the endpoint uses:

```python
joinedload(User.orders)
```

**Question:** What should you consider?

**Answer:**

The join can create a very large result set and duplicate parent data. Consider whether the endpoint needs all orders
and whether `selectinload`, pagination or a dedicated query is more appropriate.

______________________________________________________________________

## Scenario 3 — Small One-to-One Relationship

Every user needs a small profile object.

**Answer:**

`joinedload()` may be a reasonable candidate because the related result is small and can be loaded with the parent.

Validate the actual SQL and workload.

______________________________________________________________________

## Scenario 4 — Async Endpoint

An async FastAPI endpoint calls a synchronous blocking database function.

**Answer:**

The synchronous call can block the event loop. Use an appropriate async SQLAlchemy stack or deliberately isolate
blocking work.

______________________________________________________________________

## Scenario 5 — Async N+1

An endpoint uses `AsyncSession` but still executes 500 relationship queries.

**Answer:**

Async does not eliminate N+1. Reduce the query count through appropriate loading/batching/query design.

______________________________________________________________________

## Scenario 6 — Pool Exhaustion

The application has:

```text
20 instances
pool_size = 20
```

**Question:** What should you think about?

**Answer:**

The application could potentially maintain around 400 pooled connections before considering overflow and other
connections. Verify whether the database can safely support that concurrency.

______________________________________________________________________

## Scenario 7 — Huge Response

An endpoint returns 500,000 ORM objects.

**Answer:**

Investigate pagination, projection, batching/streaming and whether the API should return that much data at all.

______________________________________________________________________

## Scenario 8 — Raw SQL Proposal

A developer says:

> "The ORM query is slow. Rewrite everything using raw SQL."

**Answer:**

First inspect the generated SQL and execution plan. The problem may be N+1, missing indexes, excessive data, poor joins
or another issue that raw SQL would not automatically solve.

______________________________________________________________________

## Scenario 9 — Nested Relationships

The endpoint loads:

```text
User → Orders → Items → Product → Category
```

for every request.

**Answer:**

Question whether the complete graph is actually required. Deep eager loading can cause large SQL/result sets and
significant memory usage.

Load only the data needed by the endpoint.

______________________________________________________________________

## Scenario 10 — Slow Async Endpoint

The endpoint is async but remains slow.

**Answer:**

Async does not make slow database work faster. Measure database latency, query count, connection-pool waits,
serialization and other parts of the request lifecycle to find the actual bottleneck.

______________________________________________________________________

# 69. Practice Exercises

## Exercise 1 — Detect N+1

Create:

```text
User
Order
```

Load 100 users and access:

```python
user.orders
```

for every user.

Enable SQL logging and count the queries.

______________________________________________________________________

## Exercise 2 — Fix N+1 With `selectinload`

Rewrite the previous example using:

```python
selectinload(User.orders)
```

Compare:

```text
Query count
Latency
Database work
```

______________________________________________________________________

## Exercise 3 — Test `joinedload`

Repeat the experiment with:

```python
joinedload(User.orders)
```

Compare the generated SQL and result size.

______________________________________________________________________

## Exercise 4 — Cardinality Experiment

Create:

```text
10 users × 2 orders
```

and:

```text
10 users × 10,000 orders
```

Compare `joinedload()` and `selectinload()`.

Explain why relationship cardinality matters.

______________________________________________________________________

## Exercise 5 — Projection

Compare:

```python
select(User)
```

with:

```python
select(User.id, User.email)
```

Measure:

- Query time
- Memory usage
- Result size
- Python object creation

______________________________________________________________________

## Exercise 6 — Async SQLAlchemy

Create an async SQLAlchemy application.

Implement:

- AsyncEngine
- AsyncSession
- Async query
- Async transaction
- Rollback handling

______________________________________________________________________

## Exercise 7 — Blocking in Async

Create an async endpoint containing a blocking operation.

Measure the effect on concurrent requests.

Then replace it with an async-compatible approach.

______________________________________________________________________

## Exercise 8 — Pool Pressure

Configure a small async pool and generate concurrent requests.

Observe:

- Pool checkout time
- Waiting requests
- Timeout behavior
- Database concurrency

______________________________________________________________________

## Exercise 9 — ORM vs SQL

Implement the same query using:

1. ORM.
1. SQLAlchemy Core.
1. Raw SQL.

Compare generated SQL, readability and performance.

______________________________________________________________________

## Exercise 10 — FastAPI Integration

Create a FastAPI endpoint using `AsyncSession`.

Implement:

```text
dependency
 ↓
endpoint
 ↓
service
 ↓
database
```

Ensure Session cleanup occurs after the request.

______________________________________________________________________

## Exercise 11 — Pagination

Implement a paginated endpoint.

Compare:

```text
OFFSET pagination
```

with:

```text
keyset/cursor pagination
```

for a large dataset.

______________________________________________________________________

## Exercise 12 — Performance Investigation

Take one slow endpoint and document:

```text
Baseline
Query count
Generated SQL
Execution plan
Largest query
Pool behavior
Loading strategy
Optimization
New measurement
```

______________________________________________________________________

# 70. Quick Revision

| Concept | Key Point |
|---|---|
| Lazy loading | Loads relationship when accessed |
| Eager loading | Explicitly loads related data |
| N+1 | One parent query + N child queries |
| `joinedload` | Eager loading using joins |
| `selectinload` | Eager loading using additional SELECT |
| Joined collections | Can multiply result rows |
| `unique()` | De-duplicates joined collection results |
| Over-eager loading | Loads unnecessary data |
| Projection | Select only required columns |
| ORM | Object/database abstraction |
| Raw SQL | Direct SQL control |
| Async SQLAlchemy | Async database API |
| `AsyncEngine` | Async database engine |
| `AsyncSession` | Async ORM Session |
| Async `execute` | Await database execution |
| Async `commit` | Await transaction commit |
| Async `flush` | Await ORM flush |
| Event loop | Must not be blocked by synchronous work |
| Async pooling | Reuses async-compatible connections |
| Pool exhaustion | Concurrent demand exceeds available connections |
| Pool sizing | Must account for total application instances |
| Query optimization | Measure → inspect → change → measure |
| Query count | Number of DB round trips matters |
| Result size | Affects DB, network and application |
| FastAPI integration | Clear Session/request lifecycle |
| N+1 + async | Async does not eliminate unnecessary queries |

______________________________________________________________________

# 71. Completion Checklist

Before moving to File 25, make sure you can explain:

- [ ] Lazy loading
- [ ] Eager loading
- [ ] N+1
- [ ] Detecting N+1
- [ ] `joinedload`
- [ ] `selectinload`
- [ ] Joined collection row multiplication
- [ ] `unique()`
- [ ] Choosing joined vs select-in loading
- [ ] Nested eager loading
- [ ] Over-eager loading
- [ ] Projection/selecting required columns
- [ ] ORM vs raw SQL
- [ ] When to use Core/raw SQL
- [ ] Async SQLAlchemy
- [ ] `AsyncEngine`
- [ ] `AsyncSession`
- [ ] Async queries
- [ ] Async transactions
- [ ] Async flush/commit
- [ ] Blocking calls in async applications
- [ ] Async connection pooling
- [ ] Pool exhaustion
- [ ] Pool sizing
- [ ] Multi-instance pool capacity
- [ ] Query optimization workflow
- [ ] Query count
- [ ] Result size
- [ ] Pagination
- [ ] Bulk operations overview
- [ ] Streaming/batched results overview
- [ ] FastAPI integration
- [ ] Session lifecycle
- [ ] Transaction ownership
- [ ] Async N+1
- [ ] ORM performance trade-offs

______________________________________________________________________

# 72. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is lazy loading?
1. What is eager loading?
1. What is the N+1 query problem?
1. Why is N+1 dangerous?
1. How would you detect N+1?
1. What is `joinedload()`?
1. What is `selectinload()`?
1. Compare `joinedload()` and `selectinload()`.
1. Why can joined loading create duplicate parent rows?
1. Why might `unique()` be needed?
1. When would you choose `joinedload()`?
1. When would you choose `selectinload()`?
1. Is `joinedload()` always faster?
1. Is `selectinload()` always faster?
1. What is over-eager loading?
1. Why can deep eager loading be expensive?
1. Why should you select only required columns?
1. What is a projection?
1. Is SQLAlchemy ORM always slower than raw SQL?
1. When would you use raw SQL?
1. What is Async SQLAlchemy?
1. What is `AsyncEngine`?
1. What is `AsyncSession`?
1. Does async make database queries faster?
1. What happens when blocking code runs in an async endpoint?
1. Why can a synchronous DB call block FastAPI's event loop?
1. How should an async FastAPI application manage `AsyncSession`?
1. Should `AsyncSession` be shared globally?
1. What is async connection pooling?
1. What causes connection-pool exhaustion?
1. Why isn't increasing pool size indefinitely a solution?
1. How does the number of application instances affect pool sizing?
1. What is the difference between query latency and query count?
1. Why can reducing query count improve performance dramatically?
1. How would you optimize an endpoint performing 101 SQL queries?
1. How would you investigate a slow ORM query?
1. Why does result size matter?
1. Why can creating millions of ORM objects be expensive?
1. How can pagination improve ORM performance?
1. What is keyset pagination?
1. Does async solve N+1?
1. Does async solve slow SQL?
1. What is the relationship between SQLAlchemy and the database execution plan?
1. How would you decide between ORM and Core?
1. How would you decide between `joinedload` and `selectinload`?
1. What causes pool pressure in a FastAPI application?
1. How can long transactions affect connection availability?
1. How would you optimize a large one-to-many relationship?
1. How would you optimize an endpoint that loads a deep object graph?
1. Give a senior-level answer to: "SQLAlchemy is slow."

If you can answer these confidently and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [23. SQLAlchemy ORM](./23-sqlalchemy-core.md)

**Next:** [25. Database Scaling](./25-database-scaling.md)

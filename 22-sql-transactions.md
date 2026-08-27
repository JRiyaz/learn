# 22. Transactions, ACID & Database Concurrency

**Previous:** [21. SQL Indexes & Query Performance](./21-sql-indexes-performance.md)

**Next:** [23. SQLAlchemy Core](./23-sqlalchemy-core.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain what a database transaction is.
- Explain ACID with practical backend examples.
- Understand atomicity, consistency, isolation and durability.
- Explain common transaction isolation levels.
- Understand dirty reads, non-repeatable reads and phantom reads.
- Explain database locks.
- Understand deadlocks and how to reduce their occurrence.
- Explain MVCC at a practical level.
- Compare optimistic and pessimistic locking.
- Recognize transaction/concurrency problems in real backend services.
- Choose appropriate transaction boundaries in Python applications.

> **Scope note:** This topic focuses on relational database transactions and concurrency. SQLAlchemy-specific transaction APIs are covered in File 23.

______________________________________________________________________

# 1. What Is a Transaction?

A transaction is a logical unit of database work that should be treated as one operation.

For example, transferring money between two accounts requires:

```text
Debit account A
+
Credit account B
```

Both operations should succeed together or neither should take effect.

______________________________________________________________________

# 2. Basic Transaction Flow

Conceptually:

```text
BEGIN
  ↓
Operation 1
  ↓
Operation 2
  ↓
COMMIT
```

If something fails:

```text
BEGIN
  ↓
Operation 1
  ↓
Operation 2 fails
  ↓
ROLLBACK
```

The exact transaction syntax varies by database.

______________________________________________________________________

# 3. Why Transactions Matter

Without transactions, a multi-step operation can leave partial state.

Example:

```text
Account A: ₹10,000
Account B: ₹5,000
```

Transfer ₹1,000.

If the debit succeeds:

```text
A = ₹9,000
```

but the credit fails:

```text
B = ₹5,000
```

the money has effectively disappeared.

A transaction prevents this partial outcome when both operations are correctly included in the same transaction.

______________________________________________________________________

# 4. ACID

ACID stands for:

- Atomicity
- Consistency
- Isolation
- Durability

These properties describe important guarantees provided by transactional database systems.

______________________________________________________________________

# 5. Atomicity

Atomicity means a transaction is treated as an all-or-nothing unit.

Example:

```text
Create order
+
Create order items
+
Reserve inventory
```

If a required operation fails and the transaction is rolled back, the transaction should not leave a partial committed
state.

______________________________________________________________________

# 6. Atomicity Example

Suppose:

```text
orders
order_items
payments
```

An order creation flow performs:

```text
INSERT order
INSERT order items
INSERT payment record
```

If payment-record creation fails and the business operation requires all three changes to be atomic, the transaction
should roll back the earlier changes.

______________________________________________________________________

# 7. Consistency

Consistency means a committed transaction moves the database from one valid state to another valid state according to
the database's constraints and application rules.

Examples of database constraints include:

- Primary keys
- Foreign keys
- Unique constraints
- `NOT NULL`
- `CHECK` constraints

A transaction should not leave data violating enforced integrity rules.

______________________________________________________________________

# 8. Atomicity vs Consistency

These are often confused.

### Atomicity

> Did the transaction happen completely or not?

### Consistency

> Did the transaction preserve the required database invariants?

A transaction can be atomic while still containing incorrect application logic.

ACID consistency does not mean:

> "The database guarantees that all business logic is correct."

______________________________________________________________________

# 9. Isolation

Isolation controls how concurrent transactions interact with each other.

Consider:

```text
Transaction A
Transaction B
```

running at the same time.

Isolation determines which intermediate or concurrent changes each transaction can observe.

______________________________________________________________________

# 10. Durability

Durability means that once a transaction is successfully committed, the database is designed to preserve that committed
state despite appropriate failures.

Database engines typically achieve durability through mechanisms such as:

- Write-ahead logging
- Persistent storage
- Recovery procedures
- Replication configurations

The exact guarantees depend on the database and deployment configuration.

______________________________________________________________________

# 11. ACID Interview Summary

| Property | Meaning |
|---|---|
| Atomicity | All-or-nothing transaction |
| Consistency | Preserves defined integrity/invariants |
| Isolation | Controls interaction between concurrent transactions |
| Durability | Committed data survives appropriate failures |

______________________________________________________________________

# 12. Transaction Lifecycle

A simplified lifecycle is:

```text
BEGIN
  ↓
Read / Write
  ↓
Validation
  ↓
COMMIT
```

or:

```text
BEGIN
  ↓
Read / Write
  ↓
Error
  ↓
ROLLBACK
```

A transaction may also be aborted because of a concurrency conflict or database error.

______________________________________________________________________

# 13. Commit

`COMMIT` makes the transaction's changes durable according to the database's transaction guarantees.

Conceptually:

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 1000
WHERE id = 1;

UPDATE accounts
SET balance = balance + 1000
WHERE id = 2;

COMMIT;
```

______________________________________________________________________

# 14. Rollback

`ROLLBACK` discards uncommitted changes in the transaction.

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 1000
WHERE id = 1;

-- Something goes wrong

ROLLBACK;
```

The transaction's uncommitted changes are undone.

______________________________________________________________________

# 15. Transaction Boundary

A transaction boundary defines which operations belong to one atomic unit.

For example:

```text
API request
    ↓
BEGIN
    ↓
Validate
    ↓
Update order
    ↓
Update inventory
    ↓
COMMIT
    ↓
Response
```

The correct boundary depends on the business operation.

______________________________________________________________________

# 16. Keep Transactions Focused

Long transactions can cause:

- Longer lock durations
- More contention
- More resources held
- Higher deadlock probability
- Reduced throughput

Avoid keeping a transaction open while performing unrelated slow work such as external API calls unless there is a
strong reason.

______________________________________________________________________

# 17. Transaction and External APIs

Consider:

```text
BEGIN
 ↓
Update database
 ↓
Call payment API
 ↓
COMMIT
```

This can be dangerous if the payment API takes several seconds.

The database transaction may remain open while waiting for a network operation.

A better architecture may use:

- Short database transactions
- Idempotent external operations
- Outbox/event patterns where appropriate
- Explicit state transitions

The exact architecture depends on business requirements.

______________________________________________________________________

# 18. Isolation Levels

Common SQL isolation levels are:

```text
READ UNCOMMITTED
READ COMMITTED
REPEATABLE READ
SERIALIZABLE
```

The exact behavior varies by database engine.

Some databases also provide additional or engine-specific semantics.

______________________________________________________________________

# 19. READ UNCOMMITTED

This is the weakest standard isolation level.

It may permit reading changes that have not yet been committed by another transaction.

This enables dirty reads.

Support and exact behavior vary by database.

______________________________________________________________________

# 20. READ COMMITTED

A transaction generally sees only committed data.

It prevents dirty reads.

However, the same query executed twice within a transaction may observe different committed values if another
transaction commits a change between the reads.

That is a non-repeatable read.

______________________________________________________________________

# 21. REPEATABLE READ

The goal is to provide stronger consistency for repeated reads within a transaction.

A transaction generally gets a stable view for rows it reads, although exact behavior varies significantly between
database engines.

Some systems provide snapshot-based semantics.

______________________________________________________________________

# 22. SERIALIZABLE

Serializable provides the strongest standard isolation level.

The goal is for concurrent execution to behave as though transactions were executed serially.

This can reduce concurrency and may cause:

- Blocking
- Serialization failures
- Transaction retries

It should be used when its stronger guarantees are required and the workload can tolerate the cost.

______________________________________________________________________

# 23. Isolation Level Summary

| Isolation | Dirty Read | Non-Repeatable Read | Phantom Read |
|---|---:|---:|---:|
| Read Uncommitted | Possible | Possible | Possible |
| Read Committed | Prevented | Possible | Possible |
| Repeatable Read | Prevented | Prevented by standard definition | Implementation-dependent |
| Serializable | Prevented | Prevented | Prevented |

> **Important:** Real database engines do not always map perfectly onto this simplified table. For interviews, understand the standard concepts and mention database-specific behavior when relevant.

______________________________________________________________________

# 24. Dirty Read

A dirty read occurs when one transaction reads data written by another transaction before that transaction commits.

Example:

```text
Transaction A:
balance = 9000
not committed

Transaction B:
reads balance = 9000
```

If A later rolls back:

```text
balance = 10000
```

B read a value that was never committed.

______________________________________________________________________

# 25. Non-Repeatable Read

A transaction reads a row twice and obtains different values because another transaction committed an update between the
reads.

Example:

```text
Transaction A:
SELECT balance → 10000

Transaction B:
UPDATE balance → 9000
COMMIT

Transaction A:
SELECT balance → 9000
```

The same logical read produced different values.

______________________________________________________________________

# 26. Phantom Read

A phantom read occurs when a repeated range query sees a different set of matching rows because another transaction
inserted or deleted rows that satisfy the predicate.

Example:

```text
Transaction A:
SELECT *
FROM orders
WHERE amount > 1000;
```

Transaction B inserts another matching order and commits.

Transaction A runs the range query again and sees an additional row.

That new row is a phantom.

______________________________________________________________________

# 27. Dirty vs Non-Repeatable vs Phantom

| Problem | What Changed? |
|---|---|
| Dirty read | Uncommitted value |
| Non-repeatable read | Existing row's value |
| Phantom read | Set of matching rows |

This distinction is frequently tested in interviews.

______________________________________________________________________

# 28. Locks

A database lock controls concurrent access to data.

Locks can help prevent conflicting operations from happening simultaneously.

Common conceptual categories include:

- Shared/read locks
- Exclusive/write locks

Exact lock modes and behavior vary by database.

______________________________________________________________________

# 29. Shared Lock

A shared lock generally allows compatible reads while preventing conflicting modifications for the protected resource.

Conceptually:

```text
Reader A ──┐
Reader B ──┼── shared access
Reader C ──┘

Writer → may need to wait
```

The exact behavior depends on the database's locking model.

______________________________________________________________________

# 30. Exclusive Lock

An exclusive lock is generally used for modifications.

Conceptually:

```text
Writer
  ↓
Exclusive access
  ↓
Conflicting readers/writers may wait
```

Modern MVCC databases can allow certain readers to proceed without waiting for writers, so avoid assuming every read
blocks during every write.

______________________________________________________________________

# 31. Lock Granularity

Databases may lock resources at different granularities, depending on the engine:

- Row
- Page/block
- Table
- Other engine-specific resources

Finer-grained locking can improve concurrency but may require more lock-management overhead.

______________________________________________________________________

# 32. Lock Contention

Lock contention occurs when transactions compete for the same resources.

Example:

```text
Transaction A → row 10
Transaction B → row 10
```

If both need conflicting locks, one may have to wait.

High contention can increase latency and reduce throughput.

______________________________________________________________________

# 33. Deadlock

A deadlock occurs when transactions wait on each other in a cycle.

Example:

```text
Transaction A locks row 1
Transaction B locks row 2

A waits for row 2
B waits for row 1
```

Neither can continue.

______________________________________________________________________

# 34. Deadlock Detection

Many database engines can detect deadlocks.

The database may abort one transaction so the other can continue.

The application should be prepared to retry appropriate transient transaction failures.

Do not blindly retry every database exception.

______________________________________________________________________

# 35. Preventing Deadlocks

Common strategies:

### 1. Consistent lock ordering

Always acquire resources in the same order.

For example:

```text
account_id ascending
```

instead of allowing different code paths to lock accounts in different orders.

### 2. Keep transactions short

Reduce the time resources remain locked.

### 3. Avoid unnecessary locks

Lock only what the operation actually needs.

### 4. Retry transient failures

Implement bounded retries with appropriate backoff where supported by the application's correctness model.

______________________________________________________________________

# 36. Deadlock Example

Bad:

```text
Transfer A → B
    lock A
    lock B

Transfer B → A
    lock B
    lock A
```

Possible deadlock.

Better:

```text
Always lock the lower account ID first.
```

Then both operations follow:

```text
lock min(A,B)
lock max(A,B)
```

This can eliminate that specific circular-wait pattern.

______________________________________________________________________

# 37. MVCC

MVCC stands for **Multi-Version Concurrency Control**.

Instead of making every reader wait for writers, MVCC can maintain multiple versions of data and allow transactions to
see an appropriate version.

This can improve read concurrency.

The exact implementation varies by database.

______________________________________________________________________

# 38. MVCC Conceptual Example

Suppose:

```text
Current balance = 10000
```

Transaction A updates it:

```text
10000 → 9000
```

Another transaction may continue reading an appropriate older committed version depending on its isolation semantics.

Conceptually:

```text
Version 1 → 10000
Version 2 → 9000
```

The database determines which version a transaction can see.

______________________________________________________________________

# 39. MVCC Advantages

MVCC can provide:

- Better read/write concurrency
- Reduced reader/writer blocking
- Snapshot-style reads
- Efficient concurrent access

But MVCC introduces its own costs and complexities, such as:

- Multiple row versions
- Cleanup/version maintenance
- Storage overhead
- Long-running transaction effects

______________________________________________________________________

# 40. MVCC and Long Transactions

Long-running transactions can prevent old versions from being cleaned up efficiently in some MVCC systems.

This can lead to:

- Storage growth
- Table/index bloat
- More cleanup work
- Performance degradation

Therefore:

> Keep transactions as short as practical.

______________________________________________________________________

# 41. Optimistic Locking

Optimistic locking assumes conflicts are relatively uncommon.

The application reads a version:

```text
version = 5
```

and later updates conditionally:

```sql
UPDATE accounts
SET balance = ?,
    version = version + 1
WHERE id = ?
  AND version = 5;
```

If zero rows are updated, another transaction may have modified the record.

The application can detect the conflict.

______________________________________________________________________

# 42. Optimistic Locking Example

Initial:

```text
id = 10
balance = 1000
version = 5
```

Transaction A reads version 5.

Transaction B also reads version 5.

A updates:

```text
version 5 → 6
```

B attempts:

```sql
WHERE version = 5
```

The update affects zero rows.

B detects that its copy is stale.

______________________________________________________________________

# 43. Why Optimistic Locking Is Useful

It works well when:

- Conflicts are relatively rare.
- Holding database locks for long periods is undesirable.
- Requests may be separated by application processing.
- The application can gracefully handle conflicts.

Common use cases include:

- Editing records
- Inventory updates
- Account/profile changes
- API-level concurrent updates

______________________________________________________________________

# 44. Pessimistic Locking

Pessimistic locking assumes conflicts are likely and acquires a lock before making a critical change.

Conceptually:

```text
SELECT row
FOR UPDATE
```

The exact syntax and semantics depend on the database.

Other transactions attempting conflicting operations may have to wait or fail according to the lock configuration.

______________________________________________________________________

# 45. Optimistic vs Pessimistic Locking

| | Optimistic | Pessimistic |
|---|---|---|
| Assumption | Conflicts uncommon | Conflicts likely |
| Mechanism | Version/check condition | Database lock |
| Waiting | Usually less | Potentially more |
| Conflict handling | Detect after conflict | Prevent/serialize conflict |
| Good for | Low-contention updates | Critical contested rows |
| Risk | Retry/conflict handling | Blocking/deadlocks |

______________________________________________________________________

# 46. Inventory Example

Suppose:

```text
inventory = 1
```

Two requests attempt to buy the final item.

A naive flow:

```text
Read inventory = 1
Read inventory = 1
```

Both requests may think they can purchase it.

This is a concurrency bug.

______________________________________________________________________

# 47. Inventory With Atomic Update

One possible approach is:

```sql
UPDATE inventory
SET quantity = quantity - 1
WHERE product_id = ?
  AND quantity > 0;
```

Then check the number of affected rows.

If:

```text
1 row updated
```

the reservation succeeded.

If:

```text
0 rows updated
```

there was no available inventory.

This can avoid a separate read-then-write race.

______________________________________________________________________

# 48. Read-Modify-Write Race

Dangerous pattern:

```text
read value
   ↓
application calculation
   ↓
write value
```

Two transactions can read the same old value and overwrite each other's changes.

Prefer an atomic database operation or appropriate locking/version checking.

______________________________________________________________________

# 49. Lost Update

A lost update occurs when concurrent transactions overwrite each other's changes.

Example:

```text
Initial value = 100

A reads 100
B reads 100

A writes 120
B writes 110
```

A's update is effectively lost.

Optimistic locking or appropriate database locking can prevent this.

______________________________________________________________________

# 50. Transaction Isolation Is Not the Same as Locking

Isolation and locking are related but not identical concepts.

Isolation describes what concurrent transactions can observe.

Locks are one mechanism databases can use to control conflicting access.

MVCC is another major mechanism.

A database can combine:

```text
MVCC
+
locks
+
isolation rules
```

______________________________________________________________________

# 51. Application Transaction Boundaries

In a Python backend, avoid scattering transaction control randomly across repository functions.

For example, if:

```text
create_order()
reserve_inventory()
create_payment()
```

must succeed atomically, the application should have a clear transaction boundary around the complete business
operation.

The exact layering depends on the architecture.

______________________________________________________________________

# 52. Transaction Scope in Web APIs

A typical request may follow:

```text
Request
  ↓
Validate
  ↓
Begin transaction
  ↓
Business operations
  ↓
Commit
  ↓
Response
```

If the business operation fails:

```text
Rollback
```

Framework and ORM behavior varies, so understand what your application actually does.

______________________________________________________________________

# 53. Do Not Hold Transactions Across Slow Work

Avoid unnecessarily doing:

```text
BEGIN
 ↓
Database update
 ↓
HTTP API call
 ↓
File operation
 ↓
Long computation
 ↓
COMMIT
```

This can increase transaction duration and contention.

Prefer:

```text
Short DB transaction
+
External workflow/state management
```

when the business process allows it.

______________________________________________________________________

# 54. Transaction Retry

Some concurrency failures are transient.

For example:

```text
deadlock
serialization failure
```

may be retriable.

A robust retry strategy should include:

- Limited retry count
- Backoff
- Idempotent transaction logic
- Specific error classification
- Logging/metrics

Do not retry arbitrary database errors indefinitely.

______________________________________________________________________

# 55. Idempotency and Transactions

A transaction protects database state, but it does not automatically make an API request idempotent.

For example:

```text
POST /payments
```

may succeed in the database while the client times out before receiving the response.

The client may retry.

An idempotency key can help ensure the same logical request is not processed multiple times.

This is an application-level concern that works alongside transactions.

______________________________________________________________________

# 56. Isolation Level Selection

Do not automatically choose:

```text
SERIALIZABLE
```

for every operation.

Consider:

- Correctness requirement
- Contention
- Throughput
- Transaction duration
- Retry behavior
- Database engine
- Workload

Use the weakest isolation level that correctly satisfies the business requirements, when practical.

______________________________________________________________________

# 57. Common Transaction Mistakes

## Mistake 1 — One transaction for an entire workflow

Long transactions can increase contention.

## Mistake 2 — External API calls inside transactions

Network delays can keep database resources open unnecessarily.

## Mistake 3 — Read then write without concurrency protection

This can create lost updates.

## Mistake 4 — Retrying every database error

Only appropriate transient failures should normally be retried.

## Mistake 5 — Ignoring deadlocks

Deadlocks are possible in concurrent systems and should be handled intentionally.

## Mistake 6 — Assuming isolation semantics are identical everywhere

Database engines differ.

## Mistake 7 — Assuming MVCC eliminates locks

MVCC reduces some reader/writer conflicts but does not eliminate all locking.

______________________________________________________________________

# 58. Interview Questions & Answers

## Q1. What is a database transaction?

**Answer:**

A transaction is a logical unit of database work whose operations are committed or rolled back as a unit according to
the transaction's guarantees.

______________________________________________________________________

## Q2. What does ACID stand for?

**Answer:**

Atomicity, Consistency, Isolation and Durability.

______________________________________________________________________

## Q3. Explain atomicity.

**Answer:**

A transaction's changes are treated as an all-or-nothing unit.

______________________________________________________________________

## Q4. Explain consistency.

**Answer:**

A successful transaction preserves the database's enforced integrity constraints and required invariants.

______________________________________________________________________

## Q5. Explain isolation.

**Answer:**

Isolation controls what concurrent transactions can observe and how their operations interact.

______________________________________________________________________

## Q6. Explain durability.

**Answer:**

Once a transaction commits successfully, its committed state is designed to survive appropriate failures according to
the database's durability guarantees.

______________________________________________________________________

## Q7. Atomicity vs consistency?

**Answer:**

Atomicity concerns whether all transaction operations happen as a unit.

Consistency concerns whether the resulting committed state satisfies the required constraints/invariants.

______________________________________________________________________

## Q8. What is a dirty read?

**Answer:**

Reading data written by another transaction before that transaction commits.

______________________________________________________________________

## Q9. What is a non-repeatable read?

**Answer:**

Reading the same row twice and seeing different committed values because another transaction changed it between reads.

______________________________________________________________________

## Q10. What is a phantom read?

**Answer:**

Repeating a range query and seeing a different set of matching rows because another transaction inserted, deleted or
otherwise changed rows relevant to the predicate.

______________________________________________________________________

## Q11. What are common isolation levels?

**Answer:**

Read Uncommitted, Read Committed, Repeatable Read and Serializable.

Exact semantics vary by database engine.

______________________________________________________________________

## Q12. Which isolation level prevents dirty reads?

**Answer:**

Read Committed and stronger standard isolation levels prevent dirty reads.

______________________________________________________________________

## Q13. Can Read Committed have non-repeatable reads?

**Answer:**

Yes.

Another transaction can commit an update between two reads in the same transaction.

______________________________________________________________________

## Q14. What is Serializable?

**Answer:**

An isolation level intended to make concurrent execution equivalent to some serial ordering of transactions.

It can reduce concurrency and cause retries or blocking.

______________________________________________________________________

## Q15. What is a lock?

**Answer:**

A database mechanism for controlling conflicting concurrent access to resources.

______________________________________________________________________

## Q16. Shared vs exclusive lock?

**Answer:**

Shared locks generally allow compatible readers while conflicting with certain writes.

Exclusive locks protect modifications against conflicting access.

Exact semantics depend on the database.

______________________________________________________________________

## Q17. What is lock contention?

**Answer:**

When concurrent transactions compete for the same database resources and one or more must wait.

______________________________________________________________________

## Q18. What is a deadlock?

**Answer:**

A circular dependency where transactions wait for resources held by each other, so none can proceed.

______________________________________________________________________

## Q19. How do you prevent deadlocks?

**Answer:**

Use consistent lock ordering, keep transactions short, avoid unnecessary locking and handle transient deadlock errors
with bounded retries where appropriate.

______________________________________________________________________

## Q20. What is MVCC?

**Answer:**

Multi-Version Concurrency Control maintains multiple versions of data so transactions can often read an appropriate
version without blocking on every concurrent write.

______________________________________________________________________

## Q21. Does MVCC eliminate locks?

**Answer:**

No.

MVCC reduces some reader/writer conflicts but databases still use locks for various operations and conflict control.

______________________________________________________________________

## Q22. What is optimistic locking?

**Answer:**

A concurrency-control approach where updates verify that the row has not changed since it was read, often using a
version column.

______________________________________________________________________

## Q23. What is pessimistic locking?

**Answer:**

A strategy that acquires database locks proactively to prevent conflicting concurrent modifications.

______________________________________________________________________

## Q24. Optimistic vs pessimistic locking?

**Answer:**

Optimistic locking detects conflicts when updating.

Pessimistic locking attempts to prevent conflicting access by acquiring locks before the critical operation.

______________________________________________________________________

## Q25. What is a lost update?

**Answer:**

When concurrent read-modify-write operations cause one transaction's update to overwrite another transaction's update.

______________________________________________________________________

## Q26. How do you prevent lost updates?

**Answer:**

Use atomic SQL updates, optimistic version checks, appropriate row locking or stronger transaction semantics depending
on the requirement.

______________________________________________________________________

## Q27. Why are long transactions dangerous?

**Answer:**

They can hold resources longer, increase contention, increase deadlock probability and reduce throughput.

______________________________________________________________________

## Q28. Should external API calls happen inside database transactions?

**Answer:**

Usually avoid it when possible because network latency can keep the transaction open. Use appropriate state-management,
idempotency or asynchronous patterns instead.

______________________________________________________________________

## Q29. Can a transaction guarantee an external API call also commits?

**Answer:**

No.

A normal database transaction does not automatically provide atomicity across an unrelated external service.

Distributed transaction patterns or application-level coordination may be required.

______________________________________________________________________

## Q30. What is transaction retry?

**Answer:**

Re-executing an appropriate transaction after a transient concurrency failure such as a deadlock or serialization
failure.

______________________________________________________________________

## Q31. Should every transaction error be retried?

**Answer:**

No.

Only known transient and safely retriable failures should be retried.

______________________________________________________________________

## Q32. Why is idempotency useful with transactions?

**Answer:**

It protects against repeated logical requests, especially when clients retry after timeouts.

A database transaction alone does not guarantee API-level idempotency.

______________________________________________________________________

## Q33. What is a transaction boundary?

**Answer:**

The boundary that defines which operations must commit or roll back together.

______________________________________________________________________

## Q34. How should transaction boundaries be chosen?

**Answer:**

Around a coherent business operation whose database changes require atomicity, while keeping the transaction as short as
practical.

______________________________________________________________________

## Q35. Why can Serializable reduce throughput?

**Answer:**

It requires stronger coordination between concurrent transactions, potentially causing more blocking, conflicts or
retries.

______________________________________________________________________

## Q36. Should you always use Serializable?

**Answer:**

No.

Choose isolation based on correctness requirements and workload characteristics.

______________________________________________________________________

## Q37. What is the difference between a lock and isolation level?

**Answer:**

An isolation level defines concurrency/visibility guarantees.

A lock is one mechanism used by a database to control conflicting access.

______________________________________________________________________

## Q38. Why can MVCC increase storage usage?

**Answer:**

Multiple versions of rows may exist temporarily and require cleanup.

______________________________________________________________________

## Q39. How can long transactions affect MVCC databases?

**Answer:**

They can keep older versions visible for longer, delaying cleanup and potentially causing storage growth or bloat.

______________________________________________________________________

## Q40. Give a senior-level transaction strategy.

**Answer:**

Define clear business transaction boundaries, keep transactions short, use the minimum isolation/locking needed for
correctness, protect read-modify-write operations, maintain consistent lock ordering, handle transient concurrency
failures deliberately and use idempotency for retryable external/API workflows.

______________________________________________________________________

# 59. Scenario-Based Questions

## Scenario 1 — Money Transfer

Two updates must happen together:

```text
Debit A
Credit B
```

**Answer:**

Put both database changes in one transaction so either both commit or both roll back.

______________________________________________________________________

## Scenario 2 — Inventory Race

Inventory is 1 and two users attempt to purchase it simultaneously.

**Answer:**

Avoid an unsafe read-then-write sequence.

Use an atomic conditional update, appropriate row locking, or another concurrency-control strategy and verify the
affected-row count.

______________________________________________________________________

## Scenario 3 — Lost Update

Two requests read:

```text
version = 5
```

and both attempt to save changes.

**Answer:**

Use optimistic locking with a version condition or another appropriate concurrency mechanism.

______________________________________________________________________

## Scenario 4 — Deadlock

Transaction A locks row 1 then waits for row 2.

Transaction B locks row 2 then waits for row 1.

**Answer:**

This is a deadlock.

Use consistent resource-lock ordering and handle database deadlock errors with bounded retry where appropriate.

______________________________________________________________________

## Scenario 5 — Slow Payment API

A transaction updates an order and then waits five seconds for a payment provider.

**Answer:**

Avoid unnecessarily holding the database transaction open during the network call.

Consider an explicit order/payment state machine, idempotency and an appropriate asynchronous or outbox-based workflow.

______________________________________________________________________

## Scenario 6 — Read Committed

A transaction executes the same query twice and sees:

```text
100
120
```

**Answer:**

This is consistent with a non-repeatable read under Read Committed if another transaction committed the update between
the two reads.

______________________________________________________________________

## Scenario 7 — Phantom Rows

A transaction queries:

```sql
SELECT COUNT(*)
FROM orders
WHERE amount > 1000;
```

and later sees a larger count because another transaction inserted a matching order.

**Answer:**

This is a phantom-read scenario under an isolation model that permits it.

______________________________________________________________________

## Scenario 8 — Long MVCC Transaction

A reporting transaction runs for 30 minutes while the system continuously updates a table.

**Answer:**

Investigate whether the long-running transaction is preventing old versions from being cleaned up, causing storage/bloat
or other performance problems.

______________________________________________________________________

## Scenario 9 — Client Timeout

The client submits an order.

The database commits successfully.

The response times out before reaching the client.

The client retries.

**Answer:**

Use an idempotency key or equivalent request-identity mechanism so the retry does not create a duplicate logical order.

______________________________________________________________________

## Scenario 10 — Choosing Locking Strategy

A frequently edited record has very few concurrent conflicts.

**Answer:**

Optimistic locking may be appropriate because conflicts are rare and holding database locks unnecessarily could reduce
concurrency.

If conflicts are frequent and serialization is required, pessimistic locking may be more appropriate.

______________________________________________________________________

# 60. Practice Exercises

## Exercise 1 — ACID

Explain ACID using a money-transfer example.

For each property, give one concrete consequence.

______________________________________________________________________

## Exercise 2 — Isolation Phenomena

Create two concurrent transaction examples demonstrating:

- Dirty read
- Non-repeatable read
- Phantom read

Record which isolation level permits/prevents each behavior in your database.

______________________________________________________________________

## Exercise 3 — Lost Update

Implement a read-modify-write race.

Then fix it using:

1. Atomic SQL.
1. Optimistic locking.
1. Pessimistic locking.

Compare the approaches.

______________________________________________________________________

## Exercise 4 — Deadlock

Create two transactions that intentionally acquire two rows in opposite order.

Observe the deadlock behavior in a safe test environment.

Then fix it with consistent ordering.

______________________________________________________________________

## Exercise 5 — Transaction Boundary

Design an order-creation workflow containing:

```text
order
order_items
inventory
payment
```

Decide which operations should be in one database transaction and which should happen outside it.

Explain your reasoning.

______________________________________________________________________

## Exercise 6 — Retry

Implement bounded retry handling for a known transient transaction failure.

Include:

- Maximum retry count
- Backoff
- Logging
- Error classification

______________________________________________________________________

## Exercise 7 — Optimistic Locking

Add:

```text
version
```

to a table.

Implement an update that succeeds only when the expected version matches.

______________________________________________________________________

## Exercise 8 — Pessimistic Locking

Use your database's row-locking syntax to safely update a contested record.

Measure behavior under concurrent requests.

______________________________________________________________________

## Exercise 9 — Pagination and Transactions

Investigate how long-running transactions interact with pagination/reporting workloads in your database.

Document any observed impact.

______________________________________________________________________

## Exercise 10 — API Idempotency

Design an idempotent order API using:

```text
idempotency_key
```

Explain how the database transaction and idempotency mechanism work together.

______________________________________________________________________

# 61. Quick Revision

| Concept | Key Point |
|---|---|
| Transaction | Logical unit of database work |
| `COMMIT` | Makes transaction changes committed |
| `ROLLBACK` | Discards uncommitted transaction changes |
| ACID | Atomicity, Consistency, Isolation, Durability |
| Atomicity | All-or-nothing |
| Consistency | Preserves enforced invariants/constraints |
| Isolation | Controls concurrent visibility/interactions |
| Durability | Committed state survives appropriate failures |
| Read Uncommitted | Weakest standard isolation |
| Read Committed | Prevents dirty reads |
| Repeatable Read | Stronger repeated-read guarantees |
| Serializable | Strongest standard isolation |
| Dirty read | Reads uncommitted data |
| Non-repeatable read | Same row changes between reads |
| Phantom read | Matching row set changes |
| Lock | Controls conflicting access |
| Shared lock | Compatible read-oriented locking |
| Exclusive lock | Conflicting modification protection |
| Lock contention | Transactions compete for resources |
| Deadlock | Circular wait |
| MVCC | Multiple data versions for concurrency |
| Optimistic locking | Detect conflict with version/check |
| Pessimistic locking | Acquire lock before critical operation |
| Lost update | One concurrent update overwrites another |
| Transaction boundary | Defines atomic business unit |
| Long transaction | More contention/resource retention |
| Retry | Re-execute appropriate transient failure |
| Idempotency | Same logical request can safely be repeated |

______________________________________________________________________

# 62. Completion Checklist

Before moving to File 23, make sure you can explain:

- [ ] Transactions
- [ ] `BEGIN`
- [ ] `COMMIT`
- [ ] `ROLLBACK`
- [ ] ACID
- [ ] Atomicity
- [ ] Consistency
- [ ] Isolation
- [ ] Durability
- [ ] Transaction boundaries
- [ ] Long transactions
- [ ] External API calls and transactions
- [ ] Read Uncommitted
- [ ] Read Committed
- [ ] Repeatable Read
- [ ] Serializable
- [ ] Dirty reads
- [ ] Non-repeatable reads
- [ ] Phantom reads
- [ ] Shared locks
- [ ] Exclusive locks
- [ ] Lock granularity
- [ ] Lock contention
- [ ] Deadlocks
- [ ] Deadlock prevention
- [ ] Deadlock retries
- [ ] MVCC
- [ ] MVCC version cleanup
- [ ] Long-running MVCC transactions
- [ ] Optimistic locking
- [ ] Pessimistic locking
- [ ] Lost updates
- [ ] Atomic conditional updates
- [ ] Transaction retries
- [ ] Idempotency
- [ ] Transaction isolation selection
- [ ] ORM/application transaction boundaries
- [ ] Production concurrency trade-offs

______________________________________________________________________

# 63. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is a database transaction?
1. What does ACID stand for?
1. Explain atomicity.
1. Explain consistency.
1. Explain isolation.
1. Explain durability.
1. Atomicity vs consistency?
1. Give a real-world example where atomicity is required.
1. What is a transaction boundary?
1. Why should transactions generally be short?
1. What is Read Uncommitted?
1. What is Read Committed?
1. What is Repeatable Read?
1. What is Serializable?
1. What is a dirty read?
1. What is a non-repeatable read?
1. What is a phantom read?
1. Explain the difference between all three.
1. Which isolation level prevents dirty reads?
1. Can Read Committed have non-repeatable reads?
1. What is a database lock?
1. Shared vs exclusive lock?
1. What is lock contention?
1. What is a deadlock?
1. Give a concrete deadlock example.
1. How do you prevent deadlocks?
1. Why does consistent lock ordering help?
1. Should every database error be retried?
1. What is MVCC?
1. Does MVCC eliminate locks?
1. What are the benefits of MVCC?
1. What are the costs of MVCC?
1. How can long-running transactions affect MVCC?
1. What is optimistic locking?
1. What is pessimistic locking?
1. Compare optimistic and pessimistic locking.
1. What is a lost update?
1. How can you prevent lost updates?
1. Why is read-modify-write dangerous?
1. How can an atomic SQL update avoid a race?
1. Should you call an external API inside a database transaction?
1. Why can long transactions hurt throughput?
1. When might Serializable be appropriate?
1. Why shouldn't every operation use Serializable?
1. What is transaction retry?
1. What makes a transaction safely retriable?
1. Why is idempotency important for APIs?
1. How would you design an idempotent order endpoint?
1. How would you choose between optimistic and pessimistic locking?
1. Give a senior-level strategy for handling database concurrency in a Python backend.

If you can answer these confidently and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [21. SQL Indexes & Query Performance](./21-sql-indexes-performance.md)

**Next:** [23. SQLAlchemy Core](./23-sqlalchemy-core.md)

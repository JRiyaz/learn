# CAP Theorem

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Master CAP Theorem, understand why distributed systems must make trade-offs, and confidently answer CAP-related System Design interview questions.

______________________________________________________________________

# Introduction

One database

works well.

```
Application

↓

Database
```

Now suppose

we replicate

the database

across

multiple regions.

```
India

↓

USA

↓

Germany
```

Everything looks better.

Higher availability.

Lower latency.

But then

a network cable fails.

```
India

❌

USA
```

Now

the databases

cannot communicate.

What should happen?

Should they

continue accepting requests?

Or

should they stop

until communication

is restored?

This question

leads to

```
CAP Theorem
```

______________________________________________________________________

# What Is CAP Theorem?

CAP Theorem states that

a distributed system

cannot simultaneously guarantee

all three

of the following

during a network partition.

```
Consistency

Availability

Partition Tolerance
```

You can guarantee

at most

two

during a partition.

______________________________________________________________________

# What Does Each Letter Mean?

```
C

Consistency
```

```
A

Availability
```

```
P

Partition Tolerance
```

Let's understand

each one.

______________________________________________________________________

# Consistency (C)

Consistency means

every client

sees

the same data

at the same time.

Example

Suppose

your balance

is

```
₹1000
```

You transfer

₹500.

Immediately

every database

returns

```
₹500
```

Nobody

sees

old data.

______________________________________________________________________

# Availability (A)

Availability means

every request

receives

a response.

Even if

some servers

have failed.

Example

```
User

↓

Request

↓

Always

Gets Response
```

The response

may not

contain

the newest data,

but

the system

remains available.

______________________________________________________________________

# Partition Tolerance (P)

Partition

means

network failure.

Example

```
India

❌

Germany
```

Servers

cannot communicate.

Partition Tolerance

means

the system

continues operating

despite

network failures.

______________________________________________________________________

# Why Is Partition Tolerance Required?

In distributed systems,

network failures

are inevitable.

Examples

- Fiber cable cut
- Router failure
- Data center outage
- Cloud network issue

Large systems

must assume

partitions

will happen.

Therefore,

modern distributed systems

almost always

require

Partition Tolerance.

______________________________________________________________________

# Visual Example

Normal

```
Server A

⇄

Server B
```

Partition

```
Server A

❌

Server B
```

Communication

stops.

Now

the system

must decide.

______________________________________________________________________

# The Trade-Off

When a partition occurs,

you must choose

between

```
Consistency

or

Availability
```

Because

Partition Tolerance

is usually

non-negotiable.

______________________________________________________________________

# CP Systems

Choose

```
Consistency

+

Partition Tolerance
```

When a partition occurs,

some requests

may fail.

```
User

↓

Request

↓

Rejected

↓

Correct Data
```

Better

to reject

than

return

incorrect data.

______________________________________________________________________

# AP Systems

Choose

```
Availability

+

Partition Tolerance
```

Every request

receives

a response.

```
User

↓

Response

↓

Possibly Stale Data
```

Eventually

all replicas

synchronize.

______________________________________________________________________

# CA Systems

```
Consistency

+

Availability
```

Only possible

when

there is

no network partition.

In distributed systems,

partitions

are unavoidable,

so

true CA systems

are generally

limited

to single-node

or tightly coupled

deployments.

______________________________________________________________________

# Banking Example

Suppose

you transfer

₹10,000.

During

a network partition,

would you rather

```
Reject

the transaction
```

or

```
Allow

different balances?
```

Correct answer

```
Reject

the request
```

Banking

requires

Consistency.

Banking

is usually

```
CP
```

______________________________________________________________________

# Social Media Example

Suppose

someone likes

your photo.

Another user

doesn't see

the new like

for

2 seconds.

Acceptable?

Yes.

Social media

prefers

Availability.

```
AP
```

______________________________________________________________________

# WhatsApp Example

Sending messages

must remain

available.

A typing indicator

can tolerate

slight inconsistency.

Different features

within the same application

may make

different trade-offs.

______________________________________________________________________

# DNS Example

DNS

often favors

Availability.

Updates

may take time

to propagate.

Temporary

stale responses

are acceptable.

______________________________________________________________________

# Eventual Consistency

Very common

interview term.

Instead of

immediate consistency,

replicas

eventually

become consistent.

Example

```
Primary Updated

↓

Replica Updates

2 Seconds Later
```

Eventually

everyone

sees

the same data.

______________________________________________________________________

# Strong Consistency

Every read

returns

the latest write.

No stale data.

Usually

requires

coordination

between nodes.

Higher latency.

______________________________________________________________________

# Eventual vs Strong

| Strong | Eventual |
|----------|-----------|
| Latest data | May return stale data |
| Higher latency | Lower latency |
| Banking | Social Media |

______________________________________________________________________

# Why Not Always Use Strong Consistency?

Because

coordination

between

distributed nodes

takes time.

Latency increases.

Availability

may decrease

during partitions.

______________________________________________________________________

# CAP Decision

Suppose

network partition

occurs.

Choose

```
Reject Requests

↓

Consistency
```

OR

```
Serve Requests

↓

Availability
```

There is

no perfect answer.

Only

business requirements.

______________________________________________________________________

# Real Systems

Generally

| System | Preference |
|---------|------------|
| Banking | CP |
| Payment Gateway | CP |
| Hospital Records | CP |
| Inventory | CP |
| Social Media Feed | AP |
| Likes | AP |
| Comments | AP |
| DNS | AP |

Remember

individual features

within one application

may choose

different trade-offs.

______________________________________________________________________

# NoSQL And CAP

Many NoSQL databases

prioritize

Availability

and

Partition Tolerance.

Examples

- Cassandra
- DynamoDB
- Riak

Often

using

eventual consistency.

______________________________________________________________________

# SQL And CAP

Traditional relational databases

often emphasize

strong consistency.

Distributed SQL systems

introduce

their own

trade-offs

and coordination mechanisms.

Avoid saying

"All SQL databases are CP."

Instead,

discuss

the application's

consistency requirements.

______________________________________________________________________

# Interview Questions

## Is CAP only about databases?

No.

CAP applies

to

distributed systems

in general.

Databases

are

the most common example.

______________________________________________________________________

## What happens if there is no partition?

Without a partition,

systems

can often provide

both

consistency

and

availability.

CAP trade-offs

specifically arise

during

network partitions.

______________________________________________________________________

## Can one application be both CP and AP?

Yes.

Different services

or features

within the same application

can make

different choices.

Example

```
Payment

↓

CP
```

```
Recommendations

↓

AP
```

______________________________________________________________________

# PACELC (Interview Bonus)

Some interviewers

may ask

about

PACELC.

PACELC extends

CAP.

It says

```
If

Partition

↓

Choose

Availability

or

Consistency

Else

(No Partition)

↓

Choose

Latency

or

Consistency
```

In other words,

even without

network failures,

distributed systems

still make

trade-offs.

You don't need

deep knowledge

unless interviewing

for Staff-level roles,

but mentioning

PACELC

can leave

a strong impression.

______________________________________________________________________

# Common Mistakes

## Thinking CAP Means Choose Only Two Forever

Incorrect.

The trade-off

matters

during

network partitions.

______________________________________________________________________

## Ignoring Business Requirements

Business needs

determine

whether

Consistency

or

Availability

is more important.

______________________________________________________________________

## Assuming Every NoSQL Database Is AP

Different databases

make different trade-offs

and often

offer configurable

consistency levels.

______________________________________________________________________

## Assuming SQL Solves Everything

Distributed SQL

also faces

CAP trade-offs.

______________________________________________________________________

# Best Practices

✅ Start with business requirements.

✅ Assume partitions will happen.

✅ Explain the consistency requirements.

✅ Discuss eventual consistency where appropriate.

✅ Mention trade-offs instead of absolutes.

______________________________________________________________________

# Interview Deep Dive

## Question

What is CAP Theorem?

### Answer

CAP Theorem states that during a network partition, a distributed system can provide either Consistency or Availability,
but not both simultaneously, while continuing to tolerate the partition.

______________________________________________________________________

## Question

Why is Partition Tolerance usually required?

### Answer

Because network failures are unavoidable in distributed systems. Applications deployed across multiple servers, data
centers, or cloud regions must continue operating despite communication failures.

______________________________________________________________________

## Question

Why do social media platforms often prefer eventual consistency?

### Answer

Small delays in propagating updates, such as likes or comments, usually do not significantly impact the user experience.
Prioritizing availability allows the platform to continue serving users even during network disruptions.

______________________________________________________________________

# Practice Exercise

For each application,

decide

whether

Consistency

or

Availability

is more important

during a partition.

Applications

1. Banking System
1. ATM Network
1. WhatsApp Messages
1. Instagram Feed
1. Netflix
1. Online Shopping Cart
1. Hospital Records
1. Airline Reservation System
1. Food Delivery Tracking
1. DNS

Explain

your reasoning

for each.

______________________________________________________________________

# Summary

CAP Theorem is one of the most important concepts in distributed systems.

It teaches us that

during a network partition,

we must choose

between

- Strong consistency
- High availability

The correct choice

depends entirely

on business requirements.

Senior engineers

don't memorize

CP

or

AP.

They explain

**why**

a particular trade-off

fits the application.

______________________________________________________________________

# Next

[Consistent Hashing](15-consistent-hashing.md)

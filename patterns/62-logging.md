# System Design - Part 62

# Logging

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Logging is
- Why Logging is important
- Log Levels
- Structured Logging
- Centralized Logging
- Log Aggregation
- Log Rotation
- Correlation IDs
- ELK Stack
- FastAPI examples
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

is running

in production.

One day,

a customer reports

that

they cannot

borrow books.

Question.

How do you

find

what happened?

You weren't

watching

the server

when

the problem

occurred.

The answer is

**Logs.**

______________________________________________________________________

# The Problem

Suppose

your application

throws

an exception.

```text id="log6201"
500 Internal Server Error
```

The user

sees

an error.

But

why

did it happen?

Without logs,

you have

almost no clue.

______________________________________________________________________

# Another Problem

Suppose

you have

100 application servers.

```text id="log6202"
Server 1

Server 2

...

Server 100
```

A bug

appears

only

on

Server 73.

Where

do you look?

Reading

100 log files

manually

isn't practical.

______________________________________________________________________

# What is Logging?

**Logging**

is the process

of recording

events,

errors,

and important

application activity

for debugging,

monitoring,

auditing,

and troubleshooting.

______________________________________________________________________

# Example

Suppose

a member

borrows

a book.

Instead of

simply

processing

the request,

record

a log.

```text id="log6203"
INFO

Member 101

borrowed

Book 502
```

Later,

developers

can understand

what happened.

______________________________________________________________________

# Why Logging Matters

Logs help us:

- Debug issues
- Investigate incidents
- Monitor systems
- Audit user actions
- Understand application behavior

Without logs,

production debugging

becomes

extremely difficult.

______________________________________________________________________

# Log Levels

Interview favorite.

Most logging systems

support

different severity levels.

______________________________________________________________________

## DEBUG

Very detailed

information

used

during development.

Example

```text id="log6204"
Loading user profile...
```

Usually

disabled

in production.

______________________________________________________________________

## INFO

Normal

application events.

Example

```text id="log6205"
Book borrowed successfully.
```

______________________________________________________________________

## WARNING

Something

unexpected happened,

but

the application

continues.

Example

```text id="log6206"
Cache unavailable.

Using database.
```

______________________________________________________________________

## ERROR

An operation

failed.

Example

```text id="log6207"
Payment processing failed.
```

______________________________________________________________________

## CRITICAL

The application

cannot

continue safely.

Example

```text id="log6208"
Database connection lost.
```

Immediate action

is required.

______________________________________________________________________

# Structured Logging

Instead of

plain text,

modern applications

use

structured logs.

Example

```json id="log6209"
{
  "level": "INFO",
  "service": "loan-service",
  "member_id": 101,
  "book_id": 502,
  "request_id": "abc123"
}
```

Structured logs

are easier

to search,

filter,

and analyze.

______________________________________________________________________

# Bad Logging

Example

```text id="log6210"
Something failed.
```

This tells

developers

almost nothing.

______________________________________________________________________

# Better Logging

Example

```text id="log6211"
Payment failed

PaymentID=1024

UserID=89

Reason=Timeout
```

Now

developers

can investigate

the issue.

______________________________________________________________________

# Centralized Logging

Suppose

you have

100 servers.

Each server

creates logs.

Instead of

logging locally,

send

all logs

to

one platform.

```text id="log6212"
App 1

↓

Log Server
```

```text id="log6213"
App 2

↓

Log Server
```

Developers

search

one place.

______________________________________________________________________

# ELK Stack

One of

the most common

logging stacks.

```text id="log6214"
Elasticsearch

↓

Logstash

↓

Kibana
```

Components:

- Logstash collects logs
- Elasticsearch stores logs
- Kibana visualizes logs

______________________________________________________________________

# Fluentd / Fluent Bit

Modern Kubernetes

deployments

often use:

- Fluentd
- Fluent Bit

These tools

collect logs

from containers

and

forward them

to

Elasticsearch,

OpenSearch,

or cloud logging systems.

______________________________________________________________________

# Correlation ID

Interview favorite.

Suppose

one request

passes through

five microservices.

```text id="log6215"
Gateway

↓

Loan Service

↓

Payment Service

↓

Notification Service
```

How do

we identify

all logs

belonging

to

the same request?

Use

a

**Correlation ID.**

Example

```text id="log6216"
Request-ID

abc123
```

Every service

logs

the same ID.

______________________________________________________________________

# Log Rotation

Logs

grow

continuously.

Eventually,

they consume

disk space.

Log Rotation

creates

new log files

periodically

and

archives

old ones.

Example

```text id="log6217"
app.log

↓

app.log.1

↓

app.log.2
```

______________________________________________________________________

# Log Retention

Organizations

don't keep

logs forever.

Example

```text id="log6218"
Keep Logs

30 Days
```

After that,

logs

are archived

or deleted.

______________________________________________________________________

# Sensitive Data

Never log:

- Passwords
- Credit Card Numbers
- OTPs
- API Secrets
- Access Tokens

Logs

are often

accessible

to many engineers.

Protect

customer data.

______________________________________________________________________

# FastAPI Example

Instead of

printing

messages,

use

a logger.

```python id="log6219"
logger.info(
    "Book borrowed",
    extra={
        "member_id": 101,
        "book_id": 502
    }
)
```

This produces

structured logs.

______________________________________________________________________

# Kubernetes Example

Containers

write logs

to

stdout/stderr.

Kubernetes

collects

these logs,

and

logging agents

forward them

to

a centralized

logging platform.

Applications

should not

manage

log files

inside containers.

______________________________________________________________________

# AI/ML Example

Suppose

an LLM request

fails.

Useful logs

include:

- Request ID
- Model Name
- Token Count
- Processing Time
- Error Reason

Do **not**

log

the entire prompt

if

it contains

sensitive information.

______________________________________________________________________

# Real Backend Example

Suppose

an order

fails.

Logs

from

multiple services

share

the same

Correlation ID.

Developers

can reconstruct

the entire request

across

the distributed system.

______________________________________________________________________

# Logging vs Monitoring

Interview favorite.

| Logging | Monitoring |
| ------------------- | --------------------- |
| Detailed events | Overall system health |
| Individual requests | Aggregated metrics |
| Debugging | Alerting |

You need

both.

______________________________________________________________________

# Logging vs Tracing

| Logging | Tracing |
| --------------------- | ------------------------ |
| Individual events | Entire request journey |
| Local service context | Cross-service visibility |

We'll study

Distributed Tracing

later.

______________________________________________________________________

# Benefits

Logging provides:

✅ Easier debugging

✅ Incident investigation

✅ Auditing

✅ Production visibility

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Storage costs

❌ Search complexity

❌ Performance overhead

if

logging excessively

______________________________________________________________________

# When NOT to Log

Avoid logging:

- Passwords
- Authentication tokens
- Personally identifiable information (PII)
- Large binary data

Log

only

what helps

operate

the system safely.

______________________________________________________________________

# Best Practices

✅ Use structured logging.

✅ Include Correlation IDs.

✅ Use appropriate log levels.

✅ Centralize logs.

______________________________________________________________________

# Common Mistakes

### Using print()

Production applications

should use

logging frameworks,

not

`print()` statements.

______________________________________________________________________

### Logging Everything

Excessive logging

increases:

- Storage
- Cost
- Noise

Log

meaningful events.

______________________________________________________________________

### Missing Context

Logs

without

request IDs,

user IDs,

or

service names

are much harder

to investigate.

______________________________________________________________________

### Logging Secrets

Never expose

credentials,

tokens,

or

customer-sensitive data

in logs.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is structured logging preferred over plain text logging?

Structured logging stores log data in a machine-readable format, typically JSON, where fields such as timestamp, log
level, request ID, user ID, and service name are stored separately. This makes logs easy to search, filter, aggregate,
and analyze using tools like Elasticsearch and Kibana. In distributed systems, structured logging combined with
Correlation IDs enables engineers to trace requests across multiple microservices quickly, making debugging and incident
response significantly more effective than plain text logs.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Logging is
- Log Levels
- Structured Logging
- Centralized Logging
- ELK Stack
- Correlation IDs
- Log Rotation
- FastAPI example
- Kubernetes example
- Best practices

______________________________________________________________________

# 🧠 Observability Progress

You have started the **Observability** module:

- ✅ Logging

Next, we'll learn **Monitoring & Metrics**, where we'll measure system health, latency, throughput, error rates, and
create production alerts before customers notice problems.

______________________________________________________________________

# What's Next

[Monitoring & Metrics](63-monitoring-and-metrics.md)

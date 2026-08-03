# System Design - Part 63

# Monitoring & Metrics

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Monitoring is
- Why Monitoring is important
- Metrics
- Time Series Data
- The Four Golden Signals
- RED Method
- USE Method
- Dashboards
- Alerting
- Prometheus & Grafana
- FastAPI examples
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

is running

perfectly.

Suddenly,

users complain

that

the website

is slow.

Question.

How do you know

whether

the problem is:

- CPU?
- Database?
- Network?
- Cache?
- Load Balancer?

Logs

help explain

**what happened**.

Monitoring

helps answer

**what is happening right now**.

______________________________________________________________________

# The Problem

Suppose

your application

crashes

at

2:00 AM.

Nobody

is watching

the server.

How do

you know

it happened?

Without monitoring,

you usually learn

from

your customers.

That's too late.

______________________________________________________________________

# What is Monitoring?

**Monitoring**

is the continuous

observation

of a system's health,

performance,

and availability

using

metrics,

dashboards,

and alerts.

Its goal is

to detect

problems

before

users are affected.

______________________________________________________________________

# What is a Metric?

A **Metric**

is

a numerical value

that changes

over time.

Examples:

- CPU Usage
- Memory Usage
- Requests Per Second
- Error Rate
- Response Time

Metrics

are collected

continuously.

______________________________________________________________________

# Time Series Data

Metrics

are stored

with

timestamps.

Example

```text id="mon6301"
10:00

CPU = 25%
```

```text id="mon6302"
10:01

CPU = 31%
```

```text id="mon6303"
10:02

CPU = 42%
```

This is called

**Time Series Data.**

______________________________________________________________________

# Monitoring Architecture

```text id="mon6304"
Application

↓

Metrics

↓

Prometheus

↓

Grafana

↓

Dashboard
```

Applications

expose metrics.

Monitoring systems

collect

and visualize them.

______________________________________________________________________

# Types of Metrics

Infrastructure Metrics

- CPU
- Memory
- Disk
- Network

Application Metrics

- Request Count
- Latency
- Errors
- Active Users

Business Metrics

- Orders Per Minute
- Revenue
- New Registrations

______________________________________________________________________

# Why Business Metrics Matter

Suppose

CPU

looks normal.

Memory

looks normal.

Latency

looks normal.

But

orders

drop

by

80%.

Infrastructure

appears healthy,

but

the business

isn't.

Good monitoring

includes

business metrics.

______________________________________________________________________

# The Four Golden Signals

Interview favorite.

According to

Google SRE,

every service

should monitor

four signals.

______________________________________________________________________

## 1. Latency

How long

does

a request

take?

Example

```text id="mon6305"
GET /books

120 ms
```

Increasing latency

often indicates

an emerging problem.

______________________________________________________________________

## 2. Traffic

How much

work

is the system

handling?

Examples:

- Requests/sec
- Users
- Messages/sec

______________________________________________________________________

## 3. Errors

How many requests

fail?

Example

```text id="mon6306"
HTTP 500

2%
```

Error rate

should remain

very low.

______________________________________________________________________

## 4. Saturation

How close

is the system

to

its limits?

Examples:

- CPU = 95%
- Memory = 92%
- Queue Length = 50,000

High saturation

means

capacity

is running out.

______________________________________________________________________

# RED Method

Interview favorite.

For APIs,

monitor:

**R**

Rate

↓

Requests/sec

**E**

Errors

↓

Failure Rate

**D**

Duration

↓

Latency

RED

is commonly used

for

microservices.

______________________________________________________________________

# USE Method

For infrastructure,

monitor:

**U**

Utilization

↓

CPU Usage

**S**

Saturation

↓

Queue Length

**E**

Errors

↓

Disk Failures

USE

helps identify

resource bottlenecks.

______________________________________________________________________

# Dashboards

Metrics

are displayed

using dashboards.

Example

```text id="mon6307"
CPU

Memory

Latency

Errors
```

Dashboards

provide

a real-time

view

of

system health.

______________________________________________________________________

# Prometheus

Prometheus

is

one of

the most popular

monitoring systems.

Features:

- Time-series database
- Metric collection
- Alert rules
- PromQL queries

Applications

expose metrics

through

an endpoint.

Example

```text id="mon6308"
/metrics
```

______________________________________________________________________

# Grafana

Grafana

connects

to

Prometheus

and

creates

interactive dashboards.

Typical graphs:

- CPU usage
- Request latency
- Error rate
- Database connections

______________________________________________________________________

# Alerting

Monitoring

without alerts

is incomplete.

Suppose

CPU

reaches

95%.

Trigger

an alert.

Example

```text id="mon6309"
CPU > 90%

5 Minutes

↓

Notify On-Call
```

Alerts

should be

actionable.

______________________________________________________________________

# Good Alerts

Example

```text id="mon6310"
Error Rate

> 5%

for 10 Minutes
```

This

is meaningful.

______________________________________________________________________

# Bad Alerts

Example

```text id="mon6311"
CPU

85%

for

5 Seconds
```

This creates

alert fatigue.

Temporary spikes

are normal.

______________________________________________________________________

# FastAPI Example

Suppose

your API

exposes

metrics.

```python id="mon6312"
GET /metrics
```

Prometheus

scrapes

this endpoint

every

15 seconds.

______________________________________________________________________

# Kubernetes Example

Kubernetes

provides

metrics

for:

- Pods
- Nodes
- Deployments
- CPU
- Memory

Prometheus

collects

these metrics,

while

Grafana

visualizes them.

______________________________________________________________________

# AI/ML Example

Suppose

an LLM service.

Useful metrics

include:

- Tokens/sec
- Prompt latency
- Completion latency
- GPU utilization
- Requests/sec
- Failed inference requests

Monitoring

helps detect

GPU bottlenecks

before

users notice.

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce platform.

A dashboard

shows:

- Checkout latency
- Orders/minute
- Payment failures
- Active users
- Inventory API latency

Operations teams

identify

production issues

within minutes.

______________________________________________________________________

# Monitoring vs Logging

Interview favorite.

| Monitoring | Logging |
| ----------------- | ----------------- |
| Numerical metrics | Detailed events |
| Detects problems | Explains problems |
| Real-time health | Request details |

Both

work together.

______________________________________________________________________

# Monitoring vs Tracing

| Monitoring | Tracing |
| ------------------ | -------------------------- |
| Overall health | Individual request journey |
| Aggregated metrics | End-to-end request path |

Tracing

will be covered

next.

______________________________________________________________________

# Benefits

Monitoring provides:

✅ Early problem detection

✅ Capacity planning

✅ Performance visibility

✅ Faster incident response

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Infrastructure cost

❌ Metric storage

❌ Alert tuning

❌ Dashboard maintenance

______________________________________________________________________

# Service Level Indicators (SLIs)

An **SLI**

measures

service performance.

Examples:

- Availability
- Latency
- Error Rate

SLIs

are

raw measurements.

______________________________________________________________________

# Service Level Objectives (SLOs)

An **SLO**

defines

the target

for an SLI.

Example

```text id="mon6313"
99.9%

Availability
```

If

the service

drops below

the target,

it violates

its SLO.

______________________________________________________________________

# Service Level Agreements (SLAs)

An **SLA**

is

a contractual commitment

to customers.

Example

```text id="mon6314"
99.95%

Monthly Availability
```

Unlike

an SLO,

an SLA

may include

financial penalties

if

targets

are missed.

______________________________________________________________________

# When NOT to Monitor

Never

collect

every possible metric.

Too many metrics

increase:

- Storage cost
- Processing cost
- Dashboard complexity

Monitor

metrics

that help

operate

the system.

______________________________________________________________________

# Best Practices

✅ Monitor

the Four Golden Signals.

✅ Build

business dashboards.

✅ Create

meaningful alerts.

✅ Review

metrics regularly.

______________________________________________________________________

# Common Mistakes

### Monitoring Only Infrastructure

Healthy servers

don't guarantee

healthy business operations.

Include

business metrics.

______________________________________________________________________

### Alert Fatigue

Too many

low-quality alerts

cause engineers

to ignore

important ones.

______________________________________________________________________

### No Baseline

Without

historical metrics,

it's difficult

to determine

whether

today's performance

is normal.

______________________________________________________________________

### Ignoring Trends

A gradual increase

in latency

often indicates

future failures.

Trend analysis

is as important

as

real-time monitoring.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is monitoring, and how is it different from logging?

Monitoring is the continuous collection and analysis of numerical metrics that describe the health and performance of a
system. It helps detect problems in real time using dashboards and alerts. Logging, on the other hand, records detailed
application events that help engineers investigate and debug issues after they occur. Monitoring answers "Is the system
healthy?", while logging answers "Why did this specific request fail?". Together, they form two essential pillars of
observability.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Monitoring is
- Metrics
- Time Series Data
- The Four Golden Signals
- RED Method
- USE Method
- Prometheus
- Grafana
- Alerting
- SLIs, SLOs, and SLAs
- Best practices

______________________________________________________________________

# 🧠 Observability Progress

You now understand:

- ✅ Logging
- ✅ Monitoring & Metrics

One final observability topic remains:

> **Distributed Tracing**, which allows you to follow a single request as it travels across dozens of microservices.

______________________________________________________________________

# What's Next

[Distributed Tracing](64-distributed-tracing.md)

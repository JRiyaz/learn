# Celery Masterclass for Backend Engineers

## File 19 – Celery Beat, Periodic Tasks & Production Scheduling

> **Course Level:** Intermediate → Advanced
>
> So far, every Celery task has been triggered by an event.
>
> Examples:
>
> - User uploads an image
> - Customer places an order
> - Payment succeeds
> - Email is sent
>
> But many production tasks are **not triggered by users**.
>
> Instead, they run automatically.
>
> Examples:
>
> - Every day at midnight
> - Every Monday at 9 AM
> - Every 5 minutes
> - Every hour
> - On the first day of every month
>
> Celery provides **Celery Beat** for this purpose.

______________________________________________________________________

# Learning Objectives

By the end of this chapter, you will be able to:

- Understand Celery Beat.
- Understand periodic tasks.
- Configure interval schedules.
- Configure cron schedules.
- Understand Beat architecture.
- Design production scheduling systems.
- Avoid duplicate scheduled executions.
- Compare Celery Beat with Cron Jobs.

______________________________________________________________________

# Table of Contents

1. Why Scheduling Exists
1. What is Celery Beat?
1. Beat Architecture
1. Periodic Tasks
1. Interval Scheduling
1. Cron Scheduling
1. Solar Scheduling
1. Beat Scheduler
1. Production Deployment
1. Celery Beat vs Cron
1. Best Practices
1. Summary
1. Key Takeaways
1. Interview Deep Dive
1. Practice Questions
1. Mini Assignment
1. Common Mistakes
1. What's Next?

______________________________________________________________________

# Why Scheduling Exists

Imagine a banking application.

Every night,

the system should

```
Generate Statements

↓

Backup Database

↓

Archive Logs

↓

Generate Reports
```

Nobody clicks a button.

The work happens automatically.

______________________________________________________________________

Another example

Every hour

```
Sync Exchange Rates
```

______________________________________________________________________

Every Monday

```
Generate Payroll
```

______________________________________________________________________

Every month

```
Send Subscription Invoice
```

These are

**Scheduled Tasks**.

______________________________________________________________________

# What is Celery Beat?

Celery Beat

is a scheduler.

It does **not execute tasks**.

Instead,

it decides

**when**

tasks should be executed.

______________________________________________________________________

Think of it like

```
Alarm Clock
```

It wakes Workers

at the correct time.

______________________________________________________________________

# Celery Beat Architecture

```
                Celery Beat

                     │

      Time Reached?

                     │

                     ▼

              RabbitMQ Broker

                     │

                     ▼

             Celery Workers

                     │

                     ▼

             Execute Task
```

Notice

Beat

never executes Python code.

Workers still do the work.

______________________________________________________________________

# Important Misconception

Many developers think

```
Beat

↓

Runs Task
```

Wrong.

Beat only publishes tasks.

Workers execute them.

Exactly like

FastAPI publishes tasks.

______________________________________________________________________

# Periodic Tasks

A periodic task

runs automatically.

Example

```
Every Hour

↓

Sync Exchange Rates
```

______________________________________________________________________

Another

```
Daily

↓

Clean Temporary Files
```

______________________________________________________________________

Another

```
Weekly

↓

Generate Reports
```

______________________________________________________________________

# Configuring Beat

Example

```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    "daily-report": {
        "task": "tasks.generate_report",
        "schedule": crontab(hour=0, minute=0),
    }
}
```

Meaning

```
Every Day

00:00
```

Publish

```
generate_report
```

______________________________________________________________________

# Interval Scheduling

Run every

```
10 Seconds
```

```python
schedule = 10.0
```

______________________________________________________________________

Run every

```
5 Minutes
```

```python
schedule = 300.0
```

______________________________________________________________________

Timeline

```
10:00

↓

Run

↓

10:05

↓

Run

↓

10:10

↓

Run
```

______________________________________________________________________

# Interval Use Cases

Good for

- Cache cleanup
- Heartbeats
- Polling APIs
- Sync jobs
- Health checks

______________________________________________________________________

# Cron Scheduling

Cron scheduling

runs at

specific calendar times.

Example

Every day

```
9:00 AM
```

```python
crontab(
    hour=9,
    minute=0
)
```

______________________________________________________________________

Every Monday

```
8:00 AM
```

```python
crontab(
    hour=8,
    minute=0,
    day_of_week=1
)
```

______________________________________________________________________

Every first day

of the month

```
Midnight
```

```python
crontab(
    day_of_month=1,
    hour=0,
    minute=0
)
```

______________________________________________________________________

# Cron Examples

Daily Backup

```
00:00
```

______________________________________________________________________

Weekly Report

```
Monday

08:00
```

______________________________________________________________________

Monthly Invoice

```
Day 1

09:00
```

______________________________________________________________________

Every 15 Minutes

```python
crontab(minute="*/15")
```

______________________________________________________________________

# Solar Scheduling

Celery also supports

Solar Events.

Examples

```
Sunrise

Sunset

Dawn

Dusk
```

Useful for

- IoT
- Agriculture
- Lighting
- Energy systems

Much less common in business applications.

______________________________________________________________________

# Beat Scheduler

Internally,

Beat continuously checks

```
Current Time

↓

Task Schedule

↓

Should Run?

↓

Publish Task
```

Workers remain unchanged.

______________________________________________________________________

# Complete Flow

```
09:00

↓

Beat

↓

Publish

↓

RabbitMQ

↓

Worker

↓

Execute
```

______________________________________________________________________

# Multiple Scheduled Tasks

Example

```
00:00

↓

Backup

-------------------

01:00

↓

Cleanup

-------------------

09:00

↓

Generate Report

-------------------

Every Hour

↓

Exchange Rate Sync
```

Beat manages all of them.

______________________________________________________________________

# Production Deployment

Typical architecture

```
            Celery Beat

                 │

                 ▼

             RabbitMQ

                 │

        ┌────────┼────────┐

        ▼        ▼        ▼

    Worker1   Worker2   Worker3
```

Only

one Beat

should publish schedules.

Many Workers

can execute them.

______________________________________________________________________

# Why Only One Beat?

Suppose

```
Beat A

↓

Generate Invoice
```

and

```
Beat B

↓

Generate Invoice
```

Both publish

the same task.

Result

```
Duplicate Invoice
```

Production deployments

usually run

**one Beat instance**.

______________________________________________________________________

# High Availability

Need high availability?

Don't run multiple independent Beat instances.

Instead,

use a scheduler that supports leader election

or ensure only one Beat instance is active at a time.

The goal is

```
One Scheduler

Many Workers
```

______________________________________________________________________

# Celery Beat vs Cron

Many people ask

```
Why not Cron?
```

Let's compare.

______________________________________________________________________

Cron

```
Runs Shell Commands
```

______________________________________________________________________

Beat

```
Publishes Celery Tasks
```

______________________________________________________________________

Cron

```
Single Machine
```

______________________________________________________________________

Beat

```
Distributed Workers
```

______________________________________________________________________

Cron

```
No Queue
```

______________________________________________________________________

Beat

```
Uses RabbitMQ
```

______________________________________________________________________

Comparison

| Cron | Celery Beat |
|------|-------------|
| OS Scheduler | Celery Scheduler |
| Runs Commands | Publishes Tasks |
| Single Server | Distributed |
| Limited Scaling | Horizontally Scalable |
| No Task Queue | Uses Broker |

______________________________________________________________________

# Production Example

E-commerce Platform

Every Night

```
Backup Database
```

Every Hour

```
Sync Inventory
```

Every Day

```
Generate Sales Report
```

Every Month

```
Generate Customer Invoice
```

Every Minute

```
Clear Expired OTP
```

Every one

is a Beat task.

______________________________________________________________________

# Another Example

Food Delivery App

Every

```
30 Seconds
```

```
Check Driver Location
```

Every

```
10 Minutes
```

```
Expire Pending Orders
```

Every

```
Night

↓

Generate Daily Report
```

______________________________________________________________________

# Best Practices

✔ Run only one Beat scheduler.

✔ Keep scheduled tasks idempotent.

✔ Keep Beat lightweight.

✔ Use Cron for calendar schedules.

✔ Use Intervals for repeated polling.

✔ Monitor failed scheduled tasks.

✔ Log every scheduled execution.

______________________________________________________________________

# Summary

Celery Beat is a scheduling service that publishes Celery tasks at predefined intervals or calendar times.

Beat does not execute tasks.

Workers continue to execute all Python code.

Together,

Beat,

RabbitMQ,

and Workers

form a complete distributed scheduling system.

______________________________________________________________________

# Key Takeaways

- Beat schedules tasks.
- Workers execute tasks.
- Interval schedules repeat after fixed durations.
- Cron schedules run at calendar times.
- Only one Beat scheduler should publish schedules.
- Scheduled tasks should be idempotent.
- Beat integrates naturally with RabbitMQ.
- Cron and Beat solve different problems.

______________________________________________________________________

# Interview Deep Dive

## Question 1

### What is Celery Beat?

#### Answer

Celery Beat is a scheduler that publishes Celery tasks according to predefined schedules. It does not execute tasks
itself; Workers consume and execute the published tasks.

______________________________________________________________________

## Question 2

### What is the difference between Beat and a Worker?

#### Answer

Beat decides when tasks should run and publishes them to the Broker. Workers consume those tasks from the Broker and
execute the corresponding Python functions.

______________________________________________________________________

## Question 3

### Why should only one Beat instance run?

#### Answer

Running multiple independent Beat instances can cause duplicate task publication, resulting in tasks executing multiple
times. Production systems typically ensure only one active scheduler.

______________________________________________________________________

## Question 4

### When should you use Interval scheduling?

#### Answer

Use Interval scheduling for recurring tasks that repeat after a fixed duration, such as health checks, polling APIs,
cache cleanup, or periodic synchronization.

______________________________________________________________________

## Question 5

### When should you use Cron scheduling?

#### Answer

Use Cron scheduling when tasks must execute at specific calendar times, such as daily reports, weekly payroll, monthly
billing, or nightly backups.

______________________________________________________________________

## Question 6

### What is the difference between Cron and Celery Beat?

#### Answer

Cron is an operating system scheduler that executes commands on a single machine. Celery Beat is an application-level
scheduler that publishes distributed Celery tasks through a message broker for execution by Workers.

______________________________________________________________________

## Question 7

### Why should scheduled tasks be idempotent?

#### Answer

Scheduled tasks may be retried or accidentally published more than once. Idempotency ensures repeated executions produce
the same final result without unwanted side effects.

______________________________________________________________________

# Practice Questions

1. What is Celery Beat?
1. Why doesn't Beat execute tasks?
1. Compare Beat and Workers.
1. Explain Interval scheduling.
1. Explain Cron scheduling.
1. Why should only one Beat instance exist?
1. Compare Cron and Beat.
1. Design a scheduling system for an online bank.
1. Which tasks should use Interval scheduling?
1. Which tasks should use Cron scheduling?

______________________________________________________________________

# Mini Assignment

Design the scheduling system for a SaaS platform.

Requirements:

- Daily backup at 2:00 AM
- Generate invoices on the 1st of every month
- Sync exchange rates every hour
- Clean expired sessions every 15 minutes
- Send weekly usage reports every Monday
- Archive logs every night

For each task, specify:

- Interval or Cron?
- Expected execution frequency
- Queue
- Worker Pool
- Retry policy
- Idempotency strategy

Explain your design.

______________________________________________________________________

# Common Mistakes

❌ Running multiple Beat schedulers without coordination.

❌ Assuming Beat executes tasks.

❌ Using Interval scheduling for calendar-based jobs.

❌ Using Cron scheduling for simple polling tasks.

❌ Forgetting idempotency for recurring jobs.

❌ Scheduling CPU-intensive and lightweight tasks on the same Worker pool.

______________________________________________________________________

# What's Next?

Now you've mastered task scheduling.

The next chapter covers one of the most important production topics:

- Celery Worker Concurrency
- Worker Pools
- Prefork
- Threads
- Eventlet
- Gevent
- Autoscaling
- Queue Routing
- Performance Tuning
- Production Deployment Strategies

➡ **Next File:** [File 20 – Worker Pools, Concurrency & Performance Tuning](20-worker-concurrency.md)

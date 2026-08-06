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

---

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

---

# Table of Contents

1. Why Scheduling Exists
2. What is Celery Beat?
3. Beat Architecture
4. Periodic Tasks
5. Interval Scheduling
6. Cron Scheduling
7. Solar Scheduling
8. Beat Scheduler
9. Production Deployment
10. Celery Beat vs Cron
11. Best Practices
12. Summary
13. Key Takeaways
14. Interview Deep Dive
15. Practice Questions
16. Mini Assignment
17. Common Mistakes
18. What's Next?

---

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

---

Another example

Every hour

```
Sync Exchange Rates
```

---

Every Monday

```
Generate Payroll
```

---

Every month

```
Send Subscription Invoice
```

These are

**Scheduled Tasks**.

---

# What is Celery Beat?

Celery Beat

is a scheduler.

It does **not execute tasks**.

Instead,

it decides

**when**

tasks should be executed.

---

Think of it like

```
Alarm Clock
```

It wakes Workers

at the correct time.

---

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

---

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

---

# Periodic Tasks

A periodic task

runs automatically.

Example

```
Every Hour

↓

Sync Exchange Rates
```

---

Another

```
Daily

↓

Clean Temporary Files
```

---

Another

```
Weekly

↓

Generate Reports
```

---

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

---

# Interval Scheduling

Run every

```
10 Seconds
```

```python
schedule = 10.0
```

---

Run every

```
5 Minutes
```

```python
schedule = 300.0
```

---

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

---

# Interval Use Cases

Good for

- Cache cleanup
- Heartbeats
- Polling APIs
- Sync jobs
- Health checks

---

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

---

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

---

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

---

# Cron Examples

Daily Backup

```
00:00
```

---

Weekly Report

```
Monday

08:00
```

---

Monthly Invoice

```
Day 1

09:00
```

---

Every 15 Minutes

```python
crontab(minute="*/15")
```

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

# Celery Beat vs Cron

Many people ask

```
Why not Cron?
```

Let's compare.

---

Cron

```
Runs Shell Commands
```

---

Beat

```
Publishes Celery Tasks
```

---

Cron

```
Single Machine
```

---

Beat

```
Distributed Workers
```

---

Cron

```
No Queue
```

---

Beat

```
Uses RabbitMQ
```

---

Comparison

| Cron | Celery Beat |
|------|-------------|
| OS Scheduler | Celery Scheduler |
| Runs Commands | Publishes Tasks |
| Single Server | Distributed |
| Limited Scaling | Horizontally Scalable |
| No Task Queue | Uses Broker |

---

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

---

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

---

# Best Practices

✔ Run only one Beat scheduler.

✔ Keep scheduled tasks idempotent.

✔ Keep Beat lightweight.

✔ Use Cron for calendar schedules.

✔ Use Intervals for repeated polling.

✔ Monitor failed scheduled tasks.

✔ Log every scheduled execution.

---

# Summary

Celery Beat is a scheduling service that publishes Celery tasks at predefined intervals or calendar times.

Beat does not execute tasks.

Workers continue to execute all Python code.

Together,

Beat,

RabbitMQ,

and Workers

form a complete distributed scheduling system.

---

# Key Takeaways

- Beat schedules tasks.
- Workers execute tasks.
- Interval schedules repeat after fixed durations.
- Cron schedules run at calendar times.
- Only one Beat scheduler should publish schedules.
- Scheduled tasks should be idempotent.
- Beat integrates naturally with RabbitMQ.
- Cron and Beat solve different problems.

---

# Interview Deep Dive

## Question 1

### What is Celery Beat?

#### Answer

Celery Beat is a scheduler that publishes Celery tasks according to predefined schedules. It does not execute tasks itself; Workers consume and execute the published tasks.

---

## Question 2

### What is the difference between Beat and a Worker?

#### Answer

Beat decides when tasks should run and publishes them to the Broker. Workers consume those tasks from the Broker and execute the corresponding Python functions.

---

## Question 3

### Why should only one Beat instance run?

#### Answer

Running multiple independent Beat instances can cause duplicate task publication, resulting in tasks executing multiple times. Production systems typically ensure only one active scheduler.

---

## Question 4

### When should you use Interval scheduling?

#### Answer

Use Interval scheduling for recurring tasks that repeat after a fixed duration, such as health checks, polling APIs, cache cleanup, or periodic synchronization.

---

## Question 5

### When should you use Cron scheduling?

#### Answer

Use Cron scheduling when tasks must execute at specific calendar times, such as daily reports, weekly payroll, monthly billing, or nightly backups.

---

## Question 6

### What is the difference between Cron and Celery Beat?

#### Answer

Cron is an operating system scheduler that executes commands on a single machine. Celery Beat is an application-level scheduler that publishes distributed Celery tasks through a message broker for execution by Workers.

---

## Question 7

### Why should scheduled tasks be idempotent?

#### Answer

Scheduled tasks may be retried or accidentally published more than once. Idempotency ensures repeated executions produce the same final result without unwanted side effects.

---

# Practice Questions

1. What is Celery Beat?
2. Why doesn't Beat execute tasks?
3. Compare Beat and Workers.
4. Explain Interval scheduling.
5. Explain Cron scheduling.
6. Why should only one Beat instance exist?
7. Compare Cron and Beat.
8. Design a scheduling system for an online bank.
9. Which tasks should use Interval scheduling?
10. Which tasks should use Cron scheduling?

---

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

---

# Common Mistakes

❌ Running multiple Beat schedulers without coordination.

❌ Assuming Beat executes tasks.

❌ Using Interval scheduling for calendar-based jobs.

❌ Using Cron scheduling for simple polling tasks.

❌ Forgetting idempotency for recurring jobs.

❌ Scheduling CPU-intensive and lightweight tasks on the same Worker pool.

---

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

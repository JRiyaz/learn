# RabbitMQ Masterclass for Backend Engineers

## File 07 – Work Queues, Prefetch & Fair Dispatch

> **Course Level:** Intermediate → Advanced
>
> So far we've learned how RabbitMQ reliably stores and delivers messages.
>
> But another important question remains:
>
> **If there are multiple consumers, who gets the next message?**
>
> Should every consumer receive the same number of messages?
>
> What if one consumer is much slower than the others?
>
> This chapter answers these questions.

______________________________________________________________________

# Learning Objectives

By the end of this chapter, you will be able to:

- Understand the Work Queue pattern.
- Explain Round-Robin Dispatch.
- Understand Fair Dispatch.
- Explain Prefetch Count.
- Understand Unacknowledged Messages.
- Design scalable worker architectures.
- Optimize consumer throughput.
- Prevent slow consumers from becoming bottlenecks.

______________________________________________________________________

# Table of Contents

1. Why Work Queues Exist
1. The Work Queue Pattern
1. Multiple Consumers
1. Round-Robin Dispatch
1. The Problem with Round-Robin
1. Fair Dispatch
1. Prefetch Count
1. Unacknowledged Messages
1. Choosing the Right Prefetch Value
1. Backpressure
1. Scaling Consumers
1. Real Production Example
1. Summary
1. Key Takeaways
1. Interview Deep Dive
1. Practice Questions
1. Mini Assignment
1. Common Mistakes
1. What's Next?

______________________________________________________________________

# Why Work Queues Exist

Imagine an application that generates PDFs.

Every request creates one task.

```
Generate Invoice

↓

Queue
```

Now imagine

```
100,000 PDF Requests
```

One worker has to process everything.

```
Queue

↓

Worker
```

This quickly becomes a bottleneck.

The obvious solution is to add more workers.

```
Queue

↓

Worker 1

Worker 2

Worker 3

Worker 4
```

RabbitMQ automatically distributes work.

This is called the **Work Queue Pattern**.

______________________________________________________________________

# What is a Work Queue?

A Work Queue distributes tasks among multiple workers.

Instead of one worker processing every message,

multiple workers share the workload.

```
                Queue

                 │

      ┌──────────┼──────────┐

      ▼          ▼          ▼

   Worker1   Worker2   Worker3
```

Each task is processed only once.

______________________________________________________________________

# Why Use Work Queues?

Imagine processing

- Images
- Videos
- Emails
- Reports
- Machine Learning jobs

All of these are CPU or I/O intensive.

Instead of slowing down your API,

RabbitMQ moves these jobs to background workers.

______________________________________________________________________

# Multiple Consumers

Suppose a Queue contains

```
Task 1

Task 2

Task 3

Task 4

Task 5

Task 6
```

Three workers connect.

```
Queue

↓

Worker A

Worker B

Worker C
```

Who gets which task?

RabbitMQ uses a dispatch strategy.

Let's understand it.

______________________________________________________________________

# Round-Robin Dispatch

By default,

RabbitMQ distributes messages using **Round-Robin**.

Example

```
Queue

↓

Task1 → Worker A

Task2 → Worker B

Task3 → Worker C

Task4 → Worker A

Task5 → Worker B

Task6 → Worker C
```

Every worker receives an equal number of messages.

Seems perfect.

But there is a problem.

______________________________________________________________________

# The Problem with Round-Robin

Suppose

Worker A

```
Processes Emails

100 milliseconds
```

Worker B

```
Processes AI Images

20 Seconds
```

Worker C

```
Processes Notifications

50 milliseconds
```

Round-Robin still distributes equally.

```
Task1 → Worker A

Task2 → Worker B

Task3 → Worker C

Task4 → Worker A

Task5 → Worker B

Task6 → Worker C
```

Worker B becomes overloaded.

Workers A and C remain mostly idle.

Overall throughput decreases.

______________________________________________________________________

# Visual Example

```
Worker A

✔ Done

✔ Done

✔ Done

---------------------

Worker B

Still Processing...

---------------------

Worker C

✔ Done

✔ Done

✔ Done
```

Round-Robin ignores processing speed.

It only counts message delivery.

______________________________________________________________________

# The Solution: Fair Dispatch

Instead of blindly distributing messages,

RabbitMQ can distribute work based on

**who is actually available.**

```
Queue

↓

Worker A (Idle)

↓

Gets Next Task

------------------

Worker B (Busy)

↓

Gets Nothing

------------------

Worker C (Idle)

↓

Gets Next Task
```

This is called **Fair Dispatch**.

______________________________________________________________________

# How Fair Dispatch Works

RabbitMQ waits until a worker finishes processing.

Only after receiving an ACK

does RabbitMQ send another message.

```
Worker

↓

Task

↓

Processing

↓

ACK

↓

Next Task
```

Busy workers receive fewer tasks.

Idle workers receive more.

______________________________________________________________________

# Prefetch Count

Fair Dispatch is controlled using

**Prefetch Count**.

This is one of RabbitMQ's most important performance settings.

______________________________________________________________________

# What is Prefetch Count?

Prefetch Count limits

how many unacknowledged messages a Consumer can hold.

Example

```
Prefetch = 1
```

RabbitMQ sends

```
One Message
```

Worker processes it.

Sends ACK.

Only then

RabbitMQ sends another.

______________________________________________________________________

Diagram

```
Queue

↓

Worker

↓

Task

↓

ACK

↓

Next Task
```

Simple.

______________________________________________________________________

# What Happens with Prefetch = 5?

```
Queue

↓

Worker

↓

Task1

Task2

Task3

Task4

Task5
```

RabbitMQ sends

five messages immediately.

Worker processes them one by one.

No additional messages are delivered until one is acknowledged.

______________________________________________________________________

# Prefetch = Unlimited

If no limit exists,

RabbitMQ may deliver

```
1000 Messages
```

to one Consumer.

Another Consumer

receives nothing.

Result

```
Worker A

1000 Tasks

-----------------

Worker B

Idle
```

Poor load balancing.

______________________________________________________________________

# Why Prefetch = 1 is Popular

Suppose

```
Worker A

Processing Large Video
```

RabbitMQ waits.

Meanwhile

```
Worker B

Idle
```

RabbitMQ sends the next task to Worker B.

Everyone stays busy.

This maximizes throughput.

______________________________________________________________________

# Unacknowledged Messages

When RabbitMQ delivers a message,

it waits for an ACK.

During this time,

the message becomes

```
Unacknowledged
```

Diagram

```
Queue

↓

Worker

↓

Processing

↓

ACK Pending
```

RabbitMQ counts these messages.

Prefetch Count limits how many unacknowledged messages each Consumer can have.

______________________________________________________________________

# Example

Prefetch = 2

Worker currently processing

```
Task A

Task B
```

RabbitMQ sends nothing else.

Only after

```
Task A

↓

ACK
```

does RabbitMQ deliver

```
Task C
```

______________________________________________________________________

# Choosing the Right Prefetch Count

There is no universal answer.

It depends on your workload.

______________________________________________________________________

## CPU Intensive Tasks

Examples

- Video Encoding
- AI Models
- Image Processing

Recommended

```
Prefetch = 1
```

Keeps work balanced.

______________________________________________________________________

## I/O Intensive Tasks

Examples

- HTTP Requests
- Database Reads
- File Downloads

Recommended

```
Prefetch = 10–50
```

Workers spend time waiting.

Receiving multiple messages improves utilization.

______________________________________________________________________

## Very Fast Tasks

Examples

- Cache Updates
- Logging
- Metrics

Recommended

```
Prefetch = 100+
```

Reduces network overhead.

______________________________________________________________________

# Backpressure

Suppose Producers publish

```
500 Messages/sec
```

Consumers process

```
100 Messages/sec
```

Queue size grows.

```
500

↓

400

↓

300

↓

200

↓

100

↓

Backlog
```

Eventually

```
Queue

500,000 Messages
```

This is called **Backpressure**.

______________________________________________________________________

# Handling Backpressure

Several approaches exist.

______________________________________________________________________

## Add More Consumers

```
Queue

↓

10 Workers

↓

20 Workers

↓

50 Workers
```

______________________________________________________________________

## Increase Worker Resources

Upgrade

- CPU
- RAM
- Disk

______________________________________________________________________

## Optimize Processing

Reduce

- Database queries
- Network calls
- Blocking operations

______________________________________________________________________

## Split Queues

Instead of

```
General Queue
```

Create

```
Email Queue

Image Queue

PDF Queue

Notification Queue
```

Different workloads can now scale independently.

______________________________________________________________________

# Consumer Scaling

RabbitMQ makes scaling simple.

```
Queue

↓

Worker 1

Worker 2

Worker 3

Worker 4

Worker 5

Worker 6
```

Adding another worker usually requires

no Producer changes.

RabbitMQ automatically includes the new worker.

______________________________________________________________________

# Real Production Example

Suppose an e-commerce platform.

During Black Friday,

millions of emails must be sent.

Architecture

```
Order Service

↓

Email Queue

↓

Email Worker 1

Email Worker 2

Email Worker 3

...

Email Worker 100
```

Each worker

```
Prefetch = 20
```

Emails are distributed efficiently.

As demand increases,

new workers are added without changing the Producer.

______________________________________________________________________

# Performance Tips

✔ Keep Consumers stateless.

✔ Monitor Queue length.

✔ Monitor unacknowledged messages.

✔ Tune Prefetch based on workload.

✔ Scale Consumers horizontally.

✔ Separate heavy and lightweight jobs.

______________________________________________________________________

# Summary

RabbitMQ distributes work among Consumers using dispatch strategies.

Round-Robin works well for equally sized tasks,

but Fair Dispatch combined with Prefetch Count provides much better load balancing for real-world systems.

Proper Prefetch configuration improves

- Throughput
- Resource utilization
- Scalability
- Latency

Choosing the correct value depends on the nature of your workload.

______________________________________________________________________

# Key Takeaways

- Work Queues distribute tasks among multiple Consumers.
- RabbitMQ uses Round-Robin by default.
- Round-Robin ignores processing speed.
- Fair Dispatch sends work only to available Consumers.
- Prefetch Count limits unacknowledged messages.
- Lower Prefetch improves fairness.
- Higher Prefetch improves throughput for lightweight workloads.
- Monitor Queue length and unacknowledged messages in production.
- Scale Consumers independently of Producers.

______________________________________________________________________

# Interview Deep Dive

## Question 1

### What is the Work Queue Pattern?

#### Answer

The Work Queue Pattern distributes tasks among multiple Consumers so that each task is processed only once. It enables
horizontal scaling and improves throughput for background processing systems.

______________________________________________________________________

## Question 2

### How does RabbitMQ distribute messages by default?

#### Answer

RabbitMQ uses Round-Robin dispatch, delivering messages sequentially to connected Consumers without considering how long
each Consumer takes to process a message.

______________________________________________________________________

## Question 3

### Why is Round-Robin not always efficient?

#### Answer

Round-Robin assumes all Consumers process messages at the same speed. If one Consumer is slower than the others, it
still receives an equal number of messages, creating bottlenecks and reducing overall throughput.

______________________________________________________________________

## Question 4

### What is Fair Dispatch?

#### Answer

Fair Dispatch prevents overloaded Consumers from receiving additional messages until they acknowledge previously
delivered ones. It is achieved using Manual ACKs together with an appropriate Prefetch Count.

______________________________________________________________________

## Question 5

### What is Prefetch Count?

#### Answer

Prefetch Count specifies the maximum number of unacknowledged messages RabbitMQ can deliver to a Consumer. Once the
limit is reached, RabbitMQ waits until the Consumer acknowledges a message before sending another.

______________________________________________________________________

## Question 6

### Why is Prefetch = 1 commonly recommended?

#### Answer

Prefetch = 1 ensures that each Consumer receives only one unacknowledged message at a time. This provides excellent load
balancing for long-running or CPU-intensive tasks because faster Consumers naturally receive more work.

______________________________________________________________________

## Question 7

### How would you choose a Prefetch Count?

#### Answer

Choose a lower Prefetch Count (often 1) for long-running CPU-intensive tasks and a higher Prefetch Count for lightweight
or I/O-bound tasks where Consumers spend significant time waiting on external systems.

______________________________________________________________________

# Practice Questions

1. Explain the Work Queue Pattern.
1. What is Round-Robin dispatch?
1. Why does Round-Robin become inefficient?
1. Explain Fair Dispatch.
1. What is Prefetch Count?
1. What are unacknowledged messages?
1. Why is Prefetch = 1 recommended for CPU-intensive tasks?
1. What causes backpressure?
1. How would you scale Consumers during peak traffic?
1. How would you tune Prefetch for a high-throughput email service?

______________________________________________________________________

# Mini Assignment

Design the worker architecture for a social media platform.

When a user uploads a photo, the following tasks should occur:

- Generate thumbnails
- Resize images
- Scan for inappropriate content
- Update analytics
- Notify followers

For each task, determine:

- Which Queue it belongs to.
- How many Workers should process it.
- An appropriate Prefetch Count.
- Whether the workload is CPU-bound or I/O-bound.

Explain your reasoning.

______________________________________________________________________

# Common Mistakes

❌ Leaving Prefetch unlimited in production.

❌ Assuming Round-Robin always provides optimal performance.

❌ Using the same Prefetch Count for every workload.

❌ Mixing long-running and short-running tasks in the same Queue.

❌ Ignoring unacknowledged message counts.

❌ Scaling Producers instead of Consumers when Queues grow.

______________________________________________________________________

# What's Next?

Now that you understand how RabbitMQ distributes work efficiently, it's time to learn how RabbitMQ handles **failed
messages**.

In the next chapter, we'll cover:

- Dead Letter Exchanges (DLX)
- Dead Letter Queues (DLQ)
- Retry patterns
- Poison messages
- Retry delays
- Production retry architectures

➡ **Next File:** [File 08 – Dead Letter Exchanges, Retries & Failure Handling](08-dead-letter-exchanges.md)

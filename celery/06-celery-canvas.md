# Celery Masterclass for Backend Engineers

## File 18 – Celery Canvas: Chains, Groups, Chords & Workflow Orchestration

> **Course Level:** Intermediate → Advanced
>
> Up to this point, every Celery task has been independent.
>
> ```
> Send Email
> ```
>
> ```
> Resize Image
> ```
>
> ```
> Generate Invoice
> ```
>
> But real production systems rarely execute just one task.
>
> Instead, they execute **workflows**.
>
> Example:
>
> ```
> Upload Video
>
> ↓
>
> Extract Frames
>
> ↓
>
> Generate Thumbnail
>
> ↓
>
> Run AI Moderation
>
> ↓
>
> Notify User
> ```
>
> Celery provides the **Canvas API** to build these workflows.

______________________________________________________________________

# Learning Objectives

By the end of this chapter, you will be able to:

- Understand the Canvas API.
- Understand Signatures.
- Build Chains.
- Build Groups.
- Build Chords.
- Use Map and Starmap.
- Design complex task workflows.
- Choose the correct Canvas primitive.

______________________________________________________________________

# Table of Contents

1. Why Canvas Exists
1. What is a Signature?
1. Chains
1. Groups
1. Chords
1. Maps
1. Starmaps
1. Workflow Patterns
1. Production Examples
1. Summary
1. Key Takeaways
1. Interview Deep Dive
1. Practice Questions
1. Mini Assignment
1. Common Mistakes
1. What's Next?

______________________________________________________________________

# Why Canvas Exists

Imagine processing an uploaded video.

Steps

```
Upload

↓

Store File

↓

Extract Audio

↓

Generate Thumbnail

↓

AI Moderation

↓

Publish Video
```

Every step depends on the previous one.

Writing this manually becomes messy.

Celery Canvas lets us compose workflows.

______________________________________________________________________

# What is Canvas?

Canvas is Celery's workflow engine.

Instead of executing

```
One Task
```

Canvas executes

```
Multiple Tasks

↓

Connected Together
```

______________________________________________________________________

Canvas provides

```
Signature

Chain

Group

Chord

Map

Starmap
```

Let's learn each one.

______________________________________________________________________

# Signatures

A Signature is

a description of a task

that has **not executed yet**.

Think of it as

```
Blueprint

Not Building
```

Example

```python
send_email.s(user_id)
```

Notice

```
.s()
```

No execution happens.

It simply creates a task signature.

______________________________________________________________________

# delay()

```
Execute Immediately
```

______________________________________________________________________

# Signature

```
Prepare

↓

Execute Later
```

______________________________________________________________________

Example

```python
task = send_email.s(101)
```

Nothing runs.

Later

```python
task.delay()
```

Now execution starts.

______________________________________________________________________

# Why Signatures?

Because Chains,

Groups,

and Chords

are built using them.

______________________________________________________________________

# Chains

Suppose

Invoice generation

must happen before

Email.

Workflow

```
Generate Invoice

↓

Send Email

↓

Update Analytics
```

Tasks execute

one after another.

______________________________________________________________________

Example

```python
from celery import chain

workflow = chain(
    generate_invoice.s(order_id),
    send_email.s(),
    update_analytics.s()
)

workflow.delay()
```

______________________________________________________________________

# How Chains Work

Step 1

```
Generate Invoice
```

↓

Returns

```
Invoice.pdf
```

↓

Automatically passed into

```
Send Email
```

↓

Returns

```
Email Sent
```

↓

Passed into

```
Analytics
```

Each task receives

the previous task's output.

______________________________________________________________________

# Chain Diagram

```
Task A

↓

Task B

↓

Task C

↓

Task D
```

Sequential execution.

______________________________________________________________________

# Production Example

```
User Registration

↓

Save User

↓

Generate JWT

↓

Send Email

↓

Update CRM

↓

Analytics
```

Every step depends

on the previous one.

Use

```
Chain
```

______________________________________________________________________

# Groups

Sometimes

tasks are independent.

Example

```
Upload Photo
```

Need to

```
Resize

Blur

Watermark

Compress
```

None depend on each other.

Run them simultaneously.

______________________________________________________________________

Example

```python
from celery import group

group(
    resize_image.s(image),
    compress_image.s(image),
    watermark_image.s(image)
).delay()
```

______________________________________________________________________

Diagram

```
            Upload

               │

      ┌────────┼────────┐

      ▼        ▼        ▼

 Resize     Compress   Watermark
```

Parallel execution.

______________________________________________________________________

# Why Groups?

Groups

reduce overall execution time.

Without Groups

```
Resize

↓

Compress

↓

Watermark

↓

30 Seconds
```

With Groups

```
Resize

Compress

Watermark

↓

10 Seconds
```

Huge improvement.

______________________________________________________________________

# Chords

Now imagine

Parallel tasks

followed by

one final task.

Workflow

```
Resize

Compress

Watermark

↓

Notify User
```

Notify User

must wait

until all three finish.

______________________________________________________________________

This is called

a

```
Chord
```

______________________________________________________________________

Example

```python
from celery import chord

workflow = chord(
    [
        resize_image.s(img),
        compress_image.s(img),
        watermark_image.s(img)
    ]
)(
    notify_user.s()
)
```

______________________________________________________________________

Diagram

```
Resize

      \

Compress -----> Notify User

      /

Watermark
```

The final callback waits.

______________________________________________________________________

# Difference Between Group and Chord

Group

```
Run Together

Done.
```

Chord

```
Run Together

↓

Execute Callback
```

______________________________________________________________________

Comparison

| Group | Chord |
|--------|--------|
| Parallel | Parallel |
| No callback | Callback |
| Independent finish | Final aggregation |

______________________________________________________________________

# Map

Suppose

100 images.

Same task.

```
Resize

↓

Image1

Image2

Image3

Image4
```

Instead of

writing

100 tasks,

use

```
map()
```

______________________________________________________________________

Example

```python
resize_image.map(images)
```

Equivalent to

```
Resize Image1

Resize Image2

Resize Image3

...
```

______________________________________________________________________

# Starmap

Suppose

arguments differ.

```
Resize

↓

Image1

300x300

----------------

Image2

500x500

----------------

Image3

800x600
```

Use

```
starmap()
```

______________________________________________________________________

Example

```python
resize_image.starmap(
    [
        ("a.jpg",300,300),
        ("b.jpg",500,500),
        ("c.jpg",800,600)
    ]
)
```

Each tuple

becomes

individual arguments.

______________________________________________________________________

# Workflow Comparison

Sequential

```
Chain
```

______________________________________________________________________

Parallel

```
Group
```

______________________________________________________________________

Parallel

-

Final Callback

```
Chord
```

______________________________________________________________________

Same Task

Many Inputs

```
Map
```

______________________________________________________________________

Same Task

Different Arguments

```
Starmap
```

______________________________________________________________________

# Production Example

Video Upload

```
Upload

↓

Group

↓

Extract Audio

Generate Thumbnail

Generate Preview

Run AI

↓

Chord Callback

↓

Publish Video

↓

Notify User
```

Excellent real-world example.

______________________________________________________________________

# Another Production Example

Order Processing

```
Order Created

↓

Chain

↓

Reserve Inventory

↓

Charge Card

↓

Generate Invoice

↓

Email Customer
```

Each step depends

on the previous one.

______________________________________________________________________

# Choosing the Right Primitive

Need

```
Sequential

↓

Chain
```

Need

```
Parallel

↓

Group
```

Need

```
Parallel

↓

Then Aggregate

↓

Chord
```

Need

```
Same Task

↓

Many Inputs

↓

Map
```

Need

```
Different Arguments

↓

Starmap
```

______________________________________________________________________

# Best Practices

✔ Keep individual tasks small.

✔ Avoid extremely long Chains.

✔ Use Groups for independent work.

✔ Use Chords sparingly for expensive callbacks.

✔ Keep callback tasks idempotent.

✔ Monitor workflow failures.

______________________________________________________________________

# Summary

Celery Canvas allows multiple tasks to be composed into workflows.

Signatures define tasks without executing them.

Chains execute tasks sequentially.

Groups execute tasks in parallel.

Chords execute parallel tasks followed by a callback.

Map and Starmap simplify applying the same task across many inputs.

Canvas is essential for building sophisticated asynchronous systems.

______________________________________________________________________

# Key Takeaways

- Canvas builds workflows.
- Signatures describe tasks.
- Chains execute sequentially.
- Groups execute in parallel.
- Chords synchronize parallel tasks.
- Maps apply one task to many inputs.
- Starmaps support multiple arguments.
- Choose primitives based on task dependencies.

______________________________________________________________________

# Interview Deep Dive

## Question 1

### What is Celery Canvas?

#### Answer

Celery Canvas is a workflow framework that allows multiple tasks to be composed into complex execution graphs such as
sequential pipelines, parallel execution, and callback workflows.

______________________________________________________________________

## Question 2

### What is a Signature?

#### Answer

A Signature is a serialized description of a task and its arguments that can be passed around, combined with other
Signatures, and executed later. It is created using methods like `.s()`.

______________________________________________________________________

## Question 3

### What is the difference between a Chain and a Group?

#### Answer

A Chain executes tasks sequentially, with each task receiving the previous task's result. A Group executes multiple
independent tasks in parallel without sharing results.

______________________________________________________________________

## Question 4

### What is a Chord?

#### Answer

A Chord combines a Group with a callback task. The callback executes only after every task in the Group has completed
successfully.

______________________________________________________________________

## Question 5

### When should you use a Group?

#### Answer

Use a Group when tasks are independent of one another and can safely execute in parallel, such as resizing images into
multiple formats.

______________________________________________________________________

## Question 6

### What is the difference between Map and Starmap?

#### Answer

Map applies the same task to multiple inputs where each input is treated as a single argument. Starmap applies the same
task to multiple tuples, expanding each tuple into separate positional arguments.

______________________________________________________________________

## Question 7

### Give a real-world example of a Chord.

#### Answer

A video processing pipeline may generate thumbnails, extract audio, create previews, and run AI moderation in parallel.
Once all complete, a callback publishes the video and notifies the user.

______________________________________________________________________

# Practice Questions

1. What is Celery Canvas?
1. Explain Task Signatures.
1. Compare Chain and Group.
1. Compare Group and Chord.
1. When should Map be used?
1. When should Starmap be used?
1. Design a video-processing workflow.
1. Design an invoice-generation workflow.
1. Explain how task results flow through a Chain.
1. Why should callback tasks be idempotent?

______________________________________________________________________

# Mini Assignment

Design the Celery workflow for a video streaming platform.

When a user uploads a video:

- Extract audio
- Generate thumbnails
- Generate preview clips
- Run AI moderation
- Detect language
- Generate subtitles
- Notify the uploader
- Publish the video

For each task, determine:

- Chain, Group, or Chord?
- Can it run in parallel?
- Which tasks depend on previous results?
- Which task should execute last?

Draw the entire workflow using ASCII diagrams.

______________________________________________________________________

# Common Mistakes

❌ Using Chains when tasks are independent.

❌ Using Groups when later tasks depend on earlier results.

❌ Forgetting that Chord callbacks wait for every task.

❌ Creating extremely large Groups without monitoring Worker capacity.

❌ Assuming Map and Starmap are interchangeable.

❌ Making callback tasks non-idempotent.

______________________________________________________________________

# What's Next?

Now that you understand workflow orchestration, we'll explore **Celery Beat**, the scheduling component that allows
tasks to run automatically on recurring schedules.

The next chapter covers:

- Celery Beat
- Periodic Tasks
- Cron Scheduling
- Interval Scheduling
- Solar Scheduling
- Production Scheduling
- Beat Architecture
- High Availability Considerations

➡ **Next File:** [File 19 – Celery Beat & Scheduled Tasks](19-celery-beat.md)

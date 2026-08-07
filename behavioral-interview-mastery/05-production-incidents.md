# Production Incident Questions

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Learn how to confidently answer production support, outage, and incident management questions expected in Senior Software Engineer interviews.

______________________________________________________________________

# Introduction

If you have

5+ years

of experience,

there is a very high chance

you'll be asked

about production.

Interviewers know

any engineer

can write code.

They want to know

```
Can you handle

production?
```

______________________________________________________________________

# Why Production Questions Matter

Production incidents reveal

much more than

technical knowledge.

They reveal

- Decision Making
- Communication
- Leadership
- Debugging Skills
- Prioritization
- Calmness
- Ownership

______________________________________________________________________

# What Interviewers Are Actually Evaluating

They're not asking

```
Did production fail?
```

They're asking

```
How did YOU

respond?
```

______________________________________________________________________

# The Incident Lifecycle

Every production incident

should follow

this flow.

```
Alert

↓

Understand

↓

Contain

↓

Investigate

↓

Root Cause

↓

Fix

↓

Monitor

↓

Postmortem

↓

Prevent
```

Memorize this.

______________________________________________________________________

# Golden Rule

The priority is

NOT

finding

who caused

the problem.

The priority is

```
Restore Service

↓

Understand Root Cause

↓

Prevent Recurrence
```

______________________________________________________________________

# Question 1

## Tell me about a production incident.

______________________________________________________________________

### What Interviewer Is Evaluating

```
Ownership

↓

Debugging

↓

Communication

↓

Decision Making
```

______________________________________________________________________

### Weak Answer

> Production was down.

> We fixed it.

Too vague.

______________________________________________________________________

### Excellent Answer

Situation

> Shortly after a deployment, API response times increased significantly and customer requests began timing out.

Task

> My responsibility was to help identify the issue, restore service quickly, and minimize customer impact.

Action

> We first confirmed the issue using monitoring dashboards and logs. I analyzed application metrics, identified slow database queries, and verified that the problem was introduced by a recently deployed feature. We temporarily rolled back the deployment to restore service while continuing our investigation in staging.

Result

> Service recovered within a short time, customer impact was minimized, and we later deployed an optimized solution after proper testing.

Learning

> The incident reinforced the importance of performance testing before deployment and monitoring key production metrics immediately after releases.

______________________________________________________________________

# Why This Works

Shows

```
Calm Thinking

↓

Investigation

↓

Communication

↓

Recovery

↓

Learning
```

______________________________________________________________________

# Question 2

## What is the first thing you do during a production incident?

______________________________________________________________________

### Weak Answer

> Start fixing code.

Wrong.

______________________________________________________________________

### Excellent Answer

```
Confirm Incident

↓

Measure Impact

↓

Communicate

↓

Stabilize System

↓

Investigate

↓

Fix

↓

Monitor
```

Never

start changing code

before understanding

the problem.

______________________________________________________________________

# Question 3

## How do you investigate a production issue?

______________________________________________________________________

### Excellent Answer

My investigation usually follows

```
Logs

↓

Metrics

↓

Recent Deployments

↓

Database

↓

Infrastructure

↓

External Services
```

I avoid making assumptions

until evidence

supports them.

______________________________________________________________________

# Question 4

## Tell me about a high-priority production bug.

______________________________________________________________________

### Excellent Answer

Situation

> Customers were intermittently receiving HTTP 500 errors after a deployment.

Task

> I needed to identify the cause and restore service quickly.

Action

> I compared successful and failed requests, reviewed logs, correlated the issue with a recent deployment, and isolated a configuration problem affecting one service. After validating the fix in staging, we deployed it and monitored production closely.

Result

> Error rates returned to normal, and we added deployment validation checks to prevent similar issues.

Learning

> Configuration validation should be automated whenever possible.

______________________________________________________________________

# Question 5

## How do you prioritize during an incident?

______________________________________________________________________

### Excellent Answer

Priority

should always be

```
Customer Impact

↓

Service Availability

↓

Business Risk

↓

Root Cause

↓

Permanent Fix
```

Don't optimize

while

customers

cannot use

the system.

______________________________________________________________________

# Question 6

## What if you don't know the cause?

______________________________________________________________________

### Weak Answer

> I'll try random fixes.

______________________________________________________________________

### Excellent Answer

> I avoid making assumptions. Instead, I gather evidence from logs, monitoring systems, recent deployments, infrastructure metrics, and team members before making changes. If necessary, I stabilize the service first and continue investigating in a controlled environment.

______________________________________________________________________

# Question 7

## Have you ever rolled back a deployment?

______________________________________________________________________

### Excellent Answer

Situation

> A new deployment introduced significantly higher API latency.

Task

> Our priority was restoring customer service.

Action

> After confirming the issue was deployment-related, we rolled back to the previous stable version while continuing root cause analysis in staging.

Result

> Customer impact was minimized, and we deployed a corrected version after resolving the underlying issue.

Learning

> Fast rollback procedures are an essential part of reliable deployment strategies.

______________________________________________________________________

# Question 8

## How do you communicate during incidents?

______________________________________________________________________

### Excellent Answer

Good communication follows

```
Current Status

↓

Impact

↓

Actions

↓

ETA

↓

Next Update
```

Avoid

```
We're working on it.
```

Instead

provide

useful information.

______________________________________________________________________

# Question 9

## What happens after the incident?

______________________________________________________________________

### Excellent Answer

Never stop

after fixing.

Complete process

```
Root Cause Analysis

↓

Postmortem

↓

Action Items

↓

Automation

↓

Documentation

↓

Monitoring Improvements
```

This demonstrates

engineering maturity.

______________________________________________________________________

# Question 10

## What is a postmortem?

______________________________________________________________________

### Excellent Answer

A postmortem

is a structured review

of an incident

to understand

```
What Happened

↓

Why It Happened

↓

Impact

↓

Timeline

↓

Root Cause

↓

Corrective Actions

↓

Preventive Actions
```

A good postmortem

is

blameless.

The goal is

learning,

not punishment.

______________________________________________________________________

# Typical Production Problems

Expect scenarios like

```
High CPU

High Memory

Slow APIs

Database Lock

Deadlock

Disk Full

Pod Crash

Cache Failure

RabbitMQ Queue Growth

Redis Down

Network Issue

Certificate Expired

Deployment Failure

Timeout

OOMKilled

High Latency
```

We'll cover

each

in dedicated files

later.

______________________________________________________________________

# Production Mindset

Junior

```
Bug

↓

Fix
```

Senior

```
Detect

↓

Communicate

↓

Stabilize

↓

Investigate

↓

Recover

↓

Prevent
```

______________________________________________________________________

# Incident Timeline

```
Alert

↓

Verify

↓

Communicate

↓

Contain

↓

Root Cause

↓

Fix

↓

Validate

↓

Monitor

↓

Postmortem

↓

Automation
```

Memorize

this sequence.

______________________________________________________________________

# Common Follow-Up Questions

Expect

- How did you identify the issue?
- How did you prioritize?
- Who did you communicate with?
- What monitoring tools did you use?
- What would you improve?
- How did you prevent recurrence?

______________________________________________________________________

# Common Mistakes

## Jumping To Conclusions

Never

assume

the root cause.

Collect evidence.

______________________________________________________________________

## Making Changes In Production Immediately

Understand

before

changing.

______________________________________________________________________

## Poor Communication

Silence

creates panic.

Keep stakeholders

updated.

______________________________________________________________________

## No Monitoring

After fixing,

always

verify

the system

is healthy.

______________________________________________________________________

## No Prevention

Every incident

should end with

```
How do we stop

this

from happening again?
```

______________________________________________________________________

# Best Practices

✅ Stay calm.

✅ Prioritize customer impact.

✅ Gather evidence.

✅ Communicate frequently.

✅ Validate fixes.

✅ Conduct postmortems.

✅ Improve monitoring.

✅ Automate prevention.

______________________________________________________________________

# Production Cheat Sheet

```
Alert

↓

Assess

↓

Communicate

↓

Contain

↓

Investigate

↓

Recover

↓

Validate

↓

Learn

↓

Prevent
```

______________________________________________________________________

# Practice Exercise

Prepare STAR stories for

1. High API latency
1. Deployment rollback
1. Database issue
1. Production bug
1. RabbitMQ issue
1. Kubernetes failure
1. AWS outage
1. Cache problem
1. Monitoring alert
1. Customer escalation

For each story,

include

```
Situation

↓

Task

↓

Action

↓

Result

↓

Root Cause

↓

Prevention

↓

Learning
```

______________________________________________________________________

# Interview Deep Dive

## Question

What do interviewers expect during production incident questions?

### Answer

They expect a structured approach that prioritizes customer impact, clear communication, evidence-based debugging,
collaboration, and long-term prevention—not just technical troubleshooting.

______________________________________________________________________

## Question

Should I admit that I didn't know the cause immediately?

### Answer

Yes. In fact, experienced engineers rarely know the root cause immediately. Interviewers appreciate candidates who
investigate systematically instead of making assumptions.

______________________________________________________________________

## Question

What is the biggest mistake engineers make during incidents?

### Answer

Jumping directly to solutions without understanding the problem, failing to communicate with stakeholders, and treating
recovery as the end of the incident instead of completing root cause analysis and preventive improvements.

______________________________________________________________________

# Summary

Production incident questions are among the most important questions for Senior Software Engineers.

The strongest candidates demonstrate

- Calm decision-making
- Structured investigation
- Clear communication
- Ownership
- Root cause analysis
- Long-term prevention

These qualities build trust and distinguish experienced engineers from developers who only focus on implementation.

______________________________________________________________________

# Next

[Teamwork & Cross-Team Collaboration](06-teamwork-and-collaboration.md)

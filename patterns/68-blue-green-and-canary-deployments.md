# System Design - Part 68

# Blue-Green & Canary Deployments

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why Deployment Strategies matter
- Deployment Challenges
- Blue-Green Deployment
- Canary Deployment
- Rolling Deployment
- Recreate Deployment
- Feature Flags
- Rollbacks
- Kubernetes Deployment Strategies
- CI/CD Integration
- FastAPI examples
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

has

Version 1

running

in production.

Today,

we want

to deploy

Version 2.

Question.

What happens

if

Version 2

contains

a critical bug?

Should

every user

receive

the broken version

immediately?

No.

Production deployments

must be

safe.

______________________________________________________________________

# The Problem

Traditional deployment

looks like this.

```text id="dep6801"
Stop Version 1

↓

Deploy Version 2

↓

Start Version 2
```

Problems:

❌ Downtime

❌ Difficult rollback

❌ All users affected

______________________________________________________________________

# Another Problem

Suppose

Version 2

has

a database bug.

Within minutes,

thousands

of users

experience failures.

Rolling back

may take

several minutes.

By then,

damage

has already occurred.

______________________________________________________________________

# The Idea

Deploy

new versions

gradually,

observe

their behavior,

and

roll back

quickly

if problems occur.

______________________________________________________________________

# Blue-Green Deployment

Interview favorite.

Maintain

two

identical environments.

```text id="dep6802"
Blue

(Current)
```

```text id="dep6803"
Green

(New)
```

Users

initially

use

Blue.

Deploy

the new version

to

Green.

______________________________________________________________________

# Blue-Green Flow

```text id="dep6804"
Users

↓

Load Balancer

↓

Blue
```

Deploy

Version 2

to

Green.

After validation,

switch

the Load Balancer.

```text id="dep6805"
Users

↓

Load Balancer

↓

Green
```

______________________________________________________________________

# Rollback

Suppose

Green

has

a bug.

Rollback

is simple.

```text id="dep6806"
Load Balancer

↓

Blue
```

Traffic

returns

immediately

to

the previous version.

______________________________________________________________________

# Advantages

Blue-Green

provides:

✅ Zero downtime

✅ Instant rollback

✅ Easy testing

______________________________________________________________________

# Disadvantages

Blue-Green

requires

two complete

production environments.

This doubles

infrastructure cost

during deployment.

______________________________________________________________________

# Canary Deployment

Interview favorite.

Instead of

sending

all users

to

Version 2,

send

only

a small percentage.

Example

```text id="dep6807"
95%

↓

Version 1
```

```text id="dep6808"
5%

↓

Version 2
```

Observe

metrics

before

increasing traffic.

______________________________________________________________________

# Canary Rollout

Typical rollout

looks like:

```text id="dep6809"
5%

↓

10%

↓

25%

↓

50%

↓

100%
```

If

errors increase,

stop

the rollout.

______________________________________________________________________

# Why Canary?

Suppose

only

5%

of users

experience

a bug.

95%

remain

unaffected.

Risk

is greatly reduced.

______________________________________________________________________

# Rolling Deployment

Kubernetes

commonly uses

Rolling Deployments.

Instead of

replacing

every instance,

replace

them

one at a time.

```text id="dep6810"
Pod 1

↓

Pod 2

↓

Pod 3
```

Old Pods

are removed

only after

new Pods

become healthy.

______________________________________________________________________

# Recreate Deployment

The simplest strategy.

```text id="dep6811"
Stop Old Version

↓

Start New Version
```

Advantages

✅ Very simple

Disadvantages

❌ Downtime

Usually

used only

for

development

or

internal systems.

______________________________________________________________________

# Deployment Strategy Comparison

| Strategy | Downtime | Rollback | Cost |
| ---------- | -------- | -------- | ------ |
| Recreate | High | Slow | Low |
| Rolling | None | Medium | Low |
| Blue-Green | None | Fast | High |
| Canary | None | Fast | Medium |

______________________________________________________________________

# Feature Flags

Interview favorite.

Suppose

Version 2

contains

a new feature.

Instead of

deploying

a separate version,

deploy

the code

but

keep

the feature

disabled.

```text id="dep6812"
New Search

↓

OFF
```

Later,

enable

it

without

redeploying.

______________________________________________________________________

# Feature Flag Example

Suppose

only

internal employees

should see

the feature.

```text id="dep6813"
Employee

↓

New Dashboard
```

Regular users

continue

using

the old interface.

______________________________________________________________________

# Rollback Strategy

A deployment

is successful

only if

rollback

is easy.

Examples

of rollback triggers:

- Error rate increases
- Latency spikes
- CPU usage rises
- Business metrics decline

______________________________________________________________________

# Health Checks

Before

routing traffic,

verify

the application.

Example

```text id="dep6814"
/health
```

Only

healthy instances

receive traffic.

______________________________________________________________________

# Kubernetes Example

Kubernetes

supports

Rolling Deployments

natively.

Example

```yaml id="dep6815"
strategy:

RollingUpdate
```

For

Blue-Green

or

Canary,

tools such as

- Argo Rollouts
- Flagger

are commonly used.

______________________________________________________________________

# CI/CD Pipeline

Typical pipeline

```text id="dep6816"
Code

↓

Build

↓

Test

↓

Deploy

↓

Monitor

↓

Rollback (if needed)
```

Deployment

doesn't end

when

the application

starts.

Monitoring

continues

after release.

______________________________________________________________________

# FastAPI Example

Suppose

Version 2

adds

a recommendation engine.

Deploy

using

Canary.

5%

of users

receive

the new version.

Monitor:

- Error Rate
- Latency
- Recommendation Click Rate

If

everything looks good,

increase

traffic gradually.

______________________________________________________________________

# AI/ML Example

Suppose

you train

a better

recommendation model.

Should

all users

immediately

receive it?

No.

Deploy

the new model

to

10%

of users.

Compare:

- Click-through Rate
- Latency
- Revenue
- Accuracy

If

the model

performs better,

increase rollout.

This is

Model Canary Deployment.

______________________________________________________________________

# Database Challenge

Interview favorite.

Suppose

Version 2

requires

a new database column.

If

Version 1

still runs,

both versions

must work

with

the database.

Therefore,

database migrations

should usually be:

- Backward compatible
- Forward compatible

Deploy

schema changes

before

application changes

when possible.

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce platform

deploys

Checkout v2.

Deployment:

```text id="dep6817"
1%

↓

5%

↓

20%

↓

100%
```

Operations teams

monitor:

- Checkout failures
- Revenue
- Payment success rate
- Response time

If

checkout failures

increase,

traffic

returns

to

Version 1.

______________________________________________________________________

# Blue-Green vs Canary

Interview favorite.

| Blue-Green | Canary |
| -------------------------- | --------------------------- |
| Two environments | One environment |
| Traffic switches instantly | Traffic increases gradually |
| Fast rollback | Lower deployment risk |
| Higher infrastructure cost | Better production testing |

______________________________________________________________________

# Rolling vs Canary

| Rolling | Canary |
| ------------------------------- | --------------------------- |
| Replaces instances gradually | Splits user traffic |
| Kubernetes default | Requires traffic routing |
| Less control over user exposure | Precise traffic percentages |

______________________________________________________________________

# Benefits

Modern deployment strategies provide:

✅ Zero downtime

✅ Safer releases

✅ Faster rollback

✅ Better production confidence

______________________________________________________________________

# Drawbacks

They also introduce:

❌ Infrastructure complexity

❌ Monitoring requirements

❌ Deployment automation

❌ Version compatibility concerns

______________________________________________________________________

# When NOT to Use Blue-Green

Blue-Green

may not

be practical

for:

- Small applications
- Limited infrastructure budgets
- Short-lived internal tools

Rolling Deployments

are often

sufficient.

______________________________________________________________________

# Best Practices

✅ Automate deployments.

✅ Automate rollbacks.

✅ Use health checks.

✅ Monitor business metrics

after deployment.

______________________________________________________________________

# Common Mistakes

### Deploying Everything at Once

Large deployments

increase

the impact

of bugs.

Prefer

gradual rollouts.

______________________________________________________________________

### Ignoring Monitoring

A successful deployment

requires

continuous monitoring,

not

just

successful startup.

______________________________________________________________________

### Forgetting Database Compatibility

Application

and database

must remain

compatible

during deployment.

______________________________________________________________________

### Manual Rollbacks

Automated rollback

reduces

incident response time

and

human error.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between Blue-Green Deployment and Canary Deployment?

Blue-Green Deployment maintains two identical production environments. The new version is deployed to the inactive
environment, and traffic is switched all at once after validation. If problems occur, traffic can be switched back
immediately. Canary Deployment, on the other hand, gradually exposes the new version to a small percentage of users
before increasing traffic over time. Blue-Green offers faster rollbacks, while Canary reduces deployment risk by
limiting the number of affected users during testing.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Blue-Green Deployment
- Canary Deployment
- Rolling Deployment
- Recreate Deployment
- Feature Flags
- Health Checks
- Rollbacks
- Kubernetes deployment strategies
- Best practices

______________________________________________________________________

# 🧠 Deployment & Operations Progress

You have started the **Deployment & Operations** module:

- ✅ Blue-Green & Canary Deployments

One final operational topic remains before the foundation course is complete:

> **Disaster Recovery & Backups**

This lesson ties together availability, resilience, backups, recovery strategies, and business continuity.

______________________________________________________________________

# What's Next

[Disaster Recovery & Backups](69-disaster-recovery-and-backups.md)

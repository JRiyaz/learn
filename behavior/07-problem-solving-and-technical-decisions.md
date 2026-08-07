# Problem Solving, Decision Making & Technical Judgment

This chapter separates mid-level engineers from senior engineers.

By the time you reach a Senior Software Engineer interview, companies assume you can write code.

What they really want to understand is:

> **Can you make good engineering decisions?**

Senior engineers solve problems that don't have obvious answers.

There are trade-offs.

Constraints.

Business priorities.

Technical debt.

Limited time.

Your job is to make the **best decision**, not the perfect one.

______________________________________________________________________

# What Interviewers Are Evaluating

They're looking for engineers who can:

- Analyze problems before coding
- Evaluate multiple solutions
- Understand trade-offs
- Think about long-term maintainability
- Balance business and technical needs
- Make decisions using data
- Explain *why* they made a decision

______________________________________________________________________

# Common Questions

## Problem Solving

- Tell me about a difficult technical problem.
- Tell me about your most challenging project.
- Tell me about solving a production issue.
- Tell me about debugging a difficult problem.
- Tell me about removing a bottleneck.

______________________________________________________________________

## Decision Making

- Tell me about a difficult technical decision.
- Tell me about choosing between two solutions.
- Tell me about a trade-off.
- Tell me about disagreeing with the team.
- Tell me about making a decision with limited information.

______________________________________________________________________

## Technical Judgment

- Why did you choose that architecture?
- Why did you choose Kafka?
- Why Redis?
- Why not another solution?
- What would you change today?

______________________________________________________________________

# A Framework For Every Technical Answer

Whenever you're discussing technical decisions, follow this sequence.

```
Problem

↓

Constraints

↓

Options Considered

↓

Decision

↓

Trade-offs

↓

Outcome

↓

What You Learned
```

This makes your thinking process very clear.

______________________________________________________________________

# Your Best Story

## ZSync Distributed Replication Framework

This is arguably the strongest technical story on your resume.

It demonstrates architecture, distributed systems, reliability, and technical judgment.

______________________________________________________________________

# Situation

Your system relied on ZEO servers for transaction handling.

A single point of failure meant that if one server became unavailable, availability and reliability could be affected.

The challenge wasn't simply replicating data.

It was doing so with:

- low latency
- consistency
- reliability
- minimal operational impact

______________________________________________________________________

# Task

Design a framework capable of synchronizing transactions across multiple ZEO servers while eliminating the single point
of failure.

The solution also needed to integrate into an existing production environment without negatively affecting performance.

______________________________________________________________________

# Action

Before designing anything, you evaluated the problem.

You asked questions like:

- Where is the current bottleneck?
- What actually creates the single point of failure?
- Which consistency guarantees are necessary?
- How much replication latency is acceptable?
- What happens if one node fails?
- How should recovery work?

Only after understanding these constraints did you begin designing the architecture.

The framework focused on:

- distributed replication
- low-latency synchronization
- high availability
- fault tolerance
- operational simplicity

Throughout development you continuously validated design assumptions instead of assuming the first solution was correct.

______________________________________________________________________

# Result

The final solution removed the single point of failure while enabling low-latency transaction synchronization across
multiple ZEO servers.

It significantly improved overall system reliability and created a stronger foundation for future scalability.

______________________________________________________________________

# Example Answer

> One of the most technically challenging projects I worked on was designing a distributed transaction replication framework called ZSync.

> The existing architecture depended heavily on a single ZEO server, creating a potential single point of failure. Rather than simply introducing replication, I first analyzed the reliability requirements, acceptable synchronization latency, recovery scenarios, and operational complexity.

> Based on those constraints, I designed a framework that synchronized transactions across multiple ZEO servers with low latency while minimizing changes to the existing system. Throughout development, I continuously validated design assumptions and considered how failures would affect consistency and availability.

> The result was a distributed replication framework that removed the single point of failure and significantly improved system reliability without introducing unnecessary operational complexity.

______________________________________________________________________

# Why This Is A Strong Answer

Notice that you spend most of the answer discussing:

- analysis
- trade-offs
- design thinking

—not implementation details.

Senior interviews value engineering judgment more than code.

______________________________________________________________________

# Your Second Strong Story

## Kafka Event-Driven Architecture

This story demonstrates architectural decision making.

______________________________________________________________________

# Situation

As backend services grew, synchronous communication increased coupling between services.

Changes in one service had a greater impact on others.

Scaling also became more difficult.

______________________________________________________________________

# Decision

Instead of relying entirely on synchronous service-to-service communication, you implemented an event-driven
architecture using Kafka.

______________________________________________________________________

# Why Kafka?

A strong answer should include your reasoning.

Examples:

- Better decoupling
- Improved scalability
- Asynchronous communication
- Independent deployments
- Easier future integrations

Notice that you're explaining *why*, not simply naming a technology.

______________________________________________________________________

# Trade-offs

Good interview answers always acknowledge trade-offs.

For Kafka, examples include:

Advantages

- Scalability
- Loose coupling
- Independent services
- Better throughput

Challenges

- Operational complexity
- Event ordering
- Retry handling
- Monitoring
- Eventual consistency

Interviewers love candidates who acknowledge both sides.

______________________________________________________________________

# Example Answer

> As our services grew, we realized synchronous communication was creating tighter coupling than we wanted. Before introducing a solution, we evaluated several approaches and concluded that an event-driven architecture would better support future scalability.

> We chose Kafka because it allowed services to communicate asynchronously, making deployments more independent while reducing direct dependencies between services.

> We also considered the operational trade-offs, including monitoring, retry mechanisms, and message ordering, and incorporated those into the overall design.

> The resulting architecture was significantly more scalable and easier to extend as new services were introduced.

______________________________________________________________________

# Handling Decision Questions

Interviewers often ask:

> Why didn't you choose another solution?

Don't defend your decision emotionally.

Instead discuss trade-offs.

Example:

Instead of saying

> Kafka is better.

Say

> Kafka aligned better with our scalability and decoupling requirements, although it did introduce additional operational complexity that we planned for.

This demonstrates engineering maturity.

______________________________________________________________________

# Follow-up Questions

## Why Redis?

Possible discussion points:

- fast in-memory access
- session management
- caching
- performance
- simplicity

Don't say

> Because it's fast.

Explain *why* speed mattered in your context.

______________________________________________________________________

## Why Microservices?

Avoid

> Because microservices are modern.

Instead discuss:

- deployment independence
- scalability
- team ownership
- maintainability

______________________________________________________________________

## What Would You Change Today?

Always have an answer.

Examples:

- add better monitoring
- automate deployments earlier
- improve observability
- strengthen testing
- improve documentation

Interviewers appreciate engineers who continuously reflect.

______________________________________________________________________

# Technical Judgment Tips

Whenever discussing architecture:

Mention

- trade-offs
- constraints
- alternatives
- measurements
- maintainability
- operational impact
- business goals

Avoid sounding like technology choices were obvious.

Every architectural decision has compromises.

______________________________________________________________________

# Common Mistakes

## ❌ Talking Only About Code

Senior engineers solve business problems.

Code is only one part of the solution.

______________________________________________________________________

## ❌ Pretending Every Decision Was Perfect

Good engineers revisit decisions.

Technology changes.

Requirements change.

It's perfectly acceptable to say:

> Knowing what I know today, I'd approach part of the design differently.

______________________________________________________________________

## ❌ Ignoring Business Context

Always connect technical work back to business outcomes.

Examples:

- Faster deployments
- Better reliability
- Reduced operational effort
- Improved scalability
- Lower maintenance costs
- Better developer productivity

______________________________________________________________________

# Pro Tips

One sentence that consistently impresses interviewers is:

> "Before deciding on a solution, I wanted to understand the constraints."

That sentence immediately signals senior-level thinking.

Other useful phrases include:

- We evaluated multiple approaches.
- We discussed the trade-offs.
- We optimized for maintainability.
- We prioritized operational simplicity.
- We validated our assumptions.
- We measured the impact after implementation.

These phrases demonstrate structured decision making.

______________________________________________________________________

# Practice Questions

Use your own projects to answer:

1. Tell me about the most difficult technical problem you've solved.
1. Tell me about a major architectural decision.
1. Tell me about choosing between two technical approaches.
1. Tell me about solving a production bottleneck.
1. Tell me about improving system reliability.
1. Tell me about designing a scalable system.
1. Tell me about reducing technical debt.
1. Tell me about a design you would change today.
1. Tell me about balancing business needs with technical quality.
1. Tell me about a project where trade-offs were necessary.

______________________________________________________________________

# Interview Tip

One thing interviewers consistently appreciate is when candidates say:

> "Here's what we considered before making the decision."

Most candidates jump straight to the final solution.

Senior engineers explain **how they arrived at the solution**.

That's what demonstrates technical judgment.

______________________________________________________________________

# Summary

Strong problem solvers don't immediately write code.

They:

- Understand the problem.
- Identify constraints.
- Evaluate alternatives.
- Consider trade-offs.
- Make informed decisions.
- Measure outcomes.
- Learn from the results.

Your **ZSync** and **Kafka Event-Driven Architecture** stories are ideal for demonstrating these qualities because they
show not just what you built, but how you approached complex engineering decisions.

______________________________________________________________________

# Next

[Pressure, Prioritization & Production Incidents](08-pressure-prioritization-and-incidents.md)

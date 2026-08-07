# Failure, Mistakes & Feedback

This chapter is one of the most important in the entire course.

Many candidates are uncomfortable talking about failure.

Ironically, interviewers often learn more about you from your failures than your successes.

Nobody expects a senior engineer to have a perfect career.

They expect you to:

- Admit mistakes
- Learn from them
- Improve systems
- Help others avoid repeating them

______________________________________________________________________

# What Interviewers Are Actually Evaluating

When they ask about failure, they want to know:

- Are you honest?
- Do you take accountability?
- Can you learn from mistakes?
- Do you blame others?
- Have you matured as an engineer?
- Do you improve processes after failures?

The question is NOT

> "Have you failed?"

The question is

> "What happened after you failed?"

______________________________________________________________________

# Common Questions

## Failure

- Tell me about a failure.
- Tell me about a mistake you made.
- Tell me about something you would do differently.
- Tell me about missing a deadline.
- Tell me about when things didn't go as planned.

______________________________________________________________________

## Feedback

- Tell me about receiving difficult feedback.
- Tell me about constructive criticism.
- Tell me about improving after feedback.
- Tell me about changing your approach.

______________________________________________________________________

# Choosing the Right Story

A good failure story should:

✅ Be real

✅ Be significant

✅ Be recoverable

✅ End positively

Avoid stories involving:

- Ethics violations
- Security negligence
- Dishonesty
- Major customer outages caused by carelessness

Also avoid fake failures like:

> "I work too hard."

Interviewers recognize these immediately.

______________________________________________________________________

# Your Best Story

Based on your resume, the strongest approach is **not** to invent a catastrophic failure.

Instead, use a project where the **first approach wasn't sufficient**, and explain how you improved it.

One excellent example is your **Authentication & Authorization Framework**.

______________________________________________________________________

# Story

## Situation

As your backend ecosystem grew, different services began implementing authentication in slightly different ways.

Initially, this didn't seem like a major issue.

Over time, however, inconsistencies made maintenance more difficult and contributed to authentication-related production
issues.

______________________________________________________________________

## Task

Rather than continuing to fix issues individually, you wanted to identify the root cause and build a long-term solution.

______________________________________________________________________

## Action

The first realization was that the architecture itself encouraged duplication.

Instead of patching every service independently, you proposed building a reusable Authentication & Authorization
Framework.

You:

- analyzed existing implementations
- identified common patterns
- standardized authentication flows
- reduced duplicated logic
- worked with the team to integrate the framework gradually

______________________________________________________________________

## Result

Authentication-related production incidents decreased by approximately 40%.

More importantly, future services adopted the framework from the beginning, preventing the same class of issues from
recurring.

______________________________________________________________________

# Why This Is A Good Failure Story

Notice what you're saying.

You're not saying

> "I failed."

You're saying

> "We realized our original approach didn't scale, so I took ownership of improving it."

This shows engineering maturity.

Senior engineers improve systems.

______________________________________________________________________

# Example Answer

> One experience that taught me a lot involved how authentication was implemented across multiple backend services. Initially, different services evolved independently, and authentication logic became duplicated over time. While it worked in the beginning, the inconsistencies eventually contributed to production issues and made maintenance increasingly difficult.

> Instead of continuing to fix individual problems, I stepped back and analyzed the overall architecture. I realized the real issue wasn't a specific bug—it was the lack of a standardized solution. I proposed building a reusable Authentication & Authorization Framework that centralized authentication logic while remaining flexible enough for different services.

> Rolling it out required coordination across multiple services, but once adopted, authentication-related production incidents dropped by around 40%, and future services became much easier to maintain.

> The biggest lesson I learned was that repeatedly fixing symptoms usually costs more than investing in solving the root cause.

______________________________________________________________________

# Another Excellent Story

## Autolance

This can answer:

> Tell me about a mistake.

______________________________________________________________________

## Situation

Traditional deployments occasionally caused unnecessary downtime.

Although deployments succeeded, they weren't as reliable as they could be.

______________________________________________________________________

## Lesson

Instead of accepting downtime as "normal," you investigated deployment behavior and designed Autolance.

______________________________________________________________________

## Result

Downtime reduced by 40%.

______________________________________________________________________

Notice again:

The failure isn't

> "I broke production."

It's

> "I recognized an engineering weakness and improved the system."

That's a much stronger senior-level answer.

______________________________________________________________________

# Receiving Feedback

Interviewers also ask:

> Tell me about feedback you received.

Many candidates answer this poorly.

Good engineers seek feedback.

Great engineers apply it.

______________________________________________________________________

# Example Answer

> Earlier in my career, I received feedback that I sometimes focused heavily on implementing technical solutions without communicating enough context to the rest of the team.

> I realized that even a good technical solution loses value if teammates don't understand the reasoning behind it. After receiving that feedback, I started documenting design decisions more thoroughly, explaining trade-offs during technical discussions, and writing clearer API documentation.

> Over time, this improved collaboration across the team and also reduced onboarding time for new developers.

______________________________________________________________________

Why this works:

- The feedback is believable.
- It doesn't question your technical ability.
- You clearly demonstrate improvement.

______________________________________________________________________

# A Story You Should Never Tell

Avoid stories like:

> I accidentally deleted the production database.

Unless the interview is specifically about incident response, this creates unnecessary concern.

Interviewers may spend the rest of the interview wondering about your judgment rather than your recovery.

______________________________________________________________________

# Follow-up Questions

## What would you do differently?

Always answer this.

Possible examples:

- Involve stakeholders earlier.
- Validate assumptions sooner.
- Create smaller milestones.
- Improve documentation.
- Add monitoring sooner.
- Automate repetitive tasks.
- Gather feedback earlier.

Never say

> Nothing.

______________________________________________________________________

## What did you learn?

This is the most important question.

Possible lessons:

- Solve root causes.
- Communicate earlier.
- Validate assumptions.
- Measure before optimizing.
- Prioritize maintainability.
- Design for future growth.
- Document technical decisions.

______________________________________________________________________

## Did you make the same mistake again?

The answer should be

No.

Explain what changed.

______________________________________________________________________

# Common Mistakes

## ❌ Blaming Others

Bad

> QA didn't test properly.

Good

> We realized our testing process had gaps, and I helped improve it.

______________________________________________________________________

## ❌ Hiding Your Role

Don't say

> The team failed.

Say

> I was responsible for...

Interviewers want accountability.

______________________________________________________________________

## ❌ Picking A Tiny Failure

"I forgot to attend a meeting."

Too small.

______________________________________________________________________

## ❌ Picking A Catastrophic Failure

Avoid stories that permanently damaged trust or suggest poor judgment.

Choose a story that demonstrates growth.

______________________________________________________________________

# Pro Tips

When discussing failures:

Focus less on

The mistake.

Focus more on

The analysis.

Focus even more on

The improvement.

Interviewers remember people who continuously improve systems.

______________________________________________________________________

# Practice Questions

Use your own experiences to answer:

1. Tell me about a failure.
1. Tell me about a mistake you made.
1. Tell me about a difficult lesson.
1. Tell me about receiving constructive feedback.
1. Tell me about improving after criticism.
1. Tell me about changing your mind.
1. Tell me about a project that didn't go as planned.
1. Tell me about solving the wrong problem first.
1. Tell me about something you'd do differently today.
1. Tell me about learning from experience.

______________________________________________________________________

# Interview Tip

One of the biggest differences between junior and senior engineers is how they talk about mistakes.

A junior engineer often says:

> "I fixed the bug."

A senior engineer says:

> "I identified why the bug happened, improved the architecture, added safeguards, and prevented similar issues from happening again."

The second answer demonstrates engineering maturity because it focuses on long-term improvement rather than short-term
fixes.

______________________________________________________________________

# Summary

Every engineer encounters setbacks.

Strong candidates don't try to hide them.

Instead, they demonstrate:

- Accountability
- Reflection
- Continuous improvement
- Long-term thinking
- Better engineering practices

Your strongest stories in this area are **Authentication & Authorization Framework** and **Autolance**, because they
show how recognizing weaknesses led to lasting architectural improvements rather than temporary fixes.

______________________________________________________________________

# Next

[Problem Solving, Decision Making & Technical Judgment](07-problem-solving-and-technical-decisions.md)

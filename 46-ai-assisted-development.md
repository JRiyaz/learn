# 46. AI-Assisted Software Engineering

**Previous:** [45. Resume & Project Deep Dive](./45-resume-projects.md)

**Next:** [47. Rapid-Fire Python Backend Q&A](./47-rapid-fire-python-backend.md)

______________________________________________________________________

## Objective

AI-assisted software engineering is increasingly becoming part of normal backend development.

The important interview topic is not:

> "Can you use an AI coding tool?"

It is:

> **"Can you use AI to increase engineering productivity while retaining technical judgment, correctness, security and ownership?"**

AI can help with:

```text
Coding
Debugging
Refactoring
Testing
Code review
Documentation
Repository understanding
```

But AI-generated output must be treated as:

```text
Candidate solution
→ Verify
→ Test
→ Review
→ Adapt
→ Own
```

The engineer remains responsible for the resulting software.

______________________________________________________________________

# Part 1 — AI-Assisted Coding

# 1. What Is AI-Assisted Coding?

AI-assisted coding means using AI tools to support software development activities.

Examples:

```text
Generate a function
Explain existing code
Suggest implementation approaches
Generate tests
Refactor code
Find potential bugs
Generate documentation
Explain an unfamiliar repository
```

AI should generally be treated as an engineering assistant rather than an autonomous owner of the codebase.

______________________________________________________________________

# 2. Good Uses of AI for Coding

AI can be useful for:

```text
Boilerplate
Repetitive code
Small utility functions
Test scaffolding
Documentation drafts
Code explanations
Refactoring suggestions
Alternative implementations
```

Example:

```text
Developer:
"Generate a Pydantic model for this API payload."

AI:
→ Draft implementation

Developer:
→ Review
→ Adapt
→ Run tests
→ Verify behavior
```

The important part is the verification step.

______________________________________________________________________

# 3. AI Does Not Replace Engineering Judgment

AI can generate code that:

```text
Looks correct
Compiles
Passes a narrow test
```

and is still wrong.

Possible problems:

```text
Incorrect business logic
Security vulnerabilities
Race conditions
Poor database queries
Incorrect assumptions
Incompatible dependencies
Performance problems
```

Therefore:

> **Generated code is not automatically trusted code.**

______________________________________________________________________

# 4. AI-Assisted Coding Workflow

A practical workflow:

```text
Understand requirement
        ↓
Give AI relevant context
        ↓
Generate suggestion
        ↓
Review reasoning/code
        ↓
Run tests
        ↓
Run static checks
        ↓
Review security/performance
        ↓
Integrate
        ↓
Own the result
```

Do not skip the human review step.

______________________________________________________________________

# Part 2 — Debugging

# 5. AI-Assisted Debugging

AI can help analyze:

```text
Stack traces
Logs
Exceptions
Error messages
Code paths
Configuration
Potential causes
```

For example:

```text
Error:
TimeoutError connecting to PostgreSQL

Provide:
- stack trace
- relevant connection code
- configuration
- recent changes
- observed symptoms
```

AI can suggest hypotheses.

It should not be treated as proof of the root cause.

______________________________________________________________________

# 6. Hypothesis-Driven Debugging

A good workflow is:

```text
Observed symptom
      ↓
Possible causes
      ↓
Evidence needed
      ↓
Experiment
      ↓
Result
      ↓
Root cause
```

AI can help generate:

```text
Possible causes
Diagnostic commands
Instrumentation ideas
Test cases
```

But the engineer must validate them against the actual system.

______________________________________________________________________

# 7. Example Debugging Interaction

Instead of:

```text
"Why is my API slow?"
```

provide structured context:

```text
Endpoint:
GET /orders

Observed:
p95 increased from 200 ms to 1.2 s

Database:
PostgreSQL

Recent change:
Added customer filtering

Query:
...

EXPLAIN output:
...

Application metrics:
...
```

This gives the AI a much better basis for reasoning.

______________________________________________________________________

# 8. Do Not Accept the First Diagnosis

Suppose AI says:

```text
"The problem is the database index."
```

Ask:

```text
What evidence supports that?
What else could cause the latency?
What would distinguish those hypotheses?
What measurement should I collect?
```

This turns AI into a reasoning assistant rather than an authority.

______________________________________________________________________

# Part 3 — Refactoring

# 9. AI-Assisted Refactoring

AI can help with:

```text
Extracting functions
Renaming variables
Reducing duplication
Improving readability
Converting patterns
Adding type hints
Modernizing syntax
```

Example:

```text
Legacy function
     ↓
Ask AI to identify responsibilities
     ↓
Review proposed decomposition
     ↓
Add tests
     ↓
Refactor
     ↓
Run tests
```

______________________________________________________________________

# 10. Refactoring Safety

Before a significant AI-generated refactor:

```text
Understand existing behavior
        ↓
Add/verify tests
        ↓
Make small changes
        ↓
Run tests
        ↓
Review diff
```

The biggest danger is changing behavior while believing you are only improving structure.

______________________________________________________________________

# 11. AI and Legacy Code

AI can be especially useful for unfamiliar legacy code.

Ask it to:

```text
Explain the control flow
Identify dependencies
Identify side effects
Describe state transitions
Suggest tests
Identify suspicious areas
```

But verify the explanation against the source code.

AI may infer behavior that does not actually exist.

______________________________________________________________________

# Part 4 — Test Generation

# 12. AI-Assisted Test Generation

AI can generate:

```text
Unit tests
Integration tests
API tests
Edge cases
Fixtures
Mock setups
Parameterized tests
```

Example:

```text
Function
    ↓
AI-generated test cases
    ↓
Review expected behavior
    ↓
Run tests
    ↓
Add missing cases
```

______________________________________________________________________

# 13. Good Test Prompt

Instead of:

```text
"Write tests for this function."
```

provide:

```text
Function:
...

Expected behavior:
...

Invalid inputs:
...

Business constraints:
...

External dependencies:
...

Testing framework:
pytest
```

The resulting tests are more likely to reflect the intended behavior.

______________________________________________________________________

# 14. Tests Can Be Wrong Too

AI-generated tests may:

```text
Test implementation details
Miss important edge cases
Assert incorrect behavior
Overuse mocks
Duplicate existing tests
Create brittle assertions
```

A passing AI-generated test does not prove that the implementation is correct.

The engineer must verify the test's expected behavior.

______________________________________________________________________

# 15. Test Quality Question

Ask:

> **"If the implementation were wrong, would this test actually fail?"**

This is a useful way to evaluate generated tests.

A test that merely confirms the current implementation may provide little protection.

______________________________________________________________________

# Part 5 — Code Review

# 16. AI-Assisted Code Review

AI can review a diff for possible:

```text
Bugs
Security issues
Performance problems
Missing error handling
Missing tests
Readability problems
Potential race conditions
```

A useful workflow:

```text
Developer creates change
        ↓
AI preliminary review
        ↓
Developer fixes obvious issues
        ↓
Human code review
        ↓
Tests / CI
```

AI should supplement rather than replace human review.

______________________________________________________________________

# 17. Ask AI for Review by Category

Instead of:

```text
"Review this code."
```

ask specifically:

```text
Review this diff for:
1. correctness
2. concurrency issues
3. SQL/query problems
4. security vulnerabilities
5. error handling
6. performance
7. test gaps
```

Specific review criteria generally produce more useful output.

______________________________________________________________________

# 18. Human Code Review Still Matters

Human reviewers understand things AI may not fully know:

```text
Business context
Team conventions
Architecture constraints
Operational history
Product priorities
Known technical debt
Organizational constraints
```

AI can inspect code.

Humans remain responsible for the engineering decision.

______________________________________________________________________

# Part 6 — Documentation

# 19. AI-Assisted Documentation

AI is useful for drafting:

```text
README files
API descriptions
Docstrings
Architecture summaries
Runbooks
Migration notes
Release notes
```

Example:

```text
Source code
   ↓
AI-generated documentation draft
   ↓
Engineer verification
   ↓
Published documentation
```

______________________________________________________________________

# 20. Documentation Verification

AI-generated documentation can contain:

```text
Incorrect assumptions
Outdated behavior
Invented configuration
Missing edge cases
Incorrect examples
```

Therefore:

> **Documentation should be verified against the actual implementation.**

______________________________________________________________________

# Part 7 — Repository Understanding

# 21. AI for Repository Understanding

Large repositories can be difficult to understand.

AI can help answer:

```text
Where does the request enter?
Where is authentication performed?
Where is the database session created?
Where are transactions committed?
Where are background jobs started?
Where are exceptions handled?
Where are configuration values loaded?
```

______________________________________________________________________

# 22. Repository Exploration Workflow

Use a structured approach:

```text
Repository structure
        ↓
Entry points
        ↓
Configuration
        ↓
Request flow
        ↓
Business logic
        ↓
Persistence
        ↓
Async/background processing
        ↓
Tests
        ↓
Deployment
```

Do not ask the AI to understand an entire repository blindly.

Give it focused tasks.

______________________________________________________________________

# 23. Build a Mental Model

AI can help create a first-pass map:

```text
API
 ↓
Router
 ↓
Dependency
 ↓
Service
 ↓
Repository
 ↓
Database
```

Then verify each connection in the source.

The goal is to build **your own understanding**, not outsource understanding to the model.

______________________________________________________________________

# Part 8 — Prompting

# 24. What Makes a Good Engineering Prompt?

A useful prompt often contains:

```text
Context
Goal
Constraints
Relevant code/data
Expected behavior
Environment
Output format
```

Example:

```text
Context:
FastAPI application using SQLAlchemy and PostgreSQL.

Goal:
Optimize this endpoint.

Constraints:
Do not change the API contract.

Symptoms:
p95 latency increased to 900 ms.

Relevant code:
...

Please:
1. identify likely bottlenecks
2. explain the reasoning
3. propose minimal changes
4. identify risks
5. propose tests
```

______________________________________________________________________

# 25. Bad vs Good Prompt

### Bad

```text
Fix this code.
```

### Better

```text
This FastAPI endpoint intermittently returns 500 errors.

Expected behavior:
...

Observed error:
...

Recent change:
...

Constraints:
Do not change the response schema.

Analyze the likely causes and propose the smallest safe fix.
Explain how I can verify the fix.
```

The second prompt provides a problem definition.

______________________________________________________________________

# 26. Ask for Reasoning, Not Just Code

Useful requests include:

```text
Explain your assumptions.
List alternative approaches.
Identify failure cases.
Identify security risks.
Explain the trade-offs.
Suggest tests.
```

This makes the output more useful for engineering decisions.

______________________________________________________________________

# 27. Iterative Prompting

Do not expect one giant prompt to solve a complex task.

Use:

```text
Understand
 ↓
Clarify
 ↓
Design
 ↓
Implement
 ↓
Test
 ↓
Review
 ↓
Refine
```

This is usually easier to verify than a single huge generated change.

______________________________________________________________________

# Part 9 — Verification

# 28. Verification Is the Most Important Skill

The AI can generate a plausible answer.

The engineer needs to determine whether it is correct.

Verification can include:

```text
Read the diff
Run unit tests
Run integration tests
Run static analysis
Run type checking
Run security checks
Run benchmarks
Inspect logs
Test failure cases
Review dependencies
```

______________________________________________________________________

# 29. Verification Pyramid

A practical sequence:

```text
Code review
    ↓
Unit tests
    ↓
Integration tests
    ↓
Static/type/security checks
    ↓
Performance validation
    ↓
Production monitoring
```

Not every change needs every step, but higher-risk changes require stronger verification.

______________________________________________________________________

# 30. Verify Generated SQL

AI can generate SQL that is syntactically valid but inefficient.

For important queries:

```text
Read SQL
 ↓
EXPLAIN
 ↓
Check indexes
 ↓
Check row estimates
 ↓
Measure execution time
```

Never assume a generated query is performant because it looks clean.

______________________________________________________________________

# 31. Verify Generated Concurrency Code

Concurrency code deserves extra scrutiny.

Look for:

```text
Race conditions
Lock ordering
Deadlocks
Shared mutable state
Cancellation handling
Timeouts
Resource cleanup
```

A small-looking code change can have large runtime consequences.

______________________________________________________________________

# Part 10 — Hallucinations

# 32. What Is an AI Hallucination?

A hallucination is when an AI produces information that appears plausible but is incorrect or unsupported.

Examples:

```text
Invented API
Incorrect library method
Nonexistent configuration option
Fake documentation
Incorrect version behavior
Made-up database feature
```

______________________________________________________________________

# 33. Why Hallucinations Matter in Engineering

They can lead to:

```text
Broken code
Incorrect architecture
Security vulnerabilities
Wrong dependencies
Incorrect production configuration
Wasted debugging time
```

Therefore:

> **Treat uncertain AI output as a hypothesis, not a fact.**

______________________________________________________________________

# 34. How to Reduce Hallucination Risk

Use:

```text
Specific context
Known versions
Actual source code
Official documentation
Tests
Compiler/type checker
Runtime verification
```

Ask:

```text
"What assumptions are you making?"
```

and:

```text
"Which parts should I verify?"
```

______________________________________________________________________

# Part 11 — Security

# 35. AI-Assisted Development and Security

AI-generated code can introduce security problems.

Potential examples:

```text
SQL injection
Command injection
Path traversal
Unsafe deserialization
Weak authentication
Incorrect authorization
Hard-coded secrets
Insecure file handling
SSRF
Sensitive logging
```

Always review generated code from a security perspective.

______________________________________________________________________

# 36. Never Blindly Accept Security-Sensitive Code

Pay extra attention to:

```text
Authentication
Authorization
Cryptography
File uploads
Shell commands
SQL queries
Secrets
Network requests
Deserialization
User-controlled paths
```

For security-sensitive changes, use trusted documentation and appropriate security review.

______________________________________________________________________

# 37. AI Security Prompt

A useful review prompt:

```text
Review this code specifically for:
- authentication issues
- authorization bypass
- injection vulnerabilities
- secret exposure
- unsafe input handling
- SSRF
- path traversal
- insecure dependencies

For each finding, explain the evidence and suggest a safe remediation.
```

Then independently verify the findings.

______________________________________________________________________

# Part 12 — Privacy

# 38. Do Not Send Sensitive Data Blindly

Before putting information into an AI tool, consider:

```text
Credentials
API keys
Passwords
Tokens
Customer data
Personal information
Production secrets
Private source code
Confidential business information
```

Follow your organization's AI and data-handling policies.

______________________________________________________________________

# 39. Data Minimization

If AI only needs:

```text
Function A
```

do not necessarily provide:

```text
Entire production repository
+
Database dump
+
Customer records
```

Provide the minimum relevant context.

This reduces privacy and security risk.

______________________________________________________________________

# 40. Redact Sensitive Information

Before sharing logs or configuration:

```text
API_KEY=********
TOKEN=********
PASSWORD=********
CUSTOMER_ID=<redacted>
```

Use sanitized examples when possible.

______________________________________________________________________

# Part 13 — Dependency Risks

# 41. AI Can Suggest Dependencies

AI may recommend:

```text
New Python package
New JavaScript package
New framework
New library
```

Do not install it blindly.

Check:

```text
Does the package actually exist?
Is it maintained?
Is the version compatible?
What license does it use?
Are there known vulnerabilities?
Is it necessary?
```

______________________________________________________________________

# 42. Dependency Verification

A practical workflow:

```text
AI suggests package
       ↓
Verify package exists
       ↓
Check official documentation
       ↓
Check maintenance/activity
       ↓
Check security advisories
       ↓
Check license/policy
       ↓
Check whether dependency is necessary
       ↓
Add only if justified
```

______________________________________________________________________

# Part 14 — Human Ownership

# 43. Who Owns AI-Generated Code?

The engineer does.

If AI generated:

```python
def process_payment(...):
    ...
```

and you merge it, you own the result.

You should be able to explain:

```text
What it does
Why it is correct
What assumptions it makes
How it fails
How it is tested
What dependencies it uses
```

______________________________________________________________________

# 44. AI Should Not Become an Accountability Shield

Avoid:

```text
"AI generated it."
```

as an explanation for a bug.

A professional response is:

```text
"I used AI to assist with the implementation, but I reviewed and
tested the resulting code. The issue was missed during validation."
```

Then explain how you would improve the process.

______________________________________________________________________

# 45. Skill Retention

Over-reliance on AI can weaken understanding.

Avoid using AI to replace:

```text
Thinking
Debugging
Reading documentation
Understanding architecture
Learning fundamentals
```

Use it to accelerate those activities.

______________________________________________________________________

# Part 15 — Practical Backend Workflow

# 46. AI-Assisted Backend Workflow

A practical workflow:

```text
1. Understand requirement
2. Inspect existing code
3. Define constraints
4. Ask AI for analysis
5. Review proposed design
6. Implement incrementally
7. Generate/expand tests
8. Run tests
9. Review diff
10. Run static/type/security checks
11. Validate performance where relevant
12. Deploy through normal process
13. Monitor production
```

AI is integrated into the workflow rather than replacing the workflow.

______________________________________________________________________

# 47. Example — Building a FastAPI Endpoint

Requirement:

```text
Create:
POST /orders
```

Workflow:

```text
Requirement
 ↓
Ask AI to propose API design
 ↓
Review request/response model
 ↓
Implement
 ↓
Generate unit/API tests
 ↓
Review validation
 ↓
Review authorization
 ↓
Run tests
 ↓
Review database transaction behavior
 ↓
Deploy
 ↓
Monitor
```

______________________________________________________________________

# 48. Example — Debugging a Slow API

```text
Symptom:
p95 = 1.5 seconds
```

Workflow:

```text
Collect metrics
 ↓
Inspect logs
 ↓
Inspect SQL
 ↓
EXPLAIN query
 ↓
Give evidence to AI
 ↓
Ask for possible causes
 ↓
Evaluate hypotheses
 ↓
Implement minimal fix
 ↓
Benchmark
 ↓
Deploy
 ↓
Compare metrics
```

AI helps with analysis, but measurements determine whether the fix actually worked.

______________________________________________________________________

# 49. Example — Refactoring Legacy Code

```text
Legacy module
 ↓
Understand behavior
 ↓
Ask AI to explain structure
 ↓
Identify responsibilities
 ↓
Add characterization tests
 ↓
Ask AI for refactoring options
 ↓
Choose design
 ↓
Refactor incrementally
 ↓
Run tests after each meaningful step
 ↓
Review diff
```

Characterization tests are especially useful when behavior is poorly documented.

______________________________________________________________________

# 50. Example — Code Review

```text
Pull Request
 ↓
AI preliminary review
 ↓
Correct obvious issues
 ↓
Human review
 ↓
CI
 ├── Tests
 ├── Type checking
 ├── Linting
 └── Security checks
 ↓
Merge
```

AI is one review input, not the approval authority.

______________________________________________________________________

# Part 16 — AI and Senior Engineers

# 51. What Changes at Senior Level?

A junior engineer may primarily use AI for:

```text
Code generation
Syntax help
Simple explanations
```

A senior engineer should also use it for:

```text
Architecture exploration
Trade-off analysis
Debugging hypotheses
Test strategy
Code review
Risk identification
Documentation
Repository understanding
```

The senior responsibility remains:

```text
Decision quality
System correctness
Operational safety
Team communication
```

______________________________________________________________________

# 52. AI as a Second Opinion

A useful mindset:

```text
My analysis
     +
AI analysis
     ↓
Compare
     ↓
Verify
     ↓
Decision
```

Do not treat AI output as a replacement for your own analysis.

______________________________________________________________________

# 53. Ask AI to Challenge Your Design

Instead of only asking:

```text
"Is this architecture good?"
```

ask:

```text
"What are the weakest assumptions in this architecture?"

"What happens if PostgreSQL becomes unavailable?"

"What happens if messages are duplicated?"

"Where can this design become a bottleneck?"

"What failure modes have I missed?"

"What would you change for 10x traffic?"
```

This can make AI more useful as a design-review partner.

______________________________________________________________________

# Part 17 — Measuring AI Productivity

# 54. More Code Is Not More Productivity

AI can increase:

```text
Lines of code
```

without increasing:

```text
Business value
Reliability
Maintainability
Developer productivity
```

Measure outcomes instead.

______________________________________________________________________

# 55. Useful Productivity Signals

Depending on the workflow:

```text
Time to implement
Time to debug
Time to review
Test quality
Defect rate
Deployment frequency
Lead time
Developer feedback
```

Avoid optimizing purely for:

```text
Lines generated
```

______________________________________________________________________

# 56. AI-Assisted Development Trade-Offs

| Benefit | Risk |
|---|---|
| Faster implementation | Incorrect code |
| Faster boilerplate | Over-generation |
| Better exploration | Hallucinations |
| Faster documentation | Outdated/inaccurate docs |
| Test generation | Weak tests |
| Debugging assistance | False diagnosis |
| Code review assistance | Missed context |
| Repository exploration | Incorrect inferred behavior |

The correct response is not to avoid AI.

It is to build strong verification practices around it.

______________________________________________________________________

# Part 18 — Interview Questions & Answers

## Q1. How do you use AI in software development?

**Answer:**

I use AI as an engineering assistant for tasks such as code generation, debugging, refactoring, test generation,
documentation and repository exploration. I still review, test and validate the output before integrating it.

______________________________________________________________________

## Q2. Do you trust AI-generated code?

**Answer:**

No code should be trusted simply because AI generated it. I treat it as a candidate implementation and verify it through
code review, tests, static checks and, where appropriate, performance and security validation.

______________________________________________________________________

## Q3. How do you use AI for debugging?

**Answer:**

I provide relevant evidence such as stack traces, logs, recent changes and metrics and ask the AI to generate possible
hypotheses. I then validate those hypotheses using measurements and experiments rather than accepting the first
diagnosis.

______________________________________________________________________

## Q4. Can AI replace code reviews?

**Answer:**

No. AI can provide a useful preliminary review, but human reviewers understand business context, architecture, team
conventions and operational constraints that may not be available to the model.

______________________________________________________________________

## Q5. Can AI replace testing?

**Answer:**

No. AI can generate test cases and scaffolding, but engineers must verify that the tests represent the intended behavior
and actually detect incorrect implementations.

______________________________________________________________________

## Q6. How do you verify AI-generated code?

**Answer:**

I review the diff, run appropriate unit and integration tests, use static/type/security checks and validate important
performance or failure behavior. The level of verification depends on the risk of the change.

______________________________________________________________________

## Q7. What is an AI hallucination?

**Answer:**

It is incorrect information presented as if it were plausible or factual. In development this can include nonexistent
APIs, incorrect library behavior or invented configuration.

______________________________________________________________________

## Q8. How do you reduce hallucination risk?

**Answer:**

I provide specific context, use known versions, ask the model to state assumptions, verify claims against source code or
official documentation and validate behavior through tests or experiments.

______________________________________________________________________

## Q9. What security risks exist with AI-generated code?

**Answer:**

AI-generated code can contain common vulnerabilities such as injection, authorization errors, insecure file handling,
SSRF, unsafe deserialization or secret exposure. Security-sensitive code needs explicit review and verification.

______________________________________________________________________

## Q10. Can you share production code with an AI tool?

**Answer:**

Only according to the organization's approved policies and the tool's data-handling rules. Sensitive information such as
credentials, customer data and secrets should not be shared without appropriate authorization. Data minimization and
redaction are important.

______________________________________________________________________

## Q11. How do you handle AI-suggested dependencies?

**Answer:**

I verify that the package exists, check its official documentation, compatibility, maintenance status, security
advisories and licensing requirements, and determine whether adding the dependency is actually justified.

______________________________________________________________________

## Q12. How do you use AI with a large repository?

**Answer:**

I use it incrementally: first understand the repository structure and entry points, then trace specific flows such as
request handling, persistence or background processing. I verify the model's explanations against the actual source.

______________________________________________________________________

## Q13. What makes a good AI coding prompt?

**Answer:**

Relevant context, a clear goal, constraints, expected behavior, environment/version information and a specific requested
output. Good prompts reduce ambiguity rather than simply asking the model to "fix" something.

______________________________________________________________________

## Q14. Should AI write an entire feature?

**Answer:**

It can assist with substantial portions of a feature, but I prefer an incremental workflow where requirements, design,
implementation and verification are separated. This makes mistakes easier to detect and review.

______________________________________________________________________

## Q15. What is the biggest risk of AI-assisted development?

**Answer:**

One major risk is accepting plausible output without understanding or verifying it. That can introduce correctness,
security, performance or maintainability problems while creating false confidence.

______________________________________________________________________

## Q16. What is the biggest benefit?

**Answer:**

AI can reduce the time spent on repetitive implementation, exploration, documentation and first-pass analysis, allowing
engineers to spend more time on higher-value reasoning and system decisions.

______________________________________________________________________

## Q17. Does using AI reduce the need to understand fundamentals?

**Answer:**

No. Strong fundamentals become more important because they allow an engineer to evaluate whether generated code and
recommendations are correct.

______________________________________________________________________

## Q18. How do you prevent over-reliance on AI?

**Answer:**

I use AI to accelerate exploration and implementation but still read the relevant code, understand the architecture,
verify behavior and make the final engineering decisions myself.

______________________________________________________________________

# Part 19 — Scenario-Based Interview Q&A

## Scenario 1 — AI Generates a Database Query

AI produces a query that looks correct.

### What do you do?

```text
Read query
→ Check correctness
→ Check indexes
→ EXPLAIN
→ Benchmark
→ Test edge cases
```

Do not deploy it simply because it executes successfully.

______________________________________________________________________

## Scenario 2 — AI Says It Found the Root Cause

### What do you do?

Ask:

```text
What evidence supports the diagnosis?
What alternative causes exist?
What experiment can confirm it?
```

Then collect evidence.

______________________________________________________________________

## Scenario 3 — AI Generates a Security Fix

### What do you do?

Treat it as high-risk code.

Verify:

```text
Security requirement
Implementation
Attack scenarios
Tests
Documentation
Trusted security guidance
```

Use appropriate human security review where necessary.

______________________________________________________________________

## Scenario 4 — AI Suggests a New Package

### What do you do?

Verify:

```text
Package existence
Official documentation
Version
Maintenance
Security
License
Necessity
```

Then decide whether the dependency is justified.

______________________________________________________________________

## Scenario 5 — AI Generates Tests and All Pass

### Is the code definitely correct?

No.

The tests themselves may be wrong or incomplete.

Ask:

```text
What behavior do the tests verify?
What edge cases are missing?
Would an intentionally incorrect implementation fail?
```

______________________________________________________________________

## Scenario 6 — AI Refactors a Critical Module

### What should you do?

Use:

```text
Existing behavior
→ Characterization tests
→ Small changes
→ Tests
→ Diff review
→ Integration validation
→ Performance validation if relevant
```

Do not accept a large unreviewed rewrite.

______________________________________________________________________

# Part 20 — Practical AI-Assisted Backend Checklist

Before asking AI:

- [ ] Understand the problem.
- [ ] Define expected behavior.
- [ ] Identify constraints.
- [ ] Remove sensitive information.
- [ ] Provide relevant context.
- [ ] Specify versions when important.

While using AI:

- [ ] Ask for alternatives.
- [ ] Ask for assumptions.
- [ ] Ask about failure cases.
- [ ] Ask about security.
- [ ] Ask about performance.
- [ ] Keep complex tasks incremental.

After receiving output:

- [ ] Read the code.
- [ ] Review the diff.
- [ ] Verify APIs and library behavior.
- [ ] Run tests.
- [ ] Add missing tests.
- [ ] Run type/static checks.
- [ ] Run security checks where appropriate.
- [ ] Benchmark performance-sensitive changes.
- [ ] Verify documentation.
- [ ] Review dependencies.
- [ ] Own the final implementation.

______________________________________________________________________

# 57. Final Interview Readiness Checklist

## AI-Assisted Coding

- [ ] Explain how you use AI for coding.
- [ ] Explain where AI is useful.
- [ ] Explain where AI is risky.
- [ ] Explain your verification workflow.

## Debugging

- [ ] Use AI to generate hypotheses.
- [ ] Provide structured evidence.
- [ ] Verify hypotheses independently.
- [ ] Avoid accepting unsupported diagnoses.

## Refactoring

- [ ] Understand behavior first.
- [ ] Use tests before significant changes.
- [ ] Refactor incrementally.
- [ ] Review the resulting diff.

## Testing

- [ ] Generate test scaffolding.
- [ ] Review generated tests.
- [ ] Identify missing edge cases.
- [ ] Ensure tests can fail on incorrect behavior.

## Code Review

- [ ] Use AI for preliminary review.
- [ ] Review correctness.
- [ ] Review security.
- [ ] Review performance.
- [ ] Review concurrency.
- [ ] Perform human review.

## Documentation

- [ ] Use AI for drafts.
- [ ] Verify against implementation.
- [ ] Check examples.
- [ ] Check for outdated assumptions.

## Repository Understanding

- [ ] Start with repository structure.
- [ ] Trace entry points.
- [ ] Trace request/data flow.
- [ ] Verify AI explanations.

## Prompting

- [ ] Provide context.
- [ ] Define goals.
- [ ] Define constraints.
- [ ] Specify expected output.
- [ ] Ask for assumptions.
- [ ] Ask for trade-offs.
- [ ] Ask for failure modes.

## Safety

- [ ] Understand hallucination risk.
- [ ] Protect sensitive data.
- [ ] Follow organizational AI policies.
- [ ] Review security-sensitive code.
- [ ] Verify dependencies.
- [ ] Retain human ownership.

______________________________________________________________________

# 58. Final Takeaways

The right mental model is:

```text
AI
 ↓
Accelerates engineering work
```

not:

```text
AI
 ↓
Replaces engineering judgment
```

A strong AI-assisted workflow is:

```text
Understand
   ↓
Contextualize
   ↓
Ask
   ↓
Evaluate
   ↓
Implement
   ↓
Test
   ↓
Verify
   ↓
Review
   ↓
Own
```

The most important skills remain:

```text
Problem solving
System understanding
Technical judgment
Verification
Security awareness
Communication
```

AI can make an engineer faster.

It does not automatically make the engineer correct.

For senior backend engineers, the highest-value use of AI is often not simply:

```text
"Write this code."
```

but:

```text
"Help me explore this problem."

"Challenge this design."

"What failure modes am I missing?"

"Review this implementation for concurrency and security risks."

"Give me alternative approaches and their trade-offs."

"Help me build a test strategy."
```

The engineer then makes the final decision.

> **Use AI aggressively for acceleration, but conservatively for trust.**

______________________________________________________________________

**Previous:** [45. Resume & Project Deep Dive](./45-resume-projects.md)

**Next:** [47. Rapid-Fire Python Backend Q&A](./47-rapid-fire-python-backend.md)

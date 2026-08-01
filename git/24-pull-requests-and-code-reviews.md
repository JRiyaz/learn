# Git - Part 24

# Pull Requests & Code Reviews

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What a Pull Request (PR) is
- Why Pull Requests are important
- The lifecycle of a Pull Request
- How code reviews work
- Best practices for writing PRs
- Common review comments
- Real-world team workflow

______________________________________________________________________

# Why Do We Need Pull Requests?

Imagine you're working in a team of 10 developers.

You complete a new feature.

Without Pull Requests,

you might directly merge your code into `main`.

What if:

- There's a bug?
- The code doesn't follow team standards?
- You forgot to handle an edge case?
- The implementation can be improved?

Pull Requests solve this problem.

______________________________________________________________________

# What is a Pull Request?

A Pull Request (PR) is a request to merge changes from one branch into another.

Usually,

it looks like this.

```text id="git2401"
feature/jwt-auth

↓

Pull Request

↓

main
```

The Pull Request gives other developers an opportunity to review the code before it becomes part of the main branch.

______________________________________________________________________

# Why is it Called a Pull Request?

The name can be confusing.

You're not asking GitHub to **push** your code.

You're asking the maintainers of the target branch to **pull** your changes into their branch.

Hence,

the name:

**Pull Request**.

______________________________________________________________________

# Typical Workflow

```text id="git2402"
Create Feature Branch

↓

Write Code

↓

Commit

↓

Push

↓

Open Pull Request

↓

Code Review

↓

Fix Review Comments

↓

Merge

↓

Delete Branch
```

This is the workflow you'll use in most software companies.

______________________________________________________________________

# Creating a Pull Request

After pushing your branch,

GitHub usually displays a button.

```text id="git2403"
Compare & Pull Request
```

Click it.

Select:

- Source Branch
- Target Branch

Example

```text id="git2404"
Source

feature/jwt-auth

↓

Target

main
```

______________________________________________________________________

# Writing a Good Pull Request

A good Pull Request explains:

- What changed
- Why it changed
- How it was tested
- Anything reviewers should pay attention to

Example

```text id="git2405"
Title

Add JWT Authentication

Description

- Added JWT login endpoint
- Added token validation
- Updated tests
- Updated API documentation
```

This helps reviewers understand your work quickly.

______________________________________________________________________

# Code Review

Another developer reviews your Pull Request.

They might check:

- Code quality
- Readability
- Performance
- Security
- Naming
- Edge cases
- Tests

The goal is to improve the code,

not criticize the developer.

______________________________________________________________________

# Common Review Comments

Examples:

```text id="git2406"
Can this method be simplified?

↓

Please add unit tests.

↓

Handle the null case.

↓

Rename this variable.

↓

Move this logic into a service.
```

These comments help improve the implementation before merging.

______________________________________________________________________

# Responding to Review Comments

Suppose a reviewer asks you to add validation.

You:

- Update your code
- Commit the changes
- Push again

```bash id="git2407"
git add .

git commit -m "Address PR review comments"

git push
```

The Pull Request updates automatically.

You don't create a new PR.

______________________________________________________________________

# Approval

Once reviewers are satisfied,

they approve the Pull Request.

Example

```text id="git2408"
Approved

↓

Ready to Merge
```

Many organizations require at least one or two approvals before merging.

______________________________________________________________________

# Merging the Pull Request

After approval,

choose a merge strategy.

Common options:

- Merge Commit
- Squash and Merge
- Rebase and Merge

We'll briefly discuss these next.

______________________________________________________________________

# Merge Strategies

### Merge Commit

Keeps the branch history exactly as it happened.

```text id="git2409"
main

↓

Merge Commit
```

______________________________________________________________________

### Squash and Merge

Combines all commits into one.

```text id="git2410"
10 Commits

↓

1 Commit
```

Very common for feature branches.

______________________________________________________________________

### Rebase and Merge

Replays commits onto the target branch,

creating a clean linear history.

No merge commit is created.

______________________________________________________________________

# Delete the Branch

After merging,

delete the feature branch.

```text id="git2411"
feature/jwt-auth

↓

Merged

↓

Deleted
```

This keeps the repository clean.

______________________________________________________________________

# Real Backend Example

Suppose you implement

Rate Limiting.

Workflow

```text id="git2412"
feature/rate-limiter

↓

Develop

↓

Commit

↓

Push

↓

Pull Request

↓

Review

↓

Fix Comments

↓

Approve

↓

Merge

↓

Delete Branch
```

This is exactly how many backend teams operate.

______________________________________________________________________

# Best Practices

### Keep Pull Requests Small

Instead of:

```text id="git2413"
5000 Lines
```

Prefer:

```text id="git2414"
200–400 Lines
```

Smaller Pull Requests are easier to review.

______________________________________________________________________

### One Feature Per Pull Request

Don't mix:

- JWT
- Docker
- Redis
- Logging

into one PR.

Keep each PR focused on a single logical change.

______________________________________________________________________

### Write Clear Descriptions

A reviewer shouldn't have to guess what changed.

Explain the purpose and impact.

______________________________________________________________________

### Respond Professionally

Code review is collaborative.

Treat feedback as a discussion about the code,

not about you.

______________________________________________________________________

# Common Mistakes

### Creating Huge Pull Requests

Large PRs are harder to review,

test,

and merge.

______________________________________________________________________

### Ignoring Review Comments

Always respond to comments,

even if you disagree.

Explain your reasoning respectfully.

______________________________________________________________________

### Merging Without Review

In team projects,

avoid merging directly into `main`

unless it's an agreed emergency process.

______________________________________________________________________

### Leaving Stale Branches

Delete feature branches after merging.

______________________________________________________________________

# Commands You'll Commonly Use

| Command | Purpose | When You'll Use It |
| ------------ | -------------------- | --------------------- |
| `git push` | Upload branch | Before opening a PR |
| `git add` | Stage review changes | Address comments |
| `git commit` | Save review changes | Update PR |
| `git push` | Update Pull Request | After review feedback |

> Most Pull Request actions (creating, reviewing, approving, and merging) are performed through platforms like GitHub, GitLab, or Bitbucket.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why do software teams use Pull Requests?

Pull Requests allow developers to review code before it is merged into the main branch. They improve code quality by
enabling discussions about implementation, identifying bugs, enforcing coding standards, and ensuring that tests and
documentation are complete. Pull Requests also provide a record of why changes were made and how they were reviewed.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What a Pull Request is
- Why Pull Requests are important
- The Pull Request lifecycle
- Code reviews
- Merge strategies
- Best practices
- Common mistakes

______________________________________________________________________

# What's Next

[Git Cheat Sheet & Interview Revision](25-git-cheat-sheet.md)

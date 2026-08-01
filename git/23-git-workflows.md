# Git - Part 23

# Git Workflows - Git Flow, GitHub Flow & Trunk-Based Development

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What a Git workflow is
- Why teams need workflows
- Git Flow
- GitHub Flow
- Trunk-Based Development
- Which workflow is most commonly used today
- Which workflow you should use

______________________________________________________________________

# Why Do We Need a Workflow?

Imagine a team of 20 developers.

Without any rules,

developers might:

- Commit directly to `main`
- Push unfinished features
- Overwrite each other's work
- Deploy unstable code

A Git workflow defines **how a team uses Git**.

Think of it as a set of team rules.

______________________________________________________________________

# What is a Git Workflow?

A Git workflow defines:

- When to create branches
- When to merge
- Who reviews code
- When code is deployed

Git itself doesn't enforce a workflow.

The development team chooses one.

______________________________________________________________________

# Workflow 1 - Git Flow

Git Flow was one of the earliest popular Git workflows.

It uses several long-lived branches.

```text id="git2301"
main

│

├── develop

│

├── feature/*

│

├── release/*

│

└── hotfix/*
```

Each branch has a specific purpose.

______________________________________________________________________

# Git Flow Branches

### main

Contains production-ready code.

______________________________________________________________________

### develop

Contains the latest completed development work.

______________________________________________________________________

### feature/\*

Used for new features.

Example

```text id="git2302"
feature/login

feature/payment

feature/jwt
```

______________________________________________________________________

### release/\*

Used while preparing a release.

Example

```text id="git2303"
release/v1.0
```

______________________________________________________________________

### hotfix/\*

Used for urgent production fixes.

Example

```text id="git2304"
hotfix/login-bug
```

______________________________________________________________________

# When Was Git Flow Popular?

Git Flow was widely used when:

- Releases happened every few months
- Teams had long release cycles
- CI/CD wasn't common

Today,

it's less common,

especially in cloud-native development.

______________________________________________________________________

# Workflow 2 - GitHub Flow

GitHub Flow is much simpler.

```text id="git2305"
main

↓

Create Feature Branch

↓

Write Code

↓

Push

↓

Pull Request

↓

Code Review

↓

Merge

↓

Delete Branch
```

That's it.

No

- develop
- release
- hotfix

branches.

Everything starts from

```text id="git2306"
main
```

______________________________________________________________________

# Why Is GitHub Flow Popular?

Because it's:

- Simple
- Easy to understand
- Great for CI/CD
- Perfect for continuous deployment

This is the workflow used by many modern software teams.

______________________________________________________________________

# Workflow 3 - Trunk-Based Development

Trunk-Based Development goes even further.

There is usually only one long-lived branch.

```text id="git2307"
main
```

Developers create

very short-lived feature branches,

or sometimes commit directly to `main`

behind feature flags.

Example

```text id="git2308"
main

↓

Small Feature

↓

Merge

↓

Small Feature

↓

Merge

↓

Deploy
```

______________________________________________________________________

# Why Do Companies Use It?

Large companies such as:

- Google
- Meta
- Netflix (varies by team)

often prefer short-lived branches

because:

- Smaller Pull Requests
- Easier reviews
- Faster deployments
- Fewer merge conflicts

______________________________________________________________________

# Workflow Comparison

| Feature | Git Flow | GitHub Flow | Trunk-Based |
| -------------------- | --------- | ----------- | ----------- |
| Complexity | High | Low | Low |
| Long-lived branches | Many | One | One |
| CI/CD Friendly | Moderate | Excellent | Excellent |
| Frequent deployments | Not ideal | Excellent | Excellent |

______________________________________________________________________

# Which Workflow Should You Use?

### Personal Projects

Use

```text id="git2309"
GitHub Flow
```

Simple,

clean,

easy to manage.

______________________________________________________________________

### Small Teams

Also use

```text id="git2310"
GitHub Flow
```

______________________________________________________________________

### Large Enterprises

Depends on the organization.

Some still use Git Flow,

while many modern engineering teams have moved to GitHub Flow or Trunk-Based Development.

______________________________________________________________________

# Typical GitHub Flow

This is what you'll likely use most often.

```text id="git2311"
git switch -c feature/login

↓

Write Code

↓

git add

↓

git commit

↓

git push

↓

Pull Request

↓

Review

↓

Merge

↓

Delete Branch
```

If you remember only one workflow from this lesson,

make it this one.

______________________________________________________________________

# Real Backend Example

Suppose you're adding JWT authentication.

```text id="git2312"
main

↓

feature/jwt-auth

↓

Develop

↓

Commit

↓

Push

↓

Pull Request

↓

Merge

↓

Delete Branch
```

This is how many backend teams work today.

______________________________________________________________________

# Common Mistakes

### Using Git Flow Everywhere

Git Flow is powerful,

but often unnecessary

for small projects.

______________________________________________________________________

### Long-Lived Feature Branches

Avoid working on the same branch

for weeks.

Merge frequently.

______________________________________________________________________

### Large Pull Requests

Smaller Pull Requests

are easier to review,

test,

and merge.

______________________________________________________________________

### Skipping Code Reviews

A workflow isn't just about Git commands.

Code review

is a critical part

of modern software development.

______________________________________________________________________

# Commands You'll Commonly Use

The workflow itself doesn't introduce new Git commands.

Instead,

it combines commands you've already learned.

Typical sequence

```bash id="git2313"
git switch -c feature/login

git add .

git commit -m "Add login API"

git push -u origin feature/login
```

Then create a Pull Request,

review,

merge,

and delete the branch.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between Git Flow and GitHub Flow?

Git Flow uses multiple long-lived branches such as `main`, `develop`, `release`, and `hotfix`, making it suitable for
structured release cycles. GitHub Flow is much simpler, using only the `main` branch and short-lived feature branches
that are merged through Pull Requests. Today, GitHub Flow is more common because it supports continuous integration and
continuous deployment more effectively.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Git workflows are
- Git Flow
- GitHub Flow
- Trunk-Based Development
- Workflow comparison
- Which workflow to choose
- Best practices

______________________________________________________________________

# What's Next

[Pull Requests & Code Reviews](24-pull-requests-and-code-reviews.md)

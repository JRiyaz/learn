# Git - Part 18

# Git Hooks - Automating Tasks with Git

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Git Hooks are
- Why Git Hooks are useful
- Common Git Hooks
- When to use them
- Where hooks are stored
- Best practices

______________________________________________________________________

# Why Do We Need Git Hooks?

Imagine this situation.

A developer writes some code.

```text
Write Code

↓

Commit

↓

Oops!

Tests Fail
```

The bad code has already been committed.

Wouldn't it be better if Git automatically ran the tests **before** allowing the commit?

That's exactly what Git Hooks are for.

______________________________________________________________________

# What are Git Hooks?

Git Hooks are scripts that Git automatically executes when specific events occur.

Think of them as **automation points**.

Example

```text
git commit

↓

Run Script

↓

Allow or Reject Commit
```

______________________________________________________________________

# Where are Git Hooks Stored?

Every Git repository contains a directory called

```text
.git/hooks
```

Example

```text
library-api/

├── .git/

│   └── hooks/

│       ├── pre-commit

│       ├── commit-msg

│       ├── pre-push

│       └── ...
```

Git looks inside this folder whenever a Git event occurs.

______________________________________________________________________

# Important Note

When you clone a repository,

Git **does not** copy the hooks.

They are local to your machine.

This prevents unknown scripts from automatically running on developers' computers.

In real projects,

teams often use tools like:

- Husky (JavaScript)
- pre-commit (Python)

to share hook configurations.

______________________________________________________________________

# Common Git Hooks

The hooks you'll encounter most often are:

| Hook | Runs When |
| ---------- | --------------------------------- |
| pre-commit | Before a commit is created |
| commit-msg | After entering the commit message |
| pre-push | Before code is pushed |
| post-merge | After a merge completes |

Let's look at each one.

______________________________________________________________________

# pre-commit

Runs **before** Git creates a commit.

Typical uses:

- Run unit tests
- Check formatting
- Run a linter
- Detect secrets in `.env`
- Prevent committing debug code

Example workflow

```text
git commit

↓

Run Tests

↓

Tests Pass?

↓

Yes → Commit

No → Reject
```

______________________________________________________________________

## When will you use this?

Very often.

Many companies don't allow commits unless:

- Tests pass
- Formatting is correct
- Linting succeeds

______________________________________________________________________

# commit-msg

Runs after you enter a commit message.

Typical uses:

- Enforce commit message format
- Require ticket numbers
- Prevent empty messages

Example

Allowed

```text
AUTH-123 Add JWT authentication
```

Rejected

```text
Update
```

______________________________________________________________________

## When will you use this?

Large teams often enforce commit message standards.

______________________________________________________________________

# pre-push

Runs before Git uploads commits.

Typical uses:

- Run integration tests
- Verify build
- Prevent pushing to protected branches

Example

```text
git push

↓

Run Tests

↓

Tests Pass?

↓

Yes → Push

No → Reject
```

______________________________________________________________________

## When will you use this?

Useful when tests are too slow to run on every commit,

but should run before sharing code.

______________________________________________________________________

# post-merge

Runs after a merge completes.

Typical uses:

- Install dependencies
- Update generated files
- Refresh configuration
- Rebuild assets

Example

```text
git pull

↓

Merge

↓

Automatically Install Dependencies
```

______________________________________________________________________

## When will you use this?

Occasionally,

especially in projects where merges require local setup.

______________________________________________________________________

# Example Hook

A simple

```text
pre-commit
```

hook might do this.

```text
Run Black

↓

Run Ruff

↓

Run Pytest

↓

Allow Commit
```

If any step fails,

the commit is blocked.

______________________________________________________________________

# Real-World Example

Suppose your team accidentally commits API keys.

To prevent this,

a pre-commit hook scans files.

```text
git commit

↓

Secret Scanner

↓

API Key Found

↓

Commit Rejected
```

This simple automation can prevent serious security incidents.

______________________________________________________________________

# Git Hooks vs CI/CD

Many beginners confuse these.

| Git Hooks | CI/CD |
| ------------------------- | -------------------------------- |
| Run on your local machine | Run on a remote server |
| Before commit or push | After code reaches GitHub/GitLab |
| Fast feedback | Full project validation |

A common workflow is:

```text
Developer

↓

Git Hook

↓

GitHub

↓

CI/CD Pipeline
```

Hooks catch problems early,

while CI/CD performs deeper validation.

______________________________________________________________________

# Common Mistakes

### Putting Heavy Tasks in pre-commit

If the hook takes several minutes,

developers may become frustrated.

Keep pre-commit hooks fast.

______________________________________________________________________

### Depending Only on Hooks

Hooks are local.

A developer can bypass them.

Critical validation should also run in CI/CD.

______________________________________________________________________

### Forgetting Hooks Aren't Shared

Cloning a repository

does not automatically install hooks.

Use dedicated tools if your team wants shared hook configurations.

______________________________________________________________________

### Blocking Every Commit

Not every check belongs in a pre-commit hook.

Choose appropriate tasks for each hook.

______________________________________________________________________

# Commands Learned

There isn't a daily Git command for hooks.

Instead,

you'll mainly work with the files inside:

```text
.git/hooks
```

The most important concepts are:

| Hook | Typical Use |
| ---------- | ---------------------------- |
| pre-commit | Tests, formatting, linting |
| commit-msg | Validate commit messages |
| pre-push | Final validation before push |
| post-merge | Local setup after merge |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What are Git Hooks, and how are they used?

Git Hooks are scripts that Git automatically executes when certain events occur, such as before a commit or before a
push. They are commonly used to automate tasks like running tests, formatting code, checking commit messages, scanning
for secrets, or preventing invalid commits. Hooks improve code quality by catching problems before changes are shared.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Git Hooks are
- Where hooks are stored
- Common hook types
- Practical use cases
- Hooks vs CI/CD
- Best practices
- Common mistakes

______________________________________________________________________

# What's Next

[Submodules - Managing External Repositories (Overview)](19-submodules.md)

# Git - Part 3

# Commits & Commit History

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What a commit is
- How to create commits
- How to write good commit messages
- How to view commit history
- Why commits should be small and meaningful

______________________________________________________________________

# What is a Commit?

A commit is a **snapshot** of your project at a specific point in time.

Imagine saving a game.

```
Level 1

↓

Save Game
```

Later,

if something goes wrong,

you can return to that save.

Git commits work the same way.

______________________________________________________________________

# Git Workflow Recap

```
Edit Files

↓

git add

↓

git commit
```

Only **staged files** become part of the commit.

______________________________________________________________________

# Creating Your First Commit

After staging your files,

run:

## Command

```bash id="git301"
git commit -m "Initial project setup"
```

Example Output

```text id="git302"
[main abc1234]

Initial project setup

1 file changed
```

______________________________________________________________________

## When will you use this?

Whenever you complete a logical piece of work.

Examples:

- Added login API
- Fixed Redis connection bug
- Added Docker support
- Updated README

______________________________________________________________________

# What Does `-m` Mean?

```bash id="git303"
git commit -m "Added JWT authentication"
```

`-m` stands for **message**.

Every commit should have a clear description explaining **what changed**.

______________________________________________________________________

# Good Commit Messages

Good

```text id="git304"
Add JWT authentication

Fix Redis connection timeout

Implement book borrowing API

Update Docker Compose configuration
```

These immediately tell other developers what changed.

______________________________________________________________________

# Bad Commit Messages

Avoid messages like:

```text id="git305"
Update

Fix

Changes

Work

Done

asdf
```

These become meaningless after a few weeks.

______________________________________________________________________

# A Good Rule

Imagine another developer reads your commit history six months later.

Can they understand what each commit did?

If yes,

your commit messages are good.

______________________________________________________________________

# Viewing Commit History

## Command

```bash id="git306"
git log
```

Example

```text id="git307"
commit 4f7c2ab...

Author: Riyaz

Date: ...

Add JWT authentication
```

Git shows:

- Commit ID
- Author
- Date
- Commit message

______________________________________________________________________

## When will you use this?

Frequently.

Especially when you want to:

- Find an old change
- Investigate a bug
- See what changed recently

______________________________________________________________________

# Compact History

Sometimes,

the default log is too verbose.

Use:

```bash id="git308"
git log --oneline
```

Example

```text id="git309"
4f7c2ab Add JWT authentication

91ad2be Add Redis caching

af23b7d Initial project setup
```

Much easier to read.

______________________________________________________________________

## When will you use this?

Almost daily.

Most developers prefer this format.

______________________________________________________________________

# Visualizing History

As your project grows,

branches appear.

You can view them using:

```bash id="git310"
git log --oneline --graph
```

Example

```text id="git311"
* Add JWT

* Add Redis

* Initial setup
```

Later,

when we learn branches,

this graph becomes very useful.

______________________________________________________________________

# What Should One Commit Contain?

One logical change.

Good example:

```
Add User Login

↓

models.py

routes.py

schemas.py
```

Everything belongs to one feature.

One commit.

______________________________________________________________________

Bad example:

```
JWT

↓

Docker

↓

README

↓

Bug Fix

↓

Redis

↓

Random Changes
```

All mixed together.

Very difficult to understand later.

______________________________________________________________________

# Commit Often

Don't wait until Friday evening.

Instead,

commit after each completed task.

Example

```
Morning

↓

Database Models

↓

Commit

↓

Afternoon

↓

REST APIs

↓

Commit

↓

Evening

↓

Redis Cache

↓

Commit
```

Small commits are much easier to review and debug.

______________________________________________________________________

# Why Commits Matter

Suppose

today's code works.

Tomorrow

you introduce a bug.

Git allows you to return to yesterday's commit.

Without commits,

recovering old code becomes much harder.

______________________________________________________________________

# Common Mistakes

### Giant Commits

Avoid committing hundreds of unrelated changes together.

______________________________________________________________________

### Meaningless Messages

Avoid

```
Update

Fix

Changes
```

Be descriptive.

______________________________________________________________________

### Forgetting to Stage Files

Only staged files are committed.

Always check:

```bash id="git312"
git status
```

before committing.

______________________________________________________________________

### Committing Broken Code

Whenever possible,

commit code that builds and passes basic tests.

This makes the project history more reliable.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| --------------------------- | ------------------------ | --------------------------------- |
| `git commit -m "message"` | Create a commit | After completing a logical change |
| `git log` | View full commit history | Investigating project history |
| `git log --oneline` | Compact commit history | Daily usage |
| `git log --oneline --graph` | Visualize commit history | Working with branches |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is a Git commit, and what makes a good commit?

A Git commit is a snapshot of the project's staged changes at a specific point in time. A good commit represents one
logical unit of work, has a clear and descriptive commit message, and is small enough to be easily understood, reviewed,
or reverted if necessary.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What a commit is
- How to create commits
- Writing meaningful commit messages
- Viewing commit history
- Using `git log`
- Using `git log --oneline`
- Why small commits are important

______________________________________________________________________

# What's Next

[Branches - Working on Multiple Features Safely](04-branches.md)

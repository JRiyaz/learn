# Git - Part 16

# Squashing Commits

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What squashing commits means
- Why developers squash commits
- How to squash commits
- Merge Squash vs Interactive Rebase Squash
- When to use each approach
- Best practices

______________________________________________________________________

# What is Squashing?

Squashing means **combining multiple commits into a single commit**.

Instead of this history

```text id="git1601"
Add Login API

↓

Fix Typo

↓

Forgot Import

↓

Remove Debug

↓

Update README
```

you get

```text id="git1602"
Implement Login Feature
```

The project history becomes much cleaner.

______________________________________________________________________

# Why Squash Commits?

During development,

your commits often look like this.

```text id="git1603"
Initial Code

↓

Fix Bug

↓

Fix Another Bug

↓

Forgot Import

↓

Remove Print

↓

Final Fix
```

These commits are useful while you're working,

but they don't provide much value after the feature is complete.

Instead,

combine them into one meaningful commit.

______________________________________________________________________

# When Will You Use It?

Very often.

Typical workflow:

```text id="git1604"
Develop Feature

↓

Many Small Commits

↓

Squash

↓

Create Pull Request
```

This is common in professional software teams.

______________________________________________________________________

# Method 1

## Interactive Rebase

We learned this in the previous lesson.

Run

```bash id="git1605"
git rebase -i HEAD~5
```

Then change

```text id="git1606"
pick
```

to

```text id="git1607"
squash
```

Example

```text id="git1608"
pick Add Login

squash Fix Typo

squash Forgot Import

squash Remove Debug
```

Git combines everything into one commit.

______________________________________________________________________

## When will you use this?

Before pushing your branch

or before opening a Pull Request.

______________________________________________________________________

# Method 2

## Squash Merge

Many Git hosting platforms,

including GitHub,

allow you to squash commits when merging.

Workflow

```text id="git1609"
Feature Branch

↓

Pull Request

↓

Squash and Merge

↓

One Commit on Main
```

This keeps the `main` branch history clean,

even if the feature branch had many commits.

______________________________________________________________________

## When will you use this?

When your team uses Pull Requests

and prefers one commit per feature.

______________________________________________________________________

# Example

Feature branch history

```text id="git1610"
Commit 1

↓

Commit 2

↓

Commit 3

↓

Commit 4
```

After Squash Merge

```text id="git1611"
Main

↓

Implement Authentication
```

The intermediate commits remain on the feature branch,

but `main` receives only one clean commit.

______________________________________________________________________

# Should You Always Squash?

No.

It depends on the team.

### Squash

Good for:

- Small features
- Bug fixes
- Personal projects
- Clean history

______________________________________________________________________

### Don't Squash

Sometimes,

each commit tells an important story.

Example

```text id="git1612"
Database Migration

↓

Backend API

↓

Frontend Update
```

These may deserve separate commits.

______________________________________________________________________

# Benefits of Squashing

- Cleaner history
- Easier code reviews
- Simpler rollbacks
- Easier debugging
- Better release history

______________________________________________________________________

# Drawbacks

After squashing,

the detailed development history is lost.

Example

Instead of

```text id="git1613"
10 Development Commits
```

you only have

```text id="git1614"
1 Final Commit
```

Sometimes,

those intermediate commits can be useful for investigation.

______________________________________________________________________

# Real-World Example

Suppose you're implementing JWT Authentication.

During development,

you create:

```text id="git1615"
Create JWT

↓

Fix Secret Key

↓

Fix Token Expiry

↓

Update Tests

↓

Remove Debug Logs
```

Before merging,

squash them into

```text id="git1616"
Implement JWT Authentication
```

Now the project history is much easier to understand.

______________________________________________________________________

# Common Mistakes

### Squashing Shared History

Don't rewrite history

after other developers have started using it.

______________________________________________________________________

### Squashing Unrelated Features

Only combine commits

that belong to the same logical change.

______________________________________________________________________

### Huge Squashed Commits

Avoid creating one massive commit

that contains multiple unrelated features.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| ---------------------- | ----------------------------------------- | -------------------- |
| `git rebase -i HEAD~N` | Squash local commits | Before pushing or PR |
| `squash` | Combine commits during interactive rebase | Clean commit history |

> Squash Merge is usually performed through your Git hosting platform (such as GitHub) during the Pull Request merge process rather than with a daily Git CLI command.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why do software teams squash commits?

Software teams squash commits to create a clean and meaningful project history. During development, developers often
make many small commits for fixes and experiments. Before merging, these commits are combined into a single logical
commit representing the completed feature, making code reviews, debugging, and release history easier to understand.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What squashing is
- Why teams squash commits
- Interactive Rebase squashing
- Squash Merge
- Benefits and drawbacks
- Best practices

______________________________________________________________________

# What's Next

[Git Bisect - Finding the Commit That Introduced a Bug](17-git-bisect.md)

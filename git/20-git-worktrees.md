# Git - Part 20

# Git Worktrees

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Git Worktrees are
- Why Worktrees exist
- How to create a Worktree
- How to list Worktrees
- How to remove Worktrees
- When to use Worktrees
- Worktrees vs Clone

______________________________________________________________________

# Why Do We Need Worktrees?

Imagine this situation.

You're working on a feature.

```text id="git2001"
feature/jwt-auth
```

Suddenly,

a production issue appears.

You need to fix it immediately.

Normally,

you would switch branches.

But your current branch contains

unfinished work.

You don't want to:

- Commit unfinished code
- Create a stash
- Lose your progress

Git Worktrees solve this problem.

______________________________________________________________________

# What is a Git Worktree?

A Git Worktree allows one Git repository

to be checked out

into **multiple working directories**.

Think of it like this.

```text id="git2002"
One Repository

↓

Working Directory A

(main)

↓

Working Directory B

(feature)

↓

Working Directory C

(hotfix)
```

Each directory

is on a different branch,

but all of them share

the same Git repository.

______________________________________________________________________

# Real-World Example

Suppose you're working on

```text id="git2003"
feature/payment
```

At the same time,

you need to investigate

a production issue.

Instead of interrupting your current work,

create another working directory.

```text id="git2004"
project/

↓

feature/payment

project-hotfix/

↓

hotfix/login
```

Now you can work on both

simultaneously.

______________________________________________________________________

# Create a Worktree

## Command

```bash id="git2005"
git worktree add ../library-api-hotfix hotfix/login
```

Meaning

```text id="git2006"
Create New Folder

↓

Checkout

↓

hotfix/login
```

If the branch doesn't exist,

Git creates it automatically.

______________________________________________________________________

## When will you use this?

Whenever you need

multiple branches

open at the same time.

______________________________________________________________________

# List Worktrees

## Command

```bash id="git2007"
git worktree list
```

Example

```text id="git2008"
/projects/library-api

main

/projects/library-api-hotfix

hotfix/login
```

This shows

all active worktrees.

______________________________________________________________________

# Remove a Worktree

Suppose

you're finished

with the hotfix.

Remove it.

```bash id="git2009"
git worktree remove ../library-api-hotfix
```

The extra working directory

is deleted.

The branch itself

is **not** deleted.

______________________________________________________________________

## When will you use this?

After completing

a feature

or hotfix.

______________________________________________________________________

# Typical Workflow

```text id="git2010"
Main Project

↓

Feature Branch

↓

Need Hotfix

↓

Create Worktree

↓

Fix Bug

↓

Merge

↓

Remove Worktree

↓

Continue Feature
```

Notice

you never interrupted

your feature work.

______________________________________________________________________

# Worktree vs Clone

Many beginners ask:

> Why not just clone the repository again?

Here's the difference.

| Worktree | Clone |
| ----------------------------------- | ---------------------------------------- |
| Shares the same Git repository | Creates a completely separate repository |
| Saves disk space | Uses more disk space |
| Shares commit history automatically | Independent repository |
| Faster to create | Slower |

______________________________________________________________________

# Real Backend Example

Suppose

you're building

a Library API.

You have

```text id="git2011"
feature/auth
```

open.

Meanwhile,

QA reports

a Docker issue.

Create another worktree.

```text id="git2012"
library-api/

↓

feature/auth


library-api-docker/

↓

hotfix/docker
```

Both projects

can remain open

in separate IDE windows.

______________________________________________________________________

# Advantages

- No need to stash work
- No need to clone again
- Multiple branches open simultaneously
- Faster context switching
- Shared Git history

______________________________________________________________________

# Disadvantages

- Slightly more advanced
- Multiple folders to manage
- Easy to forget old worktrees

______________________________________________________________________

# When Will You Use Worktrees?

Most useful when:

- Working on multiple features
- Production hotfixes
- Comparing branches
- Large repositories
- Code reviews

______________________________________________________________________

# Common Mistakes

### Deleting the Folder Manually

Always use

```bash id="git2013"
git worktree remove
```

instead of deleting the directory directly.

______________________________________________________________________

### Forgetting Which Worktree You're In

Each worktree

is on a different branch.

Check

```bash id="git2014"
git branch
```

if you're unsure.

______________________________________________________________________

### Thinking Worktrees Replace Branches

They don't.

A worktree is simply

another working directory

for a branch.

______________________________________________________________________

### Creating Too Many Worktrees

Remove worktrees

when you're finished.

This keeps your workspace organized.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| ---------------------------------- | ------------------ | ------------------------------------- |
| `git worktree add <path> <branch>` | Create a worktree | Work on another branch simultaneously |
| `git worktree list` | View all worktrees | Manage worktrees |
| `git worktree remove <path>` | Remove a worktree | Cleanup |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What problem do Git Worktrees solve?

Git Worktrees allow multiple branches from the same Git repository to be checked out into separate working directories
simultaneously. This lets developers work on features, bug fixes, or code reviews in parallel without switching
branches, stashing changes, or cloning the repository again.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Git Worktrees are
- Why they exist
- Creating worktrees
- Listing worktrees
- Removing worktrees
- Worktrees vs Clones
- Best practices

______________________________________________________________________

# What's Next

[Git Internals - Objects, Blobs, Trees & Commits](21-git-internals.md)

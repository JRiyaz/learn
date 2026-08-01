# Git - Part 14

# Git Rebase

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Git Rebase is
- Why teams use Rebase
- Rebase vs Merge
- How to rebase a branch
- When to use Rebase
- When **not** to use Rebase
- Common mistakes

______________________________________________________________________

# Why Do We Need Rebase?

Suppose you're working on a feature branch.

Meanwhile,

other developers continue making changes to `main`.

Your repository now looks like this.

```text
main

A

↓

B

↓

C

↓

D


feature

A

↓

B

↓

X

↓

Y
```

Now your feature branch is **behind** `main`.

You need the latest changes before merging.

There are two ways:

- Merge
- Rebase

______________________________________________________________________

# What is Rebase?

Rebase moves your commits so they appear **after** the latest commits of another branch.

Think of it as:

> "Replay my work on top of the latest code."

______________________________________________________________________

# Visual Example

Before Rebase

```text
main

A

↓

B

↓

C

↓

D


feature

A

↓

B

↓

X

↓

Y
```

Run

```bash
git rebase main
```

After Rebase

```text
main

A

↓

B

↓

C

↓

D


feature

A

↓

B

↓

C

↓

D

↓

X'

↓

Y'
```

Notice

```text
X'

Y'
```

These are **new commits**.

Git replayed your work on top of `main`.

______________________________________________________________________

# Why Use Rebase?

Without Rebase,

Git history often looks like this.

```text
A

↓

B

├──── C

│

└──── X

      │

      Y

↓

Merge Commit
```

After Rebase,

history becomes linear.

```text
A

↓

B

↓

C

↓

X

↓

Y
```

Many teams prefer this because it's easier to read.

______________________________________________________________________

# Step 1

Switch to your feature branch.

```bash
git switch jwt-auth
```

______________________________________________________________________

# Step 2

Update your local main branch.

```bash
git switch main

git pull
```

This ensures you're rebasing onto the latest code.

______________________________________________________________________

# Step 3

Switch back.

```bash
git switch jwt-auth
```

______________________________________________________________________

# Step 4

Run Rebase.

```bash
git rebase main
```

Git replays your commits on top of `main`.

______________________________________________________________________

# When Will You Use This?

Very often.

Typical workflow:

```text
Morning

↓

git pull main

↓

git rebase main

↓

Continue Development
```

This keeps your feature branch up to date.

______________________________________________________________________

# Rebase Conflicts

Rebase can produce conflicts,

just like merging.

Git pauses.

Resolve the files.

Then continue.

```bash
git rebase --continue
```

______________________________________________________________________

# Abort a Rebase

Changed your mind?

Cancel it.

```bash
git rebase --abort
```

Everything returns to the previous state.

______________________________________________________________________

# Rebase vs Merge

This is one of the most common interview questions.

| Merge | Rebase |
| ------------------------- | -------------------------------- |
| Creates a merge commit | Rewrites commit history |
| Preserves actual history | Creates a cleaner linear history |
| Safer for shared branches | Best for local feature branches |

______________________________________________________________________

# Which One Should You Use?

## Use Merge

When:

- Branches are shared
- Working with teammates
- Preserving history is important

______________________________________________________________________

## Use Rebase

When:

- Cleaning your own feature branch
- Updating your local branch
- Preparing a Pull Request
- Nobody else is using your branch

______________________________________________________________________

# Golden Rule

**Never rebase a branch that other developers are already using.**

Why?

Because Rebase rewrites commit history.

Imagine this.

Developer A

```text
Commit X
```

Developer B

also has

```text
Commit X
```

Developer A rebases.

Now

```text
Commit X
```

becomes

```text
Commit X'
```

Developer B still has the old history.

Now the two histories no longer match,

making future pulls and merges confusing.

**Rule:**

- Rebase your own local branches.
- Avoid rebasing shared branches.

______________________________________________________________________

# Real-World Example

Suppose you've been working on:

```text
feature/payment
```

for three days.

Meanwhile,

`main` receives:

- Security fixes
- Redis improvements
- Docker updates

Before creating a Pull Request,

run:

```bash
git rebase main
```

Your feature is now based on the latest code,

making the eventual merge cleaner.

______________________________________________________________________

# Common Mistakes

### Rebasing Main

Don't do this.

Usually,

you update `main` using:

```bash
git pull
```

Rebase is mainly for feature branches.

______________________________________________________________________

### Rebasing Shared Branches

This is the biggest mistake.

It rewrites history

that other developers depend on.

______________________________________________________________________

### Forgetting to Pull Main First

Always update `main`

before rebasing.

Otherwise,

you're rebasing onto outdated code.

______________________________________________________________________

### Panic During Conflicts

Rebase conflicts

are resolved the same way

as merge conflicts.

Resolve,

stage,

continue.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| ----------------------- | ---------------------------------- | --------------------- |
| `git rebase main` | Replay commits on top of main | Update feature branch |
| `git rebase --continue` | Continue after conflict resolution | During rebase |
| `git rebase --abort` | Cancel the rebase | Restart or recover |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Git Rebase, and how is it different from Merge?

Git Rebase moves the commits of one branch so they are replayed on top of another branch, creating a cleaner, linear
commit history. Unlike Merge, which creates a merge commit and preserves the exact branching history, Rebase rewrites
commit history. Rebase is commonly used on local feature branches before they are shared, while Merge is generally
preferred for integrating shared branches.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Rebase is
- Why Rebase is useful
- Rebase vs Merge
- Updating a feature branch
- Handling rebase conflicts
- When to use Rebase
- When not to use Rebase
- Best practices

______________________________________________________________________

# What's Next

[Interactive Rebase - Cleaning Up Commit History](15-interactive-rebase.md)

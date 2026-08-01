# Git - Part 22

# Git Garbage Collection & Repository Maintenance

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why Git repositories grow over time
- What Git Garbage Collection (GC) is
- What `git gc` does
- What `git prune` does
- When you'll use these commands
- Best practices

______________________________________________________________________

# Why Does a Git Repository Grow?

Imagine you're working on a project for two years.

You create:

- Thousands of commits
- Hundreds of branches
- Hundreds of merges
- Thousands of temporary objects

Even after deleting branches,

Git doesn't immediately remove everything.

Why?

Because Git wants to protect your data.

______________________________________________________________________

# What is Garbage Collection?

Garbage Collection (GC) is Git's housekeeping process.

Think of it like cleaning your room.

```text id="git2201"
Old Objects

↓

Unused Objects

↓

Compressed Objects

↓

Clean Repository
```

Git removes unnecessary data

and optimizes the repository.

______________________________________________________________________

# Does Git Run GC Automatically?

Yes.

Git automatically runs garbage collection

from time to time

when it decides the repository needs optimization.

Most developers

never have to think about it.

______________________________________________________________________

# Run Garbage Collection Manually

## Command

```bash id="git2202"
git gc
```

______________________________________________________________________

## What does it do?

Git performs several maintenance tasks, including:

- Compressing objects
- Cleaning unnecessary data
- Optimizing object storage
- Rebuilding indexes

______________________________________________________________________

## When will you use this?

Rarely.

Examples:

- Repository becomes unusually large
- After importing many commits
- After deleting many branches
- When troubleshooting repository performance

For day-to-day development,

Git usually manages this automatically.

______________________________________________________________________

# What is Pruning?

Sometimes,

Git keeps objects

that are no longer referenced.

These are called

**unreachable objects**.

Example

```text id="git2203"
Old Commit

↓

Branch Deleted

↓

Commit No Longer Reachable
```

Eventually,

Git can remove them.

______________________________________________________________________

# Prune

## Command

```bash id="git2204"
git prune
```

______________________________________________________________________

## What does it do?

It removes unreachable objects

that Git no longer needs.

______________________________________________________________________

## Should You Use It?

Generally,

**No.**

Normally,

`git gc`

runs pruning when appropriate.

Running `git prune`

manually is uncommon.

______________________________________________________________________

# Loose Objects vs Packed Objects

Initially,

Git stores objects individually.

```text id="git2205"
Blob

Blob

Blob

Commit

Tree
```

Over time,

Git packs them together.

```text id="git2206"
Pack File

↓

Many Objects
```

This reduces disk usage

and improves performance.

______________________________________________________________________

# Pack Files

Inside

```text id="git2207"
.git/objects/pack
```

Git stores compressed pack files.

These contain many objects

in an optimized format.

______________________________________________________________________

# Verify Repository Size

You can check repository statistics.

## Command

```bash id="git2208"
git count-objects -v
```

Example Output

```text id="git2209"
count: 120

size: 960

in-pack: 3400

packs: 2
```

______________________________________________________________________

## When will you use this?

Mostly when diagnosing:

- Large repositories
- Storage issues
- Git performance

______________________________________________________________________

# Verify Repository Integrity

Suppose

you suspect corruption.

Run

```bash id="git2210"
git fsck
```

______________________________________________________________________

## What does it do?

Git checks:

- Object integrity
- Missing objects
- Corrupted references
- Broken commits

Think of it as

a health check

for your repository.

______________________________________________________________________

## When will you use this?

Very rarely.

Usually only if:

- Git reports corruption
- A repository behaves unexpectedly
- You're recovering damaged history

______________________________________________________________________

# Real-World Example

Suppose

your repository has existed

for five years.

Thousands of feature branches

have been created

and deleted.

Git automatically performs maintenance

to keep the repository

small

and fast.

As a developer,

you usually don't need

to intervene.

______________________________________________________________________

# Should You Memorize These Commands?

Not really.

You should know:

- What they do
- When they're useful

You probably won't run them

every week.

______________________________________________________________________

# Common Mistakes

### Running `git prune` Without Understanding It

Avoid manually removing unreachable objects

unless you know why you're doing it.

______________________________________________________________________

### Thinking `git gc` Deletes Commits

It doesn't delete

reachable commits.

It only cleans

unnecessary data

and optimizes storage.

______________________________________________________________________

### Ignoring Repository Corruption

If Git reports corruption,

run

```bash id="git2211"
git fsck
```

before making further changes.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| ---------------------- | --------------------------- | -------------------------- |
| `git gc` | Optimize repository | Rare maintenance |
| `git prune` | Remove unreachable objects | Advanced maintenance |
| `git count-objects -v` | View object statistics | Repository diagnostics |
| `git fsck` | Verify repository integrity | Troubleshooting corruption |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What does `git gc` do?

`git gc` runs Git's garbage collection process. It optimizes the repository by compressing objects into pack files,
cleaning unnecessary data, rebuilding indexes, and improving performance. Git performs this automatically in most cases,
so developers rarely need to run it manually.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Why Git repositories grow
- Garbage Collection
- `git gc`
- `git prune`
- Pack files
- Repository statistics
- Repository integrity checks
- Best practices

______________________________________________________________________

# What's Next

[Git Workflows - Git Flow, GitHub Flow & Trunk-Based Development](23-git-workflows.md)

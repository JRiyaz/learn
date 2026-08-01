# Git - Part 13

# Cherry Pick - Applying Specific Commits

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What `git cherry-pick` is
- When to use it
- How to cherry-pick a commit
- How to cherry-pick multiple commits
- How to handle conflicts
- Common mistakes

______________________________________________________________________

# Why Do We Need Cherry Pick?

Imagine this situation.

You have two branches.

```text
main

↓

payment-feature
```

While working on the payment feature,

you accidentally fix a bug.

```text
Fix Redis Connection

↓

payment-feature
```

Now,

the Redis bug fix is needed immediately in

```text
main
```

But the payment feature is only 30% complete.

You **don't** want to merge the entire branch.

You only want **one commit**.

That's exactly what `git cherry-pick` does.

______________________________________________________________________

# What is Cherry Pick?

Cherry-picking copies **specific commit(s)** from one branch to another.

Instead of merging the whole branch,

you select only the commits you need.

Think of it like picking one apple from a tree,

not cutting down the whole tree.

______________________________________________________________________

# Visual Example

Before

```text id="git1301"
main

A

↓

B


feature

A

↓

B

↓

C

↓

D

↓

E
```

Suppose

only commit

```text
D
```

contains an important bug fix.

Cherry-pick creates

```text id="git1302"
main

A

↓

B

↓

D'
```

Notice

```text
D'
```

It is a **new commit**

with the same changes,

not the original commit.

______________________________________________________________________

# Find the Commit

First,

find the commit hash.

## Command

```bash id="git1303"
git log --oneline
```

Example

```text id="git1304"
8af21bc Fix Redis timeout

1bd72fd JWT authentication

92ca8de Docker support
```

Suppose

we want

```text
8af21bc
```

______________________________________________________________________

# Switch to the Destination Branch

Cherry-picking always applies the commit

to your **current branch**.

Example

```bash id="git1305"
git switch main
```

______________________________________________________________________

# Cherry Pick a Commit

## Command

```bash id="git1306"
git cherry-pick 8af21bc
```

Git copies

the changes

into

```text
main
```

and creates

a new commit.

______________________________________________________________________

## When will you use this?

Very often in situations like:

- Urgent bug fixes
- Production hotfixes
- Copying a useful change
- Avoiding a full merge

______________________________________________________________________

# Cherry Pick Multiple Commits

Suppose

you need

three commits.

```bash id="git1307"
git cherry-pick abc123 def456 xyz789
```

Git applies them

one after another.

______________________________________________________________________

# Cherry Pick a Range

Suppose

your history is

```text
A

↓

B

↓

C

↓

D

↓

E
```

You want

```text
C

↓

D

↓

E
```

Use

```bash id="git1308"
git cherry-pick C^..E
```

Git copies

all three commits.

______________________________________________________________________

## When will you use this?

When a feature consists of several related commits,

but you still don't want to merge the entire branch.

______________________________________________________________________

# Conflict During Cherry Pick

Cherry-pick can produce conflicts,

just like merging.

Example

```text id="git1309"
CONFLICT

↓

Resolve File

↓

git add

↓

Continue
```

Continue

```bash id="git1310"
git cherry-pick --continue
```

______________________________________________________________________

# Abort Cherry Pick

Suppose

you changed your mind.

Cancel everything.

```bash id="git1311"
git cherry-pick --abort
```

Git restores

the branch

to its previous state.

______________________________________________________________________

# Real-World Example

Imagine

your feature branch contains

```text id="git1312"
JWT

↓

Redis Bug Fix

↓

API Refactoring
```

Production only needs

the Redis fix.

Instead of merging everything,

run

```bash id="git1313"
git cherry-pick <redis-fix-commit>
```

Now

production gets

only

the bug fix.

______________________________________________________________________

# Cherry Pick vs Merge

Many developers confuse these.

| Merge | Cherry Pick |
| --------------------------- | --------------------------- |
| Brings an entire branch | Brings selected commits |
| Preserves branch history | Copies commits |
| Used for completed features | Used for individual changes |

______________________________________________________________________

# Common Mistakes

### Cherry Picking Large Features

If you need

almost every commit,

just merge the branch.

Cherry-pick is for **specific commits**.

______________________________________________________________________

### Forgetting to Switch Branches

Always check

```bash id="git1314"
git branch
```

before cherry-picking.

Git applies the commit

to the current branch.

______________________________________________________________________

### Cherry Picking the Same Commit Twice

Git treats it as a new commit.

This can duplicate changes

and create confusion.

______________________________________________________________________

### Ignoring Conflicts

Resolve conflicts carefully,

then continue

using

```bash id="git1315"
git cherry-pick --continue
```

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| ---------------------------- | ---------------------------------- | --------------------------- |
| `git cherry-pick <commit>` | Copy one commit | Bug fixes, hotfixes |
| `git cherry-pick <c1> <c2>` | Copy multiple commits | Related changes |
| `git cherry-pick C^..E` | Copy a range of commits | Several consecutive commits |
| `git cherry-pick --continue` | Continue after resolving conflicts | Conflict resolution |
| `git cherry-pick --abort` | Cancel cherry-pick | Wrong commit or restart |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** When would you use `git cherry-pick` instead of `git merge`?

`git cherry-pick` is used when only specific commits need to be copied from one branch to another, such as applying a
bug fix from a feature branch to the main branch. Unlike `git merge`, which brings the entire branch history, `git
cherry-pick` copies only the selected commit(s), creating new commits on the target branch.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Cherry Pick is
- When to use it
- Cherry-picking one commit
- Cherry-picking multiple commits
- Cherry-picking a range
- Handling conflicts
- Cherry Pick vs Merge
- Common mistakes

______________________________________________________________________

# What's Next

[Git Rebase - Keeping History Clean](14-git-rebase.md)

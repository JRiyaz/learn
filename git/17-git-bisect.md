# Git - Part 17

# Git Bisect - Finding the Commit That Introduced a Bug

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Git Bisect is
- Why it is useful
- How Git Bisect works
- The commands involved
- When to use Git Bisect
- Common mistakes

______________________________________________________________________

# Why Do We Need Git Bisect?

Imagine this situation.

Last week,

your application worked perfectly.

Today,

users report that login is broken.

Your commit history looks like this.

```text id="git1701"
Commit A

↓

Commit B

↓

Commit C

↓

Commit D

↓

Commit E

↓

Commit F
```

Somewhere between

Commit A

and

Commit F,

a bug was introduced.

Instead of checking every commit manually,

Git can find it much faster.

This is what **Git Bisect** does.

______________________________________________________________________

# What is Git Bisect?

Git Bisect is a debugging tool that uses **binary search** to find the commit that introduced a bug.

Instead of checking every commit one by one,

Git repeatedly checks the middle commit,

cutting the search space in half each time.

______________________________________________________________________

# Why is it Fast?

Suppose your project has

```text id="git1702"
1000 commits
```

Checking them one by one

could take hours.

Git Bisect uses binary search.

Example

```text id="git1703"
1000

↓

500

↓

250

↓

125

↓

63

↓

32

↓

16

↓

8

↓

4

↓

2

↓

1
```

Instead of checking 1000 commits,

you check about **10**.

______________________________________________________________________

# Real-World Example

Suppose

Commit A

works.

Commit F

is broken.

```text id="git1704"
A ✅

↓

B

↓

C

↓

D

↓

E

↓

F ❌
```

Git starts with

the middle commit.

```text id="git1705"
D
```

You test it.

If D works,

the bug must be after D.

If D is broken,

the bug must be before D.

Git keeps repeating this process

until it identifies the exact commit.

______________________________________________________________________

# Start Git Bisect

## Command

```bash id="git1706"
git bisect start
```

This tells Git

you want to begin a bisect session.

______________________________________________________________________

# Mark the Bad Commit

Usually,

this is your current commit.

```bash id="git1707"
git bisect bad
```

Meaning

```text id="git1708"
Current Commit

↓

Bug Exists
```

______________________________________________________________________

# Mark a Good Commit

Now tell Git

which older commit definitely worked.

```bash id="git1709"
git bisect good 8af21bc
```

Example

```text id="git1710"
Commit

8af21bc

↓

Working
```

Git now begins the binary search.

______________________________________________________________________

# Test the Suggested Commit

Git checks out

a commit for you.

Example

```text id="git1711"
Checking out Commit D
```

Run your application.

If it works,

tell Git.

```bash id="git1712"
git bisect good
```

If it fails,

tell Git.

```bash id="git1713"
git bisect bad
```

Git automatically moves

to the next candidate commit.

Repeat until Git finds

the first bad commit.

______________________________________________________________________

# Finish the Session

Once Git identifies

the problematic commit,

return to your original branch.

## Command

```bash id="git1714"
git bisect reset
```

______________________________________________________________________

## When will you use this?

Always after finishing a bisect session.

It restores your repository

to its original state.

______________________________________________________________________

# Typical Workflow

```text id="git1715"
Bug Found

↓

git bisect start

↓

Mark Bad Commit

↓

Mark Good Commit

↓

Test Suggested Commit

↓

good / bad

↓

Repeat

↓

Problem Commit Found

↓

git bisect reset
```

______________________________________________________________________

# Real-World Scenario

Suppose your Redis integration

stopped working.

The project has

500 commits.

Instead of reading every commit,

run Git Bisect.

Within a few minutes,

Git tells you exactly

which commit introduced the bug.

______________________________________________________________________

# When Will You Use It?

Git Bisect is especially useful when:

- A bug appeared recently
- You know an older version worked
- The project has many commits
- You can't immediately identify the cause

______________________________________________________________________

# Common Mistakes

### Not Knowing a Good Commit

Git Bisect requires:

- One known good commit
- One known bad commit

Without both,

it can't perform the search.

______________________________________________________________________

### Forgetting to Reset

Always run

```bash id="git1716"
git bisect reset
```

Otherwise,

your repository remains

checked out

at an intermediate commit.

______________________________________________________________________

### Changing Code During Bisect

Don't edit files

while running Git Bisect.

Simply test

whether the current commit is good or bad.

______________________________________________________________________

### Using Bisect for Very Small Histories

If only

2–3 commits changed,

it's usually faster

to inspect them manually.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| -------------------------- | ----------------------------- | ------------------ |
| `git bisect start` | Start bisect session | Begin bug search |
| `git bisect bad` | Mark current commit as bad | Bug exists |
| `git bisect good <commit>` | Mark known good commit | Starting point |
| `git bisect good` | Current tested commit is good | During search |
| `git bisect bad` | Current tested commit is bad | During search |
| `git bisect reset` | Exit bisect mode | Finish debugging |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Git Bisect, and why is it useful?

Git Bisect is a Git debugging tool that uses binary search to identify the commit that introduced a bug. By marking one
known good commit and one known bad commit, Git repeatedly checks out intermediate commits until it finds the first bad
commit. This is much faster than manually inspecting every commit, especially in repositories with a long history.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Git Bisect is
- How binary search helps locate bugs
- Starting a bisect session
- Marking good and bad commits
- Completing the bisect process
- Real-world debugging workflow
- Best practices

______________________________________________________________________

# What's Next

[Git Hooks - Automating Tasks with Git](18-git-hooks.md)

# Git - Part 5

# Merging Branches

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What merging is
- Why merging is needed
- How to merge a branch
- Fast-forward merge
- Three-way merge
- When you'll use each type
- Common merge mistakes

______________________________________________________________________

# Why Do We Merge?

Suppose you're working on a new feature.

You created a branch.

```
main

↓

Create Branch

↓

jwt-auth
```

You completed the feature.

Now you want everyone to use it.

How do you bring it back into the main branch?

You **merge** it.

______________________________________________________________________

# What is a Merge?

A merge combines changes from one branch into another.

```
main

│

├── jwt-auth

↓

Merge

↓

main
```

After the merge,

the changes become part of the target branch.

______________________________________________________________________

# Real-World Example

Suppose you're implementing JWT Authentication.

You work for three days on

```
jwt-auth
```

When it's tested and approved,

you merge it into

```
main
```

Now everyone gets the new feature.

______________________________________________________________________

# Before Merging

Always make sure you're on the destination branch.

Usually,

that's

```
main
```

Check your branch.

## Command

```bash id="git501"
git branch
```

Example

```text id="git502"
* jwt-auth

main
```

You're currently on

```
jwt-auth
```

Switch first.

______________________________________________________________________

# Switch to Main

## Command

```bash id="git503"
git switch main
```

Now you're ready to merge.

______________________________________________________________________

# Merge a Branch

## Command

```bash id="git504"
git merge jwt-auth
```

Meaning:

> Merge the changes from **jwt-auth** into the current branch (**main**).

______________________________________________________________________

## When will you use this?

Whenever a feature,

bug fix,

or refactoring

is complete.

This is one of the most common Git commands.

______________________________________________________________________

# Example Workflow

```
main

↓

Create jwt-auth

↓

Write Code

↓

Commit

↓

Switch to main

↓

git merge jwt-auth
```

Feature complete.

______________________________________________________________________

# Fast-Forward Merge

Suppose nobody changed

```
main
```

while you were working.

Git simply moves the branch pointer forward.

```
Before

main

↓

A

↓

B

↓

jwt-auth

↓

C
```

After merge

```
A

↓

B

↓

C

↑

main
```

Git calls this a

**Fast-Forward Merge**.

______________________________________________________________________

## Why is it called Fast-Forward?

Because Git doesn't create a new merge commit.

It simply advances the pointer.

It's fast

and keeps history simple.

______________________________________________________________________

# Three-Way Merge

Suppose another developer also modified

```
main
```

while you worked.

History now looks like this.

```
A

↓

B

├───── C (main)

└───── D (jwt-auth)
```

Git cannot fast-forward.

Instead,

it creates a new merge commit.

```
A

↓

B

├── C

└── D

↓

M
```

Where

```
M
```

is the merge commit.

______________________________________________________________________

## When will you see this?

Very often

on team projects.

Whenever multiple developers work in parallel,

Git usually performs a three-way merge.

______________________________________________________________________

# Merge Result

After a successful merge,

Git displays something like

```text id="git505"
Merge made by the 'ort' strategy.
```

or

```text id="git506"
Fast-forward
```

Both indicate

the merge succeeded.

______________________________________________________________________

# Verify the Merge

## Command

```bash id="git507"
git log --oneline --graph
```

Example

```text id="git508"
* Merge branch 'jwt-auth'

* Add JWT Authentication

* Initial Project
```

The graph now shows

the merged history.

______________________________________________________________________

# Delete the Branch

After merging,

the feature branch is usually no longer needed.

```bash id="git509"
git branch -d jwt-auth
```

This keeps your repository clean.

______________________________________________________________________

# Typical Team Workflow

```
Create Branch

↓

Write Code

↓

Commit

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

Later,

when we learn GitHub,

you'll see this workflow every day.

______________________________________________________________________

# Common Mistakes

### Merging While on the Wrong Branch

Suppose you're on

```
jwt-auth
```

and run

```bash
git merge main
```

Instead of merging your feature into main,

you've merged main into your feature.

Always check

```bash id="git510"
git branch
```

first.

______________________________________________________________________

### Forgetting to Pull Latest Changes

On team projects,

always make sure your target branch is up to date before merging.

We'll learn

```bash
git pull
```

later.

______________________________________________________________________

### Deleting the Branch Too Early

Don't delete the feature branch

until you've confirmed the merge was successful.

______________________________________________________________________

### Merging Unfinished Work

Merge only after:

- Code is complete
- Tests pass
- Review is complete

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| --------------------------- | --------------------- | ------------------ |
| `git switch main` | Switch to main branch | Before merging |
| `git merge <branch>` | Merge a branch | Finish a feature |
| `git log --oneline --graph` | View merge history | Verify merges |
| `git branch -d <branch>` | Delete merged branch | Cleanup |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between a Fast-Forward Merge and a Three-Way Merge?

A Fast-Forward Merge occurs when the target branch has not changed since the feature branch was created. Git simply
moves the branch pointer forward without creating a merge commit. A Three-Way Merge occurs when both branches have new
commits. Git combines the histories by creating a new merge commit that has both branches as parents.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What merging is
- How to merge branches
- Fast-forward merges
- Three-way merges
- Merge verification
- Merge workflow
- Common merge mistakes

______________________________________________________________________

# What's Next

[Merge Conflicts & How to Resolve Them](06-merge-conflicts.md)

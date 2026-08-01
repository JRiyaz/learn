# Git - Part 4

# Branches

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What a branch is
- Why branches are used
- How to create a branch
- How to switch branches
- How to list branches
- How to delete branches
- The most commonly used branch commands

______________________________________________________________________

# Why Do We Need Branches?

Imagine you're working on a Library API.

The current application works perfectly.

Now your manager asks you to implement JWT Authentication.

If you directly modify the main codebase,

you risk breaking the working application.

Branches solve this problem.

______________________________________________________________________

# What is a Branch?

A branch is an **independent line of development**.

Think of it as creating a copy of your project where you can safely experiment.

```text id="git401"
main

│

├── login-feature

├── jwt-auth

└── bug-fix
```

Each branch can evolve independently.

______________________________________________________________________

# Real-World Example

Suppose three developers are working on the same project.

```text id="git402"
main

│

├── Riyaz

├── Alice

└── Bob
```

Each developer creates a separate branch.

Nobody modifies the `main` branch directly.

______________________________________________________________________

# Why Not Work on Main?

Imagine this situation.

```text id="git403"
main

↓

Working

↓

You add new feature

↓

Application crashes
```

Now everyone is affected.

Instead,

keep `main`

stable

and develop new features on separate branches.

______________________________________________________________________

# View Current Branch

## Command

```bash id="git404"
git branch
```

Example Output

```text id="git405"
* main
```

The `*`

indicates

the current branch.

______________________________________________________________________

## When will you use this?

Whenever you want to know which branch you're currently working on.

______________________________________________________________________

# Create a Branch

## Command

```bash id="git406"
git branch jwt-auth
```

This creates

a new branch

called

```text id="git407"
jwt-auth
```

Notice

you're still on

```text id="git408"
main
```

Creating a branch

doesn't automatically switch to it.

______________________________________________________________________

## When will you use this?

Whenever you begin a new feature,

bug fix,

or experiment.

______________________________________________________________________

# Switch to a Branch

## Command

```bash id="git409"
git switch jwt-auth
```

Example Output

```text id="git410"
Switched to branch 'jwt-auth'
```

Now

every change

belongs to

```text id="git411"
jwt-auth
```

______________________________________________________________________

## Older Command

You'll also see

```bash id="git412"
git checkout jwt-auth
```

Older Git versions used `checkout`.

Modern Git recommends

```text id="git413"
git switch
```

for changing branches.

______________________________________________________________________

# Create and Switch Together

Instead of two commands,

use one.

```bash id="git414"
git switch -c jwt-auth
```

Equivalent to

```bash id="git415"
git branch jwt-auth

git switch jwt-auth
```

______________________________________________________________________

## When will you use this?

Almost every time you start a new feature.

Most developers use this shortcut.

______________________________________________________________________

# List All Branches

## Command

```bash id="git416"
git branch
```

Example

```text id="git417"
* jwt-auth

main

bug-fix
```

The current branch

has

```text id="git418"
*
```

beside it.

______________________________________________________________________

# Switching Back

Finished working?

Return to main.

```bash id="git419"
git switch main
```

Your project now shows

the state of

the `main` branch.

______________________________________________________________________

# Delete a Branch

Suppose

the feature

has been merged.

The branch

is no longer needed.

## Command

```bash id="git420"
git branch -d jwt-auth
```

Git removes

the local branch.

______________________________________________________________________

## When will you use this?

After a feature has been merged

and the branch is no longer required.

______________________________________________________________________

# Force Delete

Sometimes

Git refuses

to delete a branch

because it contains unmerged commits.

Force deletion

```bash id="git421"
git branch -D jwt-auth
```

Be careful.

This can permanently discard commits that exist only on that branch.

______________________________________________________________________

# Typical Development Workflow

```text id="git422"
main

↓

Create Branch

↓

Write Code

↓

Commit

↓

Merge

↓

Delete Branch
```

This is the workflow

used by most software teams.

______________________________________________________________________

# Branch Naming

Good examples

```text id="git423"
feature/login

feature/jwt-auth

bugfix/redis-timeout

hotfix/payment

refactor/database
```

Names should describe the purpose of the branch.

______________________________________________________________________

# Common Mistakes

### Working Directly on Main

Avoid adding new features directly to `main`.

Use feature branches.

______________________________________________________________________

### Forgetting Which Branch You're On

Always check

```bash id="git424"
git branch
```

before making changes.

______________________________________________________________________

### Deleting an Unmerged Branch

Don't use

```bash id="git425"
git branch -D
```

unless you're certain the work isn't needed.

______________________________________________________________________

### Using Random Branch Names

Avoid names like

```text id="git426"
test

new

abc

branch1
```

Use descriptive names instead.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| ---------------------- | -------------------- | ------------------------------- |
| `git branch` | List branches | Check current branch |
| `git branch <name>` | Create a branch | Start a new feature |
| `git switch <name>` | Switch branches | Move between branches |
| `git switch -c <name>` | Create and switch | Most common way to start work |
| `git branch -d <name>` | Delete merged branch | Cleanup after merge |
| `git branch -D <name>` | Force delete branch | Remove unwanted unmerged branch |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why do software teams use Git branches?

Git branches allow developers to work on features, bug fixes, and experiments independently without affecting the stable
code in the main branch. Multiple developers can work in parallel, and once their changes are reviewed and tested, the
branches can be merged back into the main branch.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What a Git branch is
- Why branches are important
- Creating branches
- Switching branches
- Listing branches
- Deleting branches
- Branch naming conventions
- Common branching mistakes

______________________________________________________________________

# What's Next

[Merging Branches](05-merging-branches.md)

# Git - Part 9

# Clone, Fetch, Pull & Push

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- How to clone an existing repository
- The difference between Fetch, Pull, and Push
- When to use each command
- How these commands fit into a real development workflow

______________________________________________________________________

# Why Do We Need These Commands?

Imagine your team has a project on GitHub.

```
GitHub

↓

Library API
```

You need a copy on your laptop.

Later,

your teammates make changes.

You need those changes.

Finally,

you complete your own feature.

The team needs your changes.

This is where:

- clone
- fetch
- pull
- push

come in.

______________________________________________________________________

# Clone

## What is it?

`git clone` downloads an entire Git repository from a remote server.

It includes:

- Source code
- Commit history
- Branches
- Remote configuration

______________________________________________________________________

## Command

```bash
git clone https://github.com/username/library-api.git
```

______________________________________________________________________

## Example

```
GitHub

↓

git clone

↓

Your Laptop
```

______________________________________________________________________

## When will you use this?

Whenever you're working on an existing project.

Examples:

- Joining a new company
- Contributing to open source
- Working on a friend's project

You usually clone **once**.

______________________________________________________________________

# Fetch

## What is it?

`git fetch` downloads the latest changes from the remote repository,

but **does not** modify your current branch.

Think of it as:

> "Show me what's new, but don't change my code."

______________________________________________________________________

## Command

```bash
git fetch
```

______________________________________________________________________

## Example

```
GitHub

↓

Download New Commits

↓

Local Repository

(No changes to working files)
```

______________________________________________________________________

## When will you use this?

Suppose another developer has pushed new commits.

You want to see what's changed before updating your branch.

Use:

```bash
git fetch
```

______________________________________________________________________

# Pull

## What is it?

`git pull` is a shortcut for:

```text
git fetch

+

git merge
```

It downloads new commits

and immediately merges them into your current branch.

______________________________________________________________________

## Command

```bash
git pull
```

______________________________________________________________________

## Example

```
GitHub

↓

Download Changes

↓

Merge Changes

↓

Your Branch
```

______________________________________________________________________

## When will you use this?

Almost every morning.

A common workflow is:

```
Start Work

↓

git pull

↓

Write Code
```

This ensures you're working with the latest version.

______________________________________________________________________

# Push

## What is it?

`git push` uploads your local commits to the remote repository.

______________________________________________________________________

## Command

```bash
git push
```

______________________________________________________________________

## Example

```
Laptop

↓

git push

↓

GitHub
```

Now everyone on your team can access your commits.

______________________________________________________________________

## When will you use this?

Whenever you've completed work and want to share it.

Typical workflow:

```
Write Code

↓

git add

↓

git commit

↓

git push
```

______________________________________________________________________

# First Push

The first time you push a new branch,

Git may ask you to set an upstream branch.

Example

```bash
git push -u origin jwt-auth
```

______________________________________________________________________

## What does `-u` mean?

It tells Git:

> "Remember that this local branch is connected to this remote branch."

After that,

you can simply run:

```bash
git push
```

______________________________________________________________________

# Complete Workflow

A normal workday looks like this.

```
Morning

↓

git pull

↓

Write Code

↓

git add

↓

git commit

↓

git push
```

Simple,

repeatable,

and used by almost every development team.

______________________________________________________________________

# Fetch vs Pull

Many beginners confuse these commands.

| Command | Downloads Changes | Updates Your Branch |
| ----------- | ----------------- | ------------------- |
| `git fetch` | ✅ Yes | ❌ No |
| `git pull` | ✅ Yes | ✅ Yes |

Remember:

- Fetch = Download only
- Pull = Download + Merge

______________________________________________________________________

# Clone vs Pull

Another common confusion.

| Command | When You'll Use It |
| ----------- | ----------------------------------- |
| `git clone` | First time downloading a repository |
| `git pull` | Updating an existing repository |

______________________________________________________________________

# Common Mistakes

### Using Clone Repeatedly

Don't clone the repository every day.

Clone once,

then use

```bash
git pull
```

______________________________________________________________________

### Forgetting to Pull

If you don't pull regularly,

you may encounter unnecessary merge conflicts.

______________________________________________________________________

### Pushing Without Committing

`git push` only uploads commits.

If you haven't committed,

nothing is pushed.

______________________________________________________________________

### Working Without Fetching or Pulling

Always update your branch before starting new work,

especially on team projects.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| ----------------------------- | -------------------------- | ------------------------------- |
| `git clone <url>` | Download a repository | First time working on a project |
| `git fetch` | Download remote changes | Review changes before merging |
| `git pull` | Download and merge changes | Start of the workday |
| `git push` | Upload commits | Share completed work |
| `git push -u origin <branch>` | First push of a new branch | New feature branch |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between `git fetch` and `git pull`?

`git fetch` downloads the latest changes from the remote repository without modifying the current branch. It updates the
local copy of the remote branches so you can review changes first. `git pull` performs a `git fetch` followed by a merge
(or rebase, depending on configuration), immediately updating the current branch with the downloaded changes.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Cloning repositories
- Fetching remote changes
- Pulling updates
- Pushing commits
- First-time push
- The difference between fetch and pull
- A typical daily Git workflow

______________________________________________________________________

# What's Next

[Tags & Releases](10-tags-and-releases.md)

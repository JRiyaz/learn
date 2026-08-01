# Git - Part 1

# Installing Git & Creating Your First Repository

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- How to install Git
- How to verify the installation
- How to configure Git
- How to create your first Git repository

______________________________________________________________________

# Why Do We Need Git?

Imagine you're building a FastAPI application.

Today you add a new feature.

Tomorrow you introduce a bug.

Next week you want yesterday's working code back.

Git keeps a history of your project so you can safely track and recover changes.

______________________________________________________________________

# Step 1: Install Git

Download Git from:

https://git-scm.com/

Install it using the default options for your operating system.

______________________________________________________________________

# Step 2: Verify Installation

## Command

```bash
git --version
```

## Example Output

```text
git version 2.51.0
```

______________________________________________________________________

## When will you use this?

Whenever you set up a new machine or want to verify that Git is installed correctly.

______________________________________________________________________

# Step 3: Configure Git

Git stores your name and email inside every commit.

## Set your username

```bash
git config --global user.name "Riyaz J"
```

## Set your email

```bash
git config --global user.email "your-email@example.com"
```

______________________________________________________________________

## When will you use this?

Only once for each computer.

After that, Git automatically uses these values whenever you create commits.

______________________________________________________________________

# Verify Configuration

## Command

```bash
git config --list
```

Example

```text
user.name=Riyaz J
user.email=your-email@example.com
```

______________________________________________________________________

## When will you use this?

When:

- Setting up a new laptop
- Troubleshooting Git configuration
- Checking which account Git is using

______________________________________________________________________

# Step 4: Create a Project

Example

```bash
mkdir library-api

cd library-api
```

______________________________________________________________________

# Step 5: Initialize Git

## Command

```bash
git init
```

Example Output

```text
Initialized empty Git repository
```

______________________________________________________________________

## What does this do?

It creates a hidden directory called

```text
.git
```

This directory stores the complete history of your project.

______________________________________________________________________

## When will you use this?

Whenever you start a brand-new project.

Examples:

- FastAPI project
- AI project
- Personal project
- Practice project

If you clone an existing repository, you **do not** run `git init` because the repository is already initialized.

______________________________________________________________________

# Verify the Repository

## Command

```bash
ls -la
```

You'll see

```text
.git
```

This confirms the directory is now a Git repository.

> On Windows Command Prompt, use:
>
> ```cmd
> dir /a
> ```

______________________________________________________________________

# Check Repository Status

## Command

```bash
git status
```

Example Output

```text
On branch main

No commits yet

nothing to commit
```

______________________________________________________________________

## What does this command do?

It tells you:

- Which branch you're on
- Which files changed
- Which files are staged
- Which files are untracked
- Whether your working tree is clean

______________________________________________________________________

## When will you use this?

**All the time.**

It is one of the most frequently used Git commands.

A good habit is:

```text
Write Code

↓

git status

↓

Commit

↓

git status
```

______________________________________________________________________

# Common Beginner Mistakes

### Running `git init` inside another Git repository

Avoid creating nested repositories unless you intentionally want a Git submodule.

______________________________________________________________________

### Forgetting to configure your name and email

Your commits may use incorrect or missing author information.

______________________________________________________________________

### Editing files without checking `git status`

Always know the current state of your repository before committing.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| -------------------------------- | --------------------------- | ------------------ |
| `git --version` | Verify Git installation | New machine |
| `git config --global user.name` | Configure username | One-time setup |
| `git config --global user.email` | Configure email | One-time setup |
| `git config --list` | View configuration | Verify settings |
| `git init` | Create a new Git repository | New project |
| `git status` | Check repository status | Constantly |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What does `git init` do?

`git init` initializes a new Git repository by creating a hidden `.git` directory. This directory stores Git's metadata,
commit history, branches, and configuration for the project. After running `git init`, the directory becomes a Git
repository, and Git can start tracking changes.

______________________________________________________________________

# Summary

In this lesson, you learned:

- How to install Git
- How to configure Git
- How to initialize a repository
- How to verify Git status
- The first commands you'll use in almost every project

______________________________________________________________________

# What's Next

[Git Workflow (Working Directory, Staging Area & Repository)](02-git-workflow-working-directory-staging-repository.md)

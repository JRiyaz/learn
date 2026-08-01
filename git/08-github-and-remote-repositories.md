# Git - Part 8

# GitHub & Remote Repositories

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What a Remote Repository is
- What GitHub is
- Why remote repositories are needed
- How to connect a local repository to GitHub
- How to view configured remotes
- How to remove or change a remote

______________________________________________________________________

# Local Repository vs Remote Repository

So far,

everything we've done has been on our computer.

```
Laptop

↓

Git Repository
```

That's called a **Local Repository**.

But what happens if:

- Your laptop crashes?
- You buy a new computer?
- Another developer needs your code?

You need a **Remote Repository**.

______________________________________________________________________

# What is a Remote Repository?

A Remote Repository is a Git repository hosted on another machine.

Usually,

it's stored on platforms like:

- GitHub
- GitLab
- Bitbucket

Think of it as a central place where your team shares code.

______________________________________________________________________

# What is GitHub?

GitHub is a cloud platform that hosts Git repositories.

Git provides version control.

GitHub provides:

- Repository hosting
- Collaboration
- Pull Requests
- Code Reviews
- Issues
- Actions (CI/CD)

Git works without GitHub,

but GitHub makes collaboration much easier.

______________________________________________________________________

# Typical Workflow

```text id="git801"
Your Laptop

↓

Git

↓

GitHub

↓

Other Developers
```

Everyone works locally,

then shares changes through GitHub.

______________________________________________________________________

# Create a GitHub Repository

On GitHub,

click

```text id="git802"
New Repository
```

Give it a name.

Example

```text id="git803"
library-api
```

GitHub will create an empty remote repository.

______________________________________________________________________

# Connect Local Repository to GitHub

## Command

```bash id="git804"
git remote add origin https://github.com/username/library-api.git
```

Replace

```text id="git805"
username
```

with your GitHub username.

______________________________________________________________________

## What does this command do?

It tells Git:

> "This GitHub repository is my remote repository."

The name

```text id="git806"
origin
```

is simply a nickname.

By convention,

almost every project uses

```text id="git807"
origin
```

for the primary remote.

______________________________________________________________________

## When will you use this?

Once,

when connecting a new local project to GitHub.

______________________________________________________________________

# View Configured Remotes

## Command

```bash id="git808"
git remote -v
```

Example

```text id="git809"
origin

https://github.com/username/library-api.git

(fetch)

origin

https://github.com/username/library-api.git

(push)
```

______________________________________________________________________

## When will you use this?

Whenever you want to verify:

- Which GitHub repository you're connected to
- Whether the remote URL is correct

______________________________________________________________________

# Remove a Remote

Suppose

you connected

to the wrong repository.

Remove it.

## Command

```bash id="git810"
git remote remove origin
```

______________________________________________________________________

## When will you use this?

Rarely.

Usually when:

- You accidentally connected to the wrong repository
- You're moving the project to another GitHub account

______________________________________________________________________

# Add the Correct Remote Again

```bash id="git811"
git remote add origin https://github.com/username/new-library-api.git
```

Now

your project points

to the new repository.

______________________________________________________________________

# Rename a Remote

Sometimes

you want to rename

a remote.

## Command

```bash id="git812"
git remote rename origin github
```

Now

the remote is called

```text id="git813"
github
```

instead of

```text id="git814"
origin
```

______________________________________________________________________

## Will you use this often?

Not really.

Most teams simply keep the name

```text id="git815"
origin
```

for consistency.

______________________________________________________________________

# Multiple Remotes

A repository can have multiple remotes.

Example

```text id="git816"
origin

↓

Personal GitHub

upstream

↓

Company Repository
```

This is common when contributing

to open-source projects.

We'll revisit this later.

______________________________________________________________________

# Real-World Example

Suppose you create

a FastAPI project.

```
FastAPI

↓

Local Git Repository

↓

GitHub Repository

↓

Team Members Clone It
```

Everyone now works

from the same shared repository.

______________________________________________________________________

# Common Mistakes

### Confusing Git with GitHub

Git

is the version control system.

GitHub

is a hosting platform.

______________________________________________________________________

### Forgetting to Verify the Remote

Always check

```bash id="git817"
git remote -v
```

before pushing code.

______________________________________________________________________

### Using the Wrong Repository URL

If you push to the wrong repository,

your code ends up in the wrong place.

Always double-check the URL.

______________________________________________________________________

### Renaming `origin` Unnecessarily

Most teams keep

```text id="git818"
origin
```

as the primary remote.

Changing it usually adds confusion.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| --------------------------------- | ---------------------------- | -------------------- |
| `git remote add origin <url>` | Connect local repo to GitHub | New project |
| `git remote -v` | View configured remotes | Verify configuration |
| `git remote remove origin` | Remove a remote | Wrong repository |
| `git remote rename origin github` | Rename a remote | Rarely used |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between Git and GitHub?

Git is a distributed version control system used to track changes in a project. GitHub is a cloud-based platform that
hosts Git repositories and provides collaboration features such as pull requests, code reviews, issue tracking, and
CI/CD integrations. Git can be used without GitHub, but GitHub relies on Git.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Local vs Remote repositories
- What GitHub is
- Connecting a repository to GitHub
- Viewing remotes
- Removing remotes
- Renaming remotes
- Multiple remotes
- Common mistakes

______________________________________________________________________

# What's Next

[Clone, Fetch, Pull & Push](09-clone-fetch-pull-push.md)

# Git - Part 25

# Git Cheat Sheet & Interview Revision

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll have:

- A quick Git command reference
- A complete Git workflow
- Common interview questions
- Best practices
- Common mistakes
- A roadmap for continued learning

______________________________________________________________________

# The Complete Git Workflow

This is the workflow you'll use most often.

```text id="git2501"
Clone Repository

↓

Create Feature Branch

↓

Write Code

↓

git add

↓

git commit

↓

git push

↓

Pull Request

↓

Code Review

↓

Merge

↓

Delete Branch
```

If you remember only one workflow,

remember this one.

______________________________________________________________________

# Repository Commands

| Command | Purpose |
| ----------------- | ------------------------------- |
| `git init` | Create a new Git repository |
| `git clone <url>` | Download an existing repository |
| `git status` | Show repository status |
| `git remote -v` | View configured remotes |

______________________________________________________________________

# Staging Commands

| Command | Purpose |
| ------------------------------ | ----------------- |
| `git add file.py` | Stage one file |
| `git add .` | Stage all changes |
| `git restore --staged file.py` | Unstage a file |

______________________________________________________________________

# Commit Commands

| Command | Purpose |
| ------------------------- | ---------------------- |
| `git commit -m "message"` | Create a commit |
| `git commit --amend` | Modify the last commit |

______________________________________________________________________

# Branch Commands

| Command | Purpose |
| ----------------------------- | ---------------------- |
| `git branch` | List branches |
| `git branch feature/login` | Create a branch |
| `git switch feature/login` | Switch branches |
| `git switch -c feature/login` | Create and switch |
| `git branch -d feature/login` | Delete a merged branch |

______________________________________________________________________

# Merge Commands

| Command | Purpose |
| ------------------------- | -------------- |
| `git merge feature/login` | Merge a branch |
| `git merge --abort` | Cancel a merge |

______________________________________________________________________

# Remote Commands

| Command | Purpose |
| ---------------------------------- | -------------------------- |
| `git fetch` | Download remote changes |
| `git pull` | Download and merge changes |
| `git push` | Upload commits |
| `git push -u origin feature/login` | First push of a branch |

______________________________________________________________________

# Undo Commands

| Situation | Command |
| -------------------- | ------------------------------ |
| Discard file changes | `git restore file.py` |
| Unstage file | `git restore --staged file.py` |
| Undo local commit | `git reset` |
| Undo pushed commit | `git revert` |

______________________________________________________________________

# Stash Commands

| Command | Purpose |
| ----------------- | --------------------------------- |
| `git stash` | Save unfinished work |
| `git stash list` | View stashes |
| `git stash pop` | Restore and remove stash |
| `git stash apply` | Restore stash without removing it |

______________________________________________________________________

# Rebase Commands

| Command | Purpose |
| ----------------------- | ------------------------ |
| `git rebase main` | Replay commits |
| `git rebase -i HEAD~5` | Interactive Rebase |
| `git rebase --continue` | Continue after conflicts |
| `git rebase --abort` | Cancel a rebase |

______________________________________________________________________

# Cherry Pick Commands

| Command | Purpose |
| ---------------------------- | ------------------------ |
| `git cherry-pick <commit>` | Copy one commit |
| `git cherry-pick --continue` | Continue after conflicts |
| `git cherry-pick --abort` | Cancel cherry-pick |

______________________________________________________________________

# Tag Commands

| Command | Purpose |
| -------------------------------- | -------------------- |
| `git tag` | List tags |
| `git tag -a v1.0.0 -m "Release"` | Create annotated tag |
| `git push origin --tags` | Push all tags |

______________________________________________________________________

# Worktree Commands

| Command | Purpose |
| ---------------------------------- | --------------- |
| `git worktree add <path> <branch>` | Create worktree |
| `git worktree list` | List worktrees |
| `git worktree remove <path>` | Remove worktree |

______________________________________________________________________

# Bisect Commands

| Command | Purpose |
| ------------------ | ------------------- |
| `git bisect start` | Start bisect |
| `git bisect good` | Mark commit as good |
| `git bisect bad` | Mark commit as bad |
| `git bisect reset` | End bisect |

______________________________________________________________________

# Daily Commands You'll Use Most

As a backend developer,

these are the commands you'll use almost every day.

```bash id="git2502"
git status

git pull

git switch -c feature/new-feature

git add .

git commit -m "Implement feature"

git push

git log --oneline
```

You don't need to memorize every Git command.

Master these first.

______________________________________________________________________

# Commands You'll Use Occasionally

```bash id="git2503"
git stash

git cherry-pick

git rebase

git tag

git revert

git restore

git worktree
```

These become useful as your projects grow.

______________________________________________________________________

# Rarely Used Commands

```bash id="git2504"
git bisect

git gc

git fsck

git prune

git submodule
```

Know what they do,

but don't worry if you don't use them often.

______________________________________________________________________

# Common Interview Questions

### What is Git?

A distributed version control system that tracks changes in source code and enables collaboration.

______________________________________________________________________

### What is the difference between Git and GitHub?

Git is the version control system.

GitHub is a cloud platform that hosts Git repositories and provides collaboration features.

______________________________________________________________________

### Merge vs Rebase?

Merge preserves branch history by creating a merge commit.

Rebase rewrites commit history to create a linear history.

______________________________________________________________________

### Reset vs Revert?

Reset rewrites local history.

Revert creates a new commit that reverses previous changes and is safe for shared branches.

______________________________________________________________________

### Fetch vs Pull?

Fetch downloads changes.

Pull downloads and merges them into the current branch.

______________________________________________________________________

### Branch vs Tag?

Branches move as new commits are added.

Tags point to a fixed commit, usually representing a release.

______________________________________________________________________

### What is Git Stash?

A temporary storage area for uncommitted work, allowing you to switch tasks without creating a commit.

______________________________________________________________________

### What is Cherry Pick?

Copies selected commits from one branch to another.

______________________________________________________________________

### What is a Pull Request?

A request to merge code into another branch after review.

______________________________________________________________________

# Best Practices

- Commit small, logical changes.
- Write meaningful commit messages.
- Pull before starting work.
- Use feature branches.
- Keep Pull Requests small.
- Review code carefully.
- Delete merged branches.
- Never commit secrets or `.env` files.
- Use `.gitignore` correctly.

______________________________________________________________________

# Common Beginner Mistakes

- Working directly on `main`
- Committing unrelated changes together
- Using `git reset --hard` without understanding it
- Forgetting to pull before starting work
- Ignoring merge conflicts
- Pushing without reviewing changes
- Committing secrets
- Creating huge Pull Requests

______________________________________________________________________

# Git Learning Complete

You now understand:

- Repository basics
- Commits
- Branching
- Merging
- Merge conflicts
- GitHub
- Pull Requests
- Rebasing
- Stashing
- Cherry Picking
- Tags
- Worktrees
- Git Internals
- Git Workflows
- Code Reviews

This is enough Git knowledge for the vast majority of backend engineering roles.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What Git topics should an experienced backend engineer be comfortable with?

An experienced backend engineer should understand repositories, commits, branching, merging, merge conflicts, remote
repositories, Pull Requests, rebasing, stashing, cherry-picking, tags, Git workflows, code reviews, and the differences
between commonly confused commands such as `fetch` vs `pull`, `merge` vs `rebase`, and `reset` vs `revert`. They should
also know when to use each command in real-world development.

______________________________________________________________________

# Summary

Congratulations! 🎉

You have completed the Git module.

You now have the knowledge needed to:

- Work effectively in a professional Git-based workflow
- Collaborate with software teams
- Handle most day-to-day Git tasks confidently
- Answer common Git interview questions

______________________________________________________________________

# What's Next

[OWASP Top 10 & Backend Security](../security/01-introduction-to-web-security.md)

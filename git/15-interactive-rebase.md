# Git - Part 15

# Interactive Rebase

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Interactive Rebase is
- Why developers use it
- How to start an Interactive Rebase
- Reordering commits
- Squashing commits
- Editing commit messages
- Dropping commits
- Best practices

______________________________________________________________________

# Why Do We Need Interactive Rebase?

Suppose you've been working on a feature.

Your commit history looks like this.

```text
Add login API

↓

Fix typo

↓

Forgot import

↓

Debug

↓

Remove debug

↓

Final fix
```

Technically,

everything works.

But the commit history is messy.

Wouldn't it be better if it looked like this?

```text
Implement Login API
```

That's exactly what Interactive Rebase helps you do.

______________________________________________________________________

# What is Interactive Rebase?

Interactive Rebase allows you to **rewrite your local commit history** before sharing it with others.

You can:

- Reorder commits
- Rename commit messages
- Combine commits
- Delete unwanted commits

Think of it as editing the draft of your Git history before publishing it.

______________________________________________________________________

# When Will You Use It?

Usually,

right before creating a Pull Request.

Instead of sharing

15 small commits,

you clean them into

3–5 meaningful commits.

This makes code reviews much easier.

______________________________________________________________________

# Start Interactive Rebase

Suppose you want to edit

the last five commits.

## Command

```bash
git rebase -i HEAD~5
```

Meaning:

```text
Edit

↓

Last 5 Commits
```

______________________________________________________________________

# What Opens?

Git opens your default editor.

You'll see something like this.

```text
pick a1b2c3 Add login

pick d4e5f6 Fix typo

pick g7h8i9 Remove debug

pick j1k2l3 Add tests

pick m4n5o6 Update README
```

Each line represents one commit.

______________________________________________________________________

# Reorder Commits

Simply move the lines.

Example

Before

```text
Add Tests

↓

Add Login
```

After

```text
Add Login

↓

Add Tests
```

Git replays them

in the new order.

______________________________________________________________________

# Edit a Commit Message

Change

```text
pick
```

to

```text
reword
```

Example

```text
reword a1b2c3 Add login
```

Git pauses

and lets you enter

a better commit message.

______________________________________________________________________

# Squash Commits

Suppose your history is

```text
Add Login

↓

Fix Typo

↓

Forgot Import
```

These belong together.

Change

```text
pick
```

to

```text
squash
```

Example

```text
pick a1b2c3 Add login

squash d4e5f6 Fix typo

squash g7h8i9 Forgot import
```

Git combines them into

one commit.

______________________________________________________________________

# Drop a Commit

Suppose you accidentally committed

debugging code.

You don't want it anymore.

Replace

```text
pick
```

with

```text
drop
```

Example

```text
drop a1b2c3 Debug prints
```

Git removes that commit

from your local history.

______________________________________________________________________

# Common Interactive Rebase Actions

| Action | Purpose |
| -------- | ------------------------------------------ |
| `pick` | Keep the commit |
| `reword` | Change the commit message |
| `edit` | Pause to modify the commit |
| `squash` | Combine with previous commit |
| `fixup` | Combine without keeping the commit message |
| `drop` | Remove the commit |

You don't need to memorize all of them today.

The most commonly used are:

- pick
- reword
- squash
- drop

______________________________________________________________________

# Real-World Example

Suppose you've worked all day.

Your history is

```text
Fix typo

↓

Fix typo again

↓

Forgot import

↓

Remove print

↓

Final implementation
```

Before opening a Pull Request,

run

```bash
git rebase -i HEAD~5
```

Clean it into

```text
Implement Authentication
```

Now your teammates review

one clean commit

instead of five noisy ones.

______________________________________________________________________

# Interactive Rebase vs Normal Rebase

| Normal Rebase | Interactive Rebase |
| ---------------- | ----------------------------- |
| Replays commits | Replays **and edits** commits |
| Updates branch | Cleans history |
| Mostly automatic | User controls each commit |

______________________________________________________________________

# Important Rule

Interactive Rebase **rewrites history**.

That means:

✅ Safe

- Before pushing
- On your own feature branch

❌ Avoid

- Shared branches
- Public history
- Branches other developers are using

______________________________________________________________________

# Common Mistakes

### Rebasing Shared Branches

Don't rewrite history

that teammates already depend on.

______________________________________________________________________

### Squashing Unrelated Commits

Only combine commits

that belong to the same logical change.

______________________________________________________________________

### Dropping Important Commits

Review carefully

before using

```text
drop
```

______________________________________________________________________

### Using Interactive Rebase Too Late

It's best done

before opening a Pull Request,

not after the branch has been widely shared.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| ---------------------- | --------------------- | ----------------------- |
| `git rebase -i HEAD~5` | Edit last 5 commits | Clean history before PR |
| `pick` | Keep commit | Default action |
| `reword` | Rename commit message | Improve commit history |
| `squash` | Combine commits | Clean noisy history |
| `drop` | Remove commit | Delete unwanted commits |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why would you use Interactive Rebase?

Interactive Rebase is used to clean up local commit history before sharing code. It allows developers to reorder
commits, edit commit messages, combine related commits, and remove unnecessary commits. This results in a cleaner, more
readable history that simplifies code reviews. Because it rewrites history, it should only be used on local or unshared
branches.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Interactive Rebase is
- When to use it
- Starting an Interactive Rebase
- Reordering commits
- Editing commit messages
- Squashing commits
- Dropping commits
- Best practices for rewriting history

______________________________________________________________________

# What's Next

[Squashing Commits](16-squashing-commits.md)

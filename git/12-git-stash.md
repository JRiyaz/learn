# Git - Part 12

# Git Stash - Saving Work Without Committing

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Git Stash is
- When to use Git Stash
- How to create a stash
- How to view stashes
- How to restore a stash
- How to delete stashes
- Common mistakes

______________________________________________________________________

# Why Do We Need Git Stash?

Imagine this situation.

You're halfway through implementing JWT Authentication.

```
auth.py

↓

50% Complete
```

Suddenly,

your manager says:

> Production is down. Fix it immediately.

You cannot commit your unfinished work.

You also don't want to lose it.

This is exactly why Git Stash exists.

______________________________________________________________________

# What is Git Stash?

Git Stash temporarily saves your uncommitted changes and restores your working directory to a clean state.

Think of it as:

```
Current Work

↓

Temporary Shelf

↓

Clean Working Directory
```

Later,

you can restore your work from the shelf.

______________________________________________________________________

# When Will You Use It?

Common situations:

- Production bug appears
- Need to switch branches
- Need to pull the latest changes
- Need to review someone else's code
- Need to test something quickly

Instead of making a "Work in Progress" commit,

stash your changes.

______________________________________________________________________

# Save Your Work

## Command

```bash id="git1201"
git stash
```

______________________________________________________________________

## What does it do?

It saves:

- Modified tracked files
- Staged changes

Then it restores your working directory to the last commit.

______________________________________________________________________

## Example

Before

```
Working Directory

↓

Modified Files
```

Run

```bash id="git1202"
git stash
```

After

```
Working Directory

↓

Clean
```

Your work isn't lost.

It's stored in Git's stash.

______________________________________________________________________

# Verify the Working Directory

## Command

```bash id="git1203"
git status
```

Expected

```text id="git1204"
nothing to commit,
working tree clean
```

______________________________________________________________________

# View Saved Stashes

## Command

```bash id="git1205"
git stash list
```

Example

```text id="git1206"
stash@{0}

stash@{1}
```

Every stash gets an index.

Newest stash

↓

```text id="git1207"
stash@{0}
```

______________________________________________________________________

## When will you use this?

Whenever you've saved multiple stashes and want to see what's available.

______________________________________________________________________

# Restore the Latest Stash

## Command

```bash id="git1208"
git stash apply
```

______________________________________________________________________

## What does it do?

It restores your latest stash.

The stash **remains** in the stash list.

______________________________________________________________________

## When will you use this?

When you're unsure whether you'll need the stash again.

______________________________________________________________________

# Restore and Remove

Usually,

this is the command you'll use.

```bash id="git1209"
git stash pop
```

______________________________________________________________________

## What does it do?

It restores your latest stash

and removes it from the stash list.

Think of it as

```
Take From Shelf

↓

Continue Working
```

______________________________________________________________________

## When will you use this?

Most of the time.

Once you've resumed work,

you usually don't need the stash anymore.

______________________________________________________________________

# Restore a Specific Stash

Suppose

you have multiple stashes.

Restore one.

```bash id="git1210"
git stash apply stash@{1}
```

______________________________________________________________________

## When will you use this?

Rarely,

but useful if you've saved several pieces of work.

______________________________________________________________________

# Delete a Stash

Remove one stash.

```bash id="git1211"
git stash drop stash@{0}
```

______________________________________________________________________

## When will you use this?

When you no longer need a particular stash.

______________________________________________________________________

# Delete All Stashes

## Command

```bash id="git1212"
git stash clear
```

______________________________________________________________________

## Warning

This removes **every stash**.

There is no easy way to recover them afterward.

Use it carefully.

______________________________________________________________________

# Stashing Untracked Files

By default,

Git Stash ignores untracked files.

Example

```
new_file.py
```

To include them,

use

```bash id="git1213"
git stash -u
```

or

```bash id="git1214"
git stash --include-untracked
```

______________________________________________________________________

## When will you use this?

When you've created new files

that aren't tracked by Git yet.

______________________________________________________________________

# Add a Description

Instead of anonymous stashes,

give them names.

```bash id="git1215"
git stash push -m "Half completed JWT authentication"
```

View them.

```bash id="git1216"
git stash list
```

Example

```text id="git1217"
stash@{0}

On main:

Half completed JWT authentication
```

This makes it much easier to remember why you created the stash.

______________________________________________________________________

# Real-World Workflow

```
Working on Feature

↓

Production Bug Reported

↓

git stash

↓

Switch Branch

↓

Fix Bug

↓

Commit

↓

Switch Back

↓

git stash pop

↓

Continue Feature
```

This is one of the most common uses of Git Stash.

______________________________________________________________________

# Stash vs Commit

Many beginners ask:

> Should I stash or commit?

| Git Stash | Commit |
| ----------------------- | ---------------------- |
| Temporary | Permanent |
| Local only | Part of history |
| Usually unfinished work | Completed logical work |
| Not shared | Can be shared |

Rule of thumb:

- Finished work → Commit
- Temporary interruption → Stash

______________________________________________________________________

# Common Mistakes

### Using Stash Instead of Commits

Don't use stash as long-term storage.

It's meant to be temporary.

______________________________________________________________________

### Forgetting About Old Stashes

Run

```bash id="git1218"
git stash list
```

occasionally

and clean up old stashes.

______________________________________________________________________

### Forgetting Untracked Files

Remember,

plain

```bash id="git1219"
git stash
```

doesn't save new untracked files.

Use

```bash id="git1220"
git stash -u
```

if needed.

______________________________________________________________________

### Using Apply Instead of Pop

If you don't need the stash anymore,

prefer

```bash id="git1221"
git stash pop
```

Otherwise,

your stash list keeps growing.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| --------------------------- | ------------------------ | --------------------------- |
| `git stash` | Save current work | Interrupted by another task |
| `git stash list` | View stashes | Check saved work |
| `git stash apply` | Restore stash | Keep stash for later |
| `git stash pop` | Restore and remove stash | Continue working |
| `git stash apply stash@{n}` | Restore a specific stash | Multiple stashes |
| `git stash drop stash@{n}` | Delete one stash | Cleanup |
| `git stash clear` | Delete all stashes | Remove everything |
| `git stash -u` | Include untracked files | Save new files |
| `git stash push -m "..."` | Create a named stash | Easier identification |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** When would you use Git Stash instead of creating a commit?

Git Stash is useful when you have unfinished work that you don't want to commit yet, but you need a clean working
directory to switch branches, fix an urgent bug, or pull the latest changes. Unlike a commit, a stash is temporary,
local to your machine, and not intended to become part of the project's history.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Git Stash is
- When to use it
- Creating stashes
- Viewing stashes
- Restoring stashes
- Removing stashes
- Named stashes
- Stashing untracked files
- Stash vs Commit

______________________________________________________________________

# What's Next

[Cherry Pick - Applying Specific Commits](13-cherry-pick.md)

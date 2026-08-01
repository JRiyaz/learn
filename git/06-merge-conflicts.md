# Git - Part 6

# Merge Conflicts

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What a merge conflict is
- Why merge conflicts happen
- How to identify them
- How to resolve them
- The Git commands involved
- Best practices to minimize conflicts

______________________________________________________________________

# What is a Merge Conflict?

A merge conflict happens when Git cannot automatically combine changes from two branches.

Git doesn't know

which version

is correct,

so it asks **you** to decide.

______________________________________________________________________

# Real-World Example

Suppose

your `main` branch contains

```python id="git601"
DATABASE_URL = "localhost"
```

Meanwhile,

on your feature branch,

you changed it to

```python id="git602"
DATABASE_URL = "postgres"
```

At the same time,

another developer changed it to

```python id="git603"
DATABASE_URL = "db.internal"
```

Now Git has two different values for the same line.

Which one should it keep?

It can't decide automatically.

This creates a merge conflict.

______________________________________________________________________

# Typical Scenario

```text id="git604"
main

↓

Change app.py

│

├──────────────┐

│              │

▼              ▼

Feature A    Feature B

│              │

Modify Same Line

│              │

└──────Merge──────┘

↓

Conflict
```

______________________________________________________________________

# Attempting a Merge

Suppose you're on

```text id="git605"
main
```

Run

```bash id="git606"
git merge jwt-auth
```

Git may respond with

```text id="git607"
CONFLICT (content):

Merge conflict in app.py

Automatic merge failed.
```

The merge pauses

until you resolve the conflict.

______________________________________________________________________

# Check Repository Status

## Command

```bash id="git608"
git status
```

Example

```text id="git609"
You have unmerged paths.

Fix conflicts and run

git commit
```

This tells you

which files need attention.

______________________________________________________________________

# Open the File

Git marks conflicts like this.

```text id="git610"
<<<<<<< HEAD

DATABASE_URL = "db.internal"

=======

DATABASE_URL = "postgres"

>>>>>>> jwt-auth
```

______________________________________________________________________

# What Do These Symbols Mean?

```text id="git611"
<<<<<<< HEAD
```

Current branch.

______________________________________________________________________

```text id="git612"
=======
```

Separator.

______________________________________________________________________

```text id="git613"
>>>>>>> jwt-auth
```

Incoming branch.

______________________________________________________________________

# Resolve the Conflict

Choose the correct version.

Example

```python id="git614"
DATABASE_URL = "postgres"
```

Or combine both changes,

if appropriate.

Then remove

all conflict markers.

______________________________________________________________________

# Stage the Resolved File

After editing,

tell Git

the conflict has been resolved.

## Command

```bash id="git615"
git add app.py
```

______________________________________________________________________

# Complete the Merge

Now finish it.

## Command

```bash id="git616"
git commit
```

Git opens the default editor

with a merge commit message.

Save

and close.

The merge is complete.

______________________________________________________________________

# Abort the Merge

Suppose

you don't want to continue.

Cancel the merge.

## Command

```bash id="git617"
git merge --abort
```

______________________________________________________________________

## When will you use this?

If:

- You merged the wrong branch.
- The conflicts are too complicated.
- You want to start over.

Git restores the repository

to its state before the merge.

______________________________________________________________________

# Verify the Merge

## Command

```bash id="git618"
git log --oneline --graph
```

Confirm

the merge completed successfully.

______________________________________________________________________

# How to Reduce Merge Conflicts

### Commit Frequently

Small commits

are easier to merge.

______________________________________________________________________

### Pull Changes Often

Don't let your branch become weeks behind.

Regularly update your branch with the latest changes.

We'll learn `git pull` later.

______________________________________________________________________

### Keep Branches Short-Lived

A feature branch should ideally exist for:

- a few hours
- a few days

not several months.

______________________________________________________________________

### Avoid Editing the Same Files

Large teams often divide work

to minimize overlap.

______________________________________________________________________

# Common Mistakes

### Deleting Conflict Markers Incorrectly

Remove

```text id="git619"
<<<<<<<

=======

>>>>>>>
```

but keep the correct code.

______________________________________________________________________

### Forgetting `git add`

Resolving the file isn't enough.

Git won't know it's resolved until you stage it.

______________________________________________________________________

### Creating New Commits Before Resolving

Always resolve

the merge first.

______________________________________________________________________

### Panic

Merge conflicts

look scary

the first few times.

They're completely normal

and every developer encounters them.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| -------------------- | ------------------------- | ---------------------- |
| `git merge <branch>` | Merge branches | Finish a feature |
| `git status` | View conflicted files | During conflicts |
| `git add <file>` | Mark conflict as resolved | After editing |
| `git commit` | Finish merge | After resolving |
| `git merge --abort` | Cancel merge | Wrong merge or restart |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is a Git merge conflict, and how do you resolve it?

A merge conflict occurs when Git cannot automatically combine changes from two branches, usually because the same part
of a file was modified differently. To resolve it, identify the conflicted files using `git status`, edit the files to
keep the correct changes, remove the conflict markers, stage the resolved files using `git add`, and complete the merge
with `git commit`. If necessary, the merge can be canceled using `git merge --abort`.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What merge conflicts are
- Why they happen
- How Git marks conflicts
- How to resolve them
- How to abort a merge
- Best practices to reduce conflicts
- Common mistakes during conflict resolution

______________________________________________________________________

# What's Next

[.gitignore - Ignoring Files and Folders](07-gitignore.md)

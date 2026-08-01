# Git - Part 11

# Undoing Changes - restore, reset & revert

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- When to use `git restore`
- When to use `git reset`
- When to use `git revert`
- The differences between them
- Which command is safe on shared branches
- Common mistakes

______________________________________________________________________

# Why Do We Need Undo Commands?

Everyone makes mistakes.

Examples:

- You accidentally modified a file.
- You staged the wrong file.
- You created the wrong commit.
- You pushed a buggy commit.

Git provides different commands for different situations.

The biggest mistake beginners make is trying to use **one command for everything**.

Instead, choose the right tool for the job.

______________________________________________________________________

# Think Before Choosing

Ask yourself:

```text id="git1101"
Did I...

↓

Modify a file?

↓

Stage the wrong file?

↓

Create a bad commit?

↓

Push a bad commit?
```

Each situation has a different solution.

______________________________________________________________________

# Scenario 1

## "I modified a file but don't want the changes."

Example

```python id="git1102"
print("Hello")

↓

print("Bug")
```

You haven't staged it.

You simply want to discard the changes.

Use

```bash id="git1103"
git restore app.py
```

______________________________________________________________________

## What does it do?

It restores the file to the last committed version.

Your uncommitted changes are lost.

______________________________________________________________________

## When will you use this?

Very often.

Example:

You experimented with some code,

it didn't work,

and you want to return to the previous version.

______________________________________________________________________

# Scenario 2

## "I staged the wrong file."

Example

```bash id="git1104"
git add app.py
```

Oops.

You didn't want to stage it.

Use

```bash id="git1105"
git restore --staged app.py
```

______________________________________________________________________

## What does it do?

It removes the file from the Staging Area.

Your code changes remain.

Only the staging is undone.

______________________________________________________________________

## When will you use this?

Whenever you accidentally use

```bash id="git1106"
git add .
```

and stage more files than intended.

______________________________________________________________________

# Scenario 3

## "My last commit message is wrong."

Suppose

you committed

```text id="git1107"
Fix Bug
```

You wanted

```text id="git1108"
Fix Redis connection timeout
```

Use

```bash id="git1109"
git commit --amend
```

Git opens your editor,

allowing you to update the commit message.

______________________________________________________________________

## When will you use this?

When the last commit:

- has a typo
- needs a better description
- is missing a small file (before pushing)

______________________________________________________________________

# Scenario 4

## "I want to move HEAD backward."

This is where

```text id="git1110"
git reset
```

comes in.

There are three commonly used modes.

______________________________________________________________________

# Soft Reset

## Command

```bash id="git1111"
git reset --soft HEAD~1
```

______________________________________________________________________

## What does it do?

Removes the last commit,

but keeps all changes staged.

______________________________________________________________________

## When will you use this?

Suppose you made two commits,

but want to combine them into one.

A soft reset is useful before recommitting.

______________________________________________________________________

# Mixed Reset

## Command

```bash id="git1112"
git reset HEAD~1
```

or

```bash id="git1113"
git reset --mixed HEAD~1
```

______________________________________________________________________

## What does it do?

Removes the last commit

and unstages the files.

Your code remains unchanged.

______________________________________________________________________

## When will you use this?

When you want to reorganize your commits.

______________________________________________________________________

# Hard Reset

## Command

```bash id="git1114"
git reset --hard HEAD~1
```

______________________________________________________________________

## What does it do?

Removes:

- the commit
- the staged changes
- the working directory changes

Everything after that commit is discarded.

______________________________________________________________________

## When will you use this?

Rarely.

Usually only when you're absolutely sure you don't need the changes.

______________________________________________________________________

# Warning

```text id="git1115"
git reset --hard
```

can permanently remove uncommitted work.

Always double-check before running it.

______________________________________________________________________

# Scenario 5

## "I already pushed a bad commit."

Imagine this workflow.

```text id="git1116"
Commit

↓

Push

↓

Oops!
```

Should you use

```text id="git1117"
git reset
```

No.

Other developers may already have pulled the commit.

Instead,

use

```text id="git1118"
git revert
```

______________________________________________________________________

# Revert

## Command

```bash id="git1119"
git revert HEAD
```

______________________________________________________________________

## What does it do?

Instead of deleting the commit,

Git creates a **new commit**

that reverses the changes.

Example

```text id="git1120"
Commit A

↓

Commit B

↓

Revert Commit
```

History remains intact.

______________________________________________________________________

## When will you use this?

Whenever the commit has already been pushed

or shared with other developers.

This is the safest option for team projects.

______________________________________________________________________

# Which Command Should I Use?

| Situation | Command |
| ----------------------- | ---------------------- |
| Discard file changes | `git restore` |
| Unstage a file | `git restore --staged` |
| Fix last commit message | `git commit --amend` |
| Remove local commits | `git reset` |
| Undo a pushed commit | `git revert` |

This table alone answers many day-to-day Git questions.

______________________________________________________________________

# Real-World Examples

### Accidentally edited a file

```bash id="git1121"
git restore app.py
```

______________________________________________________________________

### Staged too many files

```bash id="git1122"
git restore --staged app.py
```

______________________________________________________________________

### Wrong commit message

```bash id="git1123"
git commit --amend
```

______________________________________________________________________

### Bad commit already on GitHub

```bash id="git1124"
git revert HEAD
```

______________________________________________________________________

# Common Mistakes

### Using `git reset --hard` Without Understanding It

This can permanently remove work.

Be very careful.

______________________________________________________________________

### Using `git reset` on Shared Branches

Avoid rewriting history

that other developers are using.

Use

```text id="git1125"
git revert
```

instead.

______________________________________________________________________

### Forgetting the Difference

Remember:

- **restore** → files
- **reset** → local history
- **revert** → shared history

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| ----------------------------- | ---------------------------------- | ------------------------------ |
| `git restore <file>` | Discard local file changes | Undo edits |
| `git restore --staged <file>` | Unstage a file | Wrong `git add` |
| `git commit --amend` | Modify last commit | Fix message or add missed file |
| `git reset --soft HEAD~1` | Remove commit, keep staged changes | Combine commits |
| `git reset HEAD~1` | Remove commit, unstage changes | Reorganize commits |
| `git reset --hard HEAD~1` | Remove everything | Discard local work |
| `git revert HEAD` | Undo a pushed commit | Team projects |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between `git reset` and `git revert`?

`git reset` moves the branch pointer to an earlier commit, effectively rewriting local history. It is useful for undoing
local commits that haven't been shared. `git revert` creates a new commit that reverses the changes made by an earlier
commit without rewriting history. Because it preserves the commit history, `git revert` is the preferred approach for
undoing changes that have already been pushed to a shared repository.

______________________________________________________________________

# Summary

In this lesson, you learned:

- How to discard file changes
- How to unstage files
- How to amend commits
- Soft, mixed, and hard reset
- Reverting pushed commits
- Choosing the right undo command
- Best practices for local and shared repositories

______________________________________________________________________

# What's Next

[Git Stash - Saving Work Without Committing](12-git-stash.md)

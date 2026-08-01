# Git - Part 2

# Git Workflow (Working Directory, Staging Area & Repository)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll understand:

- How Git stores changes
- Working Directory
- Staging Area
- Repository
- How code moves through Git
- The commands you'll use every day

______________________________________________________________________

# Why Do We Need a Workflow?

Suppose you're working on your FastAPI project.

You modify 15 files.

Only 5 of them are complete.

Should Git save all 15?

Probably not.

Git allows you to choose **exactly** which changes should be saved.

This is done using the **Staging Area**.

______________________________________________________________________

# Git Workflow

Every change follows the same path.

```text
Working Directory

↓

Staging Area

↓

Repository (Commit)
```

Understanding this flow is the key to using Git effectively.

______________________________________________________________________

# Step 1 — Working Directory

The Working Directory is simply your project folder.

Example

```text
library-api/

├── app/

├── Dockerfile

├── requirements.txt

└── README.md
```

Whenever you:

- create a file
- edit a file
- delete a file

you're changing the **Working Directory**.

______________________________________________________________________

## When will you use it?

Always.

Every change you make starts here.

______________________________________________________________________

# Check Current Status

## Command

```bash
git status
```

Example

```text
Changes not staged for commit

modified: app.py
```

Git is saying:

> "I noticed you changed a file."

But it isn't ready to save it yet.

______________________________________________________________________

## When will you use this?

Constantly.

Most developers run:

```bash
git status
```

many times every day.

______________________________________________________________________

# Step 2 — Staging Area

The Staging Area is like a **waiting room**.

Files placed here are ready to become part of the next commit.

Think of it as selecting files before taking a photo.

______________________________________________________________________

# Stage One File

## Command

```bash
git add app.py
```

Now

only

```text
app.py
```

is prepared for the next commit.

______________________________________________________________________

## When will you use this?

Whenever you finish working on a file and want to include it in the next commit.

Example:

You edited

- app.py ✅
- models.py ❌ (still incomplete)

You stage only

```bash
git add app.py
```

______________________________________________________________________

# Stage Multiple Files

## Command

```bash
git add app.py models.py routes.py
```

______________________________________________________________________

## When will you use this?

When multiple completed files belong to the same feature.

Example:

```
User Login

↓

app.py

routes.py

schemas.py
```

Commit them together.

______________________________________________________________________

# Stage Everything

## Command

```bash
git add .
```

This stages every new, modified, and deleted file in the current directory and its subdirectories.

______________________________________________________________________

## When will you use this?

When all your changes are complete and belong in the same commit.

______________________________________________________________________

## Be Careful

Many beginners always use

```bash
git add .
```

This can accidentally include:

- temporary files
- debugging code
- unfinished work

Always check

```bash
git status
```

before committing.

______________________________________________________________________

# Verify the Staging Area

## Command

```bash
git status
```

Example

```text
Changes to be committed

modified: app.py
```

Notice the difference.

Previously

```
Changes not staged
```

Now

```
Changes to be committed
```

The file has moved into the Staging Area.

______________________________________________________________________

# Step 3 — Repository

The Repository is where Git permanently stores your commits.

Once committed,

the snapshot becomes part of your project's history.

We'll create commits in the next lesson.

______________________________________________________________________

# Complete Flow

```text
Edit File

↓

git status

↓

git add

↓

git status

↓

git commit
```

This is the basic Git workflow you'll repeat throughout your career.

______________________________________________________________________

# Real Project Example

Suppose you're adding JWT authentication.

You modify:

```text
auth.py

main.py

requirements.txt

README.md
```

All these changes belong to one feature.

Stage them together.

```bash
git add auth.py main.py requirements.txt README.md
```

Then commit them together.

This keeps your history clean and meaningful.

______________________________________________________________________

# Common Mistakes

### Forgetting to Stage Files

You edit a file,

run

```bash
git commit
```

and wonder why nothing happened.

Git only commits staged changes.

______________________________________________________________________

### Always Using `git add .`

It's convenient,

but don't use it blindly.

Review what you're staging first.

______________________________________________________________________

### Large Commits

Instead of one huge commit containing unrelated work,

make several smaller,

logical commits.

They're much easier to review and debug.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| --------------------- | ----------------------- | --------------------------------- |
| `git status` | Check repository status | Constantly |
| `git add app.py` | Stage one file | After finishing a file |
| `git add file1 file2` | Stage multiple files | One feature across multiple files |
| `git add .` | Stage all changes | When everything is ready |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the purpose of the Git Staging Area?

The Staging Area allows developers to select which changes should be included in the next commit. Instead of committing
every modification in the working directory, Git lets you review and organize changes into logical commits, resulting in
a cleaner and more meaningful project history.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Working Directory
- Staging Area
- Repository
- `git status`
- `git add`
- The complete Git workflow
- When to stage files
- Common staging mistakes

______________________________________________________________________

# What's Next

[Commits & Commit History](03-commits-and-commit-history.md)

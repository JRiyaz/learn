# Git - Part 7

# .gitignore - Ignoring Files and Folders

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What `.gitignore` is
- Why it's important
- When to use it
- How to ignore files and folders
- Common patterns
- Common mistakes

______________________________________________________________________

# Why Do We Need .gitignore?

Not every file in your project should be tracked by Git.

Imagine your FastAPI project.

```text
library-api/

├── app/

├── .venv/

├── __pycache__/

├── .env/

├── logs/

└── requirements.txt
```

Should Git track everything?

No.

Some files are:

- Temporary
- Machine-specific
- Generated automatically
- Secret

That's where `.gitignore` comes in.

______________________________________________________________________

# What is .gitignore?

`.gitignore` is a text file that tells Git:

> "Ignore these files and folders."

Git won't track them unless they were already being tracked before.

______________________________________________________________________

# Create a .gitignore File

Simply create a file named

```text
.gitignore
```

at the root of your project.

Example

```text
library-api/

├── .gitignore

├── app/

└── requirements.txt
```

______________________________________________________________________

# Ignore a File

Suppose your project contains

```text
.env
```

Inside `.gitignore`

```text
.env
```

______________________________________________________________________

## When will you use this?

Almost every backend project.

`.env` usually contains:

- Database passwords
- API keys
- JWT secrets
- Cloud credentials

These should **never** be committed.

______________________________________________________________________

# Ignore a Folder

Example

```text
__pycache__/
```

Git ignores

the entire folder.

______________________________________________________________________

## When will you use this?

Python automatically creates

```text
__pycache__/
```

You should never commit it.

______________________________________________________________________

# Ignore Virtual Environment

Example

```text
.venv/
```

or

```text
venv/
```

______________________________________________________________________

## Why?

Every developer has their own virtual environment.

Instead,

commit

```text
requirements.txt
```

and let others recreate the environment.

______________________________________________________________________

# Ignore Log Files

Example

```text
*.log
```

This ignores

```text
app.log

server.log

error.log
```

______________________________________________________________________

## When will you use this?

Applications often generate log files.

They don't belong in Git.

______________________________________________________________________

# Ignore Python Cache

Example

```text
__pycache__/

*.pyc
```

These files are generated automatically.

They can always be recreated.

______________________________________________________________________

# Ignore IDE Files

VS Code

```text
.vscode/
```

PyCharm

```text
.idea/
```

These contain personal editor settings.

They usually shouldn't be shared.

______________________________________________________________________

# Ignore OS Files

macOS

```text
.DS_Store
```

Windows

```text
Thumbs.db
```

These files are operating system artifacts.

______________________________________________________________________

# A Typical Python .gitignore

```text
.venv/

__pycache__/

*.pyc

.env

*.log

.vscode/

.idea/

.DS_Store

Thumbs.db
```

This is a great starting point for most Python projects.

______________________________________________________________________

# What if Git is Already Tracking a File?

Suppose you accidentally committed

```text
.env
```

Adding it to `.gitignore`

does **not** stop Git from tracking it.

Git already knows about the file.

You must remove it from Git's index.

## Command

```bash
git rm --cached .env
```

Then commit the change.

Now Git will ignore it.

______________________________________________________________________

## When will you use this?

Whenever you accidentally commit:

- `.env`
- Log files
- Virtual environments
- Cache files

______________________________________________________________________

# Check Ignored Files

Sometimes you're unsure

whether Git is ignoring a file.

## Command

```bash
git status
```

If the file doesn't appear,

it's being ignored.

______________________________________________________________________

# Real Project Example

A FastAPI project usually ignores

```text
.venv/

__pycache__/

.env

*.pyc

*.log

.vscode/
```

These are some of the most common entries you'll see in production repositories.

______________________________________________________________________

# Common Mistakes

### Forgetting `.env`

One of the biggest mistakes beginners make.

Never commit secrets.

______________________________________________________________________

### Committing Virtual Environments

A virtual environment can contain thousands of files.

Only commit

```text
requirements.txt
```

or

```text
pyproject.toml
```

______________________________________________________________________

### Thinking `.gitignore` Removes Tracked Files

It doesn't.

Use

```bash
git rm --cached <file>
```

first.

______________________________________________________________________

### Ignoring Too Much

Be careful not to ignore important files

like

```text
requirements.txt

Dockerfile
```

These should absolutely be tracked.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| ------------------------ | -------------------- | ------------------------------ |
| Create `.gitignore` | Ignore files | Every project |
| `git rm --cached <file>` | Stop tracking a file | Accidentally committed secrets |
| `git status` | Verify ignored files | Anytime |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the purpose of a `.gitignore` file?

A `.gitignore` file tells Git which files and directories should not be tracked. It is commonly used to exclude
generated files, virtual environments, cache files, logs, IDE settings, and sensitive files such as `.env`. This keeps
the repository clean and prevents unnecessary or confidential files from being committed.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What `.gitignore` is
- Why it's important
- How to ignore files and folders
- Common ignore patterns
- How to stop tracking an already committed file
- Best practices for Python projects

______________________________________________________________________

# What's Next

[GitHub, Remote Repositories & Connecting Your Local Repository](08-github-and-remote-repositories.md)

# Git - Part 21

# Git Internals - Objects, Blobs, Trees & Commits

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- How Git stores data
- What Git Objects are
- Blob Objects
- Tree Objects
- Commit Objects
- HEAD
- Why Git is fast

> **Note:** You don't need to memorize Git internals for daily development. However, understanding them helps explain why Git behaves the way it does and is a common interview topic.

______________________________________________________________________

# How Does Git Store Your Project?

Many beginners think Git stores:

```text id="git2101"
project.zip

↓

project_v2.zip

↓

project_v3.zip
```

It doesn't.

Git stores your project as a collection of **objects**.

______________________________________________________________________

# Git Object Database

Inside every repository,

there is a hidden directory.

```text id="git2102"
.git/

↓

objects/
```

This is Git's database.

Every file,

directory,

and commit

is stored as an object.

______________________________________________________________________

# Three Main Object Types

Git mainly stores:

```text id="git2103"
Blob

↓

Tree

↓

Commit
```

Everything else is built around these.

______________________________________________________________________

# Blob Object

A **Blob** stores the contents of a file.

Example

```text id="git2104"
app.py

↓

Blob
```

Important:

A Blob stores only the file's contents.

It does **not** know:

- Filename
- Folder
- Permissions

______________________________________________________________________

# Example

Suppose

```python id="git2105"
print("Hello")
```

Git stores

```text id="git2106"
Blob

↓

print("Hello")
```

Nothing else.

______________________________________________________________________

# Tree Object

A Tree represents a directory.

Example

```text id="git2107"
project/

├── app.py

├── models.py

└── routes.py
```

Git stores

```text id="git2108"
Tree

↓

Blob (app.py)

↓

Blob (models.py)

↓

Blob (routes.py)
```

A Tree knows:

- File names
- Folder names
- Relationships between files

______________________________________________________________________

# Commit Object

A Commit doesn't store files directly.

Instead,

it points to a Tree.

Example

```text id="git2109"
Commit

↓

Tree

↓

Files
```

A Commit also stores:

- Author
- Date
- Commit Message
- Parent Commit

______________________________________________________________________

# Commit Chain

Imagine three commits.

```text id="git2110"
Commit C

↓

Commit B

↓

Commit A
```

Each commit points

to its parent.

This creates

Git's history.

______________________________________________________________________

# What is HEAD?

HEAD is simply a pointer.

Usually,

it points to

your current branch.

Example

```text id="git2111"
HEAD

↓

main

↓

Latest Commit
```

When you switch branches,

HEAD moves.

______________________________________________________________________

# Example

Current branch

```text id="git2112"
main
```

Run

```bash id="git2113"
git switch feature/login
```

Now

```text id="git2114"
HEAD

↓

feature/login
```

HEAD always represents

where you're currently working.

______________________________________________________________________

# Why Is Git Fast?

Suppose

you change

one line

in

```text id="git2115"
app.py
```

Git does **not** duplicate

your entire project.

Instead,

it creates:

```text id="git2116"
New Blob

↓

New Tree

↓

New Commit
```

Everything else

is reused.

This is one reason Git is so efficient.

______________________________________________________________________

# SHA Hashes

Every Git object

has a unique identifier.

Example

```text id="git2117"
3f92ab71d6...
```

This is a SHA hash.

Git uses these hashes

to identify objects.

If the file changes,

its hash changes.

______________________________________________________________________

# Real Project Example

Suppose

your project contains

```text id="git2118"
app.py

models.py

Dockerfile
```

Git stores something like

```text id="git2119"
Blob

↓

app.py

Blob

↓

models.py

Blob

↓

Dockerfile

↓

Tree

↓

Commit
```

Everything is connected

through objects.

______________________________________________________________________

# Why Should You Care?

Most developers

never directly interact

with Git objects.

But understanding them explains:

- Why commits are fast
- Why Git detects changes efficiently
- Why commit hashes are unique
- Why history is reliable

______________________________________________________________________

# Common Mistakes

### Thinking Commits Store Entire Projects

Commits point to Trees.

Trees point to Blobs.

______________________________________________________________________

### Confusing HEAD with a Branch

HEAD isn't a branch.

It points to your current branch

(or directly to a commit in detached HEAD mode).

______________________________________________________________________

### Memorizing Internals

Don't memorize object formats.

Understand the concepts.

That's enough for interviews.

______________________________________________________________________

# Concepts Learned

| Concept | Purpose |
| -------- | -------------------------------- |
| Blob | Stores file contents |
| Tree | Stores directory structure |
| Commit | Stores project snapshot metadata |
| HEAD | Points to current branch/commit |
| SHA Hash | Unique object identifier |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How does Git store data internally?

Git stores data as objects inside the `.git/objects` directory. File contents are stored as **Blob** objects,
directories are represented by **Tree** objects, and project snapshots are stored as **Commit** objects, which reference
a Tree and contain metadata such as the author, date, message, and parent commit. Git identifies every object using a
SHA hash, making the repository efficient and reliable.

______________________________________________________________________

# Summary

In this lesson, you learned:

- How Git stores data
- Blob objects
- Tree objects
- Commit objects
- HEAD
- SHA hashes
- Why Git is efficient
- Basic Git internals

______________________________________________________________________

# What's Next

[Git Garbage Collection & Repository Maintenance](22-git-garbage-collection.md)

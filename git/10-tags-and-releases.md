# Git - Part 10

# Tags & Releases

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Git Tags are
- Why Tags are used
- Lightweight vs Annotated Tags
- How to create Tags
- How to list Tags
- How to delete Tags
- How Tags are used for software releases

______________________________________________________________________

# Why Do We Need Tags?

Imagine you've been working on your Library API for six months.

Your commit history looks like this.

```text id="git1001"
Commit A

↓

Commit B

↓

Commit C

↓

Commit D

↓

Commit E

↓

Commit F
```

Now your manager says:

> Deploy **Version 1.0.0**

Which commit is Version 1.0.0?

Without a tag,

you have to remember the commit hash.

That's difficult.

Instead,

we attach a **Tag**.

______________________________________________________________________

# What is a Tag?

A Tag is a **named reference to a specific commit**.

Instead of remembering

```text id="git1002"
3f92ab7
```

you can use

```text id="git1003"
v1.0.0
```

Much easier.

______________________________________________________________________

# Real-World Example

Suppose your project evolves like this.

```text id="git1004"
Initial Project

↓

Login Feature

↓

JWT Authentication

↓

Redis Cache

↓

Docker Support
```

After Docker support,

you release

```text id="git1005"
v1.0.0
```

Now,

anyone can retrieve the exact code used for version 1.0.0.

______________________________________________________________________

# List Existing Tags

## Command

```bash id="git1006"
git tag
```

Example

```text id="git1007"
v1.0.0

v1.1.0

v2.0.0
```

______________________________________________________________________

## When will you use this?

Whenever you want to see

which versions

have been released.

______________________________________________________________________

# Create a Lightweight Tag

## Command

```bash id="git1008"
git tag v1.0.0
```

This creates

a simple tag

pointing to

the current commit.

______________________________________________________________________

## When will you use this?

Rarely.

Most teams prefer

Annotated Tags

because they store additional information.

______________________________________________________________________

# Create an Annotated Tag

## Command

```bash id="git1009"
git tag -a v1.0.0 -m "First production release"
```

Example

```text id="git1010"
Tag:

v1.0.0

Message:

First production release
```

______________________________________________________________________

## Why Annotated Tags?

They store:

- Tag name
- Creator
- Date
- Message

Making them ideal

for production releases.

______________________________________________________________________

# View Tag Information

## Command

```bash id="git1011"
git show v1.0.0
```

Example

```text id="git1012"
Tag:

v1.0.0

Message:

First production release

Commit:

...
```

______________________________________________________________________

## When will you use this?

When reviewing

release information

or checking

what a version contains.

______________________________________________________________________

# Tag an Older Commit

Suppose you forgot

to tag a release.

First,

find the commit.

```bash id="git1013"
git log --oneline
```

Example

```text id="git1014"
9ab12cd Add Docker

8ff31de Add Redis

4cb21ef Add JWT
```

Tag it.

```bash id="git1015"
git tag -a v1.0.0 9ab12cd -m "Version 1.0.0"
```

______________________________________________________________________

## When will you use this?

Sometimes

a release is created

after development is complete.

Git allows you

to tag any commit.

______________________________________________________________________

# Push Tags to GitHub

Tags are **not** pushed automatically.

Push a specific tag.

```bash id="git1016"
git push origin v1.0.0
```

Push every tag.

```bash id="git1017"
git push origin --tags
```

______________________________________________________________________

## When will you use this?

Whenever you're publishing

a new release

to GitHub.

______________________________________________________________________

# Delete a Local Tag

## Command

```bash id="git1018"
git tag -d v1.0.0
```

______________________________________________________________________

## When will you use this?

If you created

the wrong tag

or need to recreate it.

______________________________________________________________________

# Delete a Remote Tag

## Command

```bash id="git1019"
git push origin --delete v1.0.0
```

______________________________________________________________________

## When will you use this?

Occasionally,

if an incorrect release

was published.

______________________________________________________________________

# Tags vs Branches

Many beginners confuse them.

| Branch | Tag |
| -------------------- | --------------------------- |
| Continues to move | Points to one commit |
| Used for development | Used for releases |
| Receives new commits | Never changes automatically |

Think of it this way:

- Branch = Work in Progress
- Tag = Released Version

______________________________________________________________________

# Version Naming

Most projects follow

Semantic Versioning.

```text id="git1020"
v1.0.0

Major.Minor.Patch
```

Example

```text id="git1021"
v1.0.0

↓

v1.0.1

↓

v1.1.0

↓

v2.0.0
```

Where:

- **Major** → Breaking changes
- **Minor** → New features (backward compatible)
- **Patch** → Bug fixes

______________________________________________________________________

# Real Project Workflow

```text id="git1022"
Develop Feature

↓

Commit

↓

Merge

↓

Test

↓

Create Tag

↓

Push Tag

↓

Create GitHub Release
```

This is how many teams publish software.

______________________________________________________________________

# Common Mistakes

### Thinking Tags Move

They don't.

A tag always points

to the same commit

unless you delete and recreate it.

______________________________________________________________________

### Forgetting to Push Tags

```bash id="git1023"
git push
```

does **not** push tags.

You must push them separately.

______________________________________________________________________

### Using Branches as Releases

Branches are for development.

Tags identify released versions.

______________________________________________________________________

### Creating Too Many Tags

Create tags

for meaningful releases,

not every commit.

______________________________________________________________________

# Commands Learned

| Command | Purpose | When You'll Use It |
| -------------------------------- | ---------------------- | ------------------------- |
| `git tag` | List tags | View releases |
| `git tag v1.0.0` | Create lightweight tag | Rarely |
| `git tag -a v1.0.0 -m "..."` | Create annotated tag | Production releases |
| `git show <tag>` | View tag details | Inspect releases |
| `git push origin <tag>` | Push one tag | Publish release |
| `git push origin --tags` | Push all tags | Publish multiple releases |
| `git tag -d <tag>` | Delete local tag | Remove incorrect tag |
| `git push origin --delete <tag>` | Delete remote tag | Remove incorrect release |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the purpose of Git Tags?

Git Tags are used to mark specific commits as important milestones, typically software releases. Unlike branches, tags
do not move as new commits are added. They provide an easy way to reference released versions such as `v1.0.0` instead
of remembering commit hashes.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Git Tags are
- Lightweight vs Annotated Tags
- Creating tags
- Viewing tags
- Tagging older commits
- Pushing tags
- Deleting tags
- Semantic Versioning
- Tags vs Branches

______________________________________________________________________

# What's Next

[Undoing Changes - restore, reset & revert](11-undoing-changes.md)

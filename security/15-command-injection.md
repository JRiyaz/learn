# Security - Part 15

# Command Injection

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Command Injection is
- Why it happens
- How backend applications become vulnerable
- Unsafe Python examples
- Secure alternatives
- Safe use of `subprocess`
- Best practices

______________________________________________________________________

# What is Command Injection?

Command Injection is a vulnerability where **untrusted user input becomes part of an operating system command**.

Instead of treating the input as **data**,

the operating system interprets it as part of the command.

This allows an attacker to execute unintended system commands.

______________________________________________________________________

# Why Does It Happen?

Backend applications sometimes need to execute system commands.

Examples:

- Compress files
- Resize images
- Convert PDFs
- Run backups
- Execute shell scripts
- Check server status

The danger arises when user input is directly included in those commands.

______________________________________________________________________

# Typical Flow

```text id="cmd1501"
User Input

↓

Build Shell Command

↓

Operating System

↓

Command Executes
```

The operating system cannot distinguish between:

- Intended command
- User-controlled input

______________________________________________________________________

# Real-World Example

Suppose your application allows users to check whether a server is reachable.

Workflow

```text id="cmd1502"
User

↓

Host Name

↓

Backend

↓

System Command
```

If the application builds the command unsafely,

unexpected commands may also execute.

______________________________________________________________________

# Vulnerable Example

❌ Do **not** write code like this.

```python id="cmd1503"
import os

def ping(host: str):
    os.system(f"ping -c 4 {host}")
```

______________________________________________________________________

# Why Is This Vulnerable?

The command is built using string interpolation.

```python id="cmd1504"
f"ping -c 4 {host}"
```

The operating system receives

one complete command string.

Whenever user input changes the command itself,

there is a risk of command injection.

______________________________________________________________________

# Another Vulnerable Example

```python id="cmd1505"
import subprocess

subprocess.run(
    f"ls {directory}",
    shell=True
)
```

The dangerous part is:

```text id="cmd1506"
shell=True
```

The shell interprets the command,

making injection possible.

______________________________________________________________________

# Root Cause

Just like SQL Injection,

the root problem is:

```text id="cmd1507"
Command

+

User Input

↓

One String
```

Never allow untrusted input

to modify shell commands.

______________________________________________________________________

# Secure Solution 1

## Avoid Shell Commands

Instead of

```text id="cmd1508"
Shell Command
```

use

```text id="cmd1509"
Python Standard Library
```

Example

Instead of

```python id="cmd1510"
os.system("mkdir uploads")
```

Use

```python id="cmd1511"
from pathlib import Path

Path("uploads").mkdir(
    exist_ok=True
)
```

Native Python functions are usually safer.

______________________________________________________________________

# Secure Solution 2

## Use `subprocess` Safely

Good Example

```python id="cmd1512"
import subprocess

subprocess.run(
    ["ping", "-c", "4", host],
    check=True
)
```

Notice:

- Command arguments are passed as a list.
- `shell=True` is not used.

The operating system treats each argument separately.

______________________________________________________________________

# Secure Solution 3

## Validate Input

Suppose users may specify

a filename.

Validate:

- Length
- Allowed characters
- Expected format

Example

```python id="cmd1513"
import re

if not re.fullmatch(
    r"[A-Za-z0-9._-]+",
    filename,
):
    raise ValueError(
        "Invalid filename"
    )
```

Validation reduces risk,

but should not replace safe command execution.

______________________________________________________________________

# Secure Solution 4

## Principle of Least Privilege

Suppose your application executes commands.

The application user should have

only the permissions required.

Example

```text id="cmd1514"
Application User

↓

Read Uploads

↓

Write Uploads

↓

Cannot Modify System Files
```

Even if something goes wrong,

the damage is limited.

______________________________________________________________________

# Secure FastAPI Example

Workflow

```text id="cmd1515"
Request

↓

Validate Input

↓

Safe subprocess.run()

↓

Return Result
```

Never execute

raw user commands.

______________________________________________________________________

# Dangerous Python Functions

Be cautious with:

```python id="cmd1516"
os.system()

os.popen()

subprocess.run(..., shell=True)

subprocess.Popen(..., shell=True)
```

These are not inherently insecure,

but they become dangerous

when combined with untrusted input.

______________________________________________________________________

# Safer Alternatives

Prefer:

- `pathlib`
- `shutil`
- `os.listdir()`
- `glob`
- `subprocess.run()` with argument lists

Most filesystem tasks

do not require shell commands.

______________________________________________________________________

# Defense in Depth

Protect command execution with multiple layers.

```text id="cmd1517"
Input Validation

↓

No shell=True

↓

Argument Lists

↓

Least Privilege

↓

Logging
```

______________________________________________________________________

# Best Practices

✅ Prefer Python libraries over shell commands.

✅ Use `subprocess.run()` with argument lists.

✅ Avoid `shell=True`.

✅ Validate user input.

✅ Run applications with minimal privileges.

✅ Log command execution where appropriate.

______________________________________________________________________

# Common Mistakes

### Using `shell=True`

Only use it when absolutely necessary,

and never with user-controlled input.

______________________________________________________________________

### Trusting Filenames

Treat filenames,

paths,

and command arguments

as untrusted input.

______________________________________________________________________

### Executing User Commands

Users should never be able

to specify arbitrary system commands.

______________________________________________________________________

### Running Applications as Root

Follow the Principle of Least Privilege.

A command injection vulnerability becomes far more severe

if the application runs with administrative privileges.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| ----------------------------- | ----------------------- |
| `os.system()` with user input | Native Python libraries |
| `shell=True` | Argument list |
| No validation | Validate input |
| Root privileges | Least privilege |
| Arbitrary commands | Fixed commands |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Command Injection, and how can developers prevent it?

Command Injection occurs when untrusted user input becomes part of an operating system command, allowing unintended
commands to execute. Developers can prevent it by avoiding shell commands whenever possible, using Python's standard
library, calling `subprocess.run()` with argument lists instead of `shell=True`, validating user input, and following
the Principle of Least Privilege.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Command Injection is
- Why it happens
- Unsafe Python examples
- Safe `subprocess` usage
- Input validation
- Least privilege
- Best practices

______________________________________________________________________

# What's Next

[Path Traversal](16-path-traversal.md)

# Security - Part 16

# Path Traversal (Directory Traversal)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Path Traversal is
- Why it happens
- How attackers exploit file paths
- Vulnerable FastAPI examples
- Secure file access
- Safe file uploads/downloads
- Best practices

______________________________________________________________________

# What is Path Traversal?

Path Traversal (also called **Directory Traversal**) is a vulnerability where an attacker manipulates a file path to
access files or directories outside the intended location.

Instead of accessing only allowed files,

the attacker attempts to navigate the file system.

______________________________________________________________________

# Why Does It Happen?

Many applications allow users to:

- Download files
- View images
- Read documents
- Upload files
- Export reports

If the application directly trusts the file path provided by the user,

attackers may access unintended files.

______________________________________________________________________

# Typical Flow

```text id="pt1601"
User Input

↓

File Path

↓

Backend Reads File

↓

Sensitive File Returned
```

The backend assumes

the requested path

is safe.

______________________________________________________________________

# Real-World Example

Suppose your application stores reports in:

```text id="pt1602"
/uploads/reports/
```

Users should only download files from this directory.

Instead,

the application allows users to specify any filename.

______________________________________________________________________

# Vulnerable FastAPI Example

```python id="pt1603"
from fastapi import FastAPI

app = FastAPI()

@app.get("/download")
def download(filename: str):

    with open(
        f"uploads/{filename}",
        "r"
    ) as file:
        return file.read()
```

______________________________________________________________________

# Why Is This Vulnerable?

The application trusts

the user's filename.

Workflow

```text id="pt1604"
User Input

↓

String Concatenation

↓

File System
```

If the filename points outside the uploads directory,

the backend may read unintended files.

______________________________________________________________________

# The Root Problem

The issue isn't

`open()`.

The issue is

allowing the client

to control

the filesystem path.

______________________________________________________________________

# Unsafe Design

```text id="pt1605"
User

↓

Filename

↓

Direct File Access
```

The application never verifies

whether the file

belongs to the allowed directory.

______________________________________________________________________

# Secure Solution 1

## Use File IDs

Instead of accepting

a filename,

accept

a database ID.

Workflow

```text id="pt1606"
User

↓

File ID

↓

Database Lookup

↓

Stored Safe Path

↓

Read File
```

Now,

users cannot choose

arbitrary file paths.

This is the preferred design.

______________________________________________________________________

# Secure Solution 2

## Use `pathlib`

Instead of string concatenation,

use

```python id="pt1607"
from pathlib import Path

UPLOAD_DIR = Path("uploads")

file_path = (
    UPLOAD_DIR / filename
).resolve()
```

The resolved path

can then be validated.

______________________________________________________________________

# Secure Solution 3

## Verify the Path

Ensure the resolved path

remains inside

the upload directory.

Example

```python id="pt1608"
if not str(file_path).startswith(
    str(UPLOAD_DIR.resolve())
):
    raise HTTPException(
        status_code=403,
        detail="Access denied",
    )
```

Now,

even if someone manipulates the filename,

files outside the upload directory are rejected.

______________________________________________________________________

# Secure Solution 4

## Restrict Allowed Files

Instead of serving every file,

allow only expected types.

Example

```text id="pt1609"
Allowed

↓

PDF

PNG

JPG

TXT
```

Reject unknown or unsupported file types.

______________________________________________________________________

# Secure File Downloads

Good workflow

```text id="pt1610"
File ID

↓

Database Lookup

↓

Ownership Check

↓

Safe Path

↓

Read File
```

Notice

there are multiple security checks.

______________________________________________________________________

# Secure File Uploads

Uploads should also be validated.

Check:

- File size
- MIME type
- Extension
- Storage directory
- Generated filename

Never store files

using the original filename.

Instead,

generate unique filenames.

Example

```text id="pt1611"
invoice.pdf

↓

8c91a7d2.pdf
```

We'll discuss uploads in detail

in the next lesson.

______________________________________________________________________

# Principle of Least Exposure

Users should only access

files they are authorized to access.

Example

```text id="pt1612"
Current User

↓

Own Documents

↓

Allowed

↓

Other User's Documents

↓

Forbidden
```

Path validation alone

doesn't replace

authorization.

______________________________________________________________________

# Defense in Depth

Secure file access combines:

```text id="pt1613"
File ID

↓

Ownership Validation

↓

Path Validation

↓

Allowed Directory

↓

Logging
```

______________________________________________________________________

# Best Practices

✅ Use file IDs instead of filenames.

✅ Validate resolved paths.

✅ Use `pathlib`.

✅ Restrict file types.

✅ Generate unique filenames.

✅ Verify ownership.

______________________________________________________________________

# Common Mistakes

### Trusting User Filenames

Treat filenames

like any other user input.

Never trust them.

______________________________________________________________________

### Building Paths with Strings

Avoid

```python
"uploads/" + filename
```

Prefer

`pathlib.Path`.

______________________________________________________________________

### Returning Files Without Authorization

Even a valid path

should still require

authorization checks.

______________________________________________________________________

### Using Original Filenames

Generated filenames

reduce collisions

and improve security.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| -------------------- | ------------------------- |
| User-controlled path | File ID lookup |
| String concatenation | `pathlib.Path` |
| No path validation | Verify resolved path |
| Original filename | Generated filename |
| No ownership check | Authorization + ownership |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Path Traversal, and how can developers prevent it?

Path Traversal is a vulnerability where attackers manipulate file paths to access files outside the intended directory.
Developers can prevent it by avoiding user-controlled file paths, using file IDs instead of filenames, validating
resolved paths with libraries such as `pathlib`, restricting access to approved directories, generating unique
filenames, and enforcing authorization checks before serving files.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Path Traversal is
- Why it happens
- Vulnerable FastAPI code
- Safe file access
- Path validation
- `pathlib`
- Ownership validation
- Best practices

______________________________________________________________________

# What's Next

[File Upload Security](17-file-upload-security.md)

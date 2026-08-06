# Linux Complete Interview & Production Course

# File 07 — File Permissions

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Users & Permissions
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 06 — Users and Groups

______________________________________________________________________

# Table of Contents

1. Introduction
1. Why Permissions Matter
1. Understanding Linux Permission Model
1. Ownership
1. Reading Permission Strings
1. Permission Types
1. Numeric (Octal) Permissions
1. Symbolic Permissions
1. The `chmod` Command
1. The `chown` Command
1. The `chgrp` Command
1. The `umask` Command
1. Default File and Directory Permissions
1. Recursive Permission Changes
1. Production Examples
1. Common Mistakes
1. Best Practices
1. Interview Questions
1. Practice Exercises
1. Cheat Sheet
1. Summary
1. Next

______________________________________________________________________

# 1. Introduction

Linux permissions are one of its strongest security features.

Every file and directory has an associated permission set that determines:

- Who can read it
- Who can modify it
- Who can execute it

Without permissions, any user could modify or delete another user's files, making the system insecure.

______________________________________________________________________

# 2. Why Permissions Matter

Imagine a production server running:

- Nginx
- PostgreSQL
- Redis
- FastAPI

If every process could freely access every file:

- Secrets could be stolen.
- Databases could be modified.
- Configuration files could be deleted.
- Applications could overwrite each other's data.

Permissions prevent these issues.

______________________________________________________________________

# 3. Understanding Linux Permission Model

Every file belongs to:

- An owner (User)
- A group
- Everyone else (Others)

Linux checks permissions in this order:

```
Request

↓

Owner?

↓

Group?

↓

Others?
```

The first matching rule determines access.

______________________________________________________________________

# 4. Ownership

Display ownership:

```bash
ls -l
```

Example:

```text
-rw-r--r-- 1 riyaz developers 2450 Jul 20 app.py
```

Breakdown:

```
-rw-r--r--

↓

Permission String

riyaz

↓

Owner

developers

↓

Group
```

______________________________________________________________________

# 5. Reading Permission Strings

Example:

```text
-rwxr-xr--
```

Break it into parts:

```
-

File Type

rwx

Owner

r-x

Group

r--

Others
```

______________________________________________________________________

## First Character

| Symbol | Meaning |
|---------|----------|
| - | Regular file |
| d | Directory |
| l | Symbolic link |
| c | Character device |
| b | Block device |
| s | Socket |
| p | Named pipe |

______________________________________________________________________

## Permission Characters

| Symbol | Meaning |
|---------|----------|
| r | Read |
| w | Write |
| x | Execute |
| - | Permission absent |

______________________________________________________________________

# 6. Permission Types

## Read (`r`)

Value:

```
4
```

Allows:

- Open a file
- Read its contents

For directories:

- View directory contents

______________________________________________________________________

## Write (`w`)

Value:

```
2
```

Allows:

- Modify file contents
- Delete or rename files (with appropriate directory permissions)

For directories:

- Create files
- Delete files
- Rename files

______________________________________________________________________

## Execute (`x`)

Value:

```
1
```

Allows:

- Execute programs or scripts

For directories:

- Enter the directory
- Access files within it (if combined with appropriate permissions)

______________________________________________________________________

# Example

File:

```text
-rwx------
```

Owner can:

- Read
- Write
- Execute

Everyone else:

No access.

______________________________________________________________________

# 7. Numeric (Octal) Permissions

Linux represents permissions using numbers.

| Permission | Value |
|------------|------:|
| Read | 4 |
| Write | 2 |
| Execute | 1 |

Add the values together.

______________________________________________________________________

## Examples

### 7

```
4 + 2 + 1

↓

rwx
```

______________________________________________________________________

### 6

```
4 + 2

↓

rw-
```

______________________________________________________________________

### 5

```
4 + 1

↓

r-x
```

______________________________________________________________________

### 4

```
4

↓

r--
```

______________________________________________________________________

### 0

```
---

↓

No permission
```

______________________________________________________________________

## Common Permission Values

| Numeric | Symbolic | Meaning |
|----------|----------|---------|
| 777 | rwxrwxrwx | Full access for everyone |
| 755 | rwxr-xr-x | Common for directories and executables |
| 750 | rwxr-x--- | Owner full, group read/execute |
| 700 | rwx------ | Private directory |
| 644 | rw-r--r-- | Common for files |
| 640 | rw-r----- | Owner read/write, group read |
| 600 | rw------- | Private file |

______________________________________________________________________

# 8. Symbolic Permissions

Instead of numbers, Linux also supports symbolic notation.

Users:

| Symbol | Meaning |
|---------|----------|
| u | User |
| g | Group |
| o | Others |
| a | All |

Operations:

| Symbol | Meaning |
|---------|----------|
| + | Add permission |
| - | Remove permission |
| = | Set exact permission |

______________________________________________________________________

Examples:

Add execute permission for owner:

```bash
chmod u+x app.py
```

______________________________________________________________________

Remove write permission:

```bash
chmod g-w app.py
```

______________________________________________________________________

Give everyone read permission:

```bash
chmod a+r app.py
```

______________________________________________________________________

# 9. The `chmod` Command

Change permissions.

Basic syntax:

```bash
chmod permissions file
```

______________________________________________________________________

Numeric mode

```bash
chmod 755 app.py
```

______________________________________________________________________

Private file

```bash
chmod 600 secrets.txt
```

______________________________________________________________________

Executable script

```bash
chmod +x deploy.sh
```

Equivalent:

```bash
chmod u+x deploy.sh
```

______________________________________________________________________

Remove execute permission

```bash
chmod -x deploy.sh
```

______________________________________________________________________

Set exact symbolic permissions

```bash
chmod u=rwx,g=rx,o=r app.py
```

______________________________________________________________________

Recursive

```bash
chmod -R 755 project
```

Use with care.

______________________________________________________________________

# 10. The `chown` Command

Changes ownership.

Basic syntax:

```bash
sudo chown owner file
```

Example:

```bash
sudo chown riyaz app.py
```

______________________________________________________________________

Change owner and group:

```bash
sudo chown riyaz:developers app.py
```

______________________________________________________________________

Recursive:

```bash
sudo chown -R riyaz:developers project
```

______________________________________________________________________

# 11. The `chgrp` Command

Changes only the group.

```bash
sudo chgrp developers app.py
```

Recursive:

```bash
sudo chgrp -R developers project
```

______________________________________________________________________

# 12. The `umask` Command

When a new file is created, Linux starts with default permissions and then subtracts the **umask** value.

Display current umask:

```bash
umask
```

Example:

```text
0022
```

______________________________________________________________________

Typical defaults:

Files:

```
666
```

Directories:

```
777
```

Subtract:

```
022
```

Result:

Files:

```
644
```

Directories:

```
755
```

______________________________________________________________________

Temporarily change umask:

```bash
umask 027
```

New files:

```
640
```

New directories:

```
750
```

______________________________________________________________________

# 13. Default File and Directory Permissions

Most Linux systems create:

New file:

```text
-rw-r--r--
```

New directory:

```text
drwxr-xr-x
```

These values come from the interaction between the system defaults and the current `umask`.

______________________________________________________________________

# 14. Recursive Permission Changes

Apply permissions to an entire directory tree.

```bash
chmod -R 755 project
```

Change ownership recursively:

```bash
sudo chown -R www-data:www-data /var/www/html
```

Always verify the target path before using `-R`.

______________________________________________________________________

# 15. Production Examples

## Make deployment script executable

```bash
chmod +x deploy.sh
```

______________________________________________________________________

## Secure SSH private key

```bash
chmod 600 ~/.ssh/id_rsa
```

SSH will refuse to use keys with overly permissive permissions.

______________________________________________________________________

## Fix web server ownership

```bash
sudo chown -R www-data:www-data /var/www/html
```

______________________________________________________________________

## Share project with developers group

```bash
sudo chgrp -R developers project
chmod -R 775 project
```

______________________________________________________________________

## Restrict secret configuration

```bash
chmod 600 .env
```

______________________________________________________________________

# 16. Common Mistakes

❌ Using `chmod 777` on everything.

This removes meaningful access control and creates security risks.

______________________________________________________________________

❌ Running recursive permission changes on the wrong directory.

Example:

```bash
chmod -R 777 /
```

This can severely compromise a system.

______________________________________________________________________

❌ Forgetting execute permission on shell scripts.

______________________________________________________________________

❌ Confusing file permissions with directory permissions.

Directories require execute permission to access their contents.

______________________________________________________________________

❌ Changing ownership unnecessarily.

______________________________________________________________________

# 17. Best Practices

- Follow the principle of least privilege.
- Avoid `777` unless absolutely necessary.
- Keep secret files (`.env`, SSH keys) readable only by their owner.
- Verify recursive commands before executing them.
- Use groups to share access rather than changing ownership repeatedly.

______________________________________________________________________

# Interview Questions

## Q1. What do the permission values `755` and `644` represent?

**Answer**

`755` means the owner has read, write, and execute permissions, while the group and others have read and execute
permissions. It is commonly used for directories and executable files.

`644` means the owner has read and write permissions, while the group and others have read-only access. It is commonly
used for regular files.

______________________________________________________________________

## Q2. What is the difference between `chmod`, `chown`, and `chgrp`?

**Answer**

- `chmod` changes file permissions.
- `chown` changes the file owner (and optionally the group).
- `chgrp` changes only the group ownership.

______________________________________________________________________

## Q3. Why should SSH private keys have permission `600`?

**Answer**

SSH requires private keys to be accessible only by their owner. If group or others have access, SSH treats the key as
insecure and refuses to use it.

______________________________________________________________________

## Q4. What is `umask`?

**Answer**

`umask` defines which permission bits are removed from the default permissions when new files and directories are
created.

______________________________________________________________________

## Q5. Why is `chmod 777` considered a bad practice?

**Answer**

It grants read, write, and execute permissions to everyone, allowing any user or process to modify or execute the file.
This significantly weakens system security.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Create a file and inspect its permissions.

```bash
touch notes.txt
ls -l notes.txt
```

______________________________________________________________________

## Exercise 2

Change permissions using:

- Numeric mode
- Symbolic mode

______________________________________________________________________

## Exercise 3

Create a shell script and make it executable.

______________________________________________________________________

## Exercise 4

Display your current `umask`.

Create a new file and observe the resulting permissions.

______________________________________________________________________

## Exercise 5

Create a project directory and recursively change:

- Ownership
- Group
- Permissions

______________________________________________________________________

# Cheat Sheet

## View Permissions

```bash
ls -l
```

______________________________________________________________________

## Change Permissions

```bash
chmod
chmod -R
```

______________________________________________________________________

## Change Owner

```bash
chown
chown -R
```

______________________________________________________________________

## Change Group

```bash
chgrp
chgrp -R
```

______________________________________________________________________

## View Umask

```bash
umask
```

______________________________________________________________________

## Common Values

| Value | Meaning |
|--------|---------|
| 755 | Standard executable/directory |
| 700 | Private directory |
| 644 | Standard file |
| 600 | Secret file |
| 777 | Avoid unless absolutely necessary |

______________________________________________________________________

# Summary

In this chapter, you learned how Linux controls access using ownership and permissions, how to interpret symbolic and
numeric permission formats, how to modify permissions with `chmod`, ownership with `chown`, group ownership with
`chgrp`, and how `umask` affects newly created files and directories. These concepts are essential for securing Linux
systems and are frequently tested in backend and DevOps interviews.

______________________________________________________________________

## Next

[ACL, SUID, SGID, and Sticky Bit](08-acl-suid-sgid-sticky-bit.md)

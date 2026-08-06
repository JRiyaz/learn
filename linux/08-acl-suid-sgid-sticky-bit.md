# Linux Complete Interview & Production Course

# File 08 — ACL, SUID, SGID, and Sticky Bit

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Users & Permissions
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 07 — File Permissions

______________________________________________________________________

# Table of Contents

1. Introduction
1. Limitations of Traditional Linux Permissions
1. What is an ACL?
1. Understanding ACL Entries
1. Managing ACLs
1. Default ACLs
1. What is SUID?
1. What is SGID?
1. What is the Sticky Bit?
1. Understanding Permission Indicators
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

Traditional Linux permissions work well for many situations, but they have limitations.

Suppose you have:

```
project/
```

Owner:

```
riyaz
```

Group:

```
developers
```

Now imagine only one additional user, `alice`, should have access.

Using normal permissions, you would have to:

- Change ownership, or
- Add Alice to the developers group.

Neither option is ideal.

Linux solves this with **Access Control Lists (ACLs)**.

Similarly, Linux provides three special permission bits:

- SUID
- SGID
- Sticky Bit

These enable controlled privilege escalation and shared directory behavior.

______________________________________________________________________

# 2. Limitations of Traditional Linux Permissions

Traditional permissions support only three categories:

```
Owner

↓

Group

↓

Others
```

Example:

```text
-rwxr-x---
```

What if:

- Alice needs access
- Bob should not
- Charlie only needs read access

Traditional permissions cannot express these rules directly.

ACLs solve this problem.

______________________________________________________________________

# 3. What is an ACL?

ACL stands for:

**Access Control List**

An ACL allows permissions to be assigned to:

- Individual users
- Specific groups

without changing the file owner or primary group.

Example:

```
Owner

↓

riyaz

↓

ACL

↓

alice → Read

bob → Read + Write

developers → Read
```

______________________________________________________________________

# Check ACL Support

Many modern Linux distributions support ACLs by default.

Verify:

```bash
mount | grep acl
```

______________________________________________________________________

# Install ACL Tools (Ubuntu)

```bash
sudo apt install acl
```

______________________________________________________________________

# 4. Understanding ACL Entries

Display ACL:

```bash
getfacl app.py
```

Example:

```text
# file: app.py
# owner: riyaz
# group: developers

user::rw-
user:alice:r--
group::r--
mask::rw-
other::---
```

Explanation:

| Entry | Meaning |
|--------|---------|
| user:: | Owner permissions |
| user:alice | Alice's permissions |
| group:: | Group permissions |
| mask | Maximum effective ACL permissions |
| other | Everyone else |

______________________________________________________________________

# 5. Managing ACLs

## Grant ACL

Give Alice read access.

```bash
setfacl -m u:alice:r app.py
```

______________________________________________________________________

Read and write.

```bash
setfacl -m u:alice:rw app.py
```

______________________________________________________________________

Grant a group access.

```bash
setfacl -m g:developers:rwx project
```

______________________________________________________________________

Remove ACL.

```bash
setfacl -x u:alice app.py
```

______________________________________________________________________

Remove all ACL entries.

```bash
setfacl -b app.py
```

______________________________________________________________________

# Verify

```bash
getfacl app.py
```

______________________________________________________________________

# 6. Default ACLs

Normally, newly created files inherit standard permissions.

ACLs allow inheritance of custom permissions.

Set default ACL:

```bash
setfacl -d -m g:developers:rwx project
```

Now every new file inside `project` inherits this rule.

______________________________________________________________________

View default ACL:

```bash
getfacl project
```

Look for:

```text
default:
```

entries.

______________________________________________________________________

# 7. What is SUID?

SUID stands for:

**Set User ID**

When applied to an executable,

the program runs with the permissions of its **owner**, not the user executing it.

______________________________________________________________________

Example:

```
User

↓

Runs passwd

↓

Program executes as root

↓

Password updated
```

Without SUID,

normal users could not change their own passwords.

______________________________________________________________________

View SUID:

```bash
ls -l /usr/bin/passwd
```

Example:

```text
-rwsr-xr-x
```

Notice:

```
s
```

instead of

```
x
```

______________________________________________________________________

Set SUID

```bash
chmod u+s program
```

Numeric:

```bash
chmod 4755 program
```

______________________________________________________________________

Remove:

```bash
chmod u-s program
```

______________________________________________________________________

# Find All SUID Files

```bash
find / -perm -4000
```

Useful for:

- Security audits
- Penetration testing
- System administration

______________________________________________________________________

# 8. What is SGID?

SGID stands for:

**Set Group ID**

Behavior depends on whether it's applied to:

- File
- Directory

______________________________________________________________________

## SGID on Files

Program executes using the file's group.

Set:

```bash
chmod g+s program
```

Numeric:

```bash
chmod 2755 program
```

______________________________________________________________________

## SGID on Directories

Very common.

Every newly created file inherits the directory's group.

Example:

```
project/

↓

Group

developers

↓

Every new file

↓

developers
```

Instead of:

```
Current User's Group
```

This is extremely useful for team collaboration.

______________________________________________________________________

# Find SGID Files

```bash
find / -perm -2000
```

______________________________________________________________________

# 9. What is the Sticky Bit?

Sticky Bit is mainly used on directories.

Without Sticky Bit:

Anyone with write permission can delete anyone else's files.

Example:

```
shared/

↓

Alice deletes Bob's file
```

Problem.

______________________________________________________________________

With Sticky Bit:

Users can delete only:

- Their own files
- Files owned by root

Example:

```
/tmp
```

uses Sticky Bit.

______________________________________________________________________

View

```bash
ls -ld /tmp
```

Output:

```text
drwxrwxrwt
```

Notice:

```
t
```

______________________________________________________________________

Set Sticky Bit

```bash
chmod +t shared
```

Numeric:

```bash
chmod 1777 shared
```

______________________________________________________________________

Remove

```bash
chmod -t shared
```

______________________________________________________________________

Find Sticky Bit Directories

```bash
find / -perm -1000
```

______________________________________________________________________

# 10. Understanding Permission Indicators

Example:

```text
-rwsr-xr-x
```

```
s

↓

SUID
```

______________________________________________________________________

Example:

```text
drwxrwsr-x
```

```
s

↓

SGID
```

______________________________________________________________________

Example:

```text
drwxrwxrwt
```

```
t

↓

Sticky Bit
```

______________________________________________________________________

Uppercase versions indicate:

Permission bit is set,

but execute permission is not.

Examples:

```
S

T
```

______________________________________________________________________

# Numeric Values

| Value | Meaning |
|--------|---------|
| 4000 | SUID |
| 2000 | SGID |
| 1000 | Sticky Bit |

Combined examples:

| Value | Meaning |
|--------|---------|
| 4755 | SUID |
| 2755 | SGID |
| 1777 | Sticky Bit |
| 6755 | SUID + SGID |

______________________________________________________________________

# 11. Production Examples

## Shared Development Directory

```bash
sudo chgrp developers project
chmod 2775 project
```

Every new file belongs to the `developers` group.

______________________________________________________________________

## Shared Upload Directory

```bash
chmod 1777 uploads
```

Users cannot delete each other's uploads.

______________________________________________________________________

## Password Management

```bash
ls -l /usr/bin/passwd
```

Observe the SUID bit.

______________________________________________________________________

## Grant Temporary User Access

```bash
setfacl -m u:alice:r reports.csv
```

______________________________________________________________________

## Remove Temporary Access

```bash
setfacl -x u:alice reports.csv
```

______________________________________________________________________

# 12. Common Mistakes

❌ Using ACLs when standard group permissions are sufficient.

______________________________________________________________________

❌ Granting SUID to custom scripts or binaries without understanding the security implications.

______________________________________________________________________

❌ Forgetting that SGID on directories affects newly created files.

______________________________________________________________________

❌ Assuming Sticky Bit prevents file modification.

It only controls file deletion and renaming within the directory.

______________________________________________________________________

❌ Leaving unnecessary ACL entries after a project ends.

______________________________________________________________________

# 13. Best Practices

- Prefer standard permissions when possible.
- Use ACLs for exceptional access requirements.
- Avoid creating unnecessary SUID executables.
- Periodically audit SUID and SGID files.
- Use SGID on shared team directories.
- Use Sticky Bit on shared writable directories.

______________________________________________________________________

# Interview Questions

## Q1. What problem do ACLs solve?

**Answer**

ACLs allow administrators to assign permissions to individual users or groups without changing file ownership or relying
solely on the owner, group, and others permission model.

______________________________________________________________________

## Q2. What is the purpose of SUID?

**Answer**

SUID allows an executable to run with the permissions of its owner instead of the user executing it. A common example is
the `passwd` program, which requires temporary root privileges to update password information.

______________________________________________________________________

## Q3. What is the difference between SGID on a file and on a directory?

**Answer**

On a file, SGID causes the program to execute with the file's group privileges. On a directory, SGID ensures that newly
created files and subdirectories inherit the directory's group ownership.

______________________________________________________________________

## Q4. What does the Sticky Bit do?

**Answer**

The Sticky Bit prevents users from deleting or renaming files owned by other users within a shared writable directory.
It is commonly used on directories like `/tmp`.

______________________________________________________________________

## Q5. When would you choose ACLs over traditional permissions?

**Answer**

ACLs are useful when a small number of specific users require different permissions without modifying the existing
ownership or group structure. They provide more granular access control than the standard permission model.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Display the ACL of a file.

```bash
getfacl app.py
```

______________________________________________________________________

## Exercise 2

Grant another user read access using ACL.

Verify the result.

______________________________________________________________________

## Exercise 3

Create a shared directory using SGID.

Verify that new files inherit the directory's group.

______________________________________________________________________

## Exercise 4

Inspect `/tmp`.

Verify that the Sticky Bit is set.

______________________________________________________________________

## Exercise 5

Locate all SUID files on your system.

______________________________________________________________________

## Exercise 6

Locate all SGID files on your system.

______________________________________________________________________

# Cheat Sheet

## ACL

```bash
getfacl
setfacl
```

______________________________________________________________________

## SUID

```bash
chmod u+s
chmod 4755
find / -perm -4000
```

______________________________________________________________________

## SGID

```bash
chmod g+s
chmod 2755
find / -perm -2000
```

______________________________________________________________________

## Sticky Bit

```bash
chmod +t
chmod 1777
find / -perm -1000
```

______________________________________________________________________

## Useful Commands

```bash
ls -l
ls -ld
```

______________________________________________________________________

# Summary

In this chapter, you learned how ACLs extend the traditional Linux permission model by allowing fine-grained access
control for specific users and groups. You also explored the three special permission bits—SUID, SGID, and Sticky
Bit—their behavior, security implications, and common production use cases such as shared project directories, password
management, and collaborative environments.

______________________________________________________________________

## Next

[Bash Shell and Environment](09-bash-shell-and-environment.md)

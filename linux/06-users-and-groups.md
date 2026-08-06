# Linux Complete Interview & Production Course

# File 06 — Users and Groups

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Users & Permissions
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 05 — File Searching and Links

______________________________________________________________________

# Table of Contents

1. Introduction
1. What are Users?
1. Why Linux is Multi-User
1. Types of Users
1. Understanding Groups
1. User and Group Relationship
1. User Information Files
1. Group Information Files
1. Essential User Commands
1. Group Management Commands
1. Switching Users
1. Sudo and Privilege Escalation
1. User Environment
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

Linux is designed as a **multi-user operating system**, allowing multiple users to work on the same machine
simultaneously while keeping their data isolated and secure.

Each user has:

- A username
- A unique User ID (UID)
- A primary group
- A home directory
- A default shell
- Specific permissions

Understanding users and groups is fundamental because almost every permission decision in Linux depends on them.

______________________________________________________________________

# 2. What are Users?

A user represents an identity recognized by the Linux operating system.

Every process running on Linux belongs to a user.

Examples:

- Running a Python application
- Starting an Nginx server
- Executing a Docker container
- Connecting via SSH

All of these actions are performed on behalf of a user.

______________________________________________________________________

# Why Do Users Exist?

Users provide:

- Security
- Isolation
- Accountability
- Permission management
- Resource ownership

Without users, every process would have unrestricted access to the system.

______________________________________________________________________

# 3. Types of Users

Linux primarily has three categories of users.

## Root User

The root user is the system administrator.

Username:

```text
root
```

UID:

```text
0
```

The root user can:

- Access every file
- Modify every configuration
- Install software
- Create users
- Delete users
- Shutdown the system

Use the root account carefully.

______________________________________________________________________

## Normal Users

Regular users perform everyday tasks.

Examples:

```text
riyaz
john
alice
```

Normal users have limited permissions and cannot modify critical system files without elevated privileges.

______________________________________________________________________

## System Users

System users are created for services and applications.

Examples:

```text
mysql
postgres
nginx
redis
www-data
```

They typically do not log in interactively.

Their purpose is to isolate services from each other.

______________________________________________________________________

# 4. Why Linux is Multi-User

Imagine a university server.

Users:

```
Student A

Student B

Professor

Administrator
```

All use the same machine simultaneously.

Each user has:

- Separate files
- Separate permissions
- Separate processes

One user cannot modify another user's files without permission.

______________________________________________________________________

# 5. Understanding Groups

A group is a collection of users.

Instead of assigning permissions individually, Linux allows permissions to be granted to groups.

Example:

```
Developers

├── Alice
├── Bob
└── Charlie
```

Granting permissions to the "Developers" group automatically applies them to all its members.

______________________________________________________________________

# Primary Group

Every user has one primary group.

Example:

```
User

riyaz

↓

Primary Group

riyaz
```

______________________________________________________________________

# Supplementary Groups

A user can belong to multiple additional groups.

Example:

```
riyaz

↓

docker

↓

sudo

↓

developers
```

This allows users to access different resources without changing ownership.

______________________________________________________________________

# 6. User and Group Relationship

```
User

↓

Primary Group

↓

Supplementary Groups

↓

Permissions
```

Whenever Linux checks permissions, it considers:

1. User ownership
1. Group membership
1. Others

______________________________________________________________________

# 7. User Information Files

Linux stores user information in:

```text
/etc/passwd
```

View it:

```bash
cat /etc/passwd
```

Example entry:

```text
riyaz:x:1000:1000:Riyaz:/home/riyaz:/bin/bash
```

Fields:

| Field | Description |
|--------|-------------|
| Username | Login name |
| Password Placeholder | Usually `x` |
| UID | User ID |
| GID | Primary Group ID |
| Description | Optional user info |
| Home Directory | User's home |
| Shell | Default shell |

______________________________________________________________________

# 8. Group Information Files

Groups are stored in:

```text
/etc/group
```

Display:

```bash
cat /etc/group
```

Example:

```text
docker:x:998:riyaz
```

Fields:

| Field | Description |
|--------|-------------|
| Group Name | Name |
| Password Placeholder | Usually `x` |
| GID | Group ID |
| Members | Users |

______________________________________________________________________

# Password Information

Passwords are stored separately in:

```text
/etc/shadow
```

This file is readable only by privileged users.

______________________________________________________________________

# 9. Essential User Commands

## whoami

Displays the current user.

```bash
whoami
```

Example:

```text
riyaz
```

______________________________________________________________________

## id

Displays user identity.

```bash
id
```

Example:

```text
uid=1000(riyaz)
gid=1000(riyaz)
groups=1000,27,999
```

______________________________________________________________________

## groups

Shows group memberships.

```bash
groups
```

Output:

```text
riyaz sudo docker developers
```

______________________________________________________________________

## who

Shows logged-in users.

```bash
who
```

______________________________________________________________________

## w

Displays logged-in users and their current activity.

```bash
w
```

______________________________________________________________________

## last

Shows login history.

```bash
last
```

______________________________________________________________________

## users

Displays currently logged-in usernames.

```bash
users
```

______________________________________________________________________

# 10. Group Management Commands

## groupadd

Create a group.

```bash
sudo groupadd developers
```

______________________________________________________________________

## groupdel

Delete a group.

```bash
sudo groupdel developers
```

______________________________________________________________________

## groupmod

Rename a group.

```bash
sudo groupmod -n backend developers
```

______________________________________________________________________

# 11. Switching Users

## su

Switch user.

```bash
su username
```

Example:

```bash
su root
```

______________________________________________________________________

Switch and load the user's environment.

```bash
su - username
```

______________________________________________________________________

Exit:

```bash
exit
```

______________________________________________________________________

# 12. Sudo and Privilege Escalation

Instead of logging in as root, Linux encourages using:

```bash
sudo
```

Example:

```bash
sudo apt update
```

Advantages:

- Safer
- Auditable
- Temporary elevation
- Reduced risk of accidental system damage

______________________________________________________________________

## Check Sudo Access

```bash
sudo -l
```

______________________________________________________________________

# 13. User Environment

Display current user.

```bash
echo $USER
```

Home directory.

```bash
echo $HOME
```

Current shell.

```bash
echo $SHELL
```

Current working directory.

```bash
pwd
```

______________________________________________________________________

# 14. Production Examples

## Determine the user running Nginx

```bash
ps aux | grep nginx
```

______________________________________________________________________

## Check Docker group membership

```bash
groups
```

______________________________________________________________________

## Verify current identity

```bash
id
```

______________________________________________________________________

## Review login history

```bash
last
```

______________________________________________________________________

## Switch to another administrative account

```bash
su - admin
```

______________________________________________________________________

# 15. Common Mistakes

❌ Logging in as the root user for everyday work.

______________________________________________________________________

❌ Editing `/etc/passwd` manually without understanding its format.

______________________________________________________________________

❌ Forgetting to add users to required groups such as `docker`.

______________________________________________________________________

❌ Confusing UID with GID.

______________________________________________________________________

❌ Using `su` when `sudo` is more appropriate.

______________________________________________________________________

# 16. Best Practices

- Use normal user accounts for daily work.
- Use `sudo` instead of logging in as root.
- Grant permissions through groups whenever possible.
- Regularly review group memberships.
- Protect `/etc/passwd` and `/etc/shadow`.

______________________________________________________________________

# Interview Questions

## Q1. What is the difference between a normal user and the root user?

**Answer**

The root user (UID 0) has unrestricted administrative privileges across the system, while normal users have limited
permissions and require `sudo` or root access to perform administrative tasks.

______________________________________________________________________

## Q2. What is the purpose of groups in Linux?

**Answer**

Groups simplify permission management by allowing multiple users to share the same access rights without assigning
permissions individually.

______________________________________________________________________

## Q3. What information is stored in `/etc/passwd`?

**Answer**

It stores user account information such as username, UID, GID, home directory, and default shell. Password hashes are
not stored here; they are stored in `/etc/shadow`.

______________________________________________________________________

## Q4. Why is `/etc/shadow` protected?

**Answer**

It contains password hashes and password policy information. Restricting access helps prevent unauthorized users from
obtaining sensitive authentication data.

______________________________________________________________________

## Q5. Why is `sudo` preferred over logging in as root?

**Answer**

`sudo` provides temporary privilege escalation, improves accountability through logging, and reduces the risk of
accidental system-wide changes by encouraging users to operate with limited privileges most of the time.

______________________________________________________________________

# Practice Exercises

1. Display your current user information using:

```bash
whoami
id
groups
```

______________________________________________________________________

2. View:

```bash
/etc/passwd
/etc/group
```

______________________________________________________________________

3. Display your login history.

______________________________________________________________________

4. Display all currently logged-in users.

______________________________________________________________________

5. Display:

- Current user
- Home directory
- Current shell

using environment variables.

______________________________________________________________________

# Cheat Sheet

## User Information

```bash
whoami
id
groups
users
who
w
last
```

______________________________________________________________________

## Switch Users

```bash
su
su -
exit
```

______________________________________________________________________

## Administrative Access

```bash
sudo
sudo -l
```

______________________________________________________________________

## Group Management

```bash
groupadd
groupdel
groupmod
```

______________________________________________________________________

## Important Files

```text
/etc/passwd
/etc/group
/etc/shadow
```

______________________________________________________________________

# Summary

In this chapter, you learned how Linux manages users and groups, the difference between root, normal, and system users,
how group memberships simplify permission management, the purpose of `/etc/passwd`, `/etc/group`, and `/etc/shadow`, and
how to inspect identities and safely perform administrative tasks using `sudo`.

______________________________________________________________________

## Next

[File Permissions](07-file-permissions.md)

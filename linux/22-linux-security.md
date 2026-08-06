# Linux Complete Interview & Production Course

# File 22 — Linux Security

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Security
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 21 — Log Management and Monitoring

______________________________________________________________________

# Table of Contents

1. Introduction
1. Why Linux Security Matters
1. Security Layers in Linux
1. Authentication
1. Authorization
1. File Permissions Revisited
1. Sudo and Least Privilege
1. Password Security
1. SSH Security
1. Firewall Basics
1. SELinux and AppArmor
1. File Integrity
1. Process Security
1. Security Auditing
1. Common Security Commands
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

Security is one of the most important responsibilities of a Linux administrator and backend engineer.

A production server may contain:

- Customer data
- API secrets
- Database credentials
- Source code
- Financial records

A single misconfiguration can expose sensitive information or allow unauthorized access.

Linux provides multiple layers of security to help protect systems.

______________________________________________________________________

# 2. Why Linux Security Matters

Imagine a publicly accessible Linux server.

Possible risks include:

- Weak passwords
- Exposed SSH service
- World-writable files
- Misconfigured firewall
- Outdated software
- Privilege escalation
- Malware

Good security practices significantly reduce the attack surface.

______________________________________________________________________

# 3. Security Layers in Linux

Linux security is based on defense in depth.

```
Application

↓

User Permissions

↓

File Permissions

↓

Firewall

↓

SSH Security

↓

Kernel Security

↓

Hardware
```

If one layer fails, additional layers continue to provide protection.

______________________________________________________________________

# 4. Authentication

Authentication answers:

```
Who are you?
```

Common authentication methods:

- Password
- SSH key
- Multi-factor authentication (MFA)
- Kerberos
- LDAP

Linux stores account information in:

```text
/etc/passwd
```

Password hashes:

```text
/etc/shadow
```

Only privileged users can read:

```text
/etc/shadow
```

______________________________________________________________________

# 5. Authorization

Authorization answers:

```
What are you allowed to do?
```

Linux determines access based on:

- User
- Group
- File permissions
- Access Control Lists (ACLs)
- Security policies (SELinux/AppArmor)

Example:

```
User

↓

Can Read

↓

Cannot Write
```

______________________________________________________________________

# 6. File Permissions Revisited

View permissions:

```bash
ls -l
```

Example:

```text
-rwxr-x---
```

Meaning:

```
Owner

↓

rwx

Group

↓

r-x

Others

↓

---
```

Permission values:

| Permission | Value |
|------------|-------|
| Read | 4 |
| Write | 2 |
| Execute | 1 |

Examples:

```bash
chmod 755 file
chmod 644 file
chmod 600 id_ed25519
```

Ownership:

```bash
chown user:group file
```

______________________________________________________________________

# Special Permission Bits

Setuid:

```bash
chmod u+s program
```

______________________________________________________________________

Setgid:

```bash
chmod g+s directory
```

______________________________________________________________________

Sticky Bit:

```bash
chmod +t directory
```

Example:

```text
/tmp
```

The sticky bit prevents users from deleting files owned by other users within a shared directory.

______________________________________________________________________

# 7. Sudo and Least Privilege

Avoid logging in as:

```text
root
```

Instead:

```bash
sudo command
```

Benefits:

- Audit trail
- Reduced accidental damage
- Better security

______________________________________________________________________

Sudo configuration:

```text
/etc/sudoers
```

Edit safely:

```bash
visudo
```

Never edit `/etc/sudoers` directly with a text editor.

______________________________________________________________________

# Principle of Least Privilege

Grant only the permissions required to perform a task.

Example:

A web server should not have unrestricted access to the entire filesystem.

______________________________________________________________________

# 8. Password Security

Change password:

```bash
passwd
```

______________________________________________________________________

Change another user's password:

```bash
sudo passwd username
```

______________________________________________________________________

Password aging:

```bash
chage -l username
```

______________________________________________________________________

Lock account:

```bash
sudo passwd -l username
```

______________________________________________________________________

Unlock account:

```bash
sudo passwd -u username
```

______________________________________________________________________

Strong password guidelines:

- Long
- Unique
- Random
- Password manager recommended

______________________________________________________________________

# 9. SSH Security

Disable root login:

```text
PermitRootLogin no
```

______________________________________________________________________

Disable password authentication:

```text
PasswordAuthentication no
```

______________________________________________________________________

Use SSH keys:

```bash
ssh-keygen -t ed25519
```

______________________________________________________________________

Restrict users:

```text
AllowUsers riyaz deploy
```

______________________________________________________________________

Restart SSH:

```bash
sudo systemctl restart ssh
```

______________________________________________________________________

# 10. Firewall Basics

A firewall controls incoming and outgoing network traffic.

Common Linux firewalls:

- UFW (Ubuntu)
- firewalld (RHEL/Fedora)
- iptables
- nftables

______________________________________________________________________

## UFW

Enable:

```bash
sudo ufw enable
```

______________________________________________________________________

Status:

```bash
sudo ufw status
```

______________________________________________________________________

Allow SSH:

```bash
sudo ufw allow ssh
```

______________________________________________________________________

Allow port:

```bash
sudo ufw allow 8080
```

______________________________________________________________________

Deny port:

```bash
sudo ufw deny 23
```

______________________________________________________________________

Delete rule:

```bash
sudo ufw delete allow 8080
```

______________________________________________________________________

## firewalld

Status:

```bash
sudo firewall-cmd --state
```

______________________________________________________________________

Allow HTTP:

```bash
sudo firewall-cmd --permanent --add-service=http
```

______________________________________________________________________

Reload:

```bash
sudo firewall-cmd --reload
```

______________________________________________________________________

# 11. SELinux and AppArmor

Traditional permissions are sometimes not enough.

Linux supports Mandatory Access Control (MAC).

______________________________________________________________________

## SELinux

Common on:

- RHEL
- CentOS
- Fedora

Check status:

```bash
getenforce
```

Possible output:

```text
Enforcing
Permissive
Disabled
```

______________________________________________________________________

Temporarily permissive:

```bash
sudo setenforce 0
```

______________________________________________________________________

## AppArmor

Common on:

- Ubuntu

Status:

```bash
sudo aa-status
```

AppArmor confines applications using security profiles.

______________________________________________________________________

# 12. File Integrity

Generate checksum:

```bash
sha256sum file.txt
```

______________________________________________________________________

Verify checksum:

```bash
sha256sum -c checksum.txt
```

______________________________________________________________________

Other algorithms:

```bash
md5sum
sha1sum
sha512sum
```

SHA-256 or stronger is generally recommended over MD5 or SHA-1 for integrity verification.

______________________________________________________________________

# 13. Process Security

View running processes:

```bash
ps aux
```

______________________________________________________________________

Open network ports:

```bash
ss -tulpn
```

______________________________________________________________________

Find listening services:

```bash
lsof -i
```

______________________________________________________________________

Terminate suspicious process:

```bash
kill PID
```

______________________________________________________________________

# 14. Security Auditing

Find world-writable files:

```bash
find / -perm -002
```

______________________________________________________________________

Find SUID files:

```bash
find / -perm -4000
```

______________________________________________________________________

Failed SSH logins:

```bash
grep "Failed password" /var/log/auth.log
```

or

```bash
journalctl -u ssh
```

depending on the distribution.

______________________________________________________________________

Installed updates:

```bash
apt list --upgradable
```

______________________________________________________________________

Check open ports:

```bash
ss -tulpn
```

______________________________________________________________________

# 15. Common Security Commands

User information:

```bash
id
whoami
groups
```

______________________________________________________________________

Permissions:

```bash
chmod
chown
chgrp
```

______________________________________________________________________

Hashes:

```bash
sha256sum
```

______________________________________________________________________

Firewall:

```bash
ufw
firewall-cmd
```

______________________________________________________________________

Authentication:

```bash
passwd
chage
```

______________________________________________________________________

# 16. Production Examples

## Check Open Ports

```bash
ss -tulpn
```

______________________________________________________________________

## Restrict SSH to Key Authentication

Edit:

```text
/etc/ssh/sshd_config
```

Set:

```text
PasswordAuthentication no
```

______________________________________________________________________

## Verify File Integrity

```bash
sha256sum app.tar.gz
```

______________________________________________________________________

## Allow HTTPS

```bash
sudo ufw allow 443
```

______________________________________________________________________

## Find SUID Files

```bash
find / -perm -4000
```

______________________________________________________________________

## Review Authentication Failures

```bash
journalctl -u ssh
```

______________________________________________________________________

# 17. Common Mistakes

❌ Logging in directly as `root`.

______________________________________________________________________

❌ Using weak or reused passwords.

______________________________________________________________________

❌ Disabling the firewall without understanding the consequences.

______________________________________________________________________

❌ Setting permissions to:

```bash
chmod 777
```

without necessity.

______________________________________________________________________

❌ Ignoring security updates.

______________________________________________________________________

❌ Storing private SSH keys in shared or unsecured locations.

______________________________________________________________________

# 18. Best Practices

- Follow the principle of least privilege.
- Use SSH keys instead of passwords.
- Keep packages updated.
- Enable and configure a firewall.
- Audit open ports and running services regularly.
- Use SHA-256 or stronger for integrity verification.
- Restrict file permissions to the minimum required.

______________________________________________________________________

# Interview Questions

## Q1. What is the difference between authentication and authorization?

**Answer**

Authentication verifies a user's identity, while authorization determines what actions or resources that authenticated
user is permitted to access.

______________________________________________________________________

## Q2. Why is `visudo` preferred over editing `/etc/sudoers` directly?

**Answer**

`visudo` performs syntax validation before saving changes, reducing the risk of configuration errors that could prevent
administrative access.

______________________________________________________________________

## Q3. What is the principle of least privilege?

**Answer**

The principle of least privilege states that users and applications should receive only the permissions necessary to
perform their required tasks and no more.

______________________________________________________________________

## Q4. What is the difference between SELinux and AppArmor?

**Answer**

Both provide Mandatory Access Control (MAC). SELinux uses label-based security policies and is common on RHEL-based
systems, while AppArmor uses path-based profiles and is common on Ubuntu-based systems.

______________________________________________________________________

## Q5. Why is `chmod 777` generally discouraged?

**Answer**

`chmod 777` grants read, write, and execute permissions to everyone, greatly increasing the risk of accidental
modification, privilege misuse, or unauthorized access.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Inspect:

- `/etc/passwd`
- `/etc/shadow` (with appropriate privileges)

and identify their purposes.

______________________________________________________________________

## Exercise 2

Modify file permissions using:

```bash
chmod
chown
```

and verify the results.

______________________________________________________________________

## Exercise 3

Configure a firewall rule allowing only SSH and HTTP.

______________________________________________________________________

## Exercise 4

Generate and verify a SHA-256 checksum for a file.

______________________________________________________________________

## Exercise 5

List:

- Open ports
- Running services
- Logged-in users

using appropriate Linux commands.

______________________________________________________________________

## Exercise 6

Find:

- World-writable files
- SUID files

on a test system or virtual machine.

______________________________________________________________________

# Cheat Sheet

## Authentication

```bash
passwd
chage
id
whoami
groups
```

______________________________________________________________________

## Permissions

```bash
chmod
chown
chgrp
```

______________________________________________________________________

## SSH

```bash
ssh-keygen
sshd_config
```

______________________________________________________________________

## Firewall

```bash
ufw
firewall-cmd
ss
```

______________________________________________________________________

## Security

```bash
sha256sum
getenforce
aa-status
find
journalctl
```

______________________________________________________________________

# Summary

In this chapter, you learned the core concepts of Linux security, including authentication, authorization, file
permissions, sudo, SSH hardening, firewalls, SELinux, AppArmor, file integrity verification, process security, and basic
security auditing techniques. These practices help protect Linux systems against unauthorized access and are essential
for administering production servers securely.

______________________________________________________________________

## Next

[Troubleshooting Linux Systems](23-troubleshooting-linux-systems.md)

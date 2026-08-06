# Linux Complete Interview & Production Course

# File 17 — SSH and Remote Administration

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Networking
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 16 — Linux Networking

______________________________________________________________________

# Table of Contents

1. Introduction
1. What is SSH?
1. Why SSH Matters
1. SSH Architecture
1. Installing OpenSSH
1. Starting and Managing the SSH Service
1. Connecting to a Remote Server
1. SSH Authentication
1. SSH Key-Based Authentication
1. Managing SSH Keys
1. The `ssh-agent`
1. Copying Files with `scp`
1. File Synchronization with `rsync`
1. SSH Configuration
1. SSH Port Forwarding
1. SSH Tunneling
1. SSH Security Best Practices
1. Production Examples
1. Common Mistakes
1. Interview Questions
1. Practice Exercises
1. Cheat Sheet
1. Summary
1. Next

______________________________________________________________________

# 1. Introduction

SSH (Secure Shell) is the standard protocol for securely accessing remote Linux systems.

Almost every backend engineer uses SSH daily to:

- Connect to cloud servers
- Deploy applications
- Restart services
- Inspect logs
- Copy files
- Debug production issues

If you've logged into an AWS EC2 instance, a DigitalOcean Droplet, or a Kubernetes node, you've almost certainly used
SSH.

______________________________________________________________________

# 2. What is SSH?

SSH (Secure Shell) is a cryptographic network protocol that provides secure remote access to systems over an untrusted
network.

It encrypts:

- Commands
- Passwords
- File transfers
- Authentication

Default port:

```text
22
```

Without SSH, sensitive information would travel across the network in plain text.

______________________________________________________________________

# 3. Why SSH Matters

Imagine a production FastAPI server running in AWS.

Instead of physically accessing the machine, you simply execute:

```bash
ssh ubuntu@34.201.10.25
```

You now have a secure terminal on the remote machine.

Common SSH tasks include:

- Deploying applications
- Restarting services
- Viewing logs
- Managing Docker containers
- Monitoring resources
- Updating packages

______________________________________________________________________

# 4. SSH Architecture

```
SSH Client

↓

Encrypted Connection

↓

SSH Server (sshd)

↓

Linux Server
```

The client initiates the connection, while the server authenticates the user and executes commands.

______________________________________________________________________

# 5. Installing OpenSSH

Ubuntu/Debian

Install SSH client:

```bash
sudo apt install openssh-client
```

Install SSH server:

```bash
sudo apt install openssh-server
```

______________________________________________________________________

CentOS/RHEL

```bash
sudo yum install openssh-server
```

or

```bash
sudo dnf install openssh-server
```

______________________________________________________________________

Verify installation:

```bash
ssh -V
```

______________________________________________________________________

# 6. Starting and Managing the SSH Service

Start:

```bash
sudo systemctl start ssh
```

______________________________________________________________________

Enable on boot:

```bash
sudo systemctl enable ssh
```

______________________________________________________________________

Restart:

```bash
sudo systemctl restart ssh
```

______________________________________________________________________

Status:

```bash
systemctl status ssh
```

______________________________________________________________________

# 7. Connecting to a Remote Server

Basic syntax:

```bash
ssh username@hostname
```

Example:

```bash
ssh ubuntu@192.168.1.100
```

______________________________________________________________________

Using an IP address:

```bash
ssh riyaz@10.0.0.15
```

______________________________________________________________________

Specify a custom port:

```bash
ssh -p 2222 ubuntu@example.com
```

______________________________________________________________________

Run a single remote command:

```bash
ssh ubuntu@server "df -h"
```

______________________________________________________________________

# 8. SSH Authentication

SSH supports multiple authentication methods.

## Password Authentication

The user enters a password after connecting.

Example:

```bash
ssh ubuntu@server
```

______________________________________________________________________

## Public Key Authentication

Recommended for production.

Authentication is performed using a public/private key pair.

Advantages:

- More secure
- No password required
- Resistant to brute-force attacks
- Commonly used in cloud environments

______________________________________________________________________

# 9. SSH Key-Based Authentication

Generate a key pair:

```bash
ssh-keygen
```

Default location:

```text
~/.ssh/
```

Generated files:

```text
id_rsa
```

Private key

```text
id_rsa.pub
```

Public key

______________________________________________________________________

Modern recommendation:

Generate an Ed25519 key:

```bash
ssh-keygen -t ed25519
```

______________________________________________________________________

Copy the public key to the server:

```bash
ssh-copy-id ubuntu@server
```

Or manually append it to:

```text
~/.ssh/authorized_keys
```

______________________________________________________________________

After this:

```bash
ssh ubuntu@server
```

No password is required if key authentication succeeds.

______________________________________________________________________

# 10. Managing SSH Keys

List keys:

```bash
ls ~/.ssh
```

______________________________________________________________________

Change permissions:

Private key:

```bash
chmod 600 ~/.ssh/id_ed25519
```

Public key:

```bash
chmod 644 ~/.ssh/id_ed25519.pub
```

SSH may reject private keys with insecure permissions.

______________________________________________________________________

# 11. The `ssh-agent`

`ssh-agent` stores decrypted private keys in memory.

Start the agent:

```bash
eval "$(ssh-agent -s)"
```

Add a key:

```bash
ssh-add ~/.ssh/id_ed25519
```

List loaded keys:

```bash
ssh-add -l
```

This prevents repeatedly entering the passphrase for encrypted private keys.

______________________________________________________________________

# 12. Copying Files with `scp`

Copy a local file to a remote server:

```bash
scp file.txt ubuntu@server:/home/ubuntu/
```

______________________________________________________________________

Copy a remote file to the local machine:

```bash
scp ubuntu@server:/var/log/nginx/access.log .
```

______________________________________________________________________

Copy a directory:

```bash
scp -r project ubuntu@server:/home/ubuntu/
```

______________________________________________________________________

Specify a custom port:

```bash
scp -P 2222 file.txt ubuntu@server:/tmp/
```

______________________________________________________________________

# 13. File Synchronization with `rsync`

`rsync` efficiently synchronizes files and directories.

Copy a directory:

```bash
rsync -av project/ ubuntu@server:/home/ubuntu/project/
```

______________________________________________________________________

Synchronize only changed files.

______________________________________________________________________

Show progress:

```bash
rsync -av --progress project/ ubuntu@server:/home/ubuntu/project/
```

______________________________________________________________________

Delete remote files that no longer exist locally:

```bash
rsync -av --delete project/ ubuntu@server:/home/ubuntu/project/
```

Use `--delete` carefully.

______________________________________________________________________

# 14. SSH Configuration

SSH client configuration file:

```text
~/.ssh/config
```

Example:

```text
Host production
    HostName 34.201.10.25
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
    Port 22
```

Now connect using:

```bash
ssh production
```

______________________________________________________________________

SSH server configuration:

```text
/etc/ssh/sshd_config
```

Common settings:

```text
PermitRootLogin no
PasswordAuthentication no
Port 22
```

Restart SSH after modifying server configuration:

```bash
sudo systemctl restart ssh
```

______________________________________________________________________

# 15. SSH Port Forwarding

Port forwarding securely tunnels traffic through an SSH connection.

Local forwarding:

```bash
ssh -L 8080:localhost:80 ubuntu@server
```

Now:

```text
localhost:8080
```

forwards traffic to:

```text
server:80
```

Useful for accessing internal web applications securely.

______________________________________________________________________

# 16. SSH Tunneling

Remote forwarding:

```bash
ssh -R 9000:localhost:5000 ubuntu@server
```

______________________________________________________________________

Dynamic SOCKS proxy:

```bash
ssh -D 1080 ubuntu@server
```

This creates a SOCKS proxy that can securely route application traffic through the remote server.

______________________________________________________________________

# 17. SSH Security Best Practices

- Prefer SSH keys over passwords.
- Disable root login.
- Disable password authentication when possible.
- Use strong passphrases for private keys.
- Restrict access using firewalls or security groups.
- Rotate keys periodically.
- Keep OpenSSH updated.

______________________________________________________________________

# 18. Production Examples

## Connect to an EC2 Instance

```bash
ssh -i my-key.pem ubuntu@ec2-public-ip
```

______________________________________________________________________

## Copy Application Logs

```bash
scp ubuntu@server:/var/log/app.log .
```

______________________________________________________________________

## Deploy Application Code

```bash
rsync -av --progress app/ ubuntu@server:/opt/app/
```

______________________________________________________________________

## Restart a Service

```bash
ssh production "sudo systemctl restart nginx"
```

______________________________________________________________________

## View Disk Usage

```bash
ssh production "df -h"
```

______________________________________________________________________

## Access an Internal Database UI

```bash
ssh -L 5432:localhost:5432 production
```

______________________________________________________________________

# 19. Common Mistakes

❌ Logging in directly as `root`.

______________________________________________________________________

❌ Storing private keys in shared locations.

______________________________________________________________________

❌ Forgetting to set correct permissions on private keys.

______________________________________________________________________

❌ Using passwords instead of SSH keys in production.

______________________________________________________________________

❌ Leaving unused public keys in `authorized_keys`.

______________________________________________________________________

❌ Using `scp` for large repeated transfers instead of `rsync`.

______________________________________________________________________

# 20. Interview Questions

## Q1. Why is SSH considered secure?

**Answer**

SSH encrypts all communication between the client and server, including authentication credentials and transmitted data,
protecting against eavesdropping and man-in-the-middle attacks.

______________________________________________________________________

## Q2. What is the difference between a public key and a private key?

**Answer**

The private key remains on the client and must never be shared. The public key is copied to the remote server and is
used to verify the client's identity during authentication.

______________________________________________________________________

## Q3. When would you use `rsync` instead of `scp`?

**Answer**

`rsync` is preferred for synchronizing directories because it transfers only changed files or changed portions of files,
reducing bandwidth usage and improving performance.

______________________________________________________________________

## Q4. What is SSH port forwarding?

**Answer**

SSH port forwarding securely tunnels traffic from one network endpoint to another through an encrypted SSH connection,
allowing access to services that are not directly exposed.

______________________________________________________________________

## Q5. Why should password authentication be disabled in production?

**Answer**

Password authentication is more vulnerable to brute-force attacks. Key-based authentication provides stronger security
and is the recommended approach for production servers.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Generate an SSH key pair using:

```bash
ssh-keygen -t ed25519
```

______________________________________________________________________

## Exercise 2

Connect to a remote Linux machine using SSH.

______________________________________________________________________

## Exercise 3

Copy a file using:

```bash
scp
```

______________________________________________________________________

## Exercise 4

Synchronize a directory using:

```bash
rsync
```

______________________________________________________________________

## Exercise 5

Create an SSH client configuration entry in:

```text
~/.ssh/config
```

and connect using the configured host alias.

______________________________________________________________________

## Exercise 6

Configure local port forwarding to access a web service running on a remote machine.

______________________________________________________________________

# Cheat Sheet

## SSH

```bash
ssh
ssh -p
ssh -i
```

______________________________________________________________________

## SSH Keys

```bash
ssh-keygen
ssh-copy-id
ssh-add
ssh-agent
```

______________________________________________________________________

## File Transfer

```bash
scp
scp -r
rsync
```

______________________________________________________________________

## Configuration

```text
~/.ssh/config
/etc/ssh/sshd_config
```

______________________________________________________________________

## Port Forwarding

```bash
ssh -L
ssh -R
ssh -D
```

______________________________________________________________________

# Summary

In this chapter, you learned how SSH provides secure remote access to Linux systems, how SSH authentication and
key-based login work, how to transfer files using `scp` and `rsync`, how to configure SSH clients and servers, and how
to use SSH port forwarding and tunneling. These are essential skills for managing cloud infrastructure, deploying
applications, and securely administering production servers.

______________________________________________________________________

## Next

[Disk Management and Filesystems](18-disk-management-and-filesystems.md)

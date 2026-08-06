# Linux Complete Interview & Production Course

# File 24 — Linux Interview Scenarios and Cheat Sheet

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Interview Preparation
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 23 — Troubleshooting Linux Systems

______________________________________________________________________

# Table of Contents

1. Introduction
1. Linux Interview Strategy
1. Frequently Asked Linux Interview Questions
1. Scenario-Based Interview Questions
1. Senior Backend Interview Questions
1. DevOps Interview Questions
1. Rapid-Fire Linux Questions
1. Linux Command Cheat Sheet
1. File Permissions Cheat Sheet
1. Process Management Cheat Sheet
1. Networking Cheat Sheet
1. Package Management Cheat Sheet
1. Disk Management Cheat Sheet
1. Service Management Cheat Sheet
1. Troubleshooting Cheat Sheet
1. 30-Minute Linux Revision Plan
1. Final Tips
1. Summary

______________________________________________________________________

# 1. Introduction

This chapter is designed as a **last-minute revision guide** before an interview.

It consolidates the most important Linux concepts, commands, and troubleshooting techniques covered throughout the
course.

Use it to quickly refresh your knowledge before technical interviews or production support tasks.

______________________________________________________________________

# 2. Linux Interview Strategy

When answering Linux questions:

1. Explain the concept briefly.
1. Explain why it exists.
1. Mention where it is used.
1. Give a practical command.
1. Mention one production example.

Example:

**Question:** What is `systemctl`?

**Answer**

`systemctl` is the command-line interface for managing services controlled by systemd. It is used to start, stop,
restart, enable, disable, and inspect services. For example:

```bash
sudo systemctl restart nginx
```

This command is commonly used after changing an Nginx configuration.

______________________________________________________________________

# 3. Frequently Asked Linux Interview Questions

## Q1. What is Linux?

**Answer**

Linux is an open-source Unix-like operating system kernel. Linux distributions combine the kernel with system utilities
and software to provide a complete operating system used in servers, cloud infrastructure, embedded systems, and
desktops.

______________________________________________________________________

## Q2. What is the Linux Kernel?

**Answer**

The kernel is the core component of the operating system. It manages CPU scheduling, memory, devices, filesystems,
networking, and communication between hardware and software.

______________________________________________________________________

## Q3. What is the difference between a process and a thread?

**Answer**

A process has its own memory space and system resources. Threads are lightweight execution units within a process that
share the same memory and resources.

______________________________________________________________________

## Q4. What is a daemon?

**Answer**

A daemon is a long-running background process that provides services such as SSH, web serving, logging, or scheduling.

______________________________________________________________________

## Q5. What is the difference between `kill` and `kill -9`?

**Answer**

`kill` sends `SIGTERM`, allowing a process to exit gracefully. `kill -9` sends `SIGKILL`, immediately terminating the
process without allowing cleanup.

______________________________________________________________________

## Q6. What is a symbolic link?

**Answer**

A symbolic link is a special file that points to another file or directory. It acts like a shortcut and can reference
files across different filesystems.

______________________________________________________________________

## Q7. What is the difference between a hard link and a symbolic link?

**Answer**

A hard link references the same inode as the original file and cannot span filesystems. A symbolic link references the
file path and can span filesystems but becomes broken if the target is removed.

______________________________________________________________________

## Q8. What is the difference between `df` and `du`?

**Answer**

`df` reports filesystem usage, while `du` reports the size of files and directories.

______________________________________________________________________

## Q9. What is swap?

**Answer**

Swap is disk space used as virtual memory when physical RAM is exhausted.

______________________________________________________________________

## Q10. What is the purpose of `journalctl`?

**Answer**

`journalctl` provides access to logs stored by `systemd-journald`, allowing logs to be filtered by service, priority,
time, and boot session.

______________________________________________________________________

# 4. Scenario-Based Interview Questions

## Scenario 1

### CPU Usage Suddenly Reaches 100%

How would you investigate?

**Answer**

1. Check CPU usage:

```bash
top
```

2. Identify the highest CPU-consuming process:

```bash
ps aux --sort=-%cpu
```

3. Inspect application logs.

1. Determine whether the process is expected or malfunctioning.

1. Restart or terminate the process only after identifying the root cause.

______________________________________________________________________

## Scenario 2

### Disk is 100% Full

**Answer**

Check filesystem usage:

```bash
df -h
```

Find large directories:

```bash
du -sh *
```

Check deleted files still held open:

```bash
lsof +L1
```

Investigate logs, backups, Docker images, and temporary files before deleting data.

______________________________________________________________________

## Scenario 3

### Website Returns HTTP 502

**Answer**

Check:

```bash
systemctl status nginx
systemctl status myapp
journalctl -u nginx
ss -tulpn
```

Verify:

- Backend application is running.
- Nginx configuration is valid.
- Backend port is listening.
- Logs show no upstream errors.

______________________________________________________________________

## Scenario 4

### Unable to SSH into a Server

**Answer**

Check:

- SSH service status.
- Firewall rules.
- Network connectivity.
- SSH configuration.
- Authorized keys.
- User permissions.

Useful commands:

```bash
systemctl status ssh
ss -tulpn
journalctl -u ssh
```

______________________________________________________________________

## Scenario 5

### Application Cannot Connect to Database

**Answer**

Verify:

- Database service is running.
- Database port is listening.
- DNS resolves correctly.
- Firewall permits traffic.
- Credentials and connection string are correct.

______________________________________________________________________

# 5. Senior Backend Interview Questions

## Q1. How would you investigate a production outage?

**Answer**

Gather logs and metrics, verify the health of services and infrastructure, inspect recent deployments or configuration
changes, identify the root cause using evidence, apply the smallest safe fix, verify recovery, and continue monitoring.

______________________________________________________________________

## Q2. Why is `SIGTERM` preferred over `SIGKILL`?

**Answer**

`SIGTERM` allows applications to close files, release resources, flush buffers, and exit gracefully. `SIGKILL`
immediately terminates the process and should be used only when graceful termination fails.

______________________________________________________________________

## Q3. What information would you collect before restarting a failed service?

**Answer**

Service status, logs, resource utilization, recent configuration changes, dependency health, and any recent deployments
or updates.

______________________________________________________________________

## Q4. How would you identify which process is using port 8080?

**Answer**

```bash
ss -tulpn | grep 8080
```

or

```bash
lsof -i :8080
```

______________________________________________________________________

## Q5. Why is Linux widely used for backend systems?

**Answer**

Linux offers stability, security, performance, strong networking, excellent automation capabilities, open-source
tooling, and broad cloud support, making it ideal for servers and backend infrastructure.

______________________________________________________________________

# 6. DevOps Interview Questions

## Q1. How do you monitor Linux services?

**Answer**

Using:

```bash
systemctl
journalctl
top
htop
ss
```

and monitoring systems such as Prometheus or Grafana in production environments.

______________________________________________________________________

## Q2. How do you automate recurring maintenance tasks?

**Answer**

Using:

```bash
cron
```

or, on some modern systems, systemd timers.

______________________________________________________________________

## Q3. How do you investigate high memory usage?

**Answer**

Use:

```bash
free -h
ps aux --sort=-%mem
vmstat
```

and inspect application logs for memory leaks or abnormal behavior.

______________________________________________________________________

## Q4. How do you verify that a firewall is blocking traffic?

**Answer**

Inspect firewall rules using:

```bash
ufw status
```

or

```bash
firewall-cmd --list-all
```

and confirm whether the required ports are open.

______________________________________________________________________

## Q5. Why are logs important in production?

**Answer**

Logs provide historical records of system and application events, helping engineers diagnose failures, identify trends,
and verify the effectiveness of fixes.

______________________________________________________________________

# 7. Rapid-Fire Linux Questions

| Question | Short Answer |
|----------|--------------|
| Kernel PID | 1 is `systemd` (on most modern systems) |
| SSH Port | 22 |
| HTTP Port | 80 |
| HTTPS Port | 443 |
| DNS Port | 53 |
| View Processes | `ps`, `top`, `htop` |
| View Memory | `free -h` |
| View Disk Usage | `df -h` |
| View Directory Size | `du -sh` |
| View Network Interfaces | `ip addr` |
| View Open Ports | `ss -tulpn` |
| Restart Service | `systemctl restart` |
| View Logs | `journalctl` |
| Edit Crontab | `crontab -e` |
| Search Text | `grep` |

______________________________________________________________________

# 8. Linux Command Cheat Sheet

## Files

```bash
ls
pwd
cd
cp
mv
rm
mkdir
touch
find
locate
```

______________________________________________________________________

## Text Processing

```bash
grep
cut
tr
sort
uniq
sed
awk
xargs
```

______________________________________________________________________

## Processes

```bash
ps
top
htop
kill
killall
pgrep
jobs
fg
bg
```

______________________________________________________________________

## Networking

```bash
ip
ping
curl
wget
dig
host
ss
```

______________________________________________________________________

## Services

```bash
systemctl
journalctl
```

______________________________________________________________________

## Storage

```bash
df
du
lsblk
mount
umount
blkid
```

______________________________________________________________________

## Scheduling

```bash
cron
at
batch
```

______________________________________________________________________

## Security

```bash
chmod
chown
passwd
ufw
sha256sum
```

______________________________________________________________________

# 9. File Permissions Cheat Sheet

| Permission | Numeric |
|------------|---------|
| rwx | 7 |
| rw- | 6 |
| r-x | 5 |
| r-- | 4 |
| -wx | 3 |
| -w- | 2 |
| --x | 1 |
| --- | 0 |

Common values:

```bash
755
644
600
700
```

______________________________________________________________________

# 10. Process Management Cheat Sheet

```bash
ps aux
top
htop
kill PID
kill -9 PID
pgrep
pidof
jobs
fg
bg
```

______________________________________________________________________

# 11. Networking Cheat Sheet

```bash
ip addr
ip route
ping
curl
dig
host
ss -tulpn
```

______________________________________________________________________

# 12. Package Management Cheat Sheet

Ubuntu:

```bash
apt update
apt upgrade
apt install
apt remove
```

RHEL/Fedora:

```bash
dnf install
dnf update
dnf remove
```

______________________________________________________________________

# 13. Disk Management Cheat Sheet

```bash
df -h
du -sh
lsblk
blkid
mount
umount
```

______________________________________________________________________

# 14. Service Management Cheat Sheet

```bash
systemctl status
systemctl start
systemctl stop
systemctl restart
systemctl enable
journalctl -u
```

______________________________________________________________________

# 15. Troubleshooting Cheat Sheet

High CPU:

```bash
top
ps aux --sort=-%cpu
```

______________________________________________________________________

High Memory:

```bash
free -h
ps aux --sort=-%mem
```

______________________________________________________________________

Disk Full:

```bash
df -h
du -sh *
lsof +L1
```

______________________________________________________________________

Network Issues:

```bash
ip addr
ping
dig
curl
ss
```

______________________________________________________________________

Logs:

```bash
journalctl
tail -F
dmesg
```

______________________________________________________________________

# 16. 30-Minute Linux Revision Plan

### Minutes 1–5

Review:

- Linux architecture
- Filesystem hierarchy
- Users and permissions

______________________________________________________________________

### Minutes 6–10

Review:

- Process management
- Signals
- Services
- systemd

______________________________________________________________________

### Minutes 11–15

Review:

- Networking
- SSH
- DNS
- `curl`
- `ss`

______________________________________________________________________

### Minutes 16–20

Review:

- Disk management
- Package management
- Cron

______________________________________________________________________

### Minutes 21–25

Review:

- Logs
- Security
- Troubleshooting

______________________________________________________________________

### Minutes 26–30

Practice:

- Top 20 Linux commands
- Scenario-based questions
- Production troubleshooting workflow

______________________________________________________________________

# 17. Final Tips

- Understand concepts before memorizing commands.
- Practice commands on a Linux virtual machine or cloud instance.
- Read error messages carefully—they often point directly to the issue.
- Develop a habit of checking logs before making changes.
- Build muscle memory for commonly used commands.
- Explain not only **what** a command does, but **why** and **when** you would use it in production.

______________________________________________________________________

# Summary

Congratulations! You have completed the **Linux Complete Interview & Production Course**.

Across these 24 files, you covered:

- Linux fundamentals
- Filesystem and permissions
- Users and groups
- Shell scripting
- Text processing
- Regular expressions
- Process management
- systemd and services
- Networking
- SSH
- Disk management
- Package management
- Scheduling
- Logging and monitoring
- Security
- Troubleshooting
- Interview-focused scenarios and command cheat sheets

You now have a strong foundation for Linux administration, backend development, DevOps workflows, and technical
interviews. Continue practicing these commands in real environments to reinforce your understanding and build
confidence.

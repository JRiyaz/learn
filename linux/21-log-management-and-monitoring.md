# Linux Complete Interview & Production Course

# File 21 — Log Management and Monitoring

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Monitoring & Troubleshooting
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 20 — Scheduling Tasks with Cron and At

______________________________________________________________________

# Table of Contents

1. Introduction
1. Why Logs Matter
1. What is a Log?
1. Linux Log Locations
1. System Logging Architecture
1. The `journalctl` Command
1. Traditional Log Files
1. The `tail` Command
1. The `head` Command
1. The `less` Command
1. The `dmesg` Command
1. The `logrotate` Utility
1. Monitoring System Resources
1. Useful Monitoring Commands
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

Every Linux system continuously generates logs.

Logs record:

- System events
- Application activity
- Authentication attempts
- Errors
- Warnings
- Performance information

When something fails in production, logs are usually the **first place** engineers investigate.

Understanding logs is one of the most valuable troubleshooting skills for backend engineers.

______________________________________________________________________

# 2. Why Logs Matter

Suppose your API suddenly starts returning:

```
HTTP 500
```

Possible causes include:

- Database connection failure
- Out of memory
- Disk full
- Configuration error
- Permission issue

Logs provide the evidence needed to identify the actual cause.

______________________________________________________________________

# 3. What is a Log?

A log is a chronological record of events.

Example:

```text
2026-08-01 10:15:42 INFO Server started
2026-08-01 10:16:03 INFO User login
2026-08-01 10:17:11 ERROR Database timeout
```

Logs generally include:

- Timestamp
- Severity
- Component
- Message

______________________________________________________________________

# Common Log Levels

| Level | Meaning |
|---------|----------|
| DEBUG | Detailed diagnostic information |
| INFO | Normal application events |
| WARNING | Potential issues |
| ERROR | Operation failed |
| CRITICAL | Severe failure |

______________________________________________________________________

# 4. Linux Log Locations

Most log files are stored under:

```text
/var/log
```

Examples:

| File | Purpose |
|------|----------|
| /var/log/syslog | General system logs (Ubuntu) |
| /var/log/messages | General system logs (RHEL) |
| /var/log/auth.log | Authentication logs |
| /var/log/kern.log | Kernel logs |
| /var/log/dpkg.log | Package installation history |
| /var/log/nginx/ | Nginx logs |
| /var/log/apache2/ | Apache logs |

______________________________________________________________________

View available logs:

```bash
ls /var/log
```

______________________________________________________________________

# 5. System Logging Architecture

Modern Linux systems often use:

```
Applications

↓

systemd-journald

↓

Journal

↓

journalctl
```

Some systems also forward logs to:

```
rsyslog

↓

Log Files

↓

/var/log
```

Applications may additionally write their own dedicated log files.

______________________________________________________________________

# 6. The `journalctl` Command

Display all journal entries:

```bash
journalctl
```

______________________________________________________________________

Latest 100 lines:

```bash
journalctl -n 100
```

______________________________________________________________________

Follow logs in real time:

```bash
journalctl -f
```

______________________________________________________________________

Current boot:

```bash
journalctl -b
```

______________________________________________________________________

Previous boot:

```bash
journalctl -b -1
```

______________________________________________________________________

Logs for a service:

```bash
journalctl -u nginx
```

______________________________________________________________________

Follow service logs:

```bash
journalctl -fu nginx
```

______________________________________________________________________

Logs since today:

```bash
journalctl --since today
```

______________________________________________________________________

Logs from the last hour:

```bash
journalctl --since "1 hour ago"
```

______________________________________________________________________

Error-level logs:

```bash
journalctl -p err
```

______________________________________________________________________

# 7. Traditional Log Files

View a log:

```bash
cat /var/log/syslog
```

______________________________________________________________________

Search logs:

```bash
grep ERROR /var/log/syslog
```

______________________________________________________________________

Count failures:

```bash
grep -c ERROR app.log
```

______________________________________________________________________

Search authentication failures:

```bash
grep "Failed password" /var/log/auth.log
```

______________________________________________________________________

# 8. The `tail` Command

Display the end of a file.

```bash
tail app.log
```

______________________________________________________________________

Last 50 lines:

```bash
tail -50 app.log
```

______________________________________________________________________

Follow new entries:

```bash
tail -f app.log
```

______________________________________________________________________

Follow and retry after log rotation:

```bash
tail -F app.log
```

`-F` is generally preferred for long-running monitoring.

______________________________________________________________________

# 9. The `head` Command

Display the beginning of a file.

```bash
head app.log
```

______________________________________________________________________

First 20 lines:

```bash
head -20 app.log
```

Useful for checking log headers or configuration files.

______________________________________________________________________

# 10. The `less` Command

Read large files efficiently.

```bash
less app.log
```

Navigation:

| Key | Action |
|------|---------|
| Space | Next page |
| b | Previous page |
| / | Search |
| n | Next match |
| q | Quit |

Unlike `cat`, `less` does not load the entire file into the terminal.

______________________________________________________________________

# 11. The `dmesg` Command

Display kernel messages.

```bash
dmesg
```

______________________________________________________________________

Human-readable timestamps:

```bash
dmesg -T
```

______________________________________________________________________

Search for USB events:

```bash
dmesg | grep USB
```

______________________________________________________________________

Search for disk errors:

```bash
dmesg | grep error
```

Useful for diagnosing:

- Hardware issues
- Driver problems
- Boot messages

______________________________________________________________________

# 12. The `logrotate` Utility

Log files grow continuously.

Without maintenance:

```
Disk

↓

Logs

↓

Disk Full
```

`logrotate` automatically:

- Rotates logs
- Compresses old logs
- Deletes old archives
- Creates new log files

______________________________________________________________________

Configuration:

```text
/etc/logrotate.conf
```

Additional rules:

```text
/etc/logrotate.d/
```

______________________________________________________________________

Test configuration:

```bash
sudo logrotate -d /etc/logrotate.conf
```

______________________________________________________________________

Force rotation:

```bash
sudo logrotate -f /etc/logrotate.conf
```

______________________________________________________________________

# 13. Monitoring System Resources

Memory:

```bash
free -h
```

______________________________________________________________________

Disk:

```bash
df -h
```

______________________________________________________________________

CPU and processes:

```bash
top
```

or

```bash
htop
```

______________________________________________________________________

Uptime and load:

```bash
uptime
```

______________________________________________________________________

Running processes:

```bash
ps aux
```

______________________________________________________________________

Network sockets:

```bash
ss -tulpn
```

______________________________________________________________________

# 14. Useful Monitoring Commands

Memory:

```bash
vmstat
```

______________________________________________________________________

I/O statistics:

```bash
iostat
```

(available via the `sysstat` package)

______________________________________________________________________

CPU statistics:

```bash
mpstat
```

______________________________________________________________________

Process statistics:

```bash
pidstat
```

______________________________________________________________________

Real-time disk usage:

```bash
watch df -h
```

______________________________________________________________________

Real-time memory usage:

```bash
watch free -h
```

______________________________________________________________________

# 15. Production Examples

## Monitor Nginx Logs

```bash
tail -F /var/log/nginx/access.log
```

______________________________________________________________________

## Monitor FastAPI Logs

```bash
journalctl -fu myapp
```

______________________________________________________________________

## Find Failed SSH Logins

```bash
grep "Failed password" /var/log/auth.log
```

______________________________________________________________________

## Check Available Disk Space

```bash
df -h
```

______________________________________________________________________

## Monitor CPU Usage

```bash
htop
```

______________________________________________________________________

## Check Kernel Messages

```bash
dmesg -T
```

______________________________________________________________________

## Rotate Logs Immediately

```bash
sudo logrotate -f /etc/logrotate.conf
```

______________________________________________________________________

# 16. Common Mistakes

❌ Using `cat` to open multi-gigabyte log files.

______________________________________________________________________

❌ Ignoring log rotation, allowing logs to consume all available disk space.

______________________________________________________________________

❌ Looking only at application logs and forgetting system logs.

______________________________________________________________________

❌ Assuming every error is logged at the `ERROR` level.

______________________________________________________________________

❌ Following rotated log files with `tail -f` instead of `tail -F`.

______________________________________________________________________

# 17. Best Practices

- Use `journalctl` on systemd-based systems.
- Use `tail -F` for continuous log monitoring.
- Rotate logs regularly.
- Centralize application logs when possible.
- Monitor disk usage to prevent log files from filling the filesystem.
- Search logs with `grep` rather than reading entire files manually.

______________________________________________________________________

# Interview Questions

## Q1. Where are Linux logs typically stored?

**Answer**

Traditional log files are usually stored under `/var/log`. On modern Linux systems using systemd, logs are also stored
in the system journal and accessed using `journalctl`.

______________________________________________________________________

## Q2. What is the difference between `tail -f` and `tail -F`?

**Answer**

`tail -f` follows an open file descriptor. If the log file is rotated or recreated, it may stop following new data.
`tail -F` follows the filename and automatically reconnects after log rotation, making it more suitable for production
monitoring.

______________________________________________________________________

## Q3. What is `logrotate`?

**Answer**

`logrotate` is a utility that automatically rotates, compresses, archives, and removes old log files to prevent them
from consuming excessive disk space.

______________________________________________________________________

## Q4. When would you use `dmesg`?

**Answer**

`dmesg` is used to inspect kernel messages related to hardware detection, drivers, boot events, and low-level system
errors.

______________________________________________________________________

## Q5. Why is `journalctl` preferred on modern Linux systems?

**Answer**

`journalctl` provides centralized access to structured logs collected by `systemd-journald`, allowing filtering by
service, boot session, priority, and time without searching multiple log files.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Display:

- System journal
- Current boot logs
- Previous boot logs

______________________________________________________________________

## Exercise 2

Monitor a log file using:

```bash
tail -F
```

______________________________________________________________________

## Exercise 3

Search for:

- ERROR
- WARNING
- Failed password

in available log files.

______________________________________________________________________

## Exercise 4

View kernel messages and identify:

- Boot information
- USB devices
- Network interfaces

______________________________________________________________________

## Exercise 5

Check:

- Memory usage
- Disk usage
- CPU usage
- Network sockets

using the appropriate monitoring commands.

______________________________________________________________________

## Exercise 6

Inspect your system's log rotation configuration.

______________________________________________________________________

# Cheat Sheet

## Logs

```bash
journalctl
journalctl -u
journalctl -f
journalctl -b
```

______________________________________________________________________

## Files

```bash
tail
tail -F
head
less
cat
```

______________________________________________________________________

## Kernel

```bash
dmesg
dmesg -T
```

______________________________________________________________________

## Monitoring

```bash
top
htop
free
df
uptime
vmstat
iostat
pidstat
ss
```

______________________________________________________________________

## Log Rotation

```bash
logrotate
```

______________________________________________________________________

# Summary

In this chapter, you learned how Linux systems generate, store, and manage logs using traditional log files and the
systemd journal. You explored `journalctl`, `tail`, `head`, `less`, `dmesg`, `logrotate`, and essential monitoring
commands for CPU, memory, disk, and network resources. These tools form the foundation of troubleshooting and
observability in production Linux environments.

______________________________________________________________________

## Next

[Linux Security](22-linux-security.md)

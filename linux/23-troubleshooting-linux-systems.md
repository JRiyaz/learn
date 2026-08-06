# Linux Complete Interview & Production Course

# File 23 — Troubleshooting Linux Systems

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Troubleshooting
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 22 — Linux Security

______________________________________________________________________

# Table of Contents

1. Introduction
1. Troubleshooting Methodology
1. Collecting System Information
1. Diagnosing CPU Issues
1. Diagnosing Memory Issues
1. Diagnosing Disk Issues
1. Diagnosing Network Issues
1. Diagnosing Service Failures
1. Diagnosing Permission Problems
1. Diagnosing High Load
1. Diagnosing Boot Problems
1. Diagnosing Application Crashes
1. Useful Diagnostic Commands
1. Production Troubleshooting Scenarios
1. Common Mistakes
1. Best Practices
1. Interview Questions
1. Practice Exercises
1. Cheat Sheet
1. Summary
1. Next

______________________________________________________________________

# 1. Introduction

Troubleshooting is one of the most valuable skills for a backend engineer.

In production, your responsibility is rarely limited to writing code. You may also need to investigate why an
application is slow, why a deployment failed, or why a service has become unavailable.

Effective troubleshooting requires a structured approach rather than guessing.

______________________________________________________________________

# 2. Troubleshooting Methodology

A recommended workflow is:

```
Observe

↓

Collect Information

↓

Identify the Root Cause

↓

Apply a Fix

↓

Verify the Fix

↓

Monitor
```

Avoid making multiple changes simultaneously. Change one variable at a time and verify the outcome.

______________________________________________________________________

# 3. Collecting System Information

Operating system:

```bash
uname -a
```

______________________________________________________________________

Distribution information:

```bash
cat /etc/os-release
```

______________________________________________________________________

Kernel version:

```bash
uname -r
```

______________________________________________________________________

Hostname:

```bash
hostname
```

______________________________________________________________________

Current user:

```bash
whoami
```

______________________________________________________________________

System uptime:

```bash
uptime
```

______________________________________________________________________

Logged-in users:

```bash
who
```

______________________________________________________________________

# 4. Diagnosing CPU Issues

Check CPU usage:

```bash
top
```

or

```bash
htop
```

______________________________________________________________________

Display processes sorted by CPU usage:

```bash
ps aux --sort=-%cpu
```

______________________________________________________________________

Check CPU information:

```bash
lscpu
```

______________________________________________________________________

Identify runaway processes consuming excessive CPU.

______________________________________________________________________

# 5. Diagnosing Memory Issues

Memory usage:

```bash
free -h
```

______________________________________________________________________

Memory statistics:

```bash
vmstat
```

______________________________________________________________________

Processes using the most memory:

```bash
ps aux --sort=-%mem
```

______________________________________________________________________

Check swap usage:

```bash
swapon --show
```

______________________________________________________________________

Out-of-memory events:

```bash
dmesg | grep -i oom
```

______________________________________________________________________

# 6. Diagnosing Disk Issues

Filesystem usage:

```bash
df -h
```

______________________________________________________________________

Directory sizes:

```bash
du -sh *
```

______________________________________________________________________

Disk devices:

```bash
lsblk
```

______________________________________________________________________

Filesystem errors (where applicable):

```bash
dmesg | grep -i disk
```

______________________________________________________________________

Search for deleted files still held open:

```bash
lsof +L1
```

Useful when disk space is unexpectedly full.

______________________________________________________________________

# 7. Diagnosing Network Issues

Display IP addresses:

```bash
ip addr
```

______________________________________________________________________

Routing table:

```bash
ip route
```

______________________________________________________________________

Connectivity test:

```bash
ping google.com
```

______________________________________________________________________

DNS lookup:

```bash
dig google.com
```

______________________________________________________________________

Open ports:

```bash
ss -tulpn
```

______________________________________________________________________

Test HTTP endpoint:

```bash
curl -I https://example.com
```

______________________________________________________________________

# 8. Diagnosing Service Failures

Service status:

```bash
systemctl status nginx
```

______________________________________________________________________

Service logs:

```bash
journalctl -u nginx
```

______________________________________________________________________

Failed services:

```bash
systemctl --failed
```

______________________________________________________________________

Restart:

```bash
sudo systemctl restart nginx
```

Verify the service status after restarting.

______________________________________________________________________

# 9. Diagnosing Permission Problems

Current user:

```bash
whoami
```

______________________________________________________________________

User information:

```bash
id
```

______________________________________________________________________

File permissions:

```bash
ls -l
```

______________________________________________________________________

Directory permissions:

```bash
namei -l /path/to/file
```

This command helps identify permission issues at each directory level.

______________________________________________________________________

# 10. Diagnosing High Load

Current load:

```bash
uptime
```

Example:

```text
load average: 0.20 0.18 0.10
```

High load may indicate:

- CPU-intensive processes
- Disk I/O bottlenecks
- Processes waiting on resources

______________________________________________________________________

Check CPU:

```bash
top
```

______________________________________________________________________

Check disk activity:

```bash
iostat
```

______________________________________________________________________

Check memory:

```bash
free -h
```

______________________________________________________________________

# 11. Diagnosing Boot Problems

Current boot logs:

```bash
journalctl -b
```

______________________________________________________________________

Previous boot:

```bash
journalctl -b -1
```

______________________________________________________________________

Kernel messages:

```bash
dmesg -T
```

______________________________________________________________________

Failed units:

```bash
systemctl --failed
```

______________________________________________________________________

# 12. Diagnosing Application Crashes

View application logs:

```bash
journalctl -u myapp
```

______________________________________________________________________

Search for exceptions:

```bash
grep ERROR app.log
```

______________________________________________________________________

Monitor logs in real time:

```bash
tail -F app.log
```

______________________________________________________________________

Verify configuration files before restarting services whenever possible.

______________________________________________________________________

# 13. Useful Diagnostic Commands

System information:

```bash
uname
hostname
```

______________________________________________________________________

Resources:

```bash
top
htop
free
df
du
```

______________________________________________________________________

Processes:

```bash
ps
pgrep
kill
```

______________________________________________________________________

Networking:

```bash
ip
ss
ping
curl
dig
```

______________________________________________________________________

Storage:

```bash
lsblk
blkid
mount
```

______________________________________________________________________

Logging:

```bash
journalctl
tail
dmesg
```

______________________________________________________________________

# 14. Production Troubleshooting Scenarios

## Scenario 1

### Website is Down

Checklist:

- Is the service running?
- Is the process listening on the expected port?
- Is the firewall blocking access?
- Are there recent errors in the logs?
- Is DNS resolving correctly?

Useful commands:

```bash
systemctl status nginx
ss -tulpn
journalctl -u nginx
curl localhost
```

______________________________________________________________________

## Scenario 2

### Disk is Full

Commands:

```bash
df -h
du -sh *
lsof +L1
```

Possible causes:

- Large log files
- Backup files
- Deleted files still held open
- Docker images or volumes

______________________________________________________________________

## Scenario 3

### High CPU Usage

Commands:

```bash
top
ps aux --sort=-%cpu
```

Possible causes:

- Infinite loops
- High request volume
- Expensive database queries
- Background jobs

______________________________________________________________________

## Scenario 4

### High Memory Usage

Commands:

```bash
free -h
ps aux --sort=-%mem
```

Look for:

- Memory leaks
- Large caches
- Excessive numbers of processes

______________________________________________________________________

## Scenario 5

### Cannot Connect to Database

Checklist:

- Is the database running?
- Is the port open?
- Is DNS resolving?
- Is the firewall allowing traffic?
- Are credentials correct?

Useful commands:

```bash
systemctl status postgresql
ss -tulpn
ping
dig
```

______________________________________________________________________

## Scenario 6

### SSH Login Fails

Check:

```bash
systemctl status ssh
journalctl -u ssh
ss -tulpn
```

Verify:

- SSH service is running
- Firewall rules
- SSH configuration
- Authorized keys
- User permissions

______________________________________________________________________

# 15. Common Mistakes

❌ Restarting services before checking logs.

______________________________________________________________________

❌ Assuming the first observed symptom is the root cause.

______________________________________________________________________

❌ Making multiple configuration changes simultaneously.

______________________________________________________________________

❌ Ignoring disk space and memory usage during investigations.

______________________________________________________________________

❌ Failing to verify that a fix actually resolved the issue.

______________________________________________________________________

# 16. Best Practices

- Gather evidence before making changes.
- Start with logs.
- Verify service status before restarting.
- Check system resources early.
- Use a repeatable troubleshooting methodology.
- Document findings for future incidents.

______________________________________________________________________

# Interview Questions

## Q1. What is your general approach to troubleshooting a production issue?

**Answer**

I begin by understanding the reported symptoms, collecting logs and system metrics, checking the health of relevant
services, identifying the root cause through evidence, applying the smallest necessary fix, verifying the outcome, and
monitoring the system to ensure the issue does not recur.

______________________________________________________________________

## Q2. What commands would you use if a Linux server suddenly became slow?

**Answer**

I would typically inspect CPU usage with `top` or `htop`, memory with `free -h`, disk usage with `df -h`, processes with
`ps`, load averages using `uptime`, and relevant logs using `journalctl` or application log files.

______________________________________________________________________

## Q3. How would you investigate why a service failed to start?

**Answer**

I would check the service status with `systemctl status`, review its logs using `journalctl -u`, verify configuration
files, inspect dependencies, and confirm that required ports and resources are available.

______________________________________________________________________

## Q4. What is the difference between a symptom and a root cause?

**Answer**

A symptom is the observable problem, such as a website returning HTTP 500 errors. The root cause is the underlying issue
responsible for the symptom, such as a database outage or exhausted disk space.

______________________________________________________________________

## Q5. Why should logs be checked before restarting a failed service?

**Answer**

Restarting a service may clear valuable diagnostic information or temporarily hide the underlying issue. Reviewing logs
first helps preserve evidence and increases the likelihood of identifying the true cause.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Collect:

- OS version
- Kernel version
- Hostname
- Uptime

using Linux commands.

______________________________________________________________________

## Exercise 2

Identify the top five processes by:

- CPU usage
- Memory usage

______________________________________________________________________

## Exercise 3

Inspect:

- Disk usage
- Largest directories
- Mounted filesystems

______________________________________________________________________

## Exercise 4

Verify:

- Running services
- Open ports
- Active network interfaces

______________________________________________________________________

## Exercise 5

Use `journalctl` to inspect logs for a system service.

______________________________________________________________________

## Exercise 6

Simulate a troubleshooting workflow for a service that fails to start and document the steps you would take.

______________________________________________________________________

# Cheat Sheet

## System

```bash
uname
hostname
uptime
who
```

______________________________________________________________________

## Resources

```bash
top
htop
free
df
du
vmstat
```

______________________________________________________________________

## Processes

```bash
ps
pgrep
kill
```

______________________________________________________________________

## Networking

```bash
ip
ss
ping
dig
curl
```

______________________________________________________________________

## Services

```bash
systemctl
journalctl
```

______________________________________________________________________

## Logs

```bash
tail
less
dmesg
```

______________________________________________________________________

# Summary

In this chapter, you learned a structured approach to troubleshooting Linux systems. You explored how to diagnose CPU,
memory, disk, networking, service, permission, and boot issues using common Linux utilities and how to investigate
real-world production scenarios methodically. These skills are critical for maintaining reliable backend services and
responding effectively to production incidents.

______________________________________________________________________

## Next

[Linux Interview Scenarios and Cheat Sheet](24-linux-interview-scenarios-and-cheat-sheet.md)

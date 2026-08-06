# Linux Complete Interview & Production Course

# File 20 — Scheduling Tasks with Cron and At

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** System Administration
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 19 — Package Management

______________________________________________________________________

# Table of Contents

1. Introduction
1. Why Task Scheduling Matters
1. What is Cron?
1. Cron Architecture
1. Cron Time Format
1. Managing Crontab
1. System-Wide Cron
1. Cron Directories
1. Cron Environment
1. Common Cron Expressions
1. The `at` Command
1. The `batch` Command
1. Cron Logging
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

Many system administration tasks need to run automatically.

Examples:

- Database backups
- Log cleanup
- Sending reports
- Synchronizing files
- Restarting services
- Health checks
- Cache cleanup

Instead of running these commands manually, Linux provides scheduling utilities such as:

- **cron** — recurring tasks
- **at** — one-time tasks
- **batch** — run when system load is low

______________________________________________________________________

# 2. Why Task Scheduling Matters

Suppose a database backup must run every night at **2:00 AM**.

Without automation:

```
Administrator

↓

Wake up every day

↓

Run backup
```

With cron:

```
Cron

↓

Runs Automatically

↓

Backup Completed
```

Automation improves reliability and reduces human error.

______________________________________________________________________

# 3. What is Cron?

Cron is a background service (daemon) that executes scheduled commands at specified times.

Daemon:

```text
cron
```

or

```text
crond
```

depending on the Linux distribution.

Verify:

```bash
systemctl status cron
```

or

```bash
systemctl status crond
```

______________________________________________________________________

# 4. Cron Architecture

```
Cron Daemon

↓

Reads Schedule

↓

Matches Current Time

↓

Executes Command

↓

Logs Result
```

Each user can have an individual schedule called a **crontab**.

______________________________________________________________________

# 5. Cron Time Format

A cron expression contains five time fields.

```text
* * * * * command
│ │ │ │ │
│ │ │ │ └── Day of Week (0-7)
│ │ │ └──── Month (1-12)
│ │ └────── Day of Month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

______________________________________________________________________

## Examples

Run every minute:

```text
* * * * *
```

______________________________________________________________________

Run daily at 2:30 AM:

```text
30 2 * * *
```

______________________________________________________________________

Run every Sunday:

```text
0 3 * * 0
```

______________________________________________________________________

Run every weekday:

```text
0 9 * * 1-5
```

______________________________________________________________________

Run every 10 minutes:

```text
*/10 * * * *
```

______________________________________________________________________

Run every January 1st:

```text
0 0 1 1 *
```

______________________________________________________________________

# Special Strings

| Expression | Meaning |
|------------|---------|
| @reboot | Run after boot |
| @yearly | Once a year |
| @monthly | Once a month |
| @weekly | Once a week |
| @daily | Every day |
| @hourly | Every hour |

Example:

```text
@daily /home/riyaz/backup.sh
```

______________________________________________________________________

# 6. Managing Crontab

Edit your crontab:

```bash
crontab -e
```

______________________________________________________________________

List entries:

```bash
crontab -l
```

______________________________________________________________________

Remove all entries:

```bash
crontab -r
```

Be careful—this deletes the entire crontab.

______________________________________________________________________

Edit another user's crontab:

```bash
sudo crontab -u username -e
```

______________________________________________________________________

# Example Crontab

```text
0 2 * * * /home/riyaz/backup.sh
```

Runs every day at 2:00 AM.

______________________________________________________________________

# 7. System-Wide Cron

System cron configuration:

```text
/etc/crontab
```

Example:

```text
30 3 * * * root backup.sh
```

Unlike user crontabs, the system crontab includes the user account that should execute the command.

______________________________________________________________________

# 8. Cron Directories

Linux also provides special cron directories.

| Directory | Frequency |
|------------|-----------|
| /etc/cron.hourly | Hourly |
| /etc/cron.daily | Daily |
| /etc/cron.weekly | Weekly |
| /etc/cron.monthly | Monthly |

Example:

```text
/etc/cron.daily/logrotate
```

______________________________________________________________________

# 9. Cron Environment

Cron runs with a minimal environment.

Important variables may be missing.

For example:

```bash
PATH
HOME
```

may not be identical to an interactive shell.

Specify the full path to commands.

Instead of:

```bash
python script.py
```

Prefer:

```bash
/usr/bin/python3 /home/riyaz/script.py
```

______________________________________________________________________

Set environment variables inside a crontab:

```text
PATH=/usr/local/bin:/usr/bin:/bin
```

______________________________________________________________________

Redirect output:

```text
0 2 * * * backup.sh > backup.log 2>&1
```

______________________________________________________________________

# 10. Common Cron Expressions

Every hour:

```text
0 * * * *
```

______________________________________________________________________

Every day at midnight:

```text
0 0 * * *
```

______________________________________________________________________

Every Monday:

```text
0 8 * * 1
```

______________________________________________________________________

Every 15 minutes:

```text
*/15 * * * *
```

______________________________________________________________________

Every 5 hours:

```text
0 */5 * * *
```

______________________________________________________________________

Every 30 seconds?

**Not possible.**

Cron's minimum scheduling interval is one minute.

______________________________________________________________________

# 11. The `at` Command

`at` schedules a command to run **once**.

Run at 6 PM:

```bash
at 6:00 PM
```

Type commands:

```bash
echo "Backup complete"
```

Press:

```
Ctrl + D
```

______________________________________________________________________

Schedule using natural language:

```bash
at now + 1 hour
```

______________________________________________________________________

Tomorrow:

```bash
at tomorrow
```

______________________________________________________________________

View jobs:

```bash
atq
```

______________________________________________________________________

Remove a job:

```bash
atrm JOB_ID
```

______________________________________________________________________

# 12. The `batch` Command

`batch` runs commands when the system load becomes sufficiently low.

Example:

```bash
batch
```

Type:

```bash
updatedb
```

Finish with:

```
Ctrl + D
```

Useful for CPU-intensive maintenance tasks.

______________________________________________________________________

# 13. Cron Logging

View cron logs.

Ubuntu:

```bash
grep CRON /var/log/syslog
```

______________________________________________________________________

Using systemd:

```bash
journalctl -u cron
```

or

```bash
journalctl -u crond
```

depending on the distribution.

______________________________________________________________________

# 14. Production Examples

## Daily Database Backup

```text
0 2 * * * /opt/scripts/db-backup.sh
```

______________________________________________________________________

## Delete Old Logs

```text
0 1 * * * find /logs -mtime +30 -delete
```

______________________________________________________________________

## Restart Service Every Sunday

```text
0 4 * * 0 systemctl restart nginx
```

______________________________________________________________________

## Synchronize Files

```text
*/30 * * * * rsync -av source/ backup/
```

______________________________________________________________________

## Check Disk Usage

```text
0 */6 * * * df -h > /tmp/disk.txt
```

______________________________________________________________________

## Run Cleanup Once in One Hour

```bash
at now + 1 hour
```

______________________________________________________________________

# 15. Common Mistakes

❌ Forgetting to use absolute paths.

______________________________________________________________________

❌ Assuming cron has the same environment as your terminal.

______________________________________________________________________

❌ Forgetting to redirect output.

A cron job that fails silently can be difficult to debug.

______________________________________________________________________

❌ Scheduling long-running jobs too frequently, causing overlapping executions.

______________________________________________________________________

❌ Editing `/etc/crontab` when a user crontab is sufficient.

______________________________________________________________________

# 16. Best Practices

- Use full paths for commands and scripts.
- Redirect stdout and stderr to log files.
- Test scripts manually before scheduling them.
- Avoid overlapping jobs for long-running tasks.
- Monitor cron logs periodically.
- Use meaningful comments in complex crontabs.

______________________________________________________________________

# Interview Questions

## Q1. What is the difference between `cron` and `at`?

**Answer**

`cron` is used for recurring scheduled tasks, while `at` schedules a command to run only once at a specified time.

______________________________________________________________________

## Q2. Why do cron jobs often fail even though the command works in the terminal?

**Answer**

Cron runs with a minimal environment and may not have the same `PATH`, environment variables, or working directory as an
interactive shell. Using absolute paths and setting required variables usually resolves the issue.

______________________________________________________________________

## Q3. What is the minimum scheduling interval supported by cron?

**Answer**

Cron supports a minimum interval of one minute. It cannot schedule tasks every few seconds.

______________________________________________________________________

## Q4. What is the purpose of `/etc/crontab`?

**Answer**

`/etc/crontab` is the system-wide cron configuration file. Unlike user crontabs, it specifies the user account under
which each scheduled command should run.

______________________________________________________________________

## Q5. When would you use `batch` instead of `cron`?

**Answer**

`batch` is appropriate for resource-intensive jobs that should run only when the system load is low, rather than at a
fixed time.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Create a cron job that prints the current date every minute.

______________________________________________________________________

## Exercise 2

Schedule a script to execute daily at 3:00 AM.

______________________________________________________________________

## Exercise 3

Create a one-time job using:

```bash
at
```

______________________________________________________________________

## Exercise 4

List all scheduled cron jobs and `at` jobs.

______________________________________________________________________

## Exercise 5

Redirect both output and errors from a cron job to a log file.

______________________________________________________________________

## Exercise 6

Inspect your system's cron logs using:

```bash
journalctl
```

or

```bash
grep CRON
```

______________________________________________________________________

# Cheat Sheet

## Cron

```bash
crontab -e
crontab -l
crontab -r
```

______________________________________________________________________

## Cron Files

```text
/etc/crontab
/etc/cron.hourly
/etc/cron.daily
/etc/cron.weekly
/etc/cron.monthly
```

______________________________________________________________________

## At

```bash
at
atq
atrm
batch
```

______________________________________________________________________

## Logs

```bash
journalctl -u cron
grep CRON /var/log/syslog
```

______________________________________________________________________

# Summary

In this chapter, you learned how Linux automates recurring and one-time tasks using `cron`, `at`, and `batch`. You
explored cron syntax, user and system crontabs, cron directories, scheduling expressions, environment considerations,
logging, and best practices for reliable automation in production systems.

______________________________________________________________________

## Next

[Log Management and Monitoring](21-log-management-and-monitoring.md)

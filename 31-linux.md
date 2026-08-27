# 31. Linux for Backend Engineers

**Previous:** [30. Docker](./30-docker.md)

**Next:** [32. Production Debugging & Incident Response](./32-production-debugging.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Navigate and reason about the Linux filesystem.
- Understand users, groups and file permissions.
- Work with processes and threads.
- Understand common Unix/Linux signals.
- Use the shell effectively for backend operations.
- Use pipes and redirection.
- Search and transform text with `grep`, `awk` and `sed`.
- Connect to servers using SSH.
- Diagnose basic Linux networking problems.
- Inspect CPU, memory and disk usage.
- Understand `systemd` and services.
- Locate and inspect system/application logs.
- Understand `cron` and scheduled jobs.
- Diagnose common backend problems from the command line.
- Answer practical Linux questions expected from a 5+ year backend engineer.

______________________________________________________________________

# 1. Why Linux Matters for Backend Engineers

Most Python backend applications eventually run on Linux.

Even if you primarily write:

```text
Python
FastAPI
SQLAlchemy
Redis
Kafka
Docker
```

you still need to understand the operating system underneath them.

Linux knowledge helps when:

- An application is consuming too much memory.
- A process is using excessive CPU.
- A service is not starting.
- A port is already occupied.
- Disk space is exhausted.
- A process is stuck.
- Logs need to be investigated.
- A remote server needs to be accessed.
- Network connectivity needs to be diagnosed.

For a senior backend engineer, Linux should be practical rather than purely theoretical.

______________________________________________________________________

# 2. Linux Filesystem

Linux uses a hierarchical filesystem.

The root directory is:

```text
/
```

Common directories include:

```text
/
├── bin
├── boot
├── dev
├── etc
├── home
├── lib
├── opt
├── proc
├── root
├── run
├── tmp
├── usr
└── var
```

The exact contents vary by distribution.

______________________________________________________________________

# 3. Important Filesystem Directories

## `/etc`

Contains system and service configuration.

Examples:

```text
/etc/hosts
/etc/ssh/
/etc/systemd/
```

______________________________________________________________________

## `/var`

Contains variable data such as:

- Logs
- Caches
- Application/service data

A common log location is:

```text
/var/log
```

______________________________________________________________________

## `/home`

Contains regular users' home directories.

Example:

```text
/home/riyaz
```

______________________________________________________________________

## `/tmp`

Used for temporary files.

Applications should not assume that temporary files stored there will persist indefinitely.

______________________________________________________________________

## `/proc`

A virtual filesystem exposing process and kernel information.

Examples:

```text
/proc/cpuinfo
/proc/meminfo
/proc/<pid>/
```

______________________________________________________________________

## `/dev`

Contains device-related filesystem entries.

Examples include:

```text
/dev/null
/dev/zero
```

______________________________________________________________________

# 4. Absolute vs Relative Paths

An absolute path starts from `/`.

Example:

```bash
/etc/hosts
```

A relative path is interpreted from the current working directory.

Example:

```bash
./config/settings.yaml
```

Important commands:

```bash
pwd
cd
ls
```

______________________________________________________________________

# 5. `pwd`

`pwd` prints the current working directory.

```bash
pwd
```

Example:

```text
/app
```

This is especially useful when debugging scripts that use relative paths.

______________________________________________________________________

# 6. `cd`

Changes the current working directory.

Examples:

```bash
cd /var/log
cd ..
cd ~
cd -
```

Useful meanings:

```text
.. → parent directory
~  → current user's home directory
-  → previous working directory
```

______________________________________________________________________

# 7. `ls`

Lists directory contents.

Examples:

```bash
ls
ls -l
ls -la
ls -lh
```

Useful options:

```text
-l  detailed listing
-a  hidden files
-h  human-readable sizes
```

______________________________________________________________________

# 8. File Types

Linux commonly represents different filesystem objects through file types.

Examples include:

- Regular files
- Directories
- Symbolic links
- Devices
- Sockets

Check a file with:

```bash
file <path>
```

Inspect links with:

```bash
ls -l
```

______________________________________________________________________

# 9. Symbolic Links

A symbolic link points to another path.

Example:

```bash
ln -s /opt/app/current /opt/app/releases/2026-08-27
```

Conceptually:

```text
current
   ↓
release directory
```

Symbolic links are common in deployments where:

```text
current → latest release
```

can be changed without copying the entire application.

______________________________________________________________________

# 10. Hard Links — Overview

A hard link provides another directory entry referring to the same underlying file data.

For interviews, know the basic distinction:

```text
Symbolic link
→ points to a path

Hard link
→ another directory entry for the same underlying inode
```

Hard links have filesystem restrictions and are less commonly used in application deployment.

______________________________________________________________________

# 11. File Permissions

Linux permissions are commonly represented as:

```text
rwx
```

for:

```text
user
group
others
```

Example:

```text
-rwxr-x---
```

Breakdown:

```text
user   → rwx
group  → r-x
others → ---
```

______________________________________________________________________

# 12. Read, Write, Execute

For regular files:

```text
r → read
w → write
x → execute
```

For directories, permissions have slightly different semantics.

### Directory read

Allows listing directory entries.

### Directory write

Allows creating/removing entries, subject to other permissions.

### Directory execute

Allows accessing entries within the directory when other permissions permit it.

This distinction is important during Linux debugging.

______________________________________________________________________

# 13. Numeric Permissions

Permissions can be represented numerically.

```text
r = 4
w = 2
x = 1
```

Therefore:

```text
7 = rwx
6 = rw-
5 = r-x
4 = r--
0 = ---
```

Example:

```bash
chmod 750 script.sh
```

means:

```text
user  → rwx
group → r-x
other → ---
```

______________________________________________________________________

# 14. `chmod`

Changes permissions.

Examples:

```bash
chmod 644 config.txt
chmod 755 script.sh
chmod 600 secret.txt
```

Typical meanings:

```text
644 → owner read/write, others read
755 → owner full access, others read/execute
600 → owner read/write only
```

Use the least privilege appropriate for the file.

______________________________________________________________________

# 15. `chown`

Changes file ownership.

Example:

```bash
chown appuser:appgroup app.log
```

This sets:

```text
owner = appuser
group = appgroup
```

______________________________________________________________________

# 16. `chgrp`

Changes the group ownership.

```bash
chgrp appgroup app.log
```

______________________________________________________________________

# 17. `umask`

`umask` controls default permission bits removed when new files/directories are created.

Check it with:

```bash
umask
```

It is useful when diagnosing why newly created files have unexpected permissions.

______________________________________________________________________

# 18. Users and Groups

Linux uses users and groups to control ownership and access.

A process normally runs under a user identity.

Groups allow multiple users/processes to share access to resources.

Useful commands:

```bash
id
whoami
groups
```

______________________________________________________________________

# 19. `whoami`

Shows the current effective user identity.

```bash
whoami
```

Useful when a script behaves differently under:

```text
root
```

versus:

```text
appuser
```

______________________________________________________________________

# 20. `id`

Shows user and group identity information.

```bash
id
```

Example information can include:

```text
uid
gid
groups
```

______________________________________________________________________

# 21. Root User

`root` has extensive privileges on a Linux system.

Running everything as root is dangerous because a compromised process has significantly more capability.

Backend services should generally run under a dedicated least-privileged account when practical.

______________________________________________________________________

# 22. `sudo`

`sudo` allows an authorized user to execute a command with elevated privileges.

Example:

```bash
sudo systemctl restart myapp
```

Use elevated privileges only when necessary.

______________________________________________________________________

# 23. Processes

A process is a running instance of a program.

For example:

```text
uvicorn
```

may run as one or more OS processes.

Each process has a process ID:

```text
PID
```

______________________________________________________________________

# 24. Process IDs

Useful commands:

```bash
ps
pgrep
pidof
```

Example:

```bash
pgrep uvicorn
```

can find matching process IDs.

______________________________________________________________________

# 25. `ps`

`ps` displays process information.

Common commands:

```bash
ps aux
ps -ef
```

Useful information includes:

- PID
- User
- CPU usage
- Memory usage
- Command

______________________________________________________________________

# 26. Process Tree

Processes can have parent/child relationships.

A useful command is:

```bash
pstree
```

or:

```bash
ps --forest
```

Conceptually:

```text
systemd
   ↓
service
   ↓
worker
```

Understanding parent/child relationships helps during debugging.

______________________________________________________________________

# 27. Process States

Linux processes can be in states such as:

```text
Running
Sleeping
Stopped
Zombie
```

The exact state codes shown by tools depend on the command.

A sleeping process is not necessarily unhealthy; many processes sleep while waiting for I/O or events.

______________________________________________________________________

# 28. Zombie Processes

A zombie is a terminated child process whose parent has not yet collected its exit status.

Conceptually:

```text
Child exits
    ↓
Zombie
    ↓
Parent waits/reaps
    ↓
Zombie removed
```

A zombie is not actively consuming CPU like a normal process, but many zombies can indicate a process-management
problem.

______________________________________________________________________

# 29. Orphan Processes

An orphan is a process whose original parent has exited.

Linux reassigns orphaned processes to an appropriate reaper process.

Do not confuse:

```text
Zombie
```

with:

```text
Orphan
```

An orphan is still running; a zombie has already terminated.

______________________________________________________________________

# 30. Threads

A thread is an execution unit within a process.

Threads within the same process share resources such as:

- Address space
- Heap
- Open resources

but have their own execution state.

Python's threading behavior is also affected by the CPython GIL, covered earlier in the concurrency topic.

______________________________________________________________________

# 31. Process vs Thread

### Process

- Separate address space
- Stronger isolation
- More expensive communication
- Higher creation/resource overhead

### Thread

- Shares process address space
- Lower overhead
- Easier shared-memory communication
- Requires synchronization for shared state

______________________________________________________________________

# 32. Signals

Signals are asynchronous notifications delivered to processes.

Important signals include:

```text
SIGTERM
SIGKILL
SIGINT
SIGHUP
SIGSTOP
SIGCONT
```

Backend engineers should understand the operational meaning of the most common ones.

______________________________________________________________________

# 33. SIGTERM

`SIGTERM` requests graceful termination.

A process can generally handle it and perform cleanup.

For services:

```text
SIGTERM
  ↓
Graceful shutdown
  ↓
Close connections
  ↓
Finish/stop work
  ↓
Exit
```

This is why applications should handle shutdown correctly.

______________________________________________________________________

# 34. SIGKILL

`SIGKILL` forcibly terminates a process.

The process cannot catch or handle it.

Therefore:

```text
SIGTERM
```

is generally preferred when graceful shutdown is possible.

______________________________________________________________________

# 35. SIGINT

`SIGINT` commonly represents an interrupt, such as pressing:

```text
Ctrl+C
```

It can be handled by applications.

______________________________________________________________________

# 36. SIGHUP

Historically associated with terminal hangups.

Some daemons/services also use it as a signal to reload configuration, depending on the application.

Always check the specific service's documented signal behavior.

______________________________________________________________________

# 37. SIGSTOP and SIGCONT

`SIGSTOP` stops a process.

`SIGCONT` resumes a stopped process.

Unlike normal application-level signals, these are primarily process-control operations.

______________________________________________________________________

# 38. `kill`

`kill` sends a signal to a process.

Example:

```bash
kill -TERM <pid>
```

or:

```bash
kill -9 <pid>
```

Prefer:

```bash
kill -TERM
```

before using:

```bash
kill -9
```

because SIGKILL does not allow graceful cleanup.

______________________________________________________________________

# 39. Shell

A shell is a command interpreter.

Common shells include:

```text
bash
zsh
sh
```

A shell allows you to:

- Execute programs
- Set variables
- Redirect output
- Pipe commands
- Run scripts
- Control processes

______________________________________________________________________

# 40. Environment Variables

Environment variables provide configuration to processes.

Example:

```bash
export DATABASE_URL="postgresql://..."
```

A child process started from that shell can inherit the environment variable.

Inspect variables:

```bash
env
printenv
echo "$DATABASE_URL"
```

______________________________________________________________________

# 41. Shell Exit Status

Commands return an exit status.

Conventionally:

```text
0 → success
non-zero → failure
```

Check the previous command:

```bash
echo $?
```

This is important in:

- Shell scripts
- CI/CD
- Docker
- systemd
- Automation

______________________________________________________________________

# 42. `&&`

Run the second command only if the first succeeds.

```bash
pytest && echo "tests passed"
```

If `pytest` returns non-zero, the second command is not executed.

______________________________________________________________________

# 43. `||`

Run the second command if the first fails.

```bash
pytest || echo "tests failed"
```

This is useful for simple shell control flow.

______________________________________________________________________

# 44. Pipes

A pipe sends the standard output of one command to the standard input of another.

Example:

```bash
ps aux | grep uvicorn
```

Conceptually:

```text
ps
 ↓ stdout
pipe
 ↓ stdin
grep
```

Pipes are one of the most useful Linux debugging techniques.

______________________________________________________________________

# 45. Standard Streams

Linux processes commonly use:

```text
stdin   → 0
stdout  → 1
stderr  → 2
```

Understanding these is important for shell scripting and application debugging.

______________________________________________________________________

# 46. Output Redirection

Redirect stdout:

```bash
command > output.log
```

Append stdout:

```bash
command >> output.log
```

Redirect stderr:

```bash
command 2> error.log
```

Redirect both:

```bash
command > output.log 2>&1
```

______________________________________________________________________

# 47. `/dev/null`

`/dev/null` discards written data.

Example:

```bash
command > /dev/null
```

Discard both stdout and stderr:

```bash
command > /dev/null 2>&1
```

Use it carefully during debugging because it can hide useful errors.

______________________________________________________________________

# 48. `grep`

`grep` searches text.

Examples:

```bash
grep "ERROR" app.log
grep -i "timeout" app.log
grep -R "DATABASE_URL" /etc/myapp
```

Useful options include:

```text
-i → case-insensitive
-n → line numbers
-r/-R → recursive search
-v → invert match
-E → extended regular expressions
```

______________________________________________________________________

# 49. `grep` in Production Debugging

Example:

```bash
grep -i "timeout" /var/log/myapp.log
```

You can combine commands:

```bash
grep -i "error" app.log | tail -50
```

This quickly narrows large log files.

______________________________________________________________________

# 50. `awk`

`awk` is useful for structured text processing and field-based extraction.

Example:

```bash
awk '{print $1, $7}' access.log
```

For whitespace-separated fields:

```text
$1 → first field
$2 → second field
...
```

`awk` becomes particularly useful for logs and command output.

______________________________________________________________________

# 51. `sed`

`sed` is a stream editor.

A common use is replacing text:

```bash
sed 's/old/new/g' file.txt
```

It can also:

- Select lines
- Delete lines
- Transform text
- Perform scripted substitutions

______________________________________________________________________

# 52. `grep` vs `awk` vs `sed`

| Tool | Best Use |
|---|---|
| `grep` | Search/filter |
| `awk` | Extract/process fields |
| `sed` | Transform/edit streams |

In real production debugging, these tools are often combined.

______________________________________________________________________

# 53. `tail`

Useful for inspecting the end of log files.

```bash
tail -100 app.log
```

Follow a file:

```bash
tail -f app.log
```

This is useful for watching application logs during an incident.

______________________________________________________________________

# 54. `head`

Shows the beginning of a file.

```bash
head -50 app.log
```

Useful for quickly inspecting large files.

______________________________________________________________________

# 55. `less`

`less` allows interactive inspection of large text files.

```bash
less app.log
```

Useful controls include:

```text
/term → search
n      → next match
q      → quit
```

______________________________________________________________________

# 56. SSH

SSH provides secure remote access to Linux systems.

Example:

```bash
ssh user@server
```

A typical backend engineer workflow is:

```text
Laptop
  ↓
SSH
  ↓
Linux server
  ↓
Inspect service/logs/resources
```

______________________________________________________________________

# 57. SSH Keys

SSH commonly uses key-based authentication.

Conceptually:

```text
Private key → client
Public key  → server
```

The private key should be protected and should not be copied to servers unnecessarily.

______________________________________________________________________

# 58. SSH Debugging

Verbose SSH output can help diagnose connection problems:

```bash
ssh -v user@server
```

Additional verbosity levels can be used when required.

Common issues include:

- Wrong username
- Incorrect key permissions
- Network connectivity
- SSH daemon configuration
- Firewall/security rules

______________________________________________________________________

# 59. File Transfer

Common tools include:

```bash
scp
rsync
```

Example:

```bash
scp app.log user@server:/tmp/
```

`rsync` is often preferable for efficient repeated synchronization.

______________________________________________________________________

# 60. Linux Networking Basics

Backend engineers should understand:

- IP addresses
- Ports
- DNS
- TCP
- UDP
- Listening sockets
- Routing
- Localhost
- Interfaces

Useful commands include:

```bash
ss
ip
ping
curl
dig
```

______________________________________________________________________

# 61. Listening Ports

Use:

```bash
ss -lntp
```

to inspect listening TCP sockets.

This can help answer:

> Which process is listening on port 8000?

______________________________________________________________________

# 62. Find a Port

A common workflow:

```bash
ss -lntp | grep :8000
```

Then identify the process and investigate it.

Depending on system permissions, process details may be limited for users without sufficient privileges.

______________________________________________________________________

# 63. `ip`

The `ip` command is a modern Linux networking tool.

Examples:

```bash
ip addr
ip route
ip link
```

Use it to inspect:

- Interfaces
- Addresses
- Routes
- Link state

______________________________________________________________________

# 64. `curl`

`curl` is extremely useful for HTTP debugging.

Example:

```bash
curl http://localhost:8000/health
```

Headers:

```bash
curl -i http://localhost:8000/health
```

Verbose mode:

```bash
curl -v http://localhost:8000/health
```

______________________________________________________________________

# 65. `dig`

`dig` is useful for DNS troubleshooting.

Example:

```bash
dig example.com
```

It can help determine whether DNS resolution is working and what records are returned.

______________________________________________________________________

# 66. `ping`

`ping` tests basic IP-level reachability using ICMP where permitted.

Example:

```bash
ping 8.8.8.8
```

Important:

> A failed ping does not necessarily mean an application service is unreachable because ICMP may be blocked while TCP/HTTP works.

______________________________________________________________________

# 67. DNS Debugging

A useful troubleshooting flow:

```text
Can hostname resolve?
        ↓
dig hostname
        ↓
Can IP be reached?
        ↓
Can TCP port connect?
        ↓
Can application respond?
```

Use the appropriate tool for each layer.

______________________________________________________________________

# 68. Disk Usage

Important commands:

```bash
df -h
du -sh
du -sh *
```

### `df`

Shows filesystem-level free/used space.

### `du`

Shows space consumed by files/directories.

______________________________________________________________________

# 69. `df` vs `du`

This is a common interview/debugging question.

### `df`

Answers:

> How much space is used/free on the filesystem?

### `du`

Answers:

> Which files/directories are consuming space?

______________________________________________________________________

# 70. Disk Full Debugging

If an application reports:

```text
No space left on device
```

check:

```bash
df -h
```

Then identify large directories:

```bash
du -sh /var/*
```

Also investigate:

- Logs
- Temporary files
- Container storage
- Database files
- Deleted-but-open files

______________________________________________________________________

# 71. Deleted-but-Open Files

A process can keep a deleted file open.

The filename is gone from the directory, but disk space can remain occupied until the process closes the file
descriptor.

This can explain cases where:

```text
df
```

shows high usage but obvious files do not account for it.

Tools such as:

```bash
lsof
```

can help investigate this.

______________________________________________________________________

# 72. Memory

Useful commands include:

```bash
free -h
ps aux
top
```

Memory concepts include:

- Used memory
- Available memory
- Cache
- Swap

Do not assume that all "used" memory is unavailable to applications.

______________________________________________________________________

# 73. `free -h`

Shows memory and swap information in human-readable form.

```bash
free -h
```

When diagnosing memory pressure, pay attention to:

```text
available
swap
```

as well as total/used values.

______________________________________________________________________

# 74. `top`

`top` provides a live view of processes and resource usage.

Useful information includes:

- CPU
- Memory
- Process ID
- Process state

It is one of the first tools to use during CPU/memory incidents.

______________________________________________________________________

# 75. `htop`

`htop` is an interactive process viewer available on many Linux systems.

It provides a more user-friendly interface than `top`.

It may not be installed on every server.

______________________________________________________________________

# 76. CPU Investigation

A useful workflow:

```text
High CPU
  ↓
top
  ↓
Find process
  ↓
Identify PID
  ↓
Inspect process
  ↓
Determine thread/application cause
```

For Python applications, distinguish:

```text
CPU-bound work
```

from:

```text
I/O waiting
```

before deciding how to fix it.

______________________________________________________________________

# 77. Process Memory Investigation

Start with:

```bash
ps aux --sort=-%mem | head
```

This can show processes using significant memory.

Then inspect the specific process more deeply.

______________________________________________________________________

# 78. Open Files

Processes use file descriptors for resources such as:

- Files
- Sockets
- Pipes

`lsof` can help inspect them.

Example:

```bash
lsof -p <pid>
```

______________________________________________________________________

# 79. File Descriptor Limits

A service handling many network connections can hit file descriptor limits.

Symptoms can include errors such as:

```text
Too many open files
```

Investigate:

```bash
ulimit -n
```

and the service's configured limits.

______________________________________________________________________

# 80. systemd

`systemd` is a common Linux service and initialization system.

It manages services such as:

```text
FastAPI application
Nginx
PostgreSQL
Redis
```

depending on the environment.

______________________________________________________________________

# 81. systemctl

Common commands:

```bash
systemctl status myapp
systemctl start myapp
systemctl stop myapp
systemctl restart myapp
systemctl enable myapp
systemctl disable myapp
```

______________________________________________________________________

# 82. Service Status

When a service is failing:

```bash
systemctl status myapp
```

Check:

- Active/inactive state
- Exit status
- Recent logs
- Process information

Then inspect detailed logs.

______________________________________________________________________

# 83. systemd Service Unit

A simplified service might look like:

```ini
[Unit]
Description=My FastAPI Application
After=network.target

[Service]
User=appuser
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

The exact production configuration depends on the application and deployment environment.

______________________________________________________________________

# 84. Restart Policies

A service can be configured to restart after failure.

Example:

```ini
Restart=on-failure
```

Restart policies can improve availability, but they should not hide persistent application failures.

If a service repeatedly crashes:

```text
Crash
 ↓
Restart
 ↓
Crash
 ↓
Restart
```

investigate the underlying cause.

______________________________________________________________________

# 85. systemd Logs

`journalctl` is commonly used to inspect systemd-managed logs.

Examples:

```bash
journalctl -u myapp
journalctl -u myapp -f
journalctl -u myapp --since "1 hour ago"
```

______________________________________________________________________

# 86. Application Logs

Depending on deployment, application logs may be found in:

```text
journald
/var/log
container logging
centralized logging platform
```

Always understand where the service actually writes logs before debugging.

______________________________________________________________________

# 87. `journalctl`

Useful examples:

```bash
journalctl -u myapp
journalctl -u myapp -n 100
journalctl -u myapp -f
journalctl --since today
```

Use time filtering during incidents to reduce noise.

______________________________________________________________________

# 88. Log Rotation

Logs can grow indefinitely if not managed.

Log rotation systems can:

- Rotate files
- Compress old logs
- Remove old logs
- Control retention

Without log rotation, a busy service can eventually consume disk space.

______________________________________________________________________

# 89. Cron

`cron` runs commands on a schedule.

Example:

```text
Every night
    ↓
Backup script
```

A user's crontab can be edited with:

```bash
crontab -e
```

______________________________________________________________________

# 90. Cron Syntax

A traditional cron schedule contains:

```text
minute hour day-of-month month day-of-week
```

Example:

```cron
0 2 * * *
```

means approximately:

```text
Every day at 02:00
```

______________________________________________________________________

# 91. Cron Environment

Cron runs with an environment that may differ from an interactive shell.

Common surprises include:

- Different `PATH`
- Missing environment variables
- Different working directory
- Different shell behavior

Use absolute paths and explicitly configure required environment.

______________________________________________________________________

# 92. Cron vs systemd Timers

Both can schedule jobs.

For interview purposes:

```text
cron
→ traditional scheduled command

systemd timer
→ scheduling integrated with systemd service management
```

The choice depends on the environment and operational requirements.

______________________________________________________________________

# 93. Linux Backend Debugging Workflow

When an application is failing, avoid randomly running commands.

Use a structured flow:

```text
1. Is the process running?
2. Is the service healthy?
3. Is the port listening?
4. Are logs showing errors?
5. Is CPU/memory normal?
6. Is disk space available?
7. Can dependencies be reached?
8. Are permissions correct?
9. Are recent deployments/config changes involved?
```

This approach is more valuable than memorizing hundreds of commands.

______________________________________________________________________

# 94. Backend Incident: Service Down

Suppose:

```text
API unavailable
```

Start with:

```bash
systemctl status myapp
```

Then:

```bash
journalctl -u myapp -n 100
```

Check the port:

```bash
ss -lntp
```

Then test locally:

```bash
curl -v http://localhost:8000/health
```

______________________________________________________________________

# 95. Backend Incident: High CPU

Start with:

```bash
top
```

Identify the process.

Then inspect:

```bash
ps -fp <pid>
```

If necessary, investigate:

- Threads
- Application profiling
- Recent deployments
- Traffic increase
- Infinite loops
- CPU-bound workloads

Do not immediately kill the process without understanding the impact.

______________________________________________________________________

# 96. Backend Incident: High Memory

Start with:

```bash
free -h
ps aux --sort=-%mem | head
```

Determine:

```text
System memory pressure?
Process memory growth?
Swap activity?
```

Then investigate application behavior.

For Python, possible causes include:

- Large object retention
- Unbounded caches
- Large result sets
- Memory leaks in dependencies/extensions
- Excessive concurrency

______________________________________________________________________

# 97. Backend Incident: Disk Full

Start with:

```bash
df -h
```

Then:

```bash
du -sh /var/*
```

Investigate:

- Logs
- Container images/layers
- Database files
- Temporary files
- Deleted-but-open files

Avoid deleting files blindly in production.

______________________________________________________________________

# 98. Backend Incident: Port Conflict

Suppose the API should listen on:

```text
8000
```

but startup fails.

Run:

```bash
ss -lntp | grep :8000
```

Identify the process occupying the port and determine whether it should be stopped or whether the application
configuration should change.

______________________________________________________________________

# 99. Backend Incident: Permission Denied

Check:

```bash
ls -l <path>
```

Then investigate:

```text
owner
group
permissions
directory permissions
process user
```

Use:

```bash
id
```

to determine which user the application is running as.

Do not immediately use:

```bash
chmod 777
```

as a fix.

______________________________________________________________________

# 100. Why `chmod 777` Is Usually Wrong

`777` grants:

```text
read
write
execute
```

to everyone.

It often hides the real ownership/permission problem and creates unnecessary security risk.

Correct the:

```text
owner
group
permission
```

instead.

______________________________________________________________________

# 101. Backend Incident: DNS Failure

Suppose an application cannot reach:

```text
database.internal
```

Test:

```bash
dig database.internal
```

Then determine whether the returned address is reachable and whether the expected port is open.

Separate:

```text
DNS problem
```

from:

```text
TCP connectivity problem
```

and:

```text
application authentication problem
```

______________________________________________________________________

# 102. Backend Incident: HTTP Failure

Use:

```bash
curl -v http://service:8000/health
```

Inspect:

- DNS
- TCP connection
- TLS where applicable
- HTTP status
- Headers
- Response body

This helps identify which layer is failing.

______________________________________________________________________

# 103. Useful Command Cheat Sheet

| Problem | Commands |
|---|---|
| Current directory | `pwd` |
| Files | `ls -lah` |
| Process list | `ps aux` |
| Process tree | `pstree` |
| Find process | `pgrep`, `pidof` |
| CPU/memory | `top`, `htop` |
| Memory | `free -h` |
| Disk filesystem | `df -h` |
| Directory size | `du -sh` |
| Listening ports | `ss -lntp` |
| Network interfaces | `ip addr` |
| Routes | `ip route` |
| HTTP | `curl` |
| DNS | `dig` |
| Search text | `grep` |
| Field processing | `awk` |
| Text transformation | `sed` |
| Follow logs | `tail -f` |
| Service status | `systemctl status` |
| Service logs | `journalctl -u` |
| SSH | `ssh` |
| File transfer | `scp`, `rsync` |
| Open files | `lsof` |
| Signals | `kill` |

______________________________________________________________________

# 104. Common Linux Mistakes

## Mistake 1 — Using root for everything

Use least privilege.

## Mistake 2 — `chmod 777` as a universal fix

Fix ownership and permissions correctly.

## Mistake 3 — Killing with SIGKILL first

Try graceful termination where possible.

## Mistake 4 — Assuming high memory means all memory is unavailable

Understand cache and available memory.

## Mistake 5 — Confusing `df` and `du`

They answer different questions.

## Mistake 6 — Debugging application code before checking the service

First establish:

```text
process
service
port
logs
resources
```

## Mistake 7 — Assuming ping proves application connectivity

Ping tests ICMP reachability, not application-level TCP/HTTP behavior.

## Mistake 8 — Ignoring cron's environment

Scheduled jobs may run with different environment variables and paths.

## Mistake 9 — Restarting repeatedly without investigation

Restarts can temporarily hide the symptom while the underlying failure remains.

______________________________________________________________________

# 105. Interview Questions & Answers

## Q1. Why should backend engineers know Linux?

**Answer:**

Because most backend services run on Linux, and diagnosing processes, networking, resources, permissions, services and
logs requires OS-level knowledge.

______________________________________________________________________

## Q2. What is the Linux root directory?

**Answer:**

`/` is the root of the Linux filesystem hierarchy.

______________________________________________________________________

## Q3. What is `/etc` used for?

**Answer:**

System and application/service configuration.

______________________________________________________________________

## Q4. What is `/var` used for?

**Answer:**

Variable application/system data such as logs, caches and service data.

______________________________________________________________________

## Q5. What is `/proc`?

**Answer:**

A virtual filesystem exposing process and kernel information.

______________________________________________________________________

## Q6. What is the difference between an absolute and relative path?

**Answer:**

An absolute path starts from `/`; a relative path is interpreted from the current working directory.

______________________________________________________________________

## Q7. Explain Linux file permissions.

**Answer:**

Permissions are commonly specified for the owner, group and others, with read, write and execute bits.

______________________________________________________________________

## Q8. What does `755` mean?

**Answer:**

Owner has `rwx`; group and others have `r-x`.

______________________________________________________________________

## Q9. What does `644` mean?

**Answer:**

Owner has read/write, while group and others have read-only access.

______________________________________________________________________

## Q10. What does `600` mean?

**Answer:**

Only the owner has read/write access.

______________________________________________________________________

## Q11. What is the difference between `chmod` and `chown`?

**Answer:**

`chmod` changes permissions. `chown` changes ownership.

______________________________________________________________________

## Q12. What is `umask`?

**Answer:**

It controls which permission bits are removed from the default permissions when new filesystem objects are created.

______________________________________________________________________

## Q13. What is a process?

**Answer:**

A process is a running instance of a program with its own process state and address-space context.

______________________________________________________________________

## Q14. What is a PID?

**Answer:**

A Process ID uniquely identifies a process while it exists.

______________________________________________________________________

## Q15. Process vs thread?

**Answer:**

Processes have separate address spaces and stronger isolation. Threads within a process share memory/resources but have
separate execution state.

______________________________________________________________________

## Q16. What is a zombie process?

**Answer:**

A terminated child process whose parent has not yet collected its exit status.

______________________________________________________________________

## Q17. What is an orphan process?

**Answer:**

A still-running process whose original parent has exited and which is subsequently adopted by an appropriate reaper
process.

______________________________________________________________________

## Q18. What is SIGTERM?

**Answer:**

A termination request that allows a process to perform graceful shutdown.

______________________________________________________________________

## Q19. What is SIGKILL?

**Answer:**

A forceful termination signal that cannot be caught or handled by the target process.

______________________________________________________________________

## Q20. SIGTERM vs SIGKILL?

**Answer:**

SIGTERM allows graceful cleanup; SIGKILL immediately terminates the process without allowing application cleanup.

______________________________________________________________________

## Q21. What does Ctrl+C normally send?

**Answer:**

SIGINT.

______________________________________________________________________

## Q22. What does `kill` do?

**Answer:**

It sends a signal to a process. Despite its name, it is not limited to terminating processes.

______________________________________________________________________

## Q23. What is a shell?

**Answer:**

A command interpreter that executes commands and supports scripting, environment variables, pipes and redirection.

______________________________________________________________________

## Q24. What are stdout and stderr?

**Answer:**

stdout is standard output stream 1; stderr is standard error stream 2. stdin is standard input stream 0.

______________________________________________________________________

## Q25. What does `|` do?

**Answer:**

It connects one command's stdout to another command's stdin.

______________________________________________________________________

## Q26. What does `>` do?

**Answer:**

It redirects stdout to a file, replacing the file's existing contents.

______________________________________________________________________

## Q27. What does `>>` do?

**Answer:**

It appends stdout to a file.

______________________________________________________________________

## Q28. What does `2>&1` mean?

**Answer:**

It redirects stderr to the same destination as stdout at that point in the command.

______________________________________________________________________

## Q29. What is `grep` used for?

**Answer:**

Searching and filtering text based on patterns.

______________________________________________________________________

## Q30. What is `awk` useful for?

**Answer:**

Processing structured text and extracting or transforming fields.

______________________________________________________________________

## Q31. What is `sed` useful for?

**Answer:**

Stream-based text transformation such as substitutions, selection and deletion.

______________________________________________________________________

## Q32. grep vs awk vs sed?

**Answer:**

Use `grep` primarily for searching/filtering, `awk` for field-oriented processing and `sed` for stream transformations.

______________________________________________________________________

## Q33. What is SSH?

**Answer:**

A secure protocol commonly used for remote command-line access to Linux systems.

______________________________________________________________________

## Q34. Why use SSH keys?

**Answer:**

They provide key-based authentication without requiring a password for every connection and can be integrated into
controlled access systems.

______________________________________________________________________

## Q35. How do you check which process is listening on port 8000?

**Answer:**

Use a command such as:

```bash
ss -lntp | grep :8000
```

with sufficient permissions if process details are required.

______________________________________________________________________

## Q36. What does `curl -v` help with?

**Answer:**

It provides verbose HTTP/network information useful for diagnosing connection, TLS and HTTP-level issues.

______________________________________________________________________

## Q37. What is `dig` used for?

**Answer:**

DNS lookup and troubleshooting.

______________________________________________________________________

## Q38. Does ping prove that an HTTP service is available?

**Answer:**

No. Ping uses ICMP. A host can block ICMP while its TCP/HTTP service remains available.

______________________________________________________________________

## Q39. `df` vs `du`?

**Answer:**

`df` shows filesystem space usage/free space; `du` shows space consumed by files/directories.

______________________________________________________________________

## Q40. How would you debug "No space left on device"?

**Answer:**

Start with `df -h`, identify large directories with `du`, and investigate logs, temporary files, container storage,
database files and deleted-but-open files.

______________________________________________________________________

## Q41. What is a deleted-but-open file?

**Answer:**

A file removed from the directory namespace but still held open by a process. Its storage can remain allocated until the
process closes the file descriptor.

______________________________________________________________________

## Q42. What is `systemd`?

**Answer:**

A common Linux initialization and service-management system.

______________________________________________________________________

## Q43. What is `systemctl`?

**Answer:**

A command-line tool used to manage and inspect systemd services.

______________________________________________________________________

## Q44. What is `journalctl`?

**Answer:**

A command-line tool for querying logs stored by the systemd journal.

______________________________________________________________________

## Q45. How would you debug a failed systemd service?

**Answer:**

Start with:

```bash
systemctl status myapp
journalctl -u myapp -n 100
```

Then inspect configuration, command paths, environment, permissions, dependencies and application logs.

______________________________________________________________________

## Q46. What is cron?

**Answer:**

A traditional Linux scheduling mechanism for running commands at specified times or intervals.

______________________________________________________________________

## Q47. Why can a cron job work manually but fail under cron?

**Answer:**

Cron can have a different `PATH`, environment variables, working directory and shell environment. Use explicit paths and
explicitly configure required environment.

______________________________________________________________________

## Q48. Why should services avoid running as root?

**Answer:**

Least privilege reduces the potential impact of application compromise or accidental destructive operations.

______________________________________________________________________

## Q49. Why is `chmod 777` a bad solution?

**Answer:**

It grants excessive permissions to everyone and can hide the underlying ownership/group configuration problem.

______________________________________________________________________

## Q50. Give a senior-level Linux debugging answer.

**Answer:**

"I debug Linux backend incidents layer by layer rather than randomly restarting services. I first establish whether the
process and service are running, then verify listening ports and local connectivity. I inspect recent logs, CPU, memory,
disk and file-descriptor usage, followed by DNS/TCP/HTTP connectivity when dependencies are involved. I verify the
process user and filesystem permissions when access errors occur. For service-managed applications I use systemd and
journalctl, and for scheduled jobs I account for cron's different environment. During remediation I prefer graceful
signals, least privilege and root-cause fixes over destructive commands such as SIGKILL or chmod 777."

______________________________________________________________________

# 106. Scenario-Based Questions

## Scenario 1 — FastAPI Service Is Down

The API suddenly stops responding.

**Answer:**

Use:

```bash
systemctl status myapp
journalctl -u myapp -n 100
ss -lntp | grep :8000
curl -v http://localhost:8000/health
```

Determine whether the issue is:

```text
Process
Service
Port
Application
Dependency
```

before restarting.

______________________________________________________________________

## Scenario 2 — Port 8000 Is Already in Use

The new application cannot start.

**Answer:**

Run:

```bash
ss -lntp | grep :8000
```

Identify the process and determine whether it is an old application instance, another service or an unexpected process.

______________________________________________________________________

## Scenario 3 — Permission Denied

The application cannot write:

```text
/var/log/myapp/app.log
```

**Answer:**

Check:

```bash
ls -ld /var/log/myapp
ls -l /var/log/myapp/app.log
id
```

Verify owner, group and directory permissions. Correct the ownership/permissions rather than using `chmod 777`.

______________________________________________________________________

## Scenario 4 — CPU Suddenly Reaches 100%

**Answer:**

Start with:

```bash
top
```

Identify the process/PID, inspect recent deployments and traffic, and determine whether the workload is CPU-bound, stuck
in a loop or unexpectedly processing excessive work.

______________________________________________________________________

## Scenario 5 — Memory Keeps Increasing

**Answer:**

Check:

```bash
free -h
ps aux --sort=-%mem | head
```

Determine whether the problem is system-wide or isolated to a process. Then investigate application-level memory
retention, caches, large objects, concurrency and dependency behavior.

______________________________________________________________________

## Scenario 6 — Disk Is Full

**Answer:**

Start with:

```bash
df -h
```

Then locate large directories with:

```bash
du -sh /var/*
```

Also investigate deleted-but-open files using tools such as `lsof`.

Do not blindly delete database or application files.

______________________________________________________________________

## Scenario 7 — Database Hostname Does Not Resolve

**Answer:**

Run:

```bash
dig database.internal
```

If DNS fails, investigate DNS configuration. If DNS succeeds, continue to TCP connectivity and application-level
authentication separately.

______________________________________________________________________

## Scenario 8 — API Returns Connection Refused

**Answer:**

Check:

```bash
ss -lntp
curl -v
```

Verify that the target service is listening on the expected interface and port and that network routing/firewall rules
permit the connection.

______________________________________________________________________

## Scenario 9 — Service Keeps Restarting

**Answer:**

Inspect:

```bash
systemctl status myapp
journalctl -u myapp
```

A restart policy can improve availability, but repeated restarts indicate an underlying failure that must be diagnosed.

______________________________________________________________________

## Scenario 10 — Cron Backup Works Manually but Not Automatically

**Answer:**

Check:

- Absolute paths
- `PATH`
- Environment variables
- Working directory
- File permissions
- User executing the cron job
- Cron logs

Cron does not necessarily run with the same environment as an interactive shell.

______________________________________________________________________

# 107. Practice Exercises

## Exercise 1 — Filesystem Navigation

Practice:

```bash
pwd
ls -lah
cd
find
```

Navigate through:

```text
/etc
/var/log
/tmp
/home
/proc
```

Identify what each directory is used for.

______________________________________________________________________

## Exercise 2 — Permissions

Create:

```text
secret.txt
script.sh
```

Set:

```text
secret.txt → 600
script.sh   → 755
```

Verify with:

```bash
ls -l
```

______________________________________________________________________

## Exercise 3 — Users and Groups

Create a test user and group in a disposable Linux environment.

Change ownership of a file and verify access behavior.

______________________________________________________________________

## Exercise 4 — Processes

Run a long-running process.

Find it using:

```bash
ps
pgrep
```

Inspect its PID and terminate it gracefully.

______________________________________________________________________

## Exercise 5 — Signals

Run a test application that handles SIGTERM.

Send:

```bash
kill -TERM <pid>
```

Observe graceful shutdown.

Then understand the difference when using SIGKILL.

______________________________________________________________________

## Exercise 6 — Pipes

Practice:

```bash
ps aux | grep python
```

Then extend it with:

```text
grep
sort
head
tail
```

______________________________________________________________________

## Exercise 7 — Log Analysis

Create a sample log containing:

```text
INFO
WARNING
ERROR
TIMEOUT
```

Use:

```text
grep
awk
sed
```

to extract useful information.

______________________________________________________________________

## Exercise 8 — SSH

Connect to a disposable Linux server using SSH keys.

Practice:

```text
ssh
scp
rsync
```

______________________________________________________________________

## Exercise 9 — Networking

Run a local HTTP service.

Use:

```bash
ss
curl
dig
```

to investigate:

- Listening port
- HTTP response
- DNS resolution

______________________________________________________________________

## Exercise 10 — Disk Investigation

Create large temporary files.

Use:

```bash
df -h
du -sh
```

to identify filesystem and directory usage.

______________________________________________________________________

## Exercise 11 — Memory Investigation

Run a memory-intensive process.

Use:

```bash
free -h
top
ps
```

to identify the process and understand system memory pressure.

______________________________________________________________________

## Exercise 12 — systemd

Create a simple test systemd service.

Practice:

```bash
systemctl start
systemctl stop
systemctl restart
systemctl status
journalctl -u
```

______________________________________________________________________

## Exercise 13 — Cron

Create a cron job that writes a timestamp to a file every minute.

Verify:

- Environment
- Permissions
- Working directory
- Output/errors

______________________________________________________________________

## Exercise 14 — FastAPI Incident Simulation

Run a FastAPI application as a Linux service.

Simulate:

- Wrong port
- Missing environment variable
- Permission problem
- Process crash

Diagnose each issue using only Linux tools.

______________________________________________________________________

## Exercise 15 — Senior Incident Drill

Simulate:

```text
API is unavailable
CPU is high
Disk is 95% full
One dependency is unreachable
```

You must produce a structured diagnosis:

```text
1. Impact
2. Process status
3. Service status
4. Port status
5. Logs
6. CPU
7. Memory
8. Disk
9. Network
10. Root cause
11. Safe mitigation
12. Follow-up prevention
```

______________________________________________________________________

# 108. Quick Revision

| Concept | Key Point |
|---|---|
| `/` | Filesystem root |
| `/etc` | Configuration |
| `/var` | Variable data/logs |
| `/home` | User home directories |
| `/tmp` | Temporary data |
| `/proc` | Process/kernel information |
| Absolute path | Starts from `/` |
| Relative path | Relative to current directory |
| `pwd` | Current directory |
| `ls` | List files |
| `chmod` | Change permissions |
| `chown` | Change ownership |
| `umask` | Default permission mask |
| User | Process/file identity |
| Group | Shared access identity |
| Root | Highly privileged user |
| Process | Running program instance |
| PID | Process identifier |
| Thread | Execution unit within process |
| Zombie | Terminated child awaiting reaping |
| Orphan | Running process whose parent exited |
| SIGTERM | Graceful termination request |
| SIGKILL | Uncatchable forced termination |
| SIGINT | Interrupt |
| Shell | Command interpreter |
| stdout | Standard output |
| stderr | Standard error |
| Pipe | stdout → stdin |
| `grep` | Search/filter text |
| `awk` | Field/text processing |
| `sed` | Stream transformation |
| SSH | Secure remote access |
| `ss` | Socket/network inspection |
| `ip` | Network configuration/inspection |
| `curl` | HTTP/network testing |
| `dig` | DNS testing |
| `df` | Filesystem usage |
| `du` | File/directory usage |
| `free` | Memory information |
| `top` | Live process/resource view |
| `lsof` | Open file/resource inspection |
| systemd | Service management/init |
| `systemctl` | Manage systemd services |
| `journalctl` | Query systemd logs |
| cron | Scheduled commands |
| least privilege | Minimize permissions |
| graceful shutdown | Controlled termination |

______________________________________________________________________

# 109. Completion Checklist

Before moving to File 32, make sure you can explain:

- [ ] Linux filesystem hierarchy
- [ ] `/etc`
- [ ] `/var`
- [ ] `/home`
- [ ] `/tmp`
- [ ] `/proc`
- [ ] Absolute paths
- [ ] Relative paths
- [ ] File types
- [ ] Symbolic links
- [ ] Hard links overview
- [ ] File permissions
- [ ] Read/write/execute semantics
- [ ] Numeric permissions
- [ ] `chmod`
- [ ] `chown`
- [ ] `chgrp`
- [ ] `umask`
- [ ] Users
- [ ] Groups
- [ ] Root
- [ ] `sudo`
- [ ] Processes
- [ ] PIDs
- [ ] `ps`
- [ ] Process trees
- [ ] Process states
- [ ] Zombies
- [ ] Orphans
- [ ] Threads
- [ ] Process vs thread
- [ ] Signals
- [ ] SIGTERM
- [ ] SIGKILL
- [ ] SIGINT
- [ ] SIGHUP
- [ ] SIGSTOP/SIGCONT
- [ ] `kill`
- [ ] Shell
- [ ] Environment variables
- [ ] Exit status
- [ ] `&&`
- [ ] `||`
- [ ] Pipes
- [ ] stdin/stdout/stderr
- [ ] Redirection
- [ ] `/dev/null`
- [ ] `grep`
- [ ] `awk`
- [ ] `sed`
- [ ] `tail`
- [ ] `head`
- [ ] `less`
- [ ] SSH
- [ ] SSH keys
- [ ] `scp`
- [ ] `rsync`
- [ ] Linux networking basics
- [ ] Listening ports
- [ ] `ss`
- [ ] `ip`
- [ ] `curl`
- [ ] `dig`
- [ ] `ping`
- [ ] DNS troubleshooting
- [ ] Disk usage
- [ ] `df`
- [ ] `du`
- [ ] Deleted-but-open files
- [ ] Memory investigation
- [ ] `free`
- [ ] `top`
- [ ] File descriptors
- [ ] `ulimit`
- [ ] systemd
- [ ] `systemctl`
- [ ] Service units
- [ ] Restart policies
- [ ] `journalctl`
- [ ] Logs
- [ ] Log rotation
- [ ] cron
- [ ] Cron environment
- [ ] Production debugging workflow
- [ ] Permission troubleshooting
- [ ] CPU troubleshooting
- [ ] Memory troubleshooting
- [ ] Disk troubleshooting
- [ ] Network troubleshooting
- [ ] Service troubleshooting
- [ ] Graceful remediation

______________________________________________________________________

# 110. Interview Readiness Test

Answer these aloud without looking at the notes:

1. Explain the Linux filesystem hierarchy.
1. What is `/etc`?
1. What is `/var`?
1. What is `/proc`?
1. Absolute vs relative path?
1. Symbolic link vs hard link?
1. Explain Linux file permissions.
1. What does `755` mean?
1. What does `644` mean?
1. What does `600` mean?
1. `chmod` vs `chown`?
1. What is `umask`?
1. Why should backend services avoid root?
1. What is a process?
1. What is a PID?
1. Process vs thread?
1. What is a zombie process?
1. Zombie vs orphan?
1. What is SIGTERM?
1. SIGTERM vs SIGKILL?
1. What does Ctrl+C send?
1. What does `kill` actually do?
1. What is a shell?
1. What are stdin, stdout and stderr?
1. What does `|` do?
1. What does `>` do?
1. What does `2>&1` do?
1. What is `grep`?
1. What is `awk`?
1. What is `sed`?
1. grep vs awk vs sed?
1. What is SSH?
1. How do SSH keys work conceptually?
1. How do you check which process is listening on port 8000?
1. How do you test an HTTP endpoint from a Linux server?
1. What is `dig`?
1. Does ping prove an HTTP service is reachable?
1. `df` vs `du`?
1. How do you debug "No space left on device"?
1. What is a deleted-but-open file?
1. How do you inspect memory usage?
1. How do you identify the process consuming the most memory?
1. How do you investigate high CPU?
1. What is a file descriptor?
1. What causes "Too many open files"?
1. What is systemd?
1. What does `systemctl status` show?
1. How do you inspect systemd service logs?
1. What is `journalctl`?
1. What is cron?
1. Why can cron behave differently from an interactive shell?
1. How would you debug a FastAPI service that is down?
1. How would you debug a port conflict?
1. How would you debug permission denied?
1. How would you debug high CPU?
1. How would you debug high memory?
1. How would you debug a full disk?
1. How would you debug DNS failure?
1. How would you debug connection refused?
1. Why is `chmod 777` usually wrong?
1. Why prefer SIGTERM over SIGKILL?
1. How would you safely investigate a production incident?
1. Give a senior-level Linux debugging workflow.

______________________________________________________________________

# 111. Final Senior Interview Scenario

You are on call for a Python backend running on Linux.

At 2:00 AM, monitoring reports:

```text
API latency increased
Some requests are failing
CPU = 95%
Memory = 88%
Disk = 92%
```

The application is managed by systemd.

A strong investigation should proceed systematically:

### Step 1 — Service

```bash
systemctl status myapp
```

### Step 2 — Logs

```bash
journalctl -u myapp --since "30 minutes ago"
```

### Step 3 — Processes

```bash
ps aux
top
```

### Step 4 — Port

```bash
ss -lntp
```

### Step 5 — Local HTTP

```bash
curl -v http://localhost:8000/health
```

### Step 6 — Memory

```bash
free -h
ps aux --sort=-%mem | head
```

### Step 7 — Disk

```bash
df -h
du -sh /var/*
```

### Step 8 — Dependency Network

Use:

```bash
dig
curl
ss
```

to distinguish DNS, TCP and HTTP failures.

### Step 9 — Recent Changes

Check:

```text
Deployment
Configuration
Traffic
Dependencies
Database behavior
```

### Step 10 — Safe Mitigation

Choose the least disruptive mitigation based on evidence.

Do not immediately:

```bash
kill -9
chmod 777
rm -rf
```

A strong senior engineer first determines the failure mode and then applies a controlled mitigation.

______________________________________________________________________

# 112. Final Takeaways

For a Python backend engineer, Linux preparation should focus on being able to answer:

> **What is happening to my application at the operating-system level?**

You should be able to move from:

```text
User reports API failure
```

to:

```text
Service
→ Process
→ Port
→ Logs
→ CPU
→ Memory
→ Disk
→ Network
→ Permissions
→ Dependency
→ Root cause
```

That debugging mindset is more valuable in a senior backend interview than memorizing every Linux command.

______________________________________________________________________

**Previous:** [30. Docker](./30-docker.md)

**Next:** [32. Production Debugging & Incident Response](./32-production-debugging.md)

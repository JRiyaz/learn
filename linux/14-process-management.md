# Linux Complete Interview & Production Course

# File 14 — Process Management

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Process Management
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 13 — Regular Expressions

______________________________________________________________________

# Table of Contents

1. Introduction
1. What is a Process?
1. Program vs Process
1. Process Lifecycle
1. Process States
1. Process Identifiers
1. Foreground and Background Processes
1. Viewing Processes
1. Managing Processes
1. Signals
1. Job Control
1. Process Priority
1. Daemons
1. Zombie and Orphan Processes
1. Process Tree
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

Every application running on Linux is a **process**.

Examples:

- Python application
- FastAPI server
- PostgreSQL
- Redis
- Nginx
- Docker
- VS Code
- Chrome

Linux is a **multitasking operating system**, capable of running thousands of processes simultaneously.

Understanding process management is essential for:

- Backend Engineers
- DevOps Engineers
- SREs
- Linux Administrators

Almost every production issue eventually involves processes.

______________________________________________________________________

# 2. What is a Process?

A **process** is a program that is currently executing.

Example:

Python file:

```text
app.py
```

Running:

```bash
python3 app.py
```

Before execution:

```
Program
```

After execution:

```
Process
```

______________________________________________________________________

Every process has:

- Process ID (PID)
- Parent Process ID (PPID)
- Owner
- Memory allocation
- CPU usage
- Priority
- Current state

______________________________________________________________________

# 3. Program vs Process

| Program | Process |
|----------|----------|
| Static file on disk | Running instance |
| Passive | Active |
| No CPU usage | Uses CPU |
| No memory allocation | Allocated memory |
| Example: `python3` | Example: `python3 app.py` |

______________________________________________________________________

One program can create many processes.

Example:

```
python app1.py

python app2.py

python app3.py
```

Three processes.

______________________________________________________________________

# 4. Process Lifecycle

```
Program

↓

Created

↓

Ready

↓

Running

↓

Waiting

↓

Running

↓

Terminated
```

______________________________________________________________________

Explanation

### New

The process is created.

______________________________________________________________________

### Ready

Waiting for CPU.

______________________________________________________________________

### Running

Currently executing.

______________________________________________________________________

### Waiting

Waiting for:

- Disk
- Network
- User input
- Sleep timer

______________________________________________________________________

### Terminated

Execution completed.

______________________________________________________________________

# 5. Process States

View process state:

```bash
ps aux
```

Common states:

| State | Meaning |
|--------|----------|
| R | Running |
| S | Sleeping |
| D | Uninterruptible Sleep |
| T | Stopped |
| Z | Zombie |

______________________________________________________________________

### Running (R)

Currently using CPU.

______________________________________________________________________

### Sleeping (S)

Waiting for an event.

Most Linux processes spend the majority of their lifetime here.

______________________________________________________________________

### Uninterruptible Sleep (D)

Waiting for I/O operations such as disk access.

These processes cannot easily be interrupted.

______________________________________________________________________

### Stopped (T)

Paused by:

```
Ctrl + Z
```

or debugging tools.

______________________________________________________________________

### Zombie (Z)

Finished execution,

but the parent has not yet collected its exit status.

We'll discuss this in detail later.

______________________________________________________________________

# 6. Process Identifiers

Every process has a unique Process ID.

Display current shell PID.

```bash
echo $$
```

Example:

```text
24851
```

______________________________________________________________________

Display parent PID.

```bash
echo $PPID
```

______________________________________________________________________

Find process IDs.

```bash
pgrep python
```

______________________________________________________________________

List processes.

```bash
ps
```

______________________________________________________________________

# 7. Foreground and Background Processes

## Foreground

Runs in the terminal.

Example:

```bash
python app.py
```

Terminal remains occupied.

______________________________________________________________________

## Background

Runs independently.

```bash
python app.py &
```

Terminal is immediately available.

______________________________________________________________________

View jobs.

```bash
jobs
```

Example:

```text
[1]+ Running python app.py &
```

______________________________________________________________________

Bring back.

```bash
fg
```

______________________________________________________________________

Send to background.

```
Ctrl + Z

↓

bg
```

______________________________________________________________________

# 8. Viewing Processes

## ps

Current shell processes.

```bash
ps
```

______________________________________________________________________

All processes.

```bash
ps -e
```

______________________________________________________________________

Detailed information.

```bash
ps -ef
```

______________________________________________________________________

BSD format.

```bash
ps aux
```

Columns include:

- USER
- PID
- CPU
- MEM
- VSZ
- RSS
- STAT
- START
- TIME
- COMMAND

______________________________________________________________________

## top

Real-time process viewer.

```bash
top
```

Displays:

- CPU usage
- Memory usage
- Running processes
- Load average

______________________________________________________________________

Quit:

```
q
```

______________________________________________________________________

## htop

Improved version of `top`.

```bash
htop
```

Advantages:

- Interactive
- Mouse support
- Easier filtering
- Better visualization

Install:

```bash
sudo apt install htop
```

______________________________________________________________________

## pgrep

Find processes by name.

```bash
pgrep nginx
```

______________________________________________________________________

## pidof

Display PID.

```bash
pidof docker
```

______________________________________________________________________

# 9. Managing Processes

## kill

Terminate a process.

```bash
kill PID
```

Example:

```bash
kill 2458
```

This sends **SIGTERM** by default.

______________________________________________________________________

## kill -9

Force termination.

```bash
kill -9 PID
```

Equivalent to:

```
SIGKILL
```

Use only when normal termination fails.

______________________________________________________________________

## killall

Kill by process name.

```bash
killall python3
```

______________________________________________________________________

## pkill

Kill using patterns.

```bash
pkill nginx
```

______________________________________________________________________

## nice

Start with lower priority.

```bash
nice -n 10 python app.py
```

______________________________________________________________________

## renice

Change priority.

```bash
sudo renice 5 -p 2458
```

______________________________________________________________________

# 10. Signals

Signals are software interrupts.

They notify processes that an event has occurred.

Common signals:

| Signal | Number | Purpose |
|----------|--------|----------|
| SIGTERM | 15 | Graceful termination |
| SIGKILL | 9 | Immediate termination |
| SIGINT | 2 | Ctrl + C |
| SIGSTOP | 19 | Stop process |
| SIGCONT | 18 | Continue process |
| SIGHUP | 1 | Reload configuration |

______________________________________________________________________

Send signal.

```bash
kill -15 PID
```

______________________________________________________________________

Force.

```bash
kill -9 PID
```

______________________________________________________________________

Reload Nginx.

```bash
kill -HUP PID
```

Many services use `SIGHUP` to reload configuration without restarting.

______________________________________________________________________

# 11. Job Control

Start in background.

```bash
sleep 100 &
```

______________________________________________________________________

List jobs.

```bash
jobs
```

______________________________________________________________________

Suspend.

```
Ctrl + Z
```

______________________________________________________________________

Resume background.

```bash
bg
```

______________________________________________________________________

Resume foreground.

```bash
fg
```

______________________________________________________________________

# 12. Process Priority

Linux scheduler uses priorities.

Nice values:

```
-20

Highest Priority

↓

19

Lowest Priority
```

Default:

```
0
```

Lower nice value

↓

Higher scheduling priority.

______________________________________________________________________

Display nice value.

```bash
ps -o pid,ni,comm
```

______________________________________________________________________

# 13. Daemons

A daemon is a background service.

Examples:

- sshd
- nginx
- dockerd
- systemd
- cron

Characteristics:

- Starts automatically
- Runs continuously
- No interactive terminal
- Waits for requests

______________________________________________________________________

List daemon example.

```bash
ps aux | grep sshd
```

______________________________________________________________________

# 14. Zombie and Orphan Processes

## Zombie Process

```
Child finished

↓

Parent didn't collect status

↓

Zombie
```

State:

```
Z
```

Consumes almost no resources,

but occupies a process table entry.

______________________________________________________________________

## Orphan Process

```
Parent exits

↓

Child still running

↓

Adopted by init/systemd
```

Orphan processes continue running normally.

______________________________________________________________________

Display zombies.

```bash
ps aux | grep Z
```

______________________________________________________________________

# 15. Process Tree

View process hierarchy.

```bash
pstree
```

Example:

```
systemd
├── sshd
├── nginx
├── docker
└── python
```

Install if necessary:

```bash
sudo apt install psmisc
```

______________________________________________________________________

# 16. Production Examples

## Find Python Processes

```bash
pgrep python
```

______________________________________________________________________

## Monitor CPU Usage

```bash
top
```

______________________________________________________________________

## Kill Hung Process

```bash
kill PID
```

______________________________________________________________________

## Force Kill

```bash
kill -9 PID
```

______________________________________________________________________

## Restart Job

```bash
pkill gunicorn
```

______________________________________________________________________

## Reload Nginx Configuration

```bash
kill -HUP $(pidof nginx)
```

______________________________________________________________________

## View Process Tree

```bash
pstree
```

______________________________________________________________________

# 17. Common Mistakes

❌ Using `kill -9` immediately instead of trying `SIGTERM` first.

______________________________________________________________________

❌ Killing the wrong process because the PID was not verified.

______________________________________________________________________

❌ Forgetting that `Ctrl + Z` suspends a process instead of terminating it.

______________________________________________________________________

❌ Assuming zombie processes consume CPU or memory.

They primarily consume a process table entry.

______________________________________________________________________

❌ Setting very high scheduling priority unnecessarily.

______________________________________________________________________

# 18. Best Practices

- Use `SIGTERM` before `SIGKILL`.
- Verify the PID before terminating a process.
- Use `top` or `htop` during performance investigations.
- Monitor zombie processes on long-running servers.
- Understand the difference between jobs and system processes.
- Use `nice` and `renice` sparingly.

______________________________________________________________________

# Interview Questions

## Q1. What is the difference between a program and a process?

**Answer**

A program is a static executable stored on disk, while a process is a running instance of that program with allocated
CPU time, memory, and other system resources.

______________________________________________________________________

## Q2. What is the difference between `kill` and `kill -9`?

**Answer**

`kill` sends `SIGTERM` (signal 15), allowing the application to shut down gracefully. `kill -9` sends `SIGKILL` (signal
9), which immediately terminates the process without giving it an opportunity to clean up resources.

______________________________________________________________________

## Q3. What is a zombie process?

**Answer**

A zombie process has completed execution but remains in the process table because its parent process has not yet
collected its exit status using a system call such as `wait()`.

______________________________________________________________________

## Q4. What is an orphan process?

**Answer**

An orphan process is a child process whose parent has exited. It is automatically adopted by `init` or `systemd`,
allowing it to continue running.

______________________________________________________________________

## Q5. What is a daemon?

**Answer**

A daemon is a long-running background service that starts automatically, runs without an interactive terminal, and
provides system or application functionality such as SSH, web serving, or scheduling.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Display:

- Current shell PID
- Parent PID

______________________________________________________________________

## Exercise 2

Start a long-running process using:

```bash
sleep 300
```

Suspend it.

Resume it.

Run it in the background.

______________________________________________________________________

## Exercise 3

Display:

```bash
ps
ps -ef
ps aux
```

Compare their outputs.

______________________________________________________________________

## Exercise 4

Monitor your system using:

```bash
top
htop
```

______________________________________________________________________

## Exercise 5

Create a background process and terminate it using:

- `kill`
- `killall`
- `pkill`

______________________________________________________________________

## Exercise 6

Display the process tree using:

```bash
pstree
```

______________________________________________________________________

# Cheat Sheet

## View Processes

```bash
ps
ps -ef
ps aux
top
htop
pgrep
pidof
pstree
```

______________________________________________________________________

## Manage Processes

```bash
kill
kill -9
killall
pkill
```

______________________________________________________________________

## Job Control

```bash
jobs
fg
bg
```

______________________________________________________________________

## Priority

```bash
nice
renice
```

______________________________________________________________________

## Signals

```text
SIGTERM
SIGKILL
SIGINT
SIGSTOP
SIGCONT
SIGHUP
```

______________________________________________________________________

# Summary

In this chapter, you learned how Linux represents running programs as processes, how processes move through different
lifecycle states, how to inspect and manage them using commands like `ps`, `top`, `htop`, `kill`, `pgrep`, and `pstree`,
and how signals, job control, priorities, daemons, zombie processes, and orphan processes work. These concepts are
fundamental for diagnosing and managing applications in production Linux environments.

______________________________________________________________________

## Next

[Systemd and Service Management](15-systemd-and-service-management.md)

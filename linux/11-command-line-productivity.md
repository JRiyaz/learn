# Linux Complete Interview & Production Course

# File 11 — Command Line Productivity

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Shell & Command Line
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 10 — Input, Output, Redirection, Pipes, and Tee

______________________________________________________________________

# Table of Contents

1. Introduction
1. Why Command Line Productivity Matters
1. Wildcards (Globbing)
1. Brace Expansion
1. Command History
1. Keyboard Shortcuts
1. Auto Completion
1. Command Help System
1. The `watch` Command
1. The `time` Command
1. The `sleep` Command
1. The `timeout` Command
1. The `yes` Command
1. The `seq` Command
1. `echo` vs `printf`
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

One of the biggest differences between a beginner and an experienced Linux engineer is **speed**.

Experienced engineers rarely type long commands repeatedly.

Instead, they rely on:

- Shell expansion
- Keyboard shortcuts
- History search
- Auto-completion
- Productivity utilities

Mastering these features can save hours every week.

______________________________________________________________________

# 2. Why Command Line Productivity Matters

Consider these two approaches.

### Without Productivity Features

```bash
cd /home/riyaz/projects/backend-service/src/controllers
```

Typed every single time.

______________________________________________________________________

### With Productivity Features

```bash
cd ~/projects/back<TAB>
```

Completed automatically.

Or simply:

```text
Ctrl + R
```

to search command history.

The second approach is faster, less error-prone, and commonly used by experienced Linux users.

______________________________________________________________________

# 3. Wildcards (Globbing)

Wildcards allow the shell to match filenames.

They are expanded **before** the command is executed.

______________________________________________________________________

## `*` (Match Everything)

Matches zero or more characters.

Example:

```bash
ls *.py
```

Matches:

```text
app.py
main.py
utils.py
```

______________________________________________________________________

Delete all log files.

```bash
rm *.log
```

______________________________________________________________________

Copy all Python files.

```bash
cp *.py backup/
```

______________________________________________________________________

## `?` (Single Character)

Matches exactly one character.

Example:

```bash
ls file?.txt
```

Matches:

```text
file1.txt
file2.txt
fileA.txt
```

Does **not** match:

```text
file10.txt
```

______________________________________________________________________

## Character Sets

```bash
ls file[123].txt
```

Matches:

```text
file1.txt
file2.txt
file3.txt
```

______________________________________________________________________

Range

```bash
ls file[a-z].txt
```

______________________________________________________________________

Negation

```bash
ls file[!0-9].txt
```

______________________________________________________________________

# 4. Brace Expansion

Brace expansion creates combinations before execution.

Example:

```bash
mkdir project/{src,tests,docs}
```

Creates:

```text
project/
├── docs
├── src
└── tests
```

______________________________________________________________________

Create multiple files.

```bash
touch file{1..5}.txt
```

Creates:

```text
file1.txt
file2.txt
file3.txt
file4.txt
file5.txt
```

______________________________________________________________________

Alphabet

```bash
echo {a..f}
```

Output:

```text
a b c d e f
```

______________________________________________________________________

Numbers

```bash
echo {1..10}
```

______________________________________________________________________

Nested braces

```bash
mkdir {backend,frontend}/{src,test}
```

Creates:

```text
backend/
├── src
└── test

frontend/
├── src
└── test
```

______________________________________________________________________

# 5. Command History

View history.

```bash
history
```

______________________________________________________________________

Search interactively.

```
Ctrl + R
```

Type:

```
docker
```

The shell searches previous Docker commands.

______________________________________________________________________

Repeat previous command.

```bash
!!
```

______________________________________________________________________

Repeat previous command as root.

```bash
sudo !!
```

Very useful.

Example:

```bash
apt update
```

Oops.

Forgot `sudo`.

Simply run:

```bash
sudo !!
```

______________________________________________________________________

Repeat command by number.

```bash
!450
```

______________________________________________________________________

Repeat previous `git` command.

```bash
!git
```

______________________________________________________________________

# 6. Keyboard Shortcuts

| Shortcut | Action |
|----------|---------|
| Ctrl + A | Beginning of line |
| Ctrl + E | End of line |
| Ctrl + U | Delete to beginning |
| Ctrl + K | Delete to end |
| Ctrl + W | Delete previous word |
| Ctrl + L | Clear screen |
| Ctrl + C | Interrupt process |
| Ctrl + D | Logout / EOF |
| Ctrl + Z | Suspend process |
| Ctrl + R | Search history |

______________________________________________________________________

## Ctrl + C

Stops the running process.

______________________________________________________________________

## Ctrl + Z

Suspends the process.

Resume in foreground:

```bash
fg
```

Resume in background:

```bash
bg
```

We'll revisit job control in the Process Management module.

______________________________________________________________________

# 7. Auto Completion

Press:

```
TAB
```

Example:

```bash
cd Doc<TAB>
```

Expands to:

```bash
cd Documents
```

______________________________________________________________________

Double TAB

Shows available completions.

______________________________________________________________________

Program completion.

```bash
git ch<TAB>
```

Expands to:

```bash
git checkout
```

(if shell completion is installed)

______________________________________________________________________

# 8. Command Help System

## man

Display manual.

```bash
man grep
```

Navigation:

| Key | Action |
|-----|---------|
| Space | Next page |
| b | Previous page |
| / | Search |
| q | Quit |

______________________________________________________________________

## info

GNU documentation.

```bash
info ls
```

______________________________________________________________________

## help

Shell built-in help.

```bash
help cd
```

______________________________________________________________________

## --help

Quick reference.

```bash
grep --help
```

______________________________________________________________________

## apropos

Search manual pages.

```bash
apropos copy
```

______________________________________________________________________

## whatis

Short command description.

```bash
whatis grep
```

______________________________________________________________________

# 9. The `watch` Command

Runs a command repeatedly.

Example:

```bash
watch date
```

Updates every 2 seconds.

______________________________________________________________________

Watch disk usage.

```bash
watch df -h
```

______________________________________________________________________

Watch Docker containers.

```bash
watch docker ps
```

______________________________________________________________________

Watch Kubernetes pods.

```bash
watch kubectl get pods
```

______________________________________________________________________

Refresh every second.

```bash
watch -n 1 "ps aux"
```

______________________________________________________________________

# 10. The `time` Command

Measures execution time.

Example:

```bash
time python app.py
```

Output:

```text
real

user

sys
```

______________________________________________________________________

Time a copy operation.

```bash
time cp large.iso backup/
```

______________________________________________________________________

Useful for:

- Performance analysis
- Benchmarking
- Comparing algorithms

______________________________________________________________________

# 11. The `sleep` Command

Pause execution.

```bash
sleep 5
```

Waits five seconds.

______________________________________________________________________

Minutes

```bash
sleep 2m
```

______________________________________________________________________

Hours

```bash
sleep 1h
```

______________________________________________________________________

Used extensively in scripts and automation.

______________________________________________________________________

# 12. The `timeout` Command

Stop a command after a specified duration.

```bash
timeout 10 ping google.com
```

Stops after:

```
10 seconds
```

______________________________________________________________________

Useful for:

- Automation
- CI/CD
- Preventing hanging commands

______________________________________________________________________

# 13. The `yes` Command

Continuously prints text.

```bash
yes
```

Output:

```text
y
y
y
y
...
```

______________________________________________________________________

Custom text.

```bash
yes hello
```

______________________________________________________________________

Automatically answer prompts.

```bash
yes | rm -i *.tmp
```

Be careful with this command.

______________________________________________________________________

# 14. The `seq` Command

Generate sequences.

```bash
seq 5
```

Output:

```text
1
2
3
4
5
```

______________________________________________________________________

Custom step.

```bash
seq 2 2 10
```

Output:

```text
2
4
6
8
10
```

______________________________________________________________________

Useful in shell loops.

______________________________________________________________________

# 15. `echo` vs `printf`

## echo

Simple output.

```bash
echo Hello
```

______________________________________________________________________

Supports variables.

```bash
echo $HOME
```

______________________________________________________________________

## printf

More control.

```bash
printf "Name: %s\n" "Riyaz"
```

Output:

```text
Name: Riyaz
```

______________________________________________________________________

Numbers.

```bash
printf "%04d\n" 7
```

Output:

```text
0007
```

______________________________________________________________________

Formatting tables.

```bash
printf "%-15s %s\n" Name Score
```

Output:

```text
Name            Score
```

Unlike `echo`, `printf` provides predictable formatting and is preferred in shell scripts.

______________________________________________________________________

# 16. Production Examples

## Monitor CPU Usage

```bash
watch -n 2 top
```

______________________________________________________________________

## Benchmark Compression

```bash
time tar -czf backup.tar.gz project/
```

______________________________________________________________________

## Generate 100 Test Files

```bash
touch file{1..100}.txt
```

______________________________________________________________________

## Create Microservice Structure

```bash
mkdir -p services/{user,order,payment}/{src,test}
```

______________________________________________________________________

## Automatically Confirm Package Installation

```bash
yes | sudo apt install package-name
```

Use only when you understand the prompts being answered.

______________________________________________________________________

## Limit Command Runtime

```bash
timeout 60 python long_running_script.py
```

______________________________________________________________________

# 17. Common Mistakes

❌ Using `rm *.log` without verifying the wildcard expansion.

______________________________________________________________________

❌ Forgetting that shell expansion happens before the command executes.

______________________________________________________________________

❌ Relying on `yes` without understanding the prompts.

______________________________________________________________________

❌ Using `echo` for complex formatted output instead of `printf`.

______________________________________________________________________

❌ Leaving `watch` running unnecessarily.

______________________________________________________________________

# 18. Best Practices

- Use TAB completion instead of typing long paths.
- Learn keyboard shortcuts to improve efficiency.
- Use `printf` in scripts requiring formatted output.
- Verify wildcard expansions before destructive commands.
- Use `watch` for monitoring rather than repeatedly executing commands manually.
- Use `timeout` for automation involving potentially long-running commands.

______________________________________________________________________

# Interview Questions

## Q1. What is shell globbing?

**Answer**

Shell globbing is the process where the shell expands wildcard patterns such as `*`, `?`, and character ranges into
matching filenames before executing the command.

______________________________________________________________________

## Q2. What is the difference between wildcard expansion and brace expansion?

**Answer**

Wildcard expansion matches existing filenames in the filesystem. Brace expansion generates text combinations before
command execution and does not depend on existing files.

______________________________________________________________________

## Q3. What is the purpose of the `watch` command?

**Answer**

`watch` repeatedly executes a command at regular intervals, making it useful for monitoring changing system information
such as processes, disk usage, or Kubernetes resources.

______________________________________________________________________

## Q4. Why is `printf` preferred over `echo` in shell scripts?

**Answer**

`printf` provides consistent and predictable formatting across environments, supports formatted output, and avoids the
portability issues associated with different implementations of `echo`.

______________________________________________________________________

## Q5. What does `sudo !!` do?

**Answer**

It reruns the previous command with `sudo`, which is useful when a command fails because it required administrative
privileges.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Create the following directory structure using brace expansion:

```text
project/
├── backend/
│   ├── src/
│   └── test/
└── frontend/
    ├── src/
    └── test/
```

______________________________________________________________________

## Exercise 2

Generate:

- 20 files
- 26 alphabet characters
- Even numbers from 2 to 20

using brace expansion or `seq`.

______________________________________________________________________

## Exercise 3

Practice:

- `Ctrl + A`
- `Ctrl + E`
- `Ctrl + R`
- `Ctrl + U`
- `Ctrl + W`

______________________________________________________________________

## Exercise 4

Monitor:

- Memory usage
- Disk usage
- Running processes

using `watch`.

______________________________________________________________________

## Exercise 5

Compare the execution time of two different commands using `time`.

______________________________________________________________________

## Exercise 6

Format output using `printf`.

______________________________________________________________________

# Cheat Sheet

## Wildcards

```bash
*
?
[]
[!]
```

______________________________________________________________________

## Brace Expansion

```bash
{1..10}
{a..z}
{dir1,dir2}
```

______________________________________________________________________

## Help

```bash
man
info
help
apropos
whatis
--help
```

______________________________________________________________________

## Productivity

```bash
watch
time
sleep
timeout
yes
seq
```

______________________________________________________________________

## Output

```bash
echo
printf
```

______________________________________________________________________

## History

```bash
history
!!
!number
!command
Ctrl + R
```

______________________________________________________________________

# Summary

In this chapter, you learned productivity techniques that experienced Linux users rely on daily, including shell
globbing, brace expansion, command history, keyboard shortcuts, auto-completion, Linux help systems, and utilities such
as `watch`, `time`, `sleep`, `timeout`, `yes`, `seq`, `echo`, and `printf`. These skills improve speed, reduce errors,
and make command-line work significantly more efficient.

______________________________________________________________________

## Next

[Text Processing Commands](12-text-processing-commands.md)

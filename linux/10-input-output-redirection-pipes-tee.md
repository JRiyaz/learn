# Linux Complete Interview & Production Course

# File 10 — Input, Output, Redirection, Pipes, and Tee

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Shell & Command Line
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 09 — Bash Shell and Environment

______________________________________________________________________

# Table of Contents

1. Introduction
1. Standard Input, Output, and Error
1. File Descriptors
1. Output Redirection
1. Input Redirection
1. Error Redirection
1. Redirecting Both Output and Errors
1. Appending Output
1. The `/dev/null` Device
1. Pipes
1. The `tee` Command
1. The `xargs` Command
1. Combining Pipes and Redirection
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

One of the biggest strengths of Linux is that small commands can be combined to perform powerful tasks.

Instead of writing large programs, Linux encourages building pipelines.

Example:

```bash
cat access.log | grep "ERROR" | sort | uniq
```

Each command performs a single task.

Together, they solve a complex problem.

Understanding input, output, pipes, and redirection is essential for:

- Backend Engineers
- DevOps Engineers
- SREs
- Platform Engineers
- Linux Administrators

______________________________________________________________________

# 2. Standard Input, Output, and Error

Every Linux program starts with three communication channels.

| File Descriptor | Name | Purpose |
|----------------:|------|----------|
| 0 | stdin | Standard Input |
| 1 | stdout | Standard Output |
| 2 | stderr | Standard Error |

Think of them as three open files that every process automatically receives.

```
Keyboard
      │
      ▼
stdin (0)

Program

stdout (1) ─────► Terminal

stderr (2) ─────► Terminal
```

______________________________________________________________________

# Example

```bash
echo "Hello"
```

Output

```
Hello
```

The text is written to:

```
stdout
```

______________________________________________________________________

If you try:

```bash
cat missing.txt
```

Output

```
cat: missing.txt: No such file or directory
```

This message is written to:

```
stderr
```

not stdout.

______________________________________________________________________

# 3. File Descriptors

Linux represents each stream with a number.

```
0

↓

stdin

1

↓

stdout

2

↓

stderr
```

You can redirect them independently.

______________________________________________________________________

# 4. Output Redirection

Normally,

stdout appears on the terminal.

```
Program

↓

Terminal
```

Redirect it into a file.

```bash
echo "Hello Linux" > hello.txt
```

Instead of printing,

Linux creates:

```
hello.txt
```

Contents

```
Hello Linux
```

______________________________________________________________________

Overwrite existing file

```bash
date > output.txt
```

Running again replaces the previous contents.

______________________________________________________________________

# 5. Input Redirection

Normally,

programs read from the keyboard.

```
Keyboard

↓

stdin
```

Redirect input from a file instead.

```bash
sort < names.txt
```

Linux reads:

```
names.txt
```

instead of waiting for keyboard input.

______________________________________________________________________

# 6. Error Redirection

Redirect only errors.

```bash
cat missing.txt 2> error.log
```

Terminal

↓

No error displayed.

Instead:

```
error.log
```

contains

```
No such file...
```

______________________________________________________________________

# Append Errors

```bash
cat missing.txt 2>> error.log
```

______________________________________________________________________

# 7. Redirecting Both Output and Errors

Example

```bash
command > output.log 2> error.log
```

stdout

↓

output.log

stderr

↓

error.log

______________________________________________________________________

Redirect both together

```bash
command > output.log 2>&1
```

Explanation

```
2

↓

stderr

&1

↓

Send stderr to wherever stdout goes
```

______________________________________________________________________

Modern Bash

```bash
command &> output.log
```

Both streams go into one file.

______________________________________________________________________

Append both

```bash
command &>> output.log
```

______________________________________________________________________

# 8. Appending Output

Overwrite

```bash
echo "Hello" > file.txt
```

Append

```bash
echo "World" >> file.txt
```

Result

```
Hello

World
```

______________________________________________________________________

# 9. The `/dev/null` Device

Linux provides a special device.

```
/dev/null
```

Anything written here disappears forever.

Think of it as a black hole.

______________________________________________________________________

Ignore output

```bash
command > /dev/null
```

______________________________________________________________________

Ignore errors

```bash
command 2> /dev/null
```

______________________________________________________________________

Ignore everything

```bash
command > /dev/null 2>&1
```

or

```bash
command &> /dev/null
```

______________________________________________________________________

# When is it Useful?

Running scheduled scripts.

Ignoring expected errors.

Suppressing noisy output.

Automation.

______________________________________________________________________

# 10. Pipes

Pipe operator

```bash
|
```

takes the stdout of one command and sends it to the stdin of another.

```
Command A

↓

stdout

↓

Pipe

↓

stdin

↓

Command B
```

______________________________________________________________________

Example

```bash
ls | sort
```

______________________________________________________________________

Count files

```bash
ls | wc -l
```

______________________________________________________________________

Search log

```bash
cat access.log | grep ERROR
```

______________________________________________________________________

Remove duplicates

```bash
cat users.txt | sort | uniq
```

______________________________________________________________________

Count unique entries

```bash
cat users.txt | sort | uniq -c
```

______________________________________________________________________

Find largest files

```bash
du -sh * | sort -h
```

______________________________________________________________________

# Why Pipes Matter

Linux philosophy

```
Small programs

↓

Combined

↓

Powerful workflows
```

______________________________________________________________________

# 11. The `tee` Command

Normally,

redirecting output to a file hides it from the terminal.

Example

```bash
echo Hello > file.txt
```

Nothing appears on screen.

______________________________________________________________________

`tee`

writes to:

- Terminal
- File

simultaneously.

Example

```bash
echo Hello | tee file.txt
```

Output

```
Hello
```

and

```
file.txt
```

contains

```
Hello
```

______________________________________________________________________

Append

```bash
echo World | tee -a file.txt
```

______________________________________________________________________

# Production Example

Save Docker logs.

```bash
docker logs app | tee logs.txt
```

Watch logs while also saving them.

______________________________________________________________________

# 12. The `xargs` Command

`xargs`

takes input and converts it into command-line arguments.

Example

Without xargs

```bash
rm file1 file2 file3
```

______________________________________________________________________

With xargs

```bash
cat files.txt | xargs rm
```

Contents

```
file1

file2

file3
```

______________________________________________________________________

Find and delete logs

```bash
find . -name "*.log" | xargs rm
```

Safer version

```bash
find . -name "*.log" -print0 | xargs -0 rm
```

Supports filenames containing spaces.

______________________________________________________________________

Install packages

```bash
cat packages.txt | xargs sudo apt install -y
```

______________________________________________________________________

# 13. Combining Pipes and Redirection

Example

```bash
cat app.log \
| grep ERROR \
| sort \
| uniq -c \
| tee errors.txt
```

Workflow

```
Read Log

↓

Filter Errors

↓

Sort

↓

Count

↓

Save

↓

Display
```

______________________________________________________________________

Find Python files

```bash
find . -name "*.py" \
| sort \
| tee python-files.txt
```

______________________________________________________________________

Count running Python processes

```bash
ps aux \
| grep python \
| wc -l
```

______________________________________________________________________

Search system logs

```bash
journalctl \
| grep nginx
```

______________________________________________________________________

# 14. Production Examples

## Monitor Nginx Errors

```bash
tail -f /var/log/nginx/error.log \
| grep ERROR
```

______________________________________________________________________

## Save Kubernetes Logs

```bash
kubectl logs pod-name \
| tee pod.log
```

______________________________________________________________________

## Find Large Files

```bash
find . -size +500M \
| tee large-files.txt
```

______________________________________________________________________

## Count HTTP Status Codes

```bash
cat access.log \
| awk '{print $9}' \
| sort \
| uniq -c
```

______________________________________________________________________

## Remove Old Cache Files

```bash
find cache -name "*.tmp" \
| xargs rm
```

______________________________________________________________________

## Ignore Command Output

```bash
python cleanup.py > /dev/null 2>&1
```

Useful for cron jobs.

______________________________________________________________________

# 15. Common Mistakes

❌ Using `>` instead of `>>` and accidentally overwriting files.

______________________________________________________________________

❌ Assuming stderr is redirected with stdout automatically.

It is not.

______________________________________________________________________

❌ Forgetting to handle filenames with spaces when using `xargs`.

______________________________________________________________________

❌ Using unnecessary `cat`.

Instead of:

```bash
cat file.txt | grep hello
```

Prefer:

```bash
grep hello file.txt
```

unless the pipeline specifically benefits from `cat`.

______________________________________________________________________

❌ Redirecting output before verifying the command.

______________________________________________________________________

# 16. Best Practices

- Prefer pipes over temporary files.
- Use `tee` when you need to both view and save output.
- Redirect errors separately during troubleshooting.
- Use `/dev/null` only when intentionally suppressing output.
- Combine small commands instead of writing large shell scripts for simple tasks.
- Use `find ... -print0 | xargs -0` for filenames that may contain spaces.

______________________________________________________________________

# Interview Questions

## Q1. What is the difference between stdout and stderr?

**Answer**

`stdout` (file descriptor 1) is used for normal program output, while `stderr` (file descriptor 2) is used for error
messages. They are independent streams and can be redirected separately.

______________________________________________________________________

## Q2. What does `2>&1` mean?

**Answer**

It redirects `stderr` (file descriptor 2) to the same destination as `stdout` (file descriptor 1), allowing both normal
output and error messages to be written to the same location.

______________________________________________________________________

## Q3. What is the purpose of `/dev/null`?

**Answer**

`/dev/null` is a special device that discards everything written to it. It is commonly used to suppress unwanted output
or error messages.

______________________________________________________________________

## Q4. What is the purpose of a pipe (`|`)?

**Answer**

A pipe connects the standard output of one command to the standard input of another command, allowing multiple commands
to work together as a processing pipeline.

______________________________________________________________________

## Q5. What does the `tee` command do?

**Answer**

`tee` reads from standard input and writes the data to both standard output and one or more files. It is useful when you
want to view output while simultaneously saving it.

______________________________________________________________________

## Q6. What problem does `xargs` solve?

**Answer**

`xargs` converts input from standard input into command-line arguments, making it easy to pass lists of items from one
command to another.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Redirect command output to a file.

______________________________________________________________________

## Exercise 2

Append additional output to the same file.

______________________________________________________________________

## Exercise 3

Redirect only error messages into a separate file.

______________________________________________________________________

## Exercise 4

Redirect both stdout and stderr into a single file.

______________________________________________________________________

## Exercise 5

Use `tee` to display and save output simultaneously.

______________________________________________________________________

## Exercise 6

Find all Python files and save the results using `tee`.

______________________________________________________________________

## Exercise 7

Create pipelines using:

- `grep`
- `sort`
- `uniq`
- `wc`

______________________________________________________________________

## Exercise 8

Delete a list of files using `xargs`.

______________________________________________________________________

# Cheat Sheet

## Redirection

```bash
>
>>
<
2>
2>>
&>
2>&1
```

______________________________________________________________________

## Streams

```text
0 → stdin
1 → stdout
2 → stderr
```

______________________________________________________________________

## Pipes

```bash
|
```

______________________________________________________________________

## Tee

```bash
tee
tee -a
```

______________________________________________________________________

## Xargs

```bash
xargs
xargs -0
```

______________________________________________________________________

## Null Device

```text
/dev/null
```

______________________________________________________________________

# Summary

In this chapter, you learned how Linux programs communicate using standard input, standard output, and standard error.
You explored file descriptors, output and input redirection, error handling, appending output, the purpose of
`/dev/null`, how pipes connect commands into powerful workflows, and how `tee` and `xargs` enable efficient data
processing and automation. These are among the most frequently used concepts in production Linux environments and
technical interviews.

______________________________________________________________________

## Next

[Command Line Productivity](11-command-line-productivity.md)

# Linux Complete Interview & Production Course

# File 09 — Bash Shell and Environment

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Shell & Command Line
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 08 — ACL, SUID, SGID, and Sticky Bit

______________________________________________________________________

# Table of Contents

1. What is a Shell?
1. Why Do We Need a Shell?
1. How the Shell Works
1. Types of Shells
1. What is Bash?
1. Login Shell vs Non-Login Shell
1. Interactive vs Non-Interactive Shell
1. Environment Variables
1. Shell Variables
1. PATH Variable
1. Viewing Environment Variables
1. Exporting Variables
1. Startup Files
1. Aliases
1. Command History
1. Command Substitution
1. Quoting
1. Escape Characters
1. Exit Status
1. Production Examples
1. Common Mistakes
1. Best Practices
1. Interview Questions
1. Practice Exercises
1. Cheat Sheet
1. Summary
1. Next

______________________________________________________________________

# 1. What is a Shell?

The **Shell** is a command interpreter.

It acts as a bridge between:

```
User

↓

Shell

↓

Kernel

↓

Hardware
```

When you type:

```bash
ls
```

The shell:

- Reads your command
- Parses it
- Finds the executable
- Executes it
- Displays the output

Without the shell, interacting with Linux would be extremely difficult.

______________________________________________________________________

# 2. Why Do We Need a Shell?

Imagine speaking directly to the Linux kernel.

Instead of:

```bash
ls
```

you would have to invoke system calls manually.

The shell simplifies this interaction by providing a human-readable interface.

It also supports:

- Variables
- Loops
- Conditions
- Functions
- Pipes
- Redirection
- Automation

This makes it much more than just a command executor.

______________________________________________________________________

# 3. How the Shell Works

Suppose you execute:

```bash
python3 app.py
```

Internally:

```
Keyboard Input

↓

Shell

↓

Search PATH

↓

Locate executable

↓

Create Process

↓

Kernel

↓

Execute Program

↓

Return Exit Status

↓

Display Output
```

______________________________________________________________________

# 4. Types of Shells

Linux provides multiple shells.

## Bourne Shell (sh)

Original UNIX shell.

Very portable.

______________________________________________________________________

## Bash (Bourne Again Shell)

Default on most Linux distributions.

Supports:

- History
- Aliases
- Arrays
- Functions
- Job Control

Most widely used.

______________________________________________________________________

## Zsh

Popular among developers.

Provides:

- Better auto-completion
- Plugins
- Themes

Often used with:

- Oh My Zsh

______________________________________________________________________

## Fish

Friendly Interactive Shell.

Designed for ease of use.

Excellent autocomplete.

______________________________________________________________________

## Dash

Very lightweight.

Frequently used for system scripts.

______________________________________________________________________

# Check Current Shell

```bash
echo $SHELL
```

Example

```text
/bin/bash
```

______________________________________________________________________

# List Available Shells

```bash
cat /etc/shells
```

Example

```text
/bin/bash
/bin/sh
/bin/zsh
/bin/dash
```

______________________________________________________________________

# 5. What is Bash?

Bash stands for:

> **Bourne Again Shell**

It is:

- A shell
- A scripting language
- A command interpreter

Nearly every Linux administrator and backend engineer uses Bash daily.

______________________________________________________________________

# Check Bash Version

```bash
bash --version
```

______________________________________________________________________

# Start Another Bash Session

```bash
bash
```

Exit

```bash
exit
```

______________________________________________________________________

# 6. Login Shell vs Non-Login Shell

## Login Shell

Starts when:

- Logging in through SSH
- Logging into a terminal
- Logging into a Linux desktop

It loads login configuration files.

______________________________________________________________________

## Non-Login Shell

Started from an existing shell.

Example:

```bash
bash
```

This creates another Bash session inside the current one.

______________________________________________________________________

# 7. Interactive vs Non-Interactive Shell

## Interactive

Accepts user input.

Example:

```bash
bash
```

You type commands.

______________________________________________________________________

## Non-Interactive

Runs a script.

Example:

```bash
bash deploy.sh
```

No user interaction is required.

______________________________________________________________________

# 8. Environment Variables

Environment variables are values inherited by child processes.

Examples:

```
HOME

PATH

USER

SHELL

PWD

LANG
```

Display one variable:

```bash
echo $HOME
```

Example

```text
/home/riyaz
```

______________________________________________________________________

# Display Current User

```bash
echo $USER
```

______________________________________________________________________

# Display Current Directory

```bash
echo $PWD
```

______________________________________________________________________

# Display Home Directory

```bash
echo $HOME
```

______________________________________________________________________

# Display Current Shell

```bash
echo $SHELL
```

______________________________________________________________________

# 9. Shell Variables

Shell variables exist only inside the current shell.

Create one:

```bash
name="Riyaz"
```

Display:

```bash
echo $name
```

Output

```text
Riyaz
```

Close the terminal.

Variable disappears.

______________________________________________________________________

# 10. PATH Variable

One of the most important environment variables.

Display:

```bash
echo $PATH
```

Example

```text
/usr/local/bin:
/usr/bin:
/bin
```

When you type:

```bash
python3
```

Bash searches each directory in PATH until it finds:

```text
/usr/bin/python3
```

______________________________________________________________________

# Add Directory Temporarily

```bash
export PATH=$PATH:/home/riyaz/bin
```

______________________________________________________________________

# Verify

```bash
echo $PATH
```

______________________________________________________________________

# 11. Viewing Environment Variables

Display all:

```bash
env
```

or

```bash
printenv
```

Display a specific variable:

```bash
printenv HOME
```

______________________________________________________________________

# 12. Exporting Variables

Create variable:

```bash
API_KEY=12345
```

Only the current shell can see it.

Export it:

```bash
export API_KEY
```

Now child processes inherit it.

Shortcut:

```bash
export API_KEY=12345
```

______________________________________________________________________

# Remove Variable

```bash
unset API_KEY
```

______________________________________________________________________

# 13. Startup Files

Bash automatically loads configuration files during startup.

Important files:

| File | Purpose |
|------|----------|
| ~/.bashrc | Interactive shell configuration |
| ~/.bash_profile | Login shell configuration |
| ~/.profile | Generic login configuration |
| /etc/profile | System-wide login configuration |
| /etc/bash.bashrc | System-wide Bash configuration (Ubuntu) |

______________________________________________________________________

# Reload Configuration

```bash
source ~/.bashrc
```

Equivalent:

```bash
. ~/.bashrc
```

______________________________________________________________________

# 14. Aliases

Aliases create command shortcuts.

Example:

```bash
alias ll="ls -lah"
```

Use:

```bash
ll
```

Output:

```text
total 40
...
```

______________________________________________________________________

List aliases:

```bash
alias
```

______________________________________________________________________

Remove:

```bash
unalias ll
```

______________________________________________________________________

Persist alias:

Add it to:

```text
~/.bashrc
```

______________________________________________________________________

# 15. Command History

Display history:

```bash
history
```

______________________________________________________________________

Search history:

```bash
Ctrl + R
```

______________________________________________________________________

Repeat last command:

```bash
!!
```

______________________________________________________________________

Run history item:

```bash
!250
```

______________________________________________________________________

Clear history:

```bash
history -c
```

______________________________________________________________________

# 16. Command Substitution

Run one command inside another.

Modern syntax:

```bash
echo $(pwd)
```

Output:

```text
/home/riyaz/projects
```

______________________________________________________________________

Older syntax:

```bash
echo `pwd`
```

Modern syntax is recommended.

______________________________________________________________________

# Example

```bash
mkdir backup-$(date +%F)
```

Output

```text
backup-2026-08-07
```

______________________________________________________________________

# 17. Quoting

## Double Quotes

Variables expand.

```bash
name="Riyaz"

echo "Hello $name"
```

Output

```text
Hello Riyaz
```

______________________________________________________________________

## Single Quotes

Variables do not expand.

```bash
echo 'Hello $name'
```

Output

```text
Hello $name
```

______________________________________________________________________

# 18. Escape Characters

Escape special characters using:

```
\
```

Example

```bash
echo "He said \"Hello\""
```

Output

```text
He said "Hello"
```

______________________________________________________________________

# 19. Exit Status

Every command returns an exit code.

Success:

```
0
```

Failure:

```
Non-zero
```

Check previous exit status:

```bash
echo $?
```

Example:

```bash
mkdir test
echo $?
```

Output

```text
0
```

______________________________________________________________________

Failing example:

```bash
cat missing.txt
echo $?
```

Output

```text
1
```

Exit codes are heavily used in automation and CI/CD pipelines.

______________________________________________________________________

# 20. Production Examples

## Add custom binaries

```bash
export PATH=$PATH:/opt/tools/bin
```

______________________________________________________________________

## Store API token

```bash
export API_TOKEN=abcdef
```

______________________________________________________________________

## Reload Bash configuration

```bash
source ~/.bashrc
```

______________________________________________________________________

## Create useful aliases

```bash
alias gs="git status"
alias k="kubectl"
alias d="docker"
```

______________________________________________________________________

## Generate timestamped backup

```bash
mkdir backup-$(date +%F)
```

______________________________________________________________________

# 21. Common Mistakes

❌ Editing `.bashrc` but forgetting to reload it.

______________________________________________________________________

❌ Overwriting `PATH` instead of appending to it.

Incorrect:

```bash
export PATH=/my/bin
```

Correct:

```bash
export PATH=$PATH:/my/bin
```

______________________________________________________________________

❌ Storing secrets permanently inside shell configuration files.

______________________________________________________________________

❌ Using backticks instead of `$(...)` for command substitution.

______________________________________________________________________

❌ Assuming shell variables are inherited by child processes.

Only exported variables are inherited.

______________________________________________________________________

# 22. Best Practices

- Use Bash for automation and scripting.
- Use `export` only when child processes require the variable.
- Keep aliases meaningful and memorable.
- Prefer `$(...)` over backticks.
- Reload `.bashrc` after modifications.
- Avoid storing sensitive secrets permanently in shell configuration files.

______________________________________________________________________

# Interview Questions

## Q1. What is the difference between a shell variable and an environment variable?

**Answer**

A shell variable exists only in the current shell session. An environment variable is exported and inherited by child
processes, allowing programs launched from the shell to access it.

______________________________________________________________________

## Q2. What is the purpose of the `PATH` environment variable?

**Answer**

`PATH` contains a list of directories that the shell searches when executing commands. This allows users to run programs
without specifying their full path.

______________________________________________________________________

## Q3. What is the difference between `.bashrc` and `.bash_profile`?

**Answer**

`.bashrc` is typically used for interactive shell configuration, while `.bash_profile` is executed for login shells and
often sources `.bashrc`.

______________________________________________________________________

## Q4. What does `source ~/.bashrc` do?

**Answer**

It reloads the `.bashrc` configuration into the current shell without requiring the user to open a new terminal session.

______________________________________________________________________

## Q5. What is the purpose of `echo $?`?

**Answer**

It displays the exit status of the previously executed command. A value of `0` indicates success, while a non-zero value
indicates an error or failure.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Display:

```bash
echo $HOME
echo $PATH
echo $USER
echo $PWD
echo $SHELL
```

______________________________________________________________________

## Exercise 2

Create a shell variable and an exported environment variable.

Observe the difference using a child shell.

______________________________________________________________________

## Exercise 3

Create three useful aliases.

Persist them using `.bashrc`.

______________________________________________________________________

## Exercise 4

Reload your shell configuration without restarting the terminal.

______________________________________________________________________

## Exercise 5

Use command substitution to create a directory with today's date.

______________________________________________________________________

## Exercise 6

Run successful and failing commands.

Inspect their exit status.

______________________________________________________________________

# Cheat Sheet

## Environment

```bash
env
printenv
export
unset
```

______________________________________________________________________

## Variables

```bash
echo
```

______________________________________________________________________

## Shell Configuration

```bash
~/.bashrc
~/.bash_profile
source
```

______________________________________________________________________

## Aliases

```bash
alias
unalias
```

______________________________________________________________________

## History

```bash
history
!!
!number
Ctrl + R
```

______________________________________________________________________

## Exit Status

```bash
echo $?
```

______________________________________________________________________

## Command Substitution

```bash
$(...)
```

______________________________________________________________________

# Summary

In this chapter, you learned how the Bash shell interacts with the Linux kernel, the differences between shell variables
and environment variables, how `PATH` works, how to configure Bash using startup files, create aliases, use command
history, perform command substitution, and interpret command exit statuses. These concepts form the foundation for
effective command-line usage and Bash scripting.

______________________________________________________________________

## Next

[Input, Output, Redirection, Pipes, and Tee](10-input-output-redirection-pipes-tee.md)

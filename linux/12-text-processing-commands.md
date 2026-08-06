# Linux Complete Interview & Production Course

# File 12 — Text Processing Commands

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Text Processing
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 11 — Command Line Productivity

______________________________________________________________________

# Table of Contents

1. Introduction
1. Why Text Processing Matters
1. What is Text Processing?
1. The `grep` Command
1. The `egrep` Command
1. The `fgrep` Command
1. The `cut` Command
1. The `tr` Command
1. The `paste` Command
1. The `tee` Command (Advanced Usage)
1. The `xargs` Command (Advanced Usage)
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

Linux is designed around the idea that **everything is text**.

Configuration files

```
nginx.conf
```

Logs

```
application.log
```

CSV files

```
users.csv
```

JSON

```
config.json
```

YAML

```
deployment.yaml
```

System information

```
ps
df
top
journalctl
```

Almost everything can be processed using Linux text processing commands.

Mastering these commands is one of the biggest productivity boosts for backend engineers.

______________________________________________________________________

# 2. Why Text Processing Matters

Imagine a production log containing:

```
5 GB
```

Opening it in a text editor is impractical.

Instead, Linux lets you answer questions like:

- How many ERROR messages occurred?
- Which IP address appears most frequently?
- Which user logged in the most?
- Which endpoint returned HTTP 500?

using a few commands.

______________________________________________________________________

# 3. What is Text Processing?

Text processing means reading, filtering, transforming, extracting, and analyzing text.

Typical workflow:

```
Input File

↓

Filter

↓

Transform

↓

Extract

↓

Output
```

Example:

```bash
cat access.log | grep ERROR | sort | uniq -c
```

______________________________________________________________________

# 4. The `grep` Command

`grep` searches text for matching patterns.

Basic syntax:

```bash
grep PATTERN FILE
```

______________________________________________________________________

Search for a word.

```bash
grep ERROR app.log
```

______________________________________________________________________

Ignore case.

```bash
grep -i error app.log
```

______________________________________________________________________

Show line numbers.

```bash
grep -n ERROR app.log
```

______________________________________________________________________

Count matches.

```bash
grep -c ERROR app.log
```

______________________________________________________________________

Invert match.

```bash
grep -v INFO app.log
```

______________________________________________________________________

Recursive search.

```bash
grep -r TODO .
```

______________________________________________________________________

Only filenames.

```bash
grep -l ERROR *.log
```

______________________________________________________________________

Multiple files.

```bash
grep ERROR *.log
```

______________________________________________________________________

Highlight matches.

```bash
grep --color=auto ERROR app.log
```

______________________________________________________________________

# Common grep Options

| Option | Description |
|---------|-------------|
| -i | Ignore case |
| -v | Invert match |
| -n | Line numbers |
| -c | Count |
| -r | Recursive |
| -l | Matching filenames |
| -w | Whole word |
| -o | Only matching text |

______________________________________________________________________

# 5. The `egrep` Command

Historically,

`egrep`

enabled Extended Regular Expressions.

Example

```bash
egrep "ERROR|WARN" app.log
```

Modern systems generally recommend:

```bash
grep -E
```

Equivalent:

```bash
grep -E "ERROR|WARN" app.log
```

______________________________________________________________________

# 6. The `fgrep` Command

Historically,

`fgrep`

searched for fixed strings.

Modern equivalent:

```bash
grep -F
```

Example

```bash
grep -F "ERROR (500)" app.log
```

Useful when searching for text containing regex characters.

______________________________________________________________________

# 7. The `cut` Command

Extract columns from text.

Example CSV:

```text
1,Riyaz,India
2,Alice,USA
3,Bob,Canada
```

Extract first column.

```bash
cut -d "," -f1 users.csv
```

Output

```text
1
2
3
```

______________________________________________________________________

Extract second column.

```bash
cut -d "," -f2 users.csv
```

Output

```text
Riyaz
Alice
Bob
```

______________________________________________________________________

Extract multiple fields.

```bash
cut -d "," -f1,3 users.csv
```

______________________________________________________________________

Extract characters.

```bash
cut -c1-5 file.txt
```

______________________________________________________________________

# 8. The `tr` Command

Translate or delete characters.

Convert lowercase to uppercase.

```bash
echo "linux" | tr a-z A-Z
```

Output

```text
LINUX
```

______________________________________________________________________

Remove digits.

```bash
echo "abc123" | tr -d 0-9
```

Output

```text
abc
```

______________________________________________________________________

Replace spaces.

```bash
echo "hello world" | tr " " "_"
```

Output

```text
hello_world
```

______________________________________________________________________

Compress repeated spaces.

```bash
tr -s " "
```

______________________________________________________________________

# 9. The `paste` Command

Merge files horizontally.

Example:

file1

```text
Alice
Bob
Charlie
```

file2

```text
25
30
28
```

Command

```bash
paste file1 file2
```

Output

```text
Alice   25
Bob     30
Charlie 28
```

______________________________________________________________________

Custom delimiter.

```bash
paste -d "," file1 file2
```

Output

```text
Alice,25
Bob,30
Charlie,28
```

______________________________________________________________________

# 10. The `tee` Command (Advanced Usage)

`tee` can write to multiple files.

```bash
echo "Hello" | tee file1 file2
```

Both files receive the output.

______________________________________________________________________

Append.

```bash
echo "World" | tee -a file.txt
```

______________________________________________________________________

Useful for debugging pipelines.

```bash
cat app.log \
| tee original.log \
| grep ERROR
```

______________________________________________________________________

# 11. The `xargs` Command (Advanced Usage)

Convert input into command arguments.

______________________________________________________________________

Display file sizes.

```bash
find . -name "*.py" | xargs ls -lh
```

______________________________________________________________________

Search inside multiple files.

```bash
find . -name "*.py" | xargs grep TODO
```

______________________________________________________________________

Delete empty files.

```bash
find . -empty | xargs rm
```

______________________________________________________________________

Parallel execution.

```bash
xargs -P 4
```

Example:

```bash
cat urls.txt | xargs -P 4 curl
```

Runs four commands simultaneously.

______________________________________________________________________

Limit arguments.

```bash
xargs -n 2
```

Example

```bash
echo "a b c d" | xargs -n 2
```

Output

```text
a b
c d
```

______________________________________________________________________

Safe handling of spaces.

```bash
find . -print0 | xargs -0 rm
```

______________________________________________________________________

# 12. Production Examples

## Find Failed Requests

```bash
grep "500" access.log
```

______________________________________________________________________

## Count Login Failures

```bash
grep -c "Failed password" auth.log
```

______________________________________________________________________

## Extract Usernames

```bash
cut -d ":" -f1 /etc/passwd
```

______________________________________________________________________

## Convert CSV to Uppercase

```bash
cat users.csv | tr a-z A-Z
```

______________________________________________________________________

## Merge Reports

```bash
paste names.txt scores.txt
```

______________________________________________________________________

## Search Every Python File

```bash
find . -name "*.py" | xargs grep TODO
```

______________________________________________________________________

## Search Kubernetes YAML Files

```bash
find . -name "*.yaml" | xargs grep image
```

______________________________________________________________________

# 13. Common Mistakes

❌ Using `grep` when exact string matching (`grep -F`) is required.

______________________________________________________________________

❌ Forgetting the delimiter with `cut`.

______________________________________________________________________

❌ Using `xargs` without handling filenames containing spaces.

______________________________________________________________________

❌ Forgetting that `tr` operates on characters, not words.

______________________________________________________________________

❌ Overusing `cat` in pipelines when the command can read files directly.

______________________________________________________________________

# 14. Best Practices

- Prefer `grep -F` for fixed-string searches.
- Use `grep -E` instead of `egrep` for modern scripts.
- Use `find -print0 | xargs -0` for safe filename handling.
- Use `cut` for simple column extraction and reserve `awk` for more complex processing.
- Combine small tools into pipelines rather than writing large scripts for simple tasks.

______________________________________________________________________

# Interview Questions

## Q1. What is the difference between `grep`, `grep -E`, and `grep -F`?

**Answer**

`grep` uses basic regular expressions. `grep -E` enables extended regular expressions with additional pattern syntax,
while `grep -F` treats the search pattern as a literal string without interpreting regular expression characters.

______________________________________________________________________

## Q2. When would you use `cut` instead of `awk`?

**Answer**

`cut` is ideal for simple extraction of fixed columns or character ranges. `awk` is more powerful and should be used
when conditional logic, calculations, or complex text processing is required.

______________________________________________________________________

## Q3. What does the `tr` command do?

**Answer**

`tr` translates, deletes, or squeezes characters from standard input. It operates on individual characters rather than
words or fields.

______________________________________________________________________

## Q4. Why is `find -print0 | xargs -0` recommended?

**Answer**

It safely handles filenames containing spaces, tabs, or newlines by using a null character as the separator instead of
whitespace.

______________________________________________________________________

## Q5. What is the advantage of `tee` in a pipeline?

**Answer**

`tee` allows a pipeline's output to be displayed on the terminal while simultaneously writing it to one or more files,
making it useful for logging and debugging.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Search for:

- ERROR
- WARN
- INFO

inside a sample log file.

______________________________________________________________________

## Exercise 2

Extract:

- Username
- UID
- Shell

from:

```text
/etc/passwd
```

using `cut`.

______________________________________________________________________

## Exercise 3

Convert lowercase text to uppercase using `tr`.

______________________________________________________________________

## Exercise 4

Merge two files using `paste`.

______________________________________________________________________

## Exercise 5

Search every Python file in a directory for the word:

```
TODO
```

using `find` and `xargs`.

______________________________________________________________________

## Exercise 6

Use `tee` to save and display command output simultaneously.

______________________________________________________________________

# Cheat Sheet

## Search

```bash
grep
grep -E
grep -F
```

______________________________________________________________________

## Extract

```bash
cut
```

______________________________________________________________________

## Transform

```bash
tr
```

______________________________________________________________________

## Merge

```bash
paste
```

______________________________________________________________________

## Pipelines

```bash
tee
xargs
```

______________________________________________________________________

# Summary

In this chapter, you learned the core Linux text processing utilities used for searching, extracting, transforming, and
combining text. You explored `grep`, `grep -E`, `grep -F`, `cut`, `tr`, `paste`, `tee`, and advanced `xargs` usage,
along with practical production examples and best practices for building efficient text-processing pipelines.

______________________________________________________________________

## Next

[Regular Expressions](13-regular-expressions.md)

# Linux Complete Interview & Production Course

# File 13 — Regular Expressions

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Text Processing
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 12 — Text Processing Commands

______________________________________________________________________

# Table of Contents

1. Introduction
1. What is a Regular Expression?
1. Why Regular Expressions Matter
1. Basic Regular Expressions (BRE)
1. Extended Regular Expressions (ERE)
1. Common Regular Expression Metacharacters
1. Character Classes
1. Anchors
1. Quantifiers
1. Grouping and Alternation
1. Escaping Special Characters
1. Regular Expressions with `grep`
1. Regular Expressions with `sed`
1. Regular Expressions with `awk`
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

Regular Expressions (Regex) are one of the most powerful tools available in Linux.

Instead of searching for fixed text such as:

```text
ERROR
```

Regex allows you to search for patterns.

Examples:

- Email addresses
- IP addresses
- Dates
- Phone numbers
- UUIDs
- Log entries
- HTTP status codes

Regex is heavily used in:

- Linux
- Python
- Java
- JavaScript
- Go
- SQL
- VS Code
- Vim
- Kubernetes
- Docker
- CI/CD Pipelines

Learning Regex is one of the highest ROI skills for backend engineers.

______________________________________________________________________

# 2. What is a Regular Expression?

A Regular Expression is a sequence of characters that describes a search pattern.

Instead of searching for:

```text
ERROR
```

You can search for:

```
Any line starting with ERROR
```

or

```
Every 3-digit HTTP status code
```

or

```
Every IPv4 address
```

______________________________________________________________________

# Example

File:

```text
ERROR Connection failed
INFO User logged in
WARNING Disk almost full
ERROR Database timeout
```

Command:

```bash
grep "^ERROR" app.log
```

Output:

```text
ERROR Connection failed
ERROR Database timeout
```

______________________________________________________________________

# 3. Why Regular Expressions Matter

Imagine a log containing:

```
20 million lines
```

You need:

- Every failed login
- Every IP address
- Every email
- Every HTTP 500 response

Regex makes these searches possible with concise patterns.

______________________________________________________________________

# 4. Basic Regular Expressions (BRE)

`grep` uses **Basic Regular Expressions (BRE)** by default.

Example:

```bash
grep "^ERROR" app.log
```

______________________________________________________________________

Extended expressions require:

```bash
grep -E
```

______________________________________________________________________

# 5. Extended Regular Expressions (ERE)

ERE adds additional operators.

Example:

```bash
grep -E "ERROR|WARN"
```

Matches:

```text
ERROR
WARN
```

Without `-E`, the `|` operator is treated differently and generally requires escaping.

______________________________________________________________________

# 6. Common Regular Expression Metacharacters

| Symbol | Meaning |
|---------|----------|
| . | Any single character |
| ^ | Start of line |
| $ | End of line |
| * | Zero or more |
| + | One or more (ERE) |
| ? | Zero or one (ERE) |
| [] | Character class |
| () | Grouping (ERE) |
| | | Alternation (ERE uses `|`) |
| \\ | Escape character |

______________________________________________________________________

# Dot (`.`)

Matches any single character.

Pattern:

```text
c.t
```

Matches:

```text
cat
cut
cot
c9t
```

Does not match:

```text
cart
```

______________________________________________________________________

# 7. Character Classes

## Digits

```text
[0-9]
```

Matches:

```text
5
```

______________________________________________________________________

## Lowercase

```text
[a-z]
```

______________________________________________________________________

## Uppercase

```text
[A-Z]
```

______________________________________________________________________

## Alphabet

```text
[A-Za-z]
```

______________________________________________________________________

## Alphanumeric

```text
[A-Za-z0-9]
```

______________________________________________________________________

## Negation

```text
[^0-9]
```

Matches:

Everything except digits.

______________________________________________________________________

# Examples

Find HTTP status codes.

```bash
grep -E "[0-9][0-9][0-9]" access.log
```

______________________________________________________________________

Find usernames starting with "a".

```bash
grep "^a" users.txt
```

______________________________________________________________________

# 8. Anchors

## Beginning of Line

```text
^
```

Example

```bash
grep "^ERROR" app.log
```

______________________________________________________________________

## End of Line

```text
$
```

Example

```bash
grep "failed$" app.log
```

Matches:

```text
Login failed
```

______________________________________________________________________

Exact match.

```bash
grep "^root$" users.txt
```

Matches only:

```text
root
```

______________________________________________________________________

# 9. Quantifiers

## `*`

Zero or more.

Pattern:

```text
ab*
```

Matches:

```text
a
ab
abb
abbb
```

______________________________________________________________________

## `+` (ERE)

One or more.

```bash
grep -E "ab+"
```

Matches:

```text
ab
abb
abbbb
```

______________________________________________________________________

## `?` (ERE)

Zero or one.

```bash
grep -E "colou?r"
```

Matches:

```text
color
colour
```

______________________________________________________________________

## Exact Count

```text
{3}
```

Example

```bash
grep -E "[0-9]{3}"
```

Matches:

Three consecutive digits.

______________________________________________________________________

Range

```text
{2,5}
```

______________________________________________________________________

Minimum

```text
{2,}
```

______________________________________________________________________

# 10. Grouping and Alternation

Grouping

```text
(...)
```

Example

```bash
grep -E "(ERROR|WARN)"
```

Matches

```
ERROR

WARN
```

______________________________________________________________________

Alternation

```text
|
```

Equivalent to logical OR.

______________________________________________________________________

# 11. Escaping Special Characters

Special characters have meaning.

To match them literally:

Escape them.

Example

Search for:

```text
192.168.1.10
```

Use:

```bash
grep "192\.168\.1\.10"
```

Without escaping:

```
.

↓

Any character
```

______________________________________________________________________

# 12. Regular Expressions with `grep`

Find lines ending with `.py`

```bash
grep "\.py$" files.txt
```

______________________________________________________________________

Three-digit numbers.

```bash
grep -E "[0-9]{3}"
```

______________________________________________________________________

Match only lowercase words.

```bash
grep -E "^[a-z]+$"
```

______________________________________________________________________

Find UUID-like values (simplified).

```bash
grep -E "[a-f0-9-]{36}"
```

______________________________________________________________________

# 13. Regular Expressions with `sed`

Replace every number.

```bash
sed -E "s/[0-9]+/NUMBER/g" data.txt
```

______________________________________________________________________

Replace multiple spaces.

```bash
sed -E "s/ +/ /g"
```

______________________________________________________________________

Delete blank lines.

```bash
sed "/^$/d"
```

______________________________________________________________________

# 14. Regular Expressions with `awk`

Print lines beginning with ERROR.

```bash
awk '/^ERROR/'
```

______________________________________________________________________

Print HTTP 500 responses.

```bash
awk '/500/'
```

______________________________________________________________________

Print emails containing gmail.

```bash
awk '/gmail/'
```

______________________________________________________________________

# 15. Production Examples

## Find Python Files

```bash
find . | grep "\.py$"
```

______________________________________________________________________

## Find IP Addresses (Simple Pattern)

```bash
grep -E "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
```

______________________________________________________________________

## Find HTTP Status Codes

```bash
grep -E "[1-5][0-9][0-9]"
```

______________________________________________________________________

## Replace Version Numbers

```bash
sed -E "s/v[0-9]+/vX/g"
```

______________________________________________________________________

## Search Nginx Errors

```bash
grep "^ERROR" nginx.log
```

______________________________________________________________________

## Validate Usernames

```bash
grep -E "^[a-z][a-z0-9_]{2,15}$"
```

______________________________________________________________________

# 16. Common Mistakes

❌ Forgetting that `.` matches any character.

______________________________________________________________________

❌ Using `grep` instead of `grep -E` when extended regex syntax is required.

______________________________________________________________________

❌ Forgetting to escape literal periods in IP addresses or filenames.

______________________________________________________________________

❌ Assuming shell wildcards and regular expressions are the same.

They are different concepts.

______________________________________________________________________

❌ Writing overly complex regular expressions that are difficult to maintain.

______________________________________________________________________

# 17. Best Practices

- Keep regular expressions as simple as possible.
- Escape special characters when matching literal text.
- Use `grep -E` for extended regular expressions.
- Test complex expressions on sample data before using them in production.
- Comment complicated regex patterns in scripts for maintainability.

______________________________________________________________________

# Interview Questions

## Q1. What is the difference between shell wildcards and regular expressions?

**Answer**

Shell wildcards (globbing) are expanded by the shell before a command executes and are primarily used for matching
filenames. Regular expressions are pattern-matching expressions interpreted by programs such as `grep`, `sed`, and `awk`
to search or manipulate text.

______________________________________________________________________

## Q2. What is the difference between Basic Regular Expressions (BRE) and Extended Regular Expressions (ERE)?

**Answer**

BRE is the default syntax used by `grep` and requires escaping for certain operators. ERE, enabled with `grep -E`,
supports additional operators such as `+`, `?`, `()`, and `|` without requiring escaping.

______________________________________________________________________

## Q3. What do `^` and `$` represent in regular expressions?

**Answer**

`^` matches the beginning of a line, while `$` matches the end of a line. Together they can be used to match an entire
line exactly.

______________________________________________________________________

## Q4. Why must the period (`.`) be escaped when matching an IP address?

**Answer**

In regular expressions, `.` matches any single character. Escaping it (`\.`) tells the regex engine to match a literal
period instead.

______________________________________________________________________

## Q5. When would you use `grep -E`?

**Answer**

`grep -E` is used when a pattern requires extended regular expression features such as alternation (`|`), grouping
(`()`), or quantifiers like `+` and `?`.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Find all lines beginning with:

```text
ERROR
```

______________________________________________________________________

## Exercise 2

Find every line ending with:

```text
failed
```

______________________________________________________________________

## Exercise 3

Extract every three-digit number from a log file.

______________________________________________________________________

## Exercise 4

Find all Python filenames ending in:

```text
.py
```

______________________________________________________________________

## Exercise 5

Replace all numeric values with:

```text
NUMBER
```

using `sed`.

______________________________________________________________________

## Exercise 6

Write regular expressions to match:

- Email addresses (basic pattern)
- IPv4 addresses (basic pattern)
- Dates in `YYYY-MM-DD` format
- Usernames containing lowercase letters, digits, and underscores

______________________________________________________________________

# Cheat Sheet

## Anchors

```text
^
$
```

______________________________________________________________________

## Character Classes

```text
[]
[^]
[a-z]
[A-Z]
[0-9]
```

______________________________________________________________________

## Quantifiers

```text
*
+
?
{n}
{n,m}
```

______________________________________________________________________

## Operators

```text
.
()
|
\
```

______________________________________________________________________

## Commands

```bash
grep
grep -E
sed
awk
```

______________________________________________________________________

# Summary

In this chapter, you learned the fundamentals of regular expressions, including basic and extended regex syntax,
character classes, anchors, quantifiers, grouping, alternation, and escaping special characters. You also explored how
regular expressions are used with `grep`, `sed`, and `awk` to search, filter, and transform text in real-world Linux
environments.

______________________________________________________________________

## Next

[Process Management](14-process-management.md)

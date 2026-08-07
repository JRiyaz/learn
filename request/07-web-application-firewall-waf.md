# Complete HTTP Request Lifecycle Deep Dive

## 07. Web Application Firewall (WAF)

> Target Audience: Backend Engineers (Beginner → Senior)
>
> Goal: Understand how a Web Application Firewall (WAF) protects web applications, what happens internally when a request reaches a WAF, how attacks are detected, what technologies are used, and why WAFs are an essential part of modern production systems.

______________________________________________________________________

# Introduction

In the previous chapter,

the request

successfully reached

the CDN.

Suppose

the CDN

doesn't have

the requested content.

```
Browser

↓

CDN

↓

Cache Miss
```

Now

the request

must go

to

your backend.

But

before

it reaches

your infrastructure,

another layer

usually exists.

```
Web Application Firewall
```

______________________________________________________________________

# High-Level Flow

```
Browser

↓

Internet

↓

CDN

↓

Web Application Firewall

↓

Load Balancer

↓

Reverse Proxy

↓

API Gateway

↓

Application
```

Notice

the WAF

sits

before

your application.

______________________________________________________________________

# Why Do We Need A WAF?

Imagine

someone sends

this request

```
GET /users?id=1
```

Looks harmless.

Now imagine

this

```
GET /users?id=1
UNION SELECT password FROM users
```

Or

```
<script>

alert(1)

</script>
```

Your backend

should

never

receive

these requests.

The WAF

blocks them

before

they enter

your infrastructure.

______________________________________________________________________

# What Is A WAF?

WAF stands for

```
Web Application Firewall
```

Unlike

traditional firewalls,

which inspect

IP addresses

and ports,

a WAF

understands

```
HTTP

HTTPS

Headers

Cookies

Query Parameters

JSON

Form Data
```

It protects

web applications,

not

network devices.

______________________________________________________________________

# Traditional Firewall vs WAF

Interview favorite.

## Network Firewall

Works at

```
Layer 3

Layer 4
```

Understands

- IP Address
- Port
- Protocol

Example

```
Allow

Port 443
```

______________________________________________________________________

## WAF

Works at

```
Layer 7
```

Understands

```
HTTP

JSON

Cookies

Headers

Request Body
```

Can detect

SQL Injection,

XSS,

CSRF,

and more.

______________________________________________________________________

# Real Production Architecture

```
Internet

↓

Cloudflare

↓

AWS WAF

↓

Application Load Balancer

↓

Nginx

↓

FastAPI

↓

Redis

↓

PostgreSQL
```

Many attacks

never

reach

FastAPI.

______________________________________________________________________

# What Happens When A Request Arrives?

Suppose

the browser sends

```
POST /login
```

The request

first reaches

the WAF.

```
Incoming Request

↓

Read Headers

↓

Read URL

↓

Read Query Parameters

↓

Read Body

↓

Apply Rules

↓

Allow?

↓

Yes

↓

Forward

↓

No

↓

Block
```

______________________________________________________________________

# Step 1

# Read Request

The WAF

parses

the request.

Example

```
Method

POST
```

```
Path

/login
```

```
Headers

Authorization

Content-Type
```

```
Body

JSON
```

Unlike

a network firewall,

the WAF

understands

HTTP.

______________________________________________________________________

# Step 2

# Normalize Request

Interview favorite.

Attackers

often

hide

malicious payloads.

Example

Instead of

```
<script>
```

they send

```
%3Cscript%3E
```

or

```
%253Cscript%253E
```

The WAF

first

normalizes

the request.

```
Decode URL

↓

Decode Unicode

↓

Remove Encodings

↓

Canonical Form
```

Only then

does it

inspect

the content.

______________________________________________________________________

# Step 3

# Rule Engine

Now

the WAF

compares

the request

against

thousands

of rules.

Examples

```
SQL Injection

↓

XSS

↓

Command Injection

↓

Path Traversal

↓

Bad Bots

↓

Known Exploits
```

______________________________________________________________________

# Step 4

# Decision

If

no rules

match

```
Allow
```

Otherwise

```
403 Forbidden

or

Block Connection
```

The backend

never

sees

the request.

______________________________________________________________________

# Rule Types

Interview favorite.

## Signature Rules

Known attack patterns.

Example

```
UNION SELECT
```

______________________________________________________________________

## Regex Rules

Example

```
<script>
```

Pattern matching.

______________________________________________________________________

## Behavioral Rules

Example

```
500 Requests

in

10 Seconds
```

Possible bot.

______________________________________________________________________

## Reputation Rules

Known malicious

IP addresses.

Automatically blocked.

______________________________________________________________________

## Geo Rules

Allow

only

specific countries.

Example

```
Only India

and

Singapore
```

______________________________________________________________________

# SQL Injection Detection

Suppose

attacker sends

```
GET /user?id=1

OR 1=1
```

The WAF

detects

```
OR

1=1
```

Pattern.

```
Block Request
```

The database

never receives

the attack.

______________________________________________________________________

# Cross Site Scripting (XSS)

Example

```
<script>

alert(1)

</script>
```

The WAF

recognizes

the payload

and blocks it.

______________________________________________________________________

# Command Injection

Example

```
; rm -rf /
```

or

```
&& cat /etc/passwd
```

Blocked

before

the application

executes it.

______________________________________________________________________

# Path Traversal

Example

```
../../etc/passwd
```

Attempting

to read

system files.

Blocked.

______________________________________________________________________

# File Upload Inspection

Suppose

a user uploads

```
virus.exe
```

The WAF

may inspect

```
File Type

↓

Extension

↓

Magic Bytes

↓

Malware Signatures
```

______________________________________________________________________

# Bot Detection

Interview favorite.

Not every

visitor

is human.

Bots

may

- Scrape websites
- Perform credential stuffing
- Launch attacks

The WAF

detects

automated traffic.

______________________________________________________________________

# Rate Limiting

Suppose

one IP

sends

```
10,000 Requests

per minute
```

The WAF

can

limit

or

block

that IP.

______________________________________________________________________

# DDoS Protection

Interview favorite.

Suppose

1 million devices

send

requests.

Without WAF

```
Backend

↓

Crash
```

With WAF

```
Attack

↓

Filtered

↓

Backend Protected
```

______________________________________________________________________

# IP Reputation

Many WAFs

maintain

lists

of

known malicious

IP addresses.

Incoming request

↓

Known attacker?

↓

Block immediately.

______________________________________________________________________

# Geo Blocking

Example

Company operates

only

inside India.

Requests

from

other countries

may be blocked.

______________________________________________________________________

# OWASP Top 10

Interview favorite.

Modern WAFs

protect against

many

OWASP Top 10

attacks.

Examples

- SQL Injection
- XSS
- SSRF
- Command Injection
- File Inclusion
- Deserialization Attacks

______________________________________________________________________

# JSON Inspection

Unlike

old firewalls,

modern WAFs

understand

JSON.

Example

```
POST /login

{
    "username":"admin",
    "password":"' OR 1=1"
}
```

The WAF

parses

the JSON

before

inspection.

______________________________________________________________________

# GraphQL Protection

Modern WAFs

can inspect

GraphQL queries.

Detect

- Deep recursion
- Expensive queries
- Introspection abuse

______________________________________________________________________

# API Protection

Interview favorite.

Modern WAFs

protect APIs.

Examples

- JSON validation
- Header validation
- JWT inspection
- Rate limiting
- Schema validation

______________________________________________________________________

# What Happens Internally?

```
Incoming Packet

↓

TLS Decryption

↓

HTTP Parsing

↓

Normalization

↓

Rule Engine

↓

Threat Detection

↓

Allow?

↓

Forward

↓

Block
```

Notice

the WAF

must understand

the request

before

it can inspect it.

______________________________________________________________________

# Logging

Every request

may generate

logs.

Example

```
Timestamp

↓

IP

↓

Country

↓

User-Agent

↓

Attack Type

↓

Action
```

Useful

for

Security Operations.

______________________________________________________________________

# False Positives

Interview favorite.

Sometimes

legitimate users

are blocked.

Example

Developer searches

```
UNION

SQL Tutorial
```

WAF

might

mistakenly

detect

SQL Injection.

Proper tuning

is important.

______________________________________________________________________

# Managed Rule Sets

Most companies

don't write

every rule.

They use

managed rules.

Examples

```
AWS Managed Rules

OWASP Rules

Cloudflare Managed Rules
```

______________________________________________________________________

# WAF Learning Mode

Some WAFs

learn

normal traffic

first.

Then

they detect

abnormal behavior.

Useful

for

large applications.

______________________________________________________________________

# Common Attacks

## SQL Injection

```
UNION SELECT
```

Blocked.

______________________________________________________________________

## Cross Site Scripting

```
<script>
```

Blocked.

______________________________________________________________________

## Command Injection

```
&& rm -rf /
```

Blocked.

______________________________________________________________________

## Path Traversal

```
../../etc/passwd
```

Blocked.

______________________________________________________________________

## Local File Inclusion

Attempts

to load

server files.

Blocked.

______________________________________________________________________

## Remote File Inclusion

Attempts

to execute

remote scripts.

Blocked.

______________________________________________________________________

## Credential Stuffing

Thousands

of stolen

username/password

pairs.

Rate limiting

and bot detection

help prevent it.

______________________________________________________________________

## Brute Force

Repeated

login attempts.

Blocked

using

rate limiting.

______________________________________________________________________

# Popular WAF Technologies

Interview favorite.

Cloud

```
AWS WAF

Cloudflare WAF

Azure WAF

Google Cloud Armor
```

Self Hosted

```
ModSecurity

NGINX App Protect

F5 BIG-IP
```

______________________________________________________________________

# Technologies Used

| Component | Technologies |
|-----------|--------------|
| Cloud WAF | AWS WAF, Cloudflare WAF, Azure WAF |
| Self Hosted | ModSecurity, F5, NGINX App Protect |
| Rule Sets | OWASP CRS, AWS Managed Rules |
| DDoS | Cloudflare, AWS Shield |
| Bot Detection | Cloudflare Bot Management |

______________________________________________________________________

# Common Interview Questions

## Why use a WAF if the application already validates input?

Application validation protects business logic, while a WAF blocks malicious requests before they consume backend
resources. The WAF provides an additional defense layer and reduces attack traffic reaching the application.

______________________________________________________________________

## What is the difference between a Firewall and a WAF?

A traditional firewall operates at the network layer and filters based on IP addresses, ports, and protocols. A WAF
operates at the application layer and understands HTTP requests, headers, cookies, JSON payloads, and web attacks.

______________________________________________________________________

## Can a WAF prevent SQL Injection completely?

No. A WAF significantly reduces the risk but should never replace secure coding practices such as parameterized queries
and input validation. It is one layer of a defense-in-depth strategy.

______________________________________________________________________

## Why does a WAF normalize requests before inspection?

Attackers often encode malicious payloads using URL encoding, Unicode, or multiple encoding layers. Normalization
converts these representations into a standard form so attack signatures can be detected accurately.

______________________________________________________________________

## Why can WAFs produce false positives?

Pattern-based rules may classify legitimate input as malicious. Organizations tune rules, create exceptions, and monitor
logs to reduce false positives without weakening security.

______________________________________________________________________

# Interview Deep Dive

## Question

Walk me through what happens when a request reaches a WAF.

### Answer

The WAF decrypts HTTPS traffic if TLS terminates there, parses the HTTP request, normalizes encoded input, examines the
URL, headers, query parameters, cookies, and request body against its rule engine, applies managed and custom security
policies, and either forwards the request to the next infrastructure component or blocks it with an appropriate
response. All actions are typically logged for security monitoring.

______________________________________________________________________

# Summary

A Web Application Firewall is the first intelligent security layer protecting modern web applications.

Key concepts include

- HTTP inspection
- Request normalization
- Rule engine
- SQL Injection detection
- XSS protection
- Bot detection
- Rate limiting
- DDoS mitigation
- OWASP Top 10
- False positives
- Managed rule sets

After a request passes the WAF, it is considered safe enough to enter your infrastructure.

The next component responsible for deciding **which backend server should receive the request** is the **Load
Balancer**.

______________________________________________________________________

# Next

[08. Load Balancer Deep Dive](08-load-balancer-deep-dive.md)

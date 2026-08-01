# Security - Part 20

# HTTPS & TLS

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What HTTP is
- Why HTTPS exists
- What TLS is
- How HTTPS works
- SSL vs TLS
- Certificates
- Certificate Authorities (CA)
- HTTPS in FastAPI deployments
- Best practices

______________________________________________________________________

# Why Do We Need HTTPS?

Imagine you log in to a website.

```text id="tls2001"
Username

↓

Password

↓

Internet
```

If you're using plain HTTP,

the data travels as plain text.

Anyone who can intercept the network traffic may read it.

HTTPS solves this problem.

______________________________________________________________________

# HTTP vs HTTPS

## HTTP

```text id="tls2002"
Client

↓

Plain Text

↓

Server
```

Data is readable during transmission.

______________________________________________________________________

## HTTPS

```text id="tls2003"
Client

↓

Encrypted

↓

Server
```

Even if someone intercepts the traffic,

they cannot easily understand its contents.

______________________________________________________________________

# What is TLS?

TLS stands for

**Transport Layer Security**.

It is the protocol responsible for securing HTTPS communication.

Think of it like this:

```text id="tls2004"
HTTP

+

TLS

↓

HTTPS
```

HTTPS is simply

HTTP running over TLS.

______________________________________________________________________

# SSL vs TLS

You may hear both terms.

```text id="tls2005"
SSL

↓

Old

↓

Deprecated
```

```text id="tls2006"
TLS

↓

Modern

↓

Secure
```

Today,

people often say "SSL Certificate,"

but modern systems actually use TLS.

______________________________________________________________________

# What Does HTTPS Protect?

HTTPS provides three important guarantees.

______________________________________________________________________

## 1. Confidentiality

Only the client

and server

can read the data.

Example

```text id="tls2007"
Password

↓

Encrypted
```

______________________________________________________________________

## 2. Integrity

Data cannot be modified

without detection.

Example

```text id="tls2008"
Original Message

↓

Modified?

↓

Detected
```

______________________________________________________________________

## 3. Authentication

The client verifies

it is communicating

with the correct server.

This prevents many impersonation attacks.

______________________________________________________________________

# What is a Certificate?

A certificate proves

the identity of a website.

Example

```text id="tls2009"
library.example.com

↓

Certificate

↓

Verified
```

Without certificates,

anyone could pretend

to be your website.

______________________________________________________________________

# Certificate Authority (CA)

Who issues certificates?

Trusted organizations

called

Certificate Authorities.

Examples include:

- Let's Encrypt
- DigiCert
- GlobalSign

Workflow

```text id="tls2010"
Website

↓

Certificate Authority

↓

Certificate Issued

↓

Browser Trusts Site
```

______________________________________________________________________

# Simplified HTTPS Handshake

The real TLS handshake is complex,

but the basic idea is simple.

```text id="tls2011"
Client

↓

Hello

↓

Server

↓

Certificate

↓

Verify Certificate

↓

Generate Encryption Keys

↓

Encrypted Communication
```

After this,

all communication

is encrypted.

______________________________________________________________________

# HTTPS in FastAPI

FastAPI itself

usually doesn't handle HTTPS directly.

Instead,

HTTPS is terminated

at a reverse proxy.

Typical deployment

```text id="tls2012"
Browser

↓

HTTPS

↓

Nginx

↓

HTTP

↓

FastAPI
```

The reverse proxy manages:

- TLS
- Certificates
- Encryption

FastAPI focuses on application logic.

______________________________________________________________________

# Reverse Proxy

A reverse proxy

sits in front

of your application.

Examples:

- Nginx
- Apache
- Traefik
- HAProxy

Responsibilities include:

- HTTPS termination
- Load balancing
- Compression
- Request routing

______________________________________________________________________

# Secure Cookies

When using cookies,

mark them as:

```text id="tls2013"
Secure
```

Example

```http id="tls2014"
Set-Cookie:

session=abc123;

Secure;

HttpOnly;

SameSite=Lax
```

The `Secure` flag ensures

cookies are sent

only over HTTPS.

______________________________________________________________________

# HSTS

HSTS stands for

**HTTP Strict Transport Security**.

It tells browsers:

```text id="tls2015"
Always Use HTTPS
```

Even if a user types

```text id="tls2016"
http://library.example.com
```

the browser automatically upgrades

to HTTPS.

______________________________________________________________________

# Why HTTPS Alone Isn't Enough

HTTPS protects data

while it travels.

It does **not** protect against:

- SQL Injection
- XSS
- Broken Authentication
- Broken Access Control
- SSRF

You still need secure application code.

______________________________________________________________________

# Defense in Depth

A secure backend combines:

```text id="tls2017"
HTTPS

↓

Authentication

↓

Authorization

↓

Input Validation

↓

Logging

↓

Monitoring
```

HTTPS is only one layer.

______________________________________________________________________

# Best Practices

✅ Use HTTPS everywhere.

✅ Redirect HTTP to HTTPS.

✅ Use trusted certificates.

✅ Enable HSTS.

✅ Mark cookies as `Secure`.

✅ Keep TLS configurations updated.

✅ Use modern TLS versions.

______________________________________________________________________

# Common Mistakes

### Running Production Over HTTP

Every production application

should use HTTPS.

______________________________________________________________________

### Using Expired Certificates

Expired certificates

cause browsers

to warn users

and may block access.

Monitor certificate expiration.

______________________________________________________________________

### Assuming HTTPS Protects Everything

HTTPS protects communication,

not application logic.

______________________________________________________________________

### Hardcoding Certificates

Manage certificates

through your infrastructure

or reverse proxy,

not in application code.

______________________________________________________________________

# Quick Comparison

| HTTP | HTTPS |
| --------------------------- | ------------------------ |
| Plain text | Encrypted |
| No identity verification | Certificate verification |
| Vulnerable to interception | Protected communication |
| Not suitable for production | Production standard |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between HTTP and HTTPS?

HTTP transmits data in plain text, making it vulnerable to interception and modification. HTTPS uses TLS (Transport
Layer Security) to encrypt communication between the client and server, ensuring confidentiality, integrity, and server
authentication through digital certificates. HTTPS protects data while it is in transit but does not replace secure
application design or coding practices.

______________________________________________________________________

# Summary

In this lesson, you learned:

- HTTP vs HTTPS
- TLS
- SSL vs TLS
- Certificates
- Certificate Authorities
- HTTPS handshake
- Reverse proxies
- Secure cookies
- HSTS
- Best practices

______________________________________________________________________

# What's Next

[Secrets Management](21-secrets-management.md)

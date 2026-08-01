# Security - Part 32

# Replay Attacks

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What a Replay Attack is
- How Replay Attacks work
- Real-world examples
- Why HTTPS alone is not always enough
- Nonces
- Timestamps
- Idempotency Keys
- JWT replay considerations
- Best practices

______________________________________________________________________

# What is a Replay Attack?

A Replay Attack occurs when an attacker captures a **valid request** and sends it again later.

The request itself is legitimate.

The problem is that it is **executed more than once**.

Unlike SQL Injection or XSS,

the attacker does not modify the request.

They simply replay it.

______________________________________________________________________

# Typical Flow

```text id="ra3201"
Valid Request

↓

Captured

↓

Sent Again

↓

Server Processes Again
```

______________________________________________________________________

# Real-World Example

Imagine an online payment.

The user sends

```text id="ra3202"
POST /payments

Amount = ₹5000
```

The payment succeeds.

Later,

the attacker resends

the exact same request.

If the server processes it again,

the customer may be charged twice.

______________________________________________________________________

# Another Example

Suppose an API transfers money.

```text id="ra3203"
POST /transfer

₹10,000
```

Without replay protection,

the attacker can resend

the same request

multiple times.

______________________________________________________________________

# Why Does This Happen?

The server sees

a valid request.

It has:

- Valid authentication
- Valid parameters
- Correct format

Without additional checks,

the server cannot determine

whether it is the first request

or a replay.

______________________________________________________________________

# Doesn't HTTPS Prevent This?

A very common interview question.

**No.**

HTTPS encrypts communication

while it travels over the network.

It ensures:

- Confidentiality
- Integrity
- Server authentication

However,

if a legitimate request

is captured from another source (for example, malicious software on the client, compromised logs, or misuse within the
application),

HTTPS alone cannot determine

whether the request

has already been processed.

Replay protection

must be implemented

at the application level.

______________________________________________________________________

# Prevention 1

## Nonce

A **Nonce**

(Number used once)

is a unique random value

attached to every request.

Workflow

```text id="ra3204"
Request

↓

Nonce

↓

Server Stores Nonce

↓

Reuse?

↓

Reject
```

Every nonce

can be used

only once.

______________________________________________________________________

# Prevention 2

## Timestamp

Attach

the current timestamp.

Example

```text id="ra3205"
Request Time

↓

12:30:15
```

The server accepts

only requests

within a small time window.

Example

```text id="ra3206"
Valid

↓

Last 5 Minutes
```

Old requests

are rejected.

______________________________________________________________________

# Prevention 3

## Idempotency Keys

This is one of the most common solutions

for payment APIs.

The client generates

a unique key.

Example

```text id="ra3207"
Idempotency-Key

↓

A1B2C3D4
```

Workflow

```text id="ra3208"
Request

↓

Idempotency Key

↓

Server Stores Key

↓

Already Processed?

↓

Yes

↓

Return Previous Result
```

The payment

is executed only once,

even if the client retries.

______________________________________________________________________

# Why Are Idempotency Keys Useful?

Suppose

the client

never receives the response

because of a network issue.

The client retries

the same request.

Without an Idempotency Key,

two payments

might occur.

With the same key,

the server recognizes

the duplicate request

and safely returns

the original result.

______________________________________________________________________

# JWT Replay

JWTs are signed,

but they can still be replayed

while they remain valid.

Example

```text id="ra3209"
JWT

↓

Captured

↓

Used Again

↓

Still Valid
```

To reduce risk:

- Use short expiration times.
- Use HTTPS.
- Store tokens securely.
- Revoke tokens when necessary.

______________________________________________________________________

# Refresh Tokens

Refresh tokens

should receive

stronger protection

than access tokens.

Best practices include:

- Long random values
- Secure storage
- Rotation after every use

This reduces

the impact

of token theft.

______________________________________________________________________

# One-Time Passwords (OTP)

OTPs naturally prevent

replay attacks.

Workflow

```text id="ra3210"
OTP

↓

Use Once

↓

Invalidate
```

The same OTP

cannot be reused.

______________________________________________________________________

# API Design Example

A payment API

might require:

```text id="ra3211"
Authentication

↓

Authorization

↓

Idempotency Key

↓

Business Logic

↓

Payment
```

This protects

against accidental retries

and replay attacks.

______________________________________________________________________

# Defense in Depth

Secure APIs combine:

```text id="ra3212"
HTTPS

↓

Authentication

↓

Authorization

↓

Nonce

↓

Timestamp

↓

Idempotency Key

↓

Logging
```

______________________________________________________________________

# Best Practices

✅ Use HTTPS.

✅ Use Idempotency Keys for payment APIs.

✅ Validate timestamps.

✅ Use nonces where appropriate.

✅ Use short-lived JWTs.

✅ Rotate refresh tokens.

______________________________________________________________________

# Common Mistakes

### Assuming HTTPS Prevents Replay

HTTPS encrypts traffic,

but replay protection

must still be implemented

by the application.

______________________________________________________________________

### No Idempotency for Payments

Payment APIs

should always support

Idempotency Keys.

______________________________________________________________________

### Long-Lived Tokens

Short expiration times

reduce replay risk

if a token is compromised.

______________________________________________________________________

### Accepting Old Requests

Timestamp validation

helps reject

stale requests.

______________________________________________________________________

### Reusing OTPs

One-Time Passwords

must become invalid

after successful use.

______________________________________________________________________

# Quick Comparison

| Vulnerable | Secure |
| --------------------------------- | ------------------- |
| Same request processed repeatedly | Idempotency Key |
| No timestamp validation | Validate timestamps |
| Long-lived tokens | Short expiration |
| Reusable OTPs | One-time OTPs |
| No replay detection | Nonce / Idempotency |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is a Replay Attack, and how can developers prevent it?

A Replay Attack occurs when a valid request is captured and sent again, causing the server to execute the same action
multiple times. Developers can reduce the risk by using HTTPS, validating timestamps, generating one-time nonces,
implementing Idempotency Keys for operations such as payments, using short-lived access tokens, rotating refresh tokens,
and rejecting duplicate or expired requests.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Replay Attacks are
- Why they happen
- Why HTTPS alone is insufficient
- Nonces
- Timestamps
- Idempotency Keys
- JWT replay considerations
- Best practices

______________________________________________________________________

# What's Next

[Open Redirect](33-open-redirect.md)

# Complete HTTP Request Lifecycle Deep Dive

## 05. TLS, HTTPS and HTTP Protocols

> Target Audience: Backend Engineers (Beginner → Senior)
>
> Goal: Understand how HTTPS secures communication, what happens during the TLS handshake, how certificates work, how HTTP evolves from HTTP/1.1 to HTTP/3, and what actually happens inside the browser and server during secure communication.

______________________________________________________________________

# Introduction

In the previous chapter,

our browser

successfully established

a TCP connection.

```
Browser

↓

TCP Connection

Established
```

Now

the browser

could start sending

HTTP requests.

But there's a problem.

Without encryption,

anyone between

your computer

and the server

can read

everything.

Example

```
Username

Password

Credit Card

Cookies

JWT Token
```

This is why

HTTPS exists.

______________________________________________________________________

# HTTP vs HTTPS

Interview favorite.

## HTTP

```
Plain Text
```

Anyone

can read

the data.

______________________________________________________________________

## HTTPS

```
Encrypted
```

Only

the client

and

the server

can understand

the data.

______________________________________________________________________

# Example

Without HTTPS

```
Browser

↓

POST /login

↓

email=riyaz@gmail.com

password=MyPassword
```

Every router

between

you

and

Google

can read it.

______________________________________________________________________

With HTTPS

```
Browser

↓

Encrypted Bytes

↓

Internet

↓

Encrypted Bytes

↓

Google
```

Nobody

can read

the content.

______________________________________________________________________

# Where Does HTTPS Work?

```
Application

↓

HTTP

↓

TLS

↓

TCP

↓

IP

↓

Ethernet
```

Notice

TLS

sits

between

HTTP

and

TCP.

______________________________________________________________________

# SSL vs TLS

Interview favorite.

SSL

is old.

```
SSL 2.0

❌

Deprecated
```

```
SSL 3.0

❌

Deprecated
```

Modern systems use

```
TLS 1.2

TLS 1.3
```

People still say

"SSL Certificate"

but

almost everyone

actually means

TLS.

______________________________________________________________________

# What Does TLS Provide?

TLS provides

three things.

```
Confidentiality

↓

Integrity

↓

Authentication
```

______________________________________________________________________

# Confidentiality

Means

only

the sender

and receiver

can read

the message.

Achieved using

Encryption.

______________________________________________________________________

# Integrity

Means

the data

was not modified

during transmission.

If someone

changes

even

one byte,

TLS detects it.

______________________________________________________________________

# Authentication

How do you know

you're talking to

Google

instead of

a hacker?

TLS certificates

prove

the server's identity.

______________________________________________________________________

# Encryption Types

Interview favorite.

Two kinds

of encryption

exist.

```
Symmetric

↓

Same Key
```

```
Asymmetric

↓

Public Key

+

Private Key
```

______________________________________________________________________

# Symmetric Encryption

Example

```
AES
```

One key

encrypts

and

decrypts.

Fast.

Used

for

actual communication.

______________________________________________________________________

# Problem

How do

both sides

obtain

the same key

securely?

______________________________________________________________________

# Asymmetric Encryption

Uses

two keys.

```
Public Key

↓

Encrypt
```

```
Private Key

↓

Decrypt
```

Public Key

can be shared.

Private Key

must remain

secret.

______________________________________________________________________

# Why Not Use Asymmetric Encryption Always?

Interview favorite.

Because

it's slow.

Instead

TLS uses

```
Asymmetric

↓

Exchange Keys

↓

Symmetric

↓

Actual Data
```

Best

of both worlds.

______________________________________________________________________

# Digital Certificate

A certificate

contains

```
Domain

↓

Public Key

↓

Expiration

↓

Certificate Authority

↓

Signature
```

______________________________________________________________________

# Certificate Authority

Examples

- Let's Encrypt
- DigiCert
- GlobalSign
- Sectigo

Browsers

already trust

these organizations.

______________________________________________________________________

# What Happens Internally?

Suppose

Chrome connects

to

Google.

```
Browser

↓

TCP Connected

↓

Start TLS
```

______________________________________________________________________

# TLS Handshake

Interview favorite.

```
Client Hello

↓

Server Hello

↓

Certificate

↓

Key Exchange

↓

Session Keys

↓

Encrypted Communication
```

______________________________________________________________________

# Step 1

# Client Hello

Browser sends

```
Supported TLS Versions

Supported Cipher Suites

Random Number

Extensions

SNI
```

______________________________________________________________________

# What Is SNI?

Interview favorite.

SNI

means

```
Server Name Indication
```

Suppose

one server

hosts

```
google.com

gmail.com

maps.google.com
```

Browser tells

the server

which certificate

it wants.

______________________________________________________________________

# Step 2

# Server Hello

Server replies

```
TLS Version

Chosen Cipher

Random Number

Certificate
```

______________________________________________________________________

# Step 3

# Certificate Verification

Browser

checks

```
Certificate Expired?

↓

Correct Domain?

↓

Trusted CA?

↓

Signature Valid?
```

If

any check fails

browser displays

```
Your connection

is not private
```

______________________________________________________________________

# What Is Inside A Certificate?

Example

```
Subject

www.google.com
```

```
Issuer

Google Trust Services
```

```
Public Key
```

```
Valid Until

2030
```

______________________________________________________________________

# Step 4

# Key Exchange

Interview favorite.

Browser

and

server

generate

a shared secret.

Modern TLS

usually uses

```
ECDHE
```

Elliptic Curve

Diffie-Hellman

Ephemeral.

______________________________________________________________________

# Why ECDHE?

Provides

```
Perfect Forward Secrecy
```

Even if

the server's

private key

is stolen later,

old conversations

remain secure.

______________________________________________________________________

# Step 5

# Session Key

Both sides

now generate

the same

```
AES Session Key
```

No one else

knows it.

______________________________________________________________________

# Step 6

# Secure Communication

Now

every HTTP request

is encrypted.

```
HTTP

↓

AES Encryption

↓

TLS

↓

TCP
```

______________________________________________________________________

# Complete TLS Flow

```
TCP Connected

↓

Client Hello

↓

Server Hello

↓

Certificate

↓

Certificate Validation

↓

Key Exchange

↓

Session Key

↓

Encrypted HTTP
```

______________________________________________________________________

# Cipher Suite

Interview favorite.

A cipher suite

defines

```
Key Exchange

+

Encryption

+

Integrity
```

Example

```
TLS_AES_256_GCM_SHA384
```

______________________________________________________________________

# Session Resumption

Opening

new TLS connections

is expensive.

Browsers

reuse

previous sessions

when possible.

Benefits

- Faster
- Less CPU
- Lower latency

______________________________________________________________________

# Perfect Forward Secrecy

Suppose

someone records

your HTTPS traffic

today.

Ten years later

they steal

Google's private key.

Can they decrypt

today's traffic?

With

PFS

```
No
```

______________________________________________________________________

# HTTPS Request

Only after

TLS completes

does the browser

send

```
GET /

HTTP/1.1
```

Now

everything

is encrypted.

______________________________________________________________________

# What Actually Gets Encrypted?

Entire HTTP payload.

Examples

```
Headers

Cookies

JWT

Body

JSON

HTML
```

Only

the destination IP

and

port

remain visible

to routers.

______________________________________________________________________

# HTTP Versions

Interview favorite.

______________________________________________________________________

## HTTP/1.1

Features

- One request per connection
- Keep Alive
- Text protocol

Problem

```
Head Of Line Blocking
```

______________________________________________________________________

## HTTP/2

Features

- Multiplexing
- Binary protocol
- Header Compression
- Multiple streams

Much faster.

______________________________________________________________________

## HTTP/3

Uses

```
QUIC
```

instead of

TCP.

Benefits

- Lower latency
- Faster reconnects
- Better performance
- Built-in TLS

______________________________________________________________________

# HTTP Request Example

```
GET /users/1 HTTP/1.1

Host: api.company.com

Authorization: Bearer JWT

Accept: application/json
```

______________________________________________________________________

# HTTP Response Example

```
HTTP/1.1 200 OK

Content-Type: application/json

Cache-Control: no-cache
```

______________________________________________________________________

# HTTP Methods

Interview favorite.

```
GET

Read
```

```
POST

Create
```

```
PUT

Replace
```

```
PATCH

Update
```

```
DELETE

Remove
```

______________________________________________________________________

# HTTP Status Codes

```
200

Success
```

```
201

Created
```

```
400

Bad Request
```

```
401

Unauthorized
```

```
403

Forbidden
```

```
404

Not Found
```

```
500

Internal Server Error
```

______________________________________________________________________

# Common TLS Attacks

## Man-in-the-Middle

Without HTTPS

attacker

reads

all traffic.

TLS

prevents this

through

certificate validation

and encryption.

______________________________________________________________________

## Certificate Spoofing

Attacker

uses

a fake certificate.

Browser

rejects it

if

the CA

isn't trusted

or

the domain

doesn't match.

______________________________________________________________________

## Downgrade Attack

Attacker

tries

to force

an older,

weaker protocol.

Modern browsers

disable

old SSL versions.

______________________________________________________________________

## Replay Attack

Captured packets

are replayed.

TLS uses

random values

and session keys

to prevent this.

______________________________________________________________________

# HSTS

Interview favorite.

HTTP Strict Transport Security.

Browser remembers

```
Always use

HTTPS
```

Future requests

never use

plain HTTP.

______________________________________________________________________

# Certificate Pinning

Application

expects

a specific certificate

or

public key.

Useful

for

high-security

mobile apps.

______________________________________________________________________

# Mutual TLS (mTLS)

Normally

only

the server

proves

its identity.

With mTLS

```
Client

↓

Certificate

↓

Server

↓

Certificate
```

Both sides

authenticate

each other.

Used in

- Service Mesh
- Banking
- Internal APIs

______________________________________________________________________

# What Happens Inside The Browser?

```
TCP Connected

↓

Start TLS

↓

Receive Certificate

↓

Verify CA

↓

Verify Domain

↓

Generate Session Key

↓

Store Session

↓

Encrypted Communication
```

______________________________________________________________________

# What Happens Inside The Server?

```
TCP Accepted

↓

Load Certificate

↓

Private Key

↓

Negotiate Cipher

↓

Generate Session Key

↓

Decrypt Requests

↓

Encrypt Responses
```

______________________________________________________________________

# Technologies Used

| Component | Technologies |
|-----------|--------------|
| TLS Library | OpenSSL, BoringSSL, LibreSSL |
| Certificates | X.509 |
| CAs | Let's Encrypt, DigiCert |
| Symmetric Encryption | AES-128, AES-256, ChaCha20 |
| Asymmetric Encryption | RSA, ECDSA |
| Key Exchange | ECDHE |
| HTTP Server | Nginx, Envoy, Apache |

______________________________________________________________________

# Common Interview Questions

## Why do we need both asymmetric and symmetric encryption?

Asymmetric encryption securely exchanges the session key, while symmetric encryption efficiently encrypts the actual
data because it is much faster.

______________________________________________________________________

## Why doesn't HTTPS encrypt the destination IP?

Routers need the destination IP address to know where to forward packets. Encrypting it would make routing impossible.

______________________________________________________________________

## Why is TLS faster after the handshake?

After the handshake, both sides use a shared symmetric session key (such as AES), which is significantly faster than
asymmetric encryption.

______________________________________________________________________

## What is the purpose of a Certificate Authority?

A Certificate Authority verifies domain ownership and signs certificates, allowing browsers to trust the server's
identity.

______________________________________________________________________

## Why is HTTP/2 faster than HTTP/1.1?

HTTP/2 supports multiplexing, allowing multiple requests and responses to share a single connection simultaneously,
reducing latency and improving performance.

______________________________________________________________________

## Why does HTTP/3 use QUIC?

QUIC runs over UDP and integrates TLS, reducing connection setup time, avoiding TCP head-of-line blocking, and improving
performance on unreliable networks.

______________________________________________________________________

# Interview Deep Dive

## Question

Walk me through the TLS handshake.

### Answer

After the TCP connection is established, the client sends a Client Hello containing supported TLS versions, cipher
suites, and a random value. The server responds with a Server Hello, selects a cipher suite, and sends its certificate.
The client validates the certificate, both sides perform a key exchange (typically ECDHE), derive a shared session key,
and then all subsequent HTTP traffic is encrypted using symmetric encryption such as AES.

______________________________________________________________________

# Summary

HTTPS secures communication by combining the strengths of asymmetric and symmetric cryptography.

Key concepts include

- TLS Handshake
- Certificates
- Certificate Authorities
- Public & Private Keys
- Session Keys
- Cipher Suites
- Perfect Forward Secrecy
- HTTP/1.1
- HTTP/2
- HTTP/3
- HSTS
- mTLS

At this point,

the browser has established a **secure encrypted channel** to the destination server.

The next step is understanding **what happens when the encrypted request reaches edge infrastructure such as CDNs**
before it finally arrives at your backend application.

______________________________________________________________________

# Next

[06. CDN, Edge Network and Caching](06-cdn-edge-network-and-caching.md)

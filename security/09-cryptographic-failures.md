# Security - Part 9

# Cryptographic Failures

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What cryptography is
- Encryption vs Hashing vs Encoding
- Symmetric vs Asymmetric Encryption
- Digital Signatures
- Password Hashing
- Salting
- Secrets Management
- Secure Python implementations
- Common cryptographic mistakes

______________________________________________________________________

# What is Cryptography?

Cryptography is the practice of protecting information so that only authorized parties can read or verify it.

Backend developers use cryptography every day, often without realizing it.

Examples:

- HTTPS
- JWT
- Password Hashing
- Digital Signatures
- API Keys
- Secure Cookies

______________________________________________________________________

# Why Do We Need Cryptography?

Imagine your application sends:

```text id="crypto901"
Username

↓

Password

↓

Internet
```

Without cryptography,

anyone intercepting the traffic could read the password.

Instead,

we protect the communication and stored data using cryptographic techniques.

______________________________________________________________________

# Four Things Backend Developers Should Know

There are four concepts that are often confused.

```text id="crypto902"
Encoding

↓

Hashing

↓

Encryption

↓

Signing
```

Let's understand each.

______________________________________________________________________

# Encoding

Encoding changes data into another format.

Example:

```text id="crypto903"
Hello

↓

SGVsbG8=
```

(Base64 encoding)

Purpose:

- Data transport
- Compatibility

Important:

Encoding is **not security**.

Anyone can decode Base64.

______________________________________________________________________

# Hashing

Hashing converts data into a fixed-length value.

Example

```text id="crypto904"
password123

↓

Hash

↓

9b876...
```

Properties:

- One-way operation
- Cannot be reversed
- Same input → Same hash

Used for:

- Password storage
- File integrity
- Checksums

______________________________________________________________________

# Encryption

Encryption transforms readable data into unreadable ciphertext.

Unlike hashing,

encryption can be reversed using a key.

```text id="crypto905"
Plain Text

↓

Encryption Key

↓

Cipher Text

↓

Decryption Key

↓

Plain Text
```

Used for:

- HTTPS
- Secure file storage
- Database encryption
- API communication

______________________________________________________________________

# Digital Signatures

A digital signature proves:

- The data came from the expected sender.
- The data was not modified.

Example

```text id="crypto906"
Message

↓

Private Key

↓

Digital Signature

↓

Receiver

↓

Public Key

↓

Verified
```

JWT signatures work using this principle.

______________________________________________________________________

# Encoding vs Hashing vs Encryption

| Technique | Reversible? | Primary Use |
| ---------- | ----------- | ------------------------- |
| Encoding | Yes | Data transport |
| Hashing | No | Passwords, integrity |
| Encryption | Yes | Protect confidential data |

One of the most common interview questions.

______________________________________________________________________

# Symmetric Encryption

One key is used for both encryption and decryption.

```text id="crypto907"
Secret Key

↓

Encrypt

↓

Decrypt
```

Examples:

- AES

Advantages:

- Fast
- Efficient

Disadvantage:

Both parties must securely share the same key.

______________________________________________________________________

# Asymmetric Encryption

Uses two keys.

```text id="crypto908"
Public Key

↓

Encrypt

↓

Private Key

↓

Decrypt
```

Examples:

- RSA
- ECC

Advantages:

- No shared secret required initially
- Used in HTTPS and digital signatures

______________________________________________________________________

# Password Hashing

Passwords should **never** be encrypted.

They should be hashed.

Example

```python id="crypto909"
import bcrypt

password = b"password123"

hashed = bcrypt.hashpw(
    password,
    bcrypt.gensalt()
)
```

Verification

```python id="crypto910"
bcrypt.checkpw(
    password,
    hashed
)
```

______________________________________________________________________

# Why Not Encrypt Passwords?

If passwords are encrypted,

someone who obtains the encryption key

can decrypt every password.

Hashing avoids this problem.

The server verifies passwords

without ever recovering the original password.

______________________________________________________________________

# Salting

Suppose two users choose:

```text id="crypto911"
password123
```

Without salting,

their hashes are identical.

With salting,

each password receives a unique random value before hashing.

```text id="crypto912"
Password

+

Random Salt

↓

bcrypt
```

bcrypt automatically generates and stores the salt.

______________________________________________________________________

# Secrets Management

Applications use secrets such as:

- JWT Secret Keys
- Database Passwords
- API Keys
- OAuth Client Secrets

Never store them like this.

```python id="crypto913"
SECRET_KEY = "my-secret-key"
```

Instead,

load them securely.

```python id="crypto914"
import os

SECRET_KEY = os.getenv("JWT_SECRET")
```

Production systems often use:

- Docker Secrets
- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault

______________________________________________________________________

# Secure Data Encryption

Python's

`cryptography`

library provides modern encryption primitives.

Example

```python id="crypto915"
from cryptography.fernet import Fernet

key = Fernet.generate_key()

cipher = Fernet(key)

encrypted = cipher.encrypt(
    b"Sensitive Data"
)

decrypted = cipher.decrypt(
    encrypted
)
```

Notice:

Encryption protects confidential data,

not passwords.

______________________________________________________________________

# Defense in Depth

Cryptography is only one layer.

A secure application combines:

```text id="crypto916"
HTTPS

↓

Encryption

↓

Hashing

↓

Secrets Management

↓

Authentication

↓

Authorization
```

______________________________________________________________________

# Best Practices

✅ Hash passwords using bcrypt or Argon2.

✅ Use HTTPS.

✅ Store secrets outside source code.

✅ Use modern cryptographic libraries.

✅ Rotate secrets when necessary.

✅ Encrypt sensitive data at rest when required.

______________________________________________________________________

# Common Mistakes

### Using Base64 as Security

Base64 is encoding,

not encryption.

______________________________________________________________________

### Encrypting Passwords

Passwords should be hashed,

not encrypted.

______________________________________________________________________

### Using SHA256 for Passwords

Use bcrypt,

Argon2,

or scrypt instead.

______________________________________________________________________

### Hardcoding Secrets

Secrets belong in secure configuration,

not in source code.

______________________________________________________________________

### Writing Your Own Cryptography

Never implement your own encryption algorithms.

Use trusted libraries.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| --------------------- | -------------------------------------- |
| Base64 for protection | Proper encryption |
| SHA256 passwords | bcrypt / Argon2 |
| Hardcoded secrets | Secret manager / Environment variables |
| Custom crypto | Trusted libraries |
| Plain-text secrets | Encrypted storage |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between hashing and encryption?

Hashing is a one-way operation used to verify data without recovering the original value, making it ideal for password
storage. Encryption is a reversible process that protects confidential information using cryptographic keys and is used
for securing data such as files, network communication, and database fields. Passwords should be hashed, while sensitive
information that must later be read should be encrypted.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What cryptography is
- Encoding vs Hashing vs Encryption
- Digital signatures
- Symmetric vs Asymmetric encryption
- Password hashing
- Salting
- Secrets management
- Secure Python examples
- Best practices

______________________________________________________________________

# What's Next

[Security Misconfiguration](10-security-misconfiguration.md)

# 33. Backend Security

**Previous:** [32. Production Debugging & Incident Response](./32-production-debugging.md)

**Next:** [34. Git & Engineering Workflow](./34-git.md)

______________________________________________________________________

## Objective

By the end of this topic, you should be able to:

- Explain the major security risks relevant to Python backend systems.
- Recognize common OWASP vulnerability classes.
- Prevent SQL injection, XSS, CSRF, SSRF and command injection.
- Understand authentication vs authorization.
- Explain common JWT and OAuth2 security considerations.
- Secure APIs with HTTPS, CORS, security headers and rate limiting.
- Handle file uploads safely.
- Protect secrets and credentials.
- Apply least-privilege principles.
- Understand dependency and supply-chain security.
- Answer practical security questions expected from a 5+ year backend engineer.

______________________________________________________________________

# 1. Security Mindset

Backend security is not a single feature.

Security must be considered across:

```text
Client
 ↓
Network
 ↓
Authentication
 ↓
Authorization
 ↓
Validation
 ↓
Business logic
 ↓
Database
 ↓
External services
 ↓
Infrastructure
```

A secure backend assumes that user-controlled input can be malicious.

______________________________________________________________________

# 2. OWASP Fundamentals

OWASP provides widely used guidance for application security.

For interviews, understand the major vulnerability categories rather than memorizing every OWASP list item.

Important backend concerns include:

- Injection
- Broken authentication
- Broken authorization/access control
- Cross-site scripting
- CSRF
- SSRF
- Security misconfiguration
- Vulnerable dependencies
- Sensitive data exposure
- Insufficient logging/monitoring

The exact OWASP Top 10 list can evolve, so focus on the underlying security principles.

______________________________________________________________________

# 3. Authentication vs Authorization

These are frequently confused.

### Authentication

Answers:

> Who are you?

Examples:

```text
Username/password
JWT
OAuth2
Session cookie
```

### Authorization

Answers:

> What are you allowed to do?

Examples:

```text
Admin
Manager
User
Read-only user
```

A user can be authenticated but not authorized to perform an operation.

______________________________________________________________________

# 4. Broken Authentication

Authentication failures can include:

- Weak passwords
- Credential stuffing
- Poor session management
- Long-lived tokens
- Token leakage
- Missing brute-force protection
- Incorrect password handling
- Insecure password reset flows

A backend should protect the entire authentication lifecycle, not just the login endpoint.

______________________________________________________________________

# 5. Password Storage

Never store plaintext passwords.

Use a password hashing algorithm designed for password storage, such as:

```text
Argon2
bcrypt
scrypt
```

Conceptually:

```text
Password
   ↓
Password hashing function
   ↓
Stored password hash
```

During login:

```text
Submitted password
   ↓
Verify against stored hash
```

Do not use a general-purpose fast hash such as plain SHA-256 as a password-storage solution.

______________________________________________________________________

# 6. SQL Injection

SQL injection occurs when untrusted input changes the structure of a SQL query.

Unsafe conceptual example:

```python
query = f"SELECT * FROM users WHERE name = '{name}'"
```

If `name` contains malicious SQL syntax, the generated query may behave unexpectedly.

______________________________________________________________________

# 7. Preventing SQL Injection

Use parameterized queries:

```python
cursor.execute(
    "SELECT * FROM users WHERE name = %s",
    (name,),
)
```

With SQLAlchemy, prefer expression/query APIs and bound parameters rather than constructing SQL strings from user input.

The key principle is:

> **Data should remain data, not become executable SQL syntax.**

______________________________________________________________________

# 8. ORM Does Not Automatically Make Everything Safe

Using an ORM reduces many injection risks when used correctly.

However, raw SQL can still be dangerous if user input is interpolated directly.

Unsafe:

```python
text(f"SELECT * FROM users WHERE name = '{name}'")
```

Prefer:

```python
text("SELECT * FROM users WHERE name = :name")
```

with a bound parameter.

______________________________________________________________________

# 9. SQL Injection Beyond WHERE Clauses

Injection risks can also appear in:

- `ORDER BY`
- Dynamic table names
- Search filters
- Raw SQL
- Reporting queries
- Stored procedures
- Database administration interfaces

Parameters cannot always be used for identifiers.

When identifiers must be selected dynamically, use a strict allowlist.

______________________________________________________________________

# 10. XSS

Cross-Site Scripting occurs when attacker-controlled content is interpreted as executable browser-side code.

Common forms include:

```text
Stored XSS
Reflected XSS
DOM-based XSS
```

A backend can contribute to XSS vulnerabilities by returning unsafe user-controlled content.

______________________________________________________________________

# 11. Stored XSS

An attacker submits malicious content that is stored by the application.

Example:

```text
User profile
Comment
Message
```

Later, another user's browser renders that content as executable HTML/JavaScript.

______________________________________________________________________

# 12. Reflected XSS

Malicious content is supplied in a request and reflected into the response.

Example:

```text
/search?q=<malicious-content>
```

If the application renders the value without appropriate output encoding, the browser may interpret it as code.

______________________________________________________________________

# 13. XSS Prevention

Use:

- Context-aware output encoding
- Safe templating
- Input validation where appropriate
- Content Security Policy where applicable
- Avoid unsafe HTML rendering

Do not rely only on filtering a few known strings.

______________________________________________________________________

# 14. CSRF

Cross-Site Request Forgery tricks a user's browser into making an authenticated request to a target application.

It is especially relevant when authentication relies on automatically attached browser credentials such as cookies.

Example concept:

```text
Victim logged into bank
        ↓
Attacker-controlled page
        ↓
Browser sends bank cookie automatically
        ↓
Unwanted state-changing request
```

______________________________________________________________________

# 15. CSRF Protection

Common approaches include:

- CSRF tokens
- SameSite cookies
- Origin/Referer validation where appropriate
- Avoiding unsafe state-changing GET requests

The correct strategy depends on the authentication mechanism and application architecture.

______________________________________________________________________

# 16. JWT

JWT stands for JSON Web Token.

A JWT commonly contains:

```text
Header
Payload
Signature
```

Conceptually:

```text
header.payload.signature
```

______________________________________________________________________

# 17. JWT Is Signed, Not Necessarily Encrypted

A signed JWT provides integrity/authenticity when properly validated.

The payload is generally readable by whoever possesses the token.

Therefore:

> Do not put sensitive secrets in ordinary JWT claims merely because the token is signed.

______________________________________________________________________

# 18. JWT Validation

A backend should validate relevant properties such as:

- Signature
- Expected signing algorithm
- Issuer where applicable
- Audience where applicable
- Expiration
- Not-before time where applicable
- Required claims

Do not simply decode a JWT and trust its contents.

______________________________________________________________________

# 19. JWT Expiration

Access tokens should generally have an appropriate lifetime.

Long-lived tokens increase the potential impact of token theft.

A common architecture uses:

```text
Short-lived access token
+
Controlled refresh mechanism
```

The exact design depends on the application.

______________________________________________________________________

# 20. JWT Revocation Challenge

JWTs are often designed to be stateless.

That creates a trade-off:

```text
Stateless verification
        vs
Immediate revocation
```

A compromised token can remain usable until expiration unless the system has additional revocation mechanisms.

______________________________________________________________________

# 21. OAuth2

OAuth2 is an authorization framework.

It allows an application to obtain delegated access to resources without directly handling another system's password.

Important concepts include:

```text
Resource Owner
Client
Authorization Server
Resource Server
Access Token
```

______________________________________________________________________

# 22. OAuth2 Authorization Code Flow

A common browser/application flow is:

```text
User
 ↓
Client
 ↓
Authorization Server
 ↓
User authentication/consent
 ↓
Authorization Code
 ↓
Client
 ↓
Token endpoint
 ↓
Access Token
 ↓
Resource Server
```

For public clients such as SPAs/mobile applications, PKCE is an important protection.

______________________________________________________________________

# 23. OAuth2 vs JWT

They are not alternatives in the same category.

```text
OAuth2
→ authorization framework/protocol

JWT
→ token format
```

OAuth2 access tokens may use JWTs, but OAuth2 does not require JWT.

______________________________________________________________________

# 24. HTTPS

HTTPS is HTTP over TLS.

It provides protection against network attackers by providing:

- Encryption
- Integrity
- Server authentication through certificates

Conceptually:

```text
HTTP
 ↓
TLS
 ↓
TCP
```

______________________________________________________________________

# 25. TLS

TLS protects communication between endpoints.

The handshake establishes cryptographic parameters and authenticates the server using certificates.

After the handshake, application data is exchanged over the protected connection.

______________________________________________________________________

# 26. HTTPS Best Practices

Use:

- Valid certificates
- Modern TLS configurations
- HTTP to HTTPS redirection where appropriate
- Secure cookies
- HSTS where appropriate
- Proper certificate validation

Do not disable certificate verification simply to make a connection work.

______________________________________________________________________

# 27. CORS

CORS stands for Cross-Origin Resource Sharing.

Browsers enforce same-origin restrictions.

CORS allows a server to explicitly permit browser requests from selected origins.

Example:

```text
https://frontend.example.com
```

may be allowed to call:

```text
https://api.example.com
```

______________________________________________________________________

# 28. CORS Is Not Authentication

CORS controls browser cross-origin behavior.

It does not:

```text
authenticate users
```

and does not replace:

```text
authorization
```

A server-to-server request is not protected by browser CORS rules.

______________________________________________________________________

# 29. CORS Configuration

Avoid blindly allowing:

```text
*
```

especially when credentials are involved.

Prefer an explicit allowlist of trusted origins where appropriate.

Also understand:

```text
Allowed methods
Allowed headers
Credentials
Preflight requests
```

______________________________________________________________________

# 30. SSRF

Server-Side Request Forgery occurs when an attacker can influence a server into making a request to an unintended
destination.

Example:

```text
User supplies URL
      ↓
Backend fetches URL
      ↓
Attacker targets internal service
```

Potential targets can include:

```text
Internal APIs
Cloud metadata endpoints
Admin interfaces
Private network services
```

______________________________________________________________________

# 31. SSRF Prevention

Use:

- Strict URL validation
- Allowlisted destinations
- Network egress controls
- Block private/internal ranges where appropriate
- Safe DNS/IP resolution strategy
- Redirect validation
- Appropriate timeouts

Do not rely solely on checking the initial hostname.

______________________________________________________________________

# 32. SSRF and DNS Rebinding

An attacker-controlled hostname may resolve differently over time.

Therefore a naive:

```text
Check hostname
 ↓
Allow
 ↓
Resolve/connect later
```

can be unsafe.

Security controls should account for the actual destination being contacted.

______________________________________________________________________

# 33. Command Injection

Command injection occurs when untrusted input becomes part of an operating-system command.

Unsafe pattern:

```python
os.system(f"convert {filename}")
```

If `filename` is attacker-controlled, command syntax may be injected.

______________________________________________________________________

# 34. Preventing Command Injection

Prefer direct subprocess APIs with argument arrays:

```python
subprocess.run(
    ["convert", filename],
    check=True,
)
```

Also:

- Validate inputs.
- Use allowlists.
- Avoid shell execution unless necessary.
- Do not pass untrusted strings to `shell=True`.

______________________________________________________________________

# 35. Path Traversal

Path traversal occurs when an attacker manipulates a path to access files outside the intended directory.

Conceptual attack:

```text
../../secret.txt
```

The important principle is:

> Never assume a filename supplied by a client stays inside the intended directory.

______________________________________________________________________

# 36. Path Traversal Prevention

Use:

- Safe path resolution
- Allowlisted filenames/IDs
- Controlled storage directories
- Canonicalization
- Boundary checks

Conceptually:

```python
resolved = candidate.resolve()

if base not in resolved.parents:
    reject()
```

The exact implementation should account for platform and symlink behavior.

______________________________________________________________________

# 37. File Upload Security

File uploads are a common attack surface.

Risks include:

- Malicious files
- Huge files
- Executable content
- Path traversal
- MIME spoofing
- Archive bombs
- Malware
- Resource exhaustion
- Public exposure

______________________________________________________________________

# 38. Secure File Upload Strategy

Consider:

```text
Authentication
 ↓
Authorization
 ↓
File size limit
 ↓
Extension validation
 ↓
Content/type validation
 ↓
Safe generated filename
 ↓
Non-executable storage
 ↓
Malware scanning where required
 ↓
Controlled download
```

Do not trust the original filename.

______________________________________________________________________

# 39. File Names

Avoid storing uploads using attacker-controlled names.

Instead generate server-side identifiers:

```text
user-provided name:
../../shell.py

stored name:
2f4b8d2e-....bin
```

Keep the original display name separately if required.

______________________________________________________________________

# 40. Archive Extraction

Archives can contain paths such as:

```text
../../application.py
```

Blindly extracting archives can overwrite files outside the intended directory.

Validate archive members before extraction.

______________________________________________________________________

# 41. Secrets

Secrets include:

- Database passwords
- API keys
- JWT signing keys
- OAuth client secrets
- Cloud credentials
- Encryption keys

Never hardcode production secrets in source code.

______________________________________________________________________

# 42. Secret Storage

Prefer:

```text
Secret manager
Environment/injected configuration
Protected deployment configuration
```

depending on the deployment platform.

Avoid committing secrets to Git.

______________________________________________________________________

# 43. Secret Leakage

Secrets can accidentally appear in:

```text
Source code
Git history
Logs
Error messages
Stack traces
Environment dumps
Docker images
CI logs
```

Protect against leakage throughout the lifecycle.

______________________________________________________________________

# 44. Secret Rotation

A good secret-management strategy supports:

```text
Creation
Storage
Access control
Rotation
Revocation
Auditing
```

If a credential leaks, the response should include revoking/rotating it rather than merely deleting it from the latest
source file.

______________________________________________________________________

# 45. Rate Limiting

Rate limiting controls how much traffic a client can generate.

Example:

```text
100 requests/minute/user
```

It can protect against:

- Brute-force attempts
- Abuse
- Resource exhaustion
- Accidental overload
- API scraping

______________________________________________________________________

# 46. Rate-Limit Dimensions

Limits can be applied by:

```text
IP
User
API key
Tenant
Endpoint
Global service
```

The correct key depends on the threat model.

______________________________________________________________________

# 47. Distributed Rate Limiting

In a multi-instance backend:

```text
Request
 ↓
Load Balancer
 ↓
Instance A/B/C
```

An in-memory counter on each instance may not provide a global limit.

A shared mechanism such as Redis can be used when appropriate.

______________________________________________________________________

# 48. Rate Limiting Algorithms

Know the concepts:

- Fixed window
- Sliding window
- Token bucket
- Leaky bucket

For interviews, understand the trade-offs rather than memorizing implementation details.

______________________________________________________________________

# 49. Security Headers

Useful security-related headers include:

```text
Strict-Transport-Security
Content-Security-Policy
X-Content-Type-Options
Referrer-Policy
Permissions-Policy
```

Some legacy headers are obsolete or browser-dependent, so focus on modern security controls.

______________________________________________________________________

# 50. Content Security Policy

CSP can restrict what browsers are allowed to load or execute.

Conceptually:

```text
Content-Security-Policy
```

can reduce the impact of some XSS attacks.

CSP should be designed deliberately rather than copied blindly.

______________________________________________________________________

# 51. Secure Cookies

Security-sensitive cookies commonly use:

```text
Secure
HttpOnly
SameSite
```

### Secure

Cookie is sent over HTTPS.

### HttpOnly

JavaScript cannot directly read the cookie.

### SameSite

Controls cross-site cookie behavior.

______________________________________________________________________

# 52. Dependency Security

Python applications depend on many packages.

Risks include:

- Known vulnerabilities
- Malicious packages
- Compromised maintainers
- Dependency confusion
- Transitive dependencies

Use controlled dependency management and regularly assess vulnerabilities.

______________________________________________________________________

# 53. Dependency Pinning

Locking dependencies helps provide reproducible builds.

For example:

```text
requirements lockfile
poetry.lock
uv.lock
```

depending on the project tooling.

Pinning alone is not enough; vulnerable versions must still be updated.

______________________________________________________________________

# 54. Dependency Updates

A practical strategy:

```text
Scan
 ↓
Prioritize
 ↓
Test
 ↓
Upgrade
 ↓
Deploy
 ↓
Monitor
```

Do not blindly upgrade every dependency directly in production.

______________________________________________________________________

# 55. Dependency Confusion

Dependency confusion can occur when an attacker publishes a malicious package with a name that an internal build system
resolves incorrectly.

Controls include:

- Trusted package indexes
- Package source configuration
- Dependency locking
- Internal package naming conventions
- Supply-chain controls

______________________________________________________________________

# 56. Least Privilege

Give users, services and applications only the permissions they require.

Examples:

```text
API
 ↓
Database user with required permissions
```

rather than:

```text
API
 ↓
Database administrator
```

Similarly:

```text
Service
 ↓
Only required filesystem permissions
```

______________________________________________________________________

# 57. Database Least Privilege

An application generally should not need unrestricted database administration privileges.

For example, separate capabilities where appropriate:

```text
Application user
→ SELECT/INSERT/UPDATE/DELETE

Migration/admin user
→ schema changes
```

This reduces the blast radius of an application compromise.

______________________________________________________________________

# 58. Authorization

Authorization should be checked on the server.

Do not rely on:

```text
Hidden frontend buttons
```

for access control.

Example:

```text
GET /users/123
```

must verify that the authenticated user is allowed to access user 123.

______________________________________________________________________

# 59. IDOR / Object-Level Authorization

A common authorization problem is allowing users to access another user's object by changing an ID.

Example:

```text
/user/orders/100
```

becomes:

```text
/user/orders/101
```

The backend must verify ownership/authorization for the requested object.

______________________________________________________________________

# 60. Role-Based Access Control

RBAC assigns permissions through roles.

Example:

```text
Admin
Manager
User
```

Then:

```text
Admin → manage users
Manager → manage team resources
User → access own resources
```

Avoid scattering authorization logic inconsistently throughout the codebase.

______________________________________________________________________

# 61. Authentication Dependency vs Authorization Dependency

In a FastAPI application:

```text
Authentication
→ identify user

Authorization
→ determine whether user can perform operation
```

They are separate responsibilities even if implemented through nested dependencies.

______________________________________________________________________

# 62. Input Validation

Validate:

- Type
- Length
- Range
- Format
- Allowed values
- Business constraints

Pydantic models are useful for structural validation in Python APIs.

But validation is not a substitute for authorization or safe query construction.

______________________________________________________________________

# 63. Validation vs Sanitization

### Validation

Determines whether input satisfies expected rules.

### Sanitization

Transforms potentially unsafe input into an acceptable form.

Prefer strict validation where possible.

Do not rely on sanitization as the only defense against injection.

______________________________________________________________________

# 64. Error Handling

Production errors should not expose:

```text
Passwords
Tokens
Secrets
Internal paths
SQL statements
Stack traces
Infrastructure details
```

Return safe client-facing errors while keeping detailed diagnostics in protected logs.

______________________________________________________________________

# 65. Security Logging

Useful security events can include:

- Authentication failures
- Authorization failures
- Password reset events
- Token events
- Privilege changes
- Suspicious requests
- Administrative operations

Logs should support investigation without exposing sensitive credentials.

______________________________________________________________________

# 66. Logging and Sensitive Data

Avoid logging:

```text
Passwords
Access tokens
Refresh tokens
API keys
Session secrets
Full payment credentials
```

Mask or omit sensitive fields.

______________________________________________________________________

# 67. Secure API Design

A secure backend commonly combines:

```text
HTTPS
+
Authentication
+
Authorization
+
Validation
+
Safe database access
+
Rate limiting
+
Secure error handling
+
Logging/monitoring
```

No single mechanism provides complete protection.

______________________________________________________________________

# 68. Defense in Depth

Defense in depth means using multiple independent security controls.

Example:

```text
Authentication
 ↓
Authorization
 ↓
Input validation
 ↓
Parameterized SQL
 ↓
Least-privileged DB account
 ↓
Network restrictions
 ↓
Monitoring
```

If one control fails, others still reduce impact.

______________________________________________________________________

# 69. Security by Default

Prefer secure defaults.

Examples:

```text
HTTPS enabled
Cookies Secure/HttpOnly where appropriate
CORS allowlist
Authentication required
Least-privileged service account
Debug disabled in production
Safe error responses
```

A developer should not have to remember to enable basic security for every endpoint.

______________________________________________________________________

# 70. Common Security Mistakes

## Mistake 1 — Trusting the frontend

The backend must enforce authorization.

## Mistake 2 — Building SQL with strings

Use parameterized queries.

## Mistake 3 — Treating JWT decoding as validation

Validate signature and relevant claims.

## Mistake 4 — Storing plaintext passwords

Use password hashing algorithms designed for passwords.

## Mistake 5 — Using `chmod 777` or excessive permissions

Apply least privilege.

## Mistake 6 — Allowing arbitrary outbound URLs

Protect against SSRF.

## Mistake 7 — Trusting uploaded filenames

Generate safe server-side names.

## Mistake 8 — Logging secrets

Mask or omit credentials.

## Mistake 9 — Treating CORS as authentication

CORS is a browser security mechanism, not an authorization system.

## Mistake 10 — Blindly trusting file extensions

Validate content and enforce safe storage.

______________________________________________________________________

# 71. Security Review Workflow

When reviewing a new backend endpoint, ask:

```text
1. Who can call it?
2. How are they authenticated?
3. What are they authorized to access?
4. What input is user-controlled?
5. Can input reach SQL?
6. Can input reach the shell?
7. Can input control a URL?
8. Can input control a filesystem path?
9. Can input control uploaded content?
10. Is rate limiting required?
11. Could errors expose secrets?
12. Are logs safe?
13. What happens if a dependency fails?
14. What privileges does the service have?
```

______________________________________________________________________

# 72. Threat Modeling — Practical Overview

For important features, identify:

```text
Assets
Threats
Entry points
Trust boundaries
Potential attackers
Security controls
Impact
```

You do not need a complex framework for every endpoint.

The goal is to proactively identify realistic attack paths.

______________________________________________________________________

# 73. Trust Boundaries

A trust boundary exists where data crosses between components with different trust levels.

Examples:

```text
Browser → API
API → Database
API → External API
User upload → File storage
Internet → Internal network
```

Treat data crossing these boundaries carefully.

______________________________________________________________________

# 74. Security and Background Jobs

Background workers need security controls too.

For example:

```text
Kafka message
 ↓
Worker
 ↓
Database
```

Do not assume messages are trustworthy simply because they come from an internal broker.

Validate message structure and enforce authorization/business invariants.

______________________________________________________________________

# 75. Security and External APIs

When calling external services:

- Validate responses.
- Set timeouts.
- Use TLS.
- Protect API credentials.
- Avoid blindly following redirects.
- Avoid sending unnecessary sensitive data.
- Validate external URLs when user-controlled.

______________________________________________________________________

# 76. Security and Containers

Even though container fundamentals were covered earlier, remember:

- Do not run applications as root unnecessarily.
- Minimize image contents.
- Scan dependencies/images.
- Do not bake secrets into images.
- Restrict filesystem access.
- Use resource limits.
- Keep base images maintained.

______________________________________________________________________

# 77. Authentication Incident

Suppose attackers are making thousands of login attempts.

Possible controls:

```text
Rate limiting
 ↓
Account protection
 ↓
Monitoring
 ↓
Alerting
```

Avoid designing controls that allow attackers to trivially cause denial of service by locking every account permanently.

Security controls must consider abuse scenarios.

______________________________________________________________________

# 78. Authorization Incident

Suppose:

```text
User A
```

can access:

```text
User B's order
```

by changing an ID.

The issue is not authentication.

The user is authenticated.

The problem is:

```text
Object-level authorization
```

Fix the server-side access-control check.

______________________________________________________________________

# 79. SQL Injection Incident

Suppose an endpoint accepts:

```text
search
```

and constructs raw SQL through string interpolation.

### Fix

Replace dynamic string construction with:

```text
Parameterized queries
```

and review all similar query paths.

Do not assume fixing one endpoint eliminates the class of vulnerability.

______________________________________________________________________

# 80. SSRF Incident

Suppose:

```text
POST /fetch
{
    "url": "..."
}
```

allows arbitrary URLs.

An attacker attempts to reach internal services.

### Fix

Implement:

```text
Destination allowlist
+
Network egress restrictions
+
Safe resolution/redirect handling
+
Timeouts
```

______________________________________________________________________

# 81. File Upload Incident

Suppose users can upload files that are later served publicly.

Questions:

```text
Can executable files be uploaded?
Can filenames escape the upload directory?
Can huge files exhaust disk?
Are files scanned?
Are uploaded files served with safe content types?
```

Security should cover the entire upload and download lifecycle.

______________________________________________________________________

# 82. Secrets Incident

Suppose a production API key is committed to Git.

Deleting the line in a later commit is not sufficient.

The key may remain in:

```text
Git history
```

The correct response includes:

```text
Revoke/rotate key
 ↓
Remove exposure
 ↓
Investigate usage
 ↓
Update secret management
 ↓
Prevent recurrence
```

______________________________________________________________________

# 83. Security Interview Questions & Answers

## Q1. What is OWASP?

**Answer:**

OWASP is a widely used community organization/project ecosystem focused on application security guidance, standards and
resources.

______________________________________________________________________

## Q2. What is SQL injection?

**Answer:**

SQL injection occurs when attacker-controlled input changes the intended SQL query structure. The primary defense is
parameterized/bound queries rather than string interpolation.

______________________________________________________________________

## Q3. Does using SQLAlchemy completely prevent SQL injection?

**Answer:**

No. Normal ORM/query APIs provide safer parameter handling, but manually constructed raw SQL can still be vulnerable if
untrusted input is interpolated.

______________________________________________________________________

## Q4. What is XSS?

**Answer:**

Cross-Site Scripting occurs when attacker-controlled content is interpreted as executable code in a user's browser.

______________________________________________________________________

## Q5. How do you prevent XSS?

**Answer:**

Use context-aware output encoding, safe templating, appropriate validation and, where useful, Content Security Policy.
Avoid unsafe HTML rendering.

______________________________________________________________________

## Q6. What is CSRF?

**Answer:**

CSRF tricks a victim's browser into making an unwanted authenticated request to another application, especially when
credentials such as cookies are automatically attached.

______________________________________________________________________

## Q7. How do you prevent CSRF?

**Answer:**

Use appropriate CSRF tokens, SameSite cookie protections and origin validation where appropriate. The exact strategy
depends on the authentication architecture.

______________________________________________________________________

## Q8. What is the difference between authentication and authorization?

**Answer:**

Authentication establishes who the caller is. Authorization determines what that caller is allowed to do.

______________________________________________________________________

## Q9. What is JWT?

**Answer:**

JWT is a token format commonly containing a header, payload and signature. A signed JWT provides integrity/authenticity
when correctly validated, but its payload is generally readable.

______________________________________________________________________

## Q10. Is a JWT encrypted?

**Answer:**

Not by default. A normal signed JWT is encoded and signed, not encrypted.

______________________________________________________________________

## Q11. What should you validate in a JWT?

**Answer:**

At minimum, verify the signature using the expected algorithm and validate relevant claims such as expiration, issuer
and audience where applicable.

______________________________________________________________________

## Q12. What is OAuth2?

**Answer:**

OAuth2 is an authorization framework that enables delegated access using access tokens.

______________________________________________________________________

## Q13. OAuth2 vs JWT?

**Answer:**

OAuth2 is an authorization framework/protocol, while JWT is a token format. OAuth2 can use JWTs but does not require
them.

______________________________________________________________________

## Q14. What is PKCE?

**Answer:**

PKCE adds a proof mechanism to the authorization-code flow that helps protect public clients from authorization-code
interception/substitution attacks.

______________________________________________________________________

## Q15. What is HTTPS?

**Answer:**

HTTPS is HTTP transported over TLS, providing encryption, integrity and server authentication through TLS certificates.

______________________________________________________________________

## Q16. What is CORS?

**Answer:**

CORS is a browser security mechanism that controls which origins are permitted to make certain cross-origin requests.

______________________________________________________________________

## Q17. Is CORS a security mechanism for server-to-server requests?

**Answer:**

No. CORS is enforced by browsers. Server-to-server clients are not constrained by browser CORS policy.

______________________________________________________________________

## Q18. What is SSRF?

**Answer:**

SSRF occurs when an attacker influences a server to make a request to an unintended destination, potentially including
internal services or metadata endpoints.

______________________________________________________________________

## Q19. How do you prevent SSRF?

**Answer:**

Use destination allowlists, restrict outbound network access, validate resolved destinations and redirects, and use
appropriate timeouts.

______________________________________________________________________

## Q20. What is command injection?

**Answer:**

Command injection occurs when untrusted input becomes executable operating-system command syntax.

______________________________________________________________________

## Q21. How do you prevent command injection in Python?

**Answer:**

Prefer subprocess calls using argument arrays, validate inputs and avoid shell execution with untrusted strings,
especially `shell=True`.

______________________________________________________________________

## Q22. What is path traversal?

**Answer:**

It occurs when an attacker manipulates a path to access files outside the intended directory, often using sequences such
as `../`.

______________________________________________________________________

## Q23. How do you secure file uploads?

**Answer:**

Authenticate/authorize uploads, limit size, validate content, generate server-side filenames, store files safely outside
executable locations where appropriate, scan when required and protect archive extraction.

______________________________________________________________________

## Q24. How should passwords be stored?

**Answer:**

Using a password hashing algorithm designed for password storage, such as Argon2, bcrypt or scrypt. Never store
plaintext passwords.

______________________________________________________________________

## Q25. Why shouldn't you use SHA-256 directly for passwords?

**Answer:**

SHA-256 is designed to be fast. Password hashing should deliberately be computationally expensive and use appropriate
password-hashing schemes.

______________________________________________________________________

## Q26. What is rate limiting?

**Answer:**

Rate limiting restricts how frequently a client or identity can perform operations, helping protect against abuse, brute
force and resource exhaustion.

______________________________________________________________________

## Q27. Why can per-process rate limiting fail in a distributed application?

**Answer:**

Each application instance maintains its own counter, so a client can distribute requests across instances and exceed the
intended global limit. A shared mechanism may be required.

______________________________________________________________________

## Q28. What is least privilege?

**Answer:**

Giving a user, service or application only the permissions necessary to perform its required tasks.

______________________________________________________________________

## Q29. Why is least privilege important?

**Answer:**

It reduces blast radius. If an application or credential is compromised, the attacker has fewer capabilities.

______________________________________________________________________

## Q30. What are security headers?

**Answer:**

HTTP response headers that instruct browsers to apply additional security controls, such as HSTS, CSP,
X-Content-Type-Options and Referrer-Policy.

______________________________________________________________________

## Q31. What is HSTS?

**Answer:**

HTTP Strict Transport Security instructs supporting browsers to use HTTPS for a domain for a configured period.

______________________________________________________________________

## Q32. What is CSP?

**Answer:**

Content Security Policy restricts which sources and behaviors a browser is allowed to execute/load, reducing the impact
of some XSS attacks.

______________________________________________________________________

## Q33. What does HttpOnly do?

**Answer:**

It prevents client-side JavaScript from directly reading a cookie.

______________________________________________________________________

## Q34. What does Secure do on a cookie?

**Answer:**

It tells the browser to send the cookie only over secure HTTPS connections.

______________________________________________________________________

## Q35. What does SameSite do?

**Answer:**

It controls whether a cookie is sent in cross-site contexts and can help reduce CSRF risk.

______________________________________________________________________

## Q36. How should production secrets be stored?

**Answer:**

Use a managed secret store or secure deployment configuration rather than source code. Protect access, rotate secrets
and avoid logging them.

______________________________________________________________________

## Q37. Is deleting a secret from the latest Git commit enough?

**Answer:**

No. The secret may remain in Git history or other systems. Revoke/rotate the credential and investigate the exposure.

______________________________________________________________________

## Q38. What is dependency confusion?

**Answer:**

It is a supply-chain attack where a package resolver retrieves a malicious package instead of the intended
internal/private package.

______________________________________________________________________

## Q39. How do you secure Python dependencies?

**Answer:**

Use trusted package sources, lock dependencies, scan for known vulnerabilities, review dependency changes and update
vulnerable packages in a controlled process.

______________________________________________________________________

## Q40. Why is frontend authorization insufficient?

**Answer:**

An attacker can bypass the frontend entirely and call the API directly. Authorization must be enforced server-side.

______________________________________________________________________

## Q41. What is IDOR?

**Answer:**

Insecure Direct Object Reference is an access-control problem where changing an object identifier allows a user to
access another user's resource without proper authorization.

______________________________________________________________________

## Q42. How would you secure a FastAPI endpoint?

**Answer:**

"I would authenticate the caller, enforce object/role-level authorization, validate input with appropriate schemas, use
parameterized database queries, protect sensitive operations with rate limits where needed, return safe errors, avoid
leaking secrets in logs and apply appropriate transport/browser protections."

______________________________________________________________________

## Q43. What is defense in depth?

**Answer:**

Using multiple independent security controls so that failure of one control does not immediately compromise the entire
system.

______________________________________________________________________

## Q44. What is the difference between validation and sanitization?

**Answer:**

Validation checks whether input conforms to expected rules. Sanitization transforms input. Prefer strict validation
where possible and use context-appropriate encoding/output handling rather than relying on generic sanitization.

______________________________________________________________________

## Q45. How would you perform a security review of a new endpoint?

**Answer:**

"I identify who can call it, how authentication works, what authorization is required, which inputs are
attacker-controlled and where those inputs flow. I check SQL, shell, URL, filesystem and file-upload risks, then review
rate limiting, secrets, error handling, logging, dependency behavior and service privileges."

______________________________________________________________________

## Q46. What should a backend do if an external URL is user-controlled?

**Answer:**

Treat it as a potential SSRF attack surface. Validate and allowlist destinations where possible, restrict outbound
network access, validate redirects/resolution and use timeouts.

______________________________________________________________________

## Q47. Why are file uploads dangerous?

**Answer:**

They can introduce executable content, path traversal, resource exhaustion, malicious archives, malware and unsafe
public content. Upload security must cover validation, storage and serving.

______________________________________________________________________

## Q48. What is a secure cookie strategy for session authentication?

**Answer:**

Use HTTPS and appropriate `Secure`, `HttpOnly` and `SameSite` attributes, along with appropriate CSRF protections for
state-changing requests.

______________________________________________________________________

## Q49. What is a security incident response for a leaked API key?

**Answer:**

Immediately revoke/rotate the key, determine where it was exposed, investigate possible use, replace it through secure
secret management and add controls to prevent similar leakage.

______________________________________________________________________

## Q50. Give a senior-level backend security answer.

**Answer:**

"I approach security as defense in depth. I start with strong authentication and server-side authorization, then treat
all external input as untrusted. I use parameterized SQL, safe subprocess execution, strict URL/path handling and secure
file-upload workflows. For browser-facing applications I consider CSRF, CORS, cookies and security headers. I protect
secrets through controlled storage and rotation, apply least privilege to applications and databases, manage dependency
risk and use rate limiting and observability for abuse detection. The goal is not just preventing individual
vulnerabilities but reducing blast radius when one control fails."

______________________________________________________________________

# 92. Security Scenario Practice

## Scenario 1 — SQL Injection

An endpoint accepts:

```text
GET /users?name=<input>
```

The developer builds SQL using an f-string.

### Your response

Identify:

```text
SQL injection
```

Fix using:

```text
Parameterized/bound queries
```

Then audit other raw SQL paths.

______________________________________________________________________

## Scenario 2 — IDOR

A logged-in user requests:

```text
/orders/501
```

and can change it to:

```text
/orders/502
```

to access another user's order.

### Your response

Authentication works.

Authorization does not.

Add an object-level ownership/permission check.

______________________________________________________________________

## Scenario 3 — SSRF

An endpoint accepts:

```json
{
  "url": "https://example.com"
}
```

and the backend fetches it.

### Your response

Treat the endpoint as SSRF-sensitive.

Use:

```text
Allowlist
+
Egress controls
+
Safe destination validation
+
Redirect handling
+
Timeouts
```

______________________________________________________________________

## Scenario 4 — File Upload

Users can upload:

```text
invoice.pdf
```

but the server stores the original filename directly.

### Risks

- Path traversal
- Filename collisions
- Malicious content
- Resource exhaustion

### Fix

Generate server-side filenames and validate content/size/storage behavior.

______________________________________________________________________

## Scenario 5 — JWT

A developer says:

> "We decode the JWT and then trust the user ID."

### Response

Decoding is not validation.

Verify:

```text
Signature
Algorithm
Expiration
Issuer/Audience where applicable
Required claims
```

before trusting claims.

______________________________________________________________________

## Scenario 6 — CORS

A developer proposes:

```text
allow_origins = ["*"]
allow_credentials = True
```

for a production API.

### Response

Review the browser credential model and use an explicit trusted-origin policy where credentials are required. CORS
should not be treated as authentication.

______________________________________________________________________

## Scenario 7 — Login Brute Force

An attacker sends thousands of login attempts.

### Response

Consider:

```text
Rate limiting
Monitoring
Alerting
Credential protection
Appropriate account-abuse controls
```

Avoid creating an account-lockout mechanism that attackers can trivially weaponize.

______________________________________________________________________

## Scenario 8 — Leaked Secret

A production database password is committed to Git.

### Response

Do not just delete the line.

```text
Revoke/rotate credential
 ↓
Investigate exposure
 ↓
Replace with secret management
 ↓
Audit access
 ↓
Prevent recurrence
```

______________________________________________________________________

# 93. Security Review Checklist

Before shipping an API:

### Authentication

- [ ] Authentication required where appropriate.
- [ ] Passwords are securely hashed.
- [ ] Tokens are properly validated.
- [ ] Token lifetimes are appropriate.
- [ ] Authentication abuse is controlled.

### Authorization

- [ ] Server-side authorization.
- [ ] Object-level access checks.
- [ ] Role/permission checks.
- [ ] No reliance on hidden frontend controls.

### Input

- [ ] Input validation.
- [ ] Parameterized SQL.
- [ ] No unsafe shell execution.
- [ ] Safe URL handling.
- [ ] Safe filesystem handling.

### Browser

- [ ] HTTPS.
- [ ] CORS reviewed.
- [ ] CSRF protections where applicable.
- [ ] Secure cookie attributes.
- [ ] Security headers where applicable.

### Files

- [ ] Upload size limits.
- [ ] Content validation.
- [ ] Safe generated filenames.
- [ ] Safe storage location.
- [ ] Archive extraction protected.
- [ ] Malware scanning where required.

### Secrets

- [ ] No secrets in source.
- [ ] No secrets in logs.
- [ ] Rotation mechanism.
- [ ] Restricted access.

### Dependencies

- [ ] Trusted package sources.
- [ ] Lock/controlled versions.
- [ ] Vulnerability scanning.
- [ ] Regular updates.

### Operations

- [ ] Rate limiting.
- [ ] Security logging.
- [ ] Alerting.
- [ ] Least privilege.
- [ ] Safe production errors.

______________________________________________________________________

# 94. Final Interview Readiness Checklist

Before moving to File 34, make sure you can explain:

- [ ] OWASP fundamentals
- [ ] Authentication vs authorization
- [ ] Broken authentication
- [ ] Password hashing
- [ ] SQL injection
- [ ] Parameterized queries
- [ ] ORM security
- [ ] XSS
- [ ] Stored XSS
- [ ] Reflected XSS
- [ ] XSS prevention
- [ ] CSRF
- [ ] CSRF prevention
- [ ] JWT
- [ ] JWT validation
- [ ] JWT expiration
- [ ] JWT revocation trade-offs
- [ ] OAuth2
- [ ] Authorization Code flow
- [ ] PKCE
- [ ] OAuth2 vs JWT
- [ ] HTTPS
- [ ] TLS
- [ ] CORS
- [ ] CORS vs authentication
- [ ] SSRF
- [ ] SSRF prevention
- [ ] DNS rebinding considerations
- [ ] Command injection
- [ ] Safe subprocess usage
- [ ] Path traversal
- [ ] File upload security
- [ ] Archive traversal
- [ ] Secrets management
- [ ] Secret rotation
- [ ] Rate limiting
- [ ] Distributed rate limiting
- [ ] Rate limiting algorithms
- [ ] Security headers
- [ ] CSP
- [ ] Secure cookies
- [ ] Dependency security
- [ ] Dependency pinning
- [ ] Dependency confusion
- [ ] Least privilege
- [ ] Database least privilege
- [ ] RBAC
- [ ] Object-level authorization
- [ ] Input validation
- [ ] Validation vs sanitization
- [ ] Secure error handling
- [ ] Security logging
- [ ] Defense in depth
- [ ] Threat modeling basics
- [ ] Trust boundaries
- [ ] Security incident response
- [ ] FastAPI security review
- [ ] Production security mindset

______________________________________________________________________

# 95. Final Takeaways

For a senior Python backend engineer, security is not just:

```text
JWT
+
HTTPS
```

A secure backend considers the complete request and data lifecycle:

```text
Input
 ↓
Authentication
 ↓
Authorization
 ↓
Validation
 ↓
Business logic
 ↓
Database
 ↓
External services
 ↓
Storage
 ↓
Response
 ↓
Logging/monitoring
```

The most important interview mindset is:

> **Never trust input, never assume authentication means authorization, and always minimize the privileges and blast radius of every component.**

When reviewing a backend system, continuously ask:

```text
What can the attacker control?
Where does that data go?
What can it influence?
What happens if a control fails?
How large is the blast radius?
```

That reasoning is more valuable than memorizing a list of vulnerabilities.

______________________________________________________________________

**Previous:** [32. Production Debugging & Incident Response](./32-production-debugging.md)

**Next:** [34. Git & Engineering Workflow](./34-git.md)

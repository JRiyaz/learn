# 12. HTTP, TCP/IP, TLS & Networking

**Previous:** [11. Typing & Testing](./11-python-exceptions-typing-testing.md)

**Next:** [13. Complete Backend Request Lifecycle](./13-request-lifecycle.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain what happens when a client accesses a backend service by domain name.
- Explain DNS at a practical backend-engineer level.
- Understand TCP and why reliable connections matter.
- Explain the TCP three-way handshake.
- Understand UDP and when it is useful.
- Explain TLS and how HTTPS protects communication.
- Understand HTTP methods and their semantics.
- Explain important HTTP status-code categories.
- Understand HTTP headers, cookies, sessions and keep-alive.
- Compare HTTP/1.1 with HTTP/2 at a high level.
- Explain REST principles and common API design choices.
- Understand idempotency and why it matters for backend APIs and retries.
- Debug common networking/API failures from symptoms.
- Answer senior-level HTTP/networking interview questions clearly.

______________________________________________________________________

# 1. What Happens When You Open a URL?

Suppose a client requests:

```text
https://api.example.com/users/42
```

At a high level:

```text
Client
  ↓
DNS
  ↓
IP address
  ↓
TCP connection
  ↓
TLS handshake
  ↓
HTTP request
  ↓
Server
  ↓
HTTP response
```

The actual path can contain additional infrastructure such as:

- DNS resolvers
- Load balancers
- Proxies
- Firewalls
- CDNs
- API gateways

For a backend interview, you should be able to explain the basic chain and then discuss where infrastructure can be
inserted.

______________________________________________________________________

# 2. DNS

DNS stands for **Domain Name System**.

Its primary purpose is to translate human-readable domain names into IP addresses.

Example:

```text
api.example.com
       ↓
   DNS lookup
       ↓
203.0.113.10
```

Applications generally connect to an IP address rather than directly to a human-readable hostname.

______________________________________________________________________

# 3. DNS Resolution

A simplified DNS lookup can involve:

```text
Application
    ↓
OS / local resolver
    ↓
Recursive DNS resolver
    ↓
Root DNS server
    ↓
TLD server
    ↓
Authoritative DNS server
```

The recursive resolver can cache results, so the complete hierarchy does not necessarily need to be contacted for every
request.

______________________________________________________________________

# 4. DNS Records

Common DNS record types include:

| Record | Purpose |
|---|---|
| A | Maps a hostname to an IPv4 address |
| AAAA | Maps a hostname to an IPv6 address |
| CNAME | Alias to another hostname |
| MX | Mail-server routing |
| TXT | Text/configuration information |
| NS | Name-server delegation |

For backend interviews, A, AAAA and CNAME are particularly useful to understand.

______________________________________________________________________

# 5. DNS Caching and TTL

DNS responses can be cached.

A DNS record can have a **TTL (Time To Live)** indicating how long the result may be cached.

Caching reduces:

- DNS latency
- Resolver load
- Authoritative DNS traffic

But it also means DNS changes may not become visible everywhere immediately.

______________________________________________________________________

# 6. TCP

TCP stands for **Transmission Control Protocol**.

It provides a connection-oriented transport mechanism with features such as:

- Reliable delivery
- Ordered byte-stream delivery
- Retransmission
- Flow control
- Congestion control

HTTP/1.1 and HTTP/2 commonly run over TCP.

______________________________________________________________________

# 7. TCP Is a Byte Stream

TCP does not preserve application-level message boundaries.

If an application sends:

```text
message A
message B
```

the receiving application sees a byte stream.

The application protocol determines how those bytes are interpreted.

This is important when implementing low-level network protocols.

______________________________________________________________________

# 8. TCP Three-Way Handshake

A TCP connection is established using a three-way handshake.

Conceptually:

```text
Client                    Server

  SYN  -------------------->
       <---------------- SYN + ACK
  ACK  -------------------->
```

After this exchange, both sides have established the TCP connection state needed for communication.

______________________________________________________________________

# 9. Why Three Steps?

The handshake allows both sides to establish and acknowledge initial sequence information and confirm that communication
is possible in both directions.

For an interview, know:

```text
SYN
SYN-ACK
ACK
```

and be able to explain that this establishes the TCP connection.

______________________________________________________________________

# 10. TCP Reliability

TCP can detect missing data and retransmit it.

It also maintains ordering.

For example, if packets arrive:

```text
3
1
2
```

TCP presents the byte stream to the application in the correct order.

This reliability comes with overhead compared with simpler transport protocols.

______________________________________________________________________

# 11. TCP Flow Control

Flow control prevents a sender from overwhelming a receiver that cannot process data quickly enough.

The receiver advertises how much data it can currently accept.

This is separate from congestion control.

______________________________________________________________________

# 12. TCP Congestion Control

Congestion control deals with the network path.

The sender adjusts its behavior based on signs of network congestion.

The important distinction:

```text
Flow control
→ protects the receiver

Congestion control
→ responds to network capacity/congestion
```

______________________________________________________________________

# 13. UDP

UDP stands for **User Datagram Protocol**.

UDP is connectionless and provides datagrams without TCP's built-in reliability and ordering guarantees.

UDP generally has lower protocol overhead.

It can be useful where:

- Low latency matters
- The application can tolerate loss
- The application implements its own reliability
- Broadcast/multicast-style communication is relevant

Examples include some real-time media and networking protocols.

______________________________________________________________________

# 14. TCP vs UDP

| Feature | TCP | UDP |
|---|---|---|
| Connection-oriented | Yes | No |
| Reliable delivery | Yes | No built-in guarantee |
| Ordered delivery | Yes | No built-in guarantee |
| Retransmission | Yes | No built-in |
| Overhead | Higher | Lower |
| Typical use | HTTP, databases, reliable streams | Real-time/latency-sensitive protocols |

Do not say UDP is simply "faster" in every situation. Its lower overhead and different semantics make it suitable for
particular workloads.

______________________________________________________________________

# 15. Ports

An IP address identifies a host/interface at the network layer.

A port identifies a service endpoint at the transport layer.

Conceptually:

```text
IP address + port
        ↓
network service endpoint
```

Examples:

```text
HTTPS → 443
HTTP  → 80
```

A backend server commonly listens on a TCP port.

______________________________________________________________________

# 16. Sockets

A socket provides an interface for network communication.

A TCP connection can be identified by a combination involving:

```text
source IP
source port
destination IP
destination port
protocol
```

Backend applications normally interact with sockets indirectly through web servers, frameworks and networking libraries.

______________________________________________________________________

# 17. TLS

TLS stands for **Transport Layer Security**.

TLS provides security properties including:

- Encryption
- Integrity
- Server authentication through certificates
- Protection against many forms of network interception

HTTPS is HTTP carried over TLS.

______________________________________________________________________

# 18. TLS and HTTPS

Conceptually:

```text
HTTP
  ↓
TLS
  ↓
TCP
  ↓
IP
```

So HTTPS is not a completely different application protocol from HTTP.

It is HTTP protected by TLS.

______________________________________________________________________

# 19. TLS Handshake — High Level

A simplified modern TLS connection involves:

```text
Client
  ↓
ClientHello
  ↓
ServerHello + certificate
  ↓
Key agreement
  ↓
Encrypted application traffic
```

The exact handshake depends on the TLS version and configuration.

For interviews, focus on the purpose:

- Agree on cryptographic parameters.
- Authenticate the server.
- Establish shared key material.
- Protect subsequent application data.

______________________________________________________________________

# 20. Certificates

A TLS certificate binds an identity, such as a hostname, to a public key and is signed by a trusted certificate
authority or a configured trust chain.

A client can validate things such as:

- Certificate chain
- Hostname
- Validity period
- Trust relationship

Certificate validation helps prevent an attacker from simply pretending to be the legitimate server.

______________________________________________________________________

# 21. Encryption vs Authentication

TLS provides more than encryption.

### Encryption

Prevents unauthorized parties from reading protected traffic.

### Integrity

Helps detect tampering with protected traffic.

### Authentication

Certificates help the client verify the server's identity.

This distinction is important in interviews.

______________________________________________________________________

# 22. HTTP

HTTP stands for **Hypertext Transfer Protocol**.

It is an application-layer protocol used for communication between clients and servers.

A request generally contains:

```text
Method
URL/path
Headers
Optional body
```

A response generally contains:

```text
Status code
Headers
Optional body
```

______________________________________________________________________

# 23. HTTP Request Example

Conceptually:

```http
GET /users/42 HTTP/1.1
Host: api.example.com
Accept: application/json
Authorization: Bearer <token>
```

The exact wire representation depends on the HTTP version and transport details.

______________________________________________________________________

# 24. HTTP Response Example

Conceptually:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 42,
    "name": "Riyaz"
}
```

The status code communicates the broad result of the request.

______________________________________________________________________

# 25. HTTP Methods

Important HTTP methods include:

- `GET`
- `POST`
- `PUT`
- `PATCH`
- `DELETE`
- `HEAD`
- `OPTIONS`

Understanding their semantics is more important than memorizing names.

______________________________________________________________________

# 26. GET

`GET` requests a representation of a resource.

Example:

```http
GET /users/42
```

GET is generally expected to be:

- Safe
- Idempotent
- Cacheable under appropriate conditions

Safe means it is not intended to modify server state as part of the requested operation.

______________________________________________________________________

# 27. POST

`POST` is commonly used to submit data for processing or create a subordinate resource.

Example:

```http
POST /users
```

POST is generally **not idempotent** by default.

Sending the same POST request multiple times can create multiple effects.

______________________________________________________________________

# 28. PUT

`PUT` commonly represents replacing or creating the resource at a known URI.

Example:

```http
PUT /users/42
```

PUT is defined as idempotent.

Repeated identical requests should have the same intended effect as making the request once.

______________________________________________________________________

# 29. PATCH

`PATCH` is commonly used for partial modifications.

Example:

```http
PATCH /users/42
```

PATCH's idempotency depends on the semantics of the specific operation.

Do not automatically claim that every PATCH request is idempotent.

______________________________________________________________________

# 30. DELETE

`DELETE` requests deletion of a resource.

Example:

```http
DELETE /users/42
```

DELETE is defined as idempotent in HTTP semantics, although repeated requests may produce different response status
codes.

The important distinction is:

> Idempotency refers to the intended effect, not necessarily identical response bodies/status codes.

______________________________________________________________________

# 31. HEAD and OPTIONS

### HEAD

Similar to GET but requests response headers without the response body.

Useful for checking metadata without transferring the full representation.

### OPTIONS

Describes communication options supported by a resource/server.

It is also important in browser CORS workflows.

______________________________________________________________________

# 32. HTTP Status Codes

Status codes are grouped into categories.

| Range | Meaning |
|---|---|
| 1xx | Informational |
| 2xx | Success |
| 3xx | Redirection |
| 4xx | Client-side/request issue |
| 5xx | Server-side failure |

______________________________________________________________________

# 33. Important 2xx Codes

### 200 OK

Request succeeded.

### 201 Created

A resource was successfully created.

### 202 Accepted

Request accepted for processing but not necessarily completed.

Useful for asynchronous/background operations.

### 204 No Content

Request succeeded without a response body.

______________________________________________________________________

# 34. Important 3xx Codes

### 301 / 308

Permanent redirection.

### 302 / 307

Temporary redirection.

There are important differences in how clients handle methods across redirect types.

For API development, choose redirects deliberately.

______________________________________________________________________

# 35. Important 4xx Codes

### 400 Bad Request

The request is malformed or invalid.

### 401 Unauthorized

Authentication is required or failed.

Despite the name, this is about authentication.

### 403 Forbidden

The server understood the request but refuses to authorize it.

### 404 Not Found

Requested resource was not found.

### 409 Conflict

Request conflicts with the current state of the resource.

### 422 Unprocessable Content

The request syntax is valid but the content fails semantic validation.

______________________________________________________________________

# 36. Important 5xx Codes

### 500 Internal Server Error

Unexpected server-side failure.

### 502 Bad Gateway

A gateway/proxy received an invalid response from an upstream service.

### 503 Service Unavailable

The service is currently unable to handle the request, often temporarily.

### 504 Gateway Timeout

A gateway/proxy did not receive a timely response from an upstream service.

______________________________________________________________________

# 37. HTTP Headers

Headers carry metadata.

Examples:

```text
Content-Type
Accept
Authorization
Cache-Control
Cookie
Set-Cookie
Host
User-Agent
```

Headers can describe:

- Content format
- Authentication
- Caching
- Cookies
- Client capabilities
- Request metadata

______________________________________________________________________

# 38. Content-Type vs Accept

This is a common interview question.

### Content-Type

Describes the format of the message body.

Example:

```http
Content-Type: application/json
```

### Accept

Describes response formats the client is willing to receive.

Example:

```http
Accept: application/json
```

Remember:

```text
Content-Type → what this body is
Accept       → what response I want
```

______________________________________________________________________

# 39. Cookies

A cookie is data associated with a domain that a browser can send with subsequent requests.

A server can issue a cookie using:

```http
Set-Cookie
```

The browser may later send:

```http
Cookie
```

Cookies are commonly used for:

- Session identifiers
- Preferences
- Tracking
- Authentication state

______________________________________________________________________

# 40. Important Cookie Attributes

Important attributes include:

### Secure

Send the cookie over HTTPS.

### HttpOnly

Prevents JavaScript from directly reading the cookie through browser APIs such as `document.cookie`.

### SameSite

Controls when cookies are sent in cross-site contexts and helps mitigate certain CSRF scenarios.

Common values:

```text
Strict
Lax
None
```

`SameSite=None` generally requires `Secure`.

______________________________________________________________________

# 41. Sessions

HTTP itself is stateless.

A session mechanism allows an application to associate multiple requests with the same logical client/session.

A common model is:

```text
Browser
   ↓
session cookie
   ↓
server-side session store
```

The cookie may contain only a session identifier while the actual session state is stored server-side.

______________________________________________________________________

# 42. Session Storage

Session data can be stored in:

- Application memory
- Redis
- Database
- Other shared stores

For horizontally scaled applications, shared session storage or another distributed session strategy may be required.

______________________________________________________________________

# 43. Cookie-Based vs Token-Based Authentication

A simplified comparison:

### Session-based

```text
Cookie
  ↓
Session ID
  ↓
Server-side state
```

### Token-based

```text
Client
  ↓
Token
  ↓
Server validates token
```

Neither approach is automatically superior.

The correct choice depends on:

- Client type
- Security requirements
- Revocation needs
- Infrastructure
- Token/session lifecycle
- Browser behavior

______________________________________________________________________

# 44. Keep-Alive

Creating a new TCP connection has overhead.

HTTP keep-alive allows multiple HTTP requests/responses to reuse a connection when supported by the
protocol/client/server configuration.

Conceptually:

```text
TCP connection
   ↓
HTTP request 1
HTTP response 1
   ↓
HTTP request 2
HTTP response 2
   ↓
...
```

This reduces repeated connection setup overhead.

______________________________________________________________________

# 45. HTTP/1.1

HTTP/1.1 commonly uses persistent TCP connections.

Requests and responses are represented in a textual message format.

A key limitation is that request processing can suffer from **head-of-line blocking** at the HTTP/1.1 connection level
when pipelining/connection reuse patterns cause an earlier response to delay later work.

Clients commonly use multiple connections to improve concurrency.

______________________________________________________________________

# 46. HTTP/2 Overview

HTTP/2 introduces binary framing and multiplexing.

Multiple streams can share a single TCP connection.

Conceptually:

```text
One TCP connection
   ├── Stream A
   ├── Stream B
   ├── Stream C
   └── Stream D
```

Other features include:

- Header compression
- Stream multiplexing
- Binary framing

HTTP/2 reduces many HTTP-level inefficiencies compared with HTTP/1.1.

______________________________________________________________________

# 47. HTTP/1.1 vs HTTP/2

| Feature | HTTP/1.1 | HTTP/2 |
|---|---|---|
| Message framing | Text-oriented | Binary framing |
| Multiplexing | No general stream multiplexing | Yes |
| Header compression | No HPACK | Yes |
| Connection usage | Often multiple connections | Multiple streams over connection |
| Request concurrency | Limited by connection behavior | Stream multiplexing |

HTTP/2 still commonly runs over TCP, so TCP-level issues such as packet loss can affect the shared connection.

______________________________________________________________________

# 48. REST

REST stands for **Representational State Transfer**.

REST is an architectural style rather than a protocol.

Common REST-oriented principles include:

- Resource-oriented APIs
- Stateless requests
- Uniform interface
- Standard HTTP methods
- Representations of resources

Example:

```text
GET    /users/42
POST   /users
PUT    /users/42
PATCH  /users/42
DELETE /users/42
```

______________________________________________________________________

# 49. REST Resource Design

Prefer resource-oriented paths.

Less REST-oriented:

```text
POST /getUser
POST /deleteUser
```

More resource-oriented:

```text
GET    /users/42
DELETE /users/42
```

The HTTP method communicates the intended operation.

______________________________________________________________________

# 50. Statelessness

In a REST-style API, each request should contain the information needed to process it.

This does not mean the backend cannot store data.

It means the server should not depend on hidden per-client conversational state in order to interpret the request.

Sessions can still exist in an application; the term "stateless" needs to be interpreted carefully in API design
discussions.

______________________________________________________________________

# 51. Idempotency

An operation is idempotent when making the same request multiple times has the same intended effect as making it once.

Examples from HTTP semantics:

```text
GET    → idempotent
PUT    → idempotent
DELETE → idempotent
```

POST is not idempotent by default.

______________________________________________________________________

# 52. Why Idempotency Matters

Consider:

```text
Client
  ↓
POST /payments
  ↓
Server processes payment
  ↓
Network timeout
```

The client does not know whether the payment succeeded.

If it retries:

```text
POST /payments
```

the payment could potentially happen twice.

An **idempotency key** can allow the server to recognize retries of the same logical operation.

______________________________________________________________________

# 53. Idempotency Keys

A client can send:

```http
Idempotency-Key: abc123
```

The server can associate the key with the result of the operation.

A retry using the same key can return the previous result rather than creating another side effect.

This pattern is especially useful for:

- Payments
- Orders
- Resource creation
- External API calls
- Message-triggered operations

The exact storage and expiry strategy depends on the application.

______________________________________________________________________

# 54. Safe vs Idempotent

These concepts are different.

### Safe

The method is intended not to modify server state.

Examples:

```text
GET
HEAD
OPTIONS
```

### Idempotent

Repeating the same request has the same intended effect.

Examples:

```text
GET
PUT
DELETE
```

A method can be idempotent without being safe.

For example:

```text
DELETE
```

is idempotent but modifies server state.

______________________________________________________________________

# 55. Networking Debugging Mindset

When an API fails, avoid immediately assuming the application code is broken.

Break the path into layers:

```text
DNS
 ↓
Network
 ↓
TCP
 ↓
TLS
 ↓
HTTP
 ↓
Proxy / Load Balancer
 ↓
Application
 ↓
Database / Dependency
```

Then identify the first layer that fails.

______________________________________________________________________

# 56. Common Failure Symptoms

| Symptom | Possible area |
|---|---|
| DNS resolution failure | DNS/configuration |
| Connection refused | Service/port/firewall/listener |
| Connection timeout | Network/firewall/routing/service overload |
| TLS certificate error | Certificate/trust/hostname/config |
| 400 | Request/validation |
| 401 | Authentication |
| 403 | Authorization |
| 404 | Resource/routing |
| 502 | Upstream/proxy |
| 503 | Service unavailable |
| 504 | Upstream timeout |

These are starting points, not definitive diagnoses.

______________________________________________________________________

# 57. Latency Breakdown

For a request:

```text
Total latency
=
DNS
+
connection setup
+
TLS
+
request transmission
+
server processing
+
upstream calls
+
response transmission
```

In practice, connection reuse can eliminate repeated DNS/TCP/TLS costs.

This is useful when diagnosing unexpectedly high API latency.

______________________________________________________________________

# 58. Backend Interview Mental Model

For almost any HTTP/networking question, reason from:

```text
Name
 ↓
Address
 ↓
Connection
 ↓
Security
 ↓
Request
 ↓
Routing
 ↓
Processing
 ↓
Response
```

Map that to:

```text
DNS
 ↓
IP
 ↓
TCP
 ↓
TLS
 ↓
HTTP
 ↓
Load balancer / server
 ↓
Application
 ↓
HTTP response
```

This mental model makes many networking questions easier.

______________________________________________________________________

# 59. Common Interview Traps

## Trap 1 — "HTTPS is a separate protocol from HTTP"

HTTPS is HTTP over TLS.

______________________________________________________________________

## Trap 2 — "TCP is just slower UDP"

They provide different semantics.

TCP provides reliability, ordering, flow control and congestion control.

______________________________________________________________________

## Trap 3 — "401 means not authorized"

401 is primarily about authentication.

403 is the usual status for a request that is understood but not permitted.

______________________________________________________________________

## Trap 4 — "PATCH is always idempotent"

Not necessarily.

Its idempotency depends on the operation semantics.

______________________________________________________________________

## Trap 5 — "POST cannot be made idempotent"

POST is not idempotent by default, but applications can implement idempotency using mechanisms such as idempotency keys.

______________________________________________________________________

## Trap 6 — "REST means JSON over HTTP"

REST is an architectural style.

JSON over HTTP is a common implementation choice, not the definition of REST.

______________________________________________________________________

# 60. Interview Questions & Answers

## Q1. What happens when you call an HTTPS API by hostname?

**Answer:**

At a high level:

1. DNS resolves the hostname to an IP.
1. The client establishes a TCP connection.
1. TLS negotiates a secure connection and authenticates the server.
1. The client sends the HTTP request.
1. Infrastructure and the application process it.
1. The HTTP response is returned.

______________________________________________________________________

## Q2. What is DNS?

**Answer:**

DNS maps domain names to network addresses and provides a distributed naming system.

Resolvers cache results according to TTLs.

______________________________________________________________________

## Q3. What is TCP?

**Answer:**

TCP is a connection-oriented transport protocol that provides reliable, ordered byte-stream delivery along with flow and
congestion control.

______________________________________________________________________

## Q4. Explain the TCP three-way handshake.

**Answer:**

The simplified handshake is:

```text
SYN
SYN-ACK
ACK
```

It establishes the connection state and confirms communication between both endpoints.

______________________________________________________________________

## Q5. TCP vs UDP?

**Answer:**

TCP provides reliable, ordered delivery with connection management and congestion/flow control.

UDP provides connectionless datagrams without built-in reliability or ordering.

______________________________________________________________________

## Q6. What is TLS?

**Answer:**

TLS provides secure communication through encryption, integrity protection and server authentication.

HTTPS is HTTP carried over TLS.

______________________________________________________________________

## Q7. What does a TLS certificate do?

**Answer:**

It binds an identity such as a hostname to a public key and is validated through a trust chain.

______________________________________________________________________

## Q8. What is the difference between encryption and authentication?

**Answer:**

Encryption protects confidentiality.

Authentication verifies identity.

TLS provides both confidentiality/integrity protections and server authentication through certificates.

______________________________________________________________________

## Q9. What are HTTP methods?

**Answer:**

Common methods include:

```text
GET
POST
PUT
PATCH
DELETE
HEAD
OPTIONS
```

Each has defined semantics.

______________________________________________________________________

## Q10. GET vs POST?

**Answer:**

GET retrieves a representation and is safe/idempotent.

POST submits data for processing and is not idempotent by default.

______________________________________________________________________

## Q11. PUT vs PATCH?

**Answer:**

PUT commonly represents replacing or creating a resource at a known URI and is idempotent.

PATCH is used for partial modifications, and its idempotency depends on the operation.

______________________________________________________________________

## Q12. Is DELETE idempotent?

**Answer:**

Yes, in HTTP semantics.

Repeating the operation has the same intended effect, although the responses can differ—for example, the first request
might return 204 and a later one might return 404.

______________________________________________________________________

## Q13. What is the difference between 401 and 403?

**Answer:**

401 indicates an authentication problem or that authentication is required.

403 means the server understood the request but refuses to authorize it.

______________________________________________________________________

## Q14. 400 vs 422?

**Answer:**

400 generally indicates a malformed or invalid request.

422 commonly indicates syntactically valid content that fails semantic validation.

Exact API conventions can vary.

______________________________________________________________________

## Q15. 502 vs 503 vs 504?

**Answer:**

- 502: gateway/proxy received an invalid upstream response.
- 503: service is unavailable.
- 504: gateway/proxy timed out waiting for an upstream response.

______________________________________________________________________

## Q16. What are HTTP headers?

**Answer:**

Headers carry metadata about requests and responses, including content type, authentication, caching and cookies.

______________________________________________________________________

## Q17. Content-Type vs Accept?

**Answer:**

`Content-Type` describes the body being sent.

`Accept` describes response formats the client is willing to receive.

______________________________________________________________________

## Q18. What are cookies?

**Answer:**

Cookies are browser-associated data that can be sent with subsequent requests to applicable domains.

They are commonly used for sessions, preferences and authentication-related state.

______________________________________________________________________

## Q19. What is a session?

**Answer:**

A session lets an application associate multiple requests with a logical client/session.

A common implementation stores a session identifier in a cookie and session data server-side.

______________________________________________________________________

## Q20. What is keep-alive?

**Answer:**

Keep-alive allows multiple HTTP requests to reuse an established connection instead of creating a new TCP connection for
every request.

This reduces connection setup overhead.

______________________________________________________________________

## Q21. What is HTTP/2?

**Answer:**

HTTP/2 is an HTTP version using binary framing and stream multiplexing, allowing multiple logical streams to share a
connection.

It also supports header compression.

______________________________________________________________________

## Q22. HTTP/1.1 vs HTTP/2?

**Answer:**

HTTP/1.1 is text-oriented and commonly uses multiple persistent connections for concurrency.

HTTP/2 uses binary frames and multiplexes multiple streams over a connection.

______________________________________________________________________

## Q23. What is REST?

**Answer:**

REST is an architectural style based around concepts such as resources, stateless requests and a uniform interface.

HTTP is commonly used to implement RESTful APIs.

______________________________________________________________________

## Q24. What does stateless mean in REST?

**Answer:**

Each request should contain the information required to process it without depending on hidden conversational state from
previous requests.

The server can still persist business data or use sessions; statelessness refers to how requests are interpreted.

______________________________________________________________________

## Q25. What is idempotency?

**Answer:**

An operation is idempotent when repeating the same request has the same intended effect as making it once.

GET, PUT and DELETE are defined as idempotent HTTP methods.

______________________________________________________________________

## Q26. Why is idempotency important in distributed systems?

**Answer:**

Networks fail and clients may retry requests after timeouts.

For operations with side effects, idempotency prevents retries from accidentally creating duplicate effects.

______________________________________________________________________

## Q27. How would you make a payment API idempotent?

**Answer:**

Accept an idempotency key from the client.

Store the key and the resulting operation outcome for an appropriate period.

If the same logical request is retried with the same key, return the previous result instead of performing the side
effect again.

______________________________________________________________________

## Q28. What is DNS TTL?

**Answer:**

TTL specifies how long DNS results can be cached before they should be refreshed.

______________________________________________________________________

## Q29. Why can DNS changes take time to propagate?

**Answer:**

Resolvers and other caching layers may continue using previously cached records until their TTL expires.

______________________________________________________________________

## Q30. What is a port?

**Answer:**

A port identifies a service endpoint associated with a host at the transport layer.

For example, HTTPS commonly uses TCP port 443.

______________________________________________________________________

## Q31. What is a socket?

**Answer:**

A socket is an interface used by software to communicate over a network.

TCP connections can be identified using endpoint addresses and ports along with the transport protocol.

______________________________________________________________________

## Q32. What is the difference between flow control and congestion control?

**Answer:**

Flow control protects the receiver from being overwhelmed.

Congestion control responds to congestion in the network path.

______________________________________________________________________

## Q33. Why is TCP called a byte stream?

**Answer:**

TCP provides an ordered stream of bytes rather than preserving the boundaries of application-level messages.

The application protocol determines message framing.

______________________________________________________________________

## Q34. Why is blocking network code important to backend engineers?

**Answer:**

Blocking operations can consume threads or block an async event loop, reducing concurrency.

Choosing appropriate synchronous/asynchronous clients and execution models is therefore important.

______________________________________________________________________

# 61. Scenario-Based Questions

## Scenario 1 — API Works by IP but Not Domain

You can call:

```text
https://203.0.113.10
```

but:

```text
https://api.example.com
```

fails to resolve.

**Question:** Where would you investigate first?

**Answer:**

DNS.

Check:

- DNS records
- Resolver behavior
- TTL/caching
- Authoritative DNS
- Local DNS configuration

If the IP works, the problem is likely before the TCP connection stage.

______________________________________________________________________

## Scenario 2 — Connection Refused

The API returns:

```text
Connection refused
```

**Question:** What would you investigate?

**Answer:**

Check whether:

- The service is running.
- The expected port is listening.
- The client is connecting to the correct IP/port.
- A firewall or security policy is interfering.
- A proxy/load balancer is routing incorrectly.

Connection refused usually indicates that the connection reached a host but no service accepted the connection on that
endpoint.

______________________________________________________________________

## Scenario 3 — Connection Timeout

The client waits for a long time and eventually times out while establishing a connection.

**Question:** What layers could be involved?

**Answer:**

Investigate:

- Routing
- Firewall/security groups
- Network reachability
- Load balancer
- Service availability
- Port configuration

Do not immediately assume application-level code is responsible.

______________________________________________________________________

## Scenario 4 — TLS Certificate Failure

The TCP connection succeeds, but the client reports a certificate/hostname validation error.

**Question:** What layer failed?

**Answer:**

TLS.

Investigate:

- Certificate validity
- Hostname/SAN
- Certificate chain
- Trust store
- Expiration
- TLS configuration

______________________________________________________________________

## Scenario 5 — 502 Bad Gateway

A client receives:

```text
502 Bad Gateway
```

from a reverse proxy.

**Question:** What does that suggest?

**Answer:**

The proxy/gateway received an invalid or unusable response from the upstream service.

Investigate:

```text
Client
 ↓
Proxy
 ↓
Upstream service
```

Focus on the proxy-to-upstream connection and upstream behavior.

______________________________________________________________________

## Scenario 6 — 504 Gateway Timeout

A load balancer returns:

```text
504 Gateway Timeout
```

**Question:** What would you check?

**Answer:**

The gateway likely waited too long for the upstream response.

Investigate:

- Upstream latency
- Database queries
- External API calls
- Connection pools
- Gateway timeout
- Application timeout
- Network problems

______________________________________________________________________

## Scenario 7 — Duplicate Payment

The client times out after submitting a payment and retries the request.

The payment is charged twice.

**Question:** How would you redesign the API?

**Answer:**

Introduce an idempotency key.

The server should persist the key and operation result so retries of the same logical operation do not execute the
payment twice.

______________________________________________________________________

## Scenario 8 — Slow API After Every Deployment

An API becomes significantly slower after deployment.

Profiling shows the application itself is fast, but every request has noticeable connection setup time.

**Question:** What networking feature would you investigate?

**Answer:**

Connection reuse/keep-alive.

Repeated TCP and TLS setup can add latency.

Investigate client connection pooling, server keep-alive settings and intermediary behavior.

______________________________________________________________________

## Scenario 9 — Async API Under Load

An asynchronous Python service handles a few requests well but becomes extremely slow under load.

Investigation finds a synchronous blocking HTTP client being called from async endpoints.

**Question:** Why is this a problem?

**Answer:**

The blocking client can block the event loop, preventing other async tasks from progressing.

Use an async client or move blocking work to an appropriate executor/thread.

______________________________________________________________________

## Scenario 10 — 401 vs 403

A user has valid credentials but is not allowed to access an admin endpoint.

**Question:** Which status is more appropriate?

**Answer:**

403 Forbidden, assuming authentication succeeded but authorization failed.

______________________________________________________________________

## Scenario 11 — HTTP Method Choice

You need an endpoint that changes only a user's email address.

**Question:** Would PUT or PATCH be more natural?

**Answer:**

PATCH is often more natural for a partial modification.

Whether the operation is idempotent depends on the exact semantics.

______________________________________________________________________

## Scenario 12 — HTTP/1.1 to HTTP/2

A team wants better request concurrency and fewer connection-level inefficiencies.

**Question:** What HTTP/2 features are relevant?

**Answer:**

HTTP/2 provides:

- Binary framing
- Stream multiplexing
- Header compression

Multiple logical streams can share a TCP connection.

______________________________________________________________________

# 62. Practice Exercises

## Exercise 1 — DNS Investigation

Pick a public domain and investigate:

- A record
- AAAA record
- CNAME if present
- TTL
- Authoritative nameservers

Explain the resolution path.

______________________________________________________________________

## Exercise 2 — TCP Handshake

Draw the TCP handshake from memory:

```text
SYN
SYN-ACK
ACK
```

Explain what each step accomplishes.

______________________________________________________________________

## Exercise 3 — HTTP Request

Construct a request containing:

- Method
- Path
- Host
- Content-Type
- Accept
- Authorization
- JSON body

Explain each component.

______________________________________________________________________

## Exercise 4 — Status Codes

For each scenario, choose the most appropriate status:

1. Successful GET.
1. New resource created.
1. Validation failure.
1. Authentication failure.
1. Authenticated but forbidden.
1. Missing resource.
1. Resource state conflict.
1. Unexpected application error.
1. Reverse proxy upstream failure.
1. Reverse proxy upstream timeout.

Explain why.

______________________________________________________________________

## Exercise 5 — Idempotency

Design:

```text
POST /payments
```

with an idempotency-key mechanism.

Define:

- Key format
- Storage
- Expiration
- Duplicate handling
- Response replay behavior
- What happens if the first request is still processing

______________________________________________________________________

## Exercise 6 — Networking Debugging

Given:

```text
DNS works
TCP connects
TLS succeeds
HTTP returns 504
```

Identify the most likely layer to investigate next and list five things you would check.

______________________________________________________________________

## Exercise 7 — HTTP/1.1 vs HTTP/2

Explain to another engineer why HTTP/2 can multiplex several requests over one connection while HTTP/1.1 commonly relies
on multiple connections for concurrency.

______________________________________________________________________

## Exercise 8 — Cookies and Sessions

Design a session-based authentication flow:

```text
Login
→ Set-Cookie
→ Subsequent request
→ Session lookup
→ Authenticated user
```

Explain where you would use:

```text
Secure
HttpOnly
SameSite
```

______________________________________________________________________

## Exercise 9 — REST Design

Design REST-style endpoints for:

```text
Users
Orders
Order items
```

Include:

- GET
- POST
- PUT/PATCH
- DELETE

Explain your URI choices.

______________________________________________________________________

## Exercise 10 — Latency Analysis

An API request takes 1.5 seconds.

Break the request into:

```text
DNS
TCP
TLS
Application
Database
External API
Response
```

Determine where the latency is actually being spent and propose improvements.

______________________________________________________________________

# 63. Quick Revision

| Concept | Key Point |
|---|---|
| DNS | Maps names to network addresses |
| A | IPv4 DNS record |
| AAAA | IPv6 DNS record |
| CNAME | Hostname alias |
| TTL | DNS cache lifetime |
| TCP | Reliable ordered byte stream |
| TCP handshake | SYN → SYN-ACK → ACK |
| UDP | Connectionless datagrams |
| Port | Identifies service endpoint |
| Socket | Network communication interface |
| Flow control | Protects receiver |
| Congestion control | Responds to network congestion |
| TLS | Encryption, integrity and authentication |
| HTTPS | HTTP over TLS |
| Certificate | Binds identity to public key through trust chain |
| HTTP | Application-layer request/response protocol |
| GET | Safe and idempotent retrieval |
| POST | Processing/creation; not idempotent by default |
| PUT | Replacement/creation at known URI; idempotent |
| PATCH | Partial modification |
| DELETE | Idempotent deletion semantics |
| 200 | Success |
| 201 | Created |
| 202 | Accepted |
| 204 | Success, no content |
| 400 | Bad request |
| 401 | Authentication problem |
| 403 | Forbidden |
| 404 | Not found |
| 409 | Conflict |
| 422 | Semantic validation failure |
| 500 | Server error |
| 502 | Bad upstream response |
| 503 | Service unavailable |
| 504 | Upstream timeout |
| Content-Type | Format of request/response body |
| Accept | Desired response format |
| Cookie | Browser-associated request data |
| Session | Logical client/session state across requests |
| Keep-alive | Reuse connection |
| HTTP/1.1 | Persistent connections, no stream multiplexing |
| HTTP/2 | Binary framing and multiplexed streams |
| REST | Architectural style |
| Statelessness | Request contains information needed to process it |
| Idempotency | Repeating request has same intended effect |
| Idempotency-Key | Application mechanism for safe retries |

______________________________________________________________________

# 64. Completion Checklist

Before moving to File 13, make sure you can explain:

- [ ] URL request flow
- [ ] DNS
- [ ] DNS resolution
- [ ] DNS records
- [ ] DNS TTL and caching
- [ ] TCP
- [ ] TCP byte-stream model
- [ ] TCP three-way handshake
- [ ] TCP reliability
- [ ] Flow control
- [ ] Congestion control
- [ ] UDP
- [ ] TCP vs UDP
- [ ] Ports
- [ ] Sockets
- [ ] TLS
- [ ] HTTPS
- [ ] TLS handshake at a high level
- [ ] Certificates
- [ ] Encryption
- [ ] Integrity
- [ ] Authentication
- [ ] HTTP request structure
- [ ] HTTP response structure
- [ ] HTTP methods
- [ ] GET
- [ ] POST
- [ ] PUT
- [ ] PATCH
- [ ] DELETE
- [ ] HEAD
- [ ] OPTIONS
- [ ] HTTP status-code categories
- [ ] Important 2xx codes
- [ ] Important 3xx codes
- [ ] Important 4xx codes
- [ ] Important 5xx codes
- [ ] HTTP headers
- [ ] Content-Type vs Accept
- [ ] Cookies
- [ ] Cookie security attributes
- [ ] Sessions
- [ ] Session storage
- [ ] Session vs token-based authentication
- [ ] Keep-alive
- [ ] HTTP/1.1
- [ ] HTTP/2 overview
- [ ] HTTP/1.1 vs HTTP/2
- [ ] REST
- [ ] REST resource design
- [ ] Statelessness
- [ ] Idempotency
- [ ] Idempotency keys
- [ ] Safe vs idempotent
- [ ] Networking debugging
- [ ] Latency breakdown
- [ ] Common networking interview traps

______________________________________________________________________

# 65. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What happens when you call an HTTPS API using a domain name?
1. What is DNS?
1. How does DNS resolution work at a high level?
1. What are A, AAAA and CNAME records?
1. What is DNS TTL?
1. What is TCP?
1. Explain the TCP three-way handshake.
1. Why does TCP provide reliable delivery?
1. What does it mean that TCP is a byte stream?
1. Flow control vs congestion control?
1. What is UDP?
1. TCP vs UDP?
1. What is a port?
1. What is a socket?
1. What is TLS?
1. What does HTTPS actually mean?
1. Explain the TLS handshake at a high level.
1. What is a TLS certificate?
1. Encryption vs authentication?
1. What is HTTP?
1. Explain the structure of an HTTP request.
1. Explain the structure of an HTTP response.
1. GET vs POST?
1. PUT vs PATCH?
1. Is DELETE idempotent?
1. Is PATCH idempotent?
1. What are the main HTTP status-code categories?
1. 400 vs 422?
1. 401 vs 403?
1. 404 vs 409?
1. 502 vs 503 vs 504?
1. What are HTTP headers?
1. Content-Type vs Accept?
1. What are cookies?
1. What is a session?
1. Where can session state be stored?
1. Explain Secure, HttpOnly and SameSite.
1. Session-based vs token-based authentication?
1. What is HTTP keep-alive?
1. What is HTTP/1.1?
1. What does HTTP/2 improve?
1. Explain HTTP/1.1 vs HTTP/2.
1. What is REST?
1. What does REST statelessness mean?
1. What is idempotency?
1. Why is idempotency important for payment APIs?
1. How would you implement an idempotency key?
1. Safe vs idempotent?
1. How would you debug an API that cannot resolve its hostname?
1. How would you debug connection refused?
1. How would you debug a TLS certificate error?
1. How would you debug a 502?
1. How would you debug a 504?
1. An async backend uses a blocking HTTP client. What problem can this create?
1. An API is slow because every request establishes a new connection. What would you investigate?
1. A client retries a POST after a timeout and creates duplicate resources. How would you fix the API?
1. Explain the complete path from DNS resolution to application response.
1. Where can latency be introduced in an HTTPS request?
1. How would you decide whether a failure is DNS, TCP, TLS or HTTP?
1. Why can an application return a 504 even though the application code itself has no obvious error?

If you can answer these clearly and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [11. Typing & Testing](./11-python-exceptions-typing-testing.md)

**Next:** [13. Complete Backend Request Lifecycle](./13-request-lifecycle.md)

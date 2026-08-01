# Security - Part 35

# DoS & DDoS Attacks

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What DoS is
- What DDoS is
- Difference between DoS and DDoS
- Common attack types
- Application-layer attacks
- Infrastructure-layer attacks
- Prevention techniques
- CDN
- WAF
- Rate Limiting
- Best practices

______________________________________________________________________

# What is DoS?

DoS stands for

**Denial of Service**.

A DoS attack attempts to make an application or service unavailable to legitimate users.

Instead of stealing data,

the attacker tries to **exhaust system resources**.

______________________________________________________________________

# What is DDoS?

DDoS stands for

**Distributed Denial of Service**.

Instead of using a single computer,

the attacker uses **many computers** simultaneously.

These computers are often called a

```text id="dd3501"
Botnet
```

______________________________________________________________________

# DoS vs DDoS

| DoS | DDoS |
| ------------------------ | ------------------------------------------ |
| Single attacking machine | Thousands or millions of attacking devices |
| Easier to detect | Much harder to detect |
| Smaller scale | Massive scale |
| Easier to block | Difficult to block |

______________________________________________________________________

# Typical Attack

```text id="dd3502"
Attacker

↓

Millions of Requests

↓

Backend

↓

Resources Exhausted

↓

Legitimate Users Blocked
```

______________________________________________________________________

# Real-World Example

Suppose your API normally receives

```text id="dd3503"
100 Requests / Second
```

During an attack,

it suddenly receives

```text id="dd3504"
2,000,000 Requests / Second
```

The server spends all its resources

processing malicious traffic,

leaving none for genuine users.

______________________________________________________________________

# Why Are DoS Attacks Dangerous?

Attackers may exhaust:

- CPU
- Memory
- Database connections
- Network bandwidth
- Disk I/O
- Thread pools

Eventually,

your application

becomes unavailable.

______________________________________________________________________

# Common Attack Types

## 1. Application-Layer Attack

Targets your application directly.

Example

```text id="dd3505"
GET /search
```

millions of times.

These requests may appear legitimate,

making them harder to distinguish.

______________________________________________________________________

## 2. Network Flood

The attacker floods

the network

with enormous traffic.

Example

```text id="dd3506"
Internet

↓

Huge Traffic

↓

Server
```

The network connection

becomes saturated

before requests even reach your application.

______________________________________________________________________

## 3. Login Flood

Attackers repeatedly call

```text id="dd3507"
POST /login
```

This consumes CPU

because password hashing

is intentionally expensive.

______________________________________________________________________

## 4. Expensive Query Attack

Suppose your API allows

complex searches.

The attacker repeatedly requests

expensive database operations,

causing high CPU

and database load.

______________________________________________________________________

# Prevention 1

## Rate Limiting

One of the simplest defenses.

Example

```text id="dd3508"
100 Requests

↓

1 Minute

↓

Allowed
```

Further requests receive

```http id="dd3509"
429 Too Many Requests
```

Rate limiting

reduces abuse,

especially at the application layer.

______________________________________________________________________

# Prevention 2

## Web Application Firewall (WAF)

A WAF sits

in front of your application.

```text id="dd3510"
Client

↓

WAF

↓

FastAPI
```

The WAF filters

malicious traffic

before it reaches your backend.

Popular WAFs include:

- Cloudflare WAF
- AWS WAF
- Azure WAF

______________________________________________________________________

# Prevention 3

## Content Delivery Network (CDN)

A CDN distributes content

across many servers.

```text id="dd3511"
Client

↓

Nearest CDN

↓

Origin Server
```

Benefits:

- Reduces latency
- Absorbs large traffic spikes
- Helps mitigate many DDoS attacks

Examples:

- Cloudflare
- Amazon CloudFront
- Fastly
- Akamai

______________________________________________________________________

# Prevention 4

## Load Balancer

Instead of one server,

use multiple.

```text id="dd3512"
Load Balancer

↓

FastAPI 1

↓

FastAPI 2

↓

FastAPI 3
```

Traffic is distributed,

reducing the chance

of a single server becoming overloaded.

______________________________________________________________________

# Prevention 5

## Caching

Frequently requested data

should come from

a cache

instead of the database.

```text id="dd3513"
Request

↓

Redis

↓

Database (only if needed)
```

Caching reduces

backend workload

during traffic spikes.

______________________________________________________________________

# Prevention 6

## Timeouts

Requests should not run forever.

Configure:

- Database timeouts
- HTTP timeouts
- Connection timeouts

This prevents

resources from being occupied indefinitely.

______________________________________________________________________

# Monitoring

Monitor:

- Request rate
- Error rate
- CPU usage
- Memory usage
- Database latency
- Network traffic

Sudden spikes

may indicate

an attack.

______________________________________________________________________

# Defense in Depth

A resilient architecture

uses multiple layers.

```text id="dd3514"
CDN

↓

WAF

↓

Load Balancer

↓

Rate Limiting

↓

Authentication

↓

Caching

↓

FastAPI
```

No single mechanism

is sufficient

against all attacks.

______________________________________________________________________

# What About Authentication?

Authentication helps,

but it doesn't stop

all DoS attacks.

Public endpoints

such as:

- Login
- Registration
- Search
- Health checks

may still be targeted.

Infrastructure protections

remain essential.

______________________________________________________________________

# Best Practices

✅ Use Rate Limiting.

✅ Deploy behind a CDN.

✅ Use a WAF.

✅ Cache frequently requested data.

✅ Configure load balancing.

✅ Monitor traffic continuously.

✅ Set appropriate timeouts.

______________________________________________________________________

# Common Mistakes

### Relying Only on Rate Limiting

Large DDoS attacks

often overwhelm

the network

before requests reach your application.

A CDN and WAF

provide additional protection.

______________________________________________________________________

### No Monitoring

Without monitoring,

an attack

may go unnoticed

until users report outages.

______________________________________________________________________

### Ignoring Public Endpoints

Public APIs

are common attack targets.

Protect them appropriately.

______________________________________________________________________

### No Resource Limits

Unbounded CPU,

memory,

or database usage

makes attacks more effective.

______________________________________________________________________

# Quick Comparison

| DoS | DDoS |
| --------------- | --------------------- |
| Single attacker | Many attackers |
| Easier to block | Harder to mitigate |
| Smaller traffic | Massive traffic |
| Limited impact | Internet-scale impact |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between DoS and DDoS attacks, and how can backend systems defend against them?

A Denial of Service (DoS) attack originates from a single source and attempts to make a service unavailable by
exhausting its resources. A Distributed Denial of Service (DDoS) attack uses many compromised systems to generate a much
larger volume of traffic, making it significantly harder to block. Defenses include rate limiting, Web Application
Firewalls (WAFs), Content Delivery Networks (CDNs), load balancers, caching, request timeouts, continuous monitoring,
and scalable infrastructure.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What DoS is
- What DDoS is
- DoS vs DDoS
- Common attack types
- Rate Limiting
- WAF
- CDN
- Load Balancers
- Monitoring
- Best practices

______________________________________________________________________

# What's Next

[Security Headers & Timing Attacks](36-security-headers-and-timing-attacks.md)

# Linux Complete Interview & Production Course

# File 16 — Linux Networking

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Networking
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 15 — Systemd and Service Management

______________________________________________________________________

# Table of Contents

1. Introduction
1. What is Computer Networking?
1. Why Networking Matters for Backend Engineers
1. Network Interface Cards (NICs)
1. IP Addresses
1. Subnets and CIDR
1. MAC Addresses
1. Default Gateway
1. DNS
1. Viewing Network Configuration
1. The `ip` Command
1. The `ss` Command
1. The `netstat` Command
1. The `ping` Command
1. The `curl` Command
1. The `wget` Command
1. The `dig` Command
1. The `host` Command
1. The `nslookup` Command
1. The `arp` Command
1. The `route` and `ip route` Commands
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

Networking is one of the most important skills for a backend engineer.

Every backend application communicates over a network.

Examples:

- Browser → Backend API
- Backend → Database
- Backend → Redis
- Backend → Kafka
- Backend → External APIs
- Kubernetes Pods
- Docker Containers

When something stops working, networking is often the first place to investigate.

______________________________________________________________________

# 2. What is Computer Networking?

A network is a collection of devices that communicate with each other.

Example:

```text
Laptop
    │
    ▼
Router
    │
    ├──────── Internet
    │
    ▼
Cloud Server
```

Communication happens using protocols such as:

- TCP
- UDP
- HTTP
- HTTPS
- SSH
- DNS

______________________________________________________________________

# 3. Why Networking Matters for Backend Engineers

Suppose a FastAPI application cannot connect to PostgreSQL.

Possible reasons include:

- Wrong IP address
- Incorrect port
- DNS failure
- Firewall blocking traffic
- Database not running
- Routing issues

Networking tools help identify the real cause quickly.

______________________________________________________________________

# 4. Network Interface Cards (NICs)

A **Network Interface Card (NIC)** is the hardware or virtual device that allows a machine to communicate over a
network.

Examples:

```text
eth0
ens33
enp0s3
wlan0
lo
```

`lo`

↓

Loopback interface

Used for communication with the same machine.

______________________________________________________________________

# View Interfaces

```bash
ip link
```

Example:

```text
lo
eth0
wlan0
```

______________________________________________________________________

# 5. IP Addresses

Every device on a network has an IP address.

Example:

```text
192.168.1.10
```

Public IP example:

```text
34.123.56.210
```

Private IP ranges:

| Range | Purpose |
|--------|----------|
| 10.0.0.0/8 | Private |
| 172.16.0.0/12 | Private |
| 192.168.0.0/16 | Private |

______________________________________________________________________

# IPv4 vs IPv6

IPv4:

```text
192.168.1.10
```

IPv6:

```text
2001:db8::1
```

IPv6 provides a much larger address space and is increasingly common in modern networks.

______________________________________________________________________

# 6. Subnets and CIDR

CIDR notation:

```text
192.168.1.0/24
```

Meaning:

- Network: `192.168.1.0`
- Prefix: `/24`

Equivalent subnet mask:

```text
255.255.255.0
```

A `/24` network typically provides 254 usable host addresses.

______________________________________________________________________

Common CIDR Prefixes

| CIDR | Subnet Mask |
|------|--------------|
| /8 | 255.0.0.0 |
| /16 | 255.255.0.0 |
| /24 | 255.255.255.0 |
| /32 | Single host |

______________________________________________________________________

# 7. MAC Addresses

Every network interface has a MAC (Media Access Control) address.

Example:

```text
08:00:27:3A:45:91
```

Characteristics:

- Layer 2 identifier
- Unique to the interface
- Used within local networks

View MAC address:

```bash
ip link
```

______________________________________________________________________

# 8. Default Gateway

The gateway is the device that forwards traffic to other networks.

Example:

```text
Laptop

↓

192.168.1.1

↓

Internet
```

Display routing table:

```bash
ip route
```

Example:

```text
default via 192.168.1.1
```

______________________________________________________________________

# 9. DNS

DNS (Domain Name System) translates names into IP addresses.

Example:

```text
google.com

↓

142.250.183.14
```

Without DNS, users would have to remember IP addresses instead of domain names.

DNS configuration is commonly stored in:

```text
/etc/resolv.conf
```

______________________________________________________________________

# 10. Viewing Network Configuration

Display IP addresses:

```bash
ip addr
```

Short version:

```bash
ip a
```

______________________________________________________________________

Display interfaces:

```bash
ip link
```

______________________________________________________________________

Display routing table:

```bash
ip route
```

______________________________________________________________________

Display hostname:

```bash
hostname
```

______________________________________________________________________

Display hostname and IP:

```bash
hostname -I
```

______________________________________________________________________

# 11. The `ip` Command

`ip` is the modern networking tool.

It replaces older commands such as:

- ifconfig
- route
- arp

______________________________________________________________________

Show interfaces:

```bash
ip link
```

______________________________________________________________________

Show IP addresses:

```bash
ip addr
```

______________________________________________________________________

Show routes:

```bash
ip route
```

______________________________________________________________________

Bring interface up:

```bash
sudo ip link set eth0 up
```

______________________________________________________________________

Bring interface down:

```bash
sudo ip link set eth0 down
```

______________________________________________________________________

# 12. The `ss` Command

`ss` displays socket information.

List listening TCP ports:

```bash
ss -tln
```

______________________________________________________________________

Listening UDP ports:

```bash
ss -uln
```

______________________________________________________________________

Show processes:

```bash
ss -tulpn
```

Useful for identifying which application is listening on a port.

______________________________________________________________________

# 13. The `netstat` Command

Older networking utility.

List listening ports:

```bash
netstat -tulpn
```

Many distributions recommend using `ss` instead because it is faster and more feature-rich.

______________________________________________________________________

# 14. The `ping` Command

Tests connectivity using ICMP Echo Requests.

Example:

```bash
ping google.com
```

______________________________________________________________________

Send four packets:

```bash
ping -c 4 google.com
```

______________________________________________________________________

Interpretation:

Successful replies indicate basic network connectivity.

Failure may indicate:

- Network issues
- Firewall restrictions
- DNS problems
- Host unreachable

______________________________________________________________________

# 15. The `curl` Command

Transfer data to or from a server.

Fetch a web page:

```bash
curl https://example.com
```

______________________________________________________________________

View only headers:

```bash
curl -I https://example.com
```

______________________________________________________________________

Make an API request:

```bash
curl https://api.github.com
```

______________________________________________________________________

POST request:

```bash
curl -X POST https://example.com/api
```

______________________________________________________________________

Download a file:

```bash
curl -O https://example.com/file.zip
```

______________________________________________________________________

# 16. The `wget` Command

Download files.

```bash
wget https://example.com/file.zip
```

______________________________________________________________________

Specify output file:

```bash
wget -O latest.zip https://example.com/file.zip
```

______________________________________________________________________

Resume download:

```bash
wget -c https://example.com/file.zip
```

______________________________________________________________________

# 17. The `dig` Command

Query DNS information.

```bash
dig google.com
```

______________________________________________________________________

Short answer:

```bash
dig +short google.com
```

______________________________________________________________________

Query specific record:

```bash
dig MX gmail.com
```

______________________________________________________________________

# 18. The `host` Command

Simple DNS lookup.

```bash
host google.com
```

Reverse lookup:

```bash
host 8.8.8.8
```

______________________________________________________________________

# 19. The `nslookup` Command

DNS lookup utility.

```bash
nslookup google.com
```

Query a specific DNS server:

```bash
nslookup google.com 8.8.8.8
```

______________________________________________________________________

# 20. The `arp` Command

Display ARP table.

```bash
arp -a
```

Modern alternative:

```bash
ip neigh
```

Shows IP-to-MAC address mappings.

______________________________________________________________________

# 21. The `route` and `ip route` Commands

Older command:

```bash
route -n
```

Modern equivalent:

```bash
ip route
```

Example output:

```text
default via 192.168.1.1 dev eth0
192.168.1.0/24 dev eth0
```

______________________________________________________________________

# 22. Production Examples

## Check if Nginx is Listening

```bash
ss -tulpn | grep 80
```

______________________________________________________________________

## Verify DNS Resolution

```bash
dig example.com
```

______________________________________________________________________

## Test API Connectivity

```bash
curl -I https://api.example.com
```

______________________________________________________________________

## Download Backup

```bash
wget https://backup.example.com/latest.sql.gz
```

______________________________________________________________________

## Check Default Gateway

```bash
ip route
```

______________________________________________________________________

## Find Service Listening on Port 5432

```bash
ss -tulpn | grep 5432
```

______________________________________________________________________

# 23. Common Mistakes

❌ Assuming `ping` failure always means the host is down.

Some servers block ICMP.

______________________________________________________________________

❌ Using `netstat` when `ss` is available.

______________________________________________________________________

❌ Forgetting DNS when troubleshooting connectivity.

______________________________________________________________________

❌ Confusing private IP addresses with public IP addresses.

______________________________________________________________________

❌ Ignoring routing table issues.

______________________________________________________________________

# 24. Best Practices

- Prefer `ip` over legacy networking commands.
- Use `ss` instead of `netstat` when available.
- Verify DNS before assuming network failure.
- Use `curl` for API testing.
- Understand the difference between Layer 2 (MAC) and Layer 3 (IP).

______________________________________________________________________

# Interview Questions

## Q1. What is the difference between an IP address and a MAC address?

**Answer**

An IP address identifies a device at the network layer (Layer 3) and is used for routing between networks. A MAC address
identifies a network interface at the data link layer (Layer 2) and is used for communication within a local network.

______________________________________________________________________

## Q2. Why is `ip` preferred over `ifconfig`?

**Answer**

The `ip` command is part of the iproute2 suite and provides a unified interface for managing network interfaces,
addresses, routes, and neighbors. It is actively maintained and has largely replaced older tools such as `ifconfig`,
`route`, and `arp`.

______________________________________________________________________

## Q3. What is the purpose of DNS?

**Answer**

DNS translates human-readable domain names into IP addresses, allowing applications and users to connect to servers
without knowing their numeric addresses.

______________________________________________________________________

## Q4. What is the difference between `curl` and `wget`?

**Answer**

`curl` is designed for transferring data to and from servers and supports many protocols, making it ideal for API
testing. `wget` is primarily designed for downloading files and supports features such as recursive downloads and
download resumption.

______________________________________________________________________

## Q5. Why is `ss` preferred over `netstat`?

**Answer**

`ss` is faster, provides more detailed socket information, and is the modern replacement for `netstat` on most Linux
distributions.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Display:

- Network interfaces
- IP addresses
- Routing table

using the `ip` command.

______________________________________________________________________

## Exercise 2

Ping:

- localhost
- Your default gateway
- google.com

Observe the results.

______________________________________________________________________

## Exercise 3

Query DNS records using:

- `dig`
- `host`
- `nslookup`

______________________________________________________________________

## Exercise 4

Display all listening TCP and UDP ports using `ss`.

______________________________________________________________________

## Exercise 5

Use `curl` to:

- Fetch a web page
- Display only response headers
- Send a simple POST request

______________________________________________________________________

## Exercise 6

Download a file using `wget` and resume an interrupted download.

______________________________________________________________________

# Cheat Sheet

## Network Information

```bash
ip addr
ip link
ip route
hostname
hostname -I
```

______________________________________________________________________

## Connectivity

```bash
ping
curl
wget
```

______________________________________________________________________

## DNS

```bash
dig
host
nslookup
```

______________________________________________________________________

## Ports

```bash
ss
netstat
```

______________________________________________________________________

## Neighbors

```bash
arp -a
ip neigh
```

______________________________________________________________________

# Summary

In this chapter, you learned the fundamentals of Linux networking, including IP addresses, MAC addresses, subnets,
gateways, DNS, network interfaces, and essential networking tools such as `ip`, `ss`, `ping`, `curl`, `wget`, `dig`,
`host`, `nslookup`, and `ip route`. These commands are indispensable for diagnosing connectivity issues and managing
production Linux systems.

______________________________________________________________________

## Next

[SSH and Remote Administration](17-ssh-and-remote-administration.md)

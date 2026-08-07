# Complete HTTP Request Lifecycle Deep Dive

## 04. TCP/IP and Network Routing

> Target Audience: Backend Engineers (Beginner → Senior)
>
> Goal: Understand how data travels from your computer to a remote server over the Internet, including TCP, IP, routers, NAT, ports, packet transmission, congestion control, retransmission, and what actually happens inside the operating system.

______________________________________________________________________

# Introduction

In the previous chapter,

DNS

returned

the IP address.

Example

```
www.google.com

↓

142.250.xxx.xxx
```

Now

the browser knows

where

Google lives.

The next question is

```
How does

my computer

actually

send data

to Google's server?
```

The answer is

```
TCP/IP
```

______________________________________________________________________

# The Journey

```
Browser

↓

Operating System

↓

TCP

↓

IP

↓

Ethernet / WiFi

↓

Home Router

↓

ISP

↓

Internet Routers

↓

Google Network

↓

Google Server
```

Everything

travels

as

packets.

______________________________________________________________________

# What Is TCP/IP?

Interview favorite.

TCP/IP

is actually

a collection

of protocols.

```
Application

↓

Transport

↓

Internet

↓

Network
```

______________________________________________________________________

# TCP/IP Layers

```
Application Layer

↓

Transport Layer

↓

Internet Layer

↓

Network Layer
```

______________________________________________________________________

## Application Layer

Examples

- HTTP
- HTTPS
- DNS
- SMTP
- FTP
- SSH

Your application

works here.

______________________________________________________________________

## Transport Layer

Protocols

```
TCP

UDP
```

Responsible for

- Reliable delivery
- Ports
- Ordering
- Retransmission

______________________________________________________________________

## Internet Layer

Responsible for

routing.

Protocol

```
IP
```

______________________________________________________________________

## Network Layer

Responsible for

physical communication.

Examples

- Ethernet
- WiFi

______________________________________________________________________

# TCP vs UDP

Interview favorite.

## TCP

Reliable

Ordered

Connection Oriented

Retransmission

Flow Control

Examples

- HTTPS
- SSH
- Database Connections

______________________________________________________________________

## UDP

Fast

Connectionless

No guarantee

No ordering

Examples

- DNS
- VoIP
- Online Games
- Video Streaming

______________________________________________________________________

# Why HTTP Uses TCP

Imagine

buying something

online.

Losing

one packet

could mean

losing

payment data.

HTTP requires

reliability.

Therefore

HTTP

uses

TCP.

______________________________________________________________________

# What Happens Before Sending Data?

The browser

cannot simply

start sending

HTTP data.

It first needs

a TCP connection.

This happens using

```
Three-Way Handshake
```

______________________________________________________________________

# Three-Way Handshake

Interview favorite.

```
Client

↓

SYN

↓

Server

↓

SYN + ACK

↓

Client

↓

ACK
```

Connection

is now

established.

______________________________________________________________________

# Step 1

# SYN

Client says

```
Hello

Can we connect?
```

Contains

- Source Port
- Destination Port
- Initial Sequence Number

______________________________________________________________________

# Step 2

# SYN + ACK

Server replies

```
Yes

Let's connect
```

Acknowledges

the client's

sequence number.

Provides

its own

sequence number.

______________________________________________________________________

# Step 3

# ACK

Client confirms

```
Connection Established
```

Now

both sides

can exchange

application data.

______________________________________________________________________

# Visual Flow

```
Client                     Server

SYN ---------------------->

<------------- SYN + ACK

ACK ----------------------->
```

______________________________________________________________________

# Why Three Steps?

Interview favorite.

Both client

and server

must agree

on

- Sequence numbers
- Connection state

This prevents

old packets

from

being reused.

______________________________________________________________________

# What Happens Inside The OS?

When Chrome

opens

a connection

it calls

```
socket()
```

The operating system

creates

a socket.

```
Chrome

↓

socket()

↓

Kernel

↓

TCP Socket
```

The kernel

manages

the connection,

not Chrome.

______________________________________________________________________

# Socket

Interview favorite.

A socket

is an endpoint

for communication.

Identified by

```
Source IP

+

Source Port

+

Destination IP

+

Destination Port
```

Example

```
192.168.1.5:52341

↓

142.250.xxx.xxx:443
```

______________________________________________________________________

# Ports

Ports identify

applications.

Examples

```
80

HTTP
```

```
443

HTTPS
```

```
22

SSH
```

```
5432

PostgreSQL
```

Client ports

are usually

random.

Example

```
52341
```

______________________________________________________________________

# Ephemeral Ports

Interview favorite.

Client

doesn't always use

port 80.

Instead

the OS

chooses

a temporary port.

Example

```
52341
```

Called

an

Ephemeral Port.

______________________________________________________________________

# Sequence Numbers

TCP

numbers

every byte.

Example

```
Packet 1

Sequence 1000
```

```
Packet 2

Sequence 1500
```

Receiver

knows

the correct order.

______________________________________________________________________

# Why Sequence Numbers?

Packets

may arrive

out of order.

TCP

reassembles

them correctly.

______________________________________________________________________

# Acknowledgements

Receiver

confirms

received bytes.

Example

```
ACK

2000
```

Means

```
Everything before

2000

received successfully.
```

______________________________________________________________________

# Retransmission

Interview favorite.

Suppose

Packet 2

is lost.

TCP detects

missing ACK.

```
Packet Lost

↓

Timeout

↓

Resend Packet
```

Reliable delivery.

______________________________________________________________________

# Flow Control

Suppose

the receiver

is slow.

TCP

prevents

overloading it.

Uses

```
Receive Window
```

Sender

transmits

only

what the receiver

can handle.

______________________________________________________________________

# Congestion Control

Interview favorite.

Suppose

the Internet

becomes congested.

TCP

reduces

its sending speed.

Algorithms

include

- Reno
- Cubic
- BBR

Purpose

Avoid

network collapse.

______________________________________________________________________

# MSS

Maximum Segment Size.

Example

```
1460 Bytes
```

Large messages

are split

into

multiple TCP segments.

______________________________________________________________________

# MTU

Maximum Transmission Unit.

Ethernet

commonly supports

```
1500 Bytes
```

Packets

larger than MTU

may require

fragmentation.

______________________________________________________________________

# Packet Fragmentation

Large packets

may be divided

into

smaller packets

during transmission.

Too much fragmentation

reduces performance.

______________________________________________________________________

# IP Addresses

Every device

needs

an IP address.

Example

```
192.168.1.10
```

Private.

______________________________________________________________________

```
8.8.8.8
```

Public.

______________________________________________________________________

# Private vs Public IP

Private

```
192.168.x.x

10.x.x.x

172.16.x.x
```

Public

Visible

on the Internet.

______________________________________________________________________

# NAT

Interview favorite.

Most homes

have

one public IP.

Multiple devices

share it.

```
Laptop

↓

Phone

↓

TV

↓

Router

↓

Public IP
```

The router

performs

```
Network Address Translation
```

______________________________________________________________________

# Routing

Packets

travel

through

multiple routers.

```
Laptop

↓

Home Router

↓

ISP

↓

Regional Router

↓

Internet Backbone

↓

Google Router

↓

Google Server
```

Each router

looks only

at

the destination IP.

______________________________________________________________________

# What Does A Router Do?

Router

reads

```
Destination IP
```

Looks

inside

its routing table.

Forwards

the packet

to

the next hop.

______________________________________________________________________

# TTL

Interview favorite.

IP packets

contain

```
Time To Live
```

Every router

reduces TTL

by

1.

If TTL

reaches

0

packet

is discarded.

Prevents

infinite routing loops.

______________________________________________________________________

# What Actually Travels?

Not

the HTTP request

directly.

Instead

```
HTTP

↓

TCP Segment

↓

IP Packet

↓

Ethernet Frame
```

Each layer

adds

its own header.

______________________________________________________________________

# Encapsulation

Interview favorite.

```
HTTP Request

↓

TCP Header

↓

IP Header

↓

Ethernet Header
```

This process

is called

```
Encapsulation
```

______________________________________________________________________

# At The Server

The reverse happens.

```
Ethernet

↓

IP

↓

TCP

↓

HTTP
```

Called

```
Decapsulation
```

______________________________________________________________________

# Packet Journey Example

```
Chrome

↓

Kernel

↓

TCP

↓

IP

↓

WiFi

↓

Router

↓

ISP

↓

Google

↓

Kernel

↓

TCP

↓

Nginx

↓

FastAPI
```

______________________________________________________________________

# What Happens If A Router Fails?

Routers

exchange

routing information.

Traffic

automatically

finds

another path.

This is why

the Internet

is resilient.

______________________________________________________________________

# Common Attacks

## SYN Flood

Interview favorite.

Attacker sends

millions of

```
SYN
```

packets

but never

completes

the handshake.

Result

Server resources

are exhausted.

Mitigation

- SYN Cookies
- Firewalls
- Rate Limiting

______________________________________________________________________

## IP Spoofing

Attacker

forges

the source IP.

Used

in

DDoS attacks.

______________________________________________________________________

## Packet Sniffing

Unencrypted traffic

can be intercepted.

Solution

HTTPS.

______________________________________________________________________

## Man-in-the-Middle

Attacker

intercepts

traffic

between

client

and server.

TLS

helps prevent

this attack.

______________________________________________________________________

# Technologies Used

| Layer | Technologies |
|--------|--------------|
| Application | HTTP, HTTPS |
| Transport | TCP, UDP |
| Internet | IPv4, IPv6 |
| Network | Ethernet, WiFi |
| Routing | BGP, OSPF |
| NAT | Home Router, Firewalls |

______________________________________________________________________

# Common Interview Questions

## Why does HTTP use TCP instead of UDP?

HTTP requires reliable, ordered delivery. TCP guarantees that data arrives completely and in the correct order, while
UDP does not.

______________________________________________________________________

## Why is the Three-Way Handshake necessary?

It establishes a reliable connection by synchronizing sequence numbers and confirming that both the client and server
are ready to communicate.

______________________________________________________________________

## What is the difference between an IP address and a port?

An IP address identifies a device on the network. A port identifies the application or service running on that device.

______________________________________________________________________

## What is NAT?

Network Address Translation allows multiple private devices to share a single public IP address by translating internal
addresses to an external one.

______________________________________________________________________

## What is encapsulation?

Each protocol layer wraps the data from the layer above with its own header before transmission. This process is called
encapsulation.

______________________________________________________________________

# Interview Deep Dive

## Question

Walk me through what happens after DNS returns an IP address.

### Answer

The browser asks the operating system to create a TCP socket. The OS performs the TCP three-way handshake with the
server. After the connection is established, HTTP data is encapsulated inside TCP segments, then IP packets, then
Ethernet frames. These packets travel through routers across the Internet until they reach the destination server.

______________________________________________________________________

# Summary

Before the first HTTP request is sent,

the operating system establishes a reliable TCP connection.

Key concepts include

- TCP vs UDP
- Three-Way Handshake
- Sockets
- Ports
- Sequence Numbers
- ACKs
- Retransmission
- Flow Control
- Congestion Control
- NAT
- Routing
- Encapsulation

Only after the TCP connection is established does the browser begin the **TLS Handshake**, which secures the
communication channel.

______________________________________________________________________

# Next

[05. TLS, HTTPS and HTTP Protocols](05-tls-https-and-http-protocols.md)

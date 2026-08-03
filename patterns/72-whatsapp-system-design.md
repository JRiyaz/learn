# System Design - Part 72

# WhatsApp System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Requirement gathering
- Capacity estimation
- API design
- High-Level Architecture
- One-to-One Messaging
- Group Messaging
- WebSockets
- Message Delivery
- Read Receipts
- Online Presence
- Offline Synchronization
- Media Messages
- Push Notifications
- Database Design
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design WhatsApp.**

This is one of

the most common

System Design interviews.

Unlike TinyURL,

WhatsApp is

a

real-time,

distributed,

high-scale system.

Millions

of users

send

billions

of messages

every day.

______________________________________________________________________

# Step 1

# Clarify Requirements

Functional Requirements

- Send messages
- Receive messages
- Group chat
- Online status
- Read receipts
- Typing indicators
- Media sharing
- Push notifications
- Message history

Non-Functional Requirements

- Low latency
- High availability
- Massive scalability
- Reliable delivery
- Message durability
- End-to-end encryption (out of scope for deep cryptography)

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

the platform has

2 Billion users.

Daily Active Users

```text id="wa7201"
500 Million
```

Average

messages/day

```text id="wa7202"
100 Billion
```

Average

Requests/sec

```text id="wa7203"
≈1.2 Million/sec
```

Peak traffic

may reach

3–5×

the average.

______________________________________________________________________

# Step 3

# API Design

Send Message

```http id="wa7204"
POST /messages
```

Request

```json id="wa7205"
{
  "receiver_id": 102,
  "message": "Hello"
}
```

______________________________________________________________________

Fetch Messages

```http id="wa7206"
GET /conversations/{id}
```

______________________________________________________________________

Upload Media

```http id="wa7207"
POST /media
```

______________________________________________________________________

# Step 4

# High-Level Architecture

```text id="wa7208"
Client

↓

Load Balancer

↓

API Gateway

↓

Chat Service

↓

Message Queue

↓

Database
```

For

real-time delivery,

another component

is required.

```text id="wa7209"
Client

↔

WebSocket Gateway
```

______________________________________________________________________

# Why WebSockets?

Interview favorite.

Polling

would generate

millions

of unnecessary requests.

WebSockets

maintain

persistent

connections.

Messages

are pushed

instantly.

______________________________________________________________________

# Sending a Message

Workflow

```text id="wa7210"
Sender

↓

Chat Service

↓

Store Message

↓

Queue

↓

Receiver
```

The sender

doesn't communicate

directly

with

the receiver.

______________________________________________________________________

# Message Storage

Store messages

before

delivering them.

Benefits

- Durability
- Offline delivery
- Retry capability

Database

is

the source

of truth.

______________________________________________________________________

# Database Schema

Messages

```text id="wa7211"
message_id

sender_id

receiver_id

conversation_id

content

status

created_at
```

Indexes

should exist

on

```text id="wa7212"
conversation_id
```

and

```text id="wa7213"
created_at
```

______________________________________________________________________

# Message Status

Each message

moves

through

multiple states.

```text id="wa7214"
Sent

↓

Delivered

↓

Read
```

The sender

receives

status updates

through

WebSockets.

______________________________________________________________________

# Delivery Flow

Suppose

Receiver

is online.

```text id="wa7215"
Sender

↓

Chat Service

↓

Receiver
```

Message

is delivered

immediately.

______________________________________________________________________

# Offline Users

Suppose

Receiver

is offline.

```text id="wa7216"
Store Message

↓

Wait

↓

User Connects

↓

Deliver
```

No message

is lost.

______________________________________________________________________

# Online Presence

Interview favorite.

Each client

maintains

a

WebSocket connection.

Server tracks

```text id="wa7217"
Online

Offline
```

Presence

is usually stored

inside

Redis

because

it changes

frequently.

______________________________________________________________________

# Typing Indicator

Typing indicators

should **not**

be stored

in

the database.

Workflow

```text id="wa7218"
Typing...

↓

WebSocket

↓

Receiver
```

These are

temporary events.

______________________________________________________________________

# Read Receipts

Suppose

Receiver

opens

the conversation.

```text id="wa7219"
Read

↓

Server

↓

Sender
```

Update

message status

to

Read.

______________________________________________________________________

# Group Chat

Interview favorite.

Suppose

a group

contains

100 members.

One message

must reach

99 recipients.

Workflow

```text id="wa7220"
Sender

↓

Group Service

↓

Queue

↓

Recipients
```

Delivery

is parallelized.

______________________________________________________________________

# Why Message Queue?

Sending

100 messages

synchronously

would increase

latency.

Instead,

publish

one event.

Workers

deliver

messages

independently.

______________________________________________________________________

# Media Messages

Images,

Videos,

and Documents

should **not**

be stored

inside

the database.

Workflow

```text id="wa7221"
Upload

↓

Object Storage

↓

Media URL

↓

Message
```

The message

contains

only

the media reference.

______________________________________________________________________

# Push Notifications

Suppose

Receiver

is offline.

The server

sends

a push notification.

```text id="wa7222"
Chat Service

↓

Push Service

↓

APNs / FCM

↓

Receiver
```

When

the user

opens

the app,

pending messages

are synchronized.

______________________________________________________________________

# Message Ordering

Interview favorite.

Users

expect messages

to appear

in order.

Possible approaches:

- Timestamp
- Sequence Number
- Conversation-specific ordering

Ordering

becomes harder

across

multiple servers.

______________________________________________________________________

# Duplicate Messages

Suppose

a network retry

occurs.

The same message

may arrive

twice.

Each message

should have

a unique

```text id="wa7223"
message_id
```

Duplicate IDs

are ignored.

This is

Idempotency.

______________________________________________________________________

# Scaling WebSockets

Millions

of users

cannot connect

to

one server.

```text id="wa7224"
Load Balancer

↓

WebSocket Server 1

WebSocket Server 2

WebSocket Server 3
```

Users

are distributed

across

multiple servers.

______________________________________________________________________

# Cross-Server Messaging

Suppose

Sender

connects

to

Server A,

while

Receiver

connects

to

Server B.

Servers

communicate

using

Kafka,

Redis Pub/Sub,

or another

message broker.

```text id="wa7225"
Server A

↓

Kafka

↓

Server B
```

______________________________________________________________________

# Database Scaling

Messages

grow rapidly.

Use

Sharding

based on

Conversation ID

or

User ID.

Read Replicas

can serve

history requests.

______________________________________________________________________

# Caching

Redis

stores:

- Online users
- Recent conversations
- Session data
- Presence information

Avoid

caching

entire

message history.

______________________________________________________________________

# Security

Implement:

- Authentication
- Authorization
- Rate Limiting
- TLS
- End-to-End Encryption

Authentication

protects

the platform.

Encryption

protects

message privacy.

______________________________________________________________________

# Observability

Monitor:

- Active WebSocket connections
- Message latency
- Delivery success rate
- Queue length
- Push notification failures
- Database latency

Logs

should include

Correlation IDs

for debugging.

______________________________________________________________________

# Failure Scenario

Suppose

WebSocket Server

crashes.

Clients

automatically

reconnect

to

another server.

Undelivered messages

remain

in

the database

or

message queue.

______________________________________________________________________

# Another Failure

Suppose

Kafka

is unavailable.

Messages

can still

be accepted

and stored,

but

cross-server delivery

may be delayed

until

Kafka recovers.

Retry mechanisms

prevent

message loss.

______________________________________________________________________

# End-to-End Architecture

```text id="wa7226"
Users

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Chat Service

↓

Kafka

↓

WebSocket Gateway

↓

Redis

↓

PostgreSQL

↓

Object Storage

↓

Push Notification Service
```

______________________________________________________________________

# Trade-offs

WebSockets

vs

Polling

| WebSockets | Polling |
| --------------------- | -------------------- |
| Low latency | Higher latency |
| Persistent connection | Repeated requests |
| More memory usage | More network traffic |

______________________________________________________________________

Redis

vs

Database

| Redis | Database |
| --------- | --------------- |
| Presence | Message history |
| Fast | Durable |
| In-memory | Persistent |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design WhatsApp?

Begin by gathering requirements and estimating the scale of users and messages. Use WebSockets for real-time
communication and store messages in a durable database before delivery to ensure reliability. Use Redis to maintain
online presence and recent session information. Store media files in Object Storage and include only media references in
messages. Use a message broker such as Kafka for asynchronous delivery across WebSocket servers, especially when sender
and receiver are connected to different servers. Scale stateless services horizontally behind load balancers, shard the
message database as data grows, and use push notifications for offline users. Implement authentication, rate limiting,
monitoring, and retry mechanisms to ensure reliability and scalability.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Requirement gathering
- Capacity estimation
- WebSockets
- Message delivery
- Group messaging
- Read receipts
- Online presence
- Media storage
- Push notifications
- Scaling
- Trade-offs

______________________________________________________________________

# 🧠 Real System Design Progress

You have completed:

- ✅ TinyURL
- ✅ WhatsApp

These two designs introduce many recurring patterns that you'll see in almost every distributed system.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll design **Instagram**, which combines:

- Social graph
- Feed generation
- Likes & comments
- Media uploads
- Followers
- News Feed ranking
- CDN
- Object Storage
- Recommendation systems

______________________________________________________________________

# What's Next

[Instagram System Design](73-instagram-system-design.md)

# System Design Case Study – WhatsApp

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Learn how to design a globally scalable real-time messaging platform like WhatsApp by applying concepts such as WebSockets, message queues, databases, caching, service discovery, replication, sharding, and end-to-end message delivery.

______________________________________________________________________

# Introduction

WhatsApp

is one of

the most popular

System Design interviews.

Unlike

Instagram,

the biggest challenge

is

```
Real-Time Communication
```

This design covers

- Real-time messaging
- WebSockets
- Message delivery
- Online presence
- Read receipts
- Message ordering
- Offline users
- Media sharing
- Notifications
- Scaling

______________________________________________________________________

# Step 1

# Clarify Requirements

Before

designing,

ask questions.

Example

```
One-to-One Chat?
```

```
Group Chat?
```

```
Media Sharing?
```

```
Voice Notes?
```

```
Read Receipts?
```

```
Online Status?
```

```
End-to-End Encryption?
```

______________________________________________________________________

# Functional Requirements

Assume

WhatsApp supports

- User registration
- One-to-one chat
- Group chat
- Media sharing
- Read receipts
- Online status
- Push notifications
- Offline messaging

______________________________________________________________________

# Non-Functional Requirements

Need

- Extremely low latency
- High availability
- Massive scalability
- Reliable delivery
- Fault tolerance
- Horizontal scaling

______________________________________________________________________

# Step 2

# Capacity Estimation

Assumptions

```
2 Billion Users
```

```
800 Million DAU
```

Each user

sends

```
50 Messages/day
```

Daily messages

```
40 Billion
```

______________________________________________________________________

# Peak Load

Average

```
≈463,000 Messages/sec
```

Peak

```
1–2 Million Messages/sec
```

Must support

millions

of concurrent

connections.

______________________________________________________________________

# Step 3

# High-Level Architecture

```
                    Users
                       │
                       ▼
                     DNS
                       │
                       ▼
                Load Balancer
                       │
                       ▼
                Connection Servers
                       │
              (WebSocket Servers)
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 Message Service  Presence Service  Group Service
        │              │              │
        ▼              ▼              ▼
 Redis Cache     Database      RabbitMQ / Kafka
```

______________________________________________________________________

# Why HTTP Is Not Enough

Suppose

User A

sends

a message.

With HTTP

```
Request

↓

Response

↓

Closed
```

Real-time chat

would require

continuous polling.

Very inefficient.

______________________________________________________________________

# WebSockets

Interview favorite.

WebSocket

creates

one

persistent connection.

```
Client

⇄

Server
```

Messages

flow

instantly

in

both directions.

______________________________________________________________________

# Why WebSockets?

Benefits

- Real-time communication
- Low latency
- Less network overhead
- Persistent connection

Perfect

for chat applications.

______________________________________________________________________

# Step 4

# Connection Servers

Every user

maintains

a WebSocket connection.

```
User A

⇄

Connection Server
```

```
User B

⇄

Connection Server
```

The server

knows

which users

are online.

______________________________________________________________________

# Step 5

# Sending A Message

```
User A

↓

Connection Server

↓

Message Service

↓

Database

↓

Queue

↓

Connection Server

↓

User B
```

______________________________________________________________________

# Step 6

# Message Storage

Messages

must be

stored.

Simple schema

| Column | Description |
|----------|------------|
| id | Message ID |
| sender | Sender ID |
| receiver | Receiver ID |
| content | Message |
| timestamp | Time |
| status | Sent/Delivered/Read |

______________________________________________________________________

# Database Choice

Message history

can be stored

in

SQL

or

NoSQL

depending

on requirements.

Large-scale systems

often favor

distributed databases

optimized

for high write throughput.

The interview

focus

is

the reasoning,

not

the product name.

______________________________________________________________________

# Step 7

# Message Queue

Instead of

sending

messages

directly

```
Sender

↓

Queue

↓

Receiver
```

Benefits

- Retry
- Reliability
- Decoupling
- Scalability

______________________________________________________________________

# Step 8

# Offline Users

Suppose

User B

is offline.

```
Message

↓

Database

↓

Pending
```

When

User B

comes online,

messages

are delivered.

______________________________________________________________________

# Step 9

# Message Status

Typical lifecycle

```
Sent

↓

Delivered

↓

Read
```

Each state

is updated

as events occur.

______________________________________________________________________

# Read Receipts

Suppose

User B

opens

the chat.

```
Read

↓

Receipt

↓

Sender Updated
```

Blue ticks

appear.

______________________________________________________________________

# Step 10

# Online Presence

Presence Service

tracks

who is online.

```
User Connected

↓

Redis

↓

Online
```

When

the connection closes,

status changes

to

```
Offline
```

______________________________________________________________________

# Why Redis?

Presence

changes

very frequently.

Redis

provides

fast

in-memory storage

for

online status.

______________________________________________________________________

# Step 11

# Typing Indicator

Typing

should not

be stored

inside

the database.

Instead

```
Typing

↓

WebSocket

↓

Receiver
```

Temporary

real-time event.

______________________________________________________________________

# Step 12

# Group Chat

Group

contains

multiple members.

```
Sender

↓

Group Service

↓

Members

↓

Queue

↓

Delivery
```

Large groups

require

efficient fan-out.

______________________________________________________________________

# Fan-Out

Suppose

Group

has

100 members.

```
One Message

↓

100 Deliveries
```

Workers

can distribute

delivery

asynchronously.

______________________________________________________________________

# Step 13

# Media Sharing

Photos

videos

documents

should not

travel

through

the database.

Flow

```
Upload

↓

Object Storage

↓

URL

↓

Message
```

Message

contains

only

metadata.

______________________________________________________________________

# CDN

Media

should be

downloaded

through

a CDN.

Benefits

- Faster downloads
- Lower latency
- Reduced origin load

______________________________________________________________________

# Step 14

# Push Notifications

Suppose

receiver

is offline.

```
Message

↓

Notification Service

↓

FCM / APNs

↓

Mobile Device
```

The user

is notified

without

an active

WebSocket connection.

______________________________________________________________________

# Step 15

# Message Ordering

Interview favorite.

Suppose

User A

sends

```
Hi

↓

How are you?

↓

See you.
```

Receiver

must see

the same order.

Ordering

is critical

within

a conversation.

______________________________________________________________________

# Sequence Numbers

Each conversation

can assign

sequence numbers.

```
1

↓

2

↓

3
```

Helps

preserve ordering

and detect

missing messages.

______________________________________________________________________

# Step 16

# Duplicate Messages

Networks

may retry.

```
Message

↓

Delivered

↓

Retry
```

Clients

should detect

duplicate

message IDs

and ignore

repeated deliveries.

______________________________________________________________________

# Step 17

# End-to-End Encryption

Interview bonus.

Messages

are encrypted

on

the sender's device

and decrypted

only

on

the receiver's device.

Servers

forward

encrypted data

without

reading

the message content.

______________________________________________________________________

# Step 18

# Database Replication

```
Primary

↓

Replica

↓

Replica
```

Provides

high availability.

______________________________________________________________________

# Step 19

# Database Sharding

Eventually

billions

of messages

exist.

Shard

using

```
Conversation ID

or

User ID
```

A stable,

high-cardinality key

helps distribute

message data.

______________________________________________________________________

# Step 20

# Service Discovery

Connection servers

need

to locate

message services.

Use

Service Discovery

for

dynamic routing.

______________________________________________________________________

# Step 21

# Monitoring

Monitor

- Active connections
- Message latency
- Delivery success
- Queue length
- WebSocket disconnects
- Error rate

______________________________________________________________________

# Failure Scenarios

## Connection Server Fails

Users

reconnect

to

another

connection server.

______________________________________________________________________

## Queue Failure

Messages

remain

until

workers recover.

______________________________________________________________________

## Database Failure

Replica

becomes

new primary.

______________________________________________________________________

## Receiver Offline

Messages

remain stored

until

delivery succeeds.

______________________________________________________________________

# Read vs Write Ratio

Unlike

Instagram,

WhatsApp

is

write-heavy.

Optimization

must support

high message throughput

while still serving

chat history efficiently.

______________________________________________________________________

# CAP Discussion

Availability

is important,

but

within

an individual conversation,

message ordering

and reliable delivery

are also critical.

Different features

may make

different trade-offs.

______________________________________________________________________

# Typical Architecture

```
                    Users
                       │
                       ▼
                Load Balancer
                       │
                       ▼
              WebSocket Servers
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 Message Service  Presence Service  Group Service
        │              │              │
        ▼              ▼              ▼
 Database         Redis Cache    RabbitMQ / Kafka
        │
        ▼
 Object Storage
        │
        ▼
      CDN
```

______________________________________________________________________

# Common Interview Follow-Up Questions

## Why use WebSockets instead of HTTP?

WebSockets maintain a persistent bidirectional connection, allowing messages to be delivered instantly without repeated
polling.

______________________________________________________________________

## Why use Redis for presence?

Online status changes frequently and requires extremely fast reads and writes. Redis provides low-latency in-memory
storage well suited for presence information.

______________________________________________________________________

## How do offline users receive messages?

Messages are stored durably. When the user reconnects, pending messages are delivered. Push notifications can also alert
offline users.

______________________________________________________________________

## Why use Object Storage for media?

Large media files should be stored separately from chat metadata. Messages contain references to media rather than the
media itself.

______________________________________________________________________

## How do you preserve message ordering?

Assign sequence numbers within each conversation and process messages in order for that conversation. Ordering across
unrelated conversations is generally unnecessary.

______________________________________________________________________

# Common Mistakes

## Using HTTP Polling

Persistent

WebSockets

provide

better efficiency

for real-time chat.

______________________________________________________________________

## Storing Media In Database

Store

media

inside

Object Storage.

______________________________________________________________________

## Ignoring Offline Users

Reliable delivery

requires

persistent storage

for pending messages.

______________________________________________________________________

## Forgetting Ordering

Users

expect

messages

to appear

in the correct order.

______________________________________________________________________

## Treating Presence As Permanent Data

Presence

is transient

and belongs

in

fast in-memory storage,

not

a relational database.

______________________________________________________________________

# Best Practices

✅ Use WebSockets for real-time messaging.

✅ Store media in Object Storage.

✅ Cache presence in Redis.

✅ Use message queues for reliable delivery.

✅ Preserve ordering within conversations.

✅ Scale connection servers horizontally.

______________________________________________________________________

# Interview Deep Dive

## Question

Why are WebSockets essential for WhatsApp?

### Answer

WebSockets provide persistent bidirectional communication, allowing messages, typing indicators, and read receipts to be
exchanged in real time with significantly lower overhead than repeated HTTP polling.

______________________________________________________________________

## Question

How do you handle users who are offline?

### Answer

Messages are stored in durable storage with a pending status. When the user reconnects, undelivered messages are
retrieved and sent. Push notifications may also alert the user.

______________________________________________________________________

## Question

What is the biggest challenge in designing WhatsApp?

### Answer

Maintaining low-latency, reliable, and ordered message delivery for millions of concurrent users while scaling
connection servers and handling intermittent network connectivity.

______________________________________________________________________

# Practice Exercise

Design WhatsApp

for

3 Billion Users.

Explain

1. API design
1. WebSocket architecture
1. Message storage
1. Presence service
1. Offline delivery
1. Media handling
1. Database choice
1. Queue design
1. Replication
1. Sharding
1. Monitoring
1. Trade-offs

Try presenting

the entire design

within

45–60 minutes,

similar to

a real

System Design interview.

______________________________________________________________________

# Summary

WhatsApp is an excellent System Design case study because it emphasizes real-time communication at massive scale.

A strong solution should demonstrate

- Requirement gathering
- WebSocket architecture
- Reliable message delivery
- Offline messaging
- Presence tracking
- Media storage
- Message ordering
- Caching
- Replication
- Sharding
- High availability
- Trade-off analysis

Mastering this design prepares you for interviews involving messaging platforms, collaboration tools, and other
low-latency distributed systems.

______________________________________________________________________

# Next

[System Design Case Study – Uber](24-design-uber.md)

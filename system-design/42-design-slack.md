# Advanced Distributed Systems – Designing Slack

> Target Audience: Senior Backend Engineers (5–10 Years)
>
> Goal: Understand how to design a real-time collaboration platform like Slack, including messaging, channels, WebSockets, presence, notifications, file sharing, search, and scalability.

______________________________________________________________________

# Introduction

Slack

is much more

than

a chat application.

It provides

- Real-time messaging
- Channels
- Direct Messages
- Presence
- Notifications
- File Sharing
- Search
- Threads
- Reactions

The biggest challenge

is

```
Deliver

Millions

of Messages

In Real Time
```

while

maintaining

ordering,

availability,

and

low latency.

______________________________________________________________________

# Functional Requirements

Assume

our system

supports

- Channels
- Direct Messages
- Group Chats
- File Uploads
- Search
- Threads
- Reactions
- Presence
- Notifications
- Message History

______________________________________________________________________

# Non-Functional Requirements

Need

- Low Latency
- High Availability
- Horizontal Scalability
- Ordering
- Reliability
- Fault Tolerance

______________________________________________________________________

# High-Level Architecture

```
                   Users

                     │

                     ▼

              Load Balancer

                     │

                     ▼

              Gateway Service

                     │

          WebSocket Connections

                     │

     ┌───────────────┼───────────────┐

     ▼               ▼               ▼

 Messaging      Presence        Notification

     │               │               │

     ▼               ▼               ▼

 Kafka         Redis Cluster      Queue

     │

     ▼

 Message Database
```

______________________________________________________________________

# Core Services

Split

the application

into

multiple services.

- Gateway Service
- Authentication
- Messaging Service
- Channel Service
- Presence Service
- Notification Service
- Search Service
- File Service
- Reaction Service

______________________________________________________________________

# Authentication

User

logs in

using

OAuth

or

credentials.

Receives

```
JWT
```

Used

for

WebSocket

authentication.

______________________________________________________________________

# Why WebSockets?

Interview favorite.

HTTP

requires

continuous polling.

Instead

Slack uses

```
Persistent

WebSocket

Connection
```

Messages

arrive instantly.

______________________________________________________________________

# Connection Flow

```
Client

↓

Authenticate

↓

Open WebSocket

↓

Receive Messages

↓

Send Messages
```

______________________________________________________________________

# Why Not Polling?

Polling

```
Every

2 Seconds
```

causes

- Higher latency
- More requests
- More bandwidth

WebSockets

eliminate

repeated requests.

______________________________________________________________________

# Channel Model

Each message

belongs

to

a channel.

Example

```
#backend

#devops

#general
```

Users

subscribe

to channels.

______________________________________________________________________

# Direct Messages

Private

conversation

between

users.

```
User A

↓

DM

↓

User B
```

Stored

separately

from

channels.

______________________________________________________________________

# Sending A Message

```
Client

↓

Gateway

↓

Messaging Service

↓

Kafka

↓

Database

↓

Online Users
```

______________________________________________________________________

# Why Kafka?

Interview favorite.

Message traffic

can spike

dramatically.

Kafka

buffers

messages

and

decouples

producers

from

consumers.

______________________________________________________________________

# Message Persistence

Never

deliver

messages

only

from memory.

Always

persist

them.

```
Message

↓

Database

↓

Delivery
```

This allows

history

and

offline synchronization.

______________________________________________________________________

# Ordering

Interview favorite.

Messages

inside

the same

channel

should appear

in order.

Possible approaches

- Partition by Channel ID
- Sequence Numbers
- Timestamp ordering

______________________________________________________________________

# Database Design

Messages

| id | channel | sender | text |

Channels

| id | name |

Users

| id | name |

Reactions

| message | emoji | user |

______________________________________________________________________

# File Uploads

Files

should not

be stored

inside

the database.

Use

Object Storage.

```
Upload

↓

Object Storage

↓

URL

↓

Message
```

______________________________________________________________________

# Presence

Interview favorite.

Presence

shows

whether

a user

is

```
Online

Offline

Away
```

______________________________________________________________________

# Presence Tracking

Users

send

heartbeats.

```
Heartbeat

↓

Redis

↓

Online
```

If

heartbeats stop

mark

user

offline.

______________________________________________________________________

# Typing Indicator

Typing

should

not

be persisted.

```
Typing

↓

WebSocket

↓

Channel Members
```

Temporary

real-time event.

______________________________________________________________________

# Read Receipts

Track

the latest

message

seen

by

each user.

Example

```
Channel

↓

Last Read Message ID
```

______________________________________________________________________

# Notifications

If

receiver

is offline

```
Store Notification

↓

Push Notification

↓

Mobile Device
```

If

receiver

is online

deliver

through

WebSocket.

______________________________________________________________________

# Offline Users

Interview favorite.

Suppose

user

disconnects.

Messages

are

stored

in

database.

When

the user

reconnects

```
Last Seen

↓

Fetch Missing Messages
```

______________________________________________________________________

# Search

Messages

can be

indexed

inside

Elasticsearch

or

another

search engine.

Supports

- Full-text search
- Filters
- Date ranges

______________________________________________________________________

# Threads

Thread

contains

child messages.

```
Message

↓

Replies
```

Parent

message

stores

thread metadata.

______________________________________________________________________

# Reactions

Emoji

reactions

are stored

separately.

```
👍

❤️

🎉
```

Avoid

rewriting

entire messages.

______________________________________________________________________

# Message Editing

Maintain

history

when required.

```
Original

↓

Edited
```

Auditability

may be

important

for enterprise

customers.

______________________________________________________________________

# Message Deletion

Delete

or

soft delete

depending

on

retention policy.

______________________________________________________________________

# Multi-Tenant Support

Interview bonus.

Slack

supports

organizations.

Every request

includes

```
Workspace ID
```

Messages

are isolated

per workspace.

______________________________________________________________________

# Rate Limiting

Prevent

spam.

Example

```
100 Messages

Per Minute
```

Different

limits

may apply

to bots,

users,

and integrations.

______________________________________________________________________

# Monitoring

Monitor

- Active WebSockets
- Message latency
- Delivery success
- Offline queue size
- Search latency
- Presence updates
- Kafka lag

______________________________________________________________________

# Failure Scenarios

## WebSocket Server Failure

Reconnect

client

to

another

Gateway Server.

______________________________________________________________________

## Kafka Failure

Retry

or

use

replicated brokers.

______________________________________________________________________

## Database Failure

Serve

from

replica

when appropriate,

then

promote

a new primary

if necessary.

______________________________________________________________________

## User Offline

Store

messages

and

deliver

after reconnect.

______________________________________________________________________

## Notification Failure

Retry

delivery

using

queue

and

backoff.

______________________________________________________________________

# Typical Architecture

```
                   Users

                      │

                      ▼

               Load Balancer

                      │

                      ▼

             WebSocket Gateway

                      │

      ┌───────────────┼───────────────┐

      ▼               ▼               ▼

 Messaging       Presence        Notification

      │               │               │

      ▼               ▼               ▼

 Kafka          Redis Cluster      Queue

      │

      ▼

 Message Database

      │

      ▼

 Search Index

      │

      ▼

 Object Storage
```

______________________________________________________________________

# Common Interview Questions

## Why use WebSockets?

WebSockets provide persistent bidirectional communication, enabling real-time message delivery without continuous
polling.

______________________________________________________________________

## Why use Kafka?

Kafka decouples message producers and consumers, absorbs traffic spikes, and enables scalable asynchronous processing.

______________________________________________________________________

## Why store messages before delivery?

Persisting messages ensures reliable history, supports offline users, and allows clients to synchronize after
reconnecting.

______________________________________________________________________

## How do offline users receive messages?

Messages are stored in the database. When users reconnect, the client requests all messages after the last acknowledged
message.

______________________________________________________________________

## How do you maintain message ordering?

Messages within a channel can be partitioned by Channel ID and assigned sequence numbers to preserve ordering for that
conversation.

______________________________________________________________________

# Common Mistakes

## Using Polling

Prefer

WebSockets

for

real-time messaging.

______________________________________________________________________

## No Persistence

Always

store

messages

before

delivery.

______________________________________________________________________

## Database For Presence

Presence

changes frequently.

Use

Redis

or

another

fast in-memory store.

______________________________________________________________________

## Files Inside Database

Store

large files

inside

Object Storage.

______________________________________________________________________

## Ignoring Offline Users

Always

support

message synchronization

after reconnect.

______________________________________________________________________

# Best Practices

✅ Use WebSockets.

✅ Persist messages before delivery.

✅ Track presence in Redis.

✅ Store files in Object Storage.

✅ Index messages for search.

✅ Use Kafka for scalable messaging.

✅ Support offline synchronization.

______________________________________________________________________

# Interview Deep Dive

## Question

Why is WebSocket preferred over HTTP polling?

### Answer

WebSockets maintain a persistent connection, allowing instant bidirectional communication with significantly lower
latency and reduced network overhead compared to repeated polling.

______________________________________________________________________

## Question

How does Slack support offline users?

### Answer

Messages are stored durably in the database. After reconnecting, the client requests all messages that were sent after
its last acknowledged message.

______________________________________________________________________

## Question

How do you scale Slack to millions of users?

### Answer

Distribute WebSocket gateways, partition messages by Channel ID, use Kafka for asynchronous messaging, Redis for
presence, object storage for files, and separate search infrastructure for indexing.

______________________________________________________________________

# Practice Exercise

Design

Slack.

Explain

1. WebSocket architecture
1. Authentication
1. Message flow
1. Ordering
1. Presence
1. Offline synchronization
1. Notifications
1. Search
1. File uploads
1. Monitoring
1. Failure recovery
1. Trade-offs

Present

your solution

within

60 minutes,

similar to

a Senior Backend Engineer

System Design interview.

______________________________________________________________________

# Summary

Slack is one of the best advanced System Design interview problems because it combines real-time communication,
distributed messaging, persistence, search, notifications, and scalability.

A strong solution should demonstrate

- WebSockets
- Messaging architecture
- Kafka
- Presence tracking
- Offline synchronization
- Message ordering
- Search indexing
- Object storage
- Monitoring
- Trade-off analysis

Mastering Slack prepares you for interviews involving collaboration platforms, chat systems, real-time applications, and
large-scale distributed backend services.

______________________________________________________________________

# Next

[43. Designing Kubernetes Control Plane](43-design-kubernetes-control-plane.md)

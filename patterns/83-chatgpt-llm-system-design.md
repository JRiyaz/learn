# System Design - Part 83

# ChatGPT / LLM System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Requirement gathering
- Capacity estimation
- API design
- High-Level Architecture
- LLM Serving
- Prompt Processing
- Context Management
- Token Streaming
- Model Routing
- GPU Inference
- Conversation History
- RAG Integration
- Safety & Moderation
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design ChatGPT.**

Unlike

WhatsApp

or

Amazon,

ChatGPT

doesn't retrieve

predefined data.

It

**generates**

responses

token by token.

The biggest challenges

are:

- GPU inference
- Low response latency
- Long conversations
- Massive compute cost
- Context management

______________________________________________________________________

# Step 1

# Clarify Requirements

Functional Requirements

- User authentication
- Start conversation
- Continue conversation
- Stream responses
- Upload documents
- Search knowledge (optional)
- Conversation history

Optional

- Voice mode
- Image understanding
- Code execution
- Web search

______________________________________________________________________

# Non-Functional Requirements

- Low latency
- High availability
- Massive scalability
- Streaming responses
- High GPU utilization

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

the platform

has

```text id="llm8301"
300 Million Users
```

Daily Active Users

```text id="llm8302"
80 Million
```

Peak Requests

```text id="llm8303"
250,000 Requests/sec
```

Average Response

```text id="llm8304"
800 Tokens
```

Observation.

The bottleneck

is

GPU inference,

not

the database.

______________________________________________________________________

# Step 3

# API Design

New Conversation

```http id="llm8305"
POST /conversations
```

______________________________________________________________________

Send Message

```http id="llm8306"
POST /chat
```

______________________________________________________________________

Conversation History

```http id="llm8307"
GET /conversations/{id}
```

______________________________________________________________________

Upload Document

```http id="llm8308"
POST /documents
```

______________________________________________________________________

# Step 4

# High-Level Architecture

```text id="llm8309"
Client

↓

API Gateway

↓

Chat Service

↓

LLM Router

↓

GPU Workers

↓

Streaming Service
```

Supporting services:

- Conversation Service
- Authentication Service
- Moderation Service
- Vector Database (optional)
- Analytics

______________________________________________________________________

# Request Flow

```text id="llm8310"
User Prompt

↓

Authentication

↓

Conversation Lookup

↓

Prompt Builder

↓

LLM

↓

Stream Tokens
```

______________________________________________________________________

# Conversation History

Interview favorite.

LLMs

are stateless.

They do not

remember

previous conversations

between requests.

Therefore,

the application

stores

conversation history.

Schema

```text id="llm8311"
conversation_id

user_id

message

role

timestamp
```

Before

calling

the LLM,

retrieve

relevant messages.

______________________________________________________________________

# Prompt Construction

The final prompt

is built

from:

- System Prompt
- Previous Messages
- User Message

Example

```text id="llm8312"
System Prompt

↓

Conversation

↓

User Prompt
```

This combined prompt

is sent

to

the model.

______________________________________________________________________

# Context Window

Interview favorite.

Every model

has

a maximum

context size.

Example

```text id="llm8313"
128K Tokens
```

If

the conversation

becomes longer,

the system

must:

- Remove older messages
- Summarize history
- Retrieve relevant context

______________________________________________________________________

# Prompt Compression

Instead of

sending

the entire conversation,

older messages

can be summarized.

```text id="llm8314"
100 Messages

↓

Summary

↓

Recent Messages
```

This saves

tokens

and

reduces cost.

______________________________________________________________________

# Model Routing

Interview favorite.

Not every request

needs

the largest model.

Example

```text id="llm8315"
Simple Question

↓

Small Model
```

```text id="llm8316"
Complex Coding

↓

Large Model
```

Routing

reduces

GPU cost.

______________________________________________________________________

# GPU Workers

The LLM

runs

on

GPU clusters.

```text id="llm8317"
Router

↓

GPU Pool

↓

Inference
```

Multiple GPUs

serve

requests

in parallel.

______________________________________________________________________

# Token Streaming

Interview favorite.

Users

should not

wait

until

the entire answer

is generated.

Instead,

stream

tokens

as they

are produced.

```text id="llm8318"
Token

↓

Token

↓

Token

↓

Complete
```

Streaming

improves

perceived latency.

______________________________________________________________________

# Why Streaming?

Suppose

the response

takes

20 seconds.

Without streaming,

the user

waits

20 seconds.

With streaming,

the first token

may appear

within

1 second.

______________________________________________________________________

# Batch Inference

Interview favorite.

GPU utilization

improves

by batching

multiple requests.

```text id="llm8319"
Request A

↓

Request B

↓

Request C

↓

One GPU Batch
```

Trade-off:

Larger batches

increase throughput,

but

may increase latency.

______________________________________________________________________

# Retrieval-Augmented Generation (RAG)

Optional

knowledge retrieval.

Workflow

```text id="llm8320"
User Query

↓

Embedding

↓

Vector Search

↓

Relevant Chunks

↓

LLM
```

This enables

the model

to answer

questions

using

external knowledge.

______________________________________________________________________

# Moderation

Before

sending

the prompt,

run

Safety Checks.

Workflow

```text id="llm8321"
Prompt

↓

Moderation

↓

LLM
```

The response

may also

be checked

before

returning it.

______________________________________________________________________

# Conversation Storage

Messages

are stored

inside

a database.

Redis

may cache

recent conversations.

Older conversations

remain

in

persistent storage.

______________________________________________________________________

# Search

Conversation search

can use

Elasticsearch

for:

- Keyword search
- Message history
- Shared conversations

______________________________________________________________________

# File Uploads

Documents

are stored

in

Object Storage.

Metadata

is stored

inside

the database.

If

RAG

is enabled,

documents

are:

```text id="llm8322"
Upload

↓

Chunk

↓

Embedding

↓

Vector Database
```

______________________________________________________________________

# Caching

Redis stores:

- User sessions
- Recent conversations
- Authentication tokens
- Frequently used prompts
- Rate limit counters

Model outputs

may also

be cached

for

identical prompts

when appropriate.

______________________________________________________________________

# Scaling

Scale independently:

- API Gateway
- Chat Service
- GPU Workers
- Vector Search
- Moderation
- Analytics

GPU clusters

can autoscale

based on

queue length.

______________________________________________________________________

# AI/ML Example

Modern LLM systems

may use:

- Multiple models
- Mixture-of-Experts (MoE)
- Tool calling
- Code execution
- Web search
- Function calling

The Router

chooses

the appropriate

pipeline.

______________________________________________________________________

# Failure Scenario

Suppose

the GPU cluster

is overloaded.

Possible actions:

- Queue requests
- Route to another region
- Use a smaller model
- Return a "server busy" response

Graceful degradation

maintains

availability.

______________________________________________________________________

# Another Failure

Suppose

the Vector Database

fails.

Chat

still works.

Only

knowledge retrieval

is unavailable.

The system

falls back

to

base model inference.

______________________________________________________________________

# End-to-End Architecture

```text id="llm8323"
User

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Authentication

↓

Chat Service

↓

Conversation Service

↓

Redis

↓

PostgreSQL

↓

LLM Router

↓

Moderation

↓

GPU Workers

↓

Streaming Service

↓

Object Storage

↓

Embedding Service

↓

Vector Database

↓

Analytics
```

______________________________________________________________________

# Trade-offs

Streaming

vs

Complete Response

| Streaming | Complete Response |
| ------------------------------ | --------------------- |
| Better UX | Simpler |
| Lower perceived latency | User waits longer |
| More implementation complexity | Easier implementation |

______________________________________________________________________

Small Model

vs

Large Model

| Small | Large |
| --------------- | ---------------- |
| Lower cost | Better quality |
| Faster | Slower |
| Lower GPU usage | Higher GPU usage |

______________________________________________________________________

RAG

vs

Fine-Tuning

| RAG | Fine-Tuning |
| ----------------------- | -------------------------- |
| Uses external knowledge | Changes model behavior |
| Easy to update | Expensive retraining |
| Good for dynamic data | Good for specialized tasks |

______________________________________________________________________

# Best Practices

✅ Stream tokens.

✅ Separate conversation storage from model inference.

✅ Use model routing to optimize cost.

✅ Cache recent conversations.

✅ Apply moderation before and after generation.

______________________________________________________________________

# Common Mistakes

### Treating the LLM as Stateful

The model

does not

remember

previous API calls.

Always

send

the required context.

______________________________________________________________________

### Sending Entire Conversation

Long conversations

increase:

- Cost
- Latency
- GPU memory usage

Use

summarization

or

context selection.

______________________________________________________________________

### Blocking on External Retrieval

RAG

should have

timeouts

and

fallback behavior.

A failed retrieval

should not

bring down

the chat system.

______________________________________________________________________

### Ignoring GPU Bottlenecks

CPU scaling

doesn't help

if

GPU inference

is the bottleneck.

Monitor:

- GPU utilization
- Queue length
- Tokens/sec
- Time-to-first-token

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design ChatGPT?

Start by separating API handling, conversation management, and model inference. Store conversation history in a database
because LLMs are stateless, then construct prompts by combining the system prompt, relevant conversation history, and
the latest user message. Route requests through a model router that selects an appropriate model based on complexity.
Execute inference on GPU workers and stream generated tokens back to the client for low perceived latency. Optionally
integrate Retrieval-Augmented Generation by retrieving relevant documents from a vector database before inference. Use
Redis for caching sessions, Kafka for analytics, moderation services for safety, and autoscaling GPU clusters to handle
changing workloads while monitoring GPU utilization and token generation latency.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Conversation management
- Prompt construction
- Context windows
- Prompt compression
- Model routing
- GPU inference
- Token streaming
- RAG integration
- Moderation
- Scaling
- Trade-offs

______________________________________________________________________

# 🧠 Real System Design Progress

You have completed:

- ✅ TinyURL
- ✅ WhatsApp
- ✅ Instagram
- ✅ Twitter/X
- ✅ YouTube
- ✅ Netflix
- ✅ Spotify
- ✅ Google Drive
- ✅ Uber
- ✅ Amazon
- ✅ Payment Gateway
- ✅ Notification Service
- ✅ ChatGPT / LLM System

You now understand the architecture behind modern Large Language Model applications.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll design one of the hottest AI architectures used in enterprise applications:

- Document ingestion
- Chunking strategies
- Embeddings
- Vector databases
- Retrieval pipeline
- Re-ranking
- Prompt augmentation
- Hallucination reduction

We'll design a **RAG (Retrieval-Augmented Generation) System**.

______________________________________________________________________

# What's Next

[RAG System Design](84-rag-system-design.md)

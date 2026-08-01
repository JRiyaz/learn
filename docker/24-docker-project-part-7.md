# Docker - Part 24

# Docker Project - Part 7

# End-to-End Testing

______________________________________________________________________

# Introduction

Our Library API now includes:

- FastAPI
- PostgreSQL
- Redis
- Kafka
- Docker Compose

Every component is connected.

Now we need to answer an important question.

> **Does everything actually work together?**

Individual services working correctly does **not** guarantee the complete application works correctly.

This chapter focuses on **end-to-end testing** of the entire Docker stack.

______________________________________________________________________

# What is End-to-End Testing?

End-to-end (E2E) testing verifies the complete application from the client's perspective.

Instead of testing

```text id="e2e001"
FastAPI
```

or

```text id="e2e002"
PostgreSQL
```

individually,

we test

```text id="e2e003"
Client

↓

FastAPI

↓

Redis

↓

PostgreSQL

↓

Kafka
```

Everything together.

______________________________________________________________________

# Test Environment

Start the application.

```bash id="e2e004"
docker compose up --build
```

Verify

```bash id="e2e005"
docker compose ps
```

Expected

```text id="e2e006"
api

postgres

redis

kafka

Running
```

Every service should be healthy before testing.

______________________________________________________________________

# Verify Health Endpoint

```http id="e2e007"
GET /health
```

Expected response

```json id="e2e008"
{
    "status": "healthy"
}
```

______________________________________________________________________

# Create a Book

Request

```http id="e2e009"
POST /books
```

Body

```json id="e2e010"
{
    "title": "Designing Data-Intensive Applications",
    "author": "Martin Kleppmann"
}
```

Expected

```json id="e2e011"
{
    "id": 1,
    "title": "Designing Data-Intensive Applications",
    "author": "Martin Kleppmann",
    "available": true
}
```

______________________________________________________________________

# Verify PostgreSQL

Connect

```bash id="e2e012"
docker exec -it postgres \
psql \
-U appuser \
-d library
```

Run

```sql id="e2e013"
SELECT *

FROM books;
```

Expected

```text id="e2e014"
1

Designing Data-Intensive Applications

Martin Kleppmann

true
```

The data exists

inside PostgreSQL.

______________________________________________________________________

# Verify Redis Cache

First request

```http id="e2e015"
GET /books/1
```

Expected flow

```text id="e2e016"
Redis

↓

Miss

↓

PostgreSQL

↓

Redis

↓

Response
```

______________________________________________________________________

# Second Request

```http id="e2e017"
GET /books/1
```

Expected flow

```text id="e2e018"
Redis

↓

Hit

↓

Response
```

The database

isn't queried again.

______________________________________________________________________

# Verify Redis

Open Redis CLI.

```bash id="e2e019"
docker exec -it redis \
redis-cli
```

Retrieve

```bash id="e2e020"
GET book:1
```

Expected

```json id="e2e021"
{
    "id": 1,
    "title": "Designing Data-Intensive Applications",
    "author": "Martin Kleppmann",
    "available": true
}
```

Redis

contains

the cached object.

______________________________________________________________________

# Borrow the Book

```http id="e2e022"
POST /books/1/borrow
```

Expected

```json id="e2e023"
{
    "available": false
}
```

______________________________________________________________________

# Verify Cache Invalidation

Immediately

retrieve

the book again.

```http id="e2e024"
GET /books/1
```

Expected

```text id="e2e025"
Redis

↓

Miss

↓

Database

↓

New Cache
```

The cache should now contain the updated state.

______________________________________________________________________

# Return the Book

```http id="e2e026"
POST /books/1/return
```

Expected

```json id="e2e027"
{
    "available": true
}
```

______________________________________________________________________

# Verify Kafka Event

Run

the temporary consumer.

Expected

```text id="e2e028"
book.created

book.borrowed

book.returned
```

Every operation

publishes an event.

______________________________________________________________________

# Verify Logs

FastAPI

```bash id="e2e029"
docker compose logs api
```

Redis

```bash id="e2e030"
docker compose logs redis
```

PostgreSQL

```bash id="e2e031"
docker compose logs postgres
```

Kafka

```bash id="e2e032"
docker compose logs kafka
```

Logs help identify integration problems.

______________________________________________________________________

# Restart Containers

Stop everything.

```bash id="e2e033"
docker compose down
```

Start again.

```bash id="e2e034"
docker compose up
```

Expected

```text id="e2e035"
Book Still Exists
```

because PostgreSQL uses a named volume.

______________________________________________________________________

# Verify Volume

Check

```bash id="e2e036"
docker volume ls
```

Expected

```text id="e2e037"
postgres-data

redis-data
```

Persistent storage

is working.

______________________________________________________________________

# Test Failure Scenario

Stop PostgreSQL.

```bash id="e2e038"
docker stop postgres
```

Call

```http id="e2e039"
GET /books
```

Expected

```text id="e2e040"
Database Error
```

The API should fail gracefully,

returning an appropriate error instead of crashing unexpectedly.

______________________________________________________________________

# Restart PostgreSQL

```bash id="e2e041"
docker start postgres
```

Verify

the API

works again.

______________________________________________________________________

# Verify Networking

Enter

the API container.

```bash id="e2e042"
docker exec -it library-api sh
```

Confirm

environment variables.

```bash id="e2e043"
printenv
```

Expected

```text id="e2e044"
DATABASE_URL

REDIS_URL

KAFKA_BROKER
```

______________________________________________________________________

# Test Checklist

```text id="e2e045"
✓ FastAPI Running

✓ PostgreSQL Connected

✓ Redis Connected

✓ Kafka Connected

✓ CRUD Working

✓ Cache Working

✓ Events Published

✓ Volumes Working

✓ Networking Working
```

If every box is checked,

the application is functioning correctly.

______________________________________________________________________

# Manual Testing Tools

Useful tools

```text id="e2e046"
Swagger UI

curl

HTTPie

Postman
```

Swagger UI

is already available

through FastAPI.

______________________________________________________________________

# Common Mistakes

### Testing Only Individual Services

Always verify

the complete request flow.

______________________________________________________________________

### Ignoring Logs

Logs often reveal the root cause.

______________________________________________________________________

### Forgetting Persistent Volumes

Restart containers

to confirm

data persists.

______________________________________________________________________

### Not Testing Failure Cases

Successful requests

aren't enough.

Test recovery

and error handling.

______________________________________________________________________

# Best Practices

- Test the full application stack.
- Verify persistence.
- Verify caching.
- Verify Kafka events.
- Test restarts.
- Test failure scenarios.
- Check logs during debugging.

______________________________________________________________________

# Hands-on Exercise

1. Start the Docker stack.
1. Create a book.
1. Verify it in PostgreSQL.
1. Retrieve it twice and observe Redis caching.
1. Borrow the book.
1. Verify cache invalidation.
1. Verify Kafka events.
1. Restart the application.
1. Confirm the data still exists.
1. Simulate a database failure and observe the API behavior.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What would you verify during an end-to-end test of a Dockerized backend application?

I would verify that all containers start correctly, health checks pass, and services communicate over the Docker
network. Then I would test the complete user workflow, confirm data is stored in PostgreSQL, verify Redis caching and
cache invalidation, ensure Kafka events are published, confirm data persists after container restarts, and test failure
scenarios such as database unavailability to validate error handling.

______________________________________________________________________

# Summary

In this chapter, you learned:

- End-to-end testing
- Service verification
- CRUD validation
- Redis cache validation
- Kafka event validation
- Volume persistence
- Restart testing
- Failure testing
- Log inspection
- Production testing workflow

Our Dockerized application is now fully integrated and verified.

In the next chapter, we'll optimize the project for production by improving the Dockerfile, reducing image size,
strengthening security, and preparing it for deployment.

______________________________________________________________________

## Next File

[Docker Project - Part 8](25-docker-project-part-8.md)

# Kafka Order Processing Project - Part 1

## Project Overview

In this project, we'll build a **simple but realistic Order Processing System** using Kafka.

Unlike the final production project that we'll build after completing the Microservices section, this project focuses on
**learning Kafka** while still following good backend development practices.

We'll build a single FastAPI application that:

- Accepts orders through a REST API.
- Stores orders in PostgreSQL.
- Publishes an event to Kafka.
- Allows multiple independent consumers to process the event.

By the end of this project, you'll understand how Kafka fits into a backend application.

______________________________________________________________________

# Project Architecture

```text
                        Client
                           │
                           ▼
                    FastAPI Application
                           │
                Create Order API Endpoint
                           │
                           ▼
                     PostgreSQL Database
                           │
                           ▼
                     Kafka Producer
                           │
                     orders.created
                           │
        ┌──────────┬────────────┬────────────┬────────────┐
        ▼          ▼            ▼            ▼
   Inventory    Payment      Email      Analytics
    Consumer    Consumer     Consumer     Consumer
```

Notice that the API never directly calls Inventory, Payment, or Email.

It only publishes an event.

______________________________________________________________________

# Learning Objectives

In this project you'll learn:

- SQLModel
- PostgreSQL
- FastAPI
- Kafka Producer
- Kafka Consumer
- JSON Events
- Event-Driven Architecture

______________________________________________________________________

# Suggested Folder Structure

Although all code is included in this Markdown file, a real project could be organized like this:

```text
order_processing/

├── app.py
├── database.py
├── models.py
├── schemas.py
├── producer.py
├── consumer.py
├── config.py
└── requirements.txt
```

______________________________________________________________________

# Step 1 — Install Dependencies

```bash
pip install fastapi

pip install uvicorn

pip install sqlmodel

pip install psycopg2-binary

pip install confluent-kafka
```

______________________________________________________________________

# Step 2 — Database Configuration

**database.py**

```python
from sqlmodel import SQLModel
from sqlmodel import create_engine

DATABASE_URL = (
    "postgresql://postgres:password@localhost:5432/orders_db"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)


def create_db():

    SQLModel.metadata.create_all(engine)
```

______________________________________________________________________

# Step 3 — Order Model

**models.py**

```python
from typing import Optional

from sqlmodel import SQLModel
from sqlmodel import Field


class Order(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    customer_id: int

    product_name: str

    quantity: int

    price: float

    status: str = "CREATED"
```

______________________________________________________________________

# Step 4 — API Schema

**schemas.py**

```python
from pydantic import BaseModel


class CreateOrderRequest(BaseModel):

    customer_id: int

    product_name: str

    quantity: int

    price: float
```

______________________________________________________________________

# Why Separate Models?

Database Model

↓

Stores data

API Schema

↓

Validates requests

Never expose database models directly through your API.

______________________________________________________________________

# Step 5 — Kafka Event

Instead of publishing the SQLModel object,

publish an event.

Example

```json
{
    "event_type": "OrderCreated",
    "order_id": 1,
    "customer_id": 5,
    "product_name": "Keyboard",
    "quantity": 2,
    "price": 4999
}
```

Notice

This is a **business event**.

Not a database object.

______________________________________________________________________

# Step 6 — Kafka Producer

**producer.py**

```python
import json

from confluent_kafka import Producer


producer = Producer(
    {
        "bootstrap.servers": "localhost:9092"
    }
)


def publish_order_created(event: dict):

    producer.produce(
        topic="orders.created",
        key=str(event["order_id"]),
        value=json.dumps(event),
    )

    producer.flush()
```

______________________________________________________________________

# Why Use order_id as Key?

Kafka guarantees ordering **within a partition**.

Using the order ID ensures that all events related to the same order are routed consistently based on the partitioning
strategy, preserving their order.

______________________________________________________________________

# Step 7 — FastAPI Application

**app.py**

```python
from fastapi import FastAPI

app = FastAPI()
```

______________________________________________________________________

# Create Database

```python
from database import create_db


@app.on_event("startup")

def startup():

    create_db()
```

______________________________________________________________________

# Database Session

```python
from sqlmodel import Session

from database import engine


def get_session():

    with Session(engine) as session:

        yield session
```

______________________________________________________________________

# Create Order Endpoint

```python
from fastapi import Depends

from sqlmodel import Session

from models import Order

from schemas import CreateOrderRequest

from producer import publish_order_created


@app.post("/orders")

def create_order(

    request: CreateOrderRequest,

    session: Session = Depends(get_session)

):

    order = Order(

        customer_id=request.customer_id,

        product_name=request.product_name,

        quantity=request.quantity,

        price=request.price

    )

    session.add(order)

    session.commit()

    session.refresh(order)

    publish_order_created(

        {

            "event_type": "OrderCreated",

            "order_id": order.id,

            "customer_id": order.customer_id,

            "product_name": order.product_name,

            "quantity": order.quantity,

            "price": order.price

        }

    )

    return order
```

______________________________________________________________________

# Complete Flow

```text
Client

↓

POST /orders

↓

Validate Request

↓

Insert into PostgreSQL

↓

Publish Kafka Event

↓

Return Response
```

______________________________________________________________________

# Testing the API

Request

```http
POST /orders
```

Body

```json
{
    "customer_id": 10,
    "product_name": "Mechanical Keyboard",
    "quantity": 1,
    "price": 6999
}
```

Response

```json
{
    "id": 1,
    "customer_id": 10,
    "product_name": "Mechanical Keyboard",
    "quantity": 1,
    "price": 6999,
    "status": "CREATED"
}
```

______________________________________________________________________

# Kafka Event Produced

```json
{
    "event_type": "OrderCreated",
    "order_id": 1,
    "customer_id": 10,
    "product_name": "Mechanical Keyboard",
    "quantity": 1,
    "price": 6999
}
```

This event is now available for any interested consumer.

______________________________________________________________________

# Why Save Before Publishing?

Correct sequence

```text
Save Order

↓

Commit Transaction

↓

Publish Event
```

If the database transaction fails, no event should be published.

> **Note:** In highly reliable production systems, this pattern is often replaced or strengthened with the **Transactional Outbox Pattern** to avoid inconsistencies if the application crashes after the database commit but before publishing to Kafka. We'll cover that in the Microservices section.

______________________________________________________________________

# Common Mistakes

### Publishing Before Saving

Wrong

```text
Publish Event

↓

Save Database
```

If the database write fails,

Kafka now contains an event for an order that never existed.

______________________________________________________________________

### Sending ORM Objects

Publish business events instead.

______________________________________________________________________

### Hardcoding Topics Everywhere

Centralize topic names in a configuration module.

______________________________________________________________________

### Forgetting JSON Serialization

Kafka messages are bytes.

Serialize structured data before publishing.

______________________________________________________________________

# Best Practices

- Publish business events.
- Keep events immutable.
- Save to the database before publishing (or use the Outbox Pattern in production).
- Keep event payloads focused on business information.
- Use meaningful topic names.
- Use message keys when ordering matters.

______________________________________________________________________

# Hands-on Exercise

Extend the project.

Requirements

1. Add an `order_status` field.
1. Add a `currency` field.
1. Publish the currency in the Kafka event.
1. Add validation for positive quantity.
1. Add validation for positive price.
1. Create a second endpoint to fetch an order by ID.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should Kafka events contain business information instead of database models?

Kafka events are contracts between services. If events expose database models directly, consumers become tightly coupled
to the producer's database schema. Any schema change can break downstream services. Business events describe what
happened in the domain (for example, `OrderCreated`) and remain stable even if the underlying database implementation
changes.

______________________________________________________________________

# Summary

In this part, you built:

- PostgreSQL configuration
- SQLModel model
- FastAPI application
- Create Order endpoint
- Kafka Producer
- Business event publishing

In the next part, we'll build the consumers that react independently to the `orders.created` topic.

______________________________________________________________________

## Next File

[7-kafka-order-processing-project-part-2.md](7-kafka-order-processing-project-part-2.md)

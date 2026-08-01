# Kafka with Python & FastAPI - Part 1

## Introduction

In previous chapters, you learned:

- Kafka Architecture
- Producers
- Consumers
- Partitions
- Offsets
- Replication
- Consumer Groups

Now it's time to build a **production-ready Kafka integration** using Python and FastAPI.

This chapter covers:

- Project Structure
- Configuration Management
- Producer Wrapper
- Consumer Wrapper
- Pydantic Models
- JSON Serialization
- Dependency Injection
- FastAPI Integration
- Production Folder Structure
- Best Practices

______________________________________________________________________

# Project Architecture

A typical microservice using Kafka should not contain Kafka code directly inside API endpoints.

Instead, separate responsibilities.

```text id="kf001"
FastAPI

↓

Service Layer

↓

Kafka Producer

↓

Kafka Broker
```

Consumers should also be independent services.

```text id="kf002"
Kafka

↓

Consumer

↓

Business Logic

↓

Database
```

______________________________________________________________________

# Recommended Project Structure

```text id="kf003"
order_service/

├── app/

│   ├── api/

│   ├── core/

│   ├── kafka/

│   │      ├── producer.py

│   │      ├── consumer.py

│   │      ├── config.py

│   │      └── serializer.py

│   ├── models/

│   ├── schemas/

│   ├── services/

│   └── main.py

└── requirements.txt
```

Keep Kafka logic isolated.

______________________________________________________________________

# Installing Dependencies

```bash id="kf004"
pip install fastapi

pip install uvicorn

pip install confluent-kafka

pip install pydantic-settings
```

______________________________________________________________________

# Configuration Management

Never hardcode Kafka addresses.

Bad

```python id="kf005"
Producer({

"bootstrap.servers":

"localhost:9092"

})
```

Good

Configuration file.

______________________________________________________________________

# config.py

```python id="kf006"
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    kafka_bootstrap_servers: str = "localhost:9092"

    kafka_orders_topic: str = "orders"

    class Config:

        env_file = ".env"


settings = Settings()
```

______________________________________________________________________

# .env

```text id="kf007"
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

KAFKA_ORDERS_TOPIC=orders
```

Now configuration can change without changing code.

______________________________________________________________________

# Producer Wrapper

Instead of creating producers everywhere,

build one reusable class.

```python id="kf008"
from confluent_kafka import Producer

from app.kafka.config import settings


class KafkaProducer:

    def __init__(self):

        self.producer = Producer(

            {

                "bootstrap.servers":

                settings.kafka_bootstrap_servers

            }

        )
```

______________________________________________________________________

# Delivery Callback

```python id="kf009"
def delivery_report(

    err,

    msg

):

    if err:

        print(

            "Delivery Failed",

            err

        )

    else:

        print(

            f"Delivered to "

            f"{msg.topic()} "

            f"partition "

            f"{msg.partition()} "

            f"offset "

            f"{msg.offset()}"

        )
```

______________________________________________________________________

# Publish Method

```python id="kf010"
import json


class KafkaProducer:

    ...

    def publish(

        self,

        topic,

        key,

        message

    ):

        self.producer.produce(

            topic=topic,

            key=key,

            value=json.dumps(message),

            on_delivery=delivery_report

        )

        self.producer.flush()
```

Now every API can reuse this class.

______________________________________________________________________

# Why Create a Wrapper?

Without wrapper

```text id="kf011"
Endpoint A

↓

Producer Code

Endpoint B

↓

Producer Code

Endpoint C

↓

Producer Code
```

Code duplication.

With wrapper

```text id="kf012"
Endpoints

↓

KafkaProducer

↓

Kafka
```

Cleaner.

______________________________________________________________________

# Serializer

Kafka messages should have a consistent format.

serializer.py

```python id="kf013"
import json


def serialize(

    data: dict

):

    return json.dumps(data)
```

______________________________________________________________________

Deserialize

```python id="kf014"
import json


def deserialize(

    value: bytes

):

    return json.loads(

        value.decode()

    )
```

Centralizing serialization keeps producer and consumer behavior consistent.

______________________________________________________________________

# Pydantic Model

```python id="kf015"
from pydantic import BaseModel


class OrderEvent(

    BaseModel

):

    order_id: int

    customer_id: int

    amount: float
```

Advantages

- Validation
- Type safety
- Documentation

______________________________________________________________________

# Producer Using Pydantic

```python id="kf016"
event = OrderEvent(

    order_id=101,

    customer_id=42,

    amount=500

)
```

Publish

```python id="kf017"
producer.publish(

    topic="orders",

    key=str(

        event.customer_id

    ),

    message=event.model_dump()

)
```

`model_dump()` converts the model into a dictionary suitable for JSON serialization.

______________________________________________________________________

# FastAPI Dependency

Create

```python id="kf018"
producer = KafkaProducer()
```

Reuse

```python id="kf019"
from fastapi import Depends


def get_producer():

    return producer
```

Endpoint

```python id="kf020"
@app.post("/orders")

def create_order(

    event: OrderEvent,

    producer:

    KafkaProducer = Depends(

        get_producer

    )

):

    producer.publish(

        topic="orders",

        key=str(

            event.customer_id

        ),

        message=event.model_dump()

    )

    return {

        "status":

        "published"

    }
```

______________________________________________________________________

# Why Dependency Injection?

Instead of

```text id="kf021"
Endpoint

↓

New Producer
```

Use

```text id="kf022"
Application

↓

One Producer

↓

All Endpoints
```

Producer creation is relatively expensive.

Reuse it.

______________________________________________________________________

# Consumer Wrapper

Consumer logic should also be encapsulated.

```python id="kf023"
from confluent_kafka import Consumer

from app.kafka.config import settings


class KafkaConsumer:

    def __init__(

        self,

        group

    ):

        self.consumer = Consumer(

            {

                "bootstrap.servers":

                settings.kafka_bootstrap_servers,

                "group.id": group,

                "auto.offset.reset":

                "earliest"

            }

        )
```

______________________________________________________________________

# Subscribe

```python id="kf024"
consumer.consumer.subscribe(

    [

        settings.kafka_orders_topic

    ]

)
```

______________________________________________________________________

# Polling

```python id="kf025"
while True:

    message = consumer.consumer.poll(

        1

    )

    if message is None:

        continue

    if message.error():

        print(

            message.error()

        )

        continue

    print(

        deserialize(

            message.value()

        )

    )
```

______________________________________________________________________

# Producer Flow

```text id="kf026"
Client

↓

FastAPI

↓

Pydantic

↓

KafkaProducer

↓

Kafka
```

______________________________________________________________________

# Consumer Flow

```text id="kf027"
Kafka

↓

KafkaConsumer

↓

Deserialize

↓

Business Logic
```

______________________________________________________________________

# Logging

Instead of

```python id="kf028"
print(...)
```

Prefer Python's `logging` module.

```python id="kf029"
import logging

logger = logging.getLogger(__name__)

logger.info(

    "Order Published"

)
```

______________________________________________________________________

# Configuration Per Environment

Development

```text id="kf030"
localhost
```

Production

```text id="kf031"
kafka-1.internal

kafka-2.internal

kafka-3.internal
```

Environment variables make this transition simple.

______________________________________________________________________

# Common Mistakes

### Creating a Producer Per Request

Wrong

```text id="kf032"
Request

↓

New Producer
```

Reuse producers.

______________________________________________________________________

### Hardcoding Topics

Use configuration.

______________________________________________________________________

### Ignoring Validation

Always validate incoming events with Pydantic before publishing.

______________________________________________________________________

### Mixing Kafka Code with Business Logic

Separate responsibilities.

______________________________________________________________________

# Best Practices

- Create one Producer instance.
- Use dependency injection.
- Validate messages using Pydantic.
- Centralize serialization.
- Keep configuration in environment variables.
- Separate Kafka infrastructure from business logic.
- Log publish failures.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should Kafka code be wrapped inside reusable classes instead of being written directly in API
endpoints?

Wrapping Kafka operations inside dedicated producer and consumer classes separates infrastructure concerns from business
logic. This improves maintainability, testing, and code reuse. Endpoints remain focused on request validation and
business behavior, while Kafka-specific configuration, serialization, retries, and logging are centralized in one place.
This design also makes it easier to replace or extend the messaging layer in the future.

______________________________________________________________________

# Practice Questions

## Conceptual

1. Why create a Producer wrapper?
1. Why use dependency injection?
1. Why use Pydantic?
1. Why separate serialization?
1. Why avoid hardcoded topics?
1. Why reuse Producer instances?

## Coding

1. Create a reusable Producer class.
1. Create a reusable Consumer class.
1. Implement JSON serialization.
1. Build a FastAPI endpoint that publishes events.
1. Load Kafka configuration from environment variables.

______________________________________________________________________

# Hands-on Exercise

Build the Order Service.

Requirements:

1. Create a reusable Kafka Producer.
1. Configure Kafka using `.env`.
1. Create an `OrderEvent` Pydantic model.
1. Publish order events through FastAPI.
1. Create a reusable Consumer.
1. Deserialize received messages.
1. Add logging.
1. Organize the project using the recommended folder structure.

______________________________________________________________________

# Summary

In this lecture, you learned:

- Production project structure
- Kafka configuration management
- Producer wrapper
- Consumer wrapper
- Pydantic models
- JSON serialization
- FastAPI dependency injection
- Logging
- Production best practices
- Interview patterns

______________________________________________________________________

## Next File

[4-kafka-python-fastapi-part-2.md](4-kafka-python-fastapi-part-2.md)

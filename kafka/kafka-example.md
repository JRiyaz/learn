# Kafka Python Producer and Consumer Examples

## Using kafka-python library

Install:

```bash
pip install kafka-python
```

______________________________________________________________________

# 1. Single Kafka Broker Example

Assume Kafka is running:

```
localhost:9092
```

Topic:

```
orders
```

______________________________________________________________________

# Create Topic

```bash
kafka-topics.sh \
--create \
--topic orders \
--bootstrap-server localhost:9092 \
--partitions 3 \
--replication-factor 1
```

______________________________________________________________________

# Producer Example

File:

```
producer.py
```

```python
from kafka import KafkaProducer
import json
import time


producer = KafkaProducer(

    bootstrap_servers=[
        "localhost:9092"
    ],


    key_serializer=lambda k:
        k.encode("utf-8"),


    value_serializer=lambda v:
        json.dumps(v).encode("utf-8"),


    # Wait for leader acknowledgement

    acks="all"

)



for i in range(1, 11):


    order_id = f"order-{i}"


    message = {


        "order_id": order_id,

        "status": "CREATED",

        "amount": i * 100

    }



    future = producer.send(

        topic="orders",

        key=order_id,

        value=message

    )


    metadata = future.get(timeout=10)


    print(
        f"""
        Message sent

        Topic:
        {metadata.topic}

        Partition:
        {metadata.partition}

        Offset:
        {metadata.offset}
        """
    )


    time.sleep(1)



producer.close()
```

______________________________________________________________________

# What Happens Here?

Example:

```
key = order-1
```

Kafka calculates:

```
hash(order-1) % number_of_partitions
```

Example:

```
hash(order-1)%3

= Partition 2
```

Message goes:

```
orders

Partition 2

Offset 0
```

______________________________________________________________________

# Consumer Example

File:

```
consumer.py
```

```python
from kafka import KafkaConsumer
import json



consumer = KafkaConsumer(


    "orders",


    bootstrap_servers=[
        "localhost:9092"
    ],



    group_id="order-service",



    key_deserializer=lambda k:
        k.decode("utf-8"),



    value_deserializer=lambda v:
        json.loads(
            v.decode("utf-8")
        ),



    auto_offset_reset="earliest",



    enable_auto_commit=False

)



print("Consumer started")



for message in consumer:


    print(
        f"""

        Key:

        {message.key}


        Value:

        {message.value}


        Partition:

        {message.partition}


        Offset:

        {message.offset}

        """
    )


    # process message here


    consumer.commit()
```

______________________________________________________________________

# Consumer Flow

```
Kafka


Partition 0

0
1
2


Consumer


Reads:

0

Processes


Commit:

offset=1
```

Kafka stores:

```
__consumer_offsets


group:

order-service


offset:

1

```

______________________________________________________________________

# 2. Delivery Callback Example

Kafka producer callback tells:

"Was the message successfully stored by Kafka?"

It does NOT mean:

"The consumer received it"

______________________________________________________________________

Example:

```python
from kafka import KafkaProducer


def delivery_callback(record_metadata):

    print(
        "Delivered"

    )



producer = KafkaProducer(

    bootstrap_servers=[
        "localhost:9092"
    ]

)



future = producer.send(

    "orders",

    value=b"hello"

)



future.add_callback(
    delivery_callback
)


future.add_errback(
    lambda exc:
    print(
        "Failed:",
        exc
    )
)


producer.flush()
```

Flow:

```
Producer

   |
   v

Kafka Leader

   |
   |
Callback called


Consumer may read later
```

______________________________________________________________________

# 3. Multiple Kafka Cluster Example

Example:

```
Cluster A


localhost:19092


Topic:

orders



Cluster B


localhost:29092


Topic:

payments

```

______________________________________________________________________

# Producer To Cluster A

File:

```
producer_cluster_a.py
```

```python
from kafka import KafkaProducer
import json



producer = KafkaProducer(


    bootstrap_servers=[

        "localhost:19092"

    ],



    key_serializer=lambda x:
        x.encode("utf-8"),



    value_serializer=lambda x:
        json.dumps(x).encode("utf-8")

)



producer.send(

    "orders",

    key="order-100",

    value={

        "id":100,

        "status":"CREATED"

    }

)



producer.flush()


producer.close()
```

______________________________________________________________________

# Consumer From Cluster A

```python
from kafka import KafkaConsumer
import json



consumer = KafkaConsumer(


    "orders",



    bootstrap_servers=[

        "localhost:19092"

    ],



    group_id="orders-service",



    auto_offset_reset="earliest",



    value_deserializer=lambda x:

        json.loads(
            x.decode("utf-8")
        )

)



for msg in consumer:


    print(msg.value)

```

______________________________________________________________________

# Producer To Cluster B

```python
from kafka import KafkaProducer
import json



producer = KafkaProducer(


    bootstrap_servers=[

        "localhost:29092"

    ],



    value_serializer=lambda x:

        json.dumps(x).encode()

)



producer.send(

    "payments",

    {

        "payment_id":123,

        "status":"SUCCESS"

    }

)



producer.flush()

producer.close()
```

______________________________________________________________________

# Consumer From Cluster B

```python
from kafka import KafkaConsumer
import json



consumer = KafkaConsumer(


    "payments",


    bootstrap_servers=[

        "localhost:29092"

    ],



    group_id="payment-service",



    auto_offset_reset="earliest",



    value_deserializer=lambda x:

        json.loads(
            x.decode()
        )

)



for message in consumer:


    print(

        message.value

    )
```

______________________________________________________________________

# 4. Multiple Brokers In Same Cluster

Usually configure:

```python
bootstrap_servers=[

    "broker1:9092",

    "broker2:9092",

    "broker3:9092"

]
```

Example:

```python
producer = KafkaProducer(

    bootstrap_servers=[

        "kafka1:9092",

        "kafka2:9092",

        "kafka3:9092"

    ]

)
```

Kafka discovers:

```
Broker 1

Broker 2

Broker 3


Partitions

Leaders

Replicas
```

______________________________________________________________________

# 5. Producer Configuration For Production

Recommended:

```python
producer = KafkaProducer(

    bootstrap_servers=[
        "broker1:9092",
        "broker2:9092",
        "broker3:9092"
    ],


    acks="all",


    retries=5,


    enable_idempotence=True,


    compression_type="gzip"

)
```

Meaning:

```
acks=all

Wait for replicas


retries

Retry failures


idempotence

Avoid duplicates


compression

Reduce network usage
```

______________________________________________________________________

# 6. Consumer Configuration For Production

```python
consumer = KafkaConsumer(


    "orders",


    bootstrap_servers=[

        "broker1:9092",

        "broker2:9092",

        "broker3:9092"

    ],


    group_id="order-service",


    enable_auto_commit=False,


    auto_offset_reset="earliest"

)
```

______________________________________________________________________

# Final Architecture

```
                 Python Producer


                       |
                       |
                       v


              Kafka Cluster A


        Broker1  Broker2  Broker3


                       |
                       |
                       v


              Consumer Group


        Consumer1 Consumer2 Consumer3


```

# Important Rules

1. Producer callback means:

```
Message stored in Kafka broker

NOT consumed
```

2. Offset belongs to:

```
Consumer Group
+
Topic
+
Partition
```

3. Multiple clusters are independent:

```
Cluster A != Cluster B
```

4. Same topic name can exist:

```
Cluster A

orders


Cluster B

orders

```

They are different topics.

5. Kafka discovers brokers using metadata:

```
bootstrap_servers

        |
        v

metadata request

        |
        v

all brokers discovered
```

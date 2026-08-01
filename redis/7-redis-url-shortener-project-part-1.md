# Redis URL Shortener Project - Part 1

## Project Overview

Congratulations on completing the Redis section!

Now it's time to build a **Redis-powered URL Shortener**.

This project is intentionally simple but realistic. It focuses on **learning Redis** while demonstrating how Redis is
commonly used in backend applications.

By the end of this project, you'll understand how Redis can be used for:

- Caching
- Key-Value Storage
- Expiration (TTL)
- Counters
- Hashes
- Sets
- Sorted Sets
- Connection Pooling

Unlike the final production project we'll build later, this project keeps everything inside a single application.

______________________________________________________________________

# What We'll Build

Users can:

- Create a short URL
- Open a short URL
- Count visits
- View analytics
- Cache frequently accessed URLs
- Automatically expire temporary URLs

______________________________________________________________________

# Technologies

- Python
- FastAPI
- Redis
- redis-py

______________________________________________________________________

# Features

### URL Management

- Shorten URL
- Redirect to Original URL
- Delete URL
- Temporary URLs

______________________________________________________________________

### Analytics

- Total Clicks
- Top URLs
- Last Access Time

______________________________________________________________________

### Performance

- Redis Cache
- Connection Pool
- TTL
- Fast Lookups

______________________________________________________________________

# Concepts Covered

| Redis Topic | Used |
| --------------- | ---- |
| Strings | ✅ |
| Hashes | ✅ |
| Sets | ✅ |
| Sorted Sets | ✅ |
| TTL | ✅ |
| Counters | ✅ |
| Pipelines | ✅ |
| Connection Pool | ✅ |
| Expiration | ✅ |
| redis-py | ✅ |

______________________________________________________________________

# Project Architecture

```text id="redisp001"
Client

↓

FastAPI

↓

Redis
```

Everything is stored inside Redis.

No PostgreSQL is required for this learning project.

______________________________________________________________________

# Suggested Folder Structure

Although all code is included in this Markdown document,

a real project could look like:

```text id="redisp002"
url_shortener/

app.py

redis_client.py

shortener.py

analytics.py

config.py
```

______________________________________________________________________

# Step 1 — Install Dependencies

```bash id="redisp003"
pip install fastapi

pip install uvicorn

pip install redis
```

______________________________________________________________________

# Step 2 — Redis Connection Pool

**redis_client.py**

```python id="redisp004"
import redis


pool = redis.ConnectionPool(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

client = redis.Redis(
    connection_pool=pool
)
```

Why use a connection pool?

Instead of opening a new TCP connection for every request, the application reuses existing connections, improving
performance and reducing overhead.

______________________________________________________________________

# Step 3 — FastAPI Application

**app.py**

```python id="redisp005"
from fastapi import FastAPI

app = FastAPI()
```

______________________________________________________________________

# Step 4 — Generate Short Codes

**shortener.py**

```python id="redisp006"
import random
import string


def generate_code(length=6):

    characters = (
        string.ascii_letters +
        string.digits
    )

    return "".join(
        random.choice(characters)
        for _ in range(length)
    )
```

Example

```text id="redisp007"
aB31Xd
```

______________________________________________________________________

# Step 5 — Store URL

Redis Strings

```python id="redisp008"
def save_url(
    code,
    original_url
):

    client.set(
        f"url:{code}",
        original_url
    )
```

Example

```text id="redisp009"
Key

url:aB31Xd

↓

Value

https://www.example.com
```

______________________________________________________________________

# Step 6 — Create Short URL

```python id="redisp010"
@app.post("/shorten")

def shorten_url(

    original_url: str

):

    code = generate_code()

    save_url(

        code,

        original_url

    )

    return {

        "short_code": code

    }
```

______________________________________________________________________

# Step 7 — Redirect

```python id="redisp011"
@app.get("/{code}")

def redirect(

    code: str

):

    url = client.get(

        f"url:{code}"

    )

    return {

        "original_url": url

    }
```

For simplicity, we return the original URL. In a production FastAPI application, you would typically return a redirect
response (for example, an HTTP 307 or 302).

______________________________________________________________________

# Step 8 — Delete URL

```python id="redisp012"
@app.delete("/{code}")

def delete_url(

    code: str

):

    client.delete(

        f"url:{code}"

    )

    return {

        "status": "deleted"

    }
```

______________________________________________________________________

# Temporary URLs

Suppose a URL should expire after one hour.

```python id="redisp013"
client.setex(

    "url:abc123",

    3600,

    "https://example.com"

)
```

After one hour,

Redis automatically removes the key.

______________________________________________________________________

# Checking TTL

```python id="redisp014"
client.ttl(

    "url:abc123"

)
```

Example Output

```text id="redisp015"
2480
```

Seconds remaining.

______________________________________________________________________

# Current Data

```text id="redisp016"
url:aB31Xd

↓

https://example.com
```

Redis stores everything in memory for very fast lookups.

______________________________________________________________________

# Testing

Request

```http id="redisp017"
POST /shorten
```

Body

```text id="redisp018"
https://www.python.org
```

Response

```json id="redisp019"
{
    "short_code": "Xp92Az"
}
```

Open

```http id="redisp020"
GET /Xp92Az
```

Response

```json id="redisp021"
{
    "original_url": "https://www.python.org"
}
```

______________________________________________________________________

# Common Mistakes

### Opening a New Redis Connection Per Request

Use a connection pool.

______________________________________________________________________

### Using Long Keys

Prefer concise, meaningful key names.

Example

```text id="redisp022"
url:abc123
```

instead of

```text id="redisp023"
this_is_my_url_key_for_the_shortener_application:abc123
```

______________________________________________________________________

### Never Expiring Temporary Data

Use TTL when data should automatically disappear.

______________________________________________________________________

### Ignoring Missing Keys

Always handle the case where `GET` returns `None`.

______________________________________________________________________

# Best Practices

- Reuse Redis connections.
- Keep keys short and consistent.
- Use prefixes (`url:`) to organize keys.
- Use TTL for temporary data.
- Keep values small when possible.
- Handle missing keys gracefully.

______________________________________________________________________

# Hands-on Exercise

1. Change the short code length to 8 characters.
1. Prevent duplicate short codes.
1. Add an endpoint to check the remaining TTL.
1. Add support for custom expiration times.
1. Return a proper HTTP redirect instead of JSON.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is Redis a good choice for a URL shortener?

Redis stores data in memory, making key lookups extremely fast—typically in constant time for string keys. A URL
shortener performs a large number of read operations, where each request maps a short code to its original URL. Redis
also provides built-in expiration (TTL), making it ideal for temporary links without requiring scheduled cleanup jobs.

______________________________________________________________________

# Summary

In this part, you built:

- Redis connection pool
- FastAPI application
- URL storage
- URL retrieval
- URL deletion
- Temporary URLs using TTL
- Basic URL shortener

In the next part, we'll add:

- Click counters
- Hashes
- Analytics
- Sorted Sets
- Top URLs
- Last access time

______________________________________________________________________

## Next File

[7-redis-url-shortener-project-part-2.md](7-redis-url-shortener-project-part-2.md)

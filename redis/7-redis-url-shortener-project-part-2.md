# Redis URL Shortener Project - Part 2

## Introduction

In Part 1, we built a basic URL shortener using Redis Strings.

Current flow:

```text id="redis201"
Client

↓

FastAPI

↓

Redis String

↓

Original URL
```

Now we'll make it much more useful by adding **analytics**.

We'll learn:

- Counters
- Hashes
- Sorted Sets
- Sets
- Multiple Redis data structures
- URL Analytics
- Top URLs
- Last Access Time

These are some of the most common Redis patterns used in real applications.

______________________________________________________________________

# Current Redis Keys

```text id="redis202"
url:abc123

↓

https://example.com
```

We'll now store much more information.

______________________________________________________________________

# New Redis Structure

Instead of one key,

we'll use multiple keys.

```text id="redis203"
url:abc123

url_meta:abc123

clicks:abc123

top_urls
```

Every key has one responsibility.

______________________________________________________________________

# Click Counter

Every redirect increments a counter.

```python id="redis204"
client.incr(

    f"clicks:{code}"

)
```

Suppose

```text id="redis205"
clicks:abc123

5
```

Next visit

↓

```text id="redis206"
clicks:abc123

6
```

Redis performs this increment atomically.

______________________________________________________________________

# Retrieve Click Count

```python id="redis207"
count = client.get(

    f"clicks:{code}"

)
```

Example

```text id="redis208"
18
```

______________________________________________________________________

# Update Redirect Endpoint

```python id="redis209"
@app.get("/{code}")

def redirect(

    code: str

):

    url = client.get(

        f"url:{code}"

    )

    if url is None:

        return {

            "error":"Not Found"

        }

    client.incr(

        f"clicks:{code}"

    )

    return {

        "original_url": url

    }
```

______________________________________________________________________

# Store Metadata

Instead of multiple string keys,

use a Redis Hash.

```python id="redis210"
client.hset(

    f"url_meta:{code}",

    mapping={

        "created_by":"Alice",

        "created_at":"2026-08-02",

        "category":"Tech"

    }

)
```

______________________________________________________________________

# Read Metadata

```python id="redis211"
metadata = client.hgetall(

    f"url_meta:{code}"

)
```

Example Output

```text id="redis212"
created_by

Alice

created_at

2026-08-02

category

Tech
```

______________________________________________________________________

# Why Use Hashes?

Instead of

```text id="redis213"
created_by:abc123

created_at:abc123

category:abc123
```

Store everything together.

Cleaner.

More efficient.

______________________________________________________________________

# Last Access Time

Every redirect updates

```python id="redis214"
from datetime import datetime

client.hset(

    f"url_meta:{code}",

    "last_access",

    datetime.utcnow().isoformat()

)
```

Now we know the most recent access time.

______________________________________________________________________

# Track Unique Visitors

Suppose every request includes a user ID.

Use a Redis Set.

```python id="redis215"
client.sadd(

    f"visitors:{code}",

    user_id

)
```

Duplicate IDs are ignored automatically.

______________________________________________________________________

# Count Unique Visitors

```python id="redis216"
unique_visitors = client.scard(

    f"visitors:{code}"

)
```

Example

```text id="redis217"
127
```

______________________________________________________________________

# Why Use Sets?

Suppose

User 10 visits

100 times.

The set still stores

```text id="redis218"
10
```

only once.

Perfect for unique visitor tracking.

______________________________________________________________________

# Top URLs

Use a Sorted Set.

```python id="redis219"
client.zincrby(

    "top_urls",

    1,

    code

)
```

Each visit increases the score.

______________________________________________________________________

# Retrieve Top URLs

```python id="redis220"
top = client.zrevrange(

    "top_urls",

    0,

    9,

    withscores=True

)
```

Example

```text id="redis221"
abc123

350

xyz987

280

mno456

190
```

______________________________________________________________________

# Analytics Function

```python id="redis222"
def get_analytics(

    code

):

    return {

        "url": client.get(

            f"url:{code}"

        ),

        "clicks": client.get(

            f"clicks:{code}"

        ),

        "metadata": client.hgetall(

            f"url_meta:{code}"

        ),

        "unique_visitors":

        client.scard(

            f"visitors:{code}"

        )

    }
```

______________________________________________________________________

# Analytics Endpoint

```python id="redis223"
@app.get("/analytics/{code}")

def analytics(

    code: str

):

    return get_analytics(

        code

    )
```

Example Response

```json id="redis224"
{
    "url": "https://python.org",
    "clicks": 18,
    "metadata": {
        "created_by": "Alice",
        "created_at": "2026-08-02",
        "last_access": "2026-08-03T10:20:30"
    },
    "unique_visitors": 12
}
```

______________________________________________________________________

# Redis Data Structures Used

```text id="redis225"
String

↓

Original URL

Hash

↓

Metadata

Set

↓

Unique Visitors

Sorted Set

↓

Top URLs

Counter

↓

Total Clicks
```

This project now demonstrates several core Redis data structures.

______________________________________________________________________

# Complete Flow

```text id="redis226"
Client

↓

Redirect

↓

Increment Counter

↓

Update Last Access

↓

Track Visitor

↓

Update Top URLs

↓

Return Original URL
```

______________________________________________________________________

# Common Mistakes

### Using Strings for Everything

Choose the Redis data structure that matches the problem.

______________________________________________________________________

### Counting Unique Visitors with a Counter

Counters measure total visits,

not unique users.

______________________________________________________________________

### Forgetting Sorted Sets

Sorted Sets are excellent for rankings and leaderboards.

______________________________________________________________________

### Not Updating Analytics

Every redirect should update analytics data.

______________________________________________________________________

# Best Practices

- Use Strings for simple values.
- Use Hashes for related fields.
- Use Sets for uniqueness.
- Use Sorted Sets for rankings.
- Keep key naming consistent.
- Design keys based on access patterns.

______________________________________________________________________

# Hands-on Exercise

1. Store browser information in metadata.
1. Track device type.
1. Count visits per day.
1. Create a "Top 20 URLs" endpoint.
1. Return the last five accessed URLs.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why use a Redis Sorted Set to track the most popular URLs instead of a normal Set?

A normal Set stores unique values without any ordering. A Sorted Set stores each member with an associated score and
automatically maintains the members in sorted order based on that score. By incrementing the score on each visit, Redis
can efficiently return the most popular URLs without requiring a separate sorting operation.

______________________________________________________________________

# Summary

In this chapter, you implemented:

- Click counters
- Hashes
- Metadata
- Last access time
- Unique visitors
- Sets
- Sorted Sets
- Top URLs
- Analytics API

The URL shortener now supports both URL management and basic analytics.

______________________________________________________________________

## Next File

[7-redis-url-shortener-project-part-3.md](7-redis-url-shortener-project-part-3.md)

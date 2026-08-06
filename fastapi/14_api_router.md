# APIRouter

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 3 - Routing
>
> **File:** `14_api_router.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What APIRouter is
- Why APIRouter is Needed
- Creating Routers
- Including Routers
- Route Prefixes
- Tags
- Dependencies
- Nested Routers
- Large Project Organization
- Production Best Practices

______________________________________________________________________

# What is APIRouter?

`APIRouter` is FastAPI's way of organizing routes into separate modules.

Instead of

```
main.py

↓

500 Routes
```

We organize routes by feature.

```
users.py

orders.py

products.py

payments.py
```

______________________________________________________________________

# Why Do We Need APIRouter?

Small projects

```
main.py

↓

20 Routes
```

Manageable.

Large projects

```
main.py

↓

1000+ Routes
```

Difficult to maintain.

______________________________________________________________________

# Without APIRouter

```
main.py

│

├── GET /users

├── POST /users

├── GET /orders

├── POST /orders

├── GET /products

├── DELETE /products

...

500 More Routes
```

Not scalable.

______________________________________________________________________

# With APIRouter

```
app/

│

├── routers/

│

│     users.py

│

│     orders.py

│

│     products.py

│

└── main.py
```

Each feature owns its own routes.

______________________________________________________________________

# Import APIRouter

```python
from fastapi import APIRouter
```

______________________________________________________________________

# Create a Router

```python
from fastapi import APIRouter

router = APIRouter()
```

`router` behaves similarly to a `FastAPI` application for defining endpoints.

______________________________________________________________________

# Add Routes

```python
@router.get("/")

def users():

    return [

        "Alice",

        "Bob"

    ]
```

Notice

```
router.get()

Not

app.get()
```

______________________________________________________________________

# Project Structure

```
app/

│

├── main.py

│

└── routers/

      users.py
```

______________________________________________________________________

# users.py

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")

def users():

    return [

        "Alice"

    ]
```

______________________________________________________________________

# main.py

```python
from fastapi import FastAPI

from routers.users import router

app = FastAPI()

app.include_router(

    router
)
```

The routes are now registered with the application.

______________________________________________________________________

# include_router()

```
FastAPI

↓

Include Router

↓

Routes Available
```

You can include multiple routers.

______________________________________________________________________

# Multiple Routers

```python
app.include_router(

    users_router

)

app.include_router(

    orders_router

)

app.include_router(

    products_router
)
```

Each router is independent.

______________________________________________________________________

# Route Prefix

Instead of

```python
@router.get("/users")
```

Create

```python
router = APIRouter(

    prefix="/users"
)
```

Then

```python
@router.get("/")
```

Final URL

```
/users/
```

______________________________________________________________________

# Prefix Example

Users Router

```python
prefix="/users"
```

Routes

```python
"/"

"/{id}"

"/search"
```

Generated URLs

```
/users/

/users/{id}

/users/search
```

No duplication.

______________________________________________________________________

# Tags

```python
router = APIRouter(

    prefix="/users",

    tags=["Users"]
)
```

Swagger groups endpoints.

```
Users

↓

GET

POST

PUT

DELETE
```

______________________________________________________________________

# Dependencies

Dependencies can be applied to every route in a router.

```python
router = APIRouter(

    dependencies=[

        Depends(

            get_current_user

        )

    ]
)
```

Every endpoint now requires authentication.

______________________________________________________________________

# Router-Level Dependencies

Without

```
Route 1

Depends()

Route 2

Depends()

Route 3

Depends()
```

With

```
Router

↓

Depends()

↓

All Routes Protected
```

Cleaner and easier to maintain.

______________________________________________________________________

# Response Configuration

Router-level defaults

```python
router = APIRouter(

    responses={

        404: {

            "description":

            "Not Found"

        }

    }
)
```

Common responses can be shared.

______________________________________________________________________

# Nested Structure

Example

```
api/

↓

v1/

↓

users.py

orders.py

products.py
```

Organized by API version.

______________________________________________________________________

# Typical Enterprise Layout

```
app/

│

├── api/

│

│     v1/

│

│        users.py

│

│        products.py

│

│        auth.py

│

│        orders.py

│

├── services/

├── repositories/

├── models/

├── schemas/

└── main.py
```

______________________________________________________________________

# Flow

```
Request

↓

FastAPI

↓

Router

↓

Route

↓

Service

↓

Repository

↓

Database
```

The router only handles HTTP concerns.

______________________________________________________________________

# Routers and Services

Bad

```
Router

↓

Business Logic
```

Good

```
Router

↓

Service

↓

Repository
```

Routes should stay thin.

______________________________________________________________________

# Router Responsibilities

A router should

- Receive Requests
- Validate Input
- Call Services
- Return Responses

It should **not**

- Query the database directly
- Contain business rules
- Manage transactions

______________________________________________________________________

# Versioning

Example

```
/api/v1/users

/api/v2/users
```

Using prefixes

```python
prefix="/api/v1/users"
```

Versioning becomes simple.

______________________________________________________________________

# Swagger Organization

Without tags

```
100 Endpoints

↓

Mixed Together
```

With tags

```
Authentication

Users

Orders

Products
```

Much easier to navigate.

______________________________________________________________________

# Common Mistakes

❌ Putting every route in `main.py`

❌ Writing business logic inside routers

❌ Forgetting route prefixes

❌ Repeating authentication dependencies on every endpoint

❌ Mixing unrelated routes in one router

______________________________________________________________________

# Production Best Practices

- Organize routes by feature.
- Use one router per domain.
- Use route prefixes.
- Use tags for documentation.
- Keep routers thin.
- Apply shared dependencies at the router level.
- Keep business logic in services.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should large FastAPI applications use APIRouter instead of placing every endpoint in `main.py`?**

### Answer

`APIRouter` improves modularity and maintainability.

Benefits include:

- Separation of concerns.
- Better project organization.
- Easier collaboration among developers.
- Cleaner API versioning.
- Reusable router-level dependencies.
- Better Swagger documentation through tags.

As applications grow, routers help organize endpoints by feature rather than placing everything in a single file.

______________________________________________________________________

# Summary

In this chapter you learned:

- APIRouter
- include_router()
- Route Prefixes
- Tags
- Router Dependencies
- Router Organization
- API Versioning
- Enterprise Project Structure
- Production Best Practices

`APIRouter` is the foundation for organizing medium and large FastAPI applications into clean, maintainable,
feature-based modules.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is `APIRouter`?
1. Why is `APIRouter` needed?
1. What does `include_router()` do?

______________________________________________________________________

## Organization

4. Why should routes be split into multiple routers?
1. What is the purpose of route prefixes?
1. Why are tags useful?

______________________________________________________________________

## Dependencies

7. Why apply dependencies at the router level?
1. What kinds of dependencies are commonly shared across routers?

______________________________________________________________________

## Architecture

9. What responsibilities should routers have?
1. Why shouldn't routers contain business logic?
1. How should routers interact with services and repositories?

______________________________________________________________________

## Versioning

12. How can API versioning be implemented using routers?
01. Why is feature-based organization preferred over a single large route file?

______________________________________________________________________

## Scenario-Based

14. Your `main.py` contains 800 API endpoints. How would you reorganize the project?
01. Every endpoint in your `users` module requires authentication. How can router-level dependencies reduce duplicated code?
01. Your Swagger documentation contains hundreds of endpoints in one unorganized list. How can `tags` improve the developer experience?
01. A teammate performs SQL queries directly inside router functions. Why is this considered poor architecture?
01. Your application needs both `/api/v1/users` and `/api/v2/users` during a migration. How can `APIRouter` help manage both versions?
01. Your team has separate backend engineers working on authentication, orders, and payments. How does `APIRouter` improve collaboration?
01. Your application grows from 10 endpoints to over 1,000 endpoints. Why does modular routing become increasingly important?

______________________________________________________________________

# Next

[API Versioning](15_api_versioning.md)

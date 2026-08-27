# 14. FastAPI Fundamentals

**Previous:** [13. Complete Backend Request Lifecycle](./13-request-lifecycle.md)

**Next:** [15. FastAPI Dependency Injection, Middleware & Errors](./15-fastapi-di-middleware-errors.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain FastAPI's architecture and how it fits into ASGI.
- Define and organize API routes.
- Use path parameters, query parameters and request bodies.
- Explain Pydantic's role in FastAPI.
- Understand request validation.
- Define response models.
- Explain serialization and response validation.
- Organize endpoints using routers.
- Understand OpenAPI generation.
- Use automatically generated API documentation.
- Explain practical API versioning strategies.
- Read headers and cookies.
- Handle form data.
- Handle file uploads.
- Explain common FastAPI interview questions and production considerations.

______________________________________________________________________

# 1. What Is FastAPI?

FastAPI is a modern Python web framework for building APIs.

It is built around:

- Python type hints
- ASGI
- Pydantic-based data validation/modeling
- Automatic OpenAPI schema generation

A simplified architecture is:

```text
Client
   ↓
ASGI Server
   ↓
FastAPI
   ↓
Router
   ↓
Endpoint
   ↓
Business Logic
```

FastAPI is the application framework; the ASGI server runs the application.

______________________________________________________________________

# 2. FastAPI and ASGI

FastAPI is an ASGI application.

A common deployment looks like:

```text
Nginx / Load Balancer
        ↓
Uvicorn
        ↓
FastAPI
```

The ASGI server handles the server-side protocol integration and invokes the FastAPI application.

This separation is important:

- **FastAPI** → framework/application behavior
- **Uvicorn** → ASGI server
- **Nginx/load balancer** → infrastructure/proxy responsibilities

______________________________________________________________________

# 3. Minimal FastAPI Application

A minimal application:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

The application exposes an ASGI-compatible interface.

______________________________________________________________________

# 4. Routing

Routing determines which endpoint handles an incoming request.

Example:

```python
@app.get("/users")
async def list_users():
    return []
```

The route combines:

```text
HTTP method + path
```

So:

```text
GET /users
```

matches the endpoint above.

______________________________________________________________________

# 5. HTTP Method Decorators

FastAPI provides decorators such as:

```python
@app.get(...)
@app.post(...)
@app.put(...)
@app.patch(...)
@app.delete(...)
@app.options(...)
@app.head(...)
```

Example:

```python
@app.post("/users")
async def create_user():
    ...
```

The HTTP method is part of the route definition.

______________________________________________________________________

# 6. Path Parameters

Path parameters are variables embedded in the URL.

Example:

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id}
```

Request:

```http
GET /users/42
```

FastAPI extracts:

```python
user_id = 42
```

and validates it according to the declared type.

______________________________________________________________________

# 7. Path Parameter Validation

Given:

```python
user_id: int
```

the framework expects an integer.

A request such as:

```http
GET /users/abc
```

does not satisfy the declared input type and results in a validation error response.

The important principle is:

> Validate input at the API boundary before business logic depends on it.

______________________________________________________________________

# 8. Query Parameters

Query parameters appear after `?`.

Example:

```http
GET /users?page=2&limit=20
```

FastAPI can define them directly:

```python
@app.get("/users")
async def list_users(
    page: int = 1,
    limit: int = 20,
):
    ...
```

The framework parses and validates the values.

______________________________________________________________________

# 9. Required vs Optional Query Parameters

A query parameter without a default is generally required.

```python
async def search(q: str):
    ...
```

while:

```python
async def search(q: str | None = None):
    ...
```

allows the parameter to be omitted.

The exact typing syntax depends on the project's Python version.

______________________________________________________________________

# 10. Query Parameter Constraints

FastAPI can express additional validation constraints.

For example, you may want:

```text
limit >= 1
limit <= 100
```

The endpoint can declare these constraints using FastAPI's parameter utilities.

The benefit is that API requirements become explicit at the boundary.

______________________________________________________________________

# 11. Request Bodies

Request bodies are commonly used for POST, PUT and PATCH operations.

Example:

```python
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
```

Then:

```python
@app.post("/users")
async def create_user(user: UserCreate):
    return user
```

FastAPI can parse the incoming JSON and validate it against the model.

______________________________________________________________________

# 12. Pydantic

Pydantic is used extensively with FastAPI for data modeling and validation.

Example:

```python
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
```

The model describes the expected data structure.

It can validate incoming data and provide a structured Python representation to application code.

______________________________________________________________________

# 13. Nested Pydantic Models

Models can contain other models.

Example:

```python
class Address(BaseModel):
    city: str
    country: str


class UserCreate(BaseModel):
    name: str
    address: Address
```

This is useful for structured API payloads.

______________________________________________________________________

# 14. Pydantic Field Constraints

Models can define validation constraints.

For example:

```python
from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str
    price: float = Field(gt=0)
```

This expresses a domain/input constraint at the model boundary.

______________________________________________________________________

# 15. Validation Flow

A simplified FastAPI request flow is:

```text
HTTP Request
    ↓
Route matching
    ↓
Parameter/body parsing
    ↓
Pydantic/FastAPI validation
    ↓
Endpoint
```

If validation fails, the endpoint does not proceed normally.

The client receives a validation error response.

______________________________________________________________________

# 16. Validation vs Business Rules

Not every rule belongs in request validation.

Example:

```text
email must be a valid email format
```

is a good boundary-validation rule.

But:

```text
user cannot place an order because their account is suspended
```

is a business rule.

A useful separation is:

```text
Input shape/type
      ↓
API validation

Business meaning/rules
      ↓
Service/domain logic
```

______________________________________________________________________

# 17. Response Models

FastAPI allows an endpoint to define a response model.

Example:

```python
class UserResponse(BaseModel):
    id: int
    name: str


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    ...
```

This defines the intended response contract.

______________________________________________________________________

# 18. Why Response Models Matter

Suppose an internal object contains:

```text
id
name
email
password_hash
internal_notes
```

The API should not accidentally expose everything.

A response model can define:

```text
id
name
email
```

and keep internal fields out of the public response.

Response models also make the API contract explicit.

______________________________________________________________________

# 19. Serialization

Serialization converts Python/application data into a representation suitable for the HTTP response.

For example:

```python
{
    "id": 42,
    "name": "Riyaz",
}
```

can be encoded as JSON:

```json
{
    "id": 42,
    "name": "Riyaz"
}
```

FastAPI works with Pydantic models and response handling to produce API responses.

______________________________________________________________________

# 20. Response Validation

When a response model is declared, FastAPI/Pydantic can validate the returned data against the expected response schema.

This can expose programming errors where the endpoint returns data that does not match its public contract.

For example:

```python
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    return {
        "id": user_id,
        "name": "Riyaz",
        # response fields must match the declared model
    }
```

The response model therefore acts as a contract, not just documentation.

______________________________________________________________________

# 21. Routers

As an application grows, putting every route in one file becomes difficult to maintain.

FastAPI provides `APIRouter`.

Example:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(user_id: int):
    ...
```

Then register it:

```python
app.include_router(router)
```

______________________________________________________________________

# 22. Why Use Routers?

Routers help organize endpoints by responsibility.

For example:

```text
routers/
├── users.py
├── orders.py
├── payments.py
└── health.py
```

This improves:

- Maintainability
- Separation of concerns
- Team ownership
- API organization

______________________________________________________________________

# 23. Router Prefixes and Tags

A router can define:

```python
router = APIRouter(
    prefix="/users",
    tags=["users"],
)
```

Then:

```python
@router.get("/{user_id}")
```

produces:

```text
GET /users/{user_id}
```

Tags also help organize generated API documentation.

______________________________________________________________________

# 24. OpenAPI

FastAPI automatically generates an OpenAPI schema.

The schema describes the API, including information such as:

- Routes
- Methods
- Parameters
- Request bodies
- Response schemas
- Validation constraints

This can be used by tools to understand the API contract.

______________________________________________________________________

# 25. API Documentation

FastAPI commonly exposes interactive documentation based on the generated OpenAPI schema.

Typical endpoints are:

```text
/docs
/redoc
```

The exact availability can be configured.

The documentation is generated from the application's route and model definitions.

______________________________________________________________________

# 26. Why OpenAPI Matters

OpenAPI can be used for:

- API discovery
- Frontend/backend collaboration
- Client generation
- Contract review
- Testing
- Documentation

It helps make the API contract machine-readable.

______________________________________________________________________

# 27. API Versioning

APIs evolve.

A common approach is URL versioning:

```text
/api/v1/users
/api/v2/users
```

Routers can make this easy:

```python
v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")
```

______________________________________________________________________

# 28. Versioning Strategies

Common approaches include:

### URL versioning

```text
/api/v1/users
```

### Header-based versioning

```text
API-Version: 2
```

### Media-type versioning

For example, using an `Accept` media type to identify a version.

There is no universally correct strategy.

Choose one that is consistent, documented and compatible with your clients/infrastructure.

______________________________________________________________________

# 29. API Versioning Principles

Do not create a new version for every tiny change.

Consider a new API version when making breaking changes such as:

- Removing fields
- Changing field meanings
- Changing response structure incompatibly
- Changing required request fields
- Changing semantics

Backward-compatible additions may not require a new major API version.

______________________________________________________________________

# 30. Headers

FastAPI can access HTTP headers.

Example:

```python
from fastapi import Header


@app.get("/items")
async def get_items(x_request_id: str | None = Header(default=None)):
    return {"request_id": x_request_id}
```

FastAPI maps the parameter to the corresponding HTTP header.

______________________________________________________________________

# 31. Header Naming

HTTP headers commonly use hyphenated names:

```text
X-Request-ID
```

Python identifiers cannot naturally contain hyphens, so FastAPI's parameter/header handling can map Python names such
as:

```python
x_request_id
```

to:

```text
X-Request-ID
```

depending on configuration and alias behavior.

______________________________________________________________________

# 32. Cookies

FastAPI provides a `Cookie` dependency helper.

Example:

```python
from fastapi import Cookie


@app.get("/profile")
async def profile(session_id: str | None = Cookie(default=None)):
    ...
```

The application can read a cookie from the incoming request.

For setting cookies, use the response object:

```python
from fastapi import Response


@app.post("/login")
async def login(response: Response):
    response.set_cookie(
        key="session_id",
        value="abc123",
        httponly=True,
        secure=True,
    )
    return {"ok": True}
```

Production cookie configuration should also consider `SameSite`, expiration and scope.

______________________________________________________________________

# 33. Forms

Form data can be accepted using FastAPI's form support.

Example:

```python
from fastapi import Form


@app.post("/login")
async def login(
    username: str = Form(),
    password: str = Form(),
):
    ...
```

This is different from a JSON request body.

A common content type is:

```text
application/x-www-form-urlencoded
```

Multipart form data is used when files are also involved.

______________________________________________________________________

# 34. File Uploads

FastAPI can handle uploaded files using `UploadFile`.

Example:

```python
from fastapi import File, UploadFile


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
    }
```

`UploadFile` is preferable for many uploads because it provides a file-like interface and is designed for uploaded file
handling.

______________________________________________________________________

# 35. File Upload Security

Never assume an uploaded file is safe just because the filename or content type looks correct.

Consider:

- File size limits
- Extension validation
- Content validation
- Malware scanning where appropriate
- Storage isolation
- Randomized storage names
- Access control
- Avoiding executable upload locations

File uploads are an application security boundary.

______________________________________________________________________

# 36. JSON vs Form vs Multipart

| Input | Typical use |
|---|---|
| JSON | Structured API payload |
| Form URL-encoded | Simple form fields |
| Multipart form-data | Form fields + files |
| File upload | Binary/file content |

Choose the format based on the client and data being submitted.

______________________________________________________________________

# 37. Request Body vs Query Parameters

Use a query parameter for filtering or controlling retrieval.

Example:

```http
GET /users?status=active&limit=20
```

Use a request body for structured data being submitted.

Example:

```http
POST /users
Content-Type: application/json
```

```json
{
    "name": "Riyaz",
    "email": "user@example.com"
}
```

______________________________________________________________________

# 38. Dependency on Python Type Hints

One of FastAPI's key design features is that Python type annotations participate in API definition.

For example:

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    ...
```

The annotation contributes to:

- Input parsing
- Validation
- OpenAPI schema
- Editor/type-checking information

This reduces duplication between code and API documentation.

______________________________________________________________________

# 39. FastAPI Application Structure

A practical project may look like:

```text
app/
├── main.py
├── routers/
│   ├── users.py
│   └── orders.py
├── schemas/
│   ├── users.py
│   └── orders.py
├── services/
├── repositories/
└── models/
```

The exact structure depends on project size and architecture.

Do not introduce folders purely for the sake of following a template.

______________________________________________________________________

# 40. Route Handler Responsibilities

A route handler should ideally focus on HTTP concerns.

For example:

```python
@app.post("/users")
async def create_user(user: UserCreate):
    return await user_service.create(user)
```

The service can contain business rules.

The repository can handle persistence.

This separation becomes especially useful as applications grow.

______________________________________________________________________

# 41. Response Status Codes

FastAPI allows explicit response status codes.

Example:

```python
from fastapi import status


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: UserCreate):
    ...
```

Choosing an appropriate status code communicates the result clearly to clients.

______________________________________________________________________

# 42. Custom Responses

FastAPI supports response configuration for cases such as:

- Custom status codes
- Custom headers
- Cookies
- Streaming
- Different response formats

Use custom response behavior when the API contract requires it rather than adding complexity unnecessarily.

______________________________________________________________________

# 43. API Documentation as a Contract

Generated documentation should be treated as part of the API contract.

Good APIs make clear:

- Request format
- Response format
- Status codes
- Authentication requirements
- Validation behavior
- Error structure
- Versioning

An API should not rely on developers reverse-engineering endpoint behavior from implementation code.

______________________________________________________________________

# 44. Common FastAPI Mistakes

## Mistake 1 — Putting business logic directly in every route

Large route handlers become difficult to test and maintain.

______________________________________________________________________

## Mistake 2 — Returning internal database models directly

This can accidentally expose fields that should remain private.

Use explicit response models where appropriate.

______________________________________________________________________

## Mistake 3 — Treating type hints as complete runtime validation

Type annotations help FastAPI define/validate API inputs, but Python annotations themselves are not general runtime
enforcement.

______________________________________________________________________

## Mistake 4 — Blocking inside async endpoints

A synchronous blocking library can block the event loop.

______________________________________________________________________

## Mistake 5 — Ignoring request size/file limits

Large request bodies and uploads can consume significant resources.

______________________________________________________________________

## Mistake 6 — Versioning every change

Not every backward-compatible change requires a new API version.

______________________________________________________________________

## Mistake 7 — Mixing API concerns and persistence concerns

A route should not become a giant database/business-logic function.

______________________________________________________________________

# 45. Interview Questions & Answers

## Q1. What is FastAPI?

**Answer:**

FastAPI is a Python web framework for building APIs. It uses type hints, Pydantic-based modeling/validation and ASGI to
support modern API development.

______________________________________________________________________

## Q2. Is FastAPI an ASGI server?

**Answer:**

No.

FastAPI is an ASGI application/framework.

An ASGI server such as Uvicorn runs the application.

______________________________________________________________________

## Q3. FastAPI vs Uvicorn?

**Answer:**

FastAPI provides application and routing behavior.

Uvicorn is an ASGI server responsible for running the application and handling the server-side protocol integration.

______________________________________________________________________

## Q4. How does FastAPI use Python type hints?

**Answer:**

Type annotations help FastAPI understand parameters, validate request data, generate OpenAPI schemas and provide a clear
API contract.

______________________________________________________________________

## Q5. What are path parameters?

**Answer:**

Variables embedded in the URL path.

Example:

```text
/users/{user_id}
```

FastAPI extracts and validates the value according to the endpoint annotation.

______________________________________________________________________

## Q6. What are query parameters?

**Answer:**

Parameters supplied after `?` in the URL.

Example:

```text
/users?page=2
```

FastAPI can parse and validate them from endpoint parameters.

______________________________________________________________________

## Q7. How do you define a request body?

**Answer:**

Typically with a Pydantic model:

```python
class UserCreate(BaseModel):
    name: str
    email: str
```

and use it as an endpoint parameter.

______________________________________________________________________

## Q8. What is Pydantic used for?

**Answer:**

It provides data models and validation used extensively by FastAPI for request and response data.

______________________________________________________________________

## Q9. What is a response model?

**Answer:**

A response model defines the expected API response schema and can validate/filter the returned data according to the
public contract.

______________________________________________________________________

## Q10. Why use response models?

**Answer:**

They make the response contract explicit, improve documentation and help prevent accidental exposure of internal fields.

______________________________________________________________________

## Q11. What is serialization?

**Answer:**

Serialization converts application data into a representation suitable for transmission, such as JSON.

______________________________________________________________________

## Q12. What is an `APIRouter`?

**Answer:**

`APIRouter` organizes related routes into modular groups that can be included in the main FastAPI application.

______________________________________________________________________

## Q13. Why use routers?

**Answer:**

They improve organization, maintainability, separation of concerns and team ownership in larger APIs.

______________________________________________________________________

## Q14. What is OpenAPI?

**Answer:**

OpenAPI is a machine-readable specification format for describing HTTP APIs, including endpoints, parameters, request
bodies and response schemas.

______________________________________________________________________

## Q15. How does FastAPI generate API documentation?

**Answer:**

FastAPI generates an OpenAPI schema from route definitions, type annotations and models.

Interactive documentation can then be exposed through tools such as Swagger UI and ReDoc.

______________________________________________________________________

## Q16. What are `/docs` and `/redoc`?

**Answer:**

They are commonly used endpoints for interactive API documentation generated from the OpenAPI schema.

______________________________________________________________________

## Q17. How would you version a FastAPI API?

**Answer:**

A common approach is router prefixes such as:

```text
/api/v1
/api/v2
```

Other strategies include headers or media types.

The key is consistency and deliberate handling of breaking changes.

______________________________________________________________________

## Q18. When should you create a new API version?

**Answer:**

Usually for breaking changes, such as incompatible response changes, removing fields or changing required request
semantics.

Backward-compatible additions generally do not require a new major version.

______________________________________________________________________

## Q19. How do you access a request header?

**Answer:**

Use FastAPI's `Header` helper or access the request object when appropriate.

______________________________________________________________________

## Q20. How do you access cookies?

**Answer:**

Use FastAPI's `Cookie` helper or the request object.

______________________________________________________________________

## Q21. How do you set a cookie?

**Answer:**

Use the response object:

```python
response.set_cookie(...)
```

and configure security attributes such as `HttpOnly`, `Secure` and appropriate `SameSite` behavior.

______________________________________________________________________

## Q22. How do you handle form data?

**Answer:**

Use FastAPI's `Form` helper.

Form encoding differs from a JSON request body.

______________________________________________________________________

## Q23. How do you handle file uploads?

**Answer:**

Use `UploadFile` with `File`.

For example:

```python
async def upload(file: UploadFile = File(...)):
    ...
```

______________________________________________________________________

## Q24. Why use `UploadFile`?

**Answer:**

It provides a file-like interface and is designed for efficient handling of uploaded files compared with loading every
upload directly into memory as a plain bytes value.

______________________________________________________________________

## Q25. What is the difference between JSON and multipart form data?

**Answer:**

JSON is suitable for structured JSON payloads.

Multipart form data is commonly used when a request contains files and form fields.

______________________________________________________________________

## Q26. Where should validation happen?

**Answer:**

Basic input shape/type validation should happen at the API boundary.

Business rules should remain in the appropriate service/domain layer.

______________________________________________________________________

## Q27. Does FastAPI validate everything automatically?

**Answer:**

FastAPI validates data according to the declared route parameters and models.

It does not know arbitrary business rules unless those rules are explicitly implemented.

______________________________________________________________________

## Q28. Can FastAPI response models prevent data leakage?

**Answer:**

They can help by defining the fields that belong in the public response and filtering/validating returned data according
to that contract.

They should be part of a broader security design.

______________________________________________________________________

## Q29. What happens when a path parameter has the wrong type?

**Answer:**

FastAPI's validation layer rejects the request before normal endpoint processing.

The client receives a validation error response.

______________________________________________________________________

## Q30. What is the difference between a query parameter and a path parameter?

**Answer:**

A path parameter identifies a resource as part of the URL path.

A query parameter commonly controls filtering, pagination, searching or other optional request behavior.

______________________________________________________________________

## Q31. What is the role of response serialization?

**Answer:**

It converts the endpoint's result into the representation sent over HTTP, commonly JSON, while applying the response
contract where configured.

______________________________________________________________________

## Q32. Why shouldn't every endpoint contain database code?

**Answer:**

It mixes HTTP, business and persistence responsibilities.

Separating route, service and repository responsibilities generally improves maintainability and testability.

______________________________________________________________________

## Q33. What is a common mistake with async FastAPI endpoints?

**Answer:**

Using blocking synchronous operations inside `async def` endpoints.

This can block the event loop and reduce concurrency.

______________________________________________________________________

## Q34. How would you structure a large FastAPI application?

**Answer:**

A common structure is:

```text
Routers
  ↓
Services
  ↓
Repositories
  ↓
Database
```

with schemas/models separated appropriately.

The exact structure should match the application's complexity.

______________________________________________________________________

# 46. Scenario-Based Questions

## Scenario 1 — Invalid Path Parameter

You define:

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    ...
```

A client sends:

```text
GET /users/abc
```

**Question:** What happens?

**Answer:**

FastAPI validates the path parameter and rejects the request because `"abc"` cannot satisfy the declared integer type.

The endpoint's normal business logic does not execute.

______________________________________________________________________

## Scenario 2 — Internal Model Leakage

Your database user object contains:

```text
id
name
email
password_hash
internal_notes
```

The endpoint returns the database object directly.

**Question:** What risk exists?

**Answer:**

Internal fields may accidentally become part of the API response.

Define an explicit response model containing only the fields intended for clients.

______________________________________________________________________

## Scenario 3 — Huge Route Handler

An endpoint contains:

```text
HTTP parsing
authentication
business rules
database queries
email sending
serialization
```

in one 300-line function.

**Question:** How would you improve it?

**Answer:**

Separate concerns:

```text
Router
 ↓
Authentication/dependencies
 ↓
Service
 ↓
Repository
 ↓
External integrations
```

Keep the route handler focused on API concerns.

______________________________________________________________________

## Scenario 4 — API Versioning

You need to change:

```json
{
    "name": "Riyaz"
}
```

to a completely incompatible structure.

**Question:** Would you create a new version?

**Answer:**

If existing clients cannot consume the new response/request contract, treat it as a breaking change and consider a new
API version.

______________________________________________________________________

## Scenario 5 — Blocking Dependency

An async endpoint calls:

```python
requests.get(...)
```

**Question:** What is the problem?

**Answer:**

The synchronous HTTP call can block the event loop.

Use an async-compatible HTTP client or isolate the blocking operation appropriately.

______________________________________________________________________

## Scenario 6 — File Upload

Users can upload arbitrary files.

**Question:** What should you consider?

**Answer:**

At minimum:

- Size limits
- File/content validation
- Storage isolation
- Safe filenames/storage keys
- Malware scanning where appropriate
- Access control
- Preventing executable file exposure

______________________________________________________________________

## Scenario 7 — Query vs Body

You need:

```text
GET /products?category=books&limit=20
```

and:

```text
POST /products
```

with:

```json
{
    "name": "Book",
    "price": 20
}
```

**Question:** Why use query parameters in the first and a body in the second?

**Answer:**

The GET query parameters control retrieval/filtering.

The POST body contains structured data being submitted to create a resource.

______________________________________________________________________

## Scenario 8 — Response Validation Failure

An endpoint declares:

```python
response_model=UserResponse
```

but accidentally returns:

```python
{
    "id": "not-an-int",
    ...
}
```

**Question:** Why is this useful during development?

**Answer:**

The response contract can expose an application bug instead of silently returning data that violates the documented API
schema.

______________________________________________________________________

## Scenario 9 — Large Uploads

A service accepts multiple 500 MB uploads concurrently.

**Question:** What concerns arise?

**Answer:**

Potential problems include:

- Memory/resource pressure
- Disk pressure
- Network bandwidth
- Request timeouts
- Worker capacity
- Storage limits

Uploads should have explicit resource limits and an appropriate storage/processing architecture.

______________________________________________________________________

## Scenario 10 — OpenAPI Drift

Developers manually maintain API documentation separately from endpoint code.

Over time, the documentation becomes incorrect.

**Question:** How can FastAPI help?

**Answer:**

FastAPI can generate OpenAPI documentation from route definitions, type annotations and Pydantic models, reducing
duplication between implementation and API schema.

______________________________________________________________________

# 47. Practice Exercises

## Exercise 1 — Basic API

Create:

```text
GET    /users
GET    /users/{id}
POST   /users
PATCH  /users/{id}
DELETE /users/{id}
```

Use appropriate request and response models.

______________________________________________________________________

## Exercise 2 — Validation

Create a request model containing:

```text
name
email
age
```

Add meaningful validation constraints.

Test:

- Valid input
- Missing fields
- Invalid types
- Boundary values

______________________________________________________________________

## Exercise 3 — Routers

Split the API into:

```text
users.py
orders.py
```

Use `APIRouter` and include both routers in the main application.

______________________________________________________________________

## Exercise 4 — Response Models

Create an internal user object containing:

```text
id
name
email
password_hash
internal_notes
```

Return only:

```text
id
name
email
```

using a response model.

______________________________________________________________________

## Exercise 5 — OpenAPI

Inspect the generated OpenAPI schema.

Identify where it describes:

- Routes
- Parameters
- Request bodies
- Response models
- Validation constraints

______________________________________________________________________

## Exercise 6 — API Versioning

Implement:

```text
/api/v1/users
/api/v2/users
```

with intentionally different response contracts.

Explain how you would migrate clients.

______________________________________________________________________

## Exercise 7 — Headers and Cookies

Implement an endpoint that:

- Reads a request ID header.
- Reads a session cookie.
- Sets a secure session cookie on login.

Explain the security attributes.

______________________________________________________________________

## Exercise 8 — Forms

Create a form-based login endpoint.

Test:

- Valid credentials
- Missing fields
- Invalid credentials

______________________________________________________________________

## Exercise 9 — File Upload

Create an upload endpoint using `UploadFile`.

Add:

- File-size protection
- Extension/content checks
- Safe storage naming

Explain what additional production protections you would add.

______________________________________________________________________

## Exercise 10 — Architecture Review

Take one large FastAPI route from a project.

Refactor it conceptually into:

```text
Router
 ↓
Service
 ↓
Repository
 ↓
Database
```

Identify which responsibilities belong in each layer.

______________________________________________________________________

# 48. Quick Revision

| Concept | Key Point |
|---|---|
| FastAPI | Python API framework |
| ASGI | Async Python application interface |
| Uvicorn | ASGI server |
| Routing | Maps method + path to handler |
| Path parameter | Variable in URL path |
| Query parameter | Data after `?` |
| Request body | Structured submitted data |
| Pydantic | Data modeling/validation |
| Validation | Checks declared input requirements |
| Response model | Public response contract |
| Serialization | Converts data to response representation |
| `APIRouter` | Modular route organization |
| OpenAPI | Machine-readable API specification |
| `/docs` | Interactive API docs |
| `/redoc` | ReDoc API docs |
| Versioning | Managing API evolution |
| Header | HTTP metadata |
| Cookie | Browser-associated request data |
| Session | State associated with a client/session |
| Form | Form-encoded request data |
| `UploadFile` | File-upload abstraction |
| JSON | Structured API payload |
| Multipart | Form fields + files |
| Blocking code | Can block async event loop |
| Service layer | Business logic |
| Repository | Persistence access |

______________________________________________________________________

# 49. Completion Checklist

Before moving to File 15, make sure you can explain:

- [ ] FastAPI architecture
- [ ] FastAPI vs ASGI server
- [ ] ASGI
- [ ] Minimal FastAPI application
- [ ] Routing
- [ ] HTTP method decorators
- [ ] Path parameters
- [ ] Path parameter validation
- [ ] Query parameters
- [ ] Required vs optional parameters
- [ ] Query constraints
- [ ] Request bodies
- [ ] Pydantic
- [ ] Nested Pydantic models
- [ ] Pydantic field constraints
- [ ] Validation flow
- [ ] Validation vs business rules
- [ ] Response models
- [ ] Response model security benefits
- [ ] Serialization
- [ ] Response validation
- [ ] `APIRouter`
- [ ] Router prefixes
- [ ] Router tags
- [ ] OpenAPI
- [ ] Automatic API documentation
- [ ] `/docs`
- [ ] `/redoc`
- [ ] API versioning
- [ ] Breaking vs non-breaking API changes
- [ ] Headers
- [ ] Cookies
- [ ] Cookie security
- [ ] Forms
- [ ] File uploads
- [ ] File-upload security
- [ ] JSON vs form vs multipart
- [ ] Type hints in FastAPI
- [ ] FastAPI application structure
- [ ] Route-handler responsibilities
- [ ] Response status codes
- [ ] Custom responses
- [ ] API documentation as a contract
- [ ] Common FastAPI mistakes

______________________________________________________________________

# 50. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is FastAPI?
1. Is FastAPI an ASGI server?
1. FastAPI vs Uvicorn?
1. What is ASGI?
1. How does routing work in FastAPI?
1. What are path parameters?
1. What are query parameters?
1. How do you define a request body?
1. What is Pydantic used for?
1. How does FastAPI validate request data?
1. Validation vs business rules?
1. What are response models?
1. Why are response models important?
1. What is serialization?
1. What is response validation?
1. What is an `APIRouter`?
1. Why use routers?
1. What is OpenAPI?
1. How does FastAPI generate OpenAPI?
1. What are `/docs` and `/redoc`?
1. Why is OpenAPI useful?
1. How would you version a FastAPI API?
1. When should you introduce a new API version?
1. What are HTTP headers?
1. How do you read headers in FastAPI?
1. How do you read cookies?
1. How do you set cookies?
1. Explain `Secure`, `HttpOnly` and `SameSite`.
1. How do you handle form data?
1. How do you handle file uploads?
1. Why use `UploadFile`?
1. JSON vs form vs multipart?
1. Query parameter vs request body?
1. How do Python type hints participate in FastAPI?
1. How would you structure a large FastAPI application?
1. What should a route handler be responsible for?
1. Why should internal database models not necessarily be returned directly?
1. What is a common mistake with async FastAPI endpoints?
1. How would you protect a file-upload endpoint?
1. How would you prevent API documentation from drifting from implementation?
1. An endpoint receives an invalid path parameter. What happens?
1. A response model contains fewer fields than the internal database object. Why is that useful?
1. A route has 300 lines of business and database logic. How would you refactor it?
1. A new API change breaks existing clients. How would you handle versioning?
1. An async endpoint uses a blocking library. What problem does it create?
1. A service accepts 500 MB uploads. What production concerns do you consider?
1. How would you explain FastAPI's request handling from ASGI server to response?
1. How do type hints, Pydantic and OpenAPI work together?
1. How would you design a maintainable FastAPI application for a growing team?
1. What responsibilities belong in the router, service and repository layers?

If you can answer these clearly and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [13. Complete Backend Request Lifecycle](./13-request-lifecycle.md)

**Next:** [15. FastAPI Dependency Injection, Middleware & Errors](./15-fastapi-di-middleware-errors.md)

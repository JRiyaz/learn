# FastAPI Questions - Part 1

> **Course:** FastAPI for Backend Engineers
>
> **File:** `fastapi-questions-01.md`
>
> **Difficulty:** Easy → Intermediate
>
> **Questions:** 1–100

______________________________________________________________________

# FastAPI Fundamentals

### 1.

What is FastAPI?

### 2.

Why was FastAPI created?

### 3.

What are the main advantages of FastAPI over Flask?

### 4.

Why is FastAPI considered high-performance?

### 5.

What does ASGI stand for?

### 6.

How is ASGI different from WSGI?

### 7.

Why does FastAPI use ASGI instead of WSGI?

### 8.

What are some ASGI servers?

### 9.

What is Uvicorn?

### 10.

How do you start a FastAPI application?

______________________________________________________________________

# FastAPI Application

### 11.

What is the purpose of the `FastAPI()` class?

### 12.

Where is the application instance usually created?

### 13.

Can a project contain multiple FastAPI applications?

### 14.

What happens internally when a request reaches FastAPI?

### 15.

How does FastAPI know which function should handle a request?

______________________________________________________________________

# Routing

### 16.

What is a route?

### 17.

What is a path operation?

### 18.

Difference between GET and POST?

### 19.

Difference between PUT and PATCH?

### 20.

When should DELETE be used?

### 21.

What is an idempotent HTTP method?

### 22.

Which HTTP methods are idempotent?

### 23.

Why is POST not idempotent?

### 24.

Can multiple routes have the same path?

### 25.

How does FastAPI match routes?

______________________________________________________________________

# Path Parameters

### 26.

What are path parameters?

### 27.

How are they validated?

### 28.

What happens if validation fails?

### 29.

Difference between path parameters and query parameters?

### 30.

Can path parameters have default values?

______________________________________________________________________

# Query Parameters

### 31.

What are query parameters?

### 32.

How are optional query parameters declared?

### 33.

How do default values work?

### 34.

Can query parameters be lists?

### 35.

How does FastAPI validate query parameters?

______________________________________________________________________

# Request Body

### 36.

How is JSON request data received?

### 37.

Why are Pydantic models used?

### 38.

How does FastAPI know whether data belongs to body or query?

### 39.

Can one endpoint accept multiple request bodies?

### 40.

How are nested request bodies handled?

______________________________________________________________________

# Pydantic

### 41.

What is Pydantic?

### 42.

Why is Pydantic used?

### 43.

What happens when validation fails?

### 44.

Difference between type hints and validation?

### 45.

How are optional fields defined?

### 46.

How are default values assigned?

### 47.

What are field validators?

### 48.

Why should response models be different from ORM models?

### 49.

What is serialization?

### 50.

What is deserialization?

______________________________________________________________________

# Response Models

### 51.

Why use response models?

### 52.

How do response models improve security?

### 53.

What happens if returned data doesn't match the response model?

### 54.

Difference between request schema and response schema?

### 55.

Can response models exclude fields?

______________________________________________________________________

# Status Codes

### 56.

Common success status codes?

### 57.

Difference between 200 and 201?

### 58.

Difference between 204 and 200?

### 59.

Difference between 400 and 422?

### 60.

Difference between 401 and 403?

### 61.

Difference between 404 and 409?

### 62.

Difference between 500 and 503?

### 63.

Why is choosing proper status codes important?

______________________________________________________________________

# Headers

### 64.

What are HTTP headers?

### 65.

Difference between request headers and response headers?

### 66.

What is the Authorization header?

### 67.

What is Content-Type?

### 68.

What is Accept?

### 69.

How do you read headers in FastAPI?

### 70.

How are custom headers read?

______________________________________________________________________

# Cookies

### 71.

What are cookies?

### 72.

Difference between cookies and headers?

### 73.

What is HttpOnly?

### 74.

What is Secure?

### 75.

What is SameSite?

### 76.

How do you set cookies?

### 77.

How do you delete cookies?

______________________________________________________________________

# Forms

### 78.

What is form data?

### 79.

Difference between JSON and form data?

### 80.

When should forms be used?

### 81.

What package is required for form parsing?

### 82.

What content type is used for forms?

______________________________________________________________________

# File Uploads

### 83.

How are files uploaded?

### 84.

Difference between File and UploadFile?

### 85.

Why is UploadFile recommended?

### 86.

How do you upload multiple files?

### 87.

How do you validate uploaded files?

### 88.

Why shouldn't filenames be trusted?

______________________________________________________________________

# Middleware

### 89.

What is middleware?

### 90.

Why use middleware?

### 91.

What does `call_next()` do?

### 92.

Difference between middleware and dependencies?

### 93.

What tasks are commonly handled by middleware?

______________________________________________________________________

# Exception Handling

### 94.

What is HTTPException?

### 95.

Why use custom exception handlers?

### 96.

Why shouldn't HTTPException be raised from repositories?

### 97.

What is a global exception handler?

### 98.

Why shouldn't stack traces be returned to clients?

### 99.

What is a consistent error response format?

### 100.

Why is proper exception handling important in production APIs?

______________________________________________________________________

# Next

[FastAPI Questions - Part 2](37-fastapi-questions-02.md)

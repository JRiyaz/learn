# Request & Response

> **Course:** Flask for Backend Engineers
>
> **Module:** 1
>
> **File:** `03_request_response.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What an HTTP Request is
- What an HTTP Response is
- Flask Request Object
- Request Lifecycle
- Headers
- Query Parameters
- Form Data
- JSON Data
- Cookies
- Sessions
- File Uploads
- Response Object
- Status Codes
- Custom Responses
- Best Practices

______________________________________________________________________

# What is an HTTP Request?

An HTTP Request is a message sent by a client to a server asking it to perform an action.

Example

```
Browser

↓

GET /users/10

↓

Flask
```

Every Flask route starts by receiving an HTTP request.

______________________________________________________________________

# Components of a Request

A request consists of:

```
HTTP Method

↓

URL

↓

Headers

↓

Body

↓

Cookies
```

Example

```
POST /login

Headers

Authorization

Content-Type

Body

{
    "username": "riyaz",
    "password": "******"
}
```

______________________________________________________________________

# What is an HTTP Response?

After processing the request,

Flask sends a response.

A response contains:

```
Status Code

↓

Headers

↓

Body
```

Example

```
200 OK

Content-Type: application/json

{
    "message": "Login Successful"
}
```

______________________________________________________________________

# Request Lifecycle

```
Client

↓

HTTP Request

↓

Flask

↓

Route

↓

Business Logic

↓

Database

↓

Response

↓

Client
```

Every request follows this lifecycle.

______________________________________________________________________

# Flask Request Object

Flask provides a global `request` object.

```python
from flask import request
```

It contains information about the incoming request.

______________________________________________________________________

# Request URL

```python
from flask import request

@app.route("/")
def home():

    return request.url
```

Example Output

```
http://localhost:5000/
```

______________________________________________________________________

# Request Method

```python
request.method
```

Example

```python
@app.route(
    "/users",
    methods=["GET", "POST"]
)
def users():

    return request.method
```

Possible output

```
GET
```

or

```
POST
```

______________________________________________________________________

# Request Headers

Headers contain metadata.

Example

```
Authorization

Content-Type

User-Agent

Accept
```

Read headers

```python
request.headers
```

Specific header

```python
request.headers.get(
    "Authorization"
)
```

______________________________________________________________________

# Common HTTP Headers

| Header | Purpose |
|----------|----------|
| Authorization | Authentication |
| Content-Type | Body Format |
| Accept | Response Format |
| User-Agent | Client Information |
| Host | Server Host |

______________________________________________________________________

# Query Parameters

URL

```
/users?page=2
```

Python

```python
page = request.args.get("page")
```

Default value

```python
page = request.args.get(
    "page",
    1,
    type=int
)
```

______________________________________________________________________

# Route Parameters

```python
@app.route("/users/<int:id>")
def user(id):

    return str(id)
```

Request

```
/users/100
```

↓

```
100
```

Route parameters are passed directly to the function.

______________________________________________________________________

# Form Data

HTML Forms send data as

```
application/x-www-form-urlencoded
```

Read form values

```python
username = request.form.get(
    "username"
)
```

Password

```python
password = request.form.get(
    "password"
)
```

______________________________________________________________________

# JSON Requests

Modern REST APIs usually send JSON.

Example Request

```json
{
    "name": "Riyaz",
    "age": 27
}
```

______________________________________________________________________

# Reading JSON

```python
data = request.get_json()

name = data["name"]
```

Safer approach

```python
data = request.get_json() or {}

name = data.get("name")
```

______________________________________________________________________

# JSON Example

```python
@app.route(
    "/users",
    methods=["POST"]
)
def create_user():

    data = request.get_json()

    return data
```

______________________________________________________________________

# Raw Request Body

Sometimes raw data is needed.

```python
body = request.data
```

Returns bytes.

Useful for:

- Webhooks
- Signature Verification
- Binary Data

______________________________________________________________________

# Cookies

Read cookie

```python
request.cookies.get(
    "session_id"
)
```

Cookies store small pieces of client-side information.

______________________________________________________________________

# Sessions

Flask provides session support.

```python
from flask import session
```

Store value

```python
session["username"] = "riyaz"
```

Read value

```python
session.get("username")
```

Sessions are typically backed by securely signed cookies by default.

______________________________________________________________________

# File Upload

HTML

```
multipart/form-data
```

Python

```python
file = request.files["image"]
```

Save

```python
file.save("image.png")
```

Production systems often upload files to S3 instead of local storage.

______________________________________________________________________

# Request Validation

Never trust client input.

Bad

```python
age = data["age"]
```

Better

```python
age = data.get("age")
```

Validate

- Type
- Length
- Required Fields
- Allowed Values

______________________________________________________________________

# Response Object

Simplest response

```python
return "Hello"
```

Flask converts it into an HTTP response automatically.

______________________________________________________________________

# Returning JSON

```python
from flask import jsonify

@app.route("/")
def home():

    return jsonify(
        {
            "status": "success"
        }
    )
```

Produces a JSON response with the correct `Content-Type`.

______________________________________________________________________

# Returning Status Code

```python
return (
    jsonify(
        {"error": "Not Found"}
    ),
    404
)
```

______________________________________________________________________

# Common Status Codes

| Code | Meaning |
|--------|----------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Unprocessable Entity |
| 500 | Internal Server Error |

______________________________________________________________________

# Custom Response

```python
from flask import make_response

response = make_response(
    "Success",
    200
)

response.headers[
    "X-Version"
] = "1.0"

return response
```

______________________________________________________________________

# Setting Cookies

```python
response = make_response(
    "Logged In"
)

response.set_cookie(
    "username",
    "riyaz"
)

return response
```

______________________________________________________________________

# Deleting Cookies

```python
response.delete_cookie(
    "username"
)
```

______________________________________________________________________

# Response Headers

Add custom headers

```python
response.headers[
    "X-App"
] = "Flask"
```

Useful for

- Versioning
- Caching
- Security
- Debugging

______________________________________________________________________

# File Download

```python
from flask import send_file

return send_file(
    "report.pdf"
)
```

Useful for

- Reports
- Images
- Documents

______________________________________________________________________

# Redirect Response

```python
from flask import redirect

return redirect("/login")
```

Returns

```
302 Found
```

by default.

______________________________________________________________________

# Typical REST API Response

```json
{
    "success": true,
    "data": {
        "id": 10,
        "name": "Riyaz"
    }
}
```

Error

```json
{
    "success": false,
    "error": "User not found"
}
```

A consistent response structure makes APIs easier to consume.

______________________________________________________________________

# Common Mistakes

❌ Using `request.form` for JSON APIs

❌ Trusting client input

❌ Returning Python dictionaries without considering framework behavior (prefer `jsonify()` for explicitness and
compatibility)

❌ Returning incorrect status codes

❌ Saving uploaded files directly to local storage in production

❌ Exposing sensitive information in responses

______________________________________________________________________

# Production Best Practices

- Validate all input.
- Use `jsonify()` for JSON responses.
- Return meaningful HTTP status codes.
- Never trust client data.
- Store uploaded files in object storage (such as S3).
- Use structured error responses.
- Avoid exposing stack traces to clients.
- Sanitize and validate uploaded files.

______________________________________________________________________

# Interview Deep Dive

### Question

**How do you handle incoming JSON requests and return proper JSON responses in Flask?**

### Answer

A typical REST API implementation includes:

1. Read the request body using `request.get_json()`.
1. Validate the incoming data.
1. Execute business logic.
1. Return a JSON response using `jsonify()`.
1. Include an appropriate HTTP status code.

Example:

```python
from flask import request, jsonify

@app.route("/users", methods=["POST"])
def create_user():

    data = request.get_json() or {}

    if "name" not in data:
        return jsonify(
            {"error": "Name is required"}
        ), 400

    return jsonify(
        {
            "message": "User created",
            "user": data
        }
    ), 201
```

This approach produces consistent, standards-compliant REST API responses.

______________________________________________________________________

# Summary

In this chapter you learned:

- HTTP Requests
- HTTP Responses
- Request Object
- Headers
- Query Parameters
- Route Parameters
- Form Data
- JSON Requests
- Cookies
- Sessions
- File Uploads
- Response Object
- Status Codes
- Custom Responses

Understanding the request-response cycle is fundamental because every Flask application is built around processing HTTP
requests and generating HTTP responses.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is an HTTP Request?
1. What is an HTTP Response?
1. What information does Flask's `request` object provide?

______________________________________________________________________

## Request Data

4. How do you read query parameters?
1. How do you read route parameters?
1. How do you read form data?
1. How do you read JSON request bodies?
1. When would you use `request.data` instead of `request.get_json()`?

______________________________________________________________________

## Responses

9. Why is `jsonify()` recommended?
1. How do you return a custom status code?
1. How do you add custom response headers?
1. How do you send a file as a response?

______________________________________________________________________

## Cookies & Sessions

13. How do you read cookies?
01. How do you set cookies?
01. What is the difference between cookies and sessions?

______________________________________________________________________

## Scenario-Based

16. Your REST API receives JSON, but the developer uses `request.form`. Why is this incorrect?
01. A client sends invalid JSON data. How should your API respond?
01. Your application allows users to upload profile pictures. Why shouldn't you store uploads directly on the web server in production?
01. Your API always returns HTTP 200, even when errors occur. Why is this a bad design?
01. A developer directly accesses `data["username"]` from the request body without validation. What problems could this cause?

______________________________________________________________________

# Next

[Templates & Jinja2](04_templates_jinja.md)

# Flask Routing

> **Course:** Flask for Backend Engineers
>
> **Module:** 1
>
> **File:** `02_flask_routing.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Routing is
- URL Mapping
- Route Decorators
- HTTP Methods
- Dynamic URL Parameters
- Path Converters
- Query Parameters
- URL Building
- Redirects
- Custom URL Converters
- Route Organization
- Best Practices
- Common Mistakes

______________________________________________________________________

# What is Routing?

Routing is the process of mapping a URL to a Python function.

Example

```
Browser

↓

GET /users

↓

Flask

↓

users()

↓

Response
```

Without routing,

Flask would not know which function should execute.

______________________________________________________________________

# Real World Analogy

Imagine a receptionist.

```
Customer

↓

"I need Sales"

↓

Receptionist

↓

Sales Department
```

Flask Routing works exactly the same.

```
Request

↓

URL

↓

Matching Function
```

______________________________________________________________________

# Basic Route

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Home Page"
```

Request

```
GET /
```

↓

Response

```
Home Page
```

______________________________________________________________________

# Multiple Routes

```python
@app.route("/")
def home():
    return "Home"

@app.route("/about")
def about():
    return "About"

@app.route("/contact")
def contact():
    return "Contact"
```

Routing Table

| URL | Function |
|------|----------|
| / | home |
| /about | about |
| /contact | contact |

______________________________________________________________________

# Route Decorator

The decorator

```python
@app.route("/users")
```

tells Flask

```
If

/users

↓

Execute

users()
```

The decorator registers the function with Flask's routing system.

______________________________________________________________________

# HTTP Methods

Different HTTP methods represent different operations.

| Method | Purpose |
|---------|----------|
| GET | Read Data |
| POST | Create Data |
| PUT | Replace Data |
| PATCH | Update Data |
| DELETE | Delete Data |

______________________________________________________________________

# Default Method

```python
@app.route("/users")
def users():
    return "Users"
```

This route accepts only

```
GET
```

requests.

______________________________________________________________________

# Multiple HTTP Methods

```python
@app.route(
    "/users",
    methods=["GET", "POST"]
)
def users():
    return "Users"
```

Now Flask accepts

```
GET /users

POST /users
```

______________________________________________________________________

# Better Practice

Instead of one function doing everything,

separate responsibilities where practical.

Example

```
GET /users

↓

List Users
```

```
POST /users

↓

Create User
```

The route is the same,

but behavior depends on the HTTP method.

______________________________________________________________________

# Using request.method

```python
from flask import request

@app.route(
    "/users",
    methods=["GET", "POST"]
)
def users():

    if request.method == "GET":
        return "List Users"

    return "Create User"
```

______________________________________________________________________

# Dynamic URL Parameters

Instead of

```
/user1

/user2

/user3
```

Flask supports variables.

```python
@app.route("/users/<id>")
def user(id):
    return f"User {id}"
```

Example

```
GET /users/10
```

↓

```
User 10
```

______________________________________________________________________

# Integer Converter

```python
@app.route("/users/<int:id>")
def user(id):
    return str(id)
```

Now

```
/users/100
```

works.

```
/users/abc
```

returns

```
404
```

because `"abc"` is not an integer.

______________________________________________________________________

# Common Path Converters

| Converter | Example |
|------------|----------|
| string | `<string:name>` |
| int | `<int:id>` |
| float | `<float:price>` |
| path | `<path:file>` |
| uuid | `<uuid:id>` |

______________________________________________________________________

# String Converter

```python
@app.route("/hello/<string:name>")
def hello(name):
    return f"Hello {name}"
```

Request

```
/hello/riyaz
```

↓

```
Hello riyaz
```

______________________________________________________________________

# Float Converter

```python
@app.route("/price/<float:value>")
def price(value):
    return str(value)
```

Example

```
/price/99.99
```

______________________________________________________________________

# Path Converter

Useful for file paths.

```python
@app.route("/files/<path:file_path>")
def files(file_path):
    return file_path
```

Request

```
/files/docs/python/flask.pdf
```

↓

```
docs/python/flask.pdf
```

______________________________________________________________________

# Query Parameters

Query parameters are **not** part of the route.

Example

```
/users?page=2
```

The route remains

```
/users
```

______________________________________________________________________

# Reading Query Parameters

```python
from flask import request

@app.route("/users")
def users():

    page = request.args.get("page")

    return page
```

Request

```
/users?page=5
```

↓

```
5
```

______________________________________________________________________

# Multiple Query Parameters

```
/search?q=python&page=2
```

```python
q = request.args.get("q")

page = request.args.get("page")
```

Useful for:

- Pagination
- Filtering
- Searching
- Sorting

______________________________________________________________________

# Route Variables vs Query Parameters

Route Variable

```
/users/10
```

Usually identifies

```
One Resource
```

Query Parameter

```
/users?page=2
```

Usually modifies

```
The Request
```

______________________________________________________________________

# URL Building

Never hardcode URLs.

Instead use

```python
from flask import url_for
```

Example

```python
@app.route("/users")
def users():
    return "Users"

@app.route("/")
def home():
    return url_for("users")
```

Output

```
/users
```

Benefits

- Easier maintenance
- Safer refactoring

______________________________________________________________________

# Dynamic URL Building

```python
@app.route("/users/<int:id>")
def user(id):
    return str(id)

url_for(
    "user",
    id=5
)
```

Result

```
/users/5
```

______________________________________________________________________

# Redirect

```python
from flask import redirect

@app.route("/")
def home():
    return redirect("/login")
```

Request

```
/
```

↓

Redirect

↓

```
/login
```

______________________________________________________________________

# Redirect with url_for

Preferred

```python
return redirect(
    url_for("login")
)
```

Instead of

```python
return redirect("/login")
```

______________________________________________________________________

# 404 Not Found

Request

```
/unknown
```

No matching route

↓

```
404 Not Found
```

Flask automatically handles unmatched routes.

______________________________________________________________________

# Route Order

Specific routes should generally be defined before broader dynamic routes for readability, although Flask's routing
system prioritizes more specific rules.

Example

```python
@app.route("/users/new")
```

before

```python
@app.route("/users/<id>")
```

This avoids ambiguity and improves maintainability.

______________________________________________________________________

# Custom URL Converter

Flask allows custom converters.

Example

```python
from werkzeug.routing import BaseConverter

class UpperConverter(BaseConverter):
    regex = "[A-Z]+"

app.url_map.converters["upper"] = UpperConverter

@app.route("/code/<upper:value>")
def code(value):
    return value
```

Now

```
/code/ABC
```

matches.

```
/code/abc
```

does not.

Custom converters are rarely needed but useful for advanced routing requirements.

______________________________________________________________________

# Route Organization

Small applications

```
app.py
```

Large applications

```
routes/

↓

users.py

products.py

orders.py
```

Later,

Blueprints make route organization even cleaner.

______________________________________________________________________

# RESTful Routing

Instead of

```
/getUsers

/createUser
```

Prefer

```
GET /users

POST /users

GET /users/10

DELETE /users/10
```

This is the standard REST style.

______________________________________________________________________

# Common Mistakes

❌ Hardcoding URLs

❌ Using query parameters for resource identifiers

❌ Creating routes like `/getUserData`

❌ Putting too much business logic inside route functions

❌ Ignoring HTTP methods

______________________________________________________________________

# Production Best Practices

- Use RESTful URLs.
- Use `url_for()` instead of hardcoded URLs.
- Keep route functions small.
- Validate route parameters.
- Use appropriate HTTP methods.
- Organize routes using Blueprints.
- Return meaningful HTTP status codes.

______________________________________________________________________

# Interview Deep Dive

### Question

**What is the difference between a route parameter and a query parameter? When would you use each?**

### Answer

A **route parameter** identifies a specific resource.

Example

```
GET /users/42
```

Here, `42` identifies a particular user.

A **query parameter** modifies how the request is processed.

Examples include:

```
GET /users?page=2

GET /users?sort=name

GET /users?active=true
```

Query parameters are commonly used for pagination, filtering, searching, and sorting, while route parameters identify
resources.

______________________________________________________________________

# Summary

In this chapter you learned:

- What Routing is
- Route Decorators
- HTTP Methods
- Dynamic URL Parameters
- Path Converters
- Query Parameters
- URL Building
- Redirects
- Custom URL Converters
- RESTful Routing
- Best Practices

Routing is the foundation of every Flask application because every incoming HTTP request begins by matching a route.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is routing?
1. How does Flask map URLs to functions?
1. What is the purpose of `@app.route()`?

______________________________________________________________________

## HTTP Methods

4. Which HTTP method is used by default?
1. How do you allow multiple HTTP methods for a route?
1. Why should REST APIs use different HTTP methods instead of different URLs?

______________________________________________________________________

## Route Parameters

7. What is a dynamic route parameter?
1. What path converters does Flask provide?
1. What happens if an `int` converter receives a string?

______________________________________________________________________

## Query Parameters

10. How do you read query parameters?
01. What is the difference between `request.args` and route parameters?
01. When should query parameters be used?

______________________________________________________________________

## URL Building

13. Why is `url_for()` preferred over hardcoded URLs?
01. How do you generate a URL containing route parameters?
01. How do you redirect a user to another route?

______________________________________________________________________

## Scenario-Based

16. Your application currently has routes such as `/getUsers`, `/createUser`, and `/deleteUser`. How would you redesign them following REST principles?
01. Your application supports pagination and filtering. Which parts of the URL should be route parameters and which should be query parameters?
01. A developer hardcodes URLs throughout the application. What problems could this cause when routes change?
01. A request to `/users/abc` returns a 404 error even though the route exists. The route is defined as `/users/<int:id>`. Why?
01. Your Flask project has more than 100 routes in a single file. How would you reorganize the project?

______________________________________________________________________

# Next

[Request & Response](03_request_response.md)

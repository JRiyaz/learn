# 17. Flask

**Previous:** [16. Production FastAPI](./16-fastapi-production.md)

**Next:** [18. SQL Fundamentals](./18-sql-fundamentals.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain Flask's architecture and request lifecycle.
- Understand Flask routing and request/response handling.
- Explain Blueprints and application factories.
- Understand Flask configuration and extensions.
- Build and reason about REST APIs in Flask.
- Explain authentication at a practical interview level.
- Understand Flask testing.
- Explain WSGI and how Gunicorn serves Flask applications.
- Compare Flask and FastAPI.
- Discuss when Flask remains a good backend choice.

This is intentionally an **interview-ready overview**, not a deep Flask specialization.

______________________________________________________________________

# 1. What Is Flask?

Flask is a lightweight Python web framework built around WSGI.

It provides core web application capabilities such as:

- Routing
- Request handling
- Response handling
- Templates
- Sessions
- Error handling

Additional functionality is commonly added through extensions or application code.

______________________________________________________________________

# 2. Flask Philosophy

Flask is intentionally minimal.

Instead of forcing one complete application architecture, Flask allows teams to choose:

- ORM
- Authentication solution
- Validation library
- Serialization library
- Project structure
- Extension ecosystem

This flexibility is one of Flask's major strengths.

The trade-off is that teams need to establish their own conventions.

______________________________________________________________________

# 3. Flask Application

A minimal Flask application:

```python
from flask import Flask

app = Flask(__name__)


@app.get("/health")
def health():
    return {"status": "ok"}
```

The application object holds configuration, routes and other application-level behavior.

______________________________________________________________________

# 4. Routing

Routes map HTTP requests to Python functions.

Example:

```python
@app.get("/users/<int:user_id>")
def get_user(user_id):
    ...
```

The route declares:

```text
HTTP method
+
URL pattern
+
view function
```

______________________________________________________________________

# 5. Path Parameters

Flask supports converters for route parameters.

Example:

```python
@app.get("/users/<int:user_id>")
def get_user(user_id):
    return {"id": user_id}
```

The `<int:user_id>` converter ensures that the route parameter is interpreted as an integer.

______________________________________________________________________

# 6. Query Parameters

Query parameters are available through the request object.

Example:

```python
from flask import request


@app.get("/users")
def users():
    page = request.args.get("page", 1, type=int)
    return {"page": page}
```

Query validation is generally handled by application code or additional libraries.

______________________________________________________________________

# 7. Request Object

Flask exposes request information through:

```python
from flask import request
```

Common information includes:

- HTTP method
- Headers
- Query parameters
- Path parameters
- Cookies
- Form data
- Request body
- Files

______________________________________________________________________

# 8. JSON Request Bodies

A Flask endpoint can read JSON:

```python
data = request.get_json()
```

For production APIs, validate incoming data rather than assuming the JSON structure is correct.

Validation can be implemented with application code or libraries such as Marshmallow or Pydantic.

______________________________________________________________________

# 9. Responses

A Flask view can return:

```python
return {"message": "ok"}
```

It can also explicitly return status codes and headers:

```python
return {"created": True}, 201
```

For more control, Flask provides `make_response()` and response objects.

______________________________________________________________________

# 10. REST APIs with Flask

A Flask REST API commonly follows:

```text
Route
  ↓
Validation
  ↓
Service/business logic
  ↓
Repository/database
  ↓
Serialization
  ↓
Response
```

Flask itself does not force this architecture.

The team should define boundaries explicitly.

______________________________________________________________________

# 11. Blueprints

Blueprints allow an application to organize routes into reusable components.

Example:

```python
from flask import Blueprint

users_bp = Blueprint("users", __name__)


@users_bp.get("/users")
def users():
    ...
```

The blueprint can then be registered with the application.

______________________________________________________________________

# 12. Why Use Blueprints?

Blueprints help organize larger applications by separating route groups.

For example:

```text
users
orders
payments
admin
```

can each have their own blueprint.

This avoids putting all routes into one large module.

______________________________________________________________________

# 13. Application Factory

Instead of creating one globally configured application, Flask applications can use an application factory.

Example:

```python
def create_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    return app
```

The factory creates and configures an application instance.

______________________________________________________________________

# 14. Why Application Factories Matter

Application factories are useful for:

- Testing
- Multiple configurations
- Environment-specific setup
- Avoiding initialization side effects
- Better application modularity

For example:

```text
create_app(test_config)
create_app(dev_config)
create_app(prod_config)
```

______________________________________________________________________

# 15. Configuration

Flask provides a configuration object:

```python
app.config
```

Configuration may include:

```text
DATABASE_URL
SECRET_KEY
DEBUG
TESTING
```

Sensitive values should not be committed to source control.

______________________________________________________________________

# 16. Flask Extensions

Flask's ecosystem provides extensions for functionality such as:

- Database access
- Authentication
- Migrations
- Caching
- REST APIs

The extension model provides flexibility but requires teams to evaluate compatibility and maintenance.

______________________________________________________________________

# 17. Flask-SQLAlchemy

A common Flask ecosystem choice is Flask-SQLAlchemy.

Conceptually:

```text
Flask
 ↓
Flask-SQLAlchemy
 ↓
SQLAlchemy
 ↓
Database
```

The important interview point is that Flask does not require SQLAlchemy.

It can use different persistence approaches.

______________________________________________________________________

# 18. Authentication

Authentication determines who is making the request.

A Flask API can implement authentication using:

- Session cookies
- API keys
- JWT
- OAuth2/OIDC integrations

The specific choice depends on application requirements.

______________________________________________________________________

# 19. Authentication Decorators

A common Flask pattern is a decorator:

```python
@app.get("/profile")
@require_auth
def profile():
    ...
```

The decorator can:

1. Read credentials.
1. Validate them.
1. Establish the current identity.
1. Reject unauthorized requests.

This is conceptually similar to reusable security dependencies in FastAPI, although the mechanisms differ.

______________________________________________________________________

# 20. Authorization

Authentication is not authorization.

After identifying the caller, the application still needs to determine whether the caller has permission.

Example:

```text
Authentication
      ↓
Current user
      ↓
Permission check
      ↓
Endpoint
```

______________________________________________________________________

# 21. Error Handling

Flask supports application-level error handlers.

Example:

```python
@app.errorhandler(404)
def not_found(error):
    return {"error": "not found"}, 404
```

Custom exception handling can be used to establish a consistent API error format.

______________________________________________________________________

# 22. Custom Exceptions

Define domain exceptions independently of HTTP when appropriate:

```python
class UserNotFoundError(Exception):
    pass
```

Then translate the exception at the API boundary.

This keeps business logic less coupled to Flask.

______________________________________________________________________

# 23. Request Lifecycle

A simplified Flask lifecycle is:

```text
HTTP request
 ↓
WSGI server
 ↓
Flask application
 ↓
Request processing
 ↓
Routing
 ↓
View function
 ↓
Response
 ↓
WSGI server
 ↓
Client
```

Middleware-like behavior can be implemented using Flask hooks or WSGI middleware.

______________________________________________________________________

# 24. Before and After Request Hooks

Flask provides request lifecycle hooks such as:

```python
@app.before_request
def before_request():
    ...
```

and:

```python
@app.after_request
def after_request(response):
    return response
```

These can be used for cross-cutting request behavior.

Use them carefully because they can affect many routes.

______________________________________________________________________

# 25. WSGI

WSGI stands for Web Server Gateway Interface.

It defines an interface between Python web applications/frameworks and WSGI servers.

Conceptually:

```text
HTTP
 ↓
Web server / WSGI server
 ↓
WSGI application
 ↓
Flask
```

Flask is traditionally a WSGI application.

______________________________________________________________________

# 26. Gunicorn

Gunicorn is a production WSGI server commonly used to serve Flask applications.

Conceptually:

```text
Client
 ↓
Reverse Proxy / Load Balancer
 ↓
Gunicorn
 ├── Worker
 ├── Worker
 └── Worker
       ↓
     Flask
```

The exact deployment can vary.

______________________________________________________________________

# 27. Why Not Use Flask's Development Server in Production?

Flask's development server is intended for development.

Production deployments generally use a production-grade WSGI server such as Gunicorn behind appropriate infrastructure.

The development server is not the production process-management and serving solution you want for a serious deployment.

______________________________________________________________________

# 28. Gunicorn Workers

Gunicorn can run multiple worker processes.

Conceptually:

```text
Gunicorn master
   ├── worker 1
   ├── worker 2
   ├── worker 3
   └── worker 4
```

Multiple workers allow requests to be processed by multiple processes.

Worker configuration should consider:

- CPU
- Memory
- Workload
- Database connections
- Expected concurrency

More workers are not automatically better.

______________________________________________________________________

# 29. Flask and Blocking I/O

Traditional Flask applications often use synchronous request handlers.

A blocking operation can occupy a worker while it waits.

For example:

```text
Worker
 ↓
External API
 ↓
wait
 ↓
response
```

This is an important architectural consideration when choosing concurrency strategies.

______________________________________________________________________

# 30. Flask Testing

Flask provides a test client that can exercise routes without requiring a real network server.

Example:

```python
def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
```

Testing can cover:

- Routes
- Request validation
- Authentication
- Error handling
- Database integration

______________________________________________________________________

# 31. Testing with Application Factories

Factories make testing easier because a test can create an isolated application configuration.

For example:

```text
create_app(TESTING_CONFIG)
       ↓
test client
       ↓
endpoint
```

This helps avoid accidentally testing against production configuration.

______________________________________________________________________

# 32. Flask REST API Project Structure

A practical project could look like:

```text
app/
├── __init__.py
├── routes/
│   ├── users.py
│   └── orders.py
├── services/
├── repositories/
├── models/
├── schemas/
├── extensions.py
└── config.py
```

The exact structure is a team decision.

The important point is separating responsibilities as complexity grows.

______________________________________________________________________

# 33. Flask vs FastAPI — Architecture

### Flask

```text
WSGI
 ↓
Flask
 ↓
Routes
```

### FastAPI

```text
ASGI
 ↓
FastAPI
 ↓
Routes
```

FastAPI is designed around modern async-capable ASGI infrastructure.

Flask is traditionally WSGI-based, although modern Flask versions have support for async view functions with important
limitations and do not turn the entire WSGI stack into an ASGI application.

______________________________________________________________________

# 34. Flask vs FastAPI — Validation

Flask itself does not provide FastAPI-style automatic request-model validation.

A Flask application commonly uses:

- Manual validation
- Marshmallow
- Pydantic
- Other validation libraries

FastAPI integrates tightly with Pydantic-based request/response validation.

______________________________________________________________________

# 35. Flask vs FastAPI — Documentation

FastAPI automatically integrates API schemas with OpenAPI and interactive documentation.

Flask does not provide the same level of automatic API documentation from its core framework.

Teams typically add libraries or tooling when they need this.

______________________________________________________________________

# 36. Flask vs FastAPI — Async

FastAPI is built on ASGI and is designed for asynchronous I/O.

Flask's traditional deployment model is WSGI and synchronous.

Flask supports `async def` views, but under a WSGI deployment an async view does not provide the same long-lived
event-loop concurrency model as an ASGI application.

This distinction is important in interviews.

______________________________________________________________________

# 37. Flask vs FastAPI — Flexibility

Flask is intentionally unopinionated.

This can be an advantage when:

- The team already has established libraries.
- The application is relatively simple.
- You need fine-grained architectural control.
- Existing Flask infrastructure is mature.

The trade-off is more architectural decisions for the team.

______________________________________________________________________

# 38. Flask vs FastAPI — When to Choose

Choose Flask when:

- Existing organizational expertise is strong.
- The application benefits from Flask's ecosystem.
- The service is primarily synchronous.
- Minimal framework constraints are desirable.

Choose FastAPI when:

- Async I/O is important.
- Strong request/response validation is valuable.
- OpenAPI generation is important.
- Modern API development is the primary focus.

This is not an absolute rule.

______________________________________________________________________

# 39. Production Flask Checklist

A production Flask service should consider:

```text
Production WSGI server
Configuration management
Authentication
Authorization
Input validation
Database pooling
Timeouts
Error handling
Logging
Metrics
Health checks
Graceful shutdown
Security
Testing
```

The exact infrastructure depends on the deployment environment.

______________________________________________________________________

# 40. Common Flask Mistakes

## Mistake 1 — One giant application module

Separate routes and responsibilities as the application grows.

## Mistake 2 — Business logic inside route functions

Keep substantial business logic in services or appropriate application layers.

## Mistake 3 — No input validation

Never assume incoming JSON is valid.

## Mistake 4 — Development server in production

Use an appropriate production WSGI server and deployment architecture.

## Mistake 5 — Hard-coded secrets

Keep secrets out of source control.

## Mistake 6 — Confusing authentication with authorization

A valid identity does not automatically mean permission to perform every action.

______________________________________________________________________

# 41. Interview Questions & Answers

## Q1. What is Flask?

**Answer:**

Flask is a lightweight Python web framework traditionally built around WSGI.

It provides core web functionality while leaving many architectural choices to the application.

______________________________________________________________________

## Q2. Why is Flask called lightweight?

**Answer:**

Its core framework provides essential web functionality without forcing a large set of built-in components such as a
specific ORM or authentication system.

Teams add the pieces they need.

______________________________________________________________________

## Q3. What is a Flask route?

**Answer:**

A route maps an HTTP method and URL pattern to a Python view function.

______________________________________________________________________

## Q4. What are Blueprints?

**Answer:**

Blueprints provide a way to organize related routes and application components into reusable modules.

They are particularly useful as an application grows.

______________________________________________________________________

## Q5. What is an application factory?

**Answer:**

An application factory is a function that creates and configures a Flask application instance.

It improves testing, configuration management and modularity.

______________________________________________________________________

## Q6. Why are application factories useful for testing?

**Answer:**

Tests can create separate application instances with test-specific configuration without relying on a single globally
initialized application.

______________________________________________________________________

## Q7. What is `request` in Flask?

**Answer:**

It provides access to information about the current HTTP request, including headers, query parameters, cookies, form
data and request body.

______________________________________________________________________

## Q8. How do you read query parameters?

**Answer:**

Use `request.args`.

For example:

```python
request.args.get("page", type=int)
```

______________________________________________________________________

## Q9. How do you read JSON request data?

**Answer:**

Use:

```python
request.get_json()
```

and validate the resulting structure before using it.

______________________________________________________________________

## Q10. How does Flask return JSON?

**Answer:**

Modern Flask can convert a dictionary/list return value into a JSON response.

You can also construct an explicit response when you need control over headers or status.

______________________________________________________________________

## Q11. What is WSGI?

**Answer:**

WSGI is the interface between Python web applications and WSGI servers.

It allows servers such as Gunicorn to serve applications such as Flask.

______________________________________________________________________

## Q12. What is Gunicorn?

**Answer:**

Gunicorn is a production WSGI server commonly used to run Flask applications.

It can manage multiple worker processes.

______________________________________________________________________

## Q13. Why use Gunicorn instead of Flask's development server?

**Answer:**

The development server is intended for development.

Production applications need an appropriate serving and process-management architecture, commonly using a production
WSGI server such as Gunicorn.

______________________________________________________________________

## Q14. What are Flask request hooks?

**Answer:**

Hooks such as `before_request` and `after_request` allow code to execute at defined points around request processing.

They are useful for cross-cutting behavior.

______________________________________________________________________

## Q15. What are Flask error handlers?

**Answer:**

They allow the application to define how specific HTTP errors or exceptions should be converted into responses.

______________________________________________________________________

## Q16. Why use custom exceptions in Flask?

**Answer:**

Custom domain exceptions allow business logic to communicate meaningful failures without directly constructing HTTP
responses.

The API layer can translate them into appropriate responses.

______________________________________________________________________

## Q17. How would you structure a large Flask application?

**Answer:**

I would separate concerns into route/blueprint modules, services, repositories, models, schemas and configuration,
depending on application complexity.

I would also use an application factory.

______________________________________________________________________

## Q18. What is the difference between authentication and authorization?

**Answer:**

Authentication identifies the caller.

Authorization determines what that caller is allowed to do.

______________________________________________________________________

## Q19. How can authentication be implemented in Flask?

**Answer:**

Common approaches include sessions, API keys, JWT and OAuth2/OIDC integrations.

The correct choice depends on the application and client architecture.

______________________________________________________________________

## Q20. How would you test a Flask API?

**Answer:**

Use Flask's test client to make requests against the application and assert status codes, response bodies, headers and
side effects.

Use application factories and isolated test configuration where appropriate.

______________________________________________________________________

## Q21. Flask vs FastAPI?

**Answer:**

Flask is traditionally a WSGI-based lightweight framework with an intentionally minimal core.

FastAPI is ASGI-based and provides integrated validation and OpenAPI-oriented API development.

The choice depends on application requirements and existing ecosystem constraints.

______________________________________________________________________

## Q22. Does Flask support async?

**Answer:**

Modern Flask supports async view functions, but Flask's traditional WSGI architecture has different concurrency
characteristics from an ASGI framework such as FastAPI.

Using `async def` in Flask does not automatically provide the same async server model as FastAPI under ASGI.

______________________________________________________________________

## Q23. Why might Flask still be a good choice?

**Answer:**

It has a mature ecosystem, is lightweight and flexible, and is often a strong choice when an organization already has
significant Flask expertise and infrastructure.

______________________________________________________________________

## Q24. What is the biggest Flask trade-off?

**Answer:**

Its flexibility means the application team must make more decisions about validation, project structure, authentication,
API documentation and other components.

______________________________________________________________________

## Q25. How would you handle input validation in Flask?

**Answer:**

Use explicit validation at the API boundary, either with manual validation or a validation library such as Marshmallow
or Pydantic.

______________________________________________________________________

## Q26. Where should business logic live?

**Answer:**

Avoid putting substantial business logic directly in route functions.

Use services or appropriate application/domain layers so the logic can be reused and tested independently.

______________________________________________________________________

## Q27. How would you implement consistent API errors?

**Answer:**

Define a standard error schema, create domain-specific exceptions where useful and use Flask error handlers to translate
known exceptions into consistent HTTP responses.

______________________________________________________________________

## Q28. Why are Blueprints useful?

**Answer:**

They provide modular organization for related routes and make large Flask applications easier to maintain.

______________________________________________________________________

## Q29. Why should secrets not be stored in Flask source code?

**Answer:**

Source code can be copied, logged or exposed through repositories.

Secrets should be supplied through appropriate configuration/secret-management mechanisms.

______________________________________________________________________

## Q30. How would you decide between Flask and FastAPI for a new service?

**Answer:**

I would consider:

- Async I/O requirements
- Validation needs
- OpenAPI requirements
- Team expertise
- Existing infrastructure
- Ecosystem
- Operational model
- Migration/maintenance cost

I would choose based on requirements rather than framework popularity.

______________________________________________________________________

# 42. Scenario-Based Questions

## Scenario 1 — Large Flask Application

A Flask project has 300 routes in `app.py`.

**Question:** How would you improve it?

**Answer:**

Introduce Blueprints and organize routes by domain or resource.

Move business logic into services and persistence logic into repositories where appropriate.

Use an application factory to manage application initialization.

______________________________________________________________________

## Scenario 2 — Slow External API

Every Flask request calls an external API that sometimes takes 10 seconds.

**Question:** What would you investigate?

**Answer:**

Add explicit timeouts, examine connection reuse, measure external dependency latency and determine whether the operation
should be asynchronous, cached or moved to background processing.

Also consider the number of Gunicorn workers and the impact of blocked workers.

______________________________________________________________________

## Scenario 3 — Production Deployment

A team runs:

```text
flask run
```

on a production server.

**Question:** What is your concern?

**Answer:**

The development server is not the intended production serving architecture.

Use a production WSGI server such as Gunicorn and appropriate reverse-proxy/load-balancing infrastructure.

______________________________________________________________________

## Scenario 4 — Duplicate Authentication Code

Twenty routes independently parse JWTs.

**Question:** What would you change?

**Answer:**

Create reusable authentication middleware/decorators or authentication utilities and centralize token verification.

Authorization checks should remain explicit and separate from authentication where practical.

______________________________________________________________________

## Scenario 5 — Invalid JSON

A client sends:

```json
{
    "age": "unknown"
}
```

but the application assumes `age` is an integer.

**Question:** What should happen?

**Answer:**

The API should validate the request at the boundary and return a controlled client error rather than allowing malformed
data to reach business logic.

______________________________________________________________________

## Scenario 6 — Flask Factory

Tests accidentally connect to the production database.

**Question:** How can an application factory help?

**Answer:**

The test can create an application with a dedicated testing configuration and test database before constructing the test
client.

______________________________________________________________________

## Scenario 7 — Business Logic in Routes

A route function contains:

```text
validation
database queries
payment processing
email
business rules
serialization
```

**Question:** What is the problem?

**Answer:**

The route has too many responsibilities.

Move domain/business operations into services and persistence into an appropriate repository/data-access layer.

______________________________________________________________________

## Scenario 8 — Flask vs FastAPI

A team needs a high-concurrency API dominated by asynchronous external API calls.

**Question:** Which framework might be a stronger fit?

**Answer:**

FastAPI/ASGI may be a stronger fit because the workload is I/O-bound and benefits from an asynchronous concurrency
model.

The final decision should still consider the team's infrastructure and requirements.

______________________________________________________________________

# 43. Practice Exercises

## Exercise 1 — Flask Application

Create a Flask application with:

```text
GET /health
GET /users/<id>
POST /users
```

Return appropriate status codes.

______________________________________________________________________

## Exercise 2 — Blueprint

Create separate Blueprints for:

```text
users
orders
```

Register both with the application.

______________________________________________________________________

## Exercise 3 — Application Factory

Implement:

```python
create_app(config)
```

and create separate configurations for:

```text
testing
development
production
```

______________________________________________________________________

## Exercise 4 — Validation

Create a user endpoint requiring:

```text
name
email
age
```

Reject invalid input with a consistent JSON error response.

______________________________________________________________________

## Exercise 5 — Authentication

Create an authentication decorator that:

1. Reads a credential.
1. Validates it.
1. Establishes the current user.
1. Rejects unauthorized requests.

Keep authorization as a separate check.

______________________________________________________________________

## Exercise 6 — Error Handling

Create:

```python
class UserNotFoundError(Exception):
    pass
```

Register an error handler that converts it to a 404 response.

______________________________________________________________________

## Exercise 7 — Flask Testing

Using the Flask test client, test:

```text
200 health
404 unknown user
400 invalid input
401 unauthenticated
```

______________________________________________________________________

## Exercise 8 — Architecture

Refactor a route containing business logic into:

```text
Blueprint
   ↓
Service
   ↓
Repository
```

Explain the responsibility of each layer.

______________________________________________________________________

## Exercise 9 — Production Deployment

Draw or document:

```text
Client
 ↓
Reverse Proxy
 ↓
Gunicorn
 ↓
Flask workers
 ↓
Database
```

Explain what each component does.

______________________________________________________________________

## Exercise 10 — Flask vs FastAPI

Write a one-page comparison based on:

```text
WSGI vs ASGI
Validation
OpenAPI
Async
Ecosystem
Testing
Team expertise
Production deployment
```

______________________________________________________________________

# 44. Quick Revision

| Concept | Key Point |
|---|---|
| Flask | Lightweight Python web framework |
| WSGI | Traditional Python web application/server interface |
| Route | Maps HTTP request to view |
| Blueprint | Modular route/component organization |
| Application factory | Creates configured Flask applications |
| `request` | Current HTTP request context |
| `request.args` | Query parameters |
| `request.get_json()` | JSON request body |
| Error handler | Converts errors/exceptions into responses |
| Request hooks | Code around request processing |
| Extension | Adds functionality to Flask |
| Authentication | Identifies caller |
| Authorization | Checks permissions |
| Test client | Tests endpoints without real network server |
| Gunicorn | Production WSGI server |
| Worker | Process handling application requests |
| Flask async | Supported, but not equivalent to ASGI architecture |
| FastAPI | ASGI framework with integrated validation/OpenAPI |
| Factory | Useful for testing/configuration |
| Blueprint | Keeps large applications modular |

______________________________________________________________________

# 45. Completion Checklist

Before moving to File 18, make sure you can explain:

- [ ] Flask architecture
- [ ] Flask philosophy
- [ ] Flask application object
- [ ] Routing
- [ ] Path parameters
- [ ] Query parameters
- [ ] Request object
- [ ] JSON request bodies
- [ ] Responses
- [ ] REST API structure
- [ ] Blueprints
- [ ] Why Blueprints matter
- [ ] Application factories
- [ ] Factory benefits
- [ ] Configuration
- [ ] Flask extensions
- [ ] Flask-SQLAlchemy overview
- [ ] Authentication
- [ ] Authentication decorators
- [ ] Authorization
- [ ] Error handling
- [ ] Custom exceptions
- [ ] Request lifecycle
- [ ] Request hooks
- [ ] WSGI
- [ ] Gunicorn
- [ ] Production server requirements
- [ ] Gunicorn workers
- [ ] Blocking I/O
- [ ] Flask testing
- [ ] Application-factory testing
- [ ] Project structure
- [ ] Flask vs FastAPI architecture
- [ ] Validation differences
- [ ] OpenAPI differences
- [ ] Async differences
- [ ] Flask flexibility
- [ ] Flask production checklist
- [ ] Common Flask mistakes

______________________________________________________________________

# 46. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is Flask?
1. Why is Flask considered lightweight?
1. What is a Flask route?
1. What are Blueprints?
1. Why would you use Blueprints?
1. What is an application factory?
1. Why is an application factory useful for testing?
1. How do you access query parameters?
1. How do you read JSON request data?
1. How does Flask return JSON?
1. What is WSGI?
1. What is Gunicorn?
1. Why shouldn't Flask's development server be used as the production serving solution?
1. What are Gunicorn workers?
1. How would you choose the number of workers?
1. What are Flask request hooks?
1. What is an error handler?
1. Why use custom exceptions?
1. How would you structure a large Flask application?
1. How would you implement authentication?
1. Authentication vs authorization?
1. How would you implement consistent API errors?
1. How would you validate incoming JSON?
1. How would you test a Flask API?
1. Why are application factories useful in tests?
1. How does Flask's traditional concurrency model differ from FastAPI?
1. Does Flask support `async def`?
1. Why doesn't Flask `async def` automatically make the application equivalent to ASGI?
1. What are Flask's biggest strengths?
1. What are Flask's biggest trade-offs?
1. When would you choose Flask over FastAPI?
1. When would you choose FastAPI over Flask?
1. How would you productionize a Flask service?
1. How would you handle a slow external API in Flask?
1. Why should business logic not live entirely in route functions?
1. How would you refactor 300 routes in one module?
1. How would you prevent tests from connecting to production infrastructure?
1. How would you separate authentication from authorization?
1. How would you handle invalid request data?
1. Explain the Flask request lifecycle from client to response.

If you can answer these confidently and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [16. Production FastAPI](./16-fastapi-production.md)

**Next:** [18. SQL Fundamentals](./18-sql-fundamentals.md)

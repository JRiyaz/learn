# HttpClient

Angular applications rarely work in isolation.

Almost every Angular application communicates with a backend.

Examples

- Login
- Fetch Users
- Save Orders
- Upload Images
- Download Reports
- Authentication
- Payments

Angular provides the **HttpClient** module to communicate with backend APIs.

If you're a backend engineer, think of `HttpClient` as Angular's equivalent of

- Python `requests`
- Java `RestTemplate`
- Java `WebClient`
- JavaScript `fetch()`

______________________________________________________________________

# What is HttpClient?

`HttpClient` is Angular's built-in service for making HTTP requests.

It supports

- GET
- POST
- PUT
- PATCH
- DELETE
- Headers
- Query Parameters
- Authentication
- File Upload
- File Download
- Error Handling
- Interceptors

______________________________________________________________________

# Communication Flow

```
Angular Component

↓

Service

↓

HttpClient

↓

REST API

↓

Backend

↓

Database

↓

JSON

↓

HttpClient

↓

Service

↓

Component

↓

Template
```

Notice

Components never talk directly to the backend.

______________________________________________________________________

# Where Should HttpClient Be Used?

Correct

```
Component

↓

Service

↓

HttpClient
```

Wrong

```
Component

↓

HttpClient
```

Keep networking inside services.

______________________________________________________________________

# Registering HttpClient

Modern Angular

```typescript
import {

    provideHttpClient

}

from "@angular/common/http";

bootstrapApplication(

    AppComponent,

    {

        providers: [

            provideHttpClient()

        ]

    }

);
```

This registers `HttpClient` for the application.

______________________________________________________________________

# Injecting HttpClient

```typescript
import {

    HttpClient

}

from "@angular/common/http";

@Injectable({

    providedIn: "root"

})

export class UserService {

    constructor(

        private http:

        HttpClient

    ) {}

}
```

Angular injects the service automatically.

______________________________________________________________________

# Base URL

Suppose backend

```
http://localhost:8080/api
```

Endpoints

```
/users

/orders

/products
```

Usually,

the base URL comes from environment configuration.

We'll cover environments later.

______________________________________________________________________

# GET Request

Fetch data.

```typescript
getUsers() {

    return this.http.get<User[]>(

        "/api/users"

    );

}
```

Notice

```
<User[]>
```

TypeScript knows

what the backend returns.

______________________________________________________________________

# GET Flow

```
Component

↓

UserService

↓

GET /api/users

↓

Backend

↓

JSON

↓

Observable<User[]>
```

______________________________________________________________________

# Backend Example

Spring Boot

```java
@GetMapping("/users")

public List<User> getUsers() {

}
```

Angular

```typescript
this.http.get<User[]>(

"/api/users"

)
```

______________________________________________________________________

# POST Request

Create data.

```typescript
createUser(

user: User

) {

    return this.http.post<User>(

        "/api/users",

        user

    );

}
```

Request

```json
{

"name":"Alice"

}
```

______________________________________________________________________

# PUT Request

Replace an entire resource.

```typescript
updateUser(

id:number,

user:User

){

return this.http.put<User>(

`/api/users/${id}`,

user

);

}
```

______________________________________________________________________

# PATCH Request

Update only changed fields.

```typescript
updateStatus(

id:number

){

return this.http.patch(

`/api/users/${id}`,

{

active:true

}

);

}
```

______________________________________________________________________

# PUT vs PATCH

PUT

```
Entire Object
```

PATCH

```
Partial Update
```

______________________________________________________________________

# DELETE Request

```typescript
deleteUser(

id:number

){

return this.http.delete(

`/api/users/${id}`

);

}
```

______________________________________________________________________

# HTTP Methods Summary

| Method | Purpose |
|----------|----------|
| GET | Read |
| POST | Create |
| PUT | Replace |
| PATCH | Partial Update |
| DELETE | Remove |

______________________________________________________________________

# Query Parameters

Example

```
GET

/api/users

?page=1

&size=20
```

Angular

```typescript
const params =

new HttpParams()

.set("page","1")

.set("size","20");

return this.http.get(

"/api/users",

{

params

}

);
```

______________________________________________________________________

# Headers

Example

```typescript
const headers =

new HttpHeaders()

.set(

"Authorization",

"Bearer token"

)

.set(

"X-App",

"Angular"

);

return this.http.get(

"/api/users",

{

headers

}

);
```

______________________________________________________________________

# Request Body

POST

```typescript
this.http.post(

"/api/users",

{

name:"Alice",

age:25

}

);
```

Angular converts the object to JSON automatically.

______________________________________________________________________

# Strongly Typed Responses

Bad

```typescript
getUsers(){

return this.http.get(

"/api/users"

);

}
```

Good

```typescript
getUsers(){

return this.http.get<User[]>(

"/api/users"

);

}
```

Always use Generics.

______________________________________________________________________

# Observable

Unlike

```typescript
fetch()
```

Angular returns

```
Observable
```

Example

```typescript
getUsers(){

return this.http.get<User[]>(

"/api/users"

);

}
```

Nothing happens until someone subscribes.

We'll learn RxJS in detail next.

______________________________________________________________________

# Calling the API

Component

```typescript
this.userService

.getUsers()

.subscribe(

users => {

this.users = users;

}

);
```

______________________________________________________________________

# Complete Flow

```
Component

↓

Service

↓

HttpClient

↓

Backend

↓

JSON

↓

Observable

↓

subscribe()

↓

Update UI
```

______________________________________________________________________

# Authentication

Suppose backend expects

```
Authorization:

Bearer JWT
```

Angular sends

```typescript
headers:

{

Authorization:

`Bearer ${token}`

}
```

Usually,

this is handled automatically by an interceptor.

______________________________________________________________________

# Login Example

POST

```
/login
```

↓

Backend

↓

JWT

↓

Angular stores token

↓

Future requests include

```
Authorization

Header
```

______________________________________________________________________

# File Upload

Angular

```typescript
const formData =

new FormData();

formData.append(

"file",

file

);

return this.http.post(

"/upload",

formData

);
```

Browser automatically sends

```
multipart/form-data
```

______________________________________________________________________

# File Download

```typescript
return this.http.get(

"/report",

{

responseType:

"blob"

}

);
```

Used for

- PDFs
- Excel
- Images

______________________________________________________________________

# Error Handling

Backend

```
404

500

401
```

Angular receives

```
HttpErrorResponse
```

Example

```typescript
.subscribe({

next:data=>{

},

error:error=>{

console.log(error);

}

});
```

______________________________________________________________________

# HttpErrorResponse

Contains

```
Status

Headers

Message

Body
```

Very useful for debugging.

______________________________________________________________________

# Retry

Sometimes

temporary failures happen.

RxJS

```typescript
retry(3)
```

tries the request again.

We'll cover this in the RxJS chapter.

______________________________________________________________________

# Timeout

Angular can also cancel long-running requests using RxJS operators such as

```
timeout()
```

______________________________________________________________________

# Cancellation

Suppose user

changes page

before API finishes.

Angular applications often cancel requests

to save resources.

This is commonly achieved using

```
switchMap

takeUntil

AbortController (where applicable)
```

______________________________________________________________________

# Interceptors

Instead of adding headers

to every request,

Angular provides

```
HttpInterceptor
```

Flow

```
Component

↓

Interceptor

↓

Backend

↓

Interceptor

↓

Component
```

Common uses

- JWT
- Logging
- Error Handling
- Refresh Token

Dedicated chapter later.

______________________________________________________________________

# Environment Configuration

Instead of

```typescript
"http://localhost:8080"
```

hardcoding,

use

```
environment.ts
```

Example

```typescript
apiUrl
```

This simplifies deployment.

______________________________________________________________________

# Typical Enterprise Service

```typescript
@Injectable({

providedIn:"root"

})

export class UserService {

constructor(

private http:

HttpClient

){}

getUsers(){

return this.http.get<User[]>(

"/api/users"

);

}

createUser(

user:User

){

return this.http.post(

"/api/users",

user

);

}

deleteUser(

id:number

){

return this.http.delete(

`/api/users/${id}`

);

}

}
```

Notice

The component never deals with HTTP directly.

______________________________________________________________________

# Backend Comparison

Python

```python
requests.get(...)
```

Java

```java
WebClient

.get()
```

Angular

```typescript
http.get()
```

All three

communicate with REST APIs.

______________________________________________________________________

# Common Mistakes

## API Calls Inside Components

Wrong

```
Component

↓

HttpClient
```

Always use services.

______________________________________________________________________

## Not Typing Responses

Avoid

```typescript
any
```

Prefer

```typescript
User[]

Order

Product
```

______________________________________________________________________

## Hardcoding URLs

Wrong

```
http://localhost...
```

Use environment configuration.

______________________________________________________________________

## Manually Adding JWT Everywhere

Use an interceptor.

______________________________________________________________________

# Best Practices

✅ Keep HTTP code inside services.

✅ Strongly type every response.

✅ Use interceptors for authentication.

✅ Keep base URLs in environment configuration.

✅ Handle errors gracefully.

✅ Return Observables from services.

______________________________________________________________________

# Interview Deep Dive

## Question

What is HttpClient?

### Answer

`HttpClient` is Angular's built-in service for communicating with backend APIs. It supports all common HTTP methods,
automatic JSON conversion, typed responses, interceptors, and integration with RxJS Observables.

______________________________________________________________________

## Question

Why should components not call HttpClient directly?

### Answer

Components should focus on the user interface. Keeping HTTP communication inside services improves reusability,
maintainability, and testing.

______________________________________________________________________

## Question

Why does HttpClient return an Observable instead of a Promise?

### Answer

Observables support multiple values over time, cancellation, composition with RxJS operators, and lazy execution, making
them well suited for Angular applications.

______________________________________________________________________

## Question

What is the difference between PUT and PATCH?

### Answer

PUT replaces an entire resource, while PATCH updates only the specified fields.

______________________________________________________________________

## Question

What are HTTP interceptors used for?

### Answer

Interceptors allow developers to inspect or modify every HTTP request and response. They are commonly used for
authentication, logging, error handling, and refresh-token logic.

______________________________________________________________________

# Practice Questions

1. What is HttpClient?
1. Why should services use HttpClient instead of components?
1. What HTTP methods does HttpClient support?
1. Why should responses be strongly typed?
1. What is the difference between PUT and PATCH?
1. How are query parameters added?
1. How are custom headers sent?
1. How does Angular upload files?
1. Why does HttpClient return an Observable?
1. What is the purpose of an HTTP interceptor?

______________________________________________________________________

# Summary

`HttpClient` is Angular's gateway to backend APIs.

In this chapter, you learned:

- HttpClient
- GET
- POST
- PUT
- PATCH
- DELETE
- Query parameters
- Headers
- Request bodies
- Strong typing
- Observables
- Authentication
- File upload
- File download
- Error handling
- Interceptors
- Enterprise service structure
- Best practices

At this point, you've seen that `HttpClient` returns **Observables**, but we haven't explored what they are or why
Angular relies on them. The next chapter is dedicated to **RxJS**, where you'll learn Observables, Subjects,
BehaviorSubjects, operators like `map`, `switchMap`, and `forkJoin`, and how they power asynchronous programming
throughout Angular.

______________________________________________________________________

# Next

[RxJS](12-rxjs.md)

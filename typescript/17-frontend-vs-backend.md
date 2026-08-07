# Frontend vs Backend Programming

If you've primarily worked with Python (FastAPI) or Java (Spring Boot), one of the biggest questions during interviews
is:

> **"How is frontend development different from backend development?"**

This chapter explains:

- What frontend and backend really mean
- Who executes the code
- How requests travel
- Browser vs Server
- JavaScript vs TypeScript vs Java vs Python
- Build process
- Runtime
- Communication between frontend and backend

This is one of the most useful conceptual topics for backend engineers.

______________________________________________________________________

# What is Frontend?

Frontend is everything the user can **see and interact with**.

Examples

- Login page
- Dashboard
- Buttons
- Tables
- Charts
- Forms
- Navigation

Frontend runs on the **user's machine**.

______________________________________________________________________

# What is Backend?

Backend is everything that happens **behind the scenes**.

Examples

- Authentication
- Business logic
- Database queries
- Payment processing
- Sending emails
- File uploads
- API creation

Backend runs on **servers**.

______________________________________________________________________

# Overall Architecture

```
User

↓

Browser

↓

Frontend

↓

HTTP Request

↓

Backend API

↓

Database
```

Response

```
Database

↓

Backend

↓

JSON

↓

Frontend

↓

Browser
```

______________________________________________________________________

# Who Executes the Program?

## Frontend

Runs inside

```
Browser
```

Examples

- Chrome
- Edge
- Firefox
- Safari

The browser executes the frontend application.

______________________________________________________________________

## Backend

Runs inside

```
Server
```

Examples

- EC2
- Docker Container
- Kubernetes Pod
- Virtual Machine

The server executes backend code.

______________________________________________________________________

# Browser vs Server

| Browser | Server |
|----------|---------|
| User's computer | Remote machine |
| Executes frontend | Executes backend |
| Renders UI | Processes requests |
| Displays HTML | Returns data |
| Has DOM | No DOM |

______________________________________________________________________

# Frontend Languages

Most frontend applications use

```
HTML

CSS

JavaScript

TypeScript
```

Frameworks

- React
- Angular
- Vue
- Svelte

______________________________________________________________________

# Backend Languages

Examples

- Java
- Python
- Go
- Node.js (JavaScript/TypeScript)
- C#
- Kotlin
- Rust

Frameworks

- Spring Boot
- FastAPI
- Express
- NestJS
- Django
- ASP.NET

______________________________________________________________________

# Important Difference

Frontend language

↓

Runs inside browser

Backend language

↓

Runs inside server

______________________________________________________________________

# Does Browser Understand TypeScript?

No.

Browser understands only

```
JavaScript
```

Example

```
TypeScript

↓

Compiler

↓

JavaScript

↓

Browser
```

______________________________________________________________________

# Does Browser Understand Java?

No.

Java code

```
Java

↓

javac

↓

Bytecode

↓

JVM

↓

Server
```

Browser cannot execute Java backend code.

______________________________________________________________________

# Does Browser Understand Python?

No.

Python runs using

```
Python Interpreter
```

on the server.

______________________________________________________________________

# Who Executes JavaScript?

```
Browser

↓

JavaScript Engine
```

Examples

Chrome

```
V8 Engine
```

Firefox

```
SpiderMonkey
```

Safari

```
JavaScriptCore
```

______________________________________________________________________

# Who Executes Node.js?

Node.js also uses

```
V8 Engine
```

But

```
Browser

↓

V8

↓

UI
```

vs

```
Node.js

↓

V8

↓

Server
```

Same language.

Different environment.

______________________________________________________________________

# JavaScript Can Run in Two Places

```
Browser

OR

Node.js
```

This is unique.

JavaScript is the primary language that commonly runs on both frontend and backend.

______________________________________________________________________

# HTML

Purpose

```
Structure
```

Example

```html
<h1>Hello</h1>
```

______________________________________________________________________

# CSS

Purpose

```
Styling
```

Example

```css
h1 {

    color: blue;

}
```

______________________________________________________________________

# JavaScript

Purpose

```
Behavior
```

Example

```javascript
button.onclick = () => {

    alert("Clicked");

};
```

______________________________________________________________________

# TypeScript

Purpose

```
JavaScript

+

Static Typing
```

Compiled into JavaScript before execution.

______________________________________________________________________

# Java

Purpose

```
Backend

Business Logic

Enterprise APIs
```

Runs on JVM.

______________________________________________________________________

# Python

Purpose

- APIs
- AI
- Automation
- Data Science

Runs on Python Interpreter.

______________________________________________________________________

# How a Request Travels

Suppose user clicks

```
Login
```

Flow

```
User

↓

Button Click

↓

Frontend

↓

POST /login

↓

Backend

↓

Validate User

↓

Database

↓

JWT Token

↓

Frontend

↓

Store Token

↓

Dashboard
```

______________________________________________________________________

# Example

Frontend

```typescript
await fetch(

    "/api/users"

);
```

Backend

```typescript
app.get(

"/api/users",

(req,res)=>{

res.json(users);

});
```

Browser never talks directly to the database.

______________________________________________________________________

# Why?

Security.

Imagine

```
Browser

↓

Database
```

Anyone could access your database.

Instead

```
Browser

↓

Backend

↓

Database
```

Backend validates every request.

______________________________________________________________________

# Browser Responsibilities

- Render HTML
- Execute JavaScript
- Store cookies
- Store localStorage
- Display images
- Handle user input
- Call APIs

______________________________________________________________________

# Backend Responsibilities

- Authentication
- Authorization
- Validation
- Business Logic
- Database
- Logging
- Security
- Caching

______________________________________________________________________

# Can Frontend Access Database?

Usually

```
NO
```

Correct

```
Frontend

↓

API

↓

Database
```

______________________________________________________________________

# API

API is the bridge.

```
Frontend

↓

HTTP

↓

Backend
```

Common formats

```
JSON

XML
```

Today,

JSON is the standard.

______________________________________________________________________

# Browser Storage

Frontend can store

- Local Storage
- Session Storage
- Cookies

Backend stores

- Database
- Redis
- Files
- Object Storage

______________________________________________________________________

# Build Process

Frontend

```
TypeScript

↓

Vite/Webpack

↓

JavaScript

↓

Browser
```

______________________________________________________________________

Backend

Java

```
Java

↓

javac

↓

Bytecode

↓

JVM
```

______________________________________________________________________

Python

```
Python

↓

Interpreter

↓

Server
```

______________________________________________________________________

Node.js

```
TypeScript

↓

tsc

↓

JavaScript

↓

Node.js
```

______________________________________________________________________

# Frontend Frameworks

React

```
Components
```

Angular

```
Full Framework
```

Vue

```
Progressive
```

______________________________________________________________________

# Backend Frameworks

Java

↓

Spring Boot

Python

↓

FastAPI

Node.js

↓

Express

NestJS

______________________________________________________________________

# Rendering

Frontend

```
Render UI
```

Backend

```
Generate Data
```

Example

Backend

```json
{

    "name":"Alice"

}
```

Frontend

```
Alice

(Profile Card)

(Button)

(Image)
```

______________________________________________________________________

# State

Frontend

Maintains UI state.

Example

```
Dark Mode

Selected Tab

Shopping Cart
```

Backend

Maintains application state.

Example

```
Orders

Payments

Users

Sessions
```

______________________________________________________________________

# Authentication Example

Frontend

```
User enters password
```

↓

Backend

```
Verify Password
```

↓

Database

↓

JWT

↓

Frontend stores token

↓

Future requests

Authorization header

↓

Backend validates

```

---

# Common Interview Question

**Can JavaScript be used for backend development?**

Yes.

Node.js allows JavaScript (and compiled TypeScript) to run on the server using the V8 engine.

---

# Frontend vs Backend

| Frontend | Backend |
|----------|---------|
| Runs in browser | Runs on server |
| User Interface | Business Logic |
| HTML/CSS/JS | Java, Python, Go, Node.js |
| Calls APIs | Creates APIs |
| Handles clicks | Handles requests |
| Displays data | Produces data |
| Limited file access | Full server access |
| No direct DB access | Database access |

---

# Real Example

Food Delivery App

Frontend

- Home Page
- Restaurant List
- Search
- Cart
- Checkout Screen

Backend

- Login
- Restaurant Service
- Payment
- Order Creation
- Inventory
- Notifications

---

# Common Mistakes

## Thinking TypeScript Runs in Browser

Wrong

```

TypeScript

↓

Browser

```

Correct

```

TypeScript

↓

JavaScript

↓

Browser

```

---

## Thinking Browser Can Execute Java

Wrong.

Java backend code runs on a server with the JVM.

---

## Thinking Frontend Talks Directly to Database

Production applications almost always communicate through backend APIs.

---

## Confusing Node.js with Browser JavaScript

Both use JavaScript,

but their available APIs are different.

For example:

Browser

- `document`
- `window`
- `localStorage`

Node.js

- `fs`
- `path`
- `http`
- `process`

---

# Best Practices

✅ Keep frontend focused on presentation and user interaction.

✅ Keep business logic in the backend.

✅ Never expose database credentials to the frontend.

✅ Use APIs as the communication layer.

✅ Validate data on the backend, even if the frontend also validates it.

---

# Interview Deep Dive

## Question

Who executes frontend code?

### Answer

Frontend code is executed by the user's browser. HTML is rendered by the browser, CSS is applied for styling, and JavaScript is executed by the browser's JavaScript engine (such as V8 in Chrome).

---

## Question

Who executes backend code?

### Answer

Backend code runs on servers. Depending on the language, it is executed by a runtime such as the JVM (Java), the Python interpreter (Python), or Node.js (JavaScript/TypeScript).

---

## Question

Why can't the frontend connect directly to the database?

### Answer

Allowing direct database access from the browser would expose credentials and bypass authentication, authorization, validation, and business rules. Backend APIs act as a secure layer between clients and the database.

---

## Question

How do the frontend and backend communicate?

### Answer

They communicate using HTTP or HTTPS. The frontend sends requests to backend APIs, and the backend returns responses, typically in JSON format.

---

## Question

Can JavaScript run on both the frontend and backend?

### Answer

Yes. In the browser, JavaScript runs inside the browser's JavaScript engine to power user interactions. On the backend, Node.js uses the V8 engine to execute JavaScript outside the browser, enabling server-side applications.

---

# Practice Questions

1. What is the difference between frontend and backend?
2. Who executes frontend code?
3. Who executes backend code?
4. Why can't browsers execute Java or Python backend code?
5. Why is TypeScript compiled before execution?
6. How does the frontend communicate with the backend?
7. Why shouldn't the frontend access the database directly?
8. What is Node.js, and how is it different from browser JavaScript?
9. What are the responsibilities of the frontend and backend?
10. Explain the complete lifecycle of an API request from button click to database and back.

---

# Summary

Frontend and backend applications solve different problems but work together to deliver a complete user experience.

- The **frontend** runs in the browser and focuses on user interaction and presentation.
- The **backend** runs on servers and focuses on business logic, security, and data management.
- APIs connect the two worlds.
- Understanding where code executes, how it is built, and how requests flow is fundamental for every backend engineer.

---

# Summary

TypeScript and Java share many object-oriented concepts, but they target different runtimes and solve problems in different ways.

- **TypeScript** emphasizes rapid development, flexibility, and excellent support for asynchronous I/O on the JavaScript ecosystem.
- **Java** emphasizes strong runtime capabilities, mature enterprise tooling, and powerful multi-threading on the JVM.

Understanding both languages makes it much easier to transition between modern backend ecosystems and answer cross-language interview questions with confidence.

```

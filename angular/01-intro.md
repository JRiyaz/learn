# Web Fundamentals & Angular Introduction

Before learning Angular, it's important to understand **how the web works**.

Many developers jump directly into components, services, and routing without understanding what actually happens when a
user opens a website.

Once you understand these fundamentals, Angular becomes much easier to learn.

______________________________________________________________________

# How Does the Internet Work?

Imagine you type

```
https://www.amazon.com
```

into your browser.

What happens?

```
Browser

↓

DNS Lookup

↓

Find Server IP

↓

TCP Connection

↓

HTTPS Handshake

↓

HTTP Request

↓

Backend Server

↓

HTML / CSS / JavaScript

↓

Browser

↓

Render Web Page
```

Although this entire process usually takes only a few hundred milliseconds, several things happen behind the scenes.

______________________________________________________________________

# What Happens When You Press Enter?

Let's break it down.

```
User

↓

Types URL

↓

Browser

↓

DNS

↓

Server

↓

Response

↓

Browser

↓

Render Page
```

______________________________________________________________________

## Step 1 - URL

Example

```
https://www.google.com
```

This contains

- Protocol
- Domain
- Path

Example

```
https://api.example.com/users

│

├── https

├── api.example.com

└── /users
```

______________________________________________________________________

## Step 2 - DNS Lookup

Humans remember

```
google.com
```

Computers understand

```
142.250.xxx.xxx
```

DNS converts

```
google.com

↓

IP Address
```

Think of DNS as the Internet's phone book.

______________________________________________________________________

## Step 3 - TCP Connection

Once the browser knows the server's IP address,

it establishes a connection.

```
Browser

↓

Server
```

A reliable communication channel is created using TCP.

______________________________________________________________________

## Step 4 - HTTPS Handshake

If the website uses HTTPS,

the browser and server perform a secure handshake.

Purpose

- Encryption
- Authentication
- Secure communication

After this,

all communication is encrypted.

______________________________________________________________________

## Step 5 - HTTP Request

The browser sends a request.

Example

```
GET /

Host: example.com
```

The server receives the request.

______________________________________________________________________

## Step 6 - Backend Processing

The backend may

- Authenticate user
- Validate request
- Query database
- Perform business logic
- Generate response

Example

```
Browser

↓

GET /users

↓

Backend

↓

Database

↓

JSON
```

______________________________________________________________________

## Step 7 - Response

The server returns

- HTML
- CSS
- JavaScript
- Images
- JSON

depending on the request.

______________________________________________________________________

## Step 8 - Browser Rendering

Browser receives

```
HTML

↓

CSS

↓

JavaScript
```

and starts rendering.

______________________________________________________________________

# Browser Architecture

A browser is much more than a window displaying websites.

```
Browser

├── UI

├── Browser Engine

├── Rendering Engine

├── JavaScript Engine

├── Networking

├── Storage
```

Each part has a different responsibility.

______________________________________________________________________

# Browser UI

Responsible for

- Address bar
- Tabs
- Back button
- Forward button
- Bookmarks

This is **not** part of your Angular application.

______________________________________________________________________

# Browser Engine

Coordinates communication between browser components.

Think of it as the manager of the browser.

______________________________________________________________________

# Rendering Engine

Responsible for displaying the webpage.

Popular rendering engines

| Browser | Rendering Engine |
|----------|------------------|
| Chrome | Blink |
| Edge | Blink |
| Safari | WebKit |
| Firefox | Gecko |

______________________________________________________________________

# JavaScript Engine

Executes JavaScript.

Popular engines

| Browser | Engine |
|----------|---------|
| Chrome | V8 |
| Edge | V8 |
| Firefox | SpiderMonkey |
| Safari | JavaScriptCore |

Angular eventually becomes JavaScript,

and this engine executes it.

______________________________________________________________________

# HTML

HTML provides

```
Structure
```

Example

```html
<h1>Hello</h1>

<button>Login</button>
```

Without HTML,

there is nothing to display.

______________________________________________________________________

# CSS

CSS provides

```
Styling
```

Example

```css
h1 {

    color: blue;

}

button {

    background: green;

}
```

______________________________________________________________________

# JavaScript

JavaScript provides

```
Behavior
```

Example

```javascript
button.onclick = () => {

    alert("Welcome");

};
```

Without JavaScript,

web pages would mostly be static.

______________________________________________________________________

# DOM

DOM stands for

```
Document Object Model
```

The browser converts HTML into a tree.

Example

```html
<body>

    <h1>Hello</h1>

    <button>Login</button>

</body>
```

becomes

```
body

├── h1

└── button
```

JavaScript modifies the DOM.

______________________________________________________________________

# Rendering Pipeline

When a webpage loads,

the browser performs several steps.

```
Receive HTML

↓

Parse HTML

↓

Build DOM

↓

Load CSS

↓

Build CSSOM

↓

Combine

↓

Render Tree

↓

Layout

↓

Paint

↓

Display
```

Understanding this helps explain why Angular updates only parts of a page instead of reloading everything.

______________________________________________________________________

# What is the DOM?

Imagine

```html
<h1>Hello</h1>
```

Browser converts it into an object.

JavaScript can then do

```javascript
document.querySelector("h1")
```

or

```javascript
document.getElementById(...)
```

Angular manipulates the DOM for you.

______________________________________________________________________

# Event Loop (High Level)

JavaScript executes on a single thread.

How can it handle

- API calls
- Timers
- User clicks

simultaneously?

Using the Event Loop.

```
Call Stack

↓

Web APIs

↓

Callback Queue

↓

Event Loop

↓

Call Stack
```

We'll revisit this when learning RxJS.

______________________________________________________________________

# Browser Storage

Browsers provide several storage mechanisms.

```
Browser

├── Cookies

├── Local Storage

├── Session Storage

└── IndexedDB
```

______________________________________________________________________

# Cookies

Small pieces of data.

Typically used for

- Authentication
- Session IDs
- User preferences

Automatically sent with HTTP requests (subject to cookie settings).

______________________________________________________________________

# Local Storage

Stores data permanently.

Example

```
Theme

JWT Token (sometimes)

Language Preference
```

Data remains after browser restart.

______________________________________________________________________

# Session Storage

Similar to Local Storage,

but cleared when the browser tab is closed.

______________________________________________________________________

# IndexedDB

A browser database.

Used for

- Offline applications
- Large datasets
- Progressive Web Apps

Angular applications rarely use it directly,

but libraries often do.

______________________________________________________________________

# Client vs Server

One of the most important concepts.

```
Client

↓

Request

↓

Server

↓

Response
```

Client

Usually the browser.

Server

Runs backend code.

______________________________________________________________________

# Frontend Responsibilities

Frontend handles

- UI
- Forms
- Buttons
- Navigation
- User interaction
- Displaying data
- Calling backend APIs

______________________________________________________________________

# Backend Responsibilities

Backend handles

- Authentication
- Authorization
- Business Logic
- Database
- Emails
- Payments
- Security
- Logging

______________________________________________________________________

# Why Doesn't the Browser Talk Directly to the Database?

Imagine

```
Browser

↓

Database
```

Anyone could

- Delete data
- Modify records
- Read confidential information

Instead

```
Browser

↓

Backend API

↓

Database
```

The backend validates every request before accessing the database.

______________________________________________________________________

# REST APIs

Frontend and backend communicate through APIs.

Example

```
Browser

↓

GET /users

↓

Backend

↓

JSON

↓

Browser
```

Angular almost always communicates using JSON APIs.

______________________________________________________________________

# Request-Response Lifecycle

```
User Clicks Button

↓

Angular

↓

HTTP Request

↓

Backend

↓

Database

↓

JSON Response

↓

Angular

↓

Update UI
```

This cycle happens constantly in modern web applications.

______________________________________________________________________

# Where Does Angular Fit?

Without Angular

```
Browser

↓

HTML

↓

Display
```

With Angular

```
Browser

↓

Load Angular

↓

Execute JavaScript

↓

Create Components

↓

Update DOM

↓

Display UI
```

Angular acts as a layer between the browser and the DOM.

______________________________________________________________________

# Browser vs Backend Runtime

Browser

```
HTML

↓

CSS

↓

JavaScript
```

Backend

```
Java

↓

JVM
```

or

```
Python

↓

Interpreter
```

or

```
Node.js

↓

JavaScript
```

Different runtimes execute different languages.

______________________________________________________________________

# Browser Responsibilities vs Backend Responsibilities

| Browser | Backend |
|----------|----------|
| Display UI | Business Logic |
| Execute JavaScript | Execute Java, Python, Node.js, etc. |
| Handle user interaction | Process requests |
| Call APIs | Build APIs |
| Render HTML | Query database |
| Store cookies/local storage | Store data permanently |

______________________________________________________________________

# Common Mistakes

## Thinking the Browser Executes Java

Wrong.

Java backend code runs on the server using the JVM.

______________________________________________________________________

## Thinking HTML Is Programming

HTML defines structure.

JavaScript provides behavior.

______________________________________________________________________

## Thinking Angular Replaces the Browser

Angular runs **inside** the browser.

The browser still performs rendering, networking, and JavaScript execution.

______________________________________________________________________

## Thinking the Frontend Can Safely Access the Database

Production applications always communicate through backend APIs.

______________________________________________________________________

# Best Practices

✅ Understand how browsers render pages.

✅ Know the difference between client and server.

✅ Understand the request-response lifecycle.

✅ Keep business logic on the backend.

✅ Use APIs for communication between frontend and backend.

______________________________________________________________________

# Interview Deep Dive

## Question

What happens when you type a URL into a browser?

### Answer

The browser performs a DNS lookup to resolve the domain name into an IP address, establishes a TCP connection,
negotiates HTTPS if required, sends an HTTP request, receives the response from the server, parses HTML, CSS, and
JavaScript, builds the DOM, and renders the page.

______________________________________________________________________

## Question

What is the DOM?

### Answer

The DOM (Document Object Model) is the browser's object representation of an HTML document. JavaScript and frameworks
like Angular manipulate the DOM to update the user interface dynamically.

______________________________________________________________________

## Question

What is the role of the JavaScript engine?

### Answer

The JavaScript engine executes JavaScript code. Different browsers use different engines, such as V8 in Chrome and
SpiderMonkey in Firefox.

______________________________________________________________________

## Question

Why shouldn't the frontend connect directly to the database?

### Answer

Direct database access would expose credentials and bypass authentication, authorization, validation, and business
rules. Backend APIs act as a secure layer between clients and databases.

______________________________________________________________________

## Question

Where does Angular run?

### Answer

Angular runs inside the user's browser after being compiled into JavaScript. It executes using the browser's JavaScript
engine and updates the DOM to create a dynamic user interface.

______________________________________________________________________

# Practice Questions

1. What happens when you enter a URL into the browser?
1. What is DNS?
1. What is the purpose of HTTPS?
1. What is the DOM?
1. What is the rendering pipeline?
1. What is the role of the JavaScript engine?
1. What are the responsibilities of the frontend?
1. What are the responsibilities of the backend?
1. Why do frontend applications communicate with backend APIs?
1. Where does Angular execute?

______________________________________________________________________

# Summary

Before learning Angular, it's essential to understand how the web works.

In this chapter, you learned:

- How browsers communicate with servers
- DNS, TCP, and HTTPS (high level)
- Browser architecture
- HTML, CSS, and JavaScript roles
- DOM
- Rendering pipeline
- Browser storage
- Client vs Server
- Frontend vs Backend responsibilities
- REST APIs
- Request-response lifecycle
- Where Angular fits into the web architecture

These concepts form the foundation for understanding **Single Page Applications (SPA)**, which we'll cover next.

______________________________________________________________________

# Next

[Single Page Application](02-single-page-application.md)

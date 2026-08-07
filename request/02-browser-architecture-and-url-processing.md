# Complete HTTP Request Lifecycle Deep Dive

## 02. Browser Architecture and URL Processing

> Target Audience: Backend Engineers (Beginner → Senior)
>
> Goal: Understand what happens **inside the browser** immediately after a user enters a URL and presses Enter.

______________________________________________________________________

# Introduction

Everything begins

here.

```
User

↓

Chrome

↓

Type URL

↓

Press Enter
```

Many engineers think

the browser

simply sends

an HTTP request.

In reality,

the browser performs

dozens of operations

before

even creating

the first network packet.

______________________________________________________________________

# Browser Architecture

Modern browsers

are

operating systems

for web applications.

Chrome

contains

multiple processes.

```
                Chrome Browser

                      │

 ┌────────────────────┼────────────────────┐

 ▼                    ▼                    ▼

Browser Process   Renderer Process   GPU Process

                      │

                      ▼

              Network Process

                      │

                      ▼

              Utility Processes
```

______________________________________________________________________

# Why Multiple Processes?

Years ago,

browsers

used

one process.

Problem

```
One Tab Crashes

↓

Entire Browser Crashes
```

Modern browsers

isolate

tabs

into

different processes.

Benefits

- Stability
- Security
- Better Performance

______________________________________________________________________

# Browser Process

The Browser Process

is the

main controller.

Responsibilities

- Address bar
- Navigation
- Tabs
- Bookmarks
- Downloads
- History
- Process Management

Think of it as

the

"Operating System"

of the browser.

______________________________________________________________________

# Renderer Process

Each tab

normally gets

its own

Renderer Process.

Responsibilities

- HTML Parsing
- CSS Parsing
- JavaScript Execution
- DOM
- Rendering

When you visit

```
google.com
```

its page

is rendered

inside

a Renderer Process.

______________________________________________________________________

# Network Process

Interview favorite.

The Network Process

handles

everything related to

network communication.

Responsibilities

- DNS Lookup
- TCP
- TLS
- HTTP Requests
- Cookies
- Cache
- Proxy
- Downloads

The Renderer

does NOT

directly

open sockets.

______________________________________________________________________

# GPU Process

Responsible for

graphics.

Examples

- Animations
- CSS Effects
- Video
- Rendering
- WebGL

Without GPU acceleration,

modern websites

would feel

slow.

______________________________________________________________________

# Utility Processes

Perform

background tasks.

Examples

- Audio
- Video Decoding
- PDF Viewer
- Storage
- Extensions

______________________________________________________________________

# Multi-Process Architecture

Example

```
Chrome

↓

Browser Process

↓

Tab 1

↓

Renderer 1

↓

Google
```

```
Tab 2

↓

Renderer 2

↓

YouTube
```

```
Tab 3

↓

Renderer 3

↓

GitHub
```

Each tab

is isolated.

______________________________________________________________________

# User Types A URL

Example

```
https://www.google.com/search?q=python
```

The browser

must first

understand

this text.

______________________________________________________________________

# URL Parsing

The browser

breaks

the URL

into

multiple parts.

```
https://www.google.com/search?q=python#top
```

↓

```
Protocol

https
```

```
Host

www.google.com
```

```
Port

443
```

```
Path

/search
```

```
Query

q=python
```

```
Fragment

top
```

______________________________________________________________________

# URL Components

## Protocol

Determines

how

communication happens.

Examples

```
http
```

```
https
```

```
ftp
```

```
ws
```

```
wss
```

______________________________________________________________________

## Host

The hostname

identifies

the server.

Example

```
www.google.com
```

The browser

still doesn't know

its IP address.

DNS

will solve that later.

______________________________________________________________________

## Port

If omitted,

default ports

are used.

```
HTTP

80
```

```
HTTPS

443
```

______________________________________________________________________

## Path

Example

```
/search
```

Represents

the resource

being requested.

______________________________________________________________________

## Query Parameters

Everything

after

```
?
```

Example

```
q=python
```

Multiple values

```
page=2

&sort=price
```

______________________________________________________________________

## Fragment

Everything

after

```
#
```

Example

```
#section1
```

Interesting fact

Fragments

are

NOT sent

to the server.

They are

used

only

inside

the browser.

______________________________________________________________________

# URL Validation

Before

sending

any request,

the browser

checks

whether

the URL

is valid.

Examples

```
https://google.com
```

Valid

______________________________________________________________________

```
ht!tp://google
```

Invalid

______________________________________________________________________

# Browser History Check

Interview bonus.

Browser checks

whether

this page

already exists

in history.

Possible actions

- Back Navigation
- Forward Navigation
- Cached Page
- Fresh Request

______________________________________________________________________

# Service Worker Check

Modern browsers

check

whether

a Service Worker

is registered.

```
Request

↓

Service Worker

↓

Network?
```

Sometimes

the browser

never contacts

the server.

The Service Worker

returns

cached content.

Example

Offline Gmail.

______________________________________________________________________

# Browser Cache Check

Interview favorite.

Before

sending

a network request,

the browser

checks

its local cache.

```
Request

↓

Browser Cache

↓

Found?

↓

Return Cached Copy
```

If cache

is valid,

no network

is required.

______________________________________________________________________

# Cache Types

Browser

contains

multiple caches.

Examples

- Memory Cache
- Disk Cache
- Image Cache
- DNS Cache

______________________________________________________________________

# Cookies

Browser

loads

cookies

for

the domain.

Example

```
google.com
```

Cookies

may contain

- Session ID
- Authentication
- Preferences
- Language

These cookies

will later

be attached

to

the HTTP request.

______________________________________________________________________

# Local Storage

Browser

may access

```
localStorage
```

Contains

persistent

application data.

Example

```
Theme

Language

Settings
```

Not automatically

sent

to the server.

______________________________________________________________________

# Session Storage

Similar

to

Local Storage

but

exists

only

for

the current tab.

Closing

the tab

removes it.

______________________________________________________________________

# IndexedDB

Large

browser database.

Stores

offline data.

Examples

- Gmail
- Notion
- Figma

Can store

hundreds of MB

inside

the browser.

______________________________________________________________________

# Same-Origin Policy

Interview favorite.

Browser

checks

whether

JavaScript

can access

the target.

Origin

consists of

```
Protocol

+

Host

+

Port
```

Example

```
https://google.com
```

Different from

```
https://mail.google.com
```

Different origin.

______________________________________________________________________

# Mixed Content Check

Suppose

page

uses

HTTPS

but loads

```
http://image.com
```

Browser

may block

the request.

Reason

Security.

______________________________________________________________________

# HSTS Check

If

the domain

supports

HSTS,

browser

automatically upgrades

```
http

↓

https
```

before

sending

the request.

______________________________________________________________________

# Browser Security Checks

Browser

also performs

- Safe Browsing
- Certificate Preload List
- CSP Checks
- Extension Policies

before

network communication.

______________________________________________________________________

# What Happens Internally?

Let's zoom in.

```
User Presses Enter

↓

Browser Process

↓

Parse URL

↓

Validate URL

↓

History Check

↓

Service Worker Check

↓

Browser Cache Check

↓

Load Cookies

↓

Security Checks

↓

Create Navigation Request

↓

Send To Network Process
```

Notice

no network request

has happened

yet.

______________________________________________________________________

# Technologies Used

| Component | Technology |
|------------|------------|
| Browser | Chrome, Firefox, Safari, Edge |
| Rendering Engine | Blink, Gecko, WebKit |
| JavaScript Engine | V8, SpiderMonkey |
| Storage | LocalStorage, IndexedDB |
| Cache | Memory Cache, Disk Cache |
| Service Worker | PWA APIs |
| Security | HSTS, CSP, Same-Origin Policy |

______________________________________________________________________

# Common Attacks

## Malicious URL

Example

```
https://google.com.fake.com
```

Looks legitimate

but isn't.

______________________________________________________________________

## Homograph Attack

Example

Uses

Unicode characters

that resemble

English letters.

```
gооgle.com
```

The "o"

may actually

be

a Cyrillic character.

______________________________________________________________________

## Phishing

User believes

they are visiting

their bank.

Actually

the browser

opens

an attacker's website.

______________________________________________________________________

## Open Redirect

A trusted website

redirects users

to

an attacker-controlled

website.

______________________________________________________________________

# Best Practices

✅ Always use HTTPS.

✅ Verify domain names carefully.

✅ Enable HSTS.

✅ Avoid clicking suspicious links.

✅ Validate URLs before redirecting users.

______________________________________________________________________

# Common Interview Questions

## Why does Chrome use multiple processes?

Using separate processes isolates tabs and browser components, improving stability, security, and performance. If one
renderer crashes, the rest of the browser continues running.

______________________________________________________________________

## Why isn't the Renderer Process responsible for networking?

Chrome separates rendering and networking for security and architecture. The Network Process manages sockets, DNS, TLS,
cookies, proxies, and HTTP communication.

______________________________________________________________________

## What parts of a URL are sent to the server?

The protocol determines the connection, while the host, path, query parameters, headers, and body participate in the
request. The fragment (`#...`) is **never sent** to the server; it is handled entirely by the browser.

______________________________________________________________________

## Can a browser return a page without contacting the server?

Yes. Browser cache or a Service Worker may satisfy the request locally, avoiding any network communication.

______________________________________________________________________

# Interview Deep Dive

## Question

After pressing Enter, what is the first thing the browser does?

### Answer

The browser parses and validates the URL, checks browser history, service workers, browser cache, cookies, and security
policies before handing the navigation request to the Network Process. Only after these steps does it begin DNS
resolution and network communication.

______________________________________________________________________

# Summary

Before any packet leaves your computer, the browser has already performed many operations:

- Parsed the URL
- Validated the address
- Checked browser history
- Looked for a Service Worker
- Checked local cache
- Loaded cookies
- Applied security policies
- Prepared the request for the Network Process

Understanding these browser internals helps explain why requests sometimes never reach your backend at all.

______________________________________________________________________

# Next

[03. DNS Resolution Deep Dive](03-dns-resolution-deep-dive.md)

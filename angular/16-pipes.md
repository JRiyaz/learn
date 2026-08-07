# Pipes

Angular applications often receive data from the backend in a format that is **not suitable for displaying directly**.

For example,

Backend returns

```json
{

"name":"riyaz",

"salary":50000,

"createdAt":"2026-08-07T12:30:00Z"

}
```

The UI should display

```
Riyaz

₹50,000.00

07 Aug 2026
```

Instead of modifying the data itself,

Angular uses **Pipes**.

______________________________________________________________________

# What is a Pipe?

A Pipe transforms data

```
Before Displaying It
```

Think of it as

```
Original Data

↓

Pipe

↓

Formatted Data
```

The original object remains unchanged.

______________________________________________________________________

# Why Pipes?

Suppose

Component

```typescript
user = {

    name: "riyaz",

    salary: 50000

};
```

Instead of writing formatting logic

inside every component,

Angular provides reusable pipes.

______________________________________________________________________

# Pipe Syntax

```html
{{ value | pipeName }}
```

Example

```html
{{ username | uppercase }}
```

Output

```
RIYAZ
```

______________________________________________________________________

# Pipe Flow

```
Backend

↓

Component

↓

Pipe

↓

Formatted Value

↓

Browser
```

______________________________________________________________________

# Built-in Pipes

Angular includes several useful pipes.

```
uppercase

lowercase

titlecase

date

currency

decimal

percent

slice

json

async

keyvalue
```

______________________________________________________________________

# UpperCasePipe

Component

```typescript
name = "riyaz";
```

Template

```html
{{ name | uppercase }}
```

Output

```
RIYAZ
```

______________________________________________________________________

# LowerCasePipe

```html
{{ name | lowercase }}
```

Output

```
riyaz
```

______________________________________________________________________

# TitleCasePipe

```typescript
title =

"angular crash course";
```

Template

```html
{{ title | titlecase }}
```

Output

```
Angular Crash Course
```

______________________________________________________________________

# DatePipe

Suppose backend returns

```typescript
createdAt =

new Date();
```

Template

```html
{{ createdAt | date }}
```

Output

```
Aug 7, 2026
```

______________________________________________________________________

# Date Formats

```html
{{ date | date:'short' }}
```

```
8/7/26, 10:30 AM
```

______________________________________________________________________

```html
{{ date | date:'medium' }}
```

```
Aug 7, 2026, 10:30:00 AM
```

______________________________________________________________________

```html
{{ date | date:'longDate' }}
```

```
August 7, 2026
```

______________________________________________________________________

Custom format

```html
{{ date | date:'dd/MM/yyyy' }}
```

Output

```
07/08/2026
```

______________________________________________________________________

# CurrencyPipe

Component

```typescript
salary =

50000;
```

Template

```html
{{ salary | currency }}
```

Output

```
$50,000.00
```

______________________________________________________________________

Specify Currency

```html
{{ salary |

currency:'INR'
}}
```

Output

```
₹50,000.00
```

______________________________________________________________________

Another Example

```html
{{ salary |

currency:'USD'
}}
```

Output

```
$50,000.00
```

______________________________________________________________________

# DecimalPipe

```typescript
value =

1234.56789;
```

Template

```html
{{ value |

number:'1.2-2'
}}
```

Output

```
1,234.57
```

______________________________________________________________________

# PercentPipe

Component

```typescript
progress =

0.85;
```

Template

```html
{{ progress |

percent
}}
```

Output

```
85%
```

______________________________________________________________________

# SlicePipe

Strings

```html
{{

"Angular"

|

slice:0:4

}}
```

Output

```
Angu
```

______________________________________________________________________

Arrays

```html
{{

users

|

slice:0:3

}}
```

Displays

first three users.

______________________________________________________________________

# JsonPipe

Very useful

during development.

```html
<pre>

{{

user

|

json

}}

</pre>
```

Output

```json
{

"id":1,

"name":"Riyaz"

}
```

Never leave it

in production UI.

______________________________________________________________________

# AsyncPipe

One of the most important pipes.

Suppose

```typescript
users$ =

this.userService

.getUsers();
```

Template

```html
{{

users$

|

async

}}
```

Angular

- Subscribes automatically
- Updates the UI
- Unsubscribes automatically

______________________________________________________________________

# Why AsyncPipe?

Without AsyncPipe

```typescript
this.userService

.getUsers()

.subscribe(

users =>

this.users = users

);
```

With AsyncPipe

```html
{{

users$

|

async

}}
```

Less code.

Automatic cleanup.

______________________________________________________________________

# KeyValuePipe

Suppose

```typescript
user = {

name:"Riyaz",

age:30

};
```

Template

```html
@for (

item of

user | keyvalue;

track item.key

){

<p>

{{ item.key }}

:

{{ item.value }}

</p>

}
```

Useful for

dynamic objects.

______________________________________________________________________

# Chaining Pipes

Pipes can be combined.

```html
{{

salary

|

currency:'INR'

|

uppercase

}}
```

Angular executes

left

↓

right.

______________________________________________________________________

Another Example

```html
{{

date

|

date:'longDate'

|

uppercase

}}
```

______________________________________________________________________

# Pipe Parameters

Syntax

```html
{{

value

|

pipe:parameter

}}
```

Multiple parameters

```html
{{

amount

|

currency:'USD':'symbol'

}}
```

______________________________________________________________________

# Custom Pipe

Suppose

every username

should display

```
@username
```

Create

```typescript
@Pipe({

name:"username"

})
```

______________________________________________________________________

Transform

```typescript
transform(

value:string

){

return

"@" + value;

}
```

Usage

```html
{{

name

|

username

}}
```

Output

```
@riyaz
```

______________________________________________________________________

# Pipe Lifecycle

```
Value Changes

↓

Pipe Executes

↓

Formatted Value

↓

UI Updates
```

______________________________________________________________________

# Pure Pipes

Default behavior.

Angular executes

only when

```
Reference Changes
```

Fast.

Efficient.

Recommended.

______________________________________________________________________

# Example

```typescript
@Pipe({

name:"price",

pure:true

})
```

Default.

______________________________________________________________________

# Impure Pipes

```typescript
@Pipe({

name:"price",

pure:false

})
```

Runs

during

every change detection cycle.

Much slower.

Avoid unless necessary.

______________________________________________________________________

# Pure vs Impure

| Pure | Impure |
|-------|---------|
| Fast | Slower |
| Default | Rare |
| Executes on reference change | Executes frequently |
| Recommended | Use carefully |

______________________________________________________________________

# Custom Pipe Folder

```
pipes/

├── currency-format.pipe.ts

├── initials.pipe.ts

├── phone.pipe.ts

├── username.pipe.ts
```

______________________________________________________________________

# Enterprise Examples

```
CurrencyPipe

↓

Financial Applications
```

```
DatePipe

↓

Reports
```

```
TitleCasePipe

↓

CMS
```

```
MaskPhonePipe

↓

Customer Portal
```

```
StatusColorPipe

↓

Dashboards
```

______________________________________________________________________

# Pipe vs Function

Wrong

```html
{{

formatPrice()

}}
```

Angular

calls the method

during change detection.

Better

```html
{{

price

|

currency

}}
```

Pipes are optimized

for template transformations.

______________________________________________________________________

# Pipe vs Service

Pipe

```
Display Data
```

Service

```
Business Logic
```

Never place

business logic

inside a pipe.

______________________________________________________________________

# Pipe vs Directive

Pipe

↓

Transforms Values

Directive

↓

Changes DOM

Component

↓

Controls UI

______________________________________________________________________

# Performance

Good

```
DatePipe

CurrencyPipe

UpperCasePipe
```

Avoid

```
Heavy Calculations

Inside Pipe
```

______________________________________________________________________

# AsyncPipe vs subscribe()

Prefer

```
AsyncPipe
```

inside templates.

Benefits

- Cleaner templates
- Automatic subscription
- Automatic unsubscription
- Prevents memory leaks

______________________________________________________________________

# Backend Comparison

Spring Boot

```
JSON

↓

Angular

↓

Pipe

↓

Formatted UI
```

Formatting belongs

in the frontend,

not the backend,

unless required by business rules.

______________________________________________________________________

# Common Mistakes

## Business Logic in Pipes

Wrong

```
Pipe

↓

Database

↓

API Call
```

Pipes should only transform display values.

______________________________________________________________________

## Using Impure Pipes Everywhere

They execute frequently

and can hurt performance.

______________________________________________________________________

## Forgetting AsyncPipe

Templates displaying Observables

should generally use

```
AsyncPipe
```

instead of manual subscriptions.

______________________________________________________________________

## Using Methods Instead of Pipes

Prefer

```
Pipe
```

for formatting displayed values.

______________________________________________________________________

# Best Practices

✅ Prefer built-in pipes whenever possible.

✅ Create custom pipes for reusable formatting.

✅ Keep pipes focused on presentation.

✅ Prefer pure pipes.

✅ Use AsyncPipe with Observables.

✅ Avoid expensive computations inside pipes.

______________________________________________________________________

# Interview Deep Dive

## Question

What is a Pipe?

### Answer

A Pipe transforms data for display in Angular templates without modifying the original value. Pipes improve readability,
reusability, and separation of presentation logic from business logic.

______________________________________________________________________

## Question

What is the difference between a Pipe and a Service?

### Answer

A Pipe formats data for display in templates, while a Service contains reusable business logic, data access, and
application functionality.

______________________________________________________________________

## Question

What is the difference between a Pure Pipe and an Impure Pipe?

### Answer

A Pure Pipe runs only when its input reference changes, making it more efficient. An Impure Pipe runs during every
change detection cycle and should be used only when necessary.

______________________________________________________________________

## Question

Why is AsyncPipe preferred over manual subscriptions?

### Answer

AsyncPipe automatically subscribes to Observables, updates the template when new values arrive, and unsubscribes when
the component is destroyed, reducing boilerplate and preventing memory leaks.

______________________________________________________________________

## Question

When should you create a custom pipe?

### Answer

Create a custom pipe when the same presentation logic is needed in multiple templates, such as formatting phone numbers,
usernames, or custom status labels.

______________________________________________________________________

# Practice Questions

1. What is a Pipe?
1. Why are Pipes useful?
1. What are the most commonly used built-in pipes?
1. What is AsyncPipe?
1. What is the difference between Pure and Impure Pipes?
1. When should a custom pipe be created?
1. What is the difference between a Pipe and a Directive?
1. What is the difference between a Pipe and a Service?
1. Why are pipes generally preferred over formatting methods in templates?
1. Why should business logic not be placed inside a pipe?

______________________________________________________________________

# Summary

Pipes provide a clean and reusable way to transform data for presentation.

In this chapter, you learned:

- What Pipes are
- Pipe syntax
- Built-in pipes
- DatePipe
- CurrencyPipe
- DecimalPipe
- PercentPipe
- SlicePipe
- JsonPipe
- AsyncPipe
- KeyValuePipe
- Chaining pipes
- Pipe parameters
- Custom pipes
- Pure vs Impure pipes
- Performance considerations
- Pipe vs Service vs Directive
- Best practices

You now have a solid understanding of Angular's presentation layer. The next chapter focuses on **Performance & Change
Detection**, where you'll learn how Angular detects changes, optimize rendering with `OnPush`, use `track` effectively,
avoid unnecessary re-renders, and understand how **Signals** improve performance in modern Angular.

______________________________________________________________________

# Next

[Performance & Change Detection](17-performance.md)

# Templates & Data Binding

Components contain the logic.

Templates display that logic.

A template is simply an HTML file with Angular features that allow you to display data, respond to user actions, and
dynamically update the page.

If Components are the **brain**,

Templates are the **face**.

______________________________________________________________________

# What is a Template?

Every component has a template.

Example

```
UserComponent

├── user.component.ts

└── user.component.html
```

The TypeScript file contains

```
Logic
```

The HTML file contains

```
UI
```

______________________________________________________________________

# Component + Template

```
UserComponent

↓

Properties

↓

Methods

↓

Template

↓

Browser
```

Angular automatically keeps both synchronized.

______________________________________________________________________

# Example

Component

```typescript
export class UserComponent {

    title = "Angular Crash Course";

}
```

Template

```html
<h1>

{{ title }}

</h1>
```

Output

```text
Angular Crash Course
```

______________________________________________________________________

# Data Binding

Angular connects

```
TypeScript

↓

HTML
```

using

```
Data Binding
```

There are four major types.

```
Interpolation

↓

Property Binding

↓

Event Binding

↓

Two-way Binding
```

These are asked in almost every Angular interview.

______________________________________________________________________

# Data Binding Overview

```
Component

↓

Property

↓

Template

↓

User

↓

Event

↓

Component
```

Angular continuously synchronizes data between the component and template.

______________________________________________________________________

# 1. Interpolation

The simplest binding.

Syntax

```html
{{ expression }}
```

Example

Component

```typescript
title = "Users";
```

Template

```html
<h1>

{{ title }}

</h1>
```

Output

```
Users
```

______________________________________________________________________

# Multiple Values

```typescript
firstName = "John";

lastName = "Doe";
```

```html
{{ firstName }}

{{ lastName }}
```

Output

```
John Doe
```

______________________________________________________________________

# Expressions

Interpolation supports expressions.

```html
{{ 5 + 10 }}
```

Output

```
15
```

______________________________________________________________________

Example

```html
{{ firstName + " " + lastName }}
```

______________________________________________________________________

Calling methods

Component

```typescript
getTitle() {

    return "Angular";

}
```

Template

```html
{{ getTitle() }}
```

Although possible,

avoid calling expensive methods repeatedly from templates.

______________________________________________________________________

# 2. Property Binding

Property Binding sends data

```
Component

↓

HTML Element
```

Syntax

```html
[property]="value"
```

______________________________________________________________________

Example

Component

```typescript
imageUrl =

"profile.png";
```

Template

```html
<img

[src]="imageUrl"

>
```

Angular updates the HTML property.

______________________________________________________________________

Another Example

```typescript
isDisabled = true;
```

```html
<button

[disabled]="isDisabled"

>

Save

</button>
```

______________________________________________________________________

# Property vs HTML Attribute

This interview question is common.

Attribute

```
Initial HTML
```

Property

```
Live DOM Value
```

Angular binds to

```
Properties
```

because properties change dynamically.

______________________________________________________________________

# 3. Event Binding

Event Binding sends information

```
Browser

↓

Component
```

Syntax

```html
(event)="method()"
```

______________________________________________________________________

Example

Component

```typescript
save() {

    console.log(

        "Saved"

    );

}
```

Template

```html
<button

(click)="save()"

>

Save

</button>
```

______________________________________________________________________

Passing Parameters

Component

```typescript
delete(

id: number

) {

}
```

Template

```html
<button

(click)="delete(10)"

>

Delete

</button>
```

______________________________________________________________________

Using Event Object

```html
<input

(input)="onInput($event)"

>
```

Component

```typescript
onInput(

event: Event

) {

    console.log(event);

}
```

______________________________________________________________________

# Common Events

```
click

input

change

keyup

keydown

submit

mouseenter

mouseleave
```

______________________________________________________________________

# 4. Two-Way Binding

Two-way binding means

```
Component

↓

Template

↓

Component
```

Both remain synchronized.

Syntax

```html
[(ngModel)]
```

______________________________________________________________________

Example

Component

```typescript
username = "";
```

Template

```html
<input

[(ngModel)]="username"

>

<p>

{{ username }}

</p>
```

Typing updates

```
Component

AND

UI
```

simultaneously.

______________________________________________________________________

# How Two-Way Binding Works

Internally

```html
[(ngModel)]
```

is equivalent to

```
Property Binding

+

Event Binding
```

Conceptually

```
[value]

+

(input)
```

This is why it's called

```
Two-way
```

binding.

______________________________________________________________________

# One-Way vs Two-Way

One-way

```
Component

↓

UI
```

Two-way

```
Component

↓

UI

↓

Component
```

______________________________________________________________________

# String Interpolation vs Property Binding

Interpolation

```html
<img

src="{{ imageUrl }}"

>
```

Works,

but

Angular recommends

```html
<img

[src]="imageUrl"

>
```

Property binding is clearer and supports non-string values.

______________________________________________________________________

# Angular Expressions

Templates support expressions.

Examples

```html
{{ user.name }}
```

```html
{{ users.length }}
```

```html
{{ isLoggedIn }}
```

______________________________________________________________________

Avoid

- Loops
- Heavy computations
- Creating new objects

inside templates.

______________________________________________________________________

# Safe Navigation

Suppose

```typescript
user = undefined;
```

Wrong

```html
{{ user.name }}
```

Runtime error.

Correct

```html
{{ user?.name }}
```

Angular displays nothing until the value exists.

______________________________________________________________________

# Nullish Coalescing

Example

```html
{{ user?.city ??

"Unknown" }}
```

Very useful for optional data.

______________________________________________________________________

# Template Variables

Create a local variable.

```html
<input

#email

>

<button

(click)="save(email.value)"

>

Save

</button>
```

Notice

```
#email
```

exists only inside the template.

______________________________________________________________________

# ng-container

Sometimes you need Angular logic

without creating an HTML element.

Example

```html
<ng-container>

Content

</ng-container>
```

Angular processes it,

but it doesn't appear in the DOM.

Useful for grouping template logic.

______________________________________________________________________

# ng-template

Represents a template

that isn't rendered immediately.

Example

```html
<ng-template>

Loading...

</ng-template>
```

Angular renders it only when needed.

We'll see practical examples with conditional rendering later.

______________________________________________________________________

# Pipes (Introduction)

Pipes transform displayed values.

Example

```html
{{ username | uppercase }}
```

Output

```
JOHN
```

Common pipes

```
uppercase

lowercase

date

currency

json

percent

slice
```

Custom pipes will be covered later.

______________________________________________________________________

# Data Flow

Typical Angular flow

```
Backend

↓

JSON

↓

Component

↓

Template

↓

Browser

↓

User
```

______________________________________________________________________

# User Interaction Flow

```
Button Click

↓

Component Method

↓

Service

↓

API

↓

Response

↓

Component

↓

Template

↓

Updated UI
```

This is one of the most common application flows.

______________________________________________________________________

# Backend Comparison

Spring Boot

```
Controller

↓

JSON

↓

Angular Component

↓

Template

↓

Browser
```

The template is responsible only for displaying data.

______________________________________________________________________

# Modern Angular Control Flow

Angular 17+ introduced a new control flow syntax.

Instead of

```html
<div *ngIf="isLoggedIn">

Welcome

</div>
```

Modern Angular encourages

```html
@if (isLoggedIn) {

    <div>

        Welcome

    </div>

}
```

Similarly,

```
*ngFor

↓

@for
```

and

```
*ngSwitch

↓

@switch
```

We'll cover these in detail in the next chapter on Directives.

______________________________________________________________________

# Common Mistakes

## Putting Business Logic in Templates

Wrong

```html
{{ calculateTotal() }}
```

if

```
calculateTotal()
```

performs expensive work.

Compute values inside the component instead.

______________________________________________________________________

## Using String Interpolation Everywhere

For HTML properties,

prefer

```html
[src]

[disabled]

[value]
```

over interpolation.

______________________________________________________________________

## Forgetting Safe Navigation

Always use

```html
user?.name
```

when data may be undefined.

______________________________________________________________________

## Confusing Property Binding with Event Binding

Remember

```
[]

↓

Component → HTML
```

```
()

↓

HTML → Component
```

______________________________________________________________________

# Best Practices

✅ Keep templates simple.

✅ Move business logic into components or services.

✅ Use property binding for HTML properties.

✅ Use event binding for user actions.

✅ Prefer optional chaining for nullable data.

✅ Use modern control flow (`@if`, `@for`) in new Angular projects.

______________________________________________________________________

# Interview Deep Dive

## Question

What is data binding?

### Answer

Data binding is Angular's mechanism for synchronizing data between a component and its template. It allows the UI to
display component data and respond to user interactions automatically.

______________________________________________________________________

## Question

What are the four types of data binding?

### Answer

Angular supports four primary types of data binding:

- Interpolation (`{{ }}`)
- Property Binding (`[]`)
- Event Binding (`()`)
- Two-way Binding (`[()]`)

______________________________________________________________________

## Question

What is the difference between property binding and event binding?

### Answer

Property binding sends data from the component to the template, while event binding sends user events from the template
back to the component.

______________________________________________________________________

## Question

What is two-way binding?

### Answer

Two-way binding keeps component properties and form inputs synchronized. Changes in the component update the UI, and
user input updates the component automatically.

______________________________________________________________________

## Question

Why should templates remain simple?

### Answer

Templates are evaluated frequently during change detection. Heavy computations or business logic inside templates can
reduce performance and make the application harder to maintain.

______________________________________________________________________

# Practice Questions

1. What is a template?
1. What is data binding?
1. What are the four types of data binding?
1. When should interpolation be used?
1. When should property binding be used?
1. When should event binding be used?
1. How does two-way binding work?
1. What are template variables?
1. What is the purpose of `ng-container`?
1. Why should templates avoid business logic?

______________________________________________________________________

# Summary

Templates are responsible for presenting data and responding to user interactions.

In this chapter, you learned:

- Templates
- Data binding
- Interpolation
- Property binding
- Event binding
- Two-way binding
- Template variables
- `ng-container`
- `ng-template`
- Pipes (introduction)
- Safe navigation
- Data flow
- Modern Angular control flow overview

These concepts form the foundation for building interactive Angular applications. Next, we'll explore **Directives**,
where you'll learn how Angular dynamically adds, removes, and modifies elements in the DOM using both legacy (`*ngIf`,
`*ngFor`) and modern (`@if`, `@for`) syntax.

______________________________________________________________________

# Next

[Directives](07-directives.md)

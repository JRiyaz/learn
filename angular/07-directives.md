# Directives

Angular templates display data.

**Directives** make templates **dynamic**.

They allow Angular to:

- Show elements
- Hide elements
- Repeat elements
- Modify element behavior
- Add custom behavior

Think of directives as **instructions** that tell Angular what to do with HTML elements.

______________________________________________________________________

# What is a Directive?

A directive is a class that changes the appearance or behavior of an HTML element.

Without directives

```html
<div>

Hello

</div>
```

Static HTML.

______________________________________________________________________

With directives

```html
<div *ngIf="isLoggedIn">

Welcome

</div>
```

Angular decides whether to display the element.

______________________________________________________________________

# Why Directives?

Imagine displaying users.

Without directives

```html
<div>User 1</div>

<div>User 2</div>

<div>User 3</div>
```

Impossible for dynamic data.

With directives

```html
<div

*ngFor="let user of users"

>

{{ user.name }}

</div>
```

Angular automatically creates the HTML.

______________________________________________________________________

# Types of Directives

Angular has three categories.

```
Components

↓

Structural Directives

↓

Attribute Directives
```

______________________________________________________________________

# Components are Directives

Every component is technically a directive with its own template.

Example

```typescript
@Component({

})
```

Components are the most powerful type of directive.

______________________________________________________________________

# Structural Directives

Structural directives change the

```
DOM Structure
```

They can

- Add elements
- Remove elements
- Repeat elements

Examples

```
*ngIf

*ngFor

*ngSwitch
```

Modern Angular

```
@if

@for

@switch
```

______________________________________________________________________

# Attribute Directives

Attribute directives

modify existing elements.

Examples

```
ngClass

ngStyle
```

They do **not**

add or remove elements.

______________________________________________________________________

# Angular Evolution

Older Angular

```
*ngIf

*ngFor

*ngSwitch
```

Modern Angular (17+)

```
@if

@for

@switch
```

For interviews,

you should understand **both** because many enterprise projects still use the older syntax.

______________________________________________________________________

# @if (Modern)

Suppose

```typescript
isLoggedIn = true;
```

Template

```html
@if (isLoggedIn) {

    <h2>

        Welcome

    </h2>

}
```

If

```
true
```

Angular renders the HTML.

______________________________________________________________________

# else Block

```html
@if (isLoggedIn) {

    <h2>

        Welcome

    </h2>

}

@else {

    <h2>

        Please Login

    </h2>

}
```

Cleaner than older syntax.

______________________________________________________________________

# Older \*ngIf

Equivalent

```html
<div

*ngIf="isLoggedIn"

>

Welcome

</div>
```

Still very common.

______________________________________________________________________

# Comparing Both

Modern

```html
@if (isLoggedIn) {

}
```

Legacy

```html
<div

*ngIf="isLoggedIn"

>

</div>
```

Both achieve the same result.

______________________________________________________________________

# @for (Modern)

Suppose

```typescript
users = [

    "Alice",

    "Bob",

    "Charlie"

];
```

Template

```html
@for (

user of users;

track user

) {

    <p>

        {{ user }}

    </p>

}
```

Angular creates

```
3 Paragraphs
```

______________________________________________________________________

# Older \*ngFor

```html
<div

*ngFor="

let user of users

"

>

{{ user }}

</div>
```

______________________________________________________________________

# Why track?

Modern Angular encourages

```html
track user.id
```

Example

```html
@for (

user of users;

track user.id

) {

}
```

Angular knows exactly

which item changed,

improving performance.

______________________________________________________________________

# \*ngFor Index

Legacy

```html
<div

*ngFor="

let user of users;

let i = index

"

>

{{ i }}

{{ user.name }}

</div>
```

______________________________________________________________________

# @for Index

Modern

```html
@for (

user of users;

track user.id;

let i = $index

) {

    {{ i }}

}
```

______________________________________________________________________

# @empty

Modern Angular supports

```html
@for (

user of users;

track user.id

) {

    {{ user.name }}

}

@empty {

    <p>

        No Users

    </p>

}
```

Very useful.

______________________________________________________________________

# \*ngSwitch

Legacy

```html
<div

[ngSwitch]="role"

>

<div

*ngSwitchCase="'ADMIN'"

>

Admin

</div>

<div

*ngSwitchDefault

>

User

</div>

</div>
```

______________________________________________________________________

# @switch (Modern)

Cleaner syntax.

```html
@switch (role) {

    @case ("ADMIN") {

        <h2>

            Admin

        </h2>

    }

    @default {

        <h2>

            User

        </h2>

    }

}
```

______________________________________________________________________

# ngClass

Adds CSS classes dynamically.

Component

```typescript
isActive = true;
```

Template

```html
<div

[class.active]="isActive"

>

User

</div>
```

Or

```html
<div

[ngClass]="{

active:isActive

}"

>

</div>
```

______________________________________________________________________

# Multiple Classes

```html
<div

[ngClass]="{

active:true,

disabled:false

}"

>

</div>
```

Very common.

______________________________________________________________________

# ngStyle

Apply styles dynamically.

```html
<div

[ngStyle]="{

color:'red',

fontSize:'20px'

}"

>

Hello

</div>
```

______________________________________________________________________

# Hidden Property

Instead of

```html
*ngIf
```

sometimes

```html
<div

[hidden]="loading"

>

Content

</div>
```

Difference

```
hidden

↓

Still Exists
```

```
@if

↓

Removed
```

from the DOM.

______________________________________________________________________

# Attribute Binding

Example

```html
<input

[disabled]="loading"

>
```

Angular updates the DOM property.

______________________________________________________________________

# Custom Directive

Suppose

every input should automatically become uppercase.

Create

```typescript
@Directive({

selector:

"[appUppercase]"

})
```

Usage

```html
<input

appUppercase

>
```

Angular adds custom behavior.

______________________________________________________________________

# Real Enterprise Examples

Highlight overdue invoices.

```html
<tr

appHighlightOverdue

>
```

Permission-based visibility.

```html
<button

appHasPermission

>

Delete

</button>
```

Lazy image loading.

```html
<img

appLazyImage

>
```

Custom directives improve reusability.

______________________________________________________________________

# Directive Execution

```
Angular

↓

Reads Template

↓

Finds Directives

↓

Executes Directive

↓

Updates DOM
```

______________________________________________________________________

# Structural vs Attribute

Structural

```
DOM

Changes
```

Examples

```
@if

@for

@switch
```

______________________________________________________________________

Attribute

```
DOM Exists

Behavior Changes
```

Examples

```
ngClass

ngStyle
```

______________________________________________________________________

# Backend Comparison

Spring Boot

```
if

↓

JSON
```

Angular

```
@if

↓

HTML
```

Angular directives control the UI,

not backend logic.

______________________________________________________________________

# Common Mistakes

## Using \*ngIf for Styling

Wrong

```html
*ngIf
```

to hide something that should simply be invisible.

Sometimes

```html
[hidden]
```

or CSS is more appropriate.

______________________________________________________________________

## Forgetting track

When rendering lists,

always provide a tracking expression.

Modern Angular

```html
track user.id
```

improves rendering efficiency.

______________________________________________________________________

## Heavy Logic Inside Templates

Wrong

```html
@if (

calculateSomething()

) {

}
```

Compute values in the component.

______________________________________________________________________

## Confusing Structural and Attribute Directives

Remember

Structural

↓

Changes DOM

Attribute

↓

Changes behavior or appearance.

______________________________________________________________________

# Best Practices

✅ Prefer modern control flow (`@if`, `@for`, `@switch`) for new Angular applications.

✅ Learn the legacy syntax because you'll encounter it in existing codebases.

✅ Always use a tracking expression with `@for`.

✅ Keep template logic simple.

✅ Use custom directives for reusable UI behavior.

______________________________________________________________________

# Interview Deep Dive

## Question

What is a directive?

### Answer

A directive is a class that adds behavior to HTML elements or changes the DOM structure. Angular uses directives to
implement conditional rendering, loops, styling, and reusable UI behavior.

______________________________________________________________________

## Question

What is the difference between structural and attribute directives?

### Answer

Structural directives add, remove, or repeat elements in the DOM, while attribute directives modify the appearance or
behavior of existing elements without changing the DOM structure.

______________________________________________________________________

## Question

What are the modern replacements for `*ngIf` and `*ngFor`?

### Answer

Modern Angular introduces `@if` and `@for`, which provide a cleaner and more readable syntax while improving template
clarity.

______________________________________________________________________

## Question

Why should `track` be used with `@for`?

### Answer

The tracking expression allows Angular to identify which list items changed, reducing unnecessary DOM updates and
improving rendering performance.

______________________________________________________________________

## Question

When should a custom directive be created?

### Answer

Create a custom directive when the same UI behavior needs to be reused across multiple components, such as permission
checks, automatic formatting, or highlighting elements.

______________________________________________________________________

# Practice Questions

1. What is a directive?
1. What are the three categories of directives?
1. What is the difference between structural and attribute directives?
1. What is the purpose of `@if`?
1. What is the purpose of `@for`?
1. Why should `track` be used?
1. What is the purpose of `ngClass`?
1. What is the purpose of `ngStyle`?
1. When should a custom directive be created?
1. What are the differences between modern and legacy Angular control flow?

______________________________________________________________________

# Summary

Directives are one of Angular's most powerful features, allowing templates to become dynamic and interactive.

In this chapter, you learned:

- What directives are
- Types of directives
- Structural directives
- Attribute directives
- Modern control flow (`@if`, `@for`, `@switch`)
- Legacy syntax (`*ngIf`, `*ngFor`, `*ngSwitch`)
- `ngClass`
- `ngStyle`
- Custom directives
- Performance with `track`
- Best practices

Now that you know how Angular dynamically renders the UI, the next step is understanding **Dependency Injection and
Services**, one of Angular's biggest strengths and a concept that closely resembles Spring Boot's dependency injection.

______________________________________________________________________

# Next

[Dependency Injection & Services](08-dependency-injection-and-services.md)

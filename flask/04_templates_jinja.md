# Templates & Jinja2

> **Course:** Flask for Backend Engineers
>
> **Module:** 2
>
> **File:** `04_templates_jinja.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Jinja2 is
- Why Template Engines exist
- Rendering HTML
- Template Variables
- Control Statements
- Loops
- Conditionals
- Filters
- Template Inheritance
- Includes
- Macros
- Escaping
- Custom Filters
- Best Practices

______________________________________________________________________

# What is Jinja2?

**Jinja2** is Flask's template engine.

Its job is to generate HTML dynamically.

Instead of writing static HTML,

you can inject Python data into templates.

Example

```
Python

↓

Jinja2

↓

HTML

↓

Browser
```

______________________________________________________________________

# Why Use Templates?

Imagine displaying a user's profile.

Without templates,

you would manually concatenate strings.

```python
return "<h1>" + username + "</h1>"
```

This becomes difficult to maintain.

Instead,

Flask uses Jinja2.

```
Python

↓

Template

↓

Final HTML
```

______________________________________________________________________

# Project Structure

```
project/

│

├── app.py

├── templates/

│      home.html

│      about.html

│      users.html

│

└── static/
```

Flask automatically looks inside the **templates** folder.

______________________________________________________________________

# First Template

home.html

```html
<!DOCTYPE html>

<html>

<body>

<h1>Hello Flask</h1>

</body>

</html>
```

______________________________________________________________________

# Rendering a Template

```python
from flask import render_template

@app.route("/")
def home():

    return render_template(
        "home.html"
    )
```

Request

```
GET /
```

↓

Browser receives HTML.

______________________________________________________________________

# Passing Variables

Python

```python
@app.route("/")
def home():

    return render_template(
        "home.html",
        name="Riyaz"
    )
```

Template

```html
<h1>Hello {{ name }}</h1>
```

Output

```html
Hello Riyaz
```

______________________________________________________________________

# Multiple Variables

```python
return render_template(

    "user.html",

    name="Riyaz",

    age=27,

    city="Bangalore"

)
```

Template

```html
{{ name }}

{{ age }}

{{ city }}
```

______________________________________________________________________

# Rendering Objects

Python

```python
user = {

    "name": "Riyaz",

    "age": 27

}

return render_template(

    "user.html",

    user=user

)
```

Template

```html
{{ user.name }}

{{ user.age }}
```

Dictionary access also works

```html
{{ user["name"] }}
```

______________________________________________________________________

# Expressions

Jinja supports expressions.

```html
{{ 5 + 5 }}
```

Output

```
10
```

Another example

```html
{{ name.upper() }}
```

Although simple expressions are supported,

heavy business logic should remain in Python.

______________________________________________________________________

# Comments

```html
{# This is a comment #}
```

Comments are not sent to the browser.

______________________________________________________________________

# Conditionals

```html
{% if age >= 18 %}

Adult

{% else %}

Minor

{% endif %}
```

______________________________________________________________________

# Multiple Conditions

```html
{% if score > 90 %}

A

{% elif score > 80 %}

B

{% else %}

C

{% endif %}
```

______________________________________________________________________

# Loops

Python

```python
users = [

    "Alice",

    "Bob",

    "Charlie"

]
```

Template

```html
<ul>

{% for user in users %}

<li>{{ user }}</li>

{% endfor %}

</ul>
```

Output

```html
Alice

Bob

Charlie
```

______________________________________________________________________

# Loop Variables

Jinja provides

```html
{{ loop.index }}
```

Starts at

```
1
```

Other useful values

```html
loop.first

loop.last

loop.length
```

______________________________________________________________________

# Nested Loops

```html
{% for row in rows %}

    {% for item in row %}

        {{ item }}

    {% endfor %}

{% endfor %}
```

______________________________________________________________________

# Filters

Filters transform values.

Example

```html
{{ name|upper }}
```

Output

```
RIYAZ
```

______________________________________________________________________

# Common Filters

| Filter | Example |
|---------|----------|
| upper | `{{ name|upper }}` |
| lower | `{{ name|lower }}` |
| title | `{{ name|title }}` |
| length | `{{ users|length }}` |
| default | `{{ city|default("Unknown") }}` |
| safe | `{{ html|safe }}` |

______________________________________________________________________

# Default Filter

```html
{{ city|default("Unknown") }}
```

If

```
city = None
```

Output

```
Unknown
```

______________________________________________________________________

# Escaping

Jinja automatically escapes HTML.

Input

```html
<script>alert(1)</script>
```

Output

```
&lt;script&gt;
```

This protects against Cross-Site Scripting (XSS).

______________________________________________________________________

# Safe Filter

```html
{{ html|safe }}
```

Disables automatic escaping.

Use only for trusted content.

Never use it with untrusted user input.

______________________________________________________________________

# Template Inheritance

Large applications share layouts.

Instead of copying HTML,

use inheritance.

______________________________________________________________________

# Base Template

base.html

```html
<!DOCTYPE html>

<html>

<head>

<title>

{% block title %}

{% endblock %}

</title>

</head>

<body>

{% block content %}

{% endblock %}

</body>

</html>
```

______________________________________________________________________

# Child Template

home.html

```html
{% extends "base.html" %}

{% block title %}

Home

{% endblock %}

{% block content %}

<h1>Welcome</h1>

{% endblock %}
```

______________________________________________________________________

# Benefits

Without inheritance

```
Header

Footer

Navigation

Copied

100 Times
```

With inheritance

```
Base Template

↓

Reuse Everywhere
```

______________________________________________________________________

# Include

Shared components

```
Navbar

Footer

Sidebar
```

Example

```html
{% include "navbar.html" %}
```

______________________________________________________________________

# Macros

Macros behave like reusable functions.

Example

```html
{% macro button(text) %}

<button>

{{ text }}

</button>

{% endmacro %}
```

Use

```html
{{ button("Save") }}
```

______________________________________________________________________

# Custom Filters

Python

```python
@app.template_filter("currency")
def currency(value):

    return f"${value:.2f}"
```

Template

```html
{{ price|currency }}
```

Output

```
$19.99
```

______________________________________________________________________

# URL Generation

Instead of

```html
<a href="/users">
```

Use

```html
<a href="{{ url_for('users') }}">
```

Benefits

- Safer
- Easier refactoring
- No hardcoded URLs

______________________________________________________________________

# Static Files

CSS

```html
<link
rel="stylesheet"
href="{{ url_for(
'static',
filename='style.css'
) }}">
```

Images

```html
<img
src="{{ url_for(
'static',
filename='logo.png'
) }}">
```

______________________________________________________________________

# Common Mistakes

❌ Putting business logic inside templates

❌ Using `safe` with user input

❌ Duplicating HTML instead of inheritance

❌ Hardcoding URLs

❌ Large templates with no reuse

______________________________________________________________________

# Production Best Practices

- Keep templates simple.
- Move business logic into Python.
- Use inheritance.
- Use includes.
- Escape user input.
- Use `url_for()`.
- Create reusable macros.
- Keep templates readable.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should business logic not be placed inside Jinja templates?**

### Answer

Templates are responsible for presentation.

Business logic belongs in Python.

Keeping business logic inside templates causes:

- Poor readability
- Difficult testing
- Tight coupling
- Harder maintenance

A good design prepares data inside the Flask view function and passes only the required values to the template.

Templates should focus on displaying information rather than computing it.

______________________________________________________________________

# Summary

In this chapter you learned:

- Jinja2
- Rendering Templates
- Variables
- Expressions
- Loops
- Conditionals
- Filters
- Template Inheritance
- Includes
- Macros
- Escaping
- Custom Filters

Jinja2 makes it possible to build clean, reusable, and maintainable server-rendered web applications.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is Jinja2?
1. Why do web frameworks use template engines?
1. How does Flask locate templates?

______________________________________________________________________

## Variables

4. How do you pass variables to a template?
1. How do you access object attributes inside Jinja?
1. What are template expressions?

______________________________________________________________________

## Control Flow

7. How do you write an `if` statement?
1. How do you iterate over a list?
1. What useful values does the `loop` object provide?

______________________________________________________________________

## Filters

10. What are Jinja filters?
01. What does the `default` filter do?
01. Why is the `safe` filter potentially dangerous?

______________________________________________________________________

## Template Organization

13. What is template inheritance?
01. What are includes?
01. What are macros?

______________________________________________________________________

## Security

16. Why does Jinja automatically escape HTML?
01. What type of attack does automatic escaping help prevent?

______________________________________________________________________

## Scenario-Based

18. Your project contains the same navigation bar in 40 HTML files. How would you redesign it?
01. A developer writes SQL queries directly inside a Jinja template. Why is this poor design?
01. Your application renders user-generated HTML using the `safe` filter. What security risks does this introduce?
01. Your project contains dozens of hardcoded links such as `/users` and `/products`. Which Flask feature should replace them?
01. Your team wants reusable Bootstrap buttons throughout the application. Which Jinja feature would you recommend?

______________________________________________________________________

# Next

[Static Files](05_static_files.md)

# Forms & Validation

> **Course:** Flask for Backend Engineers
>
> **Module:** 2
>
> **File:** `06_forms_and_validation.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What HTML Forms are
- How Forms Work
- GET vs POST Forms
- Flask Request Processing
- Form Validation
- Client-side vs Server-side Validation
- Flask-WTF
- WTForms
- CSRF Protection
- Built-in Validators
- Custom Validators
- File Upload Validation
- Production Best Practices

______________________________________________________________________

# What is an HTML Form?

An HTML Form collects user input and sends it to a server.

Examples

- Login
- Registration
- Contact Form
- Search
- Checkout
- Profile Update

Architecture

```
User

↓

HTML Form

↓

Flask

↓

Database

↓

Response
```

______________________________________________________________________

# Basic HTML Form

```html
<form method="POST">

    <input
        type="text"
        name="username">

    <input
        type="password"
        name="password">

    <button type="submit">

        Login

    </button>

</form>
```

______________________________________________________________________

# How Forms Work

```
Browser

↓

User Fills Form

↓

Submit

↓

HTTP Request

↓

Flask

↓

Validation

↓

Database

↓

Response
```

______________________________________________________________________

# GET Forms

Example

```html
<form method="GET">

    <input
        name="q">

</form>
```

Request

```
/search?q=python
```

Use GET for:

- Searching
- Filtering
- Pagination

GET requests should not change server state.

______________________________________________________________________

# POST Forms

```html
<form method="POST">
```

Request Body

```
username=riyaz

password=******
```

Use POST for:

- Login
- Registration
- Payments
- Data Creation
- Profile Updates

______________________________________________________________________

# Reading Form Data

```python
from flask import request

@app.route(
    "/login",
    methods=["POST"]
)
def login():

    username = request.form.get(
        "username"
    )

    password = request.form.get(
        "password"
    )

    return username
```

______________________________________________________________________

# Why Validate Input?

Never trust user input.

Example

```
Age

↓

abc
```

or

```
Email

↓

not-an-email
```

Without validation,

incorrect or malicious data may reach your application.

______________________________________________________________________

# Client-side Validation

Performed in the browser.

Example

```html
<input

type="email"

required>
```

Advantages

- Immediate feedback
- Better user experience

Limitations

Users can bypass client-side validation.

______________________________________________________________________

# Server-side Validation

Performed by Flask.

Example

```python
if not username:

    return "Required", 400
```

Server-side validation is mandatory for security and data integrity.

______________________________________________________________________

# Client vs Server Validation

| Client-side | Server-side |
|--------------|-------------|
| Browser | Flask |
| Fast | Secure |
| Improves UX | Required |
| Can be bypassed | Cannot be skipped by clients |

Use both together.

______________________________________________________________________

# Manual Validation

```python
username = request.form.get(
    "username"
)

if not username:

    return "Username Required", 400
```

Simple applications may perform validation manually.

______________________________________________________________________

# Introducing Flask-WTF

**Flask-WTF** integrates WTForms with Flask.

Features

- Form Classes
- Validation
- CSRF Protection
- Better Organization

Install

```bash
pip install flask-wtf
```

______________________________________________________________________

# Creating a Form

```python
from flask_wtf import FlaskForm

from wtforms import StringField

from wtforms.validators import DataRequired

class LoginForm(FlaskForm):

    username = StringField(
        validators=[
            DataRequired()
        ]
    )
```

______________________________________________________________________

# Rendering a Form

Python

```python
form = LoginForm()

return render_template(
    "login.html",
    form=form
)
```

Template

```html
{{ form.username }}

{{ form.submit }}
```

______________________________________________________________________

# Form Validation

```python
form = LoginForm()

if form.validate_on_submit():

    return "Success"
```

`validate_on_submit()` checks:

- Request Method
- CSRF Token
- Validation Rules

______________________________________________________________________

# Common Validators

| Validator | Purpose |
|------------|----------|
| DataRequired | Required Field |
| Length | Minimum / Maximum Length |
| Email | Valid Email Format |
| NumberRange | Numeric Limits |
| EqualTo | Password Confirmation |
| Optional | Field May Be Empty |
| Regexp | Pattern Matching |

______________________________________________________________________

# DataRequired

```python
username = StringField(

    validators=[
        DataRequired()
    ]

)
```

______________________________________________________________________

# Length Validator

```python
validators=[

    Length(
        min=3,
        max=20
    )

]
```

______________________________________________________________________

# Email Validator

```python
Email()
```

Accepts

```
user@example.com
```

Rejects

```
hello
```

______________________________________________________________________

# EqualTo

Useful for password confirmation.

```python
password = PasswordField()

confirm = PasswordField(

    validators=[

        EqualTo(
            "password"
        )

    ]

)
```

______________________________________________________________________

# Custom Validator

```python
from wtforms.validators import ValidationError

def validate_username(

    form,

    field

):

    if field.data == "admin":

        raise ValidationError(

            "Reserved Username"

        )
```

Attach it

```python
validators=[

    validate_username

]
```

______________________________________________________________________

# Validation Errors

```python
if not form.validate():

    print(form.errors)
```

Example

```python
{

    "username": [

        "Required"

    ]

}
```

______________________________________________________________________

# CSRF Protection

CSRF

\=

Cross-Site Request Forgery

Without protection

```
Attacker

↓

Fake Form

↓

Victim Browser

↓

Your Website
```

Dangerous.

______________________________________________________________________

# CSRF Token

Flask-WTF automatically generates a hidden token.

Template

```html
<form method="POST">

{{ form.hidden_tag() }}

</form>
```

If the token is missing or invalid,

the request is rejected.

______________________________________________________________________

# File Upload Validation

Example

```python
image = request.files.get(
    "image"
)
```

Validate

- File Exists
- Extension
- MIME Type
- Maximum Size

Never trust the filename or extension alone.

______________________________________________________________________

# Password Validation

Good password rules

- Minimum Length
- Uppercase
- Lowercase
- Number
- Special Character

Avoid storing plaintext passwords.

Hash passwords before storing them.

______________________________________________________________________

# Validation Flow

```
User Input

↓

Browser Validation

↓

Flask Validation

↓

Business Rules

↓

Database

↓

Success
```

Every stage improves reliability.

______________________________________________________________________

# Error Messages

Instead of

```
Invalid Input
```

Use

```
Email Address

is required.
```

Specific messages improve usability.

______________________________________________________________________

# Common Mistakes

❌ Trusting browser validation only

❌ Accepting user input without validation

❌ Disabling CSRF protection unnecessarily

❌ Returning vague validation errors

❌ Saving uploaded files without checking type or size

❌ Storing plaintext passwords

______________________________________________________________________

# Production Best Practices

- Validate all user input.
- Use Flask-WTF for HTML forms.
- Enable CSRF protection.
- Hash passwords before storing them.
- Validate uploaded files.
- Return meaningful validation errors.
- Keep business validation separate from form validation.
- Never trust client-side validation alone.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is server-side validation still required if HTML forms already perform client-side validation?**

### Answer

Client-side validation improves the user experience by providing immediate feedback.

However, it is not a security mechanism because users can:

- Disable JavaScript
- Modify requests using browser developer tools
- Use tools such as Postman or curl
- Send handcrafted HTTP requests

Server-side validation is the authoritative check that protects application integrity and prevents invalid or malicious
data from reaching business logic or the database.

Both client-side and server-side validation should be used together.

______________________________________________________________________

# Summary

In this chapter you learned:

- HTML Forms
- GET vs POST
- Reading Form Data
- Validation
- Client-side Validation
- Server-side Validation
- Flask-WTF
- WTForms
- Built-in Validators
- Custom Validators
- CSRF Protection
- File Validation

Proper validation is one of the most important aspects of building secure and reliable web applications.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is an HTML form?
1. How does a browser submit form data to Flask?
1. When should GET be used?
1. When should POST be used?

______________________________________________________________________

## Validation

5. Why should user input always be validated?
1. What is the difference between client-side and server-side validation?
1. Why is client-side validation insufficient?

______________________________________________________________________

## Flask-WTF

8. What is Flask-WTF?
1. What is WTForms?
1. What does `validate_on_submit()` do?
1. What is `hidden_tag()` used for?

______________________________________________________________________

## Validators

12. What does `DataRequired()` validate?
01. What does `Length()` validate?
01. What does `Email()` validate?
01. When would you use `EqualTo()`?
01. How do you create a custom validator?

______________________________________________________________________

## Security

17. What is CSRF?
01. How does Flask-WTF protect against CSRF attacks?
01. Why should uploaded files be validated?
01. Why should passwords never be stored in plaintext?

______________________________________________________________________

## Scenario-Based

21. Your registration page only uses HTML `required` attributes for validation. What security risks remain?
01. A user uploads a file named `virus.jpg.exe`. What validation steps should your application perform?
01. Your login form fails every POST request with a CSRF error. What common implementation detail might be missing from the template?
01. A developer validates password complexity only in JavaScript. Why is this insufficient?
01. Your application needs to reject usernames that already exist in the database. Would this be handled by a built-in validator or a custom validator? Explain your approach.

______________________________________________________________________

# Next

[Blueprints](07_blueprints.md)

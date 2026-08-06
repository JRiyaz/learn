# Forms & File Uploads

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 4 - Request Data
>
> **File:** `20_forms_file_uploads.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What HTML Forms are
- Form Data vs JSON
- Multipart Form Data
- Reading Form Data
- File Uploads
- `UploadFile`
- `File`
- Multiple File Uploads
- Saving Uploaded Files
- Production Best Practices

______________________________________________________________________

# What is Form Data?

Before REST APIs became popular,

web applications primarily sent data using HTML forms.

Example

```html
<form>

<input>

<textarea>

<select>

<button>

</form>
```

When submitted,

the browser sends the form fields to the server.

______________________________________________________________________

# JSON vs Form Data

JSON

```json
{
    "name": "Riyaz",
    "email": "riyaz@example.com"
}
```

Content-Type

```
application/json
```

______________________________________________________________________

Form

```
name=Riyaz

email=riyaz@example.com
```

Content-Type

```
application/x-www-form-urlencoded
```

______________________________________________________________________

# When are Forms Used?

Forms are commonly used for

- Login Pages
- Registration Forms
- Search Forms
- Contact Forms
- Payment Forms

Traditional websites often use forms instead of JSON.

______________________________________________________________________

# Multipart Form Data

When uploading files,

the request uses

```
multipart/form-data
```

Example

```
File

+

Text Fields
```

Both can be sent in the same request.

______________________________________________________________________

# Why Multipart?

JSON

```
Text Only
```

Multipart

```
Text

+

Binary Files
```

Images, PDFs, videos, and documents require multipart encoding.

______________________________________________________________________

# Installing Dependency

FastAPI requires

```bash
pip install python-multipart
```

Without it,

form parsing will not work.

______________________________________________________________________

# Reading Form Data

Import

```python
from fastapi import Form
```

______________________________________________________________________

# Basic Example

```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login")

def login(

    username: str = Form(),

    password: str = Form()

):

    return {

        "username": username

    }
```

______________________________________________________________________

# Request

```
POST

/login
```

Body

```
username=riyaz

password=secret
```

FastAPI parses the form automatically.

______________________________________________________________________

# Optional Form Fields

```python
from typing import Optional

phone:

Optional[str] = Form(

    default=None
)
```

______________________________________________________________________

# Required Form Fields

```python
username: str = Form()
```

Missing field

↓

```
422

Validation Error
```

______________________________________________________________________

# Internal Flow

```
Multipart Request

↓

Form()

↓

Validation

↓

Route
```

______________________________________________________________________

# File Upload

Import

```python
from fastapi import File

from fastapi import UploadFile
```

______________________________________________________________________

# UploadFile

```python
file:

UploadFile = File()
```

This is the recommended way to handle uploaded files.

______________________________________________________________________

# Why UploadFile?

Compared to reading the entire file into memory,

`UploadFile` provides

- Better performance
- Streaming support
- Lower memory usage
- Access to file metadata

______________________________________________________________________

# Upload Example

```python
@app.post("/upload")

def upload(

    file:

    UploadFile = File()

):

    return {

        "filename":

        file.filename
    }
```

______________________________________________________________________

# Request

```
POST

/upload
```

Multipart

```
File

↓

resume.pdf
```

Response

```json
{
    "filename": "resume.pdf"
}
```

______________________________________________________________________

# UploadFile Properties

Useful attributes

```python
file.filename
```

Original filename

______________________________________________________________________

```python
file.content_type
```

Example

```
application/pdf
```

______________________________________________________________________

```python
file.file
```

Underlying file object.

______________________________________________________________________

# Reading Uploaded Files

Asynchronous

```python
contents = await file.read()
```

Read everything into memory.

For large files,

prefer streaming or chunked processing.

______________________________________________________________________

# File Size

FastAPI does not automatically enforce file size limits.

Applications should

- Validate size
- Reject oversized uploads
- Configure server limits

______________________________________________________________________

# Saving Files

Example

```python
contents = await file.read()

with open(

    file.filename,

    "wb"

) as f:

    f.write(contents)
```

Production applications should sanitize filenames before saving.

______________________________________________________________________

# Multiple Files

```python
from typing import List

files:

List[UploadFile] = File()
```

Client uploads

```
resume.pdf

photo.png

report.docx
```

FastAPI returns a list of uploaded files.

______________________________________________________________________

# File Metadata

Example

```python
return {

    "filename":

    file.filename,

    "content_type":

    file.content_type
}
```

Useful for validation and logging.

______________________________________________________________________

# Combining Form + File

Example

```python
@app.post("/profile")

async def profile(

    username: str = Form(),

    image:

    UploadFile = File()

):

    ...
```

Request

```
username

↓

Riyaz
```

```
image

↓

profile.png
```

Both are processed together.

______________________________________________________________________

# Validation

Applications commonly validate

- File Type
- File Extension
- MIME Type
- File Size

Example

Allowed

```
application/pdf
```

Rejected

```
application/x-msdownload
```

______________________________________________________________________

# Upload Flow

```
Browser

↓

Multipart Request

↓

FastAPI

↓

UploadFile

↓

Validation

↓

Storage
```

______________________________________________________________________

# Common File Types

```
image/png

image/jpeg

application/pdf

text/plain

application/zip
```

______________________________________________________________________

# Security

Never trust

```
Filename

↓

Client Input
```

Validate

- Extension
- MIME Type
- Size

Store files outside the application code directory when possible.

______________________________________________________________________

# Common Mistakes

❌ Reading very large files entirely into memory

❌ Trusting filenames from clients

❌ Skipping file validation

❌ Saving files with user-provided names directly

❌ Forgetting to install `python-multipart`

______________________________________________________________________

# Production Best Practices

- Use `UploadFile` instead of `bytes` for large files.
- Validate file type and size.
- Sanitize filenames.
- Store uploads outside the application source directory.
- Generate unique filenames.
- Scan uploads when security requirements demand it.
- Stream large files instead of loading them completely into memory.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is `UploadFile` preferred over `bytes` for file uploads in FastAPI?**

### Answer

`UploadFile` is designed for efficient handling of uploaded files.

Advantages include:

- Lower memory usage.
- Streaming support.
- Access to file metadata.
- Better performance for large uploads.
- Compatibility with asynchronous processing.

Using `bytes` loads the entire file into memory, making it unsuitable for large uploads.

______________________________________________________________________

# Summary

In this chapter you learned:

- Form Data
- Multipart Requests
- `Form()`
- `File()`
- `UploadFile`
- File Uploads
- Multiple Files
- Saving Files
- Validation
- Production Best Practices

FastAPI provides first-class support for HTML forms and file uploads, making it easy to build APIs that accept both
structured form data and binary files efficiently.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is form data?
1. How is form data different from JSON?
1. Why is `multipart/form-data` required for file uploads?

______________________________________________________________________

## FastAPI

4. How do you read form fields in FastAPI?
1. How do you receive uploaded files?
1. Why is `python-multipart` required?

______________________________________________________________________

## UploadFile

7. Why is `UploadFile` preferred over `bytes`?
1. What useful properties does `UploadFile` provide?
1. How do you upload multiple files?

______________________________________________________________________

## Validation

10. Why should uploaded files be validated?
01. What file properties are commonly checked?
01. Why shouldn't client-provided filenames be trusted?

______________________________________________________________________

## Security

13. Why should uploaded files be stored outside the application source directory?
01. Why is scanning uploaded files sometimes necessary?
01. Why should unique filenames be generated?

______________________________________________________________________

## Scenario-Based

16. Your API accepts 2 GB video uploads. Why would reading the entire file into memory be a poor design choice?
01. A user uploads a file named `../../../etc/passwd`. Why should filenames be sanitized before saving?
01. Your application accepts only PDF resumes. How would you validate uploaded files?
01. Your endpoint needs to receive a profile picture and a username in the same request. How would you design the FastAPI endpoint?
01. Your application receives hundreds of simultaneous file uploads. What FastAPI features and best practices help ensure good performance and scalability?

______________________________________________________________________

# Next

[Middleware](21_middleware.md)

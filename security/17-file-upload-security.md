# Security - Part 17

# File Upload Security

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why file uploads are dangerous
- Common file upload vulnerabilities
- Secure file uploads in FastAPI
- File validation
- MIME type validation
- File size limits
- Safe file storage
- Virus scanning
- Best practices

______________________________________________________________________

# Why Are File Uploads Dangerous?

File uploads look simple.

```text id="fus1701"
User

↓

Upload File

↓

Store File

↓

Done
```

But in reality,

they are one of the most common sources of security vulnerabilities.

Attackers may upload:

- Malware
- Executable files
- Extremely large files
- Fake images
- Dangerous scripts

______________________________________________________________________

# Typical Upload Flow

```text id="fus1702"
User

↓

Upload File

↓

Validate

↓

Store

↓

Access Later
```

The validation step is critical.

______________________________________________________________________

# Common Mistake 1

## Trusting the File Extension

Suppose a user uploads

```text id="fus1703"
profile.jpg
```

Can we assume it's an image?

No.

The filename can be changed easily.

A file named

```text id="fus1704"
virus.jpg
```

may not actually be an image.

Never trust file extensions alone.

______________________________________________________________________

# Common Mistake 2

## Trusting the MIME Type

Browsers send

a MIME type.

Example

```text id="fus1705"
image/jpeg
```

Unfortunately,

clients control this value.

Attackers can fake it.

Treat MIME types as helpful,

not authoritative.

______________________________________________________________________

# Secure Validation

A secure upload process checks:

```text id="fus1706"
Extension

↓

MIME Type

↓

Actual File Content

↓

Size

↓

Storage
```

No single validation is enough.

______________________________________________________________________

# FastAPI Upload Example

```python id="fus1707"
from fastapi import UploadFile

@app.post("/upload")
async def upload(
    file: UploadFile
):
    return {
        "filename": file.filename
    }
```

Receiving a file

is easy.

Validating it

is the important part.

______________________________________________________________________

# File Size Limits

Never allow unlimited uploads.

Example

```text id="fus1708"
500 MB

↓

1 GB

↓

5 GB

↓

Server Disk Full
```

Always define

maximum upload sizes.

Example limits

| File Type | Example Limit |
| --------------- | ------------------------------------ |
| Profile Picture | 5 MB |
| PDF Document | 20 MB |
| Video | 100 MB (depends on your application) |

______________________________________________________________________

# Restrict Allowed File Types

Allow only

the file types

your application needs.

Example

```text id="fus1709"
Allowed

↓

PNG

JPG

PDF
```

Reject everything else.

______________________________________________________________________

# Generate Random Filenames

Never store files

using user-provided filenames.

Bad

```text id="fus1710"
resume.pdf
```

Good

```text id="fus1711"
8c91a7d2-5b17.pdf
```

Advantages:

- Prevents overwriting
- Avoids filename guessing
- Reduces collisions

Python example

```python id="fus1712"
import uuid

filename = (
    f"{uuid.uuid4()}.pdf"
)
```

______________________________________________________________________

# Store Files Outside the Web Root

Bad

```text id="fus1713"
/var/www/html/uploads/
```

Anyone may access files directly.

Better

```text id="fus1714"
/data/uploads/
```

Serve files

through your application,

not directly from the filesystem.

This allows:

- Authorization
- Logging
- Validation

______________________________________________________________________

# Scan Uploaded Files

Production systems

often scan uploads

for malware.

Common solutions include:

- ClamAV
- Cloud antivirus services

Workflow

```text id="fus1715"
Upload

↓

Virus Scan

↓

Clean?

↓

Store
```

______________________________________________________________________

# Validate Image Content

Suppose your application accepts images.

Instead of trusting

the filename,

actually open the image.

Example

```python id="fus1716"
from PIL import Image

image = Image.open(file.file)

image.verify()
```

The library verifies

that the file

is a valid image.

______________________________________________________________________

# Authorization

Uploading a file

doesn't mean

everyone should download it.

Workflow

```text id="fus1717"
User

↓

File ID

↓

Ownership Check

↓

Download
```

Authorization is just as important

as validation.

______________________________________________________________________

# Logging

Log upload events,

not file contents.

Good

```text id="fus1718"
User uploaded

invoice.pdf

2 MB
```

Avoid logging:

- File contents
- Personal documents
- Sensitive information

______________________________________________________________________

# Secure Upload Workflow

```text id="fus1719"
Receive File

↓

Authentication

↓

Authorization

↓

Extension Check

↓

MIME Check

↓

Content Validation

↓

Virus Scan

↓

Generate Filename

↓

Store Outside Web Root

↓

Database Record
```

This is the workflow

used in many production systems.

______________________________________________________________________

# Defense in Depth

Protect uploads using multiple layers.

```text id="fus1720"
Authentication

↓

Authorization

↓

Validation

↓

Virus Scan

↓

Random Filename

↓

Secure Storage

↓

Logging
```

______________________________________________________________________

# Best Practices

✅ Restrict allowed file types.

✅ Validate file content.

✅ Enforce file size limits.

✅ Generate random filenames.

✅ Store files outside the web root.

✅ Scan uploads for malware.

✅ Verify ownership before downloads.

✅ Log upload events.

______________________________________________________________________

# Common Mistakes

### Trusting File Extensions

Extensions are easy to change.

Always inspect the file itself.

______________________________________________________________________

### Unlimited Upload Size

Large uploads

can exhaust

disk space

and memory.

______________________________________________________________________

### Public Upload Directory

Don't expose uploaded files

directly to the Internet.

Serve them through authenticated endpoints.

______________________________________________________________________

### Using Original Filenames

Generate unique filenames

for every upload.

______________________________________________________________________

### Skipping Authorization

Only authorized users

should access uploaded files.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| ----------------- | ---------------- |
| Trust extension | Validate content |
| Unlimited uploads | File size limits |
| Original filename | UUID filename |
| Public directory | Secure storage |
| No virus scan | Malware scanning |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What security checks should be performed when accepting file uploads?

A secure file upload process should authenticate the user, authorize the upload, restrict allowed file types, validate
the actual file content, enforce file size limits, generate unique filenames, store files outside the web root, scan
files for malware, log upload events, and verify authorization again before allowing downloads.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Why file uploads are risky
- File extension vs content validation
- MIME types
- File size limits
- Secure storage
- Malware scanning
- Authorization
- Best practices

______________________________________________________________________

# What's Next

[API Security](18-api-security.md)

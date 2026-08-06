# S3 Fundamentals

> **Course:** AWS for Backend Engineers
>
> **Module:** 3
>
> **File:** `05_s3_fundamentals.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Amazon S3 is
- Why S3 exists
- Object Storage
- Buckets
- Objects
- Keys
- Metadata
- Versioning
- Storage Classes
- Encryption
- Public vs Private Buckets
- Bucket Policies
- ACLs (Overview)
- Object Lifecycle
- Console
- AWS CLI
- AWS SDK (Python boto3)
- Uploading & Downloading Files
- Production Best Practices

______________________________________________________________________

# What is Amazon S3?

**Amazon S3 (Simple Storage Service)** is AWS's highly durable **Object Storage Service**.

Unlike EC2, which stores data on disks attached to virtual machines, S3 stores data as **objects** inside **buckets**.

It is designed for storing virtually unlimited amounts of data.

Examples

- Images
- Videos
- PDFs
- Backups
- Log files
- Static websites
- Machine Learning datasets
- Application uploads

______________________________________________________________________

# Why Was S3 Created?

Imagine a social media application.

Users upload

```
Photos

Videos

Documents
```

If files are stored on an EC2 server:

```
EC2 Disk

↓

Full

↓

Application Stops Uploading
```

Problems:

- Limited disk space
- Difficult backups
- Poor scalability
- Hard to share across multiple servers

Instead

```
Users

↓

S3 Bucket

↓

Unlimited Storage
```

______________________________________________________________________

# Real World Analogy

Imagine a warehouse.

```
Warehouse

↓

Shelves

↓

Boxes

↓

Labels
```

In S3

```
Bucket

↓

Objects

↓

Object Keys
```

The warehouse can grow without you buying new land.

______________________________________________________________________

# Object Storage

Unlike traditional file systems,

S3 stores **objects**.

Each object contains:

- File Data
- Metadata
- Unique Key

Example

```
photo.jpg

↓

Data

+

Metadata

+

Key
```

______________________________________________________________________

# Bucket

A Bucket is the top-level container in S3.

Example

```
company-images

customer-documents

logs-production

backup-storage
```

Every object belongs to exactly one bucket.

______________________________________________________________________

# Bucket Naming Rules

Bucket names:

- Must be globally unique
- Use lowercase letters
- Can include numbers
- Can include hyphens (`-`)
- Cannot contain spaces
- Cannot contain uppercase letters

Example

Good

```
company-images

user-uploads

production-logs
```

Bad

```
CompanyImages

User Uploads

MyBucket
```

______________________________________________________________________

# Object

An Object is a file stored in S3.

Examples

```
invoice.pdf

photo.png

video.mp4

resume.docx
```

Every object has

- Data
- Metadata
- Object Key
- Storage Class

______________________________________________________________________

# Object Key

The Object Key uniquely identifies an object within a bucket.

Example

```
images/profile/user1.png
```

Although it looks like folders,

S3 actually stores a single key string.

```
images/

↓

profile/

↓

user1.png
```

is simply part of the object's key name.

______________________________________________________________________

# Metadata

Metadata is information about an object.

Examples

- Content Type
- File Size
- Last Modified
- Encryption
- Custom Metadata

Example

```
Content-Type

image/png
```

______________________________________________________________________

# How S3 Stores Data

```
Bucket

↓

Object

↓

Metadata

↓

Storage Class
```

Each object is independently managed.

______________________________________________________________________

# Durability vs Availability

These terms are different.

______________________________________________________________________

## Durability

Durability means:

**Your data is unlikely to be lost.**

S3 is designed for extremely high durability by storing data redundantly across multiple devices within an AWS Region.

______________________________________________________________________

## Availability

Availability means:

**Can you access the data right now?**

High availability means users can access data most of the time.

______________________________________________________________________

# Versioning

Versioning keeps multiple versions of the same object.

Without Versioning

```
Upload

report.pdf

↓

Upload Again

↓

Old File Lost
```

With Versioning

```
Version 1

↓

Version 2

↓

Version 3
```

Previous versions can be recovered.

______________________________________________________________________

# Why Versioning?

Useful for:

- Accidental deletion
- Rollback
- Audit
- Recovery

Production buckets often enable versioning unless there is a reason not to.

______________________________________________________________________

# Storage Classes

Different files have different access patterns.

AWS provides multiple storage classes.

______________________________________________________________________

## Standard

For frequently accessed data.

Examples

- Websites
- APIs
- User uploads

______________________________________________________________________

## Intelligent-Tiering

Automatically moves objects between access tiers based on usage.

Useful when access patterns are unpredictable.

______________________________________________________________________

## Standard-IA (Infrequent Access)

For data that is accessed less often but still requires quick retrieval.

Example

- Monthly reports
- Older documents

______________________________________________________________________

## One Zone-IA

Stores data in a single Availability Zone.

Lower cost, but lower resilience than Standard-IA.

Suitable only for data that can be recreated if necessary.

______________________________________________________________________

## Glacier Instant Retrieval

For archived data that still requires fast retrieval.

______________________________________________________________________

## Glacier Flexible Retrieval

Designed for long-term archival where retrieval times are longer but storage is cheaper.

______________________________________________________________________

## Glacier Deep Archive

Lowest-cost archival storage.

Suitable for records that may rarely, if ever, be accessed.

______________________________________________________________________

# Choosing a Storage Class

| Data | Storage Class |
|------|---------------|
| Website Images | Standard |
| Unknown Access Pattern | Intelligent-Tiering |
| Monthly Reports | Standard-IA |
| Long-Term Backups | Glacier Flexible Retrieval |
| Compliance Archives | Glacier Deep Archive |

______________________________________________________________________

# Encryption

S3 supports encryption to protect stored data.

Options include:

- Server-side encryption with Amazon S3 managed keys (SSE-S3)
- Server-side encryption with AWS KMS keys (SSE-KMS)
- Customer-provided encryption keys (SSE-C)

Encryption helps protect data at rest.

______________________________________________________________________

# Public vs Private Buckets

Private Bucket

```
Only Authorized Users
```

Public Bucket

```
Anyone

↓

Internet
```

Most production buckets should remain private unless public access is explicitly required.

______________________________________________________________________

# Bucket Policy

Bucket Policies are JSON documents that define access at the bucket level.

Example

Allow

```
Read

↓

Public Images
```

Deny

```
Delete

↓

Everyone
```

______________________________________________________________________

# Access Control Lists (ACLs)

ACLs are an older mechanism for controlling access.

Modern AWS best practice is:

- Prefer IAM Policies
- Prefer Bucket Policies
- Keep ACL usage to a minimum unless required for compatibility

______________________________________________________________________

# Object Lifecycle

Lifecycle Rules automatically manage objects over time.

Example

```
Upload

↓

30 Days

↓

Move to Standard-IA

↓

180 Days

↓

Move to Glacier

↓

365 Days

↓

Delete
```

This reduces storage costs automatically.

______________________________________________________________________

# Common S3 Use Cases

- User uploads
- Static website hosting
- Application backups
- Log storage
- Media hosting
- Software downloads
- Data lakes
- Disaster recovery

______________________________________________________________________

# AWS Console

Using the Console you can:

- Create Buckets
- Upload Files
- Download Files
- Delete Objects
- Enable Versioning
- Configure Encryption
- Configure Lifecycle Rules
- View Object Metadata
- Manage Bucket Policies

______________________________________________________________________

# AWS CLI

## List Buckets

```bash
aws s3 ls
```

______________________________________________________________________

## Create Bucket

```bash
aws s3 mb s3://my-company-bucket
```

______________________________________________________________________

## Upload File

```bash
aws s3 cp photo.jpg s3://my-company-bucket/
```

______________________________________________________________________

## Download File

```bash
aws s3 cp s3://my-company-bucket/photo.jpg .
```

______________________________________________________________________

## Copy File

```bash
aws s3 cp \
    s3://source-bucket/photo.jpg \
    s3://destination-bucket/photo.jpg
```

______________________________________________________________________

## Delete File

```bash
aws s3 rm s3://my-company-bucket/photo.jpg
```

______________________________________________________________________

## Sync Folder

```bash
aws s3 sync ./images s3://my-company-bucket/images
```

One of the most commonly used CLI commands.

______________________________________________________________________

# AWS SDK (Python boto3)

## Installation

```bash
pip install boto3
```

______________________________________________________________________

## Create Client

```python
import boto3

s3 = boto3.client("s3")
```

______________________________________________________________________

## List Buckets

```python
response = s3.list_buckets()

for bucket in response["Buckets"]:
    print(bucket["Name"])
```

______________________________________________________________________

## Upload File

```python
s3.upload_file(
    "photo.jpg",
    "my-company-bucket",
    "photo.jpg"
)
```

______________________________________________________________________

## Download File

```python
s3.download_file(
    "my-company-bucket",
    "photo.jpg",
    "photo.jpg"
)
```

______________________________________________________________________

## Delete Object

```python
s3.delete_object(
    Bucket="my-company-bucket",
    Key="photo.jpg"
)
```

______________________________________________________________________

# Common S3 Operations

Daily operations include:

- Upload files
- Download files
- Delete objects
- Copy objects
- Enable versioning
- Configure lifecycle rules
- Review bucket permissions
- Generate reports

______________________________________________________________________

# Common Mistakes

❌ Making production buckets public unintentionally

❌ Disabling versioning for important data

❌ Storing secrets in publicly accessible buckets

❌ Using the Standard storage class for long-term archives

❌ Not enabling encryption

❌ Using wildcard IAM permissions on S3 resources

❌ Forgetting lifecycle rules, leading to unnecessary storage costs

______________________________________________________________________

# Production Best Practices

- Keep buckets private by default.
- Enable versioning for critical data.
- Enable server-side encryption.
- Use lifecycle policies for cost optimization.
- Apply least-privilege IAM policies.
- Block public access unless intentionally required.
- Use descriptive bucket names.
- Enable logging and monitoring.
- Store application uploads outside EC2 instances.
- Regularly review bucket policies.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should uploaded user files be stored in S3 instead of on an EC2 instance?**

### Answer

S3 is designed specifically for scalable object storage.

Compared to storing files on EC2:

1. S3 provides virtually unlimited storage capacity.
1. Multiple application servers can access the same objects.
1. Objects remain available even if an EC2 instance is replaced.
1. Built-in features such as versioning, lifecycle policies, encryption, and replication simplify data management.
1. Storage can be optimized using different storage classes.
1. It integrates easily with services such as CloudFront, Lambda, and Event Notifications.

Keeping application servers stateless also makes Auto Scaling and deployments much simpler.

______________________________________________________________________

# Summary

In this chapter you learned:

- What Amazon S3 is
- Object Storage
- Buckets
- Objects
- Object Keys
- Metadata
- Versioning
- Storage Classes
- Encryption
- Public vs Private Buckets
- Bucket Policies
- ACLs
- Lifecycle Rules
- AWS Console
- AWS CLI
- boto3 SDK
- Production best practices

S3 is one of the most widely used AWS services and is the standard solution for storing files, backups, logs, media, and
static content.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is Amazon S3?
1. Why was S3 created?
1. What is Object Storage?
1. What is a Bucket?
1. What is an Object?

______________________________________________________________________

## Buckets & Objects

6. What is an Object Key?
1. Why aren't S3 folders real directories?
1. What information does Metadata contain?
1. Why must bucket names be globally unique?

______________________________________________________________________

## Versioning & Storage

10. What is Versioning?
01. Why is Versioning useful?
01. Compare Standard and Intelligent-Tiering storage classes.
01. When would you choose Glacier Deep Archive?
01. What is One Zone-IA, and when should it be used?

______________________________________________________________________

## Security

15. Why should production buckets usually remain private?
01. What is a Bucket Policy?
01. Why are ACLs generally discouraged?
01. What encryption options does S3 provide?

______________________________________________________________________

## Lifecycle

19. What is an S3 Lifecycle Rule?
01. How can Lifecycle Rules reduce costs?

______________________________________________________________________

## CLI & SDK

21. Which CLI command uploads a file?
01. Which CLI command synchronizes an entire directory?
01. Which boto3 method uploads a file?
01. How do you delete an object using boto3?

______________________________________________________________________

## Scenario-Based

25. Your application stores uploaded images on EC2. What problems might arise?
01. You accidentally overwrite an important document. Which S3 feature would help recover it?
01. Your company stores compliance records that may not be accessed for years. Which storage class would you recommend?
01. A bucket containing confidential customer documents is accidentally made public. What immediate actions would you take?
01. Your storage bill continues to grow because old log files are never accessed. How could Lifecycle Rules help?
01. Your application is deployed across multiple EC2 instances behind a Load Balancer. Why is S3 a better location for user uploads than the local filesystem of each server?

______________________________________________________________________

## Next

[S3 Advanced](06_s3_advanced.md)

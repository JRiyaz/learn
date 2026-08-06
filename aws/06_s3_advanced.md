# S3 Advanced

> **Course:** AWS for Backend Engineers
>
> **Module:** 3
>
> **File:** `06_s3_advanced.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Multipart Upload
- Multipart Download
- Presigned URLs
- S3 Event Notifications
- Cross-Region Replication (CRR)
- Same-Region Replication (SRR)
- Static Website Hosting
- S3 Access Points
- Object Lock
- Object Versioning Internals
- Lifecycle Policies (Advanced)
- Performance Optimization
- Request Rate Scaling
- S3 Consistency Model
- Cost Optimization
- Logging
- Monitoring
- Security Best Practices
- Production Architecture

______________________________________________________________________

# Why Advanced S3?

Uploading a file to S3 is easy.

Running a production system that stores

```
Millions

↓

Billions

↓

Trillions

of Objects
```

requires understanding:

- Performance
- Security
- Replication
- Availability
- Cost Optimization
- Automation

______________________________________________________________________

# Large File Upload Problem

Suppose a user uploads

```
100 GB Video
```

Traditional upload

```
Client

↓

Upload

↓

Network Failure

↓

Start Again
```

This is inefficient.

______________________________________________________________________

# Multipart Upload

Multipart Upload divides a large object into smaller parts.

```
100 GB

↓

Part 1

↓

Part 2

↓

Part 3

↓

...

↓

Combine

↓

Final Object
```

______________________________________________________________________

# Advantages of Multipart Upload

- Faster uploads
- Parallel uploads
- Resume failed uploads
- Better reliability
- Improved throughput

AWS recommends multipart upload for large objects (commonly for objects over 100 MB, and it becomes required beyond
certain size limits).

______________________________________________________________________

# Multipart Upload Flow

```
Create Upload

↓

Upload Parts

↓

Upload Part 1

↓

Upload Part 2

↓

Upload Part 3

↓

Complete Upload

↓

Final Object
```

______________________________________________________________________

# Multipart Download

Objects can also be downloaded in parallel.

Benefits

- Faster downloads
- Better performance
- Parallel processing

______________________________________________________________________

# Presigned URL

Normally,

Only authorized users can upload.

Sometimes you want users to upload files **directly** to S3 without exposing AWS credentials.

Solution

```
Backend

↓

Generate Presigned URL

↓

Client

↓

Upload Directly

↓

S3
```

______________________________________________________________________

# Why Presigned URLs?

Without Presigned URL

```
Client

↓

Backend

↓

S3
```

Problems

- Backend bandwidth increases
- Higher latency
- Higher infrastructure cost

With Presigned URL

```
Backend

↓

Signed URL

↓

Client

↓

S3
```

Backend is bypassed for the file transfer.

______________________________________________________________________

# Presigned URL Characteristics

- Temporary
- Secure
- Time-limited
- Permission-limited

Example

```
Valid

15 Minutes
```

After expiration,

the URL no longer works.

______________________________________________________________________

# Generating a Presigned URL (boto3)

```python
import boto3

s3 = boto3.client("s3")

url = s3.generate_presigned_url(
    "put_object",
    Params={
        "Bucket": "user-uploads",
        "Key": "photo.jpg"
    },
    ExpiresIn=900
)

print(url)
```

______________________________________________________________________

# S3 Event Notifications

S3 can automatically notify other AWS services when events occur.

Example

```
Upload

↓

Trigger Event

↓

Lambda

↓

Resize Image
```

______________________________________________________________________

# Supported Event Targets

S3 can send events to:

- Lambda
- SNS
- SQS
- EventBridge

Common use cases:

- Image processing
- Video transcoding
- Virus scanning
- Notifications
- Data pipelines

______________________________________________________________________

# Example Architecture

```
User

↓

Upload Image

↓

S3

↓

Lambda

↓

Thumbnail

↓

Store Back in S3
```

No polling required.

______________________________________________________________________

# Cross-Region Replication (CRR)

CRR automatically copies objects to another AWS Region.

Example

```
Mumbai

↓

Upload

↓

Replicate

↓

Singapore
```

Benefits

- Disaster Recovery
- Compliance
- Global Applications

Versioning must be enabled on both buckets.

______________________________________________________________________

# Same-Region Replication (SRR)

Replication occurs within the same Region.

Useful for:

- Separate environments
- Compliance
- Data ownership separation
- Log processing

______________________________________________________________________

# Replication Flow

```
Bucket A

↓

Replication Rule

↓

Bucket B
```

Replication is asynchronous.

______________________________________________________________________

# Static Website Hosting

S3 can host static websites.

Example

```
HTML

CSS

JavaScript

↓

S3

↓

Website
```

Suitable for:

- Portfolio sites
- Documentation
- Landing pages
- Static frontends

Dynamic server-side applications still require compute services.

______________________________________________________________________

# S3 Access Points

Large organizations may have many applications using one bucket.

Instead of one large bucket policy,

create multiple Access Points.

Example

```
Bucket

↓

Marketing Access Point

↓

Finance Access Point

↓

Analytics Access Point
```

Each Access Point has its own permissions.

______________________________________________________________________

# Object Lock

Object Lock prevents objects from being deleted or modified for a retention period.

Useful for:

- Financial records
- Compliance
- Legal requirements

______________________________________________________________________

# Retention Modes

## Governance Mode

Privileged users may override restrictions under appropriate permissions.

______________________________________________________________________

## Compliance Mode

Objects cannot be modified or deleted until the retention period expires.

Even administrators cannot bypass this mode.

______________________________________________________________________

# Lifecycle Policies (Advanced)

Example

```
Upload

↓

30 Days

↓

Standard-IA

↓

90 Days

↓

Glacier Flexible Retrieval

↓

365 Days

↓

Delete
```

Entire storage lifecycle becomes automated.

______________________________________________________________________

# S3 Consistency Model

Amazon S3 now provides **strong read-after-write consistency** for:

- PUT
- GET
- LIST

This means:

```
Upload Object

↓

Immediately Read Object

↓

Latest Version Returned
```

No additional consistency layer is required for standard operations.

______________________________________________________________________

# Request Rate Scaling

Historically,

developers carefully distributed object prefixes.

Modern S3 automatically scales request rates.

You generally do **not** need to randomize prefixes solely for performance.

______________________________________________________________________

# Performance Optimization

Best practices:

- Use Multipart Upload
- Parallel uploads
- Parallel downloads
- Use CloudFront for content delivery
- Compress files when appropriate
- Cache static assets
- Avoid unnecessary object rewrites

______________________________________________________________________

# Cost Optimization

Ways to reduce costs:

- Lifecycle Rules
- Intelligent-Tiering
- Glacier storage classes
- Delete incomplete multipart uploads
- Delete unused objects
- Compress logs
- Review storage reports

______________________________________________________________________

# Delete Incomplete Multipart Uploads

Sometimes uploads fail.

Example

```
100 Parts

↓

Uploaded

30 Parts

↓

Cancelled
```

The uploaded parts still consume storage.

Lifecycle Rules can automatically remove incomplete multipart uploads.

______________________________________________________________________

# Server Access Logging

S3 can log requests made to a bucket.

Example logs include:

- GET
- PUT
- DELETE
- Requester
- Timestamp
- Source IP

Useful for:

- Auditing
- Security
- Troubleshooting

______________________________________________________________________

# Monitoring with CloudWatch

Monitor:

- Request Count
- Errors
- Latency
- Bytes Downloaded
- Bytes Uploaded

CloudWatch helps identify performance and operational issues.

______________________________________________________________________

# Security Best Practices

- Enable versioning.
- Enable server-side encryption.
- Block public access by default.
- Use Bucket Policies instead of ACLs where possible.
- Rotate KMS keys according to organizational policies.
- Use Presigned URLs instead of exposing AWS credentials.
- Enable logging.
- Apply least-privilege IAM permissions.
- Review bucket access regularly.

______________________________________________________________________

# Production Architecture

```
Users

↓

Application

↓

Generate Presigned URL

↓

Client Upload

↓

S3

↓

Event Notification

↓

Lambda

↓

Thumbnail

↓

S3

↓

CloudFront

↓

Users
```

This architecture is common for modern web applications.

______________________________________________________________________

# Common Mistakes

❌ Uploading large files without Multipart Upload

❌ Sending all uploads through backend servers

❌ Forgetting to abort incomplete multipart uploads

❌ Making buckets public unnecessarily

❌ Disabling versioning

❌ Using Standard storage for archival data

❌ Ignoring lifecycle policies

❌ Using long-lived AWS credentials on clients

______________________________________________________________________

# Interview Deep Dive

### Question

**How would you design an image upload service for millions of users using S3?**

### Answer

A scalable design would include:

1. The backend authenticates the user.
1. The backend generates a short-lived Presigned URL.
1. The client uploads the image directly to S3.
1. S3 triggers an Event Notification.
1. A Lambda function generates thumbnails and performs image validation.
1. Processed images are stored back in S3.
1. CloudFront serves images globally with low latency.
1. Lifecycle Rules archive or delete unused objects when appropriate.
1. Versioning and server-side encryption protect stored objects.

This design minimizes backend load while remaining scalable and secure.

______________________________________________________________________

# Summary

In this chapter you learned:

- Multipart Upload
- Multipart Download
- Presigned URLs
- Event Notifications
- Cross-Region Replication
- Same-Region Replication
- Static Website Hosting
- Access Points
- Object Lock
- Lifecycle Policies
- Strong Consistency
- Performance Optimization
- Cost Optimization
- Logging
- Monitoring
- Production Architecture

These features enable Amazon S3 to support large-scale production systems storing millions or billions of objects.

______________________________________________________________________

# Practice Questions

## Multipart Upload

1. What is Multipart Upload?
1. Why is Multipart Upload faster?
1. When should Multipart Upload be used?
1. Why should incomplete multipart uploads be cleaned up?

______________________________________________________________________

## Presigned URLs

5. What is a Presigned URL?
1. Why are Presigned URLs more secure than embedding AWS credentials in a client?
1. What information controls a Presigned URL's validity?
1. When would you use a Presigned URL in a production application?

______________________________________________________________________

## Event Notifications

9. What are S3 Event Notifications?
1. Which AWS services can receive S3 events?
1. Give three real-world use cases for S3 Event Notifications.

______________________________________________________________________

## Replication

12. What is Cross-Region Replication?
01. What is Same-Region Replication?
01. Why must versioning be enabled before replication?
01. When would you choose CRR instead of SRR?

______________________________________________________________________

## Object Lock & Lifecycle

16. What is Object Lock?
01. Compare Governance Mode and Compliance Mode.
01. How do Lifecycle Rules reduce storage costs?

______________________________________________________________________

## Performance

19. What consistency model does Amazon S3 provide?
01. How can CloudFront improve S3 performance?
01. Why are randomized object prefixes generally unnecessary today?

______________________________________________________________________

## Monitoring & Security

22. What information does Server Access Logging capture?
01. Which CloudWatch metrics are useful for monitoring S3?
01. List five S3 security best practices.

______________________________________________________________________

## Scenario-Based

25. Your application allows users to upload 20 GB video files. How would you design the upload process?
01. A media application serves users worldwide. How would you reduce image download latency?
01. Your legal department requires files to be undeletable for seven years. Which S3 feature would you use?
01. Your storage costs increase every month because old backups remain in Standard storage. How would you optimize costs?
01. A backend API is overwhelmed because every file upload passes through it. How would you redesign the architecture?
01. A compliance audit requires an immutable archive of financial documents. Which S3 features would you combine to satisfy this requirement?

______________________________________________________________________

## Next

[VPC Fundamentals](07_vpc_fundamentals.md)

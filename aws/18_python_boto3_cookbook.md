# Python boto3 Cookbook

> **Course:** AWS for Backend Engineers
>
> **Module:** 8
>
> **File:** `18_python_boto3_cookbook.md`

______________________________________________________________________

# What You Will Learn

This chapter is a practical reference for using **boto3**, the official AWS SDK for Python.

You will learn:

- Installing boto3
- Authentication
- Sessions
- Clients vs Resources
- IAM
- EC2
- S3
- CloudWatch
- ECR
- ECS
- Error Handling
- Pagination
- Waiters
- Best Practices

______________________________________________________________________

# What is boto3?

**boto3** is the official AWS SDK for Python.

Instead of using the AWS CLI,

your Python application can directly communicate with AWS.

Example

```python
import boto3

s3 = boto3.client("s3")
```

______________________________________________________________________

# Install boto3

```bash
pip install boto3
```

Verify installation

```bash
pip show boto3
```

______________________________________________________________________

# Authentication

boto3 automatically searches for credentials in the following order (simplified):

1. Environment variables
1. AWS CLI credentials/config
1. IAM Role (EC2, ECS, Lambda, etc.)

In production,

prefer **IAM Roles**.

______________________________________________________________________

# Create Session

```python
import boto3

session = boto3.Session(
    profile_name="production"
)
```

______________________________________________________________________

# Default Session

```python
import boto3

session = boto3.Session()
```

______________________________________________________________________

# Create Client

```python
import boto3

s3 = boto3.client("s3")
```

______________________________________________________________________

# Create Resource

```python
import boto3

ec2 = boto3.resource("ec2")
```

______________________________________________________________________

# Client vs Resource

| Client | Resource |
|---------|----------|
| Low-level API | Higher-level abstraction |
| Maps closely to AWS APIs | More Pythonic interface |
| Complete service coverage | Not available for every feature/service |
| Preferred for new development | Useful for supported object-oriented workflows |

In modern applications,

many developers primarily use **clients** because they expose the latest AWS API features.

______________________________________________________________________

# IAM Examples

## List Users

```python
import boto3

iam = boto3.client("iam")

response = iam.list_users()

for user in response["Users"]:
    print(user["UserName"])
```

______________________________________________________________________

# EC2 Examples

## List Instances

```python
import boto3

ec2 = boto3.client("ec2")

response = ec2.describe_instances()

print(response)
```

______________________________________________________________________

## Start Instance

```python
ec2.start_instances(
    InstanceIds=[
        "i-0123456789"
    ]
)
```

______________________________________________________________________

## Stop Instance

```python
ec2.stop_instances(
    InstanceIds=[
        "i-0123456789"
    ]
)
```

______________________________________________________________________

# S3 Examples

## List Buckets

```python
import boto3

s3 = boto3.client("s3")

response = s3.list_buckets()

for bucket in response["Buckets"]:
    print(bucket["Name"])
```

______________________________________________________________________

## Upload File

```python
s3.upload_file(
    "image.png",
    "my-bucket",
    "image.png"
)
```

______________________________________________________________________

## Download File

```python
s3.download_file(
    "my-bucket",
    "image.png",
    "image.png"
)
```

______________________________________________________________________

## Delete Object

```python
s3.delete_object(
    Bucket="my-bucket",
    Key="image.png"
)
```

______________________________________________________________________

# CloudWatch Examples

## List Metrics

```python
cloudwatch = boto3.client(
    "cloudwatch"
)

response = cloudwatch.list_metrics()

print(response)
```

______________________________________________________________________

## Put Custom Metric

```python
cloudwatch.put_metric_data(
    Namespace="Company/API",
    MetricData=[
        {
            "MetricName": "Orders",
            "Value": 100
        }
    ]
)
```

______________________________________________________________________

# ECR Examples

## List Repositories

```python
ecr = boto3.client("ecr")

response = ecr.describe_repositories()

print(response)
```

______________________________________________________________________

## Create Repository

```python
ecr.create_repository(
    repositoryName="backend"
)
```

______________________________________________________________________

# ECS Examples

## List Clusters

```python
ecs = boto3.client("ecs")

print(
    ecs.list_clusters()
)
```

______________________________________________________________________

## List Services

```python
ecs.list_services(
    cluster="production"
)
```

______________________________________________________________________

## Update Service

```python
ecs.update_service(
    cluster="production",
    service="backend",
    forceNewDeployment=True
)
```

______________________________________________________________________

# Waiters

Sometimes AWS operations are asynchronous.

Instead of polling manually,

use Waiters.

Example

```python
waiter = ec2.get_waiter(
    "instance_running"
)

waiter.wait(
    InstanceIds=[
        "i-0123456789"
    ]
)
```

The program waits until the instance is running.

______________________________________________________________________

# Pagination

Many AWS APIs return limited results.

Instead of:

```
1000 Instances
```

You may receive only the first page.

Use a paginator.

Example

```python
paginator = ec2.get_paginator(
    "describe_instances"
)

for page in paginator.paginate():
    print(page)
```

______________________________________________________________________

# Exception Handling

```python
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")

try:
    s3.list_buckets()

except ClientError as e:
    print(e)
```

Always handle AWS API errors gracefully.

______________________________________________________________________

# Common Errors

## AccessDenied

Missing permission.

______________________________________________________________________

## ResourceNotFound

Wrong resource.

______________________________________________________________________

## ValidationException

Invalid parameters.

______________________________________________________________________

## ThrottlingException

Too many API requests.

Implement retries with exponential backoff where appropriate.

______________________________________________________________________

# Environment Variables

Instead of hardcoding credentials,

use

```bash
export AWS_ACCESS_KEY_ID=...

export AWS_SECRET_ACCESS_KEY=...
```

For production workloads,

prefer IAM Roles over long-lived credentials.

______________________________________________________________________

# Reading Credentials

```python
session = boto3.Session()

credentials = session.get_credentials()

print(credentials)
```

Useful for debugging.

______________________________________________________________________

# Regions

Specify Region

```python
boto3.client(
    "ec2",
    region_name="ap-south-1"
)
```

______________________________________________________________________

# STS

Who am I?

```python
sts = boto3.client("sts")

print(
    sts.get_caller_identity()
)
```

Very useful during debugging.

______________________________________________________________________

# Production Example

Upload user image

```python
import boto3

s3 = boto3.client("s3")

s3.upload_file(
    "avatar.png",
    "uploads",
    "users/123/avatar.png"
)
```

Simple.

Reliable.

______________________________________________________________________

# Production Deployment Example

Trigger ECS deployment

```python
import boto3

ecs = boto3.client("ecs")

ecs.update_service(
    cluster="production",
    service="backend",
    forceNewDeployment=True
)
```

Often used by deployment automation.

______________________________________________________________________

# Common Mistakes

❌ Hardcoding AWS credentials

❌ Ignoring exceptions

❌ Forgetting pagination

❌ Forgetting Region

❌ Not using Waiters

❌ Giving excessive IAM permissions

❌ Ignoring retries after throttling

______________________________________________________________________

# Production Best Practices

- Use IAM Roles.
- Use boto3 Clients for most new applications.
- Handle exceptions.
- Use Waiters.
- Use Paginators.
- Keep Regions configurable.
- Implement retries with exponential backoff.
- Never hardcode credentials.
- Log AWS API failures.

______________________________________________________________________

# Interview Deep Dive

### Question

**How would you write a production-ready Python application that interacts with AWS using boto3?**

### Answer

A production-ready application should:

1. Authenticate using IAM Roles whenever possible.
1. Use boto3 Clients for AWS service interactions.
1. Handle `ClientError` exceptions gracefully.
1. Use Paginators when listing large numbers of resources.
1. Use Waiters for asynchronous operations.
1. Avoid hardcoded credentials and Regions.
1. Log API failures for troubleshooting.
1. Implement retry logic for transient failures such as throttling.
1. Follow the principle of least privilege for IAM permissions.

______________________________________________________________________

# Summary

This cookbook covered practical boto3 examples for:

- Sessions
- Clients
- Resources
- IAM
- EC2
- S3
- CloudWatch
- ECR
- ECS
- Pagination
- Waiters
- Error Handling
- STS
- Authentication

These are among the most commonly used boto3 features for backend engineering and AWS automation.

______________________________________________________________________

# Practice Questions

## boto3 Basics

1. What is boto3?
1. Why use boto3 instead of the AWS CLI?
1. What is the difference between a Client and a Resource?
1. Which authentication method is preferred in production?

______________________________________________________________________

## AWS Services

5. How do you list S3 buckets using boto3?
1. How do you upload a file?
1. How do you start an EC2 instance?
1. How do you trigger an ECS deployment?

______________________________________________________________________

## Reliability

9. Why should you use Waiters?
1. Why are Paginators important?
1. Why should AWS API calls be wrapped in exception handling?

______________________________________________________________________

## Security

12. Why are IAM Roles preferred?
01. Why shouldn't AWS credentials be hardcoded?
01. How can you determine which AWS identity your application is using?

______________________________________________________________________

## Architecture

15. How would you organize boto3 clients in a large Python application?
01. Why should Regions be configurable?
01. How should applications handle API throttling?

______________________________________________________________________

## Scenario-Based

18. Your application lists EC2 instances, but only the first 1000 instances are returned. What boto3 feature solves this?
01. Your deployment script updates an ECS service and immediately checks whether new tasks are running. Why might a Waiter or polling mechanism be necessary?
01. Your production application occasionally receives `ThrottlingException` responses from AWS APIs. How would you make the application more resilient?
01. A developer commits AWS Access Keys into the repository. What changes would you recommend for both development and production environments?
01. Your Python application works locally but fails on ECS because credentials cannot be found. What authentication approach should ECS use instead?

______________________________________________________________________

# Congratulations!

You have completed the **AWS Crash Course for Backend Engineers**.

You now have a practical understanding of:

- ✅ IAM
- ✅ EC2
- ✅ S3
- ✅ VPC
- ✅ CloudWatch
- ✅ ECR
- ✅ ECS
- ✅ AWS CLI
- ✅ boto3
- ✅ Production Architecture
- ✅ CI/CD Deployment
- ✅ Monitoring
- ✅ Security
- ✅ Best Practices

This foundation is enough to confidently discuss AWS in most backend software engineering interviews and to continue
learning advanced AWS services such as Lambda, API Gateway, RDS, ElastiCache, SQS, SNS, EventBridge, Step Functions,
EKS, and CDK.

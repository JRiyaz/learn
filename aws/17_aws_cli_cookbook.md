# AWS CLI Cookbook

> **Course:** AWS for Backend Engineers
>
> **Module:** 8
>
> **File:** `17_aws_cli_cookbook.md`

______________________________________________________________________

# What You Will Learn

This chapter is a practical reference containing commonly used AWS CLI commands for:

- AWS CLI Installation
- Configuration
- Profiles
- IAM
- EC2
- S3
- VPC
- CloudWatch
- ECR
- ECS
- Debugging
- Automation
- Shell Scripting
- Useful Tips

> **Note:** Replace placeholder values (for example, `ACCOUNT_ID`, `REGION`, `INSTANCE_ID`, `BUCKET_NAME`) with your own AWS resources.

______________________________________________________________________

# What is AWS CLI?

AWS CLI (Command Line Interface) allows you to manage AWS resources directly from your terminal.

Instead of clicking buttons in the AWS Console,

you execute commands.

Example

```bash
aws s3 ls
```

______________________________________________________________________

# Why Use AWS CLI?

Benefits

- Automation
- CI/CD
- Shell Scripts
- Repeatable Operations
- Faster than Console
- Infrastructure Management

______________________________________________________________________

# Check Version

```bash
aws --version
```

Example Output

```text
aws-cli/2.28.3 Python/3.x
```

______________________________________________________________________

# Configure Credentials

```bash
aws configure
```

Prompts

```text
AWS Access Key ID

AWS Secret Access Key

Region

Output Format
```

______________________________________________________________________

# View Current Configuration

```bash
aws configure list
```

______________________________________________________________________

# View Current Identity

```bash
aws sts get-caller-identity
```

One of the most useful debugging commands.

______________________________________________________________________

# Profiles

Create another profile

```bash
aws configure --profile production
```

Use profile

```bash
aws s3 ls --profile production
```

List profiles

```bash
aws configure list-profiles
```

______________________________________________________________________

# Common Output Formats

JSON

```bash
aws ec2 describe-instances \
    --output json
```

Table

```bash
aws ec2 describe-instances \
    --output table
```

Text

```bash
aws ec2 describe-instances \
    --output text
```

______________________________________________________________________

# Useful Global Options

Specify Region

```bash
aws s3 ls \
    --region ap-south-1
```

Enable Debug Output

```bash
aws s3 ls \
    --debug
```

Query JSON Output

```bash
aws ec2 describe-instances \
    --query "Reservations[].Instances[].InstanceId"
```

______________________________________________________________________

# IAM Commands

## List Users

```bash
aws iam list-users
```

______________________________________________________________________

## Create User

```bash
aws iam create-user \
    --user-name backend-user
```

______________________________________________________________________

## Delete User

```bash
aws iam delete-user \
    --user-name backend-user
```

______________________________________________________________________

## List Groups

```bash
aws iam list-groups
```

______________________________________________________________________

## Create Group

```bash
aws iam create-group \
    --group-name developers
```

______________________________________________________________________

## Add User to Group

```bash
aws iam add-user-to-group \
    --group-name developers \
    --user-name backend-user
```

______________________________________________________________________

## List Roles

```bash
aws iam list-roles
```

______________________________________________________________________

# EC2 Commands

## List Instances

```bash
aws ec2 describe-instances
```

______________________________________________________________________

## Start Instance

```bash
aws ec2 start-instances \
    --instance-ids INSTANCE_ID
```

______________________________________________________________________

## Stop Instance

```bash
aws ec2 stop-instances \
    --instance-ids INSTANCE_ID
```

______________________________________________________________________

## Reboot Instance

```bash
aws ec2 reboot-instances \
    --instance-ids INSTANCE_ID
```

______________________________________________________________________

## Terminate Instance

```bash
aws ec2 terminate-instances \
    --instance-ids INSTANCE_ID
```

______________________________________________________________________

## Describe Instance Status

```bash
aws ec2 describe-instance-status
```

______________________________________________________________________

## Create Security Group

```bash
aws ec2 create-security-group \
    --group-name backend-sg \
    --description "Backend Security Group"
```

______________________________________________________________________

# S3 Commands

## List Buckets

```bash
aws s3 ls
```

______________________________________________________________________

## Create Bucket

```bash
aws s3 mb s3://BUCKET_NAME
```

______________________________________________________________________

## Upload File

```bash
aws s3 cp image.png \
s3://BUCKET_NAME/
```

______________________________________________________________________

## Download File

```bash
aws s3 cp \
s3://BUCKET_NAME/image.png .
```

______________________________________________________________________

## Sync Folder

```bash
aws s3 sync ./uploads \
s3://BUCKET_NAME/uploads
```

______________________________________________________________________

## Delete File

```bash
aws s3 rm \
s3://BUCKET_NAME/image.png
```

______________________________________________________________________

## Delete Bucket

```bash
aws s3 rb s3://BUCKET_NAME
```

______________________________________________________________________

# VPC Commands

## List VPCs

```bash
aws ec2 describe-vpcs
```

______________________________________________________________________

## Create VPC

```bash
aws ec2 create-vpc \
--cidr-block 10.0.0.0/16
```

______________________________________________________________________

## Create Subnet

```bash
aws ec2 create-subnet \
--vpc-id VPC_ID \
--cidr-block 10.0.1.0/24
```

______________________________________________________________________

## List Route Tables

```bash
aws ec2 describe-route-tables
```

______________________________________________________________________

## List Security Groups

```bash
aws ec2 describe-security-groups
```

______________________________________________________________________

# CloudWatch Commands

## List Metrics

```bash
aws cloudwatch list-metrics
```

______________________________________________________________________

## Get Metric Statistics

```bash
aws cloudwatch get-metric-statistics
```

______________________________________________________________________

## List Log Groups

```bash
aws logs describe-log-groups
```

______________________________________________________________________

## List Log Streams

```bash
aws logs describe-log-streams \
--log-group-name "/aws/ec2/backend"
```

______________________________________________________________________

## Tail Logs

```bash
aws logs tail \
"/aws/ecs/backend" \
--follow
```

One of the most useful commands for debugging.

______________________________________________________________________

# ECR Commands

## List Repositories

```bash
aws ecr describe-repositories
```

______________________________________________________________________

## Create Repository

```bash
aws ecr create-repository \
--repository-name backend-api
```

______________________________________________________________________

## Authenticate Docker

```bash
aws ecr get-login-password \
| docker login \
--username AWS \
--password-stdin \
ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com
```

______________________________________________________________________

## List Images

```bash
aws ecr list-images \
--repository-name backend-api
```

______________________________________________________________________

## Delete Image

```bash
aws ecr batch-delete-image \
--repository-name backend-api \
--image-ids imageTag=v1.0
```

______________________________________________________________________

# ECS Commands

## List Clusters

```bash
aws ecs list-clusters
```

______________________________________________________________________

## List Services

```bash
aws ecs list-services \
--cluster production
```

______________________________________________________________________

## List Tasks

```bash
aws ecs list-tasks \
--cluster production
```

______________________________________________________________________

## Describe Task

```bash
aws ecs describe-tasks \
--cluster production \
--tasks TASK_ID
```

______________________________________________________________________

## Update Service

```bash
aws ecs update-service \
--cluster production \
--service backend \
--force-new-deployment
```

Useful when deploying a new image with an updated task definition.

______________________________________________________________________

# CloudWatch Logs

Tail logs continuously

```bash
aws logs tail \
"/aws/ecs/backend" \
--follow
```

Show last hour

```bash
aws logs tail \
"/aws/ecs/backend" \
--since 1h
```

______________________________________________________________________

# STS Commands

Check identity

```bash
aws sts get-caller-identity
```

Useful when multiple AWS accounts are configured.

______________________________________________________________________

# Cost & Billing

While many billing operations are performed through the AWS Billing Console or Cost Explorer APIs, a common identity
check before cost investigations is:

```bash
aws sts get-caller-identity
```

This helps confirm you're operating in the expected AWS account.

______________________________________________________________________

# Debugging Tips

Who am I?

```bash
aws sts get-caller-identity
```

Region?

```bash
aws configure get region
```

Credentials?

```bash
aws configure list
```

Debug request

```bash
aws s3 ls --debug
```

______________________________________________________________________

# Using JMESPath Queries

Only Instance IDs

```bash
aws ec2 describe-instances \
--query "Reservations[].Instances[].InstanceId"
```

Only Bucket Names

```bash
aws s3api list-buckets \
--query "Buckets[].Name"
```

Pretty output

```bash
aws ec2 describe-instances \
--output table
```

______________________________________________________________________

# Shell Script Example

Start an EC2 instance

```bash
#!/bin/bash

INSTANCE_ID=i-0123456789abcdef0

aws ec2 start-instances \
--instance-ids $INSTANCE_ID
```

______________________________________________________________________

# Deployment Script Example

```bash
#!/bin/bash

docker build -t backend .

docker tag backend:latest \
ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/backend:v2

docker push \
ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/backend:v2

aws ecs update-service \
--cluster production \
--service backend \
--force-new-deployment
```

______________________________________________________________________

# Common AWS CLI Errors

## AccessDenied

Usually means:

- Missing IAM Permission
- Wrong Role
- Wrong AWS Account

______________________________________________________________________

## ResourceNotFound

Usually means:

- Wrong Resource Name
- Wrong Region

______________________________________________________________________

## ExpiredToken

Usually means:

Credentials have expired.

Re-authenticate.

______________________________________________________________________

## InvalidClientTokenId

Usually means:

Wrong credentials.

______________________________________________________________________

# Common Mistakes

❌ Using the wrong AWS profile

❌ Forgetting to specify the Region

❌ Accidentally operating in the wrong AWS account

❌ Running destructive commands without verification

❌ Hardcoding AWS credentials into scripts

______________________________________________________________________

# Production Best Practices

- Use IAM Roles whenever possible.
- Prefer named profiles for multiple environments.
- Use `--query` to simplify automation.
- Use `--output json` for scripting.
- Avoid storing credentials in shell scripts.
- Verify your account with `aws sts get-caller-identity`.
- Test destructive commands in non-production environments first.

______________________________________________________________________

# Interview Deep Dive

### Question

**Your AWS CLI command returns `AccessDenied`. How would you troubleshoot the issue?**

### Answer

A structured approach would include:

1. Verify the active AWS account with `aws sts get-caller-identity`.
1. Confirm the correct AWS profile is being used.
1. Verify the configured Region.
1. Review the IAM user or role permissions.
1. Check for explicit denies from IAM policies, Permission Boundaries, SCPs, or resource policies.
1. Confirm the resource exists in the expected Region.
1. Retry with `--debug` if additional request details are needed.

______________________________________________________________________

# Summary

This cookbook covered commonly used AWS CLI commands for:

- Configuration
- Profiles
- IAM
- EC2
- S3
- VPC
- CloudWatch
- ECR
- ECS
- STS
- Debugging
- Automation

While this isn't every AWS CLI command, these are among the most frequently used by backend engineers and DevOps teams.

______________________________________________________________________

# Practice Questions

## CLI Basics

1. Why use the AWS CLI instead of the Console?
1. How do you configure AWS CLI credentials?
1. How do you switch between AWS profiles?
1. Which command displays the currently authenticated AWS identity?

______________________________________________________________________

## Service Commands

5. Which CLI command lists EC2 instances?
1. Which command uploads a file to S3?
1. Which command lists ECS tasks?
1. Which command authenticates Docker with Amazon ECR?

______________________________________________________________________

## Debugging

9. What causes an `AccessDenied` error?
1. What causes an `ExpiredToken` error?
1. Why is `aws sts get-caller-identity` often the first debugging command you run?
1. How can `--debug` help troubleshoot AWS CLI commands?

______________________________________________________________________

## Automation

13. Why is JSON output preferred for scripting?
01. What is the purpose of the `--query` option?
01. Why should AWS credentials never be hardcoded in shell scripts?

______________________________________________________________________

## Scenario-Based

16. You accidentally update resources in the wrong AWS account. Which CLI command could have prevented this mistake?
01. Your deployment script fails because Docker cannot push to Amazon ECR. Which authentication step might be missing?
01. Your shell script should automatically retrieve only EC2 instance IDs. Which AWS CLI feature would you use?
01. Your CI/CD pipeline reports `ExpiredToken` while deploying. What are the likely causes?
01. You need to automate daily infrastructure operations without using the AWS Console. Why is the AWS CLI a better choice?

______________________________________________________________________

## Next

[Python boto3 Cookbook](18_python_boto3_cookbook.md)

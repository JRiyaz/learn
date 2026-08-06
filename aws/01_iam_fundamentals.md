# IAM Fundamentals

> **Course:** AWS for Backend Engineers
>
> **Module:** 1
>
> **File:** `01_iam_fundamentals.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What IAM is
- Why IAM exists
- Authentication vs Authorization
- IAM Components
- Users
- Groups
- Roles
- Policies
- Managed Policies
- Inline Policies
- Policy JSON Structure
- IAM Credentials
- Access Keys
- Secret Access Keys
- Multi-Factor Authentication (MFA)
- Least Privilege Principle
- IAM Best Practices
- AWS Console
- AWS CLI
- AWS SDK (Python boto3)
- Common IAM Operations
- Production Best Practices

______________________________________________________________________

# What is IAM?

IAM stands for **Identity and Access Management**.

It is the AWS service responsible for controlling **who can access AWS resources** and **what actions they are allowed
to perform**.

Think of IAM as the **security guard of your AWS account**.

Every request made to AWS goes through IAM permission checks.

______________________________________________________________________

# Why Do We Need IAM?

Imagine your company has:

- 40 Developers
- 5 DevOps Engineers
- 2 Database Administrators
- 1 Security Team

Should everyone have full access to everything?

Absolutely not.

Example:

A frontend developer should not be able to delete production databases.

A DevOps engineer should not necessarily access HR files stored in S3.

IAM solves this problem.

______________________________________________________________________

# Real World Analogy

Imagine an office building.

```
Office Building

    |
Reception
    |
Security Guard
    |
Employee Badge
    |
Allowed Floors
```

Different employees have different permissions.

Example

CEO

```
All Floors
```

Developer

```
Engineering Floor
```

HR

```
HR Floor
```

Intern

```
Meeting Rooms Only
```

IAM works exactly like this.

______________________________________________________________________

# Authentication vs Authorization

These two concepts are often confused.

______________________________________________________________________

## Authentication

Authentication answers:

> **Who are you?**

Examples

- Username + Password
- Access Key + Secret Key
- MFA
- SSO

Example

```
Login Successful
```

Identity verified.

______________________________________________________________________

## Authorization

Authorization answers:

> **What are you allowed to do?**

Example

```
User authenticated

↓

Allowed to read S3

↓

Not allowed to terminate EC2
```

______________________________________________________________________

# IAM Architecture

```
          IAM

      /    |     \

 Users Groups Roles

        |

     Policies
```

Policies determine permissions.

______________________________________________________________________

# IAM Components

AWS IAM has four major building blocks:

- Users
- Groups
- Roles
- Policies

Let's understand each.

______________________________________________________________________

# IAM User

An IAM User represents a single person or application.

Examples

```
riyaz

alice

backend-api

jenkins

github-actions
```

A user can have:

- Password
- Access Keys
- Policies
- Group Membership

______________________________________________________________________

# When Should You Create IAM Users?

Create IAM Users for:

- Human administrators
- Developers
- Operations engineers
- CI/CD systems (legacy setups)
- Third-party integrations (when roles are not possible)

Do **not** create an IAM user for every EC2 instance or AWS service. Those should typically use IAM Roles.

______________________________________________________________________

# IAM Group

A Group is a collection of users.

Instead of assigning permissions individually, assign permissions to the group.

Example

```
Developers

    |
    |---- Alice

    |---- Bob

    |---- John
```

Attach one policy.

Everyone inherits it.

______________________________________________________________________

# Benefits of Groups

Without Groups

```
100 Users

↓

Attach policy 100 times
```

With Groups

```
100 Users

↓

1 Group

↓

Attach policy once
```

Much easier to manage.

______________________________________________________________________

# IAM Role

A Role is a set of permissions that can be **assumed temporarily**.

Unlike Users:

- No password
- No permanent Access Keys
- Temporary credentials
- Used by AWS services, applications, or users

______________________________________________________________________

# Why Roles?

Suppose your EC2 server needs to upload files to S3.

Bad approach

```
Store AWS Access Keys inside code
```

Good approach

```
EC2

↓

IAM Role

↓

Temporary Credentials

↓

Access S3
```

No secrets stored in your application.

______________________________________________________________________

# Common IAM Roles

Examples

- EC2 Role
- ECS Task Role
- Lambda Execution Role
- CloudFormation Role
- Cross-Account Role

You will use these extensively in production.

______________________________________________________________________

# IAM Policy

Policies define permissions.

Policies are JSON documents.

Example

```
Allow

↓

Read S3

↓

Deny Delete Bucket
```

A policy answers:

- Which actions?
- On which resources?
- Under what conditions?

______________________________________________________________________

# Managed Policies

Managed Policies are reusable.

Two types:

### AWS Managed

Created by AWS.

Examples

- AmazonS3ReadOnlyAccess
- AmazonEC2FullAccess
- CloudWatchReadOnlyAccess

Good for learning and quick setups.

______________________________________________________________________

### Customer Managed

Created by your organization.

Example

```
BackendTeamPolicy

↓

Read S3

↓

Write CloudWatch Logs

↓

No Delete Permissions
```

Recommended for production because they match your organization's needs.

______________________________________________________________________

# Inline Policies

Attached directly to one user, group, or role.

```
Alice

↓

Inline Policy
```

Cannot be reused.

Generally avoid them unless a permission is truly unique to one identity.

______________________________________________________________________

# IAM Policy Structure

Example

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-company-bucket"
      ]
    }
  ]
}
```

______________________________________________________________________

# Policy Fields

## Version

Policy language version.

Current standard

```
2012-10-17
```

______________________________________________________________________

## Statement

Contains one or more permission rules.

______________________________________________________________________

## Effect

Two values

```
Allow

Deny
```

Remember:

**An explicit `Deny` always overrides an `Allow`.**

______________________________________________________________________

## Action

Specifies what can be done.

Examples

```
s3:GetObject

ec2:StartInstances

ec2:StopInstances

logs:CreateLogGroup
```

______________________________________________________________________

## Resource

Specifies which resource is affected.

Examples

```
Specific Bucket

Specific EC2

Specific IAM Role
```

Using `"*"` means all applicable resources, which should be avoided unless required.

______________________________________________________________________

## Condition

Optional rules.

Examples

Allow only if:

- Source IP matches
- MFA is enabled
- Request happens during business hours
- Specific AWS Region

Conditions provide fine-grained access control.

______________________________________________________________________

# IAM Credentials

IAM Users can have:

Console Login

```
Username

Password
```

Programmatic Access

```
Access Key

Secret Access Key
```

______________________________________________________________________

# Access Key

Looks like

```
AKIAxxxxxxxxxxxxxxxx
```

Used by

- AWS CLI
- SDK
- Automation

______________________________________________________________________

# Secret Access Key

Generated once.

Example

```
kJHds76asd8JKL...
```

Treat it like a password.

Never commit it to GitHub.

______________________________________________________________________

# Multi-Factor Authentication (MFA)

MFA requires:

Something you know

```
Password
```

AND

Something you have

```
Authenticator App

Hardware Token
```

Even if someone steals your password, they still need the second factor.

______________________________________________________________________

# Principle of Least Privilege

One of the most important AWS security principles.

Give only the permissions required.

Example

Bad

```
AdministratorAccess
```

Good

```
Read S3

Write CloudWatch Logs

Nothing Else
```

______________________________________________________________________

# Root User

The AWS account starts with one Root User.

The Root User has unrestricted access.

Use it only for:

- Initial account setup
- Billing configuration
- Closing the account
- Emergency account recovery

Create IAM Users immediately after creating the account.

______________________________________________________________________

# Using IAM from the AWS Console

Common tasks:

- Create Users
- Create Groups
- Create Roles
- Attach Policies
- Enable MFA
- Rotate Access Keys
- Review permissions

The Console is useful for learning and occasional administrative tasks.

______________________________________________________________________

# AWS CLI

## Verify Installation

```bash
aws --version
```

______________________________________________________________________

## Configure Credentials

```bash
aws configure
```

______________________________________________________________________

## List IAM Users

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

## Create Group

```bash
aws iam create-group \
    --group-name developers
```

______________________________________________________________________

## Add User to Group

```bash
aws iam add-user-to-group \
    --user-name backend-user \
    --group-name developers
```

______________________________________________________________________

## List Groups

```bash
aws iam list-groups
```

______________________________________________________________________

## Attach AWS Managed Policy

```bash
aws iam attach-group-policy \
    --group-name developers \
    --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess
```

______________________________________________________________________

## Delete User

```bash
aws iam delete-user \
    --user-name backend-user
```

______________________________________________________________________

# AWS SDK (Python boto3)

## Installation

```bash
pip install boto3
```

______________________________________________________________________

## Create IAM Client

```python
import boto3

iam = boto3.client("iam")
```

______________________________________________________________________

## List Users

```python
import boto3

iam = boto3.client("iam")

response = iam.list_users()

for user in response["Users"]:
    print(user["UserName"])
```

______________________________________________________________________

## Create User

```python
import boto3

iam = boto3.client("iam")

iam.create_user(
    UserName="backend-user"
)
```

______________________________________________________________________

## Delete User

```python
iam.delete_user(
    UserName="backend-user"
)
```

______________________________________________________________________

# Common IAM Operations

Daily operations include:

- Creating developers
- Removing inactive users
- Rotating Access Keys
- Enabling MFA
- Assigning Groups
- Reviewing Policies
- Auditing Roles
- Creating Service Roles

______________________________________________________________________

# Common Mistakes

❌ Giving everyone AdministratorAccess

❌ Sharing one IAM User among multiple people

❌ Storing Access Keys in source code

❌ Never rotating credentials

❌ Disabling MFA

❌ Using the Root User every day

❌ Using wildcard (`*`) permissions unnecessarily

______________________________________________________________________

# Production Best Practices

- Enable MFA for privileged users.
- Use IAM Roles for AWS services instead of long-lived keys.
- Follow Least Privilege.
- Prefer Groups over individual permissions.
- Create Customer Managed Policies for your organization.
- Rotate Access Keys regularly if they are still in use.
- Audit permissions periodically.
- Avoid sharing accounts.
- Monitor IAM changes using CloudTrail (covered later).
- Remove unused users, roles, and credentials.

______________________________________________________________________

# Summary

In this chapter you learned:

- What IAM is
- Authentication vs Authorization
- Users
- Groups
- Roles
- Policies
- Managed Policies
- Inline Policies
- Policy JSON
- Access Keys
- Secret Keys
- MFA
- Least Privilege
- Root User best practices
- IAM Console
- AWS CLI
- boto3 SDK basics
- Production security practices

IAM is the foundation of AWS security. Almost every AWS service interacts with IAM to determine whether an action is
permitted.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is IAM?
1. Why is IAM required in AWS?
1. Explain Authentication vs Authorization.
1. What are the main IAM components?
1. Why shouldn't everyone have AdministratorAccess?

______________________________________________________________________

## Users, Groups, Roles

6. What is an IAM User?
1. When should you create an IAM User?
1. What is an IAM Group?
1. Why are Groups better than assigning permissions individually?
1. What is an IAM Role?
1. Why are IAM Roles preferred for EC2 instances?
1. Give five examples of AWS services that commonly use IAM Roles.

______________________________________________________________________

## Policies

13. What is an IAM Policy?
01. What is the difference between AWS Managed Policies and Customer Managed Policies?
01. When would you use an Inline Policy?
01. What does the `Effect` field represent?
01. What is the purpose of the `Resource` field?
01. What does an explicit `Deny` do?
01. What is the purpose of the `Condition` field?

______________________________________________________________________

## Credentials

20. What is an Access Key?
01. What is a Secret Access Key?
01. Why should Secret Access Keys never be committed to source control?
01. What is MFA, and why is it important?

______________________________________________________________________

## CLI & SDK

24. How do you list IAM users using the AWS CLI?
01. How do you create an IAM user using boto3?
01. What command configures the AWS CLI?

______________________________________________________________________

## Scenario-Based

27. Your EC2 application needs access to S3. Should you use an IAM User or an IAM Role? Why?
01. A new developer joins your team. How would you grant S3 read access using IAM Groups?
01. A user can log in successfully but cannot delete an EC2 instance. Is this an authentication issue or an authorization issue?
01. You discover an application with AWS Access Keys hardcoded in the source code. What risks does this create, and how would you fix the design?

______________________________________________________________________

## Next

[IAM Advanced](02_iam_advanced.md)

# IAM Advanced

> **Course:** AWS for Backend Engineers
>
> **Module:** 1
>
> **File:** `02_iam_advanced.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- IAM Permission Evaluation
- Policy Evaluation Logic
- Explicit vs Implicit Deny
- Permission Boundaries
- Service Control Policies (SCPs)
- AWS Organizations
- AWS STS
- Temporary Credentials
- Cross-Account Access
- AssumeRole
- IAM Identity Center (AWS SSO)
- Identity Federation
- IAM Access Analyzer
- Credential Rotation
- IAM Policy Simulator
- Security Auditing
- Production IAM Architecture
- Common Security Mistakes
- Best Practices

______________________________________________________________________

# Why Advanced IAM?

Most interview questions don't ask:

> "What is an IAM User?"

Instead they ask:

> "Why is my EC2 instance unable to access S3?"

or

> "How can Account A access resources in Account B?"

or

> "Why does an Administrator still receive AccessDenied?"

These questions require understanding **how IAM evaluates permissions**, not just knowing IAM components.

______________________________________________________________________

# How AWS Evaluates Permissions

Whenever a request reaches AWS

```
Application

↓

AWS API

↓

IAM Engine

↓

Allow?

↓

Execute
```

Every API call goes through IAM.

Example

```
aws s3 ls
```

AWS first checks

- Who made the request?
- Which policy applies?
- Is the action allowed?
- Is there an explicit deny?
- Are organization policies restricting it?

Only then is the request executed.

______________________________________________________________________

# IAM Permission Evaluation Flow

```
Request

↓

Authentication

↓

Policy Evaluation

↓

Allowed?

↓

Execute API
```

The evaluation combines multiple policy types.

______________________________________________________________________

# Policy Evaluation Logic

AWS evaluates permissions in this order:

```
Default

↓

Implicit Deny

↓

Explicit Allow

↓

Explicit Deny Wins
```

This is one of the most important IAM concepts.

______________________________________________________________________

# Implicit Deny

Every action starts as denied.

Example

```
User

↓

No Policies

↓

Everything Denied
```

If no policy grants access, AWS denies the request.

______________________________________________________________________

# Explicit Allow

A policy grants permission.

Example

```
Allow

s3:GetObject
```

Now the user can read objects from the permitted bucket.

______________________________________________________________________

# Explicit Deny

If **any applicable policy** contains:

```json
{
    "Effect": "Deny"
}
```

The action is denied, even if another policy allows it.

Example

```
Policy A

Allow EC2

+

Policy B

Deny EC2

↓

Denied
```

**Explicit Deny always overrides Allow.**

______________________________________________________________________

# IAM Policy Evaluation Example

User Policies

```
Allow

s3:*
```

Group Policy

```
Allow

ec2:DescribeInstances
```

Permission Boundary

```
Only Read Operations
```

Result

```
Read S3

Allowed

Write S3

Denied

Terminate EC2

Denied
```

Every applicable permission layer must allow the action.

______________________________________________________________________

# Permission Boundaries

Permission Boundaries define the **maximum permissions** an IAM User or Role can ever receive.

Think of them as a ceiling.

Example

```
Permission Boundary

↓

Read Only
```

Developer Policy

```
AdministratorAccess
```

Actual Result

```
Read Only
```

Because the boundary limits the maximum privilege.

______________________________________________________________________

# When to Use Permission Boundaries

Useful when developers are allowed to create IAM roles.

Example

Without Boundary

```
Developer

↓

Creates Admin Role

↓

Security Risk
```

With Boundary

```
Developer

↓

Creates Role

↓

Maximum Permission = Read Only
```

Safe.

______________________________________________________________________

# AWS Organizations

Large companies often have many AWS accounts.

Example

```
Company

├── Production
├── Development
├── Testing
├── Security
└── Billing
```

AWS Organizations allows centralized management.

Benefits

- Central billing
- Account hierarchy
- Organization-wide policies
- Security controls

______________________________________________________________________

# Service Control Policies (SCP)

SCPs apply at the **AWS Organization** level.

They do **not** grant permissions.

They only define the maximum permissions available to accounts.

Example

```
Organization

↓

Deny EC2 Termination
```

Even if an account grants:

```
AdministratorAccess
```

Termination is still denied.

______________________________________________________________________

# SCP vs IAM Policy

| Feature | IAM Policy | SCP |
|----------|------------|-----|
| Grants permissions | ✅ | ❌ |
| Restricts permissions | ✅ (with Deny) | ✅ |
| Applies to | Users, Groups, Roles | AWS Accounts |
| Used with AWS Organizations | ❌ | ✅ |

______________________________________________________________________

# AWS Security Token Service (STS)

STS provides **temporary security credentials**.

Instead of permanent Access Keys:

```
Temporary Credentials

↓

Automatically Expire
```

Much safer.

______________________________________________________________________

# Temporary Credentials

A temporary credential contains:

- Access Key
- Secret Access Key
- Session Token

Valid for a limited duration.

After expiration, it cannot be used.

______________________________________________________________________

# Why Temporary Credentials?

Permanent credentials

```
Valid Forever

↓

Risk if Leaked
```

Temporary credentials

```
Expire Automatically
```

Much more secure.

______________________________________________________________________

# AssumeRole

One identity temporarily uses another role.

Example

```
Developer

↓

Assume Role

↓

Production Read Role

↓

Read Logs
```

The developer never owns permanent production credentials.

______________________________________________________________________

# Cross-Account Access

Suppose

```
Account A

↓

Application
```

Needs to access

```
Account B

↓

S3 Bucket
```

Solution

```
Application

↓

AssumeRole

↓

Temporary Credentials

↓

Access Bucket
```

No Access Keys need to be shared.

______________________________________________________________________

# Trust Policy

Roles have a **Trust Policy**.

Permission Policy

```
What the role can do
```

Trust Policy

```
Who can assume the role
```

Both are required.

______________________________________________________________________

# Example Cross-Account Flow

```
Account A

↓

IAM User

↓

Assume Role

↓

STS

↓

Temporary Credentials

↓

Account B

↓

Read S3
```

______________________________________________________________________

# IAM Identity Center (AWS SSO)

Previously known as **AWS Single Sign-On (AWS SSO).**

Allows users to log in once and access:

- AWS Accounts
- Business applications
- Multiple cloud resources

Benefits

- Central identity management
- Better user experience
- Reduced password management
- Integration with corporate identity providers

______________________________________________________________________

# Identity Federation

Instead of creating IAM Users,

AWS can trust another identity provider.

Examples

- Microsoft Entra ID (Azure AD)
- Okta
- Google Workspace
- Active Directory

Flow

```
User

↓

Corporate Login

↓

Identity Provider

↓

AWS

↓

Temporary Credentials
```

Organizations usually prefer federation over thousands of IAM Users.

______________________________________________________________________

# IAM Access Analyzer

Access Analyzer helps identify resources that are accessible outside your account.

Examples

- Public S3 buckets
- Cross-account roles
- Shared KMS keys

Useful for security reviews.

______________________________________________________________________

# IAM Policy Simulator

The Policy Simulator lets you test permissions before deploying them.

Questions it answers:

- Can this user delete an EC2 instance?
- Can this role read this bucket?
- Why is access denied?

This saves debugging time.

______________________________________________________________________

# Credential Rotation

Access Keys should not remain active forever.

Recommended approach

```
Old Key

↓

Create New Key

↓

Update Applications

↓

Delete Old Key
```

Rotate regularly according to your organization's security policy.

______________________________________________________________________

# Auditing IAM

Regularly review:

- Unused Users
- Unused Roles
- Old Access Keys
- Administrator Accounts
- Unused Policies
- Inactive Credentials

Monitoring IAM activity with CloudTrail is also a standard practice.

______________________________________________________________________

# IAM Architecture in Production

Example

```
Developers

↓

IAM Identity Center

↓

Temporary Credentials

↓

AWS Accounts

↓

IAM Roles

↓

Resources
```

Applications

```
ECS

↓

Task Role

↓

S3
```

EC2

```
EC2 Instance

↓

IAM Role

↓

CloudWatch
```

Lambda

```
Lambda Function

↓

Execution Role

↓

DynamoDB
```

Notice that services use **roles**, not stored credentials.

______________________________________________________________________

# Common IAM Security Mistakes

❌ Sharing one IAM User among multiple engineers

❌ Giving `AdministratorAccess` to everyone

❌ Using wildcard (`*`) for all actions and resources

❌ Storing Access Keys in GitHub

❌ Long-lived credentials for applications

❌ No MFA for privileged users

❌ Never rotating Access Keys

❌ Ignoring Access Analyzer findings

❌ Not reviewing permissions over time

______________________________________________________________________

# Production Best Practices

- Use IAM Roles for AWS workloads.
- Prefer temporary credentials.
- Enable MFA for privileged identities.
- Follow Least Privilege.
- Use IAM Identity Center for workforce access.
- Rotate credentials.
- Use Permission Boundaries where developers create IAM resources.
- Use SCPs to enforce organization-wide guardrails.
- Audit permissions regularly.
- Monitor IAM changes with CloudTrail.
- Remove unused identities and policies.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is an EC2 instance receiving `AccessDenied` when trying to read an S3 bucket, even though an IAM policy allows
`s3:GetObject`?**

### Answer

Several permission layers may be involved:

1. Verify the EC2 instance is using the expected IAM Role.
1. Confirm the IAM policy allows `s3:GetObject` on the correct bucket or object ARN.
1. Check for an explicit `Deny` in any attached policy.
1. Verify the bucket policy isn't denying access.
1. Check whether a Permission Boundary limits the role.
1. If using AWS Organizations, ensure an SCP isn't blocking the action.
1. Confirm the object isn't encrypted with a KMS key requiring additional permissions.
1. Review CloudTrail logs and use the IAM Policy Simulator to identify the failing permission check.

______________________________________________________________________

# Summary

In this chapter you learned:

- IAM permission evaluation
- Implicit vs Explicit Deny
- Permission Boundaries
- AWS Organizations
- Service Control Policies
- STS
- Temporary Credentials
- AssumeRole
- Cross-account access
- Trust Policies
- IAM Identity Center
- Identity Federation
- Access Analyzer
- Policy Simulator
- Credential Rotation
- Production IAM architecture
- Security best practices

Understanding these concepts is essential for designing secure AWS environments and troubleshooting real-world
permission issues.

______________________________________________________________________

# Practice Questions

## Permission Evaluation

1. Explain IAM permission evaluation.
1. What is an implicit deny?
1. What is an explicit deny?
1. Which takes precedence: Allow or Deny?
1. Why does every request start as denied?

______________________________________________________________________

## Permission Boundaries

6. What is a Permission Boundary?
1. Does a Permission Boundary grant permissions?
1. When would you use one?
1. How is it different from an IAM Policy?

______________________________________________________________________

## AWS Organizations

10. What is AWS Organizations?
01. What problem does it solve?
01. What is an SCP?
01. Can an SCP grant permissions?
01. How does an SCP interact with IAM policies?

______________________________________________________________________

## STS and Roles

15. What is AWS STS?
01. What are temporary credentials?
01. Why are temporary credentials more secure than permanent Access Keys?
01. What is `AssumeRole`?
01. What is a Trust Policy?
01. Explain cross-account access using AssumeRole.

______________________________________________________________________

## Identity Management

21. What is IAM Identity Center?
01. What is Identity Federation?
01. Why do enterprises often prefer federation over creating IAM Users?

______________________________________________________________________

## Security

24. What does IAM Access Analyzer do?
01. Why should Access Keys be rotated?
01. What is the IAM Policy Simulator used for?
01. List five common IAM security mistakes.
01. Why should applications use IAM Roles instead of Access Keys?

______________________________________________________________________

## Scenario-Based

29. A developer has `AdministratorAccess` but still cannot terminate EC2 instances. What could be causing this?
01. Your company has separate Production and Development AWS accounts. How would you allow a developer from Development to read logs in Production without sharing credentials?
01. An application needs temporary access to another AWS account. Design a secure solution.
01. During a security audit, you discover IAM Users with Access Keys that haven't been rotated in two years. What actions would you take?

______________________________________________________________________

## Next

[EC2 Fundamentals](03_ec2_fundamentals.md)

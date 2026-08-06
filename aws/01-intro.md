# AWS Introduction

> **Course:** AWS for Backend Engineers
>
> **Module:** 0
>
> **File:** 00_aws_introduction.md

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Cloud Computing really is
- Why companies moved away from traditional servers
- Cloud Service Models (IaaS, PaaS, SaaS)
- Types of Cloud
- AWS Global Infrastructure
- AWS Regions
- Availability Zones
- Edge Locations
- AWS Management Console
- AWS CLI
- AWS SDK
- Free Tier
- Billing Basics
- Shared Responsibility Model
- Resource Naming
- Tags
- AWS Best Practices

______________________________________________________________________

# What is Cloud Computing?

Cloud Computing is the delivery of computing resources over the internet instead of owning and maintaining physical
servers.

Instead of buying servers, networking devices, storage devices, and maintaining them yourself, you rent them whenever
you need.

Think of cloud as **renting computing resources on demand**.

Resources include:

- Virtual Machines
- Storage
- Databases
- Networking
- Load Balancers
- AI Services
- Monitoring
- Logging
- Authentication

You only pay for what you use.

______________________________________________________________________

# Traditional Infrastructure

Imagine a startup building an application.

Without cloud:

```
Users
   |
Internet
   |
Router
   |
Firewall
   |
Physical Server
   |
Database Server
```

The company must purchase

- Servers
- Hard disks
- Networking equipment
- UPS
- Power backup
- Cooling systems
- Rack space

Then they need

- System Administrator
- Network Engineer
- Security Engineer

Problems:

- Expensive
- Slow to scale
- Hardware failures
- Maintenance costs
- Power outages
- Capacity planning

______________________________________________________________________

# Cloud Infrastructure

Instead of buying hardware

```
Users
    |
Internet
    |
AWS
    |
EC2
S3
RDS
ECS
Lambda
```

AWS owns the hardware.

You simply use it.

Benefits

- No hardware purchase
- Scale instantly
- Global availability
- Pay only when needed

______________________________________________________________________

# Why Cloud?

Traditional approach

Suppose Black Friday traffic arrives.

Current servers

```
100 Users
```

Suddenly

```
100000 Users
```

Your servers crash.

To avoid crashes you would need to purchase servers beforehand.

Most of the year those servers remain unused.

Huge waste of money.

Cloud solves this.

```
Morning

2 Servers

↓

Evening

50 Servers

↓

Night

2 Servers
```

Automatic scaling.

______________________________________________________________________

# Real World Analogy

Imagine electricity.

Nobody builds their own power plant.

Instead,

You pay the electricity company.

Cloud computing works exactly the same way.

Instead of buying computers

You consume computing power.

______________________________________________________________________

# Advantages of Cloud

## Cost Savings

No upfront investment.

Pay as you go.

______________________________________________________________________

## Elasticity

Increase resources instantly.

Decrease resources instantly.

______________________________________________________________________

## Global Reach

Deploy applications close to users.

______________________________________________________________________

## High Availability

Applications continue working even if one data center fails.

______________________________________________________________________

## Security

Cloud providers invest billions into security.

______________________________________________________________________

## Automation

Everything can be automated.

Servers

Networks

Users

Databases

Monitoring

Deployments

______________________________________________________________________

# Cloud Service Models

Cloud has three major models.

```
+--------------------+
| SaaS               |
+--------------------+
| PaaS               |
+--------------------+
| IaaS               |
+--------------------+
```

______________________________________________________________________

# Infrastructure as a Service (IaaS)

Provider gives

- Virtual Machines
- Storage
- Network

You manage

- OS
- Software
- Security patches
- Application

Examples

- AWS EC2
- Azure VM
- Google Compute Engine

Example

Renting an empty apartment.

You bring

Furniture

TV

Kitchen

Everything.

______________________________________________________________________

# Platform as a Service (PaaS)

Provider manages

- Hardware
- Operating System
- Runtime

You only deploy code.

Examples

- AWS Elastic Beanstalk
- Google App Engine
- Heroku

Analogy

Fully furnished apartment.

You only move in.

______________________________________________________________________

# Software as a Service (SaaS)

Provider manages everything.

You simply use the software.

Examples

- Gmail
- Slack
- Notion
- Salesforce

Analogy

Hotel room.

Everything is already available.

______________________________________________________________________

# Public Cloud

Infrastructure shared among customers.

Examples

AWS

Azure

Google Cloud

Most companies use this.

______________________________________________________________________

# Private Cloud

Infrastructure belongs to one organization.

Used by

Banks

Government

Military

______________________________________________________________________

# Hybrid Cloud

Combination of

Private Cloud

-

Public Cloud

Example

Sensitive banking data

↓

Private Cloud

Website

↓

AWS

______________________________________________________________________

# AWS Overview

AWS stands for

**Amazon Web Services**

Started in

**2006**

Today it offers **200+ cloud services.**

Common services

- EC2
- S3
- Lambda
- IAM
- RDS
- DynamoDB
- ECS
- EKS
- CloudWatch
- VPC
- SNS
- SQS

______________________________________________________________________

# AWS Global Infrastructure

AWS consists of

```
Regions
    |
Availability Zones
    |
Data Centers
```

______________________________________________________________________

# Region

A Region is a geographical area.

Examples

```
Mumbai

Singapore

Tokyo

Frankfurt

London

Ohio

N. Virginia
```

Every Region contains multiple Availability Zones.

______________________________________________________________________

# Why Multiple Regions?

Reasons

- Lower latency
- Disaster recovery
- Legal compliance
- Better availability

Example

Indian users

↓

Mumbai Region

European users

↓

Frankfurt Region

______________________________________________________________________

# Availability Zone (AZ)

Each Region contains multiple isolated data centers.

Example

Mumbai

```
ap-south-1a

ap-south-1b

ap-south-1c
```

Each AZ has

- Independent power
- Independent cooling
- Independent networking

______________________________________________________________________

# Why AZ?

Suppose one data center catches fire.

Applications continue running in another AZ.

______________________________________________________________________

# Edge Locations

Used for

- CloudFront
- DNS
- Content Caching

Purpose

Serve users from locations closer to them.

______________________________________________________________________

# AWS Management Console

AWS Console is the web interface.

Features

- Create servers
- Upload files
- Configure networking
- View billing
- Manage users
- Monitor services

Best for

- Beginners
- Manual operations
- Learning

______________________________________________________________________

# AWS CLI

AWS CLI (Command Line Interface) allows managing AWS resources from the terminal.

Example

```bash
aws s3 ls
```

List EC2

```bash
aws ec2 describe-instances
```

Advantages

- Automation
- Scripting
- CI/CD
- Faster than Console
- Repeatable

______________________________________________________________________

# AWS SDK

Applications communicate with AWS using SDKs.

Supported languages

- Python (boto3)
- Java
- Go
- Node.js
- C#
- PHP
- Ruby

Example

Python

```python
import boto3

s3 = boto3.client("s3")

response = s3.list_buckets()

print(response)
```

Advantages

- Programmatic access
- Automation
- Integrates into applications
- Used by backend services

______________________________________________________________________

# Console vs CLI vs SDK

| Feature | Console | CLI | SDK |
|----------|----------|-----|-----|
| Beginner Friendly | ✅ | ❌ | ❌ |
| Automation | ❌ | ✅ | ✅ |
| CI/CD | ❌ | ✅ | ✅ |
| Application Integration | ❌ | ❌ | ✅ |
| Bulk Operations | ❌ | ✅ | ✅ |

______________________________________________________________________

# Installing AWS CLI

Windows

Download installer from AWS.

macOS

```bash
brew install awscli
```

Linux

```bash
sudo apt install awscli
```

Verify installation

```bash
aws --version
```

Example output

```
aws-cli/2.x.x
```

______________________________________________________________________

# Configuring AWS CLI

Run

```bash
aws configure
```

It asks

```
AWS Access Key ID

AWS Secret Access Key

Default Region

Output Format
```

Example

```
AWS Access Key ID: AKIA************

AWS Secret: ****************

Region: ap-south-1

Output: json
```

Configuration is stored locally.

______________________________________________________________________

# Installing AWS SDK (Python)

Install boto3

```bash
pip install boto3
```

Verify

```python
import boto3

print(boto3.__version__)
```

______________________________________________________________________

# Billing Basics

AWS follows

**Pay As You Go**

You pay only for consumed resources.

Examples

- Running EC2 instances
- S3 Storage
- Network Transfer
- Database Usage

Some services charge

Per request

Others

Per hour

Some

Per GB

______________________________________________________________________

# AWS Free Tier

Useful for learning.

Includes limited usage for

- EC2
- S3
- Lambda
- DynamoDB

Always verify current limits before using resources extensively, as free-tier offerings can change over time.

______________________________________________________________________

# Shared Responsibility Model

AWS secures

- Buildings
- Hardware
- Networking
- Physical Security
- Hypervisors

You secure

- IAM Users
- Passwords
- Security Groups
- Application Code
- Data
- Encryption
- Operating System (for EC2)

Think of it as

```
AWS

↓

Infrastructure Security

---------------------

You

↓

Everything you deploy
```

______________________________________________________________________

# AWS Resource Naming

Examples

```
Production-API

Development-API

UserBucket

InvoiceBucket

Backend-VPC
```

Good names should indicate

- Environment
- Purpose
- Team
- Application

______________________________________________________________________

# Tags

Tags help organize resources.

Example

```
Environment = Production

Owner = Backend Team

Project = Payment Service

Department = Engineering
```

Benefits

- Cost tracking
- Resource filtering
- Automation
- Governance

______________________________________________________________________

# AWS Best Practices

- Never use the Root Account for daily work.
- Enable MFA on the Root Account.
- Follow the Principle of Least Privilege.
- Use IAM Roles instead of long-lived access keys whenever possible.
- Tag every resource consistently.
- Monitor costs regularly.
- Use multiple Availability Zones for production workloads.
- Automate infrastructure whenever possible.
- Delete unused resources.
- Enable logging and monitoring.

______________________________________________________________________

# Summary

In this chapter you learned

- Cloud Computing fundamentals
- Traditional vs Cloud Infrastructure
- IaaS, PaaS, SaaS
- Public, Private and Hybrid Cloud
- AWS Global Infrastructure
- Regions
- Availability Zones
- Edge Locations
- AWS Console
- AWS CLI
- AWS SDK
- Billing
- Free Tier
- Shared Responsibility Model
- Tags
- Best Practices

This knowledge forms the foundation for understanding every AWS service covered in the rest of the course.

______________________________________________________________________

# Practice Questions

## Basics

1. What is Cloud Computing?
1. Why is Cloud Computing preferred over traditional infrastructure?
1. What are the advantages of cloud computing?
1. Explain elasticity with an example.
1. What is pay-as-you-go pricing?

______________________________________________________________________

## Service Models

6. What is IaaS?
1. What is PaaS?
1. What is SaaS?
1. Give examples of each service model.
1. Which AWS services fall under IaaS?

______________________________________________________________________

## AWS Infrastructure

11. What is an AWS Region?
01. What is an Availability Zone?
01. Why should production workloads use multiple AZs?
01. What are Edge Locations used for?
01. How does deploying closer to users reduce latency?

______________________________________________________________________

## Tools

16. What is the AWS Management Console?
01. When would you choose the AWS CLI over the Console?
01. What is an AWS SDK?
01. Why is boto3 commonly used by Python developers?
01. How do you configure the AWS CLI?

______________________________________________________________________

## Security & Billing

21. Explain the Shared Responsibility Model.
01. Why should the Root Account not be used for daily work?
01. What are IAM credentials used for?
01. Why are tags important?
01. How does AWS billing work?

______________________________________________________________________

## Scenario-Based

26. Your application receives 100× more traffic during a sale. How does cloud computing help?
01. A data center becomes unavailable. How can AWS keep your application running?
01. You need to automate infrastructure creation. Which interface (Console, CLI, or SDK) would you choose, and why?
01. Your company operates in Europe and India. How would you select AWS Regions?
01. What AWS best practices would you follow before deploying your first production application?

______________________________________________________________________

## Next

[IAM Fundamentals](01_iam_fundamentals.md)

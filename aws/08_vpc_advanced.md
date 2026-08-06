# VPC Advanced

> **Course:** AWS for Backend Engineers
>
> **Module:** 4
>
> **File:** `08_vpc_advanced.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- VPC Peering
- AWS Transit Gateway
- Site-to-Site VPN
- AWS Direct Connect
- VPC Endpoints
- Gateway Endpoints
- Interface Endpoints (AWS PrivateLink)
- Private DNS
- Route Propagation
- VPC Flow Logs
- Network Troubleshooting
- Multi-VPC Architecture
- Multi-Region Networking
- Hub-and-Spoke Design
- Production Best Practices

______________________________________________________________________

# Why Advanced Networking?

A small startup might have:

```
One VPC

↓

One Application
```

A large company may have:

```
100+

AWS Accounts

↓

300+

VPCs

↓

Thousands

of Servers
```

Questions arise:

- How do VPCs communicate?
- How do on-premises data centers connect to AWS?
- How do private resources access S3 without the public internet?
- How can networking remain secure and scalable?

This chapter answers those questions.

______________________________________________________________________

# Multi-VPC Architecture

As organizations grow, they separate environments.

Example

```
Production VPC

↓

Development VPC

↓

Testing VPC

↓

Shared Services VPC
```

Reasons

- Isolation
- Security
- Compliance
- Independent deployments

______________________________________________________________________

# VPC Peering

VPC Peering creates a **private connection** between two VPCs.

```
VPC A

⇄

VPC B
```

Traffic stays on the AWS network.

No public internet is used.

______________________________________________________________________

# Why Use VPC Peering?

Example

```
Application

↓

VPC A
```

Needs database in

```
VPC B
```

Instead of exposing the database publicly,

create a VPC Peering connection.

______________________________________________________________________

# VPC Peering Architecture

```
Application

↓

VPC A

⇄ Peering ⇄

VPC B

↓

Database
```

______________________________________________________________________

# VPC Peering Characteristics

- Private communication
- Low latency
- No Internet Gateway required
- No NAT Gateway required
- CIDR ranges must **not overlap**

______________________________________________________________________

# Limitation of VPC Peering

Peering is **not transitive**.

Example

```
VPC A

⇄

VPC B

⇄

VPC C
```

A **cannot** automatically communicate with C.

Each connection must be created explicitly.

______________________________________________________________________

# AWS Transit Gateway

Managing dozens of VPC peerings becomes difficult.

Example

```
20 VPCs

↓

190+

Peering Connections
```

Instead,

use Transit Gateway.

______________________________________________________________________

# Transit Gateway Architecture

```
          Transit Gateway

      /        |        \

   VPC A    VPC B    VPC C

      \        |        /

       Shared Connectivity
```

Transit Gateway acts as a central network hub.

______________________________________________________________________

# Benefits of Transit Gateway

- Simplified networking
- Centralized routing
- Easier management
- Scales to many VPCs
- Supports VPN and Direct Connect attachments

______________________________________________________________________

# VPC Peering vs Transit Gateway

| Feature | VPC Peering | Transit Gateway |
|----------|-------------|-----------------|
| Small deployments | ✅ | ❌ |
| Large enterprises | ❌ | ✅ |
| Centralized routing | ❌ | ✅ |
| Supports transitive routing | ❌ | ✅ |
| Easier to manage at scale | ❌ | ✅ |

______________________________________________________________________

# Site-to-Site VPN

Many companies still operate their own data centers.

Need

```
Office

↓

AWS
```

Secure connection.

Solution

```
VPN Tunnel
```

______________________________________________________________________

# Site-to-Site VPN Architecture

```
Office

↓

VPN Device

⇄ Encrypted Tunnel ⇄

Virtual Private Gateway

↓

AWS VPC
```

Traffic travels over the public internet but is encrypted.

______________________________________________________________________

# Common Site-to-Site VPN Use Cases

- Hybrid Cloud
- Gradual cloud migration
- Disaster Recovery
- Secure office connectivity

______________________________________________________________________

# AWS Direct Connect

VPN uses the internet.

Some companies require:

- Lower latency
- More consistent performance
- Dedicated bandwidth

Solution

```
AWS Direct Connect
```

______________________________________________________________________

# Direct Connect Architecture

```
Data Center

↓

Dedicated Fiber Connection

↓

AWS Direct Connect

↓

AWS VPC
```

Traffic bypasses the public internet.

______________________________________________________________________

# VPN vs Direct Connect

| Feature | VPN | Direct Connect |
|----------|-----|----------------|
| Uses Internet | ✅ | ❌ |
| Encryption | ✅ | Optional (often combined with VPN if encryption is required) |
| Low Latency | Good | Better and more consistent |
| Cost | Lower | Higher |
| Typical Setup Time | Faster | Longer |

______________________________________________________________________

# Virtual Private Gateway (VGW)

A Virtual Private Gateway terminates VPN connections on the AWS side.

```
Office

↓

VPN

↓

Virtual Private Gateway

↓

VPC
```

______________________________________________________________________

# Customer Gateway (CGW)

Represents your on-premises VPN device.

```
Firewall

↓

Customer Gateway
```

AWS connects:

```
Customer Gateway

⇄

Virtual Private Gateway
```

______________________________________________________________________

# VPC Endpoints

Sometimes a private EC2 instance needs access to S3.

Without a VPC Endpoint:

```
Private EC2

↓

NAT Gateway

↓

Internet

↓

S3
```

Traffic leaves the private network path.

______________________________________________________________________

# VPC Endpoint Solution

```
Private EC2

↓

VPC Endpoint

↓

S3
```

Traffic remains within the AWS network.

______________________________________________________________________

# Types of VPC Endpoints

Two main types:

- Gateway Endpoint
- Interface Endpoint

______________________________________________________________________

# Gateway Endpoint

Supported for services such as:

- Amazon S3
- Amazon DynamoDB

Advantages

- No NAT Gateway required
- Private connectivity
- Cost-effective

______________________________________________________________________

# Interface Endpoint (AWS PrivateLink)

Creates an Elastic Network Interface (ENI) inside your subnet.

Supports many AWS services and certain partner services.

Examples

- CloudWatch
- Secrets Manager
- ECR
- Systems Manager (SSM)

______________________________________________________________________

# AWS PrivateLink

PrivateLink enables private access to supported services without exposing traffic to the internet.

Example

```
EC2

↓

PrivateLink

↓

Secrets Manager
```

No Internet Gateway or NAT Gateway is required for supported services.

______________________________________________________________________

# Private DNS

Private DNS allows applications to use standard AWS service hostnames while resolving to private endpoint IP addresses.

Example

Application

```
s3.amazonaws.com
```

Internally

↓

Private Endpoint

No code changes are required.

______________________________________________________________________

# Route Propagation

When using Transit Gateway or VPN,

routes can be propagated automatically into route tables depending on configuration.

This reduces manual routing management.

______________________________________________________________________

# VPC Flow Logs

Flow Logs record network traffic metadata.

Example

```
Source IP

↓

Destination IP

↓

Port

↓

Protocol

↓

Accept

↓

Reject
```

Useful for:

- Troubleshooting
- Security
- Auditing
- Incident investigation

______________________________________________________________________

# What Flow Logs Do NOT Capture

Flow Logs do **not** capture packet payloads.

They record metadata only.

Example

Captured

- Source IP
- Destination IP
- Port

Not captured

- HTTP request body
- SQL queries
- File contents

______________________________________________________________________

# Network Troubleshooting

Common questions

```
Cannot SSH

↓

Security Group?

↓

Route Table?

↓

NACL?

↓

Internet Gateway?

↓

Public IP?
```

Systematic troubleshooting is essential.

______________________________________________________________________

# Multi-Region Networking

Example

```
India

↓

Mumbai VPC
```

```
Europe

↓

Frankfurt VPC
```

These environments can communicate using appropriate AWS networking solutions depending on architecture.

Benefits

- Disaster Recovery
- Lower latency
- Global applications

______________________________________________________________________

# Hub-and-Spoke Architecture

A common enterprise design.

```
            Transit Gateway

        /        |        \

     Dev      Prod      Shared

                    |

              Security Tools
```

Advantages

- Centralized networking
- Easier governance
- Simplified connectivity

______________________________________________________________________

# Production Architecture

```
Corporate Office

↓

Site-to-Site VPN

↓

Transit Gateway

↓

Production VPC

↓

Private EC2

↓

Gateway Endpoint

↓

S3

↓

CloudWatch (Interface Endpoint)
```

No unnecessary internet exposure.

______________________________________________________________________

# Monitoring

Use:

- VPC Flow Logs
- CloudWatch
- CloudTrail
- Reachability Analyzer (where applicable)

to monitor and troubleshoot networking.

______________________________________________________________________

# Common Mistakes

❌ Overlapping CIDR ranges

❌ Using VPC Peering for very large environments

❌ Sending private traffic through the public internet unnecessarily

❌ Ignoring Flow Logs

❌ Placing databases in public subnets

❌ Creating overly permissive Security Groups

❌ Forgetting route table updates after creating new connections

______________________________________________________________________

# Production Best Practices

- Design CIDR ranges before creating VPCs.
- Use Transit Gateway for large environments.
- Use VPC Endpoints for AWS service access from private workloads.
- Keep databases private.
- Enable VPC Flow Logs.
- Use Site-to-Site VPN or Direct Connect for hybrid connectivity.
- Review route tables regularly.
- Use Security Groups with least privilege.
- Avoid overlapping CIDR blocks.

______________________________________________________________________

# Interview Deep Dive

### Question

**Your EC2 instances in a private subnet need to access S3 securely without traversing the public internet. How would
you design the solution?**

### Answer

A secure design would be:

1. Keep the EC2 instances in private subnets.
1. Create a **Gateway VPC Endpoint** for Amazon S3.
1. Update the route tables associated with the private subnets to use the endpoint.
1. Restrict bucket access using IAM policies and, if appropriate, bucket policies.
1. Remove any dependency on a NAT Gateway for S3 traffic.

This keeps traffic within the AWS network, improves security, and can reduce networking costs.

______________________________________________________________________

# Summary

In this chapter you learned:

- VPC Peering
- Transit Gateway
- Site-to-Site VPN
- Direct Connect
- Gateway Endpoints
- Interface Endpoints
- AWS PrivateLink
- Private DNS
- Route Propagation
- VPC Flow Logs
- Multi-VPC networking
- Multi-Region architecture
- Hub-and-Spoke design
- Production networking best practices

These services allow AWS networking to scale from a single VPC to enterprise environments spanning many accounts,
Regions, and on-premises data centers.

______________________________________________________________________

# Practice Questions

## VPC Connectivity

1. What is VPC Peering?
1. What are the limitations of VPC Peering?
1. Why can't VPC Peering provide transitive routing?
1. What is AWS Transit Gateway?
1. When would you choose Transit Gateway instead of VPC Peering?

______________________________________________________________________

## Hybrid Networking

6. What is Site-to-Site VPN?
1. What is AWS Direct Connect?
1. Compare VPN and Direct Connect.
1. What is a Virtual Private Gateway?
1. What is a Customer Gateway?

______________________________________________________________________

## VPC Endpoints

11. What is a VPC Endpoint?
01. What is the difference between a Gateway Endpoint and an Interface Endpoint?
01. Which AWS services commonly use Gateway Endpoints?
01. What is AWS PrivateLink?
01. Why are VPC Endpoints preferred over NAT Gateways for accessing supported AWS services?

______________________________________________________________________

## Monitoring

16. What information does VPC Flow Logs capture?
01. What information does VPC Flow Logs not capture?
01. Why are Flow Logs useful during incident investigations?

______________________________________________________________________

## Architecture

19. Explain a Hub-and-Spoke network architecture.
01. Why is CIDR planning important?
01. Why should private workloads use VPC Endpoints when possible?

______________________________________________________________________

## Scenario-Based

22. Your company has 60 AWS accounts and over 100 VPCs. Would you choose VPC Peering or Transit Gateway? Why?
01. Your on-premises data center needs secure access to AWS for disaster recovery. Which AWS networking solution would you recommend?
01. Your finance application in a private subnet needs to access Secrets Manager without internet connectivity. Which AWS feature would you use?
01. During a security audit, you discover overlapping CIDR blocks across multiple VPCs. What operational problems could this create?
01. An application in a private subnet cannot reach S3 even though internet access works through a NAT Gateway. How could a Gateway Endpoint improve the architecture?
01. Your network team reports dropped traffic between two subnets. Which AWS networking tools and configurations would you investigate first?

______________________________________________________________________

## Next

[CloudWatch Fundamentals](09_cloudwatch_fundamentals.md)

# VPC Fundamentals

> **Course:** AWS for Backend Engineers
>
> **Module:** 4
>
> **File:** `07_vpc_fundamentals.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Amazon VPC is
- Why VPC exists
- Private Networking
- CIDR Blocks
- IP Addressing
- Public & Private IP Addresses
- Subnets
- Public vs Private Subnets
- Route Tables
- Internet Gateway (IGW)
- NAT Gateway
- Security Groups
- Network ACLs (NACL)
- Default VPC
- Custom VPC
- AWS Console
- AWS CLI
- AWS SDK (Python boto3)
- Production VPC Design

______________________________________________________________________

# What is Amazon VPC?

**Amazon VPC (Virtual Private Cloud)** is your own **private virtual network** inside AWS.

Think of it as your company's private data center inside AWS.

Every EC2 instance, database, ECS task, and many other AWS resources are launched inside a VPC.

______________________________________________________________________

# Why Was VPC Created?

Imagine AWS without networking isolation.

```
Customer A

↓

Server

↓

Customer B

↓

Server
```

There would be no isolation.

Instead,

AWS creates an isolated network for every customer.

```
AWS

↓

Customer A VPC

↓

Customer B VPC

↓

Customer C VPC
```

Resources cannot communicate unless explicitly configured.

______________________________________________________________________

# Real World Analogy

Imagine an apartment complex.

```
Building

↓

Apartment

↓

Rooms
```

AWS

```
Cloud

↓

VPC

↓

Subnets

↓

Servers
```

Each apartment is isolated from others.

______________________________________________________________________

# VPC Architecture

```
Internet

↓

Internet Gateway

↓

Public Subnet

↓

Private Subnet

↓

Database
```

This is the most common production architecture.

______________________________________________________________________

# Default VPC

When an AWS account is created,

AWS creates a **Default VPC** in most Regions.

Characteristics

- Ready to use
- Public subnets
- Internet Gateway attached
- Easy for beginners

Useful for learning.

______________________________________________________________________

# Custom VPC

Production environments usually use custom VPCs.

Benefits

- Better security
- Better control
- Custom IP ranges
- Custom routing
- Better architecture

______________________________________________________________________

# CIDR Block

CIDR (Classless Inter-Domain Routing) defines the IP address range for a VPC.

Example

```
10.0.0.0/16
```

Meaning

```
10.0.0.0

↓

Starting Address

/16

↓

Network Size
```

This VPC contains many private IP addresses.

______________________________________________________________________

# Common Private CIDR Ranges

RFC 1918 defines private address ranges.

Examples

```
10.0.0.0/8

172.16.0.0/12

192.168.0.0/16
```

These addresses are not routable on the public internet.

______________________________________________________________________

# CIDR Examples

Example

```
10.0.0.0/16
```

Can be divided into

```
10.0.1.0/24

10.0.2.0/24

10.0.3.0/24
```

Each becomes a subnet.

______________________________________________________________________

# Public IP vs Private IP

Private IP

```
10.x.x.x

172.16.x.x

192.168.x.x
```

Accessible only inside the network.

Public IP

```
54.x.x.x

3.x.x.x
```

Reachable from the internet.

______________________________________________________________________

# Subnet

A Subnet is a smaller network inside a VPC.

Example

```
VPC

10.0.0.0/16

↓

Subnet A

10.0.1.0/24

↓

Subnet B

10.0.2.0/24
```

Each subnet resides in exactly one Availability Zone.

______________________________________________________________________

# Why Multiple Subnets?

Reasons

- Security
- High Availability
- Isolation
- Better organization

______________________________________________________________________

# Public Subnet

A Public Subnet has a route to an Internet Gateway.

Resources can receive internet traffic if they also have appropriate public IP addressing and security rules.

Example

```
Internet

↓

Internet Gateway

↓

Public Subnet

↓

EC2
```

Common resources

- Web Servers
- Bastion Hosts
- Public Load Balancers

______________________________________________________________________

# Private Subnet

Private Subnets have **no direct route** to the Internet Gateway.

Example

```
Internet

❌

↓

Private Subnet

↓

Database
```

Common resources

- Databases
- Internal APIs
- Backend Services
- ECS Tasks
- Redis
- Kafka

______________________________________________________________________

# Why Keep Databases Private?

Suppose

```
Database

↓

Public Internet
```

Anyone could attempt to reach it.

Instead

```
Database

↓

Private Subnet
```

Only internal applications can connect.

______________________________________________________________________

# Route Table

A Route Table determines where network traffic goes.

Example

```
Destination

↓

Target
```

Every subnet is associated with a route table.

______________________________________________________________________

# Example Route Table

| Destination | Target |
|------------|---------|
| 10.0.0.0/16 | Local |
| 0.0.0.0/0 | Internet Gateway |

Explanation

```
Internal Traffic

↓

Local
```

```
Internet Traffic

↓

Internet Gateway
```

______________________________________________________________________

# Internet Gateway (IGW)

An Internet Gateway connects a VPC to the public internet.

```
Internet

↓

Internet Gateway

↓

VPC
```

Without an IGW,

resources cannot communicate directly with the internet.

______________________________________________________________________

# NAT Gateway

Private resources sometimes need outbound internet access.

Example

```
Private EC2

↓

Download Updates

↓

Internet
```

They should not become publicly accessible.

Solution

```
Private EC2

↓

NAT Gateway

↓

Internet
```

The NAT Gateway allows **outbound** internet access while preventing unsolicited inbound connections.

______________________________________________________________________

# Public Subnet with NAT Gateway

```
Internet

↓

Internet Gateway

↓

Public Subnet

↓

NAT Gateway

↓

Private Subnet

↓

EC2
```

The NAT Gateway itself is placed in a public subnet.

______________________________________________________________________

# Security Groups

Security Groups act as **instance-level firewalls**.

Example

Allow

```
HTTP

80
```

Allow

```
HTTPS

443
```

Allow

```
SSH

22
```

Everything else remains denied unless explicitly allowed.

Security Groups are **stateful**.

______________________________________________________________________

# Network ACL (NACL)

A Network ACL is a **subnet-level firewall**.

Unlike Security Groups,

NACLs support both:

- Allow Rules
- Deny Rules

They are **stateless**, meaning return traffic must also be explicitly allowed.

______________________________________________________________________

# Security Group vs NACL

| Feature | Security Group | NACL |
|----------|---------------|------|
| Level | Instance/ENI | Subnet |
| Stateful | ✅ | ❌ |
| Allow Rules | ✅ | ✅ |
| Deny Rules | ❌ | ✅ |
| Default Behavior | Deny Inbound, Allow Outbound (modifiable) | Default NACL allows all traffic; custom NACLs depend on configured rules |

______________________________________________________________________

# Example Production Architecture

```
Internet

↓

Application Load Balancer

↓

Public Subnet

↓

EC2

↓

Private Subnet

↓

RDS

↓

Private Subnet
```

Only the Load Balancer is publicly reachable.

______________________________________________________________________

# AWS Console

Using the Console you can:

- Create VPC
- Create Subnets
- Attach Internet Gateway
- Create NAT Gateway
- Modify Route Tables
- Configure Security Groups
- Configure NACLs
- View Network Topology

______________________________________________________________________

# AWS CLI

## Create VPC

```bash
aws ec2 create-vpc \
    --cidr-block 10.0.0.0/16
```

______________________________________________________________________

## List VPCs

```bash
aws ec2 describe-vpcs
```

______________________________________________________________________

## Create Subnet

```bash
aws ec2 create-subnet \
    --vpc-id vpc-xxxxxxxx \
    --cidr-block 10.0.1.0/24
```

______________________________________________________________________

## Create Internet Gateway

```bash
aws ec2 create-internet-gateway
```

______________________________________________________________________

## Attach Internet Gateway

```bash
aws ec2 attach-internet-gateway \
    --internet-gateway-id igw-xxxxxxxx \
    --vpc-id vpc-xxxxxxxx
```

______________________________________________________________________

## Create Route Table

```bash
aws ec2 create-route-table \
    --vpc-id vpc-xxxxxxxx
```

______________________________________________________________________

# AWS SDK (Python boto3)

## Installation

```bash
pip install boto3
```

______________________________________________________________________

## Create EC2 Client

```python
import boto3

ec2 = boto3.client("ec2")
```

______________________________________________________________________

## List VPCs

```python
response = ec2.describe_vpcs()

for vpc in response["Vpcs"]:
    print(vpc["VpcId"])
```

______________________________________________________________________

## Create VPC

```python
ec2.create_vpc(
    CidrBlock="10.0.0.0/16"
)
```

______________________________________________________________________

## Create Subnet

```python
ec2.create_subnet(
    VpcId="vpc-xxxxxxxx",
    CidrBlock="10.0.1.0/24"
)
```

______________________________________________________________________

# Common VPC Operations

Daily operations include:

- Create VPCs
- Create Subnets
- Modify Route Tables
- Configure Security Groups
- Configure NACLs
- Attach Internet Gateways
- Deploy NAT Gateways
- Expand network architecture

______________________________________________________________________

# Common Mistakes

❌ Putting databases in public subnets

❌ Opening SSH to the entire internet

❌ Using only one Availability Zone

❌ Incorrect route table associations

❌ Forgetting to attach an Internet Gateway

❌ Placing a NAT Gateway in a private subnet

❌ Overlapping CIDR blocks across VPCs

______________________________________________________________________

# Production Best Practices

- Create custom VPCs for production.
- Separate public and private workloads.
- Deploy resources across multiple Availability Zones.
- Keep databases in private subnets.
- Use Security Groups with least-privilege rules.
- Use NAT Gateways for outbound internet access from private subnets.
- Design CIDR ranges carefully to avoid overlap.
- Use descriptive tags for networking resources.
- Monitor network traffic using VPC Flow Logs (covered later).

______________________________________________________________________

# Interview Deep Dive

### Question

**How would you design a secure VPC architecture for a production web application?**

### Answer

A secure architecture would include:

1. Create a custom VPC with an appropriate CIDR block.
1. Create public and private subnets across at least two Availability Zones.
1. Place an Application Load Balancer in the public subnets.
1. Place EC2 instances or ECS tasks in private subnets.
1. Place databases such as RDS in private subnets.
1. Attach an Internet Gateway to the VPC.
1. Deploy a NAT Gateway in a public subnet for outbound internet access from private resources.
1. Restrict Security Groups to only the required ports.
1. Use IAM Roles for compute resources.
1. Enable VPC Flow Logs for monitoring and troubleshooting.

______________________________________________________________________

# Summary

In this chapter you learned:

- What Amazon VPC is
- CIDR Blocks
- Private IP Addressing
- Public & Private IPs
- Subnets
- Public vs Private Subnets
- Route Tables
- Internet Gateway
- NAT Gateway
- Security Groups
- Network ACLs
- AWS Console
- AWS CLI
- boto3 SDK
- Production networking practices

A well-designed VPC provides the secure networking foundation for almost every production AWS deployment.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is Amazon VPC?
1. Why was VPC created?
1. What is a CIDR block?
1. What are the common private IP ranges?
1. Why do AWS resources need a VPC?

______________________________________________________________________

## Subnets

6. What is a subnet?
1. Why create multiple subnets?
1. What is the difference between a public subnet and a private subnet?
1. Why should databases usually be deployed in private subnets?

______________________________________________________________________

## Routing

10. What is a Route Table?
01. What is an Internet Gateway?
01. What is a NAT Gateway?
01. Why must a NAT Gateway be placed in a public subnet?
01. How does a private EC2 instance access the internet?

______________________________________________________________________

## Security

15. What is a Security Group?
01. What is a Network ACL?
01. Compare Security Groups and NACLs.
01. Why are Security Groups considered stateful?
01. Why are NACLs considered stateless?

______________________________________________________________________

## CLI & SDK

20. Which CLI command creates a VPC?
01. Which CLI command creates a subnet?
01. Which boto3 method creates a VPC?

______________________________________________________________________

## Scenario-Based

23. Your database is directly accessible from the internet. What architectural changes would you recommend?
01. Your private EC2 instances cannot download operating system updates. Which networking components would you investigate?
01. A team accidentally creates overlapping CIDR blocks for two VPCs. Why is this a problem?
01. Your application must remain available if one Availability Zone fails. How would you design the VPC?
01. Why should an Application Load Balancer typically be placed in public subnets while backend services remain in private subnets?
01. During troubleshooting, you discover a subnet has no route to an Internet Gateway. What symptoms would you expect?

______________________________________________________________________

## Next

[VPC Advanced](08_vpc_advanced.md)

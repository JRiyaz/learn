# EC2 Fundamentals

> **Course:** AWS for Backend Engineers
>
> **Module:** 2
>
> **File:** `03_ec2_fundamentals.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What EC2 is
- Why EC2 exists
- Virtual Machines
- Hypervisors
- Amazon Machine Images (AMI)
- EC2 Instance Lifecycle
- Instance Types
- CPU, Memory and Networking
- EBS Storage
- Instance Store
- Security Groups
- Key Pairs
- User Data
- Elastic IP
- AWS Console
- AWS CLI
- AWS SDK (Python boto3)
- Connecting to EC2
- Common EC2 Operations
- Production Best Practices

______________________________________________________________________

# What is EC2?

**EC2 (Elastic Compute Cloud)** is AWS's virtual machine service.

Instead of buying a physical server, you rent a virtual server from AWS.

You choose:

- CPU
- Memory
- Storage
- Operating System
- Networking

AWS creates the virtual machine in minutes.

______________________________________________________________________

# Why Was EC2 Created?

Before cloud computing, companies had to buy servers.

Example:

```
Need 10 Servers

↓

Purchase Hardware

↓

Wait 2-6 Weeks

↓

Install

↓

Configure

↓

Deploy
```

If traffic increased unexpectedly:

```
Buy More Servers

↓

More Waiting
```

This was slow and expensive.

With EC2:

```
Need Server

↓

Launch Instance

↓

Ready in 2 Minutes
```

______________________________________________________________________

# Real World Analogy

Imagine opening a restaurant.

Instead of buying a building,

you rent one.

If business grows,

rent a larger building.

If business slows,

move to a smaller one.

EC2 works the same way.

______________________________________________________________________

# What is a Virtual Machine?

A Virtual Machine (VM) is a software-based computer.

One physical server can host many VMs.

Example

```
Physical Server

---------------------

VM 1

Ubuntu

2 CPU

4 GB RAM

---------------------

VM 2

Windows

4 CPU

8 GB RAM

---------------------

VM 3

Amazon Linux

8 CPU

16 GB RAM
```

Each VM behaves like an independent computer.

______________________________________________________________________

# What is a Hypervisor?

A Hypervisor is software that creates and manages Virtual Machines.

```
Physical Hardware

↓

Hypervisor

↓

VM1

↓

VM2

↓

VM3
```

AWS uses the **Nitro System** for modern EC2 instances, providing virtualization, security, and high performance.

______________________________________________________________________

# EC2 Architecture

```
Internet

↓

VPC

↓

Subnet

↓

EC2

↓

Operating System

↓

Application

↓

Database
```

EC2 is usually deployed inside a VPC and subnet.

______________________________________________________________________

# Amazon Machine Image (AMI)

An AMI is a template used to launch EC2 instances.

It contains:

- Operating System
- Pre-installed Software (optional)
- Configuration
- Boot Information

Examples

- Amazon Linux
- Ubuntu
- Red Hat Enterprise Linux
- Windows Server

You can also create custom AMIs.

______________________________________________________________________

# Why Use AMIs?

Instead of configuring every server manually:

```
Create Server

↓

Install Software

↓

Configure

↓

Create AMI
```

Later:

```
Launch 100 Servers

↓

Same Configuration
```

This ensures consistency.

______________________________________________________________________

# EC2 Instance Types

AWS offers many instance families optimized for different workloads.

General Purpose

```
t3

t4g

m7i
```

Compute Optimized

```
c7g

c7i
```

Memory Optimized

```
r7g

x2idn
```

Storage Optimized

```
i4i

d3
```

Accelerated Computing (GPU)

```
g6

p5
```

> AWS regularly introduces new instance families. Always verify the latest offerings when designing production systems.

______________________________________________________________________

# Understanding Instance Names

Example

```
t3.medium
```

Breakdown

```
t

↓

Family

3

↓

Generation

medium

↓

Size
```

Larger sizes generally provide more CPU, memory, and networking capacity.

______________________________________________________________________

# Choosing an Instance Type

| Workload | Suggested Family |
|-----------|------------------|
| Small Web App | t3 / t4g |
| API Server | t3 / m7i |
| High CPU Processing | c7i |
| Large Database | r7g |
| Machine Learning | g6 / p5 |

Choose based on workload characteristics, not simply the largest instance.

______________________________________________________________________

# EC2 Instance Lifecycle

```
Launch

↓

Pending

↓

Running

↓

Stopping

↓

Stopped

↓

Starting

↓

Running

↓

Terminated
```

______________________________________________________________________

# Pending

AWS is preparing the VM.

- Allocating hardware
- Attaching storage
- Booting the operating system

Usually lasts less than a minute.

______________________________________________________________________

# Running

The server is operational.

You can:

- SSH into Linux
- RDP into Windows
- Deploy applications
- Install software

Billing for compute typically begins while the instance is running.

______________________________________________________________________

# Stop

Stopping:

- Shuts down the operating system
- Releases compute resources
- Preserves the EBS root volume (by default)

The instance can later be started again.

______________________________________________________________________

# Terminate

Termination permanently deletes the instance.

After termination:

- The VM is removed
- Instance Store data is lost
- EBS volumes marked "Delete on Termination" are deleted

This operation generally cannot be undone.

______________________________________________________________________

# Reboot

Reboot:

- Restarts the operating system
- Keeps the same instance
- Keeps the same EBS volumes
- Usually keeps the same private IP

______________________________________________________________________

# CPU and Memory

Each instance provides:

- Virtual CPUs (vCPUs)
- Memory (RAM)

Example

```
2 vCPU

4 GB RAM
```

Applications requiring more compute may need larger instance types.

______________________________________________________________________

# Networking

Each EC2 instance receives:

Private IP

```
10.x.x.x
```

Optional Public IP

```
52.x.x.x
```

Instances communicate privately within the VPC using private IP addresses.

______________________________________________________________________

# Elastic Network Interface (ENI)

An ENI is a virtual network card.

It contains:

- Private IP
- Security Groups
- MAC Address
- Optional Public IP association

An EC2 instance can have multiple ENIs depending on instance type.

______________________________________________________________________

# Elastic Block Store (EBS)

EBS is persistent block storage for EC2.

Think of it as a virtual hard drive.

```
EC2

↓

EBS Volume
```

Data remains even if the instance is stopped.

______________________________________________________________________

# EBS Features

- Persistent
- Encrypted (optional)
- Snapshots
- Resizeable
- High durability

Most production EC2 instances use EBS.

______________________________________________________________________

# Instance Store

Some EC2 instance types include local storage.

Characteristics:

- Extremely fast
- Temporary
- Data is lost when the instance stops or terminates (depending on the instance type and lifecycle)

Suitable for:

- Caches
- Temporary processing
- Scratch data

Not suitable for important persistent data.

______________________________________________________________________

# Security Groups

A Security Group acts as a **virtual firewall**.

It controls traffic entering and leaving the instance.

Example

Allow

```
SSH

22
```

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

Everything else is denied unless explicitly allowed.

______________________________________________________________________

# Security Group Characteristics

- Stateful
- Attached to ENIs
- Allow rules only
- Supports inbound and outbound rules

______________________________________________________________________

# Key Pair

Linux EC2 instances typically use SSH key pairs.

```
Private Key

↓

Your Laptop
```

```
Public Key

↓

EC2
```

Authentication is performed using the private key.

Protect your private key carefully.

______________________________________________________________________

# User Data

User Data is a startup script that runs automatically during the first boot (by default).

Example

```bash
#!/bin/bash

yum update -y

yum install nginx -y

systemctl enable nginx

systemctl start nginx
```

This automates initial server configuration.

______________________________________________________________________

# Elastic IP

Normally,

Public IP addresses may change when an instance is stopped and started.

Elastic IP is a static public IPv4 address.

```
Internet

↓

Elastic IP

↓

EC2
```

Useful when a stable public endpoint is required.

______________________________________________________________________

# Console Operations

Using the AWS Console you can:

- Launch instances
- Stop
- Start
- Reboot
- Terminate
- Attach EBS
- Modify Security Groups
- View monitoring
- Create AMIs

______________________________________________________________________

# AWS CLI

## List Instances

```bash
aws ec2 describe-instances
```

______________________________________________________________________

## Launch Instance

```bash
aws ec2 run-instances \
    --image-id ami-xxxxxxxx \
    --instance-type t3.micro \
    --key-name my-key
```

______________________________________________________________________

## Stop Instance

```bash
aws ec2 stop-instances \
    --instance-ids i-0123456789abcdef0
```

______________________________________________________________________

## Start Instance

```bash
aws ec2 start-instances \
    --instance-ids i-0123456789abcdef0
```

______________________________________________________________________

## Reboot

```bash
aws ec2 reboot-instances \
    --instance-ids i-0123456789abcdef0
```

______________________________________________________________________

## Terminate

```bash
aws ec2 terminate-instances \
    --instance-ids i-0123456789abcdef0
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

## List Instances

```python
import boto3

ec2 = boto3.client("ec2")

response = ec2.describe_instances()

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        print(instance["InstanceId"])
```

______________________________________________________________________

## Launch Instance

```python
ec2.run_instances(
    ImageId="ami-xxxxxxxx",
    InstanceType="t3.micro",
    MinCount=1,
    MaxCount=1
)
```

______________________________________________________________________

## Stop Instance

```python
ec2.stop_instances(
    InstanceIds=["i-0123456789abcdef0"]
)
```

______________________________________________________________________

## Terminate Instance

```python
ec2.terminate_instances(
    InstanceIds=["i-0123456789abcdef0"]
)
```

______________________________________________________________________

# Connecting to Linux EC2

Using SSH

```bash
chmod 400 my-key.pem
```

```bash
ssh -i my-key.pem ec2-user@PUBLIC_IP
```

Ubuntu AMIs often use:

```bash
ssh -i my-key.pem ubuntu@PUBLIC_IP
```

The default username depends on the AMI.

______________________________________________________________________

# Common EC2 Operations

Daily operations include:

- Launch servers
- Stop instances
- Restart services
- Resize instances
- Replace failed instances
- Create AMIs
- Attach EBS volumes
- Monitor CPU utilization
- Review Security Groups

______________________________________________________________________

# Common Mistakes

❌ Opening SSH (22) to the entire internet (`0.0.0.0/0`) unnecessarily

❌ Storing application secrets on the instance

❌ Using oversized instances for small workloads

❌ Forgetting to terminate unused instances

❌ Using Instance Store for critical data

❌ Logging in as the root user

❌ Not patching the operating system

❌ Launching production instances without IAM Roles

______________________________________________________________________

# Production Best Practices

- Use IAM Roles instead of Access Keys.
- Restrict Security Group access.
- Use EBS encryption.
- Enable detailed monitoring when appropriate.
- Use Auto Scaling for production workloads.
- Place instances in private subnets when possible.
- Store secrets in dedicated secret-management services.
- Take regular EBS snapshots.
- Use multiple Availability Zones for high availability.
- Keep AMIs updated with security patches.

______________________________________________________________________

# Interview Deep Dive

### Question

**Your EC2 instance is running, but you cannot SSH into it. How would you troubleshoot?**

### Answer

A systematic approach is:

1. Verify the instance is in the **Running** state.
1. Confirm the correct public IP or Elastic IP is being used.
1. Check that the Security Group allows inbound TCP port 22 from your IP.
1. Verify the subnet has a route to an Internet Gateway (if using a public subnet).
1. Ensure the instance has a public IP or Elastic IP.
1. Confirm the correct private key is being used.
1. Verify the operating system username (for example, `ec2-user` for Amazon Linux or `ubuntu` for Ubuntu).
1. Check Network ACLs if they are restrictive.
1. Review the instance's system logs through the AWS Console if boot issues are suspected.

______________________________________________________________________

# Summary

In this chapter you learned:

- What EC2 is
- Virtual Machines
- Hypervisors
- AMIs
- Instance Types
- Instance Lifecycle
- CPU, Memory and Networking
- ENIs
- EBS
- Instance Store
- Security Groups
- Key Pairs
- User Data
- Elastic IP
- AWS Console
- AWS CLI
- boto3 SDK
- Connecting to EC2
- Production best practices

EC2 is the foundation of compute in AWS and is widely used for web servers, backend APIs, microservices, batch jobs, and
many other workloads.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is Amazon EC2?
1. Why was EC2 created?
1. What is a Virtual Machine?
1. What is a Hypervisor?
1. What is the AWS Nitro System?

______________________________________________________________________

## AMIs and Instance Types

6. What is an AMI?
1. Why are AMIs useful?
1. What information does an AMI contain?
1. Explain the naming convention of `t3.medium`.
1. How would you choose an EC2 instance type for a CPU-intensive application?

______________________________________________________________________

## Lifecycle

11. Explain the EC2 instance lifecycle.
01. What happens when an instance is stopped?
01. What happens when an instance is terminated?
01. What is the difference between stopping and rebooting an instance?

______________________________________________________________________

## Storage and Networking

15. What is EBS?
01. What is the difference between EBS and Instance Store?
01. What is an ENI?
01. What is an Elastic IP?
01. Why might a public IP change after restarting an instance?

______________________________________________________________________

## Security

20. What is a Security Group?
01. Why is a Security Group considered stateful?
01. What is a Key Pair?
01. What is User Data used for?
01. Why should production EC2 instances use IAM Roles?

______________________________________________________________________

## CLI & SDK

25. Which AWS CLI command launches a new EC2 instance?
01. Which boto3 method lists EC2 instances?
01. How do you terminate an EC2 instance using the AWS CLI?

______________________________________________________________________

## Scenario-Based

28. Your application stores uploaded files on the EC2 instance itself. What risks does this create?
01. A production server's public IP changes after maintenance. How could you avoid this in the future?
01. Your web server receives "Connection Timed Out." Which EC2 networking and security components would you investigate first?
01. A backend service requires more RAM but not more CPU. Which type of EC2 instance family would you consider?

______________________________________________________________________

## Next

[EC2 Advanced](04_ec2_advanced.md)

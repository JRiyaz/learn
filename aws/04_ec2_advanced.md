# EC2 Advanced

> **Course:** AWS for Backend Engineers
>
> **Module:** 2
>
> **File:** `04_ec2_advanced.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Auto Scaling
- Launch Templates
- Load Balancers
- Placement Groups
- EC2 Purchasing Options
- Spot Instances
- Reserved Instances
- Savings Plans (Overview)
- Dedicated Hosts
- Dedicated Instances
- Elastic Network Interfaces
- EBS Snapshots
- CloudWatch Integration
- EC2 Monitoring
- Scaling Strategies
- High Availability
- Production Architecture
- Common Interview Questions
- Best Practices

______________________________________________________________________

# Why Advanced EC2?

Running **one EC2 instance** is easy.

Running

```
10

100

1000

10000
```

instances reliably is where real engineering begins.

Production systems must answer:

- What if traffic suddenly increases?
- What if a server crashes?
- What if an Availability Zone goes down?
- How do we reduce costs?
- How do we monitor servers?
- How do we deploy updates safely?

AWS provides several services and features to solve these problems.

______________________________________________________________________

# Auto Scaling

Auto Scaling automatically adjusts the number of EC2 instances based on demand.

Instead of manually launching servers:

```
Traffic Increases

↓

Auto Scaling

↓

Launch More Instances
```

When traffic decreases:

```
Traffic Drops

↓

Terminate Extra Instances
```

You pay only for the capacity you actually use.

______________________________________________________________________

# Why Auto Scaling?

Without Auto Scaling:

```
Morning

2 Servers

↓

Evening Sale

2 Servers

↓

Crash
```

With Auto Scaling:

```
Morning

2 Servers

↓

Evening Sale

20 Servers

↓

Night

2 Servers
```

Applications remain available while controlling costs.

______________________________________________________________________

# Auto Scaling Components

```
Auto Scaling Group

↓

Launch Template

↓

EC2 Instances
```

______________________________________________________________________

# Auto Scaling Group (ASG)

An Auto Scaling Group manages a collection of EC2 instances.

It ensures:

- Desired number of instances
- Health monitoring
- Automatic replacement
- Scaling up
- Scaling down

______________________________________________________________________

# Desired Capacity

Example

```
Desired = 4
```

If one instance fails:

```
Running

3

↓

ASG

↓

Launch New Instance

↓

Running

4
```

The desired capacity is maintained automatically.

______________________________________________________________________

# Minimum and Maximum Capacity

Example

```
Minimum

2

Desired

4

Maximum

10
```

AWS will never:

- Scale below 2
- Scale above 10

______________________________________________________________________

# Scaling Policies

Auto Scaling needs rules.

Example

```
CPU > 70%

↓

Launch Instance
```

```
CPU < 20%

↓

Terminate Instance
```

Policies can be based on:

- CPU utilization
- Memory (with custom metrics)
- Network traffic
- Request count
- Queue length
- Custom CloudWatch metrics

______________________________________________________________________

# Launch Templates

Launch Templates define how new EC2 instances should be created.

They include:

- AMI
- Instance Type
- Security Groups
- IAM Role
- User Data
- Storage
- Key Pair
- Tags

Every new instance launched by an ASG uses this template.

______________________________________________________________________

# Why Launch Templates?

Imagine manually creating 500 identical servers.

Instead:

```
Template

↓

Launch

↓

500 Identical Instances
```

Consistency is guaranteed.

______________________________________________________________________

# Load Balancer

When multiple EC2 instances exist,

users should not connect directly to a specific server.

Instead:

```
Users

↓

Load Balancer

↓

EC2-1

↓

EC2-2

↓

EC2-3
```

The Load Balancer distributes requests.

______________________________________________________________________

# Benefits of Load Balancing

- High Availability
- Better Performance
- Fault Tolerance
- Horizontal Scaling
- Health Checks

______________________________________________________________________

# Health Checks

Suppose

```
EC2-2

↓

Application Crash
```

Load Balancer detects:

```
Unhealthy
```

Requests stop going to that instance.

Auto Scaling launches another healthy server.

______________________________________________________________________

# Elastic Load Balancer Types

AWS provides several load balancer types.

### Application Load Balancer (ALB)

Layer 7 (HTTP/HTTPS)

Supports:

- Path-based routing
- Host-based routing
- WebSockets
- HTTP/2

Common for web applications and APIs.

______________________________________________________________________

### Network Load Balancer (NLB)

Layer 4 (TCP/UDP)

Characteristics:

- Extremely fast
- Very low latency
- Static IP support

Suitable for high-performance networking workloads.

______________________________________________________________________

### Gateway Load Balancer (GWLB)

Designed for integrating virtual network appliances such as firewalls.

______________________________________________________________________

# EC2 Placement Groups

Placement Groups control how EC2 instances are physically placed inside AWS infrastructure.

Three types:

- Cluster
- Spread
- Partition

______________________________________________________________________

# Cluster Placement Group

Instances are placed close together.

Benefits

- Lowest network latency
- Highest throughput

Used for:

- High Performance Computing (HPC)
- Big Data
- Distributed computing

______________________________________________________________________

# Spread Placement Group

Instances are placed on separate hardware.

Benefits

- Reduces correlated hardware failures

Useful for:

- Critical small deployments
- Domain controllers
- Licensing servers

______________________________________________________________________

# Partition Placement Group

Instances are divided into partitions.

Failure in one partition does not affect the others.

Useful for:

- Hadoop
- Cassandra
- Kafka
- Large distributed systems

______________________________________________________________________

# EC2 Purchasing Options

AWS provides multiple pricing models.

Choose based on workload characteristics.

______________________________________________________________________

# On-Demand Instances

Pay only while the instance runs.

Benefits

- Flexible
- No long-term commitment
- Good for development
- Good for unpredictable workloads

Most teams begin here.

______________________________________________________________________

# Reserved Instances (RI)

Commit to a longer usage term for a discounted price.

Suitable for:

- Predictable workloads
- Always-on production systems

______________________________________________________________________

# Savings Plans (Overview)

Savings Plans also provide discounts in exchange for a usage commitment.

Compared to Reserved Instances, they generally offer more flexibility across eligible compute services.

______________________________________________________________________

# Spot Instances

AWS sells unused compute capacity at significant discounts.

Benefits

- Very inexpensive

Risk

AWS can reclaim the instance with short notice.

Best for:

- Batch processing
- CI/CD jobs
- Image rendering
- Machine learning training
- Fault-tolerant workloads

Not recommended for stateful critical services unless designed for interruption.

______________________________________________________________________

# Dedicated Instances

Run on hardware dedicated to a single customer at the instance level.

Useful for certain compliance and licensing requirements.

______________________________________________________________________

# Dedicated Hosts

Provide an entire physical server dedicated to your organization.

Useful when:

- Software licensing requires physical host visibility
- Strict compliance requirements exist

______________________________________________________________________

# Elastic Network Interface (Advanced)

An ENI can be detached from one instance and attached to another (subject to compatibility and availability
constraints).

Benefits

- Faster failover
- Flexible networking
- Multiple network interfaces

______________________________________________________________________

# EBS Snapshots

Snapshots are backups of EBS volumes stored in Amazon S3 internally (managed by AWS).

Example

```
EBS Volume

↓

Snapshot

↓

Restore Later
```

Use cases:

- Disaster recovery
- Migration
- Backup
- Cloning

______________________________________________________________________

# Monitoring with CloudWatch

EC2 integrates with CloudWatch.

Available metrics include:

- CPU Utilization
- Network In
- Network Out
- Disk Operations
- Status Checks

Additional metrics can be collected using the CloudWatch Agent.

______________________________________________________________________

# CloudWatch Alarms

Example

```
CPU > 80%

↓

Alarm

↓

Notification

↓

Auto Scaling
```

Alarms can trigger automated actions.

______________________________________________________________________

# Scaling Strategies

## Vertical Scaling

Increase the size of one server.

Example

```
t3.medium

↓

m7i.large
```

Pros

- Simple

Cons

- Downtime may be required
- Hardware limits exist

______________________________________________________________________

## Horizontal Scaling

Increase the number of servers.

```
2 Servers

↓

10 Servers
```

Pros

- Better availability
- Better scalability

Preferred for cloud-native applications.

______________________________________________________________________

# High Availability

Single server

```
Users

↓

EC2
```

If it fails,

everything stops.

______________________________________________________________________

Production

```
Users

↓

Load Balancer

↓

EC2 (AZ-A)

↓

EC2 (AZ-B)

↓

EC2 (AZ-C)
```

If one Availability Zone fails,

traffic continues through the others.

______________________________________________________________________

# Blue-Green Deployment (Overview)

Instead of updating the existing environment:

```
Blue

(Current)

↓

Green

(New Version)
```

After validation,

traffic switches to the Green environment.

Benefits:

- Reduced downtime
- Easier rollback

______________________________________________________________________

# Rolling Deployment

Update instances gradually.

Example

```
10 Servers

↓

Update 2

↓

Healthy

↓

Update Next 2
```

Reduces deployment risk.

______________________________________________________________________

# Production Architecture

```
Internet

↓

Application Load Balancer

↓

Auto Scaling Group

↓

EC2 Instances

↓

IAM Role

↓

CloudWatch

↓

EBS

↓

Database
```

This is a common architecture for backend services.

______________________________________________________________________

# Cost Optimization Tips

- Use Auto Scaling.
- Shut down unused development instances.
- Use Spot Instances for interruptible workloads.
- Purchase Reserved Instances or Savings Plans for predictable workloads.
- Delete unused EBS volumes and snapshots.
- Right-size instances based on monitoring data.
- Monitor costs regularly.

______________________________________________________________________

# Common EC2 Security Practices

- Disable password-based SSH where possible.
- Restrict Security Group rules.
- Use IAM Roles.
- Encrypt EBS volumes.
- Keep operating systems updated.
- Use private subnets for internal services.
- Avoid exposing management ports to the internet.
- Rotate SSH keys when appropriate.

______________________________________________________________________

# Common Mistakes

❌ Running production on a single EC2 instance

❌ No Auto Scaling

❌ No Load Balancer

❌ Ignoring CloudWatch alarms

❌ Overprovisioning instance sizes

❌ Not taking EBS snapshots

❌ Using Spot Instances for critical stateful applications without interruption handling

❌ Allowing unrestricted inbound access in Security Groups

______________________________________________________________________

# Interview Deep Dive

### Question

**Your production application suddenly receives ten times more traffic than usual. How would you design your EC2
architecture to handle it?**

### Answer

A production-ready design would include:

1. Deploy multiple EC2 instances across at least two Availability Zones.
1. Place the instances behind an Application Load Balancer.
1. Use an Auto Scaling Group with a Launch Template.
1. Configure scaling policies based on CPU utilization or request count.
1. Monitor the application with CloudWatch metrics and alarms.
1. Store persistent application data outside the EC2 instances (for example, in databases or object storage).
1. Use IAM Roles instead of storing AWS credentials on the instances.
1. Take regular EBS snapshots and design for stateless application servers to simplify scaling and recovery.

______________________________________________________________________

# Summary

In this chapter you learned:

- Auto Scaling
- Launch Templates
- Application, Network, and Gateway Load Balancers
- Placement Groups
- Purchasing Options
- Spot Instances
- Reserved Instances
- Savings Plans
- Dedicated Hosts
- Dedicated Instances
- EBS Snapshots
- CloudWatch integration
- Vertical vs Horizontal Scaling
- High Availability
- Deployment strategies
- Production architecture
- Cost optimization

These features transform EC2 from a single virtual machine into a resilient, scalable production platform.

______________________________________________________________________

# Practice Questions

## Auto Scaling

1. What is an Auto Scaling Group?
1. What is Desired Capacity?
1. Explain Minimum, Desired, and Maximum Capacity.
1. How do scaling policies work?
1. Why are Launch Templates required?

______________________________________________________________________

## Load Balancing

6. Why do we need a Load Balancer?
1. What is the difference between an ALB and an NLB?
1. What are health checks?
1. How does a Load Balancer improve availability?

______________________________________________________________________

## Placement Groups

10. What is a Placement Group?
01. When would you use a Cluster Placement Group?
01. When is a Spread Placement Group useful?
01. Why are Partition Placement Groups common in distributed systems?

______________________________________________________________________

## Pricing

14. What are On-Demand Instances?
01. When should you use Reserved Instances?
01. What are Savings Plans?
01. What are Spot Instances?
01. Why are Spot Instances inexpensive?
01. What workloads are best suited for Spot Instances?

______________________________________________________________________

## Storage & Monitoring

20. What is an EBS Snapshot?
01. What metrics does CloudWatch collect for EC2?
01. How can CloudWatch alarms trigger Auto Scaling?

______________________________________________________________________

## Architecture

23. Explain Vertical Scaling.
01. Explain Horizontal Scaling.
01. Why is Horizontal Scaling preferred for cloud-native applications?
01. What is High Availability?
01. Explain Blue-Green Deployment.
01. Explain Rolling Deployment.

______________________________________________________________________

## Scenario-Based

29. Your application must remain available even if one Availability Zone fails. How would you design the infrastructure?
01. Your nightly batch-processing workload is very expensive. How could Spot Instances reduce costs?
01. A development team launches dozens of oversized EC2 instances that remain idle. What cost optimization steps would you recommend?
01. Your application experiences uneven traffic throughout the day. Which AWS services and EC2 features would you combine to automatically scale capacity while minimizing costs?

______________________________________________________________________

## Next

[S3 Fundamentals](05_s3_fundamentals.md)

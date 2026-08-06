# ECS Production

> **Course:** AWS for Backend Engineers
>
> **Module:** 7
>
> **File:** `15_ecs_production.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Production ECS Architecture
- High Availability
- Service Auto Scaling
- Health Checks
- Application Load Balancer Integration
- Rolling Deployments
- Blue-Green Deployments
- ECS Deployment Circuit Breaker
- Container Health Checks
- Secrets Management
- Logging
- Monitoring
- CI/CD Pipeline
- Production Security
- Troubleshooting
- Best Practices

______________________________________________________________________

# What is a Production-Ready ECS Deployment?

Running a container is easy.

Running a container that serves **millions of users** without downtime is difficult.

A production deployment must handle:

- Failures
- Traffic spikes
- Deployments
- Security
- Monitoring
- Rollbacks

______________________________________________________________________

# Typical Production Architecture

```
                    Internet
                        │
                        ▼
        +-----------------------------+
        | Application Load Balancer   |
        +-----------------------------+
                  │            │
                  ▼            ▼
           AZ-A                 AZ-B
     +---------------+   +---------------+
     | ECS Service   |   | ECS Service   |
     | Task 1        |   | Task 3        |
     | Task 2        |   | Task 4        |
     +---------------+   +---------------+
              │                 │
              └──────┬──────────┘
                     ▼
             Amazon RDS / Aurora

                     │
                     ▼
                  Amazon S3

                     │
                     ▼
              CloudWatch Logs
```

______________________________________________________________________

# High Availability

Never deploy:

```
1 Task
```

If it crashes

↓

Application Down

Instead

```
Task-1

Task-2

Task-3

↓

Load Balancer
```

One failure should not stop the application.

______________________________________________________________________

# Multi-AZ Deployment

Production deployments should span multiple Availability Zones.

```
AZ-A

↓

Tasks
```

```
AZ-B

↓

Tasks
```

If one Availability Zone fails,

the other continues serving traffic.

______________________________________________________________________

# Service Auto Scaling

Traffic changes throughout the day.

```
Morning

2 Tasks
```

```
Evening

20 Tasks
```

```
Night

2 Tasks
```

Auto Scaling adjusts the desired task count automatically.

______________________________________________________________________

# Scaling Metrics

Common scaling metrics include:

- CPU Utilization
- Memory Utilization
- ALB Request Count
- Custom CloudWatch Metrics
- SQS Queue Length (for worker services)

Choose metrics that best represent workload demand.

______________________________________________________________________

# Health Checks

Health checks prevent traffic from reaching unhealthy containers.

Two types are commonly used.

______________________________________________________________________

## Container Health Check

Runs inside the container.

Example

```
HTTP

/health
```

or

```
Check Process

↓

Healthy
```

______________________________________________________________________

## Load Balancer Health Check

The ALB periodically checks:

```
GET

/health
```

If the response fails,

traffic stops flowing to that task.

______________________________________________________________________

# Example Health Endpoint

```python
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
```

Simple.

Fast.

No database dependency unless required.

______________________________________________________________________

# Rolling Deployment

Current

```
Version 1

10 Tasks
```

Deploy

```
Replace

2 Tasks

↓

Healthy

↓

Replace Next 2
```

Benefits

- Minimal downtime
- Gradual rollout
- Easier failure detection

______________________________________________________________________

# Deployment Configuration

Typical ECS deployment settings include concepts such as:

- Desired Count
- Minimum Healthy Percent
- Maximum Percent

Example

```
Desired

10
```

```
Minimum Healthy

100%
```

```
Maximum

200%
```

This allows new tasks to start before old ones stop, reducing downtime.

______________________________________________________________________

# Blue-Green Deployment

Instead of replacing existing tasks,

create a new environment.

```
Blue

(Current)
```

↓

Deploy

```
Green

(New Version)
```

↓

Switch Traffic

↓

Delete Blue (after validation)

______________________________________________________________________

# Benefits

- Near-zero downtime
- Quick rollback
- Safer releases

______________________________________________________________________

# ECS Deployment Circuit Breaker

Suppose deployment begins.

```
Version 2

↓

Containers Crash
```

Instead of replacing every task,

the Deployment Circuit Breaker detects repeated failures and can automatically stop the deployment and roll back (when
rollback is enabled).

This protects production availability.

______________________________________________________________________

# Secrets Management

Never store

```
Database Password

API Keys

JWT Secret
```

inside

- Docker Images
- Source Code
- GitHub

Instead use:

- AWS Secrets Manager
- AWS Systems Manager Parameter Store

Applications retrieve secrets securely at runtime.

______________________________________________________________________

# Example Flow

```
Task

↓

IAM Role

↓

Secrets Manager

↓

Database Password
```

No hardcoded credentials.

______________________________________________________________________

# Logging

Containers should write logs to

```
stdout

stderr
```

ECS forwards them to:

```
CloudWatch Logs
```

Benefits

- Centralized logs
- Easy searching
- Alerts
- Long-term retention

______________________________________________________________________

# Monitoring

Monitor:

Infrastructure

- CPU
- Memory
- Network

Application

- Request Count
- Error Rate
- Response Time
- Business Metrics

Use CloudWatch dashboards and alarms.

______________________________________________________________________

# Container Insights

CloudWatch Container Insights provides additional ECS metrics such as:

- Cluster utilization
- Service utilization
- Task metrics
- Container resource usage

Useful for production monitoring.

______________________________________________________________________

# CI/CD Pipeline

Typical workflow

```
Git Push

↓

GitHub Actions

↓

Run Tests

↓

Docker Build

↓

Push Image

↓

Amazon ECR

↓

Update ECS Service

↓

Rolling Deployment
```

Every deployment is automated.

______________________________________________________________________

# Deployment Strategy Comparison

| Strategy | Downtime | Rollback | Risk |
|----------|----------|----------|------|
| Rolling | Very Low | Moderate | Low |
| Blue-Green | Near Zero | Very Fast | Lowest |
| Recreate | High | Slow | High |

______________________________________________________________________

# Production Security

- Use Task Roles.
- Keep tasks in private subnets.
- Use Security Groups with least privilege.
- Enable image scanning in ECR.
- Store secrets in Secrets Manager.
- Encrypt data at rest and in transit.
- Enable logging.
- Regularly patch base images.
- Use HTTPS through an Application Load Balancer.

______________________________________________________________________

# Troubleshooting Production Issues

Example

```
Service Down
```

Checklist

```
Task Running?

↓

Health Check Passing?

↓

ALB Healthy?

↓

Container Logs?

↓

CloudWatch Metrics?

↓

Security Groups?

↓

IAM Permissions?

↓

Application Errors?
```

A systematic approach saves time.

______________________________________________________________________

# Production Architecture

```
Internet

↓

Application Load Balancer

↓

ECS Service

↓

Tasks

↓

Task Role

↓

Amazon RDS

↓

Amazon S3

↓

Secrets Manager

↓

CloudWatch Logs

↓

CloudWatch Alarms

↓

SNS Notifications
```

______________________________________________________________________

# Cost Optimization

- Right-size CPU and memory.
- Enable Service Auto Scaling.
- Remove unused Task Definitions.
- Delete unused ECR images.
- Use Fargate Spot (where appropriate and supported).
- Scale worker services based on queue depth.
- Monitor utilization continuously.

______________________________________________________________________

# Common Mistakes

❌ Deploying only one task

❌ No health checks

❌ Storing secrets in Docker images

❌ Ignoring CloudWatch alarms

❌ Running without Auto Scaling

❌ Deploying directly to production without rollback strategy

❌ Using mutable image tags

❌ No monitoring dashboards

______________________________________________________________________

# Production Best Practices

- Deploy across multiple AZs.
- Always use an Application Load Balancer.
- Enable Auto Scaling.
- Use rolling or blue-green deployments.
- Enable Container Insights.
- Use immutable image versions.
- Store secrets outside containers.
- Centralize logs.
- Monitor infrastructure and business metrics.
- Test rollback procedures regularly.

______________________________________________________________________

# Interview Deep Dive

### Question

**How would you design a highly available ECS deployment for a production FastAPI application?**

### Answer

A production-ready design would include:

1. Build a Docker image and store it in Amazon ECR.
1. Deploy an ECS Service with multiple Tasks.
1. Spread Tasks across at least two Availability Zones.
1. Place the Service behind an Application Load Balancer.
1. Configure container and ALB health checks.
1. Enable Service Auto Scaling based on CPU utilization or request count.
1. Store secrets in AWS Secrets Manager and access them through Task Roles.
1. Send logs to CloudWatch Logs and monitor infrastructure and application metrics.
1. Use immutable image versions and automated CI/CD.
1. Prefer rolling or blue-green deployments with rollback capabilities.

______________________________________________________________________

# Summary

In this chapter you learned:

- Production ECS architecture
- High Availability
- Service Auto Scaling
- Health Checks
- Application Load Balancer integration
- Rolling Deployments
- Blue-Green Deployments
- Deployment Circuit Breaker
- Secrets Management
- Logging
- Monitoring
- Container Insights
- CI/CD integration
- Production security
- Troubleshooting
- Cost optimization

These practices form the foundation of a reliable, secure, and scalable container platform on AWS.

______________________________________________________________________

# Practice Questions

## Production Architecture

1. Why should production ECS services run multiple tasks?
1. Why should tasks be distributed across multiple Availability Zones?
1. Why is an Application Load Balancer commonly used with ECS?

______________________________________________________________________

## Health Checks

4. What is the difference between a container health check and an ALB health check?
1. Why should health endpoints be lightweight?
1. What happens when a task fails a load balancer health check?

______________________________________________________________________

## Deployments

7. Explain a Rolling Deployment.
1. Explain a Blue-Green Deployment.
1. What are the advantages of Blue-Green deployments?
1. What is the ECS Deployment Circuit Breaker?

______________________________________________________________________

## Scaling

11. Which metrics can drive ECS Service Auto Scaling?
01. Why might request count be a better scaling metric than CPU for some applications?

______________________________________________________________________

## Security

13. Why should secrets never be stored in Docker images?
01. How should ECS tasks retrieve database credentials?
01. Why are Task Roles preferred over AWS Access Keys?

______________________________________________________________________

## Monitoring

16. What metrics should be monitored for an ECS production service?
01. What is CloudWatch Container Insights?
01. Why should container logs be written to stdout and stderr?

______________________________________________________________________

## Scenario-Based

19. Your deployment succeeds, but the new tasks never receive production traffic. Which components would you investigate?
01. During a deployment, every new container immediately crashes. Which ECS feature can automatically stop the rollout?
01. Your API traffic triples during business hours every weekday. How would you configure ECS to handle this efficiently?
01. A developer accidentally commits database credentials into the Docker image. How would you redesign the solution?
01. Your company requires deployments with near-zero downtime and instant rollback capability. Which deployment strategy would you recommend and why?
01. Your operations team reports increasing response times even though CPU utilization remains low. Which application metrics and CloudWatch tools would you investigate?

______________________________________________________________________

## Next

[End-to-End Backend Deployment](16_end_to_end_backend_deployment.md)

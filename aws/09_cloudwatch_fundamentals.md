# CloudWatch Fundamentals

> **Course:** AWS for Backend Engineers
>
> **Module:** 5
>
> **File:** `09_cloudwatch_fundamentals.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Amazon CloudWatch is
- Why CloudWatch exists
- Monitoring vs Logging
- Metrics
- Dimensions
- Namespaces
- Logs
- Log Groups
- Log Streams
- CloudWatch Alarms
- Dashboards
- Events (EventBridge Overview)
- CloudWatch Agent
- Console
- AWS CLI
- AWS SDK (Python boto3)
- Production Monitoring Best Practices

______________________________________________________________________

# What is Amazon CloudWatch?

**Amazon CloudWatch** is AWS's **monitoring and observability service**.

It collects:

- Metrics
- Logs
- Events
- Alarms

from AWS resources and applications.

CloudWatch helps answer questions like:

- Is my server healthy?
- Is CPU usage too high?
- Why is my application slow?
- Did an EC2 instance fail?
- When did an error occur?

______________________________________________________________________

# Why Was CloudWatch Created?

Imagine running:

```
500 EC2 Instances

↓

No Monitoring
```

Questions become difficult to answer:

- Which server is overloaded?
- Which application is failing?
- Which instance is down?
- When did CPU spike?
- Why did latency increase?

CloudWatch provides visibility into your infrastructure.

______________________________________________________________________

# Real World Analogy

Think of a hospital.

Doctors monitor:

- Heart Rate
- Blood Pressure
- Oxygen Levels

CloudWatch monitors:

- CPU
- Memory
- Network
- Disk
- Logs
- Errors

If something abnormal happens,

an alarm is triggered.

______________________________________________________________________

# Monitoring vs Logging

These terms are different.

______________________________________________________________________

## Monitoring

Monitoring answers:

> **How is the system behaving?**

Examples

- CPU Usage
- Memory Usage
- Network Traffic
- Error Rate
- Request Count

______________________________________________________________________

## Logging

Logging answers:

> **What actually happened?**

Example Log

```
2026-08-07 10:05:23

User Login Failed

Username: riyaz

Reason: Invalid Password
```

Logs provide detailed event history.

______________________________________________________________________

# CloudWatch Architecture

```
EC2

↓

Metrics

↓

CloudWatch

↓

Dashboards

↓

Alarms

↓

Notifications
```

Applications can also send custom metrics and logs.

______________________________________________________________________

# What are Metrics?

A Metric is a numerical value measured over time.

Examples

```
CPU Utilization

42%
```

```
Memory Usage

68%
```

```
Disk Read Operations

150/sec
```

______________________________________________________________________

# Common AWS Metrics

EC2

- CPU Utilization
- Network In
- Network Out
- Disk Read Operations
- Status Checks

Application Load Balancer

- Request Count
- Target Response Time
- HTTP 4XX
- HTTP 5XX

S3

- Request Count
- Bytes Downloaded
- Errors

Lambda

- Invocations
- Errors
- Duration
- Throttles

______________________________________________________________________

# Metric Namespace

Metrics are grouped into namespaces.

Examples

```
AWS/EC2

AWS/S3

AWS/Lambda

AWS/RDS
```

Custom applications can create their own namespaces.

Example

```
Company/Payments
```

______________________________________________________________________

# Metric Dimensions

Dimensions provide additional information about a metric.

Example

```
CPU Utilization

↓

InstanceId

↓

i-0123456789
```

Another example

```
HTTP Requests

↓

Environment

↓

Production
```

Dimensions help filter and organize metrics.

______________________________________________________________________

# Metric Resolution

CloudWatch supports:

Standard Resolution

```
1 Minute
```

High Resolution

```
1 Second
```

High-resolution metrics are useful for latency-sensitive applications.

______________________________________________________________________

# CloudWatch Logs

Logs store application and system events.

Examples

```
Application Logs

Nginx Logs

Apache Logs

System Logs

Container Logs
```

______________________________________________________________________

# Log Group

A Log Group is a collection of related logs.

Example

```
/aws/ec2/backend

↓

Log Group
```

Think of it as a folder.

______________________________________________________________________

# Log Stream

A Log Stream represents one source of logs within a Log Group.

Example

```
Log Group

↓

EC2-1

↓

Log Stream
```

```
Log Group

↓

EC2-2

↓

Log Stream
```

______________________________________________________________________

# Log Hierarchy

```
CloudWatch Logs

↓

Log Group

↓

Log Stream

↓

Log Events
```

______________________________________________________________________

# Log Event Example

```
2026-08-07T10:15:21Z

INFO

User Login Successful

UserId=123
```

______________________________________________________________________

# CloudWatch Agent

By default,

EC2 provides only basic system metrics.

The CloudWatch Agent collects additional information.

Examples

- Memory Usage
- Disk Usage
- Running Processes
- Custom Logs

Install the agent on EC2 when you need enhanced monitoring.

______________________________________________________________________

# Dashboards

Dashboards display multiple metrics in one place.

Example

```
CPU

Memory

Network

↓

Dashboard
```

Useful for operations teams.

______________________________________________________________________

# Alarm

An Alarm watches a metric.

Example

```
CPU > 80%

↓

Alarm

↓

Notification
```

______________________________________________________________________

# Alarm States

CloudWatch Alarms have three states.

```
OK

↓

ALARM

↓

INSUFFICIENT_DATA
```

______________________________________________________________________

# Example Alarm

```
CPU Utilization

>

80%

↓

5 Minutes

↓

Alarm
```

Possible actions

- Send Notification
- Trigger Auto Scaling
- Invoke Systems Manager Automation

______________________________________________________________________

# CloudWatch Events (Overview)

Historically,

CloudWatch Events handled event-based automation.

Today,

**Amazon EventBridge** is the recommended service for event routing, while maintaining compatibility with CloudWatch
Events concepts.

Example

```
EC2 Stops

↓

EventBridge

↓

Lambda

↓

Send Email
```

______________________________________________________________________

# Dashboard Example

```
+----------------------+

CPU

Memory

Disk

Network

Request Count

Errors

+----------------------+
```

One screen for the entire application.

______________________________________________________________________

# AWS Console

Using the Console you can:

- View Metrics
- View Logs
- Create Dashboards
- Create Alarms
- Explore Metrics
- Configure Log Groups
- Configure Retention
- View Event History

______________________________________________________________________

# AWS CLI

## List Metrics

```bash
aws cloudwatch list-metrics
```

______________________________________________________________________

## Get Metric Statistics

```bash
aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization
```

______________________________________________________________________

## Create Alarm

```bash
aws cloudwatch put-metric-alarm \
    --alarm-name HighCPU
```

A production alarm usually includes thresholds, periods, evaluation settings, and actions.

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

# AWS SDK (Python boto3)

## Installation

```bash
pip install boto3
```

______________________________________________________________________

## Create CloudWatch Client

```python
import boto3

cloudwatch = boto3.client("cloudwatch")
```

______________________________________________________________________

## List Metrics

```python
response = cloudwatch.list_metrics()

for metric in response["Metrics"]:
    print(metric["MetricName"])
```

______________________________________________________________________

## Put Custom Metric

```python
cloudwatch.put_metric_data(
    Namespace="Company/Payments",
    MetricData=[
        {
            "MetricName": "OrdersProcessed",
            "Value": 125
        }
    ]
)
```

______________________________________________________________________

## Create Logs Client

```python
logs = boto3.client("logs")
```

______________________________________________________________________

## List Log Groups

```python
response = logs.describe_log_groups()

for group in response["logGroups"]:
    print(group["logGroupName"])
```

______________________________________________________________________

# Common CloudWatch Operations

Daily tasks include:

- Monitor CPU
- Monitor Memory
- View Logs
- Create Dashboards
- Configure Alarms
- Analyze Application Logs
- Publish Custom Metrics
- Configure Log Retention

______________________________________________________________________

# Common Mistakes

❌ Monitoring only CPU and ignoring memory

❌ Never deleting old logs

❌ Creating alarms that never notify anyone

❌ Ignoring alarm history

❌ Not collecting application logs

❌ Using inconsistent metric names

❌ Keeping log retention indefinitely without business need

______________________________________________________________________

# Production Best Practices

- Enable the CloudWatch Agent on EC2.
- Monitor infrastructure and application metrics.
- Collect structured application logs.
- Configure meaningful alarms.
- Set appropriate log retention periods.
- Create dashboards for critical services.
- Publish custom business metrics.
- Monitor error rates, not just CPU utilization.
- Review alarm thresholds periodically.

______________________________________________________________________

# Interview Deep Dive

### Question

**Your production application is reported as "slow." How would you use CloudWatch to investigate?**

### Answer

A structured investigation would include:

1. Review EC2 CPU utilization, memory usage (if the CloudWatch Agent is installed), and network metrics.
1. Check Application Load Balancer metrics such as request count, latency, and HTTP 5XX errors.
1. Examine CloudWatch Logs for application exceptions and error messages.
1. Review recent CloudWatch Alarms to identify unusual events.
1. Compare current metrics with historical trends.
1. Determine whether the issue is caused by infrastructure, the application, or increased traffic.
1. If needed, publish additional custom metrics to improve future observability.

______________________________________________________________________

# Summary

In this chapter you learned:

- What CloudWatch is
- Monitoring vs Logging
- Metrics
- Namespaces
- Dimensions
- CloudWatch Logs
- Log Groups
- Log Streams
- CloudWatch Agent
- Dashboards
- Alarms
- EventBridge overview
- AWS Console
- AWS CLI
- boto3 SDK
- Production monitoring best practices

CloudWatch is the primary observability service in AWS and forms the foundation for monitoring, alerting,
troubleshooting, and operational visibility.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is Amazon CloudWatch?
1. Why was CloudWatch created?
1. Explain the difference between Monitoring and Logging.
1. What is a Metric?
1. What is a Namespace?

______________________________________________________________________

## Metrics

6. What is a Dimension?
1. What is High-Resolution Monitoring?
1. Name five common EC2 metrics.
1. Why would an application publish custom metrics?

______________________________________________________________________

## Logs

10. What is a Log Group?
01. What is a Log Stream?
01. What is a Log Event?
01. Why should application logs be centralized?

______________________________________________________________________

## Monitoring

14. What is the CloudWatch Agent?
01. Why is the CloudWatch Agent important?
01. What is a Dashboard?
01. What are the three Alarm states?

______________________________________________________________________

## Alarms

18. How do CloudWatch Alarms work?
01. What actions can an alarm trigger?
01. Why should alarm thresholds be reviewed periodically?

______________________________________________________________________

## CLI & SDK

21. Which CLI command lists CloudWatch metrics?
01. Which boto3 method publishes a custom metric?
01. Which boto3 client is used for CloudWatch Logs?

______________________________________________________________________

## Scenario-Based

24. Your application is healthy, but users report increased response times. Which CloudWatch metrics would you investigate first?
01. Your operations team receives no notifications even though CPU usage exceeds 90%. What configuration issues might you check?
01. Your company wants to monitor the number of successful payments processed every minute. Which CloudWatch feature would you use?
01. A production EC2 instance reports normal CPU usage but is running out of memory. Why might this not appear in CloudWatch by default?
01. Your log storage costs continue to increase every month. How would you optimize CloudWatch Logs?
01. Your development team wants a single dashboard showing infrastructure health, API errors, request count, and latency. How would you build this using CloudWatch?

______________________________________________________________________

## Next

[CloudWatch Advanced](10_cloudwatch_advanced.md)

# CloudWatch Advanced

> **Course:** AWS for Backend Engineers
>
> **Module:** 5
>
> **File:** `10_cloudwatch_advanced.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Custom Metrics
- Metric Math
- Metric Filters
- Composite Alarms
- CloudWatch Logs Insights
- Log Retention Policies
- CloudWatch Agent (Advanced)
- Embedded Metric Format (EMF)
- Anomaly Detection
- EventBridge Integration
- SNS Notifications
- Auto Scaling Integration
- Cross-Account Monitoring
- Observability Best Practices
- Production Monitoring Architecture

______________________________________________________________________

# Why Advanced CloudWatch?

Monitoring CPU alone is not enough.

Production systems require answers like:

- Which API is slow?
- Which customer is generating errors?
- Which deployment caused failures?
- Are we receiving abnormal traffic?
- Can we detect problems before users notice?

Advanced CloudWatch provides these capabilities.

______________________________________________________________________

# Observability vs Monitoring

Monitoring answers:

> **Is something wrong?**

Example

```
CPU = 95%
```

Observability answers:

> **Why is something wrong?**

Example

```
API

↓

Database Slow

↓

Connection Pool Exhausted
```

CloudWatch contributes to observability through metrics, logs, alarms, and integrations.

______________________________________________________________________

# Custom Metrics

AWS automatically publishes infrastructure metrics.

Applications often need business metrics.

Examples

- Orders Processed
- Active Users
- Failed Payments
- Login Success Rate
- Messages Published
- Queue Length

These are called **Custom Metrics**.

______________________________________________________________________

# Example

Instead of monitoring

```
CPU
```

Monitor

```
Orders Per Minute
```

Business metrics often provide more meaningful operational insight.

______________________________________________________________________

# Publishing Custom Metrics

Example

```python
import boto3

cloudwatch = boto3.client("cloudwatch")

cloudwatch.put_metric_data(
    Namespace="Company/Orders",
    MetricData=[
        {
            "MetricName": "OrdersProcessed",
            "Value": 275
        }
    ]
)
```

______________________________________________________________________

# Metric Dimensions (Advanced)

Dimensions make metrics more useful.

Example

```
OrdersProcessed

↓

Region = India

↓

Environment = Production

↓

API = Checkout
```

Now you can analyze metrics at multiple levels.

______________________________________________________________________

# Metric Math

Metric Math combines multiple metrics.

Example

```
Successful Requests

/

Total Requests

↓

Success Rate
```

Another example

```
CPU-A

+

CPU-B

↓

Average CPU
```

Useful for dashboards and alarms.

______________________________________________________________________

# Metric Filters

Metric Filters convert log data into metrics.

Example Log

```
ERROR

Database Timeout
```

Metric Filter

↓

Count Errors

↓

CloudWatch Metric

↓

Alarm

No application code changes are required.

______________________________________________________________________

# Example Flow

```
Application Logs

↓

CloudWatch Logs

↓

Metric Filter

↓

Custom Metric

↓

Alarm
```

______________________________________________________________________

# CloudWatch Logs Insights

Logs Insights allows interactive querying of CloudWatch Logs.

Example query

```sql
fields @timestamp, @message
| filter level = "ERROR"
| sort @timestamp desc
| limit 20
```

Useful for troubleshooting production incidents.

______________________________________________________________________

# More Logs Insights Examples

Find slow requests

```sql
fields latency
| filter latency > 1000
```

Find login failures

```sql
fields username
| filter status = "FAILED"
```

Logs Insights supports powerful filtering, aggregation, and visualization.

______________________________________________________________________

# Log Retention

By default,

logs can remain indefinitely.

Example retention policy

```
Development

30 Days
```

```
Production

365 Days
```

Choose retention based on operational and compliance requirements.

______________________________________________________________________

# Why Retention Policies?

Without retention

```
Logs

↓

Years

↓

Higher Costs
```

Retention policies automatically remove old logs when appropriate.

______________________________________________________________________

# CloudWatch Agent (Advanced)

The agent can collect:

Infrastructure

- CPU
- Memory
- Disk
- Swap

Application

- Nginx Logs
- Apache Logs
- Custom Logs

Operating System

- Process metrics
- Disk utilization
- Network statistics

______________________________________________________________________

# Embedded Metric Format (EMF)

Instead of separately sending:

- Logs
- Metrics

Applications can embed metrics directly inside structured log entries.

Example

```
Application

↓

Structured Log

↓

CloudWatch

↓

Metrics Automatically Extracted
```

Useful for high-scale serverless and containerized applications.

______________________________________________________________________

# Anomaly Detection

Traditional alarm

```
CPU > 80%
```

Static threshold.

Anomaly Detection

```
Machine Learning

↓

Expected Pattern

↓

Unexpected Spike

↓

Alarm
```

Useful when normal traffic changes throughout the day.

______________________________________________________________________

# Example

Normal traffic

```
Morning

100 Requests
```

Evening

```
5000 Requests
```

Static alarms may create false positives.

Anomaly Detection learns normal behavior.

______________________________________________________________________

# Composite Alarms

Suppose

```
CPU High
```

and

```
Memory High
```

Instead of receiving two alerts,

combine them.

```
CPU Alarm

+

Memory Alarm

↓

Composite Alarm
```

This reduces alert noise.

______________________________________________________________________

# SNS Integration

CloudWatch commonly sends notifications using Amazon SNS.

Example

```
Alarm

↓

SNS

↓

Email

SMS

Lambda

HTTP Endpoint
```

Operations teams receive immediate notifications.

______________________________________________________________________

# Auto Scaling Integration

CloudWatch can trigger Auto Scaling.

Example

```
CPU > 70%

↓

Alarm

↓

Auto Scaling

↓

Launch New EC2
```

Or

```
CPU < 20%

↓

Terminate Extra Instances
```

______________________________________________________________________

# EventBridge Integration

CloudWatch metrics and alarms can integrate with EventBridge.

Example

```
Alarm

↓

EventBridge

↓

Lambda

↓

Create Incident
```

Or

```
EC2 Stopped

↓

EventBridge

↓

Slack Notification
```

______________________________________________________________________

# Cross-Account Monitoring

Large organizations often have:

```
Production Account

↓

Development Account

↓

Security Account
```

CloudWatch can aggregate monitoring across accounts when appropriately configured.

Useful for centralized operations teams.

______________________________________________________________________

# Cross-Region Dashboards

One dashboard can display metrics from multiple AWS Regions.

Example

```
Mumbai

↓

Frankfurt

↓

Ohio

↓

Single Dashboard
```

Useful for global applications.

______________________________________________________________________

# Production Monitoring Architecture

```
EC2

↓

CloudWatch Agent

↓

Metrics

↓

CloudWatch

↓

Dashboards

↓

Metric Filters

↓

Alarms

↓

SNS

↓

Operations Team
```

Applications

```
Application Logs

↓

CloudWatch Logs

↓

Logs Insights

↓

Troubleshooting
```

______________________________________________________________________

# Golden Signals

A common observability concept.

Monitor:

- Latency
- Traffic
- Errors
- Saturation

Example

```
API

↓

Latency

↓

Errors

↓

Requests

↓

CPU
```

These signals help identify production issues quickly.

______________________________________________________________________

# Common Mistakes

❌ Monitoring only infrastructure metrics

❌ No business metrics

❌ Too many alarms

❌ No log retention policy

❌ Ignoring Logs Insights

❌ Alerting on every warning

❌ No dashboard for production

❌ No alert ownership

______________________________________________________________________

# Production Best Practices

- Publish custom business metrics.
- Use Metric Filters to detect application errors.
- Configure log retention.
- Build operational dashboards.
- Use Composite Alarms to reduce alert fatigue.
- Use Anomaly Detection where traffic is highly variable.
- Integrate alarms with SNS.
- Monitor latency and error rates in addition to CPU.
- Regularly review alarm thresholds.

______________________________________________________________________

# Interview Deep Dive

### Question

**Your application's CPU usage is normal, but customers report that checkout requests are failing. How would CloudWatch
help you identify the problem?**

### Answer

A structured investigation would include:

1. Review application logs in CloudWatch Logs for checkout-related exceptions.
1. Use Logs Insights to filter error messages and failed requests.
1. Check custom metrics such as failed payment count or checkout success rate.
1. Review Application Load Balancer metrics for HTTP 5XX errors and response latency.
1. Examine CloudWatch dashboards to identify correlated changes across infrastructure and application metrics.
1. Review recent alarms and deployment events.
1. If recurring failures are identified, create Metric Filters and alarms to detect similar issues automatically in the future.

______________________________________________________________________

# Summary

In this chapter you learned:

- Custom Metrics
- Metric Math
- Metric Filters
- Logs Insights
- Log Retention
- Embedded Metric Format
- Composite Alarms
- Anomaly Detection
- EventBridge Integration
- SNS Notifications
- Auto Scaling Integration
- Cross-Account Monitoring
- Cross-Region Dashboards
- Golden Signals
- Production monitoring practices

These capabilities allow CloudWatch to evolve from a basic monitoring service into a comprehensive observability
platform.

______________________________________________________________________

# Practice Questions

## Metrics

1. What are Custom Metrics?
1. Why are business metrics often more valuable than CPU metrics?
1. What are Metric Dimensions?
1. What is Metric Math?
1. Give two examples of Metric Math.

______________________________________________________________________

## Logs

6. What are Metric Filters?
1. How do Metric Filters convert logs into metrics?
1. What is CloudWatch Logs Insights?
1. Why are retention policies important?

______________________________________________________________________

## Advanced Features

10. What is Embedded Metric Format?
01. What is Anomaly Detection?
01. How do Composite Alarms reduce alert fatigue?
01. What are the Golden Signals?

______________________________________________________________________

## Integrations

14. How does CloudWatch integrate with SNS?
01. How can CloudWatch trigger Auto Scaling?
01. How does EventBridge complement CloudWatch?

______________________________________________________________________

## Architecture

17. Why is cross-account monitoring useful?
01. Why are cross-region dashboards valuable for global applications?
01. Why should production systems monitor both infrastructure and business metrics?

______________________________________________________________________

## Scenario-Based

20. Your operations team receives hundreds of alerts every day, many of which are duplicates. Which CloudWatch features would help reduce alert noise?
01. Your application logs contain "Database Timeout" messages, but there is no metric tracking them. How would you create automatic monitoring?
01. Your API traffic changes dramatically between business hours and nighttime. Why might static alarm thresholds be insufficient?
01. Your compliance team requires production logs to be retained for one year while development logs should be deleted after one month. How would you implement this?
01. Customers report intermittent checkout failures, but EC2 CPU usage remains normal. Which CloudWatch tools would you use to investigate?
01. Your company wants to monitor "Orders Processed Per Minute" across multiple AWS accounts and Regions. Which CloudWatch capabilities would you use?

______________________________________________________________________

## Next

[ECR Fundamentals](11_ecr_fundamentals.md)

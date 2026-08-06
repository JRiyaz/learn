# Questions

> File: `08_questions.md`

______________________________________________________________________

# GitHub Actions & CI/CD Practice Questions

> These questions are designed for **Backend Engineers (5+ Years)** preparing for technical interviews. They progress from fundamentals to advanced production scenarios.

______________________________________________________________________

# Table of Contents

1. CI/CD Fundamentals
1. GitHub Actions Basics
1. Workflows
1. Jobs & Steps
1. Runners
1. YAML
1. Events
1. Expressions & Contexts
1. Variables & Secrets
1. Caching & Artifacts
1. Docker Integration
1. AWS Deployments
1. Kubernetes
1. Helm
1. Security
1. Pipeline Design
1. Debugging
1. Performance Optimization
1. Production Scenarios
1. Architecture & Design

______________________________________________________________________

# CI/CD Fundamentals

### Q1.

What is Continuous Integration?

______________________________________________________________________

### Q2.

What is Continuous Delivery?

______________________________________________________________________

### Q3.

What is Continuous Deployment?

______________________________________________________________________

### Q4.

Differentiate Continuous Delivery and Continuous Deployment.

______________________________________________________________________

### Q5.

Why is CI important?

______________________________________________________________________

### Q6.

What problems does CI solve?

______________________________________________________________________

### Q7.

Describe a typical CI pipeline.

______________________________________________________________________

### Q8.

Describe a typical CD pipeline.

______________________________________________________________________

### Q9.

Why should deployments be automated?

______________________________________________________________________

### Q10.

What are the advantages of CI/CD?

______________________________________________________________________

# GitHub Actions Basics

### Q11.

What is GitHub Actions?

______________________________________________________________________

### Q12.

Why do companies use GitHub Actions?

______________________________________________________________________

### Q13.

How does GitHub Actions compare with Jenkins?

______________________________________________________________________

### Q14.

How does GitHub Actions compare with GitLab CI?

______________________________________________________________________

### Q15.

What are GitHub-hosted runners?

______________________________________________________________________

### Q16.

What are self-hosted runners?

______________________________________________________________________

### Q17.

When would you use self-hosted runners?

______________________________________________________________________

### Q18.

How does a GitHub Actions workflow execute?

______________________________________________________________________

### Q19.

Explain the lifecycle of a workflow.

______________________________________________________________________

### Q20.

What is the GitHub Actions Marketplace?

______________________________________________________________________

# Workflows

### Q21.

What is a workflow?

______________________________________________________________________

### Q22.

Where are workflows stored?

______________________________________________________________________

### Q23.

How is a workflow triggered?

______________________________________________________________________

### Q24.

Can a repository have multiple workflows?

______________________________________________________________________

### Q25.

When would you split workflows?

______________________________________________________________________

### Q26.

What is `workflow_dispatch`?

______________________________________________________________________

### Q27.

What is a scheduled workflow?

______________________________________________________________________

### Q28.

Can a workflow trigger another workflow?

______________________________________________________________________

### Q29.

What is a reusable workflow?

______________________________________________________________________

### Q30.

When would you use reusable workflows?

______________________________________________________________________

# Jobs & Steps

### Q31.

What is a job?

______________________________________________________________________

### Q32.

What is a step?

______________________________________________________________________

### Q33.

Difference between a workflow and a job.

______________________________________________________________________

### Q34.

Difference between a job and a step.

______________________________________________________________________

### Q35.

Difference between `run` and `uses`.

______________________________________________________________________

### Q36.

Can jobs run in parallel?

______________________________________________________________________

### Q37.

How do you make jobs run sequentially?

______________________________________________________________________

### Q38.

What does `needs` do?

______________________________________________________________________

### Q39.

Can one job access another job's outputs?

______________________________________________________________________

### Q40.

How do you share data between jobs?

______________________________________________________________________

# Runners

### Q41.

What is a runner?

______________________________________________________________________

### Q42.

What operating systems are available?

______________________________________________________________________

### Q43.

When should you use Ubuntu runners?

______________________________________________________________________

### Q44.

When should you use Windows runners?

______________________________________________________________________

### Q45.

When should you use macOS runners?

______________________________________________________________________

### Q46.

How do GitHub-hosted runners work?

______________________________________________________________________

### Q47.

What are ephemeral runners?

______________________________________________________________________

### Q48.

What are the benefits of self-hosted runners?

______________________________________________________________________

### Q49.

What are the disadvantages of self-hosted runners?

______________________________________________________________________

### Q50.

How would you choose between GitHub-hosted and self-hosted runners?

______________________________________________________________________

# YAML

### Q51.

Why does GitHub Actions use YAML?

______________________________________________________________________

### Q52.

Why is indentation important?

______________________________________________________________________

### Q53.

Explain the purpose of the `name` keyword.

______________________________________________________________________

### Q54.

Explain the purpose of the `jobs` keyword.

______________________________________________________________________

### Q55.

Explain the purpose of the `steps` keyword.

______________________________________________________________________

### Q56.

Explain the purpose of `runs-on`.

______________________________________________________________________

### Q57.

Explain the purpose of `with`.

______________________________________________________________________

### Q58.

Explain the purpose of `env`.

______________________________________________________________________

### Q59.

Explain the purpose of `permissions`.

______________________________________________________________________

### Q60.

Explain the purpose of `defaults`.

______________________________________________________________________

# Events

### Q61.

What events can trigger workflows?

______________________________________________________________________

### Q62.

Explain `push`.

______________________________________________________________________

### Q63.

Explain `pull_request`.

______________________________________________________________________

### Q64.

Explain `release`.

______________________________________________________________________

### Q65.

Explain `workflow_dispatch`.

______________________________________________________________________

### Q66.

Explain scheduled workflows.

______________________________________________________________________

### Q67.

How do tag-based workflows work?

______________________________________________________________________

### Q68.

When would you use release workflows?

______________________________________________________________________

### Q69.

How do you trigger deployments only from the `main` branch?

______________________________________________________________________

### Q70.

How do you deploy only when a tag is created?

______________________________________________________________________

# Expressions & Contexts

### Q71.

What is `${{ }}`?

______________________________________________________________________

### Q72.

What are GitHub contexts?

______________________________________________________________________

### Q73.

Explain the `github` context.

______________________________________________________________________

### Q74.

Explain the `runner` context.

______________________________________________________________________

### Q75.

Explain the `matrix` context.

______________________________________________________________________

### Q76.

Explain the `needs` context.

______________________________________________________________________

### Q77.

Explain `success()`.

______________________________________________________________________

### Q78.

Explain `failure()`.

______________________________________________________________________

### Q79.

Explain `always()`.

______________________________________________________________________

### Q80.

When would you use conditional execution?

______________________________________________________________________

# Variables & Secrets

### Q81.

Difference between variables and secrets.

______________________________________________________________________

### Q82.

Where are repository secrets stored?

______________________________________________________________________

### Q83.

How are secrets used?

______________________________________________________________________

### Q84.

Can secrets be printed safely?

______________________________________________________________________

### Q85.

Why are secrets masked?

______________________________________________________________________

### Q86.

What are organization secrets?

______________________________________________________________________

### Q87.

What are environment secrets?

______________________________________________________________________

### Q88.

Why should secrets never be committed?

______________________________________________________________________

### Q89.

How do you rotate secrets?

______________________________________________________________________

### Q90.

Why is OIDC preferred over long-lived cloud credentials?

______________________________________________________________________

# Caching & Artifacts

### Q91.

What is dependency caching?

______________________________________________________________________

### Q92.

What is an artifact?

______________________________________________________________________

### Q93.

Difference between cache and artifacts.

______________________________________________________________________

### Q94.

What happens during a cache miss?

______________________________________________________________________

### Q95.

How are cache keys generated?

______________________________________________________________________

### Q96.

What kinds of files should be uploaded as artifacts?

______________________________________________________________________

### Q97.

Can artifacts be shared across jobs?

______________________________________________________________________

### Q98.

How long are artifacts retained?

______________________________________________________________________

### Q99.

When would you use dependency caching?

______________________________________________________________________

### Q100.

How does Docker layer caching improve build performance?

______________________________________________________________________

# Docker Integration

### Q101.

Why build Docker images inside CI?

______________________________________________________________________

### Q102.

Why deploy Docker images instead of source code?

______________________________________________________________________

### Q103.

How would you tag Docker images?

______________________________________________________________________

### Q104.

Why are immutable image tags important?

______________________________________________________________________

### Q105.

What is a container registry?

______________________________________________________________________

### Q106.

What is Amazon ECR?

______________________________________________________________________

### Q107.

How does a Docker deployment pipeline work?

______________________________________________________________________

### Q108.

How do you push Docker images to Amazon ECR?

______________________________________________________________________

### Q109.

How would you roll back a Docker deployment?

______________________________________________________________________

### Q110.

How would you debug Docker build failures?

______________________________________________________________________

# AWS Deployments

### Q111.

How would you deploy to Amazon ECS?

______________________________________________________________________

### Q112.

How would you deploy to EC2?

______________________________________________________________________

### Q113.

Difference between ECS and EC2 deployments.

______________________________________________________________________

### Q114.

What is Amazon ECR?

______________________________________________________________________

### Q115.

What is OIDC?

______________________________________________________________________

### Q116.

How does GitHub authenticate with AWS using OIDC?

______________________________________________________________________

### Q117.

Why avoid AWS access keys?

______________________________________________________________________

### Q118.

What are GitHub Environments?

______________________________________________________________________

### Q119.

Why use production approvals?

______________________________________________________________________

### Q120.

How would you implement a production deployment pipeline?

______________________________________________________________________

# Kubernetes

### Q121.

How would GitHub Actions deploy to Kubernetes?

______________________________________________________________________

### Q122.

What is a rolling update?

______________________________________________________________________

### Q123.

What is `kubectl rollout status`?

______________________________________________________________________

### Q124.

What is `kubectl rollout undo`?

______________________________________________________________________

### Q125.

Why are readiness probes important?

______________________________________________________________________

### Q126.

How would you monitor Kubernetes deployments?

______________________________________________________________________

### Q127.

How would you debug a failed deployment?

______________________________________________________________________

### Q128.

What causes CrashLoopBackOff?

______________________________________________________________________

### Q129.

How do you achieve zero downtime?

______________________________________________________________________

### Q130.

How would you roll back a Kubernetes deployment?

______________________________________________________________________

# Helm

### Q131.

What is Helm?

______________________________________________________________________

### Q132.

Why use Helm instead of raw YAML?

______________________________________________________________________

### Q133.

What is a Helm chart?

______________________________________________________________________

### Q134.

How would you deploy with Helm?

______________________________________________________________________

### Q135.

What are Helm values?

______________________________________________________________________

### Q136.

How does Helm simplify CI/CD?

______________________________________________________________________

### Q137.

Can Helm perform rollbacks?

______________________________________________________________________

### Q138.

How do Helm releases work?

______________________________________________________________________

### Q139.

How would you upgrade a Helm deployment?

______________________________________________________________________

### Q140.

How would you debug Helm deployments?

______________________________________________________________________

# Security

### Q141.

What is the principle of least privilege?

______________________________________________________________________

### Q142.

Why should permissions be minimized?

______________________________________________________________________

### Q143.

Why pin action versions?

______________________________________________________________________

### Q144.

How do you evaluate third-party GitHub Actions?

______________________________________________________________________

### Q145.

What is branch protection?

______________________________________________________________________

### Q146.

Why require pull requests?

______________________________________________________________________

### Q147.

Why require status checks?

______________________________________________________________________

### Q148.

How does secret scanning help?

______________________________________________________________________

### Q149.

Why should production deployments require approvals?

______________________________________________________________________

### Q150.

Describe a secure GitHub Actions pipeline.

______________________________________________________________________

# Pipeline Design

### Q151.

Describe a production-ready backend pipeline.

______________________________________________________________________

### Q152.

Why separate CI and CD?

______________________________________________________________________

### Q153.

What stages should a backend pipeline contain?

______________________________________________________________________

### Q154.

Why should linting run before testing?

______________________________________________________________________

### Q155.

What are smoke tests?

______________________________________________________________________

### Q156.

How would you design a deployment pipeline for FastAPI?

______________________________________________________________________

### Q157.

How would you design CI/CD for Flask?

______________________________________________________________________

### Q158.

How would you design CI/CD for Django?

______________________________________________________________________

### Q159.

How would you design CI/CD for microservices?

______________________________________________________________________

### Q160.

How would you design CI/CD for a monorepo?

______________________________________________________________________

# Debugging

### Q161.

How do you debug a failed workflow?

______________________________________________________________________

### Q162.

Where do you start reading logs?

______________________________________________________________________

### Q163.

How do you debug Docker build failures?

______________________________________________________________________

### Q164.

How do you debug Kubernetes deployments?

______________________________________________________________________

### Q165.

How do you debug ECS deployments?

______________________________________________________________________

### Q166.

How do you identify YAML syntax errors?

______________________________________________________________________

### Q167.

How do you investigate authentication failures?

______________________________________________________________________

### Q168.

How do you troubleshoot missing artifacts?

______________________________________________________________________

### Q169.

What causes cache misses?

______________________________________________________________________

### Q170.

How would you troubleshoot a failed production deployment?

______________________________________________________________________

# Performance Optimization

### Q171.

How do you reduce pipeline execution time?

______________________________________________________________________

### Q172.

Why use parallel jobs?

______________________________________________________________________

### Q173.

How does dependency caching help?

______________________________________________________________________

### Q174.

What is Docker layer caching?

______________________________________________________________________

### Q175.

How do path filters improve performance?

______________________________________________________________________

### Q176.

Why build only affected services in a monorepo?

______________________________________________________________________

### Q177.

How does concurrency improve workflows?

______________________________________________________________________

### Q178.

How do you reduce GitHub Actions costs?

______________________________________________________________________

### Q179.

When would you use self-hosted runners?

______________________________________________________________________

### Q180.

How do you optimize large CI/CD pipelines?

______________________________________________________________________

# Production Scenarios

### Q181.

A deployment succeeded but the application is failing health checks. What would you investigate first?

______________________________________________________________________

### Q182.

A GitHub Actions workflow suddenly starts failing after months of working. How would you approach debugging?

______________________________________________________________________

### Q183.

A Docker image builds locally but fails in CI. What could be the cause?

______________________________________________________________________

### Q184.

A Kubernetes deployment is stuck during rollout. What commands would you use?

______________________________________________________________________

### Q185.

A deployment introduced database errors. How would you respond?

______________________________________________________________________

### Q186.

Two deployments are running simultaneously. How would you prevent this?

______________________________________________________________________

### Q187.

A deployment accidentally exposed AWS credentials. What immediate actions would you take?

______________________________________________________________________

### Q188.

A pipeline now takes 45 minutes instead of 12. How would you investigate?

______________________________________________________________________

### Q189.

A production deployment fails halfway through. What rollback strategy would you recommend?

______________________________________________________________________

### Q190.

Your smoke tests fail after deployment. Should traffic continue to the new version? Why or why not?

______________________________________________________________________

# Architecture & Design

### Q191.

Design a CI/CD pipeline for a FastAPI microservice deployed on Amazon ECS.

______________________________________________________________________

### Q192.

Design a GitHub Actions workflow for a monorepo containing multiple Python services.

______________________________________________________________________

### Q193.

Design a secure deployment pipeline using GitHub Actions and AWS OIDC.

______________________________________________________________________

### Q194.

Design a zero-downtime deployment pipeline for Kubernetes.

______________________________________________________________________

### Q195.

Design a release pipeline supporting staging and production environments.

______________________________________________________________________

### Q196.

How would you organize GitHub Actions workflows across 100 repositories?

______________________________________________________________________

### Q197.

How would you standardize CI/CD across an engineering organization?

______________________________________________________________________

### Q198.

How would you introduce GitHub Actions into an existing Jenkins-based organization?

______________________________________________________________________

### Q199.

How would you design a rollback strategy for production deployments?

______________________________________________________________________

### Q200.

If you were designing CI/CD for a company from scratch, what principles would you follow?

______________________________________________________________________

# Congratulations!

You have completed the **GitHub Actions & CI/CD Crash Course**.

At this point, you should be comfortable discussing:

- GitHub Actions architecture
- Workflow design
- Jobs, steps, runners, and matrices
- Expressions, contexts, variables, and secrets
- CI/CD pipeline design
- Docker integration
- Amazon ECR, ECS, and EC2 deployments
- Kubernetes and Helm deployments
- GitHub Environments and approvals
- OIDC authentication
- Security best practices
- Debugging and troubleshooting
- Performance optimization
- Real-world deployment strategies
- Production incident handling
- End-to-end CI/CD system design for backend services

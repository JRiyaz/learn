# 07-storage.md

# Storage in Kubernetes

> **🎯 This is one of the most misunderstood Kubernetes topics.**
>
> Beginners often think:
>
> > "If my PostgreSQL database runs inside a Pod, my data will always be there."
>
> Unfortunately, that's **not true**.
>
> Pods are **temporary**, but your data usually isn't.
>
> This lesson teaches **how Kubernetes separates applications from data**.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 35–45 minutes |
| Revision Time | 20 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Storage is one of the first real production challenges.

Interviewers want to evaluate whether you understand:

- Why containers lose data
- Volumes
- Persistent Volumes (PV)
- Persistent Volume Claims (PVC)
- Storage Classes
- Stateful applications
- Databases in Kubernetes
- Production storage best practices

______________________________________________________________________

# Learning Goals

By the end of this lesson, you should understand:

- Why Pods lose data
- What a Volume is
- What a Persistent Volume is
- What a Persistent Volume Claim is
- What a StorageClass is
- How databases use persistent storage
- When to use StatefulSets

______________________________________________________________________

# The Biggest Production Problem

Suppose your FastAPI application uses PostgreSQL.

Architecture

```text
Pod

↓

PostgreSQL
```

Everything works.

Customers place orders.

Database stores them.

______________________________________________________________________

Now imagine

```
Pod crashes
```

ReplicaSet creates

a new Pod.

Question

Where is your data?

Gone.

______________________________________________________________________

# Why Does This Happen?

Remember

Pods are

**ephemeral**.

When a Pod is deleted,

its filesystem is also deleted.

Visual

```text
Pod

↓

Filesystem

↓

Database Files
```

Delete Pod

↓

Filesystem disappears.

______________________________________________________________________

# Backend Engineering Analogy

Imagine storing your company's customer database

inside your laptop's

`/tmp` directory.

Laptop crashes.

Temporary files disappear.

Production databases should never depend on temporary storage.

______________________________________________________________________

# Kubernetes Philosophy

Applications are temporary.

Data is permanent.

These two should be managed separately.

______________________________________________________________________

# What Is a Volume?

A Volume is

storage

attached to a Pod.

Instead of writing

```text
Container

↓

Temporary Filesystem
```

the container writes to

```text
Container

↓

Volume
```

______________________________________________________________________

# Visual

Without Volume

```text
Pod

↓

Filesystem

↓

Deleted
```

Data gone.

______________________________________________________________________

With Volume

```text
Pod

↓

Volume

↓

Persistent Storage
```

Pod disappears.

Storage remains.

______________________________________________________________________

# Different Types of Volumes

Kubernetes supports many volume types.

For backend interviews,

remember these:

- emptyDir
- Persistent Volume
- Persistent Volume Claim

______________________________________________________________________

# emptyDir

Simplest volume.

Created

when Pod starts.

Deleted

when Pod dies.

Useful for

temporary data.

Example

```text
Image Processing

↓

Temporary Files

↓

Delete Later
```

Not suitable for databases.

______________________________________________________________________

# Persistent Volume (PV)

A Persistent Volume

represents

real storage.

Examples

- AWS EBS
- Azure Disk
- Google Persistent Disk
- NFS
- SAN
- Local SSD

Think of it as

the physical storage resource.

______________________________________________________________________

# Backend Analogy

Imagine renting storage.

Cloud Provider

↓

100 GB SSD

Kubernetes sees this as

a Persistent Volume.

______________________________________________________________________

# Persistent Volume Claim (PVC)

Applications should not know

where storage comes from.

Instead,

they request storage.

Example

```text
Need

20 GB
```

The application doesn't care whether it's:

- AWS
- Azure
- GCP
- NFS

It simply requests storage.

That's a PVC.

______________________________________________________________________

# Real-Life Analogy

Imagine booking a hotel.

You don't care

which room number

you get.

You only request

```
One Room
```

Hotel assigns one.

Similarly

Application

↓

PVC

↓

Storage

______________________________________________________________________

# Relationship

```text
Pod

↓

Persistent Volume Claim

↓

Persistent Volume

↓

Cloud Disk
```

This diagram appears

very frequently

in interviews.

______________________________________________________________________

# Step-by-Step Flow

Suppose

FastAPI

needs PostgreSQL.

______________________________________________________________________

Step 1

Application requests

```text
50 GB
```

______________________________________________________________________

Step 2

PVC created.

______________________________________________________________________

Step 3

PVC binds

to

a Persistent Volume.

______________________________________________________________________

Step 4

Persistent Volume

uses

AWS EBS.

______________________________________________________________________

Step 5

Pod mounts

the storage.

Done.

______________________________________________________________________

# Visual

```text
FastAPI Pod

↓

PVC

↓

PV

↓

AWS EBS
```

Simple.

______________________________________________________________________

# StorageClass

Question

Who creates

Persistent Volumes?

Historically,

admins created them manually.

Bad experience.

Need automation.

______________________________________________________________________

StorageClass solves this.

Instead of creating

a PV manually,

StorageClass automatically provisions storage.

______________________________________________________________________

Visual

```text
PVC

↓

StorageClass

↓

AWS creates Disk

↓

PV created automatically
```

This is called

```
Dynamic Provisioning
```

______________________________________________________________________

# Backend Analogy

Imagine AWS EC2.

You don't manually install hardware.

You request

a VM.

AWS creates it.

StorageClass works similarly

for disks.

______________________________________________________________________

# Complete Architecture

```text
Application

↓

Pod

↓

PVC

↓

StorageClass

↓

PV

↓

Cloud Disk
```

______________________________________________________________________

# Why PVC Instead of Directly Using PV?

Decoupling.

Pods shouldn't know

which cloud provider

is used.

Tomorrow

you move

AWS

↓

Azure.

Application

doesn't change.

Only storage implementation changes.

______________________________________________________________________

# Database Example

Suppose

PostgreSQL

stores

```text
orders
```

Architecture

```text
PostgreSQL Pod

↓

PVC

↓

Persistent Volume

↓

AWS EBS
```

Pod crashes.

New Pod starts.

Same PVC.

Same disk.

Orders still exist.

______________________________________________________________________

# Stateful Applications

Some applications

cannot lose identity.

Examples

- PostgreSQL
- MySQL
- MongoDB
- Kafka
- Redis Cluster
- ZooKeeper

These usually use

StatefulSets.

We'll study them

next chapter.

______________________________________________________________________

# Should Databases Run Inside Kubernetes?

Common interview question.

Answer

```
It depends.
```

Small companies

often run

PostgreSQL

inside Kubernetes.

Large companies

may use

managed databases.

Example

- AWS RDS
- Cloud SQL
- Azure Database

Advantages

- Automatic backups
- Maintenance
- Replication
- Monitoring

Applications still run

inside Kubernetes.

______________________________________________________________________

# Volume YAML

```yaml
apiVersion: v1

kind: PersistentVolumeClaim

metadata:
  name: postgres-data

spec:
  accessModes:
    - ReadWriteOnce

  resources:
    requests:
      storage: 20Gi
```

Focus on

- Storage request
- Access mode

______________________________________________________________________

# Access Modes

Interviewers sometimes ask this.

______________________________________________________________________

## ReadWriteOnce (RWO)

One Node

can mount

the volume.

Most common.

Used by

PostgreSQL.

______________________________________________________________________

## ReadOnlyMany (ROX)

Many Pods

read only.

______________________________________________________________________

## ReadWriteMany (RWX)

Many Pods

can read

and write.

Useful for

shared file systems.

______________________________________________________________________

# Complete Production Flow

```text
User

↓

FastAPI

↓

PostgreSQL Pod

↓

PVC

↓

Persistent Volume

↓

AWS EBS
```

Pod crashes.

↓

New Pod.

↓

Same Volume.

↓

Data preserved.

______________________________________________________________________

# Common kubectl Commands

View PVCs

```bash
kubectl get pvc
```

______________________________________________________________________

View PVs

```bash
kubectl get pv
```

______________________________________________________________________

Describe PVC

```bash
kubectl describe pvc postgres-data
```

______________________________________________________________________

Describe PV

```bash
kubectl describe pv
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Storing database files

inside the container filesystem.

Data disappears when the Pod is recreated.

______________________________________________________________________

## Mistake 2

Confusing

PVC

with

PV.

PVC

requests storage.

PV

provides storage.

______________________________________________________________________

## Mistake 3

Thinking StorageClass stores data.

StorageClass only

creates storage automatically.

______________________________________________________________________

## Mistake 4

Using

emptyDir

for databases.

Never do this.

______________________________________________________________________

## Mistake 5

Assuming Kubernetes automatically backs up your data.

Persistent storage prevents data loss from Pod recreation, but **backups are a separate responsibility**.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Pods are ephemeral, so data stored inside the container filesystem is lost when the Pod is recreated. Kubernetes solves this by separating compute from storage. Applications request storage using a Persistent Volume Claim, which binds to a Persistent Volume. A StorageClass can dynamically provision the required storage from the underlying infrastructure. This allows applications such as PostgreSQL to survive Pod restarts without losing data."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why can't we store PostgreSQL data inside the Pod?**

Because Pods are temporary and their filesystem disappears when they are deleted.

______________________________________________________________________

**Q. What's the difference between a PV and a PVC?**

A PV is the actual storage resource.

A PVC is the application's request for storage.

______________________________________________________________________

**Q. Why use a StorageClass?**

It automatically provisions storage instead of requiring administrators to create Persistent Volumes manually.

______________________________________________________________________

**Q. Does Kubernetes back up Persistent Volumes?**

No.

Persistent storage and backups are different concerns.

______________________________________________________________________

**Q. When should I use a StatefulSet?**

When applications require stable identity and persistent storage, such as PostgreSQL, Kafka, or ZooKeeper.

______________________________________________________________________

# Pattern Summary

| Component | Responsibility |
|-----------|----------------|
| Volume | Storage attached to a Pod |
| emptyDir | Temporary storage |
| Persistent Volume (PV) | Actual storage resource |
| Persistent Volume Claim (PVC) | Storage request |
| StorageClass | Automatic storage provisioning |
| StatefulSet | Stateful applications |

______________________________________________________________________

# Quick Revision

- Pods are ephemeral.
- Container filesystems disappear when Pods are deleted.
- Volumes provide storage to Pods.
- `emptyDir` is temporary storage.
- Persistent Volumes represent real storage.
- Persistent Volume Claims request storage.
- StorageClasses enable dynamic provisioning.
- Databases should use persistent storage.
- Backups are separate from persistent storage.
- Stateful applications often use StatefulSets.

______________________________________________________________________

# Key Takeaway

The biggest lesson from this chapter is:

> **Separate compute from data.**

Pods should be treated as disposable, but your application's data should not. Kubernetes achieves this by allowing Pods
to mount persistent storage through **Persistent Volume Claims**, keeping data independent from the lifecycle of
individual Pods. This separation is fundamental to running production databases and other stateful applications on
Kubernetes.

______________________________________________________________________

# Next

[08-scaling-and-autoscaling.md](08-scaling-and-autoscaling.md)

# Linux Complete Interview & Production Course

# File 15 — Systemd and Service Management

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Process Management
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 14 — Process Management

______________________________________________________________________

# Table of Contents

1. Introduction
1. What is a Service?
1. What is systemd?
1. Why systemd Replaced init
1. Boot Process Overview
1. systemd Units
1. The `systemctl` Command
1. Managing Services
1. Service Status
1. Enabling and Disabling Services
1. Restarting and Reloading Services
1. The `journalctl` Command
1. Targets in systemd
1. Creating a Custom Service
1. Production Examples
1. Common Mistakes
1. Best Practices
1. Interview Questions
1. Practice Exercises
1. Cheat Sheet
1. Summary
1. Next

______________________________________________________________________

# 1. Introduction

Modern Linux systems use **systemd** as their initialization and service management system.

Almost every production Linux server relies on systemd to:

- Boot the operating system
- Start services
- Stop services
- Restart crashed applications
- Collect logs
- Manage dependencies
- Schedule tasks
- Control system state

If you've ever run:

```bash
sudo systemctl restart nginx
```

you've already used systemd.

______________________________________________________________________

# 2. What is a Service?

A **service** is a long-running background process that performs a specific function.

Examples:

- SSH server
- Nginx
- Docker
- Redis
- PostgreSQL
- Cron

Unlike interactive programs, services usually start automatically and continue running until the system shuts down.

______________________________________________________________________

## Examples

SSH

```
sshd
```

Docker

```
dockerd
```

Redis

```
redis-server
```

Nginx

```
nginx
```

______________________________________________________________________

# 3. What is systemd?

systemd is the first userspace process started by the Linux kernel.

Its Process ID (PID) is usually:

```text
1
```

Verify:

```bash
ps -p 1
```

Example output:

```text
PID TTY      TIME CMD
1   ?        0:03 systemd
```

systemd becomes the parent of most other processes.

______________________________________________________________________

# Responsibilities of systemd

- System initialization
- Service management
- Dependency resolution
- Logging
- Device management
- Socket activation
- Timers
- Mount management

______________________________________________________________________

# 4. Why systemd Replaced init

Older Linux systems used **SysV init**.

Problems with SysV init:

- Sequential startup
- Slower boot times
- Limited dependency management
- More difficult configuration

systemd introduced:

- Parallel startup
- Faster boot
- Better dependency handling
- Improved logging
- Unified management tools

______________________________________________________________________

# 5. Boot Process Overview

```
Power On

↓

BIOS / UEFI

↓

Bootloader (GRUB)

↓

Linux Kernel

↓

systemd (PID 1)

↓

System Services

↓

Login Screen / Terminal
```

______________________________________________________________________

# 6. systemd Units

systemd manages different resource types using **unit files**.

Common unit types:

| Extension | Purpose |
|-----------|----------|
| .service | Services |
| .target | System state |
| .socket | Socket activation |
| .mount | Mounted filesystems |
| .timer | Scheduled tasks |
| .path | File monitoring |
| .device | Devices |

The most frequently used unit type is:

```
.service
```

______________________________________________________________________

# View Unit Files

```bash
systemctl list-unit-files
```

______________________________________________________________________

View Active Units

```bash
systemctl list-units
```

______________________________________________________________________

# 7. The `systemctl` Command

`systemctl` is the primary command for interacting with systemd.

Basic syntax:

```bash
systemctl COMMAND SERVICE
```

Example:

```bash
sudo systemctl status nginx
```

______________________________________________________________________

# 8. Managing Services

## Start a Service

```bash
sudo systemctl start nginx
```

______________________________________________________________________

## Stop a Service

```bash
sudo systemctl stop nginx
```

______________________________________________________________________

## Restart a Service

```bash
sudo systemctl restart nginx
```

______________________________________________________________________

## Reload Configuration

```bash
sudo systemctl reload nginx
```

Reload applies new configuration without completely restarting the service (if supported).

______________________________________________________________________

## Reload or Restart

```bash
sudo systemctl reload-or-restart nginx
```

______________________________________________________________________

# 9. Service Status

Check service status.

```bash
systemctl status nginx
```

Example:

```text
Active: active (running)
```

Other common states:

- active
- inactive
- failed
- activating
- deactivating

______________________________________________________________________

Check whether a service is running.

```bash
systemctl is-active nginx
```

Output:

```text
active
```

______________________________________________________________________

Check whether a service is enabled.

```bash
systemctl is-enabled nginx
```

______________________________________________________________________

# 10. Enabling and Disabling Services

Start automatically during boot.

```bash
sudo systemctl enable nginx
```

______________________________________________________________________

Disable automatic startup.

```bash
sudo systemctl disable nginx
```

______________________________________________________________________

Enable and start immediately.

```bash
sudo systemctl enable --now nginx
```

______________________________________________________________________

Disable and stop immediately.

```bash
sudo systemctl disable --now nginx
```

______________________________________________________________________

# 11. Restarting and Reloading Services

Restart:

```bash
sudo systemctl restart ssh
```

Stops and starts the service.

Connections may be interrupted.

______________________________________________________________________

Reload:

```bash
sudo systemctl reload ssh
```

Reloads configuration without restarting (if supported).

______________________________________________________________________

When to use each?

| Action | Use When |
|----------|----------|
| restart | Application must restart |
| reload | Configuration changed and the service supports reloading |

______________________________________________________________________

# 12. The `journalctl` Command

systemd includes a centralized logging system called the **journal**.

View all logs:

```bash
journalctl
```

______________________________________________________________________

Latest logs:

```bash
journalctl -n 50
```

______________________________________________________________________

Follow logs in real time.

```bash
journalctl -f
```

Equivalent to:

```bash
tail -f
```

for the journal.

______________________________________________________________________

Logs for one service.

```bash
journalctl -u nginx
```

______________________________________________________________________

Follow logs for one service.

```bash
journalctl -fu nginx
```

______________________________________________________________________

Today's logs.

```bash
journalctl --since today
```

______________________________________________________________________

Logs from the last hour.

```bash
journalctl --since "1 hour ago"
```

______________________________________________________________________

Errors only.

```bash
journalctl -p err
```

______________________________________________________________________

Current boot.

```bash
journalctl -b
```

______________________________________________________________________

Previous boot.

```bash
journalctl -b -1
```

Useful after a reboot caused by a crash.

______________________________________________________________________

# 13. Targets in systemd

Targets replace traditional runlevels.

Common targets:

| Target | Purpose |
|----------|----------|
| multi-user.target | Multi-user command-line mode |
| graphical.target | Desktop environment |
| rescue.target | Recovery mode |
| emergency.target | Emergency shell |

______________________________________________________________________

View current target.

```bash
systemctl get-default
```

______________________________________________________________________

Change default target.

```bash
sudo systemctl set-default multi-user.target
```

______________________________________________________________________

# 14. Creating a Custom Service

Example service file:

```ini
[Unit]
Description=FastAPI Application
After=network.target

[Service]
User=riyaz
WorkingDirectory=/home/riyaz/app
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Save as:

```text
/etc/systemd/system/myapp.service
```

______________________________________________________________________

Reload systemd configuration.

```bash
sudo systemctl daemon-reload
```

______________________________________________________________________

Enable service.

```bash
sudo systemctl enable myapp
```

______________________________________________________________________

Start service.

```bash
sudo systemctl start myapp
```

______________________________________________________________________

View logs.

```bash
journalctl -u myapp
```

______________________________________________________________________

# 15. Production Examples

## Restart Nginx

```bash
sudo systemctl restart nginx
```

______________________________________________________________________

## View Docker Logs

```bash
journalctl -u docker
```

______________________________________________________________________

## Enable Redis at Boot

```bash
sudo systemctl enable redis
```

______________________________________________________________________

## Follow FastAPI Logs

```bash
journalctl -fu myapp
```

______________________________________________________________________

## Reload Nginx Configuration

```bash
sudo systemctl reload nginx
```

______________________________________________________________________

## Check Failed Services

```bash
systemctl --failed
```

______________________________________________________________________

# 16. Common Mistakes

❌ Editing a service file without running:

```bash
systemctl daemon-reload
```

______________________________________________________________________

❌ Using `restart` when `reload` would be sufficient.

______________________________________________________________________

❌ Forgetting to enable a service after installing it.

______________________________________________________________________

❌ Ignoring `journalctl` during troubleshooting.

______________________________________________________________________

❌ Modifying system service files directly instead of creating override files when appropriate.

______________________________________________________________________

# 17. Best Practices

- Prefer `reload` when supported.
- Check service status after configuration changes.
- Use `journalctl` instead of searching multiple log files.
- Enable only services that are actually required.
- Create dedicated systemd service files for custom backend applications.

______________________________________________________________________

# Interview Questions

## Q1. What is systemd?

**Answer**

systemd is the initialization and service management system used by most modern Linux distributions. It starts during
boot as PID 1 and manages services, system state, logging, timers, and dependencies.

______________________________________________________________________

## Q2. What is the difference between `start`, `restart`, and `reload`?

**Answer**

- `start` launches a stopped service.
- `restart` stops and starts the service again.
- `reload` instructs the running service to reload its configuration without restarting, if supported.

______________________________________________________________________

## Q3. Why is `systemctl daemon-reload` required?

**Answer**

It instructs systemd to reload unit file definitions after new or modified service files have been added. Without it,
systemd continues using its cached configuration.

______________________________________________________________________

## Q4. What is `journalctl`?

**Answer**

`journalctl` is the command-line interface for viewing logs stored by the systemd journal. It supports filtering by
service, boot session, priority, and time.

______________________________________________________________________

## Q5. What is the difference between enabling and starting a service?

**Answer**

Starting a service launches it immediately. Enabling a service configures it to start automatically during future system
boots.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Display:

```bash
systemctl list-units
```

______________________________________________________________________

## Exercise 2

Check the status of:

- SSH
- Docker
- Cron

(or any services available on your system).

______________________________________________________________________

## Exercise 3

Enable and disable a service.

Observe the difference.

______________________________________________________________________

## Exercise 4

Display logs for a service using:

```bash
journalctl -u
```

______________________________________________________________________

## Exercise 5

Create a simple custom systemd service that runs a shell script.

______________________________________________________________________

## Exercise 6

View:

- Current boot logs
- Previous boot logs
- Error logs

using `journalctl`.

______________________________________________________________________

# Cheat Sheet

## Service Management

```bash
systemctl start
systemctl stop
systemctl restart
systemctl reload
systemctl status
```

______________________________________________________________________

## Boot Configuration

```bash
systemctl enable
systemctl disable
systemctl daemon-reload
```

______________________________________________________________________

## Logs

```bash
journalctl
journalctl -u
journalctl -f
journalctl -b
journalctl -p err
```

______________________________________________________________________

## Information

```bash
systemctl list-units
systemctl list-unit-files
systemctl --failed
systemctl get-default
```

______________________________________________________________________

# Summary

In this chapter, you learned how systemd manages the Linux boot process and long-running services, how to control
services using `systemctl`, how to inspect logs with `journalctl`, how systemd unit files work, and how to create and
manage your own services. These are essential skills for deploying, operating, and troubleshooting backend applications
on modern Linux systems.

______________________________________________________________________

## Next

[Linux Networking](16-linux-networking.md)

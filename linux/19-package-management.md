# Linux Complete Interview & Production Course

# File 19 — Package Management

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** System Administration
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 18 — Disk Management and Filesystems

______________________________________________________________________

# Table of Contents

1. Introduction
1. What is a Package?
1. Why Package Managers Exist
1. Package Formats
1. Package Repositories
1. Debian-Based Package Management
1. RHEL-Based Package Management
1. Package Information Commands
1. Installing Packages
1. Removing Packages
1. Updating Packages
1. Searching Packages
1. Repository Management
1. Offline Package Installation
1. Snap Packages
1. Flatpak Packages
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

Every Linux system requires software.

Examples:

- Python
- Docker
- Git
- Nginx
- PostgreSQL
- Redis
- Node.js

Installing software manually by downloading source code, resolving dependencies, compiling, and configuring everything
is time-consuming and error-prone.

Linux solves this problem using **package managers**.

A package manager:

- Downloads software
- Resolves dependencies
- Verifies packages
- Installs software
- Updates software
- Removes software

______________________________________________________________________

# 2. What is a Package?

A package is a bundled collection of:

- Executable programs
- Libraries
- Configuration files
- Documentation
- Metadata

Think of it as an installer for Linux software.

Example:

```
nginx

↓

Package

↓

Installed Application
```

______________________________________________________________________

# 3. Why Package Managers Exist

Without package managers:

- Download source code
- Compile manually
- Resolve dependencies
- Install libraries
- Track versions yourself

With package managers:

```bash
sudo apt install nginx
```

Everything happens automatically.

______________________________________________________________________

# 4. Package Formats

Different Linux distributions use different package formats.

| Distribution | Package Format |
|--------------|----------------|
| Ubuntu | `.deb` |
| Debian | `.deb` |
| Linux Mint | `.deb` |
| CentOS | `.rpm` |
| Fedora | `.rpm` |
| RHEL | `.rpm` |

______________________________________________________________________

# Common Package Managers

| Manager | Distribution |
|----------|--------------|
| apt | Ubuntu/Debian |
| dpkg | Ubuntu/Debian |
| yum | Older RHEL/CentOS |
| dnf | Fedora/RHEL |
| rpm | RPM-based systems |

______________________________________________________________________

# 5. Package Repositories

Repositories are online servers containing software packages.

Example:

```
Local Machine

↓

APT

↓

Ubuntu Repository

↓

Download Package
```

Repositories provide:

- Verified packages
- Dependency resolution
- Updates
- Security patches

______________________________________________________________________

# 6. Debian-Based Package Management

## Update Repository Metadata

```bash
sudo apt update
```

Downloads the latest package information.

______________________________________________________________________

## Upgrade Installed Packages

```bash
sudo apt upgrade
```

Updates installed packages.

______________________________________________________________________

Full upgrade:

```bash
sudo apt full-upgrade
```

May remove packages if necessary to complete upgrades.

______________________________________________________________________

## Install Package

```bash
sudo apt install nginx
```

______________________________________________________________________

Install multiple packages:

```bash
sudo apt install git curl vim
```

______________________________________________________________________

Reinstall package:

```bash
sudo apt install --reinstall nginx
```

______________________________________________________________________

# 7. RHEL-Based Package Management

Older systems:

```bash
sudo yum install nginx
```

______________________________________________________________________

Modern systems:

```bash
sudo dnf install nginx
```

______________________________________________________________________

Update packages:

```bash
sudo dnf update
```

______________________________________________________________________

Remove:

```bash
sudo dnf remove nginx
```

______________________________________________________________________

# 8. Package Information Commands

Search:

```bash
apt search nginx
```

______________________________________________________________________

Show details:

```bash
apt show nginx
```

______________________________________________________________________

Installed packages:

```bash
apt list --installed
```

______________________________________________________________________

Installed package version:

```bash
dpkg -l nginx
```

______________________________________________________________________

Find package owning a file:

```bash
dpkg -S /usr/bin/python3
```

______________________________________________________________________

RPM equivalent:

```bash
rpm -q nginx
```

______________________________________________________________________

# 9. Installing Packages

Ubuntu:

```bash
sudo apt install docker.io
```

______________________________________________________________________

Specific version:

```bash
sudo apt install nginx=1.18.0
```

(if available)

______________________________________________________________________

Install without confirmation:

```bash
sudo apt install -y nginx
```

Useful in automation scripts.

______________________________________________________________________

# 10. Removing Packages

Remove package:

```bash
sudo apt remove nginx
```

______________________________________________________________________

Remove configuration files:

```bash
sudo apt purge nginx
```

______________________________________________________________________

Remove unused dependencies:

```bash
sudo apt autoremove
```

______________________________________________________________________

Clean downloaded package cache:

```bash
sudo apt clean
```

______________________________________________________________________

# 11. Updating Packages

Refresh package metadata:

```bash
sudo apt update
```

______________________________________________________________________

Upgrade installed packages:

```bash
sudo apt upgrade
```

______________________________________________________________________

List upgradable packages:

```bash
apt list --upgradable
```

______________________________________________________________________

Security updates are often delivered through normal package updates.

______________________________________________________________________

# 12. Searching Packages

Search by keyword:

```bash
apt search redis
```

______________________________________________________________________

Search executable:

```bash
which python3
```

______________________________________________________________________

Locate installed file:

```bash
dpkg -S /usr/bin/git
```

______________________________________________________________________

RPM:

```bash
rpm -ql nginx
```

List files installed by the package.

______________________________________________________________________

# 13. Repository Management

Repository configuration:

Ubuntu:

```text
/etc/apt/sources.list
```

Additional repositories:

```text
/etc/apt/sources.list.d/
```

______________________________________________________________________

Refresh after adding repositories:

```bash
sudo apt update
```

______________________________________________________________________

# 14. Offline Package Installation

Install `.deb` file:

```bash
sudo dpkg -i package.deb
```

If dependencies are missing:

```bash
sudo apt -f install
```

______________________________________________________________________

Install `.rpm` file:

```bash
sudo rpm -ivh package.rpm
```

or

```bash
sudo dnf install package.rpm
```

______________________________________________________________________

# 15. Snap Packages

Snap is a universal package format.

Install:

```bash
sudo snap install code
```

______________________________________________________________________

List:

```bash
snap list
```

______________________________________________________________________

Remove:

```bash
sudo snap remove code
```

______________________________________________________________________

Advantages:

- Sandboxed
- Automatic updates
- Cross-distribution compatibility

______________________________________________________________________

# 16. Flatpak Packages

Another universal package system.

Install package:

```bash
flatpak install flathub org.gimp.GIMP
```

______________________________________________________________________

Run:

```bash
flatpak run org.gimp.GIMP
```

______________________________________________________________________

List:

```bash
flatpak list
```

______________________________________________________________________

Remove:

```bash
flatpak uninstall org.gimp.GIMP
```

______________________________________________________________________

# 17. Production Examples

## Install Git

```bash
sudo apt install git
```

______________________________________________________________________

## Update Server

```bash
sudo apt update
sudo apt upgrade
```

______________________________________________________________________

## Install Docker

```bash
sudo apt install docker.io
```

______________________________________________________________________

## Remove Unused Packages

```bash
sudo apt autoremove
```

______________________________________________________________________

## Install a Local Package

```bash
sudo dpkg -i app.deb
```

______________________________________________________________________

## List Installed Packages

```bash
apt list --installed
```

______________________________________________________________________

# 18. Common Mistakes

❌ Running `apt upgrade` without first running `apt update`.

______________________________________________________________________

❌ Installing packages from untrusted repositories.

______________________________________________________________________

❌ Forgetting to remove unused dependencies.

______________________________________________________________________

❌ Using `dpkg -i` without resolving missing dependencies.

______________________________________________________________________

❌ Mixing package managers unnecessarily.

Example:

Installing the same software using both `apt` and `snap`.

______________________________________________________________________

# 19. Best Practices

- Update repository metadata before upgrading packages.
- Install software from trusted repositories.
- Remove unused packages regularly.
- Use package managers instead of compiling manually unless necessary.
- Prefer automation-friendly commands in scripts.

______________________________________________________________________

# Interview Questions

## Q1. What is the difference between `apt update` and `apt upgrade`?

**Answer**

`apt update` refreshes the local package index by downloading the latest package metadata from repositories. `apt
upgrade` installs newer versions of already installed packages based on that updated metadata.

______________________________________________________________________

## Q2. What is the difference between `apt remove` and `apt purge`?

**Answer**

`apt remove` uninstalls the package but generally leaves configuration files behind. `apt purge` removes both the
package and its associated configuration files.

______________________________________________________________________

## Q3. Why are package repositories important?

**Answer**

Repositories provide trusted software packages, dependency management, version tracking, updates, and security patches,
simplifying software installation and maintenance.

______________________________________________________________________

## Q4. What is the purpose of `dpkg`?

**Answer**

`dpkg` is the low-level package management tool for Debian-based systems. It installs, removes, and queries `.deb`
packages but does not automatically resolve dependencies.

______________________________________________________________________

## Q5. What are Snap and Flatpak?

**Answer**

Snap and Flatpak are universal package formats that allow applications to be installed across multiple Linux
distributions, often using sandboxing for improved isolation and simplified distribution.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Update package metadata.

______________________________________________________________________

## Exercise 2

Install:

- Git
- Curl
- Vim

using your distribution's package manager.

______________________________________________________________________

## Exercise 3

Search for:

- Docker
- Redis
- PostgreSQL

without installing them.

______________________________________________________________________

## Exercise 4

Display information for an installed package.

______________________________________________________________________

## Exercise 5

Install a local `.deb` or `.rpm` package inside a virtual machine.

______________________________________________________________________

## Exercise 6

List every installed package on your system.

______________________________________________________________________

# Cheat Sheet

## APT

```bash
apt update
apt upgrade
apt install
apt remove
apt purge
apt autoremove
apt search
apt show
```

______________________________________________________________________

## DPKG

```bash
dpkg -i
dpkg -l
dpkg -S
```

______________________________________________________________________

## DNF / YUM

```bash
dnf install
dnf remove
dnf update

yum install
yum remove
```

______________________________________________________________________

## Universal Packages

```bash
snap
flatpak
```

______________________________________________________________________

# Summary

In this chapter, you learned how Linux package managers simplify software installation, updates, and maintenance. You
explored package formats, repositories, APT, DPKG, DNF, YUM, Snap, and Flatpak, along with common package management
workflows, repository configuration, and offline installation techniques. These are essential skills for maintaining
Linux servers and deploying backend applications.

______________________________________________________________________

## Next

[Scheduling Tasks with Cron and At](20-scheduling-tasks-with-cron-and-at.md)

# Linux Complete Interview & Production Course

# File 18 — Disk Management and Filesystems

> **Course:** Linux Complete Interview & Production Course
>
> **Module:** Storage Management
>
> **Level:** Beginner → Senior Backend Engineer
>
> **Prerequisites:** File 17 — SSH and Remote Administration

______________________________________________________________________

# Table of Contents

1. Introduction
1. What is a Storage Device?
1. Understanding Linux Filesystems
1. Block Devices vs Character Devices
1. Partitions
1. Mounting and Unmounting
1. The Linux Directory Hierarchy
1. Viewing Disk Information
1. The `df` Command
1. The `du` Command
1. The `lsblk` Command
1. The `blkid` Command
1. The `fdisk` Command
1. The `mount` Command
1. The `umount` Command
1. The `/etc/fstab` File
1. Swap Space
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

Every Linux system stores data on storage devices such as:

- SSDs
- HDDs
- NVMe drives
- USB drives
- SAN storage
- Cloud volumes (AWS EBS, Azure Managed Disks, GCP Persistent Disks)

Linux organizes these devices into partitions and filesystems so that applications can store and retrieve data
efficiently.

Understanding storage is essential for backend engineers because databases, logs, backups, Docker volumes, and
application data all depend on reliable disk management.

______________________________________________________________________

# 2. What is a Storage Device?

A storage device is hardware used to permanently store data.

Examples:

| Device | Description |
|---------|-------------|
| HDD | Mechanical hard disk |
| SSD | Solid-state drive |
| NVMe SSD | High-speed PCIe storage |
| USB Drive | Removable storage |
| Network Storage | Remote storage over a network |

Linux represents storage devices as files under:

```text
/dev
```

Examples:

```text
/dev/sda
/dev/sdb
/dev/nvme0n1
```

______________________________________________________________________

# 3. Understanding Linux Filesystems

A filesystem defines how files and directories are organized and stored on a storage device.

Common Linux filesystems:

| Filesystem | Description |
|------------|-------------|
| ext4 | Default for many Linux distributions |
| XFS | High-performance filesystem |
| Btrfs | Snapshot and advanced features |
| FAT32 | Cross-platform compatibility |
| exFAT | Large removable media |
| NTFS | Windows filesystem |

______________________________________________________________________

## Why is a Filesystem Required?

Without a filesystem:

```
Disk

↓

Raw Bytes

↓

No Files

No Directories

No Metadata
```

The filesystem provides:

- File names
- Directories
- Permissions
- Metadata
- Free space management

______________________________________________________________________

# 4. Block Devices vs Character Devices

Linux classifies devices into two main types.

## Block Devices

Transfer data in fixed-size blocks.

Examples:

- Hard drives
- SSDs
- USB drives

Examples in Linux:

```text
/dev/sda
/dev/nvme0n1
```

______________________________________________________________________

## Character Devices

Transfer data one character or byte at a time.

Examples:

- Keyboard
- Mouse
- Serial ports

Examples:

```text
/dev/tty
/dev/null
```

______________________________________________________________________

View device type:

```bash
ls -l /dev
```

______________________________________________________________________

# 5. Partitions

A partition divides a physical disk into logical sections.

Example:

```
Disk

↓

Partition 1

↓

Partition 2

↓

Partition 3
```

Linux names partitions like:

```text
/dev/sda1
/dev/sda2
/dev/sda3
```

NVMe devices:

```text
/dev/nvme0n1p1
```

Each partition can contain a different filesystem.

______________________________________________________________________

# 6. Mounting and Unmounting

Linux does not assign drive letters (like `C:` or `D:`).

Instead, filesystems are attached to the directory tree.

Example:

```
Disk

↓

Filesystem

↓

Mount Point

↓

/mnt/data
```

______________________________________________________________________

Mount a filesystem:

```bash
sudo mount /dev/sdb1 /mnt/data
```

______________________________________________________________________

Unmount:

```bash
sudo umount /mnt/data
```

or

```bash
sudo umount /dev/sdb1
```

______________________________________________________________________

View mounted filesystems:

```bash
mount
```

or

```bash
findmnt
```

______________________________________________________________________

# 7. The Linux Directory Hierarchy

Important directories:

| Directory | Purpose |
|------------|----------|
| / | Root filesystem |
| /home | User home directories |
| /var | Variable data (logs, databases) |
| /tmp | Temporary files |
| /boot | Bootloader and kernel |
| /etc | Configuration files |
| /usr | User applications |
| /opt | Optional software |
| /mnt | Temporary mounts |
| /media | Removable media |

Understanding mount points is easier when you understand the directory hierarchy.

______________________________________________________________________

# 8. Viewing Disk Information

Display block devices:

```bash
lsblk
```

Example:

```text
NAME
sda
├── sda1
└── sda2
```

______________________________________________________________________

Display filesystem usage:

```bash
df -h
```

______________________________________________________________________

Display partition information:

```bash
blkid
```

______________________________________________________________________

# 9. The `df` Command

Displays filesystem usage.

Human-readable format:

```bash
df -h
```

Output:

```text
Filesystem      Size Used Avail Use%
```

______________________________________________________________________

Display filesystem type:

```bash
df -Th
```

______________________________________________________________________

Show specific mount point:

```bash
df -h /
```

______________________________________________________________________

# 10. The `du` Command

Shows disk usage for files and directories.

Directory size:

```bash
du -sh project
```

______________________________________________________________________

Current directory:

```bash
du -sh .
```

______________________________________________________________________

Largest directories:

```bash
du -h . | sort -h
```

______________________________________________________________________

Top-level directories:

```bash
du -sh *
```

______________________________________________________________________

# Difference Between `df` and `du`

| Command | Measures |
|----------|----------|
| `df` | Filesystem usage |
| `du` | File and directory usage |

______________________________________________________________________

# 11. The `lsblk` Command

Display storage devices:

```bash
lsblk
```

Useful options:

Filesystem information:

```bash
lsblk -f
```

______________________________________________________________________

Sizes:

```bash
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT
```

______________________________________________________________________

Tree view:

```bash
lsblk
```

shows relationships between disks and partitions.

______________________________________________________________________

# 12. The `blkid` Command

Display UUIDs and filesystem types.

```bash
sudo blkid
```

Example:

```text
/dev/sda1 UUID="..."
TYPE="ext4"
```

UUIDs are commonly used in:

```text
/etc/fstab
```

because they remain stable even if device names change.

______________________________________________________________________

# 13. The `fdisk` Command

Manage partition tables.

List disks:

```bash
sudo fdisk -l
```

Interactive mode:

```bash
sudo fdisk /dev/sdb
```

Common operations:

- Create partition
- Delete partition
- Change partition type
- Write partition table

Be cautious—incorrect changes can result in data loss.

______________________________________________________________________

# 14. The `mount` Command

Mount a filesystem:

```bash
sudo mount /dev/sdb1 /mnt/data
```

______________________________________________________________________

Mount read-only:

```bash
sudo mount -o ro /dev/sdb1 /mnt/data
```

______________________________________________________________________

Specify filesystem type:

```bash
sudo mount -t ext4 /dev/sdb1 /mnt/data
```

______________________________________________________________________

# 15. The `umount` Command

Unmount a filesystem.

```bash
sudo umount /mnt/data
```

______________________________________________________________________

If the device is busy:

```text
target is busy
```

Find open files:

```bash
lsof /mnt/data
```

or

```bash
fuser -m /mnt/data
```

______________________________________________________________________

# 16. The `/etc/fstab` File

`/etc/fstab` defines filesystems that should be mounted automatically during boot.

Example:

```text
UUID=xxxx-xxxx /data ext4 defaults 0 2
```

Fields:

| Field | Description |
|--------|-------------|
| Device/UUID | Filesystem identifier |
| Mount Point | Directory |
| Filesystem | ext4, xfs, etc. |
| Mount Options | defaults, ro, noexec, etc. |
| Dump | Backup flag |
| Pass | Filesystem check order |

______________________________________________________________________

Test configuration:

```bash
sudo mount -a
```

Always test after editing `fstab`.

______________________________________________________________________

# 17. Swap Space

Swap is disk space used as an extension of RAM.

When physical memory becomes full:

```
RAM

↓

Swap
```

Swap is slower than RAM but helps prevent applications from crashing due to memory exhaustion.

______________________________________________________________________

View swap:

```bash
swapon --show
```

______________________________________________________________________

Memory usage:

```bash
free -h
```

______________________________________________________________________

Disable swap:

```bash
sudo swapoff -a
```

______________________________________________________________________

Enable swap:

```bash
sudo swapon -a
```

______________________________________________________________________

# 18. Production Examples

## Check Disk Space

```bash
df -h
```

______________________________________________________________________

## Find Large Directories

```bash
du -sh *
```

______________________________________________________________________

## Display Mounted Filesystems

```bash
findmnt
```

______________________________________________________________________

## Mount a New Volume

```bash
sudo mount /dev/xvdf1 /data
```

______________________________________________________________________

## Verify Filesystem UUID

```bash
blkid
```

______________________________________________________________________

## Configure Automatic Mount

Edit:

```text
/etc/fstab
```

Then verify:

```bash
sudo mount -a
```

______________________________________________________________________

# 19. Common Mistakes

❌ Editing `/etc/fstab` without testing it.

______________________________________________________________________

❌ Confusing `df` with `du`.

______________________________________________________________________

❌ Removing a mounted USB drive without unmounting it.

______________________________________________________________________

❌ Mounting a filesystem to a non-empty directory without understanding that the existing contents become hidden while
the filesystem is mounted.

______________________________________________________________________

❌ Assuming `/dev/sdb` will always refer to the same disk after a reboot.

______________________________________________________________________

# 20. Best Practices

- Use UUIDs instead of device names in `/etc/fstab`.
- Test `fstab` changes with `mount -a`.
- Monitor disk usage regularly.
- Keep sufficient free space for logs and databases.
- Unmount removable media before disconnecting it.

______________________________________________________________________

# Interview Questions

## Q1. What is the difference between `df` and `du`?

**Answer**

`df` reports filesystem-level disk usage, including total, used, and available space. `du` calculates the disk usage of
individual files and directories.

______________________________________________________________________

## Q2. Why are UUIDs preferred over device names in `/etc/fstab`?

**Answer**

Device names such as `/dev/sdb1` can change after hardware changes or reboots. UUIDs uniquely identify a filesystem and
remain consistent, making automatic mounts more reliable.

______________________________________________________________________

## Q3. What happens when you mount a filesystem on a non-empty directory?

**Answer**

The contents of the mount point become temporarily hidden until the mounted filesystem is unmounted. The original files
are not deleted.

______________________________________________________________________

## Q4. What is swap space?

**Answer**

Swap is disk space used as virtual memory when physical RAM is exhausted. It provides additional memory capacity but is
significantly slower than RAM.

______________________________________________________________________

## Q5. Why should `mount -a` be run after editing `/etc/fstab`?

**Answer**

`mount -a` attempts to mount all filesystems defined in `fstab` without rebooting, allowing configuration errors to be
detected and corrected immediately.

______________________________________________________________________

# Practice Exercises

## Exercise 1

Display:

- Disk usage
- Filesystem types
- Mounted filesystems

using:

```bash
df
lsblk
findmnt
```

______________________________________________________________________

## Exercise 2

Determine the size of:

- Your home directory
- `/var`
- `/tmp`

using `du`.

______________________________________________________________________

## Exercise 3

List all storage devices and identify:

- Device name
- Filesystem
- Mount point

______________________________________________________________________

## Exercise 4

View UUIDs for all mounted filesystems.

______________________________________________________________________

## Exercise 5

Mount and unmount a removable storage device (or a loopback device in a virtual machine).

______________________________________________________________________

## Exercise 6

Inspect your system's:

```text
/etc/fstab
```

and identify each configured filesystem.

______________________________________________________________________

# Cheat Sheet

## Disk Usage

```bash
df -h
df -Th
du -sh
```

______________________________________________________________________

## Storage Devices

```bash
lsblk
lsblk -f
blkid
fdisk -l
```

______________________________________________________________________

## Mounting

```bash
mount
umount
findmnt
```

______________________________________________________________________

## Swap

```bash
free -h
swapon --show
swapoff
swapon
```

______________________________________________________________________

## Configuration

```text
/etc/fstab
```

______________________________________________________________________

# Summary

In this chapter, you learned how Linux manages storage devices, partitions, and filesystems, how to inspect disks using
`df`, `du`, `lsblk`, and `blkid`, how mounting works, how to configure automatic mounts with `/etc/fstab`, and how swap
space extends available memory. These concepts are fundamental for managing servers, databases, containers, and
persistent storage in production environments.

______________________________________________________________________

## Next

[Package Management](19-package-management.md)

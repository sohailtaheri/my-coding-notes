# 02 — Operating System Services

## Overview

An OS provides a set of services to make running programs easier and safer. These services fall into two groups:

1. **Services that help the user** (convenience-focused)
2. **Services that keep the system efficient** (resource management)

---

## Group 1 — Services for the User / Programs

### Program Execution
The OS loads a program into memory, runs it, and terminates it normally or on error. Without this, every program would need to bootstrap itself.

### I/O Operations
Programs rarely access hardware directly. The OS provides a uniform interface — a program reads/writes "a file" and the OS handles whether that's a disk, terminal, or network socket.

### File System Manipulation
- Create, delete, read, write files and directories
- Search by name, list directory contents
- Manage permissions (who can read/write/execute)

### Inter-Process Communication (IPC)
Processes need to exchange data. The OS provides:

| Mechanism | How it works |
|---|---|
| Shared memory | Processes map the same memory region |
| Message passing | OS shuttles messages between processes (send/receive) |
| Pipes | Unidirectional byte stream between processes |
| Sockets | Network-capable bidirectional IPC |

### Error Detection
The OS constantly monitors for errors:
- Hardware errors (bad memory, power failure)
- I/O errors (disk read failure, network disconnect)
- Program errors (divide by zero, illegal memory access)

For each error the OS must take an appropriate action — terminate the offending process, return an error code, or try to recover.

---

## Group 2 — Services for System Efficiency

These are invisible to individual programs but critical for the system overall.

### Resource Allocation
When multiple users or processes run simultaneously the OS allocates:
- **CPU time** — via scheduling algorithms
- **Memory** — via allocation and paging/segmentation
- **I/O devices** — via device queues and drivers
- **Files** — via file system locks

### Accounting / Logging
The OS tracks which user uses how much CPU time, memory, and I/O. Used for billing on shared systems, auditing, and performance tuning.

### Protection and Security

**Protection** — controls access to system resources between concurrent processes:
- A process cannot read another process's memory (memory protection)
- Files have owner/group/other permissions

**Security** — defends against external threats:
- User authentication (passwords, biometrics)
- Defending against denial-of-service, malware, unauthorized network access

> Protection = internal policy enforcement. Security = defense against external attack.

---

## Summary Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        OS Services                               │
│                                                                  │
│  FOR USERS                        FOR SYSTEM                     │
│  ─────────────────────────        ──────────────────────────     │
│  • Program Execution              • Resource Allocation          │
│  • I/O Operations                 • Accounting / Logging         │
│  • File System Manipulation       • Protection & Security        │
│  • Inter-Process Communication                                   │
│  • Error Detection                                               │
└──────────────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

- OS services exist at two levels: helping individual programs and keeping the whole system running fairly.
- IPC is fundamental to modern multi-process and distributed applications.
- Protection and security are distinct but complementary responsibilities of the OS.

---

*Previous: [01 — Structure](01_structure_of_operating_system.md) | Next: [03 — User–OS Interface](03_user_os_interface.md)*

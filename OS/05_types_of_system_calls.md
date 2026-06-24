# 05 — Types of System Calls

System calls are grouped into six functional categories. Every OS provides these; the names differ but the concepts are universal.

---

## 1. Process Control

These calls manage the lifecycle of processes.

| Call (POSIX / Linux) | Windows equivalent | Purpose |
|---|---|---|
| `fork()` | `CreateProcess()` | Create a new (child) process |
| `exec()` | `CreateProcess()` | Replace current process image with a new program |
| `exit()` | `ExitProcess()` | Terminate the current process |
| `wait()` | `WaitForSingleObject()` | Wait for a child process to finish |
| `getpid()` | `GetCurrentProcessId()` | Get process ID |
| `abort()` | — | Terminate abnormally |

### Fork–Exec pattern (Unix)

```c
pid_t pid = fork();          // duplicate current process
if (pid == 0) {
    // child: replace with new program
    execv("/bin/ls", args);
} else {
    // parent: wait for child
    wait(NULL);
}
```

`fork()` copies the process; `exec()` loads a new binary into it. Together they implement "run a program."

---

## 2. File Management

Operations on files and their metadata.

| Call | Purpose |
|---|---|
| `open(path, flags)` | Open or create a file; returns a file descriptor |
| `close(fd)` | Release a file descriptor |
| `read(fd, buf, n)` | Read n bytes from fd into buf |
| `write(fd, buf, n)` | Write n bytes from buf to fd |
| `lseek(fd, offset, whence)` | Move the file offset (random access) |
| `unlink(path)` | Delete a file |
| `stat(path, &buf)` | Get file metadata (size, permissions, timestamps) |
| `chmod(path, mode)` | Change file permissions |
| `rename(old, new)` | Rename or move a file |

### File Descriptors

`open()` returns a small integer called a **file descriptor** (fd). The kernel maintains a table mapping each process's fds to open files. Standard descriptors:

| fd | Name | Default |
|---|---|---|
| 0 | stdin | keyboard |
| 1 | stdout | terminal |
| 2 | stderr | terminal |

---

## 3. Device Management

I/O devices are accessed through calls that look like file operations (Unix philosophy: "everything is a file").

| Call | Purpose |
|---|---|
| `ioctl(fd, request, ...)` | Device-specific control operations |
| `read()` / `write()` | Transfer data to/from device |
| `open()` / `close()` | Acquire / release device |
| `mmap(fd, ...)` | Map device memory into process address space |

**Examples:**
- Reading from `/dev/sda` reads a raw disk block
- Writing to `/dev/null` discards data
- `ioctl` on a terminal sets baud rate, echo mode, etc.

On Windows, device access uses `CreateFile()`, `DeviceIoControl()`, `ReadFile()`, `WriteFile()`.

---

## 4. Information Maintenance

Calls that get or set system-wide data.

| Call | Purpose |
|---|---|
| `getpid()` | Get current process ID |
| `getuid()` / `getgid()` | Get user/group ID |
| `time()` | Get current time |
| `gettimeofday()` | High-resolution time |
| `uname()` | Get OS name, version, architecture |
| `sysinfo()` | Get memory totals, uptime, load averages |
| `setuid()` / `setgid()` | Change process credentials |

These are lightweight — mostly reading kernel data structures without expensive I/O.

---

## 5. Communication (IPC)

Calls for exchanging data between processes, possibly on different machines.

### Message Passing

```
Process A                  Kernel                  Process B
   │                          │                          │
   │── send(pid_B, msg) ──→   │  ──── deliver ──→        │
   │                          │                          │
   │                          │  ←── receive(pid_A) ──── │
```

| Call | Purpose |
|---|---|
| `pipe(fds)` | Create an anonymous pipe (parent↔child) |
| `mkfifo(path)` | Create a named pipe (any two processes) |
| `socket()` | Create a network/IPC socket |
| `connect()` / `accept()` | Establish socket connection |
| `send()` / `recv()` | Send/receive over socket |
| `shmget()` / `shmat()` | Create / attach shared memory segment |
| `mq_open()` / `mq_send()` | POSIX message queue |
| `kill(pid, sig)` | Send a signal to a process |

### Shared Memory vs. Message Passing

| | Shared Memory | Message Passing |
|---|---|---|
| Speed | Faster (no copy) | Slower (copy to kernel buffer) |
| Complexity | Requires synchronization (mutex/semaphore) | Simpler — kernel handles ordering |
| Scale | Same machine | Same machine or across network |

---

## 6. Protection

Calls that control access to resources.

| Call | Purpose |
|---|---|
| `chmod(path, mode)` | Set file read/write/execute permissions |
| `chown(path, uid, gid)` | Change file owner |
| `umask(mask)` | Set default permission mask for new files |
| `setuid()` / `setgid()` | Change the effective user/group of a process |
| `chroot(path)` | Change root directory (sandbox a process) |
| `seccomp()` | Restrict which syscalls a process may make |
| `getfacl()` / `setfacl()` | Access Control Lists for fine-grained permissions |

---

## Quick-Reference Summary

```
┌─────────────────────────────────────────────────────────────────┐
│           Types of System Calls                                  │
├──────────────────────┬──────────────────────────────────────────┤
│ Process Control      │ fork, exec, exit, wait, kill             │
│ File Management      │ open, close, read, write, stat, unlink   │
│ Device Management    │ ioctl, read, write, mmap                 │
│ Information Maint.   │ getpid, time, uname, sysinfo             │
│ Communication (IPC)  │ pipe, socket, shmget, send, recv         │
│ Protection           │ chmod, chown, setuid, seccomp            │
└──────────────────────┴──────────────────────────────────────────┘
```

---

## Key Takeaways

- The six categories cover everything a process can ask the OS to do.
- File and device management share the same interface in Unix ("everything is a file").
- IPC calls span from simple pipes to full network sockets.
- Protection calls are how the OS enforces the security policy defined by administrators.

---

*Previous: [04 — System Calls](04_system_calls.md) | Next: [06 — System Programs](06_system_programs.md)*

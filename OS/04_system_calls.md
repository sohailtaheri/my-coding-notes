# 04 — System Calls

## What Is a System Call?

A **system call** (syscall) is the programmatic interface through which a user-space process requests a service from the OS kernel.

> Think of a system call as the *only legal doorway* between user mode and kernel mode.

When a process needs to read a file, create a new process, or allocate memory it cannot do so directly (hardware protection prevents it). Instead it issues a system call, which:

1. Switches the CPU from **user mode → kernel mode**
2. Executes the requested kernel routine
3. Returns the result and switches back to **kernel mode → user mode**

---

## The Mode Switch in Detail

```
User Process
    │
    │  calls open("file.txt", O_RDONLY)
    │
    ▼
C Library (libc) wrapper
    │  places syscall number in a register (e.g., rax = 2 on Linux x86-64)
    │  places arguments in registers (rdi, rsi, rdx, ...)
    │  executes SYSCALL instruction  ◄── triggers hardware trap
    │
    ▼ ────────────────────────── kernel mode boundary ──────────────────────
Kernel Trap Handler
    │  saves user-mode register state
    │  looks up syscall number in syscall table
    │  dispatches to sys_open()
    │
    ▼
sys_open() executes
    │  validates path, checks permissions, finds inode, returns file descriptor
    │
    ▼
Return to user mode
    │  restores user-mode registers, places return value in rax
    │
    ▼
User Process resumes
    │  fd = return value from rax
```

---

## Syscall Numbers

Every system call has a unique integer ID. The C library wrapper puts this number in a register before executing the trap instruction. The kernel's dispatch table maps numbers to handler functions.

**Linux x86-64 examples:**

| Number | Name | Description |
|---|---|---|
| 0 | `read` | Read from file descriptor |
| 1 | `write` | Write to file descriptor |
| 2 | `open` | Open a file |
| 3 | `close` | Close a file descriptor |
| 57 | `fork` | Create a child process |
| 59 | `execve` | Execute a program |
| 60 | `exit` | Terminate process |

Numbers differ by OS and architecture — this is why binaries aren't portable between Linux and Windows.

---

## API vs. System Call

Programmers rarely invoke syscalls directly. They call **API functions** in the C standard library (POSIX on Unix, Win32 on Windows) which wrap the raw syscalls:

```
Your Code:    fopen("data.csv", "r")
              ↓
libc:         open("data.csv", O_RDONLY)    ← POSIX API
              ↓
Kernel:       sys_open(...)                 ← actual syscall
```

Benefits of using the API instead of raw syscalls:
- Portability across OS versions
- Easier calling convention (regular function call vs. register manipulation)
- Buffering, error handling, and convenience built in

---

## Parameter Passing

Three methods for passing parameters to the kernel:

| Method | How | Used when |
|---|---|---|
| Registers | Put params in CPU registers | Few, small parameters |
| Block / Table | Put params in a memory block; pass its address in one register | More or larger parameters |
| Stack | Push params onto the process stack; kernel reads them | Variable number of parameters |

Linux primarily uses registers (up to 6 on x86-64: rdi, rsi, rdx, r10, r8, r9).

---

## Cost of a System Call

A syscall is expensive relative to a normal function call because it involves:

- A hardware trap (pipeline flush)
- Context save/restore
- Kernel address space switch (TLB flush on some architectures)
- The actual kernel work
- Return trip

This is why high-performance code minimizes syscalls — e.g., `stdio` buffers writes and flushes in batches rather than calling `write()` for every character.

---

## Key Takeaways

- System calls are the only sanctioned entry points from user space into the kernel.
- Each call triggers a hardware-enforced mode switch.
- Programmers use API libraries (libc, Win32) rather than raw syscalls for portability.
- Syscalls have measurable overhead; good software minimizes unnecessary calls.

---

*Previous: [03 — User–OS Interface](03_user_os_interface.md) | Next: [05 — Types of System Calls](05_types_of_system_calls.md)*

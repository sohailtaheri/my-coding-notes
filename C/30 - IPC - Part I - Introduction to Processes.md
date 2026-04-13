
## What Is a Process?

A **process** is an independent program in execution. When you run a compiled C program, the operating system creates a process for it. Each process has its own:

- **Virtual address space** (code, stack, heap, data segments)
- **File descriptors**
- **Process ID (PID)**
- **Signal handlers**
- **Environment variables**

Processes are managed by the OS kernel, which schedules them on the CPU and enforces isolation between them.

---

## Processes vs Threads

Threads and processes are both units of concurrency, but they differ fundamentally in how they relate to memory and resources.

| Feature | Process | Thread |
|---|---|---|
| Memory space | **Separate** — each process has its own virtual memory | **Shared** — all threads in a process share the same memory |
| Creation cost | Higher (full copy of address space) | Lower (just a new stack + context) |
| Isolation | Strong — one crash rarely affects others | Weak — a bug in one thread can corrupt the whole process |
| Communication | Requires IPC (pipes, sockets, shared memory…) | Direct — via shared variables (with synchronization) |
| Context switch | Slower (TLB flush, full context save) | Faster (within the same address space) |
| Data sharing | Not by default — must be explicit | By default — must be protected with mutexes/locks |
| POSIX API | `fork()`, `exec()`, `wait()` | `pthread_create()`, `pthread_join()` |

### Key insight

Use **processes** when you need strong isolation (e.g., a crashed child shouldn't take down the parent). Use **threads** when you need low-latency sharing of data within a single program.

---

## Creating a Process — `fork()`

The primary way to create a new process in C is with `fork()`, declared in `<unistd.h>`.

```c
#include <unistd.h>

pid_t fork(void);
```

`fork()` creates a **child process** that is an almost exact copy of the parent. After the call:

- In the **parent**: `fork()` returns the child's PID (a positive integer).
- In the **child**: `fork()` returns `0`.
- On **error**: `fork()` returns `-1`.

```c
#include <stdio.h>
#include <unistd.h>

int main(void) {
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork");
        return 1;
    } else if (pid == 0) {
        // Child process
        printf("Child: PID = %d\n", getpid());
    } else {
        // Parent process
        printf("Parent: PID = %d, child PID = %d\n", getpid(), pid);
    }

    return 0;
}
```

**Output (order may vary):**

```
Parent: PID = 12345, child PID = 12346
Child: PID = 12346
```

### What `fork()` actually does

When you call `fork()`, the OS creates a **clone of your process** — same code, same variables, same position in the program. From that moment forward, there are **two separate processes** both sitting right after the `fork()` call, about to execute the next line.

The key is what `fork()` **returns** in each one:

- In the **parent** → returns the child's PID (a number > 0)
- In the **child** → returns `0`

So the `if` statement doesn't run twice in the same process — it runs **once per process**, but each process gets a different return value and therefore takes a different branch.

### Visualising it

```
main()
  |
  |  fork() called here
  |
  ●─────────────────────────────────────────────────────●
  │  (parent process continues)      (child process starts here, as a copy)
  │                                                     │
  │  fork() returned child_pid > 0   fork() returned 0 │
  │                                                     │
  ▼                                                     ▼
  else { ... }  ← parent branch        if (pid == 0) { ... }  ← child branch
```

They are two **independent processes** running the same code file, but taking different paths because of the return value.

### A mental model that helps

Think of it like a save state in a video game. `fork()` duplicates the save. Both "players" resume from the exact same point, but the game hands them different information (`0` vs. `child_pid`) so they can make different choices going forward. After that, they play completely independently — what happens to one doesn't affect the other.

### Why this design?

It's intentional and elegant. You write **one program**, and inside it you describe what the parent should do and what the child should do. The `if/else` on the return value of `fork()` is how you split those two personalities apart. The parent typically manages child lifecycles (`wait()`), while the child does the actual work (or calls `exec()` to become a completely different program).
> After `fork()`, both processes run **independently** from the same point in the code. The child inherits a copy of the parent's data — changes in one do not affect the other (Copy-on-Write semantics).

---

## PID and PPID

Every process is identified by two integers:

- **PID** (`pid_t`) — the Process ID, a unique number assigned by the kernel.
- **PPID** — the Parent Process ID, the PID of the process that created this one.

### Retrieving PID and PPID

```c
#include <unistd.h>

pid_t getpid(void);   // Returns the PID of the calling process
pid_t getppid(void);  // Returns the PPID of the calling process
```

### Example

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    printf("Parent PID:  %d\n", getpid());
    printf("Parent PPID: %d\n", getppid()); // e.g. your shell

    pid_t child = fork();

    if (child == 0) {
        printf("Child PID:   %d\n", getpid());
        printf("Child PPID:  %d\n", getppid()); // == parent's PID
    } else {
        wait(NULL); // Parent waits for child to finish
    }

    return 0;
}
```

**Output:**

```
Parent PID:  10200
Parent PPID: 9800
Child PID:   10201
Child PPID:  10200
```

### PID Hierarchy

```
init/systemd (PID 1)
    └── your shell (e.g. PID 9800)
            └── your program / parent (PID 10200)
                    └── child process (PID 10201)
```

Every process except PID 1 has a parent. If a parent dies before its child, the child becomes an **orphan** and is re-parented to PID 1 (`init`/`systemd`).

### Zombie Processes

A **zombie** is a child that has finished execution but whose exit status hasn't been collected by the parent yet. It stays in the process table until the parent calls `wait()` or `waitpid()`.

```c
#include <sys/wait.h>

pid_t wait(int *status);
pid_t waitpid(pid_t pid, int *status, int options);
```

```c
int status;
pid_t pid = wait(&status);

if (WIFEXITED(status)) {
    printf("Child %d exited with code %d\n", pid, WEXITSTATUS(status));
}
```

---

## Inter-Process Communication (IPC)

Because processes have **separate address spaces**, they cannot share variables directly. The OS provides several IPC mechanisms depending on your needs.

---

### 1. Pipes (Anonymous)

A **pipe** is a unidirectional byte stream connecting two processes. Data written to one end is read from the other. Only works between related processes (parent/child).

```c
#include <unistd.h>

int pipe(int fd[2]);
// fd[0] = read end
// fd[1] = write end
```

```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    int fd[2];
    pipe(fd);

    pid_t pid = fork();

    if (pid == 0) {
        // Child: reads from pipe
        close(fd[1]); // Close unused write end
        char buf[64];
        ssize_t n = read(fd[0], buf, sizeof(buf) - 1);
        buf[n] = '\0';
        printf("Child received: %s\n", buf);
        close(fd[0]);
    } else {
        // Parent: writes to pipe
        close(fd[0]); // Close unused read end
        const char *msg = "Hello from parent!";
        write(fd[1], msg, strlen(msg));
        close(fd[1]);
        wait(NULL);
    }

    return 0;
}
```

**Output:**

```
Child received: Hello from parent!
```

> Always close the unused end of a pipe in each process. Failing to do so prevents `read()` from returning EOF.

---

### 2. Named Pipes (FIFOs)

A **FIFO** (named pipe) works like an anonymous pipe but has a **name on the filesystem**, so unrelated processes can use it.

```c
#include <sys/stat.h>

int mkfifo(const char *pathname, mode_t mode);
```

**Writer:**

```c
#include <fcntl.h>
#include <string.h>
#include <unistd.h>

int main(void) {
    mkfifo("/tmp/myfifo", 0666);
    int fd = open("/tmp/myfifo", O_WRONLY);
    const char *msg = "data over FIFO";
    write(fd, msg, strlen(msg));
    close(fd);
    return 0;
}
```

**Reader:**

```c
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

int main(void) {
    int fd = open("/tmp/myfifo", O_RDONLY);
    char buf[64];
    ssize_t n = read(fd, buf, sizeof(buf) - 1);
    buf[n] = '\0';
    printf("Received: %s\n", buf);
    close(fd);
    return 0;
}
```

> `open()` on a FIFO **blocks** until both ends are connected (one reader and one writer are ready), unless `O_NONBLOCK` is used.

---

### 3. Signals

A **signal** is an asynchronous notification sent to a process (e.g., `SIGINT` from Ctrl+C, `SIGKILL` to forcibly terminate). You can also send signals explicitly between processes.

```c
#include <signal.h>

int kill(pid_t pid, int sig); // Send a signal to a process
int raise(int sig);           // Send a signal to yourself
```

**Custom signal handler:**

```c
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

void handler(int sig) {
    printf("Caught signal %d\n", sig);
}

int main(void) {
    signal(SIGUSR1, handler);

    pid_t pid = fork();

    if (pid == 0) {
        // Child: wait for signal
        pause(); // Suspend until a signal is received
    } else {
        // Parent: send SIGUSR1 to child
        sleep(1);
        kill(pid, SIGUSR1);
        wait(NULL);
    }

    return 0;
}
```

**Output:**

```
Caught signal 10
```

> Signals are limited in the amount of information they carry — just a signal number. Use them for notifications/events, not for data transfer.

---

### 4. Shared Memory

**Shared memory** is the fastest IPC method. Two processes map the same physical memory region into their respective address spaces and can read/write it directly. Requires explicit synchronization (e.g., semaphores) to avoid race conditions.

```c
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>

// Create/open a shared memory object
int shm_open(const char *name, int oflag, mode_t mode);

// Map it into the address space
void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
```

```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>

int main(void) {
    // Create anonymous shared memory (works between parent/child)
    char *shared = mmap(NULL, 64,
                        PROT_READ | PROT_WRITE,
                        MAP_SHARED | MAP_ANONYMOUS,
                        -1, 0);

    pid_t pid = fork();

    if (pid == 0) {
        // Child writes to shared memory
        strcpy(shared, "hello from child");
    } else {
        wait(NULL);
        // Parent reads what child wrote
        printf("Parent reads: %s\n", shared);
        munmap(shared, 64);
    }

    return 0;
}
```

**Output:**

```
Parent reads: hello from child
```

> For unrelated processes, use `shm_open()` + `ftruncate()` + `mmap()` and link with `-lrt`. Always clean up with `shm_unlink()`.

---

### 5. Message Queues (POSIX)

A **message queue** lets processes send typed, discrete messages. Unlike pipes, messages preserve boundaries and have a priority.

```c
#include <mqueue.h>
// Compile with: -lrt

mqd_t mq_open(const char *name, int oflag, ...);
int   mq_send(mqd_t mqdes, const char *msg_ptr, size_t msg_len, unsigned msg_prio);
ssize_t mq_receive(mqd_t mqdes, char *msg_ptr, size_t msg_len, unsigned *msg_prio);
int   mq_close(mqd_t mqdes);
int   mq_unlink(const char *name);
```

```c
#include <mqueue.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#define QUEUE_NAME "/demo_queue"
#define MAX_SIZE   256

int main(void) {
    struct mq_attr attr = { .mq_flags = 0, .mq_maxmsg = 10,
                            .mq_msgsize = MAX_SIZE, .mq_curmsgs = 0 };

    pid_t pid = fork();

    if (pid == 0) {
        // Child: receive
        mqd_t mq = mq_open(QUEUE_NAME, O_RDONLY);
        char buf[MAX_SIZE];
        mq_receive(mq, buf, MAX_SIZE, NULL);
        printf("Child received: %s\n", buf);
        mq_close(mq);
    } else {
        // Parent: send
        mqd_t mq = mq_open(QUEUE_NAME, O_CREAT | O_WRONLY, 0644, &attr);
        const char *msg = "message via queue";
        mq_send(mq, msg, strlen(msg) + 1, 0);
        mq_close(mq);
        wait(NULL);
        mq_unlink(QUEUE_NAME); // Clean up
    }

    return 0;
}
```

---

### 6. Sockets

**Sockets** provide bidirectional communication and are the most general IPC mechanism. They work for:

- **Local IPC** via Unix domain sockets (`AF_UNIX`) — fast, no network stack.
- **Network IPC** via TCP/UDP (`AF_INET`, `AF_INET6`) — between machines.

```c
// Unix domain socket (same machine, unrelated processes)
#include <sys/socket.h>
#include <sys/un.h>

int sock = socket(AF_UNIX, SOCK_STREAM, 0);
```

Sockets are the foundation of network programming and are covered in depth separately.

---

## IPC Methods — Summary

| Method | Direction | Related processes only? | Data type | Speed | Persistence |
|---|---|---|---|---|---|
| Anonymous pipe | Unidirectional | Yes (parent/child) | Byte stream | Fast | Until all FDs closed |
| Named pipe (FIFO) | Unidirectional | No | Byte stream | Fast | Until unlinked |
| Signal | Unidirectional | No | Signal number only | Fast | Instant / async |
| Shared memory | Bidirectional | No | Raw bytes | **Fastest** | Until unlinked |
| Message queue | Bidirectional | No | Discrete messages | Fast | Until unlinked |
| Socket (`AF_UNIX`) | Bidirectional | No | Byte stream | Fast | Until unlinked |
| Socket (`AF_INET`) | Bidirectional | No (cross-machine) | Byte stream | Network speed | Session-based |

### Choosing an IPC mechanism

```
Do the processes need to communicate across machines?
        │
       Yes ──────────────────────────────► TCP/UDP Sockets (AF_INET)
        │
       No
        │
       ▼
Do you need maximum throughput (large data)?
        │
       Yes ──────────────────────────────► Shared Memory (+ semaphore)
        │
       No
        │
       ▼
Do you need discrete, typed messages with priority?
        │
       Yes ──────────────────────────────► POSIX Message Queue
        │
       No
        │
       ▼
Are processes parent/child and just streaming data?
        │
       Yes ──────────────────────────────► Anonymous Pipe
        │
       No
        │
       ▼
                                          Named Pipe or Unix Socket
```

---

## Quick Reference

```c
#include <unistd.h>

pid_t fork(void);       // Create a child process
pid_t getpid(void);     // Get current process PID
pid_t getppid(void);    // Get parent process PID
int   pipe(int fd[2]);  // Create an anonymous pipe

#include <sys/wait.h>

pid_t wait(int *status);                        // Wait for any child
pid_t waitpid(pid_t pid, int *status, int opt); // Wait for specific child

#include <signal.h>

int kill(pid_t pid, int sig);  // Send signal to process

#include <sys/mman.h>

void *mmap(...);   // Map memory (use MAP_SHARED | MAP_ANONYMOUS for IPC)
int   munmap(void *addr, size_t length);
```

---

_Standard: POSIX.1-2008. All functions shown require a POSIX-compliant OS (Linux, macOS, etc.)._

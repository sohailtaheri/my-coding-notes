
## What Is a Signal?

A **signal** is a small asynchronous notification delivered to a process by the OS kernel, another process, or the process itself. It interrupts whatever the process is doing and triggers a response — much like a hardware interrupt, but at the software level.

Signals are defined as integer constants in `<signal.h>`. You never work with the raw numbers directly — always use the symbolic names (`SIGINT`, `SIGTERM`, etc.).

```
Process running normally
        │
        │  ← signal arrives (e.g. SIGINT)
        ▼
Normal execution is interrupted
        │
        ▼
Signal handler runs (or default action applies)
        │
        ▼
Process resumes (if not terminated)
```

---

## Standard Signals

The most common POSIX signals, their default actions, and how they are typically generated:

| Signal | Number | Default Action | Meaning |
|---|---|---|---|
| `SIGHUP` | 1 | Terminate | Hangup — terminal closed or daemon reload |
| `SIGINT` | 2 | Terminate | Keyboard interrupt (`Ctrl+C`) |
| `SIGQUIT` | 3 | Core dump | Quit from keyboard (`Ctrl+\`) |
| `SIGILL` | 4 | Core dump | Illegal CPU instruction |
| `SIGABRT` | 6 | Core dump | Abort — sent by `abort()` |
| `SIGFPE` | 8 | Core dump | Floating-point / arithmetic exception |
| `SIGKILL` | 9 | Terminate | **Force kill — cannot be caught or ignored** |
| `SIGSEGV` | 11 | Core dump | Segmentation fault (invalid memory access) |
| `SIGPIPE` | 13 | Terminate | Write to a broken pipe (no reader) |
| `SIGALRM` | 14 | Terminate | Timer expired (`alarm()`) |
| `SIGTERM` | 15 | Terminate | Graceful termination request |
| `SIGUSR1` | 10 | Terminate | User-defined signal 1 |
| `SIGUSR2` | 12 | Terminate | User-defined signal 2 |
| `SIGCHLD` | 17 | Ignore | Child process stopped or terminated |
| `SIGCONT` | 18 | Continue | Resume a stopped process |
| `SIGSTOP` | 19 | Stop | **Pause process — cannot be caught or ignored** |
| `SIGTSTP` | 20 | Stop | Stop from terminal (`Ctrl+Z`) |

### Default Actions

Each signal has one of four possible default actions if no handler is installed:

- **Terminate** — the process exits.
- **Core dump** — the process exits and writes a `core` file (snapshot of memory for debugging).
- **Ignore** — the signal is silently discarded.
- **Stop** — the process is paused (can be resumed with `SIGCONT`).
- **Continue** — resume a previously stopped process.

---

## Terminal Signal Generation

The terminal driver converts certain key sequences into signals automatically:

| Key | Signal sent | Default effect |
|---|---|---|
| `Ctrl+C` | `SIGINT` | Terminate the foreground process |
| `Ctrl+\` | `SIGQUIT` | Terminate + core dump |
| `Ctrl+Z` | `SIGTSTP` | Pause (stop) the foreground process |

You can inspect or change these key bindings with:

```bash
stty -a          # Show all terminal settings
stty intr ^C     # Set Ctrl+C as the SIGINT key
```

### Foreground vs Background

Only the **foreground process group** of a terminal receives keyboard-generated signals. Background processes (`./prog &`) are insulated from `Ctrl+C`.

```bash
./long_running_program &   # Background — Ctrl+C won't kill it
./long_running_program     # Foreground — Ctrl+C sends SIGINT
```

---

## Sending Signals

### From the Shell — `kill`

Despite the name, `kill` sends **any** signal, not just termination signals.

```bash
kill -SIGTERM 1234    # Gracefully ask PID 1234 to terminate
kill -SIGKILL 1234    # Force kill PID 1234
kill -9 1234          # Same as above (signal number)
kill -SIGUSR1 1234    # Send user-defined signal 1
kill -l               # List all signal names and numbers
```

### From C — `kill()`

```c
#include <signal.h>

int kill(pid_t pid, int sig);
```

`kill()` sends signal `sig` to the process (or group) identified by `pid`. Returns `0` on success, `-1` on error.

| `pid` value | Who receives the signal |
|---|---|
| `> 0` | The process with that specific PID |
| `0` | Every process in the sender's **process group** |
| `-1` | Every process the caller has permission to signal |
| `< -1` | Every process in the process group `abs(pid)` |

```c
#include <signal.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    pid_t child = fork();

    if (child == 0) {
        // Child: sleep forever, waiting for a signal
        while (1) {
            pause(); // sleep until any signal arrives
        }
    } else {
        sleep(1);
        printf("Parent: sending SIGTERM to child %d\n", child);
        kill(child, SIGTERM);
        wait(NULL);
        printf("Parent: child has exited\n");
    }

    return 0;
}
```

### From C — `raise()`

`raise()` sends a signal to **the calling process itself**.

```c
#include <signal.h>

int raise(int sig);
```

```c
#include <signal.h>
#include <stdio.h>

int main(void) {
    printf("About to raise SIGABRT\n");
    raise(SIGABRT); // Triggers abort (core dump by default)
    printf("This line is never reached\n");
    return 0;
}
```

> `raise(sig)` is equivalent to `kill(getpid(), sig)`.

---

## Handling Signals — `signal()`

The simplest way to install a custom signal handler is `signal()` from `<signal.h>`.

```c
#include <signal.h>

typedef void (*sighandler_t)(int);
sighandler_t signal(int signum, sighandler_t handler);
```

The `handler` argument can be:

| Value | Meaning |
|---|---|
| A function pointer `void f(int)` | Install a custom handler |
| `SIG_DFL` | Restore the default action |
| `SIG_IGN` | Ignore the signal |

### Basic Handler Example

```c
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

void sigint_handler(int sig) {
    // sig holds the signal number that triggered this call
    printf("\nCaught SIGINT (%d) — press Ctrl+C again to confirm exit\n", sig);
    // Re-install default handler so a second Ctrl+C actually exits
    signal(SIGINT, SIG_DFL);
}

int main(void) {
    signal(SIGINT, sigint_handler); // Override default Ctrl+C behavior

    printf("Running. Press Ctrl+C to test the handler.\n");

    while (1) {
        printf("Working...\n");
        sleep(1);
    }

    return 0;
}
```

**Output (Ctrl+C pressed once):**

```
Running. Press Ctrl+C to test the handler.
Working...
Working...
^C
Caught SIGINT (2) — press Ctrl+C again to confirm exit
Working...
^C     ← second press exits normally
```

### Ignoring a Signal

```c
signal(SIGINT, SIG_IGN);  // Ctrl+C now does nothing
signal(SIGPIPE, SIG_IGN); // Common: ignore broken pipe errors in servers
```

### Restoring the Default

```c
signal(SIGINT, SIG_DFL); // Ctrl+C kills the process again
```

---

## Handling Signals — `sigaction()` (Preferred)

`signal()` is simple but has portability quirks and doesn't let you control signal masking or flags. In production code, prefer `sigaction()`.

```c
#include <signal.h>

int sigaction(int signum, const struct sigaction *act, struct sigaction *oldact);
```

The `struct sigaction` gives you full control:

```c
struct sigaction {
    void     (*sa_handler)(int);                        // Simple handler (or SIG_DFL / SIG_IGN)
    void     (*sa_sigaction)(int, siginfo_t *, void *); // Extended handler (used with SA_SIGINFO)
    sigset_t   sa_mask;    // Extra signals to block while handler runs
    int        sa_flags;   // Modifier flags (see below)
};
```

> On any given `struct sigaction`, only **one** of `sa_handler` or `sa_sigaction` is active at a time. Which one is used depends on whether `SA_SIGINFO` is set in `sa_flags`.

---

### `sa_mask` — Blocking Signals During the Handler

`sa_mask` is a `sigset_t` that specifies which **additional** signals should be blocked for the duration of the handler. The signal that triggered the handler is **always** blocked automatically (so the handler cannot interrupt itself), but `sa_mask` lets you block others too.

This is crucial for preventing race conditions when your handler and your main code share state.

```c
// Functions to build the mask (same as sigprocmask set helpers)
sigemptyset(&sa.sa_mask);            // Start with an empty mask (block nothing extra)
sigfillset(&sa.sa_mask);             // Block ALL other signals while handler runs
sigaddset(&sa.sa_mask, SIGTERM);     // Block only SIGTERM during the handler
sigaddset(&sa.sa_mask, SIGUSR1);     // Block SIGUSR1 too
```

#### Example — preventing SIGTERM from racing with SIGINT handler

```c
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

volatile sig_atomic_t shutdown_requested = 0;

void sigint_handler(int sig) {
    (void)sig;
    // SIGTERM is blocked here because of sa_mask — it cannot arrive
    // and re-enter or corrupt shutdown_requested while we are here
    shutdown_requested = 1;
}

int main(void) {
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));

    sa.sa_handler = sigint_handler;
    sigemptyset(&sa.sa_mask);
    sigaddset(&sa.sa_mask, SIGTERM);  // Block SIGTERM while SIGINT handler runs
    sa.sa_flags = SA_RESTART;

    sigaction(SIGINT, &sa, NULL);

    while (!shutdown_requested) {
        sleep(1);
    }

    printf("Shutting down.\n");
    return 0;
}
```

#### What happens to blocked signals?

Signals blocked via `sa_mask` are **not dropped** — they become **pending** and are delivered immediately after the handler returns and the mask is restored. The only exception is `SIGKILL` and `SIGSTOP`, which can never be blocked.

```
Handler starts
  ├─ sa_mask is added to the process's signal mask
  ├─ Handler body runs
  │     (blocked signals queue up as "pending")
  └─ Handler returns
       ├─ sa_mask is removed from the process's signal mask
       └─ Any pending signals are now delivered
```

---

### `sa_flags` — Modifying Signal Behaviour

`sa_flags` is a bitmask of flags that control how the signal and its handler behave. Multiple flags are combined with `|`.

| Flag | Effect |
|---|---|
| `SA_RESTART` | Automatically restart slow system calls (`read`, `write`, `wait`, etc.) interrupted by this signal, instead of returning `-1` with `errno = EINTR` |
| `SA_SIGINFO` | Use `sa_sigaction` instead of `sa_handler` — gives the handler access to `siginfo_t` (sender PID, UID, fault address, etc.) |
| `SA_NOCLDSTOP` | Only valid for `SIGCHLD`: suppress notification when a child is **stopped** (only notify on exit/termination) |
| `SA_NOCLDWAIT` | Only valid for `SIGCHLD`: don't create zombies — children are reaped automatically (implies no `wait()` needed) |
| `SA_NODEFER` | Do **not** automatically block the signal while its handler runs. This allows the handler to be re-entered by the same signal (use with care) |
| `SA_RESETHAND` | Reset the handler back to `SIG_DFL` after it fires once — one-shot handler |
| `SA_ONSTACK` | Run the handler on an alternate signal stack (set up with `sigaltstack()`). Required for handling `SIGSEGV` caused by stack overflow |

#### `SA_RESTART` in depth

Without `SA_RESTART`, a signal interrupting a blocking call causes it to return `-1` and set `errno` to `EINTR`. You must then check and retry manually:

```c
// Without SA_RESTART — you must handle EINTR yourself
ssize_t n;
do {
    n = read(fd, buf, sizeof(buf));
} while (n == -1 && errno == EINTR);
```

With `SA_RESTART`, the kernel retries the syscall automatically — much cleaner for most programs. However, some calls (`poll`, `select`, `nanosleep`, `connect`) are **never** restarted even with `SA_RESTART` on some systems, so always check the man page.

#### `SA_NODEFER` — allowing re-entrant handlers

By default, a signal is blocked while its own handler runs (preventing recursive invocation). `SA_NODEFER` removes that protection:

```c
// Handler CAN be interrupted by the same signal again
sa.sa_flags = SA_NODEFER;
```

This is almost never what you want — use it only when you explicitly need re-entrant signal delivery (e.g., a SIGCHLD handler that must handle rapid-fire child exits without queuing).

#### `SA_RESETHAND` — one-shot handler

```c
// Handler fires once, then SIGINT reverts to its default (terminate)
sa.sa_flags = SA_RESETHAND;
sigaction(SIGINT, &sa, NULL);
```

This is the same behavior that the old `signal()` function used on some BSDs, and it mirrors the "catch Ctrl+C once, then let the second one kill you" pattern.

#### `SA_ONSTACK` — alternate signal stack

If your program crashes due to a stack overflow, `SIGSEGV` is delivered but there's no stack space left to run the handler. `SA_ONSTACK` tells the kernel to run the handler on a separate pre-allocated stack:

```c
#include <signal.h>
#include <stdlib.h>

#define ALT_STACK_SIZE 65536

void setup_alt_stack(void) {
    stack_t ss;
    ss.ss_sp    = malloc(ALT_STACK_SIZE);
    ss.ss_size  = ALT_STACK_SIZE;
    ss.ss_flags = 0;
    sigaltstack(&ss, NULL);
}

// Then in your sigaction setup:
sa.sa_flags = SA_ONSTACK | SA_SIGINFO;
sigaction(SIGSEGV, &sa, NULL);
```

#### Combining flags

```c
// Typical production setup for a robust handler:
sa.sa_flags = SA_RESTART    // Don't break slow syscalls
            | SA_SIGINFO    // Get sender info via siginfo_t
            | SA_NOCLDSTOP; // (for SIGCHLD only) ignore stop events
```

---

### Simple `sigaction` Example

```c
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

void handler(int sig) {
    // write() is async-signal-safe; printf() is NOT
    const char msg[] = "Signal caught!\n";
    write(STDOUT_FILENO, msg, sizeof(msg) - 1);
}

int main(void) {
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));

    sa.sa_handler = handler;
    sigemptyset(&sa.sa_mask);         // Don't block extra signals during handler
    sa.sa_flags = SA_RESTART;         // Restart interrupted system calls

    sigaction(SIGINT, &sa, NULL);
    sigaction(SIGUSR1, &sa, NULL);

    printf("PID: %d — waiting for signals...\n", getpid());

    while (1) {
        pause();
    }

    return 0;
}
```

Test it from another terminal:

```bash
kill -SIGUSR1 <PID>
```

### Extended Handler with `siginfo_t`

When `SA_SIGINFO` is set in `sa_flags`, the handler receives extra information about the signal's origin:

```c
#include <signal.h>
#include <stdio.h>
#include <string.h>

void extended_handler(int sig, siginfo_t *info, void *context) {
    printf("Signal %d received\n", sig);
    printf("  Sent by PID: %d\n", info->si_pid);
    printf("  Sender UID: %d\n", info->si_uid);
}

int main(void) {
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));

    sa.sa_sigaction = extended_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_SIGINFO | SA_RESTART; // SA_SIGINFO enables extended handler

    sigaction(SIGUSR1, &sa, NULL);

    printf("PID %d waiting...\n", getpid());
    pause();
    return 0;
}
```

---

## Signal Handler Rules — What Is Safe Inside a Handler?

Signal handlers run **asynchronously** — they can interrupt your code at any point. This creates serious restrictions on what you can safely call inside a handler.

### Only call async-signal-safe functions

The POSIX standard defines a list of **async-signal-safe** functions that are guaranteed to be safe to call from a handler. Most standard library functions are **NOT** on this list.

| Safe to call | NOT safe to call |
|---|---|
| `write()` | `printf()`, `fprintf()` |
| `read()`, `open()`, `close()` | `malloc()`, `free()` |
| `_exit()` | `exit()` |
| `kill()`, `raise()` | `fopen()`, `fclose()` |
| `signal()`, `sigaction()` | `strtok()`, `getenv()` |
| `getpid()`, `getppid()` | Any non-reentrant function |

### The volatile sig_atomic_t pattern

The correct way to communicate from a handler to the rest of your program is via a `volatile sig_atomic_t` flag:

```c
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

volatile sig_atomic_t keep_running = 1;

void handle_sigint(int sig) {
    (void)sig;           // Suppress unused parameter warning
    keep_running = 0;    // Safe: sig_atomic_t write is atomic
}

int main(void) {
    struct sigaction sa = { .sa_handler = handle_sigint };
    sigemptyset(&sa.sa_mask);
    sigaction(SIGINT, &sa, NULL);

    printf("Running. Ctrl+C to stop.\n");

    while (keep_running) {
        printf("tick\n");
        sleep(1);
    }

    printf("\nShutting down gracefully.\n");
    return 0;
}
```

> `volatile` prevents the compiler from optimizing away reads of the flag. `sig_atomic_t` ensures the read/write is atomic at the hardware level.

---

## Signal Masking — Blocking Signals Temporarily

You can **block** signals to prevent them from being delivered during a critical section, then unblock them afterwards.

```c
#include <signal.h>

// Manipulate a signal set
int sigemptyset(sigset_t *set);         // Clear all signals
int sigfillset(sigset_t *set);          // Add all signals
int sigaddset(sigset_t *set, int sig);  // Add one signal
int sigdelset(sigset_t *set, int sig);  // Remove one signal

// Apply the mask to the process
int sigprocmask(int how, const sigset_t *set, sigset_t *oldset);
```

`how` can be:

| Value | Effect |
|---|---|
| `SIG_BLOCK` | Add `set` to the current mask (block these signals) |
| `SIG_UNBLOCK` | Remove `set` from the current mask |
| `SIG_SETMASK` | Replace the mask entirely with `set` |

### Example — Protecting a Critical Section

```c
#include <signal.h>
#include <stdio.h>

int main(void) {
    sigset_t block_set, old_set;

    sigemptyset(&block_set);
    sigaddset(&block_set, SIGINT);  // We want to block Ctrl+C
    sigaddset(&block_set, SIGTERM);

    // Block SIGINT and SIGTERM
    sigprocmask(SIG_BLOCK, &block_set, &old_set);

    printf("Critical section — Ctrl+C is blocked here\n");
    sleep(3); // Simulate work; SIGINT is queued, not delivered

    // Restore previous mask — any pending signals are now delivered
    sigprocmask(SIG_SETMASK, &old_set, NULL);
    printf("Critical section done — signals unblocked\n");

    return 0;
}
```

> Blocked signals are not lost — they are **queued** (pending) and delivered as soon as you unblock them.

---

## Timer Signals — `alarm()`

`alarm()` schedules a `SIGALRM` to be sent to the process after a specified number of seconds. Useful for timeouts.

```c
#include <unistd.h>

unsigned int alarm(unsigned int seconds); // Returns seconds remaining on old alarm
```

```c
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

void alarm_handler(int sig) {
    (void)sig;
    write(STDOUT_FILENO, "Timeout!\n", 9);
}

int main(void) {
    struct sigaction sa = { .sa_handler = alarm_handler };
    sigemptyset(&sa.sa_mask);
    sigaction(SIGALRM, &sa, NULL);

    alarm(3); // Fire SIGALRM in 3 seconds

    printf("Waiting for input (3 second timeout)...\n");

    char buf[64];
    if (read(STDIN_FILENO, buf, sizeof(buf)) > 0) {
        alarm(0); // Cancel the alarm if input arrived in time
        printf("Got input!\n");
    }

    return 0;
}
```

---

## `SIGCHLD` — Reaping Child Processes

When a child process exits, the kernel sends `SIGCHLD` to the parent. The default action is to ignore it, but if the parent never calls `wait()`, the child becomes a **zombie**.

A clean pattern is to handle `SIGCHLD` and call `waitpid()` inside the handler:

```c
#include <signal.h>
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

void sigchld_handler(int sig) {
    (void)sig;
    int status;
    pid_t pid;

    // Loop: collect ALL terminated children (multiple may have exited)
    while ((pid = waitpid(-1, &status, WNOHANG)) > 0) {
        // WNOHANG: don't block if no child has exited yet
        if (WIFEXITED(status)) {
            // Can't use printf here safely — use write in real code
        }
    }
}

int main(void) {
    struct sigaction sa = { .sa_handler = sigchld_handler };
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART | SA_NOCLDSTOP; // Don't notify on stop, only exit
    sigaction(SIGCHLD, &sa, NULL);

    for (int i = 0; i < 3; i++) {
        if (fork() == 0) {
            sleep(i + 1);
            _exit(0); // Child exits
        }
    }

    printf("Parent waiting for all children...\n");
    sleep(5);
    printf("Done.\n");
    return 0;
}
```

---

## `signal()` vs `sigaction()` — When to Use Which

| Feature | `signal()` | `sigaction()` |
|---|---|---|
| Portability | Varies by OS (behavior differs on some systems) | Fully POSIX-defined, consistent |
| Extra info (`si_pid`, etc.) | Not available | Available via `SA_SIGINFO` |
| Control signal mask during handler | Not available | `sa_mask` field |
| `SA_RESTART` (auto-restart syscalls) | Not available | Available via `sa_flags` |
| Simplicity | High | Moderate |
| **Recommendation** | Quick scripts, learning | **Production code — always prefer** |

---

## Quick Reference

```c
#include <signal.h>
#include <unistd.h>

// ── Sending ──────────────────────────────────────────────────
int kill(pid_t pid, int sig);   // Send signal to another process
int raise(int sig);             // Send signal to yourself

// ── Simple handler ───────────────────────────────────────────
signal(SIGINT, my_handler);     // Install handler
signal(SIGINT, SIG_DFL);        // Restore default
signal(SIGINT, SIG_IGN);        // Ignore

// ── Robust handler ───────────────────────────────────────────
struct sigaction sa;
memset(&sa, 0, sizeof(sa));
sa.sa_handler = my_handler;
sigemptyset(&sa.sa_mask);
sa.sa_flags = SA_RESTART;
sigaction(SIGINT, &sa, NULL);

// ── Safe flag pattern ────────────────────────────────────────
volatile sig_atomic_t flag = 0;
void handler(int s) { flag = 1; }

// ── Masking ──────────────────────────────────────────────────
sigset_t set;
sigemptyset(&set);
sigaddset(&set, SIGINT);
sigprocmask(SIG_BLOCK, &set, NULL);     // Block
sigprocmask(SIG_UNBLOCK, &set, NULL);   // Unblock

// ── Timer ────────────────────────────────────────────────────
alarm(5);   // Send SIGALRM in 5 seconds
alarm(0);   // Cancel pending alarm
```

---

_Standard: POSIX.1-2008. All functions require a POSIX-compliant OS (Linux, macOS, etc.). Compile with `-Wall -Wextra` to catch signal-related pitfalls._

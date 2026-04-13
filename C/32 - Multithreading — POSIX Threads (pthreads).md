
A practical introduction to multithreading in C using the POSIX threads API: creating threads, passing data, synchronising with mutexes and condition variables, and avoiding common pitfalls.

---

## What Is a Thread?

A **thread** is an independent unit of execution that lives *inside* a process. All threads within a process share the same address space — the same heap, global variables, and file descriptors — but each thread has its own:

- **Stack** (local variables, function call frames)
- **Program counter** (where it is currently executing)
- **Register set**
- **Thread ID** (`pthread_t`)

This shared memory is what makes threads fast for communication but dangerous if not synchronised properly.

```
Process
├── Code segment  (shared)
├── Data / BSS    (shared — global and static variables)
├── Heap          (shared — malloc'd memory)
├── File descriptors (shared)
│
├── Thread 1 ── Stack + Registers + PC
├── Thread 2 ── Stack + Registers + PC
└── Thread 3 ── Stack + Registers + PC
```

---

## Compiling with pthreads

Always link with `-pthread` (not just `-lpthread` — the flag also sets preprocessor defines):

```bash
gcc -Wall -Wextra -pthread -o program program.c
```

And include the header:

```c
#include <pthread.h>
```

---

## Creating Threads — `pthread_create()`

```c
int pthread_create(pthread_t *thread,
                   const pthread_attr_t *attr,
                   void *(*start_routine)(void *),
                   void *arg);
```

| Parameter | Purpose |
|---|---|
| `thread` | Output — filled with the new thread's ID |
| `attr` | Thread attributes (`NULL` for defaults) |
| `start_routine` | The function the thread will run — signature must be `void *fn(void *)` |
| `arg` | A single argument passed to `start_routine` (cast to `void *`) |

Returns `0` on success, or an error code (not `-1` — pthreads doesn't use `errno` for return values).

### Minimal Example

```c
#include <pthread.h>
#include <stdio.h>

void *worker(void *arg) {
    printf("Hello from the thread!\n");
    return NULL;
}

int main(void) {
    pthread_t tid;

    pthread_create(&tid, NULL, worker, NULL);
    pthread_join(tid, NULL); // Wait for thread to finish

    printf("Thread done.\n");
    return 0;
}
```

**Output:**

```
Hello from the thread!
Thread done.
```

---

## Joining and Detaching Threads

### `pthread_join()` — Wait for a thread

```c
int pthread_join(pthread_t thread, void **retval);
```

Blocks the caller until `thread` finishes. If `retval` is non-NULL, it receives the value returned (or passed to `pthread_exit()`) by the thread.

```c
void *worker(void *arg) {
    int *result = malloc(sizeof(int));
    *result = 42;
    return result; // Returned via pthread_join
}

int main(void) {
    pthread_t tid;
    void *ret;

    pthread_create(&tid, NULL, worker, NULL);
    pthread_join(tid, &ret);

    int *value = (int *)ret;
    printf("Thread returned: %d\n", *value);
    free(value);
    return 0;
}
```

> A thread that is neither joined nor detached becomes a **zombie thread** — it holds resources until the process exits. Always join or detach every thread.

### `pthread_detach()` — Fire and forget

If you don't need the return value and don't want to join, detach the thread. Its resources are released automatically when it finishes.

```c
pthread_t tid;
pthread_create(&tid, NULL, worker, NULL);
pthread_detach(tid); // No need to join — resources freed on exit
```

Or detach from inside the thread itself:

```c
void *worker(void *arg) {
    pthread_detach(pthread_self());
    // ... do work
    return NULL;
}
```

---

## Passing Arguments to Threads

`pthread_create` only accepts a single `void *` argument. For multiple values, pack them into a struct.

### Passing a single value

```c
void *worker(void *arg) {
    int n = *(int *)arg;
    printf("Got: %d\n", n);
    return NULL;
}

int main(void) {
    int value = 99;
    pthread_t tid;
    pthread_create(&tid, NULL, worker, &value);
    pthread_join(tid, NULL);
    return 0;
}
```

### Passing multiple values via a struct

```c
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int   id;
    float multiplier;
} ThreadArgs;

void *worker(void *arg) {
    ThreadArgs *a = (ThreadArgs *)arg;
    printf("Thread %d: %.2f\n", a->id, a->multiplier * 10.0f);
    return NULL;
}

int main(void) {
    pthread_t tids[3];
    ThreadArgs args[3] = {
        {0, 1.5f},
        {1, 2.0f},
        {2, 3.5f},
    };

    for (int i = 0; i < 3; i++) {
        pthread_create(&tids[i], NULL, worker, &args[i]);
    }
    for (int i = 0; i < 3; i++) {
        pthread_join(tids[i], NULL);
    }
    return 0;
}
```

**Output (order may vary):**

```
Thread 0: 15.00
Thread 2: 35.00
Thread 1: 20.00
```

> Always ensure the argument data outlives the thread. Passing a stack variable that goes out of scope before the thread reads it is a common bug.

---

## Thread Safety and Race Conditions

Because threads share memory, **unsynchronized access to shared data causes race conditions** — the result depends on the unpredictable order in which threads are scheduled.

### Classic race condition

```c
#include <pthread.h>
#include <stdio.h>

int counter = 0; // Shared global

void *increment(void *arg) {
    for (int i = 0; i < 1000000; i++) {
        counter++; // NOT atomic — read-modify-write is 3 CPU operations
    }
    return NULL;
}

int main(void) {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, increment, NULL);
    pthread_create(&t2, NULL, increment, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    // Expected: 2000000 — actual: some random smaller number
    printf("Counter: %d\n", counter);
    return 0;
}
```

The `counter++` operation compiles to three CPU instructions (load, add, store). Two threads can interleave these steps and overwrite each other's results — a **lost update**.

---

## Mutexes — `pthread_mutex_t`

A **mutex** (mutual exclusion lock) ensures only one thread at a time can execute a critical section.

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER; // Static init

// Or dynamic init:
pthread_mutex_t mutex;
pthread_mutex_init(&mutex, NULL);

pthread_mutex_lock(&mutex);     // Block until lock is acquired
// --- critical section ---
pthread_mutex_unlock(&mutex);   // Release the lock

pthread_mutex_destroy(&mutex);  // Clean up (dynamic init only)
```

### Fixing the race condition

```c
#include <pthread.h>
#include <stdio.h>

int counter = 0;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *increment(void *arg) {
    for (int i = 0; i < 1000000; i++) {
        pthread_mutex_lock(&lock);
        counter++;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main(void) {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, increment, NULL);
    pthread_create(&t2, NULL, increment, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Counter: %d\n", counter); // Always 2000000
    pthread_mutex_destroy(&lock);
    return 0;
}
```

### `pthread_mutex_trylock()`

Non-blocking variant — returns immediately with `EBUSY` if the lock is taken:

```c
if (pthread_mutex_trylock(&lock) == 0) {
    // Got the lock — do work
    pthread_mutex_unlock(&lock);
} else {
    // Lock is held by another thread — do something else
}
```

### Deadlock

A **deadlock** occurs when two threads each hold a lock the other needs, and both block forever waiting.

```
Thread A holds Lock 1, waits for Lock 2
Thread B holds Lock 2, waits for Lock 1
         → Neither can proceed
```

**Prevention rules:**
- Always acquire multiple locks in the **same order** across all threads.
- Use `pthread_mutex_trylock()` with a backoff strategy.
- Keep critical sections short — lock, operate, unlock.

---

## Condition Variables — `pthread_cond_t`

A **condition variable** lets a thread sleep until another thread signals that some condition is true. Used together with a mutex.

```c
pthread_cond_t  cond  = PTHREAD_COND_INITIALIZER;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

// Waiting thread
pthread_mutex_lock(&mutex);
while (!condition_is_true) {          // Always in a while loop, not if
    pthread_cond_wait(&cond, &mutex); // Atomically releases mutex and sleeps
}
// condition is now true — proceed
pthread_mutex_unlock(&mutex);

// Signalling thread
pthread_mutex_lock(&mutex);
condition_is_true = 1;
pthread_cond_signal(&cond);    // Wake one waiting thread
// or:
pthread_cond_broadcast(&cond); // Wake ALL waiting threads
pthread_mutex_unlock(&mutex);
```

> `pthread_cond_wait()` can return **spuriously** (without being signalled) due to OS internals. This is why the condition check must always be in a `while` loop, never an `if`.

### Producer–Consumer Example

```c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

#define BUFFER_SIZE 5

int buffer[BUFFER_SIZE];
int count = 0; // Number of items in buffer

pthread_mutex_t mutex     = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t  not_full  = PTHREAD_COND_INITIALIZER;
pthread_cond_t  not_empty = PTHREAD_COND_INITIALIZER;

void *producer(void *arg) {
    for (int i = 1; i <= 10; i++) {
        pthread_mutex_lock(&mutex);

        while (count == BUFFER_SIZE) {
            pthread_cond_wait(&not_full, &mutex); // Wait until space available
        }

        buffer[count++] = i;
        printf("Produced: %d  (buffer: %d/%d)\n", i, count, BUFFER_SIZE);

        pthread_cond_signal(&not_empty); // Tell consumer there's something
        pthread_mutex_unlock(&mutex);
        usleep(100000);
    }
    return NULL;
}

void *consumer(void *arg) {
    for (int i = 0; i < 10; i++) {
        pthread_mutex_lock(&mutex);

        while (count == 0) {
            pthread_cond_wait(&not_empty, &mutex); // Wait until something to consume
        }

        int val = buffer[--count];
        printf("Consumed: %d  (buffer: %d/%d)\n", val, count, BUFFER_SIZE);

        pthread_cond_signal(&not_full); // Tell producer there's space
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main(void) {
    pthread_t prod, cons;
    pthread_create(&prod, NULL, producer, NULL);
    pthread_create(&cons, NULL, consumer, NULL);
    pthread_join(prod, NULL);
    pthread_join(cons, NULL);
    return 0;
}
```

---

## Thread-Local Storage — `_Thread_local`

Sometimes you want a variable that looks global but is **private to each thread**. Use `_Thread_local` (C11 standard) or the GCC extension `__thread`:

```c
#include <pthread.h>
#include <stdio.h>

_Thread_local int thread_id = 0; // Each thread has its own copy

void *worker(void *arg) {
    thread_id = *(int *)arg; // Only affects this thread's copy
    printf("My thread_id: %d\n", thread_id);
    return NULL;
}

int main(void) {
    pthread_t tids[3];
    int ids[3] = {1, 2, 3};

    for (int i = 0; i < 3; i++) {
        pthread_create(&tids[i], NULL, worker, &ids[i]);
    }
    for (int i = 0; i < 3; i++) {
        pthread_join(tids[i], NULL);
    }
    return 0;
}
```

Each thread sees its own `thread_id` — writes in one thread don't affect others.

---

## Thread Attributes — `pthread_attr_t`

Thread attributes let you configure a thread before creating it.

```c
pthread_attr_t attr;
pthread_attr_init(&attr);

// Set stack size (default is typically 8 MB)
pthread_attr_setstacksize(&attr, 4 * 1024 * 1024); // 4 MB

// Create as detached (no need to join)
pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

pthread_create(&tid, &attr, worker, NULL);
pthread_attr_destroy(&attr); // Always clean up attrs
```

Common attribute setters:

| Function | What it controls |
|---|---|
| `pthread_attr_setstacksize()` | Stack size for the new thread |
| `pthread_attr_setdetachstate()` | `PTHREAD_CREATE_JOINABLE` (default) or `PTHREAD_CREATE_DETACHED` |
| `pthread_attr_setschedpolicy()` | Scheduling policy (`SCHED_FIFO`, `SCHED_RR`, `SCHED_OTHER`) |
| `pthread_attr_setschedparam()` | Scheduling priority |

---

## `pthread_exit()` — Terminating a Thread

A thread ends when its start function returns, but you can also terminate it explicitly from anywhere in its call stack:

```c
void *worker(void *arg) {
    if (some_error_condition) {
        pthread_exit((void *)-1); // Exit thread with a return value
    }
    // ...
    return (void *)0;
}
```

> **Never call `exit()` from a thread** — it terminates the entire process, not just the thread.

---

## `pthread_cancel()` — Cancelling a Thread

You can request that another thread be cancelled:

```c
pthread_cancel(tid); // Request cancellation of thread tid
```

Cancellation is **not immediate** by default. The target thread is only cancelled at **cancellation points** — certain blocking system calls like `sleep()`, `read()`, `write()`, `pthread_cond_wait()`, etc.

```c
// Inside the thread — control cancellation behaviour
pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);     // Default: accept cancels
pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, NULL);    // Ignore cancel requests

pthread_setcanceltype(PTHREAD_CANCEL_DEFERRED, NULL);    // Default: at cancel points only
pthread_setcanceltype(PTHREAD_CANCEL_ASYNCHRONOUS, NULL); // Cancel immediately (dangerous)
```

Use cleanup handlers to release resources if a thread is cancelled:

```c
void cleanup(void *arg) {
    pthread_mutex_t *m = arg;
    pthread_mutex_unlock(m); // Release lock if thread was cancelled mid-section
}

void *worker(void *arg) {
    pthread_cleanup_push(cleanup, &my_mutex);

    pthread_mutex_lock(&my_mutex);
    // ... work that might be cancelled
    pthread_mutex_unlock(&my_mutex);

    pthread_cleanup_pop(0); // 0 = don't execute handler on normal exit
    return NULL;
}
```

---

## Common Pitfalls

### 1. Passing a loop variable by pointer

```c
// WRONG — all threads may see the same final value of i
for (int i = 0; i < 4; i++) {
    pthread_create(&tids[i], NULL, worker, &i); // &i is the same address every time
}

// CORRECT — pass a per-thread copy
int ids[4] = {0, 1, 2, 3};
for (int i = 0; i < 4; i++) {
    pthread_create(&tids[i], NULL, worker, &ids[i]);
}
```

### 2. Forgetting to join or detach

Every thread must be either joined or detached. Ignoring it leaks thread resources.

### 3. Returning a pointer to a local variable

```c
// WRONG — stack frame is gone when thread returns
void *worker(void *arg) {
    int result = 42;
    return &result; // Dangling pointer!
}

// CORRECT — heap-allocate the result
void *worker(void *arg) {
    int *result = malloc(sizeof(int));
    *result = 42;
    return result; // Caller must free()
}
```

### 4. Locking a mutex twice (self-deadlock)

A thread that calls `pthread_mutex_lock()` on a mutex it already holds will deadlock. Use `PTHREAD_MUTEX_RECURSIVE` if re-entrant locking is truly needed:

```c
pthread_mutexattr_t attr;
pthread_mutexattr_init(&attr);
pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_RECURSIVE);
pthread_mutex_init(&mutex, &attr);
pthread_mutexattr_destroy(&attr);
```

---

## Quick Reference

```c
#include <pthread.h>   // Compile with: gcc -pthread

// ── Lifecycle ────────────────────────────────────────────────────────
pthread_create(&tid, NULL, fn, arg);   // Create thread
pthread_join(tid, &retval);            // Wait for thread
pthread_detach(tid);                   // Release resources automatically
pthread_exit(retval);                  // Exit current thread
pthread_self();                        // Get own thread ID
pthread_equal(t1, t2);                 // Compare thread IDs

// ── Mutex ────────────────────────────────────────────────────────────
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_lock(&m);
pthread_mutex_trylock(&m);             // Non-blocking; returns EBUSY if taken
pthread_mutex_unlock(&m);
pthread_mutex_destroy(&m);

// ── Condition Variable ───────────────────────────────────────────────
pthread_cond_t c = PTHREAD_COND_INITIALIZER;
pthread_cond_wait(&c, &m);             // Atomically unlock + sleep
pthread_cond_signal(&c);               // Wake one waiter
pthread_cond_broadcast(&c);            // Wake all waiters
pthread_cond_destroy(&c);

// ── Thread-local storage ─────────────────────────────────────────────
_Thread_local int per_thread_var = 0;

// ── Cancellation ─────────────────────────────────────────────────────
pthread_cancel(tid);
pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);
pthread_cleanup_push(fn, arg);
pthread_cleanup_pop(execute);
```

---

_Standard: POSIX.1-2008 / IEEE Std 1003.1. Requires a POSIX-compliant OS. Compile with `gcc -pthread`._

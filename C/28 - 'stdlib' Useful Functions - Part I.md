# Program Control & Sorting in C: `exit`, `atexit`, `abort`, and `qsort`

A practical guide to process termination and the standard sorting function from `<stdlib.h>`.

---

## Table of Contents

1. [[#Overview]]
2. [[#`exit()` — Normal Termination]]
3. [[#`atexit()` — Register Cleanup Handlers]]
4. [[#`abort()` — Abnormal Termination]]
5. [[#`qsort()` — Generic Quicksort]]
6. [[#Comparing the Termination Functions]]
7. [[#Best Practices]]
8. [[#Common Pitfalls]]

---

## Overview

All four functions live in `<stdlib.h>`:

|Function|Purpose|
|---|---|
|`exit(status)`|Terminate normally, run cleanup handlers, flush buffers|
|`atexit(func)`|Register a function to call when `exit()` is invoked|
|`abort()`|Terminate abnormally, raise `SIGABRT`, skip cleanup|
|`qsort(base, n, size, cmp)`|Sort an array using a caller-supplied comparator|

---

## `exit()` — Normal Termination

### Syntax

```c
#include <stdlib.h>

void exit(int status);
```

`exit()` terminates the program **normally**. Before returning control to the OS it:

1. Calls all functions registered with `atexit()`, in reverse registration order
2. Flushes and closes all open `stdio` streams
3. Removes files created with `tmpfile()`
4. Returns `status` to the operating system

### Status Codes

Use the portable macros from `<stdlib.h>`:

|Macro|Value|Meaning|
|---|---|---|
|`EXIT_SUCCESS`|`0`|Program succeeded|
|`EXIT_FAILURE`|`1` (typically)|Program failed|

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp = fopen("data.txt", "r");
    if (fp == NULL) {
        perror("fopen");
        exit(EXIT_FAILURE);   // Flush stdio, run atexit handlers, then quit
    }

    // ... process file ...

    fclose(fp);
    exit(EXIT_SUCCESS);
}
```

### `exit()` vs `return` from `main()`

Returning from `main()` is almost identical to calling `exit()` — it flushes buffers and runs `atexit` handlers. Prefer `return` in `main()` for clarity; use `exit()` when terminating from a function deep in the call stack.

```c
int main(void) {
    return EXIT_SUCCESS;   // Equivalent to exit(EXIT_SUCCESS) here
}
```

> **Note:** `_Exit(status)` (C99) is a low-level variant that terminates immediately **without** calling `atexit` handlers or flushing stdio — useful in child processes after `fork()`.

---

## `atexit()` — Register Cleanup Handlers

### Syntax

```c
#include <stdlib.h>

int atexit(void (*func)(void));
```

Registers `func` to be called automatically when `exit()` is invoked (or `main()` returns). Returns `0` on success, non-zero on failure.

- The C standard guarantees support for **at least 32** registered functions.
- Functions are called in **LIFO order** (last registered, first called).
- Registered functions receive **no arguments** and return **nothing**.

### Basic Example

```c
#include <stdio.h>
#include <stdlib.h>

void cleanup_network(void) {
    printf("Closing network connections...\n");
}

void cleanup_database(void) {
    printf("Flushing database cache...\n");
}

int main(void) {
    atexit(cleanup_network);   // Registered first → called last
    atexit(cleanup_database);  // Registered last  → called first

    printf("Program running...\n");
    exit(EXIT_SUCCESS);
}
```

Output:

```
Program running...
Flushing database cache...
Closing network connections...
```

### Practical Pattern: Resource Cleanup

```c
#include <stdio.h>
#include <stdlib.h>

static FILE *log_file = NULL;

void close_log(void) {
    if (log_file) {
        fprintf(log_file, "Session ended.\n");
        fclose(log_file);
        log_file = NULL;
    }
}

int init_logging(const char *path) {
    log_file = fopen(path, "a");
    if (!log_file) return -1;

    atexit(close_log);  // Guaranteed to close even if exit() is called anywhere
    return 0;
}

int main(void) {
    if (init_logging("app.log") != 0) {
        fprintf(stderr, "Failed to open log\n");
        exit(EXIT_FAILURE);
    }

    fprintf(log_file, "Session started.\n");
    // ... application code ...
    return EXIT_SUCCESS;  // close_log() is called automatically
}
```

### What `atexit` Does NOT Do

- It is **not** called when `abort()` is used
- It is **not** called when the process is killed by a signal (e.g. `SIGKILL`)
- Handlers cannot accept arguments or communicate a status code back

---

## `abort()` — Abnormal Termination

### Syntax

```c
#include <stdlib.h>

void abort(void);
```

`abort()` terminates the program **abnormally** by raising `SIGABRT`. It:

- Does **not** call `atexit` handlers
- Does **not** flush `stdio` buffers
- Typically produces a **core dump** (on Unix systems)
- Returns an implementation-defined failure status to the OS

This is the function called internally by `assert()` when an assertion fails.

### Basic Example

```c
#include <stdio.h>
#include <stdlib.h>

void *safe_malloc(size_t n) {
    void *ptr = malloc(n);
    if (ptr == NULL) {
        fprintf(stderr, "Fatal: out of memory requesting %zu bytes\n", n);
        abort();  // This is an unrecoverable programmer/system error
    }
    return ptr;
}

int main(void) {
    int *data = safe_malloc(100 * sizeof(int));
    // ... use data ...
    free(data);
    return EXIT_SUCCESS;
}
```

### When to Use `abort()`

Use `abort()` when the program has reached a state that is:

- **Logically impossible** — an invariant has been violated so badly that continuing would corrupt data or be dangerous
- **Unrecoverable** — there is no sensible way to clean up and carry on

```c
typedef enum { SHAPE_CIRCLE, SHAPE_RECT, SHAPE_COUNT } ShapeKind;

double area(ShapeKind kind, double a, double b) {
    switch (kind) {
        case SHAPE_CIRCLE: return 3.14159 * a * a;
        case SHAPE_RECT:   return a * b;
        default:
            // This branch should be unreachable. If we get here,
            // there is a serious bug — abort rather than return garbage.
            fprintf(stderr, "area(): unknown ShapeKind %d\n", kind);
            abort();
    }
}
```

---

## `qsort()` — Generic Quicksort

### Syntax

```c
#include <stdlib.h>

void qsort(void *base, size_t nmemb, size_t size,
           int (*compar)(const void *, const void *));
```

|Parameter|Meaning|
|---|---|
|`base`|Pointer to the first element of the array|
|`nmemb`|Number of elements in the array|
|`size`|Size in bytes of each element (`sizeof(element)`)|
|`compar`|Comparator function (see below)|

`qsort` is fully **generic** — it works on any array type via `void *` and a caller-supplied comparator. The C standard does not mandate quicksort specifically; the implementation may use any algorithm.

### The Comparator Function

The comparator must return:

|Return value|Meaning|
|---|---|
|**negative**|First argument should come **before** second|
|**zero**|Arguments are **equal** (order between them is unspecified)|
|**positive**|First argument should come **after** second|

```c
int compar(const void *a, const void *b);
```

The comparator receives **pointers to elements**, not the elements themselves. You must cast them appropriately.

### Sorting Integers

```c
#include <stdio.h>
#include <stdlib.h>

int cmp_int(const void *a, const void *b) {
    int x = *(const int *)a;
    int y = *(const int *)b;
    // Safe comparison idiom — avoids integer overflow
    return (x > y) - (x < y);
}

int main(void) {
    int nums[] = { 42, 7, 19, 3, 55, 1 };
    size_t n = sizeof(nums) / sizeof(nums[0]);

    qsort(nums, n, sizeof(int), cmp_int);

    for (size_t i = 0; i < n; i++)
        printf("%d ", nums[i]);
    printf("\n");
    // Output: 1 3 7 19 42 55
    return EXIT_SUCCESS;
}
```

> ⚠️ **Avoid the raw subtraction trick** (`return x - y`) for integers — it overflows when values span negative and positive ranges. Use the comparison idiom above: `(x > y) - (x < y)`.

### Sorting Strings

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int cmp_str(const void *a, const void *b) {
    // a and b are pointers to (char *) elements
    return strcmp(*(const char **)a, *(const char **)b);
}

int main(void) {
    const char *words[] = { "banana", "apple", "cherry", "date" };
    size_t n = sizeof(words) / sizeof(words[0]);

    qsort(words, n, sizeof(char *), cmp_str);

    for (size_t i = 0; i < n; i++)
        printf("%s\n", words[i]);
    // Output: apple, banana, cherry, date
    return EXIT_SUCCESS;
}
```

### Sorting Structs

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[32];
    int  score;
} Player;

// Sort by score descending, then name ascending on tie
int cmp_player(const void *a, const void *b) {
    const Player *pa = (const Player *)a;
    const Player *pb = (const Player *)b;

    if (pb->score != pa->score)
        return pb->score - pa->score;       // Higher score first
    return strcmp(pa->name, pb->name);      // Alphabetical on tie
}

int main(void) {
    Player players[] = {
        { "Alice", 95 },
        { "Bob",   87 },
        { "Carol", 95 },
        { "Dave",  72 },
    };
    size_t n = sizeof(players) / sizeof(players[0]);

    qsort(players, n, sizeof(Player), cmp_player);

    for (size_t i = 0; i < n; i++)
        printf("%-10s %d\n", players[i].name, players[i].score);
    return EXIT_SUCCESS;
}
```

Output:

```
Alice      95
Carol      95
Bob        87
Dave       72
```

### Sorting in Reverse

To reverse any sort order, swap `a` and `b` in the comparator:

```c
int cmp_int_desc(const void *a, const void *b) {
    int x = *(const int *)a;
    int y = *(const int *)b;
    return (y > x) - (y < x);  // Note: y before x for descending
}
```

### `qsort` Stability

`qsort` is **not guaranteed to be stable**. Equal elements may appear in any order relative to each other after the sort. If stability matters, either:

- Include a tiebreaker in your comparator (as shown in the struct example above), or
- Use a stable sort from an external library

---

## Comparing the Termination Functions

||`exit()`|`_Exit()`|`abort()`|`return` from `main`|
|---|---|---|---|---|
|Calls `atexit` handlers|✅ Yes|❌ No|❌ No|✅ Yes|
|Flushes stdio buffers|✅ Yes|❌ No|❌ No|✅ Yes|
|Produces core dump|❌ No|❌ No|✅ Typically|❌ No|
|Raises signal|❌ No|❌ No|`SIGABRT`|❌ No|
|Use case|Normal exit|After `fork()`|Unrecoverable bug|Normal exit from `main`|

---

## Best Practices

### Register cleanup with `atexit` close to resource acquisition

```c
// ✅ Register the handler immediately after acquiring the resource
// so there's no window where the resource is open but unguarded.
db = db_connect(host);
if (!db) { exit(EXIT_FAILURE); }
atexit(db_disconnect);
```

### Prefer `EXIT_SUCCESS` / `EXIT_FAILURE` over raw integers

```c
// ❌ Magic numbers — non-portable and unclear
exit(0);
exit(1);

// ✅ Self-documenting and portable
exit(EXIT_SUCCESS);
exit(EXIT_FAILURE);
```

### Use `abort()` for unreachable code paths

```c
// ✅ Better than returning a dummy value from a logically unreachable branch
default:
    fprintf(stderr, "Impossible state: %d\n", state);
    abort();
```

### Always get `sizeof` right in `qsort`

```c
// ❌ Wrong — passes size of the array pointer, not size of one element
qsort(arr, n, sizeof(arr), cmp);

// ✅ Correct
qsort(arr, n, sizeof(arr[0]), cmp);
```

---

## Common Pitfalls

### Pitfall 1: Calling `exit()` from an `atexit` handler

Calling `exit()` from within an `atexit` handler produces **undefined behaviour**.

```c
// ❌ WRONG — undefined behaviour
void bad_handler(void) {
    exit(EXIT_FAILURE);
}
```

### Pitfall 2: Incorrect pointer casting in `qsort` comparator

```c
// ❌ WRONG — casting void* directly to int without dereferencing properly
int cmp_bad(const void *a, const void *b) {
    return (int)a - (int)b;  // Compares addresses, not values!
}

// ✅ CORRECT
int cmp_good(const void *a, const void *b) {
    int x = *(const int *)a;
    int y = *(const int *)b;
    return (x > y) - (x < y);
}
```

### Pitfall 3: Integer overflow in comparator subtraction

```c
// ❌ Overflows when a = INT_MIN, b = 1  →  INT_MIN - 1 wraps around
int cmp_overflow(const void *a, const void *b) {
    return *(const int *)a - *(const int *)b;
}

// ✅ Safe — no arithmetic, no overflow possible
int cmp_safe(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}
```

### Pitfall 4: Expecting `abort()` to call cleanup handlers

```c
static FILE *fp = NULL;

void cleanup(void) { if (fp) fclose(fp); }  // Never called on abort()

int main(void) {
    fp = fopen("out.txt", "w");
    atexit(cleanup);
    // ...
    abort();  // cleanup() is NOT invoked — fp is NOT flushed or closed
}
```

If cleanup on abnormal exit is required, install a `SIGABRT` signal handler — but note that behaviour after returning from it is implementation-defined.

### Pitfall 5: Side effects stripped by `NDEBUG` reaching `abort()`

If you rely on `assert()` to catch bugs that then fall through to `abort()`, remember that defining `NDEBUG` removes all `assert()` calls entirely. The `abort()` inside `assert` is gone too. Write explicit checks for truly unrecoverable conditions rather than relying solely on assertions.

---

## Quick Reference

```c
#include <stdlib.h>

// Terminate normally — flushes stdio, runs atexit handlers
exit(EXIT_SUCCESS);
exit(EXIT_FAILURE);

// Register a no-argument cleanup function (LIFO order, max >= 32)
atexit(my_cleanup_function);

// Terminate abnormally — raises SIGABRT, may dump core, skips cleanup
abort();

// Sort an array generically
qsort(array, num_elements, sizeof(array[0]), comparator_function);

// Comparator template (ascending)
int cmp(const void *a, const void *b) {
    const MyType *x = (const MyType *)a;
    const MyType *y = (const MyType *)b;
    return (x->key > y->key) - (x->key < y->key);
}
```

---

_Standard references: ISO/IEC 9899:2011 (C11) §7.22.4 — Communication with the environment; §7.22.5 — Searching and sorting utilities_
# `memcpy` and `memmove` in C

A practical guide to memory copying functions in C — what they do, how they differ, and when to use each.

---

## Overview

Both `memcpy` and `memmove` are standard library functions declared in `<string.h>`. They copy a block of bytes from a source address to a destination address. The key difference lies in how they handle **overlapping memory regions**.

---

## `memcpy`

### Signature

```c
void *memcpy(void *dest, const void *src, size_t n);
```

### Description

Copies exactly `n` bytes from `src` to `dest`. It assumes the source and destination memory regions **do not overlap**. If they do, the behavior is **undefined**.

### Example

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char src[] = "Hello, World!";
    char dest[20];

    memcpy(dest, src, strlen(src) + 1); // +1 to copy the null terminator

    printf("src:  %s\n", src);
    printf("dest: %s\n", dest);

    return 0;
}
```

**Output:**

```
src:  Hello, World!
dest: Hello, World!
```

### Key Points

- **Fast** — compilers and standard libraries heavily optimize `memcpy`, often using SIMD instructions.
- **No overlap safety** — passing overlapping regions is undefined behavior (UB); the result may be corrupt data or crashes.
- **Does not null-terminate** strings automatically — you must account for `\0` manually.
- Returns `dest`.

---

## `memmove`

### Signature

```c
void *memmove(void *dest, const void *src, size_t n);
```

### Description

Copies exactly `n` bytes from `src` to `dest`, **safely handling overlapping memory regions**. It behaves as if the bytes were first copied to a temporary buffer, then written to `dest`.

### Example — Overlapping Regions

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char buf[] = "ABCDEFGH";

    // Shift contents 2 positions to the right (overlapping!)
    memmove(buf + 2, buf, 6);

    printf("%s\n", buf); // Output: ABABCDEF

    return 0;
}
```

**Output:**

```
ABABCDEF
```

> Using `memcpy` here would be undefined behavior because `buf` and `buf + 2` overlap.

### Key Points

- **Overlap-safe** — internally checks whether `dest` is before or after `src` and copies in the appropriate direction.
- **Slightly slower** than `memcpy` due to the overlap check, though the difference is negligible in most scenarios.
- Returns `dest`.

---

## Side-by-Side Comparison

|Feature|`memcpy`|`memmove`|
|---|---|---|
|Header|`<string.h>`|`<string.h>`|
|Handles overlapping regions|❌ No (UB)|✅ Yes|
|Performance|Faster|Slightly slower|
|Return value|`dest`|`dest`|
|Null-terminates strings|No|No|
|Safe default choice|Only when no overlap|Always|

---

## Common Pitfalls

### 1. Using `memcpy` on Overlapping Memory

```c
char buf[] = "123456";

// WRONG: overlaps — undefined behavior
memcpy(buf + 2, buf, 4);

// CORRECT: use memmove for overlapping regions
memmove(buf + 2, buf, 4);
```

### 2. Forgetting the Null Terminator

```c
char src[] = "hello";
char dest[10];

memcpy(dest, src, strlen(src)); // Copies "hello" but NO null terminator!
dest[strlen(src)] = '\0';       // Must add it manually

// Or simpler:
memcpy(dest, src, strlen(src) + 1); // Copies null terminator too
```

### 3. Wrong Byte Count with Non-char Types

```c
int src[] = {1, 2, 3, 4};
int dest[4];

// WRONG: only copies 4 bytes (1 int on most platforms)
memcpy(dest, src, 4);

// CORRECT: use sizeof to get the right byte count
memcpy(dest, src, sizeof(src));         // entire array
memcpy(dest, src, 4 * sizeof(int));     // explicit element count
```

### 4. NULL Pointers

Passing a `NULL` pointer as `src` or `dest` is undefined behavior, even if `n == 0`. Always validate pointers before calling these functions.

---

## Practical Usage Patterns

### Copying a Struct

```c
typedef struct {
    int id;
    float value;
} Record;

Record a = {1, 3.14f};
Record b;

memcpy(&b, &a, sizeof(Record));
```

### Implementing a Circular Buffer Shift

```c
char buf[64] = "old data here...";
size_t offset = 4;

// Shift buffer contents left by `offset` bytes
memmove(buf, buf + offset, sizeof(buf) - offset);
```

### Zeroing Memory (use `memset` instead)

```c
// Don't use memcpy to zero memory — use memset
memset(dest, 0, sizeof(dest));
```

---

## When to Use Which

```
Do src and dest overlap (or might they)?
        │
       Yes ──────────────────► use memmove
        │
       No
        │
       ▼
    Use memcpy  (faster, compiler-optimizable)
```

When in doubt, **prefer `memmove`** — the performance difference is rarely meaningful, and it eliminates an entire class of subtle bugs.

---

## Quick Reference

```c
#include <string.h>

// Copy n bytes — no overlap allowed
void *memcpy(void *dest, const void *src, size_t n);

// Copy n bytes — overlap safe
void *memmove(void *dest, const void *src, size_t n);
```

---

_Standard: C89 and later. Both functions are defined in ISO C and POSIX._
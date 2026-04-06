# Assertions in C: `assert` and `static_assert`

A practical guide to compile-time and runtime contract enforcement in C.

---

## Table of Contents

1. [[#What Is an Assertion?]]
2. [[#Runtime Assertions with `assert()`]]
3. [[#Disabling Assertions]]
4. [[#Writing Useful Assertion Messages]]
5. [[#Static Assertions with `static_assert`]]
6. [[#Comparing `assert` vs `static_assert`]]
7. [[#Best Practices]]
8. [[#Common Pitfalls]]

---

## What Is an Assertion?

An **assertion** is a sanity check — a condition you declare _must_ be true at a specific point in your program. If it isn't, something has gone seriously wrong.

Assertions are not error handling. They are developer tools that:

- Document assumptions in code
- Catch bugs early during development
- Fail loudly and immediately instead of silently corrupting state

There are two kinds in C:

|Kind|Header|When it checks|Failure result|
|---|---|---|---|
|`assert(expr)`|`<assert.h>`|At runtime|Aborts the program|
|`static_assert(expr, msg)`|`<assert.h>` (C11+)|At compile time|Compilation error|

---

## Runtime Assertions with `assert()`

### Syntax

```c
#include <assert.h>

assert(expression);
```

If `expression` evaluates to **zero (false)**, the program:

1. Prints a diagnostic message to `stderr`
2. Calls `abort()`, terminating immediately

### Basic Example

```c
#include <assert.h>
#include <stdio.h>

int divide(int a, int b) {
    assert(b != 0);  // Precondition: divisor must not be zero
    return a / b;
}

int main(void) {
    printf("%d\n", divide(10, 2));  // OK: prints 5
    printf("%d\n", divide(10, 0));  // FAILS: aborts with diagnostic
    return 0;
}
```

### What the Failure Output Looks Like

```
main.c:5: divide: Assertion `b != 0' failed.
Aborted (core dumped)
```

The message includes:

- **File name** (`main.c`)
- **Line number** (`5`)
- **Function name** (`divide`) — in C99 and later
- **The failed expression** (`b != 0`)

### Where to Use `assert()`

```c
// ✅ Preconditions — validate inputs to a function
void set_age(Person *p, int age) {
    assert(p != NULL);
    assert(age >= 0 && age <= 150);
    p->age = age;
}

// ✅ Postconditions — validate what a function produced
int *create_buffer(size_t n) {
    int *buf = malloc(n * sizeof(int));
    assert(buf != NULL);  // Catches OOM in debug builds
    return buf;
}

// ✅ Invariants — validate internal state mid-algorithm
void sort(int *arr, size_t n) {
    // ... sorting logic ...
    assert(is_sorted(arr, n));  // Verify correctness
}
```

---

## Disabling Assertions

Define `NDEBUG` **before** including `<assert.h>` (or pass it as a compiler flag) to strip all `assert()` calls from the binary:

```c
#define NDEBUG
#include <assert.h>
```

Or on the command line:

```sh
gcc -DNDEBUG -O2 main.c -o main
```

When `NDEBUG` is defined, `assert(expr)` expands to `((void)0)` — a complete no-op. This means:

> ⚠️ **Never put side-effecting code inside `assert()`.**

```c
// ❌ WRONG — items_processed is never incremented in release builds
assert(items_processed++ < MAX_ITEMS);

// ✅ CORRECT — separate the side effect from the check
items_processed++;
assert(items_processed <= MAX_ITEMS);
```

---

## Writing Useful Assertion Messages

The standard `assert()` only shows the expression. For more context, a common idiom uses the `&&` trick with a string literal:

```c
// The string literal is always truthy, so it doesn't affect the logic.
// But it appears in the failure message.
assert(index < size && "Index out of bounds");
assert(ptr != NULL && "Pointer must be initialised before use");
```

Failure output:

```
main.c:12: process: Assertion `index < size && "Index out of bounds"' failed.
```

---

## Static Assertions with `static_assert`

Introduced in **C11**, `static_assert` checks a condition at **compile time**. If the condition is false, compilation fails with your custom error message.

### Syntax

```c
// C11 — requires <assert.h>
static_assert(constant_expression, "message string");

// C23 — message is optional
static_assert(constant_expression);
```

The expression must be a **integer constant expression** — something the compiler can evaluate without running the program.

### Basic Example

```c
#include <assert.h>
#include <stdint.h>

// Ensure the platform uses 8-bit bytes (required by our protocol code)
static_assert(sizeof(char) == 1, "char must be exactly 1 byte");

// Ensure int is at least 32 bits
static_assert(sizeof(int) >= 4, "int must be at least 32 bits wide");

int main(void) {
    return 0;
}
```

If the condition fails, the compiler outputs something like:

```
main.c:4:1: error: static assertion failed: "char must be exactly 1 byte"
```

### Practical Use Cases

#### 1. Struct size and alignment

```c
typedef struct {
    uint8_t  type;      // 1 byte
    uint8_t  flags;     // 1 byte
    uint16_t length;    // 2 bytes
    uint32_t payload;   // 4 bytes
} PacketHeader;

// Guarantee no hidden padding — critical for network/file protocols
static_assert(sizeof(PacketHeader) == 8,
              "PacketHeader must be exactly 8 bytes (check for padding)");
```

#### 2. Enum completeness

```c
typedef enum { RED, GREEN, BLUE, COLOR_COUNT } Color;

// Catch when someone adds a color but forgets to update the lookup table
static const char *color_names[COLOR_COUNT] = { "red", "green", "blue" };

static_assert(sizeof(color_names) / sizeof(color_names[0]) == COLOR_COUNT,
              "color_names table is out of sync with Color enum");
```

#### 3. Platform / type portability

```c
#include <stdint.h>

// Ensure we're compiling for a 64-bit target
static_assert(sizeof(void *) == 8, "This code requires a 64-bit platform");

// Ensure fixed-width types are actually available and sized correctly
static_assert(sizeof(int32_t) == 4, "int32_t must be 32 bits");
static_assert(sizeof(uint64_t) == 8, "uint64_t must be 64 bits");
```

#### 4. Inside functions (C11+)

`static_assert` can appear anywhere a declaration is valid, including inside a function body:

```c
void process_record(Record *r) {
    static_assert(sizeof(Record) <= 64,
                  "Record must fit in a cache line");
    // ...
}
```

---

## Comparing `assert` vs `static_assert`

|Feature|`assert(expr)`|`static_assert(expr, msg)`|
|---|---|---|
|When evaluated|**Runtime**|**Compile time**|
|Expression type|Any expression|Constant integer expression|
|Can use variables|✅ Yes|❌ No (constants only)|
|Can check sizes/types|Limited|✅ Yes — ideal use case|
|Disabled by `NDEBUG`|✅ Yes|❌ No — always active|
|Custom error message|Workaround needed|✅ Built in|
|Performance cost|Minimal (branch)|Zero (compile time)|
|C standard|C89|C11|

**Rule of thumb:**

> Use `static_assert` for anything the compiler _can_ check.  
> Use `assert` for everything else.

---

## Best Practices

### Do use assertions to document assumptions

```c
// Without assertion — silent assumption
Node *next = node->next;

// With assertion — assumption is explicit and enforced
assert(node != NULL && "node must not be NULL before traversal");
Node *next = node->next;
```

### Do prefer `static_assert` for type/size guarantees

These checks cost nothing at runtime and catch portability bugs immediately:

```c
static_assert(sizeof(off_t) == 8, "Large file support (LFS) required");
```

### Don't use assertions for user input validation

`assert` is for catching _programmer mistakes_, not for handling bad data from users or files:

```c
// ❌ Wrong — user could supply a bad value; assert should not be user-facing
int age = atoi(argv[1]);
assert(age > 0);

// ✅ Correct — proper error handling for external input
int age = atoi(argv[1]);
if (age <= 0) {
    fprintf(stderr, "Error: age must be a positive integer\n");
    return EXIT_FAILURE;
}
```

### Don't suppress assertions in tests

Leave assertions on during unit testing — they are your safety net.

---

## Common Pitfalls

### Pitfall 1: Side effects inside `assert`

```c
// ❌ WRONG — completely broken in release builds
assert(connect(socket, addr, len) == 0);

// ✅ CORRECT
int result = connect(socket, addr, len);
assert(result == 0);
```

### Pitfall 2: Using `assert` instead of proper error handling

```c
// ❌ Wrong — malloc can legitimately fail in production
int *buf = malloc(n);
assert(buf != NULL);

// ✅ Better — handle the error gracefully
int *buf = malloc(n);
if (!buf) {
    perror("malloc");
    return NULL;
}
```

### Pitfall 3: Forgetting `NDEBUG` strips everything

In production builds with `-DNDEBUG`, every `assert()` becomes a no-op. Security checks, resource cleanup, or any logic inside `assert()` **will not run**.

### Pitfall 4: Expecting `static_assert` to work with runtime values

```c
void foo(size_t n) {
    // ❌ Error: n is not a constant expression
    static_assert(n > 0, "n must be positive");

    // ✅ Use runtime assert for variable checks
    assert(n > 0);
}
```

---

## Quick Reference

```c
#include <assert.h>

// Runtime assertion (debug builds only)
assert(ptr != NULL);
assert(index < size && "Out of bounds");

// Static assertion (compile time, always active)
static_assert(sizeof(MyStruct) == 16, "Unexpected struct size");
static_assert(sizeof(int) >= 4,       "int too narrow for this code");

// Disable runtime assertions for release builds:
// gcc -DNDEBUG file.c
```

---

_Standard references: ISO/IEC 9899:2011 (C11) §7.2 — Diagnostics `<assert.h>`_
This is an important and subtle topic in C. This note explain **how const behaves across multiple files**, and when to use **static vs extern**—with clear rules and examples.

---
## 1. The Core Issue:  `const`  and Linkage

In C (unlike C++):

> A **file-scope const variable has external linkage by default**

> **unless** you explicitly make it static.

That means this:

```c
const int x = 10;
```

- Is a **definition**
- Has **external linkage**
- Can cause **multiple definition linker errors** if placed in a header

This surprises many programmers.

---

## 2. ❌ The Common Mistake: `const` in a Header

### header.h

```c
const int MAX_SIZE = 100;
```

### file1.c / file2.c

```c
#include "header.h"
```

### What happens?

Each .c file gets its own definition of MAX_SIZE.

➡ **Linker error**:

```c
multiple definition of `MAX_SIZE`
```

---

## 3. Solution 1: `static const` in a Header (Most Common)

### header.h

```c
static const int MAX_SIZE = 100;
```

### What this means

- static → **internal linkage**
- Each .c file gets **its own private copy**
- No linker conflicts
### When to use this

✔ Constants used like macros
✔ Header-only constants
✔ Compile-time configuration values
### Example

```c
// math_constants.h
static const double PI = 3.141592653589793;
```

Safe to include everywhere.

---

## 4. Solution 2: `extern const` (Single Global Constant)

Use this when you want **one shared global constant** across files.
### Step 1: Declare in Header (NO initialization)

```c
// config.h
extern const int MAX_USERS;
```
### Step 2: Define in Exactly ONE Source File

```c
// config.c
#include "config.h"

const int MAX_USERS = 100;
```
### Step 3: Use Anywhere

```
// main.c
#include "config.h"

printf("%d\n", MAX_USERS);
```

### When to use  extern const

✔ Large tables
✔ Shared configuration values
✔ Memory-mapped constants
✔ API-level constants

---

## 5. `const` Globals vs  `#define`

| **Feature**   | const | `#define` |
| ------------- | ----- | --------- |
| Type safety   | ✅     | ❌         |
| Debuggable    | ✅     | ❌         |
| Takes address | ✅     | ❌         |
| Scope control | ✅     | ❌         |

Prefer const unless:
- You need preprocessor logic
- You need compile-time constants for array sizes (pre-C99)

---

## 6. `const` and Arrays Across Files

### **Header**

```c
extern const int lookup_table[256];
```

### **Source**

```c
const int lookup_table[256] = {
    /* values */
};
```

✔ Correct
✔ Single definition
✔ Read-only intent

---
## **7.**  `static const`  vs `extern const` — Quick Rule

> **Ask yourself:** “Do I want ONE shared object or MANY private ones?”

|**Goal**|**Use**|
|---|---|
|Header-only constant|static const|
|One global constant|extern const|
|Private to one .c file|static const in .c|

---

## 8. `const` in Headers: Decision Table

|**Scenario**|**Correct Pattern**|
|---|---|
|Small numeric constant|static const in header|
|Public API constant|extern const|
|Private constant|static const in .c|
|Compile-time macro|#define|

---

## 9. Key Takeaway

- const **does not imply internal linkage**
- Headers must avoid **definitions with external linkage**
- Use:
    - static const → safe in headers
    - extern const → shared global constant
- Think of const as **“read-only,” not “header-safe”**
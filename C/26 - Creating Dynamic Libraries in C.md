## What is a Dynamic Library?

A **dynamic library** (also called a shared library) is a compiled collection of code that is loaded into memory at runtime rather than being compiled directly into your executable. This contrasts with static libraries (`.a`), which are embedded into the binary at link time.

Dynamic libraries use the `.so` extension on Linux/Unix and `.dll` on Windows. This tutorial focuses on Linux/Unix systems.

**Benefits of dynamic libraries:**

- Multiple programs can share a single copy in memory
- Update the library without recompiling programs that use it
- Smaller executable sizes
- Supports plugin architectures

---

## Step 1: Write Your Library Source Code

Create the header file and implementation file for your library.

**`mathlib.h`** — Public API (header file)

```c
#ifndef MATHLIB_H
#define MATHLIB_H

// Add two integers
int add(int a, int b);

// Subtract two integers
int subtract(int a, int b);

// Multiply two integers
int multiply(int a, int b);

// Divide two doubles (returns 0.0 on division by zero)
double divide(double a, double b);

#endif // MATHLIB_H
```

**`mathlib.c`** — Implementation

```c
#include "mathlib.h"
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

double divide(double a, double b) {
    if (b == 0.0) {
        fprintf(stderr, "Error: division by zero\n");
        return 0.0;
    }
    return a / b;
}
```

---

## Step 2: Compile to Position-Independent Code (PIC)

Dynamic libraries must be compiled with the `-fPIC` flag, which generates **Position-Independent Code** — code that can be loaded at any memory address.

```bash
gcc -c -fPIC mathlib.c -o mathlib.o
```

|Flag|Description|
|---|---|
|`-c`|Compile only, do not link|
|`-fPIC`|Generate position-independent code|
|`-o mathlib.o`|Output object file name|

---

## Step 3: Create the Shared Library

Link the object file into a shared library using `-shared`:

```bash
gcc -shared -o libmathlib.so mathlib.o
```

> **Naming Convention:** Shared libraries must be named with the `lib` prefix (e.g., `libmathlib.so`). This is required for the linker's `-l` flag to find them.

You can combine compilation and linking in one step:

```bash
gcc -shared -fPIC mathlib.c -o libmathlib.so
```

---

## Step 4: Write a Program That Uses the Library

**`main.c`**

```c
#include <stdio.h>
#include "mathlib.h"

int main() {
    int a = 20, b = 4;

    printf("add(%d, %d)      = %d\n", a, b, add(a, b));
    printf("subtract(%d, %d)  = %d\n", a, b, subtract(a, b));
    printf("multiply(%d, %d)  = %d\n", a, b, multiply(a, b));
    printf("divide(%d, %d)    = %.2f\n", a, b, divide(a, b));

    return 0;
}
```

---

## Step 5: Compile and Link Against the Library

```bash
gcc main.c -L. -lmathlib -o myapp
```

|Flag|Description|
|---|---|
|`-L.`|Look for libraries in the current directory (`.`)|
|`-lmathlib`|Link against `libmathlib.so` (drop the `lib` prefix and `.so` extension)|
|`-o myapp`|Output executable name|

---

## Step 6: Run the Program

Before running, the dynamic linker needs to find the library. You have a few options:

### Option A: Set `LD_LIBRARY_PATH` (Temporary)

```bash
export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH
./myapp
```

### Option B: Copy to a System Library Directory (Permanent)

```bash
sudo cp libmathlib.so /usr/local/lib/
sudo ldconfig
./myapp
```

### Option C: Use `-rpath` at Link Time

Embed the library search path directly in the executable:

```bash
gcc main.c -L. -lmathlib -Wl,-rpath,. -o myapp
./myapp
```

**Expected output:**

```
add(20, 4)      = 24
subtract(20, 4)  = 16
multiply(20, 4)  = 80
divide(20, 4)    = 5.00
```

---

## Step 7: Inspect Your Library (Optional but Useful)

```bash
# List exported symbols
nm -D libmathlib.so

# List shared library dependencies of your app
ldd myapp

# Inspect ELF headers
readelf -h libmathlib.so
```

---

## Dynamic Loading at Runtime with `dlopen`

You can also load shared libraries manually at runtime using the `<dlfcn.h>` API. This is the foundation of plugin systems.

**`plugin_loader.c`**

```c
#include <stdio.h>
#include <dlfcn.h>

int main() {
    // Open the shared library
    void *handle = dlopen("./libmathlib.so", RTLD_LAZY);
    if (!handle) {
        fprintf(stderr, "dlopen error: %s\n", dlerror());
        return 1;
    }

    // Clear any existing errors
    dlerror();

    // Load a function symbol
    int (*add_fn)(int, int) = dlsym(handle, "add");
    const char *error = dlerror();
    if (error) {
        fprintf(stderr, "dlsym error: %s\n", error);
        dlclose(handle);
        return 1;
    }

    // Call the function
    printf("add(10, 5) = %d\n", add_fn(10, 5));

    // Close the library
    dlclose(handle);
    return 0;
}
```

Compile with `-ldl` to link the dynamic loading library:

```bash
gcc plugin_loader.c -ldl -o plugin_loader
./plugin_loader
```

|`dlfcn.h` Function|Description|
|---|---|
|`dlopen(path, flags)`|Load a shared library|
|`dlsym(handle, symbol)`|Look up a symbol (function/variable)|
|`dlerror()`|Get last error message|
|`dlclose(handle)`|Unload the library|

**`RTLD_LAZY`** — Resolve symbols only when used (faster startup).  
**`RTLD_NOW`** — Resolve all symbols immediately (catches errors early).

---

## Versioning Your Library

It is good practice to version shared libraries so multiple versions can coexist:

```bash
# Create a versioned library
gcc -shared -fPIC mathlib.c -Wl,-soname,libmathlib.so.1 -o libmathlib.so.1.0.0

# Create symbolic links
ln -s libmathlib.so.1.0.0 libmathlib.so.1
ln -s libmathlib.so.1     libmathlib.so
```

The naming convention is:

```
libNAME.so.MAJOR.MINOR.PATCH
         │
         └── soname (used by the linker at runtime)
```

---

## Common Errors and Fixes

|Error|Cause|Fix|
|---|---|---|
|`cannot open shared object file`|Library not found at runtime|Set `LD_LIBRARY_PATH` or run `ldconfig`|
|`undefined symbol`|Function not exported or misspelled|Check `nm -D libname.so`|
|`relocation error`|Forgot `-fPIC` during compilation|Recompile with `-fPIC`|
|`wrong ELF class`|32-bit vs 64-bit mismatch|Ensure consistent architecture flags|

---

## Project File Structure

```
project/
├── mathlib.h          # Public header
├── mathlib.c          # Library source
├── main.c             # Application source
├── libmathlib.so      # Compiled shared library
└── myapp              # Compiled executable
```

---

## Quick Reference: Full Build Workflow

```bash
# 1. Compile source to position-independent object
gcc -c -fPIC mathlib.c -o mathlib.o

# 2. Link into shared library
gcc -shared mathlib.o -o libmathlib.so

# 3. Compile and link application
gcc main.c -L. -lmathlib -o myapp

# 4. Set library path and run
LD_LIBRARY_PATH=. ./myapp
```

---

## Summary

|Concept|Key Point|
|---|---|
|Compile flag|Always use `-fPIC` for shared libraries|
|Link flag|Use `-shared` to produce a `.so` file|
|Naming|Library files must start with `lib`|
|Linking app|Use `-L<dir>` and `-l<name>` (without `lib` prefix)|
|Runtime path|Set `LD_LIBRARY_PATH` or use `ldconfig`|
|Runtime loading|Use `dlopen` / `dlsym` from `<dlfcn.h>`|

Dynamic libraries are a powerful tool for building modular, maintainable C software. Once you understand the compile → link → load lifecycle, you can build plugin systems, reduce binary bloat, and ship library updates independently of the applications that use them.
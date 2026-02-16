
---

## What is a Static Library?

A static library is a collection of compiled object files bundled into a single archive file. When you link a static library into your program, the relevant code is copied directly into the final executable at compile time. The resulting binary is self-contained and has no runtime dependency on the library file.

On Linux/macOS, static libraries use the `.a` extension (archive). On Windows, they use `.lib`.

---

## Why Use a Static Library?

- **Code reuse** — write utility functions once, use them across many projects
- **Faster startup** — no dynamic linking overhead at runtime
- **Portability** — the executable carries everything it needs
- **Encapsulation** — expose only a clean public header interface

---

## The Workflow at a Glance

```
source files (.c)  →  object files (.o)  →  archive (.a)  →  link into executable
```

---

## Step-by-Step Tutorial

### Step 1 — Write Your Library Source Files

Create the functions you want to package. For this example, we'll build a simple `mathutils` library.

**mathutils.h** (the public interface)

```c
#ifndef MATHUTILS_H
#define MATHUTILS_H

int  add(int a, int b);
int  subtract(int a, int b);
int  multiply(int a, int b);
double divide(double a, double b);

#endif
```

**mathutils.c** (the implementation)

```c
#include "mathutils.h"
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

You can split a library across multiple `.c` files — each file compiles into its own object file.

---

### Step 2 — Compile to Object Files

Compile each `.c` file with the `-c` flag. This produces `.o` object files without linking.

```bash
gcc -c mathutils.c -o mathutils.o
```

For multiple source files:

```bash
gcc -c mathutils.c   -o mathutils.o
gcc -c stringutils.c -o stringutils.o
gcc -c fileutils.c   -o fileutils.o
```

> **Good practice:** use `-Wall -Wextra` to catch warnings early, and `-fPIC` if you may later want a shared version.

```bash
gcc -Wall -Wextra -c mathutils.c -o mathutils.o
```

---

### Step 3 — Bundle into a Static Library with `ar`

Use the `ar` (archiver) tool to pack all your `.o` files into a `.a` archive.

```bash
ar rcs libmathutils.a mathutils.o
```

For multiple object files:

```bash
ar rcs libmathutils.a mathutils.o stringutils.o fileutils.o
```

**The `ar` flags explained:**

|Flag|Meaning|
|---|---|
|`r`|Insert or replace members in the archive|
|`c`|Create the archive if it doesn't exist|
|`s`|Write an index (symbol table) into the archive|

> **Naming convention:** static libraries must be named `lib<name>.a`. The `lib` prefix is required so the linker can find them with the `-l` flag.

---

### Step 4 — Inspect the Library (Optional but Useful)

List the object files bundled in the archive:

```bash
ar t libmathutils.a
```

View the symbol table (exported functions and variables):

```bash
nm libmathutils.a
```

Sample `nm` output:

```
mathutils.o:
0000000000000000 T add
0000000000000010 T subtract
0000000000000020 T multiply
0000000000000030 T divide
```

`T` means the symbol is in the text (code) section — these are your exported functions.

---

### Step 5 — Write a Program That Uses the Library

**main.c**

```c
#include <stdio.h>
#include "mathutils.h"

int main(void) {
    printf("add(3, 4)        = %d\n",    add(3, 4));
    printf("subtract(10, 3)  = %d\n",    subtract(10, 3));
    printf("multiply(6, 7)   = %d\n",    multiply(6, 7));
    printf("divide(22.0, 7.0)= %.4f\n",  divide(22.0, 7.0));
    return 0;
}
```

---

### Step 6 — Compile and Link Against the Library

```bash
gcc main.c -L. -lmathutils -o myprogram
```

**Flag breakdown:**

|Flag|Meaning|
|---|---|
|`-L.`|Look for libraries in the current directory (`.`)|
|`-lmathutils`|Link with `libmathutils.a` (the `lib` prefix and `.a` are implicit)|
|`-o myprogram`|Name the output executable `myprogram`|

You can also specify the include path explicitly if the header is in a different directory:

```bash
gcc main.c -I./include -L./lib -lmathutils -o myprogram
```

---

### Step 7 — Run It

```bash
./myprogram
```

Expected output:

```
add(3, 4)        = 7
subtract(10, 3)  = 7
multiply(6, 7)   = 42
divide(22.0, 7.0)= 3.1429
```

---

## Recommended Project Layout

```
project/
├── include/
│   └── mathutils.h        ← public headers
├── src/
│   └── mathutils.c        ← library source
├── lib/
│   └── libmathutils.a     ← compiled library (generated)
├── obj/
│   └── mathutils.o        ← object files (generated)
└── main.c                 ← consumer program
```

Build commands for this layout:

```bash
gcc -Wall -c src/mathutils.c -I include -o obj/mathutils.o
ar rcs lib/libmathutils.a obj/mathutils.o
gcc main.c -I include -L lib -lmathutils -o myprogram
```

---

## Using a Makefile

Managing these commands manually gets tedious. A `Makefile` automates the build:

```makefile
CC      = gcc
CFLAGS  = -Wall -Wextra
AR      = ar
ARFLAGS = rcs

SRC     = src/mathutils.c
OBJ     = obj/mathutils.o
LIB     = lib/libmathutils.a
TARGET  = myprogram

all: $(TARGET)

$(OBJ): $(SRC)
	$(CC) $(CFLAGS) -c $< -I include -o $@

$(LIB): $(OBJ)
	$(AR) $(ARFLAGS) $@ $^

$(TARGET): main.c $(LIB)
	$(CC) $(CFLAGS) main.c -I include -L lib -l mathutils -o $@

clean:
	rm -f $(OBJ) $(LIB) $(TARGET)
```

Run with:

```bash
make        # build everything
make clean  # remove generated files
```

---

## Key Points to Remember

- Always name your library `lib<name>.a` — the `lib` prefix is mandatory for `-l` to work
- Use `ar rcs` — the `s` flag generates a symbol index, which speeds up linking
- The `-L` flag sets the library search path; `-l` names the library to link
- Headers (`.h`) are **not** part of the library archive — distribute them separately
- Static libraries embed code into the binary; changes to the library require recompiling the program

---

## Quick Reference Card

```
# Compile to object file
gcc -c source.c -o source.o

# Create static library
ar rcs libname.a file1.o file2.o

# List archive contents
ar t libname.a

# View exported symbols
nm libname.a

# Link against static library
gcc main.c -L<lib_dir> -l<name> -o program
```
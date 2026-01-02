
# Flexible Array Members in C

Flexible Array Members (FAMs) allow you to define a struct whose **last member is an array with no fixed size**, enabling efficient, contiguous allocation of variable-sized data.

==They are standardized in **C99** and later.==
## 1. Motivation

Without flexible array members, variable-length data often requires:
- Separate heap allocations
- Pointer indirection
- More complex memory management  

Flexible array members let you store metadata and data **in one contiguous block**.
## 2. Basic Syntax

```c
struct packet {
    size_t length;
    unsigned char data[];
};
```

Key rules:
- The flexible array **must be the last member**
- It **has no size** ([], not [0] or [1])
- The struct itself does **not** include space for the array
## 3. Allocating a Struct with a Flexible Array

You must allocate extra memory manually.
```c
#include <stdlib.h>

struct packet {
    size_t length;
    unsigned char data[];
};

struct packet *pkt = malloc(sizeof(struct packet) + payload_size);
```

Why this works:
- sizeof(struct packet) includes everything _except_ data
- You add the required number of bytes explicitly
## 4. Initializing and Using the Array

```c
pkt->length = payload_size;

for (size_t i = 0; i < pkt->length; i++) {
    pkt->data[i] = (unsigned char)i;
}
```

Accessing data works just like a normal array.
## 5. Complete Example

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct message {
    size_t len;
    char text[];
};

int main(void) {
    const char *hello = "Hello, flexible arrays!";
    size_t len = strlen(hello) + 1;

    struct message *msg =
        malloc(sizeof(struct message) + len);

    if (!msg) return 1;

    msg->len = len;
    memcpy(msg->text, hello, len);

    printf("Message (%zu bytes): %s\n", msg->len, msg->text);

    free(msg);
    return 0;
}
```

## 6. Memory Layout

```
+------------------+
| size_t len       |
+------------------+
| text[0]          |
| text[1]          |
| ...              |
| text[len - 1]    |
+------------------+
```

Everything is contiguous in memory.

## 7. Common Mistakes ❌

### ❌ Putting members after the array

```c
struct bad {
    int x;
    char data[];
    int y;   // INVALID
};
```

### ❌ Allocating only `sizeof(struct)`

```c
struct packet *pkt = malloc(sizeof(struct packet)); // BUG
```

### ❌ Using flexible arrays on the stack

```c
struct packet pkt; // data has size 0 → unusable
```

## 8. Flexible Array vs Zero-Length Array

```c
struct old_style {
    int n;
    char data[0];  // GCC extension, not standard
};
```

|**Feature**|char data[]|char data[0]|
|---|---|---|
|Standard C|✅ Yes (C99)|❌ No|
|Portable|✅ Yes|❌ No|
|Recommended|✅ Yes|❌ No|

Always prefer **flexible array members**.

## 9. Reallocation

You can resize the structure using realloc:

```c
pkt = realloc(pkt, sizeof(struct packet) + new_size);
pkt->length = new_size;
```

Be sure to:
- Store the result of realloc
- Update your size metadata

## 10. When to Use Flexible Array Members

Use them when:
- The struct logically _owns_ the variable-sized data
- You want fewer allocations
- Cache locality matters

Avoid them when:
- The array size frequently changes independently
- The data must be shared between multiple owners

## 11. Summary

- Flexible array members are **standard, safe, and efficient**
- They must be the **last member of a struct**
- You must **manually allocate extra memory**
- They provide **cleaner APIs and better performance**

## 12. References

- ISO/IEC 9899:1999 (C99) — §6.7.2.1
- Linux kernel coding style
- POSIX systems programming practices

If you want, I can also:
- Add **diagrams with padding/alignment**
- Compare FAMs vs pointers
- Provide **kernel-style patterns**
- Convert this into **slides or cheatsheet form**


# Complex Numbers

## Using Complex Numbers in C with <complex.h> (C99+)

### 1. What <complex.h> Provides

C99 introduces native complex-number support: built-in types, arithmetic operators, and math functions. No manual implementation required.
### 2. Compilation

Use C99 or newer and link the math library:

```bash
gcc -std=c99 main.c -lm
```

### 3. Declaring Complex Numbers

```c
#include <complex.h>

double complex z1;
float complex z2;
long double complex z3;
```

Imaginary unit:

```c
I   // standard imaginary unit
```

Example:

```c
double complex z = 3.0 + 4.0*I;
```

### 4. Initialization

Direct:

```c
double complex z = 1.0 + 2.0*I;
```

Portable macros:

```c
double complex z = CMPLX(1.0, 2.0);
float complex  f = CMPLXF(1.0f, 2.0f);
```

### 5. Real and Imaginary Parts

```c
double r = creal(z);
double i = cimag(z);
```

Printing:

```c
printf("Real: %f, Imag: %f\n", creal(z), cimag(z));
```

### 6. Arithmetic

```c
double complex a = 1 + 2*I;
double complex b = 3 - 4*I;

double complex sum  = a + b;
double complex diff = a - b;
double complex prod = a * b;
double complex quot = a / b;
```

### 7. Magnitude and Phase

```c
double mag = cabs(z);   // magnitude
double ang = carg(z);   // phase (radians)
```

### 8. Common Complex Math Functions

**==cabs, carg, conj, csqrt, cexp, clog, csin, ccos, ctan, cpow==**

Example:

```c
double complex w = cexp(1 + I);
```

### 9. Conjugate

```c
double complex zc = conj(3 + 4*I);
```

### 10. Polar Form

From polar:

```c
double complex z = 5.0 * cexp(I * M_PI/4);
```

To polar:

```c
double r = cabs(z);
double t = carg(z);
```

### 11. Comparing Complex Numbers

Avoid == for floats:

```c
if (cabs(z1 - z2) < 1e-9) { /* approximately equal */ }
```

### 12. Printing Nicely

```c
printf("%.2f %c %.2fi\n",
       creal(z),
       cimag(z) >= 0 ? '+' : '-',
       fabs(cimag(z)));
```

### 13. Common Pitfalls

- Forgetting -lm
- Using i instead of I
- Accessing fields like a struct (z.real ❌)
- Assuming exact equality with floats
### 14. Complete Example

```c
#include <stdio.h>
#include <complex.h>
#include <math.h>

int main(void) {
    double complex z1 = 3 + 4*I;
    double complex z2 = CMPLX(1.0, -2.0);

    double complex sum = z1 + z2;
    double complex prod = z1 * z2;

    printf("z1 = %.2f + %.2fi\n", creal(z1), cimag(z1));
    printf("z2 = %.2f + %.2fi\n", creal(z2), cimag(z2));
    printf("sum = %.2f + %.2fi\n", creal(sum), cimag(sum));
    printf("prod = %.2f + %.2fi\n", creal(prod), cimag(prod));
    printf("|z1| = %.2f\n", cabs(z1));
    printf("arg(z1) = %.2f radians\n", carg(z1));
    return 0;
}
```

Compile:

```bash
gcc -std=c99 complex_demo.c -lm
```

### 15. Typical Use Cases

Signal processing, control systems, electrical engineering, numerical simulations, FFTs.

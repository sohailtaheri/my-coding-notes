
## **1. Binary Data in C**

C does **not** have a dedicated “binary” data type. All data is ultimately stored in **binary form**, and binary manipulation is done using:

- Integer types
- Unsigned types
- Bitwise operators
- Bit-fields
- Byte arrays

---
## **2. Integer Types and Binary Representation**

Common integer types:

```
char, short, int, long, long long
```

- All are stored internally as binary.
- **Unsigned types** are preferred for bit-level operations.
  
Example:

```c
unsigned char x = 5;   // 00000101
```

---
## **3. Bitwise Operators**

Used to manipulate individual bits:

|**Operator**|**Purpose**|
|---|---|
|&|AND|
|`|`|
|^|XOR|
|~|NOT|
|<<|Left shift|
|>>|Right shift|

Example:
```c
x = x << 3;  // shift bits left
```

---
## **4. Binary Storage Techniques**

### **a) Bit-fields**

```c
struct Flags {
    unsigned int ready : 1;
    unsigned int error : 1;
};
```

> Layout is compiler-dependent.

### **b) Raw Binary Data**

```c
unsigned char buffer[256];
```

Used for files, networking, and protocols.

---
## **5. Boolean Type**

C99 introduced:

```c
#include <stdbool.h>
bool flag;
```

Stored as 0 or 1.

---
## **6. Integer Sizes on 64-bit Systems**

The size of integer types is determined by the **data model**, not directly by the CPU.
### **LP64 Data Model (Linux, macOS, Unix)**

|**Type**|**Size**|
|---|---|
|char|1 byte|
|short|2 bytes|
|int|4 bytes|
|long|8 bytes|
|long long|8 bytes|
|pointer|8 bytes|

➡️ unsigned int = **4 bytes (32 bits)**
### **LLP64 Data Model (Windows 64-bit)**

|**Type**|**Size**|
|---|---|
|int|4 bytes|
|long|4 bytes|
|long long|8 bytes|

---

## **7.** 

## **long** **vs long long in LP64**

- In LP64: **both are 64 bits**
- They are **different types**, despite equal size
- long long was added in C99 to guarantee **at least 64 bits**
- long size varies across platforms

---
## **8. ==Best Practices**==

- Do **not** assume sizes of int, long, etc.
- Use fixed-width types from <stdint.h>:

```c
uint8_t, uint16_t, uint32_t, uint64_t
```

- Use correct format specifiers:

```c
long       → %ld
long long  → %lld
```

- For portability and clarity, prefer int32_t / int64_t

---

## **9. Key Takeaways**

- C has no native binary datatype
- Binary manipulation uses integers and bitwise operations
- On 64-bit systems, unsigned int is usually **32 bits**
- In LP64, long and long long are both **64 bits**, but not the same type
- Use fixed-width types when size matters

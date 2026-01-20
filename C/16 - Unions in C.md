
## Introduction

A **union** is a user-defined data type in C that allows you to store different data types in the same memory location. Unlike structures where each member gets its own memory space, all members of a union share the same memory location.

## Key Characteristics

- All members share the same memory address
- Size of a union is determined by its largest member
- Only one member can hold a value at any given time
- Useful for memory-efficient programming
- Allows type punning and data interpretation

## Basic Syntax

```c
union union_name {
    data_type member1;
    data_type member2;
    data_type member3;
    // ... more members
};
```

## Declaring and Using Unions

### Example 1: Basic Union Declaration

```c
#include <stdio.h>

union Data {
    int integer;
    float decimal;
    char character;
};

int main() {
    union Data data;
    
    data.integer = 42;
    printf("Integer: %d\n", data.integer);
    
    data.decimal = 3.14;
    printf("Float: %.2f\n", data.decimal);
    
    data.character = 'A';
    printf("Character: %c\n", data.character);
    
    // Note: Only the last assigned value is valid
    printf("Integer now: %d\n", data.integer); // Garbage value
    
    return 0;
}
```

### Example 2: Memory Sharing Demonstration

```c
#include <stdio.h>

union Example {
    int i;
    float f;
    char c;
};

int main() {
    union Example ex;
    
    printf("Size of union: %lu bytes\n", sizeof(ex));
    printf("Address of i: %p\n", (void*)&ex.i);
    printf("Address of f: %p\n", (void*)&ex.f);
    printf("Address of c: %p\n", (void*)&ex.c);
    
    return 0;
}
```

**Output:**

```
Size of union: 4 bytes
Address of i: 0x7ffd5e8a9b40
Address of f: 0x7ffd5e8a9b40
Address of c: 0x7ffd5e8a9b40
```

In this example, `(void*)` is a **type cast** that converts the address to a generic pointer type. The `%p` format specifier in `printf` expects a `void*` pointer type. While many compilers will accept other pointer types without the cast, it's technically **undefined behavior** according to the C standard.
## Unions vs Structures

|Feature|Union|Structure|
|---|---|---|
|Memory allocation|Shares same memory|Separate memory for each member|
|Size|Size of largest member|Sum of all members (plus padding)|
|Value storage|Only one member at a time|All members simultaneously|
|Use case|Memory efficiency|Related data grouping|

### Comparison Example

```c
#include <stdio.h>

struct StructExample {
    int i;
    float f;
    char c;
};

union UnionExample {
    int i;
    float f;
    char c;
};

int main() {
    printf("Size of structure: %lu bytes\n", sizeof(struct StructExample));
    printf("Size of union: %lu bytes\n", sizeof(union UnionExample));
    
    return 0;
}
```

**Typical Output:**

```
Size of structure: 12 bytes
Size of union: 4 bytes
```

## Practical Applications

### 1. Type Conversion and Inspection

```c
#include <stdio.h>

union FloatInspector {
    float f;
    unsigned int bits;
};

int main() {
    union FloatInspector inspector;
    
    inspector.f = 3.14159;
    printf("Float value: %f\n", inspector.f);
    printf("Binary representation: 0x%08X\n", inspector.bits);
    
    return 0;
}
```

### 2. Tagged Unions (Discriminated Unions)

```c
#include <stdio.h>

enum DataType {
    INT_TYPE,
    FLOAT_TYPE,
    STRING_TYPE
};

struct TaggedData {
    enum DataType type;
    union {
        int i;
        float f;
        char str[20];
    } value;
};

void printData(struct TaggedData data) {
    switch(data.type) {
        case INT_TYPE:
            printf("Integer: %d\n", data.value.i);
            break;
        case FLOAT_TYPE:
            printf("Float: %.2f\n", data.value.f);
            break;
        case STRING_TYPE:
            printf("String: %s\n", data.value.str);
            break;
    }
}

int main() {
    struct TaggedData data1;
    data1.type = INT_TYPE;
    data1.value.i = 100;
    printData(data1);
    
    struct TaggedData data2;
    data2.type = FLOAT_TYPE;
    data2.value.f = 98.6;
    printData(data2);
    
    return 0;
}
```

### 3. IP Address Representation

```c
#include <stdio.h>
#include <stdint.h>

union IPAddress {
    uint32_t address;
    struct {
        uint8_t octet1;
        uint8_t octet2;
        uint8_t octet3;
        uint8_t octet4;
    } octets;
};

int main() {
    union IPAddress ip;
    
    ip.octets.octet1 = 192;
    ip.octets.octet2 = 168;
    ip.octets.octet3 = 1;
    ip.octets.octet4 = 1;
    
    printf("IP Address: %d.%d.%d.%d\n", 
           ip.octets.octet1, ip.octets.octet2,
           ip.octets.octet3, ip.octets.octet4);
    printf("32-bit value: 0x%08X\n", ip.address);
    
    return 0;
}
```

## Anonymous Unions

C11 introduced anonymous unions that can be used inside structures:

```c
#include <stdio.h>

struct Packet {
    int type;
    union {
        int integer_data;
        float float_data;
        char string_data[20];
    }; // Anonymous union
};

int main() {
    struct Packet pkt;
    pkt.type = 1;
    pkt.integer_data = 42; // Direct access without union name
    
    printf("Type: %d, Data: %d\n", pkt.type, pkt.integer_data);
    
    return 0;
}
```

## Important Considerations

### 1. Undefined Behavior Warning

```c
union Data {
    int i;
    float f;
};

union Data d;
d.i = 10;
printf("%f\n", d.f); // Undefined behavior! Reading wrong member
```

**Rule:** Always read from the same member you last wrote to, unless you're intentionally doing type punning.

### 2. Alignment and Padding

Unions follow alignment rules based on their largest member:

```c
union Example {
    char c;
    double d;  // Requires 8-byte alignment
};

// Size will be 8 bytes due to double's alignment requirements
```

### 3. Initialization

```c
union Data {
    int i;
    float f;
    char c;
};

// C99 designated initializer (initializes first member by default)
union Data d1 = {42};

// Initialize specific member
union Data d2 = {.f = 3.14};
```

## Common Pitfalls

1. **Forgetting which member was last set**
    
    - Solution: Use tagged unions with an enum type indicator
2. **Assuming all members are valid simultaneously**
    
    - Remember: Only one member holds a valid value at a time
3. **Endianness issues**
    
    - Be careful with bit-level operations across different architectures
4. **Incorrect size assumptions**
    
    - Always use `sizeof()` instead of calculating manually

## Best Practices

1. **Use tagged unions** for type safety
2. **Document which member is currently valid** in your code
3. **Prefer structures** unless memory is truly constrained
4. **Use unions for legitimate type conversion** and low-level programming
5. **Avoid unions** when code clarity is more important than memory efficiency

## Summary

Unions are powerful tools in C for:

- Memory-efficient storage when only one value is needed at a time
- Low-level bit manipulation and type inspection
- Implementing variant types
- Hardware-level programming and protocol implementation

However, they require careful usage to avoid undefined behavior and should be used judiciously with proper documentation and type tracking.

---

**Practice Exercise:** Try creating a tagged union that can represent different geometric shapes (circle, rectangle, triangle) with their specific properties, and write functions to calculate their areas.
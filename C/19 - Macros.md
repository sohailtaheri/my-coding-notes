## Introduction to C Preprocessor

The C preprocessor runs before compilation and processes directives that begin with `#`. It performs text substitution, conditional compilation, and file inclusion.

### Table of Contents
1. [[#Basic Macro Definitions]]
2. [[#The Token Pasting Operator ( )]]
3. [[#The Stringification Operator ( )]]
4. [[#Preprocessor Conditional Compilation]]
5. [[#Advanced Preprocessor Directives]]
6. [[#Predefined Macros]]
7. [[#Variadic Macros]]
8. [[#Practical Examples]]
9. [[#Common Pitfalls]]
10. [[#Conclusion]]

## Basic Macro Definitions

### Simple Object-like Macros

```c
#define PI 3.14159
#define MAX_SIZE 100
#define PROGRAM_NAME "MyApp"

int main() {
    double radius = 5.0;
    double area = PI * radius * radius;
    printf("Area: %f\n", area);
    return 0;
}
```

### Function-like Macros

```c
#define SQUARE(x) ((x) * (x))
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))

int main() {
    int num = 5;
    printf("Square of %d is %d\n", num, SQUARE(num));
    printf("Max of 10 and 20 is %d\n", MAX(10, 20));
    return 0;
}
```

**Important:** Always use parentheses around parameters and the entire expression to avoid operator precedence issues.

```c
// BAD - without parentheses
#define SQUARE_BAD(x) x * x
// SQUARE_BAD(2 + 3) expands to 2 + 3 * 2 + 3 = 11 (wrong!)

// GOOD - with parentheses
#define SQUARE(x) ((x) * (x))
// SQUARE(2 + 3) expands to ((2 + 3) * (2 + 3)) = 25 (correct!)
```

## The Token Pasting Operator (##)

The `##` operator concatenates two tokens into a single token during macro expansion.

### Basic Token Pasting

```c
#define CONCAT(a, b) a##b

int main() {
    int xy = 100;
    printf("%d\n", CONCAT(x, y));  // Expands to: xy, prints 100
    
    // Creating variable names dynamically
    int var1 = 10, var2 = 20, var3 = 30;
    int i = 2;
    // printf("%d\n", var##i);  // This won't work directly
    
    return 0;
}
```

### Practical Example: Creating Multiple Similar Variables

```c
#define DECLARE_VAR(name, num) int name##num

int main() {
    DECLARE_VAR(counter, 1);  // Expands to: int counter1
    DECLARE_VAR(counter, 2);  // Expands to: int counter2
    DECLARE_VAR(counter, 3);  // Expands to: int counter3
    
    counter1 = 10;
    counter2 = 20;
    counter3 = 30;
    
    printf("Counters: %d, %d, %d\n", counter1, counter2, counter3);
    return 0;
}
```

### Function Name Generation

```c
#define MAKE_FUNCTION(type) \
    void print_##type(type value) { \
        printf(#type " value: %d\n", (int)value); \
    }

MAKE_FUNCTION(int)     // Creates: void print_int(int value)
MAKE_FUNCTION(char)    // Creates: void print_char(char value)
MAKE_FUNCTION(short)   // Creates: void print_short(short value)

int main() {
    print_int(42);
    print_char('A');
    print_short(100);
    return 0;
}
```

### Creating Array Accessors

```c
#define ARRAY_GETTER(type) \
    type get_##type##_element(type* arr, int index) { \
        return arr[index]; \
    }

ARRAY_GETTER(int)
ARRAY_GETTER(float)
ARRAY_GETTER(double)

int main() {
    int int_arr[] = {1, 2, 3, 4, 5};
    float float_arr[] = {1.1, 2.2, 3.3};
    
    printf("Int element: %d\n", get_int_element(int_arr, 2));
    printf("Float element: %.1f\n", get_float_element(float_arr, 1));
    
    return 0;
}
```

## The Stringification Operator (#)

The `#` operator converts a macro parameter into a string literal.

```c
#define STRINGIFY(x) #x
#define PRINT_VAR(var) printf(#var " = %d\n", var)

int main() {
    int age = 25;
    int height = 175;
    
    printf("%s\n", STRINGIFY(Hello World));  // Prints: Hello World
    
    PRINT_VAR(age);     // Prints: age = 25
    PRINT_VAR(height);  // Prints: height = 175
    
    return 0;
}
```

### Combining # and

```c
#define DEBUG_PRINT(var, type) \
    printf("DEBUG: " #var " (" #type ") = " type "\n", var)

#define CREATE_STRUCT_ACCESSOR(struct_name, field) \
    int get_##struct_name##_##field(struct struct_name* s) { \
        printf("Accessing " #struct_name "." #field "\n"); \
        return s->field; \
    }

struct Person {
    int age;
    int height;
};

CREATE_STRUCT_ACCESSOR(Person, age)
CREATE_STRUCT_ACCESSOR(Person, height)

int main() {
    int value = 100;
    DEBUG_PRINT(value, "%d");
    
    struct Person p = {30, 180};
    printf("Age: %d\n", get_Person_age(&p));
    printf("Height: %d\n", get_Person_height(&p));
    
    return 0;
}
```

## Preprocessor Conditional Compilation

### #ifdef, #ifndef, #endif

```c
#define DEBUG_MODE

#ifdef DEBUG_MODE
    #define LOG(msg) printf("DEBUG: %s\n", msg)
#else
    #define LOG(msg)  // Empty definition - no output
#endif

int main() {
    LOG("Program started");  // Only prints if DEBUG_MODE is defined
    
    int x = 10;
    LOG("Variable initialized");
    
    return 0;
}
```

### #if, #elif, #else

```c
#define VERSION 2

#if VERSION == 1
    #define FEATURE "Basic"
#elif VERSION == 2
    #define FEATURE "Advanced"
#elif VERSION == 3
    #define FEATURE "Premium"
#else
    #define FEATURE "Unknown"
#endif

int main() {
    printf("Running %s version\n", FEATURE);
    return 0;
}
```

### Header Guards

```c
// myheader.h
#ifndef MYHEADER_H
#define MYHEADER_H

// Header content goes here
void my_function(void);

#endif  // MYHEADER_H
```

Modern alternative using `#pragma once`:

```c
// myheader.h
#pragma once

// Header content goes here
void my_function(void);
```

## Advanced Preprocessor Directives

### #undef

```c
#define TEMP 100
printf("%d\n", TEMP);  // Prints: 100

#undef TEMP
#define TEMP 200
printf("%d\n", TEMP);  // Prints: 200
```

### #error

```c
#ifndef REQUIRED_MACRO
    #error "REQUIRED_MACRO must be defined!"
#endif
```

### #warning (GCC extension)

```c
#warning "This is a deprecated function"
```

### #line

```c
#line 100 "custom_file.c"
// Now __LINE__ will be 100 and __FILE__ will be "custom_file.c"
```

## Predefined Macros

```c
#include <stdio.h>

int main() {
    printf("File: %s\n", __FILE__); \\ current file full path
    printf("Line: %d\n", __LINE__); \\ line of code
    printf("Date: %s\n", __DATE__);
    printf("Time: %s\n", __TIME__);
    printf("Function: %s\n", __func__); \\ name of the function 
    
    #ifdef __STDC__
        printf("Standard C: Yes\n");
    #endif
    
    return 0;
}
```

## Variadic Macros

Macros that accept variable number of arguments.

```c
#define LOG(format, ...) \
    printf("[LOG] " format "\n", ##__VA_ARGS__)

#define DEBUG(level, format, ...) \
    printf("[%s:%d] Level %d: " format "\n", __FILE__, __LINE__, level, ##__VA_ARGS__)

int main() {
    LOG("Simple message");
    LOG("Value: %d", 42);
    LOG("Two values: %d and %s", 42, "hello");
    
    DEBUG(1, "Starting program");
    DEBUG(2, "Processing value: %d", 100);
    
    return 0;
}
```

## Practical Examples

### 1. Generic Swap Macro

```c
#define SWAP(type, a, b) do { \
    type temp = a; \
    a = b; \
    b = temp; \
} while(0)

int main() {
    int x = 5, y = 10;
    printf("Before: x=%d, y=%d\n", x, y);
    SWAP(int, x, y);
    printf("After: x=%d, y=%d\n", x, y);
    
    return 0;
}
```

### 2. Array Size Macro

```c
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))

int main() {
    int numbers[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    printf("Array size: %zu\n", ARRAY_SIZE(numbers));
    
    char name[] = "Hello";
    printf("String array size: %zu\n", ARRAY_SIZE(name));
    
    return 0;
}
```

### 3. Bit Manipulation Macros

```c
#define BIT_SET(byte, bit) ((byte) |= (1U << (bit)))
#define BIT_CLEAR(byte, bit) ((byte) &= ~(1U << (bit)))
#define BIT_TOGGLE(byte, bit) ((byte) ^= (1U << (bit)))
#define BIT_CHECK(byte, bit) ((byte) & (1U << (bit)))

int main() {
    unsigned char flags = 0;
    
    BIT_SET(flags, 2);    // Set bit 2
    printf("After set bit 2: %d\n", flags);  // 4
    
    BIT_SET(flags, 5);    // Set bit 5
    printf("After set bit 5: %d\n", flags);  // 36
    
    BIT_TOGGLE(flags, 2); // Toggle bit 2
    printf("After toggle bit 2: %d\n", flags);  // 32
    
    if (BIT_CHECK(flags, 5)) {
        printf("Bit 5 is set\n");
    }
    
    return 0;
}
```

### 4. Creating Enum-to-String Converter

```c
#define ENUM_TO_STRING(name) #name

#define DEFINE_ENUM_WITH_STRING(EnumType, ...) \
    typedef enum { __VA_ARGS__ } EnumType; \
    static const char* EnumType##_to_string(EnumType value) { \
        switch(value) { \
            __VA_ARGS__ \
            default: return "Unknown"; \
        } \
    }

// Helper macro for switch cases
#define ENUM_CASE(name) case name: return #name;

typedef enum {
    RED,
    GREEN,
    BLUE,
    YELLOW
} Color;

const char* color_to_string(Color c) {
    switch(c) {
        ENUM_CASE(RED)
        ENUM_CASE(GREEN)
        ENUM_CASE(BLUE)
        ENUM_CASE(YELLOW)
        default: return "Unknown";
    }
}

int main() {
    Color c = GREEN;
    printf("Color: %s\n", color_to_string(c));
    return 0;
}
```

## Best Practices

1. **Use ALL_CAPS for macro names** to distinguish them from functions
2. **Always use parentheses** around macro parameters and expressions
3. **Use do-while(0)** for multi-statement macros:
    
    ```c
    #define SAFE_FREE(ptr) do { \    free(ptr); \    ptr = NULL; \} while(0)
    ```
    
4. **Avoid side effects** in macro arguments (no `++`, `--`, function calls that modify state)
5. **Prefer inline functions** over complex macros when possible (C99+)
6. **Use unique variable names** in macros to avoid shadowing
7. **Document macros** clearly, especially complex ones

## Common Pitfalls

### 1. Missing Parentheses

```c
// Wrong
#define MULTIPLY(x, y) x * y
// MULTIPLY(1+2, 3+4) = 1+2*3+4 = 11

// Correct
#define MULTIPLY(x, y) ((x) * (y))
// MULTIPLY(1+2, 3+4) = ((1+2) * (3+4)) = 21
```

### 2. Side Effects

```c
#define MAX(a, b) ((a) > (b) ? (a) : (b))

int x = 5, y = 10;
int result = MAX(x++, y++);  // x and y may be incremented multiple times!
```

### 3. Macro vs Function

```c
// Macro - evaluated at compile time, no type checking
#define SQUARE(x) ((x) * (x))

// Inline function - type safe, better for debugging
static inline int square(int x) {
    return x * x;
}
```

## Conclusion

C macros are powerful tools for code generation, conditional compilation, and creating reusable patterns. The `##` operator enables dynamic token concatenation, while `#` provides stringification. Use them wisely, following best practices to avoid common pitfalls and maintain readable, maintainable code.
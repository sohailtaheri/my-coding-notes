## Introduction

Preprocessor macros provide a powerful way to add debugging capabilities to your C programs without cluttering your production code. The most common pattern is the `DEBUG` macro, which allows you to print debug information during development and easily disable it for release builds.

## Basic DEBUG Macro

The simplest form of a debug macro uses variadic arguments to create a printf-like interface:

```c
#ifdef DEBUG_MODE
    #define DEBUG(fmt, ...) \
        fprintf(stderr, "[DEBUG] %s:%d:%s(): " fmt "\n", \
                __FILE__, __LINE__, __func__, ##__VA_ARGS__)
#else
    #define DEBUG(fmt, ...) do {} while(0)
#endif
```

### How It Works

**When `DEBUG_MODE` is defined:** The macro expands to a `fprintf` call that prints to stderr with:

- File name (`__FILE__`)
- Line number (`__LINE__`)
- Function name (`__func__`)
- Your custom format string and arguments

**When `DEBUG_MODE` is not defined:** The macro expands to a do-nothing statement that gets optimized away by the compiler.

**The `##__VA_ARGS__` trick:** The `##` operator removes the preceding comma if no arguments are provided, preventing syntax errors when you call `DEBUG("message")` without additional parameters.

## Usage Examples

```c
#define DEBUG_MODE  // Enable debugging
#include <stdio.h>

#ifdef DEBUG_MODE
    #define DEBUG(fmt, ...) \
        fprintf(stderr, "[DEBUG] %s:%d:%s(): " fmt "\n", \
                __FILE__, __LINE__, __func__, ##__VA_ARGS__)
#else
    #define DEBUG(fmt, ...) do {} while(0)
#endif

int calculate_sum(int a, int b) {
    DEBUG("Called with a=%d, b=%d", a, b);
    int result = a + b;
    DEBUG("Result: %d", result);
    return result;
}

int main() {
    DEBUG("Program started");
    int x = 5, y = 10;
    int sum = calculate_sum(x, y);
    DEBUG("Final sum: %d", sum);
    return 0;
}
```

**Output:**

```
[DEBUG] example.c:15:main(): Program started
[DEBUG] example.c:9:calculate_sum(): Called with a=5, b=10
[DEBUG] example.c:11:calculate_sum(): Result: 15
[DEBUG] example.c:19:main(): Final sum: 15
```

## Advanced: Multiple Debug Levels

For more sophisticated debugging, you can create different levels of verbosity:

```c
#define DEBUG_LEVEL 2  // 0=none, 1=errors, 2=warnings, 3=info

#if DEBUG_LEVEL >= 3
    #define DEBUG_INFO(fmt, ...) \
        fprintf(stderr, "[INFO] %s:%d: " fmt "\n", \
                __FILE__, __LINE__, ##__VA_ARGS__)
#else
    #define DEBUG_INFO(fmt, ...) do {} while(0)
#endif

#if DEBUG_LEVEL >= 2
    #define DEBUG_WARN(fmt, ...) \
        fprintf(stderr, "[WARN] %s:%d: " fmt "\n", \
                __FILE__, __LINE__, ##__VA_ARGS__)
#else
    #define DEBUG_WARN(fmt, ...) do {} while(0)
#endif

#if DEBUG_LEVEL >= 1
    #define DEBUG_ERROR(fmt, ...) \
        fprintf(stderr, "[ERROR] %s:%d: " fmt "\n", \
                __FILE__, __LINE__, ##__VA_ARGS__)
#else
    #define DEBUG_ERROR(fmt, ...) do {} while(0)
#endif
```

## Enhanced DEBUG Macro with Timestamps

```c
#ifdef DEBUG_MODE
    #include <time.h>
    #define DEBUG(fmt, ...) do { \
        time_t now = time(NULL); \
        char timestr[20]; \
        strftime(timestr, sizeof(timestr), "%H:%M:%S", localtime(&now)); \
        fprintf(stderr, "[%s] %s:%d:%s(): " fmt "\n", \
                timestr, __FILE__, __LINE__, __func__, ##__VA_ARGS__); \
    } while(0)
#else
    #define DEBUG(fmt, ...) do {} while(0)
#endif
```

## Conditional Debugging by Module

You can enable debugging selectively for different parts of your program:

```c
// In module1.c
#define MODULE_NAME "MODULE1"
#ifdef DEBUG_MODULE1
    #define DEBUG(fmt, ...) \
        fprintf(stderr, "[%s] " fmt "\n", MODULE_NAME, ##__VA_ARGS__)
#else
    #define DEBUG(fmt, ...) do {} while(0)
#endif

// In module2.c
#define MODULE_NAME "MODULE2"
#ifdef DEBUG_MODULE2
    #define DEBUG(fmt, ...) \
        fprintf(stderr, "[%s] " fmt "\n", MODULE_NAME, ##__VA_ARGS__)
#else
    #define DEBUG(fmt, ...) do {} while(0)
#endif
```

## Compilation Tips

**Enable debugging during compilation:**

```bash
gcc -D DEBUG_MODE program.c -o program
```

**Set debug level:**

```bash
gcc -D DEBUG_LEVEL=3 program.c -o program
```

**Production build (no debugging):**

```bash
gcc program.c -o program
```

## Best Practices

1. **Always use stderr for debug output** so it doesn't mix with your program's normal stdout output
2. **Use the `do {} while(0)` idiom** for disabled macros to ensure they work correctly in all contexts (if statements, etc.)
3. **Remove debug statements or disable them before release** to avoid performance overhead
4. **Be careful with side effects** - don't put function calls with side effects inside DEBUG macros that might be disabled
5. **Consider adding color codes** to make different debug levels more visible in the terminal

## Common Pitfalls

**Bad - Side effects:**

```c
DEBUG("Value: %d", x++);  // x might not increment in release builds!
```

**Good - Avoid side effects:**

```c
int temp = x++;
DEBUG("Value: %d", temp);
```

This tutorial covers the essentials of using preprocessor macros for debugging in C. The techniques are simple but remarkably effective for tracking down bugs during development.
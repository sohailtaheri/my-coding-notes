
Function pointers are variables that store the address of a function, allowing you to call functions indirectly and pass functions as arguments to other functions.

## Basic Syntax

The basic declaration of a function pointer looks intimidating at first:

```c
return_type (*pointer_name)(parameter_types);
```

For example, a pointer to a function that takes two integers and returns an integer:

```c
int (*func_ptr)(int, int);
```

## Assigning and Using Function Pointers

```c
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

int main() {
    int (*operation)(int, int);  // Declare function pointer
    
    operation = add;              // Assign address of add
    printf("5 + 3 = %d\n", operation(5, 3));
    
    operation = multiply;         // Reassign to multiply
    printf("5 * 3 = %d\n", operation(5, 3));
    
    return 0;
}
```

## The typedef Convention

To make function pointer declarations much more readable, the common convention is to use `typedef`:

```c
typedef return_type (*TypeName)(parameter_types);
```

### Example with typedef

```c
#include <stdio.h>

// Define a type for function pointers
typedef int (*MathOperation)(int, int);

int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }
int multiply(int a, int b) { return a * b; }

// Function that takes a function pointer as parameter
int calculate(int x, int y, MathOperation op) {
    return op(x, y);
}

int main() {
    MathOperation op;  // Much cleaner declaration!
    
    op = add;
    printf("10 + 5 = %d\n", calculate(10, 5, op));
    
    op = subtract;
    printf("10 - 5 = %d\n", calculate(10, 5, op));
    
    op = multiply;
    printf("10 * 5 = %d\n", calculate(10, 5, op));
    
    return 0;
}
```

### Comparison: With and Without typedef

**Without typedef:**

```c
int (*callback)(int, int);
void process(int a, int b, int (*func)(int, int));
```

**With typedef:**

```c
typedef int (*Callback)(int, int);
Callback callback;
void process(int a, int b, Callback func);
```

The typedef version is significantly more readable and maintainable.

## Common Use Cases

### 1. Callback Functions

```c
typedef void (*EventHandler)(const char*);

void register_event(EventHandler handler) {
    handler("Event occurred!");
}

void my_handler(const char* msg) {
    printf("Handling: %s\n", msg);
}

int main() {
    register_event(my_handler);
    return 0;
}
```

### 2. Function Tables (Strategy Pattern)

```c
typedef double (*AreaCalculator)(double);

double circle_area(double radius) {
    return 3.14159 * radius * radius;
}

double square_area(double side) {
    return side * side;
}

int main() {
    AreaCalculator calculators[] = {circle_area, square_area};
    
    printf("Circle area: %.2f\n", calculators[0](5.0));
    printf("Square area: %.2f\n", calculators[1](5.0));
    
    return 0;
}
```

### 3. Sorting with Custom Comparators

```c
#include <stdlib.h>

typedef int (*Comparator)(const void*, const void*);

int compare_ints(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

int main() {
    int arr[] = {5, 2, 8, 1, 9};
    qsort(arr, 5, sizeof(int), compare_ints);
    return 0;
}
```

## Key Points to Remember

- Function pointers store addresses of functions
- The syntax without typedef can be confusing: `return_type (*name)(params)`
- Using typedef makes code much more readable: `typedef return_type (*Name)(params)`
- Function pointers enable callbacks, polymorphism, and flexible code design
- The function signature (return type and parameters) must match exactly
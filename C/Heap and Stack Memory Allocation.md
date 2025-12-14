In C programming, stack and heap memory are two important types of memory storage, each with distinct characteristics:

## Stack Memory:

1. **Storage**: The stack is a reserved section of memory that stores temporary variables created inside functions. It uses a Last In, First Out (LIFO) data structure.
2. **Local Scope**: Variables in the stack memory only exist during the execution of the function that created them. Once the function exits, the variables are popped off the stack and are no longer accessible.
3. **Management**: Stack memory is automatically managed by the compiler, which handles allocation and deallocation.
4. **Size Limitations**: The stack has size limitations, and excessive use can lead to stack overflow, especially with deep recursion or large local variables.

## Heap Memory:

1. **Storage**: The heap is a large pool of memory used for dynamic memory allocation, where memory can be allocated and deallocated at runtime using functions like ==malloc()== and ==free()==, e.g. arrays and structs that can change size dynamically
2. **Global Scope**: Unlike stack variables, heap variables remain allocated until explicitly freed, allowing them to be accessed from anywhere within the program.
3. **Management**: The heap is managed manually by the programmer, which means you must explicitly allocate and free memory to avoid memory leaks.
4. **Size Limitations**: The only limitation on heap memory is the available physical memory on the machine, making it suitable for large data structures.

## Comparison:

- **Lifetime**: Stack variables are temporary and automatically cleared, while heap variables persist until explicitly deallocated.
- **Scope**: Stack variables are local to the function, while heap variables can be accessed globally.
- **Management**: Stack management is automatic, whereas heap management requires manual allocation and deallocation.

Understanding these differences can help you choose the appropriate memory type based on the specific needs of your program, optimising its performance and avoiding common pitfalls like memory leaks.
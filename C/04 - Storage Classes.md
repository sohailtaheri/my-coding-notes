# Automatic Variables

The lecture introduces the concept of automatic variables, commonly referred to as auto variables, which are primarily local variables in C programming. Here are the main points covered:

1. **Definition of Storage Classes**: The lecture starts by explaining storage classes, which describe various features of a variable, including its scope (where it can be accessed), visibility (which parts of the program can use it), and lifetime (how long it exists in memory).
2. **Automatic Variables**: Auto variables are created when a block of code, like a function or loop, is entered and destroyed once it is exited. They are only accessible within their defined block, making their life cycle very temporary.
3. **Default Behaviour**: In C, local variables are automatically defined with automatic storage duration, meaning they are created and destroyed automatically as needed. This feature helps in efficient memory usage since these variables only exist when required.
4. **Declaration**: The syntax for declaring auto variables is straightforward, typically involving the data type followed by the variable name. Interestingly, the auto keyword is usually omitted in practice since local variables default to automatic storage.
5. **Potential Confusion**: The instructor highlights that the keyword auto has a different meaning in C++, which can potentially lead to confusion for programmers familiar with both languages.
6. **Examples**: The lecture provides practical examples demonstrating how to declare and use these local variables, reinforcing concepts of scope and lifetime.
7. **Future Topics**: Finally, the lecture sets the foundation for discussing other storage classes such as register, extern, and static in upcoming sessions.

This lecture is essential for understanding how automatic variables work and their significance in managing memory efficiently in C programming.

# External Variable

1. In the lecture, the focus is on the extern keyword in C, which is used for declaring external variables. Here are the key points summarised:

2. **Definition**: The extern keyword indicates that a variable or function is defined in another file or elsewhere in the codebase, distinguishing it from local variables limited to a specific block. Although extern pertains to global variables, it allows access across different files within large programs.
3. **Clearer Communication**: By using extern, functions and variables defined in one source file can be accessed in others, facilitating communication between separate modules of a program.
4. **Function Declarations**: When declaring functions, using extern can clarify that the function's definition resides in another source file. However, it is essential to note that function declarations are extern by default, meaning they can be called from other files without explicitly using the extern keyword.
5. **Memory Management**: Variables with the extern declaration do not need to be initialised at their point of declaration. Instead, the storage for these variables is allocated where they are defined.

## Applications of extern:

- **Modular Programming**: extern is crucial for dividing code into multiple files, making it easier to manage larger projects by separating implementation details from their declarations.
- **Global Variables**: Facilitates the use of global variables shared across different files, making collaboration between file functions possible.
- **Maintaining Clarity**: In large applications, combining extern declarations with header files helps enforce a clear structure, reducing the chaos that might arise from many interdependent files.In conclusion, while using extern might at first seem less organised compared to languages like JavaScript, it has essential applications in C programming, particularly in managing larger codebases effectively.Was this content relevant to you?

For character arrays, we don't have to specify the size when using extern:

```c
char text[255];
```

in another file:

```c
extern char text[];
```

# Static Variables

Static variables and functions in C have a specialised role in controlling the visibility and lifetime of identifiers. They're primarily used to limit the scope of a variable or function, or to maintain a value across function calls.

## 1. Static Variables

The keyword static can be applied to variables in two main contexts: local variables (inside a function) and global variables (outside any function).

### A. Static Local Variables (Inside a Function)

When static is applied to a local variable inside a function:

- Lifetime: The variable's storage is allocated for the entire duration of the program's execution, not just for the duration of the function call (like a regular local variable). It's initialised only once when the program starts.
- Scope (Visibility): The variable remains local to the function. It cannot be accessed outside the function in which it's declared.
- Persistence: It retains its value between subsequent calls to the function.

Example:

```c
#include <stdio.h>
void counter() {       
	// 'i' is a static local variable       
	static int i = 0;       
	i++;       
	printf("Counter: %d\n", i);   
}

int main() {       
	counter(); // Output: Counter: 1       
	counter(); // Output: Counter: 2 (i retains its value)       
	counter(); // Output: Counter: 3       
	return 0;   
	}
```

### B. Static Global Variables (Outside a Function)

When static is applied to a global variable (declared outside all functions):

- Lifetime: Same as a regular global variable—it exists for the entire program duration.
- Scope (Visibility): Its visibility is restricted to the file (translation unit) in which it is declared. This is known as internal linkage.
- Purpose: It prevents the variable from being accessed or modified by functions in other source code files (when your program is composed of multiple .c files). This helps prevent naming conflicts and enforces data encapsulation.

Example (Conceptual):

Imagine you have two files: file1.c and file2.c.

In file1.c:
```c
// This variable can ONLY be seen and used within file1.c   
static int 
internal_data = 100;
int get_internal_data() {       
	return internal_data;
}
```


In file2.c:
```c
// This will cause a COMPILER ERROR because 'internal_data'
// in file1.c has internal linkage (is static) and is not visible here.
// extern int internal_data;
// printf("%d", internal_data);
````

## 2. Static Functions

The keyword static can also be applied to functions.

- Scope (Visibility): A static function's visibility is restricted to the source file (translation unit) in which it is defined. Like static global variables, they have internal linkage.
- Purpose: It prevents the function from being called by code in other source files. This is useful for utility functions that are only intended to be used internally by the functions within a specific .c file, promoting modularity and preventing namespace pollution.

Example (Conceptual):

In utilities.c:
```c
// This function can ONLY be called by other functions within utilities.c   
static int calculate_hash(char* input) {       
// ... complex calculation ...       
	return 42;   
}

// This is a regular function, visible everywhere
int get_result(char* data) {       
	// It can use the static function       
	int hash = calculate_hash(data);       
	return hash * 2;   
}
```

In main.c:
```c
// main.c can call get_result()   
extern int get_result(char* data);

int main() {       
	// This is fine       
	int result = get_result("test");

	// This will cause a LINKER ERROR because calculate_hash is static(internal linkage)       
	// int hash = calculate_hash("test");       
	return 0;   
}
```

## Summary Table


| Context         | Keyword Used On    | Lifetime               | Scope (Visibility)                       | Purpose                                                  |
| --------------- | ------------------ | ---------------------- | ---------------------------------------- | -------------------------------------------------------- |
| Local Variable  | `static int i;`    | Whole program duration | Restricted to the function               | Persists its value between function calls.               |
| Global Variable | `static int g;`    | Whole program duration | Restricted to the file(internal linkage) | Prevents access from other source files (encapsulation). |
| Function        | `static void f();` | N/A                    | Restricted to the file(internal linkage) | Prevents calls from other source files (modularity).     |

structure fields cannot be static

# Register Variables

Register variables in C are a hint to the compiler that the declared variable should be stored in a CPU register for faster access, rather than in the main memory (RAM).

## 1. How to Declare a Register Variable

You declare a register variable by using the register keyword before the data type:

```c
register int counter;
```

## 2. Key Characteristics and Purpose

### A. Speed Optimisation (The Goal) 🚀

The primary purpose of the register keyword is to achieve higher execution speed.

- CPU Registers: These are small, extremely fast storage locations directly on the Central Processing Unit (CPU).
- Access Speed: Accessing a value in a CPU register is much faster than fetching it from the main memory.
- The Hint: By using register, you're telling the compiler, "I'll be using this variable frequently, so please keep it in a register if possible."

### B. The Compiler's Decision (The Reality) 🤔

It's crucial to understand that the register keyword is only a suggestion to the compiler, not a command.

- Limited Resources: CPUs have a very limited number of registers.
- Compiler Smarts: Modern C compilers are highly optimized. They often ignore the register keyword because they have sophisticated algorithms to determine which variables would benefit most from register storage, and they may allocate registers more effectively than a programmer could manually.
- Fallback: If the compiler decides not to place the variable in a register (because registers are full or the variable isn't used frequently enough), it will simply treat it as a regular local variable and store it in memory.

### C. Restrictions on Use

The register keyword can only be used with automatic local variables and formal parameters (arguments) of a function.

#### Local Variables:  
 ```c
    void process_data(int limit) {  
        register int i; // Correct use    // ...  
    }
    ```

#### Function Parameters:  

```c
    void process_data(register int limit) { 
	    // Correct use    
	    // ...  
    }
```

#### Cannot take the address: 
Since a register variable might not have a memory address, you cannot use the address-of operator (&) on a register variable.  
      
```c
    register int i;  
    int *ptr = &i; // ERROR: Invalid use of '&' on register variable
```

#### Cannot be Global or Static: 
You cannot declare global or static variables as register because they must reside in a fixed memory location.

## 3. When to Use It

In modern C programming, the register keyword is rarely used and often considered obsolete for two main reasons:

1. Compiler Optimization: Modern compilers are highly effective at optimizing code and typically make better register allocation decisions than a human programmer.
2. Debugging: Register variables can sometimes complicate debugging because they might not appear in memory dumps.

If you are writing code where performance is absolutely critical, such as embedded systems or tight loops, you might try using register for loop counters or heavily-used pointers, but always benchmark to confirm it actually provides an improvement.
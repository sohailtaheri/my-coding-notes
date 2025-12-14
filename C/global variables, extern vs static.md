In C programming, external global and local global variables refer to the scope and linkage of variables declared at different levels in your program. Here's a concise summary of their differences and how the extern and static keywords are used:

# External Global Variables:

* Declared outside any function and accessible across multiple files.
- To use an external global variable in a different file, you declare it with the extern keyword.
* Example:
```c
		// In file1.c
		int myGlobalVar;
		
		// In file2.c
		extern int myGlobalVar; // Declaration to access the variable
```

## Local Global Variables:

- Typically, the term refers to variables declared within a single file (but still global within that file) that cannot be accessed from other files unless specified.
- If declared without static, they are accessible only within that file, making them effectively 'local' to that file for external access.
## Static Global Variables:

- When you declare a global variable with the static keyword, it restricts the variable's visibility to the file where it is declared.
- This helps in avoiding naming conflicts and makes sure that the variable cannot be accessed from other files.
- Example:

```c
// In file1.c
static int myStaticVar; // Only accessible within file1.c
```
## Usage Summary:

- `extern`: Allows access to global variables across multiple files. It is used in conjunction with a declaration in another file while ensuring that the actual definition is elsewhere.
- `static`: Limits the visibility of a variable to the file in which it is declared, thus preventing unintended interactions between files.

By understanding these concepts, you can manage variable scope effectively while minimising potential conflicts and enhancing code maintainability.
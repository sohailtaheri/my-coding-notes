Here are the main formatting and I/O functions in `stdio.h` library:
## ► 1. Formatted Output Functions

- `printf()` - print to stdout
- `fprintf()` - print to a file stream
- `sprintf()` - print to a string buffer
- `snprintf()` - print to string with size limit (safer)
- `vprintf()`, `vfprintf()`, `vsprintf()`, `vsnprintf()` - variadic versions

Here are the common format specifiers for `printf()`, `scanf()`, and related formatting functions:
### Integer Formats

- `%d` or `%i` - signed decimal integer
- `%u` - unsigned decimal integer
- `%o` - unsigned octal
- `%x` - unsigned hexadecimal (lowercase)
- `%X` - unsigned hexadecimal (uppercase)
- `%hd` - short int
- `%ld` - long int
- `%lld` - long long int
### Floating Point Formats

- `%f` - decimal floating point (lowercase)
- `%F` - decimal floating point (uppercase)
- `%e` - scientific notation (lowercase)
- `%E` - scientific notation (uppercase)
- `%g` - shortest representation (%f or %e)
- `%G` - shortest representation (%F or %E)
- `%a` - hexadecimal floating point (lowercase)
- `%A` - hexadecimal floating point (uppercase)
- `%lf` - double (for `scanf`, same as `%f` for `printf`)
### Character and String Formats

- `%c` - single character
- `%s` - string (null-terminated)
### Pointer Format

- `%p` - pointer address (hexadecimal)
### Special Formats

- `%%` - literal percent sign
- `%n` - writes number of characters printed so far (for `printf`)
### Width and Precision Modifiers

- `%5d` - minimum width of 5
- `%05d` - pad with zeros to width 5
- `%-5d` - left-align within width 5
- `%.2f` - 2 decimal places
- `%10.2f` - width 10, 2 decimal places
- `%*d` - width from argument
- `%.*f` - precision from argument
### Example Usage

```c
printf("%d\n", 42);           // 42
printf("%5d\n", 42);          // "   42"
printf("%05d\n", 42);         // "00042"
printf("%.2f\n", 3.14159);    // "3.14"
printf("%e\n", 1234.5);       // "1.234500e+03"
printf("%s\n", "Hello");      // "Hello"
printf("%p\n", &var);         // "0x7ffc8b2a1234" (address)
```
## ► 2. Formatted Input Functions

- `scanf()` - read from stdin
- `fscanf()` - read from a file stream
- `sscanf()` - read from a string

## ► 3. Character I/O Functions

- `getchar()`, `putchar()` - single character from stdin / to stdout
- `getc()`, `putc()` - single character from/to stream
- `fgetc()`, `fputc()` - single character from/to file
- `ungetc()` - push character back to stream

Here are two examples of `getc()` - one reading from a file and one reading from the terminal:
### Example 1: Reading from a File

```c
#include <stdio.h>

int main() {
    FILE *fp;
    int ch;
    
    // Open file for reading
    fp = fopen("example.txt", "r");
    if (fp == NULL) {
        perror("Error opening file");
        return 1;
    }
    
    // Read and display characters until end of file
    printf("File contents:\n");
    while ((ch = getc(fp)) != EOF) {
        putchar(ch);
    }
    
    fclose(fp);
    return 0;
}
```

### Example 2: Reading from Terminal (stdin)

```c
#include <stdio.h>

int main() {
    int ch;
    int count = 0;
    
    printf("Enter text (press Ctrl+D or Ctrl+Z to end):\n");
    
    // Read characters from stdin until EOF
    while ((ch = getc(stdin)) != EOF) {
        if (ch == '\n') {
            count++;
            printf("Line %d entered\n", count);
        }
    }
    
    printf("\nTotal lines entered: %d\n", count);
    return 0;
}
```

**Key Points:**

- For files, use `fopen()` to get a FILE pointer, then pass it to `getc()`
- For terminal input, use `stdin` (predefined FILE pointer) with `getc()`
- `getc(stdin)` is equivalent to `getchar()`
- Always check for `EOF` to detect end of input
- On Unix/Linux, press Ctrl+D to send EOF; on Windows, press Ctrl+Z then Enter

## ► 4. String I/O Functions

- `gets()` - read line from stdin (⚠️ ==deprecated/unsafe==)
- `fgets()` - read line from stream (safer)
- `puts()` - write string to stdout with newline
- `fputs()` - write string to stream
- `getline()` - This is a POSIX function (not in the C standard library, but widely available on Unix/Linux systems). It's very useful because it automatically allocates memory for the line.

Here's an example of `fgets()` which reads a line of text:

```c
#include <stdio.h>
#include <string.h>

int main() {
    char buffer[100];
    
    printf("Enter your name: ");
    
    // Read a line from stdin (up to 99 characters + null terminator)
    if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
        // Remove newline character if present
        buffer[strcspn(buffer, "\n")] = '\0';
        
        printf("Hello, %s!\n", buffer);
    } else {
        printf("Error reading input\n");
    }
    
    return 0;
}
```

**How `fgets()` works:**

- `fgets(buffer, size, stream)` reads up to `size-1` characters
- It stops at a newline or EOF
- It includes the newline character in the buffer (if there's room)
- It always null-terminates the string
- Returns `NULL` on error or EOF

**Reading from a file:**

```c
FILE *fp = fopen("data.txt", "r");
char line[256];

while (fgets(line, sizeof(line), fp) != NULL) {
    printf("%s", line);
}

fclose(fp);
```

and here are the examples for `getline()`
## Example 1: Basic Usage (Terminal Input)

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    char *line = NULL;
    size_t len = 0;
    ssize_t nread;
    
    printf("Enter a line of text: ");
    
    // getline allocates memory automatically
    nread = getline(&line, &len, stdin);
    
    if (nread != -1) {
        printf("You entered (%zd characters): %s", nread, line);
    } else {
        printf("Error reading line\n");
    }
    
    free(line);  // Don't forget to free the allocated memory!
    return 0;
}
```

## Example 2: Reading Lines from a File

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *fp;
    char *line = NULL;
    size_t len = 0;
    ssize_t nread;
    int line_num = 0;
    
    fp = fopen("example.txt", "r");
    if (fp == NULL) {
        perror("Error opening file");
        return 1;
    }
    
    // Read file line by line
    while ((nread = getline(&line, &len, fp)) != -1) {
        line_num++;
        printf("Line %d (%zd chars): %s", line_num, nread, line);
    }
    
    free(line);
    fclose(fp);
    return 0;
}
```

**Key Points:**

- Set `line = NULL` and `len = 0` initially - `getline()` will allocate memory
- Returns number of characters read (including newline), or `-1` on EOF/error
- Includes the newline character in the returned string
- **Must `free()` the line pointer when done**
- Available on Linux/Unix/macOS, but not standard C (requires `_GNU_SOURCE` on some systems)
## ► 5. File Operations

- `fopen()`, `fclose()` - open/close files
- `fread()`, `fwrite()` - binary read/write
- `fseek()`, `ftell()`, `rewind()` - file positioning
- `feof()`, `ferror()` - check end-of-file and errors
- `fflush()` - flush output buffer

## ► 6. Other Utility Functions

- `perror()` - print error message
- `remove()`, `rename()` - file management
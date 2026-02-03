
**Warnings and diagnostics:**

- `-Wall` - Enables most common warning messages (despite the name, it doesn't enable _all_ warnings)
- `-Wextra` - Enables additional warnings not covered by `-Wall`
- `-Werror` - Treats all warnings as errors, stopping compilation
- `-Wpedantic` - Issues warnings for code that doesn't strictly conform to the standard
- `-Wshadow` - Warns when a variable shadows another variable

**Optimization:**

- `-O0` - No optimization (default, fastest compilation)
- `-O1`, `-O2`, `-O3` - Increasing levels of optimization
- `-Os` - Optimize for size rather than speed
- `-Ofast` - Aggressive optimizations that may not strictly follow standards
- `gcc -Q --help=optimizers` shows all the available optimizers

**Debugging:**

- `-g` - Generates debugging information for use with GDB
- `-ggdb` - Generates debugging information specifically optimized for GDB

**Standards:**

- `-std=c99`, `-std=c11`, `-std=c17` - Specifies which C standard to use
- `-std=c++11`, `-std=c++14`, `-std=c++17`, `-std=c++20` - C++ standards

**Shared libraries:**

- `-fPIC` - Generates position-independent code, required for shared libraries
- `-shared` - Creates a shared library (.so on Linux, .dylib on macOS, .dll on Windows)

**Other useful options:**

- `-I<directory>` - Adds a directory to the include search path
- `-L<directory>` - Adds a directory to the library search path
- `-l<library>` - Links against a specified library
- `-o <file>` - Specifies the output file name
- `-c` - Compiles source files without linking
- `-D<macro>` - Defines a preprocessor macro
- `-march=native` - Optimizes for your specific CPU architecture

A commonly recommended combination for development is `-Wall -Wextra -g -O2`.

For creating a shared library, you'd typically use: `gcc -fPIC -shared -o libmylib.so mylib.c`

**Common environment variables:**

- `CC` - Specifies the C compiler to use (e.g., `export CC=gcc`)
- `CXX` - Specifies the C++ compiler to use (e.g., `export CXX=g++`)
- `CFLAGS` - Default flags for the C compiler (e.g., `export CFLAGS="-Wall -O2"`)
- `CXXFLAGS` - Default flags for the C++ compiler
- `LDFLAGS` - Flags passed to the linker (e.g., `export LDFLAGS="-L/usr/local/lib"`)
- `CPPFLAGS` - Preprocessor flags (e.g., `export CPPFLAGS="-I/usr/local/include"`)
- `PATH` - Search path for executables, includes compiler location
- `LD_LIBRARY_PATH` - Runtime search path for shared libraries (Linux)
- `DYLD_LIBRARY_PATH` - Runtime search path for shared libraries (macOS)
- `LIBRARY_PATH` - Compile-time search path for libraries

### Misc. Tools
**nm** - Lists symbols from object files and libraries

- Shows functions, variables, and other symbols in compiled code
- Useful for checking what's exported from a library or object file
- Example: `nm libmylib.so` shows all symbols in the library
- Common symbol types: `T` (text/code), `U` (undefined/external), `D` (initialized data)

**ldd** - Lists dynamic dependencies of an executable or shared library

- Shows which shared libraries a program needs to run
- Displays the actual paths where libraries are found
- Example: `ldd myprogram` shows all .so files the program depends on
- Helpful for debugging "library not found" errors and checking library versions

Quick example usage:

bash

```bash
nm myprogram | grep my_function    # Check if function exists
ldd myprogram                       # See which libraries it needs
```
## Compile Process

To compile multiple source files using GCC, use the command:

`gcc mod1.c mod2.c main.c -o executable_name`

This compiles the specified files into an executable. This will let us to focus on the file with errors only. To create intermediate object files without linking, use the -c option:

`gcc -c mod1.c   gcc -c mod2.c   gcc -c main.c`

This generates mod1.o, mod2.o, and main.o. Then, to link them, run:

`gcc mod1.o mod2.o main.o -o executable_name`

This approach supports incremental compilation, allowing you to compile only modified files.

## Make Files

Make files are a powerful utility used to manage the compilation of larger projects. Here are some key commands and their usage:

* **Basic Structure: A Makefile typically includes:**

	`target: dependencies       command`

* **Example: For a program called myprogram that depends on object files (obj):**

	`prog = myprogram`

	`$(prog): $(obj)       gcc $(obj) -o $(prog)`

* **Automatic Recompilation:**

	- The make utility automatically recompiles source files only when necessary based on file timestamps. If a .c file is modified and is newer than the corresponding .o file, make recompiles it.

* **Running Make: To run the Makefile, simply execute:**

	`make`

* **Cleaning Up: To remove object files or the executable, you can add a clean target:**

	`clean:       rm -f $(obj) $(prog)`

* **Using Variables: Use variables to simplify your Makefile. For instance:**

	`CC = gcc   CFLAGS = -Wall`

	`$(prog): $(obj)       $(CC) $(CFLAGS) $(obj) -o $(prog)`

By using a Makefile, you streamline your development process, especially in larger projects, as you no longer need to manually track which files need recompilation after code changes.
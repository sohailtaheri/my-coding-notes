# 06 — System Programs

## What Are System Programs?

**System programs** (also called system utilities or system software) are programs that ship with the OS and provide a convenient environment for developing and running user applications. They sit above the kernel but below user applications in the software stack.

```
┌────────────────────────────────────┐
│        User Applications           │  e.g., Firefox, VS Code
├────────────────────────────────────┤
│        System Programs             │  e.g., ls, gcc, bash, cron
├────────────────────────────────────┤
│        Operating System Kernel     │
├────────────────────────────────────┤
│        Hardware                    │
└────────────────────────────────────┘
```

Most of what users think of as "the operating system" is actually system programs built on top of the kernel.

---

## Categories of System Programs

### 1. File Management

Programs for creating, deleting, copying, renaming, and navigating files and directories.

| Program | Purpose |
|---|---|
| `ls` / `dir` | List directory contents |
| `cp` / `copy` | Copy files |
| `mv` / `move` | Move or rename files |
| `rm` / `del` | Delete files |
| `mkdir` / `rmdir` | Create / remove directories |
| `find` / `locate` | Search for files by name or attribute |
| `chmod`, `chown` | Change permissions and ownership |

---

### 2. Status Information

Programs that query the system and display diagnostic or monitoring data.

| Program | Purpose |
|---|---|
| `date` | Print current date and time |
| `df` / `du` | Disk free space / disk usage |
| `top` / `htop` | Real-time CPU and memory usage per process |
| `ps` | Snapshot of running processes |
| `free` | Memory usage summary |
| `uptime` | How long the system has been running |
| `uname -a` | OS name, version, architecture |
| `dmesg` | Kernel ring buffer (hardware/driver messages) |

Some OSes provide **registries** (Windows Registry) or **configuration databases** to store and query system status.

---

### 3. File Modification (Text Editors)

Programs for creating and editing text files — source code, config files, scripts.

| Program | Notes |
|---|---|
| `vi` / `vim` | Modal editor; ubiquitous on Unix |
| `nano` | Beginner-friendly terminal editor |
| `emacs` | Extensible editor with its own ecosystem |
| Notepad | Windows built-in |
| `sed`, `awk` | Stream editors for programmatic text transformation |

---

### 4. Programming Language Support

Tools that let developers write, compile, and run programs.

| Category | Examples |
|---|---|
| Compilers | `gcc`, `clang`, `javac`, `rustc` |
| Interpreters | `python3`, `ruby`, `node` |
| Assemblers | `as` (GNU assembler), `nasm` |
| Debuggers | `gdb`, `lldb` |
| Build tools | `make`, `cmake`, `ninja` |
| Linkers | `ld`, `lld` |

These are bundled with the OS or available through its package manager. Without them, writing software on the machine would require a separate development environment.

---

### 5. Program Loading and Execution

Programs that load code into memory and manage execution environments.

| Program / Concept | Purpose |
|---|---|
| Dynamic linker (`ld.so`) | Loads shared libraries at runtime |
| `ldd` | Lists shared library dependencies of a binary |
| `strace` | Traces system calls made by a process |
| `ltrace` | Traces library calls made by a process |
| Loaders | Part of the kernel/exec subsystem that maps binary into memory |

The **loader** maps the program's segments (code, data, stack) into virtual memory, resolves dynamic links, then jumps to the entry point.

---

### 6. Communication Programs

Programs that create connections between processes, users, and machines.

| Program | Purpose |
|---|---|
| `ssh` | Secure remote shell |
| `scp` / `rsync` | Secure file transfer / sync |
| `ping` / `traceroute` | Network diagnostics |
| `curl` / `wget` | Transfer data from URLs |
| `netstat` / `ss` | Show active network connections |
| `ftp` / `sftp` | File transfer protocol clients |
| Mail programs (`mail`, `sendmail`) | Send and receive email |

---

### 7. Background Services (Daemons)

Long-running programs that start at boot and provide services without direct user interaction.

| Daemon | Purpose |
|---|---|
| `sshd` | Accept SSH connections |
| `cron` / `crond` | Schedule recurring tasks |
| `systemd` | Init system; manages all other services |
| `httpd` / `nginx` | Web server |
| `syslogd` / `journald` | System logging |
| `ntpd` / `chronyd` | Time synchronization |
| `cupsd` | Printing |

On modern Linux, **systemd** manages daemon lifecycle (start, stop, restart, dependency ordering). On Windows, the **Services** subsystem fulfills the same role.

---

## System Programs vs. Application Programs

| Aspect | System Programs | Application Programs |
|---|---|---|
| Purpose | Support the OS environment | Solve user problems |
| Bundled with OS? | Usually yes | Usually no |
| Examples | `ls`, `gcc`, `ssh`, `cron` | Firefox, Photoshop, Excel |
| Users | Developers, admins, OS itself | End users |

The boundary is fuzzy — a web browser was once a developer tool, now it's a user application.

---

## Key Takeaways

- System programs are the visible "face" of an OS for most users and developers.
- They span file management, status reporting, editors, compilers, communication, and background services.
- Daemons enable the OS to provide persistent services (web serving, logging, scheduling) without user interaction.
- The kernel provides the foundation; system programs build the usable environment on top of it.

---

*Previous: [05 — Types of System Calls](05_types_of_system_calls.md)*

---

## Study Checklist

- [ ] Can you name three OS architectural approaches and their trade-offs?
- [ ] Can you list five OS services and say which group each belongs to?
- [ ] Can you describe the difference between CLI and GUI?
- [ ] Can you trace a `read()` call from user code through the kernel and back?
- [ ] Can you give one example syscall from each of the six categories?
- [ ] Can you explain the difference between a system program and an application program?

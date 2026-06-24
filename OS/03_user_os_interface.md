# 03 — User–OS Interface

## Overview

Users interact with the OS through one of three main interfaces:

1. Command-Line Interface (CLI)
2. Graphical User Interface (GUI)
3. Touch Interface

Programs interact with the OS through **system calls** (covered in file 04).

---

## 1. Command-Line Interface (CLI) / Shell

The shell reads commands typed by the user and executes them. It is either:

- **Built into the kernel** (uncommon today)
- **A user-space program** — the OS loads the shell just like any other program (common today)

Because the shell is just a program, multiple shells can coexist: `bash`, `zsh`, `fish`, `PowerShell`, `cmd.exe`.

### How commands execute

```
User types: ls -l /home

Shell:
  1. Parses "ls", "-l", "/home"
  2. Searches PATH for the "ls" binary
  3. fork() → creates a child process
  4. exec("ls", ["-l", "/home"]) → replaces child with ls program
  5. Waits for ls to exit, then shows next prompt
```

### Two implementation strategies

| Strategy | Description | Example |
|---|---|---|
| Command built-in to shell | Shell contains the code itself | `cd`, `exit`, `echo` in bash |
| Command as external program | Shell finds and exec's a file | `ls`, `grep`, `cp` |

Built-ins must exist inside the shell because they affect the shell's own state (e.g., `cd` changes the shell's working directory — an external program can't do that).

### Why CLI matters

- Scriptable — combine commands into shell scripts for automation
- Faster for experienced users
- Low resource overhead (no graphics needed)
- Essential for server administration and remote access (SSH)

---

## 2. Graphical User Interface (GUI)

A GUI lets users interact via a **desktop metaphor**: windows, icons, menus, and a pointer.

### Components

- **Window manager** — controls placement, sizing, and layering of windows
- **Desktop environment** — icons, taskbar, file manager (e.g., GNOME, KDE, Windows Explorer, macOS Finder)
- **Widget toolkit** — buttons, text fields, scroll bars drawn on screen (e.g., Qt, GTK, Win32, AppKit)

### History

GUIs were pioneered at Xerox PARC in the 1970s, popularized by Apple (Lisa, Macintosh) in the 1980s, and then by Microsoft Windows.

### GUI vs. CLI

| Aspect | CLI | GUI |
|---|---|---|
| Learning curve | Steep | Shallow |
| Speed (expert user) | Fast | Slower |
| Automation | Easy (scripts) | Harder |
| Resource use | Low | Higher |
| Discovery | Hard (need to know commands) | Easy (menus visible) |

Modern OSes offer both. Power users often use both simultaneously.

---

## 3. Touch Interface

Introduced by smartphones and tablets. Replaces mouse clicks with finger gestures:

- **Tap** → click
- **Long press** → right-click / context menu
- **Swipe** → scroll or navigate
- **Pinch/spread** → zoom

**Examples:** iOS, Android, Windows tablet mode.

Requires UI redesign — smaller touch targets are harder to use than mouse targets, so touch UIs typically feature larger buttons and gesture shortcuts.

---

## Batch Interface (Historical)

Before interactive terminals, users submitted **job decks** (stacks of punch cards) to an operator. The OS ran them in sequence with no real-time interaction. Understanding batch processing helps explain why many OS concepts (job queues, spooling) exist.

---

## Key Takeaways

- The CLI (shell) and GUI are the two dominant user-facing OS interfaces today.
- The shell is itself just a user-space program; multiple shells can coexist.
- CLI excels at automation and remote access; GUI excels at discoverability.
- The interface layer is separate from the OS kernel — swapping a shell or desktop environment doesn't change the OS.

---

*Previous: [02 — Services](02_services.md) | Next: [04 — System Calls](04_system_calls.md)*

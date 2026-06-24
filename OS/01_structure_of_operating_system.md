# 01 — Structure of an Operating System

## What Is an Operating System?

An operating system (OS) is system software that acts as an intermediary between hardware and user applications. Its two primary goals are:

- **Convenience** — make the computer easy to use
- **Efficiency** — use hardware resources effectively

---

## Layered View of a Computer System

```
┌─────────────────────────────┐
│        User Programs        │  ← Application layer
├─────────────────────────────┤
│      Operating System       │  ← Manages resources, provides services
├─────────────────────────────┤
│      Hardware (CPU, RAM,    │  ← Physical devices
│       Disk, I/O devices)    │
└─────────────────────────────┘
```

The OS sits between hardware and applications. It abstracts hardware details so programs don't need to talk to devices directly.

---

## Major Architectural Approaches

### 1. Monolithic Structure (Simple / No Structure)

All OS functionality lives in a single large kernel binary. Procedures can call each other freely.

**Example:** Early UNIX, MS-DOS

```
[ Application ]
      ↕
[ Single large kernel: file system + device drivers + memory mgmt + scheduling ]
      ↕
[ Hardware ]
```

**Pros:** Fast — few layers means low overhead.  
**Cons:** Hard to maintain; a bug anywhere can crash the whole system.

---

### 2. Layered Approach

The OS is divided into numbered layers. Layer N can only call services from layer N−1.

```
Layer 5 — User Programs
Layer 4 — I/O Buffering
Layer 3 — Operator-Console Driver
Layer 2 — Memory Management
Layer 1 — CPU Scheduling
Layer 0 — Hardware
```

**Pros:** Clean abstraction; easy to debug one layer at a time.  
**Cons:** Defining the correct layering is hard; performance suffers from many layer crossings.

---

### 3. Microkernel

Moves as much OS functionality as possible out of the kernel into user-space *servers* (file system, device drivers, networking). The kernel itself does only the bare minimum: inter-process communication (IPC), basic scheduling, and minimal memory management.

```
[ App ]  [ File Server ]  [ Device Driver ]  ← all in user space
          ↕            ↕             ↕
         [ Microkernel (IPC + basic scheduling) ]
                      ↕
                 [ Hardware ]
```

**Examples:** Mach, MINIX, QNX, macOS (Darwin is microkernel-based)

**Pros:** More reliable and secure — a crashed driver doesn't take down the kernel.  
**Cons:** Performance overhead from frequent user↔kernel context switches via IPC.

---

### 4. Modular (Loadable Kernel Modules)

The kernel has a small core and loads additional modules (device drivers, file systems) at runtime. Most modern OSes use this.

**Examples:** Linux kernel modules (`.ko` files), Solaris

**Pros:** Flexible — load only what you need; easier to extend than monolithic.  
**Cons:** Less isolation than microkernel (modules run in kernel space).

---

### 5. Hybrid Structure

Real-world OSes blend multiple approaches:

| OS | Approach |
|---|---|
| Linux | Monolithic + loadable modules |
| Windows NT/10/11 | Layered + microkernel-inspired (but runs drivers in kernel mode for speed) |
| macOS | Microkernel (Mach) + BSD monolithic layer on top |

---

## Kernel vs. User Mode

The hardware enforces two privilege levels:

- **Kernel mode (privileged):** OS code runs here; full hardware access.
- **User mode:** Application code runs here; restricted access.

When an app needs an OS service it issues a **system call**, which triggers a mode switch to kernel mode, executes the request, then returns to user mode. This boundary is fundamental to OS security and stability.

---

## Key Takeaways

- The OS manages CPU, memory, storage, and I/O on behalf of programs.
- Monolithic kernels are fast but fragile; microkernels are robust but slower; modern OSes are hybrids.
- The kernel/user-mode boundary is enforced in hardware and is central to OS design.

---

*Next: [02 — OS Services](02_services.md)*

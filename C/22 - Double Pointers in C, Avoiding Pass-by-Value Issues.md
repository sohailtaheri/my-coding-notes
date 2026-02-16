
## The Problem: Pointers Are Passed by Value

In C, **everything is passed by value**, including pointers. When you pass a pointer to a function, you're passing a _copy_ of the pointer variable itself. This means modifications to the pointer parameter inside the function won't affect the original pointer in the caller.

```c
#include <stdio.h>
#include <stdlib.h>

void allocate_memory(int *ptr) {
    ptr = malloc(sizeof(int) * 5);  // This modifies the LOCAL copy
    *ptr = 42;
}

int main() {
    int *my_ptr = NULL;
    allocate_memory(my_ptr);
    
    if (my_ptr == NULL) {
        printf("Still NULL! The allocation didn't work.\n");
    }
    
    return 0;
}
```

In this example, `my_ptr` remains `NULL` because `allocate_memory` only modified its local copy of the pointer.

## The Solution: Double Pointers (Pointer to Pointer)

To modify the original pointer, we need to pass its **address**. This requires a pointer to a pointer (double pointer).

```c
#include <stdio.h>
#include <stdlib.h>

void allocate_memory(int **ptr) {
    *ptr = malloc(sizeof(int) * 5);  // Dereference to modify the original
    if (*ptr != NULL) {
        (*ptr)[0] = 42;
    }
}

int main() {
    int *my_ptr = NULL;
    allocate_memory(&my_ptr);  // Pass the address of my_ptr
    
    if (my_ptr != NULL) {
        printf("Success! my_ptr[0] = %d\n", my_ptr[0]);
        free(my_ptr);
    }
    
    return 0;
}
```

## How It Works

When you use `int **ptr`:

- `ptr` is a pointer to a pointer
- `*ptr` dereferences once to access the original pointer variable
- `**ptr` dereferences twice to access the actual data

Think of it like this:

```
my_ptr (address: 0x1000) → NULL
&my_ptr → 0x1000

In the function:
ptr → 0x1000
*ptr → NULL (the value at 0x1000)
*ptr = malloc(...) → modifies the value at 0x1000
```

## Common Use Cases

### 1. Dynamic Memory Allocation

```c
void create_array(int **arr, int size) {
    *arr = malloc(size * sizeof(int));
    if (*arr != NULL) {
        for (int i = 0; i < size; i++) {
            (*arr)[i] = i * 2;
        }
    }
}

int main() {
    int *numbers = NULL;
    create_array(&numbers, 10);
    
    if (numbers != NULL) {
        for (int i = 0; i < 10; i++) {
            printf("%d ", numbers[i]);
        }
        free(numbers);
    }
    return 0;
}
```

### 2. Linked List Operations

```c
typedef struct Node {
    int data;
    struct Node *next;
} Node;

void insert_at_head(Node **head, int value) {
    Node *new_node = malloc(sizeof(Node));
    new_node->data = value;
    new_node->next = *head;
    *head = new_node;  // Modify the original head pointer
}

int main() {
    Node *list = NULL;
    insert_at_head(&list, 10);
    insert_at_head(&list, 20);
    insert_at_head(&list, 30);
    
    // list now points to: 30 -> 20 -> 10 -> NULL
    return 0;
}
```

### 3. Function That May Reallocate

```c
void resize_if_needed(int **arr, int *size, int new_size) {
    if (new_size > *size) {
        int *temp = realloc(*arr, new_size * sizeof(int));
        if (temp != NULL) {
            *arr = temp;  // Update the original pointer
            *size = new_size;
        }
    }
}
```

## Visual Memory Model

```
Stack (main):               Stack (function):          Heap:
┌─────────────┐            ┌─────────────┐         ┌──────────┐
│ my_ptr      │ ────┐      │ ptr         │ ───────→│ 0x1000   │
│ (0x1000)    │     │      │             │         └──────────┘
└─────────────┘     │      └─────────────┘
                    │              │
                    │              │ *ptr modifies this
                    └──────────────┘

After *ptr = malloc(...):
┌─────────────┐            ┌─────────────┐         ┌──────────┐
│ my_ptr      │ ───────────→│ 0x5000     │         │ Memory   │
│ (0x5000)    │            │             │         │ block    │
└─────────────┘            └─────────────┘         └──────────┘
```

## Key Takeaways

- Single pointers (`int *`) are passed by value like everything else in C
- To modify the original pointer, pass a pointer to it (`int **`)
- Dereference once (`*ptr`) to access and modify the original pointer
- Essential for functions that allocate memory, modify list heads, or reallocate arrays
- Always check for `NULL` after dereferencing to avoid crashes
# Array vs Linked List: Key Takeaways

## Performance Comparison Results

### Appending 10,000 Elements
- **Array**: 0.21ms
- **Singly Linked List**: 4.42ms
- **Doubly Linked List**: 3.98ms
- **Winner**: Array is ~21x faster

### Prepending 10,000 Elements (Insert at Beginning)
- **Array (insert at 0)**: 9.89ms
- **Singly Linked List**: 4.06ms
- **Doubly Linked List**: 3.83ms
- **Winner**: Linked lists are ~2.4x faster

### Random Access (1,000 accesses)
- **Array[index]**: 0.03ms
- **Singly Linked List**: 9.65ms
- **Doubly Linked List**: 8.50ms
- **Winner**: Array is ~342x faster

### Delete Last Element (1,000 times)
- **Array.pop()**: 0.04ms
- **Singly Linked List**: 18.18ms
- **Doubly Linked List**: 0.47ms
- **Winner**: Doubly linked is ~38x faster than singly linked

## When to Use Each Data Structure

### Use Array (Python List) When:
✓ You need random access (`arr[i]`)  
✓ Appending to end is primary operation  
✓ Memory efficiency matters  
✓ You want cache-friendly iteration  
✓ Most general-purpose use cases  

### Use Singly Linked List When:
✓ Frequent insertions at the beginning  
✓ You only traverse forward  
✓ Implementing stacks or queues (with head/tail)  
✓ Memory is tight (vs doubly linked)  

### Use Doubly Linked List When:
✓ Need bidirectional traversal  
✓ Frequent deletions from both ends  
✓ Implementing LRU cache  
✓ Need to traverse backwards  
✓ Implementing undo/redo functionality  

## Real World Use Cases

### Queue (FIFO)
**Best with**: Doubly Linked List or `collections.deque`
- Enqueue at tail: O(1)
- Dequeue at head: O(1)

### Stack (LIFO)
**Best with**: Array (Python list)
- Push to end: O(1)
- Pop from end: O(1)

### Browser History
**Best with**: Doubly Linked List
- Navigate forward/backward
- Easy insertion of new pages
- Can traverse in both directions

### LRU Cache
**Best with**: Doubly Linked List + Hash Map
- O(1) access with hash map
- O(1) reordering with doubly linked list
- Move recently used to front efficiently

## Time Complexity Summary

| Operation | Array | Singly Linked | Doubly Linked |
|-----------|-------|---------------|---------------|
| Append (end) | O(1) amortized | O(1) | O(1) |
| Prepend (beginning) | O(n) | O(1) | O(1) |
| Insert at index i | O(n) | O(n) | O(n) |
| Delete first | O(n) | O(1) | O(1) |
| Delete last | O(1) | O(n) | O(1) |
| Delete at index i | O(n) | O(n) | O(n) |
| Random access | O(1) | O(n) | O(n) |
| Search | O(n) | O(n) | O(n) |

## The Bottom Line

**Arrays are faster for most operations** due to cache locality and memory access patterns. Modern CPUs are optimized for sequential memory access, making arrays incredibly efficient for iteration and random access.

**Linked lists excel at specific operations** like insertions/deletions at known positions (especially the beginning/end with proper pointers). However, they suffer from poor cache performance due to pointer chasing and scattered memory allocation.

**Default choice**: Use arrays (Python lists) for 95% of use cases. Only reach for linked lists when you have a specific need for their O(1) insertion/deletion properties at the beginning or when bidirectional traversal is essential.

## Memory Overhead

**Array**:
- Stores data in contiguous memory
- Over-allocates for growth (typically 12.5% extra capacity)
- No per-element overhead

**Singly Linked List**:
- Each element: data + 1 pointer (next)
- ~50-100% memory overhead per element
- No wasted capacity from over-allocation

**Doubly Linked List**:
- Each element: data + 2 pointers (next, prev)
- ~100-200% memory overhead per element
- Most memory-intensive option

## Python-Specific Notes

Python's built-in `list` is a dynamic array, not a linked list. For linked list behavior in Python standard library:

- **`collections.deque`**: Double-ended queue, optimized for O(1) operations at both ends
- Use when you need efficient prepending and appending
- Implemented as a doubly-linked list of arrays (hybrid approach)

```python
from collections import deque

# Best for queue operations
queue = deque([1, 2, 3])
queue.append(4)      # O(1) - add to right
queue.appendleft(0)  # O(1) - add to left
queue.pop()          # O(1) - remove from right
queue.popleft()      # O(1) - remove from left
```

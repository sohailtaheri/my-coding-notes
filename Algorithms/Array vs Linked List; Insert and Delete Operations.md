 
## Insert Operations

#### **Array (Dynamic Array)**

|Operation|Complexity|Explanation|
|---|---|---|
|Insert at end|O(1) amortized|Just add to next available slot (may require resize)|
|Insert at beginning|O(n)|Must shift all n elements right|
|Insert at index i|O(n)|Must shift (n-i) elements right|
|Insert at known position|O(n)|Still need to shift elements|

#### **Linked List**

| Operation                | Complexity | Explanation                                           |
| ------------------------ | ---------- | ----------------------------------------------------- |
| Insert at end            | O(1)*      | Just update tail pointer (*O(n) without tail pointer) |
| Insert at beginning      | O(1)       | Just update head pointer                              |
| Insert at index i        | O(n)       | ==O(n) to traverse to position==, O(1) to insert      |
| Insert at known position | O(1)       | If you already have pointer to the node               |

## Delete Operations

#### **Array (Dynamic Array)**

|Operation|Complexity|Explanation|
|---|---|---|
|Delete at end|O(1)|Just decrement size|
|Delete at beginning|O(n)|Must shift all remaining elements left|
|Delete at index i|O(n)|Must shift elements after i left|
|Delete at known position|O(n)|Still need to shift to maintain contiguity|

#### **Linked List**

|Operation|Complexity|Explanation|
|---|---|---|
|Delete at end|O(n)*|Need previous node (*O(1) with doubly-linked list)|
|Delete at beginning|O(1)|Just update head pointer|
|Delete at index i|O(n)|O(n) to traverse, O(1) to delete|
|Delete at known position|O(1)|If you have pointer to previous node|

## Key Insights

### When Arrays Win

- **Random access needed**: Arrays offer O(1) access by index vs O(n) for linked lists
- **Insert/delete at end**: Arrays are O(1) amortized for append/pop
- **Cache locality**: Arrays have better memory locality → faster in practice
- **Memory efficiency**: No pointer overhead per element
- **Small, frequent insertions at end**: Arrays often faster despite same complexity

### When Linked Lists Win

- **Frequent insert/delete at beginning**: O(1) vs O(n) for arrays
- **Insert/delete at known positions**: O(1) if you have the pointer
- **Unpredictable size changes**: No reallocation cost
- **No wasted space**: Grow/shrink one node at a time
- **Insert/delete in middle during iteration**: Can modify while traversing

## Practical Example

**Scenario**: Building a queue (FIFO structure)

```python
# Array-based (bad for queue)
queue = []
queue.append(1)      # O(1) - enqueue at end
queue.pop(0)         # O(n) - dequeue from front (BAD!)

# Linked list (good for queue)
# enqueue at tail: O(1)
# dequeue at head: O(1)
```

**Scenario**: Stack (LIFO structure)

```python
# Array-based (excellent for stack)
stack = []
stack.append(1)      # O(1) - push
stack.pop()          # O(1) - pop
```

## Memory Overhead Comparison

**Array:**

- Stores: data + unused capacity
- Per element: just the data
- Total overhead: O(n) wasted slots from over-allocation

**Singly Linked List:**

- Per element: data + 1 pointer (next)
- Overhead: ~50-100% more memory per element

**Doubly Linked List:**

- Per element: data + 2 pointers (next, prev)
- Overhead: ~100-200% more memory per element

## The Surprising Reality

Despite theoretical advantages, **arrays often outperform linked lists even for insertions/deletions** in practice due to:

1. **Cache effects**: Modern CPUs prefetch contiguous memory
2. **Memory allocation**: Creating/destroying nodes has overhead
3. **Pointer chasing**: Following pointers is slower than sequential access
4. **Branch prediction**: Array operations are more predictable

**Rule of thumb**: Use arrays by default. Only use linked lists when you specifically need O(1) insertions/deletions at known positions or the beginning.
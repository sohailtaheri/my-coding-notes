## Python List Operations

### Append

- **Runtime**: O(1) amortized
- **How it works**: Python lists use dynamic arrays with over-allocation. When you append and there's space in the pre-allocated buffer, it's O(1). When the buffer is full, Python allocates a larger array (typically ~1.125x the current size) and copies everything over, which is O(n) but happens infrequently enough that it amortizes to O(1).

### Insert

- **Runtime**: O(n)
- **How it works**: Inserting at index `i` requires shifting all elements from index `i` onwards one position to the right to make room. This requires moving (n-i) elements.
    - Insert at beginning: O(n) - worst case
    - Insert at end: O(1) - equivalent to append
    - Insert in middle: O(n)

## C Array/List Operations

### Static Arrays

- **Append**: Not really possible - arrays have fixed size
- **Insert**: O(n) if you manually shift elements, but you'd need to ensure there's space

### Dynamic Arrays (manually implemented or using realloc)

- **Append**: O(1) amortized (same strategy as Python - over-allocate and reallocate when needed)
- **Insert**: O(n) - same shifting requirement as Python

### Linked Lists

- **Append**:
    - With tail pointer: O(1)
    - Without tail pointer: O(n) to traverse to end
- **Insert**:
    - At known position (with pointer): O(1)
    - At index i (unknown position): O(n) to find position, then O(1) to insert

## Key Comparisons

|Operation|Python List|C Dynamic Array|C Linked List|
|---|---|---|---|
|Append|O(1) amortized|O(1) amortized|O(1) with tail ptr|
|Insert at index i|O(n)|O(n)|O(n) find + O(1) insert|
|Insert at beginning|O(n)|O(n)|O(1)|

## Performance Differences

**Python vs C (same data structure):**

- **C is faster in practice** for the same algorithmic complexity because:
    
    - No interpreter overhead
    - Better cache locality (especially for homogeneous data)
    - Direct memory access vs pointer dereferencing to PyObjects
    - No reference counting overhead
- **Python's overhead** comes from:
    
    - PyObject structure wrapping each element
    - Reference counting on every operation
    - Type checking at runtime
    - Interpreter execution

**Example timing difference:** For appending 1 million integers:

- C: ~10-20ms
- Python: ~100-200ms (roughly 10x slower)

The asymptotic complexity is the same, but the constant factors differ significantly. For insert operations, the gap widens because Python must update reference counts while shifting elements.
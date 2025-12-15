"""
Comparison: Array (Python List) vs Linked List
Demonstrates practical differences in performance
"""

import time
from singly_linked_list import SinglyLinkedList
from doubly_linked_list import DoublyLinkedList


def time_function(func, *args, **kwargs):
    """Helper to time a function execution"""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    return (end - start) * 1000, result  # Return time in milliseconds


def compare_append(n=10000):
    """Compare append performance"""
    print(f"Appending {n:,} elements:")
    
    # Python list (dynamic array)
    array_time, _ = time_function(lambda: [list(range(n))])
    print(f"  Array:              {array_time:.2f}ms")
    
    # Singly linked list
    def sll_append():
        ll = SinglyLinkedList()
        for i in range(n):
            ll.append(i)
        return ll
    
    sll_time, _ = time_function(sll_append)
    print(f"  Singly Linked:      {sll_time:.2f}ms")
    
    # Doubly linked list
    def dll_append():
        ll = DoublyLinkedList()
        for i in range(n):
            ll.append(i)
        return ll
    
    dll_time, _ = time_function(dll_append)
    print(f"  Doubly Linked:      {dll_time:.2f}ms")
    print(f"  → Array is ~{sll_time/array_time:.1f}x faster than Singly LL")
    print()


def compare_prepend(n=10000):
    """Compare prepend (insert at beginning) performance"""
    print(f"Prepending {n:,} elements:")
    
    # Python list - O(n) per insert!
    def array_prepend():
        arr = []
        for i in range(n):
            arr.insert(0, i)
        return arr
    
    array_time, _ = time_function(array_prepend)
    print(f"  Array (insert 0):   {array_time:.2f}ms")
    
    # Singly linked list - O(1) per insert
    def sll_prepend():
        ll = SinglyLinkedList()
        for i in range(n):
            ll.prepend(i)
        return ll
    
    sll_time, _ = time_function(sll_prepend)
    print(f"  Singly Linked:      {sll_time:.2f}ms")
    
    # Doubly linked list - O(1) per insert
    def dll_prepend():
        ll = DoublyLinkedList()
        for i in range(n):
            ll.prepend(i)
        return ll
    
    dll_time, _ = time_function(dll_prepend)
    print(f"  Doubly Linked:      {dll_time:.2f}ms")
    print(f"  → Linked list is ~{array_time/sll_time:.1f}x faster for prepend!")
    print()


def compare_access(n=1000):
    """Compare random access performance"""
    print(f"Random access {n:,} times on list of {n:,} elements:")
    
    # Setup data structures
    arr = list(range(n))
    sll = SinglyLinkedList()
    dll = DoublyLinkedList()
    for i in range(n):
        sll.append(i)
        dll.append(i)
    
    # Access middle element repeatedly
    mid = n // 2
    
    # Array - O(1)
    array_time, _ = time_function(lambda: [arr[mid] for _ in range(n)])
    print(f"  Array[{mid}]:         {array_time:.2f}ms")
    
    # Singly linked - O(n)
    sll_time, _ = time_function(lambda: [sll.get(mid) for _ in range(n)])
    print(f"  Singly Linked:      {sll_time:.2f}ms")
    
    # Doubly linked - O(n) but optimized
    dll_time, _ = time_function(lambda: [dll.get(mid) for _ in range(n)])
    print(f"  Doubly Linked:      {dll_time:.2f}ms")
    print(f"  → Array is ~{sll_time/array_time:.0f}x faster for random access!")
    print()


def compare_delete_last(n=1000):
    """Compare deleting from end"""
    print(f"Delete last element {n:,} times:")
    
    # Setup
    def setup_array():
        return list(range(n))
    
    def setup_sll():
        ll = SinglyLinkedList()
        for i in range(n):
            ll.append(i)
        return ll
    
    def setup_dll():
        ll = DoublyLinkedList()
        for i in range(n):
            ll.append(i)
        return ll
    
    # Array - O(1)
    def array_delete():
        arr = setup_array()
        for _ in range(n):
            arr.pop()
    
    array_time, _ = time_function(array_delete)
    print(f"  Array.pop():        {array_time:.2f}ms")
    
    # Singly linked - O(n) per delete!
    def sll_delete():
        ll = setup_sll()
        for _ in range(n):
            ll.delete_last()
    
    sll_time, _ = time_function(sll_delete)
    print(f"  Singly Linked:      {sll_time:.2f}ms")
    
    # Doubly linked - O(1)
    def dll_delete():
        ll = setup_dll()
        for _ in range(n):
            ll.delete_last()
    
    dll_time, _ = time_function(dll_delete)
    print(f"  Doubly Linked:      {dll_time:.2f}ms")
    print(f"  → Doubly LL is ~{sll_time/dll_time:.1f}x faster than Singly LL")
    print()


def demonstrate_use_cases():
    """Show when to use each data structure"""
    print("=" * 60)
    print("WHEN TO USE EACH DATA STRUCTURE")
    print("=" * 60)
    print()
    
    print("USE ARRAY (Python list) when:")
    print("  ✓ You need random access (arr[i])")
    print("  ✓ Appending to end is primary operation")
    print("  ✓ Memory efficiency matters")
    print("  ✓ You want cache-friendly iteration")
    print("  ✓ Most general-purpose use cases")
    print()
    
    print("USE SINGLY LINKED LIST when:")
    print("  ✓ Frequent insertions at the beginning")
    print("  ✓ You only traverse forward")
    print("  ✓ Implementing stacks or queues (with head/tail)")
    print("  ✓ Memory is tight (vs doubly linked)")
    print()
    
    print("USE DOUBLY LINKED LIST when:")
    print("  ✓ Need bidirectional traversal")
    print("  ✓ Frequent deletions from both ends")
    print("  ✓ Implementing LRU cache")
    print("  ✓ Need to traverse backwards")
    print("  ✓ Implementing undo/redo functionality")
    print()
    
    print("REAL WORLD EXAMPLES:")
    print()
    
    # Queue example
    print("Queue (FIFO) - Best with Doubly Linked or Collections.deque:")
    dll = DoublyLinkedList()
    dll.append("First")
    dll.append("Second") 
    dll.append("Third")
    print(f"  Enqueue: {dll}")
    dll.delete_first()
    print(f"  After dequeue: {dll}")
    print()
    
    # Stack example
    print("Stack (LIFO) - Best with Array:")
    stack = []
    stack.append("Bottom")
    stack.append("Middle")
    stack.append("Top")
    print(f"  Push: {stack}")
    stack.pop()
    print(f"  After pop: {stack}")
    print()
    
    # Browser history example
    print("Browser History - Doubly Linked List:")
    history = DoublyLinkedList()
    history.append("google.com")
    history.append("github.com")
    history.append("stackoverflow.com")
    print(f"  Forward:  {history}")
    print(f"  Backward: {history.str_reverse()}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("PERFORMANCE COMPARISON: ARRAY vs LINKED LISTS")
    print("=" * 60)
    print()
    
    compare_append()
    compare_prepend()
    compare_access()
    compare_delete_last()
    
    demonstrate_use_cases()
    
    print("=" * 60)
    print("KEY TAKEAWAY:")
    print("Arrays are faster for most operations due to cache locality,")
    print("but linked lists excel at insertions/deletions at specific")
    print("positions (especially beginning/end with proper pointers).")
    print("=" * 60)

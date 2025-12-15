"""
Doubly Linked List Implementation in Python
"""

class DNode:
    """A node in a doubly linked list"""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
    
    def __repr__(self):
        return f"DNode({self.data})"


class DoublyLinkedList:
    """A doubly linked list implementation"""
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def is_empty(self):
        """Check if the list is empty"""
        return self.head is None
    
    def __len__(self):
        """Return the number of elements in the list"""
        return self.size
    
    def append(self, data):
        """Add element to the end of the list - O(1)"""
        new_node = DNode(data)
        
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
        self.size += 1
    
    def prepend(self, data):
        """Add element to the beginning of the list - O(1)"""
        new_node = DNode(data)
        
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        
        self.size += 1
    
    def insert_at(self, index, data):
        """Insert element at specific index - O(n)"""
        if index < 0 or index > self.size:
            raise IndexError(f"Index {index} out of range")
        
        if index == 0:
            self.prepend(data)
            return
        
        if index == self.size:
            self.append(data)
            return
        
        new_node = DNode(data)
        
        # Optimize: traverse from head or tail depending on index
        if index < self.size // 2:
            # Traverse from head
            current = self.head
            for _ in range(index):
                current = current.next
        else:
            # Traverse from tail
            current = self.tail
            for _ in range(self.size - index - 1):
                current = current.prev
        
        # Insert before current
        new_node.next = current
        new_node.prev = current.prev
        current.prev.next = new_node
        current.prev = new_node
        
        self.size += 1
    
    def delete_first(self):
        """Delete the first element - O(1)"""
        if self.is_empty():
            raise IndexError("Cannot delete from empty list")
        
        data = self.head.data
        
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        
        self.size -= 1
        return data
    
    def delete_last(self):
        """Delete the last element - O(1) for doubly linked list!"""
        if self.is_empty():
            raise IndexError("Cannot delete from empty list")
        
        data = self.tail.data
        
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        
        self.size -= 1
        return data
    
    def delete_at(self, index):
        """Delete element at specific index - O(n)"""
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of range")
        
        if index == 0:
            return self.delete_first()
        
        if index == self.size - 1:
            return self.delete_last()
        
        # Optimize: traverse from head or tail
        if index < self.size // 2:
            current = self.head
            for _ in range(index):
                current = current.next
        else:
            current = self.tail
            for _ in range(self.size - index - 1):
                current = current.prev
        
        data = current.data
        current.prev.next = current.next
        current.next.prev = current.prev
        
        self.size -= 1
        return data
    
    def search(self, data):
        """Search for an element and return its index - O(n)"""
        current = self.head
        index = 0
        
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        
        return -1
    
    def get(self, index):
        """Get element at specific index - O(n)"""
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of range")
        
        # Optimize: traverse from head or tail
        if index < self.size // 2:
            current = self.head
            for _ in range(index):
                current = current.next
        else:
            current = self.tail
            for _ in range(self.size - index - 1):
                current = current.prev
        
        return current.data
    
    def reverse(self):
        """Reverse the linked list in place - O(n)"""
        if self.is_empty() or self.head == self.tail:
            return
        
        current = self.head
        self.head, self.tail = self.tail, self.head
        
        while current:
            # Swap next and prev pointers
            current.next, current.prev = current.prev, current.next
            current = current.prev  # Move to next node (which is now prev)
    
    def __str__(self):
        """String representation of the list (forward)"""
        if self.is_empty():
            return "[]"
        
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        
        return " <-> ".join(elements)
    
    def str_reverse(self):
        """String representation of the list (backward)"""
        if self.is_empty():
            return "[]"
        
        elements = []
        current = self.tail
        while current:
            elements.append(str(current.data))
            current = current.prev
        
        return " <-> ".join(elements)
    
    def __repr__(self):
        return f"DoublyLinkedList([{', '.join(str(x) for x in self)}])"
    
    def __iter__(self):
        """Make the list iterable (forward)"""
        current = self.head
        while current:
            yield current.data
            current = current.next
    
    def reverse_iter(self):
        """Iterate backwards through the list"""
        current = self.tail
        while current:
            yield current.data
            current = current.prev


# Example usage and testing
if __name__ == "__main__":
    print("=== Doubly Linked List Demo ===\n")
    
    # Create a new linked list
    dll = DoublyLinkedList()
    
    # Test append
    print("Appending elements 1, 2, 3, 4:")
    for i in range(1, 5):
        dll.append(i)
    print(f"Forward:  {dll}")
    print(f"Backward: {dll.str_reverse()}")
    print(f"Length: {len(dll)}\n")
    
    # Test prepend
    print("Prepending 0:")
    dll.prepend(0)
    print(f"List: {dll}\n")
    
    # Test insert_at
    print("Inserting 99 at index 3:")
    dll.insert_at(3, 99)
    print(f"List: {dll}\n")
    
    # Test bidirectional traversal
    print("Forward iteration:")
    for item in dll:
        print(f"  {item}")
    
    print("\nBackward iteration:")
    for item in dll.reverse_iter():
        print(f"  {item}")
    print()
    
    # Test delete operations
    print("Deleting first element:")
    deleted = dll.delete_first()
    print(f"Deleted: {deleted}, List: {dll}\n")
    
    print("Deleting last element (O(1) in doubly linked!):")
    deleted = dll.delete_last()
    print(f"Deleted: {deleted}, List: {dll}\n")
    
    print("Deleting element at index 2:")
    deleted = dll.delete_at(2)
    print(f"Deleted: {deleted}, List: {dll}\n")
    
    # Test reverse
    print("Reversing the list:")
    dll.reverse()
    print(f"List: {dll}\n")
    
    # Performance comparison
    print("=== Performance Notes ===")
    print("Doubly Linked List advantages over Singly:")
    print("- Delete last:     O(1) vs O(n)")
    print("- Traverse back:   O(1) per step vs impossible")
    print("- Insert/delete:   Can optimize by traversing from nearest end")
    print("\nDisadvantages:")
    print("- Extra memory:    2 pointers per node vs 1")
    print("- More complex:    More pointer updates needed")

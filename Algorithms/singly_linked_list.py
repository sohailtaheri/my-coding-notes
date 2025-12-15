"""
Singly Linked List Implementation in Python
"""

class Node:
    """A node in a singly linked list"""
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def __repr__(self):
        return f"Node({self.data})"


class SinglyLinkedList:
    """A singly linked list implementation"""
    
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
        new_node = Node(data)
        
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        
        self.size += 1
    
    def prepend(self, data):
        """Add element to the beginning of the list - O(1)"""
        new_node = Node(data)
        
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
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
        
        new_node = Node(data)
        current = self.head
        
        # Traverse to the node before the insertion point
        for _ in range(index - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self.size += 1
    
    def delete_first(self):
        """Delete the first element - O(1)"""
        if self.is_empty():
            raise IndexError("Cannot delete from empty list")
        
        data = self.head.data
        self.head = self.head.next
        self.size -= 1
        
        if self.is_empty():
            self.tail = None
        
        return data
    
    def delete_last(self):
        """Delete the last element - O(n) for singly linked list"""
        if self.is_empty():
            raise IndexError("Cannot delete from empty list")
        
        if self.head == self.tail:
            data = self.head.data
            self.head = None
            self.tail = None
            self.size -= 1
            return data
        
        # Traverse to the second-to-last node
        current = self.head
        while current.next != self.tail:
            current = current.next
        
        data = self.tail.data
        current.next = None
        self.tail = current
        self.size -= 1
        return data
    
    def delete_at(self, index):
        """Delete element at specific index - O(n)"""
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of range")
        
        if index == 0:
            return self.delete_first()
        
        # Traverse to the node before the one to delete
        current = self.head
        for _ in range(index - 1):
            current = current.next
        
        data = current.next.data
        current.next = current.next.next
        
        if index == self.size - 1:
            self.tail = current
        
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
        
        current = self.head
        for _ in range(index):
            current = current.next
        
        return current.data
    
    def reverse(self):
        """Reverse the linked list in place - O(n)"""
        if self.is_empty() or self.head == self.tail:
            return
        
        prev = None
        current = self.head
        self.tail = self.head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self.head = prev
    
    def __str__(self):
        """String representation of the list"""
        if self.is_empty():
            return "[]"
        
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        
        return " -> ".join(elements)
    
    def __repr__(self):
        return f"SinglyLinkedList([{', '.join(str(x) for x in self)}])"
    
    def __iter__(self):
        """Make the list iterable"""
        current = self.head
        while current:
            yield current.data
            current = current.next


# Example usage and testing
if __name__ == "__main__":
    print("=== Singly Linked List Demo ===\n")
    
    # Create a new linked list
    ll = SinglyLinkedList()
    
    # Test append
    print("Appending elements 1, 2, 3:")
    ll.append(1)
    ll.append(2)
    ll.append(3)
    print(f"List: {ll}")
    print(f"Length: {len(ll)}\n")
    
    # Test prepend
    print("Prepending 0:")
    ll.prepend(0)
    print(f"List: {ll}\n")
    
    # Test insert_at
    print("Inserting 99 at index 2:")
    ll.insert_at(2, 99)
    print(f"List: {ll}\n")
    
    # Test get
    print(f"Element at index 2: {ll.get(2)}\n")
    
    # Test search
    print(f"Index of element 99: {ll.search(99)}")
    print(f"Index of element 100: {ll.search(100)}\n")
    
    # Test iteration
    print("Iterating through list:")
    for item in ll:
        print(f"  {item}")
    print()
    
    # Test delete operations
    print("Deleting first element:")
    deleted = ll.delete_first()
    print(f"Deleted: {deleted}, List: {ll}\n")
    
    print("Deleting last element:")
    deleted = ll.delete_last()
    print(f"Deleted: {deleted}, List: {ll}\n")
    
    print("Deleting element at index 1:")
    deleted = ll.delete_at(1)
    print(f"Deleted: {deleted}, List: {ll}\n")
    
    # Test reverse
    print("Reversing the list:")
    ll.reverse()
    print(f"List: {ll}\n")
    
    # Performance comparison note
    print("=== Performance Notes ===")
    print("Append:        O(1) - with tail pointer")
    print("Prepend:       O(1)")
    print("Insert at i:   O(n)")
    print("Delete first:  O(1)")
    print("Delete last:   O(n) - need to find second-to-last")
    print("Delete at i:   O(n)")
    print("Search:        O(n)")
    print("Access by idx: O(n)")

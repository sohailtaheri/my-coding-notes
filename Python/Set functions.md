Python’s set type is a powerhouse for comparing, filtering, and analyzing collections. Here's a full rundown of the most useful set operations:

## 🧮 Core Set Operations

| Operation            | Syntax                                 | Description                             |
| -------------------- | -------------------------------------- | --------------------------------------- |
| Union                | `a \| b or a.union(b)`                 | All unique elements from both sets      |
| Intersection         | `a & b or a.intersection(b)`           | Elements common to both sets            |
| Difference           | `a - b or a.difference(b)`             | Elements in a but not in b              |
| Symmetric Difference | `a ^ b` or `a.symmetric_difference(b)` | Elements in either a or b, but not both |
| Subset Check         | `a <= b or a.issubset(b)`              | True if all elements of a are in b      |
| Superset Check       | `a >= b or a.issuperset(b)`            | True if all elements of b are in a      |
| Disjoint Check       | `a.isdisjoint(b)`                      | True if a and b share no elements       |

## 🛠️ Set Methods for Modification

| Method             | Description                              |
| ------------------ | ---------------------------------------- |
| `add(x)`           | Adds element x to the set                |
| `remove(x)`        | Removes x; raises error if not found     |
| `discard(x)`       | Removes x if present; no error if not    |
| `pop()`            | Removes and returns an arbitrary element |
| `clear()`          | Removes all elements                     |
| `update(iterable)` | Adds elements from another iterable      |

## 🧪 Quick Demo

```python
a = {'a', 'b', 'c'}  
b = {'b', 'c', 'd'}

print("Union:", a | b)                     # {'a', 'b', 'c', 'd'}  
print("Intersection:", a & b)              # {'b', 'c'}  
print("Difference (a - b):", a - b)        # {'a'}  
print("Symmetric Difference:", a ^ b)      # {'a', 'd'}
```
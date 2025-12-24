Here's a comprehensive tutorial note on Python Comprehensions, designed to help you understand and apply them effectively.
## 🐍 Python Comprehensions Tutorial

Python comprehensions are concise ways to create collections like lists, dictionaries, sets, and even generators. They make your code more readable and expressive.
### 📘 1. List Comprehension

Syntax:

```python
[expression for item in iterable if condition]
```

Example:

```python
squares = [x**2 for x in range(10)]  
even_squares = [x**2 for x in range(10) if x % 2 == 0]
```

Explanation:

- `x**2` is the expression.
- `for x in range(10)` is the loop.
- `if x % 2 == 0` is the optional condition.
### 📗 2. Dictionary Comprehension

Syntax:

```python
{key_expr: value_expr for item in iterable if condition}
```

Example:

```python
square_dict = {x: x**2 for x in range(5)}  
even_square_dict = {x: x**2 for x in range(10) if x % 2 == 0}
```

Use Case: Quickly transform or filter key-value pairs.

### 📙 3. Set Comprehension

Syntax:

```python
{expression for item in iterable if condition}
```

Example:

```python
unique_squares = {x**2 for x in range(10)}
```

Note: Sets automatically remove duplicates.

### 📒 4. Generator Comprehension

Syntax:

```python
(expression for item in iterable if condition)
```

Example:

```python
square_gen = (x**2 for x in range(10))
```

Use Case: Efficient memory usage for large datasets.

## 🔄 Nested Comprehensions

Example:

```python
matrix = [[i * j for j in range(5)] for i in range(5)]
```

Explanation: You can nest comprehensions to build multi-dimensional structures.

## ⚠️ When Not to Use Comprehensions

- If the logic is too complex, it may reduce readability.
- Avoid deeply nested comprehensions unless absolutely necessary.

## 🧠 Practice Challenge

Try writing a list comprehension that extracts vowels from a string:

```python
text = "Python Comprehensions"  
vowels = [char for char in text if char.lower() in 'aeiou']
```
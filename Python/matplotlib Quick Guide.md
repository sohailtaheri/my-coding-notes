To create a **figure** and **axes pointers** in Matplotlib, you typically use the `plt.subplots()` function because it returns both:

- **`fig`** → the Figure object (the entire canvas)
- **`ax` or `axes[]`** → one or more Axes objects (individual plots)

---
### ✅ Example: Single Plot with Figure and Axes

```python
import matplotlib.pyplot as plt

# Create a figure and a single axes
fig, ax = plt.subplots(figsize=(6, 4))

# Plot data on the axes
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
ax.plot(x, y, label='Line')

# Customize using the axes pointer
ax.set_title__('Single Plot Example')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.legend()

plt.show()
```

---
### ✅ Example: Multiple Subplots with Axes Pointers

```python
import matplotlib.pyplot as plt

# Create a figure with 2x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(8, 6))
x = [1, 2, 3, 4, 5]
y1 = [2, 4, 6, 8, 10]
y2 = [10, 8, 6, 4, 2]

# Access each subplot via axes[row, col]
axes[0, 0].plot(x, y1, color='blue')
axes[0, 0].set_title__('Top Left')

axes[0, 1].plot(x, y2, color='red')
axes[0, 1].set_title('Top Right')

axes[1, 0].bar(x, y1, color='green')
axes[1, 0].set_title__('Bottom Left') 

axes[1, 1].scatter(x, y2, color='purple')
axes[1, 1].set_title('Bottom Right')

plt.tight_layout()
```

---
### ✅ Example: Plotting from a Pandas DataFrame
```python
import pandas as pd
import matplotlib.pyplot as plt

# Create a sample DataFrame
data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'Sales': [200, 250, 300, 280, 350],
    'Profit': [50, 65, 80, 70, 90]
}
df = pd.DataFrame(data)

# Create figure and axes
fig, ax = plt.subplots(figsize=(8, 5))

# Plot Sales and Profit on the same axes
ax.plot(df['Month'], df['Sales'], marker='o', label='Sales')
ax.plot(df['Month'], df['Profit'], marker='s', label='Profit')

# Customize
ax.set_title('Monthly Sales and Profit')
ax.set_xlabel('Month')
ax.set_ylabel('Amount')
ax.legend()
ax.grid(True)

plt.show()
```

---
### ✅ Example: Multiple Subplots from DataFrame
```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
  
# First subplot: Sales
axes[0].bar(df['Month'], df['Sales'], color='skyblue')
axes[0].set_title('Sales')

# Second subplot: Profit
axes[1].bar(df['Month'], df['Profit'], color='orange')
axes[1].set_title('Profit')

plt.tight_layout()
plt.show()
```

---
### ✅ Tips:
- You can also use **`df.plot()`** which is a wrapper around Matplotlib:
```python
df.plot(x='Month', y=['Sales', 'Profit'], kind='line', figsize=(8, 5))
plt.title('Sales and Profit')
plt.show()
```
---
### ✅ Why use `fig` and `ax` pointers?

- **`fig`** lets you control the entire figure (size, saving, global settings).
- **`ax`** gives fine control over each subplot (titles, labels, ticks, etc.).
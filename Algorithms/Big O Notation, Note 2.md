Big O notation describes the efficiency of an algorithm in terms of time or space as the input size grows. It focuses on the worst-case scenario, helping developers compare and optimize algorithms.

## 🚀 Why It Matters
* Predicts performance as input scales
* Helps choose the right algorithm for large datasets
* Guides optimization and trade-offs

## 🧠 Common Big O Classes

| Notation     | Name          | Description                            | Example                        |
| ------------ | ------------- | -------------------------------------- | ------------------------------ |
| $O(1)$       | Constant time | Fastest. Doesn’t depend on input size. | Accessing an array element     |
| $O(\log  n)$ | Logarithmic   | Input size shrinks each step.          | Binary search                  |
| $O(n)$       | Linear        | Time grows with input size.            | Loop through array             |
| $O(n\log n)$ | Linearithmic  | Efficient sorting algorithms.          | Merge sort, quicksort          |
| $O(n^2)$     | Quadratic     | Nested loops over input.               | Bubble sort, pair comparisons  |
| $O(2^n)$     | Exponential   | Doubles with each input increase.      | Recursive Fibonacci            |
| $O(n!)$      | Factorial     | All permutations.                      | Brute-force traveling salesman |

## 🔍 Examples
### 1. Constant Time - $\mathbf{O(1)}$

```python
def get_first_element(arr):
	return arr[0]
```
### 2. Linear Time - $\mathbf{O(n)}$

```python
def sum_array(arr):
	total = 0
	for num in arr:
		total += num
		return total
```
### 3. Quadratic Time - $\mathbf{O(n^2)}$

```python
def print_pairs(arr):
	for i in arr:
		for j in arr:
			print(i, j)
```
### 4. Logarithmic Time - $\mathbf{O(n\log n)}$ 

```python
def binary_search(arr, target):
low, high = 0, len(arr) - 1
while low <= high:
	mid = (low + high) // 2
	if arr[mid] == target:
		return mid
	elif arr[mid] < target:
		low = mid + 1
	else:
		high = mid - 1
	return -1
```

## 🧩 Bonus Tips
- Drop constants: $\mathbf{O(2n)} \rightarrow \mathbf{O(n)}$ 
- Focus on dominant term: $\mathbf{O(n^2+n)} \rightarrow \mathbf{O(n^2)}$ 
- Worst-case ≠ average-case (but Big O focuses on worst)
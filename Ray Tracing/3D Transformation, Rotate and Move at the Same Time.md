In 3D, rotating and moving (translating) an object simultaneously is achieved using a 4×4 transformation matrix in homogeneous coordinates.

---

#### ✅ General Form of a 3D Transformation Matrix

$$ 
\textbf{T}= \begin{bmatrix} r_{11} & r_{12} & r_{13} & t_x \\ r_{21} & r_{22} & r_{23} & t_y \\ r_{31} & r_{32} & r_{33} & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$


- Top-left 3×3 block: Rotation matrix. 
- Last column (except bottom): Translation vector $(t_x, t_y, t_z)$.
- Bottom row `[0 0 0 1]`: Homogeneous coordinates.

---

#### ✅ Rotation Matrices in 3D

- Rotate about X-axis by angle θ:

$$R_x(\theta) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & \cos\theta & -\sin\theta \\ 0 & \sin\theta & \cos\theta \end{bmatrix}$$

- Rotate about Y-axis:

$$R_y(\theta) = \begin{bmatrix} \cos\theta & 0 & \sin\theta \\ 0 & 1 & 0 \\ -\sin\theta & 0 & \cos\theta \end{bmatrix}$$

- Rotate about Z-axis:

$$R_z(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

---

#### ✅ Combining Rotation and Translation

To rotate and move at the same time:

1. Compute the rotation matrix $R$.
2. Insert it into the top-left 3×3 block.
3. Add translation $(t_x, t_y, t_z)$ in the last column.

Example (rotate around Z-axis and translate): $\begin{bmatrix} \cos\theta & -\sin\theta & 0 & t_x \\ \sin\theta & \cos\theta & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix}$

---

#### ✅ Applying to a Point

If a point is $(x, y, z)$ , represent it as $[x, y, z, 1]^T$. Multiply: $\mathbf{p'} = \mathbf{T} \cdot \mathbf{p}$

---

This method allows chaining multiple transformations (rotation + translation) into one matrix multiplication.
# Tutorial Note: MA, AR, and ARMA Digital Filters

---

## 1. Introduction

Digital filters are fundamental building blocks in signal processing, used to shape, smooth, or extract information from discrete-time signals. Three of the most important classes are:

- **MA** — Moving Average (a.k.a. FIR filter)
- **AR** — Autoregressive (a.k.a. IIR filter)
- **ARMA** — Autoregressive Moving Average (combines both)

All three are described by a **linear difference equation** relating the current output $y[n]$ to past inputs $x[n]$ and/or past outputs $y[n]$.

---

## 2. Moving Average (MA) Filter

### 2.1 Definition

A **Moving Average** filter of order $q$ computes the output as a weighted sum of the current and past $q$ input samples:

$$
y[n] = b_0\, x[n] + b_1\, x[n-1] + b_2\, x[n-2] + \cdots + b_q\, x[n-q]
$$

In compact form:

$$
y[n] = \sum_{k=0}^{q} b_k\, x[n-k]
$$

where $b_0, b_1, \ldots, b_q$ are the **filter coefficients** (weights).

### 2.2 Key Properties

| Property | Value |
|---|---|
| Filter type | FIR (Finite Impulse Response) |
| Feedback | None |
| Stability | Always stable |
| Phase response | Linear phase (if symmetric coefficients) |
| Memory | Finite — depends only on past $q$ inputs |

### 2.3 Simple Example: 3-Point Uniform MA

$$
y[n] = \frac{1}{3}\bigl(x[n] + x[n-1] + x[n-2]\bigr)
$$

This is the classic "running average" — each output is the mean of 3 consecutive input samples. It acts as a **low-pass filter**, smoothing out rapid fluctuations.

### 2.4 Transfer Function (Z-Domain)

Taking the Z-transform:

$$
H(z) = \sum_{k=0}^{q} b_k\, z^{-k} = b_0 + b_1 z^{-1} + \cdots + b_q z^{-q}
$$

The transfer function is a **polynomial in $z^{-1}$** — it has only **zeros**, no poles (other than at the origin).

### 2.5 When to Use MA Filters

- Smoothing noisy sensor data
- Anti-aliasing before downsampling
- When linear phase (no phase distortion) is required
- Audio equalization with symmetric FIR designs

---

## 3. Autoregressive (AR) Filter

### 3.1 Definition

An **Autoregressive** filter of order $p$ computes the output using the current input and a weighted sum of **past output** samples:

$$
y[n] = x[n] - a_1\, y[n-1] - a_2\, y[n-2] - \cdots - a_p\, y[n-p]
$$

In compact form:

$$
y[n] + \sum_{k=1}^{p} a_k\, y[n-k] = x[n]
$$

> **Note:** The sign convention for $a_k$ varies by textbook. Some write $+a_k$ on the left side; others move terms to the right with $-a_k$. Always check the convention being used.

### 3.2 Key Properties

| Property | Value |
|---|---|
| Filter type | IIR (Infinite Impulse Response) |
| Feedback | Yes — output feeds back into itself |
| Stability | Conditional — poles must lie inside the unit circle |
| Phase response | Non-linear in general |
| Memory | Infinite — impulse response never truly ends |

### 3.3 Simple Example: 1st-Order AR Filter

$$
y[n] = x[n] - a_1\, y[n-1]
$$

If $x[n] = \delta[n]$ (a unit impulse), the output is:

$$
y[n] = (-a_1)^n \cdot u[n]
$$

where $u[n]$ is the unit step. The impulse response **decays geometrically** — it is infinite in length but eventually goes to zero (if $|a_1| < 1$).

### 3.4 Transfer Function (Z-Domain)

$$
H(z) = \frac{1}{1 + a_1 z^{-1} + a_2 z^{-2} + \cdots + a_p z^{-p}} = \frac{1}{A(z)}
$$

The transfer function has **poles** but only a trivial zero (at origin). The poles determine the filter's frequency response and stability.

### 3.5 Stability Condition

An AR filter is **stable** if and only if **all poles lie strictly inside the unit circle** in the Z-plane:

$$
|z_i| < 1 \quad \forall\, i
$$

### 3.6 When to Use AR Filters

- Resonator and notch filter designs
- Spectral modeling and linear prediction (e.g., speech coding)
- Simulating resonant physical systems
- When sharp roll-off is needed with low filter order

---

## 4. Autoregressive Moving Average (ARMA) Filter

### 4.1 Definition

An **ARMA(p, q)** filter combines both AR and MA parts:

$$
y[n] = \sum_{k=0}^{q} b_k\, x[n-k] - \sum_{k=1}^{p} a_k\, y[n-k]
$$

Or equivalently:

$$
\sum_{k=0}^{p} a_k\, y[n-k] = \sum_{k=0}^{q} b_k\, x[n-k], \quad a_0 = 1
$$

The filter has **p** AR coefficients and **q+1** MA coefficients.

### 4.2 Key Properties

| Property | Value |
|---|---|
| Filter type | IIR (Infinite Impulse Response) |
| Feedback | Yes |
| Stability | Poles must lie inside the unit circle |
| Zeros | From the MA (numerator) part |
| Poles | From the AR (denominator) part |

### 4.3 Simple Example: ARMA(1,1)

$$
y[n] = b_0\, x[n] + b_1\, x[n-1] - a_1\, y[n-1]
$$

This single-pole, single-zero filter is one of the most common building blocks in audio processing and control systems.

### 4.4 Transfer Function (Z-Domain)

$$
H(z) = \frac{B(z)}{A(z)} = \frac{b_0 + b_1 z^{-1} + \cdots + b_q z^{-q}}{1 + a_1 z^{-1} + \cdots + a_p z^{-p}}
$$

This is a **rational function** in $z^{-1}$, with both **zeros** (from $B(z)$) and **poles** (from $A(z)$). The MA part controls the zeros; the AR part controls the poles.

### 4.5 When to Use ARMA Filters

- When you need both poles and zeros for complex frequency shaping
- Digital simulation of analog filters (Butterworth, Chebyshev, elliptic)
- Efficient approximation of long FIR filters with fewer coefficients
- System identification and modeling

---

## 5. Side-by-Side Comparison

| Feature | MA (FIR) | AR (IIR) | ARMA (IIR) |
|---|---|---|---|
| Difference equation | Output = weighted inputs | Output = input + weighted past outputs | Output = weighted inputs + weighted past outputs |
| Transfer function | $B(z)$ (numerator only) | $1/A(z)$ (denominator only) | $B(z)/A(z)$ |
| Poles | None (at origin only) | Yes | Yes |
| Zeros | Yes | None | Yes |
| Stability | Always stable | Conditional | Conditional |
| Impulse response | Finite (FIR) | Infinite (IIR) | Infinite (IIR) |
| Phase | Linear (if symmetric) | Nonlinear | Nonlinear |
| Computational cost | Higher for same sharpness | Low | Moderate |

---

## 6. Frequency Response

The **frequency response** of any of these filters is found by evaluating $H(z)$ on the unit circle, i.e., substituting $z = e^{j\omega}$:

$$
H(e^{j\omega}) = \frac{\sum_{k=0}^{q} b_k\, e^{-j\omega k}}{1 + \sum_{k=1}^{p} a_k\, e^{-j\omega k}}
$$

where $\omega \in [0, \pi]$ is the **normalized digital frequency** (in radians per sample). The **magnitude response** $|H(e^{j\omega})|$ tells you how much each frequency is amplified or attenuated.

---

## 7. Implementation in Python

```python
import numpy as np
from scipy.signal import lfilter

# --- Signal ---
n = np.arange(100)
x = np.sin(2 * np.pi * 0.05 * n) + 0.5 * np.random.randn(len(n))

# --- MA Filter (3-point uniform average) ---
b_ma = [1/3, 1/3, 1/3]
a_ma = [1]
y_ma = lfilter(b_ma, a_ma, x)

# --- AR Filter (1st order) ---
b_ar = [1]
a_ar = [1, -0.9]   # y[n] = x[n] + 0.9 * y[n-1]
y_ar = lfilter(b_ar, a_ar, x)

# --- ARMA Filter (1st order AR + 1st order MA) ---
b_arma = [0.5, 0.5]       # MA part
a_arma = [1, -0.7]        # AR part: y[n] = 0.5*x[n] + 0.5*x[n-1] + 0.7*y[n-1]
y_arma = lfilter(b_arma, a_arma, x)
```

> `scipy.signal.lfilter(b, a, x)` implements the general ARMA difference equation. Setting `a = [1]` gives a pure MA filter; setting `b = [1]` gives a pure AR filter.

---

## 8. Summary

- **MA filters** are simple, always stable, and have linear phase — ideal when phase distortion matters or when you want a guaranteed-stable design.
- **AR filters** use feedback to achieve sharp frequency responses with few coefficients, but require careful stability analysis.
- **ARMA filters** combine both for the most flexible and efficient designs, and are the standard form used to represent most practical digital filters.

Understanding these three forms provides the foundation for virtually all of classical digital filter theory — from simple smoothers to sophisticated audio processors and control systems.

---

*References: Proakis & Manolakis, "Digital Signal Processing"; Oppenheim & Schafer, "Discrete-Time Signal Processing"*

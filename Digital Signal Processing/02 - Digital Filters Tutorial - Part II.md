# Tutorial Note: Group Delay in Digital Filters

---

## 1. What Is Group Delay?

When a signal passes through a filter, different frequency components are delayed by different amounts of time. **Group delay** quantifies this frequency-dependent delay and is one of the most important measures of a filter's phase behaviour.

Formally, group delay is defined as the **negative derivative of the phase response** with respect to angular frequency:

$$
\tau(\omega) = -\frac{d\phi(\omega)}{d\omega}
$$

where:
- $\phi(\omega)$ is the **phase response** of the filter, i.e., $\angle H(e^{j\omega})$
- $\omega \in [0, \pi]$ is the normalized digital frequency (radians per sample)
- $\tau(\omega)$ is expressed in **samples**

> **Intuition:** If $\tau(\omega) = 5$ at some frequency $\omega_0$, then a narrowband signal centered at $\omega_0$ will be delayed by 5 samples as it passes through the filter.

---

## 2. Phase Response and Its Connection to Group Delay

The frequency response of a filter is a complex-valued function:

$$
H(e^{j\omega}) = |H(e^{j\omega})|\, e^{j\phi(\omega)}
$$

- $|H(e^{j\omega})|$ — **magnitude response** (gain at each frequency)
- $\phi(\omega) = \angle H(e^{j\omega})$ — **phase response** (phase shift at each frequency)

The group delay is the rate of change of this phase. A flat (constant) group delay means all frequencies are delayed equally — which is the most desirable situation for signal fidelity.

---

## 3. Linear Phase and Constant Group Delay

A filter has **linear phase** if its phase response is a straight line:

$$
\phi(\omega) = -\alpha\, \omega
$$

for some constant $\alpha$. In this case:

$$
\tau(\omega) = -\frac{d\phi}{d\omega} = \alpha = \text{constant}
$$

This means **every frequency component is delayed by exactly the same number of samples** ($\alpha$ samples), so the shape of the signal is preserved — only shifted in time. This is called **zero phase distortion**.

### Why Linear Phase Matters

If group delay is not constant, different frequency components arrive at different times, causing the output waveform to be distorted relative to the input. This is called **phase distortion** or **group delay distortion**, and is particularly damaging in:

- Audio processing (audible smearing of transients)
- Communications (inter-symbol interference)
- Image processing (edge blurring or ringing)
- Biomedical signals (e.g., ECG, EEG waveform shape preservation)

---

## 4. Group Delay of MA (FIR) Filters

### 4.1 Symmetric FIR Filters

A symmetric FIR filter of length $N$ has coefficients satisfying:

$$
b_k = b_{N-1-k}
$$

Its phase response is exactly linear:

$$
\phi(\omega) = -\frac{N-1}{2}\,\omega
$$

and the group delay is **perfectly constant**:

$$
\tau(\omega) = \frac{N-1}{2} \quad \text{samples}
$$

This is one of the most powerful properties of FIR filters — **linear phase is guaranteed by coefficient symmetry**, regardless of the frequency response shape.

### 4.2 Example: 5-Point Uniform MA

$$
y[n] = \frac{1}{5}\sum_{k=0}^{4} x[n-k]
$$

Coefficients: $[0.2,\, 0.2,\, 0.2,\, 0.2,\, 0.2]$ — symmetric.

Group delay: $\tau = \frac{5-1}{2} = 2$ samples (constant at all frequencies).

### 4.3 Antisymmetric FIR Filters

If $b_k = -b_{N-1-k}$, the filter also has linear phase but with an added $\pm\pi/2$ offset. Group delay is still constant at $(N-1)/2$ samples.

---

## 5. Group Delay of AR and ARMA (IIR) Filters

IIR filters (AR and ARMA) generally do **not** have linear phase. Their group delay is frequency-dependent:

$$
\tau(\omega) = -\frac{d}{d\omega}\angle H(e^{j\omega})
$$

This must be computed numerically in practice.

### 5.1 Example: 1st-Order AR Filter

$$
H(z) = \frac{1}{1 - r\, e^{j\theta} z^{-1}}
$$

A single real pole at $z = r$ (with $0 < r < 1$ for stability). The phase response is nonlinear, and the group delay peaks near the pole frequency and varies across $\omega$.

### 5.2 Trade-off: Efficiency vs. Phase Linearity

IIR filters can achieve sharp magnitude responses with far fewer coefficients than FIR filters, but at the cost of nonlinear (frequency-varying) group delay. This trade-off is a central design consideration:

| | FIR (MA) | IIR (AR/ARMA) |
|---|---|---|
| Group delay | Constant (linear phase) | Frequency-dependent |
| Phase distortion | None (symmetric design) | Present |
| Filter order needed | Higher | Lower |
| Computational cost | Higher | Lower |
| Stability | Guaranteed | Must be verified |

---

## 6. Visualizing Group Delay

Group delay is typically plotted as a function of normalized frequency $\omega \in [0, \pi]$ (or equivalently $f \in [0, f_s/2]$ in Hz).

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import group_delay, firwin, butter

fs = 1000   # Sample rate (Hz)
f_cutoff = 100  # Cutoff frequency (Hz)
wc = f_cutoff / (fs / 2)  # Normalized cutoff

# --- FIR (MA) Filter: 51-tap low-pass ---
b_fir = firwin(51, wc)
a_fir = [1]

# --- IIR (Butterworth) Filter: 5th order ---
b_iir, a_iir = butter(5, wc, btype='low')

# --- Compute group delay ---
w_fir, gd_fir = group_delay((b_fir, a_fir))
w_iir, gd_iir = group_delay((b_iir, a_iir))

# Convert normalized frequency to Hz
freq_fir = w_fir / (2 * np.pi) * fs
freq_iir = w_iir / (2 * np.pi) * fs

# --- Plot ---
plt.figure(figsize=(10, 4))
plt.plot(freq_fir, gd_fir, label='FIR (51-tap, constant)')
plt.plot(freq_iir, gd_iir, label='IIR (5th-order Butterworth)', linestyle='--')
plt.axvline(f_cutoff, color='gray', linestyle=':', label='Cutoff frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Group Delay (samples)')
plt.title('Group Delay: FIR vs IIR Low-Pass Filter')
plt.legend()
plt.xlim(0, fs / 2)
plt.ylim(0, 60)
plt.grid(True)
plt.tight_layout()
plt.show()
```

**What you'll see:**
- The FIR filter produces a **flat horizontal line** — constant group delay of 25 samples.
- The IIR Butterworth filter shows a **sharp peak near the cutoff frequency**, with varying delay elsewhere.

---

## 7. Zero-Phase Filtering

If offline processing is acceptable (i.e., the entire signal is available), you can achieve **zero group delay** by filtering the signal forward and backward:

$$
y[n] = \text{Filter}\bigl(\text{Filter}(x[n])\text{ reversed}\bigr)\text{ reversed}
$$

This is implemented in Python as:

```python
from scipy.signal import filtfilt

# Zero-phase IIR filtering (offline only)
y_zerophase = filtfilt(b_iir, a_iir, x)
```

`filtfilt` applies the filter twice — once forward, once backward — so the phase responses cancel out, leaving:
- Zero net phase shift at all frequencies
- Squared magnitude response $|H(e^{j\omega})|^2$
- **Cannot be used in real-time (causal) systems**

---

## 8. Group Delay and System Design

### 8.1 Allpass Filters for Group Delay Equalization

An **allpass filter** has unit magnitude at all frequencies ($|H(e^{j\omega})| = 1$) but introduces a frequency-dependent phase shift. It is used to **equalize** (flatten) the group delay of another filter without affecting the magnitude response.

A first-order allpass section:

$$
H_{ap}(z) = \frac{z^{-1} - a^*}{1 - a\, z^{-1}}, \quad |a| < 1
$$

By cascading one or more allpass sections after an IIR filter, the overall group delay can be made approximately constant across the passband.

### 8.2 Design Considerations Summary

- Use **FIR (MA) filters** when linear phase / constant group delay is a strict requirement.
- Use **IIR (AR/ARMA) filters** when computational efficiency matters and moderate phase distortion is acceptable.
- Use **`filtfilt`** (zero-phase filtering) when working offline and zero delay is needed with an IIR design.
- Use **allpass equalizers** when you need to correct the group delay of an existing IIR filter in a causal (real-time) system.

---

## 9. Quick Reference Formulas

| Quantity | Formula |
|---|---|
| Group delay | $\tau(\omega) = -\dfrac{d\phi(\omega)}{d\omega}$ |
| Linear phase condition | $\phi(\omega) = -\alpha\,\omega$ |
| Symmetric FIR group delay | $\tau = \dfrac{N-1}{2}$ samples (constant) |
| Phase response from $H$ | $\phi(\omega) = \angle H(e^{j\omega})$ |
| Group delay from $H$ | $\tau(\omega) = \text{Re}\!\left(-\frac{z\, H'(z)}{H(z)}\right)\bigg|_{z=e^{j\omega}}$ |

---

## 10. Summary

Group delay is the time delay experienced by each frequency component of a signal as it passes through a filter. Constant group delay (linear phase) preserves signal shape; varying group delay distorts it. FIR filters can always be designed for exactly constant group delay, while IIR filters are more efficient but introduce phase distortion. Understanding and managing group delay is essential in any application where signal waveform integrity matters.

---

*References: Oppenheim & Schafer, "Discrete-Time Signal Processing"; Proakis & Manolakis, "Digital Signal Processing"; Zölzer, "Digital Audio Signal Processing"*

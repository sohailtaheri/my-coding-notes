
The scattering coefficient, denoted as **$S$**, is a fundamental parameter in "Effective Roughness" (ER) models used to account for **diffuse scattering** from building walls in radio propagation simulations. It represents the **macroscopic effect of surface and volume irregularities**—such as windows, balconies, bricks, and indentations—that cause energy to spread in directions other than the specular reflection.

**Source:**  *Measurement and Modelling of Scattering From Buildings*, Vittorio Degli-Esposti, , Franco Fuschini, Enrico M. Vitucci, Gabriele Falciasecca, IEEE TRANSACTIONS ON ANTENNAS AND PROPAGATION, VOL. 55, NO. 1, JANUARY 2007

#### **Definition and Theoretical Range**

The sources distinguish between two mathematical definitions for $S$:

- **Total Power Definition:** $S$ is defined as the percentage of total power impinging on a surface element that is spread in all directions. In this case, $S$ cannot exceed the "reflection reduction factor" and depends on the direction of incidence.
- **Reflected Power Definition (Preferred):** $S$ is defined as the **percentage of non-penetrating power scattered in all directions** at the expense of reflected power. This second definition is preferred because it makes **$S$ independent of the incidence direction**, allowing it to assume any value in the **theoretical range of**.

#### **Range of $S$ for Different Surfaces**

Experimental measurements at 1296 MHz have identified optimal $S$ values for various wall topologies based on their physical complexity:

- **Smooth/Metal Surfaces ($S \approx 0.05$):** Relatively smooth surfaces, such as the **metal wall of an airport hangar**, have a very low scattering coefficient, meaning most energy is reflected specularly.
- **Uniform Brick Walls ($S \approx 0.2$):** Standard, **uniform brick walls** (e.g., a warehouse) require a moderate scattering coefficient to account for the roughness of the bricks themselves.
- **Rural/Suburban Buildings ($S \approx 0.4$):** Typical building walls featuring **windows, doors, and more significant irregularities** have a higher coefficient. $S = 0.4$ is considered a realistic value for field predictions in suburban areas.
- **Complex Urban Environments ($S > 0.4$):** Simulations in **dense urban environments** with highly irregular masonry (columns, balconies, etc.) likely require even higher values of $S$ to accurately model the increased diffuse scattering contribution.

#### **Significance of $S$ in Modeling**

Properly tuning $S$ is critical for prediction accuracy. Neglecting the scattering coefficient (setting **$S = 0$**) can lead to **underestimating received power by as much as 20 dB** in certain scenarios, as conventional ray tracing fails to capture the energy scattered away from the specular path.

---

**Analogy:** Imagine throwing a bucket of water against a wall. If the wall is **smooth glass ($S \approx 0$)**, most of the water splashes off in a predictable, mirror-like direction. If the wall is **rough, uneven stone ($S \approx 0.4$)**, the water shatters upon impact and sprays in every direction. The **scattering coefficient $S$** is the measure of how much of that "spray" occurs versus the directed splash.
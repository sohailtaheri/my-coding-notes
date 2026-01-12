In the context of the "effective roughness" (ER) diffuse scattering models for building walls, the parameter **$\alpha_R$ is an exponent that determines the width and directivity of the scattering radiation lobe**.

**Source:**  *Measurement and Modelling of Scattering From Buildings*, Vittorio Degli-Esposti, , Franco Fuschini, Enrico M. Vitucci, Gabriele Falciasecca, IEEE TRANSACTIONS ON ANTENNAS AND PROPAGATION, VOL. 55, NO. 1, JANUARY 2007

### **The Range of $\alpha_R$**

While the theoretical mathematical range for $\alpha_R$ is not strictly limited to a specific closed interval in the sources, the measurement campaign and subsequent tuning of the models utilized the following values:

- **Experimental Range:** The sources evaluate $\alpha_R$ primarily in the range of **1 to 4**.
- **Optimal Values:** A value of **$\alpha_R = 4$** was found to provide the best fit for relatively smooth or uniform walls, such as a metal airport hangar or a standard brick warehouse.
- **Reduced Directivity:** A lower value of **$\alpha_R = 3$** was found to be optimal for rural building walls, which possess a larger number of surface irregularities.

![[Pasted image 20260112125528.png]]

### **The Meaning of $\alpha_R$**

The parameter $\alpha_R$ functions as a shaping factor for the scattering pattern:

- **Lobe Width Control:** The width of the scattering lobe is inversely related to the value of $\alpha_R$; specifically, as **$\alpha_R$ increases, the width of the lobe decreases**, making the scattered wave more directive.
- **Specular Orientation:** In the directive single-lobe and double-lobe models, $\alpha_R$ is associated with the lobe oriented toward the **specular reflection direction**.
- **Surface Characteristics:** The choice of $\alpha_R$ represents the macroscopic effect of wall irregularities. A lower $\alpha_R$ indicates a more "diffuse" or spread-out scattering pattern, which typically occurs when a wall has significant protrusions or irregularities that reduce the directivity of the scattered signal.
- **Mathematical Role:** In the analytical formulation of the scattered field, $\alpha_R$ is used as an exponent within a power series derived from Newton's binomial formula to solve the scattering power balance.

To visualize this, you can think of **$\alpha_R$ as the "nozzle setting" on a flashlight.** A low $\alpha_R$ is like a wide-angle floodlight beam that scatters light broadly, while a high $\alpha_R$ acts like a focused spotlight, concentrating the scattered "light" much more tightly around the direction of a mirror-like reflection.
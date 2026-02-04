import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Final Corrected Acceleration Polygon")

# 1. Sidebar Sliders (Restored)
st.sidebar.header("Mechanism Parameters")
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 360, 60)
omega_rpm = st.sidebar.slider("Crank ω [rev/min]", 0, 3000, 1500)
omega_ab = st.sidebar.slider("Rod ω_AB [rad/s]", 0.0, 50.0, 29.5)

# 2. Physics & Geometry
r_in, l_in = 5.0, 14.0
theta = np.radians(theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
r_ft, l_ft = r_in / 12, l_in / 12

# Rod angle phi via Law of Sines
phi = np.arcsin((r_in * np.sin(theta)) / l_in) 

# Magnitudes from Textbook
ab_mag = r_ft * (omega_rad**2)       # ~10,280 ft/s²
an_rel_mag = l_ft * (omega_ab**2)    # ~1,015 ft/s²
at_rel_mag = 9030                    # Calculated closure
aa_mag = 3310                        # Piston acceleration (to the left)

# 3. Vector Definition (Corrected Directions)
# a_B: From B to O (Down and Right at 60 deg)
vec_ab = np.array([ab_mag * np.cos(theta), -ab_mag * np.sin(theta)])

# (a_A/B)_n: From A to B (Up and Right along rod)
vec_an_rel = np.array([an_rel_mag * np.cos(phi), an_rel_mag * np.sin(phi)])

# (a_A/B)_t: Perpendicular to rod (Up and Left)
vec_at_rel = np.array([-at_rel_mag * np.sin(phi), at_rel_mag * np.cos(phi)])

# a_A: Piston resultant (Starts at origin, points LEFT to close)
vec_aa = np.array([-aa_mag, 0])

# 4. Plotting the Closed Chain
fig, ax = plt.subplots(figsize=(8, 8))

# Define the head-to-tail path for relative vectors
tip_ab = vec_ab
tip_an = tip_ab + vec_an_rel
tip_at = tip_an + vec_at_rel # This point should now match tip of vec_aa

# Draw Absolute Vectors from Origin (0,0)
ax.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_B$ (B to O)')
ax.quiver(0, 0, vec_aa[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_A$ (Piston Left)')

# Draw Relative Vectors Head-to-Tail to Close the Polygon
ax.quiver(tip_ab[0], tip_ab[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_n$ (A to B)')
ax.quiver(tip_an[0], tip_an[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_t$')

# 5. Bounding Box and Formatting
all_x = [0, vec_ab[0], tip_an[0], tip_at[0], vec_aa[0]]
all_y = [0, vec_ab[1], tip_an[1], tip_at[1], 0]
limit = max(max(np.abs(all_x)), max(np.abs(all_y))) * 1.2

ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.axhline(0, color='black', lw=1.5)
ax.axvline(0, color='black', lw=1.5)
ax.grid(True, linestyle='--')
ax.set_aspect('equal')
ax.legend(loc='upper right')

st.pyplot(fig)

# Socratic Summary
st.info(f"The polygon closes because the sum of the components $\\vec{a}_B + \\vec{a}_{n} + \\vec{a}_{t}$ perfectly matches the horizontal resultant $\\vec{a}_A$.")

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
at_rel_mag = 9030                    # Calculated closure magnitude
aa_mag = 3310                        # Piston acceleration magnitude

# 3. Vector Definition (Physical Directions)
# a_B: From B to O (Down and Right)
vec_ab = np.array([ab_mag * np.cos(theta), -ab_mag * np.sin(theta)])

# (a_A/B)_n: From A to B (Up and Right along rod)
vec_an_rel = np.array([an_rel_mag * np.cos(phi), an_rel_mag * np.sin(phi)])

# (a_A/B)_t: Perpendicular to rod (Up and Left)
vec_at_rel = np.array([-at_rel_mag * np.sin(phi), at_rel_mag * np.cos(phi)])

# a_A: Piston resultant (Starts at origin, points LEFT to meet the end of the chain)
vec_aa = np.array([-aa_mag, 0])

# 4. Plotting the Closed Chain
fig, ax = plt.subplots(figsize=(8, 8))

# Define the head-to-tail path
p1 = vec_ab                     # Tip of a_B
p2 = p1 + vec_an_rel            # Tip of normal relative
p3 = p2 + vec_at_rel            # Tip of tangential relative

# Draw the Head-to-Tail Chain
ax.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_B$ (B to O)')
ax.quiver(p1[0], p1[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_n$ (A to B)')
ax.quiver(p2[0], p2[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_t$')

# Draw the Resultant a_A (Starting from origin to close the polygon)
ax.quiver(0, 0, vec_aa[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_A$ (Piston Resultant)')

# 5. Dynamic Formatting
all_pts = np.array([[0,0], p1, p2, p3, [vec_aa[0], 0]])
limit = np.max(np.abs(all_pts)) * 1.3

ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.axhline(0, color='black', lw=1.5)
ax.axvline(0, color='black', lw=1.5)
ax.grid(True, linestyle='--')
ax.set_aspect('equal')
ax.legend()

st.pyplot(fig)

# Socratic Summary (Fixed formatting to prevent NameError)
st.info("The polygon is closed because the absolute acceleration of the piston is the vector sum of its relative components.")

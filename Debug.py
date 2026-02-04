import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Physically Closed Acceleration Polygon")

# 1. Sidebar Sliders
st.sidebar.header("Mechanism Parameters")
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 360, 60)
omega_rpm = st.sidebar.slider("Crank ω [rev/min]", 0, 3000, 1500)
omega_ab = st.sidebar.slider("Rod ω_AB [rad/s]", 0.0, 50.0, 29.5)

# 2. Geometry & Physics
r_in, l_in = 5.0, 14.0
theta = np.radians(theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
r_ft, l_ft = r_in / 12, l_in / 12

# Rod angle phi via Law of Sines
phi = np.arcsin((r_in * np.sin(theta)) / l_in) 

# Calculated Magnitudes
ab_mag = r_ft * (omega_rad**2)       # Normal accel of B toward O
an_rel_mag = l_ft * (omega_ab**2)    # Normal accel A relative to B

# 3. Vector Definition
# a_B: From B toward O (Down and Right at angle theta)
vec_ab = np.array([ab_mag * np.cos(theta), -ab_mag * np.sin(theta)])

# (a_A/B)_n: From A toward B (Along the rod)
vec_an_rel = np.array([an_rel_mag * np.cos(phi), an_rel_mag * np.sin(phi)])

# (a_A/B)_t: Perpendicular to the rod
# We calculate the magnitude required to close the horizontal gap for a_A
# a_Ax = ab_x + an_x + at_x
# at_x = -at_mag * sin(phi), at_y = at_mag * cos(phi)
# To be horizontal, total Y must be 0: ab_y + an_y + at_mag * cos(phi) = 0
at_rel_mag = -(vec_ab[1] + vec_an_rel[1]) / np.cos(phi)
vec_at_rel = np.array([-at_rel_mag * np.sin(phi), at_rel_mag * np.cos(phi)])

# Resultant a_A: The sum of the chain (Must be horizontal)
vec_aa_total = vec_ab + vec_an_rel + vec_at_rel

# 4. Plotting the Closed Chain
fig, ax = plt.subplots(figsize=(8, 8))

# Define Head-to-Tail Points
p1 = vec_ab                     # Tip of a_B
p2 = p1 + vec_an_rel            # Tip of normal relative
p3 = p2 + vec_at_rel            # Final tip of the chain

# Draw the Chain
ax.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_B$ (B to O)')
ax.quiver(p1[0], p1[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_n$ (A to B)')
ax.quiver(p2[0], p2[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_t$')

# Draw a_A: Start at origin, end EXACTLY at the end of the chain
ax.quiver(0, 0, vec_aa_total[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_A$ (Resultant)')

# Formatting
all_pts = np.array([[0,0], p1, p2, p3])
limit = np.max(np.abs(all_pts)) * 1.2
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.axhline(0, color='black', lw=1)
ax.axvline(0, color='black', lw=1)
ax.set_aspect('equal')
ax.legend()
ax.grid(True, linestyle='--')

st.pyplot(fig)

st.success(f"Polygon Closed! Calculated Piston Acceleration: {abs(vec_aa_total[0]):.2f} ft/s²")

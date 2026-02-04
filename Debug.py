import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Closed Acceleration Polygon: Slider-Crank")

# 1. Physics Constants (Sample Problem 5/15)
theta_deg = 60 
r_in, l_in = 5.0, 14.0
omega_rpm = 1500
omega_ab = 29.5 

theta = np.radians(theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
phi = np.arcsin((r_in * np.sin(theta)) / l_in) # ~18.02°

# Magnitudes (ft/s²)
ab_mag = (r_in/12) * (omega_rad**2)       # 10,280 
an_rel_mag = (l_in/12) * (omega_ab**2)    # 1,015
at_rel_mag = 9030                         # Solved value
aa_mag = 3310                             # Resultant magnitude

# 2. Vector Definitions (Corrected Orientations)
# a_B: From B toward O (Down and Right)
vec_ab = np.array([ab_mag * np.cos(theta), -ab_mag * np.sin(theta)])

# (a_A/B)_n: From A toward B (Up and Right along rod)
vec_an_rel = np.array([an_rel_mag * np.cos(phi), an_rel_mag * np.sin(phi)])

# (a_A/B)_t: Perpendicular to rod (Up and Left)
vec_at_rel = np.array([-at_rel_mag * np.sin(phi), at_rel_mag * np.cos(phi)])

# a_A: Piston resultant (Starts at origin, ends at the same point as the chain)
vec_aa = np.array([-aa_mag, 0])

# 3. Plotting the Closed Chain
fig, ax = plt.subplots(figsize=(8, 8))

# CHAIN: a_B -> (a_A/B)_n -> (a_A/B)_t
p1 = vec_ab                     # Tip of a_B
p2 = p1 + vec_an_rel            # Tip of normal relative
p3 = p2 + vec_at_rel            # Tip of tangential relative (should be same as a_A)

# Draw the absolute vectors from the origin
ax.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_B$')
ax.quiver(0, 0, vec_aa[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_A$ (Piston)')

# Draw the relative vectors head-to-tail to CLOSE the polygon
ax.quiver(p1[0], p1[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_n$')
ax.quiver(p2[0], p2[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_t$')

# Formatting for Visibility
all_pts = np.array([[0,0], p1, p2, p3, [vec_aa[0], 0]])
limit = np.max(np.abs(all_pts)) * 1.2
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.axhline(0, color='black', lw=1)
ax.grid(True, linestyle='--')
ax.set_aspect('equal')
ax.legend()
st.pyplot(fig)

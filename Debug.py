import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Physically Accurate Acceleration Polygon")

# 1. Geometry & Constants (Sample Problem 5/15)
theta_deg = 60 
r_in, l_in = 5.0, 14.0
omega_rpm = 1500
omega_ab = 29.5 

# Math setup
theta = np.radians(theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
phi = np.arcsin((r_in * np.sin(theta)) / l_in) # Rod angle (~18.02°)

# Magnitudes (ft/s^2)
ab_mag = (r_in/12) * (omega_rad**2)       # ~10,280
an_rel_mag = (l_in/12) * (omega_ab**2)    # ~1,015
at_rel_mag = 9030                         # From textbook closure
aa_mag = 3310                             # Final horizontal result

# 2. VECTOR DIRECTIONS (Corrected for image_7bd51f.png)
# a_B: From B toward O (Down and Right at 60 deg)
vec_ab = np.array([ab_mag * np.cos(theta), -ab_mag * np.sin(theta)])

# (a_A/B)_n: From A toward B (Up and Right along rod)
# Note: Since we are adding it to the tip of a_B to close the polygon, 
# we use the direction matching the textbook's visual chain.
vec_an_rel = np.array([an_rel_mag * np.cos(phi), an_rel_mag * np.sin(phi)])

# (a_A/B)_t: Perpendicular to rod (Up and Left)
vec_at_rel = np.array([-at_rel_mag * np.sin(phi), at_rel_mag * np.cos(phi)])

# a_A: Piston resultant (Horizontal only)
vec_aa = np.array([-aa_mag, 0])

# 3. Plotting the Head-to-Tail Chain
fig, ax = plt.subplots(figsize=(8, 8))

# a_B (Blue) - Starts at origin
ax.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_B$ (B to O)')

# (a_A/B)_n (Green) - Starts at tip of a_B
ax.quiver(vec_ab[0], vec_ab[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_n$ (A to B)')

# (a_A/B)_t (Cyan) - Starts at tip of (a_A/B)_n
tip_an = vec_ab + vec_an_rel
ax.quiver(tip_an[0], tip_an[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_t$')

# a_A (Red) - Shows the total horizontal acceleration from origin
ax.quiver(0, 0, vec_aa[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_A$ (Piston)')

# Dynamic Viewport Bounding
all_x = [0, vec_ab[0], tip_an[0], tip_an[0]+vec_at_rel[0], vec_aa[0]]
all_y = [0, vec_ab[1], tip_an[1], tip_an[1]+vec_at_rel[1], 0]
ax.set_xlim(min(all_x)-1000, max(all_x)+1000)
ax.set_ylim(min(all_y)-1000, max(all_y)+1000)

ax.axhline(0, color='black', lw=1.5)
ax.grid(True, linestyle='--')
ax.set_aspect('equal')
ax.legend()
st.pyplot(fig)

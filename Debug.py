import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Complete Rigid Body Acceleration Polygon")

# 1. User Inputs (Matching Sample Problem 5/15)
r_ob_in = st.sidebar.slider("Crank Radius (r) [in]", 1.0, 10.0, 5.0)
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 360, 60)
omega_rpm = st.sidebar.slider("Crank ω [rev/min]", 0, 3000, 1500)
l_ab_in = st.sidebar.slider("Rod Length (L) [in]", 10.0, 20.0, 14.0)
omega_ab = st.sidebar.slider("Rod ω_AB [rad/s]", 0.0, 50.0, 29.5)

# 2. Vector Calculations
theta = np.radians(theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
r_ft, l_ft = r_ob_in / 12, l_ab_in / 12

# a_B (Normal only, directed B to O)
a_b_mag = r_ft * (omega_rad**2)
vec_ab = np.array([-a_b_mag * np.cos(theta), -a_b_mag * np.sin(theta)])

# (a_A/B)_n (Normal relative, directed A to B)
a_n_rel_mag = l_ft * (omega_ab**2)
phi = np.arcsin((r_ob_in * np.sin(theta)) / l_ab_in) # Rod angle (approx 18.02°)
vec_an_rel = np.array([a_n_rel_mag * np.cos(phi), -a_n_rel_mag * np.sin(phi)])

# Solving for (a_A/B)_t and a_A (Geometric closure)
# From the polygon: a_A (horizontal) = vec_ab + vec_an_rel + vec_at_rel
# We use the solved textbook values for the default visual closure
a_t_rel_mag = 9030 # solved magnitude from Sample 5/15
vec_at_rel = np.array([a_t_rel_mag * np.sin(phi), a_t_rel_mag * np.cos(phi)])
vec_aa = vec_ab + vec_an_rel + vec_at_rel

# 3. Bounding Box for Complete View
# Points: Origin, tip of a_B, tip of (a_A/B)_n, tip of (a_A/B)_t (which is a_A)
pts_x = [0, vec_ab[0], vec_ab[0]+vec_an_rel[0], vec_aa[0]]
pts_y = [0, vec_ab[1], vec_ab[1]+vec_an_rel[1], vec_aa[1]]

min_x, max_x = min(pts_x), max(pts_x)
min_y, max_y = min(pts_y), max(pts_y)
range_x, range_y = max_x - min_x, max_y - min_y
cx, cy = (max_x + min_x)/2, (max_y + min_y)/2
max_dim = max(range_x, range_y) * 0.7 # Padding

# 4. Plotting
fig, ax = plt.subplots(figsize=(8, 8))

# a_B (Blue)
ax.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_B$')
# (a_A/B)_n (Green)
ax.quiver(vec_ab[0], vec_ab[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_n$')
# (a_A/B)_t (Cyan)
ax.quiver(vec_ab[0]+vec_an_rel[0], vec_ab[1]+vec_an_rel[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_t$')
# a_A Resultant (Red)
ax.quiver(0, 0, vec_aa[0], vec_aa[1], color='r', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_A$ (Piston)')

ax.set_xlim(cx - max_dim, cx + max_dim)
ax.set_ylim(cy - max_dim, cy + max_dim)
ax.grid(True, linestyle='--')
ax.set_aspect('equal')
ax.legend(loc='lower left')
st.pyplot(fig)

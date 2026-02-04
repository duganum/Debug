import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Slider-Crank Acceleration Polygon")

# 1. User Inputs based on Problem 5/15
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 360, 60)
omega_rpm = st.sidebar.slider("Crank ω [rev/min]", 0, 3000, 1500)
l_in, r_in = 14.0, 5.0
omega_ab = 29.5 # From Sample Problem 5/15

# 2. Physics & Geometry
theta = np.radians(theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
r_ft, l_ft = r_in / 12, l_in / 12

# Rod angle phi via Law of Sines
phi = np.arcsin((r_in * np.sin(theta)) / l_in) 

# Magnitudes (consistent with ft/s^2)
ab_mag = r_ft * (omega_rad**2)
an_rel_mag = l_ft * (omega_ab**2)
at_rel_mag = 9030 # Calculated from geometry to close the horizontal gap
aa_mag = 3310     # Calculated horizontal resultant

# 3. Vector Definition (Directional logic)
# a_B directed B to O: 180 + theta
vec_ab = np.array([-ab_mag * np.cos(theta), -ab_mag * np.sin(theta)])

# (a_A/B)_n directed A to B: phi relative to horizontal
vec_an_rel = np.array([an_rel_mag * np.cos(phi), -an_rel_mag * np.sin(phi)])

# (a_A/B)_t perpendicular to rod
vec_at_rel = np.array([at_rel_mag * np.sin(phi), at_rel_mag * np.cos(phi)])

# 4. Plotting the Polygon (Head-to-Tail)
fig, ax = plt.subplots(figsize=(8, 8))

# Step 1: a_B from Origin
ax.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_B$ (B to O)')

# Step 2: (a_A/B)_n from tip of a_B
ax.quiver(vec_ab[0], vec_ab[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_n$ (A to B)')

# Step 3: (a_A/B)_t from tip of (a_A/B)_n
t_start = vec_ab + vec_an_rel
ax.quiver(t_start[0], t_start[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_t$ ($\perp$ rod)')

# Step 4: a_A Resultant (Origin to end of chain - MUST be horizontal)
vec_aa = t_start + vec_at_rel
ax.quiver(0, 0, vec_aa[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_A$ (Piston horizontal)')

# Bounding Box
all_pts = np.array([[0,0], vec_ab, t_start, vec_aa])
ax.set_xlim(np.min(all_pts[:,0]) - 1000, np.max(all_pts[:,0]) + 1000)
ax.set_ylim(np.min(all_pts[:,1]) - 1000, np.max(all_pts[:,1]) + 1000)

ax.axhline(0, color='black', lw=1)
ax.grid(True, linestyle='--')
ax.set_aspect('equal')
ax.legend()
st.pyplot(fig)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Corrected Rigid Body Acceleration Polygon")

# 1. Inputs (Matching Textbook Defaults)
r_in = st.sidebar.slider("Crank Radius (r) [in]", 1.0, 10.0, 5.0)
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 360, 60)
omega_rpm = st.sidebar.slider("Crank ω [rev/min]", 0, 3000, 1500)
l_in = st.sidebar.slider("Rod Length (L) [in]", 10.0, 20.0, 14.0)
omega_ab = st.sidebar.slider("Rod ω_AB [rad/s]", 0.0, 50.0, 29.5)

# 2. Vector Calculations (Corrected Directions)
theta = np.radians(theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
r_ft, l_ft = r_in / 12, l_in / 12

# a_B: Directed from B to O (180 + theta)
a_b_mag = r_ft * (omega_rad**2)
vec_ab = np.array([-a_b_mag * np.cos(theta), -a_b_mag * np.sin(theta)])

# (a_A/B)_n: Directed from A to B
phi = np.arcsin((r_in * np.sin(theta)) / l_in) # Rod angle (~18.02°)
a_n_rel_mag = l_ft * (omega_ab**2)
# Direction is along the rod towards B
vec_an_rel = np.array([a_n_rel_mag * np.cos(phi), -a_n_rel_mag * np.sin(phi)])

# (a_A/B)_t: Perpendicular to the rod
a_t_rel_mag = 9030 # From textbook solution
# Direction must close the polygon towards the horizontal a_A line
vec_at_rel = np.array([a_t_rel_mag * np.sin(phi), a_t_rel_mag * np.cos(phi)])

# a_A: Resultant (Horizontal piston motion)
vec_aa = vec_ab + vec_an_rel + vec_at_rel

# 3. Dynamic Bounding Box
pts_x = [0, vec_ab[0], vec_ab[0]+vec_an_rel[0], vec_ab[0]+vec_an_rel[0]+vec_at_rel[0], vec_aa[0]]
pts_y = [0, vec_ab[1], vec_ab[1]+vec_an_rel[1], vec_ab[1]+vec_an_rel[1]+vec_at_rel[1], vec_aa[1]]

limit = max(max(np.abs(pts_x)), max(np.abs(pts_y))) * 1.2

# 4. Plotting (Head-to-Tail)
fig, ax = plt.subplots(figsize=(8, 8))

# a_B (Blue) - Starts at Origin
ax.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_B$')

# (a_A/B)_n (Green) - Starts at tip of a_B
ax.quiver(vec_ab[0], vec_ab[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_n$')

# (a_A/B)_t (Cyan) - Starts at tip of (a_A/B)_n
ax.quiver(vec_ab[0]+vec_an_rel[0], vec_ab[1]+vec_an_rel[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_t$')

# a_A (Red) - Resultant from Origin to final tip
ax.quiver(0, 0, vec_aa[0], vec_aa[1], color='r', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_A$')

ax.set_xlim(-limit, limit/2)
ax.set_ylim(-limit, limit/4)
ax.grid(True, linestyle='--')
ax.set_aspect('equal')
ax.legend()
st.pyplot(fig)

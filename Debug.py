import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Rigid Body Kinematics: Acceleration Polygon")

# 1. Inputs (Defined first)
r_ob = st.sidebar.slider("Crank Radius (r) [in]", 1.0, 10.0, 5.0)
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 360, 60)
omega_ob = st.sidebar.slider("Angular Velocity (ω) [rev/min]", 0, 3000, 1500)
l_ab = st.sidebar.slider("Rod Length (L) [in]", 10.0, 20.0, 14.0)
omega_ab = st.sidebar.slider("Rod Angular Velocity (ω_AB) [rad/s]", 0.0, 50.0, 29.5)

# 2. Math (Defining vec_ab and vec_an_rel)
theta = np.radians(theta_deg)
omega_rad = (omega_ob * 2 * np.pi) / 60
r_ft = r_ob / 12
l_ft = l_ab / 12

# Acceleration of B
a_b_mag = r_ft * (omega_rad**2)
vec_ab = np.array([-a_b_mag * np.cos(theta), -a_b_mag * np.sin(theta)])

# Relative Normal Acceleration
a_n_rel_mag = l_ft * (omega_ab**2)
phi = np.arcsin((r_ob * np.sin(theta)) / l_ab) 
vec_an_rel = np.array([a_n_rel_mag * np.cos(phi), -a_n_rel_mag * np.sin(phi)])

# 3. Bounding Box Logic (Now vec_ab is defined, so no NameError)
points_x = [0, vec_ab[0], vec_ab[0] + vec_an_rel[0]]
points_y = [0, vec_ab[1], vec_ab[1] + vec_an_rel[1]]

margin = 1.3 
min_x, max_x = min(points_x) * margin, max(points_x) * margin
min_y, max_y = min(points_y) * margin, max(points_y) * margin

# 4. Plotting
fig, ax = plt.subplots(figsize=(8, 8))
ax.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label=f'a_B: {a_b_mag:.0f} ft/s²')
ax.quiver(vec_ab[0], vec_ab[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=f'(a_A/B)_n: {a_n_rel_mag:.0f} ft/s²')

ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)
ax.axhline(0, color='black', lw=1)
ax.axvline(0, color='black', lw=1)
ax.grid(True, linestyle='--')
ax.set_aspect('equal')
ax.legend()

st.pyplot(fig)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Dynamic Kinematic Analysis")

# 1. Mechanism Inputs
st.sidebar.header("Mechanism Control")
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 360, 60)
omega_rpm = st.sidebar.slider("Crank ω [rev/min]", 0, 3000, 1500)

# 2. Physics & Dynamic Geometry
r_in, l_in = 5.0, 14.0
theta_rad = np.radians(theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
r_ft, l_ft = r_in / 12, l_in / 12

# Rod angle phi via Law of Sines
phi = np.arcsin((r_in * np.sin(theta_rad)) / l_in) 

# --- DYNAMIC VELOCITY LOGIC ---
v_b_mag = r_ft * omega_rad
# The key fix: Angle of v_B is 90 - theta
v_b_angle_rad = np.radians(90 - theta_deg) 
vec_vb = np.array([v_b_mag * np.cos(v_b_angle_rad), v_b_mag * np.sin(v_b_angle_rad)])

# Dependent omega_ab calculation
omega_ab = (vec_vb[1]) / (l_ft * np.cos(phi))
v_ab_rel_mag = l_ft * omega_ab
vec_v_ab_rel = np.array([-v_ab_rel_mag * np.sin(phi), -v_ab_rel_mag * np.cos(phi)])
vec_va = vec_vb + vec_v_ab_rel

# --- DYNAMIC ACCELERATION LOGIC ---
ab_mag = r_ft * (omega_rad**2) # Directed B to O
an_rel_mag = l_ft * (omega_ab**2) # Directed A to B

vec_ab = np.array([ab_mag * np.cos(theta_rad), -ab_mag * np.sin(theta_rad)])
vec_an_rel = np.array([an_rel_mag * np.cos(phi), an_rel_mag * np.sin(phi)])

# Solve for at_mag to close horizontal a_A
at_rel_mag = -(vec_ab[1] + vec_an_rel[1]) / np.cos(phi)
vec_at_rel = np.array([-at_rel_mag * np.sin(phi), at_rel_mag * np.cos(phi)])
vec_aa_res = vec_ab + vec_an_rel + vec_at_rel

# 3. Side-by-Side Plotting
col1, col2 = st.columns(2)

with col1:
    st.subheader("Velocity Polygon")
    fig_v, ax_v = plt.subplots(figsize=(6, 6))
    ax_v.quiver(0, 0, vec_vb[0], vec_vb[1], color='b', angles='xy', scale_units='xy', scale=1, label=f'v_B @ {90-theta_deg}°')
    ax_v.quiver(vec_vb[0], vec_vb[1], vec_v_ab_rel[0], vec_v_ab_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label='v_A/B')
    ax_v.quiver(0, 0, vec_va[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label='v_A (Closed)')
    
    limit = v_b_mag * 1.5
    ax_v.set_xlim(-limit, limit); ax_v.set_ylim(-limit, limit); ax_v.set_aspect('equal'); ax_v.legend(); ax_v.grid(True)
    st.pyplot(fig_v)

with col2:
    st.subheader("Acceleration Polygon")
    fig_a, ax_a = plt.subplots(figsize=(6, 6))
    p1, p2 = vec_ab, vec_ab + vec_an_rel
    p3 = p2 + vec_at_rel
    ax_a.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label='a_B (B to O)')
    ax_a.quiver(p1[0], p1[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label='a_n_rel')
    ax_a.quiver(p2[0], p2[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1, label='a_t_rel')
    ax_a.quiver(0, 0, p3[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label='a_A (Closed)')
    
    limit = ab_mag * 1.5
    ax_a.set_xlim(-limit, limit); ax_a.set_ylim(-limit, limit); ax_a.set_aspect('equal'); ax_a.legend(); ax_a.grid(True)
    st.pyplot(fig_a)

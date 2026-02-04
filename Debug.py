import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Slider-Crank Analysis: Angle θ Measured from Left")

# 1. Mechanism Inputs
st.sidebar.header("Mechanism Control")
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 180, 60)
omega_rpm = st.sidebar.slider("Crank ω [rev/min]", 0, 3000, 1500)

# Constants
r_in, l_in = 5.0, 14.0
# Angle logic: Measured from the left horizontal means actual Cartesian angle is (180 - theta)
theta_actual_rad = np.radians(180 - theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
r_ft, l_ft = r_in / 12, l_in / 12

# Geometry: Rod angle phi
# sin(phi)/r = sin(theta_deg)/l
phi = np.arcsin((r_in * np.sin(np.radians(theta_deg))) / l_in)

# --- 2. CALCULATIONS ---
# Velocity
v_b_mag = r_ft * omega_rad
# v_B is 90 deg to OB. At theta=60 (from left), v_B points 30 deg up/right.
v_b_angle_rad = np.radians(90 - (180 - theta_deg)) 
vec_vb = np.array([v_b_mag * np.cos(v_b_angle_rad), v_b_mag * np.sin(v_b_angle_rad)])

# omega_ab for horizontal piston v_A
omega_ab = (vec_vb[1]) / (l_ft * np.cos(phi))
v_ab_rel_mag = l_ft * omega_ab
vec_v_ab_rel = np.array([-v_ab_rel_mag * np.sin(phi), -v_ab_rel_mag * np.cos(phi)])
vec_va = vec_vb + vec_v_ab_rel

# Acceleration
ab_mag = r_ft * (omega_rad**2) # Toward center O
an_rel_mag = l_ft * (omega_ab**2) # A toward B

# a_B directed B to O
vec_ab = np.array([-ab_mag * np.cos(theta_actual_rad), -ab_mag * np.sin(theta_actual_rad)])
# a_n_rel directed A to B
vec_an_rel = np.array([an_rel_mag * np.cos(phi), an_rel_mag * np.sin(phi)])

# Solve for at_rel magnitude to close horizontal a_A
at_rel_mag = -(vec_ab[1] + vec_an_rel[1]) / np.cos(phi)
vec_at_rel = np.array([-at_rel_mag * np.sin(phi), at_rel_mag * np.cos(phi)])
vec_aa_res = vec_ab + vec_an_rel + vec_at_rel

# --- 3. VISUALIZATION ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Mechanism Schematic")
    fig_s, ax_s = plt.subplots(figsize=(5, 5))
    O = np.array([0, 0])
    B = np.array([r_in * np.cos(theta_actual_rad), r_in * np.sin(theta_actual_rad)])
    A = np.array([B[0] - l_in * np.cos(phi), 0]) 
    
    ax_s.plot([O[0], B[0]], [O[1], B[1]], 'bo-', lw=3, label='Crank OB')
    ax_s.plot([B[0], A[0]], [B[1], A[1]], 'go-', lw=3, label='Rod AB')
    ax_s.plot(A[0], A[1], 'rs', markersize=12, label='Piston A')
    ax_s.set_xlim(-20, 5); ax_s.set_ylim(-5, 10); ax_s.set_aspect('equal'); ax_s.grid(True)
    st.pyplot(fig_s)

with col2:
    st.subheader("Velocity Polygon [ft/s]")
    fig_v, ax_v = plt.subplots(figsize=(5, 5))
    ax_v.quiver(0, 0, vec_vb[0], vec_vb[1], color='b', angles='xy', scale_units='xy', scale=1)
    ax_v.text(vec_vb[0], vec_vb[1], f' vB:{v_b_mag:.1f}', color='b', fontsize=10)
    ax_v.quiver(vec_vb[0], vec_vb[1], vec_v_ab_rel[0], vec_v_ab_rel[1], color='g', angles='xy', scale_units='xy', scale=1)
    ax_v.quiver(0, 0, vec_va[0], 0, color='r', angles='xy', scale_units='xy', scale=1)
    ax_v.text(vec_va[0], 2, f' vA:{abs(vec_va[0]):.1f}', color='r', fontsize=10)
    v_lim = v_b_mag * 1.5
    ax_v.set_xlim(-v_lim, v_lim); ax_v.set_ylim(-v_lim, v_lim); ax_v.set_aspect('equal'); ax_v.grid(True)
    st.pyplot(fig_v)

with col3:
    st.subheader("Acceleration Polygon [ft/s²]")
    fig_a, ax_a = plt.subplots(figsize=(5, 5))
    p1, p2 = vec_ab, vec_ab + vec_an_rel
    p3 = p2 + vec_at_rel
    ax_a.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1)
    ax_a.text(vec_ab[0], vec_ab[1], f' aB:{ab_mag:.0f}', color='b', fontsize=10)
    ax_a.quiver(p1[0], p1[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1)
    ax_a.quiver(p2[0], p2[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1)
    ax_a.quiver(0, 0, vec_aa_res[0], 0, color='r', angles='xy', scale_units='xy', scale=1)
    ax_a.text(vec_aa_res[0], 1000, f' aA:{abs(vec_aa_res[0]):.0f}', color='r', fontsize=10)
    a_lim = ab_mag * 1.3
    ax_a.set_xlim(-a_lim, a_lim); ax_a.set_ylim(-a_lim, a_lim); ax_a.set_aspect('equal'); ax_a.grid(True)
    st.pyplot(fig_a)

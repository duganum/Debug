import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Physically Accurate Kinematics: Orthogonal v_A/B")

# 1. Mechanism Inputs
st.sidebar.header("Mechanism Control")
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg] (from Left)", 0, 180, 60)
omega_rpm = st.sidebar.slider("Crank ω [rev/min]", 0, 3000, 1500)

# Constants (Sample Problem 5/15)
r_in, l_in = 5.0, 14.0
r_ft, l_ft = r_in / 12, l_in / 12
omega_rad = (omega_rpm * 2 * np.pi) / 60

# 2. COORDINATE GEOMETRY
# alpha is the Cartesian angle of OB from the right horizon
alpha_rad = np.radians(180 - theta_deg)
# phi (18.02°) is the angle of the rod AB from the right horizon
phi_rad = np.arcsin((r_in * np.sin(np.radians(theta_deg))) / l_in)

# 3. VELOCITY POLYGON
v_b_mag = r_ft * omega_rad
# v_B is 90° to OB: (90 - theta_deg)
v_b_angle = np.radians(90 - theta_deg) 
vec_vb = np.array([v_b_mag * np.cos(v_b_angle), v_b_mag * np.sin(v_b_angle)])

# omega_ab calculated for horizontal piston v_A
# Constraint: v_A_y = 0 -> v_B_y + v_rel_y = 0
# v_A/B is perpendicular to rod: direction is (-sin(-phi), -cos(-phi)) or similar
omega_ab = (vec_vb[1]) / (l_ft * np.cos(phi_rad))
v_ab_rel_mag = l_ft * omega_ab

# CORRECTED: v_A/B is strictly 90 degrees to the rod angle phi
# Rod angle is -phi from the right. Perpendicular is 90-phi.
vec_v_ab_rel = np.array([-v_ab_rel_mag * np.sin(phi_rad), -v_ab_rel_mag * np.cos(phi_rad)])
vec_va = vec_vb + vec_v_ab_rel

# 4. ACCELERATION POLYGON
ab_mag = r_ft * (omega_rad**2) 
an_rel_mag = l_ft * (omega_ab**2) 

# a_B directed B to O (Normal)
vec_ab = np.array([-ab_mag * np.cos(alpha_rad), -ab_mag * np.sin(alpha_rad)])
# a_n_rel directed A to B (along rod)
vec_an_rel = np.array([an_rel_mag * np.cos(phi_rad), an_rel_mag * np.sin(phi_rad)])

# a_t_rel is 90 deg to rod: Direction is (-sin(phi), cos(phi))
at_rel_mag = -(vec_ab[1] + vec_an_rel[1]) / np.cos(phi_rad)
vec_at_rel = np.array([-at_rel_mag * np.sin(phi_rad), at_rel_mag * np.cos(phi_rad)])
vec_aa_res = vec_ab + vec_an_rel + vec_at_rel

# 5. VISUALIZATION
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Mechanism Schematic")
    fig_s, ax_s = plt.subplots(figsize=(5, 5))
    B = np.array([r_in * np.cos(alpha_rad), r_in * np.sin(alpha_rad)])
    A = np.array([B[0] - l_in * np.cos(phi_rad), 0])
    ax_s.plot([0, B[0]], [0, B[1]], 'bo-', lw=3)
    ax_s.plot([B[0], A[0]], [B[1], A[1]], 'go-', lw=3)
    ax_s.plot(A[0], A[1], 'rs', markersize=12)
    ax_s.set_xlim(-20, 5); ax_s.set_ylim(-5, 10); ax_s.set_aspect('equal'); ax_s.grid(True)
    st.pyplot(fig_s)

with col2:
    st.subheader("Velocity Polygon [ft/s]")
    fig_v, ax_v = plt.subplots(figsize=(5, 5))
    ax_v.quiver(0, 0, vec_vb[0], vec_vb[1], color='b', angles='xy', scale_units='xy', scale=1)
    ax_v.text(vec_vb[0], vec_vb[1], f' vB: {v_b_mag:.1f}', color='b', weight='bold')
    # GREEN VECTOR (v_A/B) now 90 degrees to rod
    ax_v.quiver(vec_vb[0], vec_vb[1], vec_v_ab_rel[0], vec_v_ab_rel[1], color='g', angles='xy', scale_units='xy', scale=1)
    ax_v.text(vec_vb[0]+vec_v_ab_rel[0], vec_vb[1]+vec_v_ab_rel[1], f' vA/B: {abs(v_ab_rel_mag):.1f}', color='g', weight='bold')
    ax_v.quiver(0, 0, vec_va[0], 0, color='r', angles='xy', scale_units='xy', scale=1)
    ax_v.text(vec_va[0]/2, 2, f' vA: {abs(vec_va[0]):.1f}', color='r', weight='bold')
    lim = v_b_mag * 1.5
    ax_v.set_xlim(-lim, lim); ax_v

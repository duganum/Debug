import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Complete Slider-Crank Kinematic Analysis")

# 1. Mechanism Inputs
st.sidebar.header("Mechanism Control")
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 360, 60)
omega_rpm = st.sidebar.slider("Crank ω [rev/min]", 0, 3000, 1500)

# Constants (Sample Problem 5/15)
r_in, l_in = 5.0, 14.0
theta = np.radians(theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
r_ft, l_ft = r_in / 12, l_in / 12
phi = np.arcsin((r_in * np.sin(theta)) / l_in) 

# --- 2. CALCULATIONS ---
# Velocity
v_b_mag = r_ft * omega_rad
vec_vb = np.array([v_b_mag * np.cos(np.radians(theta_deg + 90)), v_b_mag * np.sin(np.radians(theta_deg + 90))])
omega_ab = (v_b_mag * np.cos(theta)) / (l_ft * np.cos(phi))
v_ab_rel_mag = l_ft * omega_ab
vec_v_ab_rel = np.array([-v_ab_rel_mag * np.sin(phi), -v_ab_rel_mag * np.cos(phi)])
vec_va = vec_vb + vec_v_ab_rel

# Acceleration
ab_mag = r_ft * (omega_rad**2)
an_rel_mag = l_ft * (omega_ab**2)
vec_ab = np.array([ab_mag * np.cos(theta), -ab_mag * np.sin(theta)])
vec_an_rel = np.array([an_rel_mag * np.cos(phi), an_rel_mag * np.sin(phi)])
at_rel_mag = -(vec_ab[1] + vec_an_rel[1]) / np.cos(phi)
vec_at_rel = np.array([-at_rel_mag * np.sin(phi), at_rel_mag * np.cos(phi)])
vec_aa = vec_ab + vec_an_rel + vec_at_rel

# --- 3. VISUALIZATION (3 Columns) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Mechanism Schematic")
    fig_s, ax_s = plt.subplots(figsize=(5, 5))
    
    # Points for schematic
    O = np.array([0, 0])
    B = np.array([r_in * np.cos(theta), r_in * np.sin(theta)])
    A = np.array([B[0] + l_in * np.cos(phi), 0]) # Piston horizontal at y=0
    
    # Draw Crank, Rod, and Piston
    ax_s.plot([O[0], B[0]], [O[1], B[1]], 'bo-', lw=3, label='Crank OB')
    ax_s.plot([B[0], A[0]], [B[1], A[1]], 'go-', lw=3, label='Rod AB')
    ax_s.plot(A[0], A[1], 'rs', markersize=12, label='Piston A')
    
    # Ground/Center references
    ax_s.axhline(0, color='black', lw=1, linestyle='--')
    ax_s.plot(0, 0, 'ko', markersize=8) # Center O
    
    ax_s.set_xlim(-7, 21); ax_s.set_ylim(-7, 7)
    ax_s.set_aspect('equal'); ax_s.legend(loc='upper right'); ax_s.grid(True)
    st.pyplot(fig_s)

with col2:
    st.subheader("Velocity Polygon [ft/s]")
    fig_v, ax_v = plt.subplots(figsize=(5, 5))
    ax_v.quiver(0, 0, vec_vb[0], vec_vb[1], color='b', angles='xy', scale_units='xy', scale=1, label=f'v_B: {abs(v_b_mag):.1f}')
    ax_v.quiver(vec_vb[0], vec_vb[1], vec_v_ab_rel[0], vec_v_ab_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=f'v_A/B')
    ax_v.quiver(0, 0, vec_va[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label=f'v_A: {abs(vec_va[0]):.1f}')
    lim_v = v_b_mag * 1.5
    ax_v.set_xlim(-lim_v, lim_v); ax_v.set_ylim(-lim_v, lim_v); ax_v.set_aspect('equal'); ax_v.grid(True); ax_v.legend()
    st.pyplot(fig_v)

with col3:
    st.subheader("Acceleration Polygon [ft/s²]")
    fig_a, ax_a = plt.subplots(figsize=(5, 5))
    p1, p2 = vec_ab, vec_ab + vec_an_rel
    p3 = p2 + vec_at_rel
    ax_a.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label=f'a_B: {ab_mag:.0f}')
    ax_a.quiver(p1[0], p1[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=f'an_rel')
    ax_a.quiver(p2[0], p2[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1, label=f'at_rel')
    ax_a.quiver(0, 0, vec_aa[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label=f'a_A: {abs(vec_aa[0]):.0f}')
    lim_a = ab_mag * 1.3
    ax_a.set_xlim(-lim_a, lim_a); ax_a.set_ylim(-lim_a, lim_a); ax_a.set_aspect('equal'); ax_a.grid(True); ax_a.legend()
    st.pyplot(fig_a)

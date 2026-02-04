import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Kinematic Analysis with Live Data Labels")

# 1. Mechanism Inputs
st.sidebar.header("Mechanism Control")
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 360, 60)
omega_rpm = st.sidebar.slider("Crank ω [rev/min]", 0, 3000, 1500)

# 2. Physics & Dynamic Geometry
r_in, l_in = 5.0, 14.0
theta_rad = np.radians(theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
r_ft, l_ft = r_in / 12, l_in / 12
phi = np.arcsin((r_in * np.sin(theta_rad)) / l_in) 

# Velocity Logic
v_b_mag = r_ft * omega_rad
v_b_angle_rad = np.radians(90 - theta_deg) 
vec_vb = np.array([v_b_mag * np.cos(v_b_angle_rad), v_b_mag * np.sin(v_b_angle_rad)])
omega_ab = (vec_vb[1]) / (l_ft * np.cos(phi))
v_ab_rel_mag = l_ft * omega_ab
vec_v_ab_rel = np.array([-v_ab_rel_mag * np.sin(phi), -v_ab_rel_mag * np.cos(phi)])
vec_va = vec_vb + vec_v_ab_rel

# Acceleration Logic
ab_mag = r_ft * (omega_rad**2)
an_rel_mag = l_ft * (omega_ab**2)
vec_ab = np.array([ab_mag * np.cos(theta_rad), -ab_mag * np.sin(theta_rad)])
vec_an_rel = np.array([an_rel_mag * np.cos(phi), an_rel_mag * np.sin(phi)])
at_rel_mag = -(vec_ab[1] + vec_an_rel[1]) / np.cos(phi)
vec_at_rel = np.array([-at_rel_mag * np.sin(phi), at_rel_mag * np.cos(phi)])
vec_aa_res = vec_ab + vec_an_rel + vec_at_rel

# 3. Plotting
col1, col2 = st.columns(2)

with col1:
    st.subheader("Velocity Polygon [ft/s]")
    fig_v, ax_v = plt.subplots(figsize=(6, 6))
    ax_v.quiver(0, 0, vec_vb[0], vec_vb[1], color='b', angles='xy', scale_units='xy', scale=1)
    ax_v.text(vec_vb[0], vec_vb[1], f' v_B: {v_b_mag:.1f}', color='b')
    
    ax_v.quiver(vec_vb[0], vec_vb[1], vec_v_ab_rel[0], vec_v_ab_rel[1], color='g', angles='xy', scale_units='xy', scale=1)
    ax_v.text(vec_vb[0]+vec_v_ab_rel[0], vec_vb[1]+vec_v_ab_rel[1], f' v_A/B: {abs(v_ab_rel_mag):.1f}', color='g')
    
    ax_v.quiver(0, 0, vec_va[0], 0, color='r', angles='xy', scale_units='xy', scale=1)
    ax_v.text(vec_va[0]/2, 10, f' v_A: {abs(vec_va[0]):.1f}', color='r')
    
    limit = v_b_mag * 1.5
    ax_v.set_xlim(-limit, limit); ax_v.set_ylim(-limit, limit); ax_v.set_aspect('equal'); ax_v.grid(True)
    st.pyplot(fig_v)

with col2:
    st.subheader("Acceleration Polygon [ft/s²]")
    fig_a, ax_a = plt.subplots(figsize=(6, 6))
    p1, p2 = vec_ab, vec_ab + vec_an_rel
    p3 = p2 + vec_at_rel
    
    ax_a.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1)
    ax_a.text(vec_ab[0], vec_ab[1], f' a_B: {ab_mag:.0f}', color='b')
    
    ax_a.quiver(p1[0], p1[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1)
    ax_a.text(p2[0], p2[1], f' an_rel: {an_rel_mag:.0f}', color='g')
    
    ax_a.quiver(p2[0], p2[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1)
    ax_a.text(p3[0], p3[1], f' at_rel: {abs(at_rel_mag):.0f}', color='c')
    
    ax_a.quiver(0, 0, p3[0], 0, color='r', angles='xy', scale_units='xy', scale=1)
    ax_a.text(p3[0]/2, 500, f' a_A: {abs(p3[0]):.0f}', color='r')
    
    limit = ab_mag * 1.5
    ax_a.set_xlim(-limit, limit); ax_a.set_ylim(-limit, limit); ax_a.set_aspect('equal'); ax_a.grid(True)
    st.pyplot(fig_a)

# 4. Summary Table Box
st.write("---")
st.subheader("Numerical Results")
data = {
    "Vector": ["Crank Velocity (v_B)", "Piston Velocity (v_A)", "Crank Accel (a_B)", "Piston Accel (a_A)", "Rod Omega (ω_AB)"],
    "Value": [f"{v_b_mag:.2f} ft/s", f"{abs(vec_va[0]):.2f} ft/s", f"{ab_mag:.0f} ft/s²", f"{abs(p3[0]):.0f} ft/s²", f"{omega_ab:.2f} rad/s"]
}
st.table(data)

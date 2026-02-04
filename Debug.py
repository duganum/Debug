import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Final Corrected Velocity & Acceleration Analysis")

# 1. Mechanism Parameters
st.sidebar.header("Mechanism Inputs")
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 360, 60)
omega_rpm = st.sidebar.slider("Crank ω [rev/min]", 0, 3000, 1500)

# Constants
r_ft, l_ft = 5/12, 14/12
theta = np.radians(theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
phi = np.arcsin((5 * np.sin(theta)) / 14) 

# --- VELOCITY POLYGON (Matching your sketch) ---
v_b_mag = r_ft * omega_rad
# v_B is 30 deg up/right (perpendicular to 60 deg crank)
vec_vb = np.array([v_b_mag * np.cos(np.radians(30)), v_b_mag * np.sin(np.radians(30))])

# Calculate omega_ab so v_A is horizontal
omega_ab = (vec_vb[1]) / (l_ft * np.cos(phi))
v_ab_rel_mag = l_ft * omega_ab
vec_v_ab_rel = np.array([-v_ab_rel_mag * np.sin(phi), -v_ab_rel_mag * np.cos(phi)])
vec_va = vec_vb + vec_v_ab_rel

# --- ACCELERATION POLYGON (Closed) ---
ab_mag = r_ft * (omega_rad**2)
an_rel_mag = l_ft * (omega_ab**2)

# a_B points B to O (Down/Right at 60 deg)
vec_ab = np.array([ab_mag * np.cos(theta), -ab_mag * np.sin(theta)])
# a_n_rel points A to B
vec_an_rel = np.array([an_rel_mag * np.cos(phi), an_rel_mag * np.sin(phi)])

# Solve for at_mag to close horizontal a_A
at_rel_mag = -(vec_ab[1] + vec_an_rel[1]) / np.cos(phi)
vec_at_rel = np.array([-at_rel_mag * np.sin(phi), at_rel_mag * np.cos(phi)])
vec_aa_res = vec_ab + vec_an_rel + vec_at_rel

# 3. Plotting
col1, col2 = st.columns(2)

with col1:
    st.subheader("Velocity Polygon")
    fig_v, ax_v = plt.subplots(figsize=(6, 6))
    ax_v.quiver(0, 0, vec_vb[0], vec_vb[1], color='b', angles='xy', scale_units='xy', scale=1, label='v_B (30° Up-Right)')
    ax_v.quiver(vec_vb[0], vec_vb[1], vec_v_ab_rel[0], vec_v_ab_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label='v_A/B')
    ax_v.quiver(0, 0, vec_va[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label='v_A (Horizontal)')
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
    # Red vector MUST close to p3
    ax_a.quiver(0, 0, p3[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label='a_A (Closed)')
    limit = ab_mag * 1.5
    ax_a.set_xlim(-limit, limit); ax_a.set_ylim(-limit, limit); ax_a.set_aspect('equal'); ax_a.legend(); ax_a.grid(True)
    st.pyplot(fig_a)

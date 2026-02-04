import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Physically Accurate Velocity & Acceleration Polygons")

# 1. Mechanism Parameters
st.sidebar.header("Control Parameters")
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 360, 60)
omega_rpm = st.sidebar.slider("Crank ω [rev/min]", 0, 3000, 1500)

# 2. Geometry & Physics Constants
r_in, l_in = 5.0, 14.0
theta = np.radians(theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
r_ft, l_ft = r_in / 12, l_in / 12

# Rod angle phi
phi = np.arcsin((r_in * np.sin(theta)) / l_in) 

# --- VELOCITY CALCULATIONS ---
v_b_mag = r_ft * omega_rad
# v_B is perpendicular to crank OB (Tangent to the circle)
vec_vb = np.array([v_b_mag * np.sin(theta), -v_b_mag * np.cos(theta)])

# Solve for omega_ab by ensuring v_A is horizontal
# v_A = v_B + v_A/B_tangential
# Using vertical component sum = 0: -v_B_y = v_A/B_y
# v_A/B is perpendicular to rod at angle phi: (-sin(phi), cos(phi))
omega_ab = (v_b_mag * np.cos(theta)) / (l_ft * np.cos(phi))
v_ab_rel_mag = l_ft * omega_ab
vec_v_ab_rel = np.array([-v_ab_rel_mag * np.sin(phi), v_ab_rel_mag * np.cos(phi)])

# Resultant Piston Velocity (Horizontal)
vec_va = vec_vb + vec_v_ab_rel

# --- ACCELERATION CALCULATIONS ---
ab_mag = r_ft * (omega_rad**2)
an_rel_mag = l_ft * (omega_ab**2)

# a_B directed from B toward O
vec_ab = np.array([ab_mag * np.cos(theta), -ab_mag * np.sin(theta)])
# (a_A/B)_n directed from A toward B along the rod
vec_an_rel = np.array([an_rel_mag * np.cos(phi), an_rel_mag * np.sin(phi)])

# Solve for at_mag to close horizontal a_A
at_rel_mag = -(vec_ab[1] + vec_an_rel[1]) / np.cos(phi)
vec_at_rel = np.array([-at_rel_mag * np.sin(phi), at_rel_mag * np.cos(phi)])
vec_aa = vec_ab + vec_an_rel + vec_at_rel

# 3. Visualization
col1, col2 = st.columns(2)

with col1:
    st.subheader("Velocity Polygon")
    fig_v, ax_v = plt.subplots(figsize=(6, 6))
    # v_B starts at origin (Tangent to circle)
    ax_v.quiver(0, 0, vec_vb[0], vec_vb[1], color='b', angles='xy', scale_units='xy', scale=1, label=r'Tangent $\vec{v}_B$')
    # v_A/B starts at tip of v_B
    ax_v.quiver(vec_vb[0], vec_vb[1], vec_v_ab_rel[0], vec_v_ab_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=r'$\vec{v}_{A/B} \perp$ rod')
    # v_A Resultant from origin (Horizontal)
    ax_v.quiver(0, 0, vec_va[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label=r'Horizontal $\vec{v}_A$')
    
    v_lim = max(np.abs([v_b_mag, v_ab_rel_mag, vec_va[0]])) * 1.5
    ax_v.set_xlim(-v_lim, v_lim); ax_v.set_ylim(-v_lim, v_lim)
    ax_v.set_aspect('equal'); ax_v.legend(); ax_v.grid(True, linestyle='--')
    st.pyplot(fig_v)

with col2:
    st.subheader("Acceleration Polygon")
    fig_a, ax_a = plt.subplots(figsize=(6, 6))
    p1, p2 = vec_ab, vec_ab + vec_an_rel
    # a_B -> a_n -> a_t
    ax_a.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_B$ (B to O)')
    ax_a.quiver(p1[0], p1[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_n$ (A to B)')
    ax_a.quiver(p2[0], p2[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1, label=r'$(\vec{a}_{A/B})_t \perp$ rod')
    # a_A Resultant from origin (Horizontal)
    ax_a.quiver(0, 0, vec_aa[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label=r'Horizontal $\vec{a}_A$')
    
    a_lim = max(np.abs([ab_mag, at_rel_mag])) * 1.5
    ax_a.set_xlim(-a_lim, a_lim); ax_a.set_ylim(-a_lim, a_lim)
    ax_a.set_aspect('equal'); ax_a.legend(); ax_a.grid(True, linestyle='--')
    st.pyplot(fig_a)

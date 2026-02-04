import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Physically Correct Velocity & Acceleration Analysis")

# 1. Mechanism Parameters
st.sidebar.header("Mechanism Inputs")
theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 360, 60)
omega_rpm = st.sidebar.slider("Crank ω [rev/min]", 0, 3000, 1500)

# Constants from Diagram
r_in, l_in = 5.0, 14.0
theta = np.radians(theta_deg)
omega_rad = (omega_rpm * 2 * np.pi) / 60
r_ft, l_ft = r_in / 12, l_in / 12

# Geometry: Rod angle phi via Law of Sines
phi = np.arcsin((r_in * np.sin(theta)) / l_in) 

# 2. VELOCITY POLYGON (v_B perpendicular to OB)
v_b_mag = r_ft * omega_rad
# Corrected: v_B is 90 degrees to OB (Tangent to circle)
vec_vb = np.array([v_b_mag * np.sin(theta), -v_b_mag * np.cos(theta)])

# Solve for omega_ab (Dependency)
omega_ab = (v_b_mag * np.cos(theta)) / (l_ft * np.cos(phi))
v_ab_rel_mag = l_ft * omega_ab
vec_v_ab_rel = np.array([-v_ab_rel_mag * np.sin(phi), v_ab_rel_mag * np.cos(phi)])

# Resultant Piston Velocity (Must be horizontal)
vec_va = vec_vb + vec_v_ab_rel

# 3. ACCELERATION POLYGON (Full closure)
ab_mag = r_ft * (omega_rad**2)       # Normal acceleration of B toward O
an_rel_mag = l_ft * (omega_ab**2)    # Normal acceleration A relative to B

# Vector Directions
vec_ab = np.array([ab_mag * np.cos(theta), -ab_mag * np.sin(theta)])
vec_an_rel = np.array([an_rel_mag * np.cos(phi), an_rel_mag * np.sin(phi)])

# Solve for at_mag to ensure closure (a_A is purely horizontal)
at_rel_mag = -(vec_ab[1] + vec_an_rel[1]) / np.cos(phi)
vec_at_rel = np.array([-at_rel_mag * np.sin(phi), at_rel_mag * np.cos(phi)])

# Resultant Piston Acceleration (Red vector)
vec_aa_res = vec_ab + vec_an_rel + vec_at_rel

# 4. Visualization
col1, col2 = st.columns(2)

with col1:
    st.subheader("Velocity Polygon")
    fig_v, ax_v = plt.subplots(figsize=(6, 6))
    ax_v.quiver(0, 0, vec_vb[0], vec_vb[1], color='b', angles='xy', scale_units='xy', scale=1, label=r'v_B $\perp$ OB')
    ax_v.quiver(vec_vb[0], vec_vb[1], vec_v_ab_rel[0], vec_v_ab_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=r'v_{A/B} $\perp$ AB')
    ax_v.quiver(0, 0, vec_va[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label=r'v_A (Resultant)')
    
    v_lim = max(np.abs([v_b_mag, v_ab_rel_mag, vec_va[0]])) * 1.5
    ax_v.set_xlim(-v_lim, v_lim); ax_v.set_ylim(-v_lim, v_lim); ax_v.set_aspect('equal'); ax_v.legend(); ax_v.grid(True)
    st.pyplot(fig_v)

with col2:
    st.subheader("Acceleration Polygon")
    fig_a, ax_a = plt.subplots(figsize=(6, 6))
    p1, p2 = vec_ab, vec_ab + vec_an_rel
    p3 = p2 + vec_at_rel # Tip of the final chain
    
    ax_a.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label=r'a_B (B to O)')
    ax_a.quiver(p1[0], p1[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=r'a_{A/B,n}')
    ax_a.quiver(p2[0], p2[1], vec_at_rel[0], vec_at_rel[1], color='c', angles='xy', scale_units='xy', scale=1, label=r'a_{A/B,t}')
    # RED vector now starts at origin and ends EXACTLY at the chain tip p3
    ax_a.quiver(0, 0, p3[0], 0, color='r', angles='xy', scale_units='xy', scale=1, label=r'a_A (Resultant)')
    
    a_lim = max(np.abs([ab_mag, at_rel_mag])) * 1.5
    ax_a.set_xlim(-a_lim, a_lim); ax_a.set_ylim(-a_lim, a_lim); ax_a.set_aspect('equal'); ax_a.legend(); ax_a.grid(True)
    st.pyplot(fig_a)

st.write(f"**Calculated Rod ω_AB:** {omega_ab:.2f} rad/s")

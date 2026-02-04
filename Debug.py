import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def render_slider_crank_acceleration():
    st.title("Rigid Body Kinematics: Slider-Crank Acceleration")
    st.write("Visualizing the relative acceleration equation: $\\vec{a}_A = \\vec{a}_B + (\\vec{a}_{A/B})_n + (\\vec{a}_{A/B})_t$")

    # Sidebar for dynamic user input
    st.sidebar.header("Crank OB Parameters")
    r_ob = st.sidebar.slider("Crank Radius (r) [in]", 1.0, 10.0, 5.0)
    theta_deg = st.sidebar.slider("Crank Angle (θ) [deg]", 0, 360, 60)
    omega_ob = st.sidebar.slider("Angular Velocity (ω) [rev/min]", 0, 3000, 1500)
    
    st.sidebar.header("Connecting Rod AB Parameters")
    l_ab = st.sidebar.slider("Rod Length (L) [in]", 10.0, 20.0, 14.0)
    omega_ab = st.sidebar.slider("Rod Angular Velocity (ω_AB) [rad/s]", 0.0, 50.0, 29.5)

    # Conversions
    theta = np.radians(theta_deg)
    omega_rad = (omega_ob * 2 * np.pi) / 60  # rpm to rad/s
    r_ft = r_ob / 12  # inches to feet for acceleration units
    l_ft = l_ab / 12

    # 1. Acceleration of Crank Pin B (Normal component only if constant ω)
    # a_B = r * ω^2
    a_b_mag = r_ft * (omega_rad**2)
    vec_ab = np.array([-a_b_mag * np.cos(theta), -a_b_mag * np.sin(theta)])

    # 2. Relative Normal Acceleration (A relative to B)
    # (a_A/B)_n = L * ω_AB^2
    a_n_rel_mag = l_ft * (omega_ab**2)
    # In the example, rod angle is approx 18.02 deg
    phi = np.arcsin((r_ob * np.sin(theta)) / l_ab) 
    vec_an_rel = np.array([a_n_rel_mag * np.cos(phi), -a_n_rel_mag * np.sin(phi)])

    # Plotting the Acceleration Polygon
    fig, ax = plt.subplots(figsize=(8, 8))
    origin = np.array([0, 0])

    # Plot Vector a_B (Blue)
    ax.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1000, label=f'a_B: {a_b_mag:.0f} ft/s²')
    
    # Plot Vector (a_A/B)_n (Green) starting from tip of a_B
    ax.quiver(vec_ab[0], vec_ab[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1000, label=f'(a_A/B)_n: {a_n_rel_mag:.0f} ft/s²')

    # Formatting
    ax.set_xlim(-15000, 5000)
    ax.set_ylim(-15000, 5000)
    ax.axhline(0, color='black', lw=1)
    ax.grid(True, linestyle='--')
    ax.set_aspect('equal')
    ax.legend()
    ax.set_title("Acceleration Polygon (Vector Addition)")
    
    st.pyplot(fig)

    # Socratic Insight based on Sample Problem 5/15
    st.info(f"**Textbook Context:** At θ = {theta_deg}°, point B moves in a circle. "
            f"If ω is constant, $a_B$ has only a normal component directed toward O.")

if __name__ == "__main__":
    render_slider_crank_acceleration()

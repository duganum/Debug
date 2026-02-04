streamlit
matplotlib

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def render_relative_acceleration_module():
    st.header("Interactive Module: Relative Acceleration Vector")
    st.write("""
    In Dynamics, we analyze the acceleration of point $B$ relative to a moving reference frame $A$ 
    using the vector addition: $\\vec{a}_B = \\vec{a}_A + \\vec{a}_{B/A}$.
    """)

    # Sidebar for Student Inputs
    st.sidebar.subheader("Vector Parameters")
    
    # Acceleration of Point A (Reference)
    ax_a = st.sidebar.slider("a_A x-component (m/s²)", -10.0, 10.0, 5.0)
    ay_a = st.sidebar.slider("a_A y-component (m/s²)", -10.0, 10.0, 2.0)
    
    # Relative Acceleration B/A
    ax_ba = st.sidebar.slider("a_{B/A} x-component (m/s²)", -10.0, 10.0, -3.0)
    ay_ba = st.sidebar.slider("a_{B/A} y-component (m/s²)", -10.0, 10.0, 6.0)

    # Calculate Resultant a_B
    ax_b = ax_a + ax_ba
    ay_b = ay_a + ay_ba

    # Plotting the Vectors
    fig, ax = plt.subplots(figsize=(8, 8))
    origin = [0, 0]

    # Vector A (Blue)
    ax.quiver(0, 0, ax_a, ay_a, color='b', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_A$')
    
    # Vector B/A (Green) - Starting from the tip of A
    ax.quiver(ax_a, ay_a, ax_ba, ay_ba, color='g', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_{B/A}$')
    
    # Vector B (Red) - The Resultant
    ax.quiver(0, 0, ax_b, ay_b, color='r', angles='xy', scale_units='xy', scale=1, label=r'$\vec{a}_B$')

    # Formatting the Plot
    limit = max(abs(ax_b), abs(ay_b), abs(ax_a), abs(ay_a)) + 2
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.grid(True, linestyle='--')
    ax.set_aspect('equal')
    ax.legend()
    ax.set_title("Vector Addition: Acceleration of B")
    
    st.pyplot(fig)

    # Socratic Checkpoint
    st.subheader("Socratic Insight")
    st.info("If Point A is moving at a constant velocity, what happens to the relationship between $\\vec{a}_B$ and $\\vec{a}_{B/A}$?")
    
    answer = st.text_input("Your reasoning:")
    if answer:
        st.write("Excellent thought. If $\\vec{a}_A = 0$, then $\\vec{a}_B = \\vec{a}_{B/A}$. This confirms that for an inertial reference frame, relative and absolute acceleration are identical.")

if __name__ == "__main__":
    render_relative_acceleration_module()

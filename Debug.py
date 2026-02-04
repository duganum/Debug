import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ... (Previous calculation logic remains the same) ...

# 3. Calculate the Bounding Box for the Vectors
# We collect all endpoints to find the min/max needed for the view
points_x = [0, vec_ab[0], vec_ab[0] + vec_an_rel[0]]
points_y = [0, vec_ab[1], vec_ab[1] + vec_an_rel[1]]

margin = 1.2 # Add 20% padding so labels aren't cut off
min_x, max_x = min(points_x) * margin, max(points_x) * margin
min_y, max_y = min(points_y) * margin, max(points_y) * margin

# Ensure the plot is never "collapsed" if vectors are small
if abs(max_x - min_x) < 100:
    min_x, max_x = -500, 500
if abs(max_y - min_y) < 100:
    min_y, max_y = -500, 500

# 4. Plotting
fig, ax = plt.subplots(figsize=(8, 8))

# Vector a_B (Blue)
ax.quiver(0, 0, vec_ab[0], vec_ab[1], color='b', angles='xy', scale_units='xy', scale=1, label=f'a_B: {a_b_mag:.0f} ft/s²')

# Vector (a_A/B)_n (Green) starting from tip of a_B
ax.quiver(vec_ab[0], vec_ab[1], vec_an_rel[0], vec_an_rel[1], color='g', angles='xy', scale_units='xy', scale=1, label=f'(a_A/B)_n: {a_n_rel_mag:.0f} ft/s²')

# APPLY DYNAMIC SCALE
ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)

ax.axhline(0, color='black', lw=1)
ax.axvline(0, color='black', lw=1)
ax.grid(True, linestyle='--')
ax.set_aspect('equal') # Keep vectors geometrically accurate
ax.legend()
ax.set_title("Acceleration Polygon (Auto-Scaled)")

st.pyplot(fig)

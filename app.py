import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Body na kružnici")

x0 = st.number_input("Souřadnice středu X:", value=0.0)
y0 = st.number_input("Souřadnice středu Y:", value=0.0)
r = st.number_input("Poloměr kružnice:", min_value=0.1, value=1.0)
n = st.number_input("Počet bodů:", min_value=1, step=1, value=8)
color = st.color_picker("Barva bodů:", "#ff0000")
unit = st.text_input("Jednotka (např. m):", "m")

angles = np.linspace(0, 2*np.pi, int(n), endpoint=False)
x_points = x0 + r * np.cos(angles)
y_points = y0 + r * np.sin(angles)

fig, ax = plt.subplots()
ax.plot(x_points, y_points, 'o', color=color)
circle = plt.Circle((x0, y0), r, fill=False, linestyle='--')
ax.add_patch(circle)
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel(f"X [{unit}]")
ax.set_ylabel(f"Y [{unit}]")
ax.grid(True)

st.pyplot(fig)

with st.expander("O aplikaci"):
    st.markdown("""
    **Autor:** Tvé jméno  
    **Email:** tvuj@email.cz  
    **Použité technologie:** Python, Streamlit, Matplotlib  
    """)

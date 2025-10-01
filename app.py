import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import io

st.title("Body na kruznici - Webova aplikace")

# Uzivatelske vstupy
x0 = st.number_input("Souradnice stredu X:", value=0.0)
y0 = st.number_input("Souradnice stredu Y:", value=0.0)
r = st.number_input("Polomer kruznice:", min_value=0.1, value=1.0)
n = st.number_input("Pocet bodu na kruznici:", min_value=1, step=1, value=8)
color = st.color_picker("Barva bodu:", "#ff0000")
unit = st.text_input("Jednotka (napr. m):", "m")

# Vypocet souradnic bodu
angles = np.linspace(0, 2*np.pi, int(n), endpoint=False)
x_points = x0 + r * np.cos(angles)
y_points = y0 + r * np.sin(angles)

# Vykresleni grafu
fig, ax = plt.subplots()
ax.plot(x_points, y_points, 'o', color=color)
circle = plt.Circle((x0, y0), r, fill=False, linestyle='--')
ax.add_patch(circle)
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel(f"X [{unit}]")
ax.set_ylabel(f"Y [{unit}]")
ax.grid(True)
st.pyplot(fig)

# Funkce pro PDF bez diakritiky
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Parametry kruznice", ln=True)
    pdf.cell(0, 10, f"Stred: ({x0}, {y0}) {unit}", ln=True)
    pdf.cell(0, 10, f"Polomer: {r} {unit}", ln=True)
    pdf.cell(0, 10, f"Pocet bodu: {n}", ln=True)
    pdf.cell(0, 10, f"Barva bodu: {color}", ln=True)

    pdf.ln(10)
    pdf.cell(0, 10, "Autor: Tve jmeno", ln=True)
    pdf.cell(0, 10, "Email: tvuj@email.cz", ln=True)
    pdf.cell(0, 10, "Pouzite technologie: Python, Streamlit, Matplotlib, FPDF", ln=True)

    pdf_str = pdf.output(dest='S').encode('latin1')
    return io.BytesIO(pdf_str)

pdf_data = None
if st.button("Vygenerovat PDF"):
    pdf_data = create_pdf()

if pdf_data:
    st.download_button(
        label="Stahnout PDF",
        data=pdf_data,
        file_name="kruznice.pdf",
        mime="application/pdf"
    )

with st.expander("O aplikaci a pouzitych technologiich"):
    st.markdown("""
    **Autor:** Tve jmeno  
    **Email:** tvuj@email.cz  
    **Pouzite technologie:** Python, Streamlit, Matplotlib, FPDF  
    """)


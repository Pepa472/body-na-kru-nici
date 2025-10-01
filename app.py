import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import tempfile
import os

st.title("Body na kružnici - Webová aplikace")

# --- Uživatelské vstupy ---
x0 = st.number_input("Souřadnice středu X:", value=0.0)
y0 = st.number_input("Souřadnice středu Y:", value=0.0)
r = st.number_input("Poloměr kružnice:", min_value=0.1, value=1.0)
n = st.number_input("Počet bodů na kružnici:", min_value=1, step=1, value=8)
color = st.color_picker("Barva bodů:", "#ff0000")
unit = st.text_input("Jednotka (např. m):", "m")

# --- Výpočet souřadnic bodů ---
angles = np.linspace(0, 2*np.pi, int(n), endpoint=False)
x_points = x0 + r * np.cos(angles)
y_points = y0 + r * np.sin(angles)

# --- Vykreslení grafu ---
fig, ax = plt.subplots()
ax.plot(x_points, y_points, 'o', color=color)
circle = plt.Circle((x0, y0), r, fill=False, linestyle='--')
ax.add_patch(circle)
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel(f"X [{unit}]")
ax.set_ylabel(f"Y [{unit}]")
ax.grid(True)

st.pyplot(fig)

# --- Funkce pro vytvoření PDF ---
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Parametry kružnice", ln=True)
    pdf.cell(0, 10, f"Střed: ({x0}, {y0}) {unit}", ln=True)
    pdf.cell(0, 10, f"Poloměr: {r} {unit}", ln=True)
    pdf.cell(0, 10, f"Počet bodů: {n}", ln=True)
    pdf.cell(0, 10, f"Barva bodů: {color}", ln=True)

    # Uložení grafu do dočasného souboru
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig.savefig(tmpfile.name)
        tmpfile_path = tmpfile.name

    pdf.image(tmpfile_path, x=10, y=70, w=pdf.w - 20)
    os.remove(tmpfile_path)

    pdf.set_xy(10, pdf.get_y() + 10)
    pdf.cell(0, 10, "Autor: Tvé jméno", ln=True)
    pdf.cell(0, 10, "Email: tvuj@email.cz", ln=True)
    pdf.cell(0, 10, "Použité technologie: Python, Streamlit, Matplotlib, FPDF", ln=True)

    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)
    return output

# --- Generování a stažení PDF ---
pdf_data = None
if st.button("Vygenerovat PDF"):
    pdf_data = create_pdf()

if pdf_data:
    st.download_button(
        label="Klikni pro stažení PDF",
        data=pdf_data,
        file_name="kruznice.pdf",
        mime="application/pdf"
    )

# --- Informace o aplikaci ---
with st.expander("O aplikaci a použitých technologiích"):
    st.markdown("""
    **Autor:** Tvé jméno  
    **Email:** tvuj@email.cz  
    **Použité technologie:** Python, Streamlit, Matplotlib, FPDF  
    """)



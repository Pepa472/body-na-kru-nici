import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import io

st.title("Body na kružnici")

# Vstupy uživatele
x0 = st.number_input("Souřadnice středu X:", value=0.0)
y0 = st.number_input("Souřadnice středu Y:", value=0.0)
r = st.number_input("Poloměr kružnice:", min_value=0.1, value=1.0)
n = st.number_input("Počet bodů:", min_value=1, step=1, value=8)
color = st.color_picker("Barva bodů:", "#ff0000")
unit = st.text_input("Jednotka (např. m):", "m")

# Výpočet bodů
angles = np.linspace(0, 2*np.pi, int(n), endpoint=False)
x_points = x0 + r * np.cos(angles)
y_points = y0 + r * np.sin(angles)

# Vykreslení grafu
fig, ax = plt.subplots()
ax.plot(x_points, y_points, 'o', color=color)
circle = plt.Circle((x0, y0), r, fill=False, linestyle='--')
ax.add_patch(circle)
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel(f"X [{unit}]")
ax.set_ylabel(f"Y [{unit}]")
ax.grid(True)

st.pyplot(fig)

# Generování PDF
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Parametry kružnice", ln=True)
    pdf.cell(0, 10, f"Střed: ({x0}, {y0}) {unit}", ln=True)
    pdf.cell(0, 10, f"Poloměr: {r} {unit}", ln=True)
    pdf.cell(0, 10, f"Počet bodů: {n}", ln=True)
    pdf.cell(0, 10, f"Barva bodů: {color}", ln=True)

    # Uložíme obrázek grafu do bufferu
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    # Přidáme obrázek do PDF
    pdf.image(buf, x=10, y=70, w=pdf.w - 20)  # trochu odsazení a šířka

    # Autor a kontakt
    pdf.set_xy(10, pdf.get_y() + 10)
    pdf.cell(0, 10, "Autor: Tvé jméno", ln=True)
    pdf.cell(0, 10, "Email: tvuj@email.cz", ln=True)
    pdf.cell(0, 10, "Použité technologie: Python, Streamlit, Matplotlib, FPDF", ln=True)

    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)
    return output

if st.button("Stáhnout PDF"):
    pdf_data = create_pdf()
    st.download_button(
        label="Klikni pro stažení PDF",
        data=pdf_data,
        file_name="kruznice.pdf",
        mime="application/pdf"
    )

with st.expander("O aplikaci"):
    st.markdown("""
    **Autor:** Tvé jméno  
    **Email:** tvuj@email.cz  
    **Použité technologie:** Python, Streamlit, Matplotlib, FPDF  
    """)

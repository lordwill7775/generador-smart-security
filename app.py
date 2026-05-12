import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

st.set_page_config(page_title="Smart Security PDF", page_icon="🛡️")
st.title("🛡️ Generador PDF Smart Security")

# Opciones de documentos
opcion = st.selectbox("Selecciona el documento", [
    "Contrato de Alianza Comercial", 
    "Declaración Jurada de Conocimiento"
])

tipo_persona = st.radio("Tipo de Persona", ["Natural", "Jurídica"], horizontal=True)

with st.form("formulario"):
    st.subheader("Datos del Cliente")
    nombre = st.text_input("Nombres y Apellidos / Razón Social")
    documento = st.text_input("DNI / RUC")
    direccion = st.text_input("Dirección")
    
    if tipo_persona == "Jurídica":
        st.subheader("Datos Legales")
        rep_legal = st.text_input("Representante Legal")
        partida = st.text_input("Partida Registral")
        asiento = st.text_input("Asiento")
    
    enviar = st.form_submit_button("GENERAR PDF")

if enviar:
    try:
        # Configuración del PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        
        # Título
        pdf.cell(200, 10, txt=f"{opcion.upper()}", ln=True, align='C')
        pdf.ln(10)
        
        # Contenido
        pdf.set_font("Arial", size=12)
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        
        texto = f"""
        Por el presente documento, se deja constancia de la información brindada:
        
        TITULAR: {nombre}
        DOCUMENTO: {documento}
        DIRECCIÓN: {direccion}
        FECHA: {fecha_hoy}
        """
        
        if tipo_persona == "Jurídica":
            texto += f"""
        REPRESENTANTE LEGAL: {rep_legal}
        PARTIDA REGISTRAL: {partida}
        ASIENTO: {asiento}
            """
        
        pdf.multi_cell(0, 10, txt=texto)
        
        # Generar archivo en memoria
        pdf_output = pdf.output(dest='S').encode('latin-1')
        
        st.success("✅ PDF generado con éxito")
        st.download_button(
            label="📥 DESCARGAR PDF",
            data=pdf_output,
            file_name=f"{nombre}_documento.pdf",
            mime="application/pdf"
        )
        
    except Exception as e:
        st.error(f"Error: {e}")

import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

st.set_page_config(page_title="Smart Security Docs", page_icon="🛡️")
st.title("🛡️ Sistema Smart Security")

# 1. Menú de opciones que pediste
categoria = st.selectbox("1. Selecciona el Documento:", ["Contrato de Alianza", "Declaración Jurada"])
tipo_persona = st.radio("2. Tipo de Persona:", ["Natural", "Jurídica"], horizontal=True)

with st.form("form_final"):
    st.subheader(f"Datos: {categoria} ({tipo_persona})")
    
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombres y Apellidos / Razón Social")
        documento = st.text_input("DNI / RUC")
    with col2:
        direccion = st.text_input("Dirección")
        ciudad = st.text_input("Ciudad de Firma", value="Lima")
    
    # Campos dinámicos para Jurídica
    rep_legal, dni_rep, partida, asiento = "", "", "", ""
    if tipo_persona == "Jurídica":
        st.divider()
        st.info("Datos del Representante Legal")
        rep_legal = st.text_input("Nombre del Representante")
        dni_rep = st.text_input("DNI del Representante")
        partida = st.text_input("Partida Registral N°")
        asiento = st.text_input("Asiento N°")

    st.divider()
    fecha_sel = st.date_input("Fecha del documento", datetime.now())
    enviar = st.form_submit_button("GENERAR PDF")

if enviar:
    try:
        # Configuración del PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "B", 16)
        
        # Título del documento
        pdf.cell(0, 10, categoria.upper(), ln=True, align="C")
        pdf.ln(10)
        
        # Cuerpo del texto (Resumen de los datos del formato)
        pdf.set_font("helvetica", size=12)
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        fecha_txt = f"{fecha_sel.day} de {meses[fecha_sel.month - 1]} de {fecha_sel.year}"
        
        texto = f"""
        Por el presente documento, se deja constancia de lo siguiente:
        
        TITULAR: {nombre}
        { "RUC" if tipo_persona == "Jurídica" else "DNI" }: {documento}
        DIRECCIÓN: {direccion}
        CIUDAD: {ciudad}
        FECHA: {fecha_txt}
        """
        
        if tipo_persona == "Jurídica":
            texto += f"""
        REPRESENTANTE LEGAL: {rep_legal}
        DNI REP. LEGAL: {dni_rep}
        PARTIDA REGISTRAL: {partida}
        ASIENTO: {asiento}
            """
        
        pdf.multi_cell(0, 10, texto)
        
        # Espacio para firma
        pdf.ln(30)
        pdf.cell(0, 10, "__________________________", ln=True, align="C")
        pdf.cell(0, 10, f"Firma: {nombre}", ln=True, align="C")

        # Generar descarga
        pdf_output = pdf.output()
        
        st.success("✅ ¡PDF generado con éxito!")
        st.download_button(
            label="📥 DESCARGAR PDF",
            data=bytes(pdf_output),
            file_name=f"{nombre}_{categoria}.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")

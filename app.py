import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

st.set_page_config(page_title="Smart Security Docs", page_icon="🛡️")
st.title("🛡️ Generador Smart Security")

# Asegúrate de que estos nombres coincidan EXACTO con tus archivos en GitHub
archivos = {
    "Contrato Persona Natural": "contratonatural.docx",
    "DJ Persona Natural": "Djnatural.docx",
    "DJ Persona Jurídica": "djpersonajuridica.docx"
}

opcion = st.selectbox("¿Qué documento vas a generar?", list(archivos.keys()))

# Variables para manejar la descarga
descarga_lista = False
output = io.BytesIO()
nombre_archivo = ""

with st.form("formulario"):
    st.subheader("Información del Cliente")
    nombre = st.text_input("Nombres y Apellidos / Razón Social")
    documento = st.text_input("DNI / RUC")
    tipo_doc = st.radio("Tipo de Documento", ["DNI", "Pasaporte", "CE"], horizontal=True)
    direccion = st.text_input("Dirección de Residencia")
    
    st.subheader("Configuración de Fecha")
    ciudad = st.text_input("Ciudad", value="Lima")
    fecha_sel = st.date_input("Fecha del documento", datetime.now())
    
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    fecha_formateada = f"{fecha_sel.day} de {meses[fecha_sel.month - 1]} de {fecha_sel.year}"

    enviar = st.form_submit_button("GENERAR DOCUMENTO")

if enviar:
    try:
        doc = DocxTemplate(archivos[opcion])
        contexto = {
            "nombre_persona_natural": nombre,
            "nombre_persona_juridica": nombre,
            "nombres_apellidos": nombre,
            "numero_dni": documento,
            "numero_ruc": documento,
            "numero_documento": documento,
            "dirección": direccion,
            "dirección_declarada": direccion,
            "ciudad": ciudad,
            "fecha_texto": fecha_formateada,
            "dni_x": "X" if tipo_doc == "DNI" else " ",
            "pas_x": "X" if tipo_doc == "Pasaporte" else " ",
            "ce_x": "X" if tipo_doc == "CE" else " "
        }
        doc.render(contexto)
        doc.save(output)
        descarga_lista = True
        nombre_archivo = f"{nombre}_{opcion}.docx"
    except Exception as e:
        st.error(f"Error al procesar: {e}")

if descarga_lista:
    st.success(f"✅ Documento para {nombre} generado")
    st.download_button(
        label="📥 DESCARGAR AQUÍ",
        data=output.getvalue(),
        file_name=nombre_archivo,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

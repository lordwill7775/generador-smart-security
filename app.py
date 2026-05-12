import streamlit as st
from docxtpl import DocxTemplate
from spire.doc import Document, FileFormat
import io
import os
from datetime import datetime

st.set_page_config(page_title="Smart Security PDF", page_icon="🛡️")
st.title("🛡️ Sistema de Documentos Smart Security")

# 1. Selección de Categoría
categoria = st.selectbox("¿Qué deseas generar?", ["Contrato de Alianza", "Declaración Jurada"])

# 2. Selección de Tipo de Persona
tipo_persona = st.radio("Tipo de Persona:", ["Natural", "Jurídica"], horizontal=True)

# Lógica para seleccionar el archivo Word correcto
if categoria == "Contrato de Alianza":
    archivo_word = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
else:
    archivo_word = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"

with st.form("formulario_dinamico"):
    st.subheader(f"Datos para: {categoria} ({tipo_persona})")
    
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombres y Apellidos / Razón Social")
        documento = st.text_input("DNI / RUC del Titular")
    with col2:
        direccion = st.text_input("Dirección")
        correo = st.text_input("Correo Electrónico")
    
    telefono = st.text_input("Teléfono/Celular")
    
    # Campos que solo aparecen si es Jurídica
    rep_legal, dni_rep, partida, asiento = "", "", "", ""
    if tipo_persona == "Jurídica":
        st.divider()
        st.subheader("Información del Representante Legal")
        rep_legal = st.text_input("Nombre Completo del Representante")
        dni_rep = st.text_input("DNI del Representante")
        partida = st.text_input("Partida Registral N°")
        asiento = st.text_input("Asiento N°")

    st.divider()
    ciudad = st.text_input("Ciudad de Firma", value="Lima")
    fecha_sel = st.date_input("Fecha del documento", datetime.now())
    
    enviar = st.form_submit_button("GENERAR PDF FINAL")

if enviar:
    try:
        # Formatear fecha en español
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        fecha_texto = f"{fecha_sel.day} de {meses[fecha_sel.month - 1]} de {fecha_sel.year}"

        # Cargar plantilla y rellenar
        doc_tpl = DocxTemplate(archivo_word)
        contexto = {
            "nombre_persona_natural": nombre,
            "nombre_persona_juridica": nombre,
            "nombres_apellidos": nombre,
            "numero_dni": dni_rep if tipo_persona == "Jurídica" else documento,
            "numero_ruc": documento,
            "numero_documento": documento,
            "direccion": direccion,
            "dirección": direccion,
            "dirección_declarada": direccion,
            "correo_electronico": correo,
            "numero_telefono": telefono,
            "nombre_representante_legal": rep_legal,
            "numero_asiento": asiento,
            "numero_partida_registral": partida,
            "ciudad": ciudad,
            "fecha_texto": fecha_texto,
            "dni_x": "X", "pas_x": " ", "ce_x": " "
        }
        
        doc_tpl.render(contexto)
        
        # Procesamiento de archivos
        temp_word = "temp_output.docx"
        temp_pdf = "final_output.pdf"
        doc_tpl.save(temp_word)
        
        # Conversión a PDF con Spire.Doc para mantener el formato original
        pdf_doc = Document()
        pdf_doc.LoadFromFile(temp_word)
        pdf_doc.SaveToFile(temp_pdf, FileFormat.PDF)
        pdf_doc.Close()
        
        with open(temp_pdf, "rb") as f:
            st.success(f"✅ {categoria} generado con éxito")
            st.download_button(
                label="📥 DESCARGAR PDF",
                data=f.read(),
                file_name=f"{nombre}_{categoria}.pdf",
                mime="application/pdf"
            )
        
        # Limpieza
        if os.path.exists(temp_word): os.remove(temp_word)
        if os.path.exists(temp_pdf): os.remove(temp_pdf)

    except Exception as e:
        st.error(f"Error: {e}. Asegúrate de que los archivos Word estén en tu GitHub.")

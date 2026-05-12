import streamlit as st
from docxtpl import DocxTemplate
import aspose.words as aw
import io
import os
from datetime import datetime

st.set_page_config(page_title="Smart Security PDF", page_icon="🛡️")
st.title("🛡️ Generador de Contratos PDF")

# Diccionario con tus formatos originales
archivos = {
    "Contrato Persona Natural": "contratonatural.docx",
    "DJ Persona Natural": "Djnatural.docx",
    "Contrato Persona Jurídica": "contratojuridica.docx",
    "DJ Persona Jurídica": "djpersonajuridica.docx"
}

opcion = st.selectbox("Selecciona el formato de Word a usar:", list(archivos.keys()))

with st.form("formulario"):
    st.subheader("Datos para el documento")
    nombre = st.text_input("Nombres y Apellidos / Razón Social")
    documento = st.text_input("DNI / RUC")
    direccion = st.text_input("Dirección")
    
    rep_legal, dni_rep, partida, asiento = "", "", "", ""
    if "Jurídica" in opcion:
        st.subheader("Datos de Empresa")
        rep_legal = st.text_input("Representante Legal")
        dni_rep = st.text_input("DNI del Representante")
        partida = st.text_input("Partida Registral")
        asiento = st.text_input("Asiento")

    enviar = st.form_submit_button("GENERAR PDF FINAL")

if enviar:
    try:
        # 1. Cargar tu Word original y rellenar datos
        doc_tpl = DocxTemplate(archivos[opcion])
        
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        hoy = datetime.now()
        fecha_formateada = f"{hoy.day} de {meses[hoy.month - 1]} de {hoy.year}"

        contexto = {
            "nombre_persona_natural": nombre,
            "nombre_persona_juridica": nombre,
            "nombres_apellidos": nombre,
            "numero_dni": dni_rep if "Jurídica" in opcion else documento,
            "numero_ruc": documento,
            "numero_documento": documento,
            "direccion": direccion,
            "dirección": direccion,
            "nombre_representante_legal": rep_legal,
            "numero_asiento": asiento,
            "numero_partida_registral": partida,
            "fecha_texto": fecha_formateada,
            "dni_x": "X", "pas_x": " ", "ce_x": " "
        }
        
        doc_tpl.render(contexto)
        
        # 2. Guardar temporalmente para convertir
        temp_word = "temp_render.docx"
        temp_pdf = "resultado.pdf"
        doc_tpl.save(temp_word)
        
        # 3. Convertir Word a PDF manteniendo el formato
        doc_aw = aw.Document(temp_word)
        doc_aw.save(temp_pdf)
        
        with open(temp_pdf, "rb") as f:
            pdf_bytes = f.read()

        st.success("✅ ¡PDF generado usando tu formato Word!")
        st.download_button(
            label="📥 DESCARGAR PDF",
            data=pdf_bytes,
            file_name=f"{nombre}_{opcion}.pdf",
            mime="application/pdf"
        )
        
        # Limpieza
        if os.path.exists(temp_word): os.remove(temp_word)
        if os.path.exists(temp_pdf): os.remove(temp_pdf)

    except Exception as e:
        st.error(f"Error: {e}. Asegúrate de que el archivo '{archivos[opcion]}' esté en tu GitHub.")

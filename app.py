import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime
from docx2pdf import convert
import pythoncom # Necesario para evitar errores de hilos en Windows/Servidores

st.set_page_config(page_title="Smart Security PDF", page_icon="🛡️")
st.title("🛡️ Generador de PDF Smart Security")

archivos = {
    "Contrato Persona Natural": "contratonatural.docx",
    "DJ Persona Natural": "Djnatural.docx",
    "Contrato Persona Jurídica": "contratojuridica.docx",
    "DJ Persona Jurídica": "djpersonajuridica.docx"
}

opcion = st.selectbox("¿Qué documento vas a convertir a PDF?", list(archivos.keys()))

with st.form("formulario"):
    nombre = st.text_input("Nombres y Apellidos / Razón Social")
    documento = st.text_input("DNI / RUC")
    direccion = st.text_input("Dirección")
    
    # Campos adicionales para Jurídica
    rep_legal, partida, asiento = "", "", ""
    if "Jurídica" in opcion:
        rep_legal = st.text_input("Representante Legal")
        partida = st.text_input("Partida Registral")
        asiento = st.text_input("Asiento")

    enviar = st.form_submit_button("GENERAR PDF")

if enviar:
    try:
        # 1. Crear el Word temporalmente en memoria
        doc = DocxTemplate(archivos[opcion])
        contexto = {
            "nombre_persona_natural": nombre,
            "nombre_persona_juridica": nombre,
            "nombres_apellidos": nombre,
            "numero_dni": documento,
            "numero_ruc": documento,
            "direccion": direccion,
            "nombre_representante_legal": rep_legal,
            "numero_partida_registral": partida,
            "numero_asiento": asiento,
            "fecha_texto": datetime.now().strftime("%d de %B de %Y")
        }
        doc.render(contexto)
        
        # Guardar Word temporal
        temp_word = "temp.docx"
        temp_pdf = "temp.pdf"
        doc.save(temp_word)
        
        # 2. Convertir Word a PDF
        # Nota: En Streamlit Cloud esto requiere una configuración de entorno específica. 
        # Si usas Linux en el servidor, se usa 'libreoffice'.
        st.info("Convirtiendo a PDF... por favor espera.")
        os.system(f"lowriter --headless --convert-to pdf {temp_word}")
        
        # 3. Leer el PDF generado para la descarga
        with open(temp_pdf, "rb") as f:
            pdf_data = f.read()

        st.success("✅ PDF generado correctamente")
        st.download_button(
            label="📥 DESCARGAR PDF",
            data=pdf_data,
            file_name=f"{nombre}_{opcion}.pdf",
            mime="application/pdf"
        )
        
    except Exception as e:
        st.error(f"Error al crear el PDF: {e}")

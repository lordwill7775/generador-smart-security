import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

# Configuración visual de la página
st.set_page_config(page_title="Smart Security Docs", page_icon="🛡️")
st.title("🛡️ Generador Smart Security")

# Nombres exactos de tus archivos cargados en GitHub
archivos = {
    "Contrato Persona Jurídica": "contratojuridica.docx.dotx",
    "Contrato Persona Natural": "contratonatural.docx.docx",
    "DJ Persona Natural": "Djnatural.docx.docx",
    "DJ Persona Jurídica": "djpersonajuridica.docx.docx"
}

# Menú para que el equipo elija el documento
opcion = st.selectbox("¿Qué documento vas a generar?", list(archivos.keys()))

with st.form("formulario_principal"):
    st.subheader("Información del Cliente")
    nombre = st.text_input("Nombres y Apellidos / Razón Social")
    documento = st.text_input("DNI / RUC")
    tipo_doc = st.radio("Tipo de Documento", ["DNI", "Pasaporte", "CE"], horizontal=True)
    direccion = st.text_input("Dirección de Residencia")
    
    st.subheader("Configuración de Fecha")
    fecha_sel = st.date_input("Fecha del documento", datetime.now())
    
    # Formateo automático de fecha en español
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    fecha_formateada = f"{fecha_sel.day} de {meses[fecha_sel.month - 1]} de {fecha_sel.year}"

    # Botón para procesar
    if st.form_submit_button("GENERAR DOCUMENTO"):
        if not nombre or not documento:
            st.error("Por favor, completa el nombre y el número de documento.")
        else:
            try:
                # Cargar la plantilla elegida
                doc = DocxTemplate(archivos[opcion])
                
                # Mapa de etiquetas (une el formulario con tu Word)
                contexto = {
                    "nombre_persona_natural": nombre,
                    "nombre_persona_juridica": nombre,
                    "nombres_apellidos": nombre,
                    "numero_dni": documento,
                    "numero_ruc": documento,
                    "numero_documento": documento,
                    "dirección": direccion,
                    "dirección_declarada": direccion,
                    "fecha_texto": fecha_formateada,
                    "dni_x": "X" if tipo_doc == "DNI" else " ",
                    "pas_x": "X" if tipo_doc == "Pasaporte" else " ",
                    "ce_x": "X" if tipo_doc == "CE" else " "
                }
                
                doc.render(contexto)
                
                # Crear el archivo para descargar
                output = io.BytesIO()
                doc.save(output)
                
                st.success(f"✅ ¡{opcion} generado con éxito!")
                st.download_button(
                    label="📥 Descargar Documento Relleno",
                    data=output.getvalue(),
                    file_name=f"{nombre}_{opcion}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(f"Hubo un error al leer el archivo: {e}. Asegúrate de que el nombre del archivo en GitHub sea correcto.")

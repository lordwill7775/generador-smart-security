import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

st.set_page_config(page_title="Smart Security Docs", page_icon="🛡️")
st.title("🛡️ Sistema Smart Security")

# 1. Menú de selección doble
categoria = st.selectbox("1. Selecciona el Documento:", ["Contrato de Alianza", "Declaración Jurada"])
tipo_persona = st.radio("2. Tipo de Persona:", ["Natural", "Jurídica"], horizontal=True)

# Mapeo de archivos según tus formatos en GitHub
if categoria == "Contrato de Alianza":
    archivo_word = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
else:
    archivo_word = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"

with st.form("form_smart_security"):
    st.subheader(f"Datos para: {categoria}")
    
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombres y Apellidos / Razón Social")
        documento = st.text_input("DNI / RUC del Titular")
        correo = st.text_input("Correo Electrónico")
    with col2:
        direccion = st.text_input("Dirección Completa")
        telefono = st.text_input("Número de Teléfono/Celular")
        ciudad = st.text_input("Ciudad de Firma", value="Lima")
    
    # Campos para Persona Jurídica
    rep_legal, dni_rep, partida, asiento = "", "", "", ""
    if tipo_persona == "Jurídica":
        st.divider()
        st.info("Información del Representante Legal")
        rep_legal = st.text_input("Nombre del Representante")
        dni_rep = st.text_input("DNI del Representante")
        partida = st.text_input("Partida Registral N°")
        asiento = st.text_input("Asiento N°")

    st.divider()
    fecha_sel = st.date_input("Fecha del documento", datetime.now())
    enviar = st.form_submit_button("GENERAR DOCUMENTO")

if enviar:
    try:
        # Rellenar tu Word original
        doc = DocxTemplate(archivo_word)
        
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        fecha_texto = f"{fecha_sel.day} de {meses[fecha_sel.month - 1]} de {fecha_sel.year}"

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
            "numero_celular": telefono,
            "nombre_representante_legal": rep_legal,
            "numero_asiento": asiento,
            "numero_partida_registral": partida,
            "ciudad": ciudad,
            "fecha_texto": fecha_texto,
            "dni_x": "X", "pas_x": " ", "ce_x": " "
        }
        
        doc.render(contexto)
        
        # Guardar en memoria para descarga
        output = io.BytesIO()
        doc.save(output)
        
        st.success(f"✅ ¡{categoria} generado exitosamente!")
        st.download_button(
            label="📥 DESCARGAR EN FORMATO WORD",
            data=output.getvalue(),
            file_name=f"{nombre}_{categoria}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        st.error(f"Error: {e}. Asegúrate de que el archivo '{archivo_word}' esté en tu GitHub.")

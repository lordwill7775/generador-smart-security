import streamlit as st
from docxtpl import DocxTemplate
import aspose.words as aw
import io
import os
from datetime import datetime

st.set_page_config(page_title="Smart Security Docs", page_icon="🛡️")
st.title("🛡️ Sistema Smart Security")

# 1. Selección de Documento
categoria = st.selectbox("1. Selecciona el Documento:", ["Contrato de Alianza", "Declaración Jurada"])

# 2. Selección de Persona
tipo_persona = st.radio("2. Tipo de Persona:", ["Natural", "Jurídica"], horizontal=True)

# Mapeo de archivos según tu GitHub
if categoria == "Contrato de Alianza":
    archivo_word = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
else:
    archivo_word = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"

with st.form("form_smart"):
    st.subheader(f"Datos: {categoria}")
    
    nombre = st.text_input("Nombres y Apellidos / Razón Social")
    documento = st.text_input("DNI / RUC")
    direccion = st.text_input("Dirección")
    
    # Campos dinámicos para Jurídica
    rep_legal, dni_rep, partida, asiento = "", "", "", ""
    if tipo_persona == "Jurídica":
        st.divider()
        rep_legal = st.text_input("Representante Legal")
        dni_rep = st.text_input("DNI del Representante")
        partida = st.text_input("Partida Registral")
        asiento = st.text_input("Asiento")

    st.divider()
    fecha_sel = st.date_input("Fecha", datetime.now())
    enviar = st.form_submit_button("GENERAR PDF")

if enviar:
    try:
        # Rellenar Word
        doc_tpl = DocxTemplate(archivo_word)
        
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
            "nombre_representante_legal": rep_legal,
            "numero_asiento": asiento,
            "numero_partida_registral": partida,
            "fecha_texto": fecha_texto,
            "dni_x": "X", "pas_x": " ", "ce_x": " "
        }
        
        doc_tpl.render(contexto)
        
        # Guardar y Convertir
        temp_w = "temp.docx"
        temp_p = "final.pdf"
        doc_tpl.save(temp_w)
        
        # Conversión Aspose (más robusta en Linux)
        aw_doc = aw.Document(temp_w)
        aw_doc.save(temp_p)
        
        with open(temp_p, "rb") as f:
            st.success("✅ Documento listo")
            st.download_button(
                label="📥 DESCARGAR PDF",
                data=f.read(),
                file_name=f"{nombre}_{categoria}.pdf",
                mime="application/pdf"
            )
            
        # Limpieza silenciosa
        os.remove(temp_w)
        os.remove(temp_p)

    except Exception as e:
        st.error(f"Error: {e}. Verifica que el archivo '{archivo_word}' esté en GitHub.")

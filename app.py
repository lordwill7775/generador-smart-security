import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

st.set_page_config(page_title="Smart Security Docs", page_icon="🛡️")
st.title("🛡️ Generador Smart Security")

# Nombres de archivos basados en tu GitHub
archivos = {
    "Contrato Persona Natural": "contratonatural.docx",
    "DJ Persona Natural": "Djnatural.docx",
    "Contrato Persona Jurídica": "contratojuridica.docx"
}

opcion = st.selectbox("¿Qué documento vas a generar?", list(archivos.keys()))

descarga_lista = False
output = io.BytesIO()
nombre_archivo = ""

with st.form("formulario"):
    st.subheader("Información General")
    nombre = st.text_input("Nombres y Apellidos / Razón Social")
    documento = st.text_input("DNI / RUC")
    direccion = st.text_input("Dirección")
    correo = st.text_input("Correo Electrónico")
    telefono = st.text_input("Teléfono / Celular")
    
    if "Jurídica" in opcion:
        st.subheader("Datos del Representante")
        rep_legal = st.text_input("Nombre del Representante Legal")
        dni_rep = st.text_input("DNI del Representante")
        partida = st.text_input("Partida Registral N°")
        asiento = st.text_input("Asiento N°")
    
    st.subheader("Configuración de Fecha y Lugar")
    ciudad = st.text_input("Ciudad", value="Lima")
    tipo_doc = st.radio("Tipo de Documento", ["DNI", "Pasaporte", "CE"], horizontal=True)
    fecha_sel = st.date_input("Fecha del documento", datetime.now())
    
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    fecha_formateada = f"{fecha_sel.day} de {meses[fecha_sel.month - 1]} de {fecha_sel.year}"

    enviar = st.form_submit_button("GENERAR DOCUMENTO")

if enviar:
    try:
        doc = DocxTemplate(archivos[opcion])
        
        # Unimos todos los datos para que funcionen en cualquier plantilla
        contexto = {
            "nombre_persona_natural": nombre,
            "nombre_persona_juridica": nombre,
            "nombres_apellidos": nombre,
            "numero_dni": documento if "Jurídica" not in opcion else dni_rep,
            "numero_ruc": documento,
            "numero_documento": documento,
            "direccion": direccion,
            "dirección": direccion,
            "dirección_declarada": direccion,
            "correo_electronico": correo,
            "numero_telefono": telefono,
            "numero_celular": telefono,
            "ciudad": ciudad,
            "fecha_texto": fecha_formateada,
            "nombre_representante_legal": rep_legal if "Jurídica" in opcion else "",
            "numero_asiento": asiento if "Jurídica" in opcion else "",
            "numero_partida_registral": partida if "Jurídica" in opcion else "",
            "dni_x": "X" if tipo_doc == "DNI" else " ",
            "pas_x": "X" if tipo_doc == "Pasaporte" else " ",
            "ce_x": "X" if tipo_doc == "CE" else " "
        }
        
        doc.render(contexto)
        doc.save(output)
        descarga_lista = True
        nombre_archivo = f"{nombre}_{opcion}.docx"
    except Exception as e:
        st.error(f"Hubo un error al leer el archivo: {e}. Asegúrate de que el nombre del archivo en GitHub sea correcto.")

if descarga_lista:
    st.success(f"¡{opcion} generado con éxito!")
    st.download_button(
        label="📥 DESCARGAR DOCUMENTO",
        data=output.getvalue(),
        file_name=nombre_archivo,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

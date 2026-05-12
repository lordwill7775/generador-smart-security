import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

st.set_page_config(page_title="Smart Security Docs", page_icon="🛡️")
st.title("🛡️ Generador Smart Security")

# Mapeo de archivos (asegúrate de que los nombres en GitHub sean estos)
archivos = {
    "Contrato Persona Natural": "contratonatural.docx",
    "DJ Persona Natural": "Djnatural.docx",
    "Contrato Persona Jurídica": "contratojuridica.docx",
    "DJ Persona Jurídica": "djpersonajuridica.docx"
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
    telefono = st.text_input("Teléfono")
    
    # Variables de control para datos de empresa
    rep_legal, dni_rep, partida, asiento = "", "", "", ""
    
    # Solo muestra estos campos si eliges una opción Jurídica
    if "Jurídica" in opcion:
        st.subheader("Datos de la Empresa / Representante")
        rep_legal = st.text_input("Nombre del Representante Legal")
        dni_rep = st.text_input("DNI del Representante")
        partida = st.text_input("Número de Partida Registral")
        asiento = st.text_input("Número de Asiento")
    
    st.subheader("Configuración de Firma")
    ciudad = st.text_input("Ciudad de firma", value="Lima")
    tipo_doc = st.radio("Documento del titular", ["DNI", "Pasaporte", "CE"], horizontal=True)
    fecha_sel = st.date_input("Fecha del documento", datetime.now())
    
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    fecha_formateada = f"{fecha_sel.day} de {meses[fecha_sel.month - 1]} de {fecha_sel.year}"

    enviar = st.form_submit_button("GENERAR DOCUMENTO")

if enviar:
    try:
        doc = DocxTemplate(archivos[opcion])
        
        # Este diccionario tiene todas las etiquetas que tus Word necesitan
        contexto = {
            "nombre_persona_natural": nombre,
            "nombre_persona_juridica": nombre,
            "nombres_apellidos": nombre,
            "numero_dni": dni_rep if "Jurídica" in opcion else documento,
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
            "nombre_representante_legal": rep_legal,
            "numero_asiento": asiento,
            "numero_partida_registral": partida,
            "dni_x": "X" if tipo_doc == "DNI" else " ",
            "pas_x": "X" if tipo_doc == "Pasaporte" else " ",
            "ce_x": "X" if tipo_doc == "CE" else " "
        }
        
        doc.render(contexto)
        doc.save(output)
        descarga_lista = True
        nombre_archivo = f"{nombre}_{opcion}.docx"
        
    except Exception as e:
        st.error(f"Error al procesar el Word: {e}. Revisa que todas las llaves esten bien cerradas en tu archivo.")

if descarga_lista:
    st.success(f"✅ ¡{opcion} generado correctamente!")
    st.download_button(
        label="📥 DESCARGAR ARCHIVO",
        data=output.getvalue(),
        file_name=nombre_archivo,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

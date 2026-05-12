import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Aló Credit - Generador", page_icon="💳", layout="centered")

# Colores de Aló Credit extraídos del logo
color_azul_oscuro = "#001B3D" 
color_cian = "#00E5FF"        
color_fondo = "#F0F2F6"       

st.markdown(f"""
    <style>
    .stApp {{ background-color: {color_fondo}; }}
    h1, h2, h3 {{ color: {color_azul_oscuro}; }}
    .stButton>button {{
        background-color: {color_azul_oscuro};
        color: white;
        border-radius: 8px;
        border: 2px solid {color_cian};
        font-weight: bold;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: {color_cian};
        color: {color_azul_oscuro};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
col_logo, col_titulo = st.columns([1, 3])
with col_logo:
    # Aquí es donde el código busca el archivo que subiste en el Paso 2
    if os.path.exists("hunter.png"):
        st.image("hunter.png", width=150)
with col_titulo:
    st.title("Generador de Documentos")
    st.write("**Aló Credit Perú S.A.C.**")

st.divider()

# --- SELECCIÓN DE DOCUMENTO ---
categoria = st.selectbox("1. Selecciona el Documento:", ["Contrato de Alianza Comercial", "Declaración Jurada"])
tipo_persona = st.radio("2. Tipo de Persona:", ["Natural", "Jurídica"], horizontal=True)

# El sistema elige el Word automáticamente
if categoria == "Contrato de Alianza Comercial":
    archivo_word = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
else:
    archivo_word = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"

with st.form("form_alo"):
    st.subheader("Datos del Cliente")
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombres / Razón Social")
        documento = st.text_input("DNI / RUC")
        correo = st.text_input("Correo Electrónico")
    with col2:
        direccion = st.text_input("Dirección")
        telefono = st.text_input("Teléfono/Celular")
        ciudad = st.text_input("Ciudad/Oficina", value="Lima")
    
    rep_legal, dni_rep, partida, asiento = "", "", "", ""
    if tipo_persona == "Jurídica":
        st.divider()
        st.info("Datos del Representante Legal")
        c1, c2 = st.columns(2)
        with c1:
            rep_legal = st.text_input("Representante Legal")
            dni_rep = st.text_input("DNI Representante")
        with c2:
            partida = st.text_input("Partida Registral")
            asiento = st.text_input("Asiento")

    enviar = st.form_submit_button("🚀 GENERAR DOCUMENTO")

if enviar:
    try:
        doc = DocxTemplate(archivo_word)
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        hoy = datetime.now()
        fecha_texto = f"{hoy.day} de {meses[hoy.month - 1]} de {hoy.year}"

        contexto = {
            "nombre_persona_natural": nombre, "nombre_persona_juridica": nombre,
            "nombres_apellidos": nombre, "numero_dni": dni_rep if tipo_persona == "Jurídica" else documento,
            "numero_ruc": documento, "numero_documento": documento,
            "direccion": direccion, "dirección": direccion, "dirección_declarada": direccion,
            "correo_electronico": correo, "numero_telefono": telefono, "numero_celular": telefono,
            "nombre_representante_legal": rep_legal, "numero_asiento": asiento,
            "numero_partida_registral": partida, "ciudad": ciudad, "fecha_texto": fecha_texto,
            "dni_x": "X", "pas_x": " ", "ce_x": " "
        }
        
        doc.render(contexto)
        output = io.BytesIO()
        doc.save(output)
        
        st.balloons()
        st.success("✅ Documento generado")
        st.download_button(
            label="📥 DESCARGAR EN WORD",
            data=output.getvalue(),
            file_name=f"ALO_CREDIT_{nombre}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Asegúrate de que '{archivo_word}' esté subido en GitHub.")

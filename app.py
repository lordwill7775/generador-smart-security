import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Aló Credit | Portal de Documentos", page_icon="💳", layout="wide")

# --- COLORES CORPORATIVOS ---
naranja_alo = "#FF7F00"
azul_alo = "#001B3D"
cian_alo = "#00E5FF"

# --- DISEÑO UI (GLASSMORPHISM) ---
st.markdown(f"""
    <style>
    /* Fondo con degradado fluido naranja y azul */
    .stApp {{
        background: linear-gradient(135deg, {azul_alo} 0%, #003a85 50%, {naranja_alo} 100%);
        background-attachment: fixed;
    }}
    
    /* Tarjeta del Formulario (Efecto Cristal) */
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 25px !important;
        padding: 50px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5) !important;
    }}

    /* Títulos y Etiquetas en Blanco para contraste */
    h1, h2, h3, p, label, .stMarkdown {{
        color: #FFFFFF !important;
        font-family: 'Poppins', sans-serif;
    }}

    /* Inputs elegantes */
    .stTextInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: {azul_alo} !important;
        border-radius: 10px !important;
        border: none !important;
    }}

    /* Botón Naranja Corporativo */
    .stButton>button {{
        background-color: {naranja_alo} !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        font-size: 20px !important;
        padding: 15px 30px !important;
        width: 100%;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(255, 127, 0, 0.3);
    }}
    
    .stButton>button:hover {{
        background-color: {cian_alo} !important;
        color: {azul_alo} !important;
        transform: scale(1.02);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA CON LOGOTIPO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("hunter.png"):
        st.image("hunter.png", use_container_width=True)
    else:
        st.markdown(f"<h1 style='text-align:center;'>ALÓ CREDIT</h1>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- SELECTORES ---
c_a, c_b = st.columns(2)
with c_a:
    categoria = st.selectbox("📂 Documento a generar:", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c_b:
    tipo_persona = st.radio("👤 Tipo de Persona:", ["Natural", "Jurídica"], horizontal=True)

# Mapeo de archivos
if categoria == "Contrato de Alianza Comercial":
    archivo_word = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
else:
    archivo_word = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"

# --- FORMULARIO DE DATOS ---
with st.form("form_datos"):
    st.markdown("<h2 style='text-align:center;'>Registro de Información</h2>", unsafe_allow_html=True)
    
    col_izq, col_der = st.columns(2)
    with col_izq:
        nombre = st.text_input("Nombres y Apellidos / Razón Social")
        documento = st.text_input("DNI / RUC")
        correo = st.text_input("Correo Electrónico")
    with col_der:
        direccion = st.text_input("Dirección")
        telefono = st.text_input("Teléfono")
        ciudad = st.text_input("Ciudad", value="Lima")
    
    if tipo_persona == "Jurídica":
        st.markdown("<hr style='opacity:0.2;'>", unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            rep_legal = st.text_input("Representante Legal")
            dni_rep = st.text_input("DNI Representante")
        with cy:
            partida = st.text_input("Partida N°")
            asiento = st.text_input("Asiento N°")

    st.markdown("<br>", unsafe_allow_html=True)
    enviar = st.form_submit_button("GENERAR DOCUMENTO")

# --- PROCESAMIENTO ---
if enviar:
    try:
        doc = DocxTemplate(archivo_word)
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        hoy = datetime.now()
        
        contexto = {
            "nombre_persona_natural": nombre, "nombre_persona_juridica": nombre,
            "nombres_apellidos": nombre, "numero_dni": dni_rep if tipo_persona == "Jurídica" else documento,
            "numero_ruc": documento, "numero_documento": documento,
            "direccion": direccion, "correo_electronico": correo, "numero_telefono": telefono,
            "nombre_representante_legal": rep_legal, "numero_asiento": asiento,
            "numero_partida_registral": partida, "ciudad": ciudad,
            "fecha_texto": f"{hoy.day} de {meses[hoy.month - 1]} de {hoy.year}",
            "dni_x": "X", "pas_x": " ", "ce_x": " "
        }
        
        doc.render(contexto)
        output = io.BytesIO()
        doc.save(output)
        
        st.success("✅ ¡Documento listo!")
        st.download_button(
            label="📥 Descargar Word",
            data=output.getvalue(),
            file_name=f"AloCredit_{nombre}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Error: Asegúrate de que '{archivo_word}' esté en GitHub.")

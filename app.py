import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Aló Credit | Portal de Documentos", page_icon="💳", layout="centered")

# --- COLORES CORPORATIVOS ---
color_azul_oscuro = "#001B3D"
color_naranja_alo = "#FF7F00"
color_texto_legible = "#001B3D" # Azul oscuro para máxima legibilidad

# --- DISEÑO UI MEJORADO ---
st.markdown(f"""
    <style>
    /* Fondo radial según la imagen de referencia */
    .stApp {{
        background: radial-gradient(circle at 20% 30%, #003a85 0%, {color_azul_oscuro} 60%, {color_naranja_alo} 130%) !important;
        background-attachment: fixed;
    }}
    
    /* Tarjeta de Cristal con mayor opacidad para lectura */
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.88) !important; /* Más sólido para que se vea el texto oscuro */
        backdrop-filter: blur(20px);
        border-radius: 30px !important;
        padding: 40px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5) !important;
    }}

    /* CAMBIO DE FUENTE Y COLOR DEL FORMULARIO */
    h2, p, label, .stMarkdown {{
        color: {color_texto_legible} !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }}

    /* Inputs con bordes definidos */
    .stTextInput>div>div>input {{
        background-color: white !important;
        border: 2px solid #DEDEDE !important;
        color: black !important;
        border-radius: 10px !important;
    }}
    
    /* BOTÓN: Texto cambiado a Azul Oscuro para mejor contraste */
    .stButton>button {{
        background-color: {color_azul_oscuro} !important;
        color: #FFFFFF !important; /* Texto blanco sobre botón oscuro */
        border: 2px solid {color_naranja_alo} !important;
        border-radius: 15px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        padding: 12px !important;
        width: 100%;
        text-transform: uppercase;
        transition: 0.3s;
    }}
    
    .stButton>button:hover {{
        background-color: {color_naranja_alo} !important;
        color: {color_azul_oscuro} !important;
        box-shadow: 0px 0px 20px {color_naranja_alo};
    }}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# --- CABECERA: LOGO MÁS PEQUEÑO ---
logo_path = "hunter1.png" 

col_l, col_c, col_r = st.columns([1.5, 1, 1.5]) # Ajustamos columnas para achicar el centro
with col_c:
    if os.path.exists(logo_path):
        st.image(logo_path, width=160) # Tamaño reducido a 160px
    else:
        st.markdown(f"<h1 style='text-align:center; color:{color_naranja_alo};'>ALÓ CREDIT</h1>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- SELECCIÓN ---
c1, c2 = st.columns(2)
with c1:
    categoria = st.selectbox("Selecciona el Documento", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c2:
    tipo_persona = st.radio("Tipo de Persona", ["Natural", "Jurídica"], horizontal=True)

if categoria == "Contrato de Alianza Comercial":
    archivo_word = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
else:
    archivo_word = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"

# --- FORMULARIO ---
with st.form("form_final"):
    st.markdown("<h2 style='text-align:center; margin-bottom:20px;'>Registro de Información</h2>", unsafe_allow_html=True)
    
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        nombre = st.text_input("Nombres y Apellidos / Razón Social")
    with r1c2:
        documento = st.text_input("DNI / RUC")
        
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        direccion = st.text_input("Dirección")
    with r2c2:
        telefono = st.text_input("Teléfono")
        
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        correo = st.text_input("Correo Electrónico")
    with r3c2:
        ciudad = st.text_input("Ciudad de Firma", value="Lima")
    
    if tipo_persona == "Jurídica":
        st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            rep_legal = st.text_input("Representante Legal

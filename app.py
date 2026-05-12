import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Aló Credit | Portal", page_icon="💳", layout="centered")

# --- COLORES CORPORATIVOS ---
color_azul_oscuro = "#001B3D"
color_naranja_alo = "#FF7F00"

# --- DISEÑO UI (SOLUCIÓN DE COLOR DE FUENTE) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

    /* 1. FONDO DE LA APP */
    .stApp {{
        background: radial-gradient(circle at 20% 30%, #003a85 0%, {color_azul_oscuro} 60%, {color_naranja_alo} 130%) !important;
        background-attachment: fixed;
    }}
    
    /* 2. LETRAS EXTERNAS (Selectores superiores) - BLANCAS */
    .stSelectbox label p, .stRadio label p, .stMarkdown p {{
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }}

    /* 3. CAJA BLANCA DEL FORMULARIO */
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.98) !important; 
        border-radius: 30px !important;
        padding: 40px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5) !important;
        border: none !important;
    }}

    /* 4. SOLUCIÓN AGRESIVA PARA LETRAS DENTRO DEL FORMULARIO - AZUL MARINO */
    /* Este selector apunta directamente a los párrafos dentro de las etiquetas del formulario */
    [data-testid="stForm"] label p, 
    [data-testid="stForm"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stForm"] h2 {{
        color: {color_azul_oscuro} !important;
        text-shadow: none !important;
        -webkit-text-fill-color: {color_azul_oscuro} !important; /* Fuerza el color en algunos navegadores */
    }}

    /* Estilo de los inputs */
    .stTextInput input {{
        color: #000000 !important;
        background-color: #f9f9f9 !important;
    }}
    
    /* BOTÓN GENERAR */
    .stButton button {{
        background-color: {color_azul_oscuro} !important;
        color: white !important;
        border: 2px solid {color_naranja_alo} !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
logo_path = "hunter1.png"
col_l, col_c, col_r = st.columns([1.5, 1, 1.5])
with col_c:
    if os.path.exists(logo_path):
        st.image(logo_path, width=150)

st.markdown("<br>", unsafe_allow_html=True)

# --- SELECTORES (PC: 2 Columnas) ---
c1, c2 = st.columns(2)
with c1:
    categoria = st.selectbox("📂 Tipo de Documento", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c2:
    tipo_persona = st.radio("👤 Perfil de Cliente", ["Natural", "Jurídica"], horizontal=True)

# --- FORMULARIO (PC: 2 Columnas) ---
with st.form("form_registro"):
    st.markdown("<h2 style='text-align:center;'>📝 Registro de Información</h2>", unsafe_allow_html=True)
    
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        nombre = st.text_input("Nombres y Apellidos / Razón Social")
    with r1c2:
        documento = st.text_input("DNI / RUC del Titular")
        
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        direccion = st.text_input("Dirección Declarada")
    with r2c2:
        telefono = st.text_input("Número de Contacto")
        
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        correo = st.text_input("Correo Electrónico")
    with r3c2:
        ciudad = st.text_input("Ciudad de Firma", value="Lima")
    
    if tipo_persona == "Jurídica":
        st.markdown("<hr>", unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            rep_legal = st.text_input("Representante Legal")
            dni_rep = st.text_input("DNI del Representante")
        with cy:
            partida = st.text_input("Partida N°")
            asiento = st.text_input("Asiento N°")

    enviar = st.form_submit_button("🚀 GENERAR DOCUMENTO OFICIAL")

# --- LÓGICA ---
if enviar:
    if not nombre or not documento:
        st.error("❌ Por favor completa el Nombre y el DNI/RUC.")
    else:
        try:
            archivo = "contratonatural.docx" # Ejemplo simplificado para prueba
            doc = DocxTemplate(archivo)
            # ... (resto de tu lógica de renderizado igual que antes)
            st.success("¡Generado!")
        except:
            st.error("Error: Verifica tus plantillas .docx")

st.markdown("<p style='text-align: center; color: white;'>Willy Ríos | Hunter Business</p>", unsafe_allow_html=True)

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

# --- DISEÑO UI (MARCOS Y COLORES CORREGIDOS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

    .stApp {{
        background: radial-gradient(circle at 20% 30%, #003a85 0%, {color_azul_oscuro} 60%, {color_naranja_alo} 130%) !important;
        background-attachment: fixed;
    }}
    
    /* LETRAS EXTERNAS - BLANCAS */
    div:not([data-testid="stForm"]) label p, 
    div:not([data-testid="stForm"]) .stMarkdown p {{
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }}

    /* CAJA BLANCA DEL FORMULARIO */
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.98) !important; 
        border-radius: 30px !important;
        padding: 40px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5) !important;
        border: 2px solid rgba(0, 27, 61, 0.1) !important;
    }}

    /* LETRAS DENTRO DEL FORMULARIO - AZUL MARINO */
    [data-testid="stForm"] label p, 
    [data-testid="stForm"] h2 {{
        color: {color_azul_oscuro} !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }}

    /* MARCOS PARA LAS CAJAS DE TEXTO (INPUTS) */
    .stTextInput div[data-baseweb="input"] {{
        border: 2px solid {color_azul_oscuro} !important; /* Marco azul marino */
        border-radius: 10px !important;
        background-color: #FFFFFF !important;
    }}

    .stTextInput input {{
        color: #000000 !important; /* Texto que escribes en negro */
        font-weight: 600 !important;
    }}
    
    /* BOTÓN GENERAR */
    .stButton button {{
        background-color: {color_azul_oscuro} !important;
        color: white !important;
        border: 2px solid {color_naranja_alo} !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        padding: 10px !important;
        width: 100%;
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

# --- SELECTORES ---
c1, c2 = st.columns(2)
with c1:
    categoria = st.selectbox("📂 Selecciona el Documento", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c2:
    tipo_persona = st.radio("👤 Perfil de Cliente", ["Natural", "Jurídica"], horizontal=True)

# --- FORMULARIO CON MARCOS ---
with st.form("form_final"):
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
        st.markdown("<hr style='border: 1px solid #001B3D;'>", unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            rep_legal = st.text_input("Representante Legal")
            dni_rep = st.text_input("DNI del Representante")
        with cy:
            partida = st.text_input("Partida N°")
            asiento = st.text_input("Asiento N°")

    st.write("")
    enviar = st.form_submit_button("🚀 GENERAR DOCUMENTO OFICIAL")

# --- LÓGICA ---
if enviar:
    if not nombre or not documento:
        st.error("❌ Por favor completa los campos principales.")
    else:
        try:
            # Aquí va tu lógica de DocxTemplate...
            st.success("✅ ¡Formulario enviado correctamente!")
        except:
            st.error("Revisa tus archivos en GitHub.")

st.markdown("<p style='text-align: center; color: white;'>Willy Ríos | Hunter Business</p>", unsafe_allow_html=True)

import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Smart Security | Portal", page_icon="💳", layout="centered")

# --- ESTILOS CORPORATIVOS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');
    
    /* OCULTAR MENÚS DE STREAMLIT */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .stApp { 
        background: radial-gradient(circle at 20% 30%, #003a85 0%, #001B3D 60%, #FF7F00 130%) !important; 
        background-attachment: fixed; 
    }
    [data-testid="stForm"] { 
        background-color: #FFFFFF !important; 
        border-radius: 20px !important; 
        padding: 25px !important; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.4); 
    }
    [data-testid="stForm"] label p, [data-testid="stForm"] h2, [data-testid="stForm"] h3 { 
        color: #001B3D !important; 
        font-family: 'Montserrat', sans-serif !important; 
        font-weight: 700; 
    }
    [data-testid="stForm"] input { color: #000000 !important; }
    [data-testid="stForm"] button { 
        background-color: #001B3D !important; 
        color: white !important; 
        font-weight: 800; 
        width: 100%; 
        border: 2px solid #FF7F00; 
        border-radius: 12px; 
        padding: 12px;
    }
    @media (max-width: 640px) {
        [data-testid="stForm"] { padding: 15px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO ---
if os.path.exists("hunter1.png"):
    col_l, col_c, col_r = st.columns([1.5, 1, 1.5])
    with col_c: st.image("hunter1.png", width=150)

# --- SELECTORES PRINCIPALES ---
c1, c2 = st.columns([1, 1])
with c1:
    categoria = st.selectbox("📂 Tipo de Documento", ["Declaración Jurada", "Contrato de Alianza Comercial"])
with c2:
    tipo_persona = st.radio("👤 Perfil", ["Natural", "Jurídica"], horizontal=True)

# --- FORMULARIO DE REGISTRO ---
with st.form("form_smart_security_v12"):
    st.markdown("<h2 style='text-align:center;'>📝 Registro de Información</h2>", unsafe_allow_html=True)
    
    if tipo_persona == "Natural":
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombres y Apellidos")
            direccion = st.text_input("Dirección / Domicilio Declarado")
            correo = st.text_input("Correo Electrónico")
            pais = st.text_input("País de Origen/Residencia", value="PERÚ")
        with col2:
            documento = st.text_input("DNI / CE")
            ruc_natural = st.text_input("RUC (Opcional, necesario para Contrato)")
            telefono = st.text_input("Teléfono / Celular")
            ciudad = st.text_input("Ciudad de Firma", value="Lima")
        
        if categoria == "Declaración Jurada":
            contexto = {
                "nombres_apellidos": nombre, 
                "numero_documento": documento,
                "dirección_declarada": direccion, 
                "numero_telefono": telefono,
                "correo_electronico": correo, 
                "ciudad": ciudad, 
                "pais": pais,
                "dni_x": "X"
            }
        else:
            contexto = {
                "nombre_persona_natural": nombre,
                "direccion": direccion,
                "numero_ruc": ruc_natural,
                "numero_dni": documento,
                "numero_telefono": telefono,       
                "correo_electron

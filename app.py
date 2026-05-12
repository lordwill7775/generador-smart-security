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

# --- DISEÑO UI PROFESIONAL (RESTAURADO Y MEJORADO) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

    /* Fondo General */
    .stApp {{
        background: radial-gradient(circle at 20% 30%, #003a85 0%, {color_azul_oscuro} 60%, {color_naranja_alo} 130%) !important;
        background-attachment: fixed;
    }}
    
    /* ETIQUETAS EXTERNAS (BLANCAS) */
    .stSelectbox label, .stRadio label, [data-testid="stMarkdownContainer"] p {{
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        font-weight: 700 !important;
    }}

    /* TARJETA DE CRISTAL (EL FORMULARIO) */
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.96) !important; 
        backdrop-filter: blur(20px);
        border-radius: 30px !important;
        padding: 40px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5) !important;
    }}

    /* ETIQUETAS INTERNAS (AZUL MARINO) */
    [data-testid="stForm"] label, [data-testid="stForm"] h2 {{
        color: {color_azul_oscuro} !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        text-shadow: none !important;
    }}

    .stTextInput>div>div>input {{
        background-color: white !important;
        border: 1px solid #ccc !important;
        color: black !important;
        border-radius: 8px !important;
    }}
    
    /* BOTÓN GENERAR */
    .stButton>button {{
        background-color: {color_azul_oscuro} !important;
        color: #FFFFFF !important;
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
    }}

    /* --- MAGIA PARA MÓVIL (No afecta a la PC) --- */
    @media (max-width: 640px) {{
        [data-testid="stForm"] {{
            padding: 20px !important;
        }}
        .stButton>button {{
            font-size: 16px !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- LOGO ---
logo_final = "hunter1.png" if os.path.exists("hunter1.png") else None

col_l, col_c, col_r = st.columns([1.5, 1, 1.5])
with col_c:
    if logo_final:
        st.image(logo_final, width=150)
    else:
        st.markdown(f"<h1 style='text-align:center; color:white;'>ALÓ CREDIT</h1>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- SELECTORES (MANTENIENDO LAS 2 COLUMNAS DE PC) ---
c1, c2 = st.columns(2)
with c1:
    categoria = st.selectbox("📂 Tipo de Documento", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c2:
    tipo_persona = st.radio("👤 Perfil de Cliente", ["Natural", "Jurídica"], horizontal=True)

# --- FORMULARIO (RESTABLECIDO A 2 COLUMNAS) ---
with st.form("form_final"):
    st.markdown("<h2 style='text-align:center;'>📝 Registro de Información</h2>", unsafe_allow_html=True)
    
    # Primera fila de inputs
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        nombre = st.text_input("Nombres y Apellidos / Razón Social")
    with r1c2:
        documento = st.text_input("DNI / RUC del Titular")
        
    # Segunda fila
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        direccion = st.text_input("Dirección Declarada")
    with r2c2:
        telefono = st.text_input("Número de Contacto")
        
    # Tercera fila
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        correo = st.text_input("Correo Electrónico")
    with r3c2:
        ciudad = st.text_input("Ciudad de Firma", value="Lima")
    
    rep_legal, dni_rep, partida, asiento = "", "", "", ""
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

# --- LÓGICA DE PROCESADO ---
if enviar:
    if not nombre or not documento:
        st.error("❌ Completa los campos obligatorios.")
    else:
        try:
            if categoria == "Contrato de Alianza Comercial":
                archivo = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
            else:
                archivo = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"
            
            doc = DocxTemplate(archivo)
            hoy = datetime.now()
            meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
            
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
            output.seek(0)
            
            st.balloons()
            st.download_button(label="📥 DESCARGAR WORD", data=output, file_name=f"AloCredit_{nombre}.docx")
        except:
            st.error("Error técnico con las plantillas.")

st.markdown("<p style='text-align: center; color: white; font-weight: bold;'>Willy Ríos | Hunter Business</p>", unsafe_allow_html=True)

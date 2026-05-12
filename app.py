import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Aló Credit | Portal de Documentos", page_icon="💳", layout="centered")

# --- COLORES CORPORATIVOS EXTRAÍDOS DE TU LOGO ---
color_azul_oscuro = "#001B3D"
color_naranja_alo = "#FF7F00"

# --- DISEÑO UI PROFESIONAL (ESTILO GLASSMORPHISM) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: radial-gradient(circle at 20% 30%, #003a85 0%, {color_azul_oscuro} 60%, {color_naranja_alo} 130%) !important;
        background-attachment: fixed;
    }}
    
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border-radius: 35px !important;
        padding: 50px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5) !important;
    }}

    h1, h2, h3, p, label, .stMarkdown {{
        color: #FFFFFF !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600 !important;
    }}

    .stTextInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
        border-radius: 12px !important;
    }}
    
    .stButton>button {{
        background-color: {color_azul_oscuro} !important;
        color: white !important;
        border: 2px solid {color_naranja_alo} !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        font-size: 20px !important;
        padding: 15px !important;
        width: 100%;
        text-transform: uppercase;
        transition: 0.4s;
    }}
    
    .stButton>button:hover {{
        background-color: {color_naranja_alo} !important;
        color: {color_azul_oscuro} !important;
        box-shadow: 0px 0px 30px {color_naranja_alo};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA: AQUÍ APARECE EL LOGOTIPO ---
# Intentamos con hunter1.png que es tu archivo más reciente
logo_path = "hunter1.png" 

col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    elif os.path.exists("hunter.png"):
        st.image("hunter.png", use_container_width=True)
    else:
        # Solo si no encuentra ningún archivo muestra el texto
        st.markdown(f"<h1 style='text-align:center; color:{color_naranja_alo};'>ALÓ CREDIT</h1>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- SELECTORES ---
c1, c2 = st.columns(2)
with c1:
    categoria = st.selectbox("Selecciona el Documento", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c2:
    tipo_persona = st.radio("Tipo de Persona", ["Natural", "Jurídica"], horizontal=True)

# Mapeo de archivos Word
if categoria == "Contrato de Alianza Comercial":
    archivo_word = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
else:
    archivo_word = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"

# --- FORMULARIO ---
with st.form("form_final"):
    st.markdown("<h2 style='text-align:center;'>Registro de Información</h2>", unsafe_allow_html=True)
    
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
        st.markdown("<hr style='opacity:0.2;'>", unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            rep_legal = st.text_input("Representante Legal")
            dni_rep = st.text_input("DNI Representante")
        with cy:
            partida = st.text_input("Partida N°")
            asiento = st.text_input("Asiento N°")

    st.write("")
    enviar = st.form_submit_button("GENERAR DOCUMENTO")

# --- LÓGICA DE PROCESAMIENTO ---
if enviar:
    try:
        doc = DocxTemplate(archivo_word)
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
        
        st.balloons()
        st.success("✅ ¡Generado con éxito!")
        st.download_button(label="📥 Descargar Word", data=output.getvalue(), file_name=f"AloCredit_{nombre}.docx")
    except Exception as e:
        st.error(f"Error: Revisa que {archivo_word} esté en GitHub.")

st.markdown("<p style='text-align: center; opacity: 0.6;'>Willy Ríos | Hunter Business</p>", unsafe_allow_html=True)

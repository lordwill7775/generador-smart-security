import streamlit as st
from docxtpl import DocxTemplate
import io
import os
import base64
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Aló Credit | Portal Corporativo", page_icon="💳", layout="wide")

# --- COLORES DEL LOGO (Extraídos de hunter.png) ---
azul_marino = "#001B3D"
cian_tecnologico = "#00E5FF"

# Función para convertir imagen a base64 (ayuda a forzar la visualización del logo)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- ESTILO PROFESIONAL ---
st.markdown(f"""
    <style>
    /* Fondo con degradado de los dos colores del logo */
    .stApp {{
        background: linear-gradient(135deg, {azul_marino} 0%, #002d62 50%, {cian_tecnologico} 100%);
        background-attachment: fixed;
    }}

    /* Tarjeta translúcida (Glassmorphism) */
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(10px);
        border-radius: 30px !important;
        padding: 40px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }}

    /* Etiquetas y Títulos */
    h1, h2, h3, label, .stMarkdown {{
        color: {azul_marino} !important;
        font-family: 'Helvetica Neue', sans-serif;
    }}

    /* Inputs con bordes definidos */
    .stTextInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid {azul_marino} !important;
        color: black !important;
        border-radius: 12px !important;
    }}

    /* Botón Profesional Aló Credit */
    .stButton>button {{
        background: linear-gradient(90deg, {azul_marino} 0%, #004080 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 30px !important;
        font-weight: bold !important;
        font-size: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px {cian_tecnologico} !important;
        color: {cian_tecnologico} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO CON LOGO ---
logo_path = "hunter.png"
if os.path.exists(logo_path):
    # Forzamos el centrado del logo con columnas
    _, col_logo, _ = st.columns([1, 1, 1])
    with col_logo:
        st.image(logo_path, width=250)
else:
    st.error("⚠️ Error: No se encuentra el archivo 'hunter.png'. Verifica el nombre en tu GitHub.")

st.markdown("<br>", unsafe_allow_html=True)

# --- SECCIÓN DE SELECCIÓN ---
col_1, col_2 = st.columns(2)
with col_1:
    categoria = st.selectbox("📂 Tipo de Documento", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with col_2:
    tipo_persona = st.radio("👤 Perfil de Cliente", ["Natural", "Jurídica"], horizontal=True)

# Mapeo de archivos Word
if categoria == "Contrato de Alianza Comercial":
    archivo_word = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
else:
    archivo_word = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"

# --- FORMULARIO ---
with st.form("form_corporativo"):
    st.markdown(f"<h2 style='text-align: center;'>Registro de Datos Oficiales</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        nombre = st.text_input("Nombre o Razón Social")
        documento = st.text_input("DNI o RUC")
        correo = st.text_input("Correo Electrónico")
    with c2:
        direccion = st.text_input("Dirección Declarada")
        telefono = st.text_input("Teléfono / Celular")
        ciudad = st.text_input("Ciudad de Firma", value="Lima")
    
    if tipo_persona == "Jurídica":
        st.markdown("<hr style='border: 0.5px solid #001B3D; opacity: 0.2;'>", unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            rep_legal = st.text_input("Representante Legal")
            dni_rep = st.text_input("DNI del Representante")
        with cy:
            partida = st.text_input("Partida Registral N°")
            asiento = st.text_input("Asiento N°")

    st.write("")
    enviar = st.form_submit_button("🔨 PROCESAR Y GENERAR")

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
        st.success(f"✅ ¡Documento generado para {nombre}!")
        st.download_button(
            label="📥 DESCARGAR FORMATO EDITABLE",
            data=output.getvalue(),
            file_name=f"Aló_Credit_{nombre}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Error técnico: {e}")

import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Aló Credit | Portal de Documentos", page_icon="💳", layout="wide")

# --- COLORES CORPORATIVOS ---
color_azul_profundo = "#001B3D" # El azul oscuro del logo
color_turquesa = "#00E5FF"      # El cian brillante del logo

# --- DISEÑO UI CON DEGRADADO ---
st.markdown(f"""
    <style>
    /* Fondo con degradado fluido entre los colores del logo */
    .stApp {{
        background: linear-gradient(145deg, {color_azul_profundo} 0%, #003a85 45%, {color_turquesa} 100%);
        background-attachment: fixed;
    }}
    
    /* Tarjeta del Formulario (Blanca y legible) */
    [data-testid="stForm"] {{
        background-color: rgba(255, 255, 255, 0.98) !important;
        border-radius: 25px !important;
        padding: 40px !important;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.4) !important;
        border: 2px solid {color_turquesa} !important;
    }}

    /* Títulos y Etiquetas */
    h1, h2, h3, p, label, .stMarkdown {{
        color: {color_azul_profundo} !important;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600 !important;
    }}

    /* Inputs Visibles con Bordes Claros */
    .stTextInput>div>div>input {{
        border: 2px solid {color_azul_profundo} !important;
        background-color: #fdfdfd !important;
        color: #000000 !important;
        border-radius: 10px !important;
    }}

    /* Botón Neón Aló Credit */
    .stButton>button {{
        background-color: {color_azul_profundo} !important;
        color: white !important;
        border: 2px solid {color_turquesa} !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        font-size: 22px !important;
        padding: 12px 24px !important;
        width: 100%;
        text-transform: uppercase;
        transition: 0.4s;
    }}
    
    .stButton>button:hover {{
        background-color: {color_turquesa} !important;
        color: {color_azul_profundo} !important;
        box-shadow: 0px 0px 25px {color_turquesa};
        border: 2px solid {color_azul_profundo} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DEL LOGO (MÉTODO SEGURO) ---
with st.container():
    # Intentamos cargar desde la ruta raíz
    logo_path = "hunter.png"
    col_l, col_c, col_r = st.columns([1, 1, 1]) # Usamos 3 columnas para centrarlo
    with col_c:
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        else:
            # Texto de respaldo si el logo sigue sin leerse
            st.markdown(f"<h1 style='text-align:center; color:{color_turquesa} !important;'>ALÓ CREDIT</h1>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- INTERFAZ DE SELECCIÓN ---
c_sel1, c_sel2 = st.columns(2)
with c_sel1:
    categoria = st.selectbox("📂 ¿Qué documento desea generar hoy?", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c_sel2:
    tipo_persona = st.radio("👤 Tipo de Cliente / Aliado:", ["Natural", "Jurídica"], horizontal=True)

# Mapeo automático de archivos Word
if categoria == "Contrato de Alianza Comercial":
    archivo_word = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
else:
    archivo_word = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"

# --- FORMULARIO DE RECOLECCIÓN ---
with st.form("form_v3"):
    st.markdown(f"<h2 style='text-align:center;'>📝 Registro de Información</h2>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombres y Apellidos / Razón Social")
        documento = st.text_input("DNI / RUC del Titular")
        correo = st.text_input("Correo Electrónico")
    with col2:
        direccion = st.text_input("Dirección Declarada")
        telefono = st.text_input("Número de Contacto")
        ciudad = st.text_input("Ciudad de Firma", value="Lima")
    
    if tipo_persona == "Jurídica":
        st.markdown(f"<hr style='border:1px solid {color_azul_profundo}; opacity: 0.3;'>", unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            rep_legal = st.text_input("Representante Legal")
            dni_rep = st.text_input("DNI del Representante")
        with cy:
            partida = st.text_input("Partida Registral N°")
            asiento = st.text_input("Asiento N°")

    st.markdown("<br>", unsafe_allow_html=True)
    enviar = st.form_submit_button("🚀 GENERAR Y PROCESAR")

if enviar:
    try:
        # Procesar Word
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
        st.success(f"✅ ¡Documento de {nombre} listo para descargar!")
        st.download_button(
            label="📥 DESCARGAR DOCUMENTO WORD",
            data=output.getvalue(),
            file_name=f"AlóCredit_{nombre}_{categoria}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Error: Verifique que el archivo '{archivo_word}' esté correctamente en su repositorio de GitHub.")

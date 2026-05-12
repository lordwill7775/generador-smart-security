import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Aló Credit | Portal de Documentos", page_icon="💳", layout="centered")

# --- COLORES CORPORATIVOS EXTRAÍDOS DE LA IMAGEN ---
color_azul_oscuro = "#001B3D"
color_naranja_alo = "#FF7F00"
color_celeste_brillante = "#00E5FF"

# --- DISEÑO UI PROFESIONAL (REPLICANDO LA IMAGEN) ---
st.markdown(f"""
    <style>
    /* Fondo con degradado radial profundo para dar profundidad */
    .stApp {{
        background: radial-gradient(circle at 20% 30%, #003a85 0%, {color_azul_oscuro} 60%, {color_naranja_alo} 130%) !important;
        background-attachment: fixed;
    }}
    
    /* Contenedor tipo Cristal (Glassmorphism) */
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border-radius: 35px !important;
        padding: 50px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5) !important;
    }}

    /* Títulos y Etiquetas en Blanco Puro */
    h1, h2, h3, p, label, .stMarkdown {{
        color: #FFFFFF !important;
        font-family: 'Poppins', 'Segoe UI', sans-serif;
        font-weight: 600 !important;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.3);
    }}

    /* Estilo de los Campos de Entrada (Input) */
    .stTextInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
        border-radius: 12px !important;
        height: 45px;
    }}
    
    /* Botón de Generar (Azul oscuro con borde Naranja neón) */
    .stButton>button {{
        background-color: {color_azul_oscuro} !important;
        color: white !important;
        border: 2px solid {color_naranja_alo} !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        font-size: 20px !important;
        padding: 15px 24px !important;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.4s;
        box-shadow: 0 4px 15px rgba(255, 127, 0, 0.3);
        margin-top: 20px;
    }}
    
    .stButton>button:hover {{
        background-color: {color_naranja_alo} !important;
        color: {color_azul_oscuro} !important;
        box-shadow: 0px 0px 30px {color_naranja_alo};
        transform: translateY(-2px);
    }}

    /* Selectbox y Radio Buttons */
    .stSelectbox>div>div {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
    }}
    
    div[data-testid="stMarkdownContainer"] p {{
        font-size: 14px;
        opacity: 0.9;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DEL LOGO ---
logo_path = "hunter.png"
col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown(f"<h1 style='text-align:center; color:{color_naranja_alo};'>ALÓ CREDIT</h1>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- SECCIÓN DE SELECCIÓN ---
# Encapsulamos en columnas para mantener el orden de la imagen
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

# --- FORMULARIO DE RECOLECCIÓN (ESTILO CRISTAL) ---
with st.form("form_final_visual"):
    st.markdown("<h2 style='text-align:center;'>Registro de Información</h2>", unsafe_allow_html=True)
    
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        nombre = st.text_input("Nombres y Apellidos / Razón Social")
    with row1_col2:
        documento = st.text_input("DNI / RUC del Titular")
        
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        direccion = st.text_input("Dirección Declarada")
    with row2_col2:
        telefono = st.text_input("Número de Contacto")
        
    row3_col1, row3_col2 = st.columns(2)
    with row3_col1:
        correo = st.text_input("Correo Electrónico")
    with row3_col2:
        ciudad = st.text_input("Ciudad de Firma", value="Lima")
    
    if tipo_persona == "Jurídica":
        st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            rep_legal = st.text_input("Representante Legal")
            dni_rep = st.text_input("DNI del Representante")
        with cy:
            partida = st.text_input("Partida Registral N°")
            asiento = st.text_input("Asiento N°")

    st.markdown("<br>", unsafe_allow_html=True)
    enviar = st.form_submit_button("Generar Documento")

# --- LÓGICA DE PROCESAMIENTO (TU CÓDIGO ORIGINAL) ---
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
        st.success(f"✅ ¡Documento generado correctamente!")
        st.download_button(
            label="📥 DESCARGAR WORD",
            data=output.getvalue(),
            file_name=f"AlóCredit_{nombre}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Error: Verifique sus archivos de plantilla en GitHub.")

# Pie de página como en la imagen
st.markdown("<p style='text-align: center; opacity: 0.6;'>Willy Ríos | Hunter Business</p>", unsafe_allow_html=True)

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

# --- DISEÑO UI PROFESIONAL ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

    .stApp {{
        background: radial-gradient(circle at 20% 30%, #003a85 0%, {color_azul_oscuro} 60%, {color_naranja_alo} 130%) !important;
        background-attachment: fixed;
    }}
    
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.94) !important; 
        backdrop-filter: blur(20px);
        border-radius: 30px !important;
        padding: 40px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5) !important;
    }}

    /* Estilo de etiquetas en azul marino profundo */
    h2, p, label, .stMarkdown, [data-testid="stWidgetLabel"] p {{
        color: {color_azul_oscuro} !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }}

    .stTextInput>div>div>input {{
        background-color: white !important;
        border: 1px solid #ccc !important;
        color: black !important;
        border-radius: 8px !important;
    }}
    
    /* Botón con texto blanco y borde naranja */
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
        margin-top: 10px;
    }}
    
    .stButton>button:hover {{
        background-color: {color_naranja_alo} !important;
        color: {color_azul_oscuro} !important;
        box-shadow: 0px 0px 15px {color_naranja_alo};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA: LOGO PEQUEÑO ---
# He configurado el buscador para intentar con los nombres que aparecen en tus capturas
logo_path = "hunter1.png"
if not os.path.exists(logo_path):
    logo_path = "hunter.png"

col_l, col_c, col_r = st.columns([1.5, 1, 1.5])
with col_c:
    if os.path.exists(logo_path):
        st.image(logo_path, width=140) # Tamaño pequeño y elegante
    else:
        st.markdown(f"<h1 style='text-align:center; color:{color_naranja_alo};'>ALÓ CREDIT</h1>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- SELECTORES FUERA DEL FORMULARIO ---
c1, c2 = st.columns(2)
with c1:
    categoria = st.selectbox("📂 Selecciona el Documento", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c2:
    tipo_persona = st.radio("👤 Tipo de Persona", ["Natural", "Jurídica"], horizontal=True)

# Asignación de archivos
if categoria == "Contrato de Alianza Comercial":
    archivo_word = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
else:
    archivo_word = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"

# --- FORMULARIO DE REGISTRO ---
with st.form("registro_datos_form"):
    st.markdown("<h2 style='text-align:center;'>📝 Registro de Información</h2>", unsafe_allow_html=True)
    
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        nombre = st.text_input("Nombres y Apellidos / Razón Social")
    with r1c2:
        documento = st.text_input("DNI / RUC")
        
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        direccion = st.text_input("Dirección")
    with r2c2:
        telefono = st.text_input("Número de Contacto")
        
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        correo = st.text_input("Correo Electrónico")
    with r3c2:
        ciudad = st.text_input("Ciudad de Firma", value="Lima")
    
    # Variables inicializadas para evitar errores
    rep_legal = ""
    dni_rep = ""
    partida = ""
    asiento = ""
    
    if tipo_persona == "Jurídica":
        st.markdown("<hr style='border: 0.5px solid #ddd;'>", unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            rep_legal = st.text_input("Representante Legal")
            dni_rep = st.text_input("DNI del Representante")
        with cy:
            partida = st.text_input("Partida Registral N°")
            asiento = st.text_input("Asiento N°")

    # EL BOTÓN DEBE ESTAR AQUÍ ADENTRO
    submit_button = st.form_submit_button("🚀 GENERAR DOCUMENTO OFICIAL")

# --- LÓGICA DE PROCESAMIENTO ---
if submit_button:
    if not nombre or not documento:
        st.warning("⚠️ Por favor, completa los campos principales (Nombre y DNI/RUC).")
    else:
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
            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            st.balloons()
            st.success(f"✅ ¡Documento para {nombre} listo!")
            st.download_button(
                label="📥 DESCARGAR ARCHIVO WORD",
                data=buffer,
                file_name=f"AloCredit_{nombre}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except

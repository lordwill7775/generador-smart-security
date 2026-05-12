import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Smart Security | Portal", page_icon="💳", layout="centered")

# --- COLORES CORPORATIVOS ---
color_azul_oscuro = "#001B3D"
color_naranja_alo = "#FF7F00"

# --- DISEÑO UI BLINDADO (PC INALTERABLE + FIX MÓVIL) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

    /* Fondo general */
    .stApp {{
        background: radial-gradient(circle at 20% 30%, #003a85 0%, {color_azul_oscuro} 60%, {color_naranja_alo} 130%) !important;
        background-attachment: fixed;
    }}
    
    /* MANTENER PC PERFECTO: Etiquetas externas blancas */
    .stSelectbox label p, .stRadio label p {{
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }}

    /* CAJA DEL FORMULARIO: Blanco sólido para evitar transparencia en móvil */
    [data-testid="stForm"] {{
        background-color: #FFFFFF !important; 
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4) !important;
    }}

    /* TEXTO INTERNO: Azul Marino siempre */
    [data-testid="stForm"] label p, [data-testid="stForm"] h2 {{
        color: {color_azul_oscuro} !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }}

    /* SOLUCIÓN CAJAS NEGRAS: Forzamos fondo blanco y borde azul */
    [data-testid="stForm"] div[data-baseweb="input"] {{
        background-color: #FFFFFF !important;
        border: 2px solid {color_azul_oscuro} !important;
        border-radius: 10px !important;
    }}

    /* Forzamos color de letra negro al escribir (evita texto invisible en móvil) */
    [data-testid="stForm"] input {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }}
    
    /* BOTÓN: Mantiene el estilo que te gustó en PC */
    [data-testid="stForm"] button {{
        background-color: {color_azul_oscuro} !important;
        color: #FFFFFF !important;
        border: 2px solid {color_naranja_alo} !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        width: 100% !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- LOGO ---
logo_path = "hunter1.png"
if os.path.exists(logo_path):
    col_l, col_c, col_r = st.columns([1.5, 1, 1.5])
    with col_c:
        st.image(logo_path, width=150)

st.markdown("<br>", unsafe_allow_html=True)

# --- SELECTORES (MANTIENEN SU LUGAR EN PC) ---
c1, c2 = st.columns([1.5, 1])
with c1:
    categoria = st.selectbox("📂 Tipo de Documento", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c2:
    tipo_persona = st.radio("👤 Perfil", ["Natural", "Jurídica"], horizontal=True)

# --- FORMULARIO ---
with st.form("form_final_v4"):
    st.markdown("<h2 style='text-align:center;'>📝 Registro de Información</h2>", unsafe_allow_html=True)
    
    # Esta estructura de columnas es la que se ve perfecta en tu PC
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombres y Apellidos / Razón Social")
        direccion = st.text_input("Dirección Declarada")
        correo = st.text_input("Correo Electrónico")
    with col2:
        documento = st.text_input("DNI / RUC del Titular")
        telefono = st.text_input("Número de Contacto")
        ciudad = st.text_input("Ciudad de Firma", value="Lima")
    
    if tipo_persona == "Jurídica":
        st.markdown("<hr style='border: 1px solid #001B3D;'>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            rep_legal = st.text_input("Representante Legal")
            dni_rep = st.text_input("DNI del Representante")
        with col4:
            partida = st.text_input("Partida N°")
            asiento = st.text_input("Asiento N°")
    else:
        rep_legal, dni_rep, partida, asiento = "", "", "", ""

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("🚀 GENERAR DOCUMENTO OFICIAL")

# --- LÓGICA ---
if submit:
    if not nombre or not documento:
        st.error("❌ Por favor completa los campos obligatorios.")
    else:
        try:
            # Determinación de archivos según tu estructura
            if categoria == "Contrato de Alianza Comercial":
                archivo = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
            else:
                archivo = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"
            
            doc = DocxTemplate(archivo)
            hoy = datetime.now()
            meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
            
            contexto = {
                "nombres_apellidos": nombre, "numero_documento": documento,
                "direccion": direccion, "correo_electronico": correo, "numero_telefono": telefono,
                "nombre_representante_legal": rep_legal, "numero_asiento": asiento,
                "numero_partida_registral": partida, "ciudad": ciudad,
                "fecha_texto": f"{hoy.day} de {meses[hoy.month - 1]} de {hoy.year}"
            }
            
            doc.render(contexto)
            output = io.BytesIO()
            doc.save(output)
            output.seek(0)
            
            st.balloons()
            st.success(f"✅ ¡Documento para {nombre} generado con éxito!")
            st.download_button(
                label="📥 DESCARGAR ARCHIVO WORD",
                data=output,
                file_name=f"Smart_Security_{nombre}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error("Archivo de plantilla no encontrado. Verifica tu GitHub.")

st.markdown("<p style='text-align: center; color: white;'>Willy Ríos | Smart Security</p>", unsafe_allow_html=True)

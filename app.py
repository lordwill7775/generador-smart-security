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
    
    /* MEJORA DE VISIBILIDAD PARA ETIQUETAS SOBRE EL FONDO AZUL */
    [data-testid="stHeader"] {{background: rgba(0,0,0,0);}}
    
    .stSelectbox label, .stRadio label, [data-testid="stMarkdownContainer"] p {{
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5); /* Sombra para resaltar sobre el fondo */
        font-weight: 700 !important;
    }}

    /* TARJETA DEL FORMULARIO (TEXTO OSCURO PARA CONTRASTE) */
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.95) !important; 
        backdrop-filter: blur(20px);
        border-radius: 30px !important;
        padding: 40px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5) !important;
    }}

    [data-testid="stForm"] label, [data-testid="stForm"] h2 {{
        color: {color_azul_oscuro} !important;
        text-shadow: none !important;
    }}

    .stTextInput>div>div>input {{
        background-color: white !important;
        border: 1px solid #ccc !important;
        color: black !important;
    }}
    
    /* BOTÓN CORPORATIVO */
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
    }}
    
    .stButton>button:hover {{
        background-color: {color_naranja_alo} !important;
        color: {color_azul_oscuro} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA: MANEJO DEL LOGO ---
logo_final = None
for nombre in ["hunter1.png", "cazador1.png", "hunter.png"]:
    if os.path.exists(nombre):
        logo_final = nombre
        break

col_l, col_c, col_r = st.columns([1.5, 1, 1.5])
with col_c:
    if logo_final:
        st.image(logo_final, width=150)
    else:
        st.markdown(f"<h1 style='text-align:center; color:{color_naranja_alo};'>ALÓ CREDIT</h1>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- SELECTORES (AHORA CON LETRAS BLANCAS LEGIBLES) ---
c1, c2 = st.columns(2)
with c1:
    categoria = st.selectbox("📂 Tipo de Documento", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c2:
    tipo_persona = st.radio("👤 Perfil de Cliente", ["Natural", "Jurídica"], horizontal=True)

if categoria == "Contrato de Alianza Comercial":
    archivo_word = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
else:
    archivo_word = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"

# --- FORMULARIO ---
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

# --- PROCESAMIENTO ---
if enviar:
    if not nombre or not documento:
        st.error("❌ Por favor completa el Nombre y el DNI/RUC.")
    else:
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
            output.seek(0)
            
            st.balloons()
            st.success("✅ ¡Generado con éxito!")
            st.download_button(
                label="📥 DESCARGAR WORD", 
                data=output, 
                file_name=f"AloCredit_{nombre}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"Error técnico. Verifica que las plantillas existan.")

st.markdown("<p style='text-align: center; color: white; font-weight: bold;'>Willy Ríos | Hunter Business</p>", unsafe_allow_html=True)

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

# --- DISEÑO UI (ESTILOS REFORZADOS Y FUNCIONALES) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

    .stApp {{
        background: radial-gradient(circle at 20% 30%, #003a85 0%, {color_azul_oscuro} 60%, {color_naranja_alo} 130%) !important;
        background-attachment: fixed;
    }}
    
    /* TEXTO EXTERNO - BLANCO */
    .stSelectbox label p, .stRadio label p, .stMarkdown p {{
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }}

    /* CAJA DEL FORMULARIO */
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.98) !important; 
        border-radius: 30px !important;
        padding: 30px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5) !important;
    }}

    /* TEXTO INTERNO - AZUL MARINO (Selector de alta prioridad) */
    div[data-testid="stForm"] .stText {color_azul_oscuro};
    div[data-testid="stForm"] label p {{
        color: {color_azul_oscuro} !important;
        font-family: 'Montserrat', sans-serif !important;
    }}
    
    div[data-testid="stForm"] h2 {{
        color: {color_azul_oscuro} !important;
    }}

    /* INPUTS CON BORDE AZUL MARINO */
    .stTextInput div[data-baseweb="input"] {{
        border: 2px solid {color_azul_oscuro} !important;
        border-radius: 10px !important;
        background-color: white !important;
    }}

    .stTextInput input {{
        color: black !important;
    }}
    
    /* BOTÓN DE ENVÍO */
    .stButton button {{
        background-color: {color_azul_oscuro} !important;
        color: white !important;
        border: 2px solid {color_naranja_alo} !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        width: 100%;
        height: 3em;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
logo_path = "hunter1.png"
if os.path.exists(logo_path):
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        st.image(logo_path, width=150)

st.write("")

# --- SELECTORES FUERA DEL FORMULARIO ---
c1, c2 = st.columns(2)
with c1:
    categoria = st.selectbox("📂 Tipo de Documento", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c2:
    tipo_persona = st.radio("👤 Perfil de Cliente", ["Natural", "Jurídica"], horizontal=True)

# --- FORMULARIO ---
with st.form("main_form"):
    st.markdown(f"<h2 style='text-align:center;'>📝 Registro de Información</h2>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        nombre = st.text_input("Nombres y Apellidos / Razón Social")
        direccion = st.text_input("Dirección Declarada")
        correo = st.text_input("Correo Electrónico")
    with col_b:
        documento = st.text_input("DNI / RUC del Titular")
        telefono = st.text_input("Número de Contacto")
        ciudad = st.text_input("Ciudad de Firma", value="Lima")
    
    if tipo_persona == "Jurídica":
        st.markdown(f"<hr style='border: 1px solid {color_azul_oscuro}'>", unsafe_allow_html=True)
        col_c, col_d = st.columns(2)
        with col_c:
            rep_legal = st.text_input("Representante Legal")
            dni_rep = st.text_input("DNI del Representante")
        with col_d:
            partida = st.text_input("Partida N°")
            asiento = st.text_input("Asiento N°")
    else:
        rep_legal, dni_rep, partida, asiento = "", "", "", ""

    # ESTE ES EL BOTÓN QUE MANDA LA SEÑAL
    submit = st.form_submit_button("🚀 GENERAR DOCUMENTO OFICIAL")

# --- PROCESO TRAS EL CLICK ---
if submit:
    if not nombre or not documento:
        st.error("❌ Por favor completa el nombre y documento.")
    else:
        try:
            # Determinamos plantilla
            if categoria == "Contrato de Alianza Comercial":
                archivo = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
            else:
                archivo = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"
            
            # Cargar y Renderizar
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
            
            # Guardar en memoria
            output = io.BytesIO()
            doc.save(output)
            output.seek(0)
            
            # Efectos y Descarga
            st.balloons()
            st.success(f"✅ ¡Datos recibidos para {nombre}!")
            st.download_button(
                label="📥 CLIC AQUÍ PARA DESCARGAR WORD",
                data=output,
                file_name=f"Documento_{nombre}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"Error: No se encontró el archivo {archivo} en GitHub.")

st.markdown("<p style='text-align: center; color: white;'>Willy Ríos | Hunter Business</p>", unsafe_allow_html=True)

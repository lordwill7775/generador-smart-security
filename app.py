import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA (Optimizada para Móvil) ---
st.set_page_config(
    page_title="Aló Credit | Móvil", 
    page_icon="💳", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- COLORES CORPORATIVOS ---
color_azul_oscuro = "#001B3D"
color_naranja_alo = "#FF7F00"

# --- CSS RESPONSIVE ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

    .stApp {{
        background: radial-gradient(circle at 20% 30%, #003a85 0%, {color_azul_oscuro} 60%, {color_naranja_alo} 130%) !important;
        background-attachment: fixed;
    }}

    /* Ajuste de contenedores para pantallas pequeñas */
    @media (max-width: 640px) {{
        .main .block-container {{
            padding: 10px !important;
        }}
        [data-testid="stForm"] {{
            padding: 20px !important;
            border-radius: 20px !important;
        }}
        h2 {{
            font-size: 1.2rem !important;
        }}
    }}
    
    /* Etiquetas externas (Blancas) */
    .stSelectbox label, .stRadio label {{
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
    }}

    /* Etiquetas internas (Azul Marino) */
    [data-testid="stForm"] label {{
        color: {color_azul_oscuro} !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.85rem !important;
    }}
    
    [data-testid="stForm"] h2 {{
        color: {color_azul_oscuro} !important;
        margin-bottom: 20px;
    }}

    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.98) !important; 
        border-radius: 25px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
    }}

    .stTextInput>div>div>input {{
        border-radius: 10px !important;
        border: 1px solid #ddd !important;
    }}
    
    /* Botón Gigante para Celular */
    .stButton>button {{
        background-color: {color_azul_oscuro} !important;
        color: white !important;
        border: 2px solid {color_naranja_alo} !important;
        border-radius: 15px !important;
        height: 3.5rem !important;
        font-weight: 800 !important;
        width: 100%;
        margin-top: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- LOGO PEQUEÑO ---
logo_final = None
for nombre in ["hunter1.png", "cazador1.png", "hunter.png"]:
    if os.path.exists(nombre):
        logo_final = nombre
        break

if logo_final:
    st.image(logo_final, width=120)
else:
    st.markdown("<h2 style='color:white; text-align:center;'>ALÓ CREDIT</h2>", unsafe_allow_html=True)

# --- SELECTORES (Uno tras otro en móvil) ---
categoria = st.selectbox("📄 Documento a generar:", ["Contrato de Alianza Comercial", "Declaración Jurada"])
tipo_persona = st.radio("👤 Perfil:", ["Natural", "Jurídica"], horizontal=True)

# --- FORMULARIO ADAPTATIVO ---
with st.form("movil_form"):
    st.markdown("<h2 style='text-align:center;'>Registro</h2>", unsafe_allow_html=True)
    
    nombre = st.text_input("Nombres / Razón Social")
    documento = st.text_input("DNI / RUC")
    direccion = st.text_input("Dirección")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo")
    ciudad = st.text_input("Ciudad de Firma", value="Lima")
    
    rep_legal, dni_rep, partida, asiento = "", "", "", ""
    if tipo_persona == "Jurídica":
        st.markdown("<hr>", unsafe_allow_html=True)
        rep_legal = st.text_input("Representante Legal")
        dni_rep = st.text_input("DNI Representante")
        partida = st.text_input("Partida N°")
        asiento = st.text_input("Asiento N°")

    enviar = st.form_submit_button("GENERAR DOCUMENTO")

# --- LÓGICA DE PROCESADO ---
if enviar:
    if not nombre or not documento:
        st.error("Campos obligatorios vacíos")
    else:
        try:
            # Selección de archivo
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
            
            st.success("¡Generado!")
            st.download_button(
                label="📥 DESCARGAR AHORA", 
                data=output, 
                file_name=f"Contrato_{nombre}.docx",
                use_container_width=True # Botón ancho total en móvil
            )
        except:
            st.error("Error: Verifica las plantillas en tu GitHub.")

st.markdown("<p style='text-align: center; color: white; font-size: 0.8rem;'>Willy Ríos | Hunter Business</p>", unsafe_allow_html=True)

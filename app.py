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

# --- DISEÑO UI BLINDADO ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');
    .stApp {{
        background: radial-gradient(circle at 20% 30%, #003a85 0%, {color_azul_oscuro} 60%, {color_naranja_alo} 130%) !important;
        background-attachment: fixed;
    }}
    .stSelectbox label p, .stRadio label p {{
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }}
    [data-testid="stForm"] {{
        background-color: #FFFFFF !important; 
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4) !important;
    }}
    [data-testid="stForm"] label p, [data-testid="stForm"] h2 {{
        color: {color_azul_oscuro} !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }}
    [data-testid="stForm"] div[data-baseweb="input"] {{
        background-color: #FFFFFF !important;
        border: 2px solid {color_azul_oscuro} !important;
        border-radius: 10px !important;
    }}
    [data-testid="stForm"] input {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }}
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

# --- CABECERA ---
logo_path = "hunter1.png"
if os.path.exists(logo_path):
    col_l, col_c, col_r = st.columns([1.5, 1, 1.5])
    with col_c: st.image(logo_path, width=150)

st.markdown("<br>", unsafe_allow_html=True)

# --- SELECTORES ---
c1, c2 = st.columns([1.5, 1])
with c1:
    categoria = st.selectbox("📂 Tipo de Documento", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c2:
    tipo_persona = st.radio("👤 Perfil", ["Natural", "Jurídica"], horizontal=True)

# --- FORMULARIO DINÁMICO ---
with st.form("form_smart_security"):
    st.markdown("<h2 style='text-align:center;'>📝 Registro de Información</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    if tipo_persona == "Natural":
        with col1:
            nombre = st.text_input("Nombres y Apellidos")
            direccion = st.text_input("Dirección Declarada")
            correo = st.text_input("Correo Electrónico")
        with col2:
            documento = st.text_input("DNI del Titular")
            telefono = st.text_input("Número de Contacto")
            ciudad = st.text_input("Ciudad de Firma", value="Lima")
        contexto = {
            "nombres_apellidos": nombre, "numero_documento": documento,
            "direccion": direccion, "correo_electronico": correo, "numero_telefono": telefono,
            "ciudad": ciudad, "dni_x": "X", "pas_x": " ", "ce_x": " "
        }
    else:
        # PERFIL JURÍDICO (Basado en tu nueva plantilla)
        with col1:
            razon_social = st.text_input("Razón Social (Empresa)")
            ruc = st.text_input("RUC de la Empresa")
            dir_empresa = st.text_input("Dirección de la Empresa")
            ciudad = st.text_input("Ciudad de Firma", value="Lima")
        with col2:
            rep_legal = st.text_input("Representante Legal (Persona)")
            dni_rep = st.text_input("DNI del Representante")
            telefono = st.text_input("Teléfono de Contacto")
            correo = st.text_input("Correo Electrónico")
            
        st.markdown("<hr style='border: 1px solid #001B3D;'>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            partida = st.text_input("Partida N°")
        with col4:
            asiento = st.text_input("Asiento N°")
            
        # Mapeo exacto de llaves para djpersonajuridica.docx.docx
        contexto = {
            "razón_social": razon_social, "numero_ruc": ruc, "dirección": dir_empresa,
            "nombre_persona_natural": rep_legal, "numero_dni": dni_rep,
            "dirección_declarada": dir_empresa, "numero_telefono": telefono,
            "correo_electronico": correo, "ciudad": ciudad, "numero_partida_registral": partida,
            "numero_asiento": asiento, "dni_x": "X", "pas_x": " ", "ce_x": " ",
            "nacionalidad": "PERUANA", "pais": "PERÚ"
        }

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("🚀 GENERAR DOCUMENTO OFICIAL")

# --- LÓGICA DE GENERACIÓN ---
if submit:
    try:
        if categoria == "Contrato de Alianza Comercial":
            archivo = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
        else:
            archivo = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"
        
        doc = DocxTemplate(archivo)
        hoy = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        contexto["fecha_texto"] = f"{hoy.day} de {meses[hoy.month - 1]} de {hoy.year}"
        
        doc.render(contexto)
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        
        st.balloons()
        st.success("✅ ¡Documento generado correctamente!")
        st.download_button(
            label="📥 DESCARGAR ARCHIVO WORD",
            data=output,
            file_name=f"Smart_Security_Doc.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Error: Asegúrate de que {archivo} esté en GitHub.")

st.markdown("<p style='text-align: center; color: white;'>Willy Ríos | Smart Security</p>", unsafe_allow_html=True)

import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Smart Security | Portal", page_icon="💳", layout="centered")

# --- ESTILOS CORPORATIVOS (OCULTA MENÚS SUPERIORES) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');
    
    /* OCULTAR MENÚ DE STREAMLIT Y BARRA SUPERIOR */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .stApp { 
        background: radial-gradient(circle at 20% 30%, #003a85 0%, #001B3D 60%, #FF7F00 130%) !important; 
        background-attachment: fixed; 
    }
    [data-testid="stForm"] { 
        background-color: #FFFFFF !important; 
        border-radius: 20px !important; 
        padding: 25px !important; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.4); 
    }
    [data-testid="stForm"] label p, [data-testid="stForm"] h2, [data-testid="stForm"] h3 { 
        color: #001B3D !important; 
        font-family: 'Montserrat', sans-serif !important; 
        font-weight: 700; 
    }
    [data-testid="stForm"] input { color: #000000 !important; }
    [data-testid="stForm"] button { 
        background-color: #001B3D !important; 
        color: white !important; 
        font-weight: 800; 
        width: 100%; 
        border: 2px solid #FF7F00; 
        border-radius: 12px; 
        padding: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO ---
if os.path.exists("hunter1.png"):
    col_l, col_c, col_r = st.columns([1.5, 1, 1.5])
    with col_c: st.image("hunter1.png", width=150)

# --- SELECTORES ---
c1, c2 = st.columns([1, 1])
with c1:
    categoria = st.selectbox("📂 Tipo de Documento", ["Declaración Jurada", "Contrato de Alianza Comercial"])
with c2:
    tipo_persona = st.radio("👤 Perfil", ["Natural", "Jurídica"], horizontal=True)

# --- FORMULARIO ---
with st.form("form_smart_final_blindado"):
    st.markdown("<h2 style='text-align:center;'>📝 Registro de Información</h2>", unsafe_allow_html=True)
    
    if tipo_persona == "Natural":
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombres y Apellidos")
            direccion = st.text_input("Dirección Declarada")
            correo = st.text_input("Correo Electrónico")
        with col2:
            documento = st.text_input("DNI / CE")
            telefono = st.text_input("Teléfono / Celular")
            ciudad = st.text_input("Ciudad de Firma", value="Lima")
        
        contexto = {
            "nombres_apellidos": nombre, "numero_documento": documento,
            "dirección_declarada": direccion, "numero_telefono": telefono,
            "correo_electronico": correo, "ciudad": ciudad, "dni_x": "X"
        }
    else:
        st.markdown("### 👤 Datos del Representante Legal")
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            rep_legal = st.text_input("Nombres y Apellidos (Representante)")
            dni_rep = st.text_input("DNI del Representante")
        with r1c2:
            correo_rep = st.text_input("Correo Electrónico")
            tel_rep = st.text_input("Teléfono de Contacto")

        st.markdown("<hr style='border: 0.5px solid #001B3D;'>", unsafe_allow_html=True)
        st.markdown("### 🏢 Datos de la Empresa")
        r2c1, r2c2 = st.columns(2)
        with r2c1:
            razon_social = st.text_input("Razón Social")
            ruc = st.text_input("RUC")
            partida = st.text_input("N° de Partida Registral")
        with r2c2:
            direccion_emp = st.text_input("Dirección Fiscal")
            asiento = st.text_input("N° de Asiento")
            ciudad_f = st.text_input("Ciudad de Firma", value="Lima")

        contexto = {
            "nombre_persona_natural": rep_legal,
            "numero_dni": dni_rep,
            "correo_electronico": correo_rep,
            "numero_telefono": tel_rep,
            "razon_social": razon_social,
            "numero_ruc": ruc,
            "dirección": direccion_emp,
            "dirección_declarada": direccion_emp,
            "numero_partida_registral": partida,
            "numero_asiento": asiento,
            "ciudad": ciudad_f,
            "pais": "PERÚ", "nacionalidad": "PERUANA", "dni_x": "X",
            "pas_x": " ", "ce_x": " ", "sol_x": " ", "cas_x": " ", "div_x": " ", "viu_x": " ", "con_x": " "
        }

    submit = st.form_submit_button("🚀 GENERAR DOCUMENTO")

# --- PROCESAMIENTO ---
if submit:
    try:
        archivo = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"
        doc = DocxTemplate(archivo)
        
        hoy = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        contexto["fecha_texto"] = f"{hoy.day} de {meses[hoy.month - 1]} de {hoy.year}"
        
        doc.render(contexto)

        if tipo_persona == "Jurídica":
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if "11641837" in cell.text:
                            cell.text = cell.text.replace("11641837", contexto["numero_partida_registral"])

        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        
        st.balloons() # ¡Globitos listos!
        st.success("✅ ¡Documento generado!")
        
        st.download_button(
            label="📥 DESCARGAR ARCHIVO WORD", 
            data=output, 
            file_name=f"Smart_Security_{tipo_persona}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("<p style='text-align: center; color: white; font-size: 12px; margin-top: 50px;'>Willy Ríos | Smart Security © 2026</p>", unsafe_allow_html=True)

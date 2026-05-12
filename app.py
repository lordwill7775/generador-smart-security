import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Smart Security | Portal", page_icon="💳", layout="centered")

# --- ESTILOS CORPORATIVOS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');
    .stApp { 
        background: radial-gradient(circle at 20% 30%, #003a85 0%, #001B3D 60%, #FF7F00 130%) !important; 
        background-attachment: fixed; 
    }
    [data-testid="stForm"] { 
        background-color: #FFFFFF !important; 
        border-radius: 20px !important; 
        padding: 30px !important; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.4); 
    }
    [data-testid="stForm"] label p, [data-testid="stForm"] h2 { 
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
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO ---
if os.path.exists("hunter1.png"):
    col_l, col_c, col_r = st.columns([1.5, 1, 1.5])
    with col_c: st.image("hunter1.png", width=150)

# --- SELECTORES ---
c1, c2 = st.columns([1.5, 1])
with c1:
    categoria = st.selectbox("📂 Tipo de Documento", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c2:
    tipo_persona = st.radio("👤 Perfil", ["Natural", "Jurídica"], horizontal=True)

# --- FORMULARIO COMPLETO ---
with st.form("form_smart_final"):
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
        # SECCIÓN JURÍDICA COMPLETA
        st.subheader("Datos del Representante Legal")
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            rep_legal = st.text_input("Nombres y Apellidos (Representante)")
            dni_rep = st.text_input("DNI del Representante")
        with row1_col2:
            correo_rep = st.text_input("Correo Electrónico")
            tel_rep = st.text_input("Teléfono de Contacto")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("Datos de la Empresa")
        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            razon_social = st.text_input("Razón Social")
            ruc = st.text_input("RUC")
            partida = st.text_input("N° de Partida")
        with row2_col2:
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
            "sol_x": " ", "cas_x": " ", "div_x": " ", "viu_x": " ", "con_x": " "
        }

    submit = st.form_submit_button("🚀 GENERAR DOCUMENTO")

# --- PROCESAMIENTO ---
if submit:
    try:
        archivo = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx.docx"
        doc = DocxTemplate(archivo)
        
        hoy = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        contexto["fecha_texto"] = f"{hoy.day} de {meses[hoy.month - 1]} de {hoy.year}"
        
        doc.render(contexto)

        # REEMPLAZO FORZADO DE PARTIDA (Si sigue apareciendo el número antiguo)
        if tipo_persona == "Jurídica":
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if "11641837" in cell.text:
                            cell.text = cell.text.replace("11641837", contexto["numero_partida_registral"])

        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        
        st.success("✅ ¡Documento generado!")
        st.download_button(label="📥 DESCARGAR ARCHIVO", data=output, file_name=f"Smart_Security_Doc.docx")
    except Exception as e:
        st.error(f"Error: {e}")

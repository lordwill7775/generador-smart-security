import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Smart Security | Portal", page_icon="💳", layout="centered")

# --- ESTILOS CORPORATIVOS (SMART SECURITY) ---
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
    [data-testid="stForm"] input { 
        color: #000000 !important; 
        background-color: #f0f2f6 !important;
    }
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

st.markdown("<br>", unsafe_allow_html=True)

# --- SELECTORES DE DOCUMENTO ---
c1, c2 = st.columns([1.5, 1])
with c1:
    categoria = st.selectbox("📂 Tipo de Documento", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with c2:
    tipo_persona = st.radio("👤 Perfil del Cliente", ["Natural", "Jurídica"], horizontal=True)

# --- FORMULARIO DE DATOS ---
with st.form("form_registro_smart"):
    st.markdown("<h2 style='text-align:center;'>📝 Registro de Información</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    if tipo_persona == "Natural":
        with col1:
            nombre = st.text_input("Nombres y Apellidos")
            direccion = st.text_input("Dirección Declarada")
        with col2:
            documento = st.text_input("DNI / CE / Pasaporte")
            ciudad_firma = st.text_input("Ciudad de Firma", value="Lima")
        
        contexto = {
            "nombres_apellidos": nombre,
            "numero_documento": documento,
            "dirección_declarada": direccion,
            "ciudad": ciudad_firma,
            "dni_x": "X"
        }
    else:
        # SECCIÓN JURÍDICA: Mapeo exacto para djpersonajuridica.docx.docx
        with col1:
            razon_social = st.text_input("Razón Social (Empresa)")
            ruc = st.text_input("RUC de la Empresa")
            dir_empresa = st.text_input("Dirección Fiscal")
        with col2:
            rep_legal = st.text_input("Representante Legal")
            dni_rep = st.text_input("DNI del Representante")
            partida = st.text_input("N° de Partida Registral")
        
        contexto = {
            "razon_social": razon_social,
            "numero_ruc": ruc,
            "dirección": dir_empresa,
            "nombre_persona_natural": rep_legal,
            "numero_dni": dni_rep,
            "dirección_declarada": dir_empresa, # Se repite para la ficha del representante
            "numero_partida_registral": partida,
            "ciudad": "Lima",
            "pais": "PERÚ",
            "nacionalidad": "PERUANA",
            "dni_x": "X", "sol_x": " ", "cas_x": " ", "div_x": " ", "viu_x": " ", "con_x": " "
        }

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("🚀 GENERAR Y DESCARGAR DOCUMENTO")

# --- LÓGICA DE PROCESAMIENTO ---
if submit:
    try:
        # Selección de archivo base
        if categoria == "Declaración Jurada":
            archivo_base = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx.docx"
        else:
            archivo_base = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
            
        doc = DocxTemplate(archivo_base)
        
        # Fecha automática
        hoy = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        contexto["fecha_texto"] = f"{hoy.day} de {meses[hoy.month - 1]} de {hoy.year}"
        
        # Renderizar datos (llaves {{ }})
        doc.render(contexto)
        
        # REEMPLAZO FORZADO (Solo para Persona Jurídica si el Word tiene el número 11641837 fijo)
        if tipo_persona == "Jurídica":
            # Buscar en párrafos
            for p in doc.paragraphs:
                if "11641837" in p.text:
                    p.text = p.text.replace("11641837", contexto["numero_partida_registral"])
            # Buscar dentro de todas las tablas
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if "11641837" in cell.text:
                            cell.text = cell.text.replace("11641837", contexto["numero_partida_registral"])

        # Guardar en memoria
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        
        st.balloons()
        st.success(f"✅ Documento generado para: {contexto.get('razon_social', contexto.get('nombres_apellidos'))}")
        
        st.download_button(
            label="📥 CLIC AQUÍ PARA DESCARGAR WORD",
            data=output,
            file_name=f"Smart_Security_{hoy.strftime('%Y%m%d')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        st.error(f"Error: Asegúrate de que el archivo '{archivo_base}' esté en tu repositorio de GitHub.")
        st.info(f"Detalle técnico: {e}")

st.markdown("<hr style='border: 0.5px solid #ffffff;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>Willy Ríos | Smart Security © 2026</p>", unsafe_allow_html=True)

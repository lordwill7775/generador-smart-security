import streamlit as st
from docxtpl import DocxTemplate
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Aló Credit | Portal de Documentos", page_icon="💳", layout="wide")

# --- DISEÑO UI PROFESIONAL (CSS AVANZADO) ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background: linear-gradient(180deg, #f0f2f6 0%, #ffffff 100%);
    }
    
    /* Contenedor del Logo y Título */
    .header-container {
        display: flex;
        align-items: center;
        padding: 20px;
        background-color: #001B3D;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Títulos Principales */
    h1 {
        color: #00E5FF !important;
        font-family: 'Trebuchet MS', sans-serif;
        margin-left: 20px !important;
    }
    
    /* Hacer que los recuadros de texto sean VISIBLES siempre */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border: 2px solid #001B3D !important; /* Bordes oscuros siempre visibles */
        border-radius: 8px !important;
        background-color: white !important;
        color: #001B3D !important;
    }
    
    /* Estilo para los botones */
    .stButton>button {
        background: linear-gradient(90deg, #001B3D 0%, #003a85 100%) !important;
        color: white !important;
        border: 2px solid #00E5FF !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        padding: 15px 30px !important;
        font-size: 18px !important;
        width: 100%;
        box-shadow: 0px 4px 10px rgba(0,229,255,0.2);
    }
    
    .stButton>button:hover {
        background: #00E5FF !important;
        color: #001B3D !important;
        transform: scale(1.02);
        transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO VISIBLE ---
with st.container():
    col_l, col_t = st.columns([1, 4])
    with col_l:
        # Buscamos el logo. Si no aparece, pondrá un texto de aviso
        if os.path.exists("hunter.png"):
            st.image("hunter.png", width=160)
        else:
            st.warning("⚠️ Sube 'hunter.png' a GitHub")
    with col_t:
        st.markdown("<h1>Portal de Gestión Documental</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:white; margin-left:25px;'>Generación Automática de Contratos y Declaraciones</p>", unsafe_allow_html=True)

st.write("---")

# --- MENÚ DE SELECCIÓN ---
col_a, col_b = st.columns(2)
with col_a:
    categoria = st.selectbox("📁 Documento a generar:", ["Contrato de Alianza Comercial", "Declaración Jurada"])
with col_b:
    tipo_persona = st.radio("👤 Perfil del Cliente:", ["Natural", "Jurídica"], horizontal=True)

# Lógica de archivos
if categoria == "Contrato de Alianza Comercial":
    archivo_word = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
else:
    archivo_word = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"

# --- FORMULARIO CREATIVO ---
with st.form("main_form"):
    st.markdown(f"<h3 style='color:#001B3D;'>📝 Completar información para {tipo_persona}</h3>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        nombre = st.text_input("Nombre Completo o Razón Social", placeholder="Ej: Juan Perez o Aló Credit S.A.C.")
        documento = st.text_input("Número de DNI o RUC", placeholder="8 o 11 dígitos")
        correo = st.text_input("Correo Electrónico de contacto")
    with c2:
        direccion = st.text_input("Dirección Domiciliaria / Fiscal")
        telefono = st.text_input("Teléfono / Celular")
        ciudad = st.text_input("Ciudad / Oficina Registral", value="Lima")
    
    # Campos para Jurídica
    rep_legal, dni_rep, partida, asiento = "", "", "", ""
    if tipo_persona == "Jurídica":
        st.markdown("<div style='background-color:#001B3D; padding:10px; border-radius:10px; color:white; margin:15px 0;'>Representación Legal</div>", unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            rep_legal = st.text_input("Nombre del Representante")
            dni_rep = st.text_input("DNI del Representante")
        with cy:
            partida = st.text_input("Partida Registral N°")
            asiento = st.text_input("Asiento N°")

    st.markdown("<br>", unsafe_allow_html=True)
    enviar = st.form_submit_button("✨ GENERAR DOCUMENTO OFICIAL")

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
        st.success(f"🎊 ¡Documento de {nombre} listo para descargar!")
        st.download_button(
            label="📥 DESCARGAR ARCHIVO EDITABLE",
            data=output.getvalue(),
            file_name=f"Documento_{nombre}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"❌ Error: El archivo '{archivo_word}' no se encuentra en GitHub o tiene errores.")

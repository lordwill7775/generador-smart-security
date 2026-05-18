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
    
    /* OCULTAR MENÚS DE STREAMLIT */
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
    @media (max-width: 640px) {
        [data-testid="stForm"] { padding: 15px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO ---
if os.path.exists("hunter1.png"):
    col_l, col_c, col_r = st.columns([1.5, 1, 1.5])
    with col_c: st.image("hunter1.png", width=150)

# --- SELECTORES PRINCIPALES ---
c1, c2 = st.columns([1, 1])
with c1:
    categoria = st.selectbox("📂 Tipo de Documento", ["Declaración Jurada", "Contrato de Alianza Comercial"])
with c2:
    tipo_persona = st.radio("👤 Perfil", ["Natural", "Jurídica"], horizontal=True)

# --- FORMULARIO DE REGISTRO ---
with st.form("form_smart_security_v10"):
    st.markdown("<h2 style='text-align:center;'>📝 Registro de Información</h2>", unsafe_allow_html=True)
    
    if tipo_persona == "Natural":
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombres y Apellidos")
            direccion = st.text_input("Dirección / Domicilio Declarado")
            correo = st.text_input("Correo Electrónico")
            pais = st.text_input("País de Origen/Residencia", value="PERÚ")
        with col2:
            documento = st.text_input("DNI / CE")
            # Añadimos RUC opcional en Persona Natural por si se genera el contrato
            ruc_natural = st.text_input("RUC (Opcional, solo para Contrato)")
            telefono = st.text_input("Teléfono / Celular")
            ciudad = st.text_input("Ciudad de Firma", value="Lima")
        
        # Mapeo inteligente según el documento elegido para Persona Natural
        if categoria == "Declaración Jurada":
            contexto = {
                "nombres_apellidos": nombre, 
                "numero_documento": documento,
                "dirección_declarada": direccion, 
                "numero_telefono": telefono,
                "correo_electronico": correo, 
                "ciudad": ciudad, 
                "pais": pais,
                "dni_x": "X"
            }
        else:
            # Llaves exactas para 'contratonatural.docx' basándonos en tu captura
            contexto = {
                "nombre_persona_natural": nombre,
                "direccion": direccion,
                "numero_ruc": ruc_natural,
                "numero_dni": documento,
                "ciudad": ciudad,
                "pais": pais
            }
            
        nombre_para_archivo = nombre.replace(" ", "_") if nombre else "Natural"
        
    else:
        # SECCIÓN JURÍDICA
        st.markdown("### 👤 Datos del Representante Legal")
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            rep_legal = st.text_input("Nombres y Apellidos (Representante)")
            dni_rep = st.text_input("DNI del Representante")
            fecha_nac_rep = st.text_input("Fecha de Nacimiento (DD/MM/AAAA)")
        with r1c2:
            nacionalidad_rep = st.text_input("Nacionalidad", value="PERUANA")
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
            "fecha_texto_nacimiento": fecha_nac_rep,
            "nacionalidad": nacionalidad_rep,
            "correo_electronico": correo_rep,
            "numero_telefono": tel_rep,
            "razon_social": razon_social,
            "numero_ruc": ruc,
            "dirección": direccion_emp,
            "dirección_declarada": direccion_emp,
            "numero_partida_registral": partida,
            "numero_asiento": asiento,
            "ciudad": city_f if 'city_f' in locals() else ciudad_f,
            "pais": "PERÚ", "dni_x": "X",
            "pas_x": " ", "ce_x": " ", "sol_x": " ", "cas_x": " ", "div_x": " ", "viu_x": " ", "con_x": " "
        }
        nombre_para_archivo = razon_social.replace(" ", "_") if razon_social else "Juridica"

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("🚀 GENERAR DOCUMENTO OFICIAL")

# --- LÓGICA DE PROCESAMIENTO ---
if submit:
    try:
        # Selección correcta del archivo en base a las opciones
        if categoria == "Declaración Jurada":
            archivo = "Djnatural.docx" if tipo_persona == "Natural" else "djpersonajuridica.docx"
        else:
            archivo = "contratonatural.docx" if tipo_persona == "Natural" else "contratojuridica.docx"
            
        doc = DocxTemplate(archivo)
        
        # Inyección de la fecha actual en formato texto
        hoy = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        contexto["fecha_texto"] = f"{hoy.day} de {meses[hoy.month - 1]} de {hoy.year}"
        
        # Renderizado de datos final
        doc.render(contexto)

        # Reemplazo forzado para corregir la partida fija en Persona Jurídica
        if tipo_persona == "Jurídica":
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if "11641837" in cell.text:
                            cell.text = cell.text.replace("11641837", contexto["numero_partida_registral"])

        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        
        st.balloons()
        st.success("✅ ¡Documento estructurado y generado con éxito!")
        
        tipo_doc_nombre = "DJ" if categoria == "Declaración Jurada" else "Contrato"
        
        st.download_button(
            label="📥 CLIC AQUÍ PARA DESCARGAR WORD", 
            data=output, 
            file_name=f"{tipo_doc_nombre}_{nombre_para_archivo}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Error: Asegúrate de que '{archivo}' esté subido correctamente a tu GitHub.")
        st.info(f"Detalle técnico: {e}")

st.markdown("<p style='text-align: center; color: white; font-size: 12px; margin-top: 50px;'>Willy Ríos | Smart Security © 2026</p>", unsafe_allow_html=True)

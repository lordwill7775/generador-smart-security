import streamlit as st
from docxtpl import DocxTemplate
import io
import os
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Smart Security | Portal", page_icon="💳", layout="centered")

# --- ESTILOS CORPORATIVOS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght=700&display=swap');
    
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

# --- SELECTOR PRINCIPALES ---
categoria = st.selectbox("📂 Tipo de Documento", ["Declaración Jurada", "Contrato de Alianza Comercial", "Formato Creación Usuarios"])

# Solo mostrar perfil Natural/Jurídica para las opciones antiguas
if categoria != "Formato Creación Usuarios":
    tipo_persona = st.radio("👤 Perfil", ["Natural", "Jurídica"], horizontal=True)

# --- FORMULARIO DE REGISTRO ---
with st.form("form_smart_security_v21"):
    st.markdown("<h2 style='text-align:center;'>📝 Registro de Información</h2>", unsafe_allow_html=True)
    
    # -------------------------------------------------------------------------
    # CASO NUEVO: FORMULARIO EXCLUSIVO PARA EXCEL DE CREACIÓN DE USUARIOS
    # -------------------------------------------------------------------------
    if categoria == "Formato Creación Usuarios":
        st.markdown("### 🏢 Datos Generales de la Empresa")
        col1, col2 = st.columns(2)
        with col1:
            rep_legal = st.text_input("Nombre del Representante Legal")
            razon_social = st.text_input("Nombre de Tienda / Razón Social")
            ruc = st.text_input("RUC")
            correo = st.text_input("Correo Electrónico")
        with col2:
            telefono1 = st.text_input("Número Celular 1")
            telefono2 = st.text_input("Número Celular 2")
            banco = st.text_input("Banco (ej. BBVA, BCP)")
            tipo_cuenta = st.text_input("Tipo de Cuenta", value="AHORROS")
            n_cuenta = st.text_input("Número de Cuenta + CCI")

        st.markdown("<hr style='border: 0.5px solid #001B3D;'>", unsafe_allow_html=True)
        st.markdown("### 📍 Relación de Tiendas")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("**Tienda 1**")
            t1_nom = st.text_input("Nombre Tienda 1")
            t1_dir = st.text_input("Dirección Tienda 1")
            t1_dep = st.text_input("Departamento Tienda 1", value="LIMA")
            t1_ciu = st.text_input("Ciudad / Distrito Tienda 1")
        with col_t2:
            st.markdown("**Tienda 2 (Opcional)**")
            t2_nom = st.text_input("Nombre Tienda 2")
            t2_dir = st.text_input("Dirección Tienda 2")
            t2_dep = st.text_input("Departamento Tienda 2", value="LIMA")
            t2_ciu = st.text_input("Ciudad / Distrito Tienda 2")

        st.markdown("<hr style='border: 0.5px solid #001B3D;'>", unsafe_allow_html=True)
        st.markdown("### 👥 Relación de Usuarios / Vendedores")
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.markdown("**Vendedor 1**")
            v1_tnd = st.text_input("Tienda Asignada Vendedor 1")
            v1_nom = st.text_input("Nombre Completo Vendedor 1")
            v1_crr = st.text_input("Correo Vendedor 1")
            v1_cel = st.text_input("Celular Vendedor 1")
        with col_v2:
            st.markdown("**Vendedor 2 (Opcional)**")
            v2_tnd = st.text_input("Tienda Asignada Vendedor 2")
            v2_nom = st.text_input("Nombre Completo Vendedor 2")
            v2_crr = st.text_input("Correo Vendedor 2")
            v2_cel = st.text_input("Celular Vendedor 2")

        nombre_para_archivo = razon_social.replace(" ", "_") if razon_social else "Usuarios"

    # -------------------------------------------------------------------------
    # CASO ANTERIOR: PERSONA NATURAL (INALTERADO)
    # -------------------------------------------------------------------------
    elif tipo_persona == "Natural":
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombres y Apellidos")
            direccion = st.text_input("Dirección / Domicilio Declarado")
            correo = st.text_input("Correo Electrónico")
            pais = st.text_input("País de Origen/Residencia", value="PERÚ")
        with col2:
            documento = st.text_input("DNI / CE")
            ruc_natural = st.text_input("RUC (Opcional, necesario para Contrato)")
            telefono = st.text_input("Teléfono / Celular")
            ciudad = st.text_input("Ciudad de Firma", value="Lima")
        
        if categoria == "Declaración Jurada":
            contexto = {
                "nombres_apellidos": nombre, 
                "numero_documento": documento,
                "dirección_declarada": direccion,    
                "direccion_declarada": direccion,     
                "dirección": direccion,               
                "direccion": direccion,                
                "numero_telefono": telefono,
                "telefono": telefono,
                "correo_electronico": correo, 
                "ciudad": ciudad, 
                "pais": pais,
                "dni_x": "X"
            }
        else:
            contexto = {
                "nombre_persona_natural": nombre,
                "direccion": direccion,
                "dirección": direccion,
                "dirección_declarada": direccion,
                "direccion_declarada": direccion,
                "numero_ruc": ruc_natural,
                "numero_dni": documento,
                "numero_telefono": telefono,       
                "telefono": telefono,
                "correo_electronico": correo,     
                "ciudad": ciudad,
                "pais": pais
            }
            
        datos_excel = {
            "Fecha Registro": [datetime.now().strftime("%d/%m/%Y")],
            "Tipo Documento": [categoria],
            "Perfil": ["Natural"],
            "Nombre / Razón Social": [nombre],
            "DNI / CE": [documento],
            "RUC": [ruc_natural],
            "Dirección": [direccion],
            "Teléfono": [telefono],
            "Correo": [correo],
            "Ciudad": [ciudad]
        }
        nombre_para_archivo = nombre.replace(" ", "_") if nombre else "Natural"
        
    # -------------------------------------------------------------------------
    # CASO ANTERIOR: PERSONA JURÍDICA (INALTERADO)
    # -------------------------------------------------------------------------
    else:
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
            "telefono": tel_rep,                   
            "razon_social": razon_social,          
            "numero_ruc": ruc,                     
            "dirección": direccion_emp,             
            "direccion": direccion_emp,              
            "dirección_declarada": direccion_emp,
            "direccion_declarada": direccion_emp,
            "numero_partida_registral": partida,
            "numero_asiento": asiento,
            "ciudad": ciudad_f,                    
            "pais": "PERÚ",                        
            "dni_x": "X",
            "pas_x": " ", "ce_x": " ", "sol_x": " ", "cas_x": " ", "div_x": " ", "viu_x": " ", "con_x": " "
        }
        
        datos_excel = {
            "Fecha Registro": [datetime.now().strftime("%d/%m/%Y")],
            "Tipo Documento": [categoria],
            "Perfil": ["Jurídica"],
            "Nombre / Razón Social": [razon_social],
            "DNI / CE": [dni_rep],
            "RUC": [ruc],
            "Dirección": [direccion_emp],
            "Teléfono": [tel_rep],
            "Correo": [correo_rep],
            "Ciudad": [ciudad_f],
            "Representante Legal": [rep_legal],
            "Partida Registral": [partida],
            "Asiento": [asiento]
        }
        nombre_para_archivo = razon_social.replace(" ", "_") if razon_social else "Juridica"

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("🚀 GENERAR DOCUMENTO OFICIAL")

# --- LÓGICA DE PROCESAMIENTO ---
if submit:
    try:
        # -------------------------------------------------------------------------
        # PROCESAMIENTO EXCLUSIVO: GENERACIÓN DEL EXCEL DE CREACIÓN DE USUARIOS
        # -------------------------------------------------------------------------
        if categoria == "Formato Creación Usuarios":
            output_excel = io.BytesIO()
            
            # Recreación de las filas en blanco y estructura exacta de tu plantilla
            filas_excel = [
                ["", "FORMATO CREACION USUARIOS", "", "", ""],
                ["", "", "", "", ""],
                ["", "", "", "", ""],
                ["", "", "", "", ""],
                ["", "", "", "", ""],
                ["", "", "", "", ""],
                ["", "", "", "", ""],
                ["", "NOMBRE DE  REPRESENTANTE LEGAL:", rep_legal.upper(), "", ""],
                ["", "NOMBRE DE TIENDA:", razon_social.upper(), "", ""],
                ["", "RUC:", ruc, "", ""],
                ["", "CORREO:", correo, "", ""],
                ["", "NUMERO CELULAR 1:", telefono1, "", ""],
                ["", "NUMERO CELULAR 2:", telefono2, "", ""],
                ["", "BANCO:", banco.upper(), "", ""],
                ["", "TIPO DE CUENTA:", tipo_cuenta.upper(), "", ""],
                ["", "NUMERO DE CUENTA:", n_cuenta, "", ""],
                ["", "", "", "", ""],
                ["", "Relacione cada tienda:", "", "", ""],
                ["", "", "", "", ""],
                ["", "", "", "", ""],

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

# --- SELECTOR PRINCIPAL ---
categoria = st.selectbox("📂 Tipo de Documento", ["Declaración Jurada", "Contrato de Alianza Comercial", "Formato Creación Usuarios"])

# =========================================================================
# VISTA 1: FORMULARIO EXCLUSIVO PARA EXCEL DE CREACIÓN DE USUARIOS
# =========================================================================
if categoria == "Formato Creación Usuarios":
    with st.form("form_creacion_usuarios"):
        st.markdown("<h2 style='text-align:center;'>📝 Registro de Usuarios</h2>", unsafe_allow_html=True)
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

        st.markdown("<br>", unsafe_allow_html=True)
        submit_u = st.form_submit_button("🚀 GENERAR EXCEL DE USUARIOS")

    if submit_u:
        try:
            output_excel = io.BytesIO()
            filas_excel = [
                ["", "FORMATO CREACION USUARIOS", "", "", ""],
                ["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""],
                ["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""],
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
                ["", "", "", "", ""], ["", "", "", "", ""],
                ["", "NOMBRE TIENDA", "DIRECCION", "DEPARTAMENTO", "CIUDAD"]
            ]
            
            if t1_nom:
                filas_excel.append(["", t1_nom.upper(), t1_dir.upper(), t1_dep.upper(), t1_ciu.upper()])
            if t2_nom:
                filas_excel.append(["", t2_nom.upper(), t2_dir.upper(), t2_dep.upper(), t2_ciu.upper()])
                
            filas_excel.extend([
                ["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""],
                ["", "Relacione aquí cada de usuario con su tienda asignada:", "", "", ""],
                ["", "", "", "", ""],
                ["", "NOMBRE TIENDA", "NOMBRE VENDEDOR", "CORREO", "CELULAR"]
            ])
            
            if v1_nom:
                filas_excel.append(["", v1_tnd.upper(), v1_nom.upper(), v1_crr, v1_cel])
            if v2_nom:
                filas_excel.append(["", v2_tnd.upper(), v2_nom.upper(), v2_crr, v2_cel])
                
            df_usuarios = pd.DataFrame(filas_excel)
            with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
                df_usuarios.to_excel(writer, index=False, header=False, sheet_name="ORIENTE SMART")
            output_excel.seek(0)
            
            st.balloons()
            st.success("✅ ¡Formato de Creación de Usuarios generado con éxito!")
            nombre_file = razon_social.replace(" ", "_") if razon_social else "Usuarios"
            st.download_button(
                label="📊 DESCARGAR EXCEL DE USUARIOS", 
                data=output_excel, 
                file_name=f"Usuarios_{nombre_file}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Ocurrió un error al armar el Excel: {e}")

# =========================================================================
# VISTA 2: FORMULARIOS ANTERIORES (CONTRATOS Y DJ TRADICIONALES)
# =========================================================================
else:
    tipo_persona = st.radio("👤 Perfil", ["Natural", "Jurídica"], horizontal=True)
    
    with st.form("form_documentos_tradicionales"):
        st.markdown("<h2 style='text-align:center;'>📝 Registro de Información</h2>", unsafe_allow_html=True)
        
        # --- SUB-FORMULARIO: PERSONA NATURAL ---
        if tipo_persona == "Natural":
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
                
        # --- SUB-FORMULARIO: PERSONA JURÍDICA ---
        else:
            st.markdown("### 👤 Datos del Representante Legal")
            r1c1, r1c2 = st.columns(2)
            with r1c1:
                rep_legal_old = st.text_input("Nombres y Apellidos (Representante)")
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
                razon_social_old = st.text_input("Razón Social")
                ruc_old = st.text_input("RUC")
                partida = st.text_input("N° de Partida Registral")
            with r2c2:
                direccion_emp = st.text_input("Dirección Fiscal")
                asiento = st.text_input("N° de Asiento")
                ciudad_f = st.text_input("Ciudad de Firma", value="Lima")

        st.markdown("<br>", unsafe_allow_html=True)
        submit_doc = st.form_submit_button("🚀 GENERAR DOCUMENTO OFICIAL")

    if submit_doc:
        try:
            contexto = {}
            datos_excel = {}
            nombre_para_archivo = "Documento"
            
            if tipo_persona == "Natural":
                if categoria == "Declaración Jurada":
                    contexto = {
                        "nombres_apellidos": nombre, "numero_documento": documento,
                        "dirección_declarada": direccion, "direccion_declarada": direccion,     
                        "dirección": direccion, "direccion": direccion,                
                        "numero_telefono": telefono, "telefono": telefono,
                        "correo_electronico": correo, "ciudad": ciudad, "pais": pais, "dni_x": "X"
                    }
                else:
                    contexto = {
                        "nombre_persona_natural": nombre, "direccion": direccion, "dirección": direccion,
                        "dirección_declarada":

import streamlit as st
import cloudinary
import cloudinary.api
import os

# --- CONFIGURACIÓN DE SEGURIDAD (Tus llaves reales) ---
cloudinary.config( 
  cloud_name = "detprbdvv", 
  api_key = "487844675958599", 
  api_secret = "lF9Z48IBN6JlGNvLzjuF1Osmgm8",
  secure = True
)

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="MAYNEXUS CLOUD",
    page_icon="☁️",
    layout="centered"
)

# --- ESTILO PERSONALIZADO (Dark Mode Industrial) ---
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stSelectbox label { color: #00ff99 !important; font-weight: bold; }
    h1 { color: #00ff99; text-align: center; border-bottom: 2px solid #00ff99; padding-bottom: 10px; }
    .stAudio { background-color: #111; border-radius: 20px; padding: 5px; }
    </style>
    """, unsafe_allow_headers=True)

st.title("MAYNEXUS CLOUD ☁️")

# --- SELECTOR DE GÉNERO ---
# Estos nombres deben coincidir con tus carpetas en Cloudinary
opciones_genero = [
    "corridos tumbados", 
    "Regueton", 
    "bandas", 
    "cristianas", 
    "pop latino"
]

genero_seleccionado = st.selectbox("📥 SELECCIONA TU CANAL:", opciones_genero)

st.markdown("---")

# --- MOTOR DE BÚSQUEDA EN LA NUBE ---
def cargar_musica(folder):
    try:
        # Buscamos archivos tipo 'video' (que incluye audio) en la carpeta específica
        res = cloudinary.api.resources(
            type="upload", 
            prefix=folder, 
            resource_type="video",
            max_results=50
        )
        return res.get('resources', [])
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return []

# --- REPRODUCTOR ---
lista_canciones = cargar_musica(genero_seleccionado)

if not lista_canciones:
    st.info(f"Aún no hay canciones en la carpeta '{genero_seleccionado}'. ¡Sube una desde la Lenovo!")
else:
    st.success(f"Se encontraron {len(lista_canciones)} canciones.")
    
    for cancion in lista_canciones:
        # Limpiamos el nombre para quitar la carpeta y la extensión
        nombre_archivo = cancion['public_id'].split('/')[-1]
        
        with st.container():
            st.write(f"🎵 **{nombre_archivo}**")
            st.audio(cancion['secure_url'])
            st.markdown("---")

st.caption("MAYNEXUS v1.0 | Ingeniería Industrial Aplicada")

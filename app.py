import streamlit as st
import cloudinary
import cloudinary.api

# --- CONFIGURACIÓN DE CONEXIÓN ---
cloudinary.config( 
  cloud_name = "detprbdvv", 
  api_key = "487844675958599", 
  api_secret = "lF9Z48IBN6JlGNvLzjuF1Osmgm8",
  secure = True
)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="MAYNEXUS CLOUD", page_icon="🎵", layout="wide")

# Diseño Industrial Dark Mode
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ff99; }
    .stSelectbox label { color: #00ff99 !important; font-size: 18px; font-weight: bold; }
    h1 { text-align: center; color: #00ff99; text-shadow: 2px 2px #000; border-bottom: 2px solid #00ff99; }
    .song-card {
        background-color: #111;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #00ff99;
        margin-bottom: 20px;
        text-align: center;
    }
    img { border-radius: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("MAYNEXUS CLOUD ☁️🎵")

# --- SELECTOR DE CARPETAS (Actualizado según tu Cloudinary) ---
opciones = [
    "corridos tumbados", 
    "bandas", 
    "Regueton", 
    "cristianas", 
    "pop latino", 
    "pop en español", 
    "pop en ingles", 
    "trance", 
    "las mas sonadas"
]

genero_elegido = st.selectbox("📂 SELECCIONA TU BIBLIOTECA:", opciones)

st.markdown("---")

# --- BOTÓN DE SINCRONIZACIÓN ---
if st.button("🔄 ACTUALIZAR Y CARGAR MÚSICA"):
    try:
        with st.spinner(f"Accediendo a la carpeta '{genero_elegido}'..."):
            
            # 1. Buscamos todas las IMÁGENES de la carpeta
            res_img = cloudinary.api.resources(
                type="upload", 
                prefix=genero_elegido, 
                resource_type="image", 
                max_results=200
            )
            # Diccionario para emparejar foto con audio por nombre
            mapa_portadas = {img['public_id'].split('/')[-1]: img['secure_url'] for img in res_img.get('resources', [])}

            # 2. Buscamos todos los AUDIOS de la carpeta
            res_audio = cloudinary.api.resources(
                type="upload", 
                prefix=genero_elegido, 
                resource_type="video", 
                max_results=200
            )
            
            canciones = res_audio.get('resources', [])

            if not canciones:
                st.warning(f"No se encontraron archivos en la carpeta '{genero_elegido}'.")
            else:
                st.success(f"¡Se cargaron {len(canciones)} canciones exitosamente!")
                
                # Mostramos en 2 columnas para que parezca app de streaming
                cols = st.columns(2)
                for i, cancion in enumerate(canciones):
                    with cols[i % 2]:
                        nombre_id = cancion['public_id'].split('/')[-1]
                        
                        # Buscamos la portada; si no hay, usamos una por defecto
                        url_foto = mapa_portadas.get(nombre_id, "https://via.placeholder.com/500x500.png?text=MAYNEXUS+MUSIC")
                        
                        st.markdown('<div class="song-card">', unsafe_allow_html=True)
                        st.image(url_foto, use_column_width=True)
                        st.markdown(f"### 🎧 {nombre_id}")
                        st.audio(cancion['secure_url'])
                        st.markdown('</div>', unsafe_allow_html=True)
                        
    except Exception as e:
        st.error(f"Error de conexión con Cloudinary: {e}")

st.sidebar.markdown("---")
st.sidebar.info(f"**Usuario:** Mynor Vazquez\n\n**Proyecto:** MAYNEXUS v1.7\n\n**Estado:** 100% Nube")

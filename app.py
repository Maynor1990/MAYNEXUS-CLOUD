import streamlit as st
import cloudinary
import cloudinary.api

# --- CONFIGURACIÓN DE TUS LLAVES ---
cloudinary.config( 
  cloud_name = "detprbdvv", 
  api_key = "487844675958599", 
  api_secret = "lF9Z48IBN6JlGNvLzjuF1Osmgm8",
  secure = True
)

# --- ESTO REEMPLAZA AL HTML (Diseño Visual) ---
st.set_page_config(page_title="MAYNEXUS CLOUD", page_icon="☁️")

st.markdown("""
    <style>
    /* Fondo negro y letras verdes estilo industrial */
    .stApp { background-color: #000000; color: #00ff99; }
    h1 { color: #00ff99; text-align: center; border-bottom: 2px solid #00ff99; }
    .stAudio { background-color: #111; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("MAYNEXUS CLOUD ☁️")
st.write("Bienvenido, Mynor. Selecciona tu estación:")

# --- LISTA DE TUS CARPETAS EN CLOUDINARY ---
genero = st.selectbox("", ["corridos tumbados", "Regueton", "bandas", "cristianas", "pop latino"])

if st.button("🎵 ACTUALIZAR REPRODUCTOR"):
    # Buscamos los archivos en la nube
    try:
        recursos = cloudinary.api.resources(type="upload", prefix=genero, resource_type="video")
        
        if not recursos['resources']:
            st.warning("No hay música en esta carpeta todavía.")
        else:
            for cancion in recursos['resources']:
                # Mostramos el nombre y el reproductor
                nombre = cancion['public_id'].split('/')[-1]
                st.markdown(f"### 🎧 {nombre}")
                st.audio(cancion['secure_url'])
                st.markdown("---")
    except Exception as e:
        st.error(f"Error al conectar con la nube: {e}")

st.caption("MAYNEXUS v1.0 | Sin túneles, 100% Nube")

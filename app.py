import streamlit as st
import cloudinary
import cloudinary.api
import random

# --- CONFIGURACIÓN ---
cloudinary.config( 
  cloud_name = "detprbdvv", 
  api_key = "487844675958599", 
  api_secret = "lF9Z48IBN6JlGNvLzjuF1Osmgm8",
  secure = True
)

st.set_page_config(page_title="MAYNEXUS TURBO", layout="wide")

# --- CSS OPTIMIZADO (Menos animaciones pesadas) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .turbo-line {
        height: 4px; width: 100%;
        background: linear-gradient(90deg, #00ff99, #0066ff, #00ff99);
        background-size: 200% 100%;
        animation: wave 3s linear infinite;
        margin-bottom: 20px;
    }
    @keyframes wave { 0% {background-position:0%} 100% {background-position:100%} }
    .song-card { background: #0a0a0a; border-radius: 12px; padding: 10px; border: 1px solid #1a1a1a; }
    .cover-art { width: 100%; aspect-ratio: 1/1; border-radius: 8px; object-fit: cover; }
    </style>
    <div class="turbo-line"></div>
    """, unsafe_allow_html=True)

# --- FUNCIÓN CON CACHÉ (ESTO EVITA QUE SE TRABE) ---
@st.cache_data(ttl=600)  # Guarda la lista por 10 minutos
def cargar_biblioteca_global():
    try:
        # Traer audios
        res_audio = cloudinary.api.resources(resource_type="video", max_results=500)
        audios = res_audio.get('resources', [])
        # Traer imágenes
        res_img = cloudinary.api.resources(resource_type="image", max_results=500)
        imagenes = {img['public_id'].split('/')[-1]: img['secure_url'] for img in res_img.get('resources', [])}
        return audios, imagenes
    except:
        return [], {}

# --- LÓGICA PRINCIPAL ---
audios, imagenes = cargar_biblioteca_global()

with st.sidebar:
    st.title("MAYNEXUS ⚡")
    st.subheader("Control de Flujo")
    if st.button("🚀 LIMPIAR CACHÉ (Nuevas descargas)"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("---")
    st.caption(f"Archivos en sistema: {len(audios)}")

# BUSCADOR (Ahora es instantáneo porque busca en la lista local)
query = st.text_input("🔍 Busca artista o canción (Peso Pluma, Sad, etc)...", "").lower()

if audios:
    # Filtrado ultra-rápido en memoria
    if query:
        resultados = [c for c in audios if query in c['public_id'].lower()]
    else:
        # Si no hay búsqueda, solo mostramos 20 al azar para no saturar
        resultados = audios[:25]

    st.write(f"Resultados: {len(resultados)}")
    
    cols = st.columns(5)
    for i, cancion in enumerate(resultados):
        with cols[i % 5]:
            nombre = cancion['public_id'].split('/')[-1]
            foto = imagenes.get(nombre, "https://via.placeholder.com/300/111/00ff99?text=♫")
            
            st.markdown(f'''
                <div class="song-card">
                    <img src="{foto}" class="cover-art">
                    <p style="font-size:11px; font-weight:bold; height:25px; overflow:hidden;">{nombre[:35]}</p>
                </div>
            ''', unsafe_allow_html=True)
            st.audio(cancion['secure_url'])
else:
    st.warning("Iniciando sistema... si no ves nada, dale al botón de 'Limpiar Caché'.")

import streamlit as st
import cloudinary
import cloudinary.api
import random

# --- CONFIGURACIÓN CLOUDINARY ---
cloudinary.config( 
  cloud_name = "detprbdvv", 
  api_key = "487844675958599", 
  api_secret = "lF9Z48IBN6JlGNvLzjuF1Osmgm8",
  secure = True
)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="MAYNEXUS GLOBAL", page_icon="🔍", layout="wide")

# --- CSS: INTERFAZ MINIMALISTA CON ONDA ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Onda de Colores Superior */
    .nexus-wave {
        height: 8px; width: 100%;
        background: linear-gradient(90deg, #00ff99, #0066ff, #ff0055, #00ff99);
        background-size: 200% 100%;
        animation: wave 5s linear infinite;
        border-radius: 10px; margin-bottom: 25px;
    }
    @keyframes wave { 0% {background-position:0%} 100% {background-position:100%} }

    /* Tarjetas de Canción */
    .song-card {
        background: #0d0d0d;
        border-radius: 15px;
        padding: 12px;
        text-align: center;
        border: 1px solid #1a1a1a;
        transition: 0.3s;
    }
    .song-card:hover { border-color: #00ff99; transform: scale(1.03); }
    .cover-art { width: 100%; aspect-ratio: 1/1; border-radius: 10px; object-fit: cover; }
    
    /* Buscador Estilizado */
    .stTextInput > div > div > input {
        background-color: #111 !important;
        color: #00ff99 !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
    }
    </style>
    <div class="nexus-wave"></div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("MAYNEXUS ⚡")
    st.markdown("### MODO GLOBAL")
    st.info("Ahora todos tus archivos se cargan juntos. Usa el buscador para filtrar por artista o género.")
    shuffle = st.toggle("🔀 MODO ALEATORIO", value=True)
    if st.button("🔄 REFRESCAR BIBLIOTECA"):
        st.cache_data.clear()
    st.markdown("---")
    st.caption("Operador: Maynor Vazquez")

# --- BUSCADOR PRINCIPAL ---
query = st.text_input("🔍 Busca por nombre, artista o género (ej: Corridos, Travis, Regueton)...", "").lower()

# --- CARGA DE DATOS SIN CARPETAS ---
try:
    with st.spinner("Sincronizando biblioteca global..."):
        # 1. Traer todas las imágenes (portadas)
        res_img = cloudinary.api.resources(resource_type="image", max_results=500)
        mapa_portadas = {img['public_id'].split('/')[-1]: img['secure_url'] for img in res_img.get('resources', [])}

        # 2. Traer todos los audios (sin prefix de carpeta)
        res_audio = cloudinary.api.resources(resource_type="video", max_results=500)
        todas_las_canciones = res_audio.get('resources', [])

    # FILTRADO POR BUSCADOR
    if query:
        canciones = [c for c in todas_las_canciones if query in c['public_id'].lower()]
    else:
        canciones = todas_las_canciones

    # APLICAR SHUFFLE
    if shuffle and not query:
        random.shuffle(canciones)

    # RENDERIZADO
    if canciones:
        st.write(f"Mostrando {len(canciones)} resultados")
        cols = st.columns(5)
        for i, cancion in enumerate(canciones):
            with cols[i % 5]:
                # Limpiar nombre para mostrar
                nombre_raw = cancion['public_id'].split('/')[-1]
                foto = mapa_portadas.get(nombre_raw, "https://via.placeholder.com/300/111/00ff99?text=♫")
                
                st.markdown(f'''
                    <div class="song-card">
                        <img src="{foto}" class="cover-art">
                        <div style="font-size:13px; font-weight:600; height:35px; overflow:hidden; margin-top:8px;">{nombre_raw}</div>
                    </div>
                ''', unsafe_allow_html=True)
                st.audio(cancion['secure_url'])
    else:
        st.warning("No se encontró nada con esa búsqueda.")

except Exception as e:
    st.error(f"Error de conexión: {e}")

import streamlit as st
import cloudinary
import cloudinary.api
import random

# --- CONFIGURACIÓN DE ACCESO ---
cloudinary.config( 
  cloud_name = "detprbdvv", 
  api_key = "487844675958599", 
  api_secret = "lF9Z48IBN6JlGNvLzjuF1Osmgm8",
  secure = True
)

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="MAYNEXUS INFINITY", page_icon="⚡", layout="wide")

# --- CSS: ONDA INFINITA Y DISEÑO ELITE ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* BARRA DE ONDA INFINITA JAMÁS VISTA (Neon Liquid Wave) */
    .infinity-wave {
        height: 12px;
        width: 100%;
        background: linear-gradient(270deg, #ff0055, #00ff99, #0066ff, #ff0055, #00ff99);
        background-size: 400% 400%;
        animation: liquidWave 6s ease-in-out infinite;
        border-radius: 50px;
        filter: blur(2px);
        box-shadow: 0 0 20px #00ff9955;
        margin-bottom: 25px;
    }
    @keyframes liquidWave {
        0% { background-position: 0% 50%; transform: scaleX(1); }
        50% { background-position: 100% 50%; transform: scaleX(1.05); }
        100% { background-position: 0% 50%; transform: scaleX(1); }
    }

    /* Tarjetas Estilo Glassmorphism */
    .song-card {
        background: rgba(20, 20, 20, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .song-card:hover {
        border-color: #00ff99;
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(0, 255, 153, 0.2);
    }
    .cover-art {
        width: 100%;
        aspect-ratio: 1/1;
        border-radius: 15px;
        object-fit: cover;
        margin-bottom: 12px;
    }
    .song-title {
        font-size: 14px;
        font-weight: 700;
        color: #fff;
        height: 38px;
        overflow: hidden;
    }

    /* Sidebar Ultra-Dark */
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #111; }
    .stButton > button {
        width: 100%; border: none !important; background: transparent !important;
        color: #666 !important; text-align: left !important; padding: 12px !important;
        font-size: 15px !important; transition: 0.3s;
    }
    .stButton > button:hover { color: #00ff99 !important; background: #111 !important; }
    </style>
    <div class="infinity-wave"></div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN Y MODO ALEATORIO ---
if 'folder' not in st.session_state:
    st.session_state.folder = "corridos tumbados"
if 'shuffle' not in st.session_state:
    st.session_state.shuffle = False

with st.sidebar:
    st.markdown("<h1 style='color:#00ff99; font-size:28px;'>MAYNEXUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#444; font-size:11px; margin-top:-15px;'>INFINITY EDITION v18</p>", unsafe_allow_html=True)
    
    # Interruptor de Modo Aleatorio
    st.session_state.shuffle = st.toggle("🔀 MODO ALEATORIO", value=st.session_state.shuffle)
    
    st.markdown("---")
    carpetas = ["corridos tumbados", "bandas", "Regueton", "cristianas", "pop latino", "pop en español", "pop en ingles", "trance", "las mas sonadas"]
    
    for c in carpetas:
        active = "⭐ " if st.session_state.folder == c else "📁 "
        if st.button(f"{active}{c.upper()}", key=f"f_{c}"):
            st.session_state.folder = c
            st.rerun()

# --- CARGA DE DATOS ---
st.markdown(f"<h2 style='letter-spacing:-1px;'>{st.session_state.folder.title()}</h2>", unsafe_allow_html=True)

try:
    with st.spinner("Sincronizando flujo infinito..."):
        # 1. Obtener Portadas e Imágenes
        res_img = cloudinary.api.resources(type="upload", prefix=st.session_state.folder, resource_type="image", max_results=100)
        mapa_portadas = {img['public_id'].split('/')[-1]: img['secure_url'] for img in res_img.get('resources', [])}

        # 2. Obtener Audios
        res_audio = cloudinary.api.resources(type="upload", prefix=st.session_state.folder, resource_type="video", max_results=100)
        canciones = res_audio.get('resources', [])

    if canciones:
        # APLICAR MODO ALEATORIO SI ESTÁ ACTIVO
        if st.session_state.shuffle:
            random.shuffle(canciones)

        # Grid de 5 columnas
        cols = st.columns(5)
        for i, cancion in enumerate(canciones):
            with cols[i % 5]:
                nombre_full = cancion['public_id'].split('/')[-1]
                url_img = mapa_portadas.get(nombre_full, "https://via.placeholder.com/400/111/00ff99?text=NEXUS")
                
                # Renderizado Premium
                st.markdown(f'''
                    <div class="song-card">
                        <img src="{url_img}" class="cover-art">
                        <div class="song-title">{nombre_full[:40]}</div>
                    </div>
                ''', unsafe_allow_html=True)
                st.audio(cancion['secure_url'])
    else:
        st.info("Carpeta vacía. Esperando señal de la Lenovo.")

except Exception as e:
    st.error(f"Error de sistema: {e}")

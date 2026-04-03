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
    
    /* BARRA DE ONDA PROFESIONAL ANIMADA (Aurora Wave) */
    .infinity-wave {
        height: 12px;
        width: 100%;
        background: linear-gradient(270deg, #00ff99, #0066ff, #ff0055, #00ff99);
        background-size: 400% 400%;
        animation: liquidWave 8s ease-in-out infinite;
        border-radius: 50px;
        filter: blur(1px);
        box-shadow: 0 0 15px rgba(0, 255, 153, 0.4);
        margin-bottom: 30px;
    }
    @keyframes liquidWave {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Tarjetas de Canción Premium */
    .song-card {
        background: #0a0a0a;
        border-radius: 15px;
        padding: 12px;
        text-align: center;
        border: 1px solid #1a1a1a;
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .song-card:hover {
        border-color: #00ff99;
        transform: translateY(-8px);
        box-shadow: 0 10px 25px rgba(0, 255, 153, 0.15);
    }
    .cover-art {
        width: 100%;
        aspect-ratio: 1/1;
        border-radius: 10px;
        object-fit: cover;
        margin-bottom: 12px;
    }
    
    /* Sidebar Industrial Moderno */
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #1a1a1a; }
    .stButton > button {
        width: 100%; text-align: left !important; background: transparent !important;
        border: none !important; color: #777 !important; padding: 12px !important;
        font-size: 15px !important; transition: 0.3s;
    }
    .stButton > button:hover { color: #00ff99 !important; background: #111 !important; }
    </style>
    <div class="infinity-wave"></div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN Y SHUFFLE ---
if 'folder' not in st.session_state:
    st.session_state.folder = "corridos tumbados"
if 'shuffle_mode' not in st.session_state:
    st.session_state.shuffle_mode = False

with st.sidebar:
    st.markdown("<h1 style='color:#00ff99; font-size:26px;'>MAYNEXUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#444; font-size:10px; margin-top:-15px;'>INFINITY EDITION v18</p>", unsafe_allow_html=True)
    
    # Toggle de Modo Aleatorio
    st.session_state.shuffle_mode = st.toggle("🔀 MODO ALEATORIO", value=st.session_state.shuffle_mode)
    
    st.markdown("---")
    carpetas = ["corridos tumbados", "bandas", "Regueton", "cristianas", "pop latino", "pop en español", "pop en ingles", "trance", "las mas sonadas"]
    
    for c in carpetas:
        active_icon = "🟢 " if st.session_state.folder == c else "📁 "
        if st.button(f"{active_icon}{c.upper()}", key=f"nav_{c}"):
            st.session_state.folder = c
            st.rerun()

# --- CARGA Y RENDERIZADO ---
st.markdown(f"<h2 style='letter-spacing:-1px;'>{st.session_state.folder.title()}</h2>", unsafe_allow_html=True)

try:
    with st.spinner("Sintonizando flujo industrial..."):
        # Obtener portadas y audios
        res_img = cloudinary.api.resources(type="upload", prefix=st.session_state.folder, resource_type="image", max_results=100)
        mapa_portadas = {img['public_id'].split('/')[-1]: img['secure_url'] for img in res_img.get('resources', [])}

        res_audio = cloudinary.api.resources(type="upload", prefix=st.session_state.folder, resource_type="video", max_results=100)
        canciones = res_audio.get('resources', [])

    if canciones:
        # APLICAR MODO ALEATORIO
        if st.session_state.shuffle_mode:
            random.shuffle(canciones)

        # Grid de 5 columnas para máxima visibilidad
        cols = st.columns(5)
        for i, cancion in enumerate(canciones):
            with cols[i % 5]:
                nombre_full = cancion['public_id'].split('/')[-1]
                url_img = mapa_portadas.get(nombre_full, "https://via.placeholder.com/400/111/00ff99?text=♫")
                
                st.markdown(f'''
                    <div class="song-card">
                        <img src="{url_img}" class="cover-art">
                        <div style="font-size:13px; font-weight:600; height:35px; overflow:hidden;">{nombre_full[:40]}</div>
                    </div>
                ''', unsafe_allow_html=True)
                st.audio(cancion['secure_url'])
    else:
        st.info(f"La carpeta '{st.session_state.folder}' está lista para recibir archivos.")

except Exception as e:
    st.error(f"Falla en el motor Nexus: {e}")

st.sidebar.markdown("---")
st.sidebar.caption(f"Inspector: Maynor Vazquez")

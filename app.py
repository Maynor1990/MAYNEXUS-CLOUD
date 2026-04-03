import streamlit as st
import cloudinary
import cloudinary.api

# --- CONFIGURACIÓN CLOUDINARY ---
cloudinary.config( 
  cloud_name = "detprbdvv", 
  api_key = "487844675958599", 
  api_secret = "lF9Z48IBN6JlGNvLzjuF1Osmgm8",
  secure = True
)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="MAYNEXUS AURORA", page_icon="🎧", layout="wide")

# --- CSS: ESTILO APPLE MUSIC CON ONDA DE COLORES ---
st.markdown("""
    <style>
    /* Fondo oscuro y tipografía limpia */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* EFECTO AURORA (Onda de colores animada en el tope) */
    .aurora-bar {
        height: 6px;
        width: 100%;
        background: linear-gradient(90deg, #ff0055, #00ff99, #0066ff, #ff0055);
        background-size: 300% 100%;
        animation: aurora 8s linear infinite;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    @keyframes aurora {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }

    /* Botones de Carpeta en Sidebar */
    div[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        text-align: left !important;
        background-color: transparent !important;
        border: none !important;
        color: #888 !important;
        padding: 12px 10px !important;
        font-size: 16px !important;
        transition: 0.3s;
        border-radius: 8px;
    }
    div[data-testid="stSidebar"] .stButton > button:hover {
        color: #00ff99 !important;
        background-color: #1a1a1a !important;
    }
    
    /* Estilo de Filas de Canción */
    .song-row {
        display: flex;
        align-items: center;
        padding: 10px;
        border-bottom: 1px solid #111;
        margin-bottom: 5px;
    }
    .thumb { width: 50px; height: 50px; border-radius: 6px; margin-right: 15px; object-fit: cover; }
    .song-name { font-weight: 500; font-size: 15px; color: #ffffff; }
    .song-artist { font-size: 13px; color: #666; }
    
    /* Sidebar Fija Oscura */
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #111; }
    </style>
    <div class="aurora-bar"></div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---
# Usamos session_state para que la carpeta no se resetee al hacer clic
if 'folder' not in st.session_state:
    st.session_state.folder = "corridos tumbados"

with st.sidebar:
    st.markdown("<h1 style='color:#00ff99; font-size: 26px; margin-bottom: 0;'>MAYNEXUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555; font-size: 11px; margin-bottom: 25px;'>NEXUS ELITE v4.0</p>", unsafe_allow_html=True)
    
    st.markdown("<p style='color:#888; font-size: 13px; font-weight: bold;'>BIBLIOTECA</p>", unsafe_allow_html=True)
    
    carpetas = [
        "corridos tumbados", "bandas", "Regueton", "cristianas", 
        "pop latino", "pop en español", "pop en ingles", "trance", "las mas sonadas"
    ]
    
    # Botones laterales para cada carpeta
    for c in carpetas:
        # Si el botón coincide con la carpeta activa, le damos un toque visual
        label = f"📁 {c.title()}"
        if st.button(label, key=f"btn_{c}"):
            st.session_state.folder = c
            st.rerun()

    st.markdown("---")
    st.caption(f"Usuario: Maynor Vazquez")

# --- CONTENIDO PRINCIPAL ---
st.markdown(f"<h2 style='font-size: 32px;'>{st.session_state.folder.title()}</h2>", unsafe_allow_html=True)

try:
    with st.spinner("Cargando flujo de datos..."):
        # 1. Buscamos imágenes
        res_img = cloudinary.api.resources(
            type="upload", prefix=st.session_state.folder, resource_type="image", max_results=100
        )
        mapa_portadas = {img['public_id'].split('/')[-1]: img['secure_url'] for img in res_img.get('resources', [])}

        # 2. Buscamos audios
        res_audio = cloudinary.api.resources(
            type="upload", prefix=st.session_state.folder, resource_type="video", max_results=100
        )
        canciones = res_audio.get('resources', [])

    if canciones:
        for cancion in canciones:
            nombre_full = cancion['public_id'].split('/')[-1]
            # Separar nombre por el guion "Artista - Cancion"
            parts = nombre_full.split(" - ")
            artist = parts[0] if len(parts) > 1 else "Artista"
            track = parts[1] if len(parts) > 1 else nombre_full
            
            url_img = mapa_portadas.get(nombre_full, "https://via.placeholder.com/100/111/00ff99?text=♫")
            
            # Layout Apple Music: Info a la izquierda, audio a la derecha
            col_info, col_play = st.columns([2.5, 1.5])
            
            with col_info:
                st.markdown(f'''
                    <div class="song-row">
                        <img src="{url_img}" class="thumb">
                        <div>
                            <div class="song-name">{track}</div>
                            <div class="song-artist">{artist}</div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
            
            with col_play:
                # El reproductor de Streamlit es minimalista por defecto
                st.audio(cancion['secure_url'])
    else:
        st.info(f"La carpeta '{st.session_state.folder}' está vacía. ¡Dale fuego a la Lenovo!")

except Exception as e:
    st.error(f"Error en la conexión Nexus: {e}")

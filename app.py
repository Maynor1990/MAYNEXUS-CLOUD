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
st.set_page_config(page_title="MAYNEXUS ELITE", page_icon="🎧", layout="wide")

# --- CSS ESTILO APPLE MUSIC / PREMIUM ---
st.markdown("""
    <style>
    /* Fondo oscuro profundo */
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    
    /* Contenedor de la fila de canción */
    .song-row {
        display: flex;
        align-items: center;
        padding: 10px;
        border-bottom: 1px solid #1a1a1a;
        transition: background 0.2s;
        border-radius: 8px;
    }
    .song-row:hover { background-color: #1a1a1a; }
    
    /* Miniatura redonda pequeña */
    .thumb {
        width: 50px;
        height: 50px;
        border-radius: 6px;
        object-fit: cover;
        margin-right: 15px;
    }
    
    /* Info de la canción */
    .song-info { flex-grow: 1; }
    .song-name { font-size: 15px; font-weight: 500; color: #ffffff; }
    .song-artist { font-size: 13px; color: #888888; }
    
    /* Títulos de sección */
    .section-title { font-size: 24px; font-weight: 700; margin: 20px 0; color: #ffffff; }
    
    /* Sidebar minimalista */
    [data-testid="stSidebar"] { background-color: #080808; border-right: 1px solid #1a1a1a; }
    .stSelectbox label { color: #888 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color:#00ff99'>MAYNEXUS</h2>", unsafe_allow_html=True)
    genero = st.selectbox("BIBLIOTECA", [
        "corridos tumbados", "bandas", "Regueton", "cristianas", 
        "pop latino", "pop en español", "pop en ingles", "trance", "las mas sonadas"
    ])
    sync = st.button("🔄 SINCRONIZAR")
    st.markdown("---")
    st.caption("v3.0 Premium | Maynor Vazquez")

# --- CUERPO PRINCIPAL ---
st.markdown(f"<div class='section-title'>Recién llegadas en {genero.title()}</div>", unsafe_allow_html=True)

if sync or 'first_run' not in st.session_state:
    st.session_state.first_run = True
    try:
        # 1. Obtener Portadas
        res_img = cloudinary.api.resources(type="upload", prefix=genero, resource_type="image", max_results=100)
        mapa_portadas = {img['public_id'].split('/')[-1]: img['secure_url'] for img in res_img.get('resources', [])}

        # 2. Obtener Audios
        res_audio = cloudinary.api.resources(type="upload", prefix=genero, resource_type="video", max_results=100)
        canciones = res_audio.get('resources', [])

        if canciones:
            for cancion in canciones:
                nombre_full = cancion['public_id'].split('/')[-1]
                # Intentamos separar Artista - Canción si el nombre tiene guion
                parts = nombre_full.split(" - ")
                artist = parts[0] if len(parts) > 1 else "Artista Desconocido"
                track = parts[1] if len(parts) > 1 else nombre_full
                
                url_img = mapa_portadas.get(nombre_full, "https://via.placeholder.com/100/1a1a1a/00ff99?text=♫")
                
                # Renderizado estilo Lista Apple Music
                col_info, col_audio = st.columns([2, 1])
                
                with col_info:
                    st.markdown(f'''
                        <div class="song-row">
                            <img src="{url_img}" class="thumb">
                            <div class="song-info">
                                <div class="song-name">{track}</div>
                                <div class="song-artist">{artist}</div>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                
                with col_audio:
                    st.audio(cancion['secure_url'])
        else:
            st.info("Selecciona una estación y pulsa Sincronizar.")
            
    except Exception as e:
        st.error(f"Error de red: {e}")

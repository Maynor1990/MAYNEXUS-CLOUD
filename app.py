import streamlit as st
import cloudinary
import cloudinary.api

# --- CONFIGURACIÓN DE ACCESO ---
cloudinary.config( 
  cloud_name = "detprbdvv", 
  api_key = "487844675958599", 
  api_secret = "lF9Z48IBN6JlGNvLzjuF1Osmgm8",
  secure = True
)

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="MAYNEXUS V17", page_icon="🎧", layout="wide")

# --- CSS: ESTILO GRID PROFESIONAL ---
st.markdown("""
    <style>
    /* Fondo negro profundo */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Onda de colores Aurora */
    .aurora-bar {
        height: 5px; width: 100%;
        background: linear-gradient(90deg, #00ff99, #0066ff, #ff0055, #00ff99);
        background-size: 300% 100%;
        animation: aurora 10s linear infinite;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    @keyframes aurora { 0% {background-position:0% 50%} 100% {background-position:100% 50%} }

    /* Tarjetas de la Cuadrícula (Grid) */
    .song-card {
        background: #0d0d0d;
        border-radius: 15px;
        padding: 12px;
        text-align: center;
        border: 1px solid #1a1a1a;
        transition: all 0.3s ease;
        margin-bottom: 10px;
    }
    .song-card:hover {
        border-color: #00ff99;
        transform: scale(1.02);
        background: #111;
    }
    .cover-art {
        width: 100%;
        aspect-ratio: 1/1;
        border-radius: 10px;
        object-fit: cover;
        margin-bottom: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .song-title {
        font-size: 14px;
        font-weight: 600;
        color: #f0f0f0;
        height: 40px;
        line-height: 1.2;
        overflow: hidden;
        margin-bottom: 10px;
    }
    
    /* Sidebar Industrial */
    [data-testid="stSidebar"] { 
        background-color: #050505 !important; 
        border-right: 1px solid #1a1a1a; 
    }
    .stButton > button {
        width: 100%;
        text-align: left !important;
        background-color: transparent !important;
        color: #777 !important;
        border: none !important;
        padding: 10px 15px !important;
        font-size: 15px !important;
        transition: 0.2s;
    }
    .stButton > button:hover {
        color: #00ff99 !important;
        background-color: #111 !important;
    }
    </style>
    <div class="aurora-bar"></div>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN LATERAL ---
if 'folder' not in st.session_state:
    st.session_state.folder = "corridos tumbados"

with st.sidebar:
    st.markdown("<h2 style='color:#00ff99; margin-bottom:0;'>MAYNEXUS V17</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#444; font-size:10px; margin-bottom:30px;'>STRYKER QUALITY SYSTEM</p>", unsafe_allow_html=True)
    
    st.markdown("<p style='color:#888; font-size:12px; font-weight:bold; margin-left:15px;'>BIBLIOTECA</p>", unsafe_allow_html=True)
    
    carpetas = [
        "corridos tumbados", "bandas", "Regueton", "cristianas", 
        "pop latino", "pop en español", "pop en ingles", "trance", "las mas sonadas"
    ]
    
    for c in carpetas:
        # Icono dinámico según selección
        icon = "🟢" if st.session_state.folder == c else "📁"
        if st.button(f"{icon} {c.upper()}", key=f"btn_{c}"):
            st.session_state.folder = c
            st.rerun()
            
    st.markdown("---")
    if st.button("🔄 REFRESCAR NUBE"):
        st.cache_data.clear()

# --- CUERPO PRINCIPAL (GRID DE CANCIONES) ---
st.markdown(f"<h2 style='letter-spacing:-1px;'>{st.session_state.folder.title()}</h2>", unsafe_allow_html=True)

try:
    with st.spinner("Sincronizando medios..."):
        # 1. Obtener Portadas
        res_img = cloudinary.api.resources(
            type="upload", prefix=st.session_state.folder, resource_type="image", max_results=100
        )
        mapa_portadas = {img['public_id'].split('/')[-1]: img['secure_url'] for img in res_img.get('resources', [])}

        # 2. Obtener Audios
        res_audio = cloudinary.api.resources(
            type="upload", prefix=st.session_state.folder, resource_type="video", max_results=100
        )
        canciones = res_audio.get('resources', [])

    if canciones:
        # Rejilla de 5 columnas (Perfecto para móvil y PC)
        cols = st.columns(5)
        for i, cancion in enumerate(canciones):
            with cols[i % 5]:
                nombre_full = cancion['public_id'].split('/')[-1]
                url_img = mapa_portadas.get(nombre_full, "https://via.placeholder.com/400/111/00ff99?text=♫")
                
                # Renderizado de Tarjeta Estilo V17
                st.markdown(f'''
                    <div class="song-card">
                        <img src="{url_img}" class="cover-art">
                        <div class="song-title">{nombre_full[:45]}</div>
                    </div>
                ''', unsafe_allow_html=True)
                # Reproductor compacto debajo de la tarjeta
                st.audio(cancion['secure_url'])
    else:
        st.info(f"La sección '{st.session_state.folder}' está lista para recibir archivos de la Lenovo.")

except Exception as e:
    st.error(f"Error de conexión: {e}")

st.sidebar.markdown("---")
st.sidebar.caption(f"Operador: Mynor Vazquez")

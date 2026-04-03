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

st.set_page_config(page_title="MAYNEXUS QUANTUM", layout="wide")

# --- CSS: OPTIMIZACIÓN TOTAL ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    
    /* Barra de onda profesional minimalista */
    .quantum-line {
        height: 3px; width: 100%;
        background: linear-gradient(90deg, #00ff99, #0066ff, #00ff99);
        background-size: 200% 100%;
        animation: wave 4s linear infinite;
        margin-bottom: 15px;
    }
    @keyframes wave { 0% {background-position:0%} 100% {background-position:100%} }

    /* Tarjetas ultra ligeras */
    .song-card { 
        background: #080808; 
        border-radius: 10px; 
        padding: 8px; 
        border: 1px solid #111;
        transition: 0.2s;
    }
    .song-card:hover { border-color: #00ff99; background: #111; }
    
    /* Imagen fija para evitar saltos de pantalla */
    .cover-art { 
        width: 100%; 
        aspect-ratio: 1/1; 
        border-radius: 6px; 
        object-fit: cover; 
    }
    
    /* Texto pequeño para ahorrar espacio */
    .song-info { font-size: 11px; font-weight: 500; color: #eee; margin-top: 5px; height: 28px; overflow: hidden; }
    </style>
    <div class="quantum-line"></div>
    """, unsafe_allow_html=True)

# --- CACHÉ DE DATOS (Optimización de Almacén) ---
@st.cache_data(ttl=600)
def fetch_global_data():
    try:
        # Traer todo de la raíz
        res_audio = cloudinary.api.resources(resource_type="video", max_results=500)
        audios = res_audio.get('resources', [])
        res_img = cloudinary.api.resources(resource_type="image", max_results=500)
        imagenes = {img['public_id'].split('/')[-1]: img['secure_url'] for img in res_img.get('resources', [])}
        return audios, imagenes
    except:
        return [], {}

# CARGA INICIAL
audios, imagenes = fetch_global_data()

# --- REPRODUCTOR FIJO (En la parte superior) ---
if 'current_song' not in st.session_state:
    st.session_state.current_song = None

with st.sidebar:
    st.title("MAYNEXUS ⚡")
    if st.button("🔄 RECARGAR NUBE"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("---")
    st.caption("v22.0 Quantum Flow")
    st.caption("Inspector: Maynor Vazquez")

# ÁREA DE REPRODUCCIÓN (Solo se activa si eliges una canción)
if st.session_state.current_song:
    st.markdown("### 🎧 Reproduciendo Ahora")
    c1, c2 = st.columns([1, 4])
    with c1:
        img_url = imagenes.get(st.session_state.current_song['public_id'].split('/')[-1], "https://via.placeholder.com/150/111/00ff99")
        st.image(img_url, width=100)
    with c2:
        st.write(f"**{st.session_state.current_song['public_id'].split('/')[-1]}**")
        st.audio(st.session_state.current_song['secure_url'], autoplay=True)
    st.markdown("---")

# --- BUSCADOR Y GALERÍA ---
query = st.text_input("🔍 Buscar en biblioteca global...", "").lower()

if audios:
    # Filtramos solo por texto (rápido)
    resultados = [c for c in audios if query in c['public_id'].lower()] if query else audios
    
    # Mostramos máximo 40 para que el cel no sufra
    lista_final = resultados[:40]
    
    st.write(f"Viendo {len(lista_final)} de {len(resultados)} canciones")
    
    cols = st.columns(5)
    for i, cancion in enumerate(lista_final):
        with cols[i % 5]:
            nombre = cancion['public_id'].split('/')[-1]
            foto = imagenes.get(nombre, "https://via.placeholder.com/300/111/00ff99?text=♫")
            
            # Tarjeta visual
            st.markdown(f'''
                <div class="song-card">
                    <img src="{foto}" class="cover-art">
                    <div class="song-info">{nombre[:30]}</div>
                </div>
            ''', unsafe_allow_html=True)
            
            # Botón de acción para cargar la canción (Esto es lo que ahorra RAM)
            if st.button(f"▶️ Sonar", key=f"play_{i}"):
                st.session_state.current_song = cancion
                st.rerun()
else:
    st.warning("No hay datos. Asegúrate de que tus archivos estén en la raíz de Cloudinary.")

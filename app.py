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

# --- INTERFAZ PREMIUM ---
st.set_page_config(page_title="MAYNEXUS INFINITY", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    
    /* BARRA DE ONDA DINÁMICA (JAMÁS VISTA) */
    .nexus-wave {
        height: 15px; width: 100%;
        background: linear-gradient(270deg, #00ff99, #0066ff, #ff0055, #00ff99);
        background-size: 400% 400%;
        animation: nexusWave 6s cubic-bezier(0.45, 0, 0.55, 1) infinite;
        border-radius: 50px;
        box-shadow: 0 0 25px rgba(0, 255, 153, 0.5);
        margin-bottom: 30px;
    }
    @keyframes nexusWave {
        0% { background-position: 0% 50%; transform: scaleY(0.8); }
        50% { background-position: 100% 50%; transform: scaleY(1.2); }
        100% { background-position: 0% 50%; transform: scaleY(0.8); }
    }

    .song-card { background: #0a0a0a; border-radius: 15px; padding: 10px; border: 1px solid #1a1a1a; transition: 0.3s; }
    .song-card:hover { border-color: #00ff99; transform: translateY(-5px); }
    .cover-art { width: 100%; aspect-ratio: 1/1; border-radius: 10px; object-fit: cover; }
    </style>
    <div class="nexus-wave"></div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
if 'shuffle' not in st.session_state: st.session_state.shuffle = False
if 'folder' not in st.session_state: st.session_state.folder = "corridos tumbados"

with st.sidebar:
    st.title("MAYNEXUS v19")
    st.session_state.shuffle = st.toggle("🔀 MODO ALEATORIO", value=st.session_state.shuffle)
    st.markdown("---")
    
    # Lista de carpetas/géneros
    generos = ["corridos tumbados", "bandas", "Regueton", "cristianas", "pop latino", "pop en español", "pop en ingles", "trance", "las mas sonadas"]
    for g in generos:
        if st.button(f"📁 {g.upper()}", key=f"g_{g}"):
            st.session_state.folder = g
            st.rerun()

# --- BUSCADOR INTELIGENTE (FIX) ---
st.header(f"Sección: {st.session_state.folder.upper()}")

try:
    with st.spinner("Sincronizando flujo de datos..."):
        # Buscamos en TODA la cuenta (sin prefix estricto) para rescatar tus archivos sueltos
        # pero filtramos por los que contengan el nombre de la carpeta en su nombre
        res_audio = cloudinary.api.resources(resource_type="video", max_results=500)
        todas_las_canciones = res_audio.get('resources', [])
        
        # Filtramos: si el archivo está en la carpeta O si el nombre tiene palabras clave
        canciones = [
            c for c in todas_las_canciones 
            if st.session_state.folder in c['public_id'].lower() or c['public_id'].startswith(st.session_state.folder)
        ]

        # Si sigue sin salir nada, buscamos imágenes para las portadas
        res_img = cloudinary.api.resources(resource_type="image", max_results=500)
        mapa_portadas = {img['public_id'].split('/')[-1]: img['secure_url'] for img in res_img.get('resources', [])}

    if canciones:
        if st.session_state.shuffle:
            random.shuffle(canciones)
            
        cols = st.columns(5)
        for i, cancion in enumerate(canciones):
            with cols[i % 5]:
                id_limpio = cancion['public_id'].split('/')[-1]
                foto = mapa_portadas.get(id_limpio, "https://via.placeholder.com/300/111/00ff99?text=♫")
                
                st.markdown(f'''
                    <div class="song-card">
                        <img src="{foto}" class="cover-art">
                        <p style="font-size:12px; font-weight:bold; height:30px; overflow:hidden; margin-top:5px;">{id_limpio}</p>
                    </div>
                ''', unsafe_allow_html=True)
                st.audio(cancion['secure_url'])
    else:
        st.warning("No se encontraron coincidencias. Intenta renombrar tus archivos en Cloudinary incluyendo el género.")

except Exception as e:
    st.error(f"Falla técnica: {e}")

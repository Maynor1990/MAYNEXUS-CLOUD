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

# --- ESTILOS NEXUS INFINITY ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .infinity-wave {
        height: 8px; width: 100%;
        background: linear-gradient(90deg, #00ff99, #0066ff, #ff0055, #00ff99);
        background-size: 200% 100%;
        animation: wave 5s linear infinite;
        border-radius: 10px; margin-bottom: 20px;
    }
    @keyframes wave { 0% {background-position:0%} 100% {background-position:100%} }
    .song-card { background: #111; border-radius: 15px; padding: 10px; border: 1px solid #222; text-align: center; }
    .cover-art { width: 100%; aspect-ratio: 1/1; border-radius: 10px; object-fit: cover; }
    </style>
    <div class="infinity-wave"></div>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if 'folder' not in st.session_state:
    st.session_state.folder = "corridos tumbados"

with st.sidebar:
    st.title("MAYNEXUS ⚡")
    carpetas = ["corridos tumbados", "bandas", "Regueton", "cristianas", "pop latino", "pop en español", "pop en ingles", "trance", "las mas sonadas"]
    
    for c in carpetas:
        if st.button(f"📁 {c.upper()}", key=f"btn_{c}"):
            st.session_state.folder = c
            st.rerun()

# --- MOTOR DE BÚSQUEDA CORREGIDO ---
st.header(f"Sección: {st.session_state.folder.upper()}")

try:
    # IMPORTANTE: El prefix debe terminar en '/' para asegurar que busque DENTRO de la carpeta
    prefix_busqueda = f"{st.session_state.folder}/"
    
    with st.spinner(f"Escaneando {prefix_busqueda}..."):
        # 1. Buscar Audios (Cloudinary los trata como 'video')
        res_audio = cloudinary.api.resources(
            type="upload", 
            prefix=st.session_state.folder, # Intentamos con y sin barra
            resource_type="video", 
            max_results=500
        )
        canciones = res_audio.get('resources', [])

        # 2. Buscar Imágenes
        res_img = cloudinary.api.resources(
            type="upload", 
            prefix=st.session_state.folder, 
            resource_type="image", 
            max_results=500
        )
        mapa_portadas = {img['public_id'].split('/')[-1]: img['secure_url'] for img in res_img.get('resources', [])}

    if canciones:
        st.success(f"¡Encontradas {len(canciones)} canciones!")
        cols = st.columns(5)
        for i, cancion in enumerate(canciones):
            with cols[i % 5]:
                # Limpiamos el ID para quitar la ruta de la carpeta del nombre visible
                nombre_archivo = cancion['public_id'].split('/')[-1]
                url_foto = mapa_portadas.get(nombre_archivo, "https://via.placeholder.com/300/111/00ff99?text=♫")
                
                st.markdown(f'''
                    <div class="song-card">
                        <img src="{url_foto}" class="cover-art">
                        <p style="font-size:12px; margin-top:5px; height:30px; overflow:hidden;">{nombre_archivo}</p>
                    </div>
                ''', unsafe_allow_html=True)
                st.audio(cancion['secure_url'])
    else:
        st.warning(f"No se detectaron archivos. Verifica que en Cloudinary la carpeta se llame exactamente: '{st.session_state.folder}'")
        # Botón de ayuda para debug
        if st.button("🔍 Ver qué hay en mi Cloudinary"):
            all_res = cloudinary.api.resources(max_results=10)
            st.write("Últimos 10 archivos subidos:", [r['public_id'] for r in all_res['resources']])

except Exception as e:
    st.error(f"Error técnico: {e}")

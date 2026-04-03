import streamlit as st
import cloudinary
import cloudinary.api

# --- CONFIGURACIÓN DE CONEXIÓN ---
cloudinary.config( 
  cloud_name = "detprbdvv", 
  api_key = "487844675958599", 
  api_secret = "lF9Z48IBN6JlGNvLzjuF1Osmgm8",
  secure = True
)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="MAYNEXUS v2.0", page_icon="🎵", layout="wide")

# --- CSS PROFESIONAL Y MINIMALISTA ---
st.markdown("""
    <style>
    /* Fondo oscuro sólido y elegante */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Estilo para las tarjetas de música */
    .song-card {
        background: #161b22;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #30363d;
        transition: transform 0.3s ease;
        margin-bottom: 25px;
    }
    .song-card:hover {
        transform: translateY(-5px);
        border-color: #00ff99;
    }
    
    /* Títulos limpios */
    h1 { font-weight: 800; letter-spacing: -1px; color: #ffffff; margin-bottom: 30px; }
    .song-title { color: #00ff99; font-size: 1.1rem; font-weight: 600; margin-top: 15px; }
    
    /* Personalización de botones */
    .stButton>button {
        width: 100%;
        background-color: #00ff99;
        color: #000000;
        border-radius: 12px;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    
    /* Esconder elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (Panel de Control) ---
with st.sidebar:
    st.image("https://res.cloudinary.com/detprbdvv/image/upload/v1/logo_nexus.png", width=150) # Si tienes logo úsalo aquí
    st.markdown("### 🎛️ PANEL DE CONTROL")
    
    genero_elegido = st.selectbox("CATEGORÍA", [
        "corridos tumbados", "bandas", "Regueton", "cristianas", 
        "pop latino", "pop en español", "pop en ingles", "trance", "las mas sonadas"
    ])
    
    actualizar = st.button("🔄 SINCRONIZAR NUBE")
    
    st.markdown("---")
    st.info(f"**Usuario:** Maynor Vazquez\n\n**Nivel:** Quality Inspector\n\n**Versión:** 2.0 Premium")

# --- CUERPO PRINCIPAL ---
st.title("MAYNEXUS `PRO` 🎵")

if actualizar:
    try:
        with st.spinner("Conectando con la bóveda de medios..."):
            # Búsqueda de recursos
            res_img = cloudinary.api.resources(type="upload", prefix=genero_elegido, resource_type="image", max_results=100)
            mapa_portadas = {img['public_id'].split('/')[-1]: img['secure_url'] for img in res_img.get('resources', [])}

            res_audio = cloudinary.api.resources(type="upload", prefix=genero_elegido, resource_type="video", max_results=100)
            canciones = res_audio.get('resources', [])

            if canciones:
                # Layout de rejilla limpio (3 columnas para minimalismo)
                cols = st.columns(3)
                for i, cancion in enumerate(canciones):
                    with cols[i % 3]:
                        nombre_id = cancion['public_id'].split('/')[-1]
                        url_foto = mapa_portadas.get(nombre_id, "https://via.placeholder.com/600x400/161b22/00ff99?text=MAYNEXUS")
                        
                        # Renderizado de Tarjeta
                        st.markdown(f'''
                            <div class="song-card">
                                <img src="{url_foto}" style="width:100%; border-radius:12px;">
                                <div class="song-title">{nombre_id}</div>
                            </div>
                        ''', unsafe_allow_html=True)
                        st.audio(cancion['secure_url'])
            else:
                st.warning("No hay medios en esta categoría.")
    except Exception as e:
        st.error(f"Error de enlace: {e}")
else:
    # Mensaje de bienvenida minimalista
    st.markdown("""
        ### Bienvenido al Nexus, Maynor.
        Selecciona una categoría en el panel izquierdo para comenzar la transmisión.
    """)
    st.image("https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&q=80&w=1000", use_column_width=True)

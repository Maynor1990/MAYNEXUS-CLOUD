import streamlit as st
import cloudinary
import cloudinary.api

# --- CONFIGURACIÓN DE CONEXIÓN (Tus llaves reales) ---
cloudinary.config( 
  cloud_name = "detprbdvv", 
  api_key = "487844675958599", 
  api_secret = "lF9Z48IBN6JlGNvLzjuF1Osmgm8",
  secure = True
)

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="MAYNEXUS CLOUD", page_icon="🎵", layout="wide")

# Estilo Dark Mode con bordes verde neón
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ff99; }
    .stSelectbox label { color: #00ff99 !important; font-size: 20px; }
    h1 { text-align: center; color: #00ff99; text-shadow: 2px 2px #000; border-bottom: 2px solid #00ff99; }
    .song-card {
        background-color: #111;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #333;
        margin-bottom: 25px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("MAYNEXUS CLOUD ☁️🎵")

# --- SELECTOR DE CARPETAS ---
# Asegúrate de que estos nombres sean iguales a tus carpetas en Cloudinary
opciones = ["corridos tumbados", "Regueton", "bandas", "cristianas", "pop latino"]
genero_elegido = st.selectbox("📂 SELECCIONA TU BIBLIOTECA:", opciones)

st.markdown("---")

if st.button("🔄 SINCRONIZAR CON LA NUBE"):
    try:
        # 1. Buscamos los archivos de audio en la carpeta seleccionada
        # Usamos 'prefix' para que solo traiga lo de esa carpeta
        recursos = cloudinary.api.resources(
            type="upload", 
            prefix=genero_elegido, 
            resource_type="video", 
            max_results=100
        )
        
        if not recursos['resources']:
            st.warning(f"No hay canciones en la carpeta '{genero_elegido}' aún.")
        else:
            st.success(f"Cargando {len(recursos['resources'])} canciones...")
            
            # 2. Creamos una rejilla de 2 columnas para las tarjetas
            cols = st.columns(2)
            
            for i, cancion in enumerate(recursos['resources']):
                with cols[i % 2]:
                    # Limpiamos el nombre (quitamos la ruta de la carpeta)
                    nombre_id = cancion['public_id'].split('/')[-1]
                    
                    # Generamos la URL de la portada (cambiamos .mp3 por .jpg)
                    # Esto funciona porque el descargador sube ambos con el mismo nombre
                    url_audio = cancion['secure_url']
                    url_portada = url_audio.replace(".mp3", ".jpg")
                    
                    # Dibujamos la tarjeta
                    st.markdown('<div class="song-card">', unsafe_allow_html=True)
                    st.image(url_portada, use_column_width=True, caption="MAYNEXUS Art")
                    st.markdown(f"### 🎧 {nombre_id}")
                    st.audio(url_audio)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
    except Exception as e:
        st.error(f"Error al conectar con Cloudinary: {e}")

st.sidebar.markdown("---")
st.sidebar.info("MAYNEXUS v1.5\nSistema de Gestión de Medios Industrial")

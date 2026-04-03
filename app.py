import streamlit as st
import cloudinary
import cloudinary.api

# --- CONFIGURACIÓN ---
cloudinary.config( 
  cloud_name = "detprbdvv", 
  api_key = "487844675958599", 
  api_secret = "lF9Z48IBN6JlGNvLzjuF1Osmgm8",
  secure = True
)

st.set_page_config(page_title="MAYNEXUS CLOUD", page_icon="🎵", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ff99; }
    .song-card {
        background-color: #111;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #00ff99;
        margin-bottom: 20px;
        text-align: center;
    }
    img { border-radius: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("MAYNEXUS CLOUD ☁️🎵")

opciones = ["corridos tumbados", "Regueton", "bandas", "cristianas", "pop latino"]
genero_elegido = st.selectbox("📂 SELECCIONA TU BIBLIOTECA:", opciones)

if st.button("🔄 SINCRONIZAR CON LA NUBE"):
    try:
        # 1. Traemos TODOS los archivos de la carpeta (imágenes y audios)
        recursos = cloudinary.api.resources(
            type="upload", 
            prefix=genero_elegido, 
            resource_type="image", # Primero buscamos las imágenes de portada
            max_results=100
        )
        
        # Guardamos las imágenes en un diccionario para acceso rápido
        portadas = {res['public_id'].split('/')[-1]: res['secure_url'] for res in recursos.get('resources', [])}

        # 2. Ahora traemos los audios
        audios = cloudinary.api.resources(
            type="upload", 
            prefix=genero_elegido, 
            resource_type="video", 
            max_results=100
        )
        
        if not audios['resources']:
            st.warning("No hay canciones aquí todavía.")
        else:
            cols = st.columns(2)
            for i, cancion in enumerate(audios['resources']):
                with cols[i % 2]:
                    nombre_id = cancion['public_id'].split('/')[-1]
                    
                    # Buscamos si existe una portada con el mismo nombre
                    url_img = portadas.get(nombre_id, "https://via.placeholder.com/500x500?text=MAYNEXUS+MUSIC")
                    
                    st.markdown('<div class="song-card">', unsafe_allow_html=True)
                    st.image(url_img, use_column_width=True)
                    st.markdown(f"### 🎧 {nombre_id}")
                    st.audio(cancion['secure_url'])
                    st.markdown('</div>', unsafe_allow_html=True)
                    
    except Exception as e:
        st.error(f"Error: {e}")

st.caption("MAYNEXUS v1.6 | Calidad Stryker")

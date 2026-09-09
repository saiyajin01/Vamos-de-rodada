import streamlit as st
import json
import urllib.parse

# Configuración de la ventana del navegador
st.set_page_config(page_title="Rutas Moteras Colombia", page_icon="🏍️", layout="wide")

# Función para cargar los pueblos desde rutas.json
@st.cache_data
def cargar_datos():
    try:
        with open("rutas.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

base_de_datos = cargar_datos()

# Título de la App
st.title("🏍️ Rutas y Destinos Moteros desde Medellín")
st.caption("Selecciona el departamento y municipio destino para consultar los datos técnicos de tu rodada.")

# Menú lateral interactivo
st.sidebar.header("🗺️ Selección de Destino")

departamentos = sorted(list(base_de_datos.keys()))
depto_sel = st.sidebar.selectbox("Selecciona Departamento:", departamentos)

if depto_sel:
    municipios = sorted(list(base_de_datos[depto_sel].keys()))
    muni_sel = st.sidebar.selectbox("Selecciona Municipio:", municipios)

    if muni_sel:
        data = base_de_datos[depto_sel][muni_sel]

        # Título del municipio seleccionado
        st.header(f"📍 {muni_sel}, {depto_sel}")
        
        # Tarjetas de datos rápidos (Distancia y Tiempo)
        col1, col2 = st.columns(2)
        col1.metric("📍 Distancia desde Medellín", data.get("distancia", "N/D"))
        col2.metric("⏱️ Tiempo Estimado", data.get("tiempo", "N/D"))

        st.markdown("---")

        # Bloques de Clima y Estado de la Vía (Sin recortes)
        col_clima, col_via = st.columns(2)
        with col_clima:
            st.markdown("**🌡️ Clima:**")
            st.info(data.get("clima", "N/D"))

        with col_via:
            st.markdown("**🛣️ Estado de la Vía:**")
            st.info(data.get("estado_via", "N/D"))

        st.markdown("---")

        # Secciones organizadas en pestañas
        tab1, tab2, tab3 = st.tabs(["🗺️ Rutas y Terreno", "📸 Lugares y Planes", "📍 Navegación GPS"])

        with tab1:
            st.subheader("Información de Carretera")
            st.write(f"**Tipo de Terreno:** {data.get('tipo_terreno', 'No especificado')}")
            st.write("**Opciones de ruta sugeridas:**")
            for r in data.get("rutas", []):
                st.info(f"👉 {r}")

        with tab2:
            st.subheader("¿Qué hacer y conocer en este destino?")
            for p in data.get("planes", []):
                st.write(f"✅ {p}")

        with tab3:
            st.subheader("Abrir ruta directa en Google Maps")
            origen = "Medellín, Antioquia"
            destino = f"{muni_sel}, {depto_sel}, Colombia"
            url_gmaps = f"https://www.google.com/maps/dir/?api=1&origin={urllib.parse.quote(origen)}&destination={urllib.parse.quote(destino)}&travelmode=driving"
            
            st.link_button(
    f"🗺️ Abrir GPS hacia {muni_sel}",
    url_gmaps,
    type="primary",
    use_container_width=True
)

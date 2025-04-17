import streamlit as st
import pandas as pd
import json
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl

# Configuración inicial
st.set_page_config(page_title="Análisis Inmobiliario Beijing", layout="wide")

# Sidebar de navegación
st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Selecciona una sección", [
    "Inicio",
    "Contexto migración y crecimiento urbano en China",
    "Datos geoespaciales de Beijing"
])

# Función para cargar datos
@st.cache_data
def cargar_datos():
    migracion = pd.read_csv("migracion.csv")
    crecimiento_urbano = pd.read_csv("crecimiento_urbano.csv")
    pib = pd.read_csv("pib.csv")
    composicion_urbana = pd.read_csv("composicion_urbana.csv")

    with open("servicios.geojson", "r", encoding="utf-8") as f:
        servicios = json.load(f)
    with open("metro.geojson", "r", encoding="utf-8") as f:
        metro = json.load(f)

    precios = pd.read_csv("precios.csv")

    return migracion, crecimiento_urbano, pib, composicion_urbana, servicios, metro, precios

# Carga de datos
migracion, crecimiento_urbano, pib, composicion_urbana, servicios, metro, precios = cargar_datos()

# Página de Inicio
if pagina == "Inicio":
    st.title("Análisis del Contexto del Mercado Inmobiliario en Beijing")
    st.markdown("""
        Esta aplicación explora los factores que influyen en el precio de la vivienda en Beijing,
        considerando tanto el contexto macro de China (migración, crecimiento urbano, PIB)
        como factores geoespaciales (proximidad a estaciones de metro, servicios y precios).
    """)

# Página de Contexto
elif pagina == "Contexto migración y crecimiento urbano en China":
    st.title("Contexto de Migración y Crecimiento Urbano en China")

    st.subheader("Migración")
    st.dataframe(migracion)

    st.subheader("Crecimiento Urbano")
    st.dataframe(crecimiento_urbano)

    st.subheader("Producto Interno Bruto")
    st.dataframe(pib)

    st.subheader("Composición Urbana")
    st.dataframe(composicion_urbana)

# Página de Datos Geoespaciales
elif pagina == "Datos geoespaciales de Beijing":
    st.title("Datos Geoespaciales de Beijing")

    st.subheader("Vista Interactiva con Kepler.gl")

    mapa = KeplerGl(height=600)
    mapa.add_data(data=precios, name="Precios")
    mapa.add_data(data=servicios, name="Servicios")
    mapa.add_data(data=metro, name="Metro")

    keplergl_static(mapa)

    st.subheader("Datos Crudos")
    st.markdown("**Precios de Vivienda**")
    st.dataframe(precios)

    st.markdown("**Resumen de Servicios (GeoJSON)**")
    st.json(servicios)

    st.markdown("**Resumen de Estaciones de Metro (GeoJSON)**")
    st.json(metro)

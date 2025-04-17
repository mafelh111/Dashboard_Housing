import pandas as pd
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import Point, LineString

# --- Carga de datos ---
@st.cache_data
def load_data(file_path):
    try:
        if file_path.endswith('.geojson') or file_path.endswith('.json'):
            gdf = gpd.read_file(file_path)
            return gdf
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            return df
        else:
            st.error(f"Formato de archivo no soportado: {file_path}")
            return None
    except FileNotFoundError:
        st.error(f"No se encontró el archivo: {file_path}")
        return None
    except Exception as e:
        st.error(f"Error al cargar el archivo {file_path}: {e}")
        return None

migracion = load_data('Migración.csv')
crecimiento = load_data('Crecimiento_urbano.csv')
pib = load_data('Gdp.csv')
composicion = load_data('composicion.csv')

beijing_services_gdf = load_data('beijing_services.geojson')
beijing_metro_gdf = load_data('beijing_metro.geojson')
precios_clean_df = load_data('precios_clean.csv')

# --- Creación de gráficos ---
def update_fig_layout(fig, y_title):
    fig.update_traces(mode='lines+markers', marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(xaxis_title='Año', yaxis_title=y_title)
    return fig

def create_composicion_charts():
    tipos_de_vivienda = composicion[composicion["Item"].isin([
        "Viviendas Individuales de Varios Pisos", "Viviendas Individuales de Una Planta",
        "Apartamento de Cuatro o Más Habitaciones", "Apartamento de Tres Habitaciones",
        "Apartamento de Dos Habitaciones", "Apartamento de Una Habitación",
        "Apartamento Tipo Tubo o Agrupado Estrechamente", "Viviendas de Una Planta", "Otros"
    ])]

    fuentes_de_vivienda = composicion[composicion["Item"].isin([
        "Viviendas Públicas Alquiladas", "Viviendas Privadas Alquiladas", "Viviendas Autoconstruidas",
        "Viviendas Comerciales Compradas", "Viviendas Compradas de la Reforma de Vivienda",
        "Viviendas de Indemnización Compradas", "Viviendas de Reasentamiento", "Viviendas por Herencia o Donación",
        "Viviendas Prestadas Gratuitamente", "Viviendas Gratuitas Suministradas por Empleadores", "Otros"
    ])]

    fig1 = px.bar(tipos_de_vivienda,
                  x="Item",
                  y=['Ciudad Entera', 'Viviendas Urbanas', 'Viviendas rurales'],
                  title="Comparación de Tipos de Vivienda",
                  labels={"Item": "Tipo de Vivienda", "value": "Porcentaje", "variable": "Categoría"},
                  barmode="group")
    fig1.update_xaxes(tickangle=45)
    fig1.update_traces(marker=dict(line=dict(width=0.5, color='black')))
    fig1.update_layout(width=800, height=600, margin=dict(l=40, r=40, t=40, b=80))

    fig2 = px.bar(fuentes_de_vivienda,
                  x="Item",
                  y=['Ciudad Entera', 'Viviendas Urbanas', 'Viviendas rurales'],
                  title="Comparación de Fuentes de Vivienda",
                  labels={"Item": "Fuente de Vivienda", "value": "Porcentaje", "variable": "Categoría"},
                  barmode="group")
    fig2.update_xaxes(tickangle=45)
    fig2.update_traces(marker=dict(line=dict(width=0.5, color='black')))
    fig2.update_layout(width=800, height=600, margin=dict(l=40, r=40, t=40, b=80))

    return fig1, fig2

fig_migracion = update_fig_layout(px.line(migracion, x='Year', y='Net Migration', title='Migración neta de China'), 'Migración neta')
fig_crecimiento = update_fig_layout(px.line(crecimiento, x='Año', y='Tasa_crecimiento', title='Crecimiento urbano de China'), 'Tasa de crecimiento urbano(%)')
fig_pib = update_fig_layout(px.line(pib, x='Año', y='Tasa PIB', title='Tasa de crecimiento del PIB de China'), 'Tasa PIB(%)')

fig_tipos_vivienda, fig_fuentes_vivienda = create_composicion_charts()

# --- Diseño del Dashboard ---
st.title('Análisis Contextual del Mercado Inmobiliario de Pekín')

tab1, tab2, tab3, tab4 = st.tabs(["Migración y Crecimiento", "PIB", "Composición de Vivienda", "Mapa"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_migracion)
    with col2:
        st.plotly_chart(fig_crecimiento)

with tab2:
    st.plotly_chart(fig_pib)

with tab3:
    st.plotly_chart(fig_tipos_vivienda)
    st.plotly_chart(fig_fuentes_vivienda)

with tab4:
    st.markdown("### Mapa Interactivo: Servicios Urbanos y Transporte en Pekín")

    # 1. Crear el mapa Folium
    m = folium.Map(location=[39.92836694172162, 116.3764795575669], zoom_start=9.827295162832453, tiles="Satellite")

    # 2. Agregar capas (adaptado a la configuración de Kepler.gl)
    # Capa de precios (precios_clean)
    if precios_clean_df is not None:
        for idx, row in precios_clean_df.iterrows():
            folium.CircleMarker(
                location=[row.Lat, row.Lng],
                radius=13.7,
                color='#E33890',  # Tomado de la colorRange de Kepler.gl
                fill=True,
                fill_color='#E33890',
                fill_opacity=0.8,
                popup=f"Precio: {row.price}"
            ).add_to(m)

    # Capa de servicios (beijing_services)
    if beijing_services_gdf is not None:
        for idx, row in beijing_services_gdf.iterrows():
            if row.geometry.geom_type == 'Point':
                folium.CircleMarker(
                    location=[row.geometry.y, row.geometry.x],
                    radius=5,
                    color='#0077BB',  # Tomado de la colorRange de Kepler.gl
                    fill=True,
                    fill_color='#0077BB',
                    fill_opacity=0.77,
                    popup=f"Servicio: {row.amenity}"
                ).add_to(m)
            elif row.geometry.geom_type.startswith('Polygon'):
                # Calcula el centroide para mostrar el marcador en el centro del polígono
                centroid = row.geometry.centroid
                folium.CircleMarker(
                    location=[centroid.y, centroid.x],
                    radius=5,
                    color='#0077BB',
                    fill=True,
                    fill_color='#0077BB',
                    fill_opacity=0.77,
                    popup=f"Servicio: {row.amenity}"
                ).add_to(m)

    # Capa de metro (beijing_metro)
    if beijing_metro_gdf is not None:
        for idx, row in beijing_metro_gdf.iterrows():
            if row.geometry.geom_type == 'LineString':
                coords = [[coord[1], coord[0]] for coord in list(row.geometry.coords)]
                folium.PolyLine(coords, color='#FFC300', weight=8.9, opacity=0.8).add_to(m)
            elif row.geometry.geom_type == 'MultiLineString':
                for line in row.geometry.geoms:
                    coords = [[coord[1], coord[0]] for coord in list(line.coords)]
                    folium.PolyLine(coords, color='#FFC300', weight=8.9, opacity=0.8).add_to(m)

    # 3. Mostrar el mapa en Streamlit
    st_folium(m, width=800, height=600)

# Expanders para información adicional (opcional)
# with st.expander("Información sobre Migración"):
#     st.write("Datos de migración neta de China desde 1990.")

# with st.expander("Información sobre Crecimiento Urbano"):
#   st.write("Tasa de crecimiento urbano de China.")

# with st.expander("Información sobre el PIB"):
#   st.write("Tasa de crecimiento del Producto Interno Bruto de China.")

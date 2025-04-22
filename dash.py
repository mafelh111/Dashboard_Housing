import pandas as pd
import geopandas as gpd
import plotly.express as px

import streamlit as st

import streamlit.components.v1 as components

from keplergl import KeplerGl

from streamlit_keplergl import keplergl_static



# Carga de datos (mismo código que antes)

migracion = pd.read_csv('Migración.csv', sep=',', skiprows=3)

migracion = migracion[migracion['Country Name'] == 'China']

migracion = migracion.drop(columns=['Country Name', 'Indicator Name', 'Indicator Code'])

migracion = migracion.T

migracion.columns = migracion.iloc[0]

migracion = migracion[1:]

migracion = migracion.dropna()

migracion = migracion.rename(columns={'CHN': 'Net Migration'})

migracion = migracion.rename_axis('Year').reset_index()

migracion = migracion.reset_index(drop=True)

migracion['Year'] = migracion['Year'].astype(int)

migracion = migracion[migracion['Year'] >= 1990]



crecimiento = pd.read_csv('Crecimiento_urbano.csv', sep=',')

crecimiento = crecimiento.T

crecimiento = crecimiento.reset_index()

crecimiento.columns = crecimiento.iloc[3]

crecimiento = crecimiento[4:]

crecimiento = crecimiento.rename(columns={'CHN': 'Tasa_crecimiento', 'Country Code': 'Año'})

crecimiento = crecimiento.dropna(axis=1, how='any')

crecimiento['Año'] = crecimiento['Año'].str.extract('(\d+)').astype(int)



pib = pd.read_csv('Gdp.csv', sep=',', skiprows=3)

pib = pib[pib['Country Name'] == 'China']

pib = pib.drop(columns=['Country Name', 'Indicator Name', 'Indicator Code'])

pib = pib.T

pib = pib.reset_index()

pib.columns = pib.iloc[0]

pib = pib[1:]

pib.columns = ['Año', 'Tasa PIB']

pib = pib.dropna()

pib['Año'] = pib['Año'].astype(int)

pib = pib[pib['Año'] >= 1990]

pib['Tasa PIB'] = pib['Tasa PIB'].astype(float)

pib = pib.reset_index(drop=True)



# Creación de gráficos (mismo código que antes)

def update_fig_layout(fig, y_title):

  fig.update_traces(mode='lines+markers', marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))

  fig.update_layout(xaxis_title='Año', yaxis_title=y_title)

  return fig



fig_migracion = update_fig_layout(px.line(migracion, x='Year', y='Net Migration', title='Migración neta de China'), 'Migración neta')

fig_crecimiento = update_fig_layout(px.line(crecimiento, x='Año', y='Tasa_crecimiento', title='Crecimiento urbano de China'), 'Tasa de crecimiento urbano(%)')

fig_pib = update_fig_layout(px.line(pib, x='Año', y='Tasa PIB', title='Tasa de crecimiento del PIB de China'), 'Tasa PIB(%)')


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
beijing_metro_gdf = load_data('beijing_metro.geojson')
beijing_services_gdf = load_data('beijing_services.geojson')
precios_clean_df = load_data('precios_clean.csv')
composicion = load_data('composicion.csv')
# --- Configuración del mapa de Kepler.gl ---
config_mapa = {
    "version": "v1",
    "config": {
        "visState": {
            "filters": [],
            "layers": [
                {
                    "id": "ju8rai",
                    "type": "geojson",
                    "config": {
                        "dataId": "-42kwdt",
                        "columnMode": "geojson",
                        "label": "precios_clean",
                        "color": [130, 154, 227],
                        "highlightColor": [252, 242, 26, 255],
                        "columns": {"geojson": "geometry"},
                        "isVisible": True,
                        "visConfig": {
                            "opacity": 0.8,
                            "strokeOpacity": 0.8,
                            "thickness": 3.4,
                            "strokeColor": None,
                            "colorRange": {
                                "colors": ["#F7F4F9", "#DCC9E2", "#D08AC2", "#E33890", "#B70B4F", "#67001F"],
                                "name": "PuRd",
                                "type": "sequential",
                                "category": "ColorBrewer"
                            },
                            "strokeColorRange": {
                                "name": "Global Warming",
                                "type": "sequential",
                                "category": "Uber",
                                "colors": ["#4C0035", "#880030", "#B72F15", "#D6610A", "#EF9100", "#FFC300"]
                            },
                            "radius": 13.7,
                            "sizeRange": [0, 10],
                            "radiusRange": [0, 50],
                            "heightRange": [0, 500],
                            "elevationScale": 5,
                            "stroked": False,
                            "filled": True,
                            "enable3d": False,
                            "wireframe": False,
                            "fixedHeight": False
                        },
                        "hidden": False,
                        "textLabel": [
                            {
                                "field": None,
                                "color": [255, 255, 255],
                                "size": 18,
                                "offset": [0, 0],
                                "anchor": "start",
                                "alignment": "center",
                                "outlineWidth": 0,
                                "outlineColor": [255, 0, 0, 255],
                                "background": False,
                                "backgroundColor": [0, 0, 200, 255]
                            }
                        ]
                    },
                    "visualChannels": {
                        "colorField": {"name": "price", "type": "integer"},
                        "colorScale": "quantize",
                        "strokeColorField": None,
                        "strokeColorScale": "quantile",
                        "sizeField": None,
                        "sizeScale": "linear",
                        "heightField": None,
                        "heightScale": "linear",
                        "radiusField": None,
                        "radiusScale": "linear"
                    }
                },
                {
                    "id": "92v23lj",
                    "type": "geojson",
                    "config": {
                        "dataId": "ecbukq",
                        "columnMode": "geojson",
                        "label": "beijing_services",
                        "color": [246, 209, 138],
                        "highlightColor": [252, 242, 26, 255],
                        "columns": {"geojson": "_geojson"},
                        "isVisible": True,
                        "visConfig": {
                            "opacity": 0.77,
                            "strokeOpacity": 0.8,
                            "thickness": 2.1,
                            "strokeColor": [36, 115, 189],
                            "colorRange": {
                                "colors": ["#EE7733", "#0077BB", "#33BBEE", "#EE3377", "#CC3311", "#009988"],
                                "name": "Tol Vibrant",
                                "type": "qualitative",
                                "category": "ColorBlind"
                            },
                            "strokeColorRange": {
                                "name": "Global Warming",
                                "type": "sequential",
                                "category": "Uber",
                                "colors": ["#4C0035", "#880030", "#B72F15", "#D6610A", "#EF9100", "#FFC300"]
                            },
                            "radius": 0,
                            "sizeRange": [0, 10],
                            "radiusRange": [0, 50],
                            "heightRange": [0, 500],
                            "elevationScale": 5,
                            "stroked": False,
                            "filled": True,
                            "enable3d": False,
                            "wireframe": False,
                            "fixedHeight": False
                        },
                        "hidden": False,
                        "textLabel": [
                            {
                                "field": None,
                                "color": [255, 255, 255],
                                "size": 18,
                                "offset": [0, 0],
                                "anchor": "start",
                                "alignment": "center",
                                "outlineWidth": 0,
                                "outlineColor": [255, 0, 0, 255],
                                "background": False,
                                "backgroundColor": [0, 0, 200, 255]
                            }
                        ]
                    },
                    "visualChannels": {
                        "colorField": {"name": "amenity", "type": "string"},
                        "colorScale": "ordinal",
                        "strokeColorField": None,
                        "strokeColorScale": "quantile",
                        "sizeField": None,
                        "sizeScale": "linear",
                        "heightField": None,
                        "heightScale": "linear",
                        "radiusField": None,
                        "radiusScale": "linear"
                    }
                },
                {
                    "id": "2hrwpmd",
                    "type": "geojson",
                    "config": {
                        "dataId": "-kgmb4t",
                        "columnMode": "geojson",
                        "label": "beijing_metro",
                        "color": [87, 57, 33],
                        "highlightColor": [252, 242, 26, 255],
                        "columns": {"geojson": "_geojson"},
                        "isVisible": True,
                        "visConfig": {
                            "opacity": 0.8,
                            "strokeOpacity": 0.8,
                            "thickness": 8.9,
                            "strokeColor": [253, 236, 0],
                            "colorRange": {
                                "name": "Global Warming",
                                "type": "sequential",
                                "category": "Uber",
                                "colors": ["#4C0035", "#880030", "#B72F15", "#D6610A", "#EF9100", "#FFC300"]
                            },
                            "strokeColorRange": {
                                "name": "Global Warming",
                                "type": "sequential",
                                "category": "Uber",
                                "colors": ["#4C0035", "#880030", "#B72F15", "#D6610A", "#EF9100", "#FFC300"]
                            },
                            "radius": 10,
                            "sizeRange": [0, 10],
                            "radiusRange": [0, 50],
                            "heightRange": [0, 500],
                            "elevationScale": 0,
                            "stroked": True,
                            "filled": True,
                            "enable3d": False,
                            "wireframe": False,
                            "fixedHeight": False
                        },
                        "hidden": False,
                        "textLabel": [
                            {
                                "field": None,
                                "color": [255, 255, 255],
                                "size": 18,
                                "offset": [0, 0],
                                "anchor": "start",
                                "alignment": "center",
                                "outlineWidth": 0,
                                "outlineColor": [255, 0, 0, 255],
                                "background": False,
                                "backgroundColor": [0, 0, 200, 255]
                            }
                        ]
                    },
                    "visualChannels": {
                        "colorField": None,
                        "colorScale": "quantile",
                        "strokeColorField": None,
                        "strokeColorScale": "quantile",
                        "sizeField": None,
                        "sizeScale": "linear",
                        "heightField": None,
                        "heightScale": "linear",
                        "radiusField": None,
                        "radiusScale": "linear"
                    }
                }
            ],
            "effects": [],
            "interactionConfig": {
                "tooltip": {
                    "fieldsToShow": {
                        "-42kwdt": [
                            {
                                "name": "Lng",
                                "format": None
                            },
                            {
                                "name": "Lat",
                                "format": None
                            }
                        ],
                        "-kgmb4t": [
                            {
                                "name": "@id",
                                "format": None
                            },
                            {
                                "name": "area",
                                "format": None
                            },
                            {
                                "name": "indoor",
                                "format": None
                            },
                            {
                                "name": "layer",
                                "format": None
                            },
                            {
                                "name": "level",
                                "format": None
                            }
                        ],
                        "ecbukq": [
                            {
                                "name": "@id",
                                "format": None
                            },
                            {
                                "name": "amenity",
                                "format": None
                            },
                            {
                                "name": "name",
                                "format": None
                            },
                            {
                                "name": "name:zh",
                                "format": None
                            },
                            {
                                "name": "name:zh-Hans",
                                "format": None
                            }
                        ],
                        "3wuqo5": [
                            {
                                "name": "url",
                                "format": None
                            },
                            {
                                "name": "id",
                                "format": None
                            },
                            {
                                "name": "Lng",
                                "format": None
                            },
                            {
                                "name": "Lat",
                                "format": None
                            },
                            {
                                "name": "Cid",
                                "format": None
                            }
                        ]
                    },
                    "compareMode": False,
                    "compareType": "absolute",
                    "enabled": False
                },
                "brush": {"size": 0.5, "enabled": False},
                "geocoder": {"enabled": False},
                "coordinate": {"enabled": False}
            },
            "layerBlending": "normal",
            "overlayBlending": "normal",
            "splitMaps": [],
            "animationConfig": {"currentTime": None, "speed": 1},
            "editor": {"features": [], "visible": True}
        },
        "mapState": {
            "bearing": 0,
            "dragRotate": False,
            "latitude": 39.92836694172162,
            "longitude": 116.3764795575669,
            "pitch": 0,
            "zoom": 9.827295162832453,
            "isSplit": False,
            "isViewportSynced": True,
            "isZoomLocked": False,
            "splitMapViewports": []
        },
        "mapStyle": {
            "styleType": "satellite",
            "topLayerGroups": {},
            "visibleLayerGroups": {
                "label": True,
                "road": True,
                "border": True,
                "building": True,
                "water": True,
                "land": True,
                "3d building": False
            },
            "threeDBuildingColor": [4.179000818945631, 7.370237807958659, 14.816457448989057],
            "backgroundColor": [0, 0, 0],
            "mapStyles": {}
        },
        "uiState": {
            "mapControls": {
                "mapLegend": {
                    "active": True,
                    "settings": {
                        "position": {"x": 35, "anchorX": "right", "y": 66, "anchorY": "bottom"},
                        "contentHeight": 351.8125
                    }
                }
            }
        }
    }
}
# --- Creación de gráficos ---
def update_fig_layout(fig, y_title):
    fig.update_traces(mode='lines+markers', marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(xaxis_title='Año', yaxis_title=y_title)
    return fig

fig_migracion = update_fig_layout(px.line(migracion, x='Year', y='Net Migration', title='Migración neta de China'), 'Migración neta')
fig_crecimiento = update_fig_layout(px.line(crecimiento, x='Año', y='Tasa_crecimiento', title='Crecimiento urbano de China'), 'Tasa de crecimiento urbano(%)')
fig_pib = update_fig_layout(px.line(pib, x='Año', y='Tasa PIB', title='Tasa de crecimiento del PIB de China'), 'Tasa PIB(%)')

# Gráficos de composición de vivienda
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
     # Inicializar el mapa de Kepler.gl con la configuración
   kepler_map = KeplerGl(height=600, config=config_mapa)
 
     # Agregar datos al mapa
   if beijing_services_gdf is not None:
       kepler_map.add_data(data=beijing_services_gdf, name='ecbukq')
   if beijing_metro_gdf is not None:
       kepler_map.add_data(data=beijing_metro_gdf, name='-kgmb4t')
   if precios_clean_df is not None:
       kepler_map.add_data(data=precios_clean_df, name='-42kwdt')
 
     # Mostrar el mapa en Streamlit
   keplergl_static(kepler_map)
 
 # Expanders para información adicional (opcional)
 # with st.expander("Información sobre Migración"):
# Expanders para información adicional (opcional)
# with st.expander("Información sobre Migración"):
#     st.write("Datos de migración neta de China desde 1990.")

# with st.expander("Información sobre Crecimiento Urbano"):
#   st.write("Tasa de crecimiento urbano de China.")

# with st.expander("Información sobre el PIB"):
#   st.write("Tasa de crecimiento del Producto Interno Bruto de China.")

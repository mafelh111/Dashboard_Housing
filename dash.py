import pandas as pd
import plotly.express as px
import streamlit as st

# Carga y procesa los datos de migración
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

# Carga y procesa los datos de crecimiento urbano
crecimiento = pd.read_csv('Crecimiento_urbano.csv', sep=',')
crecimiento = crecimiento.T
crecimiento = crecimiento.reset_index()
crecimiento.columns = crecimiento.iloc[3]
crecimiento = crecimiento[4:]
crecimiento = crecimiento.rename(columns={'CHN': 'Tasa_crecimiento', 'Country Code': 'Año'})
crecimiento = crecimiento.dropna(axis=1, how='any')
crecimiento['Año'] = crecimiento['Año'].str.extract('(\d+)').astype(int)

# Carga y procesa los datos del PIB
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

# Crea las figuras de Plotly Express
fig_migracion = px.line(migracion, x='Year', y='Net Migration', title='Migración neta de China')
fig_crecimiento = px.line(crecimiento, x='Año', y='Tasa_crecimiento', title='Crecimiento urbano de China')
fig_pib = px.line(pib, x='Año', y='Tasa PIB', title='Tasa de crecimiento del PIB de China')

# Actualiza el diseño de las figuras
def update_fig_layout(fig, y_title):
    fig.update_traces(mode='lines+markers', marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(
        xaxis_title='Año',
        yaxis_title=y_title,
        xaxis=dict(tickvals=fig.data[0]['x'].tolist(), tickangle=45)
    )
    return fig

fig_migracion = update_fig_layout(fig_migracion, 'Migración neta')
fig_crecimiento = update_fig_layout(fig_crecimiento, 'Tasa de crecimiento urbano(%)')
fig_pib = update_fig_layout(fig_pib, 'Tasa PIB(%)')

# Muestra los gráficos en Streamlit
st.title('Tablero de China')
st.write('Este tablero muestra la migración neta, el crecimiento urbano y la tasa de crecimiento del PIB de China.')
st.plotly_chart(fig_migracion)
st.plotly_chart(fig_crecimiento)
st.plotly_chart(fig_pib)
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import graph_objs as go
import matplotlib.pyplot as plt

st.title("🌎 Covid19: Dashboard Global📊")
st.markdown("Dados Mundial sobre os novos casos e novos Óbitos com COVID-19")
st.divider()

##### Dados Global Agrupado ######################################################
#load data
@st.cache_data
def load_data():
    data = pd.read_csv("data/covid19-world.csv")
    return data

df = load_data()


#DataFrame
if st.sidebar.checkbox("🧾 Mostrar Dados", False, key=1):
    st.write("🌐 Dados agrupados por continente")
    df_group = df.groupby("Continent")[["Confirmed", "New cases", "Deaths", "New deaths", "Population"]].sum().sort_values(by="Continent", ascending=True)
    df_result = pd.DataFrame(df_group).replace(np.NaN, 0)
    st.write(df_result)
    st.divider()

#Load Data expectativa x continente
@st.cache_data
def load_data():
    data = pd.read_csv("data/covid-world.csv")
    return data

df2 = load_data()

#Gráfico Casos milhares de habitantes x Expectativa de vida por continente
if st.sidebar.checkbox("📈 Mostrar Gráfico Expectativa de vida", False, key=2):
    if not st.checkbox('Ocultar gráfico', False, key=3):
        df_location = df2.loc[:, ['date','location', 'continent','life_expectancy', 'total_cases_per_million', 'population', 'total_cases']]
        st.markdown("Gráfico de Expectativa de vida por total de milhões de casos por continente")
        fig = px.scatter(df_location, x="life_expectancy", y="total_cases_per_million", 
                        size="population", color="continent",
                        hover_name="location", log_x=True, size_max=200)
                    
        st.plotly_chart(fig, theme='streamlit', use_container_width=True)


####################### Gráficos MAPAS GLOBAL##################################
    st.divider()
if st.sidebar.checkbox("🌎 Mostrar Gráfico World", False, key=4):    
    st.write("🌎 Gráfico Global de nº Casos Confirmados por país")
    if not st.checkbox('Ocultar gráfico', False, key=5):
        fig3 = px.choropleth(df,
                locations='iso_code',
                color="Confirmed",
                hover_name="Country",
                color_continuous_scale="RdYlGn",
                animation_frame="Date" )
        st.plotly_chart(fig3, theme='streamlit', use_container_width=True)

    st.divider()
    st.write("🌎 Gráfico Global de nº de Óbitos por país")
    if not st.checkbox('Ocultar gráfico', False, key=6):
        fig4 = px.choropleth(df,
                    locations='iso_code',
                    color="Deaths",
                    hover_name="Country",
                    color_continuous_scale="Viridis",
                    animation_frame="Date" )
        st.plotly_chart(fig4, theme='streamlit', use_container_width=True)

    st.divider()
    st.write("🌎 Gráfico Global de Novos casos por país")
    if not st.checkbox('Ocultar gráfico', False, key=7):
        fig5 = px.choropleth(df,
                locations='iso_code',
                color="New cases",
                hover_name="Country",
                color_continuous_scale="Blues",
                animation_frame="Date" )
        st.plotly_chart(fig5, theme='streamlit', use_container_width=True)

    st.divider()
    st.write("🌎 Gráfico Global de Novos Óbitos por país")
    if not st.checkbox('Ocultar gráfico', False, key=8):
        fig5 = px.choropleth(df,
                locations='iso_code',
                color="New deaths",
                hover_name="Country",
                color_continuous_scale="Viridis",
                animation_frame="Date" )
        st.plotly_chart(fig5, theme='streamlit', use_container_width=True) 


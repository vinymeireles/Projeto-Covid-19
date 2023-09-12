import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import graph_objs as go
import matplotlib.pyplot as plt

#Apps
st.set_page_config(page_title="App Covid 19", page_icon= ":bar_chart:")
st.title("💉Covid19: Dashboard Analytics📊")

#load data
@st.cache_data
def load_data():
    data = pd.read_csv("data/covid-world.csv")
    return data

df = load_data()

#Performance data cleaning and grouping
data = df.loc[(df["location"] != 'World') & (df["location"] != 'Africa') & 
    (df["location"] != 'Asia') & (df["location"] != 'Europe') &
    (df["location"] != 'European Union') & (df["location"] != 'North America') & 
    (df["location"] != 'Northern Cyprus') & (df["location"] != 'Northern Ireland')]


#Group data based on location and replace 'NaN' values with zeros
df_category = data[['location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']]

df_group = df_category.groupby("location")[["location", "date", "total_cases", "new_cases", "total_deaths", "new_deaths"]].max()

df_result = pd.DataFrame(df_group).replace(np.NaN, 0)

st.markdown("""Essa aplicação demonstra uma análise exploratória dos dados COVID-19 fornecidos pela Our World in Data (OWID) é feita, mostrando o avanço temporal de casos, óbitos e vacinação. 
Estudos comparativos e busca de correlações são feitos com intuito de melhor compreender os dados. Animações como a mostrada acima serão criadas e interpretadas. Nessa seção poderá realizar consultas
no DataFrame mundial, mostrar índices dos país com maiores casos, gráficos de expectativa de vida x total de casos e gráfico global, demonstrando várias estatísticas da doença.""")
st.image("img/logo WHO.png", width=80)

#Create Table Plotly
#from plotly.figure_factory import create_table
#colorscale = [[0, '#4d004c'], [.5, '#f2e5ff'], [1, '#ffffff']]
#table = create_table((df_result), colorscale=colorscale)


#Visualizar DataFrame original
if st.sidebar.checkbox("🧾 Mostrar DataFrame", False, key=0):
    st.markdown("Dados Mundial sobre COVID-19 (coronavírus)")
    with st.expander("🗓 Visualizar DataFrame Original"):
        st.write(df_result)

st.divider()

# Obtenha nomes de índices para os quais a coluna Location tem valor Não
indexNames = df[df['location'] == 'World'].index

# Exclua esses índices de linha do dataFrame
df.drop(indexNames , inplace=True)

#10 Países com o maior índice de casos confirmados
if st.sidebar.checkbox(" 🔟 Mostrar índices", False, key=1):
    st.write('10 Países com o maior índice de casos: 📊')
    df_group10 = df_category.groupby("location")["total_cases"].max()
    top_10_population = pd.DataFrame(df_group10).sort_values(by="total_cases", ascending=False)[:10]
    st.write(top_10_population, use_container_width=True)

#Gráfico 10 top
    if not st.checkbox('Ocultar gráfico 1', False, key=2):
        st.write('Gráfico dos 10 Países com o maior índice de casos: ')
        data2 = df_category.groupby("location")["location", "total_cases"].max().sort_values(by="total_cases", ascending=False)[:10]
        fig2 = px.bar(data2, x= "location" , y="total_cases", color="total_cases")
        st.plotly_chart(fig2)


   
#### Logo sidebar######
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.image("img/logo.png", caption="Data Analytics")
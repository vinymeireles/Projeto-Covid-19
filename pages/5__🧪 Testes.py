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

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


st.title("🌎 Covid19: Dashboard Global📊")
st.markdown("Dados de Testes para soro positivo do COVID-19")
st.divider()

##### Dados Global Agrupado ######################################################
#load data
@st.cache_data
def load_data():
    data = pd.read_csv("data/testing.csv")
    return data

df = load_data()

#Agrupar dados
df_group = df.groupby("location")[["location", "total_tests", "new_tests", "total_tests_per_thousand", "cumulative_positivity_rate", "testing_observations"]].max()

#df_result = pd.DataFrame(df_group).replace(np.NaN, 0) > preenche os valores NaN em 0
df_result = pd.DataFrame(df_group.dropna(axis=0))      # exclui todas as linhas com valores nulos NaN


#Selecionar por país
country_select = st.sidebar.selectbox('🔎 Selecionar a Localização:', df_result['location'])
select_country = df_result[df_result['location'] == country_select]

#Função para visualizar os resultados filtrados por país
def get_testing_analysis(dataresult):
    total_res = pd.DataFrame({'Status': ['Total testes', 'Novos testes', 'Total de testes por mil', 'taxa de positividade cumulativa','Testando observações'],
                            'Figure':(dataresult.iloc[0]['total_tests'], dataresult.iloc[0]['new_tests'], dataresult.iloc[0]['total_tests_per_thousand'], 
                                     dataresult.iloc[0]['cumulative_positivity_rate'], dataresult.iloc[0]['testing_observations'])
                            })
    return total_res

total_country = get_testing_analysis(select_country)      


# Data Visualization
location_total_tests = total_country.Figure[0]
location_new_tests = total_country.Figure[1]
location_total_tests_1000 = total_country.Figure[2]
location_cumulative_rate_positive = total_country.Figure[3]
location_tests_observation = total_country.Figure[4]

#DataFrame
if st.sidebar.checkbox("🧾 Mostrar Dados", False, key=0):
    st.write("🌐 Dados agrupados de Testes realizado por País")
    st.write(df_result)
    st.divider()
  
#Informações em colunas dos resultados
if st.sidebar.checkbox("📝 Mostrar análise por localização", False, key=1):
    st.markdown("📊 Análise de teste de casos por país:")

    # 1ª linha dos resultados dos dados
    col1, col2, col3 = st.columns(3)
    col1.text("📍Localização:")
    col1.info(country_select)
    col2.text("🧪 Total Testes:")
    col2.info(f"{location_total_tests:,}")
    col3.text("🧪 Total Novos Testes:")
    col3.info(f"{location_new_tests:,}")
    
    # 2ª linha dos resultados dos dados
    col1, col2, col3 = st.columns(3)
    col1.text(" Total Teste por mil:")
    col1.info(f"{location_total_tests_1000:,}")
    col2.text("TX positivo:")
    col2.info(f"{location_cumulative_rate_positive:,}")
    col3.text(" Testando Observações:")
    col3.info(f"{location_tests_observation:,}")
   




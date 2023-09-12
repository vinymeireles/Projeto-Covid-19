import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import graph_objs as go
import matplotlib.pyplot as plt


#Apps
st.set_page_config(page_title="App Covid 19", page_icon= ":bar_chart:")
st.title("Covid19: Dashboard Casos Hospitalizados 🏥")
st.markdown("Dados Mundial sobre os casos de pessoas hospitalizadas com COVID-19")

#load data
@st.cache_data
def load_data():
    data = pd.read_csv("data/hospitalizations.csv")
    return data

df = load_data()


## NOVO CÓDIGO EM TESTE *****************************************************************************

#Group data based on location and replace 'NaN' values with zeros
df_category = df[['entity', 'date', 'indicator', 'value']]
df_group = df_category.groupby("entity")['entity', 'date', 'indicator', 'value'].max()
df_result = pd.DataFrame(df_group).replace(np.NaN, 0)

#Selecionar por país
#st.sidebar.checkbox("Mostrar análise por localização", True, key=1)
country_select = st.sidebar.selectbox('🔎 Selecionar a Localização:', df_result['entity'])
select_country = df_result[df_result['entity'] == country_select]

#Função para visualizar os resultados filtrados por país
def get_hospitalizations_analysis(dataresult):
    total_res = pd.DataFrame({'Status': ['Data', 'Indicador', 'Valor'],
                            'Figure':(dataresult.iloc[0]['date'], dataresult.iloc[0]['indicator'], dataresult.iloc[0]['value'])
                        })
    return total_res

total_country = get_hospitalizations_analysis(select_country)  

# Data Visualisation
location_data = total_country.Figure[0]
location_indicator = total_country.Figure[1]
location_values = total_country.Figure[2]

#Visualizar DataFrame original
if st.sidebar.checkbox("🧾 Mostrar DataFrame", False, key=0):
    with st.expander("🗓 Visualizar DataFrame Original"):
        st.write(df_result)

st.divider()    

#Informações em colunas dos resultados
if st.sidebar.checkbox("📝 Mostrar análise por localização", False, key=1):
    st.markdown("📊 Análise de casos de internação por país:")

    # 1ª linha dos resultados dos dados
    col1, col2 = st.columns(2)
    col1.text("📍Localização:")
    col1.info(country_select)
    col2.text("📅 Data:")
    col2.info(f"{location_data}")
    
    # 2ª linha dos resultados dos dados
    col1, col2 = st.columns(2)
    col1.text(" Indicador:")
    col1.info(f"{location_indicator}")
    col2.text(" Total de Internação:")
    col2.info(f"{location_values :,}")

    st.divider() 

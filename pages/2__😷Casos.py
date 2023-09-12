import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import graph_objs as go
import matplotlib.pyplot as plt


#Apps
st.set_page_config(page_title="App Covid 19", page_icon= ":bar_chart:")
st.title("💉Covid19: Dashboard Casos 🤒")
st.markdown("Dados Mundial sobre os casos confirmados e mortes COVID-19")

#load data
@st.cache_data
def load_data():
    data = pd.read_csv("data/cases_deaths.csv")
    return data

df = load_data()


#Performance data cleaning and grouping
data = df.loc[(df["location"] != 'World') & (df["location"] != 'Africa') & 
    (df["location"] != 'Asia') & (df["location"] != 'Europe') &
    (df["location"] != 'European Union') & (df["location"] != 'North America') & 
    (df["location"] != 'Northern Cyprus') & (df["location"] != 'Northern Ireland')]


#Group data based on location and replace 'NaN' values with zeros
df_category = data[['location', 'date', 'total_cases', 'new_cases','total_deaths','new_deaths', 'weekly_cases', 'weekly_deaths', 'biweekly_cases', 'biweekly_deaths']]

df_group = df_category.groupby("location")[["location", "date", "total_cases", "new_cases", "total_deaths", "new_deaths", "weekly_cases", "weekly_deaths", "biweekly_cases", "biweekly_deaths"]].max()

df_result = pd.DataFrame(df_group).replace(np.NaN, 0)

#Selecionar por país
#st.sidebar.checkbox("Mostrar análise por localização", True, key=1)
country_select = st.sidebar.selectbox('🔎 Selecionar a Localização:', df_result['location'])
select_country = df_result[df_result['location'] == country_select]

#Função para visualizar os resultados filtrados por país
def get_cases_analysis(dataresult):
    total_res = pd.DataFrame({'Status': ['Total casos', 'Novos casos', 'Total mortes', 'Novas mortes', 'Casos semanais', 'Mortes semanais', 'Casos quinzenais', 'Mortes quinzenais'],
                            'Figure':(dataresult.iloc[0]['total_cases'],  dataresult.iloc[0]['new_cases'], dataresult.iloc[0]['total_deaths'],  dataresult.iloc[0]['new_deaths'],
                                      dataresult.iloc[0]['weekly_cases'], dataresult.iloc[0]['weekly_deaths'], dataresult.iloc[0]['biweekly_cases'], dataresult.iloc[0]['biweekly_deaths'])
                            })
    return total_res

total_country = get_cases_analysis(select_country)  

# Data Visualization
location_total_cases = total_country.Figure[0]
location_new_cases = total_country.Figure[1]
location_total_deaths = total_country.Figure[2]
location_new_deaths = total_country.Figure[3]
location_weekly_cases = total_country.Figure[4]
location_weekly_deaths = total_country.Figure[5]
location_biweekly_cases = total_country.Figure[6]
location_biweekly_deaths = total_country.Figure[7]


#Visualizar DataFrame original
if st.sidebar.checkbox("🧾 Mostrar DataFrame", False, key=0):
    with st.expander("🗓 Visualizar DataFrame Original"):
        st.write(df_result)

st.divider()    

#Informações em colunas dos resultados
if st.sidebar.checkbox("📝 Mostrar análise por localização", False, key=1):
    st.markdown("📊 Análise de casos confirmados e mortes por país:")

    # 1ª linha dos resultados dos dados
    col1, col2, col3, col4 = st.columns(4)
    col1.text("📍Localização:")
    col1.info(country_select)
    col2.text("✅ Total casos:")
    col2.info(f"{location_total_cases:,.0f}")
    col3.text("😷 Novos casos:")
    col3.info(f"{location_new_cases:,.0f}")
    col4.text("✖ Total mortos:")
    col4.info(f"{location_total_deaths:,.0f}")

    # 2ª linha dos resultados dos dados
    col1, col2, col3, col4 = st.columns(4)
    col1.text("😢 Novas mortes:")
    col1.info(f"{location_new_deaths:,.0f}")
    col2.text("😷 Casos semanais:")
    col2.info(f"{location_weekly_cases:,.0f}")
    col3.text("💀 Mortes semanais:")
    col3.info(f"{location_weekly_deaths:,.0f}")
    col4.text("😷Casos quinzenais:")
    col4.info(f"{location_biweekly_cases:,.0f}")
    
    st.divider()   

#Função para retornar o totais de casos confirmados
def list_cases(data_cases):
    total_cases = pd.DataFrame({'Casos': ['Total casos', 'Novos casos','Casos semanais', 'casos quinzenais'],
                                'Totais':(data_cases.iloc[0]['total_cases'],  data_cases.iloc[0]['new_cases'], 
                                    data_cases.iloc[0]['weekly_cases'], data_cases.iloc[0]['biweekly_cases'])
                            })
    return total_cases

list1 = list_cases(select_country)  

#Função para retornar o totais de mortes confirmadas
def list_deaths(data_deaths):
    total_deaths = pd.DataFrame({'Mortes': ['Total mortes', 'Novas mortes','Mortes semanais', 'Mortes quinzenais'],
                                'Totais':(data_deaths.iloc[0]['total_deaths'], data_deaths.iloc[0]['new_deaths'], 
                                        data_deaths.iloc[0]['weekly_deaths'], data_deaths.iloc[0]['biweekly_deaths'])
                            })
    return total_deaths

list2 = list_deaths(select_country)  


#Visualização em Gráficos 1: CASOS CONFIRMADOS
if st.sidebar.checkbox("📊 Mostrar Gráficos", False, key=2):
    st.markdown("📊Visualização Gráfico por país")
    
    if not st.checkbox('Ocultar gráfico', False, key=3):
        st.markdown("CASOS: Casos confirmados, Novos casos, Casos semanais e" + " Casos quinzenais em %s." %(country_select))
        cases_total_graphs = px.bar(
            list1,
            x = 'Casos',
            y = 'Totais',
            labels={'Totais': 'Totais em %s ' % (country_select)},
            color='Casos')
        
        st.plotly_chart(cases_total_graphs)    
    
        st.divider()    

#Visualização em Gráficos 2: MORTES CONFIRMADAS
        st.markdown("Mortes: Total de Óbitos, Novos Óbitos, Mortes semanais e" + " Mortes quinzenais em %s." %(country_select))
        deaths_total_graphs = px.bar(
            list2,
            x = 'Mortes', 
            y = 'Totais',
            labels={'Totais': 'Totais em %s ' % (country_select)},
            color='Mortes')
        st.plotly_chart(deaths_total_graphs)    
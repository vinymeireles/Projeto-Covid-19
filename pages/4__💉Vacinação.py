import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import graph_objs as go
import matplotlib.pyplot as plt


st.title("💉Covid19 - Vacinação Update")
st.markdown("Dados atualizados da vacinação COVID-19 por país")

#load data
@st.cache_data
def load_data():
    data = pd.read_csv("data/vaccinations.csv")
    return data

df_vaccines = load_data()

#Performance data cleaning and grouping
data = df_vaccines.loc[(df_vaccines["location"] != 'World') & (df_vaccines["location"] != 'Africa') & 
    (df_vaccines["location"] != 'Asia') & (df_vaccines["location"] != 'Europe') &
    (df_vaccines["location"] != 'European Union') & (df_vaccines["location"] != 'North America') & 
    (df_vaccines["location"] != 'Northern Cyprus') & (df_vaccines["location"] != 'Northern Ireland')]

#Group data based on location and replace 'NaN' values with zeros
df_category = data[['location', 'date', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'daily_vaccinations', 'daily_people_vaccinated']]

df_group = df_category.groupby("location")[["location", "date", "total_vaccinations", "people_vaccinated", "people_fully_vaccinated", "daily_vaccinations", "daily_people_vaccinated"]].max()

df_result = pd.DataFrame(df_group).replace(np.NaN, 0)

    
#Selecionar por país
#st.sidebar.checkbox("Mostrar análise por localização", True, key=1)
country_select = st.sidebar.selectbox('🔎 Selecionar a Localização:', df_result['location'])
select_country = df_result[df_result['location'] == country_select]

#Função para visualizar os resultados filtrados por país
def get_vaccine_analysis(dataresult):
    total_res = pd.DataFrame({'Status': ['Total vacinação', 'Pessoas vacinadas', 'Pessoas totalmente vacinadas', 'Vacinação diárias', 'Pessoas diariamente vacinadas'],
                            'Figure':(dataresult.iloc[0]['total_vaccinations'], dataresult.iloc[0]['people_vaccinated'], dataresult.iloc[0]['people_fully_vaccinated'], 
                                      dataresult.iloc[0]['daily_vaccinations'], dataresult.iloc[0]['daily_people_vaccinated'])
                            })
    return total_res

total_country = get_vaccine_analysis(select_country)      

# Data Visualization
location_total_vaccinations = total_country.Figure[0]
location_people_vaccinated = total_country.Figure[1]
location_peple_fully_vaccinated = total_country.Figure[2]
location_daily_vaccinations = total_country.Figure[3]
location_daily_people_vaccinated = total_country.Figure[4]

#Visualizar DataFrame original
if st.sidebar.checkbox("🧾 Mostrar DataFrame", False, key=4):
    with st.expander("🗓 Visualizar DataFrame Original"):
        st.write(df_result)

st.divider()    

#Informações em colunas dos resultados
if st.sidebar.checkbox("📝 Mostrar análise por localização", False, key=1):
    st.markdown("📊 Análise de nível por país")
    col1, col2, col3 = st.columns(3)
    col1.text("📍Localização:")
    col1.info(country_select)
    col2.text("💉 Total Vacinação:")
    col2.info(f"{location_total_vaccinations:,.0f}")
    col3.text("💉 Vacinação diária")
    col3.info(f"{location_daily_vaccinations:,.0f}")

    col1, col2,col3 = st.columns(3)
    col1.text(" 👨‍👩‍👦‍👦 Nº pessoas vacinadas:")
    col1.info(f"{location_people_vaccinated:,.0f}")
    col2.text(" 👨‍👩‍👦‍👦 Pessoas totalmente vacinadas:")
    col2.info(f"{location_peple_fully_vaccinated:,.0f}")
    col3.text(" 👨‍👩‍👦‍👦 Pessoas diariamente vacinadas:")
    col3.info(f"{location_daily_people_vaccinated:,.0f}")
    
    st.divider()

#Visualização em Gráficos
if st.sidebar.checkbox("📊 Mostrar Gráfico", False, key=2):
    st.markdown("📊Visualização Gráfico por país")
    st.markdown("Total vacinação, Pessoas vacinadas e" + " Pessoas totalmente vacinadas em %s" %(country_select))
    if not st.checkbox('Ocultar gráfico', False, key=3):
        state_total_graphs = px.bar(
            total_country,
            x = 'Status',
            y = 'Figure',
            labels={'Figure': 'Totais em %s ' % (country_select)},
            color='Status')
        st.plotly_chart(state_total_graphs)    



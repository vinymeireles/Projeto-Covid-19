import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import graph_objs as go
import matplotlib.pyplot as plt
from keras.models import load_model
import warnings
warnings.filterwarnings("ignore")


st.title("📈Previsões de novos casos: 2020 - 2023")
st.markdown("Previsões futuras utilizando Inteligência Artificial para calcular novos casos de acordo com o tempo em dias.")

#load data
@st.cache_data
def load_data():
    data = pd.read_csv("data/covid19_days.csv")
    return data

table = load_data()

#agrupar os dados
cases = ['Confirmed', 'Deaths', 'Recovered', 'Active']
table['Active'] = table['Confirmed'] - table['Deaths'] - table['Recovered']
table[['Province/State']] = table[['Province/State']].fillna('')
table[cases] = table[cases].fillna(0)
latest = table[table['ObservationDate'] == max(table['ObservationDate'])].reset_index()

latest_grouped = latest['Confirmed'] - latest['Deaths'] - latest['Recovered']
latest_grouped = latest.groupby('Country/Region')[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum().reset_index()

#Visualizar DataFrame original
if st.sidebar.checkbox("🧾 Mostrar DataFrame", False, key=0):
    st.markdown("Dados agrupados sobre os casos confirmados, óbitos, recuperados e ativos COVID-19")
    with st.expander("🗓 Visualizar DataFrame Original"):
        st.write(latest_grouped)

st.divider()        

#Informações em colunas dos resultados
if st.sidebar.checkbox("📝 Mostrar análise por País", False, key=1):
    st.markdown("📊 Análise de casos confirmados, óbitos, recuperados e ativos por país:")
    
    #Selecionar por país
    country_select = st.selectbox('🔎 Selecionar o país:', latest_grouped['Country/Region'])
    select_country = latest_grouped[latest_grouped['Country/Region'] == country_select]
    st.divider()

    #Função para visualizar os resultados filtrados por país
    def get_cases_analysis(dataresult):
        total_res = pd.DataFrame({'Status': ['Confirmados', 'Óbitos', 'Recuperados', 'Ativos'],
                                'Figure':(dataresult.iloc[0]['Confirmed'],  dataresult.iloc[0]['Deaths'], dataresult.iloc[0]['Recovered'],  dataresult.iloc[0]['Active'])
                                })
        return total_res

    total_country = get_cases_analysis(select_country)  

    # Data Visualization
    location_confirmed = total_country.Figure[0]
    location_deaths = total_country.Figure[1]
    location_recovered = total_country.Figure[2]
    location_active = total_country.Figure[3]

    # 1ª linha dos resultados dos dados
    col1, col2, col3 = st.columns(3)
    col1.text("📍País:")
    col1.info(country_select)
    col2.text("😷 Casos Confirmados:")
    col2.info(f"{location_confirmed:,.0f}")
    col3.text("😢 Óbitos:")
    col3.info(f"{location_deaths :,.0f}")
  
    # 2ª linha dos resultados dos dados
    col1, col2 = st.columns(2)
    col1.text("🤩 Casos Recuperados:")
    col1.info(f"{location_recovered:,.0f}")
    col2.text("🤒 Casos semanais:")
    col2.info(f"{location_active:,.0f}")
    st.divider()   

### Agrupar os dados por dias(Days)
latest_grouped = latest.groupby('Country/Region')[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum().reset_index()
df = table.groupby('Days')[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum().reset_index()

### Gráficos agrupados por tempo (Days)########################################

#Visualização em Gráficos: CASOS CONFIRMADOS / ÓBITOS / RECUPERADOS / ATIVOS
if st.sidebar.checkbox("📊 Mostrar Gráficos", False, key=2):
    st.markdown("📈Visualização Gráfico Global por série temporal ")
    
    if not st.checkbox('Ocultar gráfico 1', False, key=3):
        graph1 = go.Figure()
        graph1.add_trace(go.Scatter(x=df.Days, y=df.Confirmed,mode='lines',name='Total confirmed cases', marker_color='blue'))
        graph1.update_layout(title='1. Taxa de infecção em relação ao tempo: Casos confirmados',xaxis_title='Dias',yaxis_title='Total casos confirmados',template='plotly_dark')
        st.plotly_chart(graph1)    
      
    if not st.checkbox('Ocultar gráfico 2', False, key=4):
        graph2 = px.line(df, x="Days", y="Deaths", title = '2. Taxa de casos de morte em relação ao tempo', template='plotly_dark')
        graph2.update_traces(line_color='red')
        st.plotly_chart(graph2)


    if not st.checkbox('Ocultar gráfico 3', False, key=5):
        graph3 = px.line(df, x="Days", y="Deaths", title = '3. Taxa de casos recuperados em relação ao tempo', template='plotly_dark')
        graph3.update_traces(line_color='green')
        st.plotly_chart(graph3)
       
    if not st.checkbox('Ocultar gráfico 4', False, key=6):
        graph4 = px.line(df, x="Days", y="Active", title = '4. Taxa de casos ativos (confirmados - óbitos - recuperados) em relação ao tempo', template='plotly_dark')
        graph4.update_traces(line_color='yellow')
        st.plotly_chart(graph4)
        st.divider()

    #Gráfico de barras: Top 10 dos países com maior número de óbitos confirmados:
    if not st.checkbox('Ocultar gráfico 5', False, key=7):
        latest_grouped = latest.groupby('Country/Region')[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum().reset_index()
        pred = latest_grouped.sort_values(by='Active', ascending=False)[:10]
        fig = px.bar(pred, x='Active', y='Country/Region',
                    hover_data=['Active'], color='Active',
                    labels={},orientation='h', height=800, width=650)
        fig.update_layout(title_text='10 Países com maiores casos ativos!')
        st.plotly_chart(fig)   

# Previsões futuras de novos casos em relação ao tempo (Days)
if st.sidebar.checkbox("⏰ Previsões Futuras", False, key=8):
    st.markdown("📈 Visualização dos resultados das previsões em relação ao tempo IA (Deep Learning)")

    lstm_data = table.groupby('ObservationDate')[['Confirmed', 'Deaths', 'Recovered']].sum().reset_index()
    st.write(lstm_data)

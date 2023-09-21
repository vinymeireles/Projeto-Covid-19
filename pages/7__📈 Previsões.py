import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from datetime import timedelta, date

#Apps
st.set_page_config(page_title="App Covid 19", page_icon= ":bar_chart:")
st.title("💉Covid19: Dashboard Analytics📊")

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

st.title("📈Previsões de novos casos: 2020 - 2023")
st.markdown("""Previsões futuras utilizando Inteligência Artificial para calcular novos casos de acordo com o tempo em dias. Visualização dos resultados das previsões em relação ao tempo IA (Deep Learning)""")

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

################################################################################
# Previsões futuras de novos casos em relação ao tempo (Days)
if st.sidebar.checkbox("⏰ Previsões no Brasil", False, key=8):
    st.markdown("🌎 Dados de evolução do Covid19 no Brasil")

    with st.expander("🗓 Visualizar o DataFrame dos casos confirmado por dia no BRASIL"):
        df_brasil = table.loc[table['Country/Region'] == 'Brazil'].reset_index().drop(columns=['Country/Region','SNo', 'Province/State','index','Last Update'], axis=1)
        df_brasil['ObservationDate'] = pd.to_datetime(df_brasil['ObservationDate'] , format="%m/%d/%Y").dt.strftime('%Y-%m-%d')
        df_brasil2 = df_brasil[df_brasil.Confirmed > 0]
        st.dataframe(df_brasil2, use_container_width=True)
    st.divider()    

    #Visualização do gráfico no Brasil por dia: Casos Confirmados
    st.markdown(" 📊Visualização Gráfico dos casos confirmados no Brasil")
    if not st.checkbox('Ocultar gráfico 1', False, key=9):
        fig = px.line(df_brasil2, x='Days', y='Confirmed',
                labels={'Days':'Dias', 'Confirmed':'Número de casos confirmados'},
                title='Casos confirmados no Brasil', width=800, height=400)

        fig.update_layout(
            margin=dict(l=30, r=20, t=60, b=5),
            font=dict(size=15, color='black')
        )
        st.plotly_chart(fig)
    st.divider()     

    #Função para fazer a contagem de novos casos:
    #[Subtração entre o número de casos de um dia e o dia anterior]
    def dif(v):
        J=[v[i+1]-v[i] for i in range(len(v)-1)]
        J.insert(0, v[0])
        return J

    def dif2(v):
        J=[v[0]]
        for i in range(len(v)-1):
            J.append(v[i+1]-v[i])
        return np.array(J)

    df_brasil2 = df_brasil2.assign(novoscasos=dif(df_brasil2['Confirmed'].values))
    df_brasil2 = df_brasil2[df_brasil2.novoscasos > 0]
    
    #Visualização do gráfico no Brasil por dia: Casos Confirmados
    if not st.checkbox('Ocultar gráfico 2', False, key=10):
        graph1 = px.line(df_brasil2, x="Days", y="novoscasos", title = 'Novos casos confirmado no Brasil', template='plotly_dark')
        graph1.update_traces(line_color='yellow')
        st.plotly_chart(graph1)
        st.divider() 

    #Visualização do gráfico no Brasil por dia: óbitos
    if not st.checkbox('Ocultar gráfico 3', False, key=11):
        fig2 = go.Figure()
        fig2.add_trace(
        go.Scatter(x=df_brasil2.Days, y=df_brasil2.Deaths,
                name='Óbitos', mode='lines+markers', line=dict(color='red'))
        )

        fig2.update_layout(title='Mortes por COVID-19 no Brasil',
                    xaxis_title='Dias', yaxis_title='Número de Óbitos',
                    margin=dict(l=30, r=30, t=50, b=5),
                    width=1000, height=400, font=dict(size=16))
        st.plotly_chart(fig2)
        st.divider()
##############################################################################################################################################################
   

#Previsões de novos casos baseados em Machine Learning.  
if st.sidebar.checkbox("⏳ Previsões no Mundo", False, key=12):
    
    @st.cache_data
    def load_data1():
        data1 = pd.read_csv("data/cases_world.csv")
        return data1

    df_world= load_data1()
    
    st.markdown("🌍 Dados de Previsão de novos casos do Covid19 no Mundo entre [03/01/2020] - [30/08/2023]")

    with st.expander("🗓 Visualizar o DataFrame dos casos confirmado por dia no Mundo"):
        st.dataframe(df_world, use_container_width=True)

    df_world = df_world[['days','cases']]    
    st.divider()
    #### PREPARE DATA ####
    x = np.array(df_world['days']).reshape(-1, 1)
    y = np.array(df_world['cases']).reshape(-1, 1)
    polyFeat = PolynomialFeatures(degree=3)
    x = polyFeat.fit_transform(x)
    
    #### TRAINING DATA ####
    model = linear_model.LinearRegression()
    model.fit(x,y)
    accuracy = model.score(x,y)
    st.markdown('🎯Accurácia de acerto do modelo de Machine Learning - IA')
    st.info(f'Accuracy: {round(accuracy*100,3)} %')
    y0 = model.predict(x)
    st.divider()

    #### PREDICTION ####
    st.subheader("Previsões de novos casos")
    days = st.slider('Selecione o número de dias:', 15, 90, 30)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"📆 Previsão de novos casos após {days} dias.")
    with col2:    
        total_cases = (round(int(model.predict(polyFeat.fit_transform([[234+days]])))/1000000,2))
        st.info(f"📝 {total_cases} Milhões de casos.")
    with col3:
        dt_fin = '30/08/2023'
        date2= (pd.to_datetime(dt_fin) + pd.DateOffset(days)).date().strftime('%d/%m/%Y')
        st.info(f"📆 Data da previsão: {date2}")


    x1 = np.array(list(range(1, 234+days))).reshape(-1,1)
    y1 = model.predict(polyFeat.fit_transform(x1))
    
    st.divider()
    #Visualização do gráfico no Brasil por dia: Casos Confirmados
    st.markdown("📈 Gráfico de novos casos x dias")
    if not st.checkbox('Ocultar gráfico', False, key=10):
        fig3 = plt.figure(figsize=(8,8))
        plt.style.use("dark_background")
        plt.xlabel('Dias')
        plt.ylabel('Milhão de Casos')
        plt.title("Previsão de novos casos de Covid 19 Mundial após x dias")
        plt.plot(y1,'b')
        plt.plot(y0,'r')
        st.pyplot(fig3)

    
  
      
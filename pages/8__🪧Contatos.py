import streamlit as st
import streamlit.components.v1 as components


st.markdown("<h2 style='text-align: center; color: red;'>🪧 Contatos</h2>", unsafe_allow_html=True)


st.markdown("Para desenvolvimento de novos projeto - Dashboard utilizando Inteligência Articial: Machine Learning")
st.divider()
st.markdown("")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image("icons/whatsapp.png", caption="28 99918-3961", width=90)

with col2:
    st.image("icons/gmail.png", caption="viniciusmeireles@gmail.com", width=100)

with col3:
    st.image("icons/location.png", caption="Vitória/ES", width=90)    

with col4:
    st.image("icons/linkedin.png",caption= "/pviniciusmeireles", width=90)


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
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.image("img/logo.png")
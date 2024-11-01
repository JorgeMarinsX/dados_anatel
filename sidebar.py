import streamlit as st
import user

if 'authentication_status' not in st.session_state:
    st.error("Impossível exibir informações sem estar conectado")
else:
    nome = st.session_state['nome']

def renderSidebar():
    nome = st.session_state['nome']
    st.header(f"Seja bem-vindo(a), {nome}")
    sair = st.button("Sair", use_container_width=True)

    if sair:
        user.logOut()
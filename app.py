import streamlit as st
import pageconfig
pageconfig.pagConfig()
import user
import front
import sidebar

if 'authentication_status' not in st.session_state or st.session_state['authentication_status'] != True:
    st.title("Faça login para acessar a dashboard")
    typed_username = st.text_input('Nome de usuário')
    typed_password = st.text_input("Senha", type='password')
    login_button = st.button('Login')
    if login_button:
        if user.login(typed_username, typed_password):
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error('Usuário ou senha inválidos')


elif st.session_state['authentication_status'] == True:
        front.mainDash()
        nome = st.session_state['nome']
        painel = st.sidebar
        with painel:
            sidebar.renderSidebar()




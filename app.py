import streamlit as st
import user
import front
import sidebar

st.set_page_config(layout='wide',
                                page_title='Supranet | Acompanhamento dados Anatel', 
                                page_icon='assets/dashboard.png',
                                menu_items={
                                    'Get help': None,
                                    'Report a bug': None,
                                    'About': None
                                    })

if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    col1, col2 = st.columns(2)
    with col1:
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

    with col2:
         st.image('assets/imagem_main.png', 'Desenvolvido por Equipe Supranet')
elif st.session_state['authentication_status']:
        front.mainDash()
        nome = st.session_state['nome']
        painel = st.sidebar
        with painel:
            sidebar.renderSidebar()




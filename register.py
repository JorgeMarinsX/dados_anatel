import streamlit as st
import user

def renderFormCadastro():

    st.header("Cadastrar novo usuário")
    formcadastro = st.form("cadastro")

    with formcadastro:
        nomeExibido = st.text_input("Nome de Exibição")
        username = st.text_input("Nome de usuário")
        email = st.text_input("Seu e-mail")
        password = st.text_input("Senha", type="password")
        level_options = ['Admin', 'Usuario']
        level = st.selectbox("Nível de acesso:", options=level_options)
        novousuario = st.form_submit_button("Cadastrar")

    if novousuario:
        cadastro = user.newUser(nomeExibido, email, username, password, level)
        if cadastro:
            st.success("Cadastrado com sucesso")




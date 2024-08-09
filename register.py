import streamlit as st
import pandas_gbq
import pandas
import user
import connect as ct

ct.connect()

def newUser(nomeExibido, email, username, password, level):
    password_hashed = user.hash_password(password)
    df = pandas.DataFrame(
        {
            'nomeexibido': [f'{nomeExibido}'],
            'email': [f'{email}'],
            'username': [f'{username}'],
            'password': [f'{password_hashed}'],
            'level': [f'{level}']
        }
    )
    pandas_gbq.to_gbq(df, 'dadosanatel-430317.dadosanatel072024.users', if_exists='append')

st.title("Criar novo usuário")

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
    cadastro = newUser(nomeExibido, email, username, password, level)
    st.success("Cadastrado com sucesso")




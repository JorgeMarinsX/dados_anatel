import streamlit as st
import pandas as pd
import dash
import query
import user
import register


def mainDash():
    st.title("Supranet | Estudo de Dados Anatel")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Geral', 'MENSAL: Ritmo de crescimento', 
                                        'ANUAL: Ritmo de crescimento', 'Indicadores Supranet', 
                                        'Tabelas', 'Cadastrar novo usuário'])
    with tab1:
        st.header('G5 em acessos por ano, considerando todas as cidades')
        st.plotly_chart(dash.crescimentoTodasAsCidades())
    
    with tab2:
        st.header('Acessos em relação aos principais concorrentes')
        st.plotly_chart(dash.graficoLinhaEmpresas(), use_container_width=True)

    with tab3:
        st.header('Gráfico de crescimento ano a ano')
    
        linhas1, barras1, mercado = st.tabs(['Visualizar em linhas', 'Visualizar em barras', 
                                             'Participação de mercado'])
    
        with linhas1:
            st.plotly_chart(dash.crescimentoLinhas())
    
        with barras1:
            st.plotly_chart(dash.crescimentoBarras())

        with mercado:
            st.plotly_chart(dash.participacaoDeMercado())

    with tab4:
        st.header('Crescimento Mensal Supranet')
        st.plotly_chart(dash.crescimentoSupranetMensal())

    with tab5:
        st.header('Tabela de crescimento geral por cidade')
        tabela = dash.tabelaGeral()
        st.write(tabela)

    with tab6:
        register.renderFormCadastro()

def updateUserForm():
    user_data = query.queryUserData(st.session_state['nome'])
    nomeExibicao = st.text_input("Nome de exibição", value=user_data['nomeexibido'].values[0])
    email = st.text_input("E-mail", value=user_data['email'].values[0])
    enviaForm = st.button("Enviar")

    df = pd.DataFrame(
            {
                'nomeexibido': [f'{nomeExibicao}'],
                'email': [f'{email}'],
            }
    )

    if enviaForm:
        user.updateUser(df)
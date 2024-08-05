import streamlit as st
import pageconfig
pageconfig.pagConfig()
import dash

st.title("Supranet | Estudo de Dados Anatel")

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Geral', 'MENSAL: Ritmo de crescimento', 
                                        'ANUAL: Ritmo de crescimento', 'Indicadores Supranet', 
                                        'Tabelas'])

with tab1:
    st.header('G5 em acessos por ano, considerando todas as cidades')
    st.plotly_chart(dash.crescimentoTodasAsCidades())
    
with tab2:
    st.header('Acessos em relação aos principais concorrentes')
    st.plotly_chart(dash.graficoLinhaEmpresas(), use_container_width=True)

with tab3:
    st.header('Gráfico de crescimento ano a ano')
    
    linhas1, barras1 = st.tabs(['Visualizar em linhas', 'Visualizar em barras'])
    
    with linhas1:
        st.plotly_chart(dash.crescimentoLinhas())
    
    with barras1:
        st.plotly_chart(dash.crescimentoBarras())

with tab4:
    st.header('Crescimento Mensal Supranet')
    st.plotly_chart(dash.crescimentoSupranetMensal())

with tab5:
    st.header('Tabela de crescimento geral por cidade')
    tabela = dash.tabelaGeral()
    st.write(tabela)
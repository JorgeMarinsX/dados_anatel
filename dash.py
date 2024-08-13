import streamlit as st
import plotly.express as px
import query


#FORMATAÇÃO E MÁSCARAS
def formataMeses():
    meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho',
                'Julho','Agosto','Setembro', 'Outubro','Novembro','Dezembro']
    return meses

#GRÁFICOS
#todas as funções recebem uma query e retornam um gráfico

#Geral
def totalAcessos():
    df = query.queryTotalAcessos()
    mes = df["Mês"].unique()
    meses = formataMeses()
    ano_selecionado = st.selectbox("Selecione um ano", df['Ano'].unique(), key=1)
    fig = px.line(df[df['Ano'] == ano_selecionado], x="Mês", y="Acessos", title='Acessos por mês', markers=True)
    fig.update_xaxes(title_text="Meses do ano", range=[0,13], fixedrange=True, tickvals=mes, ticktext=meses) 
    fig.update_yaxes(title_text="Acessos por mês", fixedrange=True)
    return fig

def crescimentoSupranetMensal():
    df = query.queryGeralNominal()
    mes = sorted(df["Mês"].unique())
    meses = formataMeses()

    # Converte os nomes das empresas para minúsculas
    df['Empresa'] = df['Empresa'].str.lower()

    df_supranet = df[df['Empresa'] == 'supranet telecom e informatica ltda']
    anos_possiveis = sorted(df_supranet['Ano'].unique())
    ano_selecionado = st.selectbox("Selecione um ano", anos_possiveis, key=7)


    
    # Filtra os dados para a empresa Supranet e o ano selecionado
    empresa = df_supranet[df_supranet['Ano'] == ano_selecionado]
    
    # Agrupa por mês e soma os acessos
    soma_acessos_mensal = empresa.groupby("Mês")['Acessos'].sum().reset_index()


    #Exporta o gráfico
    fig = px.line(soma_acessos_mensal, x="Mês", y="Acessos", title='Acessos por mês da Supranet', markers=True)
    fig.update_xaxes(title_text="Meses do ano", range=[0,13], fixedrange=True, tickvals=mes, ticktext=meses) 
    fig.update_yaxes(title_text="Acessos por mês", fixedrange=True)

    return fig

def tabelaGeral():
    df = query.queryGeralNominal()
    meses = formataMeses()

    ano_selecionado = st.selectbox("Selecione um ano", df['Ano'].unique())
    cidade_selecionada = st.selectbox("Selecione uma cidade", df['Município'].unique())
    
    # Filtra dados para o ano e cidade selecionados
    filtro_ano = df[(df['Ano'] == ano_selecionado) & (df['Município'] == cidade_selecionada)]
    
    # Agrupa os dados por empresa e mês, somando os acessos
    tabela_filtrada = filtro_ano.pivot_table(index='Empresa', columns='Mês', values='Acessos', aggfunc='sum', fill_value=0)

    # Ordena os meses corretamente
    tabela_filtrada = tabela_filtrada.reindex(columns=sorted(tabela_filtrada.columns))

    # Mapeia números dos meses para nomes dos meses
    tabela_filtrada.columns = [meses[mes - 1] for mes in tabela_filtrada.columns]

    return tabela_filtrada

def graficoLinhaEmpresas():
    df = query.queryGeralNominal()
   
    # Interface para seleção de ano e cidade
    ano_selecionado = st.selectbox("Selecione um ano", df['Ano'].unique(), key=10)
    cidade_selecionada = st.selectbox("Selecione uma cidade", df['Município'].unique(), key=11)
    
    # Filtra dados para o ano e cidade selecionados
    df_filtrado = df[(df['Ano'] == ano_selecionado) & (df['Município'] == cidade_selecionada)]
    
    # Agrupa os dados por empresa e mês, somando os acessos
    agrupado = df_filtrado.groupby(['Empresa', 'Ano', 'Mês'], as_index=False)['Acessos'].sum()
    
    # Calcula o total de acessos por empresa
    total_acessos_por_empresa = agrupado.groupby('Empresa')['Acessos'].sum().reset_index()
    
    # Seleciona as 10 principais empresas com mais acessos
    top_empresas = total_acessos_por_empresa.nlargest(10, 'Acessos')['Empresa']
    
    # Filtra o DataFrame para conter apenas as 10 principais empresas
    df_top = agrupado[agrupado['Empresa'].isin(top_empresas)]
    
    # Mapeia os números dos meses para nomes dos meses usando a lista 'meses'
    mes = sorted(df['Mês'].unique())
    meses = formataMeses()

    # Cria o gráfico de barras
    fig = px.bar(df_top, x='Mês', y='Acessos', color='Empresa', barmode='group',
                 title=f'Acessos por Mês para as 10 Principais Empresas em {cidade_selecionada} ({ano_selecionado})')
    fig.update_xaxes(type='category', tickvals=mes, ticktext=meses)  # Garante que os meses sejam tratados como categorias ordenadas
    fig.update_layout(height=800, legend=dict(yanchor='middle', xanchor='left', x=-0, y=-0.5))

    return fig

def tabelaRitmoCrescimento():
    df = query.queryGeralNominal()

    # Interface para seleção de ano e cidade
    ano_selecionado = st.selectbox("Selecione um ano", df['Ano'].unique(), key=12)
    cidade_selecionada = st.selectbox("Selecione uma cidade", df['Município'].unique(), key=13)

    df_agrupado = df.groupby(['Município', 'Empresa', 'Ano', 'Mês'], as_index=False)['Acessos'].sum()
    df_agrupado = df_agrupado.sort_values(by=['Empresa', 'Ano', 'Mês'])
    df_agrupado['Crescimento'] = df_agrupado.groupby(['Empresa'])['Acessos'].diff()
    
     # Filtragem dos resultados para o ano e cidade selecionados
    df_filtrado = df_agrupado[(df_agrupado['Ano'] == ano_selecionado) & (df_agrupado['Município'] == cidade_selecionada)]
    
    return df_filtrado

def crescimentoTodasAsCidades():
    df = query.queryGeralNominal()

    # Converter os nomes das empresas para minúsculas
    df['Empresa'] = df['Empresa'].str.upper()

    # Agrupa os dados por empresa e ano, encontrando o maior valor de acessos em cada ano
    agrupado = df.groupby(['Empresa', 'Ano'], as_index=False)['Acessos'].max()

    # Calcula o total de acessos por empresa
    total_acessos_por_empresa = agrupado.groupby('Empresa')['Acessos'].sum().reset_index()

    # Seleciona os 5 maiores provedores com base no total de acessos
    top_empresas = total_acessos_por_empresa.nlargest(5, 'Acessos')['Empresa']

    # Filtra o DataFrame para conter apenas os 5 maiores provedores
    df_top = agrupado[agrupado['Empresa'].isin(top_empresas)]

    # Gráfico de barras com anos no eixo X e acessos no eixo Y
    fig = px.bar(df_top, x='Ano', y='Acessos', color='Empresa', 
                 title='Comparativo dos 5 Maiores Provedores em Número de Acessos', barmode='group')
    fig.update_xaxes(ticks='inside')

    return fig
    
def crescimentoLinhas():
    df = query.queryGeralNominal()
    
    # Converter os nomes das empresas para maiúsculas
    df['Empresa'] = df['Empresa'].str.upper()
    
    # Interface para seleção de cidade
    cidade_selecionada = st.selectbox(label="Selecione uma cidade", options=df['Município'].unique(), key=15)

    # Filtra dados para a cidade selecionada
    df_filtrado = df[df['Município'] == cidade_selecionada]
    
    # Agrupa os dados por empresa, ano e mês, encontrando o maior valor de acessos em cada ano
    agrupado = df_filtrado.groupby(['Empresa', 'Ano', 'Mês'], as_index=False)['Acessos'].sum()
    
    # Seleciona o mês com o maior número de acessos para cada empresa e ano
    max_acessos_por_ano = agrupado.loc[agrupado.groupby(['Empresa', 'Ano'])['Acessos'].idxmax()]
    
    # Calcula o total de acessos por empresa (baseado no mês de maior acessos em cada ano)
    total_acessos_por_empresa = max_acessos_por_ano.groupby('Empresa')['Acessos'].sum().reset_index()
    
    # Seleciona as 5 principais empresas com mais acessos
    top_empresas = total_acessos_por_empresa.nlargest(5, 'Acessos')['Empresa']
    
    # Filtra o DataFrame para conter apenas as 5 principais empresas
    df_top = max_acessos_por_ano[max_acessos_por_ano['Empresa'].isin(top_empresas)]

    # Gráfico de linhas com anos no eixo X e acessos no eixo Y
    fig = px.line(df_top, x='Ano', y='Acessos', color='Empresa', 
                  title=f'Crescimento por Ano para as 5 Principais Empresas em {cidade_selecionada}', markers=True)
    fig.update_xaxes(ticks='inside')
    
    return fig

def crescimentoBarras():
    df = query.queryGeralNominal()
    
    # Converter os nomes das empresas para maiúsculas
    df['Empresa'] = df['Empresa'].str.upper()
    
    # Interface para seleção de cidade
    cidade_selecionada = st.selectbox(label="Selecione uma cidade", options=df['Município'].unique(), key=17)

    # Filtra dados para a cidade selecionada
    df_filtrado = df[df['Município'] == cidade_selecionada]
    
    # Agrupa os dados por empresa, ano, mês, tecnologia e meio de acesso, somando os acessos totais
    agrupado = df_filtrado.groupby(['Empresa', 'Ano', 'Mês', 'Tecnologia', 'Meio de Acesso'], as_index=False)['Acessos'].sum()
    
    # Seleciona o mês com o maior número de acessos para cada combinação de empresa, ano, tecnologia e meio de acesso
    max_acessos_por_ano = agrupado.loc[agrupado.groupby(['Empresa', 'Ano', 'Tecnologia', 'Meio de Acesso'])['Acessos'].idxmax()]
    
    # Calcula o total de acessos por empresa (baseado no mês de maior acessos em cada ano)
    total_acessos_por_empresa = max_acessos_por_ano.groupby('Empresa')['Acessos'].sum().reset_index()
    
    # Seleciona as 5 principais empresas com mais acessos
    top_empresas = total_acessos_por_empresa.nlargest(5, 'Acessos')['Empresa']
    
    # Filtra o DataFrame para conter apenas as 5 principais empresas
    df_top = max_acessos_por_ano[max_acessos_por_ano['Empresa'].isin(top_empresas)]

    # Gráfico de barras com anos no eixo X e acessos no eixo Y
    fig = px.bar(df_top, x='Ano', y='Acessos', color='Empresa', 
                 title=f'Crescimento por Ano para as 5 Principais Empresas em {cidade_selecionada}', barmode='group')
    fig.update_xaxes(ticks='inside')
    
    return fig

def participacaoDeMercado():
    df = query.queryGeralNominal()
    
    # Converter os nomes das empresas para maiúsculas
    df['Empresa'] = df['Empresa'].str.upper()
    
    # Interface para seleção de cidade e ano
    cidade_selecionada = st.selectbox(label="Selecione uma cidade", options=df['Município'].unique(), key=18)
    ano_selecionado = st.selectbox(label="Selecione um ano", options=df['Ano'].unique(), key=16)
    
    # Filtra dados para a cidade e ano selecionados
    df_filtrado = df[(df['Município'] == cidade_selecionada) & (df['Ano'] == ano_selecionado)]
    
    # Agrupa os dados por empresa, somando os acessos totais (considerando todas as tecnologias e meios de acesso)
    total_acessos_por_empresa = df_filtrado.groupby('Empresa')['Acessos'].sum().reset_index()
    
    # Seleciona as 5 principais empresas com mais acessos
    top_empresas = total_acessos_por_empresa.nlargest(5, 'Acessos')

    # Calcula a participação de mercado
    top_empresas['Participacao'] = (top_empresas['Acessos'] / top_empresas['Acessos'].sum()) * 100
    
    # Gráfico de pizza mostrando a porcentagem de participação de mercado
    fig = px.pie(top_empresas, values='Participacao', names='Empresa', 
                 title=f'Participação de Mercado entre os 5 Maiores Provedores em {cidade_selecionada} ({ano_selecionado})', 
                 labels={'Participacao': 'Participação de Mercado (%)'})
    
    return fig
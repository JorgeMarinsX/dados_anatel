import pandas as pd

def treatData():
    df = pd.read_csv('Acessos_Banda_Larga_Fixa_2019-2020.csv', sep=';')
    df2 = pd.read_csv('Acessos_Banda_Larga_Fixa_2021.csv', sep=';')
    df3 = pd.read_csv('Acessos_Banda_Larga_Fixa_2022.csv', sep=';')
    df4 = pd.read_csv('Acessos_Banda_Larga_Fixa_2023.csv', sep=';')
    df5 = pd.read_csv('Acessos_Banda_Larga_Fixa_2024.csv', sep=';')

#headers que iremos utilizar
    headers = ['Ano','Mês','Empresa', 'UF', 'Município', 'Tecnologia', 'Meio de Acesso','Acessos']

#aplica filtros
    cidades = ['Ipatinga', 'Coronel Fabriciano', 'Timóteo', 
           'Santana do Paraíso', 'Ipaba', 'Naque', 
           'Periquito', 'Belo Oriente', 'Açucena']

    df_filtrado = df[headers][(df['UF'] == 'MG') & (df['Município'].isin(cidades))]
    df_filtrado2 = df2[headers][(df2['UF'] == 'MG') & (df2['Município'].isin(cidades))]
    df_filtrado3 = df3[headers][(df3['UF'] == 'MG') & (df3['Município'].isin(cidades))]
    df_filtrado4 = df4[headers][(df4['UF'] == 'MG') & (df4['Município'].isin(cidades))]
    df_filtrado5 = df5[headers][(df5['UF'] == 'MG') & (df5['Município'].isin(cidades))]

    dfs = [df_filtrado, df_filtrado2, df_filtrado3, df_filtrado4, df_filtrado5]

    return dfs

#prepara a exportação
def uneTabelas():
    dfs = treatData()
    tabelaUnida = pd.concat(dfs)
    tabelaUnida.to_csv('out.csv', index=False)

#exporta o documento#
uneTabelas()



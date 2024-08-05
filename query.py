import streamlit as st
import connect as ct
import pandas_gbq

#connecta ao bigQuery
ct.connect()

#QUERIES
#funções que rodam as queries
# cada tipo de query vai em uma função, sempre em cache
@st.cache_data
def queryTotalAcessos():
    query = "SELECT * FROM `dadosanatel-430317.dadosanatel072024.BandaLargaTotal072024`"
    df = pandas_gbq.read_gbq(query)
    return df

@st.cache_data
def queryGeralNominal():
    query = 'SELECT * FROM `dadosanatel-430317.dadosanatel072024.dadosAnatel2019-2024`'
    df = pandas_gbq.read_gbq(query)
    return df
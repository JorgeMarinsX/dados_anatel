import streamlit as st
from google.oauth2 import service_account
import pandas_gbq

credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])

#Conexão BigQuery
@st.cache_resource
def connect():
    pandas_gbq.context.credentials = credentials
    pandas_gbq.context.project = "dadosanatel-430317"

import streamlit as st

def pagConfig():
    #configurações da página
    pagina = st.set_page_config(layout='wide',
                                page_title='Acompanhamento dados Anatel', 
                                menu_items={
                                    'Get help': None,
                                    'Report a bug': None,
                                    'About': None
                                    })
    return pagina


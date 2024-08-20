import streamlit as st
import pandas_gbq
import query
import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def login(username, password):
    user = query.queryLogin(username)
    if not user.empty:
        hashed_password = user['password'].values[0]

        if check_password(password, hashed_password):
            st.session_state['authentication_status'] = True
            st.session_state['nome'] = user['nomeexibido'].values[0]
            return True
        else:
            st.session_state['authentication_status'] = False
            return False
            
def updateUser(df):
    pandas_gbq.to_gbq(df, 'dadosanatel-430317.dadosanatel072024.users', if_exists='replace')

def logOut():
    st.session_state['authentication_status'] = False
    st.rerun()
import streamlit as st

from SocialWorker_Interface.layout import layout as ly_sc
from Client_Interface.layout import layout_client as ly_c
from House_Interface.layout import layout_house as ly_h

from authenticate import AUTH

st.set_page_config(page_title = 'HagueHaven', page_icon = ":house:", layout = 'centered')

st.title(':house: HagueHaven')
        
authenticator = AUTH()

name, authentication_status, username =  authenticator.login('Login', 'main')

if name is not None:
    
    client_status = authenticator.credentials['usernames'][username]['client']

if authentication_status:

    if client_status == 'social':
        
        c1, c2 = st.columns([7,1])

        with c1:
            st.write(f'Welcome **{st.session_state["name"]}** ')
        with c2:
            authenticator.logout('Logout', 'main', key='unique_key')

        ly_sc()

    elif client_status == 'client':
        
        c1, c2 = st.columns([7,1])
        
        with c1:
            st.write(f'Welcome **{st.session_state["name"]}** ')
        with c2:
            authenticator.logout('Logout', 'main', key='unique_key')

        ly_c(10023,"Data/Client_Data.csv","Data/Client_Data.csv")


    elif client_status == 'organization':

        c1, c2 = st.columns([7,1])
        
        with c1:
            st.write(f'Welcome **{st.session_state["name"]}** ')
        with c2:
            authenticator.logout('Logout', 'main', key='unique_key')

        ly_h()
    
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')







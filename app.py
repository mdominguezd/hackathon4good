import streamlit as st

from SocialWorker_Interface.layout import layout as ly_sc
from SocialWorker_Interface.map_shelters import draw_map
from SocialWorker_Interface.form import setup_form

from authenticate import AUTH

st.set_page_config(page_title = 'HagueHaven', page_icon = ":house:", layout = 'centered', menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

st.title(':house: HagueHaven')
        

authenticator = AUTH()

name, authentication_status, username =  authenticator.login('Login', 'main')

if name is not None:
    
    client_status = authenticator.credentials['usernames'][username]['client']

if authentication_status:

    if client_status == 'social':
        c1, c2 = st.columns([5,1])

        with c1:
            st.write(f'Welcome **{st.session_state["name"]}** ')
        with c2:
            authenticator.logout('Logout', 'main', key='unique_key')
        
        ly_sc()
    
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')







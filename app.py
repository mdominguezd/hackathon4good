import streamlit as st

from SocialWorker_Interface.map_shelters import draw_map
from SocialWorker_Interface.form import setup_form

from authenticate import AUTH

st.set_page_config(page_title = 'HagueHaven', page_icon = ":house:", layout = 'centered', menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

st.title(':house: HagueHaven')

def layout():
    st.sidebar.header('Quick filters:')
    gender = st.sidebar.radio('Gender:', ['Male', 'Female','Non-binary'])
    age = st.sidebar.number_input('Age:', min_value = 0, step = 1, format = '%d')
    family = st.sidebar.checkbox('Family housing')
    st.sidebar.markdown("#### Special care:")
    drugs = st.sidebar.checkbox('Drug assistance:')
    domestic_vio =  st.sidebar.checkbox('Domestic violence')
    mental = st.sidebar.checkbox('Mental health assistance')

    st.sidebar.button('Get results')
    
    tab1, tab2, tab3, tab4 = st.tabs(["Housing (:house:) Locations in Den Haag", "Fill in the form (:clipboard:)", "Provider contacts (:phone:)", 'Client information (:curly_haired_person:)'])
    
    
    with tab1:
        st.markdown("""
        bla bla description
        """)
            
        draw_map()
        
    with tab2:
        setup_form()
    
    with tab3:
        st.write("Providers")

    with tab4:
        st.number_input('ID', step = 1,  format = "%d")
        st.write("")
        

authenticator = AUTH()

name, authentication_status, username =  authenticator.login('Login', 'main')

if name is not None:
    client_status = authenticator.credentials['usernames'][username]['client']

if authentication_status:
    
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{st.session_state["name"]}* ' + client_status)
    
    layout()
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')







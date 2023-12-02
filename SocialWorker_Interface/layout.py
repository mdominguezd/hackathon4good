import streamlit as st

from SocialWorker_Interface.map_shelters import draw_map
from SocialWorker_Interface.form import setup_form
from SocialWorker_Interface.client_info import search_client

def layout():
    
    st.sidebar.header('Quick filters:')
    gender = st.sidebar.radio('Gender:', ['Male', 'Female','Non-binary'])
    age = st.sidebar.number_input('Age:', min_value = 0, step = 1, format = '%d')
    family = st.sidebar.checkbox('Family housing')
    st.sidebar.markdown("#### Special care:")
    drugs = st.sidebar.checkbox('Addiction assistance')
    domestic_vio =  st.sidebar.checkbox('Domestic violence')
    mental = st.sidebar.checkbox('Mental health assistance')

    st.sidebar.button('Get results')
    
    tab1, tab2, tab3 = st.tabs(["Housing (:house:) Locations in Den Haag", "Fill in the form (:clipboard:)", 'Client information (:curly_haired_person:)'])
    
    
    with tab1:
        st.markdown("""
        Housing solutions for The Hague
        """)

        c1, c2 = st.columns(2)

        with c1:
            id = st.number_input("ID")
        with c2:
            button = st.button("Calculate suitabilty")

        if button:
            draw_map(id = id)
        else:
            draw_map()
        
    with tab2:
        setup_form()
    
    with tab3:
        search_client()
        
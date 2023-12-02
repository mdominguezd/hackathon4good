import streamlit as st

from SocialWorker_Interface.map_shelters import draw_map
from SocialWorker_Interface.form import setup_form
from SocialWorker_Interface.client_info import search_client

def layout():
    
    st.sidebar.header('Quick filters:')
    gender = st.sidebar.radio('Gender:', ['Male', 'Female','Non-binary'])
    age = st.sidebar.number_input('Age:', min_value = 0, value = 18, step = 1, format = '%d')
    family = st.sidebar.checkbox('Family housing')
    st.sidebar.markdown("#### Special care:")
    drugs = st.sidebar.checkbox('Substance abuse assistance')
    mental = st.sidebar.checkbox('Mental health assistance')

    def click_results():
        st.session_state.suit_clicked = False
        st.session_state.results_clicked = True

    results = st.sidebar.button('Get results', on_click = click_results)
    
    tab1, tab2, tab3 = st.tabs(["Housing (:house:) Locations in The Hague", "Fill in the form (:clipboard:)", 'Client information (:curly_haired_person:)'])
    
    
    with tab1:
        st.markdown("""
        #### Housing locations at The Hague
        """)

        # BUTTON FUNCTIONS
        def click_suit():
            st.session_state.suit_clicked = True
            st.session_state.results_clicked = False

        c1, c2 = st.columns([5,1])

        if 'suit_clicked' not in st.session_state:
            st.session_state.suit_clicked = False
            
        if 'results_clicked' not in st.session_state:
            st.session_state.results_clicked = False

        with c1:
            id = st.number_input("ID", value = 10000, step = 1, format = '%d')
            
        with c2:
            button = st.button("Calculate suitabilty", on_click = click_suit)
                    
        if st.session_state.suit_clicked:
            draw_map(id = id)
        elif st.session_state.results_clicked:
            filters = {'gender': gender,
                       'age' : age,
                       'family' : family,
                       'drugs' : drugs,
                       'mental' : mental}
            
            draw_map(filters = filters)
        else:
            draw_map()
        
    with tab2:
        setup_form()
    
    with tab3:
        search_client()
        
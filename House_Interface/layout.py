import streamlit as st
import pandas as pd

# Sample data for the table

def layout_house():

    house_data = [["LB004","1/2","20","Male",False,"Basic",False,"Accept"],["LP007","3/3","45","Female",True,"Plus",True,"Accept"],["HS002","2/3","16","Male",False,"Immediate shelter",False,"Accept"]]

    tab1, tab2 = st.tabs(["Requests","Homes"])

    with tab1:

        house_df = pd.DataFrame(house_data,columns=["UniqueLocID","Capacity","Age","Gender","MentalHealth","Service","SustanceAbuse","Accept"])


        # Display the table
        st.write('Requests:')
        st.markdown(house_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)
        

    with tab2:
        with st.expander("Select House"):
            # Tabs
            tab1_, tab2_, tab3_, tab4_ = st.tabs(["LB004", "LP007", "HS002", "HS005"])
            with tab1_:
                lb004_data = [[10000,"Olivia Adams","01-12-2023","End"]]
                lb004_df = pd.DataFrame(lb004_data,columns=["ID","Name","Start Date","End"])
                st.markdown(lb004_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)
                st.write("Capacity is : 1/2")
            with tab2_:
                lp007_data = [[10001,"Ethan Turner","27-11-2023","End"],[10002,"Ava Martinez","29-11-2023","End"],[10003,"Mason Chen","01-12-2023","End"]]
                lp007_df = pd.DataFrame(lp007_data,columns=["ID","Name","Start Date","End"])
                st.markdown(lp007_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)
                st.write("Capacity is : 3/3")
            with tab3_:
                hs002_data = [[10004,"Andrea Davis","25-11-2023","End"],[10005,"Liam Rodriguez","20-11-2023","End"]]
                hs002_df = pd.DataFrame(hs002_data,columns=["ID","Name","Start Date","End"])
                st.markdown(hs002_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)
                st.write("Capacity is : 2/3")
            with tab4_:
                hs005_data = [[10006,"Emma Wright","12-11-2023","End"],[10007,"Falseah Campbell","17-11-2023","End"],[10008,"Casey Taylor","01-12-2023","End"],[10009,"Jackson Lee","29-11-2023","End"]]
                hs005_df = pd.DataFrame(hs005_data,columns=["ID","Name","Start Date","End"])
                st.markdown(hs005_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)
                st.write("Capacity is : 4/6")

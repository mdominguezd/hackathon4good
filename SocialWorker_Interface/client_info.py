import streamlit as st
import pandas as pd


def search_client():
    name = st.text_input('Search by name')

    df = pd.read_csv('Data/Client_Data.csv', delimiter = ',')

    if name != '':
        names = df[df['Name'].apply(lambda d : name.upper() in d.upper())][['ID', 'Name']]
        st.write(names)
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import contextlib

def setup_form(filename = 'Data/Client_Data.csv'):

    last_ID = np.max(pd.read_csv(filename, delimiter = ',').ID)

    with st.form("Client_DB_Form"):
        st.write("Form to create a new case")

        ID = last_ID + 1
        name = st.text_input("Name:")
        birth = st.date_input('Birth date:', min_value = date(1910, 1, 1),  max_value = date.today())
        gender = st.selectbox("Gender:", ['Male', 'Female', 'Non-binary'])
        mental = st.checkbox("Mental assistance")
        type_as = st.selectbox("Assistance required:", ['Basic', 'Plus', 'Intensive', 'Immediate shelter'])
        addiction = st.checkbox("Substance addiction")
        prison = st.checkbox("Have you been in prison?")
        family = st.checkbox('Family accomodation')
        entitled = st.checkbox('Is the applicant entitled to get shelter in Den Haag?')

        HousID = None
        Req = None
        Acc = None
        start = None
        end = None
        
        row = [ID, name, birth.year, gender, mental, type_as, addiction, prison, family, entitled, HousID, Req, Acc, start, end]
        
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        
        if submitted:

            df = pd.read_csv(filename, delimiter = ',')
            d_row = pd.DataFrame([row])

            d_row.columns = df.columns

            df = pd.concat([df, d_row])
            df.reset_index(drop = True, inplace = True)
            
            st.success('New case created with ID:' + str(ID)+ '! :smile:')

            with contextlib.suppress(PermissionError):
                df.to_csv('Data/Client_Data.csv', index = False)
            
            st.write(d_row)        

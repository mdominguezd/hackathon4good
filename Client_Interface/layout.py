import streamlit as st
import pandas as pd

# Sample data for the table

def layout_client(client_id,client_folder,house_folder):

    client_df = pd.read_csv(client_folder, sep = ",")
    house_df = pd.read_csv(house_folder, sep = ";")

    if not pd.isna(client_df.loc[client_df.ID == client_id, "UniqueLocID"].values[0]):
        case_data = [[client_df.loc[client_df.ID == client_id, "Service"].values[0],"Accepted","Vaillantlaan 105- 115, Den Haag", "02-12-2023"]]
    elif not pd.isna(client_df.loc[client_df.ID == client_id, "Request"].values[0]):
        case_data = [[client_df.loc[client_df.ID == client_id, "Service"].values[0],"In progress","",""]]

    case_df = pd.DataFrame(case_data,columns=["Case","Status","Address","Starting Date"])

    case_df = case_df.reset_index(drop=True)

    name = client_df.loc[client_df.ID == client_id, "Name"].values[0]
    year_of_birth = client_df.loc[client_df.ID == client_id, "YearofBirth"].values[0]
    name = client_df.loc[client_df.ID == client_id, "Name"].values[0]
    name = client_df.loc[client_df.ID == client_id, "Name"].values[0]

    # Dashboard layout
    st.title('Dashboard')

    # Left panel with a list of information
    st.sidebar.title('My Information')

    st.sidebar.text(f"ID :  {client_id}")
    st.sidebar.text(f"Name :  {name}")
    st.sidebar.text(f"Year of birth :  {year_of_birth}")


    # Display the table
    st.write('Table:')
    st.markdown(case_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)


    # Contact information below the table
    st.title('Homeless Help Desk')
    st.write('Fruitweg 17, The Hague')
    st.write('Phone: (070) 353 72 91')

layout_client(10016,"C:/Users/Aleja/OneDrive/Bureau/Hackathonforgood/git_repo/hackathon4good/Data/Client_Data.csv","C:/Users/Aleja/OneDrive/Bureau/Hackathonforgood/git_repo/hackathon4good/Data/Client_Data.csv")
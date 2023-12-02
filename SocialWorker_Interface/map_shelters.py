import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import pandas as pd
from owslib.wfs import WebFeatureService
import os 
from datetime import date
import numpy as np
import datetime 


def draw_map(id = None, filters = None, location = [52.07819576524207, 4.309696687447081]):

    if 'Data' not in os.listdir('.'):
        os.mkdir('Data')
    
    m = folium.Map(location=location, 
                   zoom_start = 13)

    with st.spinner('Downloading the necessary Housing data. Wait for it...'):

        housing_gdf = get_careorg_data()

        housings = housing_gdf.to_crs('epsg:4326')

        client_df = get_occupancy_data()

        housings = housings.join(client_df, on = 'UniqueLocID')

        if id != None:
            suit_df = calculate_suitability(id)
            housings = housings.merge(suit_df, on = 'UniqueLocID', how = 'left')
        else:
            housings['Suitability'] = np.nan

        if filters != None:
            housings = filter_data(housings, filters)
            
        housings['RT_Occupation'] = housings['RT_Occupation'].fillna(0)

        housings['perc_ocup'] = 100*(housings['RT_Occupation']/housings['Number of places'])

        for i in range(len(housings)):
            
            if housings.iloc[i]['perc_ocup'] == 100:
                I = folium.Icon(color = 'gray', icon = 'info-sign')
                
            else:
                if np.isnan(housings.iloc[i]['Suitability']):
                    
                    if housings.iloc[i]['perc_ocup'] == 100:
                        I = folium.Icon(color = 'gray', icon = 'home')
                        
                    else:
                        I = folium.Icon(color = 'blue', icon = 'home')
                        
                else:
                    if housings.iloc[i]['Suitability'] >= 0.75:
                        I = folium.Icon(color="green", icon="home")
                    
                    elif housings.iloc[i]['Suitability'] >= 0.70:
                        I = folium.Icon(color="orange", icon="home")
                    
                    else:
                        I = folium.Icon(color = 'gray', icon = 'home')
                
            folium.Marker(
                location = [housings.iloc[i].geometry.y, housings.iloc[i].geometry.x],
                icon= I,
                popup = '<b>ID: </b>' + housings.iloc[i]['UniqueLocID'] + '<br><b>Adress: </b>' + housings.iloc[i]['Adres'] + '<br><b>Contact:</b>' + str(round(housings.iloc[i]['ContactPhone'])),
                tooltip = '<b>Occupation percent: </b>' + str(round(housings.iloc[i]['perc_ocup'], 0)) + '<br><b>Places available: </b>' + str((housings.iloc[i]['Number of places'] - housings.iloc[i]['RT_Occupation'])) + '<br><b>Suitability: </b>' + str(round(housings.iloc[i]['Suitability']*100, 0))
                ).add_to(m)
    
    map_info = st_folium(m, width = 800, 
                         height = 500)

    if map_info["last_object_clicked_popup"] is not None:
        st.markdown("### Data from selected housing organization: ")
        
        c1, c2 = st.columns([7,1])
        
        with c1:
            house_data = map_info["last_object_clicked_popup"].split('\n')
            
            st.write("**Address:** " + house_data[1].split(': ')[1])
            st.write("**Contact:** " + house_data[2].split(':')[1])
            
            H_ID = map_info["last_object_clicked_popup"].split(' ')[1][:5]
            C_ID = id
            
        with c2:
            req = st.button("Request")

        if req:
            request_housing(C_ID, H_ID)


def filter_data(df, filters):

    st.markdown("Housing locations filtered with **quick filters**:")
    # Filter by gender
    df = df[(df['Gender'].isna()) | (df['Gender'] == filters['gender'])]

    # Filter by age
    df = df[(filters['age'] > df['MinAge']) & ((filters['age'] < df['MaxAge']))]

    # Filter by family housing
    df = df[df['Family'] == filters['family']]

    # Filter by substance abuse
    if filters['drugs']:
        df = df[df['SubstanceAbuse'] == filters['drugs']]
        
    # Filter by mental illness
    df
    
    return df
    
def request_housing(ID, HousID,
                    h_fn = 'Data/House_Data.csv', 
                    c_fn = 'Data/Client_Data.csv'):

    df = pd.read_csv(c_fn)

    idx = df[df['ID'] == ID].index

    if df[df['ID'] == ID]['UniqueLocID'].isna().iloc[0]:
        df.loc[idx,'Request'] = HousID
        
    else:
        st.warning('The client has already been assigned to a housing location', icon="⚠️")

    df.to_csv(c_fn, index = False)
    

def get_careorg_data(filename = 'Data/House_Data.csv'):
    
    df = pd.read_csv(filename)

    gdf = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(x = df['X'], y = df['Y'])).set_crs('epsg:4326')

    return gdf

def get_occupancy_data(filename = 'Data/Client_Data.csv'):

    df = pd.read_csv(filename, delimiter = ',')
    
    for i in df.columns:
        if 'date' in i:
            df[i] = pd.to_datetime(df[i], format = '%d.%m.%Y')
    
    rt_ocup = df[(df['End_date'] > pd.Timestamp.now()) | (pd.isnull(df['End_date']))].groupby('UniqueLocID').count().ID
    
    rt_ocup.name = 'RT_Occupation'
    
    return pd.DataFrame(rt_ocup)
    
def calculate_suitability(client_id, client_folder = 'Data/Client_Data.csv', house_folder = 'Data/House_Data.csv'):

    house_df = pd.read_csv(house_folder, sep=",")

    client_df = pd.read_csv(client_folder, sep=",")
    
    suit_df = pd.DataFrame(house_df["UniqueLocID"])
    
    if (client_id in list(client_df['ID'])):
    
    
        today = datetime.date.today()
        age = today.year - client_df.loc[client_df.ID == client_id, "YearofBirth"].values[0]
        gender = client_df.loc[client_df.ID == client_id, "Gender"].values[0]
        mental = client_df.loc[client_df.ID == client_id, "MentalHealth"].values[0]
        service = client_df.loc[client_df.ID == client_id, "Service"].values[0]
        addiction = client_df.loc[client_df.ID == client_id, "SubstanceAbuse"].values[0]
        prison = client_df.loc[client_df.ID == client_id, "Prison"].values[0]
        family = client_df.loc[client_df.ID == client_id, "Family"].values[0]
    
        def geo_mean(iterable):
            a = np.array(iterable)
            return a.prod()**(1.0/len(a))
    
    
        suit_list = []
    
        for index, row in house_df.iterrows():
    
            suitabilities = []
    
            if row["MinAge"] < age < row["MaxAge"]:
                suitabilities.append(1.)
            else:
                suitabilities.append(0.)
    
            if pd.isna(row["Gender"]):
                suitabilities.append(0.5)
            elif row["Gender"] == gender:
                suitabilities.append(1.)
            else:
                suitabilities.append(0.)
    
            if row["MentalHealth"]==mental:
                suitabilities.append(1.)
            else:
                suitabilities.append(0.)
    
            if row["Service"]==service:
                suitabilities.append(1.)
            else:
                suitabilities.append(0.)
    
            if pd.isna(row["SubstanceAbuse"]):
                suitabilities.append(0.5)
            elif row["SubstanceAbuse"]==addiction:
                suitabilities.append(1.)
    
            if pd.isna(row["Prison"]):
                suitabilities.append(0.5)
            elif row["Prison"]==prison:
                suitabilities.append(1.)
    
            if row["Family"]==family:
                suitabilities.append(1.)
            else:
                suitabilities.append(0.)
    
            suit = geo_mean(suitabilities)
    
            suit_list.append(suit)
    
        suit_df["Suitability"] = suit_list

    else:
        suit_df["Suitability"] = np.nan

    return suit_df
    
    
# def calculate_suitability(ID = 11, c_fn = 'Data/Client_Data.csv', h_fn = 'Data/House_Data.csv'):

#     c_df = pd.read_csv(c_fn, delimiter = ',')

#     # Make sure time data is in the correct format:
#     for i in c_df.columns:
#         if 'date' in i:
#             c_df[i] = pd.to_datetime(c_df[i], format = '%d.%m.%Y')

#     h_df = pd.read_csv(h_fn)

#     h_df = h_df.set_index('UniqueLocID')

#     h_df['Suitability'] = 1
    
#     return h_df['Suitability'].reset_index()
    







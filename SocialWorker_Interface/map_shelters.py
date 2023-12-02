import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import pandas as pd
from owslib.wfs import WebFeatureService
import os 
from datetime import date


def draw_map(location = [52.07819576524207, 4.309696687447081]):

    if 'Data' not in os.listdir('.'):
        os.mkdir('Data')
    
    m = folium.Map(location=location, 
                   zoom_start = 13)

    with st.spinner('Downloading the necessary Housing data. Wait for it...'):

        housing_gdf = get_careorg_data()

        housings = housing_gdf.to_crs('epsg:4326')

        client_df = get_occupancy_data()

        housings = housings.join(client_df, on = 'UniqueLocID')
        housings['RT_Occupation'] = housings['RT_Occupation'].fillna(0)

        housings['perc_ocup'] = 100*(housings['RT_Occupation']/housings['Number of places'])

        for i in range(len(housings)):
            if housings.iloc[i]['perc_ocup'] == 100:
                I = folium.Icon(color="gray", icon="home")
            elif housings.iloc[i]['perc_ocup'] >= 70:
                I = folium.Icon(color="orange", icon="home")
            else:
                I = folium.Icon(color = 'green', icon = 'home')
            folium.Marker(
                    location = [housings.iloc[i].geometry.y, housings.iloc[i].geometry.x],
                    icon= I,
                    tooltip = '<b>Occupation percent: </b>' + str(round(housings.iloc[i]['perc_ocup'], 0)) + '<br><b>Places available: </b>' + str((housings.iloc[i]['Number of places'] - housings.iloc[i]['RT_Occupation']))
                ).add_to(m)
    
    map_info = st_folium(m, width = 800, 
                         height = 500)

    st.markdown("Data from selected housing organization: ")

    # st.write(map_info)


def get_careorg_data(filename = 'Data/Housings_Data.csv'):
    
    df = pd.read_csv(filename, delimiter = '\t')

    gdf = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(x = df['X'], y = df['Y'])).set_crs('epsg:4326')

    return gdf

def get_occupancy_data(filename = 'Data/Client_Data.csv'):

    df = pd.read_csv(filename)
    
    for i in df.columns:
        if 'time' in i:
            df[i] = pd.to_datetime(df[i])
    
    rt_ocup = df[(df['End_time'] > pd.Timestamp.now()) | (pd.isnull(df['End_time']))].groupby('UniqueLocID').count().ID
    
    rt_ocup.name = 'RT_Occupation'
    
    return pd.DataFrame(rt_ocup)
    
def download_woning_data(location = [52.07819576524207, 4.309696687447081], extent = 500):

    url = "https://geodata.zuid-holland.nl/geoserver/wonen/wfs"

    layer = 'wonen:WONINGCORPORATIEBEZIT_BAG'

    wfs = WebFeatureService(url, version='2.0.0')

    gdf = gpd.GeoDataFrame(geometry = gpd.points_from_xy(x = [location[1]], y = [location[0]]))
    gdf = gdf.set_crs('epsg:4326')

    # Get bounds
    xmin = gdf.to_crs('epsg:28992').geometry.x.iloc[0] - extent
    xmax = gdf.to_crs('epsg:28992').geometry.x.iloc[0] + extent
    ymin = gdf.to_crs('epsg:28992').geometry.y.iloc[0] - extent
    ymax = gdf.to_crs('epsg:28992').geometry.y.iloc[0] + extent
    
    response = wfs.getfeature(typename = layer, bbox=(xmin, ymin, xmax, ymax))

    # Read data from URL
    with open('Data/WoningCorporatie.gml', 'wb') as file:
        file.write(response.read())

    gdf = gpd.read_file('Data/WoningCorporatie.gml').set_crs('epsg:28992').dissolve('wl_adres')
    
    gdf.to_parquet('Data/WoningCorporatie.parquet')

    os.remove('Data/WoningCorporatie.gml')

    return gdf
    






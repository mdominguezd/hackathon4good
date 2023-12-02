import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np


def geocode_shelter(filepath): # Get latitude and longitude of shelter addresses and add them back to dataframe
    hs_locs_fp = filepath

    hs_df = pd.read_csv(hs_locs_fp, encoding='unicode_escape')
    hs_df.rename(columns={"\xa0Adres": "Adres"}, inplace=True) # Fix the weird format of the Adres

    hs_addresses = hs_df["Adres"]

    latitude_list = []
    longitude_list = []


    geolocator = Nominatim(user_agent="coffeebreakers", timeout=3)

    for address in hs_addresses:
        shelter_loc = geolocator.geocode(address, viewbox=[(51.830126,4.080322),(52.181698,4.709290)], bounded=1)
        if shelter_loc is not None:
            latitude_list.append(shelter_loc.latitude)
            longitude_list.append(shelter_loc.longitude)
        else:
            print(f"Could not find coordinates for address: {address}")
            latitude_list.append(np.nan)
            longitude_list.append(np.nan)
        


    hs_df["Latitude"] = latitude_list
    hs_df["Longitude"] = longitude_list
    
    return hs_df



living_basic_df = geocode_shelter("C:\Data\hack4good\data2\care_orgs\living_basic.csv")
living_plus_df = geocode_shelter("C:\Data\hack4good\data2\care_orgs\living_plus.csv")
other_locations_df = geocode_shelter("C:\Data\hack4good\data2\care_orgs\other_locations.csv")
living_intensive_df = geocode_shelter("C:\Data\hack4good\data2\care_orgs\living_intensive.csv")
homeless_shelters_df = geocode_shelter("C:\Data\hack4good\data2\care_orgs\homeless_shelters.csv")

living_basic_df = living_basic_df.filter(items=["Zorgaanbieder", "UniqueLocID", "Adres", "Totaal aantal plekken", "Latitude", "Longitude"])
living_plus_df = living_plus_df.filter(items=["Zorgaanbieder", "UniqueLocID", "Adres", "Number of places", "Latitude", "Longitude"])
other_locations_df = other_locations_df.filter(items=["Zorgaanbieder", "UniqueLocID", "Adres", "Aantal \nplekken", "Latitude", "Longitude"])
living_intensive_df = living_intensive_df.filter(items=["Zorgaanbieder", "UniqueLocID", "Adres", "total number of places", "Latitude", "Longitude"])
homeless_shelters_df = homeless_shelters_df.filter(items=["Zorgaanbieder", "UniqueLocID", "Adres", "Totaal aantal plekken", "Latitude", "Longitude"])

living_basic_df.columns = ["Zorgaanbieder", "UniqueLocID", "Adres", "Totaal aantal plekken", "Latitude", "Longitude"]
living_plus_df.columns = ["Zorgaanbieder", "UniqueLocID", "Adres", "Totaal aantal plekken", "Latitude", "Longitude"]
other_locations_df.columns = ["Zorgaanbieder", "UniqueLocID", "Adres", "Totaal aantal plekken", "Latitude", "Longitude"]
living_intensive_df.columns = ["Zorgaanbieder", "UniqueLocID", "Adres", "Totaal aantal plekken", "Latitude", "Longitude"]
homeless_shelters_df.columns = ["Zorgaanbieder", "UniqueLocID", "Adres", "Totaal aantal plekken", "Latitude", "Longitude"]




combined_df = pd.concat([living_basic_df,living_plus_df, living_intensive_df, homeless_shelters_df, other_locations_df], ignore_index=True, axis=0)

export_fp = "C:\Data\hack4good\data2\geocoded_shelters.csv"

combined_df.to_csv(export_fp)

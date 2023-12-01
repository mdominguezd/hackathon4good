import pandas as pd

from geopy.geocoders import Nominatim


hs_locs_fp = "C:/Data/hack4good/data2/care_orgs/homeless_shelters.csv"

hs_df = pd.read_csv(hs_locs_fp, encoding='unicode_escape')
hs_df.rename(columns={"\xa0Adres": "Adres"}, inplace=True) # Fix the weird format of the Adres

hs_addresses = hs_df["Adres"]

latitude_list = []
longitude_list = []


geolocator = Nominatim(user_agent="coffeebreakers")

for address in hs_addresses:
    shelter_loc = geolocator.geocode(address)
    if shelter_loc is not None:
        latitude_list.append(shelter_loc.latitude)
        longitude_list.append(shelter_loc.longitude)
    else:
        print(f"Could not find coordinates for address: {address}")
        latitude_list.append("unknown")
        longitude_list.append("unknown")
    


hs_df["Latitude"] = latitude_list
hs_df["Longitude"] = longitude_list
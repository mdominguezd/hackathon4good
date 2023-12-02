# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 18:15:52 2023

@author: petra
"""

import pandas as pd
import os
import datetime

datafolder = datafolder = "C:\\Data\\hack4good\\data2\\"


house_fn = "House_Data.csv"
client_fn = "Client_Data.csv"

house_df = pd.read_csv(os.path.join(datafolder, house_fn))
house_df = house_df.drop(house_df.columns[:2], axis = 1)

client_df = pd.read_csv(os.path.join(datafolder, client_fn), sep=";")

client_id = str(10019)

today = datetime.date.today()
age = today.year - client_df.loc[client_df.ID == client_id, "YearofBirth"].value
year = today.year
yob = client_df.loc[client_df.ID == client_id, "YearofBirth"].values[0]


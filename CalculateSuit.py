# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 18:15:52 2023

@author: petra
"""

def CalculateSuitability(client_id,client_folder,house_folder):

    house_df = pd.read_csv(house_folder,sep=",")

    client_df = pd.read_csv(client_folder,sep=";")

    suit_df = pd.DataFrame(house_df["UniqueLocID"])


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

    return suit_df
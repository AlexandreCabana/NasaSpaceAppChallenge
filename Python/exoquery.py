import requests
import pandas as pd
import numpy as np
df = pd.read_csv("PS_2024.10.05_11.25.47.csv")
def remove_uselesscoloumn(data):
    return data.drop(data.columns.difference(["pl_name",'ra', 'dec',"sy_dist"]), axis=1)
def findcoordonate(data):
    data["X"] = (1000 / data['parallax']) * np.sin(data['ra'])*np.cos(data['dec'])
    data["Y"] = (1000 / data['parallax']) * np.sin(data['ra'])*np.sin(data['dec'])
    data["Z"]=(1000 / data['parallax'])*np.cos(data['ra'])
    return data
def removeradecparallax(data):
    return data.drop(["parallax","sy_dist"], axis=1)

df = remove_uselesscoloumn(df)
df = df.drop_duplicates()
df["parallax"]=(1/(df["sy_dist"]))*1000
df = removeradecparallax(findcoordonate(df))
df.dropna()
df.to_csv("output.csv", index=False)

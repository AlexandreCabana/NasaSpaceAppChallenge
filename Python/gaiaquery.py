import astropy.units as u
import pandas as pd
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
import numpy as np
import sys
Gaia.ROW_LIMIT = -1
def remove_uselesscoloumn(data):
    return data.drop(data.columns.difference(['ra', 'dec',"parallax", "phot_g_mean_mag"]), axis=1)
def removenanvalue(data):
    return data.dropna()
def findcoordonate(data):
    data["X"] = (1000 / data['parallax']) * np.sin(data['ra'])*np.cos(data['dec'])
    data["Y"] = (1000 / data['parallax']) * np.sin(data['ra'])*np.sin(data['dec'])
    data["Z"]=(1000 / data['parallax'])*np.cos(data['ra'])
    return data
def removeradecparallax(data):
    return data.drop(['ra', 'dec', "parallax"], axis=1)

def calculatedistancefromearth(distx, disty, distz):
    return np.sqrt((distx**2) + (disty**2) + (distz**2))

def calculatebrighness(mgt, distet, distee):
    num = np.log10(((distet**2) * 10 ** (mgt / -2.5)) / (distee ** 2))
    den = np.log10(10**(1/-2.5))
    return num / den
StarsDf = None
planetname = sys.argv[1].replace("_", " ")
planetCataloge= pd.read_csv("output.csv")
planetRow = planetCataloge.loc[planetCataloge['pl_name'] == planetname]
ra = float(planetRow["ra"].iloc[0])
dec = float(planetRow["dec"].iloc[0])
scanscope = 0.2
step = 0.05
planetx=float(planetRow["X"].iloc[0])
planety=float(planetRow["Y"].iloc[0])
planetz=float(planetRow["Z"].iloc[0])
planetdistancefromearth= calculatedistancefromearth(planetx, planety, planetz)
currentra = ra -scanscope
currentdec = dec -scanscope
while currentra <= ra +scanscope:
    while currentdec <= dec +scanscope:
        #print(f"Current ra {currentra}. Current dec {currentdec}.")
        coord = SkyCoord(ra=currentra, dec=currentdec, unit=(u.degree, u.degree), frame='icrs')
        width = u.Quantity(0.1, u.deg)
        height = u.Quantity(0.1, u.deg)
        r = Gaia.query_object_async(coordinate=coord, width=width, height=height)
        data = r.to_pandas()
        data = removeradecparallax(findcoordonate(removenanvalue(remove_uselesscoloumn(data))))
        if (StarsDf is None):
            StarsDf = data.copy()
        else:
            StarsDf = pd.concat([StarsDf, data])
        currentdec += step
    currentra += step
StarsDf["DistXbetweenstartandexo"]= StarsDf["X"]-planetx
StarsDf["DistYbetweenstartandexo"]= StarsDf["Y"]-planety
StarsDf["DistZbetweenstartandexo"]= StarsDf["Z"]-planetz
StarsDf["DistanceFromEarth"]=calculatedistancefromearth(StarsDf["X"],StarsDf["Y"],StarsDf["Z"])
StarsDf["Brighness"]=calculatebrighness(StarsDf["phot_g_mean_mag"], StarsDf["DistanceFromEarth"],planetdistancefromearth)


StarsDf = StarsDf.drop(["phot_g_mean_mag"], axis=1)
print(StarsDf)
StarsDf.to_csv("StarsDf.csv",index=False, header=False)

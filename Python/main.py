import requests

a =requests.get("https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=cumulative").text
with open("test.csv","w+") as f:
    f.write(a)
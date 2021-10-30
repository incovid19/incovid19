import os
import datetime
import timedelta

today = (datetime.datetime.now() - timedelta.Timedelta(days=1)).date()
print(today)
# today = datetime.datetime.now().date()
folders = ["INPUT","RAWCSV","LOG"]

for folder in folders:
    if not os.path.isdir(os.path.join("..",folder,str(today))):
        os.mkdir(os.path.join("..",folder,str(today)))
        print("Created")


from getHTMLSources import getSources
from ExtractDataFromImage import ExtractDataFromImage
from ExtractDataFromPDF import ExtractFromPDF
from ExtractStateMyGov import ExtractStateMyGov
from getHTMLData import ExtractFromHTML
import pandas as pd

source = pd.read_csv(r"../sources.csv")
getSources(source,today)

print("Extracting Data")

for idx in source.index:
    if source["StateDataSourceType"][idx] == "Image(Twitter)":
        print("Image:" + source["StateCode"][idx])
        ExtractDataFromImage(source["StateCode"][idx], str(today), source['Twitter Handle'][idx], source['Twitter Search Term'][idx])
    elif source["StateDataSourceType"][idx] == "html":
        if source["myGov"][idx] != "yes":
            ExtractFromHTML(StateCode = source["StateCode"][idx],Date = str(today))
        else:
            ExtractStateMyGov(source["StateCode"][idx],str(today))
    elif source["StateDataSourceType"][idx] == "pdf":
        pass
        # ExtractFromPDF(StateCode = source["StateCode"][idx],Date = str(today))
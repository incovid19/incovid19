import os
import datetime
import timedelta
import os

today = (datetime.datetime.now() - timedelta.Timedelta(days=0)).date()
yesterday = (datetime.datetime.now() - timedelta.Timedelta(days=1)).date()
# present = datetime.datetime.now().date()

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
# today = datetime.datetime.strptime("2022-01-06", "%Y-%M-%d").date()
print("getSources for:"+ str(today))
# a=b
source = pd.read_csv(r"../sources.csv")
# print(source)
# a=b
getSources(source,today)
# cmd = 'echo swie2e@2908 | sudo -S ../INPUT/KL/kl.sh'
# os.system('python ../INPUT/KL/kl_dataDownload.py')
#*********************************************************************

print("Extracting Data for:" + str(today))
for idx in source.index:
    # if idx == 0:
    print("State:" + source["StateName"][idx])
    if source["StateDataSourceType"][idx] == "Image(Twitter)":
        if "{}_raw.csv".format(source["StateCode"][idx]) not in os.listdir("../RAWCSV/"+str(today)+"/"):
            pass
            # ExtractDataFromImage(source["StateCode"][idx], str(today), source['Twitter Handle'][idx], source['Twitter Search Term'][idx])
    elif source["StateDataSourceType"][idx] in ["html","json"]:
        if source["myGov"][idx] != "yes":
            fileStatus = os.path.isfile(os.path.join("../INPUT",str(today),source["StateCode"][idx]+ "." + source["StateDataSourceType"][idx]))
            if not(fileStatus):# and source["StateCode"][idx] != "TT":
                # ExtractStateMyGov(source["StateCode"][idx],str(today),no_source= not(fileStatus))
                pass
            else:
                # if source["StateDataSourceType"][idx] == "TT":
                ExtractFromHTML(source["StateCode"][idx],str(today))
        else:
            pass
            ExtractStateMyGov(source["StateCode"][idx],str(today))
    elif source["StateDataSourceType"][idx] == "pdf":
        fileStatus = os.path.isfile(os.path.join("../INPUT",str(today),source["StateCode"][idx]+".pdf"))
        if not(fileStatus):
            # ExtractStateMyGov(source["StateCode"][idx],str(today),no_source= not(fileStatus))
            pass
        else:
            pass
            # ExtractFromPDF(StateCode = source["StateCode"][idx],Date = str(today))

            
os.system("python /home/swiadmin/Incovid19/incovid19/src/portalUpdate.py "+ str(yesterday))
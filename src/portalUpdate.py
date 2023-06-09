from datetime import datetime, timedelta
import os
import pandas as pd 
from util import date_range, GetFileStatus, ExtractData, DownloadData, portalUpdate_second,portalUpdate_first,git_push,git_push_incovid
from getTT import getTT
from tqdm import tqdm
from UpdateDerivedValues import STATE_NAMES,updateDerivedValues,removeLogging
from StatusMsg import PortalStatusMsg,StatusMsg
from getjson import createDataMin,updateAll
import warnings
warnings.filterwarnings('ignore')

import sys
sys.path.insert(0, '/home/swiadmin/Incovid19/incovid19/CSV_APIs_Code')
from main_csv import UpadteCSV
source = pd.read_csv("/home/swiadmin/Incovid19/incovid19/sources.csv")



try: 
    endDate = str(sys.argv[2])
    prevUpdate = True
except IndexError:
    endDate = True
    prevUpdate = False
    
yesterday = (datetime.now() - timedelta(days= 26 + 1)).date()
    
dateList = date_range(str(yesterday),True)

today = (datetime.now() - timedelta(days=0)).date()
if "TT_final.csv" not in os.listdir("../RAWCSV/"+str(today)+"/"):
    # portalUpdate_first(dateList,prevUpdate)
    # resp1 = input("Would you like to proceed with the update(Yes/No):")
    resp1 = "Yes"
    if resp1 == "Yes":
        commitMessage = portalUpdate_second(dateList,prevUpdate)
        # resp3 = input("Would you like to proceed with the update(Yes/No):")
        resp3 = "Yes"
        if resp3 == "Yes":
            UpadteCSV(dateList)
            print("Commit Message:")
            if commitMessage == None or prevUpdate:
                commitMessage = input("Please Enter the commit Message:")
                git_push(commitMessage)
            else: 
                print(commitMessage)
                # resp2 = input("Would you like to proceed with the above message?(Yes/No):")
                resp2 = "Yes"
                if resp2 == "Yes":
                    git_push(commitMessage)
                elif resp2 == "No":
                    commitMessage = input("Please Enter the commit Message:")
                    git_push(commitMessage)

    else:
        pass

    # resp_incovid = input("Would you like to push the incovid Repo?(Yes/No):")
    resp_incovid = "Yes"
    if resp_incovid == "Yes":
        git_push_incovid("Update Until" + str(datetime.now()))
    else:
        pass
else:
    print("Portal Upto date") 


# resp_incovid = input("Would you like to update and push the RDF CSV's?(Yes/No):")
# if resp_incovid == "Yes":
#     print("Updating RDF CSV's....")
#     sys.path.insert(1, '../rdf')
#     from csvvacc import main as csvmain
#     from rdfgeneration import main as rdfmain
#     csvmain()
#     rdfmain()
#     os.system("cd /home/swiadmin/Incovid19/rdf/ && scp *.csv swiadmin@captain.internal.semanticwebindia.in:/home/swiadmin/files/")
# else:
#     pass



# python portalUpdate.py 2022-03-13
from datetime import datetime, timedelta
import os
import pandas as pd 
from util import date_range, GetFileStatus, ExtractData, DownloadData, portalUpdate_second,portalUpdate_first,git_push,git_push_incovid
from getTT import getTT
from tqdm import tqdm
from UpdateDerivedValues import STATE_NAMES,updateDerivedValues,removeLogging
from StatusMsg import PortalStatusMsg
from getjson import createDataMin,updateAll
import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.insert(0, '../CSV_APIs_Code')
from main_csv import UpadteCSV


source = pd.read_csv("../sources.csv")
try: 
    endDate = str(sys.argv[2])
    prevUpdate = True
except IndexError:
    endDate = True
    prevUpdate = False
    
dateList = date_range(str(sys.argv[1]),endDate)

portalUpdate_first(dateList,prevUpdate)
resp1 = input("Would you like to proceed with the update(Yes/No):")
if resp1 == "Yes":
    commitMessage = portalUpdate_second(dateList,prevUpdate)
    resp3 = input("Would you like to proceed with the update(Yes/No):")
    if resp3 == "Yes":
        UpadteCSV(dateList)
        print("Commit Message")
        if commitMessage == None or prevUpdate:
            commitMessage = input("Please Enter the commit Message:")
            git_push(commitMessage)
        else: 
            print(commitMessage)
            resp2 = input("Would you like to proceed with the above message?(Yes/No):")
            if resp2 == "Yes":
                git_push(commitMessage)
            elif resp2 == "No":
                commitMessage = input("Please Enter the commit Message:")
                git_push(commitMessage)
            
else:
    pass

resp_incovid = input("Would you like to push the incovid Repo?(Yes/No):")
if resp_incovid == "Yes":
    git_push_incovid("Update Untill" + str(datetime.now()))
else:
    pass


# python portalUpdate.py 2022-03-13
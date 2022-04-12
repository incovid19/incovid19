from datetime import datetime, timedelta
import os
import pandas as pd
from ExtractDataFromImage import ExtractDataFromImage
from ExtractDataFromPDF import ExtractFromPDF
from ExtractStateMyGov import ExtractStateMyGov
from getHTMLData import ExtractFromHTML
from getHTMLSources import getSources
from UpdateDerivedValues import STATE_NAMES,updateDerivedValues,removeLogging
from getTT import getTT
from getjson import createDataMin,updateAll
from tqdm import tqdm
from git import Repo

source = pd.read_csv("../sources.csv")

PATH_OF_GIT_REPO = r'/home/swiadmin/test/.git'  # make sure .git folder is properly configured
PATH_OF_INCOVID_GIT_REPO = r'/home/swiadmin/Incovid19/incovid19/.git'

def git_push(COMMIT_MESSAGE):
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(all=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote()
        origin.push()
    except:
        print('Some error occured while pushing the code')
        
def git_push_incovid(COMMIT_MESSAGE):
    try:
        repo = Repo(PATH_OF_INCOVID_GIT_REPO)
        repo.git.add(all=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote('origin main')
        origin.push()
    except:
        print('Some error occured while pushing the code') 

def portalUpdate_first(dateList,prevUpdate = False):
    df_fileStatus = GetFileStatus(dateList,False)[GetFileStatus(dateList,False)["Raw"] == "No"]
    print(df_fileStatus)
    for idx in df_fileStatus.index:
        if df_fileStatus["Input"][idx] == "No":
            DownloadData(df_fileStatus["State"][idx],date_range(df_fileStatus["Date"][idx],True))
            ExtractData(df_fileStatus["State"][idx],date_range(df_fileStatus["Date"][idx],True))
        if df_fileStatus["Input"][idx] == "Yes" and df_fileStatus["Raw"][idx] == "No":
            ExtractData(df_fileStatus["State"][idx],date_range(df_fileStatus["Date"][idx],True))
            print(df_fileStatus["State"][idx])
            if prevUpdate:
                resp = input("Would you like to Generate the final(Yes/No):")
                if resp == "Yes":
                    updateDerivedValues(df_fileStatus["State"][idx],df_fileStatus["Date"][idx])
                    updateDerivedValues(df_fileStatus["State"][idx],str((datetime.strptime(df_fileStatus["Date"][idx],"%Y-%m-%d")+timedelta(1)).date()))
    
    df_fileStatus = GetFileStatus(dateList,False)[GetFileStatus(dateList,False)["Raw"] == "No"]
    print(df_fileStatus)


def portalUpdate_second(dateList, prevUpdate):
    today = (datetime.now() - timedelta(days=0)).date()
    if "TT_final.csv" not in os.listdir("../RAWCSV/"+str(today)+"/"):
        getTT()
       
    for date in dateList:
        if not(prevUpdate): 
            runDate = str(date.date())
            removeLogging(runDate)
            for key,val in tqdm(STATE_NAMES.items()):
                print(key)
                updateDerivedValues(key,runDate)

            updateAll(date,log=True,OverWrite=False)
            df_fileStatus = GetFileStatus(dateList,False)[GetFileStatus(dateList,False)["Raw"] == "No"]
            print(df_fileStatus)
            if len(df_fileStatus) > 0:
                return "Portal Update for "+ runDate +" Without "+",".join(df_fileStatus["State"].to_list())
            else:
                return "Portal Update for "+ runDate
        else:
            print(date)
            updateAll(date,log=False,OverWrite=False)
        

def date_range_list(start, end):
    r = (end+timedelta(days=1)-start).days
    return [start+timedelta(days=i) for i in range(r)]
 
def date_range(start_date,end_date):
    if end_date == True:
        end_date = start_date
    end = datetime.strptime(end_date, '%Y-%m-%d')
    start = datetime.strptime(start_date, '%Y-%m-%d')
    dateList = date_range_list(start, end)
    return dateList

def GetFileStatus(dateList,Save = False):
    STATE = []
    INPUT = []
    RAW = []
    FINAL = []
    Date = []
    fileType = []
    for date in dateList:
        for idx in source.index:
            if source["myGov"][idx] != "yes":
                if source["StateDataSourceType"][idx] == "html" and source["myGov"][idx] != "yes":
                    form = "html"
                elif source["StateDataSourceType"][idx] == "json":
                    form = "json"
                elif source["StateDataSourceType"][idx] == "pdf":
                    form = "pdf"
                else:
                    form = "jpeg"

                STATE.append(source["StateCode"][idx])
                path = "../INPUT/"+str(date.date())+"/"
                Date.append(str(date.date()))
                fileType.append(form)
                dir_list = os.listdir(path)
                if "{}.{}".format(source["StateCode"][idx],form) in dir_list:
                    INPUT.append("Yes")
                else:
                    INPUT.append("No")
                path = "../RAWCSV/"+str(date.date())+"/"
                dir_list = os.listdir(path)
                if "{}_raw.csv".format(source["StateCode"][idx]) in dir_list:
                    # print(dir_list)
                    RAW.append("Yes")
                else:
                    RAW.append("No")
                if "{}_final.csv".format(source["StateCode"][idx]) in dir_list:
                    # print(dir_list)
                    FINAL.append("Yes")
                else:
                    FINAL.append("No")
    
    df = pd.DataFrame(list(zip(Date,STATE,INPUT,RAW,FINAL,fileType)),columns=["Date","State","Input","Raw","Final","Filetype"])
    df["myGovFlag"] = (df["Raw"] == "No") & (df["Input"] == "No")
    df['myGovFlag'] = df['myGovFlag'].map({False:'No',
                         True:'Yes'},
                         na_action=None)
    if Save:
        df.to_csv("../fileStatus.csv",index=False)
    return df


# print("Extracting Data for:" + str(today))
# for idx in source.index:
def DownloadData(state,dateList):
    for date in dateList:
        today = date.date()
        df_tmp = source[source["StateCode"] == state]
        getSources(df_tmp,today)


def ExtractData(state,dateList):
    for date in dateList:
        today = date.date()
        idx = source[source["StateCode"] == state].index[0]
        if source["StateDataSourceType"][idx] == "Image(Twitter)":
            if "{}_raw.csv".format(source["StateCode"][idx]) not in os.listdir("../RAWCSV/"+str(today)+"/"):
                ExtractDataFromImage(source["StateCode"][idx], str(today), source['Twitter Handle'][idx], source['Twitter Search Term'][idx])
        elif source["StateDataSourceType"][idx] in ["html","json"]:
            if source["myGov"][idx] != "yes":
                fileStatus = os.path.isfile(os.path.join("../INPUT",str(today),source["StateCode"][idx]+ "." + source["StateDataSourceType"][idx]))
                if not(fileStatus):
                    if source["StateCode"][idx] == "KL":
                        print(source["StateCode"][idx],str(today))
                        ExtractFromPDF(StateCode = source["StateCode"][idx],Date = str(today))
                else:
                    ExtractFromHTML(source["StateCode"][idx],str(today))
            else:
                pass
        elif source["StateDataSourceType"][idx] == "pdf":
            fileStatus = os.path.isfile(os.path.join("../INPUT",str(today),source["StateCode"][idx]+".pdf"))
            if not(fileStatus):
                pass
            else:
                ExtractFromPDF(StateCode = source["StateCode"][idx],Date = str(today))
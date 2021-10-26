import requests
import pandas as pd
import ssl
from shutil import copyfile
import datetime
from urllib.error import HTTPError
import urllib
import timedelta
from StatusMsg import StatusMsg
import inflect


p = inflect.engine()
ssl._create_default_https_context = ssl._create_unverified_context

source = pd.read_csv(r"../sources.csv")

def downloadFile(Date,StateCode,url):
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
        StatusMsg(StateCode,Date,"OK","File Downloaded",program="GetSource")
        with open(r"../INPUT/" + Date + "/" + source["StateCode"][idx] + ".pdf", 'wb') as f:
            f.write(response.content)
    else:
        print("Error")
        StatusMsg(StateCode,Date,"ERR","File Not Found",program="GetSource")

# today = str(datetime.datetime.now().date())
today = (datetime.datetime.now() - timedelta.Timedelta(days=1)).date()
for idx in source.index:
    if source["StateDataSourceType"][idx] == "html":
        try:
            file_name, headers = urllib.request.urlretrieve(source["StateDataURL"][idx])
            copyfile(file_name, r"../INPUT/" + str(today) + "/" + source["StateCode"][idx] + ".html")
            StatusMsg(source["StateCode"][idx],str(today),"OK","File Downloaded",program="GetSource")
        except HTTPError:
            StatusMsg(source["StateCode"][idx],str(today),"ERR","File Not Found",program="GetSource")
        except Exception:
            raise
            StatusMsg(source["StateCode"][idx],str(today),"ERR","Fatal Error in Main Loop",program="GetSource")
    elif source["StateDataSourceType"][idx] == "pdf":
        if source["StateCode"][idx] == "HR":
            url = 'http://nhmharyana.gov.in/WriteReadData/userfiles/file/CoronaVirus/Daily%20Bulletin%20of%20COVID%2019%20as%20on%20'+str(today.strftime("%d-%m-%Y"))+'.pdf'
            downloadFile(str(today),source["StateCode"][idx],url)
        elif source["StateCode"][idx] == "KA":
            url = 'https://covid19.karnataka.gov.in/storage/pdf-files/EMB-'+str(datetime.datetime.now().date().strftime("%B").upper()[0:3])+'21//'+str(today.strftime("%d-%m-%Y"))+'%20HMB%20English.pdf'
            downloadFile(str(today),source["StateCode"][idx],url)
        elif source["StateCode"][idx] == "PB":
            url = 'https://nhm.punjab.gov.in/advertisements/Media_Bulletin/Media%20Bulletin%20COVID-19%20'+ str(today.strftime("%d-%m-%Y")) +'.pdf'
            downloadFile(str(today),source["StateCode"][idx],url)
        elif source["StateCode"][idx] == "TN":
            url = 'https://stopcorona.tn.gov.in/wp-content/uploads/2020/03/Media-Bulletin-'+str(today.strftime("%d-%m-%y"))+'-COVID-19.pdf'
            downloadFile(str(today),source["StateCode"][idx],url)
        elif source["StateCode"][idx] == "UK":
            url = 'https://health.uk.gov.in/files/'+str(today.strftime("%Y.%m.%d"))+'_Health_Bulletin.pdf'
            downloadFile(str(today),source["StateCode"][idx],url)
        elif source["StateCode"][idx] == "WB":
            url = 'https://www.wbhealth.gov.in/uploaded_files/corona/WB_DHFW_Bulletin_'+p.ordinal(today.day).upper()+'_'+str(datetime.datetime.now().date().strftime("%B").upper()[0:3])+'_REPORT_FINAL.pdf'
            downloadFile(str(today),source["StateCode"][idx],url)
        elif source["StateCode"][idx] == "KL":
            url = 'https://dhs.kerala.gov.in/wp-content/uploads/2021/10/Bulletin-HFWD-English-'+str(datetime.datetime.now().date().strftime("%B"))+'-'+str(today.day)+'.pdf'
            downloadFile(str(today),source["StateCode"][idx],url)
        elif source["StateCode"][idx] == "MH":
            url = 'https://arogya.maharashtra.gov.in/pdf/ncovidmpressnote'+str(datetime.datetime.now().date().strftime("%B")).lower()+str(today.day)+'.pdf'
            downloadFile(str(today),source["StateCode"][idx],url)

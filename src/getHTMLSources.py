import requests
import pandas as pd
import ssl
from shutil import copyfile
from datetime import datetime, timedelta
from urllib.error import HTTPError
import urllib
from StatusMsg import StatusMsg
import inflect
from bs4 import BeautifulSoup
from urllib.request import urlopen


def downloadFile(Date, StateCode, url):
    response = requests.get(url)
    print(url)
    print(response.status_code)
    if response.status_code == 200:
        try:
            # print(response.text)
            StatusMsg(StateCode, Date, "OK", "File Downloaded", program="GetSource")
            with open(r"../INPUT/" + Date + "/" + StateCode + ".pdf", 'wb') as f:
                f.write(response.content)
        except:
            StatusMsg(StateCode, Date, "ERR", "File Not Found", program="GetSource")
    else:
        print("Error")
        StatusMsg(StateCode, Date, "ERR", "File Not Found", program="GetSource")


def getSources(source, date):
    p = inflect.engine()
    ssl._create_default_https_context = ssl._create_unverified_context

    for idx in source.index:
        print(source["StateCode"][idx])
        if source["myGov"][idx] != "yes":
            if source["StateDataSourceType"][idx] == "html":
                try:
                    file_name, headers = urllib.request.urlretrieve(source["StateDataURL"][idx])
                    copyfile(file_name, r"../INPUT/" + str(date) + "/" + source["StateCode"][idx] + ".html")
                    StatusMsg(source["StateCode"][idx], str(date), "OK",
                              "File Downloaded from" + source["StateDataURL"][idx], program="GetSource")
                except HTTPError:
                    StatusMsg(source["StateCode"][idx], str(date), "ERR", "File Not Found", program="GetSource")
                except Exception:
                    raise
                    StatusMsg(source["StateCode"][idx], str(date), "ERR", "Fatal Error in Main Loop", program="GetSource")
            elif source["StateDataSourceType"][idx] == "pdf":
                if source["StateCode"][idx] == "HR":
                    url = 'http://nhmharyana.gov.in/WriteReadData/userfiles/file/CoronaVirus/Daily%20Bulletin%20of%20COVID%2019%20as%20on%20' + date.strftime("%d-%m-%Y") + '.pdf'
                    downloadFile(str(date), source["StateCode"][idx], url)
                elif source["StateCode"][idx] == "KA":
                    url = 'https://covid19.karnataka.gov.in/storage/pdf-files/EMB-' + date.strftime("%b%y//%d-%m-%Y").upper() + '%20HMB%20English.pdf'
                    downloadFile(str(date), source["StateCode"][idx], url)
                elif source["StateCode"][idx] == "PB":
                    url = 'https://nhm.punjab.gov.in/advertisements/Media_Bulletin/Media%20Bulletin%20COVID-19%20' + date.strftime("%d-%m-%Y") + '.pdf'
                    downloadFile(str(date), source["StateCode"][idx], url)
                elif source["StateCode"][idx] == "TN":
                    url = 'https://stopcorona.tn.gov.in/wp-content/uploads/2020/03/Media-Bulletin-' + date.strftime("%d-%m-%y") + '-COVID-19.pdf'
                    downloadFile(str(date), source["StateCode"][idx], url)
                elif source["StateCode"][idx] == "UK":
                    url = 'https://health.uk.gov.in/files/' + date.strftime("%Y.%m.%d") + '_Health_Bulletin.pdf'
                    downloadFile(str(date), source["StateCode"][idx], url)
                elif source["StateCode"][idx] == "WB":
                    url = 'https://www.wbhealth.gov.in/uploaded_files/corona/WB_DHFW_Bulletin_' + p.ordinal(date.day).upper() + '_' + date.strftime("%b").upper() + '_REPORT_FINAL.pdf'
                    downloadFile(str(date), source["StateCode"][idx], url)
                elif source["StateCode"][idx] == "KL":
                    url = 'https://dhs.kerala.gov.in/wp-content/uploads/' + date.strftime("%Y/%m/Bulletin-HFWD-English-%B-%d.pdf")
                    downloadFile(str(date), source["StateCode"][idx], url)
                elif source["StateCode"][idx] == "MH":
                    url = 'https://arogya.maharashtra.gov.in/pdf/ncovidepressnote' + date.strftime("%B%d.pdf").lower()
                    downloadFile(str(date), source["StateCode"][idx], url)
                elif source["StateCode"][idx] == "ML":
                    url = 'https://meghalaya.gov.in/sites/default/files/announcement/District_Wise_' + date.strftime("%d_%b_%Y.pdf")
                    downloadFile(str(date), source["StateCode"][idx], url)
                elif source["StateCode"][idx] == "UK":
                    url = 'https://health.uk.gov.in/files/' + date.strftime("%Y.%m.%d_Health_Bulletin.pdf")
                    downloadFile(str(date), source["StateCode"][idx], url)
                elif source["StateCode"][idx] == "LA":
                    url = BeautifulSoup(urlopen("https://covid.ladakh.gov.in/").read(), features="html.parser").findAll('marquee')[0].find("a")["href"]
                    downloadFile(datetime.strptime(url[-14:-4], "%d.%m.%Y").strftime("%Y-%m-%d"), source["StateCode"][idx], url)
                elif source["StateCode"][idx] == "NL":
                    base_url = "https://covid19.nagaland.gov.in"
                    rows = BeautifulSoup(urlopen(base_url + "/daily-bulletins").read(), features="html.parser").findAll("table", {'class': "table tablesorter mb-3"})[0].findAll('tbody')[0].findAll('tr')
                    for i, tr in enumerate(rows):
                        if tr.findAll('td')[-1].getText() == date.strftime("%d %b %Y"):
                            url = base_url + tr.findAll("a", {"target": "_blank"})[0]['href']
                            downloadFile(str(date), source["StateCode"][idx], url)
                # elif source["StateCode"][idx] == "MZ":
                #     base_url = "https://health.mizoram.gov.in"
                #     url = base_url + BeautifulSoup(urlopen(base_url + "/post/covid-19-bulletin-" + date.strftime("%d%m%Y")).read(), features="html.parser").findAll("a", {"class": "attachment-link"})[0]['href']
                #     downloadFile(str(date), source["StateCode"][idx], url)


# df = pd.read_csv("../sources.csv")
# getSources(df, (datetime.today() - timedelta(1)).date())

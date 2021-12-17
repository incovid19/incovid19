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
import json
import os
import io
from urllib.error import URLError


def download_file_from_google_drive(Date, StateCode, url):
    print(url)
    id = url.split('/')[-2]
    drive_url = "https://docs.google.com/uc?export=download"
    CHUNK_SIZE = 32768
    session = requests.Session()
    try:
        response = session.get(drive_url, params={'id': id}, stream=True)
        token = None
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                token = value
        if token:
            params = {'id': id, 'confirm': token}
            response = session.get(drive_url, params=params, stream=True)
        if response.status_code == 200:
            with open(f'../INPUT/{Date}/{StateCode}.pdf', "wb") as f:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                StatusMsg(StateCode, Date, "OK", "File Downloaded. Source URL: " + url, program="GetSource")
        else:
            print("Error")
            StatusMsg(StateCode, Date, "ERR", "File Not Found", program="GetSource")
    except Exception as e:
        print("Error")
        StatusMsg(StateCode, Date, "ERR", "File Not Found", program="GetSource")


def downloadFile(Date, StateCode, url):
    response = requests.get(url)
    print(url)
    # print(response.status_code)
    if (response.status_code == 200) and (response.headers['content-type'] == "application/pdf"):
        try:
            # print(response.text)
            StatusMsg(StateCode, Date, "OK", "File Downloaded. Source URL: " + url, program="GetSource")
            with open(r"../INPUT/" + Date + "/" + StateCode + ".pdf", 'wb') as f:
                f.write(response.content)
        except:
            StatusMsg(StateCode, Date, "ERR", "File Not Found", program="GetSource")
    else:
        print("Error")
        StatusMsg(StateCode, Date, "ERR", "File Not Found", program="GetSource")


def check_date(url, state, date):
    try:
        soup = BeautifulSoup(requests.get(url, verify=False).content, 'html.parser')
        if state == 'AP':
            return datetime.strptime(soup.find_all('span', {'id': 'lblLast_Update'})[0].getText(), "%d-%m-%Y %I:%M:%S %p").date()
        if state == 'GJ':
            return datetime.strptime(soup.find_all('span', {'id': 'ctl00_body_lblDate'})[0].getText(), "%d/%m/%Y %I:%M:%S %p").date()
        if state == 'KL':
            return datetime.strptime(soup.find_all('li', {'class': 'breadcrumb-item active'})[0].getText().upper()[9:], "%d-%m-%Y %I:%M %p").date()
        if state == 'OR':
            soup.sup.clear()
            return datetime.strptime(soup.find_all('small')[1].getText().split('@ ')[1], "%I:%M %p on %d %b ").replace(year=datetime.now().year).date()
        if state == 'TR':
            return datetime.strptime(soup.find_all('span', {'id': 'ContentPlaceHolder1_lblSelectedDate'})[0].getText(), "%d %b %Y").date()
        if state == 'TT':
            return datetime.strptime(soup.find_all('div', {'class': 'updated-date'})[0].getText().split(" : ")[1].split(",")[0],
                                     "%d %b %Y").date()
    except Exception:
        return date


def getSources(source, date):
    p = inflect.engine()
    ssl._create_default_https_context = ssl._create_unverified_context

    for idx in source.index:
        print(source["StateCode"][idx])
        if source["myGov"][idx] != "yes":
            if source["StateDataSourceType"][idx] == "html":
                try:
                    if source["StateCode"][idx] == "TT":
                        file_name, headers = urllib.request.urlretrieve("https://www.mygov.in/corona-data/covid19-statewise-status/")
                        source_date = check_date(source["StateDataURL"][idx], source["StateCode"][idx], date)
                        copyfile(file_name, r"../INPUT/" + str(source_date) + "/TT_State.html")
                        copyfile(file_name, r"../INPUT/" + str(source_date) + "/TT_State" + "_" + datetime.now().strftime("%H_%M") + ".html")
                        file_name, headers = urllib.request.urlretrieve("https://www.mygov.in/covid-19")
                        with open(r"../INPUT/" + str(source_date) + "/TT.html", 'w', encoding='utf8') as fp:
                            fp.write(requests.post('https://www.mygov.in/covid-19', "html.parser").text)
                        with open(r"../INPUT/" + str(source_date) + "/TT" + "_" + datetime.now().strftime("%H_%M") + ".html", 'w', encoding='utf8') as fp:
                            fp.write(requests.post('https://www.mygov.in/covid-19', "html.parser").text)
                        # copyfile(file_name, r"../INPUT/" + str(source_date) + "/TT.html")
                        # copyfile(file_name, r"../INPUT/" + str(source_date) + "/TT" + "_" + datetime.now().strftime("%H_%M") + ".html")
                        StatusMsg(source["StateCode"][idx], str(source_date), "OK", "File Downloaded from" + source["StateDataURL"][idx], program="GetSource")
                        if source_date != date:
                            StatusMsg(source["StateCode"][idx], str(date), "ERR", "File Not Found", program="GetSource")
                    else:
                        file_name, headers = urllib.request.urlretrieve(source["StateDataURL"][idx])
                        source_date = check_date(source["StateDataURL"][idx], source["StateCode"][idx], date)
                        copyfile(file_name, r"../INPUT/" + str(source_date) + "/" + source["StateCode"][idx] + ".html")
                        copyfile(file_name, r"../INPUT/" + str(source_date) + "/" + source["StateCode"][idx] + "_" + datetime.now().strftime("%H_%M") + ".html")
                        StatusMsg(source["StateCode"][idx], str(source_date), "OK", "File Downloaded. Source URL: " + source["StateDataURL"][idx], program="GetSource")
                        if source_date != date:
                            StatusMsg(source["StateCode"][idx], str(date), "ERR", "File Not Found", program="GetSource")
                except HTTPError:
                    StatusMsg(source["StateCode"][idx], str(date), "ERR", "File Not Found", program="GetSource")
                except Exception:
                    # raise
                    StatusMsg(source["StateCode"][idx], str(date), "ERR", "Fatal Error in Main Loop", program="GetSource")
            if source["StateDataSourceType"][idx] == "json":
                if source["StateCode"][idx] == "MH":
                    response = requests.get(source["StateDataURL"][idx] + '/dbd-cases-file?_by=District&_by=Date')
                    if response.status_code == 200:
                        data = json.loads(response.content)
                        json_object = json.dumps(data)
                        source_date = datetime.fromtimestamp(int(data[0]['Date']) / 1000).date()
                        with open('../INPUT/' + str(source_date) + '/' + source["StateCode"][idx] + ".json", "w") as outfile:
                            outfile.write(json_object)
                        response_total = requests.get(source["StateDataURL"][idx] + '/dbd-kpi')
                        if response_total.status_code == 200:
                            json_object_total = json.dumps(json.loads(response_total.content)[0])
                            with open('../INPUT/' + str(source_date) + '/' + source["StateCode"][idx] + "_total.json", "w") as outfile:
                                outfile.write(json_object_total)
                        response_total = requests.get(source["StateDataURL"][idx] + '/d_testing')
                        if response_total.status_code == 200:
                            json_object_total = json.dumps(json.loads(response_total.content)[0])
                            with open('../INPUT/' + str(source_date) + '/' + source["StateCode"][idx] + "_testing.json", "w") as outfile:
                                outfile.write(json_object_total)
                        StatusMsg(source["StateCode"][idx], str(source_date), "OK", "File Downloaded from" + source["StateDataURL"][idx], program="GetSource")
                        if source_date != date:
                            StatusMsg(source["StateCode"][idx], str(date), "ERR", "File Not Found", program="GetSource")
                    else:
                        StatusMsg(source["StateCode"][idx], str(date), "ERR", "File Not Found", program="GetSource")
            elif source["StateDataSourceType"][idx] == "pdf":
                try:
                    if source["StateCode"][idx] == "HR":
                        url = 'http://nhmharyana.gov.in/WriteReadData/userfiles/file/CoronaVirus/Daily%20Bulletin%20of%20COVID%2019%20as%20on%20' + date.strftime(
                            "%d-%m-%Y") + '.pdf'
                        downloadFile(str(date), source["StateCode"][idx], url)
                    elif source["StateCode"][idx] == "KA":
                        # New code (from twitter)
                        header = json.load(io.open(r'../config/twitter.json'))
                        response = requests.get(
                            "https://api.twitter.com/2/tweets/search/recent?query=(Media Bulletin)(from:DHFWKA)&tweet.fields=created_at,entities",
                            headers=header
                        )
                        if response.status_code == 200:
                            response = json.loads(response.content)
                            for data in response['data']:
                                if datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ') >= datetime.strptime(str(date), "%Y-%m-%d"):
                                    url = data['entities']['urls'][0]['expanded_url'].split("?")[0]
                                    download_file_from_google_drive(str(date), source["StateCode"][idx], url)
                                    break
                                else:
                                    StatusMsg(source["StateCode"][idx], str(date), "ERR", "File Not Found", program="GetSource")
                        else:
                            print("Error")
                            StatusMsg(source["StateCode"][idx], str(date), "ERR", "File Not Found", program="GetSource")

                        # Old Code (from KA portal)
                        # url = 'https://covid19.karnataka.gov.in/storage/pdf-files/EMB-' + date.strftime(
                        #     "%b%y//%d-%m-%Y").upper() + '%20HMB%20English.pdf'
                        # downloadFile(str(date), source["StateCode"][idx], url)
                    elif source["StateCode"][idx] == "PB":
                        url = 'https://nhm.punjab.gov.in/advertisements/Media_Bulletin/Media%20Bulletin%20COVID-19%20' + date.strftime(
                            "%d-%m-%Y") + '.pdf'
                        downloadFile(str(date), source["StateCode"][idx], url)
                    elif source["StateCode"][idx] == "TN":
                        url = 'https://stopcorona.tn.gov.in/wp-content/uploads/2020/03/Media-Bulletin-' + date.strftime(
                            "%d-%m-%y") + '-COVID-19.pdf'
                        downloadFile(str(date), source["StateCode"][idx], url)
                    # elif source["StateCode"][idx] == "UK":
                    #     url = 'https://health.uk.gov.in/files/' + date.strftime("%Y.%m.%d") + '_Health_Bulletin.pdf'
                    #     downloadFile(str(date), source["StateCode"][idx], url)
                    elif source["StateCode"][idx] == "WB":
                        url = 'https://www.wbhealth.gov.in/uploaded_files/corona/WB_DHFW_Bulletin_' + p.ordinal(
                            date.day).upper() + '_' + date.strftime("%b").upper() + '_REPORT_FINAL.pdf'
                        downloadFile(str(date), source["StateCode"][idx], url)
                    elif source["StateCode"][idx] == "KL":
                        url = 'https://dhs.kerala.gov.in/wp-content/uploads/' + date.strftime(
                            "%Y/%m/Bulletin-HFWD-English-%B-%d.pdf")
                        downloadFile(str(date), source["StateCode"][idx], url)
                    elif source["StateCode"][idx] == "ML":
                        try:
                            url = 'https://meghalaya.gov.in/sites/default/files/announcement/District_Wise_' + date.strftime("%-d_%b_%Y.pdf")
                            # https://meghalaya.gov.in/sites/default/files/announcement/District_Wise_7_Nov_2021.pdf
                            downloadFile(str(date), source["StateCode"][idx], url)
                        except Exception:
                            try:
                                url = 'https://meghalaya.gov.in/sites/default/files/announcement/District_Wise_' + date.strftime(
                                    "%-d_%b_%y.pdf")
                                # https://meghalaya.gov.in/sites/default/files/announcement/District_Wise_7_Nov_2021.pdf
                                downloadFile(str(date), source["StateCode"][idx], url)
                            except Exception:
                                if ((int(str(date)[-2:]) == 11) or
                                        (int(str(date)[-2:]) == 12) or
                                        (int(str(date)[-2:]) == 13) or
                                        (int(str(date)[-2:]) % 10 >= 4) or
                                        (int(str(date)[-2:]) % 10 == 0)):
                                    url = 'https://meghalaya.gov.in/sites/default/files/announcement/District_Wise_' + date.strftime(
                                        "%-dth_%b_%y.pdf")
                                elif int(str(date)[-2:]) % 10 == 3:
                                    url = 'https://meghalaya.gov.in/sites/default/files/announcement/District_Wise_' + date.strftime(
                                        "%-drd_%b_%y.pdf")
                                elif int(str(date)[-2:]) % 10 == 2:
                                    url = 'https://meghalaya.gov.in/sites/default/files/announcement/District_Wise_' + date.strftime(
                                        "%-dnd_%b_%y.pdf")
                                elif int(str(date)[-2:]) % 10 == 1:
                                    url = 'https://meghalaya.gov.in/sites/default/files/announcement/District_Wise_' + date.strftime(
                                        "%-dst_%b_%y.pdf")

                    elif source["StateCode"][idx] == "UT":
                        url = 'https://health.uk.gov.in/files/' + date.strftime("%Y.%m.%d_Health_Bulletin.pdf")
                        downloadFile(str(date), source["StateCode"][idx], url)
                    elif source["StateCode"][idx] == "LA":
                        url = BeautifulSoup(urlopen("https://covid.ladakh.gov.in/", timeout=5).read(),
                                            features="html.parser").findAll('marquee')[0].find("a")["href"]
                        downloadFile(datetime.strptime(url[-14:-4], "%d.%m.%Y").strftime("%Y-%m-%d"),
                                     source["StateCode"][idx], url)
                    elif source["StateCode"][idx] == "NL":
                        base_url = "https://covid19.nagaland.gov.in"
                        rows = BeautifulSoup(urlopen(base_url + "/daily-bulletins").read(), features="html.parser").findAll("table", {'class': "table tablesorter mb-3"})[0].findAll('tbody')[0].findAll('tr')
                        for i, tr in enumerate(rows):
                            if tr.findAll('td')[-1].getText() == date.strftime("%d %b %Y"):
                                url = base_url + tr.findAll("a", {"target": "_blank"})[0]['href']
                                downloadFile(str(date), source["StateCode"][idx], url)
                except URLError:
                    pass
                except Exception as e:
                    print(e)
                    StatusMsg(source["StateCode"][idx], str(date), "ERR", "Fatal Error in PDF Loop", program="GetSource")
                # elif source["StateCode"][idx] == "MZ":
                #     base_url = "https://health.mizoram.gov.in"
                #     url = base_url + BeautifulSoup(urlopen(base_url + "/post/covid-19-bulletin-" + date.strftime("%d%m%Y")).read(), features="html.parser").findAll("a", {"class": "attachment-link"})[0]['href']
                #     downloadFile(str(date), source["StateCode"][idx], url)


# df = pd.read_csv("../sources.csv")
# getSources(df, (datetime.today() - timedelta(2)).date())
# getSources()

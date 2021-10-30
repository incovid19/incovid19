#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
from StatusMsg import StatusMsg
import re
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor
import json
import datetime
import yaml


def getAPData(path):
    soup = BeautifulSoup(open(path, encoding="utf8"), "html.parser")
    table = soup.find_all('table')
    df_summary = pd.read_html(str(table))[0]
    df_summary = df_summary.melt().dropna()
    # new data frame with split value columns
    new = df_summary["value"].str.rsplit(" ", n = 1, expand = True)
    # making separate first name column from new data frame
    df_summary["var"]= new[0]
    # making separate last name column from new data frame
    df_summary["val"]= new[1]
    # Dropping old Name columns
    df_summary.drop(columns =["value","variable"], inplace = True)
    
    df_districts = pd.read_html(str(table))[1]
    df_districts.columns = df_districts.iloc[0]
    print(df_districts.columns)
    dist_names = {"Name of the District":"District","Confirmed Cases":"Confirmed","Cured/ Discharged":"Recovered","Deceased":"Deceased"}
    df_districts.rename(columns=dist_names,inplace=True)
    print(df_districts.columns)
    df_districts = df_districts[1:-4]
    
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Andhra Pradesh'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)

    print("+"*50)
    print(df_summary)

    print("="*50)
    print(df_districts)
    return df_summary,df_districts

def getASData(path):
    soup = BeautifulSoup(open(path, encoding="utf8"), "html.parser")
    table = soup.find_all('table')
    # print(str(table))
    #reading html file from districts url in sources.csv
    df_districts = pd.read_html(str(table))[0]
    #dropping unwanted cols
    df_districts.drop(columns =["View Details"], inplace = True)
    #replacing removing - and converting them to NaN(implicit)
    df_districts.replace({"-":""},inplace =True)

    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Assam'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)

    # converting numeric col to float
    df_districts = df_districts.apply(pd.to_numeric, errors="ignore")
    # print(df_districts.sum())
    #creating dictionary that has summary data for state of Assam
    dict_temp = {"var":["Confirmed","Active","Recovered","Deceased"],"val":[df_districts.sum()[1],df_districts.sum()[2],df_districts.sum()[3],df_districts.sum()[4]]}
    df_summary = pd.DataFrame(dict_temp)

    # print("="*50)
    # print(df_districts)
    # print("="*50)
    # print(df_summary)
    return df_summary,df_districts

def getGJData(path):
    soup = BeautifulSoup(open(path, encoding="utf8"), "html.parser")
    table = soup.find_all('table')
    # print(str(table))
    #reading html file from districts url in sources.csv
    df_districts = pd.read_html(str(table))[0]
    # print(df_districts)
    #dropping unwanted cols
    df_districts.drop(columns =["People Under Quarantine"], inplace = True)
    df_districts = df_districts[:-1]
    #getting cummulative values
    df_districts["Cases Tested for COVID19"] = df_districts["Cases Tested for COVID19"].str.split().str[-1]
    df_districts["Patients Recovered"] = df_districts["Patients Recovered"].str.split().str[-1]
    
    #Renaming cols name
    df_districts.rename(columns={"Active Cases":"Active", "Cases Tested for COVID19": "Tested","Patients Recovered":"Recovered","Total Deaths":"Deceased"},inplace=True)
    
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Gujarat'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)

    df_districts = df_districts.apply(pd.to_numeric, errors="ignore")
    # print(df_districts.sum())
    #creating dictionary that has summary data for state of Assam
    dict_temp = {"var":["Tested","Active","Recovered","Deceased"],"val":[df_districts.sum()[2],df_districts.sum()[1],df_districts.sum()[3],df_districts.sum()[4]]}
    df_summary = pd.DataFrame(dict_temp)

    print("="*50)
    print(df_districts)
    print("="*50)
    print(df_summary)
    return df_summary,df_districts

def getODData(path):
    soup = BeautifulSoup(open(path, encoding="utf8"), "html.parser")
    script = soup.find_all("script")[-1].string.split(";")
    data = script[40].split("(")[-1].split(")")[0]
    df_districts = pd.read_json(data)
    df_districts.rename(columns={"vchDistrictName":"District","intConfirmed":"Confirmed","intActive":"Active","intDeceased":"Deceased","intRecovered":"Recovered"},inplace=True)
    df_districts.drop(columns=["intId","intDistid","intCategory","intOthDeceased","dtmCreatedOn","dtmReportedOn","intDistType"],inplace=True)
    df_districts = df_districts[:-1]
    
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Odisha'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    
    dict_temp = {"var":["Confirmed","Active","Recovered","Deceased"],"val":[df_districts.sum()[1],df_districts.sum()[2],df_districts.sum()[4],df_districts.sum()[3]]}
    df_summary = pd.DataFrame(dict_temp)
    print("="*50)
    print(df_districts)
    print("="*50)
    print(df_summary)
    return df_summary,df_districts

def getTRData(path):
    soup = BeautifulSoup(open(path, encoding="utf8"), "html.parser")
    table = soup.find_all('table')
    df_districts = pd.read_html(str(table),skiprows=0)[0]
    df_districts.columns =  [i[1] for i in df_districts.columns]
    df_districts = df_districts.drop(["SN","Total Person Under Surveillance (Cumulative)","No. of Persons Completed Observation Period (14 Days)",
    "Facility Surveillance","Home Surveillance","Total Persons Under Surveillance","Sample Negative","Patient Went Out of State"],axis=1).drop(8,axis=0)
    df_districts.rename(columns= {"Sample Collected & Tested":"Tested","Sample Positive":"Confirmed",
    "Patient Recovered":"Recovered","Death":"Deceased"}, inplace = True)
    dict_temp = {"var":["Confirmed","Tested","Recovered","Deceased"],"val":[df_districts.sum()[2],df_districts.sum()[1],df_districts.sum()[3],df_districts.sum()[4]]}
    df_summary = pd.DataFrame(dict_temp)
    print("="*50)
    print(df_districts)
    print("="*50)
    print(df_summary)
    return df_summary,df_districts

def getKLData(path):
    soup = BeautifulSoup(open(path, encoding="utf8"), "html.parser")
    script = soup.find_all("script")[-1].string.split(";")
    
    data = script[-3].split("=")[-1]#.split(")")[0]
    districts_json = data.split("datasets:")
    districts = districts_json[0]
    districts = districts.replace(",],","]}")
    districts = districts.replace("labels","\"District\"")
    dist = pd.read_json(districts)
    data = districts_json[1][:-1]
    
    # print("="*50)
    text_rep = {"labels":"District","datasets":"dsets"}
    for k,v in text_rep.items():
        data = data.replace(k,v)

    # print(data)
    # print("+"*50)
    text_dict = {"District":"\"District\"","dsets":"\"dsets\"","label":"\"label\"","fillColor":"\"fillColor\"","strokeColor":"\"strokeColor\"",
    "pointColor":"\"pointColor\"","pointStrokeColor":"\"pointStrokeColor\"","pointHighlightFill":"\"pointHighlightFill\"",
    "pointHighlightStroke":"\"pointHighlightStroke\"","data":"\"data\""}
    
    for k,v in text_dict.items():
        data = data.replace(k,v)

    data = data.replace(",]","]")
    # print(data)
    # print("-"*50)
    
    df_districts = pd.read_json(data)

    Confirmed = df_districts['data'][0]
    Recovered = df_districts['data'][1]
    Deceased = df_districts['data'][2]
    Active = df_districts['data'][3]

    df_district = pd.DataFrame(list(zip(dist['District'].tolist(),Confirmed, Recovered,Deceased,Active)),columns =['District','Confirmed',  'Recovered','Deceased','Active'])
    
    # df_districts.rename(columns={"vchDistrictName":"District","intConfirmed":"Confirmed","intActive":"Active","intDeceased":"Deceased","intRecovered":"Recovered"},inplace=True)
    # df_districts.drop(columns=["intId","intDistid","intCategory","intOthDeceased","dtmCreatedOn","dtmReportedOn","intDistType"],inplace=True)
    # df_districts = df_districts[:-1]
    
    df_json = pd.read_json("../DistrictMappingMaster.json")
    print(df_json)
    dist_map = df_json['Kerala'].to_dict()
    print(dist_map)
    df_district['District'].replace(dist_map,inplace=True)
    print(df_district)
    dict_temp = {"var":["Confirmed","Active","Recovered","Deceased"],"val":[df_district.sum()[1],df_district.sum()[4],df_district.sum()[2],df_district.sum()[3]]}
    df_summary = pd.DataFrame(dict_temp)
    print("="*50)
    print(df_district)
    print("="*50)
    print(df_summary)
    return df_summary,df_district


def getINDData(StateCode, Date):
    URL = "https://www.mygov.in/corona-data/covid19-statewise-status/"
    file_name, headers = urllib.request.urlretrieve(URL)

    soup = BeautifulSoup(open(file_name, encoding="utf8"), "html.parser")


    # table = soup.find_all('table')
    # df_summary = pd.read_html(str(table))[0]

    STATES = soup.find_all("div",
                           {"class": "field field-name-field-select-state field-type-list-text field-label-above"})

    CONFIRMED = soup.find_all("div", {
        "class": "field field-name-field-total-confirmed-indians field-type-number-integer field-label-above"})

    CURED_DISCHARGED = soup.find_all("div", {
        "class": "field field-name-field-cured field-type-number-integer field-label-above"})

    DEATH = soup.find_all("div", {"class": "field field-name-field-deaths field-type-number-integer field-label-above"})



    states = []
    for val in STATES:
        states.append(str(val.getText()).split(":")[1].lstrip())

    confirmed = []
    for val in CONFIRMED:
        confirmed.append(str(val.getText()).split(":")[1].lstrip())

    cured = []
    for val in CURED_DISCHARGED:
        cured.append(str(val.getText()).split(":")[1].lstrip())

    death = []
    for val in DEATH:
        death.append(str(val.getText()).split(":")[1].lstrip())

    states_data = pd.DataFrame(list(zip(states, confirmed, cured, death)))

    final_df_col = ['Date', 'State/UTCode', 'deltaConfirmedForState',
                    'deltaDeceasedForState', 'deltaRecoveredForState',
                    'deltaVaccinatedForState', '7DmaConfirmedForState',
                    '7DmaDeceasedForState', '7DmaRecoveredForState',
                    '7DmaVaccinatedForState', 'District', 'deltaConfirmedForDistrict',
                    'deltaDeceasedForDistrict', 'deltaRecoveredForDistrict',
                    'deltaVaccinatedForDistrict', '7DmaConfirmedForDistrict',
                    '7DmaDeceasedForDistrict', '7DmaRecoveredForDistrict',
                    '7DmaVaccinatedForDistrict', 'districtPopulation',
                    'tested_last_updated_district', 'tested_source_district',
                    'notesForDistrict', 'cumulativeConfirmedNumberForDistrict',
                    'cumulativeDeceasedNumberForDistrict',
                    'cumulativeRecoveredNumberForDistrict',
                    'cumulativeTestedNumberForDistrict',
                    'cumulativeVaccinatedNumberForDistrict', 'last_updated',
                    'statePopulation', 'tested_last_updated_statetested_source_state',
                    'notesForState', 'cumulativeConfirmedNumberForState',
                    'cumulativeDeceasedNumberForState', 'cumulativeRecoveredNumberForState',
                    'cumulativeTestedNumberForState', 'cumulativeVaccinatedNumberForState']

    states_data = states_data.rename(
        columns={0: "District", 1: "cumulativeConfirmedNumberForDistrict", 2: "cumulativeRecoveredNumberForDistrict",
                 3: "cumulativeDeceasedNumberForDistrict"})

    states_data["Date"] = str(datetime.datetime.now().date())

    states_data["State/UTCode"] = "India"

    states_data["cumulativeConfirmedNumberForState"] = states_data["cumulativeConfirmedNumberForDistrict"].astype(
        'int64').sum()

    states_data["cumulativeDeceasedNumberForState"] = states_data["cumulativeDeceasedNumberForDistrict"].astype(
        'int64').sum()

    states_data["cumulativeRecoveredNumberForState"] = states_data["cumulativeRecoveredNumberForDistrict"].astype(
        'int64').sum()

    states_data["last_updated"] = str(datetime.datetime.now())

    Testing = soup.find_all("div",
                            {"class": "field field-name-field-total-samples-tested field-type-text field-label-above"})

    states_data["cumulativeTestedNumberForState"] = int(Testing[0].getText().split(":")[1][1:].replace(',', ''))

    Vaccine = soup.find_all("div",
                            {"class": "field field-name-field-total-vaccinations field-type-text field-label-above"})

    states_data["cumulativeVaccinatedNumberForState"] = int(Vaccine[0].getText().split(":")[1][1:].replace(',', ''))

    states_data = states_data.reindex(columns=final_df_col)
    states_data.to_csv("../RAWCSV/{}/{}_raw.csv".format(Date, StateCode))
    # return states_data


def GenerateRawCsv(StateCode, Date, df_districts):
    URL = "https://www.mygov.in/covid-19"
    file_name, sum_headers = urllib.request.urlretrieve(URL)
    soup = BeautifulSoup(open(file_name, encoding="utf8"), "html.parser")

    df = pd.DataFrame(
        columns=["Date", "State/UTCode", "District", "tested_last_updated_district", "tested_source_district",
                 "notesForDistrict",
                 "cumulativeConfirmedNumberForDistrict", "cumulativeDeceasedNumberForDistrict",
                 "cumulativeRecoveredNumberForDistrict",
                 "cumulativeTestedNumberForDistrict", "last_updated", "tested_last_updated_state","tested_source_state",
                 "notesForState",
                 "cumulativeConfirmedNumberForState", "cumulativeDeceasedNumberForState",
                 "cumulativeRecoveredNumberForState", "cumulativeTestedNumberForState"])

    df['District'] = df_districts['District']
    if "Confirmed" in df_districts.columns:
        df['cumulativeConfirmedNumberForDistrict'] = df_districts['Confirmed']
        if StateCode != 'IN':
            df['cumulativeConfirmedNumberForState'] = df['cumulativeConfirmedNumberForDistrict'].astype('int64').sum()
        else:
            df['cumulativeConfirmedNumberForState'] = int(
                soup.findAll("div", {"class": "t_case"})[0].findAll("span", {"class": "icount"})[0].getText().replace(
                    ",", ""))
    if "Tested" in df_districts.columns:
        df['cumulativeTestedNumberForDistrict'] = df_districts['Tested']
        if StateCode != 'IN':
            df['cumulativeTestedNumberForState'] = df['cumulativeTestedNumberForDistrict'].astype('int64').sum()
        else:
            df['cumulativeTestedNumberForState'] = int(
                soup.findAll("div", {"class": "testing_result"})[0].findAll("strong")[0].getText().replace(",", ""))
    df['cumulativeDeceasedNumberForDistrict'] = df_districts['Deceased']
    df['cumulativeRecoveredNumberForDistrict'] = df_districts['Recovered']

    df['Date'] = Date
    df['State/UTCode'] = StateCode

    if StateCode != 'IN':
        df['cumulativeRecoveredNumberForState'] = df['cumulativeRecoveredNumberForDistrict'].astype('int64').sum()
    else:
        df['cumulativeRecoveredNumberForState'] = int(
            soup.findAll("div", {"class": "discharge"})[0].findAll("span", {"class": "icount"})[0].getText().replace(
                ",", ""))

    if StateCode != 'IN':
        df['cumulativeDeceasedNumberForState'] = df['cumulativeDeceasedNumberForDistrict'].astype('int64').sum()
    else:
        df['cumulativeDeceasedNumberForState'] = int(
            soup.findAll("div", {"class": "death_case"})[0].findAll("span", {"class": "icount"})[0].getText().replace(
                ",", ""))

    if StateCode == 'IN':
        for vcount in soup.findAll("div", {"class": "total-vcount"}):
            if 'yday' not in vcount.attrs['class']:
                df['cumulativeVaccinatedNumberForState'] = int(vcount.findAll("strong")[0].getText().replace(",", ""))

    df.to_csv("../RAWCSV/{}/{}_raw.csv".format(Date, StateCode))


def ExtractFromHTML(StateCode="AP", Date="2021-10-26"):
    # try:
    filepath = "../INPUT/{0}/{1}.html".format(Date, StateCode)
    if StateCode == "AP":
        df_summary, df_districts = getAPData(filepath)
        GenerateRawCsv(StateCode, Date, df_districts)
    elif StateCode == "AS":
        df_summary, df_districts = getASData(filepath)
        GenerateRawCsv(StateCode, Date, df_districts)
    elif StateCode == "GJ":
        df_summary, df_districts = getGJData(filepath)
        GenerateRawCsv(StateCode, Date, df_districts)
    elif StateCode == "OD":
        df_summary, df_districts = getODData(filepath)
        GenerateRawCsv(StateCode, Date, df_districts)
    elif StateCode == "TR":
        df_summary, df_districts = getTRData(filepath)
        GenerateRawCsv(StateCode, Date, df_districts)
    elif StateCode == "KL":
            df_summary,df_districts = getKLData(filepath)
            GenerateRawCsv(StateCode,Date,df_districts)
    elif StateCode == "IN":
        return getINDData(StateCode, Date)
    StatusMsg(StateCode, Date, "OK", "COMPLETED", "ExtractFromHTML")
    # except HTTPError:
    #     StatusMsg(StateCode,Date,"ERR","Source URL Not Accessible/ has been changed","ExtractFromHTML")
    # except Exception:
    #     StatusMsg(StateCode,Date,"ERR","Fatal error in main loop","ExtractFromHTML")

# dfsummary,dfdistricts = ExtractFromHTML(StateCode = "AP",Date = "2021-10-24")

# ExtractFromHTML(StateCode = "IN",Date = "2021-10-29")



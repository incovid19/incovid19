#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.request

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
    df_districts = df_districts.rename(columns=df_districts.loc[0]).drop(0, axis=0)
    return df_summary,df_districts

def getINDData():
    URL = "https://www.mygov.in/corona-data/covid19-statewise-status/"
    file_name, headers = urllib.request.urlretrieve(URL)

    soup = BeautifulSoup(open(file_name, encoding="utf8"), "html.parser")
    # table = soup.find_all('table')
    # df_summary = pd.read_html(str(table))[0]

    STATES = soup.find_all("div", {"class": "field field-name-field-select-state field-type-list-text field-label-above"})

    CONFIRMED = soup.find_all("div", {"class": "field field-name-field-total-confirmed-indians field-type-number-integer field-label-above"})

    CURED_DISCHARGED = soup.find_all("div", {"class": "field field-name-field-cured field-type-number-integer field-label-above"})

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

    states_data = pd.DataFrame(list(zip(states,confirmed,cured,death)))

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

    states_data = states_data.rename(columns={0:"District",1:"cumulativeConfirmedNumberForDistrict",2:"cumulativeRecoveredNumberForDistrict",3:"cumulativeDeceasedNumberForDistrict"})

    states_data["Date"] = str(datetime.datetime.now().date())

    states_data["State/UTCode"] = "India"

    states_data["cumulativeConfirmedNumberForState"] = states_data["cumulativeConfirmedNumberForDistrict"].astype('int64').sum()

    states_data["cumulativeDeceasedNumberForState"] = states_data["cumulativeDeceasedNumberForDistrict"].astype('int64').sum()

    states_data["cumulativeRecoveredNumberForState"] = states_data["cumulativeRecoveredNumberForDistrict"].astype('int64').sum()

    states_data["last_updated"] = str(datetime.datetime.now())

    Testing = soup.find_all("div", {"class": "field field-name-field-total-samples-tested field-type-text field-label-above"})

    states_data["cumulativeTestedNumberForState"] = int(Testing[0].getText().split(":")[1][1:].replace(',',''))

    Vaccine = soup.find_all("div", {"class": "field field-name-field-total-vaccinations field-type-text field-label-above"})

    states_data["cumulativeVaccinatedNumberForState"] = int(Vaccine[0].getText().split(":")[1][1:].replace(',',''))

    states_data = states_data.reindex(columns=final_df_col)
    return states_data

def ExtractFromHTML(StateCode = "AP",Date = "2021-10-24"):
    filepath = "INPUT\\" + Date + "\\" + StateCode + ".html"
    if StateCode == "AP":
        return getAPData(filepath)
    elif StateCode == "IND":
        return getINDData

# dfsummary,dfdistricts = ExtractFromHTML(StateCode = "AP",Date = "2021-10-24")
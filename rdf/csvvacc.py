#!/usr/bin/env python
# coding: utf-8

# In[113]:


import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from datetime import datetime,timedelta
import sys
sys.path.insert(0, '../src')
from util import GetFileStatus,date_range


# # Generate State file with Vaccination 

# In[2]:

def main():
    path = "/home/swiadmin/Incovid19/rdf/"
    df_state = pd.read_csv("/home/swiadmin/test/csv/latest/states.csv")

    df_state["Date"] = pd.to_datetime(df_state["Date"])

    df_state_vacc = pd.read_csv("/home/swiadmin/test/csv/latest/cowin_vaccine_data_statewise.csv")

    cols = ['Updated On','State','Total Doses Administered',
            'First Dose Administered','Second Dose Administered']

    df_state_vacc = df_state_vacc[cols]

    df_state_vacc['Updated On'] = df_state_vacc['Updated On'].apply(lambda _: datetime.strptime(_,"%d/%m/%Y"))

    df_state_vacc = df_state_vacc.merge(df_state,how="right",left_on=["Updated On","State"],right_on=["Date","State"])

    df_state_vacc["Vaccination3"] = df_state_vacc["Total Doses Administered"] - df_state_vacc["First Dose Administered"] - df_state_vacc["Second Dose Administered"]

    df_state_vacc = df_state_vacc.drop(['Updated On','Total Doses Administered'],axis=1)

    df_state_vacc = df_state_vacc.rename(columns = {"First Dose Administered":"Vaccination1","Second Dose Administered":"Vaccination2"})

    df_state_vacc.to_csv(path+"states_vacc.csv")


    df_districts = pd.read_csv("/home/swiadmin/test/csv/latest/districts.csv")

    df_district_vacc = pd.read_csv("/home/swiadmin/test/csv/latest/cowin_vaccine_data_districtwise.csv",header=[0,1])

    dateList = date_range("2021-11-01",str(datetime.today().date()-timedelta(1)))

    columns = ['State','District','First Dose Administered','Second Dose Administered','Total Doses Administered']

    df = pd.DataFrame(columns=columns)
    for date in dateList:
        try:
            df_temp = df_district_vacc.loc[:,["State","District",date.date().strftime("%d/%m/%Y")]]
            df_temp.columns = columns
            df_temp["Date"] = str(date.date())
            df = df.append(df_temp)
        except:
            print(str(date.date()))

    df = df_districts.merge(df,how="left",left_on=["Date","State","District"],right_on=["Date","State","District"])

    df["Vaccination3"] = df["Total Doses Administered"] - df["First Dose Administered"] - df["Second Dose Administered"]

    df = df.drop(['Total Doses Administered'],axis=1)

    df = df.rename(columns = {"First Dose Administered":"Vaccination1","Second Dose Administered":"Vaccination2"})

    df.to_csv(path+"districts_vacc.csv")


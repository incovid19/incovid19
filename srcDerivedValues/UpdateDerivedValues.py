#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
from datetime import datetime, timedelta
import numpy as np
from get7DMA import get_7dma_state

import json
import traceback
import time

def col_check_state_raw_csv(df):
    cols_ls=df.columns
    reqd_col_ls=["Date",
                 "State/UTCode",
                 "deltaConfirmedForState",
                 "deltaDeceasedForState",
                 "deltaRecoveredForState",
                 "deltaTestedForState",
                 "deltaVaccinated1ForState",
                 "deltaVaccinated2ForState",
                 "delta21_14confirmedForState",
                 "7DmaConfirmedForState",
                 "7DmaDeceasedForState",
                 "7DmaRecoveredForState",
                 "7DmaTestedForState",
                 "7DmaVaccinated1ForState",
                 "7DmaVaccinated2ForState",
                 "District",
                 "deltaConfirmedForDistrict",
                 "deltaDeceasedForDistrict",
                 "deltaRecoveredForDistrict",
                 "deltaTestedForDistrict",
                 "deltaVaccinated1ForDistrict",
                 "deltaVaccinated2ForDistrict",
                 "delta21_14confirmedForDistrict",
                 "7DmaConfirmedForDistrict",
                 "7DmaDeceasedForDistrict",
                 "7DmaRecoveredForDistrict",
                 "7DmaTestedForDistrict",
                 "7DmaVaccinated1ForDistrict",
                 "7DmaVaccinated2ForDistrict",
                 "districtPopulation",
                 "tested_last_updated_district",
                 "tested_source_district",
                 "notesForDistrict",
                 "cumulativeConfirmedNumberForDistrict",
                 "cumulativeDeceasedNumberForDistrict",
                 "cumulativeRecoveredNumberForDistrict",
                 "cumulativeTestedNumberForDistrict",
                 "cumulativeVaccinated1NumberForDistrict",
                 "cumulativeVaccinated2NumberForDistrict",
                 "last_updated",
                 "statePopulation",
                 "tested_last_updated_state",
                 "tested_source_state",
                 "notesForState",
                 "cumulativeConfirmedNumberForState",
                 "cumulativeDeceasedNumberForState",
                 "cumulativeRecoveredNumberForState",
                 "cumulativeTestedNumberForState",
                 "cumulativeVaccinated1NumberForState",
                 "cumulativeVaccinated2NumberForState"
                ]
    for col in reqd_col_ls:
        if col not in cols_ls:
            df[col]=0
    df_formatted=df[reqd_col_ls]
    return df_formatted
            
STATE_NAMES = {
  'AP': 'Andhra Pradesh',
  'AR': 'Arunachal Pradesh',
  'AS': 'Assam',
  'BR': 'Bihar',
  'CT': 'Chhattisgarh',
  'GA': 'Goa',
  'GJ': 'Gujarat',
  'HR': 'Haryana',
  'HP': 'Himachal Pradesh',
  'JH': 'Jharkhand',
  'KA': 'Karnataka',
  'KL': 'Kerala',
  'MP': 'Madhya Pradesh',
  'MH': 'Maharashtra',
  'MN': 'Manipur',
  'ML': 'Meghalaya',
  'MZ': 'Mizoram',
  'NL': 'Nagaland',
  'OR': 'Odisha',
  'PB': 'Punjab',
  'RJ': 'Rajasthan',
  'SK': 'Sikkim',
  'TN': 'Tamil Nadu',
  'TG': 'Telangana',
  'TR': 'Tripura',
  'UT': 'Uttarakhand',
  'UP': 'Uttar Pradesh',
  'WB': 'West Bengal',
  'AN': 'Andaman and Nicobar Islands',
  'CH': 'Chandigarh',
  'DN': 'Dadra and Nagar Haveli and Daman and Diu',
  'DL': 'Delhi',
  'JK': 'Jammu and Kashmir',
  'LA': 'Ladakh',
  'LD': 'Lakshadweep',
  'PY': 'Puducherry',
  # 'TT': 'India',
 # [UNASSIGNED_STATE_CODE]: 'Unassigned',
}

#Creating the mapping dictionary for multiple districts addition scenario
cowin_codes=pd.read_csv("../CSV/CowinAppStateAndDistrictCode.csv")
cowin_codes_map={}
cowin_codes["district_id_add"]=cowin_codes[["district_id_add"]].fillna("NULL")

for i,d_id in enumerate(cowin_codes["district_id"]):
    add_dist_id=cowin_codes.loc[i,"district_id_add"]
    if add_dist_id !="NULL":
        cowin_codes_map[str(int(d_id))]=[str(int(add_dist_id)),str(int(d_id))]
    else:
        cowin_codes_map[str(int(d_id))]=[str(int(d_id))]

def vaccination_numbers_api(state_name,Date):
    cowin_codes=pd.read_csv("../CSV/CowinAppStateAndDistrictCode.csv")
    
    if state_name=="Dadra and Nagar Haveli and Daman and Diu":
        vaccination_number_DNH=vaccination_numbers_api("Dadra and Nagar Haveli",Date)
        vaccination_number_DND=vaccination_numbers_api("Daman and Diu",Date)
        
        state_cumulative_vaccinated1=vaccination_number_DNH[0]+vaccination_number_DND[0]
        state_cumulative_vaccinated2=vaccination_number_DNH[1]+vaccination_number_DND[1]
        state_cumulative_vaccinated=vaccination_number_DNH[2]+vaccination_number_DND[2]
        district_vacc_dict=vaccination_number_DNH[3]
        district_vacc_dict.update(vaccination_number_DND[3])
        
        return(state_cumulative_vaccinated1,state_cumulative_vaccinated2,state_cumulative_vaccinated,district_vacc_dict)
    
#     print(state_name)
    district_cumulative_vaccinated1=0
    district_cumulative_vaccinated2=0
    district_cumulative_vaccinated=0
    
    state_cumulative_vaccinated1=0
    state_cumulative_vaccinated2=0
    state_cumulative_vaccinated=0
        
    if state_name=="Dadra and Nagar Haveli":
        cowin_state_code=8
    elif state_name=="Daman and Diu":
        cowin_state_code=37
    else:
        cowin_state_code=cowin_codes.loc[cowin_codes["state_name"]==state_name,"state_id"]
        cowin_state_code.reset_index(inplace=True,drop=True)
        cowin_state_code=list(set(cowin_state_code))[0]
    
    
    api_url_state="https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports?state_id="+str(cowin_state_code)+"&date="+Date
#     print(api_url_state)
    api_data_state=requests.get(api_url_state)
#     print(api_data_state.json())
    
    state_cumulative_vaccinated1=api_data_state.json()["topBlock"]["vaccination"]["tot_dose_1"]
    state_cumulative_vaccinated2=api_data_state.json()["topBlock"]["vaccination"]["tot_dose_2"]
    state_cumulative_vaccinated=api_data_state.json()["topBlock"]["vaccination"]["total"]
    
    district_vacc_dict={}
    for ele in api_data_state.json()["getBeneficiariesGroupBy"]:
        district_vacc_dict[ele["district_id"]]=[ele["partial_vaccinated"],ele["totally_vaccinated"],ele["total"]]
    
    return (state_cumulative_vaccinated1,state_cumulative_vaccinated2,state_cumulative_vaccinated,district_vacc_dict)

def addLogging(logDict:dict):
    loggingsFile = '../log.json'

    with open(loggingsFile) as f:
        data = json.load(f)

    data.append(logDict)

    with open(loggingsFile, 'w') as f:
        json.dump(data, f)

def currentTimeUTC(date):
    return int(time.mktime(datetime.strptime(date,'%Y-%m-%d').timetuple()))

def updateJSONLog(stateName,date):
    addLogging({
      "update": stateName + ":\n No district level updates received in state government bulletin",
      "timestamp": currentTimeUTC(date)
   })

def removeLogging(date):
    loggingsFile = "../log.json"
    
    with open(loggingsFile) as f:
        data = json.load(f)

    data = list(filter(lambda i: i['timestamp'] != time.mktime(datetime.strptime(date,'%Y-%m-%d').timetuple()), data))

    with open(loggingsFile, 'w') as f:
        json.dump(data, f)

def updateDerivedValues(StateCode,Date):
    cowin_codes=pd.read_csv("../CSV/CowinAppStateAndDistrictCode.csv")
    sources=pd.read_csv("../sources.csv") 
    try:
        state_raw_csv=pd.read_csv(f"../RAWCSV/{Date}/{StateCode}_raw.csv",index_col=False)
    except:
        state_raw_csv=pd.read_csv(f"../RAWCSV/{Date}/myGov/{StateCode}_raw.csv",index_col=False)
        if (sources[sources["StateCode"] == StateCode]["myGov"] != "yes").item():
            updateJSONLog((sources[sources["StateCode"] == StateCode]["StateName"]).item(),Date)
    
    state_population=pd.read_csv("../CSV/StatePopulation.csv")
    district_population=pd.read_csv("../CSV/DistrictPopulation.csv")
    
    state_raw_csv=col_check_state_raw_csv(state_raw_csv)
    
    state_name=STATE_NAMES[StateCode]
    
    state_raw_csv["State/UTCode"]=StateCode
    
    vaccination_numbers=vaccination_numbers_api(state_name,Date)
    
    state_cumulative_vaccinated1=vaccination_numbers[0]
    state_cumulative_vaccinated2=vaccination_numbers[1]
    state_cumulative_vaccinated=vaccination_numbers[2]
    
    state_raw_csv.loc[state_raw_csv["State/UTCode"]==StateCode,"cumulativeVaccinated1NumberForState"]=state_cumulative_vaccinated1
    state_raw_csv.loc[state_raw_csv["State/UTCode"]==StateCode,"cumulativeVaccinated2NumberForState"]=state_cumulative_vaccinated2
    state_raw_csv.loc[state_raw_csv["State/UTCode"]==StateCode,"cumulativeVaccinatedNumberForState"]=state_cumulative_vaccinated
    
    #Reading State population numbers from static source
    state_population_number=state_population.loc[state_population["State"]==StateCode,"StatePop"]
    state_population_number.reset_index(inplace=True,drop=True)
    state_population_number=state_population_number[0]    
    state_raw_csv.loc[state_raw_csv["State/UTCode"]==StateCode,"statePopulation"]=state_population_number
    
    #Deriving the delta numbers
    
    prev_date=datetime.strptime(Date,"%Y-%m-%d")+timedelta(days=(-1))
    prev_date_str=str(prev_date.date())
    try:
        previous_state_raw_csv=pd.read_csv(f"../RAWCSV/{prev_date_str}/{StateCode}_raw.csv")
    except:
        previous_state_raw_csv=pd.read_csv(f"../RAWCSV/{prev_date_str}/myGov/{StateCode}_raw.csv")
    
    vaccination_numbers_yesterday=vaccination_numbers_api(state_name,prev_date_str)
    
    try:
        if state_raw_csv["cumulativeConfirmedNumberForState"].sum() != 0:
            state_raw_csv["deltaConfirmedForState"]=state_raw_csv["cumulativeConfirmedNumberForState"]-previous_state_raw_csv["cumulativeConfirmedNumberForState"]
    except:
        state_raw_csv["deltaConfirmedForState"] = None
    
    try:
        if state_raw_csv["cumulativeDeceasedNumberForState"].sum() != 0:
            state_raw_csv["deltaDeceasedForState"]=state_raw_csv["cumulativeDeceasedNumberForState"]-previous_state_raw_csv["cumulativeDeceasedNumberForState"]
    except:
        state_raw_csv["deltaDeceasedForState"] = None
        
    try:    
        if state_raw_csv["cumulativeRecoveredNumberForState"].sum() != 0:
            state_raw_csv["deltaRecoveredForState"]=state_raw_csv["cumulativeRecoveredNumberForState"]-previous_state_raw_csv["cumulativeRecoveredNumberForState"]
    except:
        state_raw_csv["deltaDeceasedForState"] = None
    
    try:
        if state_raw_csv["cumulativeVaccinatedNumberForState"].sum() != 0:
            state_raw_csv["deltaVaccinatedForState"]=state_raw_csv["cumulativeVaccinatedNumberForState"][0]-vaccination_numbers_yesterday[2]
    except:
        state_raw_csv["deltaVaccinatedForState"] = None
        
    try:    
        if state_raw_csv["cumulativeVaccinated1NumberForState"].sum() != 0:
            state_raw_csv["deltaVaccinated1ForState"]=state_raw_csv["cumulativeVaccinated1NumberForState"]-vaccination_numbers_yesterday[0]
    except:
        state_raw_csv["deltaVaccinated1ForState"] =None
    
    try:
        if state_raw_csv["cumulativeVaccinated2NumberForState"].sum() != 0:
            state_raw_csv["deltaVaccinated2ForState"]=state_raw_csv["cumulativeVaccinated2NumberForState"]-vaccination_numbers_yesterday[1]
    except:
        state_raw_csv["deltaVaccinated2ForState"] = None
    
    try:        
        if state_raw_csv["cumulativeTestedNumberForState"].sum() != 0:
            state_raw_csv["deltaTestedForState"]=state_raw_csv["cumulativeTestedNumberForState"].astype("int64")-previous_state_raw_csv["cumulativeTestedNumberForState"].astype("int64")
    except FileNotFoundError:
        print("Tested Error")
        state_raw_csv["deltaTestedForState"] = None
        
    for district in state_raw_csv["District"]:
        # print(district,state_name)
        cowin_district_code=cowin_codes.loc[((cowin_codes["district_name"]==district)&(cowin_codes["state_name"]==state_name)),"district_id"]
        cowin_district_code.reset_index(inplace=True,drop=True)
        try:
            cowin_district_code=cowin_district_code[0]
        except IndexError:
            # print(f"{district} not found in Cowin States Districts Code")
            district_vaccination_data=False
            pass
        except KeyError:
            # print(f"{district} not found in Cowin States Districts Code")
            district_vaccination_data=False
            pass
        else:
            ls_districts_add=cowin_codes_map[str(cowin_district_code)]
            district_cumulative_vaccinated1=0
            district_cumulative_vaccinated2=0
            district_cumulative_vaccinated=0
            for dist in ls_districts_add:
                district_cumulative_vaccinated1+=vaccination_numbers[3][dist][0]
                district_cumulative_vaccinated2+=vaccination_numbers[3][dist][1]
                district_cumulative_vaccinated+=vaccination_numbers[3][dist][2]
                district_vaccination_data=True
                
        if district_vaccination_data:
            state_raw_csv.loc[((state_raw_csv["State/UTCode"]==StateCode)&(state_raw_csv["District"]==district)),"cumulativeVaccinated1NumberForDistrict"]=district_cumulative_vaccinated1
            state_raw_csv.loc[((state_raw_csv["State/UTCode"]==StateCode)&(state_raw_csv["District"]==district)),"cumulativeVaccinated2NumberForDistrict"]=district_cumulative_vaccinated2
            state_raw_csv.loc[((state_raw_csv["State/UTCode"]==StateCode)&(state_raw_csv["District"]==district)),"cumulativeVaccinatedNumberForDistrict"]=district_cumulative_vaccinated

        
        district_population_number=district_population.loc[((district_population["State"]==StateCode) & (district_population["District"]==district)) ,"DistrictPop"]#[0]
        district_population_number.reset_index(inplace=True,drop=True)
        try:
            district_population_number=district_population_number[0]
        except IndexError:
            print(f"{district} population numbers not found")
            pass
        except KeyError:
            print(f"{district} population numbers not found")
            pass
        else:
            state_raw_csv.loc[((state_raw_csv["State/UTCode"]==StateCode)&(state_raw_csv["District"]==district)),"districtPopulation"]=district_population_number
           
    lst = ["Recovered","Confirmed","Deceased","Tested","Vaccinated1","Vaccinated2","Vaccinated"]
    for val in lst:
        state_raw_csv["delta{}ForDistrict".format(val)] = 0
        for idx in state_raw_csv.index:
            # print(new_state_raw_csv["District"][idx])
            # print(new_state_raw_csv["7DmaVaccinatedForDistrict"][idx])
            avg_counter = 0
            value = 0
            i = 1
            prev_date=datetime.strptime(Date,"%Y-%m-%d")+timedelta(days=(-1*i))
            prev_date_str=str(prev_date.date())
            if i == 0:
                previous_state_raw_csv = state_raw_csv
            else:
                previous_state_raw_csv_vacc=pd.read_csv(f"../RAWCSV/{prev_date_str}/{StateCode}_final.csv")
                try:
                    previous_state_raw_csv=pd.read_csv(f"../RAWCSV/{prev_date_str}/{StateCode}_raw.csv")
                except:
                    previous_state_raw_csv=pd.read_csv(f"../RAWCSV/{prev_date_str}/myGov/{StateCode}_raw.csv")
                
            cowin_district_code=cowin_codes.loc[((cowin_codes["district_name"]==state_raw_csv["District"][idx])&(cowin_codes["state_name"]==state_name)),"district_id"]
            cowin_district_code.reset_index(inplace=True,drop=True)
            try:
                cowin_district_code=cowin_district_code[0]
                district_vaccination_data=True
            except IndexError:
                # print(f"{district} not found in Cowin States Districts Code")
                district_vaccination_data=False
                pass
            except KeyError:
                # print(f"{district} not found in Cowin States Districts Code")
                district_vaccination_data=False
                pass
            #Read final file for vaccination
            
            if val in ["Vaccinated1","Vaccinated2"]:                
                value = state_raw_csv["cumulative{}NumberForDistrict".format(val)][idx] - previous_state_raw_csv_vacc.loc[previous_state_raw_csv_vacc["District"] == state_raw_csv["District"][idx],"cumulative{}NumberForDistrict".format(val)]
            elif val != "Vaccinated":    
                value = state_raw_csv["cumulative{}NumberForDistrict".format(val)][idx] - previous_state_raw_csv.loc[previous_state_raw_csv["District"] == state_raw_csv["District"][idx],"cumulative{}NumberForDistrict".format(val)]
            try:
                state_raw_csv["delta{}ForDistrict".format(val)][idx] = value
            except:
                state_raw_csv["delta{}ForDistrict".format(val)][idx] = None
                
    state_raw_csv.to_csv(f"../RAWCSV/{Date}/{StateCode}_final.csv",index=False)
    print (f"Running 7DMA for {StateCode}")
    get_7dma_state(StateCode, Date)

# runDate = "2022-01-09"
# removeLogging(runDate)
# for key,val in STATE_NAMES.items():
#     updateDerivedValues(key,runDate)
    


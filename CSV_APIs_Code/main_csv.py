#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
# from datetime import datetime
import os
from datetime import datetime,timedelta
import requests

def vaccination_numbers_api_csv(state_name,Date):
    
    if state_name=="Dadra and Nagar Haveli and Daman and Diu":
        vaccination_number_DNH=vaccination_numbers_api_csv("Dadra and Nagar Haveli",Date)
        vaccination_number_DND=vaccination_numbers_api_csv("Daman and Diu",Date)
                
        First_Dose_Administered=vaccination_number_DNH[0]+vaccination_number_DND[0]
        Second_Dose_Administered=vaccination_number_DNH[1]+vaccination_number_DND[1]
        Total_Doses_Administered=vaccination_number_DNH[2]+vaccination_number_DND[2]
        Sessions=vaccination_number_DNH[3]+vaccination_number_DND[3]
        Sites=vaccination_number_DNH[4]+vaccination_number_DND[4]
        Male_Doses_Administered=vaccination_number_DNH[5]+vaccination_number_DND[5]
        Female_Doses_Administered=vaccination_number_DNH[6]+vaccination_number_DND[6]
        Transgender_Doses_Administered=vaccination_number_DNH[7]+vaccination_number_DND[7]
        Covaxin_Doses_Administered=vaccination_number_DNH[8]+vaccination_number_DND[8]
        CoviShield_Doses_Administered=vaccination_number_DNH[9]+vaccination_number_DND[9]
        Sputnik_Doses_Administered=vaccination_number_DNH[10]+vaccination_number_DND[10]
        aefi_Doses_Administered=vaccination_number_DNH[11]+vaccination_number_DND[11]
        years_18_44=vaccination_number_DNH[12]+vaccination_number_DND[12]
        years_45_60=vaccination_number_DNH[13]+vaccination_number_DND[13]
        years_60_plus=vaccination_number_DNH[14]+vaccination_number_DND[14]
        
        
        return(First_Dose_Administered,Second_Dose_Administered,Total_Doses_Administered,
            Sessions,Sites,Male_Doses_Administered,Female_Doses_Administered,Transgender_Doses_Administered,
           Covaxin_Doses_Administered,CoviShield_Doses_Administered,Sputnik_Doses_Administered,
           Sputnik_Doses_Administered,aefi_Doses_Administered,years_18_44,years_45_60,years_60_plus)
        
    if not isinstance(Date,str):
        Date=Date.strftime("%Y-%m-%d")
    
    cowin_codes=pd.read_csv("../CSV/CowinAppStateAndDistrictCode.csv")
#     print(state_name)
    state_cumulative_vaccinated1=0
    First_Dose_Administered=0
    Second_Dose_Administered=0
    Total_Doses_Administered=0
    Sessions=0
    Sites=0
    Male_Doses_Administered=0
    Female_Doses_Administered=0
    Transgender_Doses_Administered=0
    Covaxin_Doses_Administered=0
    CoviShield_Doses_Administered=0
    Sputnik_Doses_Administered=0
    Sputnik_Doses_Administered=0
    aefi_Doses_Administered=0
    years_18_44=0
    years_45_60=0
    years_60_plus=0
        
    #State Numbers
    if state_name=="Dadra and Nagar Haveli":
        cowin_state_code=8
    elif state_name=="Daman and Diu":
        cowin_state_code=37
    elif state_name=="India":
        cowin_state_code=None
    else:
        cowin_state_code=cowin_codes.loc[cowin_codes["state_name"]==state_name,"state_id"]
        cowin_state_code.reset_index(inplace=True,drop=True)
        cowin_state_code=list(set(cowin_state_code))[0]
    
    if state_name!="India":
        api_url_state="https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports?state_id="+str(cowin_state_code)+"&date="+Date
        api_data_state=requests.get(api_url_state)
    else:
        api_url_state="https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports?date="+Date
        api_data_state=requests.get(api_url_state)
        
    First_Dose_Administered=api_data_state.json()["topBlock"]["vaccination"]["tot_dose_1"]
    Second_Dose_Administered=api_data_state.json()["topBlock"]["vaccination"]["tot_dose_2"]
    Total_Doses_Administered=api_data_state.json()["topBlock"]["vaccination"]["total"]
    Sessions=api_data_state.json()["topBlock"]["sessions"]["total"]
    Sites=api_data_state.json()["topBlock"]["sites"]["total"]
    Male_Doses_Administered=api_data_state.json()["topBlock"]["vaccination"]["male"]
    Female_Doses_Administered=api_data_state.json()["topBlock"]["vaccination"]["female"]
    Transgender_Doses_Administered=api_data_state.json()["topBlock"]["vaccination"]["others"]
    Covaxin_Doses_Administered=api_data_state.json()["topBlock"]["vaccination"]["covaxin"]
    CoviShield_Doses_Administered=api_data_state.json()["topBlock"]["vaccination"]["covishield"]
    Sputnik_Doses_Administered=api_data_state.json()["topBlock"]["vaccination"]["sputnik"]
    aefi_Doses_Administered=api_data_state.json()["topBlock"]["vaccination"]["aefi"]
    years_18_44=api_data_state.json()["vaccinationByAge"]["vac_18_45"]
    years_45_60=api_data_state.json()["vaccinationByAge"]["vac_45_60"]
    years_60_plus=api_data_state.json()["vaccinationByAge"]["above_60"]
       
        
    return (First_Dose_Administered,Second_Dose_Administered,Total_Doses_Administered,
            Sessions,Sites,Male_Doses_Administered,Female_Doses_Administered,Transgender_Doses_Administered,
           Covaxin_Doses_Administered,CoviShield_Doses_Administered,Sputnik_Doses_Administered,
            aefi_Doses_Administered,years_18_44,years_45_60,years_60_plus)

def get_case_time_series(date):
    # source_path="../RAWCSV/2021-11-01"
    case_time_series_df=pd.read_csv("/home/swiadmin/test/csv/latest/case_time_series.csv")
    TT_final_df=pd.read_csv("../RAWCSV/"+ date +"/TT_final.csv")

    v=TT_final_df.loc[0,["Date","Date","deltaConfirmedForState","cumulativeConfirmedNumberForState","deltaRecoveredForState","cumulativeRecoveredNumberForState","deltaDeceasedForState","cumulativeDeceasedNumberForState"]]
    v[0]=datetime.strptime(v[0],"%Y-%m-%d")
    v[0]=datetime.strftime(v[0],"%d %B %Y")
    v_df=pd.DataFrame(v)
    v_df=v_df.T
    v_df.columns=case_time_series_df.columns
    new_case_time_series_df=pd.concat([case_time_series_df,v_df],axis=0)
    new_case_time_series_df.reset_index(inplace=True,drop=True)
    new_case_time_series_df = new_case_time_series_df.drop_duplicates()
    # dest_path=f"./{v[0]}"
    # os.makedirs(dest_path, exist_ok=True)
    new_case_time_series_df.to_csv("/home/swiadmin/test/csv/latest/case_time_series.csv",index=False)


def getStates_Districts(date):
    states_df=pd.read_csv("/home/swiadmin/test/csv/latest/states.csv")
    districts_df=pd.read_csv("/home/swiadmin/test/csv/latest/districts.csv")

    STATE_NAMES = {
        'TT': 'India',
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
      'PY': 'Puducherry'
     # [UNASSIGNED_STATE_CODE]: 'Unassigned',
    }

    districts_wise_df=pd.DataFrame(columns=["SlNo","State_Code","State","District_Key","District","Confirmed","Active","Recovered"
                                            ,"Deceased","Migrated_Other","Delta_Confirmed","Delta_Active","Delta_Recovered",
                                            "Delta_Deceased","District_Notes","Last_Updated"])
    states_wise_df=pd.DataFrame(columns=["State","Confirmed","Recovered","Deaths","Active","Last_Updated_Time","Migrated_Other","State_code",
                                         "Delta_Confirmed","Delta_Recovered","Delta_Deaths","State_Notes"])

    for state in STATE_NAMES.keys():
        state_=pd.read_csv("../RAWCSV/"+date+"/{}_final.csv".format(state))

        #states.csv
        state_values=state_.loc[0,["Date","State/UTCode","cumulativeConfirmedNumberForState","cumulativeRecoveredNumberForState",
                       "cumulativeDeceasedNumberForState","cumulativeTestedNumberForState"]]
        df_state=pd.DataFrame(state_values)
        df_state=df_state.T
        df_state["Others"]=""
        df_state["State/UTCode"]=df_state["State/UTCode"].apply(lambda val: STATE_NAMES.get(val))
        df_state=df_state[["Date","State/UTCode","cumulativeConfirmedNumberForState","cumulativeRecoveredNumberForState",
                       "cumulativeDeceasedNumberForState","Others","cumulativeTestedNumberForState"]]
        df_state.columns=states_df.columns
        states_df=pd.concat([states_df,df_state],axis=0)

        #state_wise.csv
        if state=="TT":
            state_["notesForState"]=""
        state_wise_values=state_.loc[0,["State/UTCode","cumulativeConfirmedNumberForState","cumulativeRecoveredNumberForState",
                       "cumulativeDeceasedNumberForState","last_updated","deltaConfirmedForState","deltaRecoveredForState","deltaDeceasedForState","notesForState"]]

        df_state_wise=pd.DataFrame(state_wise_values)
        df_state_wise=df_state_wise.T
        df_state_wise["Migrated_Other"]=0
        df_state_wise["Active"]=df_state_wise["cumulativeConfirmedNumberForState"]-(df_state_wise["cumulativeRecoveredNumberForState"]
                                                                                   +df_state_wise["cumulativeDeceasedNumberForState"]
                                                                                   +df_state_wise["Migrated_Other"])
        df_state_wise["State"]=df_state_wise["State/UTCode"].apply(lambda val: STATE_NAMES.get(val))

        df_state_wise=df_state_wise[["State","cumulativeConfirmedNumberForState","cumulativeRecoveredNumberForState",
                       "cumulativeDeceasedNumberForState","Active","last_updated","Migrated_Other","State/UTCode","deltaConfirmedForState","deltaRecoveredForState",
                                       "deltaDeceasedForState","notesForState"]]
        df_state_wise.columns=states_wise_df.columns
        states_wise_df=pd.concat([states_wise_df,df_state_wise],axis=0)

        #districts.csv
        if state!="TT":
            df_district=state_[["Date","State/UTCode","District","cumulativeConfirmedNumberForDistrict","cumulativeRecoveredNumberForDistrict",
                           "cumulativeDeceasedNumberForDistrict","cumulativeTestedNumberForDistrict"]]
            df_district["Others"]=""
            df_district["State/UTCode"]=df_district["State/UTCode"].apply(lambda val: STATE_NAMES.get(val))
            df_district=df_district[["Date","State/UTCode","District","cumulativeConfirmedNumberForDistrict","cumulativeRecoveredNumberForDistrict",
                           "cumulativeDeceasedNumberForDistrict","Others","cumulativeTestedNumberForDistrict"]]
            df_district.columns=districts_df.columns
            districts_df=pd.concat([districts_df,df_district],axis=0)

            #district_wise
            temp_district_df=state_[["State/UTCode","District","cumulativeConfirmedNumberForDistrict","cumulativeRecoveredNumberForDistrict",
                               "cumulativeDeceasedNumberForDistrict",'deltaConfirmedForDistrict','deltaRecoveredForDistrict','deltaDeceasedForDistrict',
                                    "notesForDistrict","last_updated"]]

            temp_district_df["State"]=temp_district_df["State/UTCode"].apply(lambda val: STATE_NAMES.get(val))
            temp_district_df["District_Key"]=temp_district_df.apply(lambda rw: rw["State/UTCode"]+"_"+rw["State"],axis=1)
            temp_district_df["Migrated_Other"]=0
            temp_district_df["SlNo"]=0

            temp_district_df.fillna(0,inplace=True)
            temp_district_df["Active"]=temp_district_df.apply(lambda rw: int(rw["cumulativeConfirmedNumberForDistrict"])-(int(rw["cumulativeRecoveredNumberForDistrict"])
                                                                                       +int(rw["cumulativeDeceasedNumberForDistrict"])+int(rw["Migrated_Other"])),axis=1)
            temp_district_df["delta_Active"]=temp_district_df.apply(lambda rw: rw["deltaConfirmedForDistrict"]-(rw["deltaRecoveredForDistrict"]
                                                                                       +rw["deltaDeceasedForDistrict"]),axis=1)

            temp_district_df=temp_district_df[["SlNo","State/UTCode","State","District_Key","District","cumulativeConfirmedNumberForDistrict",
                                              "Active","cumulativeRecoveredNumberForDistrict", "cumulativeDeceasedNumberForDistrict",
                                              "Migrated_Other",'deltaConfirmedForDistrict',"delta_Active",'deltaRecoveredForDistrict','deltaDeceasedForDistrict',
                                    "notesForDistrict","last_updated"]]

            temp_district_df.columns=districts_wise_df.columns
            districts_wise_df=pd.concat([districts_wise_df,temp_district_df],axis=0)




    states_df.reset_index(inplace=True,drop=True)
    states_df = states_df.drop_duplicates()
    states_df.to_csv("/home/swiadmin/test/csv/latest/states.csv",index=False)

    districts_df.reset_index(inplace=True,drop=True)
    districts_df = districts_df.drop_duplicates()
    districts_df = districts_df.dropna(subset=['Date'])
    districts_df.to_csv("/home/swiadmin/test/csv/latest/districts.csv",index=False)

    districts_wise_df.reset_index(inplace=True,drop=True)
    districts_wise_df["SlNo"]=districts_wise_df.index
    districts_wise_df = districts_wise_df.drop_duplicates()
    districts_wise_df.to_csv("/home/swiadmin/test/csv/latest/district_wise.csv",index=False)

    states_wise_df.reset_index(inplace=True,drop=True)
    states_wise_df = states_wise_df.drop_duplicates()
    states_wise_df.to_csv("/home/swiadmin/test/csv/latest/state_wise.csv",index=False)


def get_state_wise_daily(date):
    
    STATE_NAMES = {
        'TT': 'India',
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
      'PY': 'Puducherry'
     # [UNASSIGNED_STATE_CODE]: 'Unassigned',
    }

    
    state_wise_daily=pd.read_csv("/home/swiadmin/test/csv/latest/state_wise_daily.csv")
    # state_wise_daily=state_wise_daily.drop(["DD","UN"],axis=1)
    TT_final_df=pd.read_csv("../RAWCSV/"+ date +"/TT_final.csv")
    temp_df=TT_final_df[["District",'deltaConfirmedForDistrict','deltaRecoveredForDistrict','deltaDeceasedForDistrict']]
    rev_STATE_NAMES={v:k for k,v in STATE_NAMES.items()}
    temp_df["District"]=temp_df["District"].apply(lambda val: rev_STATE_NAMES.get(val))
    temp_df.index=temp_df["District"]
    temp_df_=temp_df[["deltaConfirmedForDistrict","deltaDeceasedForDistrict","deltaRecoveredForDistrict"]]

    temp_df_T=temp_df_.T
    temp_df_T.reset_index(inplace=True)
    temp_df_T["Date"]=TT_final_df.loc[0,"Date"]
    temp_df_T["Date_YMD"]=TT_final_df.loc[0,"Date"]

    temp_df_T["Date"]=temp_df_T["Date"].apply(lambda val: datetime.strptime(val,"%Y-%m-%d"))
    temp_df_T["Date"]=temp_df_T["Date"].apply(lambda val: datetime.strftime(val,"%d-%b-%Y"))

    temp_df_T=temp_df_T.rename(columns={"index":"Status"})
    temp_df_T.loc[temp_df_T["Status"]=="deltaConfirmedForDistrict","Status"]="Confirmed"
    temp_df_T.loc[temp_df_T["Status"]=="deltaRecoveredForDistrict","Status"]="Recovered"
    temp_df_T.loc[temp_df_T["Status"]=="deltaDeceasedForDistrict","Status"]="Deceased"
    temp_df_T["TT"]=[TT_final_df.loc[0,"deltaConfirmedForState"],
                    TT_final_df.loc[0,"deltaRecoveredForState"],
                    TT_final_df.loc[0,"deltaDeceasedForState"]]

    temp_df_T=temp_df_T[state_wise_daily.columns]
    state_wise_daily=pd.concat([state_wise_daily,temp_df_T],axis=0)
    state_wise_daily.reset_index(inplace=True,drop=True)
    state_wise_daily = state_wise_daily.drop_duplicates()
    state_wise_daily = state_wise_daily.dropna(subset=['Date'])
    state_wise_daily.to_csv("/home/swiadmin/test/csv/latest/state_wise_daily.csv",index=False)

def get_vaccine_district_final(date):
    dates_list = [date]
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
      'TT': 'India',
     # [UNASSIGNED_STATE_CODE]: 'Unassigned',
    }

    #Change the date here to get historical dates
    # date_=datetime.strptime('2021-12-04',"%Y-%m-%d")
    # dates_list= [date_+timedelta(days=i) for i in range(4)]
    # dates_list

    source_path="../RAWCSV"

    for Date in dates_list:
        tdate = Date
        date=tdate.strftime("%d/%m/%Y")
        if not isinstance(Date,str):
            Date=Date.strftime("%Y-%m-%d")
        print(Date)
        # /home/swiadmin/test/csv/latest/
        cowin_vaccine_data_districtwise_prev=pd.read_csv("/home/swiadmin/test/csv/latest/cowin_vaccine_data_districtwise.csv",header=[0,1])
        try:
            cowin_vaccine_data_districtwise_prev = cowin_vaccine_data_districtwise_prev.drop([date],axis=1)
        except:
            pass
        cowin_vaccine_data_districtwise_master=pd.DataFrame()
        for state in STATE_NAMES.keys():
            if state=="TT":
                continue
    #         print(state)
            state_=pd.read_csv(f"{source_path}/{Date}/{state}_final.csv")
            state_.dropna(subset=["District"],axis=0,inplace=True)
            state_.reset_index(inplace=True,drop=True)
            temp_state_df=pd.DataFrame()
            temp_state_df["District"]=state_["District"]
            temp_state_df["State_Code"]=state
            temp_state_df["State"]=temp_state_df["State_Code"].map(STATE_NAMES)
            temp_state_df["District_Key"]=temp_state_df.apply(lambda rw: rw["State_Code"]+"_"+rw["District"],axis=1)
            temp_state_df["First Dose Administered"]=state_["cumulativeVaccinated1NumberForDistrict"]
            temp_state_df["Second Dose Administered"]=state_["cumulativeVaccinated2NumberForDistrict"]
            temp_state_df["Total Dose Administered"]=temp_state_df["First Dose Administered"]+temp_state_df["Second Dose Administered"]
            cowin_vaccine_data_districtwise_master=pd.concat([cowin_vaccine_data_districtwise_master,temp_state_df],axis=0)

        # if not isinstance(Date,str):


        columns=pd.MultiIndex.from_tuples(zip(["District","State_Code","State",
                    "District_Key",date,date,date],
                   [" "," "," "," ","Total Doses Administered",
                    "First Dose Administered","Second Dose Administered"
                   ]))
        cowin_vaccine_data_districtwise_master.columns=columns
        cowin_vaccine_data_districtwise_master.reset_index(inplace=True,drop=True)

        cowin_vaccine_data_districtwise_latest=pd.merge(cowin_vaccine_data_districtwise_prev,cowin_vaccine_data_districtwise_master,
                                                       left_on=[("State_Code"," "),("State"," "),("District_Key"," "),("District"," ")],
                                                       right_on=[("State_Code"," "),("State"," "),("District_Key"," "),("District"," ")],
                                                       how="left")
        cowin_vaccine_data_districtwise_latest = cowin_vaccine_data_districtwise_latest.drop_duplicates()
        cowin_vaccine_data_districtwise_latest.to_csv("/home/swiadmin/test/csv/latest/cowin_vaccine_data_districtwise.csv",index=False)


def get_vaccine_state_csv(date):
    dates_list = [date]
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
      'TT': 'India',
     # [UNASSIGNED_STATE_CODE]: 'Unassigned',
    }

    #Creating the mapping dictionary for multiple districts addition scenario
    cowin_codes=pd.read_csv("../CSV/CowinAppStateAndDistrictCode.csv")
    cowin_codes_map={}
    cowin_codes["district_id_add"]=cowin_codes[["district_id_add"]].fillna("NULL")

    for i,d_id in enumerate(cowin_codes["district_id"]):
    #     print(d_id)
        add_dist_id=cowin_codes.loc[i,"district_id_add"]
        if add_dist_id !="NULL":
            cowin_codes_map[str(int(d_id))]=[str(int(add_dist_id)),str(int(d_id))]
        else:
            cowin_codes_map[str(int(d_id))]=[str(int(d_id))]

    #Change the date here to get historical dates
    # date_=datetime.strptime('2021-11-01',"%Y-%m-%d")
    # dates_list= [date_+timedelta(days=i) for i in range(37)]
    # dates_list

    #loop using the new vaccination_numbers_api_csv
    df_prev=pd.read_csv("/home/swiadmin/test/csv/latest/cowin_vaccine_data_statewise.csv",)
    for Date in dates_list:
    #     path=f"./Historical Data/CSV_api/{Date.strftime('%Y-%m-%d')}"
    #     os.makedirs(path, exist_ok=True)
        print(Date)
        i=0
        for _,state in STATE_NAMES.items(): #:["Uttar Pradesh"]
            i+=1
            print(i,state)
            df=pd.DataFrame(columns=["Updated On","State","Total Doses Administered",
                                     "Sessions","Sites","First Dose Administered","Second Dose Administered",
                                     "Male (Doses Administered)","Female (Doses Administered)","Transgender (Doses Administered)",
                                     "Covaxin (Doses Administered)","CoviShield (Doses Administered)","Sputnik V (Doses Administered)",
                                     "AEFI","18-44 Years (Doses Administered)","45-60 Years (Doses Administered)","60+ Years (Doses Administered)"
                                     ])

            vacc_data=vaccination_numbers_api_csv(state,Date)
            df.loc[i,"Updated On"]=Date
            df.loc[i,"State"]=state
            df.loc[i,"Total Doses Administered"]=vacc_data[2]
            df.loc[i,"Sessions"]=vacc_data[3]
            df.loc[i,"Sites"]=vacc_data[4]
            df.loc[i,"First Dose Administered"]=vacc_data[0]
            df.loc[i,"Second Dose Administered"]=vacc_data[1]
            df.loc[i,"Male (Doses Administered)"]=vacc_data[5]
            df.loc[i,"Female (Doses Administered)"]=vacc_data[6]
            df.loc[i,"Transgender (Doses Administered)"]=vacc_data[7]
            df.loc[i,"Covaxin (Doses Administered)"]=vacc_data[8]
            df.loc[i,"CoviShield (Doses Administered)"]=vacc_data[9]
            df.loc[i,"Sputnik V (Doses Administered)"]=vacc_data[10]
            df.loc[i,"AEFI"]=vacc_data[11]
            df.loc[i,"18-44 Years (Doses Administered)"]=vacc_data[12]
            df.loc[i,"45-60 Years (Doses Administered)"]=vacc_data[13]
            df.loc[i,"60+ Years (Doses Administered)"]=vacc_data[14]

            df_prev=pd.concat([df_prev,df],axis=0)
            df_prev.reset_index(inplace=True,drop=True)
    df_prev.to_csv("/home/swiadmin/test/csv/latest/cowin_vaccine_data_statewise.csv",index=False)

# df_prev.to_csv("cowin_vaccine_data_statewise_latest.csv",index=False)
        
        
        

# def date_range(start, end):
#     r = (end+timedelta(days=1)-start).days
#     return [start+timedelta(days=i) for i in range(r)]
 

# start_date = "2021-11-30"
# end_date = "2021-12-14"
# end = datetime.strptime(end_date, '%Y-%m-%d')
# start = datetime.strptime(start_date, '%Y-%m-%d')
# dateList = date_range(start, end)

# for date in dateList:
#     get_case_time_series(str(date.date()))
#     getStates_Districts(str(date.date()))
#     get_state_wise_daily(str(date.date()))
#     get_vaccine_district_final(date)
#     get_vaccine_state_csv(date)
# date = "2021-11-30"
date = (datetime.now() - timedelta(days=1)).date()
get_case_time_series(str(date))
getStates_Districts(str(date))
get_state_wise_daily(str(date))
get_vaccine_district_final(date)
get_vaccine_state_csv(date)
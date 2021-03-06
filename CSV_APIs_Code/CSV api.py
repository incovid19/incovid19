
import pandas as pd
import numpy as np
from datetime import datetime
import os



source_path="../RAWCSV/2021-11-01"
case_time_series_df=pd.read_csv("./case_time_series.csv")
TT_final_df=pd.read_csv("./TT_final.csv")

v=TT_final_df.loc[0,["Date","Date","deltaConfirmedForState","cumulativeConfirmedNumberForState","deltaRecoveredForState","cumulativeRecoveredNumberForState","deltaDeceasedForState","cumulativeDeceasedNumberForState"]]
v[0]=datetime.strptime(v[0],"%Y-%m-%d")
v[0]=datetime.strftime(v[0],"%d-%B-%Y")
v_df=pd.DataFrame(v)
v_df=v_df.T
v_df.columns=case_time_series_df.columns
new_case_time_series_df=pd.concat([case_time_series_df,v_df],axis=0)
new_case_time_series_df.reset_index(inplace=True,drop=True)

dest_path=f"./{v[0]}"
os.makedirs(dest_path, exist_ok=True)
new_case_time_series_df.to_csv(f"{dest_path}/case_time_series.csv")


# - **states.csv** 
# - **districts.csv**
# - **state_wise**
# - **district_wise**


states_df=pd.read_csv("./states.csv")
districts_df=pd.read_csv("./districts.csv")



states_df.tail()




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
    state_=pd.read_csv(f"{source_path}/{state}_final.csv")
    
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
states_df.to_csv(f"{dest_path}/states.csv",index=False)

districts_df.reset_index(inplace=True,drop=True)
districts_df.to_csv(f"{dest_path}/districts.csv",index=False)

districts_wise_df.reset_index(inplace=True,drop=True)
districts_wise_df["SlNo"]=districts_wise_df.index
districts_wise_df.to_csv(f"{dest_path}/district_wise.csv",index=False)

states_wise_df.reset_index(inplace=True,drop=True)
states_wise_df.to_csv(f"{dest_path}/state_wise.csv",index=False)

#sate_wise_daily

state_wise_daily=pd.read_csv("./state_wise_daily.csv")
state_wise_daily=state_wise_daily.drop(["DD","UN"],axis=1)
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
print(temp_df_T.head())
temp_df_T.loc[temp_df_T["Status"]=="deltaConfirmedForDistrict","Status"]="Confirmed"
temp_df_T.loc[temp_df_T["Status"]=="deltaRecoveredForDistrict","Status"]="Recovered"
temp_df_T.loc[temp_df_T["Status"]=="deltaDeceasedForDistrict","Status"]="Deceased"
temp_df_T["TT"]=[TT_final_df.loc[0,"deltaConfirmedForState"],
                TT_final_df.loc[0,"deltaRecoveredForState"],
                TT_final_df.loc[0,"deltaDeceasedForState"]]

temp_df_T.head()

temp_df_T=temp_df_T[state_wise_daily.columns]
state_wise_daily=pd.concat([state_wise_daily,temp_df_T],axis=0)
state_wise_daily.reset_index(inplace=True,drop=True)
state_wise_daily.to_csv(f"{dest_path}/state_wise_daily.csv",index=False)



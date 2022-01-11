import pandas as pd
import requests
from datetime import datetime, timedelta
import numpy as np

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

cowin_codes=pd.read_csv("./CSV/CowinAppStateAndDistrictCode.csv")
cowin_codes=pd.read_csv("./CSV/CowinAppStateAndDistrictCode.csv")
cowin_codes_map={}
cowin_codes["district_id_add"]=cowin_codes[["district_id_add"]].fillna("NULL")

for i,d_id in enumerate(cowin_codes["district_id"]):
#     print(d_id)
    add_dist_id=cowin_codes.loc[i,"district_id_add"]
    if add_dist_id !="NULL":
        cowin_codes_map[str(int(d_id))]=[str(int(add_dist_id)),str(int(d_id))]
    else:
        cowin_codes_map[str(int(d_id))]=[str(int(d_id))]

def vaccination_numbers_api(state_name,Date):
    cowin_codes=pd.read_csv("./CSV/CowinAppStateAndDistrictCode.csv")
#     print(state_name)
    district_cumulative_vaccinated1=0
    district_cumulative_vaccinated2=0
    district_cumulative_vaccinated=0
    
    state_cumulative_vaccinated1=0
    state_cumulative_vaccinated2=0
    state_cumulative_vaccinated=0
        
    #State Numbers
    cowin_state_code=cowin_codes.loc[cowin_codes["state_name"]==state_name,"state_id"]
    cowin_state_code.reset_index(inplace=True,drop=True)
    cowin_state_code=list(set(cowin_state_code))[0]
    print(cowin_state_code)
    
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

def UpdateDerivedValues(StateCode:str,Date:str,):
    """
    This function 
    1. Calulates the derived columns – Delta, Delta7 (Statewise and Districtwise) ;
    2. Updates district and population data for the state and districts of the state
    3. Updates Cumulative vaccinated numbers for the state
    4. Calculates the derived numbers for the state
    
    Input: RAWCSV file of each state    
    Output: CSV file updated with the above mentioned values
    Parameters:
    StateCode: StateCode of the corresponding State
    Date: Current Date in format "YYYY-MM-DD" type-casted as string
    
    """
    #Reading CSVs
    cowin_codes=pd.read_csv("../CSV/CowinAppStateAndDistrictCode.csv")
#     sources=pd.read_csv("Sources.csv")
#     state_districts=pd.read_csv("StateDistricts.csv")
    state_raw_csv=pd.read_csv(f"../RAWCSV/{Date}/{StateCode}_raw.csv",index_col=False)
    state_population=pd.read_csv("../CSV/StatePopulation.csv")
    district_population=pd.read_csv("../CSV/DistrictPopulation.csv")
    
    
    #Check and insert cummulativeDeceasedState 
    if state_raw_csv["cumulativeDeceasedNumberForState"].sum() == 0:
        if state_raw_csv["cumulativeDeceasedNumberForDistrict"].sum() != 0:
            state_raw_csv["cumulativeDeceasedNumberForState"] = state_raw_csv["cumulativeDeceasedNumberForDistrict"].sum()
    
    #Check for columns in state_raw_csv
    
    state_raw_csv=col_check_state_raw_csv(state_raw_csv)
#     print(state_raw_csv.head())
    
    #Reading the cumulative vaccinated numbers for the state using API
    
    state_name=STATE_NAMES[StateCode]
    print("\n")
    print(state_name)
    print("---------------------------------")
    
     #Add state/ut code
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
    
    #Reading the cumulative vaccinated numbers for the districts of the state
    districts=[district for district in state_raw_csv["District"]]
    # print(districts)
    for district in districts:
        print(district,state_name)
        cowin_district_code=cowin_codes.loc[((cowin_codes["district_name"]==district)&(cowin_codes["state_name"]==state_name)),"district_id"]
        cowin_district_code.reset_index(inplace=True,drop=True)
        try:
            cowin_district_code=cowin_district_code[0]
        except IndexError:
            print(f"{district} not found in Cowin States Districts Code")
            district_vaccination_data=False
            pass
        except KeyError:
            print(f"{district} not found in Cowin States Districts Code")
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
            
            #Reading District population numbers from static source
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
            
            state_raw_csv.loc[((state_raw_csv["State/UTCode"]==StateCode)&(state_raw_csv["District"]==district)),"cumulativeVaccinated1NumberForDistrict"]=district_cumulative_vaccinated1
            state_raw_csv.loc[((state_raw_csv["State/UTCode"]==StateCode)&(state_raw_csv["District"]==district)),"cumulativeVaccinated2NumberForDistrict"]=district_cumulative_vaccinated2
            state_raw_csv.loc[((state_raw_csv["State/UTCode"]==StateCode)&(state_raw_csv["District"]==district)),"cumulativeVaccinatedNumberForDistrict"]=district_cumulative_vaccinated

        #Deriving the delta numbers
        
        prev_date=datetime.strptime(Date,"%Y-%m-%d")+timedelta(days=(-1))
        prev_date_str=str(prev_date.year)+"-"+str(prev_date.month)+"-"+str(prev_date.day)
        previous_state_raw_csv=pd.read_csv(f"RAWCSV/{prev_date_str}/{StateCode}_raw.csv")
        
        
        # print(type(state_raw_csv["District"]),state_raw_csv.columns)
        
        # for district in state_raw_csv["District"]:
        # print(district)
        # print(state_raw_csv.loc[state_raw_csv["District"] == district,"cumulativeConfirmedNumberForDistrict"].item())
        # print(8*"*")
        # print(previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeConfirmedNumberForDistrict"])
        # print(8*"*")
        # print(state_raw_csv.loc[state_raw_csv["District"] == district,"cumulativeConfirmedNumberForDistrict"].item()-previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeConfirmedNumberForDistrict"].item())
        if state_raw_csv["cumulativeConfirmedNumberForDistrict"].sum() != 0:
            state_raw_csv.loc[state_raw_csv["District"] == district,"deltaConfirmedForDistrict"]=state_raw_csv.loc[state_raw_csv["District"] == district,"cumulativeConfirmedNumberForDistrict"].item()-previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeConfirmedNumberForDistrict"].item()

        if state_raw_csv["cumulativeDeceasedNumberForDistrict"].sum() != 0:
            state_raw_csv.loc[state_raw_csv["District"] == district,"deltaDeceasedForDistrict"]=state_raw_csv.loc[state_raw_csv["District"] == district,"cumulativeDeceasedNumberForDistrict"].item()-previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeDeceasedNumberForDistrict"].item()

        if state_raw_csv["cumulativeRecoveredNumberForDistrict"].sum() != 0:
            state_raw_csv.loc[state_raw_csv["District"] == district,"deltaRecoveredForDistrict"]=state_raw_csv.loc[state_raw_csv["District"] == district,"cumulativeRecoveredNumberForDistrict"].item()-previous_state_raw_csv.loc[previous_state_raw_csv["District"]  == district,"cumulativeRecoveredNumberForDistrict"].item()

        if state_raw_csv["cumulativeTestedNumberForDistrict"].sum() != 0:
            state_raw_csv.loc[state_raw_csv["District"] == district,"deltaTestedForDistrict"]=state_raw_csv.loc[state_raw_csv["District"] == district,"cumulativeTestedNumberForDistrict"].item()-previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeTestedNumberForDistrict"].item()

        if state_raw_csv["cumulativeVaccinatedNumberForDistrict"].sum() != 0:
            state_raw_csv.loc[state_raw_csv["District"] == district,"deltaVaccinatedForDistrict"]=state_raw_csv.loc[state_raw_csv["District"] == district,"cumulativeVaccinatedNumberForDistrict"].item()-previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeVaccinatedNumberForDistrict"].item()

        if state_raw_csv["cumulativeVaccinated1NumberForDistrict"].sum() != 0:
            state_raw_csv.loc[state_raw_csv["District"] == district,"deltaVaccinated1ForDistrict"]=state_raw_csv.loc[state_raw_csv["District"] == district,"cumulativeVaccinated1NumberForDistrict"].item()-previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeVaccinated1NumberForDistrict"].item()

        if state_raw_csv["cumulativeVaccinated2NumberForDistrict"].sum() != 0:
            state_raw_csv.loc[state_raw_csv["District"] == district,"deltaVaccinated2ForDistrict"]=state_raw_csv.loc[state_raw_csv["District"] == district,"cumulativeVaccinated2NumberForDistrict"].item()-previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeVaccinated2NumberForDistrict"].item()
            
                
        if state_raw_csv["cumulativeConfirmedNumberForState"].sum() != 0:
            # print(state_raw_csv["cumulativeConfirmedNumberForState"],type(state_raw_csv["cumulativeConfirmedNumberForState"]))
            state_raw_csv["deltaConfirmedForState"]=state_raw_csv["cumulativeConfirmedNumberForState"]-previous_state_raw_csv["cumulativeConfirmedNumberForState"]
        
        if state_raw_csv["cumulativeDeceasedNumberForState"].sum() != 0:
            state_raw_csv["deltaDeceasedForState"]=state_raw_csv["cumulativeDeceasedNumberForState"]-previous_state_raw_csv["cumulativeDeceasedNumberForState"]
        
        if state_raw_csv["cumulativeRecoveredNumberForState"].sum() != 0:
            state_raw_csv["deltaRecoveredForState"]=state_raw_csv["cumulativeRecoveredNumberForState"]-previous_state_raw_csv["cumulativeRecoveredNumberForState"]
        
        if state_raw_csv["cumulativeVaccinatedNumberForState"].sum() != 0:
            # print("today")
            # print(state_raw_csv["cumulativeVaccinatedNumberForState"])
            # print("yesterday")
            # print(previous_state_raw_csv["cumulativeVaccinatedNumberForState"])
            # print("Difference")
            # print(state_raw_csv["cumulativeVaccinatedNumberForState"]-previous_state_raw_csv["cumulativeVaccinatedNumberForState"])
            state_raw_csv["deltaVaccinatedForState"]=state_raw_csv["cumulativeVaccinatedNumberForState"][0]-previous_state_raw_csv["cumulativeVaccinatedNumberForState"][0]
        
        state_raw_csv["deltaVaccinated1ForState"]=state_raw_csv["cumulativeVaccinated1NumberForState"]-previous_state_raw_csv["cumulativeVaccinated1NumberForState"]
        state_raw_csv["deltaVaccinated2ForState"]=state_raw_csv["cumulativeVaccinated2NumberForState"]-previous_state_raw_csv["cumulativeVaccinated2NumberForState"]
        
        
        if state_raw_csv["cumulativeTestedNumberForState"].sum() != 0:
            state_raw_csv["deltaTestedForState"]=state_raw_csv["cumulativeTestedNumberForState"]-previous_state_raw_csv["cumulativeTestedNumberForState"]
        
       
        
        if district_vaccination_data:
            state_raw_csv["deltaVaccinatedForDistrict"]=state_raw_csv["cumulativeVaccinatedNumberForDistrict"]-previous_state_raw_csv["cumulativeVaccinatedNumberForDistrict"]
        avg_counter=1
        
        state_raw_csv["delta7ConfirmedForState"]=0
        state_raw_csv["delta7DeceasedForState"]=0
        state_raw_csv["delta7RecoveredForState"]=0
        state_raw_csv["delta7VaccinatedForState"]=0
        state_raw_csv["delta7TestedForState"]=0
        
        state_raw_csv["delta7ConfirmedForDistrict"]=0
        state_raw_csv["delta7DeceasedForDistrict"]=0
        state_raw_csv["delta7RecoveredForDistrict"]=0
        state_raw_csv["delta7VaccinatedForDistrict"]=0
        state_raw_csv["delta7TestedForState"]=0
        
        #Logic
        #delta7:# on (today) - # of (today-7)
        #delta21_14_: # on (today-21) - # of (today-14)
        #7dma: {(# of today)+(# of today-1)+(# of today-2)+(# of today-3)+(# of today-4)+(# of today-5+# of today-6)}/7
        
        prev_date7=datetime.strptime(Date,"%Y-%m-%d")+timedelta(days=-7)
        prev_date_str=str(prev_date7.year)+"-"+str(prev_date7.month)+"-"+str(prev_date7.day)
        previous_state_raw_csv=pd.read_csv(f"RAWCSV/{prev_date_str}/{StateCode}_raw.csv")
        
        # print(state_raw_csv["cumulativeConfirmedNumberForState"],type(state_raw_csv["cumulativeConfirmedNumberForState"]))
        state_raw_csv["delta7ConfirmedForState"]=state_raw_csv["cumulativeConfirmedNumberForState"]-previous_state_raw_csv["cumulativeConfirmedNumberForState"]
        state_raw_csv["delta7DeceasedForState"]=state_raw_csv["cumulativeDeceasedNumberForState"]-previous_state_raw_csv["cumulativeDeceasedNumberForState"]
        state_raw_csv["delta7RecoveredForState"]=state_raw_csv["cumulativeRecoveredNumberForState"]-previous_state_raw_csv["cumulativeRecoveredNumberForState"]
        state_raw_csv["delta7VaccinatedForState"]=state_raw_csv["cumulativeVaccinatedNumberForState"]-previous_state_raw_csv["cumulativeVaccinatedNumberForState"]
        state_raw_csv["delta7TestedForState"]=state_raw_csv["cumulativeTestedNumberForState"]-previous_state_raw_csv["cumulativeTestedNumberForState"]

        state_raw_csv["delta7ConfirmedForDistrict"]=state_raw_csv["cumulativeConfirmedNumberForDistrict"]-previous_state_raw_csv["cumulativeConfirmedNumberForDistrict"]
        state_raw_csv["delta7DeceasedForDistrict"]=state_raw_csv["cumulativeDeceasedNumberForDistrict"]-previous_state_raw_csv["cumulativeDeceasedNumberForDistrict"]
        state_raw_csv["delta7RecoveredForDistrict"]=state_raw_csv["cumulativeRecoveredNumberForDistrict"]-previous_state_raw_csv["cumulativeRecoveredNumberForDistrict"]
        state_raw_csv["delta7VaccinatedForDistrict"]=state_raw_csv["cumulativeVaccinatedNumberForDistrict"]-previous_state_raw_csv["cumulativeVaccinatedNumberForDistrict"]
        state_raw_csv["delta7VaccinatedForDistrict"]=state_raw_csv["cumulativeTestedNumberForDistrict"]-previous_state_raw_csv["cumulativeTestedNumberForDistrict"]

        
        prev_date21=datetime.strptime(Date,"%Y-%m-%d")+timedelta(days=-21)
        prev_date_21_str=prev_date21.strftime("%Y-%m-%d")
#         str(prev_date21.year)+"-"+str(prev_date21.month)+"-"+str(prev_date21.day)
        previous_state_21_raw_csv=pd.read_csv(f"RAWCSV/{prev_date_21_str}/{StateCode}_raw.csv")
        
        prev_date14=datetime.strptime(Date,"%Y-%m-%d")+timedelta(days=-14)
        prev_date_14_str=str(prev_date14.year)+"-"+str(prev_date14.month)+"-"+str(prev_date14.day)
        previous_state_14_raw_csv=pd.read_csv(f"RAWCSV/{prev_date_14_str}/{StateCode}_raw.csv")
        
        state_raw_csv["delta21_14ConfirmedForState"]=previous_state_14_raw_csv["cumulativeConfirmedNumberForState"]-previous_state_21_raw_csv["cumulativeConfirmedNumberForState"]
        
        # for district in state_raw_csv["District"]:
        state_raw_csv.loc[state_raw_csv["District"] == district,"delta21_14ConfirmedForDistrict"]=previous_state_14_raw_csv.loc[previous_state_14_raw_csv["District"] == district,"cumulativeConfirmedNumberForDistrict"].item()-previous_state_21_raw_csv.loc[previous_state_21_raw_csv["District"] == district,"cumulativeConfirmedNumberForDistrict"].item()
                
        state_raw_csv.loc[:,"7DmaConfirmedForState"]=0
        state_raw_csv.loc[:,"7DmaDeceasedForState"]=0
        state_raw_csv.loc[:,"7DmaRecoveredForState"]=0
        state_raw_csv.loc[:,"7DmaVaccinatedForState"]=0
        state_raw_csv.loc[:,"7DmaTestedForState"]=0
        state_raw_csv.loc[:,"7DmaVaccinated1ForState"]=0
        state_raw_csv.loc[:,"7DmaVaccinated2ForState"]=0

        state_raw_csv.loc[:,"7DmaConfirmedForDistrict"]=0
        state_raw_csv.loc[:,"7DmaDeceasedForDistrict"]=0
        state_raw_csv.loc[:,"7DmaRecoveredForDistrict"]=0
        state_raw_csv.loc[:,"7DmaVaccinatedForDistrict"]=0
        state_raw_csv.loc[:,"7DmaTestedForDistrict"]=0
        state_raw_csv.loc[:,"7DmaVaccinated1ForDistrict"]=0
        state_raw_csv.loc[:,"7DmaVaccinated2ForDistrict"]=0
        x=0
        
        
        avg_counter = 0
        for i in range(7):
            prev_date=datetime.strptime(Date,"%Y-%m-%d")+timedelta(days=(-1*i))
            print(str(prev_date))
            prev_date_str=str(prev_date.year)+"-"+str(prev_date.month)+"-"+str(prev_date.day)
            previous_state_raw_csv=pd.read_csv(f"RAWCSV/{prev_date_str}/{StateCode}_raw.csv")
            
            state_raw_csv["7DmaConfirmedForState"]+=previous_state_raw_csv["cumulativeConfirmedNumberForState"]
            state_raw_csv["7DmaDeceasedForState"]+=previous_state_raw_csv["cumulativeDeceasedNumberForState"]
            state_raw_csv["7DmaRecoveredForState"]+=previous_state_raw_csv["cumulativeRecoveredNumberForState"]
            state_raw_csv["7DmaVaccinatedForState"]+=previous_state_raw_csv["cumulativeVaccinatedNumberForState"]
            state_raw_csv["7DmaTestedForState"]+=previous_state_raw_csv["cumulativeTestedNumberForState"]
            state_raw_csv["7DmaVaccinated1ForState"]+=previous_state_raw_csv["cumulativeVaccinated1NumberForState"]
            state_raw_csv["7DmaVaccinated2ForState"]+=previous_state_raw_csv["cumulativeVaccinated2NumberForState"]
            
            
#             x=x+state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinatedForDistrict"].item() + previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeVaccinatedNumberForDistrict"].item()
#             y=previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeVaccinatedNumberForDistrict"].item()
#             print(x,y)
#             print(x+y)
            avg_counter+=1
        # state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinatedForDistrict"] = x
        # print(type(state_raw_csv.loc[state_raw_csv.loc[state_raw_csv["District"] == district].index.item(),"7DmaVaccinatedForDistrict"]))
        # state_raw_csv.loc[state_raw_csv.loc[state_raw_csv["District"] == district].index.item(),"7DmaVaccinatedForDistrict"] = float(x)
        # test.loc[test.loc[test["max_speed"] == 4,"shield"].index.item(),"shield"]
        # print(state_raw_csv["7DmaVaccinatedForDistrict"])# = x
#             # for district in state_raw_csv["District"]:
#             # state_raw_csv["7DmaVaccinatedForDistrict"] = state_raw_csv["7DmaVaccinatedForDistrict"].astype('float')
#             state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaConfirmedForDistrict"] = state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaConfirmedForDistrict"].item() + previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeConfirmedNumberForDistrict"].item()
#             state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaDeceasedForDistrict"] = state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaDeceasedForDistrict"].item() + previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeDeceasedNumberForDistrict"].item()
#             state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaRecoveredForDistrict"] = state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaRecoveredForDistrict"].item() + previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeRecoveredNumberForDistrict"].item()
#             state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinatedForDistrict"][state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinatedForDistrict"].index] = state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinatedForDistrict"].item() + previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeVaccinatedNumberForDistrict"].item()
#             print("District Vac")
#             print(state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaConfirmedForDistrict"].index)
#             print(previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeVaccinatedNumberForDistrict"])
#             print("Vac Total")
#             print(state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinatedForDistrict"])
#             state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaTestedForDistrict"] = state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaTestedForDistrict"].item() + previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeTestedNumberForDistrict"].item()
#             state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinated1ForDistrict"] = state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinated1ForDistrict"].item()+previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeVaccinated1NumberForDistrict"].item()
#             state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinated2ForDistrict"] = state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinated2ForDistrict"].item() + previous_state_raw_csv.loc[previous_state_raw_csv["District"] == district,"cumulativeVaccinated2NumberForDistrict"].item()

            
            
        state_raw_csv["7DmaConfirmedForState"]=round(state_raw_csv["7DmaConfirmedForState"]/avg_counter,0)
        state_raw_csv["7DmaDeceasedForState"]=round(state_raw_csv["7DmaDeceasedForState"]/avg_counter,0)
        state_raw_csv["7DmaRecoveredForState"]=round(state_raw_csv["7DmaRecoveredForState"]/avg_counter,0)
        state_raw_csv["7DmaVaccinatedForState"]=round(state_raw_csv["7DmaVaccinatedForState"]/avg_counter,0)
        state_raw_csv["7DmaTestedForState"]=round(state_raw_csv["7DmaTestedForState"]/avg_counter,0)
        state_raw_csv["7DmaVaccinated1ForState"]=round(state_raw_csv["7DmaVaccinated1ForState"]/avg_counter,0)
        state_raw_csv["7DmaVaccinated2ForState"]=round(state_raw_csv["7DmaVaccinated2ForState"]/avg_counter,0)
        
        
        
#         state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaConfirmedForDistrict"]=round(state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaConfirmedForDistrict"].item()/avg_counter,0)
#         state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaDeceasedForDistrict"]=round(state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaDeceasedForDistrict"].item()/avg_counter,0)
#         state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaRecoveredForDistrict"]=round(state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaRecoveredForDistrict"].item()/avg_counter,0)
#         # if state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinatedForDistrict"].isna().item():
#         #     state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinatedForDistrict"] = 0
#         # else:
#         # state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinatedForDistrict"] = round(state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinatedForDistrict"].item()/avg_counter,0)
#         state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaTestedForDistrict"]=round(state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaTestedForDistrict"].item()/avg_counter,0)
#         state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinated1ForDistrict"]=round(state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinated1ForDistrict"].item()/avg_counter,0)
#         state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinated2ForDistrict"]=round(state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinated2ForDistrict"].item()/avg_counter,0)
        
        # state_raw_csv["7DmaVaccinatedForDistrict"] = round(state_raw_csv["7DmaVaccinatedForDistrict"]/avg_counter,0)
        
        
#         print("Vac Avg")
#         print(round(state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinatedForDistrict"]/avg_counter,0))
#         print(10*"&")
#         print(state_raw_csv["7DmaVaccinatedForDistrict"])



        # if state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinatedForDistrict"].isna().item():
        #     print("True")
            # print(int(round(state_raw_csv.loc[state_raw_csv["District"] == district,"7DmaVaccinatedForDistrict"].item()/avg_counter,0)))
        
#         state_raw_csv["delta21_14ConfirmedForState"]=previous_state_raw_csv["cumulativeConfirmedNumberForState"]
        
#         state_raw_csv["delta14ConfirmedForState"]=0
#         state_raw_csv["delta21ConfirmedForState"]=0
        
#         for i in range(8,15):
#             prev_date=datetime.strptime(Date,"%Y-%m-%d")+timedelta(days=(-1*i))
#             prev_date_str=str(prev_date.year)+"-"+str(prev_date.month)+"-"+str(prev_date.day)
#             previous_state_raw_csv=pd.read_csv(f"./RAWCSV/{prev_date_str}/{StateCode}_raw.csv")
           
#             state_raw_csv["delta14ConfirmedForState"]+=previous_state_raw_csv["cumulativeConfirmedNumberForState"]
            
#         state_raw_csv["delta21ConfirmedForState"]=state_raw_csv["delta14ConfirmedForState"]
#         for i in range(15,22):
#             prev_date=datetime.strptime(Date,"%Y-%m-%d")+timedelta(days=(-1*i))
#             prev_date_str=prev_date.strftime('%Y-%m-%d')
# #             print(prev_date,prev_date_str)
#             previous_state_raw_csv=pd.read_csv(f"./RAWCSV/{prev_date_str}/{StateCode}_raw.csv")
#             state_raw_csv["delta21ConfirmedForState"]+=previous_state_raw_csv["cumulativeConfirmedNumberForState"]
#         state_raw_csv["delta21_14ConfirmedForState"]=state_raw_csv["delta21ConfirmedForState"]-state_raw_csv["delta14ConfirmedForState"]                
    
    lst = ["Recovered","Confirmed","Deceased","Tested","Vaccinated1","Vaccinated2"]
    for val in lst:
        for idx in state_raw_csv.index:
            # print(new_state_raw_csv["District"][idx])
            # print(new_state_raw_csv["7DmaVaccinatedForDistrict"][idx])
            avg_counter = 0
            value = 0
            for i in range(1,8):
                prev_date=datetime.strptime(Date,"%Y-%m-%d")+timedelta(days=(-1*i))
                prev_date_str=str(prev_date.year)+"-"+str(prev_date.month)+"-"+str(prev_date.day)
                previous_state_raw_csv=pd.read_csv(f"RAWCSV/{prev_date_str}/{StateCode}_raw.csv")
                value += previous_state_raw_csv.loc[previous_state_raw_csv["District"] == state_raw_csv["District"][idx],"cumulative{}NumberForDistrict".format(val)]
                avg_counter += 1
            state_raw_csv["7Dma{}ForDistrict".format(val)][idx] = value.item()/avg_counter

        state_raw_csv.to_csv(f"../RAWCSV/{Date}/{StateCode}_final.csv",index=False)
        return(state_raw_csv)

# keys=["AR","BR","CT","HP","MN","RJ"]
# keys = ["RJ"]
# for key in keys:
#     new_state_raw_csv=UpdateDerivedValues(key,"2021-10-27")




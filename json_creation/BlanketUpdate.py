#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import json
from functools import singledispatch
from tqdm import tqdm


# In[3]:


def CreateJson(date):
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

    data_min_json={}
    for k,v in STATE_NAMES.items():
        data_min_json[k]={"districts":{},"delta":{},"delta7":{},"delta21_14":{},"meta":{},"total":{}}

    def number_generation(df,col_name,col_value,field):
        value=df.loc[df[col_name]==col_value,field]
        value.reset_index(inplace=True,drop=True)
        if value.isna().all():
            value = "null"
        try:
            value = int(value[0])
        except:
            # raise
            value = value[0]
        return value

    for k,v in data_min_json.items():
        # print(k)
        df = pd.read_csv("../RAWCSV/"+date+"/"+k+"_final.csv")
        df_tt = pd.read_csv("../RAWCSV/"+date+"/TT_final.csv")
        # df = pd.read_csv('datamin.csv',header=[1])
        for district in df["District"]:
            try:
                district_dict={district:{"delta":{"confirmed":number_generation(df,"District",district,"deltaConfirmedForDistrict"),
                                                  "recovered":number_generation(df,"District",district,"deltaRecoveredForDistrict"),
                                                  "deceased":number_generation(df,"District",district,"deltaDeceasedForDistrict"),
                                                  "vaccinated1":number_generation(df,"District",district,"deltaVaccinated1ForDistrict"),
                                                  "vaccinated2":number_generation(df,"District",district,"deltaVaccinated2ForDistrict")
                                                 },
                                        # },#}
                # district_dict={district:{
                                         "delta7":{
                                        "confirmed": number_generation(df,"District",district,"7DmaConfirmedForDistrict"),
                                        "deceased": number_generation(df,"District",district,"7DmaDeceasedForDistrict"),
                                        "recovered": number_generation(df,"District",district,"7DmaRecoveredForDistrict"),
                                        "vaccinated1": number_generation(df,"District",district,"7DmaVaccinated1ForDistrict"),
                                        "vaccinated2": number_generation(df,"District",district,"7DmaVaccinated2ForDistrict")
                                       },
                #                }
                #               }
                               "meta":{"population": number_generation(df,"District",district,"districtPopulation"),
                                     "tested": {
                                      "last_updated": number_generation(df,"State/UTCode",k,'last_updated'),
                                      "source": number_generation(df,"State/UTCode",k,'tested_source_state'),
                                     },
                                     # "notes": number_generation(df,"State/UTCode",k,'notesForDistrict')
                               },
                                "total":{
                                   "confirmed": number_generation(df,"District",district,'cumulativeConfirmedNumberForDistrict'),
                                     "deceased": number_generation(df,"District",district,'cumulativeDeceasedNumberForDistrict'),
                                     "recovered": number_generation(df,"District",district,'cumulativeRecoveredNumberForDistrict'),
                                     # "tested": number_generation(df,"State/UTCode",k,'cumulativeTestedNumberForDistrict'),
                                     "vaccinated1": number_generation(df,"District",district,'cumulativeVaccinated1NumberForDistrict'),
                                    "vaccinated2": number_generation(df,"District",district,'cumulativeVaccinated2NumberForDistrict')
                               }}
                              }


            except KeyError as e:
                print(district,e)
                pass
            else:
                data_min_json[k]["districts"].update(district_dict)


        # print("State:"+str(number_generation(df,"State/UTCode",k,'cumulativeConfirmedNumberForState')))
        # print("TT   :"+str(number_generation(df_tt,"District",STATE_NAMES[k],'cumulativeConfirmedNumberForDistrict')))
        # if k != "TT":
        #     if number_generation(df,"State/UTCode",k,'cumulativeConfirmedNumberForState') != number_generation(df_tt,"District",STATE_NAMES[k],'cumulativeConfirmedNumberForDistrict'):
        #         updateJSONLog(STATE_NAMES[k],number_generation(df_tt,"District",STATE_NAMES[k],'cumulativeConfirmedNumberForDistrict'),number_generation(df,"State/UTCode",k,'cumulativeConfirmedNumberForState'))

        if k != "TT":
            data_min_json[k]["delta"]["confirmed"]=number_generation(df_tt,"District",STATE_NAMES[k],'deltaConfirmedForDistrict')
            data_min_json[k]["delta"]["deceased"]=number_generation(df_tt,"District",STATE_NAMES[k],'deltaDeceasedForDistrict')
            data_min_json[k]["delta"]["recovered"]=number_generation(df_tt,"District",STATE_NAMES[k],'deltaRecoveredForDistrict')
        else:
            data_min_json[k]["delta"]["confirmed"]=number_generation(df,"State/UTCode",k,'deltaConfirmedForState')
            data_min_json[k]["delta"]["deceased"]=number_generation(df,"State/UTCode",k,'deltaDeceasedForState')
            data_min_json[k]["delta"]["recovered"]=number_generation(df,"State/UTCode",k,'deltaRecoveredForState')

        data_min_json[k]["delta"]["vaccinated1"]=number_generation(df,"State/UTCode",k,'deltaVaccinated1ForState')
        data_min_json[k]["delta"]["vaccinated2"]=number_generation(df,"State/UTCode",k,'deltaVaccinated2ForState')
        data_min_json[k]["delta"]["tested"]=number_generation(df,"State/UTCode",k,'deltaTestedForState')
        # if k != "TT":
        #     data_min_json[k]["delta"]["tested"]=number_generation(df,"State/UTCode",k,'deltaTestedForState')
        # else:
        #     data_min_json[k]["delta"]["tested"]=0

        data_min_json[k]["delta7"]["confirmed"]=number_generation(df,"State/UTCode",k,'7DmaConfirmedForState')
        data_min_json[k]["delta7"]["deceased"]=number_generation(df,"State/UTCode",k,'7DmaDeceasedForState')
        data_min_json[k]["delta7"]["recovered"]=number_generation(df,"State/UTCode",k,'7DmaRecoveredForState')
        data_min_json[k]["delta7"]["vaccinated1"]=number_generation(df,"State/UTCode",k,'7DmaVaccinated1ForState')
        data_min_json[k]["delta7"]["vaccinated2"]=number_generation(df,"State/UTCode",k,'7DmaVaccinated2ForState')
        data_min_json[k]["delta7"]["tested"]=number_generation(df,"State/UTCode",k,'7DmaTestedForState')
        data_min_json[k]["delta21_14"]={"confirmed":number_generation(df,"State/UTCode",k,'delta21_14confirmedForState')}

        data_min_json[k]["meta"]={"date":number_generation(df,"State/UTCode",k,'Date'),
                                 "last_updated":number_generation(df,"State/UTCode",k,'last_updated'),
                                  "notes":number_generation(df,"State/UTCode",k,'notesForState'),
                                  "population":number_generation(df,"State/UTCode",k,'statePopulation'),
                                  "tested":{"date":number_generation(df,"State/UTCode",k,'last_updated'),
                                            "source":number_generation(df,"State/UTCode",k,'tested_source_state')
                                  }
                                 }
        if k != "TT":
            data_min_json[k]["total"]["confirmed"] = number_generation(df_tt,"District",STATE_NAMES[k],'cumulativeConfirmedNumberForDistrict')
            data_min_json[k]["total"]["deceased"] = number_generation(df_tt,"District",STATE_NAMES[k],'cumulativeDeceasedNumberForDistrict')
            data_min_json[k]["total"]["recovered"] = number_generation(df_tt,"District",STATE_NAMES[k],'cumulativeRecoveredNumberForDistrict')
        else:
            data_min_json[k]["total"]["confirmed"] = number_generation(df,"State/UTCode",k,'cumulativeConfirmedNumberForState')
            data_min_json[k]["total"]["deceased"] = number_generation(df,"State/UTCode",k,'cumulativeDeceasedNumberForState')
            data_min_json[k]["total"]["recovered"] = number_generation(df,"State/UTCode",k,'cumulativeRecoveredNumberForState')


        data_min_json[k]["total"]["tested"] = number_generation(df,"State/UTCode",k,'cumulativeTestedNumberForState')
        data_min_json[k]["total"]["vaccinated1"] = number_generation(df,"State/UTCode",k,'cumulativeVaccinated1NumberForState')
        data_min_json[k]["total"]["vaccinated2"] = number_generation(df,"State/UTCode",k,'cumulativeVaccinated2NumberForState')

    @singledispatch
    def remove_null_bool(ob):
        return ob

    @remove_null_bool.register(list)
    def _process_list(ob):
        return [remove_null_bool(v) for v in ob]

    @remove_null_bool.register(dict)
    def _process_list(ob):
        return {k: remove_null_bool(v) for k, v in ob.items()
                if v is not None and v is not 0 and v is not 'n' and v is not {}}

    with open('Updated/data-'+date+'.min.json', 'w') as json_file:
        json.dump(remove_null_bool(data_min_json), json_file)
    # print("Completed:"+date)


# In[4]:


import pandas as pd
import json
import os
import requests


# fileName = "../out_timeSeries/data.min.json"

#ASHA ... To run previous dates, use data.swi.min.json, so that the data.min.json is not disturbed..
#fileName = "../out_timeSeries/data-2021-11-17.min.json"
#ASHA ... To run previous dates, use data.swi.min.json OR the resp date JSON, so that the data.min.json is not disturbed..

def ts_json(fileName):
    # print (fileName)
    with open(fileName) as f:
        data_min = json.load(f)
        f.close()

    with open('Updated/timeseries.min.json') as fp:
            timeseries_min = json.load(fp)
            fp.close()

    for key in data_min.keys():
        # print(key)
        temp_dict = {}
        temp  = data_min[key]
        delta_keys = ['delta','delta7','total']
        for i in delta_keys:
            if i in temp.keys():
                temp_dict[i] = temp[i]

        run_date = data_min[key]['meta']['date']
        timeseries_min[key]['dates'][run_date] = temp_dict
        # print(type(run_date),run_date)

        with open('Updated/timeseries.min.json', 'w') as fp:
            json.dump(timeseries_min, fp)

            
def ts_state_all(fileName):
    delta_keys = ['delta','delta7','total']
    single_dist = {"DL":"Delhi","CH":"Chandigarh","LD":"Lakshadweep"}
    with open(fileName) as f:
        data_min = json.load(f)
        f.close()

    temp_dict = {}
    for key in data_min.keys():
        # print(key)
        temp_dict = {}
        temp  = data_min[key]
        for i in delta_keys:
            if i in temp.keys():
                temp_dict[i] = temp[i]
        
        
        with open("Updated/timeseries-{}.min.json".format(key)) as fp:
                timeseries_min = json.load(fp)
                fp.close()    
                
        run_date = data_min[key]['meta']['date']
        timeseries_min[key]["dates"][run_date] = temp_dict
        
                
        temp_dict = {}
        if key != "TT" and key not in single_dist:
            if 'districts' in data_min[key].keys():
                temp = data_min[key]['districts']
                for dist in temp:
                    if dist in timeseries_min[key]['districts']:
                        for i in delta_keys:
                            if i in temp[dist].keys():
                                temp_dict[i] = temp[dist][i]

                        run_date = data_min[key]['meta']['date']
                        if key != "TT":
                            timeseries_min[key]['districts'][dist]["dates"][run_date] = temp_dict
                            temp_dict = {}
        elif key != "TT" and key in single_dist: 
            timeseries_min[key]['districts'][single_dist[key]]["dates"][run_date] = {}
            for i in delta_keys:
                # print(key,"districts",single_dist[key],"dates",run_date,i)
                timeseries_min[key]['districts'][single_dist[key]]["dates"][run_date][i] = data_min[key][i]
                # print(data_min[key][i])

        with open("Updated/timeseries-{}.min.json".format(key), 'w') as fp:
            json.dump(timeseries_min, fp)


# In[20]:


from datetime import datetime,timedelta
def date_range(start, end):
    r = (end+timedelta(days=1)-start).days
    return [start+timedelta(days=i) for i in range(r)]
 

start_date = "2021-10-31"
end_date = "2022-01-01"
end = datetime.strptime(end_date, '%Y-%m-%d')
start = datetime.strptime(start_date, '%Y-%m-%d')
dateList = date_range(start, end)

# In[22]:

for date in tqdm(dateList):
    CreateJson(str(date.date()))
    ts_json("Updated/data-"+str(date.date())+".min.json")
    ts_state_all("Updated/data-"+str(date.date())+".min.json")


# 

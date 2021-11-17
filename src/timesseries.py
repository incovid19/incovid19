import pandas as pd
import json
import os
import requests


#fileName = "../out_timeSeries/data.min.json"

#ASHA ... To run previous dates, use data.swi.min.json, so that the data.min.json is not disturbed..
fileName = "../out_timeSeries/data.min_swi.json"
#ASHA ... To run previous dates, use data.swi.min.json, so that the data.min.json is not disturbed..

def ts_json():
    print (fileName)
    with open(fileName) as f:
        data_min = json.load(f)
        f.close()

    with open('../out_timeSeries/timeseries.min.json') as fp:
            timeseries_min = json.load(fp)
            fp.close()

    for key in data_min.keys():
        print(key)
        temp_dict = {}
        temp  = data_min[key]
        delta_keys = ['delta','delta7','total']
        for i in delta_keys:
            if i in temp.keys():
                temp_dict[i] = temp[i]

        run_date = data_min[key]['meta']['date']
        timeseries_min[key]['dates'][run_date] = temp_dict
        print(type(run_date),run_date)

        with open('../out_timeSeries/timeseries.min.json', 'w') as fp:
            json.dump(timeseries_min, fp)

            
def ts_state_all():
    delta_keys = ['delta','delta7','total']
    single_dist = {"DL":"Delhi","CH":"Chandigarh","LD":"Lakshadweep"}
    with open(fileName) as f:
        data_min = json.load(f)
        f.close()

    temp_dict = {}
    for key in data_min.keys():
        print(key)
        temp_dict = {}
        temp  = data_min[key]
        for i in delta_keys:
            if i in temp.keys():
                temp_dict[i] = temp[i]
        
        
        with open("../out_timeSeries/timeseries-{}.min.json".format(key)) as fp:
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

        with open(r"../out_timeSeries/timeseries-{}.min.json".format(key), 'w') as fp:
            json.dump(timeseries_min, fp)




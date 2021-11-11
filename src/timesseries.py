import pandas as pd
import json
import os
import requests


fileName = "../out_timeSeries/data.min.json"

#ASHA ... To run previous dates, use data.swi.min.json, so that the data.min.json is not disturbed..
#fileName = "../out_timeSeries/data.min_swi.json"
#ASHA ... To run previous dates, use data.swi.min.json, so that the data.min.json is not disturbed..

def ts_json():
    print (fileName)
    with open(fileName) as f:
        data_min = json.load(f)
        f.close()
    # dat_min_1  = json.load(f.read())
    # TS_MIN_dict = {}


    # url = 'https://data.incovid19.org/v4/min/timeseries.min.json'
    # response = requests.get(url)
    # if response.status_code == 200:
    #     with open(r"..//timeseries_min.json", 'wb') as f:
    #         f.write(response.content)
    
    # with open('../out_timeSeries/timeseries.min.json') as fp:
    #         timeseries_min = json.load(fp)
    #         fp.close()

    with open('../out_timeSeries/timeseries.min.json') as fp:
            timeseries_min = json.load(fp)
            fp.close()

    for key in data_min.keys():
        print(key)
        # TS_MIN_dict[key] = {}
        temp_dict = {}
        temp  = data_min[key]
        delta_keys = ['delta','delta7','total']
        for i in delta_keys:
            if i in temp.keys():
                temp_dict[i] = temp[i]
        # temp_dict = {"delta":temp['delta'],"delta7":temp['delta7'],'total':temp['total']}
        # print(temp_dict)

        run_date = data_min[key]['meta']['date']
        timeseries_min[key]['dates'][run_date] = temp_dict
        print(type(run_date),run_date)
        # print(timeseries_min[key]["dates"])
        # timeseries_min[key]["dates"][run_date]

        with open('../out_timeSeries/timeseries.min.json', 'w') as fp:
            json.dump(timeseries_min, fp)

        # TS_MIN_state_dict = {"dates":{data_min[key]['meta']['tested']['date']:temp_dict}}
        # print(TS_MIN_state_dict)
    # print(data_min)
def ts_state_all():
    delta_keys = ['delta','delta7','total']
    with open(fileName) as f:
        data_min = json.load(f)
        f.close()

    temp_dict = {}
    for key in data_min.keys():
        print(key)
        # url = 'https://data.incovid19.org/v4/min/timeseries-{}.min.json'.format(key)
        # response = requests.get(url)
        # if response.status_code == 200:
        #     with open(r"timeseries_{}_min.json".format(key), 'wb') as f:
        #         f.write(response.content)
        
        
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
        if key != "TT":
            if 'districts' in data_min[key].keys():
                temp = data_min[key]['districts']



                # print("="*50)
                # print(temp)
                for dist in temp:

                    if dist in timeseries_min[key]['districts']:
                        for i in delta_keys:
                            # print(temp.keys())
                    # temp = data_min[key]['districts']
                            if i in temp[dist].keys():
                                temp_dict[i] = temp[dist][i]
                        # print("="*50)
                        # print(dist)
                        # print("="*50)
                        # print(temp_dict)
                        # print("="*50)


                        run_date = data_min[key]['meta']['date']
                        if key != "TT":
                            timeseries_min[key]['districts'][dist]["dates"][run_date] = temp_dict
                            temp_dict = {}
                        # print(timeseries_min[key]['districts'][dist]["dates"][run_date])
            # a=b

        with open(r"../out_timeSeries/timeseries-{}.min.json".format(key), 'w') as fp:
            json.dump(timeseries_min, fp)




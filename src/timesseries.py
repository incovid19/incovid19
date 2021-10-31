import pandas as pd
import json
import os
import requests


def ts_json():
    with open('data_min.json') as f:
        data_min = json.load(f)
        f.close()
    # dat_min_1  = json.load(f.read())
    # TS_MIN_dict = {}


    url = 'https://data.incovid19.org/v4/min/timeseries.min.json'
    response = requests.get(url)
    if response.status_code == 200:
        with open(r"timeseries_min.json", 'wb') as f:
            f.write(response.content)

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
        with open('timeseries_min.json') as fp:
            timeseries_min = json.load(fp)
            fp.close()

        run_date = data_min[key]['meta']['date']
        timeseries_min[key]["dates"][run_date] = temp_dict
        # timeseries_min[key]["dates"][run_date]

        with open('updated_timeseries_min.json', 'w') as fp:
            json.dump(timeseries_min, fp)

        # TS_MIN_state_dict = {"dates":{data_min[key]['meta']['tested']['date']:temp_dict}}
        # print(TS_MIN_state_dict)
    # print(data_min)
def ts_state_all():
    delta_keys = ['delta','delta7','total']
    with open('data_min.json') as f:
        data_min = json.load(f)
        f.close()

    temp_dict = {}
    for key in data_min.keys():
        print(key)
        url = 'https://data.incovid19.org/v4/min/timeseries-{}.min.json'.format(key)
        response = requests.get(url)
        if response.status_code == 200:
            with open(r"timeseries_{}_min.json".format(key), 'wb') as f:
                f.write(response.content)
        
        with open("timeseries_{}_min.json".format(key)) as fp:
                timeseries_min = json.load(fp)
                fp.close()    

        
        if 'districts' in data_min[key].keys():
            temp = data_min[key]['districts']
            


            # print("="*50)
            # print(temp)
            for dist in temp:
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
                timeseries_min[key]['districts'][dist]["dates"][run_date] = temp_dict
                temp_dict = {}
                # print(timeseries_min[key]['districts'][dist]["dates"][run_date])
        # a=b

        with open(r"updated_timeseries_{}_min.json".format(key), 'w') as fp:
            json.dump(timeseries_min, fp)




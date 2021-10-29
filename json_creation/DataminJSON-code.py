
import pandas as pd
import numpy as np

path="./RAWCSV/2021-10-25"

STATE_NAMES = {
#   'AP': 'Andhra Pradesh',
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
#   'DN': 'Dadra and Nagar Haveli and Daman and Diu',
  'DL': 'Delhi',
  'JK': 'Jammu and Kashmir',
  'LA': 'Ladakh',
  'LD': 'Lakshadweep',
  'PY': 'Puducherry',
#   'TT': 'India',
 # [UNASSIGNED_STATE_CODE]: 'Unassigned',
}

data_min_json={}
for k,v in STATE_NAMES.items():
    data_min_json[k]={"districts":{},"delta":{},"delta7":{},"delta21_14":{},"meta":{},"total":{}}

def number_generation(df,col_name,col_value,field):
    value=df.loc[df[col_name]==value,field]
    value.reset_index(inplace=True,drop=True)
    return value[0]

for k,v in data_min_json.items():
    df=pd.read_csv(os.path.join(path,k+"_final.csv"))
    for district in df["District"]:
        try:
            district_dict={district:{"delta":{"comfirmed":number_generation(df,"District",district,"deltaConfirmedForDistrict"),"recoverd":number_generation(df,"District",district,"deltaRecoveredForDistrict"),"deceased":number_generation(df,"District",district,"deltaDeceasedForDistrict"),"vaccinated":number_generation(df,"District",district,"deltaVaccinatedForDistrict")}}}
        except KeyError as e:
            print(district,e)
            pass
        else:
            data_min_json[k]["districts"].update(district_dict)
        
    data_min_json[k]["delta"]["confirmed"]=number_generation(df,"State/UTCode",k,'deltaConfirmedForState')
    data_min_json[k]["delta"]["deceased"]=number_generation(df,"State/UTCode",k,'deltaDeceasedForState')
    data_min_json[k]["delta"]["recovered"]=number_generation(df,"State/UTCode",k,'deltaRecoveredForState')
    data_min_json[k]["delta"]["vaccinated"]=number_generation(df,"State/UTCode",k,'deltaVaccinatedForState')
    data_min_json[k]["delta"]["tested"]=number_generation(df,"State/UTCode",k,'deltaTestedForState')
    
    data_min_json[k]["delta7"]["confirmed"]=number_generation(df,"State/UTCode",k,'7DmadeltaConfirmedForState')
    data_min_json[k]["delta7"]["deceased"]=number_generation(df,"State/UTCode",k,'7DmadeltaDeceasedForState')
    data_min_json[k]["delta7"]["recovered"]=number_generation(df,"State/UTCode",k,'7DmadeltaRecoveredForState')
    data_min_json[k]["delta7"]["vaccinated"]=number_generation(df,"State/UTCode",k,'7DmadeltaVaccinatedForState')
    data_min_json[k]["delta7"]["tested"]=number_generation(df,"State/UTCode",k,'7DmadeltaTestedForState')
    data_min_json[k]["delta21_14"]=number_generation(df,"State/UTCode",k,'delta14_21ConfirmedForState')
    
    break
# print(data_min_json)






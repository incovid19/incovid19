# import tabula
import pandas as pd
import numpy as np
import json

# !pip install tabula-py
import camelot
import os
import string
import pytz
from datetime import datetime, timezone, timedelta
from tzlocal import get_localzone
from StatusMsg import StatusMsg
from tqdm import tqdm
from urllib.error import HTTPError
import re
import tabula
from tabulate import tabulate
import io
from numpy.core._exceptions import UFuncTypeError
# from datetime import datetime,timedelta
#programe extracts the tabels from the PDF files.
# Need some Preprocessing to convert to RawCSV
#Have Done for KA and HR for reference
# a=b
#declare the path of your file
# file_path = r"../INPUT/2021-10-26/KA.pdf"
#Convert your file
# reads all the tables in the PDF
class FileFormatChanged(Exception):
    pass

# def getAPData(file_path,date,StateCode):
#     table = camelot.read_pdf(file_path,pages='1')
#     if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
#         os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
#     table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')

#     df_districts =  pd.read_csv('../INPUT/{}/{}/foo-page-1-table-1.csv'.format(date,StateCode))
#     df_districts.columns = df_districts.columns.str.replace("\n","")
#     col_dict = {"TotalPositives":"Confirmed","TotalRecovered":"Recovered","TotalDeceased":"Deceased"}
#     df_districts.rename(columns=col_dict,inplace=True)
#     # df_districts.drop(columns=['S.No','PositivesLast 24 Hrs','TotalActive Cases'],inplace=True)
#     df_districts = df_districts[df_districts['District']!="Total AP Cases"]
#     df_summary = df_districts
#     df_districts = df_districts[:-1]

#     df_json = pd.read_json("../DistrictMappingMaster.json")
#     dist_map = df_json['Andhra Pradesh'].to_dict()
#     df_districts['District'].replace(dist_map,inplace=True)
#     df_summary = df_summary.iloc[-1,:]


#     # print(df_districts)
#     # print(df_summary)
#     # a=b
#     return df_summary,df_districts

def combine_listItems(list):
    combined_items = ' '.join([str(item) for item in list])
    return combined_items

def getAPData(file_path, date, StateCode):
    
    try:
        # print(file_path)
        file = tabula.read_pdf(file_path,pages=1,stream = True)
        # print(file)
        table = tabulate(file)
        # print(table)
        df_districts = pd.read_fwf(io.StringIO(table))
        # remove junk on top and reset the index
        df_districts.drop(df_districts.head(4).index, inplace=True)
        df_districts = df_districts.reset_index()

        # remove bottom junk
        df_districts.drop(df_districts.tail(2).index, inplace=True)
        df_other_cols = df_districts
        # print(df_districts)
        
        # remove unnecessary columns
        cols = [0, 4, 6]
        df_districts.drop(df_districts.columns[cols], axis=1, inplace=True)

        # add column names
        df_districts.columns = ['S.No','District', 'cumulativeConfirmedNumberForDistrict', 'District_1', 'Cases_2']
        df_districts.drop('S.No', axis=1, inplace=True)

        new_df = df_districts
        # splitting the dataframe
        N = 2
        splitted_list_df = np.split(df_districts, np.arange(N, len(df_districts.columns), N), axis=1)
        part_A = splitted_list_df[0]
        part_B = splitted_list_df[1]
        # print(type(part_B))

        part_B_cols = {"District_1": "District", "Cases_2": "cumulativeConfirmedNumberForDistrict"}
        part_B.rename(columns=part_B_cols, inplace=True)
        # concatenate two splitted DF's
        df_districts = pd.concat([part_A, part_B], ignore_index=True, sort=False)
        # print(df_districts)
        # base_csv= '../RAWCSV/2022-04-05/myGov/AP_raw.csv'
        # base_csv= '../RAWCSV/2022-04-24/myGov/AP_raw.csv'
        base_csv= '../RAWCSV/2022-04-28/AP_raw.csv'
        df_base_csv = pd.read_csv(base_csv)
        # print(df_base_csv)
        # df_base_csv.drop(df_base_csv.index[[0,7]],inplace=True)
        # df_base_csv = df_base_csv.reset_index(drop=True)
        # distri = df_base_csv['District']
        # con = df_base_csv['cumulativeConfirmedNumberForDistrict']
        # print(con, distri)
        # base_csv_forState = '../RAWCSV/2022-04-06/myGov/AP_raw.csv'
        base_csv_forState = '../RAWCSV/2022-04-29/myGov/AP_raw.csv'
        df_base_csv_forState = pd.read_csv(base_csv_forState)
        # df_base_csv_forState.drop(df_base_csv_forState.index[[0,7]],inplace=True)
        # df_base_csv_forState = df_base_csv_forState.reset_index(drop=True)
        # distri = df_base_csv_forState['District']
        # con = df_base_csv_forState['cumulativeConfirmedNumberForDistrict']
        # print(con, distri)
        for index, row in df_districts.iterrows():
            # print(index, row)
            cases_col = row['cumulativeConfirmedNumberForDistrict'].split(' ')[1:]
            cases_col = list(filter(str.strip, cases_col))
            # print(cases_col, len(cases_col))

            district_col = row['District'].split(' ')[1:]
            district_col = list(filter(str.strip, district_col))
            # print(district_col,len(district_col))

            if len(district_col) == 1:
                s = ''
                new_district_col = s.join(district_col)
            else:
                new_district_col = combine_listItems(district_col)
            if len(cases_col) == 1:
                s = ''
                new_cases_col = s.join(cases_col)
            else:
                new_cases_col = combine_listItems(cases_col)

            df_districts.loc[index, "District"] = new_district_col
            # print(type(new_district_col))
            df_districts.loc[index, "cumulativeConfirmedNumberForDistrict"] = new_cases_col
        # dropping rows having Nan    
        df_districts.drop(df_districts.index[[13,14,15,16,30,33]],inplace=True)
        df_districts = df_districts.reset_index(drop=True)
        df_districts['cumulativeConfirmedNumberForDistrict'] =df_districts['cumulativeConfirmedNumberForDistrict'].astype(int)

        df_districts = df_districts[:-2]
        # print(df_districts)
        
        df_json = pd.read_json("../DistrictMappingMaster.json")
        dist_map = df_json['Andhra Pradesh'].to_dict()
        df_districts['District'].replace(dist_map,inplace=True)
        
        for index,row in df_districts.iterrows():
            filtered_base_df = df_base_csv[df_base_csv['District']==row['District']]
            # print(df_base_csv_forState)
          
            # filtered_base_forState_df= df_base_csv_forState[df_base_csv_forState['District']==row['District']]
            distr = df_districts['District']
            # print(distr)
            # print(filtered_base_forState_df)
            
            # if len(filtered_base_df) == 1 and len(filtered_base_forState_df) == 1:
            if len(filtered_base_df) == 1:
                # print('printing district names',filtered_district)
                cumulative_confirmed_forDistrict = filtered_base_df.iloc[0]['cumulativeConfirmedNumberForDistrict'].astype(int)
                # print('cumulative_confirmed_forDistrict',cumulative_confirmed_forDistrict)
                
                df_districts.loc[index, 'cumulativeConfirmedNumberForDistrict'] = cumulative_confirmed_forDistrict+int(row['cumulativeConfirmedNumberForDistrict']) 
                
                df_districts['cumulativeDeceasedNumberForDistrict'] = '0'
                df_districts['cumulativeRecoveredNumberForDistrict'] = '0'
                df_districts['cumulativeTestedNumberForDistrict'] = '0'
                df_districts['cumulativeConfirmedNumberForState'] = df_districts['cumulativeConfirmedNumberForDistrict'].sum()
                
                cumulativeDeceasedNumberForState = df_base_csv_forState.iloc[0]['cumulativeDeceasedNumberForState'].astype(int)
                # print('cumulativeDeceasedNumberForState',cumulativeDeceasedNumberForState)
                df_districts['cumulativeDeceasedNumberForState'] = cumulativeDeceasedNumberForState
                cumulativeRecoveredNumberForState = df_base_csv_forState.iloc[0]['cumulativeRecoveredNumberForState'].astype(int)
                df_districts['cumulativeRecoveredNumberForState'] = cumulativeRecoveredNumberForState

                # df_districts['cumulativeTestedNumberForState'] = '33462024'
        df_summary = df_districts
        # print('printing df districts.....')
        # print(df_districts)
        
        # df_summary['cumulativeTestedNumberForState'] = '33462024' 
        # df_summary['cumulativeTestedNumberForState'] = '33469666'
        df_addTest = pd.read_csv("../INPUT/AP_Tested.csv")
        # print(df_addTest)
        try:
            df_summary['cumulativeTestedNumberForState'] = df_addTest[df_addTest["Date"] == date]["Cumulative_Tested"].item()
            # print(df_summary['Tested'])
        except:
            print("Please Enter AP Tested values in ../Input/AP_Tested.csv")
            raise
        
        df_summary.to_csv("../RAWCSV/{}/{}_raw.csv".format(date, StateCode))
        return df_summary, df_districts
        
    except Exception as e:
        raise
        # print(e)


# def getRJData(file_path,date,StateCode):
#     table = camelot.read_pdf(file_path,pages='1,2')
#     if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
#         os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
#     table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
#     print(table)

#     df_districts_1 = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-1.csv'.format(date,StateCode),header=0)
#     # df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1-edit.csv'.format(date,StateCode))
#     df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))

#     frames = [df_districts_1,df_districts_2]
#     df_districts = pd.concat(frames,ignore_index=True)
#     print('df_districts',df_districts)
#     df_districts.columns = df_districts.columns.str.replace("\n","")
#     print('before change',df_districts.columns)
    
#     #Cumulative Sample
#     col_dict = {"Unnamed: 2":"Tested", "Cumulative Positive":"Confirmed", "Cumulative Recovered/Discharged":"Recovered","Cumulative Death":"Deceased","CumulativePositive":"Confirmed",
#                 "CumulativeDeath":"Deceased","CumulativeRecovered/ Discharged":"Recovered"}
#     df_districts.rename(columns=col_dict,inplace=True)
#     print(df_districts.columns)
#     # df_districts.drop(columns=['S.No','Today\'s Positive','Today\'sDeath','Today\'sRecovered/ Discharged', 'Active Case'],inplace=True)
#     df_districts.dropna(how="all",inplace=True)
#     # print(df_districts)
#     # a=b
#     # df_summary = df_districts
#     # df_districts = df_districts[:-1]
#     # df_districts = df_districts[:-4]
#     # print(df_districts)
#     # a=b
#     df_summary = df_districts
#     # print(df_districts)
#     df_districts = df_districts[:-1]
#     print(df_districts)

#     # df_districts.drop(labels=[0,1],axis=0,inplace=True)
#     # df = df[]
#     df_districts['District'] = df_districts['District'].str.capitalize()

#     df_json = pd.read_json("../DistrictMappingMaster.json")
#     dist_map = df_json['Rajasthan'].to_dict()
#     df_districts['District'].replace(dist_map,inplace=True)
    
#     df_summary = df_summary.iloc[-1,:] #testcode needs to be updated later
#     print('df_summary',df_summary)
#     # a=b
#     return df_summary,df_districts

def getRJData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,pages='1,2')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # print(table)

    df_districts_1 = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-1.csv'.format(date,StateCode),header=0)
    df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))
    # df_districts_3 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-2.csv'.format(date,StateCode))

    frames = [df_districts_1,df_districts_2]
    df_districts = pd.concat(frames,ignore_index=True)
    # print('df_districts',df_districts)
    df_districts.columns = df_districts.columns.str.replace("\n","")
    # print('before change',df_districts.columns)
    col_dict = {"District": "District", "Today's Samples":"Tested", "Today's Positive":"Confirmed","Today's Death":"Deceased","Today's  Recovered/Discharged":"Recovered"}
    df_districts.rename(columns=col_dict,inplace=True)
    # print(df_districts.columns)
    # print(df_districts)
    df_districts = df_districts[:-1]

    df_districts.drop(columns=['Active  case'],inplace=True)
    df_districts.dropna(how="all",inplace=True)
        # print(df_districts)

    prevdate = str((datetime.strptime(date,"%Y-%m-%d")- timedelta(days=1)).date())
    prev_df = pd.read_csv("../RAWCSV/"+prevdate+"/RJ_raw.csv")
   
    df_districts['District'] = df_districts['District'].str.title()
    index_of_otherstate= df_districts[df_districts['District'] == 'Other State/'].index[0]
    df_districts.at[index_of_otherstate, 'District'] = 'Other state/'
    
    updated_data_frame = df_districts
    for index, row in prev_df.iterrows():
        District_base_col = row['District']
        # print('District_base_col',District_base_col)

        # if District_base_col != "Other state/" :
            # print('District_base_col',District_base_col)    
        filtered_dataframe= df_districts[df_districts['District'] == District_base_col]
        print('filtered_dataframe',filtered_dataframe)

        if not filtered_dataframe.empty:
            # pdf data columns
            confirmed_col= filtered_dataframe['Confirmed'].iloc[0]
            Recovered_col =filtered_dataframe['Recovered'].iloc[0]
            Deaths_col = filtered_dataframe['Deceased'].iloc[0]
            Tested_col = filtered_dataframe['Tested'].iloc[0]
            # print(confirmed_col,Recovered_col,Deaths_col,Tested_col)

            # base data columns
            confirmed_base_col = row['cumulativeConfirmedNumberForDistrict']
            Recovered_base_col = row['cumulativeRecoveredNumberForDistrict']
            Deaths_base_col = row['cumulativeDeceasedNumberForDistrict']
            Tested_base_col = row['cumulativeTestedNumberForDistrict']

            # print('confirmed_base_col:',confirmed_base_col,Recovered_base_col,Deaths_base_col,Tested_base_col)

            # addition
            confirmed_col = confirmed_col + confirmed_base_col
            Recovered_col = Recovered_col + Recovered_base_col
            Deaths_col = Deaths_col + Deaths_base_col
            Tested_result_col = Tested_col + Tested_base_col
            print('confirmed_col',confirmed_col,Recovered_col,Deaths_col,Tested_result_col)


            # updating dataframe column values with additional values
            # updated_data_frame['Date'] = prevdate
            updated_data_frame.loc[index, 'Confirmed'] = confirmed_col
            updated_data_frame.loc[index, 'Recovered'] = Recovered_col
            updated_data_frame.loc[index, 'Deceased'] = Deaths_col
            updated_data_frame.loc[index, 'Tested'] = Tested_result_col

    confirmed_sum_value = updated_data_frame['Confirmed'].sum()
    print('confirmed_sum_value is:',confirmed_sum_value)
    recovered_sum_value = updated_data_frame['Recovered'].sum()
    print('recovered_sum_value is:',recovered_sum_value)
    deceased_sum_value = updated_data_frame['Deceased'].sum()
    print('deceased_sum_value is:',deceased_sum_value)
    tested_sum_value = updated_data_frame['Tested'].sum()
    print('tested_sum_value is:',tested_sum_value)
    print('updated data frame is', updated_data_frame)   
    
    df_districts = updated_data_frame
    df_summary = df_districts
    # df_districts = df_districts[:-1]
    
    # print('df_summary',df_summary)
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Rajasthan'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    
    # df_summary['cumulativeConfirmedNumberForState'] = confirmed_sum_value
    # df_summary['cumulativeRecoveredNumberForState'] = recovered_sum_value
    # df_summary['cumulativeDeceasedNumberForState'] = deceased_sum_value
    # df_summary['cumulativeTestedNumberForState'] = tested_sum_value
    # 
    
    df_summary = df_summary.iloc[-1,:]
    df_summary['Confirmed'] = confirmed_sum_value
    df_summary['Recovered'] = recovered_sum_value
    df_summary['Deceased'] = deceased_sum_value
    df_summary['Tested'] = tested_sum_value
    print('df_summary',df_summary)

    # df_summary.to_csv("../RAWCSV/{}/{}_raw1.csv".format(date, StateCode))

    # updated_data_frame.to_csv("../RAWCSV/{}/{}_raw.csv".format(date, StateCode))
        # return df_summary, df_districts
        
    return df_summary,df_districts


def getKAData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,pages='1,5')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')

    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-5-table-1.csv'.format(date,StateCode),skiprows=3)
    df_districts.columns = df_districts.columns.str.replace("\n","")
    df_districts['District Name'] = df_districts['District Name'].str.replace("\n","")
    df_districts['District Name'] = df_districts['District Name'].str.replace("#","")
    df_districts['District Name'] = df_districts['District Name'].str.replace("*","")
    df_districts['District Name'] = df_districts['District Name'].replace(r'\s+', ' ', regex=True)
    # df_districts = df_districts.replace("nan",np.nan)
    print(df_districts.columns)
    
    # a=b
    
    # df_summary = df_districts
    # df_districts.columns = df_districts.columns.str.replace("\n","")
    
    for idx in df_districts.index:
        print(df_districts["Sl. No"][idx])
        if df_districts["Sl. No"][idx] == "21  Mandya":
            df_districts["Sl. No"][idx] = 21
            df_districts["District Name"][idx] = "Mandya"
        elif df_districts["Sl. No"][idx] == "22  Mysuru":
            df_districts["Sl. No"][idx] = 22
            df_districts["District Name"][idx] = "Mysuru"
        

    if "Non-Covid" in df_districts.columns[-1]:
        col_dict = {"District Name":"District","Total Positives":"Confirmed","Total Discharges":"Recovered","Total Covid Deaths":"Deceased" , df_districts.columns[-1]:"Other"}
    else:
        col_dict = {"District Name":"District","Total Positives":"Confirmed","Total Discharges":"Recovered","Total Covid Deaths":"Deceased" , df_districts.columns[-2]:"Other"}
        
    
    df_districts.rename(columns=col_dict,inplace=True)
    # print(df_districts.columns)
    # df_districts.drop(columns=['Sl. No','Today’s Positives','Today’s Discharges','Total Active Cases','Today’s Reported Covid Deaths','Death due to  Non-Covid reasons#'],inplace=True)
    df_districts.dropna(how="all",inplace=True)
    # print(df_districts)
    # a=b
    # a=b
    for col in df_districts.columns:
        df_districts[col] = df_districts[col].astype(str).str.replace("*","")
    # df_districts.dropna(inplace=True)
    # print(df_districts)
    # a=b

    
    df_summary = df_districts[df_districts["Sl. No"] == "Total"].iloc[0]
    # df_summary = df_districts[df_districts["District"] == "Total"].iloc[0]
    # print(df_summary)
    # a=b
    df_districts = df_districts[pd.to_numeric(df_districts['Sl. No'], errors='coerce').notnull()]
    # print(df_districts)
    # a=b
    # df_districts = df_districts[:-1]
    # print(df_districts)
    # df = df[]
    df_districts['notesForDistrict'] = df_districts['Other'].astype(str) + " cases were recorded as Deaths due to Non Covid Reasons"
    df_summary['notesForState'] = df_summary['Other'] + " cases were recorded as Deaths due to Non Covid Reasons"
    df_addTest = pd.read_csv("../INPUT/KA_Tested.csv")
    try:
        df_summary['Tested'] = df_addTest[df_addTest["Date"] == date]["Cumulative_Tested"].item()
    except:
        print("Please Enter KA Tested values in ../Input/KA_Tested.csv")
        raise
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Karnataka'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)

    

    # df_summary.rename(columns={"District":"State/UT"},inplace=True)
    # df_summary = df_summary.iloc[-1,:] #testcode needs to be updated later
    
    # print(df_districts)
    # print(df_summary)
    # print(date)
    # a=b
    return df_summary,df_districts

def getTNData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,pages='2,7')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')

    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-7-table-1.csv'.format(date,StateCode))
    df_districts.columns = df_districts.columns.str.replace("\n","")

    df_tests = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode)) 
    df_tests['COVID-19 STATISTICS'] = df_tests['COVID-19 STATISTICS'].str.replace("\n","")
    df_tests['COVID-19 STATISTICS'] = df_tests['COVID-19 STATISTICS'].str.replace("*","")
    # print(df_tests)
    # print(df_tests[df_tests['COVID-19 STATISTICS'] == 'Total Number of samples tested by  RT-PCR today/ till date']['DETAILS'].values)
    # a=b
    
    col_dict = {"Total Positive Cases":"Confirmed","Discharged":"Recovered","Death":"Deceased"}
    df_districts.rename(columns=col_dict,inplace=True)
    df_districts.drop(columns=['Sl. No','Active Cases'],inplace=True)
    df_summary = df_districts
    # print(df_districts)
    # print(df_summary)
    # a=b
    df_districts = df_districts[:-4]
    

    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Tamil Nadu'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)


    df_summary = df_summary.iloc[-1,:] #testcode needs to be updated later
    df_summary = df_summary.dropna()
    df_summary["Tested"] = df_tests[df_tests['COVID-19 STATISTICS'] == 'Total Number of samples tested by  RT-PCR today/ till date']['DETAILS'].values[0]#df_tests.loc[4,"DETAILS"][:-1]
    # print(df_summary["Tested"])
    df_summary["Tested"] = df_summary["Tested"].replace("\n","").split()[-1].replace("@","")
    df_summary = df_summary.str.replace(',', '').astype(int)

    # df_districts["Tested"] = df_summary["Tested"]
    # print(df_summary)
    # a=b 
    return df_summary,df_districts

def getHRData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,pages='1,2')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')

    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))
    # incase HR extraction not correct rename the table name and use this
    # df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1_editTable.csv'.format(date,StateCode))
    
    print('HR districts data:',df_districts)
    df_districts.columns = df_districts.columns.str.replace("\n","")
    
    df_districts['Sr No'] = df_districts['Sr No'] + ' '
    df_districts['Name of District'] = df_districts[['Sr No','Name of District']].fillna(' ').sum(axis=1)
    df_districts['Name of District'] = df_districts['Name of District'].str.split(' ')
    for i in range(0,10):
        for idx in df_districts.index:
            try:
                df_districts['Name of District'][idx].remove('')
            except:
                pass
    df_districts['Name of District'] = df_districts["Name of District"].str[-1]
    df_districts['Cumulative     Recovered/ Discharged Cases'] = df_districts['Cumulative     Recovered/ Discharged Cases'] + '['
    df_districts['Cumulative     Recovered/ Discharged Cases'] = df_districts['Cumulative     Recovered/ Discharged Cases'].fillna('')
    df_districts['Recovery Rate (%)'] = df_districts['Recovery Rate (%)'].astype(str)
    df_districts['Cumulative     Recovered/ Discharged Cases'] = df_districts[['Cumulative     Recovered/ Discharged Cases','Recovery Rate (%)']].fillna(' ').sum(axis=1)
    df_districts["Cumulative     Recovered/ Discharged Cases"] = df_districts["Cumulative     Recovered/ Discharged Cases"].str.split('[').str[0]
    
    try:
        df_districts['No. of Deaths'] = '%' + df_districts['No. of Deaths']
    except UFuncTypeError:
        df_districts['No. of Deaths'] = '%' + df_districts['No. of Deaths'].astype(str)
    df_districts['No. of Deaths'] = df_districts[['Recovery Rate (%)','No. of Deaths']].fillna(' ').sum(axis=1)
    df_districts["No. of Deaths"] = df_districts["No. of Deaths"].str.split('%').str[-1]
    
    print('HR districts columns:',df_districts.columns)
    
    df_tests = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-1.csv'.format(date,StateCode),names = ["Details","Numbers"])  
    
    col_dict = {"Name of District":"District","Cumulative Positive Cases":"Confirmed","Cumulative     Recovered/ Discharged Cases":"Recovered","No. of Deaths":"Deceased"}
    df_districts.rename(columns=col_dict,inplace=True)
    # df_districts.drop(columns=['Sr No','Positive Cases Today','Recovery Rate (%)','No of Active Cases','COVID-19, Vaccination Status  (NHM, Haryana)'],inplace=True)
    # print(df_districts)
    # a=b
    df_districts = df_districts[2:]
    # print(df_districts.columns)
    # print(df_districts['Recovered'].str.contains('['))
    # if df_districts['Recovered'].str.contains('[').any():
    df_districts["Recovered"] = df_districts["Recovered"].astype(str).str.split("[").str[0]
    # if df_districts['Deceased'].str.contains('[').any():
    df_districts["Deceased"] = df_districts["Deceased"].astype(str).str.split("[").str[0]
    df_districts["Confirmed"] = df_districts["Confirmed"].astype(str).str.split("[").str[0]
    df_summary = df_districts
    df_districts = df_districts[:-1]
    
    print('HR districts data:',df_districts[["District","Confirmed","Recovered","Deceased"]])
    print(25*"*")
    
    # df_districts.drop(labels=[0,1],axis=0,inplace=True)
    # df = df[]

    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Haryana'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)

    df_summary = df_summary.iloc[-1,:] #testcode needs to be updated later
    # print(df_summary)
    prevdate = str((datetime.strptime(date,"%Y-%m-%d")- timedelta(days=1)).date())
    # print(prevdate ,type(prevdate))
    df_prevDay = pd.read_csv('../RAWCSV/{}/{}_raw.csv'.format(prevdate,StateCode))
    df_prevDay["cumulativeTestedNumberForState"] 
    print(int(df_tests.loc[3,"Numbers"]) , int(df_prevDay["cumulativeTestedNumberForState"][0]))
    df_summary["Tested"] = int(df_tests.loc[0,"Numbers"].replace(',','')) + int(df_prevDay["cumulativeTestedNumberForState"][0])
    # df_districts["Tested"] = df_summary["Tested"]
    print(df_districts)
    print(df_summary)
    # a=b
    return df_summary,df_districts

def getWBData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,pages='1,2')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')

    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))
    df_districts.columns = df_districts.iloc[0]
    df_districts = df_districts[1:]
    df_districts.columns = df_districts.columns.str.replace("\n","")

    df_tests = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-2.csv'.format(date,StateCode))
    
    print(df_tests)
    # a=b
    
    col_dict = {"Total Cases":"Confirmed","Total Discharged":"Recovered","Total Deaths":"Deceased"}
    df_districts.rename(columns=col_dict,inplace=True)
    # df_districts.drop(columns=['S. No','Total Active Cases','Last Reported Case'],inplace=True)
    df_districts["Confirmed"] = df_districts["Confirmed"].str.split("+").str[0]
    df_districts["Recovered"] = df_districts["Recovered"].str.split("+").str[0]
    df_districts["Deceased"] = df_districts["Deceased"].str.split("+").str[0]

    df_districts["Confirmed"] = df_districts["Confirmed"].str.replace(",","")
    df_districts["Recovered"] = df_districts["Recovered"].str.replace(",","")
    df_districts["Deceased"] = df_districts["Deceased"].str.replace(",","")
    
    df_summary = df_districts
    df_districts = df_districts[:-1]
    # df_districts.drop(labels=[0,1],axis=0,inplace=True)
    # df = df[]
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['West Bengal'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    df_summary = df_summary.iloc[-1,:] #testcode needs to be updated later
    df_summary["Tested"] = df_tests.loc[1,"Number"]
    # print(df_summary)
    df_summary["Tested"]  = int(df_summary["Tested"].replace(',', '')) #.astype(int)
    # df_districts["Tested"] = df_summary["Tested"]
    # print(df_summary)
    # a=b
    # return df_summary,df_districts


def getMHData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,'1,2,3')
    # table = camelot.read_pdf(file_path,'2,3')

    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    print(table)
    # table[5].to_excel('foo.xlsx')
    df_districts_1 = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-1.csv'.format(date,StateCode))
    df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))
    df_districts_3 = pd.read_csv('../INPUT/{}/{}/foo-page-3-table-1.csv'.format(date,StateCode))

    frames = [df_districts_1,df_districts_2,df_districts_3]
    # frames = [df_districts_2,df_districts_3]

    df_districts = pd.concat(frames,ignore_index=True)
    df_districts.columns = df_districts.columns.str.replace("\n","")
  
    col_dict = {"District/Municipal Corporation":"District","COVID-19 cases":"Confirmed","Recovered patients":"Recovered","Deaths":"Deceased","District/MunicipalCorporation":"District"}
    df_districts.rename(columns=col_dict,inplace=True)
    # df_districts.drop(columns=['Sr. No.','Deaths due to other causes',  'Active cases'],inplace=True)
    
    df_summary = df_districts
    df_districts = df_districts[:-1]
    print(df_districts)
    # df_districts.drop(labels=[0,1],axis=0,inplace=True)
    # df = df[]
    df_addTest = pd.read_csv("../INPUT/MH_Tested.csv")
    # print(df_addTest)
    try:
        df_summary['Tested'] = df_addTest[df_addTest["Date"] == date]["Cumulative_Tested"].item()
        # print(df_summary['Tested'])
    except:
        print("Please Enter MH Tested values in ../Input/MH_Tested.csv")
        raise
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Maharashtra'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    df_summary = df_summary.iloc[-1,:] #testcode needs to be updated later
    return df_summary,df_districts


def getMLData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,pages='1')
    # print(file_path,date,StateCode)
    # print(table)
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-1.csv'.format(date,StateCode))#,header=0)
    # df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-1-edit.csv'.format(date,StateCode))#,header=0)
    # index_of_Rhio= df_districts[df_districts['Districts'] == 'RI-BHOI'].index[0]
    # print('index_of_Rhio',index_of_Rhio)
    # df_districts.at[index_of_Rhio, 'Districts'] = 'Ri-Bhoi'

    print(df_districts)
    df_districts.columns = df_districts.columns.str.replace("\n","")
    # print(df_districts.columns)
    prevdate = str((datetime.strptime(date,"%Y-%m-%d")- timedelta(days=1)).date())
    prev_df = pd.read_csv("../RAWCSV/"+prevdate+"/ML_final.csv")
    print(df_districts.columns)
    print(prev_df.columns)
    df_districts["Total Recoveries"] = 0
    for idx in df_districts.index:
        if df_districts["District Name"][idx] != "Total":
            df_districts["Total Recoveries"][idx] = prev_df[prev_df["District"] == df_districts["District Name"][idx]]["cumulativeRecoveredNumberForDistrict"].item() + df_districts["New Recoveries"][idx].item()
            print(df_districts["Total Recoveries"][idx])
        else:
            print(df_districts["Total Recoveries"].sum())
            df_districts["Total Recoveries"][idx] = df_districts["Total Recoveries"].sum()  
    
    col_dict = {"District Name":"District","Total Cases":"Confirmed","Total Recoveries":"Recovered","Total Deaths":"Deceased"}
    df_districts.rename(columns=col_dict,inplace=True)
    df_summary = df_districts
    df_districts = df_districts[:-1]

    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Meghalaya'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    
    df_summary = df_summary.iloc[-1,:]
    print(df_districts)
    return df_summary,df_districts

# def getPBData(file_path,date,StateCode):
#     table = camelot.read_pdf(file_path,'1,4')
#     if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
#         os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
#     table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
#     # table[5].to_excel('foo.xlsx')
#     df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-4-table-1.csv'.format(date,StateCode))
#     df_tests = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-1.csv'.format(date,StateCode),names=["Details","Numbers"])
    
#     df_districts.columns = df_districts.columns.str.replace("\n","")
    
#     col_dict = {"Total ConfirmedCases":"Confirmed","Total Cured":"Recovered","Deaths":"Deceased","Total Confirmed Cases":"Confirmed"}
#     df_districts.rename(columns=col_dict,inplace=True)
#     # print(df_districts)
#     # a=b
#     # df_districts.drop(columns=['S. No.','Total ActiveCases'],inplace=True)
#     df_summary = df_districts
#     df_districts = df_districts[:-1]
#     # df_districts.drop(labels=[0,1],axis=0,inplace=True)
#     # df = df[]
#     df_json = pd.read_json("../DistrictMappingMaster.json")
#     dist_map = df_json['Punjab'].to_dict()
#     df_districts['District'].replace(dist_map,inplace=True)
#     df_summary = df_summary.iloc[-1,:] #testcode needs to be updated later
#     df_tests["Confirmed"] = df_districts["Confirmed"].astype(str).str.split("*").str[0].astype(int)
#     if type(df_tests.loc[1,"Numbers"]) == str:
#         df_summary["Tested"] = df_tests.loc[1,"Numbers"].split('*')[1]
#     else:
#         df_summary["Tested"] = df_tests.loc[1,"Numbers"]
#     # df_districts["Tested"] = df_summary["Tested"]
#     # print(df_districts)
#     # a=b
#     return df_summary,df_districts



def getPBData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,'1,4')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')    
    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-4-table-1.csv'.format(date,StateCode))
    df_tests = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-1.csv'.format(date,StateCode),header=None)

    # removing the header part in df tests
    df_tests.drop(df_tests.head(1).index, inplace=True)
    # new coulmn is added in new PDF format removing that column.
    cols = [2]
    df_tests.drop(df_tests.columns[cols], axis=1, inplace=True)
    col_dict = {0:"S.No",1:"Description",3:"Numbers"}
    df_tests.rename(columns=col_dict,inplace=True)
    print(df_tests)
     
    df_districts.columns = df_districts.columns.str.replace("\n","")
    print(df_districts.columns)
    
    col_dict = {"District":"District",
    "Unnamed: 3":"Confirmed",
    "Unnamed: 5":"Recovered",
    "Unnamed: 7":"Deceased"}
    df_districts.rename(columns=col_dict,inplace=True)
    
    df_summary = df_districts
    df_districts = df_districts[:-1]
    
    df_districts = df_districts.dropna()

    # removing unwanted columns ,these got added in new PDF format.
    # df_districts.drop(columns=['confirmed cases from 1st April','Recovered from 1st April',
    # 'Deceased from 1st April',"Total Active Cases"],axis=0,inplace=True)
    # print(df_districts.columns)
    

    df_json = pd.read_json("../DistrictMappingMaster.json")
    
    dist_map = df_json['Punjab'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)

    # df_summary = df_summary[:-1]
    df_summary = df_summary.iloc[-1,:]

    df_tests["Confirmed"] = df_districts["Confirmed"].astype(str).str.split("*").str[0].astype(int)
    df_summary["Tested"] = df_tests.loc[1,"Numbers"]

    print(df_tests.loc[1,"Numbers"])
    df_summary["notesForState"] = "India reports 20,557 cases of COVID-19 infection, 2,603 more deaths as Punjab adds 2,563 old deaths to its tally, Published on : 20 Jul, 2022, 1:33 pm, Business Standard, NetIndian News Network"
    print(df_summary)
    return df_summary,df_districts

# def getUKData(file_path,date,StateCode):
#     table = camelot.read_pdf(file_path,'2')
#     if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
#         os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
#     table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
#     df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-2.csv'.format(date,StateCode))
#     df_districts.columns = df_districts.columns.str.replace("\n","")

#     df_tests = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode)) 
#     df_tests.columns = df_tests.columns.str.replace("\n","")  
    
#     col_dict = {"Districts":"District","Cases till Date":"Confirmed","Treated/ Cured till Date":"Recovered","Deaths":"Deceased","Migrated/ Others":"Other","Cumulative Samples Tested":"Tested"}
#     df_districts.rename(columns=col_dict,inplace=True)
#     df_tests.rename(columns=col_dict,inplace=True)
#     df_tests = df_tests[['District',"Tested"]]
#     df_districts["Confirmed"] = df_districts["Confirmed"].astype(str).str.split("*").str[0].astype(int)
#     df_districts["Recovered"] = df_districts["Recovered"].astype(str).str.split("*").str[0].astype(int)
    
#     # df_districts['Recovered'] += df_districts['Migrated']
#     # df_districts.drop(columns=['Active Cases','Migrated'],inplace=True)
#     for col in df_districts.columns:
#         df_districts[col] = df_districts[col].astype(str).str.replace("*","")
#     df_summary = df_districts
#     df_districts = df_districts[:-1]
#     df_json = pd.read_json("../DistrictMappingMaster.json")
#     dist_map = df_json['Uttarakhand'].to_dict()
#     df_districts['District'].replace(dist_map,inplace=True)
#     df_tests['District'].replace(dist_map,inplace=True)

#     df_total = pd.merge(df_districts, df_tests, on='District', how='inner')
#     # print(df_districts)
#     # print(df_tests)
#     print(df_total)
#     # a=b

#     df_summary = df_summary.iloc[-1,:] #testcode needs to be updated later
#     df_summary["Tested"] = int(df_tests.iloc[-1,-1])
    
#     df_total['notesForDistrict'] = df_total['Other'].astype(str) + " cases were recorded as Migrated / Others"
#     df_summary['notesForState'] = df_summary['Other'] + " cases were recorded as Migrated / Others"
    
#     return df_summary,df_total

def getUKData(file_path,date,StateCode):
    try:
        table = camelot.read_pdf(file_path,'2')
        # table = camelot.read_pdf(file_path,'3')

        if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
            os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
        table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
        df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-2.csv'.format(date,StateCode))
        # df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-3-table-3.csv'.format(date,StateCode))

        # change district name from U.S. nagar to Udham Singh Nagar
        index_of_USnagar= df_districts[df_districts['Districts'] == 'U.S. Nagar'].index[0]
        df_districts.at[index_of_USnagar, 'Districts'] = 'Udham Singh Nagar'

        df_districts.columns = df_districts.columns.str.replace("\n","")

        df_tests = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode)) 
        df_tests.columns = df_tests.columns.str.replace("\n","") 
    # except Exception as e:
    #     print(e)
    except FileNotFoundError:
        table = camelot.read_pdf(file_path,'3')
        # table = camelot.read_pdf(file_path,'4')

        if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
            os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
        table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
        df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-3-table-2.csv'.format(date,StateCode))

        # change district name from U.S. nagar to Udham Singh Nagar
        index_of_USnagar= df_districts[df_districts['Districts'] == 'U.S. Nagar'].index[0]
        df_districts.at[index_of_USnagar, 'Districts'] = 'Udham Singh Nagar'

        df_districts.columns = df_districts.columns.str.replace("\n","")

        df_tests = pd.read_csv('../INPUT/{}/{}/foo-page-3-table-1.csv'.format(date,StateCode)) 
        df_tests.columns = df_tests.columns.str.replace("\n","") 
    
    index_of_USnagar= df_tests[df_tests['Districts'] == 'US Nagar'].index[0]
    df_tests.at[index_of_USnagar, 'Districts'] = 'Udham Singh Nagar'
    print(df_districts.columns)
    # col_dict = {"Districts":"District","No. of Positive Cases Since 01.01.2022":"Confirmed",
    # "No. of Positive Cases Treated/ Cured Since 01.01.2022":"Recovered",
    # "Deaths Since 01.01.2022":"Deceased","Migrated Positive Cases Since 01.01.2022":"Other","Cumulative Samples Tested Since 01.01.2022":"Tested"}
    # col_dict = {"Districts":"District","Cases till Date":"Confirmed",
    # "Treated/ Cured till Date":"Recovered",
    # "Deaths":"Deceased","Migrated/ Others":"Other","Cumulative Samples Tested Since 01.01.2022":"Tested"}
    # "Cumulative Samples Tested":"Tested"
    col_dict = {"Districts":"District","No. of Positive Cases Since 01.01.2022":"Confirmed",
    "No. of Positive Cases Treated/ Cured Since 01.01.2022":"Recovered",
    "Deaths Since 01.01.2022":"Deceased","Migrated Positive Cases Since 01.01.2022":"Other","Cumulative Samples Tested Since 01.01.2022":"Tested"}
    df_districts.rename(columns=col_dict,inplace=True)
    df_tests.rename(columns=col_dict,inplace=True)
    print('after columns changed',df_districts.columns)
    
    df_districts["Confirmed"] = df_districts["Confirmed"].astype(str).str.split("*").str[0].astype(int)
    df_districts["Recovered"] = df_districts["Recovered"].astype(str).str.split("*").str[0].astype(int)
    df_districts["Deceased"] = df_districts["Deceased"].astype(str).str.split("*").str[0].astype(int)


    updated_data_frame = df_districts
    
    base_csv= '../RAWCSV/2021-12-31/UT_raw.csv'
    df_base_csv = pd.read_csv(base_csv)
    
    df_districts = pd.merge(df_districts, df_tests, on='District', how='inner')
    
    print('df districts data is', df_districts)

    for index, row in df_base_csv.iterrows():
        print(index, row)
        District_base_col = row['District']
        print('District_base_col',District_base_col)
        
        if District_base_col != "Total" :
            filtered_dataframe= df_districts[df_districts['District'] == District_base_col]
            print('filtered_dataframe',filtered_dataframe)
            
            if not filtered_dataframe.empty:
                # pdf data columns
                confirmed_col= filtered_dataframe['Confirmed'].iloc[0]
                Recovered_col =filtered_dataframe['Recovered'].iloc[0]
                Deaths_col = filtered_dataframe['Deceased'].iloc[0]
                Tested_col = filtered_dataframe['Tested'].iloc[0]
                Other_col = filtered_dataframe['Other'].iloc[0]

                # base data columns
                confirmed_base_col = row['cumulativeConfirmedNumberForDistrict']
                Recovered_base_col = row['cumulativeRecoveredNumberForDistrict']
                Deaths_base_col = row['cumulativeDeceasedNumberForDistrict']
                Tested_base_col = row['cumulativeTestedNumberForDistrict']
                other_base_col = row['notesForDistrict'].split("c")[0]

                # addition
                confirmed_col = confirmed_col + confirmed_base_col
                Recovered_col = Recovered_col + Recovered_base_col
                Deaths_col = Deaths_col + Deaths_base_col
                Tested_col = Tested_col + Tested_base_col
                Other_col = Other_col + int(other_base_col)

                # updating dataframe column values with additional values
                updated_data_frame.loc[index, 'Confirmed'] = confirmed_col
                updated_data_frame.loc[index, 'Recovered'] = Recovered_col
                updated_data_frame.loc[index, 'Deceased'] = Deaths_col
                updated_data_frame.loc[index, 'Tested'] = Tested_col
                updated_data_frame.loc[index, 'Other'] = Other_col

    
    # get the index of total row and set those row values to zero then update with sum values
    # finding index of total 
    index_of_total = updated_data_frame[updated_data_frame['District'] == 'Total'].index[0]
    print('index of total', index_of_total)

    # set the total row values to zero
    updated_data_frame.at[index_of_total, 'Confirmed'] = 0
    updated_data_frame.at[index_of_total, 'Recovered'] = 0
    updated_data_frame.at[index_of_total, 'Deceased'] = 0
    updated_data_frame.at[index_of_total, 'Tested'] = 0
    updated_data_frame.at[index_of_total, 'Other'] = 0
    
    # summing of all the Confirmed, Recovered, Deceased and Other Column values 
    Confirmed_Sumvalue = updated_data_frame['Confirmed'].sum()
    Recovered_Sumvalue = updated_data_frame['Recovered'].sum()
    Deceased_Sumvalue = updated_data_frame['Deceased'].sum()
    Tested_Sumvalue = updated_data_frame['Tested'].sum()
    Other_Sumvalue = updated_data_frame['Other'].sum()
    # print('updated data frame con sum is', Confirmed_Sumvalue, 'Recovered_Sumvalue',Recovered_Sumvalue,
    # 'Deceased_Sumvalue',Deceased_Sumvalue, 'Other_Sumvalue',Other_Sumvalue) 

    # updating total row with sum of all the (C, R, D, O) column values
    updated_data_frame.at[index_of_total, 'Confirmed'] = Confirmed_Sumvalue
    updated_data_frame.at[index_of_total, 'Recovered'] = Recovered_Sumvalue
    updated_data_frame.at[index_of_total, 'Deceased'] = Deceased_Sumvalue
    updated_data_frame.at[index_of_total, 'Tested'] = Tested_Sumvalue
    updated_data_frame.at[index_of_total, 'Other'] = Other_Sumvalue
            
    print('updated data frame is', updated_data_frame)   
 
    df_districts = updated_data_frame
    df_summary = df_districts
    df_districts = df_districts[:-1]
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Uttarakhand'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    # df_tests['District'].replace(dist_map,inplace=True)

    # df_total = pd.merge(df_districts, df_tests, on='District', how='inner')
    # print(df_districts)
    # print(df_tests)
    # print(df_total)
    # a=b

    df_summary = df_summary.iloc[-1,:] #testcode needs to be updated later
    # df_summary["Tested"] = int(df_tests.iloc[-1,-1])
    
    df_districts['notesForDistrict'] = df_districts['Other'].astype(str) + " cases were recorded as Migrated / Others"
    df_summary['notesForState'] = df_summary['Other'].astype(str) + " cases were recorded as Migrated / Others"
    print('df_districts',df_districts, 'df_summary',df_summary)
    return df_summary,df_districts


# def getNLData(file_path,date,StateCode):
#     table = camelot.read_pdf(file_path,'1')
#     if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
#         os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
#     table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
#     # table[5].to_excel('foo.xlsx')
#     df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-3.csv'.format(date,StateCode),skiprows=4,
#     names=['a','District','b','c','d','e','f','g','Recovered','Deceased','h','i','j','Confirmed'])
#     # df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))  
#     # df_districts.columns = df_districts.columns.str.replace("\n","")
       
#     df_districts.drop(columns=list(string.ascii_lowercase[:10]),inplace=True)
#     df_summary = df_districts
#     df_districts = df_districts[:-1] 
#     # df_districts.drop(labels=[0,1],axis=0,inplace=True)
#     # df = df[]
#     df_json = pd.read_json("../DistrictMappingMaster.json")
#     dist_map = df_json['Nagaland'].to_dict()
#     df_districts['District'].replace(dist_map,inplace=True)
#     df_summary = df_summary.iloc[-1,:] #testcode needs to be updated later
#     return df_summary,df_districts

def getNLData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,'1')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')
    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-3.csv'.format(date,StateCode),skiprows=4,
    names=['a','District','b','c','d','e','f','g','Recovered','Deceased','h','i','j','Confirmed'])
    # print(df_districts)
    # a=b
    df_tests = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-2.csv'.format(date,StateCode),skiprows=3,
    names=["RT PCR","Truenat","Rapid Antigen Test","Total"])
    df_tests.columns = df_tests.columns.str.replace("\n","")
    
    df_districts['Recovered'] = df_districts['Recovered']
    df_districts['Deceased'] = df_districts['Deceased']
    df_districts['Other'] = df_districts['h'] + df_districts['j']
    # df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))  
    # df_districts.columns = df_districts.columns.str.replace("\n","")
       
    # df_districts.drop(columns=list(string.ascii_lowercase[:10]),inplace=True)
    df_summary = df_districts
    df_districts = df_districts[:-1] 
    # df_districts.drop(labels=[0,1],axis=0,inplace=True)
    # df = df[]
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Nagaland'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    df_summary = df_summary.iloc[-1,:] #testcode needs to be updated later
    df_summary["Tested"] = df_tests.loc["Results Received","Total"].split("\n")[-1]
    df_districts['notesForDistrict'] = df_districts['Other'].astype(str) + " cases were recorded as Non Covid Deaths with Covid19 Positivity"
    df_summary['notesForState'] = df_summary['Other'].astype(str) + " cases were recorded as Non Covid Deaths with Covid19 Positivity"
    return df_summary,df_districts

def getLAData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,'1,2')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')
    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode),skiprows=5,
    names = ['a','District'] + list(string.ascii_lowercase[1:10]) + ['Confirmed','k','l','Recovered','Deceased'])
    # df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))  
    df_districts.columns = df_districts.columns.str.replace("\n","")

    df_tests = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-1.csv'.format(date,StateCode))
    
    
    # col_dict = {"b":"District"}
    # df_districts.rename(columns=col_dict,inplace=True)
    # df_districts.drop(columns=list(string.ascii_lowercase[:12]),inplace=True)
    df_summary = df_districts
    
    df_districts = df_districts[:-1]
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Ladakh'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    print(df_districts)
    df_summary = df_summary.iloc[-1,:] #testcode needs to be updated later
    df_summary["Tested"] = df_tests.iloc[-1,-1]
    # print(df_summary)
    # a=b
    return df_summary,df_districts


def getMZData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path)
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')
    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode),skiprows=5,
    names = ['a','District'] + list(string.ascii_lowercase[1:10]) + ['Confirmed','k','l','Recovered','Deceased'])
    # df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))  
    df_districts.columns = df_districts.columns.str.replace("\n","")
    df_districts = df_districts[:-1]
    # col_dict = {"b":"District"}
    # df_districts.rename(columns=col_dict,inplace=True)
    # df_districts.drop(columns=list(string.ascii_lowercase[:12]),inplace=True)
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Ladakh'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    df_summary = df_districts #testcode needs to be updated later
    return df_summary,df_districts

# def getUPData(file_path,date,StateCode):
#     print(file_path)
#     input_folder = '../INPUT/{}/{}/{}_data.csv'.format(date,StateCode,StateCode)
#     # print(input_folder)
#     df_districts = pd.read_csv(input_folder)
#     # print(df_districts)
#     df_districts['Confirmed'] = df_districts['Recovered']+df_districts['Deceased']+df_districts['Active']
#     print(df_districts['Confirmed'])
#     df_districts.drop('Active', inplace=True, axis=1)
#     df_summary = df_districts

#     df_json = pd.read_json("../DistrictMappingMaster.json")
#     dist_map = df_json['Uttar Pradesh'].to_dict()
#     df_districts['District'].replace(dist_map,inplace=True)
#     df_summary = df_summary.iloc[-1,:]
#     df_summary['Confirmed'] = df_districts['Confirmed'].sum()
#     df_summary['Recovered'] = df_districts['Recovered'].sum()
#     df_summary['Deceased'] = df_districts['Deceased'].sum()

#     print(df_districts)

#     return df_summary,df_districts

def hindi_to_english(state):
    hindi_dist = json.load(io.open("../DistrictMatchingHindi.json", encoding="utf8"))
    # print(hindi_dist)
    district_data = hindi_dist.get(state)
    return district_data 
    

def getUPData(file_path,date,StateCode):
    tables = tabula.read_pdf(file_path, pages = "all")
    # print(tables)
    folder_path_1 = '../INPUT/{}/{}/table_data_1.csv'.format(date,StateCode)
    folder_path_2 = '../INPUT/{}/{}/table_data_2.csv'.format(date,StateCode)

    print(len(tables))
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    # table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    tables[0].to_csv(folder_path_1)
    tables[1].to_csv(folder_path_2)
    
    df_districts_1 = pd.read_csv('../INPUT/{}/{}/foo_page_1_table_1.csv'.format(date,StateCode))
    df_districts_1.reset_index(drop=True, inplace=True)
#     print(df_districts_1)
    
    df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo_page_2_table_1.csv'.format(date,StateCode))
    df_districts_2.reset_index(drop=True, inplace=True)
#     print(df_districts_2)
    try:
        district_dict = hindi_to_english('Uttar Pradesh')
        # print(district_dict)
        df_districts = pd.concat([df_districts_1,df_districts_2], ignore_index = True, axis = 0)
        # print(df_districts)
        for index, row in df_districts.iterrows():
            hindi_district_name = row['District']
            english_district_name = district_dict.get(hindi_district_name)
            # print(hindi_district_name,english_district_name)
            df_districts['District'] =df_districts['District'].replace(hindi_district_name,english_district_name)
        df_districts['Confirmed'] = df_districts['Recovered']+df_districts['Deceased']+df_districts['Active']
        # print(df_districts['Confirmed'])
        df_districts.drop('Active', inplace=True, axis=1)
        df_summary = df_districts

        df_json = pd.read_json("../DistrictMappingMaster.json")
        dist_map = df_json['Uttar Pradesh'].to_dict()
        df_districts['District'].replace(dist_map,inplace=True)
        df_summary = df_summary.iloc[-1,:]
        df_summary['Confirmed'] = df_districts['Confirmed'].sum()
        df_summary['Recovered'] = df_districts['Recovered'].sum()
        df_summary['Deceased'] = df_districts['Deceased'].sum()

        print(df_districts)

        # df_districts.to_csv('../INPUT/{}/{}/example.csv'.format(date,StateCode))
       
    except Exception as e:
        print(e)
    return df_summary,df_districts


# def getKLData(file_path,date,StateCode):
#     # print("Extracting PDF")
#     table = camelot.read_pdf(file_path,'4,5,6')
#     # table = camelot.read_pdf(file_path,'4,5,7')


#     if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
#         os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
#     table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
#     # print('table', table)
#     try:
#         df_districts_1 = pd.read_csv('../INPUT/{}/{}/foo-page-4-table-1.csv'.format(date,StateCode))
#         df_deaths_data = pd.read_csv('../INPUT/{}/{}/foo-page-5-table-1.csv'.format(date,StateCode))
#         df_tests_data = pd.read_csv('../INPUT/{}/{}/foo-page-6-table-2.csv'.format(date,StateCode))
#         # df_tests_data = pd.read_csv('../INPUT/{}/{}/foo-page-7-table-1.csv'.format(date,StateCode))

#     except:
#         print("Format Chnaged")
#         raise FileFormatChanged

#     df_districts_1.columns = df_districts_1.columns.str.replace("\n","")
#     df_deaths_data.columns = df_deaths_data.columns.str.replace("\n","")
#     df_tests_data.columns = df_tests_data.columns.str.replace("\n","")

#     df_districts_1 = df_districts_1.iloc[:,[0, 1, 2]]    
#     df_deaths_data = df_deaths_data.iloc[:,[0, -1]]

#     df_districts = pd.merge(df_districts_1, df_deaths_data, on='District', how='inner')

#     # col_dict = {"District":"District","Positive Cases declared today":"Confirmed",
#     # "Declared Negative today":"Recovered", "Death Cases approved today (A+B+C)":"Deaths"} 

#     # for 02 Feb 2022, for deaths, this col dict
#     col_dict = {"District":"District","Positive Cases declared today":"Confirmed",
#     "Declared Negative today":"Recovered", "Death Cases approved today (A+B)":"Deceased"}   
#     df_districts.rename(columns=col_dict,inplace=True)

#     updated_data_frame = df_districts    
#     prevdate = str((datetime.strptime(date,"%Y-%m-%d")- timedelta(days=1)).date())
#     # print('prevdate',prevdate ,type(prevdate))
#     df_prevDay = pd.read_csv("../RAWCSV/{}/{}_raw.csv".format(prevdate,StateCode))
#     # df_prevDay = pd.read_csv('../RAWCSV/{}/{}_raw.csv'.format(prevdate,StateCode))

#     # print('base csv is', df_prevDay)

#     for index, row in df_prevDay.iterrows():
#         District_base_col = row['District']
#         # print('District_base_col',District_base_col)
    
#         if District_base_col != "Total" :
#             # print(District_base_col)
#             filtered_dataframe= df_districts[df_districts['District'] == District_base_col]
#             district_index = filtered_dataframe.index[0]
#             if not filtered_dataframe.empty:

#                 # pdf data columns
#                 Confirmed_col= filtered_dataframe['Confirmed'].iloc[0]
#                 Recovered_col =filtered_dataframe['Recovered'].iloc[0]
#                 Deaths_col = filtered_dataframe['Deceased'].iloc[0]
#                 # print(type(Confirmed_col))
#                 # print('Confirmed_col',Confirmed_col, 'Recovered_col',Recovered_col,'Deaths_col',Deaths_col)

#                 # base data columns
#                 Confirmed_base_col = row['cumulativeConfirmedNumberForDistrict']
#                 Recovered_base_col = row['cumulativeRecoveredNumberForDistrict']
#                 Deaths_base_col = row['cumulativeDeceasedNumberForDistrict']
#                 # print('Confirmed_base_col',Confirmed_base_col,'Recovered_base_col',Recovered_base_col,'Deaths_base_col',Deaths_base_col)

#                 # addition

#                 Confirmed_col =  Confirmed_col + Confirmed_base_col
#                 Recovered_col = Recovered_col + Recovered_base_col
#                 Deaths_col = Deaths_col + Deaths_base_col
#                 # print('Confirmed_col',Confirmed_col,
#                 # 'Recovered_col',Recovered_col,
#                 # 'Deaths_col',Deaths_col)

#                 # updating dataframe column values with addition values
#                 updated_data_frame.at[district_index, 'Confirmed'] = Confirmed_col
#                 updated_data_frame.at[district_index, 'Recovered'] = Recovered_col
#                 updated_data_frame.at[district_index, 'Deceased'] = Deaths_col
#     # print('updated_data_frame',updated_data_frame)

            
#     # get the index of total row and set those row values to zero then update with sum values
#     # finding index of total 
#     index_of_total = updated_data_frame[updated_data_frame['District'] == 'Total'].index[0]

#     # set the total row values to zero

#     updated_data_frame.at[index_of_total, 'Confirmed'] = 0
#     updated_data_frame.at[index_of_total, 'Recovered'] = 0
#     updated_data_frame.at[index_of_total, 'Deceased'] = 0

    
#     # summing of all the Confirmed, Recovered, Deceased and Other Column values 
#     Confirmed_Sumvalue = updated_data_frame['Confirmed'].sum()
#     Recovered_Sumvalue = updated_data_frame['Recovered'].sum()
#     Deceased_Sumvalue = updated_data_frame['Deceased'].sum()
    

#     # updating total row with sum of all the (C, R, D, O) column values
#     updated_data_frame.at[index_of_total, 'Confirmed'] = Confirmed_Sumvalue
#     updated_data_frame.at[index_of_total, 'Recovered'] = Recovered_Sumvalue
#     updated_data_frame.at[index_of_total, 'Deceased'] = Deceased_Sumvalue
    
#     # print('updated data frame is', updated_data_frame)

#     df_districts = updated_data_frame
#     df_summary = df_districts
#     df_districts = df_districts[:-1]
#     df_json = pd.read_json("../DistrictMappingMaster.json")
#     dist_map = df_json['Kerala'].to_dict()
#     df_districts['District'].replace(dist_map,inplace=True)


#     df_summary = df_summary.iloc[-1,:] #testcode needs to be updated later
#     # for tested result
#     test_data = df_tests_data['Cumulative Samples Sent'].astype(int)
#     # print('test_data',test_data, type(test_data))
#     df_summary["Tested"] = int(test_data)

#     # print('df_tests_data',df_tests_data)    
#     # print('df_summary',df_summary)
#     # print('df_districts',df_districts)

#     return df_summary,df_districts
#     # GenerateRawCsv(StateCode,date,df_districts,df_summary)

def getKLData(file_path,date,StateCode):
    kl_fileCode = pd.read_csv("../INPUT/KL/kl_districtCode.csv")
    prevdate = str((datetime.strptime(date,"%Y-%m-%d")- timedelta(days=1)).date())
    Date = datetime.strptime(date,"%Y-%m-%d")
    Date = Date.strftime("%d-%m-%Y")

    df_districts = pd.DataFrame(columns=['Date', 'District', 'Confirmed', 'Recovered', 'Active', 'Death'])
    for idx in kl_fileCode.index:
        DistrictData = pd.read_html('../INPUT/KL/kerala-'+ str(kl_fileCode["Code"][idx]) +'.html')
        DistrictData = DistrictData[1]
        DistrictData["District"] = kl_fileCode["District"][idx]
        df_districts = df_districts.append(DistrictData[DistrictData["Date"] == Date])
    print(df_districts)
    
    testingData = pd.read_html('../INPUT/KL/kerala-testing.html')
    testingData = testingData[1]
    testdone = testingData[testingData["Date"] == Date]["Tot. Sent"].item()

    df_districts = df_districts.rename(columns={'Death':'Deceased'})
    df_districts.loc[len(df_districts.index)] = [Date,'Total', 0, 0, 0, 0] 

    
    # print('prevdate',prevdate ,type(prevdate))
    updated_data_frame = df_districts
    df_prevDay = pd.read_csv("../RAWCSV/{}/{}_raw.csv".format(prevdate,StateCode))
    # df_prevDay = pd.read_csv('../RAWCSV/{}/{}_raw.csv'.format(prevdate,StateCode))

    # print('base csv is', df_prevDay)

    for index, row in df_prevDay.iterrows():
        District_base_col = row['District']
        # print('District_base_col',District_base_col)

        if District_base_col != "Total" :
            # print(District_base_col)
            filtered_dataframe= df_districts[df_districts['District'] == District_base_col]
            district_index = filtered_dataframe.index[0]
            if not filtered_dataframe.empty:

                # pdf data columns
                Confirmed_col= filtered_dataframe['Confirmed'].iloc[0]
                Recovered_col =filtered_dataframe['Recovered'].iloc[0]
                Deaths_col = filtered_dataframe['Deceased'].iloc[0]
                # print(type(Confirmed_col))
                # print('Confirmed_col',Confirmed_col, 'Recovered_col',Recovered_col,'Deaths_col',Deaths_col)

                # base data columns
                Confirmed_base_col = row['cumulativeConfirmedNumberForDistrict']
                Recovered_base_col = row['cumulativeRecoveredNumberForDistrict']
                Deaths_base_col = row['cumulativeDeceasedNumberForDistrict']
                # print('Confirmed_base_col',Confirmed_base_col,'Recovered_base_col',Recovered_base_col,'Deaths_base_col',Deaths_base_col)

                # addition

                Confirmed_col =  Confirmed_col + Confirmed_base_col
                Recovered_col = Recovered_col + Recovered_base_col
                Deaths_col = Deaths_col + Deaths_base_col
                # print('Confirmed_col',Confirmed_col,
                # 'Recovered_col',Recovered_col,
                # 'Deaths_col',Deaths_col)

                # updating dataframe column values with addition values
                updated_data_frame.at[district_index, 'Confirmed'] = Confirmed_col
                updated_data_frame.at[district_index, 'Recovered'] = Recovered_col
                updated_data_frame.at[district_index, 'Deceased'] = Deaths_col
    # print('updated_data_frame',updated_data_frame)


    # get the index of total row and set those row values to zero then update with sum values
    # finding index of total 
    index_of_total = updated_data_frame[updated_data_frame['District'] == 'Total'].index[0]

    # set the total row values to zero

    updated_data_frame.at[index_of_total, 'Confirmed'] = 0
    updated_data_frame.at[index_of_total, 'Recovered'] = 0
    updated_data_frame.at[index_of_total, 'Deceased'] = 0


    # summing of all the Confirmed, Recovered, Deceased and Other Column values 
    Confirmed_Sumvalue = updated_data_frame['Confirmed'].sum()
    Recovered_Sumvalue = updated_data_frame['Recovered'].sum()
    Deceased_Sumvalue = updated_data_frame['Deceased'].sum()


    # updating total row with sum of all the (C, R, D, O) column values
    updated_data_frame.at[index_of_total, 'Confirmed'] = Confirmed_Sumvalue
    updated_data_frame.at[index_of_total, 'Recovered'] = Recovered_Sumvalue
    updated_data_frame.at[index_of_total, 'Deceased'] = Deceased_Sumvalue

    # print('updated data frame is', updated_data_frame)

    df_districts = updated_data_frame
    df_summary = df_districts
    df_summary = df_summary.iloc[-1,:]
    df_summary["Tested"] = testdone
    df_districts = df_districts[:-1]
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Kerala'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    df_summary["Date"] = date
    df_districts["Date"] = date
    return df_summary,df_districts


def GenerateRawCsv(StateCode,Date,df_districts,df_summary):
    # print(df_summary['Confirmed'].values)
    utc_dt = datetime.now(timezone.utc)
    df = pd.DataFrame(columns=["Date","State/UTCode","District","tested_last_updated_district","tested_source_district","notesForDistrict",
    "cumulativeConfirmedNumberForDistrict","cumulativeDeceasedNumberForDistrict","cumulativeRecoveredNumberForDistrict",
    "cumulativeTestedNumberForDistrict","last_updated","tested_last_updated_state","tested_source_state","notesForState",
    "cumulativeConfirmedNumberForState","cumulativeDeceasedNumberForState","cumulativeRecoveredNumberForState","cumulativeTestedNumberForState"])

    df['District'] = df_districts['District']
    print('DISTRICT',df['District'])
    if "Confirmed" in df_districts.columns:
        df['cumulativeConfirmedNumberForDistrict'] = df_districts['Confirmed']
        df['cumulativeConfirmedNumberForState'] = df_summary['Confirmed']#.astype(int).sum()
        # print(df['cumulativeConfirmedNumberForState'])
    if "Tested" in df_summary.index:
        df['cumulativeTestedNumberForState'] = df_summary['Tested'] #.astype(int).sum()
    if "Tested" in df_districts.columns:
        df['cumulativeTestedNumberForDistrict'] = df_districts['Tested']
    df['cumulativeDeceasedNumberForDistrict'] = df_districts['Deceased']
    df['cumulativeRecoveredNumberForDistrict'] = df_districts['Recovered']
    # df['cumulativeOtherNumberForDistrict'] = df_districts['Other']
    # print(Date)
    # a=b
    df['Date'] = Date
    df['State/UTCode'] = StateCode
     
    df['cumulativeRecoveredNumberForState'] = df_summary['Recovered'] #.astype(int).sum()
    df['cumulativeDeceasedNumberForState'] = df_summary['Deceased'] #.astype(int).sum()
    
    try:
        df['cumulativeOtherNumberForDistrict'] = df_districts['Other']
        df['notesForDistrict'] = df_districts['notesForDistrict']
    except:
        df['cumulativeOtherNumberForDistrict'] = 0
    try:
        df['cumulativeOtherNumberForState'] = df_summary['Other']
    except:
        df['cumulativeOtherNumberForState'] = 0
    try:
        df['notesForState'] = df_summary['notesForState']
    except:
        pass
    
    IST = pytz.timezone('Asia/Kolkata')
    df['last_updated'] = utc_dt.astimezone(IST).isoformat()
    # print(df.head(1))
    # a=b
    df.to_csv("../RAWCSV/{}/{}_raw.csv".format(Date,StateCode))
    



def ExtractFromPDF(StateCode = "KA",Date = "2021-11-22"):
    try:
        filepath = "../INPUT/{0}/{1}.pdf".format(Date,StateCode)
        if StateCode == "KA":
            df_summary,df_districts = getKAData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        elif StateCode == "TN":
            df_summary,df_districts = getTNData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        elif StateCode == "HR":
            df_summary,df_districts = getHRData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        elif StateCode == "WB":
            df_summary,df_districts = getWBData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        elif StateCode == "MH":
            df_summary,df_districts = getMHData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        elif StateCode == "PB":
            df_summary,df_districts = getPBData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        elif StateCode == "UT":
            df_summary,df_districts = getUKData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        elif StateCode == "NL":
            df_summary,df_districts = getNLData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        elif StateCode == "LA":
            df_summary,df_districts = getLAData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        elif StateCode == "ML":
            df_summary,df_districts = getMLData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        elif StateCode == "RJ":
            df_summary,df_districts = getRJData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        elif StateCode == "AP":
            df_summary,df_districts = getAPData(filepath,Date,StateCode)
            # GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        elif StateCode == "UP":
            print('UP loading')
            df_summary,df_districts = getUPData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        elif StateCode == "KL":
            df_summary,df_districts = getKLData(filepath,Date,StateCode)
            print("Data Extracted Sucessfully")
            GenerateRawCsv(StateCode,Date,df_districts,df_summary)
            
        # elif StateCode == "MZ":
        #     df_summary,df_districts = getMZData(filepath,Date,StateCode)
        #     GenerateRawCsv(StateCode,Date,df_districts,df_summary)
        StatusMsg(StateCode,Date,"OK","COMPLETED","ExtractFromPDF")
    except HTTPError:
        StatusMsg(StateCode,Date,"ERR","Source URL Not Accessible/ has been changed","ExtractFromPDF")
    except FileNotFoundError:
        # raise
        StatusMsg(StateCode,Date,"ERR","Source PDF not present in input","ExtractFromPDF")
    except Exception:
        # raise
        StatusMsg(StateCode,Date,"ERR","Fatal error in main loop","ExtractFromPDF")
        

        

# def date_range(start, end):
#     r = (end+timedelta(days=1)-start).days
#     return [start+timedelta(days=i) for i in range(r)]
 

# start_date = "2022-01-04"
# end_date = "2022-01-25"
# end = datetime.strptime(end_date, '%Y-%m-%d')
# start = datetime.strptime(start_date, '%Y-%m-%d')
# dateList = date_range(start, end)

        
# for date in tqdm(dateList):
#     # pass
#     print(date)
#     ExtractFromPDF(StateCode = "NL",Date = str(date.date()))

# ExtractFromPDF(StateCode = "UT",Date = "2022-08-22")
# ExtractFromPDF(StateCode = "RJ",Date = "2022-08-29")
# ExtractFromPDF(StateCode = "TN",Date = "2022-09-17")
# ExtractFromPDF(StateCode = "PB",Date = "2022-09-26")
# ExtractFromPDF(StateCode = "MH",Date = "2022-08-04")
# ExtractFromPDF(StateCode = "UT",Date = "2022-10-17")
# ExtractFromPDF(StateCode = "UP",Date = "2021-12-17")
# ExtractFromPDF(StateCode = "UP",Date = "2022-01-05")

# ExtractFromPDF(StateCode = "TN",Date = "2022-10-15")
# ExtractFromPDF(StateCode = "UP",Date = "2022-01-27")
# ExtractFromPDF(StateCode = "UP",Date = "2022-02-14")

# upto 14th
# ExtractFromPDF(StateCode = "TN",Date = "2022-10-08")
# ExtractFromPDF(StateCode = "MH",Date = "2022-09-26")
# ExtractFromPDF(StateCode = "PB",Date = "2022-10-05")
# ExtractFromPDF(StateCode = "ML",Date = "2022-10-08")
# ExtractFromPDF(StateCode = "PB",Date = "2022-10-18")


# GenerateRawCsv(AP,"2022-04-06",df_districts,df_summary)
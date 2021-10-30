# import tabula
import pandas as pd
# !pip install tabula-py
import camelot
import os
import string
import pytz
from datetime import datetime, timezone
from tzlocal import get_localzone
from StatusMsg import StatusMsg
from urllib.error import HTTPError
#programe extracts the tabels from the PDF files.
# Need some Preprocessing to convert to RawCSV
#Have Done for KA and HR for reference
# a=b
#declare the path of your file
file_path = r"../INPUT/2021-10-26/KA.pdf"
#Convert your file
# reads all the tables in the PDF

def getKAData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,pages='5')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')

    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-5-table-1.csv'.format(date,StateCode),skiprows=3)
    df_districts.columns = df_districts.columns.str.replace("\n","")
    df_districts = df_districts[:-3]
    col_dict = {"District Name":"District","Total Positives":"Confirmed","Total Discharges":"Recovered","Total Covid Deaths":"Deceased"}
    df_districts.rename(columns=col_dict,inplace=True)
    df_districts.drop(columns=['Sl. No','Today’s Positives','Today’s Discharges','Total Active Cases','Today’s Reported Covid Deaths','Death due to  Non-Covid reasons#'],inplace=True)
    print(df_districts)
    # df = df[]

    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Karnataka'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)



    df_summary = df_districts #testcode needs to be updated later
    return df_summary,df_districts

def getTNData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,pages='7')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')

    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-7-table-1.csv'.format(date,StateCode))
    df_districts.columns = df_districts.columns.str.replace("\n","")
    df_districts = df_districts[:-4]
    col_dict = {"Total Positive Cases":"Confirmed","Discharged":"Recovered","Death":"Deceased"}
    df_districts.rename(columns=col_dict,inplace=True)
    df_districts.drop(columns=['Sl. No','Active Cases'],inplace=True)
    print(df_districts)
    # df = df[]

    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Tamil Nadu'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)


    df_summary = df_districts #testcode needs to be updated later
    return df_summary,df_districts

def getHRData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,pages='2')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')

    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))
    df_districts.columns = df_districts.columns.str.replace("\n","")
    df_districts = df_districts[:-1]
    col_dict = {"Name of District":"District","Cumulative Positive Cases":"Confirmed","Cumulative     Recovered/ Discharged Cases":"Recovered","No. of Deaths":"Deceased"}
    df_districts.rename(columns=col_dict,inplace=True)
    df_districts.drop(columns=['Sr No','Positive Cases Today','Recovery Rate (%)','No of Active Cases','COVID-19, Vaccination Status  (NHM, Haryana)',
    'Unnamed: 9','Unnamed: 10'],inplace=True)
    df_districts = df_districts[2:]
    df_districts["Recovered"] = df_districts["Recovered"].str.split("[").str[0]
    # df_districts.drop(labels=[0,1],axis=0,inplace=True)
    # df = df[]

    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Haryana'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)

    df_summary = df_districts #testcode needs to be updated later
    return df_summary,df_districts

def getWBData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,pages='2')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')

    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))
    df_districts.columns = df_districts.iloc[0]
    df_districts = df_districts[1:]
    df_districts.columns = df_districts.columns.str.replace("\n","")
    df_districts = df_districts[:-2]
    col_dict = {"Total Cases":"Confirmed","Total Discharged":"Recovered","Total Deaths":"Deceased"}
    df_districts.rename(columns=col_dict,inplace=True)
    df_districts.drop(columns=['S. No','Total Active Cases','Last Reported Case'],inplace=True)
    df_districts["Confirmed"] = df_districts["Confirmed"].str.split("+").str[0]
    df_districts["Recovered"] = df_districts["Recovered"].str.split("+").str[0]
    df_districts["Deceased"] = df_districts["Deceased"].str.split("+").str[0]

    df_districts["Confirmed"] = df_districts["Confirmed"].str.replace(",","")
    df_districts["Recovered"] = df_districts["Recovered"].str.replace(",","")
    df_districts["Deceased"] = df_districts["Deceased"].str.replace(",","")
    # df_districts.drop(labels=[0,1],axis=0,inplace=True)
    # df = df[]
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['West Bengal'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    df_summary = df_districts #testcode needs to be updated later
    return df_summary,df_districts


def getMHData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,'1,2')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')
    df_districts_1 = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-1.csv'.format(date,StateCode))
    df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))
    frames = [df_districts_1,df_districts_2]
    df_districts = pd.concat(frames,ignore_index=True)
    df_districts.columns = df_districts.columns.str.replace("\n","")
    df_districts = df_districts[:-2]
    col_dict = {"District/Municipal Corporation":"District","COVID-19 cases":"Confirmed","Recovered patients":"Recovered","Deaths":"Deceased"}
    df_districts.rename(columns=col_dict,inplace=True)
    df_districts.drop(columns=['Sr. No.','Deaths due to other causes',  'Active cases'],inplace=True)
    # df_districts.drop(labels=[0,1],axis=0,inplace=True)
    # df = df[]
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Maharashtra'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    df_summary = df_districts #testcode needs to be updated later
    return df_summary,df_districts

def getPBData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,'4')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')
    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-4-table-1.csv'.format(date,StateCode))
    # df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))
    
    df_districts.columns = df_districts.columns.str.replace("\n","")
    df_districts = df_districts[:-1]
    col_dict = {"Total ConfirmedCases":"Confirmed","Total Cured":"Recovered","Deaths":"Deceased"}
    df_districts.rename(columns=col_dict,inplace=True)
    df_districts.drop(columns=['S. No.','Total ActiveCases'],inplace=True)
    print(df_districts)
    # df_districts.drop(labels=[0,1],axis=0,inplace=True)
    # df = df[]
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Punjab'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    df_summary = df_districts #testcode needs to be updated later
    return df_summary,df_districts

def getUKData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,'6')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')
    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-6-table-2.csv'.format(date,StateCode))
    # df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))  
    df_districts.columns = df_districts.columns.str.replace("\n","")
    df_districts = df_districts[:-1]
    col_dict = {"Districts":"District","Cases till Date":"Confirmed","Treated/ Cured till Date":"Recovered","Deaths":"Deceased"}
    df_districts.rename(columns=col_dict,inplace=True)
    df_districts.drop(columns=['Active Cases','Migrated/ Others'],inplace=True)
    # df_districts.drop(labels=[0,1],axis=0,inplace=True)
    # df = df[]
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Uttarakhand'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    df_summary = df_districts #testcode needs to be updated later
    return df_summary,df_districts

def getNLData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,'1')
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    # table[5].to_excel('foo.xlsx')
    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-1-table-3.csv'.format(date,StateCode),skiprows=4,
    names=['a','District','b','c','d','e','f','g','Recovered','Deceased','h','i','j','Confirmed'])
    # df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))  
    # df_districts.columns = df_districts.columns.str.replace("\n","")
    df_districts = df_districts[:-1]    
    df_districts.drop(columns=list(string.ascii_lowercase[:10]),inplace=True)
    # df_districts.drop(labels=[0,1],axis=0,inplace=True)
    # df = df[]
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Nagaland'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    df_summary = df_districts #testcode needs to be updated later
    return df_summary,df_districts

def getLAData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path,'2')
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
    df_districts.drop(columns=list(string.ascii_lowercase[:12]),inplace=True)
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Ladakh'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    df_summary = df_districts #testcode needs to be updated later
    return df_summary,df_districts


def getMZData(file_path,date,StateCode):
    table = camelot.read_pdf(file_path)
    if not os.path.isdir('../INPUT/{}/{}/'.format(date,StateCode)):
        os.mkdir('../INPUT/{}/{}/'.format(date,StateCode))
    table.export('../INPUT/{}/{}/foo.csv'.format(date,StateCode), f='csv')
    a=b
    # table[5].to_excel('foo.xlsx')
    df_districts = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode),skiprows=5,
    names = ['a','District'] + list(string.ascii_lowercase[1:10]) + ['Confirmed','k','l','Recovered','Deceased'])
    # df_districts_2 = pd.read_csv('../INPUT/{}/{}/foo-page-2-table-1.csv'.format(date,StateCode))  
    df_districts.columns = df_districts.columns.str.replace("\n","")
    df_districts = df_districts[:-1]
    # col_dict = {"b":"District"}
    # df_districts.rename(columns=col_dict,inplace=True)
    df_districts.drop(columns=list(string.ascii_lowercase[:12]),inplace=True)
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Ladakh'].to_dict()
    df_districts['District'].replace(dist_map,inplace=True)
    df_summary = df_districts #testcode needs to be updated later
    return df_summary,df_districts


def GenerateRawCsv(StateCode,Date,df_districts):
    utc_dt = datetime.now(timezone.utc)
    df = pd.DataFrame(columns=["Date","State/UTCode","District","tested_last_updated_district","tested_source_district","notesForDistrict",
    "cumulativeConfirmedNumberForDistrict","cumulativeDeceasedNumberForDistrict","cumulativeRecoveredNumberForDistrict",
    "cumulativeTestedNumberForDistrict","last_updated","tested_last_updated_state","tested_source_state","notesForState",
    "cumulativeConfirmedNumberForState","cumulativeDeceasedNumberForState","cumulativeRecoveredNumberForState","cumulativeTestedNumberForState"])

    df['District'] = df_districts['District']
    if "Confirmed" in df_districts.columns:
        df['cumulativeConfirmedNumberForDistrict'] = df_districts['Confirmed']
        df['cumulativeConfirmedNumberForState'] = df['cumulativeConfirmedNumberForDistrict'].astype(int).sum()
    if "Tested" in df_districts.columns:
        df['cumulativeTestedNumberForDistrict'] = df_districts['Tested']
        df['cumulativeTestedNumberForState'] = df['cumulativeTestedNumberForDistrict'].astype(int).sum()
    df['cumulativeDeceasedNumberForDistrict'] = df_districts['Deceased']
    df['cumulativeRecoveredNumberForDistrict'] = df_districts['Recovered']

    df['Date'] = Date
    df['State/UTCode'] = StateCode
     
    df['cumulativeRecoveredNumberForState'] = df['cumulativeRecoveredNumberForDistrict'].astype(int).sum()
    df['cumulativeDeceasedNumberForState'] = df['cumulativeDeceasedNumberForDistrict'].astype(int).sum()
    IST = pytz.timezone('Asia/Kolkata')
    df['last_updated'] = utc_dt.astimezone(IST).isoformat()

    df.to_csv("../RAWCSV/{}/{}_raw.csv".format(Date,StateCode))


def ExtractFromPDF(StateCode = "LA",Date = "2021-10-28"):
    try:
        filepath = "../INPUT/{0}/{1}.pdf".format(Date,StateCode)
        if StateCode == "KA":
            df_summary,df_districts = getKAData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts)
        elif StateCode == "TN":
            df_summary,df_districts = getTNData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts)
        elif StateCode == "HR":
            df_summary,df_districts = getHRData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts)
        elif StateCode == "WB":
            df_summary,df_districts = getWBData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts)
        elif StateCode == "MH":
            df_summary,df_districts = getMHData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts)
        elif StateCode == "PB":
            df_summary,df_districts = getPBData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts)
        elif StateCode == "UK":
            df_summary,df_districts = getUKData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts)
        elif StateCode == "NL":
            df_summary,df_districts = getNLData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts)
        elif StateCode == "LA":
            df_summary,df_districts = getLAData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts)
        elif StateCode == "MZ":
            df_summary,df_districts = getMZData(filepath,Date,StateCode)
            GenerateRawCsv(StateCode,Date,df_districts)
        StatusMsg(StateCode,Date,"OK","COMPLETED","ExtractFromPDF")
    except HTTPError:
        StatusMsg(StateCode,Date,"ERR","Source URL Not Accessible/ has been changed","ExtractFromPDF")
    except Exception:
        raise
        StatusMsg(StateCode,Date,"ERR","Fatal error in main loop","ExtractFromPDF")
        


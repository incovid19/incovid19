import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from StatusMsg import StatusMsg
import json
import os
import io
import datetime
from ExtractStateMyGov import ExtractStateMyGov
import requests
from tqdm import tqdm
import tabula
import tabulate

def combine_listItems(list):
    combined_items = ' '.join([str(item) for item in list])
    return combined_items

def getAPData(state, date, path):
    
    try:
        # file_path1 = tabula.read_pdf('../INPUT/{}/{}/'.format(date,state),pages=1,stream = True)
        file_path = tabula.read_pdf(path,pages=1,stream = True)
        
        table = tabulate(file_path1)
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
        
        base_csv= '../RAWCSV/2022-04-05/myGov/AP_raw.csv'
        df_base_csv = pd.read_csv(base_csv)
        base_csv_forState = '../RAWCSV/2022-04-06/myGov/AP_raw.csv'
        df_base_csv_forState = pd.read_csv(base_csv_forState)

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
            df_districts.loc[index, "cumulativeConfirmedNumberForDistrict"] = new_cases_col
        
        # dropping rows having Nan    
        df_districts.drop(df_districts.index[[13,14,15,16,30]],inplace=True)
        df_districts = df_districts.reset_index(drop=True)
        # df_districts.to_csv("/mnt/c/Users/91967/Downloads/AP_PDF/2022-04-06/table_csv2.csv")
        df_districts.to_csv('../INPUT/{}/{}/foo.csv'.format(date,StateCode))

        df_summary = df_districts
        df_districts = df_districts[:-1]
        # print(df_summary, df_districts)
        df_json = pd.read_json("../DistrictMappingMaster.json")
        
        dist_map = df_json['Andhra Pradesh'].to_dict()
        df_districts['District'].replace(dist_map,inplace=True)

        for index,row in df_districts.iterrows():
            filtered_base_df = df_base_csv[df_base_csv['District']==row['District']]
            # print('filtered_base_df',filtered_base_df)
            filtered_base_forState_df= df_base_csv_forState[df_base_csv_forState['District']==row['District']]
            # print('filtered_base_forState_df',filtered_base_forState_df)
            if len(filtered_base_df)== 1 and len(filtered_base_forState_df) == 1:
                # print('District:',row['District'])
                cumulative_confirmed = filtered_base_df.iloc[0]['cumulativeConfirmedNumberForDistrict'].astype(int)
                # print(cumulative_confirmed,type(cumulative_confirmed))
                # print(row['CcumulativeConfirmedNumberForDistrictases'],type(row['CacumulativeConfirmedNumberForDistrictses']))
                df_districts.loc[index, "cumulativeConfirmedNumberForDistrict"] = cumulative_confirmed+int(row['cumulativeConfirmedNumberForDistrict'])
                df_districts['cumulativeDeceasedNumberForDistrict'] = '0'
                df_districts['cumulativeRecoveredNumberForDistrict'] = '0'
                df_districts['cumulativeTestedNumberForDistrict'] = '0'
        
                df_districts['cumulativeConfirmedNumberForState'] = df_districts['cumulativeConfirmedNumberForDistrict'].sum()

                cumulativeDeceasedNumberForState = filtered_base_forState_df.iloc[0]['cumulativeDeceasedNumberForState'].astype(int)
                # print('cumulativeDeceasedNumberForState',cumulativeDeceasedNumberForState)
                df_districts['cumulativeDeceasedNumberForState'] = cumulativeDeceasedNumberForState
                cumulativeRecoveredNumberForState = filtered_base_forState_df.iloc[0]['cumulativeRecoveredNumberForState'].astype(int)
                # print('cumulativeRecoveredNumberForState')
                df_districts['cumulativeRecoveredNumberForState'] = cumulativeRecoveredNumberForState
                
                df_districts['cumulativeTestedNumberForState'] = '33462024'

           # df_summary = df_summary.iloc[-1,:]
        return df_districts 
        
    except Exception as e:
        print(e)



def andhra_pradesh(state, date, path):
    soup = BeautifulSoup(open(path.format(date, state), encoding="utf8"), "html.parser")

    tested = int(soup.find_all('span', {'id': 'lblSamples'})[0].getText())

    table = soup.find_all('table')
    df_summary = pd.read_html(str(table))[0]
    df_summary = df_summary.melt().dropna()
    # new data frame with split value columns
    new = df_summary["value"].str.rsplit(" ", n=1, expand=True)
    # making separate first name column from new data frame
    df_summary["var"] = new[0]
    # making separate last name column from new data frame
    df_summary["val"] = new[1]
    df_summary.drop(columns=["value", "variable"], inplace=True)

    df = pd.read_html(str(table))[1]
    df.columns = df.iloc[0]
    dist_names = {"Name of the District": "District", "Confirmed Cases": "Confirmed", "Cured/ Discharged": "Recovered",
                  "Deceased": "Deceased"}
    df.rename(columns=dist_names, inplace=True)
    df = df[df['District'] != 'Total AP Cases']
    df_state = df.iloc[-1,:]
    df = df[1:-1]

    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Andhra Pradesh'].to_dict()
    df['District'].replace(dist_map, inplace=True)
    df['StateConfirmed'] = df_state['Confirmed'] #int(df_summary['val'][df_summary['var'] == 'Confirmed Cases'])
    df['StateRecovered'] = df_state['Recovered'] #int(df_summary['val'][df_summary['var'] == 'Cured/ Discharged'])
    df['StateDeceased'] = df_state['Deceased'] #int(df_summary['val'][df_summary['var'] == 'Deceased'])
    df['StateTested'] = tested
    new_dict = {}
    for key, val in df.to_dict().items():
        new_dict[key] = list(val.values())
    df = pd.DataFrame(new_dict)
    # print(df)
    # # a=b
    GenerateRawCsv(state, date, df)


def getASData(path):
    soup = BeautifulSoup(open(path, encoding="utf8"), "html.parser")
    table = soup.find_all('table')
    # print(str(table))
    # reading html file from districts url in sources.csv
    df_districts = pd.read_html(str(table))[0]
    # dropping unwanted cols
    df_districts.drop(columns=["View Details"], inplace=True)
    # replacing removing - and converting them to NaN(implicit)
    df_districts.replace({"-": ""}, inplace=True)

    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Assam'].to_dict()
    df_districts['District'].replace(dist_map, inplace=True)

    # converting numeric col to float
    df_districts = df_districts.apply(pd.to_numeric, errors="ignore")
    # print(df_districts.sum())
    # creating dictionary that has summary data for state of Assam
    dict_temp = {"var": ["Confirmed", "Active", "Recovered", "Deceased"],
                 "val": [df_districts.sum()[1], df_districts.sum()[2], df_districts.sum()[3], df_districts.sum()[4]]}
    df_summary = pd.DataFrame(dict_temp)

    # print("="*50)
    # print(df_districts)
    # print("="*50)
    # print(df_summary)
    return df_summary, df_districts


def gujarat(state, date, path):
    soup = BeautifulSoup(open(path.format(date, state), encoding="utf8"), "html.parser")
    table = soup.find_all('table')

    # reading html file from districts url in sources.csv
    df = pd.read_html(str(table))[0]

    # dropping unwanted cols
    df.drop(columns=["People Under Quarantine"], inplace=True)
    df = df[:-1]

    # getting cummulative values
    try:
        df["Cases Tested for COVID19"] = df["Cases Tested for COVID19"].str.split().str[-1]
    except:
        pass
    try:
        df["Patients Recovered"] = df["Patients Recovered"].str.split().str[-1]
    except:
        pass
    # df["Total Deaths"] = df["Total Deaths"].str.split().str[-1]
    # df["Active Cases"] = df["Active Cases"].str.split().str[-1]

    # Renaming cols name
    df.rename(
        columns={"Active Cases": "Active", "Cases Tested for COVID19": "Tested", "Patients Recovered": "Recovered",
                 "Total Deaths": "Deceased"}, inplace=True)

    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Gujarat'].to_dict()
    df['District'].replace(dist_map, inplace=True)

    df['Recovered'] = df['Recovered'].astype(int)
    try:
        df['Deceased'] = df['Deceased'].astype(int)
    except:
        df['Deceased'] = df['Deceased'].str.split().str[-1]
        df['Deceased'] = df['Deceased'].astype(int)
    df['Tested'] = df['Tested'].astype(int)

    df['Confirmed'] = df['Active'].astype(int) + df['Recovered'] + df['Deceased']

    df = df.apply(pd.to_numeric, errors="ignore")

    df['StateTested'] = tested = int(soup.find_all("h3", {'id': 'ctl00_body_h3PatientTestedCount'})[0].getText())
    df['StateRecovered'] = recovered = int(soup.find_all("h3", {'id': 'ctl00_body_h3PatientCuredCount'})[0].getText())
    df['StateDeceased'] = death = int(soup.find_all("h3", {'id': 'ctl00_body_h3TotalDath'})[0].getText())
    active = int(soup.find_all("h3", {'id': 'ctl00_body_h3TotalActiveConfirmedCount'})[0].getText())
    df['StateConfirmed'] = active + recovered + death

    # creating dictionary that has summary data for state of Assam
    dict_temp = {"var": ["Tested", "Confirmed", "Recovered", "Deceased"],
                 "val": [tested, tested + death + recovered, recovered, death]}
    df_summary = pd.DataFrame(dict_temp)
    GenerateRawCsv(state, date, df)


def odisha(state, date, path):
    soup = BeautifulSoup(open(path.format(date, state), encoding="utf8"), "html.parser")
    script = soup.find_all("script")[-1].string.split(";")
    for sc in script:
        if "var result" in sc:
            data = sc.split("(")[-1].split(")")[0]
    for div in soup.findAll('div', {'class': "graph-colm"}):
        if div.findAll('p')[0].getText().replace(" ", "").replace("\n", "") == 'Confirmed':
            confirmed = int(div.findAll('h5')[0].getText().replace(" ", "").replace("\n", "").replace(",", "").split('[')[0])
        elif div.findAll('p')[0].getText().replace(" ", "").replace("\n", "") == 'Recovered':
            recovered = int(div.findAll('h5')[0].getText().replace(" ", "").replace("\n", "").replace(",", "").split('[')[0])
        elif div.findAll('p')[0].getText().replace(" ", "").replace("\n", "") == 'Deceased':
            death = int(div.findAll('h5')[0].getText().replace(" ", "").replace("\n", "").replace(",", "").split('[')[0])
        elif div.findAll('p')[0].getText().replace(" ", "").replace("\n", "") == 'TotalTestsDone':
            tested = int(div.findAll('h5')[0].getText().replace(" ", "").replace("\n", "").replace(",", "").split('[')[0])

    df = pd.read_json(data)
    df.rename(columns={"vchDistrictName": "District", "intConfirmed": "Confirmed", "intActive": "Active",
                                 "intDeceased": "Deceased", "intRecovered": "Recovered"}, inplace=True)
    df.drop(
        columns=["intId", "intDistid", "intCategory", "intOthDeceased", "dtmCreatedOn", "dtmReportedOn", "intDistType"],
        inplace=True)
    df = df[:-1]

    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Odisha'].to_dict()
    df['District'].replace(dist_map, inplace=True)

    df['StateConfirmed'] = int(confirmed)
    df['StateRecovered'] = int(recovered)
    df['StateDeceased'] = int(death)
    df['StateTested'] = int(tested)

    dict_temp = {"var": ["Confirmed", "Recovered", "Deceased"],
                 "val": [confirmed, recovered, death]}
    df_summary = pd.DataFrame(dict_temp)
    GenerateRawCsv(state, date, df)


def tripura(state, date, path):
    soup = BeautifulSoup(open(path.format(date, state), encoding="utf8"), "html.parser")
    table = soup.find_all('table')
    df = pd.read_html(str(table), skiprows=0)[0]
    df.columns = [i[1] for i in df.columns]
    df = df.drop(
        ["SN", "Total Person Under Surveillance (Cumulative)", "No. of Persons Completed Observation Period (14 Days)",
         "Facility Surveillance", "Home Surveillance", "Total Persons Under Surveillance", "Sample Negative"], axis=1)
    df.rename(columns={"Sample Collected & Tested": "Tested", "Sample Positive": "Confirmed",
                                 "Patient Recovered": "Recovered", "Death": "Deceased","Patient Went Out of State": "Other"}, inplace=True)
    [df['StateConfirmed'], df['StateTested'], df['StateRecovered'], df['StateDeceased'], df['StateOther']] = list(df[['Confirmed', 'Tested', 'Recovered', 'Deceased' ,'Other']][df['District'] == 'Total'].values.flatten())
    dict_temp = {"var": ["Confirmed", "Tested", "Recovered", "Deceased" , "Other"],
                 "val": list(df[['Confirmed', 'Tested', 'Recovered', 'Deceased' , "Other"]][df['District'] == 'Total'].values.flatten())}
    df_summary = pd.DataFrame(dict_temp)
    df = df[:len(df) - 1]
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Tripura'].to_dict()
    df['District'].replace(dist_map, inplace=True)
    df['notesForDistrict'] = df['Other'].astype(str) + " cases were recorded as patient went out of state"
    df['notesForState'] = df['StateOther'].astype(str) + " cases were recorded as patient went out of state"
    GenerateRawCsv(state, date, df)


def kerala(state, date, path):
    tested_soup = BeautifulSoup(requests.post('https://dashboard.kerala.gov.in/covid/testing-view-public.php', "html.parser").text, 'html.parser')
    tested = int(tested_soup.find_all("span", {'class': 'info-box-number'})[0].getText())
    soup = BeautifulSoup(open(path.format(date, state), encoding="utf8"), "html.parser")
    script = soup.find_all("script")[-1].string.split(";")
    total_no = None
    for i, sc in enumerate(script):
        if "var data " in sc:
            data = sc.split("=")[-1]
        if "Total" in sc:
            total_no = i

    if total_no is not None:
        confirmed = int(script[total_no + 1].replace(' ', '').replace('\n', '').split('+')[2])
        recovered = int(script[total_no + 2].replace(' ', '').replace('\n', '').split('+')[2])
        print(recovered)
        print(script[total_no + 1])
        death = int(script[total_no + 3].replace(' ', '').replace('\n', '').split('+')[2])
    else:
        totals = []
        totals = soup.findAll('h3', {'class': "my-0 my-lg-1"})
        if len(totals) > 0:
            confirmed = int(totals[0].getText().split("(")[0].replace('*', ""))
            recovered = int(totals[2].getText().split("(")[0].replace('*', ""))
            death = int(totals[3].getText().split("(")[0].replace('*', ""))
        else:
            confirmed = recovered = death = 0

    districts_json = data.split("datasets:")
    districts = districts_json[0]
    districts = districts.replace(",],", "]}")
    districts = districts.replace("labels", "\"District\"")
    dist = pd.read_json(districts)
    data = districts_json[1][:-1]

    text_rep = {"labels": "District", "datasets": "dsets"}
    for k, v in text_rep.items():
        data = data.replace(k, v)

    text_dict = {"District": "\"District\"", "dsets": "\"dsets\"", "label": "\"label\"", "fillColor": "\"fillColor\"",
                 "strokeColor": "\"strokeColor\"",
                 "pointColor": "\"pointColor\"", "pointStrokeColor": "\"pointStrokeColor\"",
                 "pointHighlightFill": "\"pointHighlightFill\"",
                 "pointHighlightStroke": "\"pointHighlightStroke\"", "data": "\"data\""}

    for k, v in text_dict.items():
        data = data.replace(k, v)
    data = data.replace("/*", "").replace("*/", "")
    data = data.replace(",]", "]")
    
    print(data)

    df_districts = pd.read_json(data)

    Confirmed = df_districts['data'][0]
    Deceased = df_districts['data'][1]
    # Recovered = df_districts['data'][2]
    Active = df_districts['data'][2]

    df = pd.DataFrame(list(zip(dist['District'].tolist(), Confirmed, Deceased, Active)), columns=['District', 'Confirmed', 'Deceased', 'Active'])
    df["Recovered"] = df["Confirmed"] - df["Deceased"] - df["Active"]
    print(df)
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Kerala'].to_dict()
    df['District'].replace(dist_map, inplace=True)
    dict_temp = {"var": ["Confirmed", "Recovered", "Deceased"],
                 "val": [confirmed, recovered, death]}
    df['StateConfirmed'] = int(confirmed) if confirmed > 0 else sum(df['Confirmed'])
    df['StateRecovered'] = int(recovered) if recovered > 0 else sum(df['Recovered'])
    df['StateDeceased'] = int(death) if death > 0 else sum(df['Deceased'])
    df['StateTested'] = int(tested)
    df_summary = pd.DataFrame(dict_temp)
    GenerateRawCsv(state, date, df)


def maharashtra(state, date, path):
    path = path.replace('html', 'json')
    mh_data = json.load(io.open(path.format(date, state)))
    df = pd.DataFrame()
    for data in mh_data:
        df = df.append(data, ignore_index=True)
    df.drop(columns=['District Code|sum', 'Date'], inplace=True)
    df['Active Cases'] = df['Active Cases'].astype(int)
    df['Positive Cases'] = df['Positive Cases'].astype(int)
    df['Recovered'] = df['Recovered'].astype(int)
    df['Deceased'] = df['Deceased'].astype(int)
    df['Other'] = (df['Positive Cases'] - df['Recovered'] - df['Deceased']) - df['Active Cases']
    df.rename(columns={'Positive Cases': 'Confirmed'}, inplace=True)
    df_json = pd.read_json("../DistrictMappingMaster.json")
    dist_map = df_json['Maharashtra'].to_dict()
    df['District'].replace(dist_map, inplace=True)

    if os.path.isfile(path.format(date, state + '_total')):
        mh_total = json.load(io.open(path.replace('.json', '_total.json').format(date, state)))
        if type(mh_total) is list:
            mh_total = mh_total[0]
        df['StateConfirmed'] = int(mh_total['Total Prog. Positive Patient'])
        df['StateRecovered'] = int(mh_total['Progressive Discharged'])
        df['StateDeceased'] = int(mh_total['Progressive Deaths Due to Corona'])
        df['StateOther'] = sum(df['Other'])
    else:
        df['StateConfirmed'] = sum(df['Confirmed'])
        df['StateRecovered'] = sum(df['Recovered'])
        df['StateDeceased'] = sum(df['Deceased'])
        df['StateOther'] = sum(df['Other'])

    if os.path.isfile(path.format(date, state + '_testing')):
        mh_testing = json.load(io.open(path.replace('.json', '_testing.json').format(date, state)))
        if type(mh_testing) is list:
            mh_testing = mh_testing[0]
        df['StateTested'] = int(mh_testing['total'])
    
    df['notesForDistrict'] = df['Other'].astype(str) + " cases were recorded as Deaths due to Non Covid Reasons /Migrated / Others"
    df['notesForState'] = df['StateOther'].astype(str) + " cases were recorded as Deaths due to Non Covid Reasons /Migrated / Others"
    # df.to_csv("MH_test.csv")
    GenerateRawCsv(state, date, df)

# AP,KL,GJ,OD
def india(state, date, path):
    # URL = "https://www.mygov.in/corona-data/covid19-statewise-status/"
    # file_name, headers = urllib.request.urlretrieve(URL)
    soup = BeautifulSoup(open("../INPUT/"+date+"/TT_State.html", encoding="utf8"), "html.parser")

    # sum_URL = "https://www.mygov.in/covid-19"
    # sum_file_name, sum_headers = urllib.request.urlretrieve(sum_URL)
    #sum_soup = BeautifulSoup(open("../INPUT/"+date+"/TT.html", encoding="utf8"), "html.parser")
    sum_soup = BeautifulSoup(open("../INPUT/"+date+"/TT.html", encoding="utf8"), "html.parser")

    STATES = soup.find_all("div", {"class": "field field-name-field-select-state field-type-list-text field-label-above"})
    # STATES = soup.find_all("div", {"class":"marquee_data view-content"})
    # STATES = soup.find_all(soup.find_all("span", {"class":"st_name"}))
    CONFIRMED = soup.find_all("div", {"class": "field field-name-field-total-confirmed-indians field-type-number-integer field-label-above"})
    CURED_DISCHARGED = soup.find_all("div", {"class": "field field-name-field-cured field-type-number-integer field-label-above"})
    DEATH = soup.find_all("div", {"class": "field field-name-field-deaths field-type-number-integer field-label-above"})

    states = []
    for val in STATES:
        states.append(str(val.getText()).split(":")[1].lstrip().replace("Telengana", "Telangana").replace('Andaman And Nicobar', 'Andaman and Nicobar Islands').replace('Andaman and Nicobar','Andaman and Nicobar Islands'))

    confirmed = []
    for val in CONFIRMED:
        confirmed.append(str(val.getText()).split(":")[1].lstrip())

    cured = []
    for val in CURED_DISCHARGED:
        cured.append(str(val.getText()).split(":")[1].lstrip())

    death = []
    for val in DEATH:
        death.append(str(val.getText()).split(":")[1].lstrip())

    states_data = pd.DataFrame(list(zip(states, confirmed, cured, death)))
    print(states_data)

    final_df_col = [
        'Date', 'State/UTCode', 'District', 'tested_last_updated_district', 'tested_source_district',
        'notesForDistrict', 'cumulativeConfirmedNumberForDistrict', 'cumulativeDeceasedNumberForDistrict',
        'cumulativeRecoveredNumberForDistrict', 'cumulativeTestedNumberForDistrict',
        'cumulativeVaccinatedNumberForDistrict', 'last_updated', 'tested_last_updated_state', 'tested_source_state',
        'notesForState', 'cumulativeConfirmedNumberForState', 'cumulativeDeceasedNumberForState',
        'cumulativeRecoveredNumberForState', 'cumulativeTestedNumberForState', 'cumulativeVaccinatedNumberForState'
    ]

    states_data = states_data.rename(
        columns={0: "District", 1: "cumulativeConfirmedNumberForDistrict", 2: "cumulativeRecoveredNumberForDistrict",
                 3: "cumulativeDeceasedNumberForDistrict"})

    states_data["Date"] = str(datetime.datetime.now().date())
    # states_data["Date"] = date

    states_data["State/UTCode"] = state

    states_data['cumulativeConfirmedNumberForState'] = int(
        sum_soup.findAll("div", {"class": "t_case"})[0].findAll("span", {"class": "icount"})[0].getText().replace(
            ",", ""))

    states_data['cumulativeDeceasedNumberForState'] = int(
        sum_soup.findAll("div", {"class": "death_case"})[0].findAll("span", {"class": "icount"})[0].getText().replace(
            ",", ""))

    states_data['cumulativeRecoveredNumberForState'] = int(
        sum_soup.findAll("div", {"class": "discharge"})[0].findAll("span", {"class": "icount"})[0].getText().replace(
            ",", ""))

    states_data["last_updated"] = str(datetime.datetime.now())

    states_data['cumulativeTestedNumberForState'] = int(
        sum_soup.findAll("div", {"class": "testing_result"})[0].findAll("strong")[0].getText().replace(",", ""))

    for vcount in sum_soup.findAll("div", {"class": "total-vcount"}):
        if 'yday' not in vcount.attrs['class']:
            states_data['cumulativeVaccinatedNumberForState'] = int(vcount.findAll("strong")[0].getText().replace(",", ""))

    states_data = states_data.reindex(columns=final_df_col)
    # states_data = states_data.dropna(subset = ['District'])
    # states_data = states_data[states_data['District'].notna()]
    states_data.to_csv("../RAWCSV/{}/{}_raw.csv".format(date, state))


def GenerateRawCsv(state, date, df_districts):
    df = pd.DataFrame(
        columns=[
            "Date", "State/UTCode", "District", "tested_last_updated_district", "tested_source_district",
            "notesForDistrict", "cumulativeConfirmedNumberForDistrict", "cumulativeDeceasedNumberForDistrict","cumulativeOtherNumberForDistrict",
            "cumulativeRecoveredNumberForDistrict", "cumulativeTestedNumberForDistrict", "last_updated",
            "tested_last_updated_state", "tested_source_state", "notesForState", "cumulativeConfirmedNumberForState",
            "cumulativeDeceasedNumberForState", "cumulativeRecoveredNumberForState","cumulativeOtherNumberForState", "cumulativeTestedNumberForState"
        ]
    )

    state_code = json.load(io.open('../StateCode.json'))

    df['Date'] = [date] * len(df_districts)
    df['State/UTCode'] = [state] * len(df_districts)
    df['District'] = df_districts['District']
    df['last_updated'] = [datetime.datetime.now()] * len(df_districts)
    try:
        df['notesForDistrict'] = df_districts['notesForDistrict']
    except:
        df['notesForDistrict'] = None
    try:
        df['notesForState'] = df_districts['notesForState']
    except:
        df['notesForState'] = None

    df['cumulativeConfirmedNumberForDistrict'] = df_districts['Confirmed']
    df['cumulativeConfirmedNumberForState'] = df_districts['StateConfirmed']

    if "Tested" in df_districts.columns:
        df['cumulativeTestedNumberForDistrict'] = df_districts['Tested']
        df['tested_last_updated_district'] = [datetime.datetime.now()] * len(df_districts)
    if "StateTested" in df_districts.columns:
        df['cumulativeTestedNumberForState'] = df_districts['StateTested']
        df['tested_last_updated_state'] = [datetime.datetime.now()] * len(df_districts)

    df['cumulativeDeceasedNumberForDistrict'] = df_districts['Deceased']
    df['cumulativeDeceasedNumberForState'] = df_districts['StateDeceased']

    df['cumulativeRecoveredNumberForDistrict'] = df_districts['Recovered']
    df['cumulativeRecoveredNumberForState'] = df_districts['StateRecovered']
    
    try:
        df['cumulativeOtherNumberForDistrict'] = df_districts['Other']
    except:
        df['cumulativeOtherNumberForDistrict'] = 0
    try:
        df['cumulativeOtherNumberForState'] = df_districts['StateOther']
    except:
        df['cumulativeOtherNumberForState'] = 0
    df.to_csv("../RAWCSV/{}/{}_raw.csv".format(date, state), index=False)


def ExtractFromHTML(state, date):
    path = "../INPUT/{0}/{1}.html".format(date, state)
    states = {
        # 'AP': andhra_pradesh,
        # 'GJ': gujarat,
        # 'OR': odisha,
        # 'TR': tripura,
        # 'KL': kerala,
        'TT': india,
        # 'MH': maharashtra,
    }
    try:
        states[state](state, date, path)
        StatusMsg(state, date, "OK", "COMPLETED", "ExtractFromHTML")
    except Exception as e:
        # raise
        print(e)
        StatusMsg(state, date,"ERR", "Source URL Not Accessible/ has been changed", "ExtractFromHTML")
        # ExtractStateMyGov(state, date, no_source=True)

# def date_range(start, end):
#     r = (end+datetime.timedelta(days=1)-start).days
#     return [start+datetime.timedelta(days=i) for i in range(r)]
 
# start_date = "2021-10-31"
# end_date = "2022-01-20"
# end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
# start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
# dateList = date_range(start, end)

# for date in tqdm(dateList):
#     # print(str(date.date()))
#     ExtractFromHTML(state = "TR",date = str(date.date()))        

# ExtractFromHTML(state="TT", date="2023-07-03")

# ExtractFromHTML(state="TT", date="2023-06-23")
# ExtractFromHTML(state="AP", date="2022-01-29")
# ExtractFromHTML(state="MH", date="2022-01-28")
# ExtractFromHTML(state="TR", date="2022-01-24")
# ExtractFromHTML(state="KL", date="2022-04-30")
# ExtractFromHTML(state="GJ", date="2022-01-17")
# ExtractFromHTML(state="OR", date="2021-10-25")
# ExtractFromHTML(state="GJ", date="2021-10-26")
# ExtractFromHTML(state="OR", date="2021-10-26")
# ExtractFromHTML(state="GJ", date="2021-10-27")
# ExtractFromHTML(state="OR", date="2021-10-27")
# ExtractFromHTML(state="GJ", date="2021-10-28")
# ExtractFromHTML(state="OR", date="2021-10-28")
# ExtractFromHTML(state="GJ", date="2021-10-29")
# ExtractFromHTML(state="OR", date="2021-10-29")
# ExtractFromHTML(state="GJ", date="2021-10-30")
# ExtractFromHTML(state="AP", date="2022-03-18")
# ExtractFromHTML(state="TR", date="2022-07-18")

# ExtractFromHTML(state="TT", date="2023-08-02")
# ExtractFromHTML(state="TT", date="2023-08-03")
# ExtractFromHTML(state="TT", date="2023-08-05")
# ExtractFromHTML(state="TT", date="2023-08-06")
# ExtractFromHTML(state="TT", date="2023-08-07")
# ExtractFromHTML(state="TT", date="2023-08-08")
# ExtractFromHTML(state="TT", date="2023-08-09")
# ExtractFromHTML(state="TT", date="2023-08-10")
# ExtractFromHTML(state="TT", date="2023-08-11")
# ExtractFromHTML(state="TT", date="2023-08-12")
# ExtractFromHTML(state="TT", date="2023-08-13")
# ExtractFromHTML(state="TT", date="2023-08-14")
# ExtractFromHTML(state="TT", date="2023-08-15")
# ExtractFromHTML(state="TT", date="2023-08-16")
# ExtractFromHTML(state="TT", date="2023-08-17")
# ExtractFromHTML(state="TT", date="2023-08-18")
# ExtractFromHTML(state="TT", date="2023-08-19")
# ExtractFromHTML(state="TT", date="2023-08-20")
ExtractFromHTML(state="TT", date="2023-08-21")
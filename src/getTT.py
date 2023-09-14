import pandas as pd
from bs4 import BeautifulSoup
from StatusMsg import StatusMsg
import json
import os
import io
import datetime
import timedelta
import urllib.request, json 
from get7DMA import get_7dma_state
import requests

class TTNotUpdated(Exception):
    pass


def MOHFW_data(today):
    MOHFW_site_url = "https://www.mohfw.gov.in/"
    MOHFW_page = urllib.request.urlopen(MOHFW_site_url)
    applySoup = BeautifulSoup(MOHFW_page,"lxml")

    # state data json file 
    json_url = "https://www.mohfw.gov.in/data/datanew.json"
    json_data = requests.get(json_url).json()

    # tested data from ICMR 
    icmr_tested_data = "https://www.icmr.gov.in/"
    tested_page = urllib.request.urlopen(icmr_tested_data)
    applySoup_for_test_page = BeautifulSoup(tested_page, 'html.parser')

    date = applySoup.find('div', {"class":"col-xs-2"}).find_all('span')[0].text
    date = date.split(':')[1].split(',')[0]
    
    print("DateFormatted")
    print(datetime.datetime.strptime(date," %d %B %Y").date())
    
    if datetime.datetime.strptime(date," %d %B %Y").date() != datetime.datetime.today().date():
        raise TTNotUpdated("TT Not Update Please run the main.py")

    date_state = applySoup.find('div', {"class":"data-table table-responsive"}).find_all('span')[0].text
    date_state = date_state.split(':')[1].split(',')[0]
    # print(date_state)

    if datetime.datetime.strptime(date_state," %d %B %Y").date() != datetime.datetime.today().date():
        raise TTNotUpdated("TT_State Not Update Please run the main.py")

    # ICMR date 
    # using previous date as they are mentioning 
    pDate = (datetime.datetime.now() - timedelta.Timedelta(days=1)).date()

    date_tested = applySoup_for_test_page.find('div', attrs={'class':'single-cool-fact d-flex align-items-center mb-100'}).find_all('p')[0].text
    date_tested = date_tested.split('to')[2].split('(')[0].replace(",","")  
    # print(date_tested)

    if datetime.datetime.strptime(date_tested," %B %d %Y").date() !=pDate:
        raise TTNotUpdated("ICMR not updated the tested values")

    tested_data = applySoup_for_test_page.find('div', attrs={'class':'single-cool-fact d-flex align-items-center mb-100'}).find_all('h2')[0].text
    tested_value =int("".join(i for i in tested_data if i.isdecimal()))
    
    # values at India level     
    Active_value = applySoup.find('li', attrs = {'class' : 'bg-blue'}).findAll("strong")[1].text
    Recovered_value = applySoup.find('li', attrs = {'class' : 'bg-green'}).findAll("strong")[1].text
    Deaths_value = applySoup.find('li', attrs = {'class' : 'bg-red'}).findAll("strong")[1].text
    cumulativeConfirmedNumberForState = int(Active_value) + int(Recovered_value) + int(Deaths_value)

    # Vaccinated data from MOHFW
    vaccinated_value = applySoup.find('div', {"class":"col-xs-8 site-stats-count sitetotal"}).find_all('span', {'class':"coviddata"})[0].text.replace(",","")
    # print(vaccinated_value)
    
    # json_data = requests.get(json_url).json()
    states_data = pd.DataFrame(json_data)
    states_data = states_data.drop(columns=['sno','active', 'positive','cured','death','new_active','death_reconsille','total','state_code','actualdeath24hrs'])
    # print(states_data)

    states_data.drop(states_data.tail(1).index, inplace = True)
    final_df_col = [
        'Date', 'State/UTCode', 'District', 'tested_last_updated_district', 'tested_source_district',
        'notesForDistrict', 'cumulativeConfirmedNumberForDistrict', 'cumulativeDeceasedNumberForDistrict',
        'cumulativeRecoveredNumberForDistrict', 'cumulativeTestedNumberForDistrict',
        'cumulativeVaccinatedNumberForDistrict', 'last_updated', 'tested_last_updated_state', 'tested_source_state',
        'notesForState', 'cumulativeConfirmedNumberForState', 'cumulativeDeceasedNumberForState',
        'cumulativeRecoveredNumberForState', 'cumulativeTestedNumberForState', 'cumulativeVaccinatedNumberForState'
    ]

    renaming_columns_dict = {'state_name': 'District',
        'new_positive':'cumulativeConfirmedNumberForDistrict',
        'new_death':'cumulativeDeceasedNumberForDistrict',
        'new_cured':'cumulativeRecoveredNumberForDistrict'}
 
    # column rename 
    states_data.rename(columns=renaming_columns_dict, inplace=True)
    
    states_data[['District']] = states_data[['District']].replace({'\*': ''}, regex=True)

    print(states_data['District'])

    states_data["Date"] = datetime.datetime.strptime(date," %d %B %Y").date()

    states_data["State/UTCode"] = 'TT'

    states_data['cumulativeConfirmedNumberForState'] = cumulativeConfirmedNumberForState

    states_data['cumulativeDeceasedNumberForState'] = int(Deaths_value)

    states_data['cumulativeRecoveredNumberForState'] = int(Recovered_value)

    states_data["last_updated"] = str(datetime.datetime.now())
    
    states_data["tested_last_updated_state"] = str(datetime.datetime.now())

    states_data['cumulativeTestedNumberForState'] = tested_value

    states_data['cumulativeVaccinatedNumberForState'] = vaccinated_value
    
    # print(states_data)
    print("Running MOHFW...")
    states_data.to_csv('../RAWCSV/'+str(today)+'/TT_raw.csv')
    return states_data

def india(state,date):
    try:
        soup = BeautifulSoup(open("../INPUT/"+date+"/TT_State.html", encoding="utf8"), "html.parser")
        sum_soup = BeautifulSoup(open("../INPUT/"+date+"/TT.html", encoding="utf8"), "html.parser")
    except:
        if datetime.datetime.now().hour > 16:
            return MOHFW_data(date)
    
    date = sum_soup.find('div', { "class" : "updated-date"}).text.split(':')[1].split(',')[0]
    print(date)
    # date = sum_soup.find('div', { "class" : "updated-date"}).find_all('span')[0].text

    print(date)
    if datetime.datetime.strptime(date," %d %b %Y").date() != datetime.datetime.today().date():
        # return MOHFW_data()
        pass
        # raise TTNotUpdated("TT Not Update Please run the main.py")
        
    date_state = soup.find('div',{"class": "field-item even"}).text.split(",")[0]
    if datetime.datetime.strptime(date_state,"%d %b %Y").date() != datetime.datetime.today().date():
        pass
        # return MOHFW_data()
        # raise TTNotUpdated("TT_State Not Update Please run the main.py")
    
    STATES = soup.find_all("div", {"class": "field field-name-field-select-state field-type-list-text field-label-above"})
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

    states_data["Date"] = date
    # states_data["Date"] = str(datetime.datetime.now().date())

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
    
    
    states_data['tested_last_updated_state'] = sum_soup.findAll(
        "div", {"class": "test_title"})[0].getText().strip().split("up to ")[-1]
    
    states_data['deltaTestedForState'] = int(
        sum_soup.findAll("div", {"class": "testing_sample"})[0].findAll("strong")[0].getText().replace(",", ""))
    
    for vcount in sum_soup.findAll("div", {"class": "total-vcount"}):
        if 'yday' not in vcount.attrs['class']:
            states_data['cumulativeVaccinatedNumberForState'] = int(vcount.findAll("strong")[0].getText().replace(",", ""))

    # states_data = states_data.reindex(columns=final_df_col)
    return states_data

def getTT():
    today = (datetime.datetime.now() - timedelta.Timedelta(days= 43 + 0)).date()
    pDate = (datetime.datetime.now() - timedelta.Timedelta(days= 43 + 1)).date()
    cowinDate = (datetime.datetime.now() - timedelta.Timedelta(days= 43 + 2)).date()
    TT_df = india("TT",str(today))
    # TT_df = pd.read_csv("../RAWCSV/2022-08-30/TT_raw.csv")

    if not os.path.isdir(os.path.join("..","RAWCSV",str(pDate),"myGov")):
        os.mkdir(os.path.join("..","RAWCSV",str(pDate),"myGov"))
        print("Created")

    from ExtractStateMyGov import ExtractStateMyGov
    source = pd.read_csv(r"../sources.csv")
    try:
        for idx in source.index:
            if source["StateCode"][idx] != "TT":
                # print(source["StateCode"][idx])
                if source["myGov"][idx] == "yes":
                    if source["StateCode"][idx] == "DL":
                        temp_df = ExtractStateMyGov(source["StateCode"][idx],str(today))
                        df_addTest = pd.read_csv("../INPUT/DL_Tested.csv")
                        temp_df['cumulativeTestedNumberForState'] = 39999533
                    elif source["StateCode"][idx] == "AS":
                        temp_df = ExtractStateMyGov(source["StateCode"][idx],str(today))
                        temp_df['cumulativeOtherNumberForState'] = 0
                    else:
                        temp_df = ExtractStateMyGov(source["StateCode"][idx],str(today))
                else:
                    if source["StateCode"][idx] == "WB":
                        temp_df = ExtractStateMyGov(source["StateCode"][idx],str(today), no_source = True)
                        df_addTest = pd.read_csv("../INPUT/WB_Tested.csv")
                        temp_df['cumulativeTestedNumberForState'] = 26679487
                        # print(temp_df['cumulativeTestedNumberForState'])
                    else:
                        temp_df = ExtractStateMyGov(source["StateCode"][idx],str(today), no_source = True)
                temp_df["Date"] = pDate
                temp_df["notesForState"] = "As of 1st November 2022, this site will reflect the National and State level data as published by MoHFW. The district level data will not be updated beyond 31st October 2022."
                #temp_df["notesForState"] = "Since there are no updates for 25th June from MoHFW the portal reflects data of 24th June 2023"
                temp_df.to_csv(os.path.join("..","RAWCSV",str(pDate),"myGov",source["StateCode"][idx]+"_raw.csv"))
    except ValueError:
        print("Tested Values missing for DL/WB for the Date:"+ str(pDate))
        raise

    TT_df = TT_df.dropna(1)
    
    import urllib.request,json
    with urllib.request.urlopen("https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports?date="+str(pDate)) as url:
        data = json.loads(url.read().decode())

    TT_df["cumulativeVaccinated1NumberForState"] = data["topBlock"]["vaccination"]["tot_dose_1"]
    TT_df["cumulativeVaccinated2NumberForState"] = data["topBlock"]["vaccination"]["tot_dose_2"]
    TT_df["cumulativeVaccinated3NumberForState"] = data["topBlock"]["vaccination"]["tot_pd"]
    TT_df["cumulativeVaccinatedNumberForState"] = data["topBlock"]["vaccination"]["total_doses"]

    states = []
    vaccinated = []
    vaccinated1 = []
    vaccinated2 = []
    vaccinated3 = []
    for sta in data['getBeneficiariesGroupBy']:
        if (sta['title'].lower() == "dadra and nagar haveli") or (sta['title'].lower() == "daman and diu"):
            states.append('Dadra and Nagar Haveli and Daman and Diu')
        else:
            states.append(sta['title'])
        vaccinated.append(sta['total'])
        vaccinated1.append(sta['partial_vaccinated'])
        vaccinated2.append(sta['totally_vaccinated'])
        vaccinated3.append(sta['precaution_dose'])


    VAC_df = pd.DataFrame(list(zip(states,vaccinated,vaccinated1,vaccinated2,vaccinated3))).groupby(0, as_index=False).sum()

    VAC_df = VAC_df.rename(columns={0:"District",1:"cumulativeVaccinatedNumberForDistrict",2:"cumulativeVaccinated1NumberForDistrict",3:"cumulativeVaccinated2NumberForDistrict",4:"cumulativeVaccinated3NumberForDistrict"})

    TT_df = TT_df.merge(VAC_df,how="left",on="District")

    TT_df["tested_source_state"] = "https://www.icmr.gov.in/"
    
    try:
        TT_df["tested_last_updated_state"] = str(datetime.datetime.strptime(TT_df["tested_last_updated_state"][0] , '%b %d, %Y'))
    except:
        pass


    delta_date = str(pDate)

    cs = pd.read_csv("../RAWCSV/"+delta_date+"/TT_final.csv")

    TT_df["deltaConfirmedForState"] = TT_df["cumulativeConfirmedNumberForState"] - cs["cumulativeConfirmedNumberForState"][0]
    TT_df["deltaDeceasedForState"] = TT_df["cumulativeDeceasedNumberForState"] - cs["cumulativeDeceasedNumberForState"][0]
    TT_df["deltaRecoveredForState"] = TT_df["cumulativeRecoveredNumberForState"] - cs["cumulativeRecoveredNumberForState"][0]
    TT_df["deltaTestedForState"] = TT_df["cumulativeTestedNumberForState"] - cs["cumulativeTestedNumberForState"][0]

    import urllib.request, json 
    with urllib.request.urlopen("https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports?date="+str(cowinDate)) as url:
        data = json.loads(url.read().decode())

    TT_df["deltaVaccinated3ForState"] = TT_df["cumulativeVaccinated3NumberForState"] - data["topBlock"]["vaccination"]["tot_pd"]
    TT_df["deltaVaccinated2ForState"] = TT_df["cumulativeVaccinated2NumberForState"] - data["topBlock"]["vaccination"]["tot_dose_2"]
    TT_df["deltaVaccinated1ForState"] = TT_df["cumulativeVaccinated1NumberForState"] - data["topBlock"]["vaccination"]["tot_dose_1"]
    TT_df["deltaVaccinatedForState"] = TT_df["cumulativeVaccinatedNumberForState"] - data["topBlock"]["vaccination"]["total_doses"]


    states = []
    vaccinated = []
    vaccinated1 = []
    vaccinated2 = []
    vaccinated3 = []
    for sta in data['getBeneficiariesGroupBy']:
        if (sta['title'].lower() == "dadra and nagar haveli") or (sta['title'].lower() == "daman and diu"):
            states.append('Dadra and Nagar Haveli and Daman and Diu')
        else:
            states.append(sta['title'])
        vaccinated.append(sta['total'])
        vaccinated1.append(sta['partial_vaccinated'])
        vaccinated2.append(sta['totally_vaccinated'])
        vaccinated3.append(sta['precaution_dose'])

    prevdayVACC_df = pd.DataFrame(list(zip(states,vaccinated,vaccinated1,vaccinated2,vaccinated3))).groupby(0, as_index=False).sum()

    prevdayVACC_df = prevdayVACC_df.rename(columns={0:"District",1:"cumulativeVaccinatedNumberForDistrict",2:"cumulativeVaccinated1NumberForDistrict",3:"cumulativeVaccinated2NumberForDistrict",4:"cumulativeVaccinated3NumberForDistrict"})
    
    TT_df = TT_df.dropna()
    lst = ["Vaccinated1","Vaccinated2","Vaccinated3","Vaccinated"]
    for val in lst:
        TT_df["delta{}ForDistrict".format(val)] = None
        for idx in TT_df.index:
            # print(TT_df)
            TT_df["delta{}ForDistrict".format(val)][idx] = TT_df["cumulative{}NumberForDistrict".format(val)][idx] - prevdayVACC_df[prevdayVACC_df["District"] == TT_df["District"][idx]]["cumulative{}NumberForDistrict".format(val)].item()

    states_df = cs[["Date","District","cumulativeConfirmedNumberForDistrict","cumulativeRecoveredNumberForDistrict","cumulativeDeceasedNumberForDistrict"]]

    lst = ["Confirmed","Recovered","Deceased"]
    for val in lst:
        TT_df["delta{}ForDistrict".format(val)] = None
        for idx in TT_df.index:
            TT_df["delta{}ForDistrict".format(val)][idx] = int(TT_df["cumulative{}NumberForDistrict".format(val)][idx]) - int(states_df[(states_df["District"] == TT_df["District"][idx]) & (states_df["Date"] == delta_date)]["cumulative{}NumberForDistrict".format(val)].item())

    lst = ["Vaccinated1","Vaccinated2","Vaccinated3","Vaccinated"]
    for val in lst:
        TT_df["delta{}ForDistrict".format(val)] = None
        for idx in TT_df.index:
            TT_df["delta{}ForDistrict".format(val)][idx] = TT_df["cumulative{}NumberForDistrict".format(val)][idx] - prevdayVACC_df[prevdayVACC_df["District"] == TT_df["District"][idx]]["cumulative{}NumberForDistrict".format(val)].item()

    TT_df["7DmaTestedForState"] = None
    TT_df["delta21_14confirmedForState"] = None

    population = pd.read_csv("../CSV/StatePopulation.csv")

    sources = pd.read_csv("../sources.csv")

    population = population.merge(sources,how="left",left_on = "State", right_on = "StateCode")

    TT_df["statePopulation"] = population[population["StateName"] == "India"]["StatePop"].item()

    TT_df = TT_df.merge(population[["StateName","StatePop"]],how="left",left_on = "District", right_on = "StateName")

    TT_df = TT_df.rename(columns={"StatePop":"districtPopulation"})

    TT_df["Date"] = str(today)

    TT_df.to_csv('../RAWCSV/'+str(today)+'/TT_final.csv')

    TT_df.to_csv('../RAWCSV/'+str(today)+'/TT_final-'+str(today)+'.csv')

    TT_df["Date"] = str(pDate)

    TT_df.to_csv('../RAWCSV/'+str(pDate)+'/TT_final.csv')
    get_7dma_state('TT', str(pDate))
    
# india('Kerala','2022-10-17')

# getTT()
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

class TTNotUpdated(Exception):
    pass

def india(state,date):
    soup = BeautifulSoup(open("../INPUT/"+date+"/TT_State.html", encoding="utf8"), "html.parser")
    sum_soup = BeautifulSoup(open("../INPUT/"+date+"/TT.html", encoding="utf8"), "html.parser")
    
    date = sum_soup.find('div', { "class" : "updated-date"}).text.split(':')[1].split(',')[0]
    if datetime.datetime.strptime(date," %d %b %Y").date() != datetime.datetime.today().date():
        raise TTNotUpdated("TT Not Update Please run the main.py")
        
    date_state = soup.find('div',{"class": "field-item even"}).text.split(",")[0]
    if datetime.datetime.strptime(date_state,"%d %b %Y").date() != datetime.datetime.today().date():
        raise TTNotUpdated("TT_State Not Update Please run the main.py")
    
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

    states_data["Date"] = date#str(datetime.datetime.now().date())

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
    today = (datetime.datetime.now() - timedelta.Timedelta(days=1)).date()
    pDate = (datetime.datetime.now() - timedelta.Timedelta(days=2)).date()
    cowinDate = (datetime.datetime.now() - timedelta.Timedelta(days=3)).date()
    # TT_df = india("TT",str(today))
    TT_df = pd.read_csv("../RAWCSV/2022-08-30/TT_raw.csv")

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
                        temp_df['cumulativeTestedNumberForState'] = df_addTest[df_addTest["Date"] == str(pDate)]["Cumulative_Tested"].item()
                    elif source["StateCode"][idx] == "AS":
                        temp_df = ExtractStateMyGov(source["StateCode"][idx],str(today))
                        temp_df['cumulativeOtherNumberForState'] = 0
                    else:
                        temp_df = ExtractStateMyGov(source["StateCode"][idx],str(today))
                else:
                    if source["StateCode"][idx] == "WB":
                        temp_df = ExtractStateMyGov(source["StateCode"][idx],str(today), no_source = True)
                        df_addTest = pd.read_csv("../INPUT/WB_Tested.csv")
                        temp_df['cumulativeTestedNumberForState'] = df_addTest[df_addTest["Date"] == str(pDate)]["Cumulative_Tested"].item()
                    else:
                        temp_df = ExtractStateMyGov(source["StateCode"][idx],str(today), no_source = True)
                temp_df["Date"] = pDate
                temp_df.to_csv(os.path.join("..","RAWCSV",str(pDate),"myGov",source["StateCode"][idx]+"_raw.csv"))
    except ValueError:
        print("Tetsed Values missing for DL/WB for the Date:"+ str(pDate))
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

    # TT_df["tested_last_updated_state"] = str(datetime.datetime.strptime(TT_df["tested_last_updated_state"][0] , '%b %d, %Y'))


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
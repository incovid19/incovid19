#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from tqdm import tqdm
from datetime import datetime,timedelta
import inflect
import sys
sys.path.insert(0, '../src')
from util import GetFileStatus,date_range


def main():
    path = "/home/swiadmin/Incovid19/rdf/"
    dateList = date_range("2021-11-01",str((datetime.today() - timedelta(1)).date()))
    GetFileStatus(dateList,False).to_csv(path+"fileStatus.csv")
    sources = pd.read_csv(path+"sources.csv")
    sources['Parameters'] = sources.Parameters.apply(lambda x: x[1:-1].split(','))
    Date = []
    State = []
    Parameter = []
    Source = []
    ArtifactURI = []
    ExtractTime = []
    ArtifactFileFormat = []
    fs = pd.read_csv(path+"fileStatus.csv")
    for date in tqdm(dateList):
        for idx in sources.index:
            p = inflect.engine()
            for parameter in sources["Parameters"][idx]:
                Date.append(str(date.date()))
                State.append(sources["StateName"][idx])
                Parameter.append(parameter)
                # https://raw.githubusercontent.com/incovid19/incovid19/main/INPUT/2021-10-26/AP.html
                if sources["StateDataSourceType"][idx] == "Image(Twitter)":
                    ArtifactURI.append("https://raw.githubusercontent.com/incovid19/incovid19/main/INPUT/"+str(date.date())+"/"+sources["StateCode"][idx]+".jpeg")
                else:
                    ArtifactURI.append("https://raw.githubusercontent.com/incovid19/incovid19/main/INPUT/"+str(date.date())+"/"+sources["StateCode"][idx]+"."+sources["StateDataSourceType"][idx])
                if parameter in ["Confirmed","Recovered","Deceased","Others/Migrated","Tested"]:
                    try:
                        if fs[(fs["Date"] == str(date.date())) & (fs["State"] == sources["StateCode"][idx])]["myGovFlag"].item() == "No":
                            if sources["StateDataSourceType"][idx] == "pdf":
                                if sources["StateCode"][idx] == "PB":
                                    Source.append('https://nhm.punjab.gov.in/advertisements/Media_Bulletin/Media%20Bulletin%20COVID-19%20' + date.strftime("%d-%m-%Y") + '.pdf')
                                elif sources["StateCode"][idx] == "ML":
                                    Source.append('https://meghalaya.gov.in/sites/default/files/announcement/Daily_Covid_' + date.strftime("%d_%b_%Y.pdf"))
                                elif sources["StateCode"][idx] == "UT":
                                    Source.append('https://health.uk.gov.in/files/' + date.strftime("%Y.%m.%d_Health_Bulletin.pdf"))
                                elif sources["StateCode"][idx] == "WB":
                                    url = 'https://www.wbhealth.gov.in/uploaded_files/corona/WB_DHFW_Bulletin_' + p.ordinal(
                                            date.day).upper() + '_' + date.strftime("%b").upper() + '_REPORT_FINAL.pdf'
                                    Source.append(url)
                                elif sources["StateCode"][idx] == "TN":
                                    url = 'https://stopcorona.tn.gov.in/wp-content/uploads/2020/03/Media-Bulletin-' + date.strftime(
                                            "%d-%m-%y") + '-COVID-19.pdf'
                                    Source.append(url)
                                elif sources["StateCode"][idx] == "HR":
                                    url = 'http://nhmharyana.gov.in/WriteReadData/userfiles/file/CoronaVirus/Daily%20Bulletin%20of%20COVID%2019%20as%20on%20' + date.strftime(
                                            "%d-%m-%Y") + '.pdf'
                                    Source.append(url)
                                else:
                                    Source.append(sources["StateDataURL"][idx])
                            else:
                                Source.append(sources["StateDataURL"][idx])
                        else:
                            Source.append("https://www.mygov.in/covid-19")
                    except:
                        Source.append("https://www.mygov.in/covid-19")
                else:
                    Source.append("https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports")
                df = pd.read_csv("../RAWCSV/"+str(date.date())+"/"+sources["StateCode"][idx]+"_final.csv")
                ExtractTime.append(df["last_updated"][0])
                ArtifactFileFormat.append(sources["StateDataSourceType"][idx])
    df_rdf = pd.DataFrame(list(zip(Date,State,Parameter,Source,ArtifactURI,ExtractTime,ArtifactFileFormat)))
    df_rdf = df_rdf.rename(columns={0:"Date",1:"State",2:"Parameter",3:"Source",4:"ArtifactURI",5:"ExtractTime",6:"ArtifactFileFormat"})
    df_rdf.to_csv(path+"states_rdf.csv",index=False)
    df_dist = pd.read_csv("/home/swiadmin/Incovid19/incovid19/StateDistricts.csv")
    df_rdf_dist = df_dist.merge(df_rdf,left_on="State",right_on="State")
    df_rdf_dist['ArtifactURI'] = df_rdf_dist.apply(lambda x: x['Source'] if x['Parameter'] in ["Vaccination1","Vaccination2","Vaccination3"] else x['ArtifactURI'], axis=1)
    df_rdf_dist.to_csv(path+"district_rdf.csv",index=False)


# !scp *.csv swiadmin@captain.internal.semanticwebindia.in:/home/swiadmin/files/
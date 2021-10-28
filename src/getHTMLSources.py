#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
import ssl
from shutil import copyfile
import datetime
import logging
from urllib.error import HTTPError
import urllib
from StatusMsg import StatusMsg

if __name__ == "__main__":
    logging.basicConfig(filename='fetchData.log', 
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    ssl._create_default_https_context = ssl._create_unverified_context

    source = pd.read_csv(r"../sources.csv")
    today = str(datetime.datetime.now().date())

    for idx in source.index:
        if source["StateDataSourceType"][idx] == "html":
            try:
                file_name, headers = urllib.request.urlretrieve(source["StateDataURL"][idx])
                copyfile(file_name, r"../INPUT/" + today + "/" + source["StateCode"][idx] + ".html")
                logging.info("Successfully fetched file for " + source["StateCode"][idx])
                StatusMsg(source["StateCode"][idx],today,"OK","Completed","GetSource")
            except HTTPError:
                StatusMsg(source["StateCode"][idx],today,"ERR","Source URL Not Accessible/ has been changed","GetSource")
            except Exception:
                StatusMsg(source["StateCode"][idx],today,"ERR","Fatal error in main loop","GetSource")
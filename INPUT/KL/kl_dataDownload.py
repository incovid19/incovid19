#!/usr/bin/env python
# coding: utf-8

import http

import requests
import pandas as pd

df = pd.read_csv("kl_districtCode.csv")

session = requests.Session()
response = session.get('https://dashboard.kerala.gov.in/covid/index.php')

with open('kerala-index.html', 'wb') as f:
    f.write(response.content)
# print(session.cookies.get_dict())

headers = {
    'Referer': 'https://dashboard.kerala.gov.in/covid/index.php',
}
response = session.get('https://dashboard.kerala.gov.in/covid/dailyreporting-view-public-districtwise.php', headers=headers)
with open('kerala-districts.html', 'wb') as f:
    f.write(response.content)

headers = {
    'Referer': 'https://dashboard.kerala.gov.in/covid/index.php',
}
response = session.get('https://dashboard.kerala.gov.in/covid/testing-view-public.php', headers=headers)
with open('kerala-testing.html', 'wb') as f:
    f.write(response.content)

for code in df["Code"]:
    headers = {
        'Referer': 'https://dashboard.kerala.gov.in/covid/dailyreporting-view-public-districtwise.php',
    }

    files = {
        'district': (None, str(code)),
    }

    response = session.post('https://dashboard.kerala.gov.in/covid/dailyreporting-view-public-districtwise.php', headers=headers, files=files)

    with open('kerala-'+str(code)+'.html', 'wb') as f:
        f.write(response.content)

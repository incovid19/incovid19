import os
import cv2
import pandas as pd
from google.cloud import vision
from fuzzywuzzy import fuzz
from datetime import datetime
import pytz
import json
import io
import requests
import numpy as np

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../config/incovid19-728c08348911.json"


# Converts source image to bytes and then to Google Vision image input format
def get_bytes(raw_img):
    # print(raw_img)
    byte_img = cv2.imencode('.jpg', raw_img)[1].tobytes()
    vision_img = vision.Image(content=byte_img)
    return vision_img


# Performs text detection and sends the formatted text
def get_detected_text(image, col, state):
    districts = pd.read_csv('../StateDistricts.csv')
    anp = districts['District'][districts['State'] == 'Arunachal Pradesh'].tolist()
    client = vision.ImageAnnotatorClient()
    data = []
    unformatted_txt = client.document_text_detection(image=image).text_annotations[0].description
    unformatted_txt = unformatted_txt.replace("-", " ")
    if col == 'districts':
        start = 0
        for i, char in enumerate(unformatted_txt):
            if char == '\n':
                end = i
                for j, dist in enumerate(anp):
                    if 'Capital Com' in unformatted_txt[start:end]:
                        data.append("Papum Pare")
                        start = i + 1
                        break
                    partial_comp = fuzz.partial_ratio(unformatted_txt[start:end], dist)
                    comp = fuzz.ratio(unformatted_txt[start:end], dist)
                    if partial_comp >= 90:
                        if comp >= 90:
                            data.append(anp.pop(j))
                            start = i + 1
                            break
            unformatted_txt = unformatted_txt[:start] + unformatted_txt[start:i + 1].replace("\n", " ") + unformatted_txt[i+1:]
        data.append("Total")
    else:
        semiformatted_txt = unformatted_txt.split("\n")
        for text in semiformatted_txt:
            text = text.replace('.', '')
            text = text.split(" ")
            for i in text:
                try:
                    data.append(int(i))
                except ValueError:
                    continue
    return data


def get_image(state, date, search_query):
    header = json.load(io.open(r'../config/twitter.json'))

    img_count = {
        'ar': 1
    }

    query = search_query + '&expansions=attachments.media_keys&media.fields=url&tweet.fields=created_at'
    response = json.loads(
        requests.get("https://api.twitter.com/2/tweets/search/recent?query=" + query, headers=header).content)

    images = []

    for data in response['data']:
        if datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ') >= datetime.strptime(date, "%Y-%m-%d"):
            for i in range(img_count[state]):
                media_id = data['attachments']['media_keys'][0]
                media_url = next(
                    (media['url'] for media in response['includes']['media'] if media['media_key'] == media_id),
                    None
                )
                images.append(cv2.imdecode(np.frombuffer(requests.get(media_url).content, np.uint8), -1))
            return images


def arunachal_pradesh(state, date, query):
    image = get_image(state, date, query)[0]

    cv2.imwrite('../INPUT/' + date + "/" + state + ".jpeg", image)
    client = vision.ImageAnnotatorClient()

    status_text = "Status and Details of Samples Collection till"

    page = client.document_text_detection(image=get_bytes(image)).text_annotations
    page_text = page[0].description
    date_start = page_text.find(status_text)
    date_end = page_text.find("\n", date_start)

    date_string = page_text[date_start:date_end].replace(status_text + " ", "").replace("(updated at ", "").replace(")", "").replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
    last_updated = datetime.strptime(date_string[:-4], "%d %B %Y %I.%M").replace(tzinfo=pytz.timezone("Asia/Kolkata"))

    total = False
    for i, text in enumerate(page[:-1]):
        if (text.description == "Person") and (page[i + 1].description == "tested"):
            test_x1 = text.bounding_poly.vertices[0].x - 10
            test_x2 = text.bounding_poly.vertices[1].x + 10
        if (text.description == "Total") and (page[i + 1].description == "Active"):
            total_x1 = text.bounding_poly.vertices[0].x - 10
            total_x2 = text.bounding_poly.vertices[1].x + 10
        if (text.description == "Discharged") and (page[i + 1].description == "Death"):
            recover_x1 = text.bounding_poly.vertices[0].x - 10
            recover_x2 = text.bounding_poly.vertices[1].x + 10
            death_x1 = page[i + 1].bounding_poly.vertices[0].x - 10
            death_x2 = page[i + 1].bounding_poly.vertices[1].x + 10
        if text.description == 'Anjaw':
            x = text.bounding_poly.vertices[0].x - 9
            y = text.bounding_poly.vertices[0].y - 11
            total = True
        if text.description == 'Papum':
            x2 = text.bounding_poly.vertices[0].x - 9
            if (x >= x2 + 5) or (x <= x2 - 5):
                x -= 39
        if text.description == 'District':
            xm1 = text.bounding_poly.vertices[0].x
            xm2 = text.bounding_poly.vertices[1].x
        if (text.description == "Total") and total:
            y2 = text.bounding_poly.vertices[2].y + 11


    ar = {
        'districts': {
            'image': {
                'source': image[y:y2, x:xm2+xm1-x+9],
                'bytes': None
            },
            'data': None
        },
        'total': {
            'image': {
                'source': image[y:y2, total_x1:total_x2],
                'bytes': None
            },
            'data': None
        },
        'recovered': {
            'image': {
                'source': image[y:y2, recover_x1:recover_x2],
                'bytes': None
            },
            'data': None
        },
        'dead': {
            'image': {
                'source': image[y:y2, death_x1:death_x2],
                'bytes': None
            },
            'data': None
        },
        'tested': {
            'image': {
                'source': image[y:y2, test_x1:test_x2],
                'bytes': None
            },
            'data': None
        },
    }

    data_source = 'https://twitter.com/DirHealth_ArPr'

    for col in ar.keys():
        ar[col]['image']['bytes'] = get_bytes(ar[col]['image']['source'])
        ar[col]['data'] = get_detected_text(ar[col]['image']['bytes'], col, 'Arunachal Pradesh')

    anp_data = []

    for i in range(len(ar['districts']['data'])-1):
        anp_data.append({
            'District': ar['districts']['data'][i],
            'cumulativeConfirmedNumberForDistrict': ar['total']['data'][i],
            'cumulativeDeceasedNumberForDistrict': ar['dead']['data'][i],
            'cumulativeRecoveredNumberForDistrict': ar['recovered']['data'][i],
            'cumulativeTestedNumberForDistrict': ar['tested']['data'][i],
        })

    ar_df = pd.DataFrame(data=anp_data)
    ar_df = ar_df.groupby(ar_df['District']).aggregate(
        {
            'District': 'first',
            'cumulativeConfirmedNumberForDistrict': 'sum',
            'cumulativeDeceasedNumberForDistrict': 'sum',
            'cumulativeRecoveredNumberForDistrict': 'sum',
            'cumulativeTestedNumberForDistrict': 'sum',
        }
    )
    ar_df['Date'] = last_updated.date()
    ar_df['tested_last_updated_district'] = last_updated
    ar_df['last_updated'] = last_updated
    ar_df['tested_last_updated_state'] = last_updated
    ar_df['State'] = 'Arunachal Pradesh'
    ar_df['tested_source_district'] = data_source
    ar_df['tested_source_state'] = data_source
    ar_df['cumulativeConfirmedNumberForState'] = ar['total']['data'][-1]
    ar_df['cumulativeDeceasedNumberForState'] = ar['dead']['data'][-1]
    ar_df['cumulativeRecoveredNumberForState'] = ar['recovered']['data'][-1]
    ar_df['cumulativeTestedNumberForState'] = ar['tested']['data'][-1]
    ar_df.to_csv('../RAWCSV/' + date + '/ar_raw.csv', index=False, header=True)


def ExtractDataFromImage(state, date, handle, term):
    states = {
        'ar': arunachal_pradesh
    }
    query = '(' + term.replace(" ", '%20').replace(':', '%3A').replace('#', '%23').replace('@', '%40') + ')' + '(from:' + handle + ')'
    states[state](state, date, query)


ExtractDataFromImage('ar', '2021-10-24', 'DirHealth_ArPr', '#ArunachalCoronaUpdate')


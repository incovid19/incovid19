import os
import cv2
import pandas as pd
from google.cloud import vision
from fuzzywuzzy import fuzz, process
from datetime import datetime, timedelta
from pytz import timezone
import json
import io
import requests
import numpy as np
from StatusMsg import StatusMsg
from ExtractStateMyGov import ExtractStateMyGov

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../config/incovid19-google-auth.json"


# Converts source image to bytes and then to Google Vision image input format
def get_bytes(raw_img):
    byte_img = cv2.imencode('.jpg', raw_img)[1].tobytes()
    vision_img = vision.Image(content=byte_img)
    return vision_img


def get_districts(text, state):
    districts = pd.read_csv('../StateDistricts.csv')
    hindi_dist = json.load(io.open("../DistrictMatchingHindi.json", encoding="utf8"))
    district_master = json.load(io.open("../DistrictMappingMaster.json"))
    districts = districts['District'][districts['State'] == state].tolist()
    start = 0
    data = []
    if state in ['Bihar', 'Chhattisgarh']:
        for dist in text.split("\n"):
            if "Total" in dist:
                data.append("Total")
            elif dist == "":
                continue
            else:
                dist = dist.replace("|", "")
                if dist[0] == " ":
                    dist = dist[1:]
                if dist in hindi_dist[state]:
                    data.append(hindi_dist[state][dist])

    else:
        for i, char in enumerate(text):
            if char == '\n':
                end = i
                text_compare = text[start:end].replace('\n', ' ').title()
                if text_compare in district_master[state]:
                    if (text_compare == 'Papum Pare') or (text_compare not in data):
                        # print(text_compare)
                        data.append(district_master[state][text_compare])
                        start = i + 1
                elif (state == 'Arunachal Pradesh') and (text[start:end] in ['Lower', 'Upper', 'East', 'West']):
                    continue
                else:
                    token = process.extractOne(text[start:end].replace("\n", " ").lower(), districts)
                    if (token[1] > 80) and (text[start:end] != 'Valley'):
                        if (token[0] == 'Papum Pare') or (token[0] not in data):
                            data.append(token[0])
                            start = i + 1
                    else:
                        start = i + 1
                        continue
        data.append("Total")
    return data


# Performs text detection and sends the formatted text
def get_detected_text(image, col, state):
    client = vision.ImageAnnotatorClient()
    data = []
    unformatted_txt = client.document_text_detection(image=image).text_annotations[0].description
    unformatted_txt = unformatted_txt.replace("-", " ")
    if col == 'districts':
        data = get_districts(unformatted_txt, state)
    else:
        semiformatted_txt = unformatted_txt.split("\n")
        for text in semiformatted_txt:
            text = text.replace('.', '')
            text = text.replace(',', '')
            text = text.replace('*', '')
            text = text.replace('I', '1')
            text = text.replace('€', '6')
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
        'AR': 1,
        'BR': 2,
        'CT': 3,
        'HP': 2,
        'MN': 3,
        'RJ': 1,
        'JK': 4,
    }
    query = search_query + '&expansions=attachments.media_keys&media.fields=url&tweet.fields=created_at'
    response = requests.get("https://api.twitter.com/2/tweets/search/recent?query=" + query, headers=header)

    if response.status_code == 200:
        images = []
        response = json.loads(response.content)
        for data in response['data']:
            if datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ') >= datetime.strptime(date, "%Y-%m-%d"):
                if datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ') < datetime.strptime(date, "%Y-%m-%d") + timedelta(1):
                    for i in range(img_count[state]):
                        media_id = data['attachments']['media_keys'][i]
                        media_url = next(
                            (media['url'] for media in response['includes']['media'] if media['media_key'] == media_id),
                            None
                        )
                        images.append(cv2.imdecode(np.frombuffer(requests.get(media_url).content, np.uint8), -1))
                    return images
    else:
        return None


# Concatenate multiple images together
def image_concat(images):
    w = min(img.shape[1] for img in images)
    images = [cv2.resize(img, (w, int(img.shape[0] * w / img.shape[1])), interpolation=cv2.INTER_CUBIC) for img in images]
    return cv2.vconcat(images)


def get_dict(image, districts=None, total=None, recovered=None, dead=None, tested=None):
    arguments = locals()
    data = {}
    for key in arguments.keys():
        if key == 'image':
            continue
        if arguments[key] is not None:
            data[key] = {
                'image': {
                    'source': image[arguments[key][2]:arguments[key][3], arguments[key][0]:arguments[key][1]],
                    'bytes': None,
                },
                'data': None
            }
    return data


# Extract data for Arunachal Pradesh
def arunachal_pradesh(state, date, query):
    state_name = 'Arunachal Pradesh'
    image = get_image(state, date, query)
    if image is None:
        return ['ERR', 'Source not accessible']

    image = image[0]

    cv2.imwrite('../INPUT/' + date + "/" + state + ".jpeg", image)
    client = vision.ImageAnnotatorClient()

    status_text = "Status and Details of Samples Collection till "

    page = client.document_text_detection(image=get_bytes(image)).text_annotations
    page_text = page[0].description
    date_start = page_text.find(status_text)
    date_end = page_text.find("M", date_start)

    date_string = page_text[date_start:date_end+1].replace(status_text, "").replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").replace(".", "")
    last_updated = timezone("Asia/Kolkata").localize(datetime.strptime(date_string, "%d %B %Y (updated at  %I%M %p"))

    total = False
    for i, text in enumerate(page[:-1]):
        if (text.description == "Person") and (page[i + 1].description == "tested"):
            test_x1, test_x2 = text.bounding_poly.vertices[0].x - 10, text.bounding_poly.vertices[1].x + 10
        if (text.description == "Total") and not total:
            total_x1, total_x2 = text.bounding_poly.vertices[0].x - 10, text.bounding_poly.vertices[1].x + 10
        if (text.description == "Discharged") and (page[i + 1].description == "Death"):
            recover_x1, recover_x2 = text.bounding_poly.vertices[0].x - 10, text.bounding_poly.vertices[1].x + 10
            dead_x1, dead_x2 = page[i + 1].bounding_poly.vertices[0].x - 10, page[i + 1].bounding_poly.vertices[1].x + 10
        if text.description == 'Anjaw':
            x, y = text.bounding_poly.vertices[0].x - 9, text.bounding_poly.vertices[0].y - 11
            total = True
        if text.description == 'Papum':
            x2 = text.bounding_poly.vertices[0].x - 9
            if (x >= x2 + 5) or (x <= x2 - 5):
                x -= 39
        if text.description == 'District':
            xm1, xm2 = text.bounding_poly.vertices[0].x, text.bounding_poly.vertices[1].x
        if (text.description == "Total") and total:
            y2 = text.bounding_poly.vertices[2].y + 11
        elif "Siang" in text.description:
            y2 = text.bounding_poly.vertices[2].y + 31

    ar = get_dict(
        image,
        districts=[x, xm2 + xm1 - x + 9, y, y2],
        total=[total_x1, total_x2, y, y2],
        recovered=[recover_x1, recover_x2, y, y2],
        dead=[dead_x1, dead_x2, y, y2],
        tested=[test_x1, test_x2, y, y2],
    )
    data_source = 'https://twitter.com/DirHealth_ArPr'

    for col in ar.keys():
        ar[col]['image']['bytes'] = get_bytes(ar[col]['image']['source'])
        ar[col]['data'] = get_detected_text(ar[col]['image']['bytes'], col, state_name)

    ar_data = []

    single_digit = any(x < 10 for x in ar['dead']['data'])
    single_digit = any(x < 10 for x in ar['total']['data'])
    single_digit = any(x < 10 for x in ar['recovered']['data'])
    single_digit = any(x < 10 for x in ar['tested']['data'])

    if len(ar['districts']['data']) < 25:
        return ['ERR', 'Data Extraction error - Districts not detected']

    if len(ar['districts']['data']) > len(ar['dead']['data']):
        for i in range(len(ar['districts']['data']) - len(ar['dead']['data'])):
            ar['dead']['data'].insert(len(ar['dead']['data']) - 1, 0)
            single_digit = True

    if len(ar['districts']['data']) > len(ar['total']['data']):
        for i in range(len(ar['districts']['data']) - len(ar['total']['data'])):
            ar['total']['data'].insert(len(ar['total']['data']) - 1, 0)
            single_digit = True

    if len(ar['districts']['data']) > len(ar['recovered']['data']):
        for i in range(len(ar['districts']['data']) - len(ar['recovered']['data'])):
            ar['recovered']['data'].insert(len(ar['recovered']['data']) - 1, 0)
            single_digit = True

    if len(ar['districts']['data']) > len(ar['tested']['data']):
        for i in range(len(ar['districts']['data']) - len(ar['tested']['data'])):
            ar['tested']['data'].insert(len(ar['tested']['data']) - 1, 0)
            single_digit = True

    for i in range(len(ar['districts']['data'])-1):
        ar_data.append({
            'Date': date,
            'State/UTCode': state,
            'District': ar['districts']['data'][i],
            'tested_last_updated_district': last_updated,
            'tested_source_district': data_source,
            'notesForDistrict': None,
            'cumulativeConfirmedNumberForDistrict': ar['total']['data'][i],
            'cumulativeDeceasedNumberForDistrict': ar['dead']['data'][i],
            'cumulativeRecoveredNumberForDistrict': ar['recovered']['data'][i],
            'cumulativeTestedNumberForDistrict': 0,
            'last_updated': last_updated,
            'tested_last_updated_state': last_updated,
            'tested_source_state': data_source,
            'notesForState': None
        })

    ar_df = pd.DataFrame(data=ar_data)
    ar_df = ar_df.groupby(ar_df['District']).aggregate(
        {
            'Date': 'first',
            'State/UTCode': 'first',
            'District': 'first',
            'tested_last_updated_district': 'first',
            'tested_source_district': 'first',
            'notesForDistrict': 'first',
            'cumulativeConfirmedNumberForDistrict': 'sum',
            'cumulativeDeceasedNumberForDistrict': 'sum',
            'cumulativeRecoveredNumberForDistrict': 'sum',
            'cumulativeTestedNumberForDistrict': 'sum',
            'last_updated': 'first',
            'tested_last_updated_state': 'first',
            'tested_source_state': 'first',
            'notesForState': 'first',
        }
    )
    ar_df['cumulativeConfirmedNumberForState'] = ar['total']['data'][-1] if ar['total']['data'][-1] != ar_df['cumulativeConfirmedNumberForDistrict'][len(ar_df)-1] else sum(ar_df['cumulativeConfirmedNumberForDistrict'])
    ar_df['cumulativeDeceasedNumberForState'] = ar['dead']['data'][-1] if ar['dead']['data'][-1] != ar_df['cumulativeDeceasedNumberForDistrict'][len(ar_df)-1] else sum(ar_df['cumulativeDeceasedNumberForDistrict'])
    ar_df['cumulativeRecoveredNumberForState'] = ar['recovered']['data'][-1] if ar['recovered']['data'][-1] != ar_df['cumulativeRecoveredNumberForDistrict'][len(ar_df)-1] else sum(ar_df['cumulativeRecoveredNumberForDistrict'])
    ar_df['cumulativeTestedNumberForState'] = ar['tested']['data'][-1] if ar['tested']['data'][-1] != ar_df['cumulativeTestedNumberForDistrict'][len(ar_df)-1] else sum(ar_df['cumulativeTestedNumberForDistrict'])

    ar_df.to_csv('../RAWCSV/' + date + '/' + state + '_raw.csv', index=False, header=True)
    added_status_message = ""
    if single_digit:
        added_status_message = ". Single digits present in extracted data deaths column. Needs to be manually verified"
    return ["OK", "Data successfully extracted for " + state + added_status_message]


# Extract data for Bihar
def bihar(state, date, query):
    state_name = 'Bihar'
    client = vision.ImageAnnotatorClient()
    image = get_image(state, date, query)
    if image is None:
        return ['ERR', 'Source not accessible']

    page = client.document_text_detection(image=get_bytes(image[0])).text_annotations
    x = 0
    y1 = 0
    y2 = 0
    for i, text in enumerate(page):
        if text.description == 'Dated':
            last_updated = timezone("Asia/Kolkata").localize(
                datetime.strptime(page[i + 2].description, "%d-%m-%Y").replace(hour=datetime.now().hour, minute=datetime.now().minute)
            )
        if text.description == 'जाँच':
            if ((page[i - 1].description == 'कुल') and (page[i - 2].description == 'गये') and
                    (page[i - 3].description == 'किये') and (page[i - 4].description == 'में')):
                x = text.bounding_poly.vertices[1].x + 5
                y1 = text.bounding_poly.vertices[0].y - 5
                y2 = text.bounding_poly.vertices[2].y + 5
        if (text.bounding_poly.vertices[0].x > x) and (text.bounding_poly.vertices[0].y > y1) and (text.bounding_poly.vertices[2].y < y2):
            try:
                tested = int(text.description)
            except Exception:
                pass
    page1 = client.document_text_detection(image=get_bytes(image[0])).text_annotations
    p1_y = page1[-6].bounding_poly.vertices[2].y + 15
    p1_x1 = page1[-6].bounding_poly.vertices[0].x - 5
    for i, text in enumerate(page1[:-1]):
        if ((text.description == '16') and (page1[i + 1].description == ".")) or (text.description == '16.') or (text.description == '16 .'):
            p1_y = text.bounding_poly.vertices[2].y + 15
            p1_x1 = text.bounding_poly.vertices[0].x - 5
    page2 = client.document_text_detection(image=get_bytes(image[1]))
    page2 = page2.text_annotations
    p2_y = page2[1].bounding_poly.vertices[0].y - 15
    p2_x1 = page2[1].bounding_poly.vertices[0].x - 5
    for i, text in enumerate(page2[:-1]):
        if (text.description == '17') and (page2[i + 1].description == "."):
            p2_y = text.bounding_poly.vertices[0].y - 15
            p2_x1 = text.bounding_poly.vertices[0].x - 5
    x2 = min(image[0].shape[1], image[1].shape[1])
    if p1_x1 > p2_x1:
        p1_x = p1_x1 - p2_x1
        p2_x = 0
    elif p1_x1 < p2_x1:
        p2_x = p2_x1 - p1_x1
        p1_x = 0
    else:
        p1_x = p2_x = 0
    image = image_concat([image[0][:p1_y, p1_x1:x2 + p1_x], image[1][p2_y:, p2_x1:x2 + p2_x]])
    cv2.imwrite('../INPUT/' + date + "/" + state + ".jpeg", image)

    page = client.document_text_detection(image=get_bytes(image)).text_annotations
    for i, text in enumerate(page):
        if (text.description == "Positive") and (page[i + 1].description == "Cases"):
            total_x1, total_x2 = text.bounding_poly.vertices[0].x - 10, text.bounding_poly.vertices[1].x + 30
        if (text.description == "Discharged") and (page[i + 1].description == "Dead"):
            recover_x1, recover_x2 = text.bounding_poly.vertices[0].x - 10, text.bounding_poly.vertices[1].x
        if (text.description == "Dead") and (page[i + 1].description == "Active"):
            dead_x1, dead_x2 = text.bounding_poly.vertices[0].x - 10, text.bounding_poly.vertices[1].x + 20
        if text.description == 'District':
            x, x1, y = text.bounding_poly.vertices[0].x - 24, text.bounding_poly.vertices[1].x + 60, text.bounding_poly.vertices[2].y + 30
        if text.description == 'Total':
            y2 = text.bounding_poly.vertices[2].y + 11

    br = get_dict(
        image,
        districts=[x, x1, y, y2],
        total=[total_x1, total_x2, y, y2],
        recovered=[recover_x1, recover_x2, y, y2],
        dead=[dead_x1, dead_x2, y, y2]
    )

    data_source = 'https://twitter.com/BiharHealthDept'

    for col in br.keys():
        br[col]['image']['bytes'] = get_bytes(br[col]['image']['source'])
        br[col]['data'] = get_detected_text(br[col]['image']['bytes'], col, state_name)

    br_data = []

    single_digit = any(x < 10 for x in br['dead']['data'])
    single_digit = any(x < 10 for x in br['total']['data'])
    single_digit = any(x < 10 for x in br['recovered']['data'])

    if len(br['districts']['data']) < 38:
        return ['ERR', 'Data Extraction error - Districts not detected']

    if len(br['districts']['data']) > len(br['dead']['data']):
        for i in range(len(br['districts']['data']) - len(br['dead']['data'])):
            br['dead']['data'].insert(len(br['dead']['data']) - 1, 0)
            single_digit = True

    if len(br['districts']['data']) > len(br['total']['data']):
        for i in range(len(br['districts']['data']) - len(br['total']['data'])):
            br['total']['data'].insert(len(br['total']['data']) - 1, 0)
            single_digit = True

    if len(br['districts']['data']) > len(br['recovered']['data']):
        for i in range(len(br['districts']['data']) - len(br['recovered']['data'])):
            br['recovered']['data'].insert(len(br['recovered']['data']) - 1, 0)
            single_digit = True

    for i in range(len(br['districts']['data'])-1):
        br_data.append({
            'Date': date,
            'State/UTCode': state,
            'District': br['districts']['data'][i],
            'tested_last_updated_district': last_updated,
            'tested_source_district': data_source,
            'notesForDistrict': None,
            'cumulativeConfirmedNumberForDistrict': br['total']['data'][i],
            'cumulativeDeceasedNumberForDistrict': br['dead']['data'][i],
            'cumulativeRecoveredNumberForDistrict': br['recovered']['data'][i],
            'cumulativeTestedNumberForDistrict': None,
            'last_updated': last_updated,
            'tested_last_updated_state': last_updated,
            'tested_source_state': data_source,
            'notesForState': None
        })

    br_df = pd.DataFrame(data=br_data)
    br_df['cumulativeConfirmedNumberForState'] = br['total']['data'][-1]
    br_df['cumulativeDeceasedNumberForState'] = br['dead']['data'][-1]
    br_df['cumulativeRecoveredNumberForState'] = br['recovered']['data'][-1]
    br_df['cumulativeTestedNumberForState'] = int(tested)
    br_df.to_csv('../RAWCSV/' + date + '/' + state + '_raw.csv', index=False, header=True)
    added_status_message = ""
    if single_digit:
        added_status_message = ". Single digits present in extracted data deaths column. Needs to be manually verified"
    return ["OK", "Data successfully extracted for " + state + added_status_message]


# Extract data for Chhattisgarh
def chhattisgarh(state, date, query):
    state_name = 'Chhattisgarh'
    image = get_image(state, date, query)
    if image is None:
        return ['ERR', 'Source not accessible']
    client = vision.ImageAnnotatorClient()
    cv2.imwrite('../INPUT/' + date + "/" + state + ".jpeg", image_concat(image[1:]))
    summary_image = image[1]
    image = image[2]

    summary_page = client.document_text_detection(image=get_bytes(summary_image)).text_annotations

    for i, text in enumerate(summary_page):
        if text.description == 'स्थिति':
            if (summary_page[i - 1].description == 'की') and (summary_page[i - 2].description == '-19') and (summary_page[i - 3].description == 'कोविड'):
                pm = 'PM' if summary_page[i + 2].description == 'रात्रि' else 'AM'
                last_updated = timezone("Asia/Kolkata").localize(datetime.strptime(date + summary_page[i + 3].description + pm, "%Y-%m-%d%H:%M%p"))
        if text.description == 'संख्या':
            if summary_page[i - 1].description == 'की':
                tested = int(summary_page[i + 1].description.replace(",", ""))

    page = client.document_text_detection(image=get_bytes(image)).text_annotations
    for i, text in enumerate(page[:-1]):
        if text.description == "POSITIVE":
            total_x1, total_x2 = text.bounding_poly.vertices[0].x + 20, text.bounding_poly.vertices[1].x + 21
            y = text.bounding_poly.vertices[2].y + 46
        if text.description == "RECOVRED":
            recover_x1, recover_x2 = text.bounding_poly.vertices[0].x - 5, text.bounding_poly.vertices[1].x + 5
        if text.description == "DEATHS":
            dead_x1, dead_x2 = text.bounding_poly.vertices[0].x + 25, text.bounding_poly.vertices[1].x + 25
        if text.description == 'जिला':
            x, x1 = text.bounding_poly.vertices[0].x - 37, text.bounding_poly.vertices[1].x + 37
        if text.description == 'महायोग':
            y2 = text.bounding_poly.vertices[2].y

    cg = get_dict(
        image,
        districts=[x, x1, y, y2],
        total=[total_x1, total_x2, y, y2],
        recovered=[recover_x1, recover_x2, y, y2],
        dead=[dead_x1, dead_x2, y, y2]
    )

    data_source = 'https://twitter.com/HealthCgGov'

    for col in cg.keys():
        cg[col]['image']['bytes'] = get_bytes(cg[col]['image']['source'])
        cg[col]['data'] = get_detected_text(cg[col]['image']['bytes'], col, state_name)

    cg_data = []

    single_digit = any(x < 10 for x in cg['dead']['data'])
    single_digit = any(x < 10 for x in cg['total']['data'])
    single_digit = any(x < 10 for x in cg['recovered']['data'])

    if len(cg['districts']['data']) < 29:
        return ['ERR', 'Data Extraction error - Districts not detected']

    if len(cg['districts']['data']) > len(cg['dead']['data']):
        for i in range(len(cg['districts']['data']) - len(cg['dead']['data'])):
            cg['dead']['data'].insert(len(cg['dead']['data']) - 1, 0)
            single_digit = True

    if len(cg['districts']['data']) > len(cg['total']['data']):
        for i in range(len(cg['districts']['data']) - len(cg['total']['data'])):
            cg['total']['data'].insert(len(cg['total']['data']) - 1, 0)
            single_digit = True

    if len(cg['districts']['data']) > len(cg['recovered']['data']):
        for i in range(len(cg['districts']['data']) - len(cg['recovered']['data'])):
            cg['recovered']['data'].insert(len(cg['recovered']['data']) - 1, 0)
            single_digit = True

    for i in range(len(cg['districts']['data'])-1):
        cg_data.append({
            'Date': date,
            'State/UTCode': state,
            'District': cg['districts']['data'][i],
            'tested_last_updated_district': last_updated,
            'tested_source_district': data_source,
            'notesForDistrict': None,
            'cumulativeConfirmedNumberForDistrict': cg['total']['data'][i],
            'cumulativeDeceasedNumberForDistrict': cg['dead']['data'][i],
            'cumulativeRecoveredNumberForDistrict': cg['recovered']['data'][i],
            'cumulativeTestedNumberForDistrict': None,
            'last_updated': last_updated,
            'tested_last_updated_state': last_updated,
            'tested_source_state': data_source,
            'notesForState': None
        })

    cg_df = pd.DataFrame(data=cg_data)
    cg_df['cumulativeConfirmedNumberForState'] = cg['total']['data'][-1]
    cg_df['cumulativeDeceasedNumberForState'] = cg['dead']['data'][-1]
    cg_df['cumulativeRecoveredNumberForState'] = cg['recovered']['data'][-1]
    cg_df['cumulativeTestedNumberForState'] = tested
    cg_df.to_csv('../RAWCSV/' + date + '/' + state + '_raw.csv', index=False, header=True)
    added_status_message = ""
    if single_digit:
        added_status_message = ". Single digits present in extracted data deaths column. Needs to be manually verified"
    return ["OK", "Data successfully extracted for " + state + added_status_message]


# Extract data for Himachal Pradesh
def himachal_pradesh(state, date, query):
    state_name = "Himachal Pradesh"
    client = vision.ImageAnnotatorClient()
    image = get_image(state, date, query)
    test_x_before = 10
    test_x_after = 0
    if image is None:
        image = get_image(state, date, query.replace("7PM", "2PM"))
        if image is None:
            return ['ERR', 'Source not accessible']
        test_x_before = 0
        test_x_after = 30

    for img in image:
        if "Department of Health & Family Welfare" in client.document_text_detection(image=get_bytes(img)).text_annotations[0].description:
            image = img
            break

    cv2.imwrite('../INPUT/' + date + "/" + state + ".jpeg", image)

    status_text = "Media Bulletin -COVID-19\n"

    page = client.document_text_detection(image=get_bytes(image)).text_annotations
    page_text = page[0].description
    date_start = page_text.find(status_text)
    date_end = page_text.replace(status_text, "").find("\n", date_start)

    date_string = page_text[date_start+len(status_text):date_end+len(status_text)].replace(status_text, "")
    last_updated = timezone("Asia/Kolkata").localize(datetime.strptime(date_string, "%d-%m-%Y at %I:%M %p"))

    total = False
    for i, text in enumerate(page[:-1]):
        if text.description == "Sampling":
            test_x1, test_x2 = text.bounding_poly.vertices[0].x - test_x_before, text.bounding_poly.vertices[1].x + test_x_after
        if text.description == "Confirmed":
            total_x1, total_x2 = text.bounding_poly.vertices[0].x, text.bounding_poly.vertices[1].x
        if text.description == "Cured":
            if page[i + 1].description in ["Deaths", "Confirmed", "Migrated"]:
                recover_x1, recover_x2 = text.bounding_poly.vertices[0].x - 35, text.bounding_poly.vertices[1].x + 25
                total = True
        if text.description == "Deaths":
            dead_x1, dead_x2 = text.bounding_poly.vertices[0].x - 20, text.bounding_poly.vertices[1].x + 12
        if text.description == 'District':
            x, x2 = text.bounding_poly.vertices[0].x - 10, text.bounding_poly.vertices[1].x + 20
            y = text.bounding_poly.vertices[2].y + 60
        if (text.description == "Total") and total:
            y2 = text.bounding_poly.vertices[2].y + 15

    hp = get_dict(
        image,
        districts=[x, x2, y, y2],
        total=[total_x1, total_x2, y, y2],
        recovered=[recover_x1, recover_x2, y, y2],
        dead=[dead_x1, dead_x2, y, y2],
        tested=[test_x1, test_x2, y, y2],
    )
    data_source = 'https://twitter.com/nhm_hp'

    for col in hp.keys():
        hp[col]['image']['bytes'] = get_bytes(hp[col]['image']['source'])
        hp[col]['data'] = get_detected_text(hp[col]['image']['bytes'], col, state_name)

    hp_data = []

    single_digit = any(x < 10 for x in hp['dead']['data'])
    single_digit = any(x < 10 for x in hp['total']['data'])
    single_digit = any(x < 10 for x in hp['recovered']['data'])
    single_digit = any(x < 10 for x in hp['tested']['data'])

    if len(hp['districts']['data']) < 12:
        return ['ERR', 'Data Extraction error - Districts not detected']

    if len(hp['districts']['data']) > len(hp['dead']['data']):
        for i in range(len(hp['districts']['data']) - len(hp['dead']['data'])):
            hp['dead']['data'].insert(len(hp['dead']['data']) - 1, 0)
            single_digit = True

    if len(hp['districts']['data']) > len(hp['total']['data']):
        for i in range(len(hp['districts']['data']) - len(hp['total']['data'])):
            hp['total']['data'].insert(len(hp['total']['data']) - 1, 0)
            single_digit = True

    if len(hp['districts']['data']) > len(hp['recovered']['data']):
        for i in range(len(hp['districts']['data']) - len(hp['recovered']['data'])):
            hp['recovered']['data'].insert(len(hp['recovered']['data']) - 1, 0)
            single_digit = True

    if len(hp['districts']['data']) > len(hp['tested']['data']):
        for i in range(len(hp['districts']['data']) - len(hp['tested']['data'])):
            hp['tested']['data'].insert(len(hp['tested']['data']) - 1, 0)
            single_digit = True

    for i in range(len(hp['districts']['data'])-1):
        hp_data.append({
            'Date': date,
            'State/UTCode': state,
            'District': hp['districts']['data'][i],
            'tested_last_updated_district': last_updated,
            'tested_source_district': data_source,
            'notesForDistrict': None,
            'cumulativeConfirmedNumberForDistrict': hp['total']['data'][i],
            'cumulativeDeceasedNumberForDistrict': hp['dead']['data'][i],
            'cumulativeRecoveredNumberForDistrict': hp['recovered']['data'][i],
            'cumulativeTestedNumberForDistrict': hp['tested']['data'][i],
            'last_updated': last_updated,
            'tested_last_updated_state': last_updated,
            'tested_source_state': data_source,
            'notesForState': None
        })

    hp_df = pd.DataFrame(data=hp_data)
    hp_df['cumulativeConfirmedNumberForState'] = hp['total']['data'][-1]
    hp_df['cumulativeDeceasedNumberForState'] = hp['dead']['data'][-1]
    hp_df['cumulativeRecoveredNumberForState'] = hp['recovered']['data'][-1]
    hp_df['cumulativeTestedNumberForState'] = hp['tested']['data'][-1]

    added_status_message = ""
    hp_df.to_csv('../RAWCSV/' + date + '/' + state + '_raw.csv', index=False, header=True)
    if single_digit:
        added_status_message = ". Single digits present in extracted data deaths column. Needs to be manually verified"
    return ["OK", "Data successfully extracted for " + state + added_status_message]


# Extract data for Manipur
def manipur(state, date, query):
    state_name = "Manipur"
    client = vision.ImageAnnotatorClient()
    image = get_image(state, date, query)
    if image is None:
        return ['ERR', 'Source not accessible']

    recover_image = image[0]
    image = image[2]

    recover_text = "cumulative number of recovered cases is "
    recover_page = client.document_text_detection(image=get_bytes(recover_image)).text_annotations[0].description
    recover_start = recover_page.find(recover_text)
    recover_page = recover_page.replace(recover_text, "")
    recover_end = recover_page.find("(", recover_start)
    recovered = int(recover_page[recover_start:recover_end - 1].replace(",", ""))

    cv2.imwrite('../INPUT/' + date + "/" + state + ".jpeg", image)

    status_text = "Imphal, the "

    page = client.document_text_detection(image=get_bytes(image)).text_annotations
    page_text = page[0].description
    date_start = page_text.find(status_text)
    page_text = page_text.replace(status_text, "")
    date_end = page_text.find("\n", date_start)
    time_start = page_text.find("-", date_start)
    time_end = page_text.find("M", time_start)

    date_string = page_text[date_start:date_end] + page_text[time_start + 2:time_end + 1]
    date_string = date_string.replace("th", "").replace("nd", "").replace("st", "").replace("rd", "").replace("*", "")
    last_updated = timezone("Asia/Kolkata").localize(datetime.strptime(date_string, "%d %B, %Y%I:%M %p"))

    for i, text in enumerate(page[:-1]):
        if text.description == "tested":
            if page[i - 1].description in ["deaths", "Cumulative"]:
                test_x1, test_x2 = text.bounding_poly.vertices[0].x - 25, text.bounding_poly.vertices[1].x + 25
        if text.description == "positives":
            if page[i - 1].description in ["tested", "Cumulative"]:
                total_x1, total_x2 = text.bounding_poly.vertices[0].x - 20, text.bounding_poly.vertices[1].x + 15
        if text.description == "deaths":
            if page[i - 1].description in ["positives", "Cumulative"]:
                dead_x1, dead_x2 = text.bounding_poly.vertices[0].x - 15, text.bounding_poly.vertices[1].x + 10
        if text.description == 'District':
            x, x2 = text.bounding_poly.vertices[0].x - 7, text.bounding_poly.vertices[1].x + 45
            y = text.bounding_poly.vertices[0].y + 14
        if text.description == "TOTAL":
            y2 = text.bounding_poly.vertices[2].y + 2

    mn = get_dict(
        image,
        districts=[x, x2, y, y2],
        total=[total_x1, total_x2, y, y2],
        dead=[dead_x1, dead_x2, y, y2],
        tested=[test_x1, test_x2, y, y2],
    )
    data_source = 'https://twitter.com/health_manipur'

    for col in mn.keys():
        mn[col]['image']['bytes'] = get_bytes(mn[col]['image']['source'])
        mn[col]['data'] = get_detected_text(mn[col]['image']['bytes'], col, state_name)

    mn_data = []

    single_digit = any(x < 10 for x in mn['dead']['data'])
    single_digit = any(x < 10 for x in mn['total']['data'])
    single_digit = any(x < 10 for x in mn['total']['data'])

    if len(mn['districts']['data']) < 16:
        return ['ERR', 'Data Extraction error - Districts not detected']

    if len(mn['districts']['data']) > len(mn['dead']['data']):
        for i in range(len(mn['districts']['data']) - len(mn['dead']['data'])):
            mn['dead']['data'].insert(len(mn['dead']['data']) - 1, 0)
            single_digit = True

    if len(mn['districts']['data']) > len(mn['total']['data']):
        for i in range(len(mn['districts']['data']) - len(mn['total']['data'])):
            mn['total']['data'].insert(len(mn['total']['data']) - 1, 0)
            single_digit = True

    if len(mn['districts']['data']) > len(mn['tested']['data']):
        for i in range(len(mn['districts']['data']) - len(mn['tested']['data'])):
            mn['tested']['data'].insert(len(mn['tested']['data']) - 1, 0)
            single_digit = True

    for i in range(len(mn['districts']['data'])-1):
        mn_data.append({
            'Date': date,
            'State/UTCode': state,
            'District': mn['districts']['data'][i],
            'tested_last_updated_district': last_updated,
            'tested_source_district': data_source,
            'notesForDistrict': None,
            'cumulativeConfirmedNumberForDistrict': mn['total']['data'][i],
            'cumulativeDeceasedNumberForDistrict': mn['dead']['data'][i],
            'cumulativeRecoveredNumberForDistrict': None,
            'cumulativeTestedNumberForDistrict': mn['tested']['data'][i],
            'last_updated': last_updated,
            'tested_last_updated_state': last_updated,
            'tested_source_state': data_source,
            'notesForState': None
        })

    mn_df = pd.DataFrame(data=mn_data)
    mn_df['cumulativeConfirmedNumberForState'] = mn['total']['data'][-1]
    mn_df['cumulativeDeceasedNumberForState'] = mn['dead']['data'][-1]
    mn_df['cumulativeRecoveredNumberForState'] = recovered
    mn_df['cumulativeTestedNumberForState'] = mn['tested']['data'][-1]

    mn_df.to_csv('../RAWCSV/' + date + '/' + state + '_raw.csv', index=False, header=True)
    added_status_message = ""
    if single_digit:
        added_status_message = ". Single digits present in extracted data deaths column. Needs to be manually verified"
    return ["OK", "Data successfully extracted for " + state + added_status_message]


# Extract data for Rajasthan
def rajasthan(state, date, query):
    state_name = "Rajasthan"
    client = vision.ImageAnnotatorClient()
    image = get_image(state, date, query)
    if image is None:
        return ['ERR', 'Source not accessible']

    # recover_image = image[0]
    image = image[0]


    page = client.document_text_detection(image=get_bytes(image)).text_annotations
    for i, text in enumerate(page[:-1]):
        if text.description == '23':
            if page[i + 1].description == 'KARAULI':
                p1_y = text.bounding_poly.vertices[2].y + 3
        if text.description == '24':
            if page[i + 1].description == 'KOTA':
                p2_y = text.bounding_poly.vertices[0].y - 5
    image = image_concat([image[:p1_y, :], image[p2_y:, :]])

    cv2.imwrite('../INPUT/' + date + "/" + state + ".jpeg", image)

    page = client.document_text_detection(image=get_bytes(image)).text_annotations
    page_text = page[0].description

    date_status_text = "Date-"
    date_start = page_text.find(date_status_text)
    page_text = page_text.replace(date_status_text, "")
    date_end = page_text.find("(", date_start)
    time_status_text = "Time "
    time_start = page_text.find(time_status_text)
    page_text = page_text.replace(time_status_text, "")
    time_end = page_text.find(")", time_start)

    date_string = page_text[date_start:date_end] + page_text[time_start:time_end].replace(".", "")
    last_updated = timezone("Asia/Kolkata").localize(datetime.strptime(date_string, "%d.%m.%Y%I:%M %p"))

    for i, text in enumerate(page[:-1]):
        if text.description == "Sample":
            if page[i + 2].description != 'In':
                test_x1, test_x2 = text.bounding_poly.vertices[0].x - 20, text.bounding_poly.vertices[1].x + 20
        if text.description == "Positive":
            if page[i + 1].description != 'In':
                total_x1, total_x2 = text.bounding_poly.vertices[0].x - 12, text.bounding_poly.vertices[1].x + 12
        if text.description == "Death":
            dead_x1, dead_x2 = text.bounding_poly.vertices[0].x - 15, text.bounding_poly.vertices[1].x + 15
        if text.description == "charged":
            recover_x1, recover_x2 = text.bounding_poly.vertices[0].x - 10, text.bounding_poly.vertices[1].x + 10
        if text.description == 'AJMER':
            x, x2 = text.bounding_poly.vertices[0].x - 2, text.bounding_poly.vertices[1].x + 80
            y = text.bounding_poly.vertices[0].y - 2
        if text.description == "Total":
            if page[i + 1].description not in ['Status', 'Sample']:
                y2 = text.bounding_poly.vertices[2].y + 2

    rj = get_dict(
        image,
        districts=[x, x2, y, y2],
        total=[total_x1, total_x2, y, y2],
        recovered=[recover_x1, recover_x2, y, y2],
        dead=[dead_x1, dead_x2, y, y2],
        tested=[test_x1, test_x2, y, y2],
    )
    data_source = 'https://twitter.com/dineshkumawat'

    for col in rj.keys():
        rj[col]['image']['bytes'] = get_bytes(rj[col]['image']['source'])
        rj[col]['data'] = get_detected_text(rj[col]['image']['bytes'], col, state_name)
        # print(rj[col]['data'])

    rj_data = []

    single_digit = any(x < 10 for x in rj['dead']['data'])
    single_digit = any(x < 10 for x in rj['total']['data'])
    single_digit = any(x < 10 for x in rj['recovered']['data'])
    single_digit = any(x < 10 for x in rj['tested']['data'])

    if len(rj['districts']['data']) < 34:
        return ['ERR', 'Data Extraction error - Districts not detected']

    if len(rj['districts']['data']) > len(rj['dead']['data']):
        for i in range(len(rj['districts']['data']) - len(rj['dead']['data'])):
            rj['dead']['data'].insert(len(rj['dead']['data']) - 1, 0)
            single_digit = True

    if len(rj['districts']['data']) > len(rj['total']['data']):
        for i in range(len(rj['districts']['data']) - len(rj['total']['data'])):
            rj['total']['data'].insert(len(rj['total']['data']) - 1, 0)
            single_digit = True

    if len(rj['districts']['data']) > len(rj['recovered']['data']):
        for i in range(len(rj['districts']['data']) - len(rj['recovered']['data'])):
            rj['recovered']['data'].insert(len(rj['recovered']['data']) - 1, 0)
            single_digit = True

    if len(rj['districts']['data']) > len(rj['tested']['data']):
        for i in range(len(rj['districts']['data']) - len(rj['tested']['data'])):
            rj['tested']['data'].insert(len(rj['tested']['data']) - 1, 0)
            single_digit = True

    for i in range(len(rj['districts']['data'])-1):
        rj_data.append({
            'Date': date,
            'State/UTCode': state,
            'District': rj['districts']['data'][i],
            'tested_last_updated_district': last_updated,
            'tested_source_district': data_source,
            'notesForDistrict': None,
            'cumulativeConfirmedNumberForDistrict': rj['total']['data'][i],
            'cumulativeDeceasedNumberForDistrict': rj['dead']['data'][i],
            'cumulativeRecoveredNumberForDistrict': rj['recovered']['data'][i],
            'cumulativeTestedNumberForDistrict': rj['tested']['data'][i],
            'last_updated': last_updated,
            'tested_last_updated_state': last_updated,
            'tested_source_state': data_source,
            'notesForState': None
        })

    rj_df = pd.DataFrame(data=rj_data)
    rj_df['cumulativeConfirmedNumberForState'] = rj['total']['data'][-1]
    rj_df['cumulativeDeceasedNumberForState'] = rj['dead']['data'][-1]
    rj_df['cumulativeRecoveredNumberForState'] = rj['recovered']['data'][-1]
    rj_df['cumulativeTestedNumberForState'] = rj['tested']['data'][-1]

    added_status_message = ""
    rj_df.to_csv('../RAWCSV/' + date + '/' + state + '_raw.csv', index=False, header=True)
    if single_digit:
        added_status_message = ". Single digits present in extracted data deaths column. Needs to be manually verified"
    return ["OK", "Data successfully extracted for " + state + ". Images clarity may be low. Requires manual verification" + added_status_message]


# Extract data for Jammu & Kashmir
def jammu_kashmir(state, date, query):
    state_name = "Jammu and Kashmir"
    client = vision.ImageAnnotatorClient()
    image = get_image(state, date, query)
    if image is None:
        return ['ERR', 'Source not accessible']

    for img in image:
        if "Status of Surveillance" in client.document_text_detection(image=get_bytes(img)).text_annotations[0].description:
            test_image = img
        elif "UT of J&K" in client.document_text_detection(image=get_bytes(img)).text_annotations[0].description:
            image = img

    test_page = client.document_text_detection(image=get_bytes(test_image)).text_annotations
    test_text = test_page[0].description

    test_status_text = "Available till date\n"
    test_start = test_text.find(test_status_text)
    test_text = test_text.replace(test_status_text, "")
    test_end = test_text.find("\n", test_start)
    tested = int(test_text[test_start:test_end])

    status_text = "Cumulative till "
    date_start = test_text.find(status_text)
    test_text = test_text.replace(status_text, "")
    date_end = test_text.find("\n", date_start)

    last_updated = timezone("Asia/Kolkata").localize(datetime.strptime(test_text[date_start:date_end], "%d %B %Y (upto %I:%M %p)"))

    page = client.document_text_detection(image=get_bytes(image)).text_annotations
    for i, text in enumerate(page[:-1]):
        if (text.description == '10') and (text.bounding_poly.vertices[1].x <= 100):
            # if page[i + 1].description == 'Shopian':
            p1_y = text.bounding_poly.vertices[2].y + 13
        if (text.description == '11') and (text.bounding_poly.vertices[1].x <= 100):
            # if page[i + 1].description == 'Jammu':
            p2_y = text.bounding_poly.vertices[0].y - 13
        if (text.description == '20') and (text.bounding_poly.vertices[1].x <= 100):
            # if page[i + 1].description == 'Reasi':
            p3_y = text.bounding_poly.vertices[2].y + 15
        if text.description == 'UT':
            if page[i + 1].description == 'of':
                p4_y = text.bounding_poly.vertices[0].y - 12
    image = image_concat([image[:p1_y, :], image[p2_y:p3_y, :], image[p4_y:, :]])

    cv2.imwrite('../INPUT/' + date + "/" + state + ".jpeg", image_concat([test_image, image]))

    page = client.document_text_detection(image=get_bytes(image)).text_annotations
    page_text = page[0].description

    for i, text in enumerate(page[:-1]):
        if text.description == "Total":
            total_x1, total_x2 = text.bounding_poly.vertices[0].x - 20, text.bounding_poly.vertices[1].x + 20
        if text.description == "Deaths":
            dead_x1, dead_x2 = text.bounding_poly.vertices[0].x - 5, text.bounding_poly.vertices[1].x + 5
        if text.description == "Cumulative":
            recover_x1, recover_x2 = text.bounding_poly.vertices[0].x - 5, text.bounding_poly.vertices[1].x + 5
        if text.description == 'Srinagar':
            x, x2 = text.bounding_poly.vertices[0].x - 10, text.bounding_poly.vertices[1].x + 25
            y = text.bounding_poly.vertices[0].y - 10
        if text.description == "UT":
            y2 = text.bounding_poly.vertices[2].y + 10

    jk = get_dict(
        image,
        districts=[x, x2, y, y2],
        total=[total_x1, total_x2, y, y2],
        recovered=[recover_x1, recover_x2, y, y2],
        dead=[dead_x1, dead_x2, y, y2],
    )
    data_source = 'https://twitter.com/diprjk'

    for col in jk.keys():
        jk[col]['image']['bytes'] = get_bytes(jk[col]['image']['source'])
        jk[col]['data'] = get_detected_text(jk[col]['image']['bytes'], col, state_name)

    jk_data = []

    single_digit = any(x < 10 for x in jk['dead']['data'])
    single_digit = any(x < 10 for x in jk['total']['data'])
    single_digit = any(x < 10 for x in jk['recovered']['data'])

    if len(jk['districts']['data']) < 20:
        return ['ERR', 'Data Extraction error - Districts not detected']

    if len(jk['districts']['data']) > len(jk['dead']['data']):
        for i in range(len(jk['districts']['data']) - len(jk['dead']['data'])):
            jk['dead']['data'].insert(len(jk['dead']['data']) - 1, 0)
            single_digit = True

    if len(jk['districts']['data']) > len(jk['total']['data']):
        for i in range(len(jk['districts']['data']) - len(jk['total']['data'])):
            jk['total']['data'].insert(len(jk['total']['data']) - 1, 0)
            single_digit = True

    if len(jk['districts']['data']) > len(jk['recovered']['data']):
        for i in range(len(jk['districts']['data']) - len(jk['recovered']['data'])):
            jk['recovered']['data'].insert(len(jk['recovered']['data']) - 1, 0)
            single_digit = True

    for i in range(len(jk['districts']['data'])-1):
        jk_data.append({
            'Date': date,
            'State/UTCode': state,
            'District': jk['districts']['data'][i],
            'tested_last_updated_district': last_updated,
            'tested_source_district': data_source,
            'notesForDistrict': None,
            'cumulativeConfirmedNumberForDistrict': jk['total']['data'][i],
            'cumulativeDeceasedNumberForDistrict': jk['dead']['data'][i],
            'cumulativeRecoveredNumberForDistrict': jk['recovered']['data'][i],
            'cumulativeTestedNumberForDistrict': None,
            'last_updated': last_updated,
            'tested_last_updated_state': last_updated,
            'tested_source_state': data_source,
            'notesForState': None
        })

    jk_df = pd.DataFrame(data=jk_data)
    jk_df['cumulativeConfirmedNumberForState'] = jk['total']['data'][-1]
    jk_df['cumulativeDeceasedNumberForState'] = jk['dead']['data'][-1]
    jk_df['cumulativeRecoveredNumberForState'] = jk['recovered']['data'][-1]
    jk_df['cumulativeTestedNumberForState'] = tested

    added_status_message = ""
    jk_df.to_csv('../RAWCSV/' + date + '/' + state + '_raw.csv', index=False, header=True)
    if single_digit:
        added_status_message = ". Single digits present in extracted data deaths column. Needs to be manually verified"
    return ["OK", "Data successfully extracted for " + state + added_status_message]


def ExtractDataFromImage(state, date, handle, term):
    print("Executing image Extract")
    states = {
        'AR': arunachal_pradesh,
        'BR': bihar,
        'CT': chhattisgarh,
        'HP': himachal_pradesh,
        'MN': manipur,
        'RJ': rajasthan,
        'JK': jammu_kashmir,
        # 'LA': ladakh,
    }
    query = '(' + term.replace(" ", '%20').replace(':', '%3A').replace('#', '%23').replace('@', '%40') + ')' + '(from:' + handle + ')'
    try:
        response = states[state](state, date, query)
        # print(response)
        if response[1] in ['Source not accessible', 'Data Extraction error - Districts not detected']:
            response[1] = response[1].append(". Picking data from mygov")
            ExtractStateMyGov(state, date, no_source=True)
        StatusMsg(
            StateCode=state,
            date=date,
            program="ExtractDataFromImage",
            StatusCode=response[0],
            statusMessage=response[1]
        )
        # return [state, date, "ExtractDataFromImage", response[0], response[1]]
    except Exception as e:
        # print(e)
        StatusMsg(
            StateCode=state,
            date=date,
            program="ExtractDataFromImage",
            StatusCode="ERR",
            statusMessage="Data Extraction Error - {}. Picking data from mygov".format(e)
        )
        ExtractStateMyGov(state, date, no_source=True)
        # return [state, date, "ExtractDataFromImage", "ERR", "Data Extraction Error - {}".format(e)]


# API Calls - To be commented or removed from deployed code
# ExtractDataFromImage('AR', '2021-10-30', 'DirHealth_ArPr', '#ArunachalCoronaUpdate')
# ExtractDataFromImage('BR', '2021-10-30', 'BiharHealthDept', '#COVIDー19 Updates Bihar')
# ExtractDataFromImage('CT', '2021-10-30', 'HealthCgGov', '#ChhattisgarhFightsCorona')
# ExtractDataFromImage('HP', '2021-10-29', 'nhm_hp', '#7PMupdate')
ExtractDataFromImage('MN', '2021-10-30', 'health_manipur', 'Manipur updates')
# ExtractDataFromImage('RJ', '2021-10-27', 'dineshkumawat', '#Rajasthan Bulletin')
# ExtractDataFromImage('JK', '2021-10-27', 'diprjk', 'Media Bulletin')


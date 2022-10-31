import pandas as pd
from datetime import datetime, timedelta

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def col_check_state_raw_csv(df):
    cols_ls = df.columns
    reqd_col_ls = [
        "Date", "State/UTCode", "deltaConfirmedForState", "deltaDeceasedForState", "deltaRecoveredForState",
        "deltaTestedForState", "deltaVaccinated1ForState", "deltaVaccinated2ForState","deltaVaccinated3ForState", "delta21_14confirmedForState",
        "7DmaConfirmedForState", "7DmaDeceasedForState", "7DmaRecoveredForState", "7DmaTestedForState",
        "7DmaVaccinated1ForState", "7DmaVaccinated2ForState","7DmaVaccinated3ForState", "District", "deltaConfirmedForDistrict",
        "deltaDeceasedForDistrict", "deltaRecoveredForDistrict", "deltaTestedForDistrict",
        "deltaVaccinated1ForDistrict", "deltaVaccinated2ForDistrict","deltaVaccinated3ForDistrict", "delta21_14confirmedForDistrict",
        "7DmaConfirmedForDistrict", "7DmaDeceasedForDistrict", "7DmaRecoveredForDistrict", "7DmaTestedForDistrict",
        "7DmaVaccinated1ForDistrict", "7DmaVaccinated2ForDistrict","7DmaVaccinated3ForDistrict", "districtPopulation",
        "tested_last_updated_district", "tested_source_district", "notesForDistrict",
        "cumulativeConfirmedNumberForDistrict", "cumulativeDeceasedNumberForDistrict",
        "cumulativeRecoveredNumberForDistrict", "cumulativeTestedNumberForDistrict",
        "cumulativeVaccinated1NumberForDistrict", "cumulativeVaccinated2NumberForDistrict","cumulativeVaccinated3NumberForDistrict",
        "cumulativeOtherNumberForDistrict","last_updated",
        "statePopulation", "tested_last_updated_state", "tested_source_state", "notesForState",
        "cumulativeConfirmedNumberForState", "cumulativeDeceasedNumberForState", "cumulativeRecoveredNumberForState",
        "cumulativeTestedNumberForState", "cumulativeVaccinated1NumberForState", "cumulativeVaccinated2NumberForState","cumulativeVaccinated3NumberForState","cumulativeOtherNumberForState"
    ]
    for col in reqd_col_ls:
        if col not in cols_ls:
            df[col] = 0
    df_formatted = df[reqd_col_ls]
    return df_formatted


def get_7dma_state(state, date):
    df = pd.read_csv(f'../RAWCSV/{date}/{state}_final.csv')
    cols = ['Confirmed', 'Deceased', 'Recovered', 'Tested', 'Vaccinated1', 'Vaccinated2','Vaccinated3', 'Other']
    df = col_check_state_raw_csv(df)
    df.sort_values('District', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.set_index('District', inplace=True, drop=False)
    for col in cols:
        df[f'7Dma{col}ForState'] = df[f'cumulative{col}NumberForState']
        df[f'7Dma{col}ForDistrict'] = df[f'cumulative{col}NumberForDistrict']
    prev_df = pd.read_csv(f'../RAWCSV/{(datetime.strptime(date, "%Y-%m-%d") - timedelta(7)).strftime("%Y-%m-%d")}/{state}_final.csv')
    prev_df = col_check_state_raw_csv(prev_df)
    for dist in list(df['District']):
        if dist not in list(prev_df['District']):
            prev_df = prev_df.append({
                'District': dist,
                'cumulativeConfirmedNumberForState': prev_df['cumulativeConfirmedNumberForState'][0],
                'cumulativeRecoveredNumberForState': prev_df['cumulativeRecoveredNumberForState'][0],
                'cumulativeDeceasedNumberForState': prev_df['cumulativeDeceasedNumberForState'][0],
                'cumulativeTestedNumberForState': prev_df['cumulativeTestedNumberForState'][0],
                'cumulativeVaccinated1NumberForState': prev_df['cumulativeVaccinated1NumberForState'][0],
                'cumulativeVaccinated2NumberForState': prev_df['cumulativeVaccinated2NumberForState'][0],
                'cumulativeVaccinated3NumberForState': prev_df['cumulativeVaccinated3NumberForState'][0]
            }, ignore_index=True)
    prev_df.sort_values('District', inplace=True)
    prev_df.reset_index(drop=True, inplace=True)
    prev_df.set_index('District', inplace=True, drop=False)
    for col in cols:
        df[f'7Dma{col}ForState'] -= prev_df[f'cumulative{col}NumberForState']
        df[f'7Dma{col}ForDistrict'] -= prev_df[f'cumulative{col}NumberForDistrict']
    for col in cols:
        df[f'7Dma{col}ForState'] = round(df[f'7Dma{col}ForState'] / 1)
        df[f'7Dma{col}ForDistrict'] = round(df[f'7Dma{col}ForDistrict'] / 1)
    if df['7DmaTestedForState'].isnull().values.all():
        prev_date = (datetime.strptime(date, '%Y-%m-%d') - timedelta(1)).strftime("%Y-%m-%d")
        test_df = pd.read_csv(f'../RAWCSV/{prev_date}/{state}_final.csv')
        for dist in list(df['District']):
            if dist not in list(test_df['District']):
                test_df = test_df.append({
                    'District': dist,
                    '7DmaTestedForState': test_df['7DmaTestedForState'][0]
                }, ignore_index=True)
        test_df.sort_values('District', inplace=True)
        test_df.set_index('District', inplace=True, drop=False)
        df['7DmaTestedForState'] = test_df['7DmaTestedForState']
        df['7DmaTestedForDistrict'][df['District'] != 'Unknown'] = test_df['7DmaTestedForDistrict'][test_df['District'] != 'Unknown']
        
    try:
        day14 = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=14)
        day21 = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=21)
        df_14 = pd.read_csv("../RAWCSV/"+str(day14.date())+"/"+state+"_final.csv")
        df_21 = pd.read_csv("../RAWCSV/"+str(day21.date())+"/"+state+"_final.csv")
        # df = pd.read_csv("../RAWCSV/"+str(date)+"/"+state+"_final.csv")
        df["delta21_14confirmedForState"] = df_14["cumulativeConfirmedNumberForState"][0] - df_21["cumulativeConfirmedNumberForState"][0]
        # df["delta21_14confirmedForDistrict"] = df_14["cumulativeConfirmedNumberForDistrict"] - df_21["cumulativeConfirmedNumberForDistrict"]
        # print(df["delta21_14confirmedForDistrict"])
        # print(len(df_14["cumulativeConfirmedNumberForDistrict"] - df_21["cumulativeConfirmedNumberForDistrict"]),len(df["delta21_14confirmedForDistrict"]))
        for idx in df.index:
            try:
                # print(df["District"][idx])
                # print(day21)
                # print(day14)
                # print(df_14[df_14["District"] == df["District"][idx]]["cumulativeConfirmedNumberForDistrict"])
                # print(df_21[df_21["District"] == df["District"][idx]]["cumulativeConfirmedNumberForDistrict"].item())
                df["delta21_14confirmedForDistrict"][idx] = df_14[df_14["District"] == df["District"][idx]]["cumulativeConfirmedNumberForDistrict"].item()-df_21[df_21["District"] == df["District"][idx]]["cumulativeConfirmedNumberForDistrict"].item()
            except:
                pass
                # print(df["District"][idx]+" : District 14_21DMA Error")
    except:
        pass
    df.to_csv(f"../RAWCSV/{date}/{state}_final.csv", index=False)
    # print(df)
    # return df


def get_7dma(date):
    src = pd.read_csv("../sources.csv")
    for state in src['StateCode']:
        print(state)
        get_7dma_state(state, date)
        
states = ["PB"]

def date_range(start, end):
    r = (end+timedelta(days=1)-start).days
    return [start+timedelta(days=i) for i in range(r)]
 
    
# get_7dma("2022-01-25")

start_date = "2022-04-20"
end_date = "2022-04-20"
end = datetime.strptime(end_date, '%Y-%m-%d')
start = datetime.strptime(start_date, '%Y-%m-%d')
dateList = date_range(start, end)

# for date in dateList:
#     print(str(date.date()))
#     for state in states:
#         get_7dma_state(state, str(date.date()))

# get_7dma_state('ML', '2022-01-28')
# get_7dma_state('NL', '2022-03-26')
# get_7dma_state('CT', '2021-12-14')
# get_7dma_state('WB', '2021-10-31')
# get_7dma_state('RJ', '2022-08-08')
# get_7dma_state('ML', '2021-10-31')
# get_7dma_state('DL', '2022-07-27')
# get_7dma_state('PB', '2022-08-29')
# get_7dma_state('KL', '2022-09-03')
# get_7dma_state('MN', '2022-09-04')

# get_7dma_state('RJ', '2022-08-21')
# get_7dma_state('PB', '2022-10-06')
# get_7dma_state('UT', '2022-10-10')
# get_7dma_state('TN', '2022-10-24')
# get_7dma_state('BR', '2022-10-08')
# get_7dma_state('PB', '2022-10-18')
# get_7dma_state('RJ', '2022-10-29')


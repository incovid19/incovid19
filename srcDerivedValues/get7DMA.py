import pandas as pd
from datetime import datetime, timedelta

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)


def col_check_state_raw_csv(df):
    cols_ls = df.columns
    reqd_col_ls = [
        "Date", "State/UTCode", "deltaConfirmedForState", "deltaDeceasedForState", "deltaRecoveredForState",
        "deltaTestedForState", "deltaVaccinated1ForState", "deltaVaccinated2ForState", "delta21_14confirmedForState",
        "7DmaConfirmedForState", "7DmaDeceasedForState", "7DmaRecoveredForState", "7DmaTestedForState",
        "7DmaVaccinated1ForState", "7DmaVaccinated2ForState", "District", "deltaConfirmedForDistrict",
        "deltaDeceasedForDistrict", "deltaRecoveredForDistrict", "deltaTestedForDistrict",
        "deltaVaccinated1ForDistrict", "deltaVaccinated2ForDistrict", "delta21_14confirmedForDistrict",
        "7DmaConfirmedForDistrict", "7DmaDeceasedForDistrict", "7DmaRecoveredForDistrict", "7DmaTestedForDistrict",
        "7DmaVaccinated1ForDistrict", "7DmaVaccinated2ForDistrict", "districtPopulation",
        "tested_last_updated_district", "tested_source_district", "notesForDistrict",
        "cumulativeConfirmedNumberForDistrict", "cumulativeDeceasedNumberForDistrict",
        "cumulativeRecoveredNumberForDistrict", "cumulativeTestedNumberForDistrict",
        "cumulativeVaccinated1NumberForDistrict", "cumulativeVaccinated2NumberForDistrict", "last_updated",
        "statePopulation", "tested_last_updated_state", "tested_source_state", "notesForState",
        "cumulativeConfirmedNumberForState", "cumulativeDeceasedNumberForState", "cumulativeRecoveredNumberForState",
        "cumulativeTestedNumberForState", "cumulativeVaccinated1NumberForState", "cumulativeVaccinated2NumberForState"
    ]
    for col in reqd_col_ls:
        if col not in cols_ls:
            df[col] = 0
    df_formatted = df[reqd_col_ls]
    return df_formatted


def get_7dma_state(state, date):
    df = pd.read_csv(f'../RAWCSV/{date}/{state}_final.csv')
    cols = ['Confirmed', 'Deceased', 'Recovered', 'Tested', 'Vaccinated1', 'Vaccinated2']
    df = col_check_state_raw_csv(df)
    df.sort_values('District', inplace=True)
    df.reset_index(drop=True, inplace=True)
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
                'cumulativeVaccinated2NumberForState': prev_df['cumulativeVaccinated2NumberForState'][0]
            }, ignore_index=True)
    prev_df.sort_values('District', inplace=True)
    prev_df.reset_index(drop=True, inplace=True)
    for col in cols:
        df[f'7Dma{col}ForState'] -= prev_df[f'cumulative{col}NumberForState']
        df[f'7Dma{col}ForDistrict'] -= prev_df[f'cumulative{col}NumberForDistrict']
    for col in cols:
        df[f'7Dma{col}ForState'] = round(df[f'7Dma{col}ForState'] / 1)
        df[f'7Dma{col}ForDistrict'] = round(df[f'7Dma{col}ForDistrict'] / 1)
    df.to_csv(f"../RAWCSV/{date}/{state}_final.csv", index=False)
    # print(df)
    # return df


def get_7dma(date):
    src = pd.read_csv("../sources.csv")
    for state in src['StateCode']:
        print(state)
        get_7dma_state(state, date)

#get_7dma('2021-11-13')
# get_7dma_state('TT', '2021-10-31')
# get_7dma_state('TT', '2021-11-01')
# get_7dma_state('TT', '2021-11-02')
# get_7dma_state('TT', '2021-11-03')
# get_7dma_state('TT', '2021-11-04')
# get_7dma_state('TT', '2021-11-05')
# get_7dma_state('TT', '2021-11-06')
get_7dma_state('MN', '2021-10-31')


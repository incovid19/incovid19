import pandas as pd
from datetime import datetime, timedelta
from UpdateDerivedValues import col_check_state_raw_csv


def get_7dma_state(state, date):
    df = pd.read_csv(f'../RAWCSV/{date}/{state}_final.csv')
    df = col_check_state_raw_csv(df)
    df.sort_values('District', inplace=True)
    cols = ['Confirmed', 'Deceased', 'Recovered', 'Tested', 'Vaccinated1', 'Vaccinated2']
    for col in cols:
        df[f'7Dma{col}ForState'] = df[f'cumulative{col}NumberForState']
        df[f'7Dma{col}ForDistrict'] = df[f'cumulative{col}NumberForDistrict']
    for i in range(1, 7):
        prev_date = (datetime.strptime(date, "%Y-%m-%d") - timedelta(i)).strftime("%Y-%m-%d")
        prev_df = pd.read_csv(f'../RAWCSV/{prev_date}/{state}_final.csv')
        prev_df = col_check_state_raw_csv(prev_df)
        prev_df.sort_values('District', inplace=True)
        for col in cols:
            df[f'7Dma{col}ForState'] += prev_df[f'cumulative{col}NumberForState']
            df[f'7Dma{col}ForDistrict'] += prev_df[f'cumulative{col}NumberForDistrict']
    for col in cols:
        df[f'7Dma{col}ForState'] = round(df[f'7Dma{col}ForState'] / 7)
        df[f'7Dma{col}ForDistrict'] = round(df[f'7Dma{col}ForDistrict'] / 7)
    df.to_csv(f"../RAWCSV_7DMA/{state}_final.csv", index=False)
    #return df


def get_7dma(date):
    src = pd.read_csv("../sources.csv")
    for state in src['StateCode']:
        print(state)
        get_7dma_state(state, date)


# get_7dma('2021-11-10')

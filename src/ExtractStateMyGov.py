import pandas as pd
import json
import io
from datetime import datetime, timedelta

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def ExtractNoSource(df, state, date):
    STATE = state
    date = date - timedelta(1)
    cols = ['cumulativeConfirmedNumberForDistrict', 'cumulativeDeceasedNumberForDistrict', 'cumulativeRecoveredNumberForDistrict','cumulativeOtherNumberForDistrict']
    try:
        try:
            state = pd.read_csv(
                "../RAWCSV/" + date.strftime("%Y-%m-%d") + "/" + state + "_raw.csv",
                index_col=None,
                usecols=[
                    "District",
                    "cumulativeConfirmedNumberForDistrict",
                    "cumulativeDeceasedNumberForDistrict",
                    "cumulativeRecoveredNumberForDistrict",
                    "cumulativeOtherNumberForDistrict",
                    "cumulativeConfirmedNumberForState",
                    "cumulativeDeceasedNumberForState",
                    "cumulativeRecoveredNumberForState",
                    "cumulativeTestedNumberForState",
                    "cumulativeOtherNumberForState"
                ]
            )
            if STATE != "NL" and STATE != "TR":
                print("Yes")
                state["cumulativeOtherNumberForDistrict"] = 0
                state["cumulativeOtherNumberForState"] = 0
        except:
            # print(state)
            state = pd.read_csv(
                "../RAWCSV/" + date.strftime("%Y-%m-%d") + "/" + state + "_raw.csv",
                index_col=None,
                usecols=[
                    "District",
                    "cumulativeConfirmedNumberForDistrict",
                    "cumulativeDeceasedNumberForDistrict",
                    "cumulativeRecoveredNumberForDistrict",
                    "cumulativeConfirmedNumberForState",
                    "cumulativeDeceasedNumberForState",
                    "cumulativeRecoveredNumberForState",
                    "cumulativeTestedNumberForState",
                ]
            )
            state["cumulativeOtherNumberForDistrict"] = 0
            state["cumulativeOtherNumberForState"] = 0
        df["cumulativeTestedNumberForState"] = state["cumulativeTestedNumberForState"][0]
        try:
            df["cumulativeOtherNumberForState"] = state["cumulativeOtherNumberForState"][0]
            # df["cumulativeOtherNumberForState"] = 0
        except:
            pass
            # df["cumulativeOtherNumberForState"] = 0
        for district in list(state['District']):
            if district != 'Unknown':
                for col in cols:
                    try:
                        df[col][df['District'] == district] = int(state[col][state['District'] == district])
                    except:
                        df[col][df['District'] == district] = None

        for col in cols:
            df[col][df['District'] == "Unknown"] -= state[col.replace("District", "State")][0]
            
        if STATE == "HP":
            df["cumulativeDeceasedNumberForState"] = df["cumulativeDeceasedNumberForState"] - state["cumulativeOtherNumberForState"][0]
            df["cumulativeOtherNumberForState"] = state["cumulativeOtherNumberForState"][0]
        elif STATE == "NL"or STATE == "TR":
            df["cumulativeOtherNumberForState"] = state["cumulativeOtherNumberForState"][0]
            df["cumulativeRecoveredNumberForState"] = df["cumulativeRecoveredNumberForState"] - state["cumulativeOtherNumberForState"][0]

    except FileNotFoundError:
        df = ExtractNoSource(df, state, date)
    return df


def ExtractStateMyGov(state, date, no_source=False):
    print(state,date)
    states = json.load(io.open("../StateCode.json"))
    state_name = states[state]
    ind = pd.read_csv(
        "../RAWCSV/" + date + "/TT_raw.csv",
        index_col=None,
        usecols=[
            "District",
            "cumulativeConfirmedNumberForDistrict",
            "cumulativeDeceasedNumberForDistrict",
            "cumulativeRecoveredNumberForDistrict",
            "cumulativeTestedNumberForState",
            "last_updated",
        ]
    )

    state_df = pd.DataFrame()

    districts_data = json.load(io.open("../DistrictMappingMaster.json"))[state_name]
    districts = []

    for dist in districts_data.values():
        if dist not in districts:
            districts.append(dist)

    state_df["Date"] = [date] * len(districts)
    state_df["State/UTCode"] = [state] * len(districts)
    state_df["District"] = districts
    state_df['tested_last_updated_district'] = None
    state_df['tested_source_district'] = None
    state_df['notesForDistrict'] = None
    state_df['cumulativeConfirmedNumberForDistrict'] = None
    state_df['cumulativeDeceasedNumberForDistrict'] = None
    state_df['cumulativeRecoveredNumberForDistrict'] = None
    state_df['cumulativeTestedNumberForDistrict'] = None
    state_df["last_updated"] = ind["last_updated"][0]
    state_df['tested_last_updated_state'] = None
    state_df['tested_source_state'] = None
    state_df['notesForState'] = None
    # print(state_df)
    # print(ind)
    state_df["cumulativeConfirmedNumberForState"] = state_df['cumulativeConfirmedNumberForDistrict'][state_df['District'] == 'Unknown'] = int(ind["cumulativeConfirmedNumberForDistrict"][ind["District"].str.contains(state_name)].values[0])
    state_df["cumulativeDeceasedNumberForState"] = state_df['cumulativeDeceasedNumberForDistrict'][state_df['District'] == 'Unknown'] = int(ind["cumulativeDeceasedNumberForDistrict"][ind["District"].str.contains(state_name)].values[0])
    state_df["cumulativeRecoveredNumberForState"] = state_df['cumulativeRecoveredNumberForDistrict'][state_df['District'] == 'Unknown'] = int(ind["cumulativeRecoveredNumberForDistrict"][ind["District"].str.contains(state_name)].values[0])
    state_df['cumulativeTestedNumberForState'] = None#ind["cumulativeTestedNumberForState"]# * len(districts)
    state_df['cumulativeOtherNumberForState'] = 0
    state_df['cumulativeOtherNumberForDistrict'] = 0
    

    if no_source:
        state_df = ExtractNoSource(state_df, state, datetime.strptime(date, "%Y-%m-%d"))

    # state_df.to_csv("../RAWCSV/" + date + "/" + state + "_raw.csv", index=False)
    return state_df


# ExtractStateMyGov("AR", "2021-10-29", no_source=True)
# ExtractStateMyGov("NL", "2021-04-13",no_source=True)

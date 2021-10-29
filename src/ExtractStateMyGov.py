import pandas as pd
import json
import io


def ExtractStateMyGov(state, date):
    states = json.load(io.open("../StateCode.json"))
    state_name = states[state]
    ind = pd.read_csv(
        "../RAWCSV/" + date + "/IND_raw.csv",
        index_col=None,
        usecols=[
            "District",
            "cumulativeConfirmedNumberForDistrict",
            "cumulativeDeceasedNumberForDistrict",
            "cumulativeRecoveredNumberForDistrict",
            "last_updated",
        ]
    )

    state_df = pd.DataFrame()

    districts_data = json.load(io.open("../DistrictMappingMaster.json"))[state_name]
    districts = []

    for dist in districts_data.values():
        if dist not in districts:
            districts.append(dist)

    state_df["State/UTCode"] = [state_name] * len(districts)
    state_df["District"] = districts
    state_df["cumulativeConfirmedNumberForState"] = int(ind["cumulativeConfirmedNumberForDistrict"][ind["District"].str.contains(state_name)].values[0])
    state_df["cumulativeDeceasedNumberForState"] = int(ind["cumulativeDeceasedNumberForDistrict"][ind["District"].str.contains(state_name)].values[0])
    state_df["cumulativeRecoveredNumberForState"] = int(ind["cumulativeRecoveredNumberForDistrict"][ind["District"].str.contains(state_name)].values[0])
    state_df["last_updated"] = ind["last_updated"][ind["District"].str.contains(state_name)].values[0]
    state_df.to_csv("../RAWCSV/" + date + "/" + state + "_raw.csv", index=False)


ExtractStateMyGov("DN", "2021-10-26")

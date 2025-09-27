import requests
import pandas as pd

# this assignment requires the MOST RECENT version of tablur to function, please update it if you have an older version :3
from tablur import tablur


def tablify(df):
    try:
        return tablur(
            df,
            header=f"Returned Data from NHTSA API\nVin: {df.loc[df['Point'] == 'VIN', 'Value'].values[0]}",
            # make, model, year, trim (if TRIM applicable)
            footer=(
                f"Make: {df.loc[df['Point'] == 'Make', 'Value'].values[0] if ('Make' in df['Point'].values) else 'N/A'}\n"
                f"Model: {df.loc[df['Point'] == 'Model', 'Value'].values[0] if ('Model' in df['Point'].values) else 'N/A'}\n"
                f"Year: {df.loc[df['Point'] == 'ModelYear', 'Value'].values[0] if ('ModelYear' in df['Point'].values) else 'N/A'}\n"
                f"Trim: {df.loc[df['Point'] == 'Trim', 'Value'].values[0] if ('Trim' in df['Point'].values) else 'N/A'}\n"
                f"Total fields: {len(df)}"
            ),
        )
    except Exception:
        # If tablur fails (likely because the response is an error), return a readable string
        try:
            vin = df.loc[df["Point"] == "VIN", "Value"].values[0]
            err_code = df.loc[df["Point"] == "ErrorCode", "Value"].values[0]
            err_text = df.loc[df["Point"] == "ErrorText", "Value"].values[0]
            return f'\nVin number "{vin}" is invalid.\nError Code: {err_code}\nError Text: {err_text}\n'
        except Exception:
            # Fallback generic message
            return "\nInvalid VIN or unexpected response from NHTSA API.\n"


def getVinLookup(vin):
    x = requests.get(
        f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{vin}?format=json"
    )
    data = x.json()["Results"][0]
    # convert the single-result dict into a two-column DataFrame: Point, Value
    items = [(k, v) for k, v in data.items() if v != "" and v is not None]
    df = pd.DataFrame(items, columns=["Point", "Value"])

    # check if the vin is valid
    if (
        df.loc[df["Point"] == "ErrorCode", "Value"].values[0] != "0"
        and df.loc[df["Point"] == "ErrorCode", "Value"].values[0] != "1"
    ):
        # if not, return a formatted string (not a DataFrame)
        err_df = df[df["Point"].isin(["VIN", "ErrorCode", "ErrorText"])].set_index(
            "Point"
        )
        vin_val = err_df.loc["VIN", "Value"] if "VIN" in err_df.index else "N/A"
        err_code = (
            err_df.loc["ErrorCode", "Value"] if "ErrorCode" in err_df.index else "N/A"
        )
        err_text = (
            err_df.loc["ErrorText", "Value"] if "ErrorText" in err_df.index else "N/A"
        )
        return f'\nVin number "{vin_val}" is invalid.\nError Code: {err_code}\nError Text: {err_text}\n'

    # split the dataframe into multiple data frames for the general info, engine info, other info, and data points with the value "Not Applicable"
    not_applicable = df[df["Value"] == "Not Applicable"]
    general_info = df[df["Point"].isin(["VIN", "Make", "Model", "ModelYear", "Trim"])]
    # adds to the list if the Point contains "Engine", "Valve", "Transmission", or "Displacement" (case insensitive)
    engine_info = df[
        df["Point"].str.contains(
            "Engine|Valve|Transmission|Displacement|Fuel", case=False
        )
    ]
    other_info = df[
        ~df["Point"].isin(general_info["Point"])
        & ~df["Point"].isin(engine_info["Point"])
    ]

    # remove any rows with Point "ErrorCode" or "ErrorText" from other_info
    other_info = other_info[~other_info["Point"].isin(["ErrorCode", "ErrorText"])]

    # remove any duplicates that may exist between the dataframes (i.e. if xyz is in both general_info and engine_info, it should only be in general_info)
    not_applicable = not_applicable[
        ~not_applicable["Point"].isin(general_info["Point"])
    ]
    general_info = general_info[~general_info["Point"].isin(engine_info["Point"])]
    engine_info = engine_info[~engine_info["Point"].isin(general_info["Point"])]
    other_info = other_info[
        ~other_info["Point"].isin(general_info["Point"])
        & ~other_info["Point"].isin(engine_info["Point"])
        & ~other_info["Point"].isin(not_applicable["Point"])
    ]

    # concatenate the dataframes into a single dataframe with section headers
    df = pd.concat(
        [
            pd.DataFrame([["\nGeneral Info\n", ""]], columns=["Point", "Value"]),
            general_info,
            pd.DataFrame([["\nEngine Info\n", ""]], columns=["Point", "Value"]),
            engine_info,
            pd.DataFrame([["\nOther Info\n", ""]], columns=["Point", "Value"]),
            other_info,
            pd.DataFrame([["\nNot Applicable(s)\n", ""]], columns=["Point", "Value"]),
            not_applicable,
        ],
        ignore_index=True,
    )
    return tablify(df)

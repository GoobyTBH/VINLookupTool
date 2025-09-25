import requests
import pandas as pd
from tablur import tablur


def getVinLookup(vin):
    x = requests.get(
        f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{vin}?format=json"
    )
    data = x.json()["Results"][0]
    # convert the single-result dict into a two-column DataFrame: Point, Value
    items = [(k, v) for k, v in data.items() if v != "" and v is not None]
    df = pd.DataFrame(items, columns=["Point", "Value"])
    return df


# example usage:
# vin = "1HGCM82633A123456"
df = getVinLookup("1HGCM82633A123456")


def tablify(df):
    return tablur(
        df,
        header=f"Returned Data from NHTSA API\nVin: {df.loc[df['Point'] == 'VIN', 'Value'].values[0]}",
        # make, model, year, trim (if applicable)
        footer=f"Vehicle: {df.loc[df['Point'] == 'ModelYear', 'Value'].values[0]} {df.loc[df['Point'] == 'Make', 'Value'].values[0]} {df.loc[df['Point'] == 'Model', 'Value'].values[0]} {df.loc[df['Point'] == 'Trim', 'Value'].values[0]}",
    )


print(tablify(df))

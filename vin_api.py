import requests


def getVinLookup(vin):
    x = requests.get(
        f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{vin}?format=json"
    )
    return x.json()


example = getVinLookup("1HGCM82633A123456")["Results"][0]
print(example)

print(example["Make"])
print(example["Model"])
print(example["Trim"])
print(example["ModelYear"])

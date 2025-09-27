# VINLookupTool

A small utility to look up vehicle information from the NHTSA VPIC API using a VIN (Vehicle Identification Number). The project fetches decode results from the NHTSA API, converts the response into a two-column pandas DataFrame (Point, Value), and prints a friendly table using `tablur`.

## Features

- Lookup vehicle information by VIN using the NHTSA VPIC API
- Returns human-readable output formatted with `tablur` for valid VINs
- Returns a clear error string for invalid VINs

## Requirements

- Python 3.8+ (Python 3.10/3.11/3.12 recommended)
- requests
- pandas
- tablur (latest `1.3.3` recommended — older versions may behave differently)

## Install

Open PowerShell and (optionally) create and activate a virtual environment, then install dependencies:

```powershell
# optional: create venv
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# install dependencies
pip install --upgrade pip
pip install requests pandas tablur
```

If you prefer, you can pin versions or create a `requirements.txt` with the three packages.

## Usage

There are two simple ways to use the tool:

1. Run the interactive CLI in `main.py`:

```powershell
python main.py
```

Enter a VIN when prompted (or type `exit` to quit).

2. Import `getVinLookup` from `vin_api.py` in your Python code:

```python
from vin_api import getVinLookup

result = getVinLookup("1HGCM82633A123456")
print(result)
```

For valid VINs, the function returns a nicely formatted table (via `tablur`) showing rows with two columns: `Point` and `Value` (for example `Engine Type` / `Inline 4`). The table footer includes Make, Model, Year, Trim (if available) and a total field count.

For invalid VINs the function returns a plain, human-readable string describing the VIN and the API error code/text, for example:

```
Vin number "INVALIDVIN1234567" is invalid.
Error Code: 2
Error Text: VIN not found in record
```

## Notes & Troubleshooting

- If the `tablur` output looks wrong, make sure you have the latest `tablur` installed. The project expects the up-to-date API of that library.
- Network/API errors will raise exceptions from `requests`; you can wrap calls in try/except if you need to handle network failures specially.
- The tool filters out empty or null API values and groups common fields (general info, engine info, other info, not applicable).

## License

This repository does not include a license file. :3

## Contact / Contributions

Feel free to open issues or submit PRs to improve behavior, add tests, or include a `requirements.txt` and CI.

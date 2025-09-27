from vin_api import getVinLookup


def main():
    vin = input("Enter a VIN number (or 'exit' to quit): ").strip().upper()
    while vin.lower() != "exit":
        result = getVinLookup(vin)
        print(result)
        vin = input("Enter another VIN number (or 'exit' to quit): ").strip().upper()


if __name__ == "__main__":
    main()

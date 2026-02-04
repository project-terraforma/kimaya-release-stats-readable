# calls parseFile given a file (.csv) and returns the out to out.txt
# repeats calls for every .csv file in my_data folder and appends the out to out.txt
# checks if out.txt exists, if so, deletes it before writing new data

# imports
# main.py

import os
from parseFile import parseFile

DATA_DIR = "my_data"
OUT_FILE = "out.txt"


def main():
    # Delete out.txt if it exists
    if os.path.exists(OUT_FILE):
        os.remove(OUT_FILE)

    # Process each CSV file
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            csv_path = os.path.join(DATA_DIR, file)
            parseFile(csv_path, OUT_FILE)


if __name__ == "__main__":
    main()

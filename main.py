# calls parseFile given a file (.csv) and returns the out to out.txt
# repeats calls for every .csv file in my_data folder and appends the out to out.txt
# checks if out.txt exists, if so, deletes it before writing new data

# imports
# main.py

import os
from parseFile import parseFile
#from pinecone import Pinecone
import config
from metrics_cleaner import clean_metrics

# Use API key from config.py (set PINECONE_API in that file)
# Pinecone related calls commented out for local testing of cleaner
# pc = Pinecone(api_key=config.PINECONE_API)
# index = pc.Index("quickstart")

DATA_DIR = "my_data"
OUT_FILE = "out.txt"


def main():
    # Clean metrics CSVs before any other processing
    try:
        clean_metrics()
    except Exception:
        pass
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

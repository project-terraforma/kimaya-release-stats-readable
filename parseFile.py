# takes in .csv file and parses data into LLM readable txt file
# stores theme-specific column definitions 
# calls contGen to generate context for data --> add context to out.txt

# parseFile.py

import csv
import os
from contextGen import generate_context


def parseFile(csv_path: str, out_path: str):
    """Parses a CSV file and appends LLM-readable output to out.txt"""

    theme = os.path.splitext(os.path.basename(csv_path))[0]

    with open(out_path, "a", encoding="utf-8") as out_file:
        # Add context
        context = generate_context(theme)
        if context:
            out_file.write(context)

        # Read CSV
        with open(csv_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)

            for i, row in enumerate(reader, start=1):
                out_file.write(f"Record {i}:\n")
                for key, value in row.items():
                    out_file.write(f"{key}: {value}\n")
                out_file.write("\n")

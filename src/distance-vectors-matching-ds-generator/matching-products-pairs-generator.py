'''
This script generates an output CSV file with the following fields:
    - ProductTitle1
    - ProductTitle2
    - ProductPrice1
    - ProductPrice2
    - ProductCurrency1
    - ProductCurrency2
    - Match (values = { YES / NO })
'''

import pandas as pd

INPUT_FILEPATH = "../_data/Smartphones.csv"
OUTPUT_FILEPATH = "../_data/MATCHING_PRODUCTS_PAIRS.csv"

# Data load
fields = ["Title", "Price", "Currency", "MatchingID"]
df = pd.read_csv(INPUT_FILEPATH, usecols=fields)

# Set data types
df = df.astype({
    "Title": str,
    "Price": float,
    "Currency": str,
    "MatchingID": str
})

# Remove duplicates by title
df = df.drop_duplicates(subset="Title")

print("Number of rows: {}".format(df.shape[0]))
print("Number of cols: {}".format(df.shape[1]))

df_join_by_matching_id = df.join(df, on="MatchingID", how="inner", lsuffix="_l", rsuffix="_r")

print(df_join_by_matching_id.head())

# Generate matching pairs

# Generate non-matching pairs

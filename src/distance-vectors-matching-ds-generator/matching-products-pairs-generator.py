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
import numpy as np
import random

INPUT_FILEPATH = "../_data/Smartphones.csv"
OUTPUT_FILEPATH = "../_data/MATCHING_PRODUCTS_PAIRS.csv"

KNOWN_SMARTPHONES_BRANDS = ["Acer","Apple","Asus","BlackBerry","Bosch","BQ",
    "Coolpad","Emporia","Energizer","Google","Haier","HTC","Huawei",
    "Lenovo","LG","Meizu","Microsoft","Motorola","Nokia","Philips","Prestigio",
    "Samsung","Sharp","Siemens","Sony Ericson","T-Mobile","Vodafone","Wiko","Xiaomi",
    "ZTE"]

OUTPUT_COLS_NAMES = ["ProductTitle1", "ProductTitle2", "ProductPrice1",
    "ProductPrice2", "ProductCurrency1", "ProductCurrency2", "Match"] 

CSV_OUTPUT_FILE_SEP = "\t"

# Data load
fields = ["Brand", "Title", "Price", "Currency", "MatchingID"]
df = pd.read_csv(INPUT_FILEPATH, usecols=fields)

# Set data types
df = df.astype({
    "Brand": str,
    "Title": str,
    "Price": float,
    "Currency": str,
    "MatchingID": str
})

# Remove duplicates by title
df = df.drop_duplicates(subset="Title")

# Remove products with unknown smartphones brands (in order to discard
# products which are not smartphones)
df = df[df["Brand"].isin(KNOWN_SMARTPHONES_BRANDS)]

print("\nDataframe loaded.")
print("Number of rows: {}".format(df.shape[0]))
print("Number of cols: {}".format(df.shape[1]))

df_join_by_matching_id = df.merge(df, on="MatchingID", how="inner")

# Generate matching pairs
df_match = df_join_by_matching_id

print("\nMatching products pairs generated.")
print(df_match.head())
print("Number of rows: {}".format(df_match.shape[0]))
print("Number of cols: {}".format(df_match.shape[1]))

# Generate non-matching pairs
matchingIDs = list(set(df["MatchingID"].tolist()))
no_matching_pairs = []

for i in range(100000):
    random_matching_id_idx_1 = random.randint(0, len(matchingIDs) - 1)
    random_matching_id_idx_2 = random.randint(0, len(matchingIDs) - 1)

    if random_matching_id_idx_1 != random_matching_id_idx_2:
        random_matching_id_1 = matchingIDs[random_matching_id_idx_1]
        random_matching_id_2 = matchingIDs[random_matching_id_idx_2]
        
        # Get lists of indexes of rows that contain chosen MatchingIDs
        matching_id_row_indexes_1 = np.where(df["MatchingID"] == random_matching_id_1)[0]
        matching_id_row_indexes_2 = np.where(df["MatchingID"] == random_matching_id_2)[0]

        # Find two product with the the chosen MatchingIDs
        first_product = df.iloc[random.choice(matching_id_row_indexes_1)].to_dict()
        second_product = df.iloc[random.choice(matching_id_row_indexes_2)].to_dict()
       
        # Add non-matching pair to dict
        no_matching_pairs.append((first_product, second_product))

print("\nNon-matching products pairs generated.")
print("Number of pairs: {}".format(len(no_matching_pairs)))

# Export training dataset to CSV file
with open(OUTPUT_FILEPATH, "w+", encoding="utf-8") as f:
    
    # Write column names
    f.write(CSV_OUTPUT_FILE_SEP.join(OUTPUT_COLS_NAMES) + "\n")

    # Write matching products pairs
    for i, row in df_match.iterrows():
        f.write(
            row["Title_x"] + CSV_OUTPUT_FILE_SEP
            + row["Title_y"] + CSV_OUTPUT_FILE_SEP
            + str(row["Price_x"]) + CSV_OUTPUT_FILE_SEP
            + str(row["Price_y"]) + CSV_OUTPUT_FILE_SEP
            + row["Currency_x"] + CSV_OUTPUT_FILE_SEP
            + row["Currency_y"] + CSV_OUTPUT_FILE_SEP
            + "MATCH\n"
        )

    # Write non-matching products pairs
    for pair in no_matching_pairs:
        p1 = pair[0]
        p2 = pair[1]

        f.write(
            p1["Title"] + CSV_OUTPUT_FILE_SEP
            + p2["Title"] + CSV_OUTPUT_FILE_SEP
            + str(p1["Price"]) + CSV_OUTPUT_FILE_SEP
            + str(p2["Price"]) + CSV_OUTPUT_FILE_SEP
            + p1["Currency"] + CSV_OUTPUT_FILE_SEP
            + p2["Currency"] + CSV_OUTPUT_FILE_SEP
            + "UNMATCH\n"
        )

print("Dataset exported to {}.".format(OUTPUT_FILEPATH))

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
from random import randint

INPUT_FILEPATH = "../_data/Smartphones.csv"
OUTPUT_FILEPATH = "../_data/MATCHING_PRODUCTS_PAIRS.csv"

KNOWN_SMARTPHONES_BRANDS = ["Acer","Apple","Asus","BlackBerry","Bosch","BQ",
    "Coolpad","Emporia","Energizer","Google","Haier","HTC","Huawei",
    "Lenovo","LG","Meizu","Microsoft","Motorola","Nokia","Philips","Prestigio",
    "Samsung","Sharp","Siemens","Sony Ericson","T-Mobile","Vodafone","Wiko","Xiaomi",
    "ZTE"]

OUTPUT_COLS_NAMES = ["ProductTitle1", "ProductTitle2", "ProductPrice1",
    "ProductPrice2", "ProductCurrency1", "ProductCurrency2", "Match"] 

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

print("Number of rows: {}".format(df.shape[0]))
print("Number of cols: {}".format(df.shape[1]))

df_join_by_matching_id = df.merge(df, on="MatchingID", how="inner")

print(df_join_by_matching_id.head())

# Generate matching pairs
df_match = df_join_by_matching_id

# Generate non-matching pairs
matchingIDs = list(set(df_join_by_matching_id["MatchingID"].tolist()))
df_no_match = df.Dataframe()

for i in range(len(10000)):
    random_idx_1 = randint(0, len(matchingIDs) - 1)
    random_idx_2 = randint(0, len(matchingIDs) - 1)

    if random_idx_1 != random_idx_2:
        random_matching_id_1 = matchingIDs[random_idx_1]
        random_matching_id_2 = matchingIDs[random_idx_2]

        

# Export training dataset to CSV file
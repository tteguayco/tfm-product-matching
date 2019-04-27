'''
This script generates an output CSV file with the following fields:
    - Brand1Distance
    - Brand2Distance
    - Model1Distance
    - Model2Distance
    - Model3Distance
    - RAMMemoryDistance
    - ColorDistance
    - PriceDistance

For string attributes, distances are calculated using Levenshtein distance:
https://en.wikipedia.org/wiki/Levenshtein_distance.

For numerical attributes, distances are the absolute value of the substractions. 
'''

import pandas as pd
import joblib

MATCHING_PRODUCT_PAIRS_FILEPATH = "../_data/MATCHING_PRODUCTS_PAIRS.csv"
CRF_MODEL_FILEPATH = "../_models/crf_smartphones.joblib"

# Load CRF model
crf_model = joblib.load(CRF_MODEL_FILEPATH)

# Load data
df = pd.read_csv(MATCHING_PRODUCT_PAIRS_FILEPATH, sep="\t")
df = df.drop_duplicates()

print("Data loaded.")
print("Number of rows: {}".format(df.shape[0]))
print("Number of cols: {}".format(df.shape[1]))



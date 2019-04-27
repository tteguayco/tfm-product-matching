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
import numpy as np
import joblib
import distance
import re
import sys

sys.path.append('../common')
import crf_utils

MATCHING_PRODUCT_PAIRS_FILEPATH = "../_data/MATCHING_PRODUCTS_PAIRS.csv"
CRF_MODEL_FILEPATH = "../_models/crf_smartphones.joblib"

CHF_TO_EUR_FACTOR = 0.88

class StructuredProductFeatures():
    def __init__(self):
        self.brand1 = ""
        self.brand2 = ""
        self.model1 = ""
        self.model2 = ""
        self.model3 = ""
        self.gb_ram = ""
        self.color = ""
        self.eur_price = ""

    def __str__(self):
        return str(self.__dict__)


def get_product_features(crf_model, title, price, currency):
    product_features = StructuredProductFeatures()

    # Predict labels with CRF model
    splitted_title = title.split()
    title_featured = crf_utils.title2features(splitted_title)
    title_pred_labels = crf_model.predict_single(title_featured)

    b_brand_idx_list = np.where(title_pred_labels == "B-BRAND")[0]
    i_brand_idx_list = np.where(title_pred_labels == "I-BRAND")[0]
    b_model_idx_list = np.where(title_pred_labels == "B-MODEL")[0]
    i_model_idx_list = np.where(title_pred_labels == "I-MODEL")[0]
    b_ram_idx_list = np.where(title_pred_labels == "B-RAM")[0]
    i_ram_idx_list = np.where(title_pred_labels == "I-RAM")[0]
    b_color_idx_list = np.where(title_pred_labels == "B-COLOR")[0]

    # Feature BRAND
    product_features.brand1 = splitted_title[b_brand_idx_list[0]] if len(b_brand_idx_list) > 0 else ""
    product_features.brand2 = splitted_title[i_brand_idx_list[0]] if len(i_brand_idx_list) > 0 else ""

    # Feature MODEL
    product_features.model1 = splitted_title[b_model_idx_list[0]] if len(b_model_idx_list) > 0 else ""
    product_features.model2 = splitted_title[i_model_idx_list[0]] if len(i_model_idx_list) > 0 else ""
    product_features.model3 = splitted_title[i_model_idx_list[1]] if len(i_model_idx_list) > 1 else ""

    # Feature RAM
    b_ram = splitted_title[b_ram_idx_list[0]] if len(b_ram_idx_list) > 0 else ""
    i_ram = splitted_title[i_ram_idx_list[0]] if len(i_ram_idx_list) > 0 else ""

    if "GB" in b_ram or "GB" == i_ram.strip():
        product_features.gb_ram = "".join(re.findall("\d+", b_ram))

    # Feature COLOR
    product_features.color = splitted_title[b_color_idx_list[0]] if len(b_color_idx_list) > 0 else ""

    # Feature PRICE
    price = float(price)
    currency = currency.lower()

    if currency == "eur":
        product_features.eur_price = price
    elif currency == "chf":
        product_features.eur_price = price * CHF_TO_EUR_FACTOR

    return product_features


def calculate_string_similarity_perc(string1, string2):
    string1 = string1.lower()
    string2 = string2.lower()

    lev_distance = distance.levenshtein(string1, string2)
    bigger_len = max(len(string1), len(string2))
    perc = (bigger_len - lev_distance) / bigger_len

    return round(perc, 2)


# Load CRF model
crf_model = joblib.load(CRF_MODEL_FILEPATH)

# Load data with no duplicates
df = pd.read_csv(MATCHING_PRODUCT_PAIRS_FILEPATH, sep="\t")
df = df.drop_duplicates()

print("Data loaded.")
print("Number of rows: {}".format(df.shape[0]))
print("Number of cols: {}".format(df.shape[1]))

print(get_product_features(crf_model, "Apple iPhone 4S Smartphone - Black", 128.9, "EUR"))

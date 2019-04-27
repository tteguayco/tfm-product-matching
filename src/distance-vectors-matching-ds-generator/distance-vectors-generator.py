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
import math
import csv
import time

sys.path.append('../common')
import crf_utils

MATCHING_PRODUCT_PAIRS_FILEPATH = "../_data/MATCHING_PRODUCTS_PAIRS.csv"
CRF_MODEL_FILEPATH = "../_models/crf_smartphones.joblib"
MATCHING_DISTANCE_VECTORS_OUTPUT_FILEPATH = "../_data/MATCHING_DISTANCE_VECTORS.csv"

CHF_TO_EUR_FACTOR = 0.88

class StructuredProductFeatures():
    def __init__(self):
        self.brand1 = ""
        self.brand2 = ""
        self.brand3 = ""
        self.model1 = ""
        self.model2 = ""
        self.model3 = ""
        self.model4 = ""
        self.gb_ram = float("-inf")
        self.color = ""
        self.eur_price = float("-inf")

    def __str__(self):
        return str(self.__dict__)

def get_feature_val(splitted_title, pred_labels, label2find, index):
    feature_val = ""

    if len(splitted_title) != len(pred_labels):
        raise ValueError("Number of words in title and labels are not the same")

    indexes_list = [i for i, s in enumerate(pred_labels) if label2find.lower() == s.lower()]
    
    if len(indexes_list) > index:
        feature_val = splitted_title[indexes_list[index]]

    return feature_val
    

def get_product_features(crf_model, title, price, currency):
    product_features = StructuredProductFeatures()

    # Predict labels with CRF model
    splitted_title = title.split()
    title_featured = crf_utils.title2features(splitted_title)
    title_pred_labels = crf_model.predict_single(title_featured)

    # Feature BRAND
    product_features.brand1 = get_feature_val(splitted_title, title_pred_labels, "B-BRAND", 0)
    product_features.brand2 = get_feature_val(splitted_title, title_pred_labels, "I-BRAND", 0)
    product_features.brand3 = get_feature_val(splitted_title, title_pred_labels, "I-BRAND", 1)

    # Feature MODEL
    product_features.model1 = get_feature_val(splitted_title, title_pred_labels, "B-MODEL", 0)
    product_features.model2 = get_feature_val(splitted_title, title_pred_labels, "I-MODEL", 0)
    product_features.model3 = get_feature_val(splitted_title, title_pred_labels, "I-MODEL", 1)
    product_features.model4 = get_feature_val(splitted_title, title_pred_labels, "I-MODEL", 2)

    # Feature RAM
    b_ram = get_feature_val(splitted_title, title_pred_labels, "B-RAM", 0)
    i_ram = get_feature_val(splitted_title, title_pred_labels, "I-RAM", 0)

    try:
        if "GB" in b_ram or "GB" == i_ram.strip():
            product_features.gb_ram = float("".join(re.findall("\d+", b_ram)))
    except ValueError:
        product_features.gb_ram = float("-inf")

    # Feature COLOR
    product_features.color = get_feature_val(splitted_title, title_pred_labels, "B-COLOR", 0)

    # Feature PRICE
    price = float(price)
    currency = currency.lower()

    if currency == "eur":
        product_features.eur_price = price
    elif currency == "chf":
        product_features.eur_price = price * CHF_TO_EUR_FACTOR

    return product_features


def get_string_similarity_perc(string1, string2):
    string1 = string1.lower()
    string2 = string2.lower()

    lev_distance = distance.levenshtein(string1, string2)
    bigger_len = max(len(string1), len(string2))

    try:
        perc = (bigger_len - lev_distance) / bigger_len
    except ZeroDivisionError:
        perc = 0.0

    return round(perc, 2)


def get_distance_vector(product1_features, product2_features):
    if not isinstance(product1_features, StructuredProductFeatures) or \
        not isinstance(product2_features, StructuredProductFeatures):
        raise ValueError("Provided object are not instances of StructuredProductFeatures class")

    distance_vector = []
    attributes_list = product1_features.__dict__.keys()

    for attr in attributes_list:
        attr_product1 = getattr(product1_features, attr)
        attr_product2 = getattr(product2_features, attr)

        dist = ""

        if isinstance(attr_product1, float) and isinstance(attr_product2, float):
            dist = round(abs(attr_product1 - attr_product2), 2)
            if math.isnan(dist) or math.isinf(dist):
                dist = 1000000.0

        elif isinstance(attr_product1, str) and isinstance(attr_product2, str):
            # Empty string is not allowed: similarity with an empty string will
            # be the greatest possible
            if len(attr_product1) <= 0 or len(attr_product2) <= 0:
                dist = 0.0
            else: 
                dist = get_string_similarity_perc(attr_product1, attr_product2)

        distance_vector.append(dist)

    return distance_vector

if __name__ == "__main__":

    start_time = time.time()

    # Load CRF model
    crf_model = joblib.load(CRF_MODEL_FILEPATH)

    # Load data with no duplicates
    df = pd.read_csv(MATCHING_PRODUCT_PAIRS_FILEPATH, sep="\t")
    df = df.drop_duplicates()

    print("Data loaded.")
    print("Number of rows: {}".format(df.shape[0]))
    print("Number of cols: {}".format(df.shape[1]))

    # Calculate distance vectors
    labeled_distance_vectors = []
    for index, row in df.iterrows():
        match = row["Match"]
        product1 = get_product_features(crf_model, row["ProductTitle1"], row["ProductPrice1"], row["ProductCurrency1"])
        product2 = get_product_features(crf_model, row["ProductTitle2"], row["ProductPrice2"], row["ProductCurrency2"])

        #print(product1)
        #print(product2)

        distance_vector = get_distance_vector(product1, product2)
        labeled_distance_vectors.append((distance_vector, match))

    # Export dataset to file
    with open(MATCHING_DISTANCE_VECTORS_OUTPUT_FILEPATH, "w", newline="") as f:
        csv_writer = csv.writer(f, delimiter=",")

        # Headers
        headers = [attrname.upper() for attrname in list(product1.__dict__.keys())]
        headers.append("MATCH")
        csv_writer.writerow(headers)

        # Distances and label rows
        for v in labeled_distance_vectors:
            distances = v[0]
            match_label = v[1]
            distances.append(match_label)
            csv_writer.writerow(distances)

    print("Dataset exported to {}.".format(MATCHING_DISTANCE_VECTORS_OUTPUT_FILEPATH))

    finish_time = time.time()
    elapsed_time = round(finish_time - start_time, 2)
    print("Process finished. Took {} seconds.".format(elapsed_time))

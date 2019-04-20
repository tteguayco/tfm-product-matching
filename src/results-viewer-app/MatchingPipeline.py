from joblib import load
import json
import numpy as np
import pandas as pd
import sys

sys.path.append('../common')
import crf_utils

CRF_MODEL_FILEPATH = "../_models/crf_smartphones.joblib"
KNN_MODEL_FILEPATH = "../_models/knn_smartphones.joblib"
OHE_MODEL_FILEPATH = "../_models/ohe.joblib"

class MatchingPipeline():

    def __init__(self):
        self.crf = load(CRF_MODEL_FILEPATH)
        self.knn = load(KNN_MODEL_FILEPATH)
        self.ohe = load(OHE_MODEL_FILEPATH)

    def get_features_from_crf(self, title):
        cleaned_title = title # TODO preprocess product title
        splitted_title = cleaned_title.split()

        title_featured = crf_utils.title2features(splitted_title)

        # Predict product features using pre-trained CRF model
        pred_labels = self.crf.predict_single(title_featured)

        return splitted_title, pred_labels

    def get_parsed_product_features(self, prod_title, labels):
        prod_features = {}

        if len(prod_title) != len(labels):
            ValueError("Provided lists of features and labels must have the same length")

        # Collecting relevant features
        for i in range(len(prod_title)):
            word = prod_title[i]
            label = labels[i][2:]

            if label != "O":
                if label not in prod_features:
                    prod_features[label] = []
                prod_features[label].append(word)

        # Join lists of strings as an only string
        for key in prod_features:
            prod_features[key] = " ".join(prod_features[key])
            prod_features[key] = prod_features[key].strip()

        return prod_features

    def get_pred_matching_code(self, features, price, currency):
        df = pd.DataFrame(columns=["Brand", "Model", "Price", "Currency", "Color"])
        df.loc[0] = [
            features["BRAND"] if "BRAND" in features else "",
            features["MODEL"] if "MODEL" in features else "",
            price,
            currency,
            features["COLOR"] if "COLOR" in features else "",
        ]
        
        encoded_prod_features = self.ohe.transform(df)

        knn_res = self.knn.predict(encoded_prod_features)

        return knn_res

    def get_matching_result(self, title, price, currency):
        prod_title, pred_labels = self.get_features_from_crf(title)
        parsed_features_from_title = self.get_parsed_product_features(prod_title, pred_labels)

        print(parsed_features_from_title)

        pred_matching_code = self.get_pred_matching_code(parsed_features_from_title, price, currency)
        print(pred_matching_code)


if __name__ == "__main__":
    product_title = "apple iphone 4s 4g 64gb blue"

    matchingPipeline = MatchingPipeline()
    matchingPipeline.get_matching_result(product_title, 500.0, "EUR")

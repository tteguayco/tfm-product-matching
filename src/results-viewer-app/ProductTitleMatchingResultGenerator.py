from joblib import load
import json

CRF_MODEL_FILEPATH = "../_models/crf_smartphones.joblib"
KNN_MODEL_FILEPATH = "../_models/knn_smartphones.joblib"

class ProductTitleMatchingResultGenerator():

    def __init__(self):
        self.crf = load(CRF_MODEL_FILEPATH)
        self.knn = load(KNN_MODEL_FILEPATH)

    def get_matching_results(self, product_title):
        result = {}
        splitted_title = product_title.split()
        title_pred_labels = self.crf.predict(splitted_title)[0]

        b_brand_idx = [i for i in range(len(title_pred_labels)) if 'B-BRAND' in title_pred_labels[i]]
        i_brand_idx = [i for i in range(len(title_pred_labels)) if 'I-BRAND' in title_pred_labels[i]]
        b_model_idx = [i for i in range(len(title_pred_labels)) if 'B-MODEL' in title_pred_labels[i]]
        i_model_idx = [i for i in range(len(title_pred_labels)) if 'I-MODEL' in title_pred_labels[i]]
        b_color_idx = [i for i in range(len(title_pred_labels)) if 'B-COLOR' in title_pred_labels[i]]

        b_brand = [splitted_title[i] for i in range(len(splitted_title)) if i in b_brand_idx]
        i_brand = [splitted_title[i] for i in range(len(splitted_title)) if i in i_brand_idx]
        b_model = [splitted_title[i] for i in range(len(splitted_title)) if i in b_model_idx]
        i_model = [splitted_title[i] for i in range(len(splitted_title)) if i in i_model_idx]
        b_color = [splitted_title[i] for i in range(len(splitted_title)) if i in b_color_idx]

        features = {}

        if len(b_brand) > 0: features["B-BRAND"] = b_brand
        if len(i_brand) > 0: features["I-BRAND"] = i_brand
        if len(b_model) > 0: features["B-MODEL"] = b_model
        if len(i_model) > 0: features["I-MODEL"] = i_model
        if len(b_color) > 0: features["B-COLOR"] = b_color

        # Create result as JSON object
        result["features"] = json.dumps(features)

        return result


if __name__ == "__main__":
    product_title = "Apple iPhone 4 8GB SIM-Free - Black"

    matchingResultGenerator = ProductTitleMatchingResultGenerator()
    res = matchingResultGenerator.get_matching_results(product_title)
    print(res)

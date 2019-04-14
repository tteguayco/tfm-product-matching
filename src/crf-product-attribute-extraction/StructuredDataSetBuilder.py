import pandas as pd
import time
import os

from joblib import load
import sklearn_crfsuite
import utils


class StructuredDatasetBuilder:

    def __init__(self, crf_model_path, titles, prices, currencies, matching_codes, limit=0):
        # CRF Model
        self.crf = load(crf_model_path)

        # Already existing product data attributes
        self.titles = titles
        self.prices = prices
        self.currencies = currencies
        self.matching_codes = matching_codes

        self.products_limit = limit
        self.structured_data_set = None

        self.preprocess_titles()

        if len(self.titles) != len(self.prices) or len(self.titles) != len(self.matching_codes):
            raise ValueError("Provided lists of titles, prices and matching codes do not have the same length")

    def preprocess_titles(self):
        self.titles = utils.preprocess(self.titles, with_rows_removal=False)

    def start(self):
        col_names = ["Title", "Brand", "Model", "Price", "Currency", "Color", "MatchingCode"]
        self.structured_data_set = pd.DataFrame(columns=col_names)
        titles_to_process = self.titles[:self.products_limit] if self.products_limit > 0 else self.titles

        for i, title in enumerate(titles_to_process):
            splitted_title = title.split()
            title_labels = self.crf.predict([splitted_title])[0]

            brand = ""
            model = ""
            color = ""

            if len(splitted_title) == len(title_labels):
                for j, label in enumerate(title_labels):
                    if "-BRAND" in label:
                        brand += splitted_title[j] + " "
                    elif "-MODEL" in label:
                        model += splitted_title[j] + " "
                    elif "-COLOR" in label:
                        color += splitted_title[j] + " "

            brand = brand.strip()
            model = model.strip()
            color = color.strip()
            price = self.prices[i]
            currency = self.currencies[i]
            matching_code = self.matching_codes[i]

            # Add instance to the dataset
            self.structured_data_set.loc[len(self.structured_data_set)] = [
                title,
                brand,
                model,
                price,
                currency,
                color,
                matching_code,]

    def print_builder_summary(self):
        print("  - Number of titles: {}".format(len(self.titles)))
        print("  - Number of prices: {}".format(len(self.prices)))
        print("  - Number of matching codes: {}".format(len(self.matching_codes)))

    def print_structured_data_set_summary(self):
        if self.structured_data_set is None:
            print("  - Structured data set is empty. It seems the method start() has not been run yet.")
        else:
            print("  - Number of structured products: {}".format(self.structured_data_set.shape[0]))
            print("  - Number of extracted attributes: {}".format(self.structured_data_set.shape[1]))
            print("  - List of extracted attributes: {}".format(self.structured_data_set.columns.values))

    def export_data_to_csv(self, output_path):
        if self.structured_data_set is not None:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            self.structured_data_set.to_csv(output_path, sep=',', encoding='utf-8', index=False)


if __name__ == '__main__':

    CRF_MODEL_PATHFILE = "./out/models/crf.joblib"
    SMARTPHONES_DATASET_FILEPATH = "../../data/Smartphones.csv"
    SMARTPHONES_DATASET_COLS = ["Name", "Price", "Currency", "Color", "MatchingID"]
    STRUCTURED_DATASET_OUTPUT_FILEPATH = "./out/data/StructuredSmartPhonesDataset.csv"

    df = pd.read_csv(SMARTPHONES_DATASET_FILEPATH, usecols=SMARTPHONES_DATASET_COLS)

    product_titles = df["Name"].astype(str).values.tolist()
    product_prices = df["Price"].astype(float).values.tolist()
    product_currencies = df["Currency"].astype(str).values.tolist()
    product_matching_codes = df["MatchingID"].astype(str).values.tolist()

    # Start structured data set building
    structuredDatasetBuilder = StructuredDatasetBuilder(crf_model_path=CRF_MODEL_PATHFILE,
                                                        titles=product_titles,
                                                        prices=product_prices, 
                                                        currencies=product_currencies,
                                                        matching_codes=product_matching_codes, 
                                                        limit=50000)

    print("\nSummary:")

    structuredDatasetBuilder.print_builder_summary()

    print("\nStarting building of structured dataset")

    start_time = time.time()
    structuredDatasetBuilder.start()
    elapsed_time = round(time.time() - start_time, 3)

    print("\nBuilding of structured dataset finished. Elapsed time (s): {}".format(elapsed_time))
    print("\nSummary:")

    structuredDatasetBuilder.print_structured_data_set_summary()

    print()

    structuredDatasetBuilder.export_data_to_csv(STRUCTURED_DATASET_OUTPUT_FILEPATH)

    print("Structured dataset exported to file.")

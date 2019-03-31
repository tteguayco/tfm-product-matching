import utils
import pandas as pd
import pycrfsuite
import time
import os


class StructuredDataSetBuilder:

    def __init__(self, crf_model_path, titles, prices, matching_codes, limit=0):
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(crf_model_path)

        self.titles = titles
        self.prices = prices
        self.matching_codes = matching_codes

        self.products_limit = limit
        self.structured_data_set = None

        self.preprocess_titles()
        self.preprocess_prices()
        self.preprocess_matching_codes()

        if len(self.titles) != len(self.prices) or len(self.titles) != len(self.matching_codes):
            raise ValueError("Provided lists of titles, prices and matching codes do not have the same length")

    def preprocess_titles(self):
        self.titles = utils.preprocess(self.titles, with_rows_removal=False)

    def preprocess_prices(self):
        pass

    def preprocess_matching_codes(self):
        pass

    def start(self):

        col_names = ['Brand', 'Model', 'Price', 'MatchingCode', 'OriginalTitle']
        self.structured_data_set = pd.DataFrame(columns=col_names)
        titles_to_process = self.titles[:self.products_limit] if self.products_limit > 0 else self.titles

        for i, title in enumerate(titles_to_process):
            splitted_title = title.split()
            title_labels = self.tagger.tag(splitted_title)

            brand = ''
            model = ''

            if len(splitted_title) == len(title_labels):
                for j, label in enumerate(title_labels):
                    if '-BRAND' in label:
                        brand += splitted_title[j] + ' '
                    elif '-MODEL' in label:
                        model += splitted_title[j] + ' '

            brand = brand.strip()
            model = model.strip()
            price = self.prices[i]
            matching_code = self.matching_codes[i]

            # Add instance to the data set
            self.structured_data_set.loc[len(self.structured_data_set)] = [
                brand,
                model,
                price,
                matching_code,
                title]

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

    FINAL_DATA_SET_PATH = '../../RawData/DataFinal/SmartphonesProductDataFinal.csv'
    FINAL_DATA_SET_COLS = ['Name', 'Price', 'Currency', 'MatchingID']
    TRAINED_CRF_MODEL_PATH = './out/crf.model'
    STRUCTURED_DATA_SET_OUTPUT_PATH = './out/StructuredSmartPhonesDataset.csv'

    df = pd.read_csv(FINAL_DATA_SET_PATH, usecols=FINAL_DATA_SET_COLS)

    # Get products only with prices in EUROS
    df = df.loc[df['Currency'] == 'EUR']

    product_titles = df['Name'].astype(str).values.tolist()
    product_prices = df['Price'].astype(float).values.tolist()
    product_matching_codes = df['MatchingID'].astype(str).values.tolist()

    # Start structured data set building
    structuredDataSetBuilder = StructuredDataSetBuilder(TRAINED_CRF_MODEL_PATH,
                                                        product_titles,
                                                        product_prices, product_matching_codes, limit=50000)

    print("\nSummary:")

    structuredDataSetBuilder.print_builder_summary()

    start_time = time.time()
    structuredDataSetBuilder.start()
    elapsed_time = round(time.time() - start_time, 3)

    print("\nStructured data set building finished. Elapsed time (s): {}".format(elapsed_time))
    print("\nSummary:")

    structuredDataSetBuilder.print_structured_data_set_summary()

    print()

    structuredDataSetBuilder.export_data_to_csv(STRUCTURED_DATA_SET_OUTPUT_PATH)

    print("Structured data set exported to file.")

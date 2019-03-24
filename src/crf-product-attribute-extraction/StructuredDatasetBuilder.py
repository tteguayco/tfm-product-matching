import pandas as pd
import pycrfsuite
import os

FINAL_DATASET_PATH = '../../RawData/DataFinal/SmartphonesProductDataFinal.csv'
TRAINED_CRF_MODEL_PATH = './crf.model'
STRUCTURED_DATASET_OUTPUT_PATH = './out/StructuredSmartPhonesDataset.csv'

class StructuredDatasetBuilder:

    def __init__(self, crf_model_path, titles, prices, matching_codes):
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(crf_model_path)

        self.titles = titles
        self.prices = prices
        self.matching_codes = matching_codes

        self.structured_dataset = None

        if len(self.titles) != len(self.prices) or len(self.titles) != len(self.matching_codes):
            raise ValueError('Provided lists of titles, prices and matching codes do not have the same length')

    def start(self):

        col_names = ['Brand', 'Model', 'Price', 'MatchingCode']
        self.structured_dataset = pd.DataFrame(columns=col_names)

        for i, title in enumerate(self.titles):
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

            # Add instance to the dataset
            self.structured_dataset.loc[len(self.structured_dataset)] = [brand, model, price, matching_code]

    def export_dataset_to_csv(self):
        if self.structured_dataset is not None:
            os.makedirs(os.path.dirname(STRUCTURED_DATASET_OUTPUT_PATH), exist_ok=True)
            self.structured_dataset.to_csv(STRUCTURED_DATASET_OUTPUT_PATH, sep=',', encoding='utf-8', index=False)


if __name__ == '__main__':

    df = pd.read_csv(FINAL_DATASET_PATH, nrows=1000)

    # Get products only with prices in EUROS
    df = df.loc[df['Currency'] == 'EUR']

    titles = df['Name'].astype(str).values.tolist()
    prices = df['Price'].astype(float).values.tolist()
    matching_codes = df['MatchingID'].astype(str).values.tolist()

    # Start structured dataset building
    structuredDatasetBuilder = StructuredDatasetBuilder(TRAINED_CRF_MODEL_PATH, titles, prices, matching_codes)
    structuredDatasetBuilder.start()
    structuredDatasetBuilder.export_dataset_to_csv()

import pandas as pd


class BIOTagger:

    SMARTPHONES_PRODUCT_DATA_FINAL_PATH = "../../RawData/DataFinal/SmartphonesProductDataFinal.csv"

    def __init__(self):
        self.encoded_titles = []
        self.brands_list = []
        self.color_list = []

        self.smartphones_dataset = pd.read_csv(BIOTagger.SMARTPHONES_PRODUCT_DATA_FINAL_PATH)
        self.brands_list = self.smartphones_dataset['BrandName'].tolist()

        self.preprocess_brands()

    def preprocess_brands(self):
        self.brands_list = list(set(self.brands_list))
        self.brands_list = [brand for brand in self.brands_list if str(brand) != 'nan']

    def tag_titles(self):
        pass


bio_tagger = BIOTagger()

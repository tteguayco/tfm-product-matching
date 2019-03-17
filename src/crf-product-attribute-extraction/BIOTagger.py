import pandas as pd


class BIOTagger:

    SMARTPHONES_PRODUCT_DATA_FINAL_PATH = "../../RawData/DataFinal/SmartphonesProductDataFinal.csv"

    def __init__(self):
        self.encoded_titles = []
        self.brands_list = []
        self.colors_list = []

        self.smartphones_dataset = pd.read_csv(BIOTagger.SMARTPHONES_PRODUCT_DATA_FINAL_PATH)
        self.brands_list = self.smartphones_dataset['BrandName'].tolist()
        self.colors_list = self.smartphones_dataset['Color'].tolist()

        self.preprocess_brands()
        self.preprocess_colors()

    def preprocess_brands(self):
        self.brands_list = [brand for brand in self.brands_list if str(brand) != 'nan']
        self.brands_list = list(set(self.brands_list))

    def preprocess_colors(self):
        self.colors_list = [color for color in self.colors_list if str(color) != 'nan']
        self.colors_list = [color.lower() for color in self.colors_list]
        self.colors_list = [color.replace('farbe', '') for color in self.colors_list]
        self.colors_list = list(set(self.colors_list))

    def tag_titles(self):
        pass


bio_tagger = BIOTagger()
print(bio_tagger.colors_list)

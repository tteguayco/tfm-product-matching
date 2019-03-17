import pandas as pd


class BIOTagger:

    SMARTPHONES_PRODUCT_DATA_FINAL_PATH = "../../RawData/DataFinal/SmartphonesProductDataFinal.csv"

    def __init__(self):
        self.encoded_titles = []
        self.brands_list = []
        self.colors_list = []

        self.smartphones_dataset = pd.read_csv(BIOTagger.SMARTPHONES_PRODUCT_DATA_FINAL_PATH)
        self.products_titles = self.smartphones_dataset['Name'].astype(str).values.tolist()
        self.brands_list = self.smartphones_dataset['BrandName'].astype(str).values.tolist()
        self.colors_list = self.smartphones_dataset['Color'].astype(str).values.tolist()

        self.preprocess_titles()
        self.preprocess_brands()
        self.preprocess_colors()

    def preprocess_titles(self):
        # TODO remove punctuation
        self.products_titles = [title.lower() for title in self.products_titles]

    def preprocess_brands(self):
        self.brands_list = [brand.lower() for brand in self.brands_list]
        self.brands_list = [brand for brand in self.brands_list if str(brand) != 'nan']
        self.brands_list = list(set(self.brands_list))

    def preprocess_colors(self):
        self.colors_list = [color for color in self.colors_list if str(color) != 'nan']
        self.colors_list = [color.lower() for color in self.colors_list]
        self.colors_list = [color.replace('farbe', '') for color in self.colors_list]
        self.colors_list = list(set(self.colors_list))

    def tag_titles(self):
        for title in self.products_titles:
            encoded_title = {}
            splitted_title = title.split()

            for word in splitted_title:
                # Tag brands

                # Tag colors
                if word in self.colors_list:
                    encoded_title[word] = 'B-COLOR'

                else:
                    encoded_title[word] = 'O'

            self.encoded_titles.append(encoded_title)

bio_tagger = BIOTagger()
bio_tagger.tag_titles()
for encoded_title in bio_tagger.encoded_titles:
    print(encoded_title)

import pandas as pd
import time


class SmartPhoneBIOTagger:

    SMARTPHONES_FINAL_DATASET_PATH = "../../RawData/DataFinal/SmartphonesProductDataFinal.csv"
    SMARTPHONES_GSMARENA_DATASET_PATH = "../../RawData/GSMArenaPhoneDataset/phone_dataset.csv"

    def __init__(self):
        self.titles_features = []
        self.titles_labels = []

        self.brands_list = []
        self.colors_list = []
        self.models_list = []

        self.smartphones_final_dataset = pd.read_csv(SmartPhoneBIOTagger.SMARTPHONES_FINAL_DATASET_PATH, nrows=1000)
        self.smartphones_gsmarena_dataset = pd.read_csv(SmartPhoneBIOTagger.SMARTPHONES_GSMARENA_DATASET_PATH)

        self.products_titles = self.smartphones_final_dataset['Name'].astype(str).values.tolist()
        self.brands_list = self.smartphones_final_dataset['BrandName'].astype(str).values.tolist()
        self.colors_list = self.smartphones_final_dataset['Color'].astype(str).values.tolist()

        self.models_list = self.smartphones_gsmarena_dataset['model'].astype(str).values.tolist()

        self.preprocess_titles()
        self.preprocess_brands()
        self.preprocess_colors()
        self.preprocess_models()

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
        self.colors_list = [color.strip() for color in self.colors_list]
        self.colors_list = list(set(self.colors_list))

    def preprocess_models(self):
        self.models_list = [model.lower() for model in self.models_list]

        # Descending order based on the number of words in model
        self.models_list.sort(key=lambda model: len(model.split()), reverse=True)

    def tag_titles(self):
        for title in self.products_titles:
            title_features = []
            title_labels = []

            splitted_title = title.split()

            # Initialize features and labels
            for i, word in enumerate(splitted_title):
                title_features.append(word)
                title_labels.append('O')

            # Tag brands
            # for i, brand in enumerate(self.brands_list):
            #     if brand in title:
            #         splitted_brand = brand.split()
            #         if len(splitted_brand) == 0:
            #             for j, word in enumerate(splitted_title):
            #                 if splitted_brand[0] == encoded_title[j]:
            #                     encoded_title[j] = (word, 'B-BRAND')
            #         else:
            #             for j, word in enumerate(splitted_title):
            #                 for k, brand_part in enumerate(splitted_brand):
            #                     if word == brand_part:
            #                         if k == 0:
            #                             encoded_title[j] = (word, 'B-BRAND')
            #                         else:
            #                             encoded_title[j] = (word, 'I-BRAND')

            # Tag colors
            # for i, word_title in enumerate(splitted_title):
            #     for j, color in enumerate(self.colors_list):
            #         if color in title:
            #             if color == word_title:
            #                 encoded_title[i] = (word_title, 'B-COLOR')

            # Tag models
            for model in self.models_list:

                # If the whole model name is contained in the product title
                if set(model.split()) <= set(title.split()):
                    splitted_model = model.split()
                    for i, model_part in enumerate(splitted_model):
                        tag2apply = 'B-MODEL' if i == 0 else 'I-MODEL'
                        for j, word_title in enumerate(splitted_title):
                            if model_part == word_title:
                                title_features[j] = word_title
                                title_labels[j] = tag2apply

                    # Only one model allowed for a single title
                    break

            self.titles_features.append(title_features)
            self.titles_labels.append(title_labels)

            print(self.titles_features[-1])
            print(self.titles_labels[-1])

if __name__ == "__main__":
    bio_tagger = SmartPhoneBIOTagger()

    start_time = time.time()
    bio_tagger.tag_titles()
    elapsed_time = time.time() - start_time

    print("Elapsed time of BIO Encoding: {}".format(elapsed_time))

    print(bio_tagger.titles_features[0])
    print(bio_tagger.titles_labels[0])

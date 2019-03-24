import pandas as pd
import time
import re


class SmartPhoneBIOTagger:

    def __init__(self, titles, colors, brands, models_by_brand):

        # Structures to BIO encode product titles
        self.title_features = []
        self.title_labels = []

        # Store data
        self.product_titles = titles
        self.product_colors = colors
        self.product_brands = brands
        self.product_models_by_brand = models_by_brand

        # Clean textual data
        self.preprocess_titles()
        self.preprocess_brands()
        self.preprocess_colors()
        self.preprocess_models()

    def common_preprocess(self, attr_list):
        # Lowercase words
        attr_list = [x.lower() for x in attr_list]

        # Remove punctuation
        attr_list = [re.sub(r'[^\w\s]', '', x) for x in attr_list]

        # Remove NULL values
        attr_list = [x for x in attr_list if str(x) != 'nan']

        # Remove duplicates
        attr_list = list(set(attr_list))

        # Trim surrounding spaces
        attr_list = [x.strip() for x in attr_list]

        # Remove sequential spaces
        attr_list = [re.sub(r'\s{2,}', ' ', x) for x in attr_list]

        return attr_list

    def preprocess_titles(self):
        self.product_titles = self.common_preprocess(self.product_titles)

    def preprocess_brands(self):
        self.product_brands = self.common_preprocess(self.product_brands)

    def preprocess_colors(self):
        self.product_colors = self.common_preprocess(self.product_colors)
        self.product_colors = [color.replace('farbe', '') for color in self.product_colors]

    def preprocess_models(self):

        # Descending order the models for a given brand based on the number of words the model has
        # This will avoid to wrongly match the model as 'Liquid Z6' when it is 'Liquid Z6 Plus',
        # as the models list is inspected sequentially (longer models are matched first)
        for brand, models_list in self.product_models_by_brand.items():
            models_list.sort(key=lambda model: len(model.split()), reverse=True)

    def title_contains_model(self, title, model):

        if set(model.split()) <= set(title.split()):
            indexes_list = []
            splitted_title = title.split()
            splitted_model = model.split()

            for word_model in splitted_model:
                indexes_list.append(splitted_title.index(word_model))

            # Check if all the collected indexes are consecutive
            if (len(splitted_model) == len(indexes_list) and
                len(set(indexes_list)) == len(indexes_list) and
                    sorted(indexes_list) == indexes_list):
                first_index = indexes_list[0]
                last_index = indexes_list[-1]
                if (last_index - first_index) == len(indexes_list) - 1:
                    return True

        return False

    def tag_titles(self):

        for title in self.product_titles:
            title_features = []
            title_labels = []
            found_brand = ''

            splitted_title = title.split()

            # Initialize features and labels
            for word in splitted_title:
                title_features.append(word)
                title_labels.append('O')

            # Tag brands
            for i, brand in enumerate(self.product_brands):
                if brand in title:
                    splitted_brand = brand.split()
                    found_brand = brand
                    if len(splitted_brand) == 0:
                        for j, word in enumerate(splitted_title):
                            if splitted_brand[0] == title_features[j]:
                                title_features[j] = word
                                title_labels[j] = 'B-BRAND'
                    else:
                        for j, word in enumerate(splitted_title):
                            for k, brand_part in enumerate(splitted_brand):
                                if word == brand_part:
                                    if k == 0:
                                        title_features[j] = word
                                        title_labels[j] = 'B-BRAND'
                                    else:
                                        title_features[j] = word
                                        title_labels[j] = 'I-BRAND'

            # Tag colors
            for i, word_title in enumerate(splitted_title):
                for j, color in enumerate(self.product_colors):
                    if color in title:
                        if color == word_title:
                            title_features[i] = word_title
                            title_labels[i] = 'B-COLOR'

            # Tag models
            if len(found_brand) > 0:

                models_for_found_brand = []
                if found_brand in self.product_models_by_brand:
                    models_for_found_brand = self.product_models_by_brand[found_brand]

                for model in models_for_found_brand:
                    if self.title_contains_model(title, model):
                        splitted_model = model.split()
                        for i, word_model in enumerate(splitted_model):
                            tag2apply = 'B-MODEL' if i == 0 else 'I-MODEL'
                            for j, word_title in enumerate(splitted_title):
                                if word_model == word_title:
                                    title_features[j] = word_title
                                    title_labels[j] = tag2apply

            self.title_features.append(title_features)
            self.title_labels.append(title_labels)

            print(self.title_features[-1])
            print(self.title_labels[-1])
            print()


def get_models_by_brand(df, brands):
    models_by_brand = {}

    for brand in brands:
        current_brand_models_list = df[df['brand'].str.lower() == brand.lower()]['model'].astype(str).values.tolist()
        current_brand_models_list = [x.lower() for x in current_brand_models_list]
        models_by_brand[brand.lower()] = current_brand_models_list

    return models_by_brand


if __name__ == "__main__":

    SMARTPHONES_FINAL_DATASET_PATH = "../../RawData/DataFinal/SmartphonesProductDataFinal.csv"
    SMARTPHONES_GSMARENA_DATASET_PATH = "../../RawData/GSMArenaPhoneDataset/phone_dataset.csv"

    # Get data
    final_product_data = pd.read_csv(SMARTPHONES_FINAL_DATASET_PATH, nrows=100)
    structured_product_data = pd.read_csv(SMARTPHONES_GSMARENA_DATASET_PATH)

    product_titles = final_product_data['Name'].astype(str).values.tolist()
    product_colors = final_product_data['Color'].astype(str).values.tolist()

    product_brands = structured_product_data['brand'].astype(str).values.tolist()
    product_models_by_brand = get_models_by_brand(structured_product_data, product_brands)

    # Start BIO encoding
    bio_tagger = SmartPhoneBIOTagger(product_titles, product_colors, product_brands, product_models_by_brand)

    print("BIOTagger object created.")
    print("Starting BIO encoding...")

    start_time = time.time()
    bio_tagger.tag_titles()
    elapsed_time = time.time() - start_time

    print("BIO encoded finished. Elapsed time: {}".format(elapsed_time))


    print(bio_tagger.title_contains_model("ksd asnd liquid z6 Plus akjdasad", "liquid z6 plus"))
    print(bio_tagger.product_models_by_brand)
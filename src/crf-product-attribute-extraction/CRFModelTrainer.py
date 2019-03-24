import pycrfsuite
import re

BIO_ENCODED_PRODUCT_TITLES_FILE = "./out/encoded_titles.txt"


def get_training_set_from_file(file_path):
    training_set = []

    with(open(file_path, 'r')) as f:
        for line in f:
            product_title = []
            features_list = []
            labels_list = []

            splitted_line = line.split(';')
            features_line = splitted_line[0]
            labels_line = splitted_line[1]

            pattern = re.compile(r'\'([\w-]+)\'')

            for feature in re.findall(pattern, features_line):
                features_list.append(feature)

            for label in re.findall(pattern, labels_line):
                labels_list.append(label)

            product_title.append(features_list)
            product_title.append(labels_list)
            training_set.append(product_title)

    return training_set


training_set = get_training_set_from_file(BIO_ENCODED_PRODUCT_TITLES_FILE)

trainer = pycrfsuite.Trainer(verbose=True)

for encoded_title in training_set:
    print(encoded_title[0])
    print(encoded_title[1])
    trainer.append(encoded_title[0], encoded_title[1])

trainer.set_params({
    'c1': 0.1,
    'c2': 0.01,
    'max_iterations': 200,
    'feature.possible_transitions': True
})

trainer.train('crf.model')

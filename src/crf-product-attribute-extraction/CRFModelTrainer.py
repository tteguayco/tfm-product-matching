import pycrfsuite
import time
import re

BIO_ENCODED_PRODUCT_TITLES_FILE = './out/encoded_titles.txt'
CRF_MODEL_OUTPUT_FILE = './out/crf.model'
VERBOSE_MODE = True


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

if VERBOSE_MODE:
    print("Number of rows in training data set: {}".format(len(training_set)))

trainer = pycrfsuite.Trainer(verbose=VERBOSE_MODE)

for encoded_title in training_set:
    trainer.append(encoded_title[0], encoded_title[1])

trainer.set_params({
    'c1': 0.1,
    'c2': 0.01,
    'max_iterations': 200,
    'feature.possible_transitions': True
})

start_time = time.time()
trainer.train(CRF_MODEL_OUTPUT_FILE)
elapsed_time = round(time.time() - start_time, 3)

if VERBOSE_MODE:
    print("CRF model training finished. Elapsed time (s): {}".format(elapsed_time))

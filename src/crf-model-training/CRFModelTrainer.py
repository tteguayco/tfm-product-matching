import pandas as pd
import time

from sklearn import model_selection
from joblib import dump
from sklearn_crfsuite import metrics
import sklearn_crfsuite

#import pycrfsuite <--- include in the memory this was tested but discarded

BIO_ENCODED_PRODUCT_TITLES_PATHFILE = "./out/data/bio_titles.csv"
CRF_MODEL_OUTPUT_FILE = "./out/models/crf.joblib"
VERBOSE_MODE = True


def get_bio_encoded_titles(file_path):
    '''
    Returns the features for the product titles (i.e. the words) as a list of 
    lists of strings and the labels for these features as a list of lists of strings.
    '''
    features = []
    labels = []
    classes = []

    bio_titles_df = pd.read_csv(BIO_ENCODED_PRODUCT_TITLES_PATHFILE, encoding='iso-8859-1')
    classes = bio_titles_df["BIOTag"].unique()

    for titleNum in bio_titles_df["TitleNumber"].unique():
        title_features = bio_titles_df.loc[bio_titles_df["TitleNumber"] == titleNum, "Word"].tolist()
        title_labels = bio_titles_df.loc[bio_titles_df["TitleNumber"] == titleNum, "BIOTag"].tolist()

        features.append(title_features)
        labels.append(title_labels)

    return features, labels, classes


if __name__ == "__main__":

    print("Reading BIO encoded product titles")

    start_time = time.time()
    bio_encoded_titles = get_bio_encoded_titles(BIO_ENCODED_PRODUCT_TITLES_PATHFILE)
    elapsed_time = round(time.time() - start_time, 3)

    print("Elapsed time (s): {}".format(elapsed_time))
    print("Number of BIO encoded titles collected: {}\n".format(len(bio_encoded_titles[0])))

    features = bio_encoded_titles[0]
    labels = bio_encoded_titles[1]
    classes = bio_encoded_titles[2]

    if len(features) != len(labels):
        raise ValueError("Lengths of features and labels are not the same: "
                         "features ({}), labels ({})".format(len(features), len(labels)))

    X_train, X_test, y_train, y_test = model_selection.train_test_split(features, 
                                                        labels,
                                                        test_size=0.30,
                                                        random_state=0)

    print("Training CRF model")

    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.01,
        max_iterations=200,
        all_possible_transitions=True
    )

    start_time = time.time()
    crf.fit(X_train, y_train)
    elapsed_time = round(time.time() - start_time, 3)

    print("Elapsed time (s): {}".format(elapsed_time))

    y_pred = crf.predict(X_test)

    print(metrics.flat_classification_report(y_test, y_pred, labels = classes))

    # Save CRF model
    dump(crf, CRF_MODEL_OUTPUT_FILE)

from flask_restful import Resource, reqparse
import joblib
import sys

sys.path.append('../common')
import crf_utils

CRF_MODEL_PATH = "../_models/crf_smartphones.joblib"

crf_model = joblib.load(CRF_MODEL_PATH)
parser = reqparse.RequestParser()
parser.add_argument("title")

class PredictProductFeaturesFromTitle(Resource):

    def get(self):
        args = parser.parse_args()
        product_title = args["title"]
        output = {}

        if product_title is not None:

            # Predict the labels on product title
            splitted_title = product_title.split()
            title_featured = crf_utils.title2features(splitted_title)
            pred_labels = crf_model.predict_single(title_featured)

            # Create JSON object for the response
            output = {'labels': pred_labels}

        return output

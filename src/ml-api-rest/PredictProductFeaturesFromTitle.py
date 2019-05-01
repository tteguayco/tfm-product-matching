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
            probs = crf_model.predict_marginals_single(title_featured)
            
            for prob_dict in probs:
                for key in prob_dict:
                    prob_dict[key] = round(prob_dict[key] * 100, 2)
            
            features = []
            
            if len(splitted_title) == len(pred_labels) and len(splitted_title) == len(probs):
                for i, word in enumerate(splitted_title):
                    features.append((word, pred_labels[i], {"confidence": probs[i]}))

            # Create JSON object for the response
            output = {
                'features': features
            }

        return output

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from PredictProductFeaturesFromTitle import PredictProductFeaturesFromTitle

app = Flask(__name__)
api = Api(app)

api.add_resource(PredictProductFeaturesFromTitle, "/predictFeaturesFromTitle")

if __name__ == '__main__':
    app.run(debug=True)

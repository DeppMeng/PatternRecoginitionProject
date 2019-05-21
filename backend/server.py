from flask import Flask, request, jsonify
import json
from classifier import Classifier
import numpy as np

app = Flask(__name__)
classifier = Classifier() # To confirm: global variable should be defined here?

def unpack(package):
    '''
    # For example:
    package = [{"x": 0.084248461548879, "y": 0.4889971262375139, "label": 0.0},
               {"x": -0.085910405756836283, "y": 2.9155646782084554, "label": 1.0},
               {"x": -2.1217101421337463, "y": -1.22781866628299, "label": 0.0},
               {"x": 1.0532482381992037, "y": -0.20140028191871351, "label": 1.0}]
    '''
    points = []
    labels = []
    for i in range(len(package)):
        points.append([package[i]["x"], package[i]["y"]])
        labels.append(package[i]["label"])
    return np.array(points), np.array(labels, dtype=int)

def train(jsonpack):
    train_points, train_labels = unpack(jsonpack['traindata'])
    method = 'min_dis'
    # if jsonpack['method']:
    #     method = jsonpack['method']
    classifier.train(train_points, train_labels, method=method)
    result = {
        "train_accuracy": classifier.train_accuracy,
        "pred_labels": classifier.pred_labels.tolist()
    }
    return result

def test(jsonpack):
    test_points, test_labels = unpack(jsonpack['testdata'])
    classifier.test(test_points, test_labels)
    result = {
        "test_accuracy": classifier.test_accuracy,
        "pred_labels": classifier.pred_labels.tolist()
    }
    return result

def predict(jsonpack):
    pred_points, _ = unpack(jsonpack['testdata'])
    classifier.predict(pred_points)
    print(classifier.pred_labels)
    result = {
        "pred_labels": classifier.pred_labels.tolist()
    }
    return result

POST_FUNCS = {
    "Train": train,
    "Test": test,
    "Predict": predict
}


@app.route('/post', methods=['POST'])
def post():

    jsonpack = request.json

    rtype = jsonpack['request_type']

    if rtype in POST_FUNCS:
        return jsonify(POST_FUNCS[rtype](jsonpack))
    return jsonify('')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)